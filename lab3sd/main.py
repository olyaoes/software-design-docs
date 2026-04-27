import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dal import SqlAlchemyEmployeeRepository, FileReaderFactory
from bll import OnboardingService
from presentation import OnboardingController

engine = create_engine('sqlite:///onboarding.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyEmployeeRepository(session)
factory = FileReaderFactory()

service = OnboardingService(repository=repository, reader_factory=factory)

controller = OnboardingController(service=service)

app = FastAPI(title="Employee MVC App with Patterns")
app.include_router(controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)