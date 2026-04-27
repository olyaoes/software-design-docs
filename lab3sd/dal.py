import csv
import json
from abc import ABC, abstractmethod
from models import Employee

class IEmployeeRepository(ABC):
    @abstractmethod
    def save(self, employee: Employee):
        pass

    @abstractmethod
    def get_all(self) -> list[Employee]:
        pass

    @abstractmethod
    def get_by_id(self, emp_id: int) -> Employee:
        pass

    @abstractmethod
    def update(self, employee: Employee):
        pass

    @abstractmethod
    def delete(self, emp_id: int):
        pass

class SqlAlchemyEmployeeRepository(IEmployeeRepository):
    def __init__(self, session):
        self.session = session

    def save(self, employee: Employee):
        self.session.add(employee)
        self.session.commit()

    def get_all(self) -> list[Employee]:
        return self.session.query(Employee).all()

    def get_by_id(self, emp_id: int) -> Employee:
        return self.session.query(Employee).filter(Employee.id == emp_id).first()

    def update(self, employee: Employee):
        self.session.commit()

    def delete(self, emp_id: int):
        emp = self.get_by_id(emp_id)
        if emp:
            self.session.delete(emp)
            self.session.commit()

class IFileReader(ABC):
    @abstractmethod
    def read_file(self, filepath: str) -> list:
        pass

class CsvFileReader(IFileReader):
    def read_file(self, filepath: str) -> list:
        data = []
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

class ExternalJsonReader:
    def extract_data(self, filepath: str) -> list:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

class JsonReaderAdapter(IFileReader):
    def __init__(self):
        self.legacy_reader = ExternalJsonReader()

    def read_file(self, filepath: str) -> list:
        return self.legacy_reader.extract_data(filepath)

class FileReaderFactory:
    @staticmethod
    def get_reader(filepath: str) -> IFileReader:
        if filepath.endswith('.csv'):
            return CsvFileReader()
        elif filepath.endswith('.json'):
            return JsonReaderAdapter()
        else:
            raise ValueError(f"Unsupported file format for: {filepath}")