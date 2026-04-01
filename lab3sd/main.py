import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dal import SqlAlchemyEmployeeRepository, CsvFileReader
from bll import OnboardingService
from presentation import OnboardingController

# 1. Database Setup
engine = create_engine('sqlite:///onboarding.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 2. DAL
repository = SqlAlchemyEmployeeRepository(session)
reader = CsvFileReader()

# 3. BLL
service = OnboardingService(repository=repository, csv_reader=reader)

# 4. Presentation (Controller)
controller = OnboardingController(service=service)

# 5. App Setup
app = FastAPI(title="Employee MVC App")
app.include_router(controller.router)

if __name__ == "__main__":
    print("Starting Web Server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)