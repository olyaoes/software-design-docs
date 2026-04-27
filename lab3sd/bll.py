import random
from abc import ABC, abstractmethod
from models import Employee
from dal import IEmployeeRepository, FileReaderFactory

class EmployeeFactory:
    @staticmethod
    def create_employee(emp_type="developer") -> Employee:
        if emp_type == "developer":
            return Employee(
                first_name="Factory",
                last_name=f"Worker_{random.randint(1, 999)}",
                email="factory.dev@lviv.polytechnic.ua",
                position="Software Engineer",
                equipment_model="Factory-Build PC",
                system_account="FAC_SYS_X"
            )
        return Employee(first_name="Generic", last_name="Staff")

class ExternalCandidate:
    def __init__(self, full_name: str, contact_mail: str, job_role: str):
        self.full_name = full_name
        self.contact_mail = contact_mail
        self.job_role = job_role

class CandidateAdapter:
    @staticmethod
    def adapt(candidate: ExternalCandidate) -> Employee:
        names = candidate.full_name.split(" ", 1)
        first = names[0]
        last = names[1] if len(names) > 1 else "External"
        
        return Employee(
            first_name=first,
            last_name=last,
            email=candidate.contact_mail,
            position=candidate.job_role,
            equipment_model="Adapted Laptop",
            system_account=f"ADAPT_{random.randint(100, 999)}"
        )

class IOnboardingService(ABC):
    @abstractmethod
    def process_onboarding_data(self, filepath: str): pass
    @abstractmethod
    def get_all_employees(self) -> list[Employee]: pass
    @abstractmethod
    def get_employee(self, emp_id: int) -> Employee: pass
    @abstractmethod
    def create_employee(self, emp: Employee): pass
    @abstractmethod
    def update_employee(self, emp_id: int, updated_data: dict): pass
    @abstractmethod
    def delete_employee(self, emp_id: int): pass
    @abstractmethod
    def add_via_factory(self): pass
    @abstractmethod
    def add_via_adapter(self): pass

class OnboardingService(IOnboardingService):
    def __init__(self, repository: IEmployeeRepository, reader_factory: FileReaderFactory):
        self.repository = repository
        self.reader_factory = reader_factory

    def process_onboarding_data(self, filepath: str):
        reader = self.reader_factory.get_reader(filepath)
        raw_data = reader.read_file(filepath)
        for row in raw_data:
            emp = Employee(
                first_name=row.get("FirstName", ""),
                last_name=row.get("LastName", ""),
                email=row.get("Email", ""),
                position=row.get("Position", ""),
                equipment_model=row.get("EquipmentModel", ""),
                system_account=row.get("SystemAccount", "")
            )
            self.repository.save(emp)

    def get_all_employees(self) -> list[Employee]:
        return self.repository.get_all()

    def get_employee(self, emp_id: int) -> Employee:
        return self.repository.get_by_id(emp_id)

    def create_employee(self, emp: Employee):
        self.repository.save(emp)

    def update_employee(self, emp_id: int, updated_data: dict):
        emp = self.repository.get_by_id(emp_id)
        if emp:
            for key, value in updated_data.items():
                setattr(emp, key, value)
            self.repository.update(emp)

    def delete_employee(self, emp_id: int):
        self.repository.delete(emp_id)

    def add_via_factory(self):
        new_emp = EmployeeFactory.create_employee("developer")
        self.repository.save(new_emp)

    def add_via_adapter(self):
        external_person = ExternalCandidate(
            full_name="John Doe",
            contact_mail="john.doe@external.com",
            job_role="Senior Analyst"
        )
        adapted_emp = CandidateAdapter.adapt(external_person)
        self.repository.save(adapted_emp)