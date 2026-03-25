from abc import ABC, abstractmethod
from models import Employee
from dal import IEmployeeRepository, ICsvReader

class IOnboardingService(ABC):
    @abstractmethod
    def process_onboarding_data(self, filepath: str):
        pass

class OnboardingService(IOnboardingService):
    def __init__(self, repository: IEmployeeRepository, csv_reader: ICsvReader):
        self.repository = repository
        self.csv_reader = csv_reader

    def process_onboarding_data(self, filepath: str):
        print(f"Reading data from {filepath}...")
        raw_data = self.csv_reader.read_file(filepath)
        
        print("Saving data to the database...")
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
            
        print(f"Successfully saved {len(raw_data)} records to the database.")