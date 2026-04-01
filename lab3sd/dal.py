import csv
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

class CsvFileReader(ICsvReader):
    def read_file(self, filepath: str) -> list:
        data = []
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data