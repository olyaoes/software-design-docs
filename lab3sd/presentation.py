import os
import shutil
from fastapi import APIRouter, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bll import IOnboardingService
from models import Employee

class OnboardingController:
    def __init__(self, service: IOnboardingService):
        self.service = service
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="templates")
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/", response_class=HTMLResponse)
        async def read_employees(request: Request):
            employees = self.service.get_all_employees()
            # Додано явне вказування request=request та name=...
            return self.templates.TemplateResponse(
                request=request, name="index.html", context={"request": request, "employees": employees}
            )

        @self.router.post("/upload-file/")
        async def upload_file(file: UploadFile = File(...)):
            if not file.filename.endswith('.csv'):
                raise HTTPException(status_code=400, detail="Only .csv files are allowed.")
            temp_file_path = f"temp_{file.filename}"
            try:
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                self.service.process_onboarding_data(temp_file_path)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            return RedirectResponse(url="/", status_code=303)

        @self.router.get("/create", response_class=HTMLResponse)
        async def create_form(request: Request):
            return self.templates.TemplateResponse(
                request=request, name="form.html", context={"request": request, "employee": None}
            )

        @self.router.post("/create")
        async def create_employee(
            first_name: str = Form(...), last_name: str = Form(...),
            email: str = Form(...), position: str = Form(...),
            equipment_model: str = Form(...), system_account: str = Form(...)
        ):
            emp = Employee(
                first_name=first_name, last_name=last_name, email=email,
                position=position, equipment_model=equipment_model, system_account=system_account
            )
            self.service.create_employee(emp)
            return RedirectResponse(url="/", status_code=303)

        @self.router.get("/edit/{emp_id}", response_class=HTMLResponse)
        async def edit_form(request: Request, emp_id: int):
            emp = self.service.get_employee(emp_id)
            return self.templates.TemplateResponse(
                request=request, name="form.html", context={"request": request, "employee": emp}
            )

        @self.router.post("/edit/{emp_id}")
        async def update_employee(
            emp_id: int, first_name: str = Form(...), last_name: str = Form(...),
            email: str = Form(...), position: str = Form(...),
            equipment_model: str = Form(...), system_account: str = Form(...)
        ):
            updated_data = {
                "first_name": first_name, "last_name": last_name, "email": email,
                "position": position, "equipment_model": equipment_model, "system_account": system_account
            }
            self.service.update_employee(emp_id, updated_data)
            return RedirectResponse(url="/", status_code=303)

        @self.router.get("/delete/{emp_id}")
        async def delete_employee(emp_id: int):
            self.service.delete_employee(emp_id)
            return RedirectResponse(url="/", status_code=303)