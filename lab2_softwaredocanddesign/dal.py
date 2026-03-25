import csv
from abc import ABC, abstractmethod
from models import Employee

class IEmployeeRepository(ABC):
    @abstractmethod
    def save(self, employee: Employee):
        pass

class ICsvReader(ABC):
    @abstractmethod
    def read_file(self, filepath: str) -> list:
        pass

class SqlAlchemyEmployeeRepository(IEmployeeRepository):
    def __init__(self, session):
        self.session = session

    def save(self, employee: Employee):
        self.session.add(employee)
        self.session.commit()

class CsvFileReader(ICsvReader):
    def read_file(self, filepath: str) -> list:
        data = []
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data