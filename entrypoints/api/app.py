from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from example_project.database.repositories import DatabaseUserRepository
from example_project.logic import UserLogic

from .create_app import create_app


def create_user_logic() -> UserLogic:
    engine = create_engine("sqlite:///user_database.db")
    session = Session(engine)
    user_repository = DatabaseUserRepository(session)
    user_logic = UserLogic(user_repository)
    return user_logic


user_logic = create_user_logic()
app = create_app(user_logic)
