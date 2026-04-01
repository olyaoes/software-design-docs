from abc import ABC, abstractmethod
from models import Employee
from dal import IEmployeeRepository, ICsvReader

class IOnboardingService(ABC):
    @abstractmethod
    def process_onboarding_data(self, filepath: str):
        pass
    
    @abstractmethod
    def get_all_employees(self) -> list[Employee]:
        pass

    @abstractmethod
    def get_employee(self, emp_id: int) -> Employee:
        pass

    @abstractmethod
    def create_employee(self, emp: Employee):
        pass

    @abstractmethod
    def update_employee(self, emp_id: int, updated_data: dict):
        pass

    @abstractmethod
    def delete_employee(self, emp_id: int):
        pass

class OnboardingService(IOnboardingService):
    def __init__(self, repository: IEmployeeRepository, csv_reader: ICsvReader):
        self.repository = repository
        self.csv_reader = csv_reader

    def process_onboarding_data(self, filepath: str):
        raw_data = self.csv_reader.read_file(filepath)
        for row in raw_data:
            emp = Employee(
                first_name=row["FirstName"],
                last_name=row["LastName"],
                email=row["Email"],
                position=row["Position"],
                equipment_model=row["EquipmentModel"],
                system_account=row["SystemAccount"]
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
            emp.first_name = updated_data.get("first_name", emp.first_name)
            emp.last_name = updated_data.get("last_name", emp.last_name)
            emp.email = updated_data.get("email", emp.email)
            emp.position = updated_data.get("position", emp.position)
            emp.equipment_model = updated_data.get("equipment_model", emp.equipment_model)
            emp.system_account = updated_data.get("system_account", emp.system_account)
            self.repository.update(emp)

    def delete_employee(self, emp_id: int):
        self.repository.delete(emp_id)