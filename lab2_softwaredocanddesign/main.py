from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dal import SqlAlchemyEmployeeRepository, CsvFileReader
from bll import OnboardingService

def main():
    print("Configuring the database...")
    engine = create_engine('sqlite:///onboarding.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    repository = SqlAlchemyEmployeeRepository(session)
    reader = CsvFileReader()

    service = OnboardingService(repository=repository, csv_reader=reader)

    file_path = "onboarding_data.csv"
    service.process_onboarding_data(file_path)

if __name__ == "__main__":
    main()