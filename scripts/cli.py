import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from decoupled_repositories_example.database.models import metadata
from decoupled_repositories_example.database.repository import UserRepositorySql
from decoupled_repositories_example.logic import UserLogic
from decoupled_repositories_example.repositories.models import User


def create_user_logic() -> UserLogic:
    engine = create_engine("sqlite:///user_database.db")
    session = Session(engine)
    user_repository = UserRepositorySql(session)
    user_logic = UserLogic(user_repository)
    return user_logic


def view_user(user: User) -> str:
    return f"{user.name}, age: {user.age}"


def main() -> None:
    if len(sys.argv) == 1:
        print("Available commands:\n - add-random-user\n - create-database\n - get-average-user-age")
        exit(0)

    command = sys.argv[1]
    user_logic = create_user_logic()

    if command == "add-random-user":
        user_logic.add_random_user()
        print("Done")
    elif command == "list-all-users":
        print(" - " + "\n - ".join([view_user(user) for user in user_logic.list_all_users()]))
    elif command == "get-average-user-age":
        print(round(user_logic.get_average_user_age(), 2))
    elif command == "create-database":
        metadata.create_all(create_engine("sqlite:///user_database.db"))
        print("Done")
