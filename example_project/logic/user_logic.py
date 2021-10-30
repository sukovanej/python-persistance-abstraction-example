from random import randint
from typing import Sequence

from example_project.models import User
from example_project.repositories import UserRepository


class UserLogic:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_average_user_age(self) -> float:
        all_users = self._user_repository.get_all()
        all_ages = [user.age for user in all_users]
        return sum(all_ages) / len(all_ages)

    def add_random_user(self) -> None:
        random_name = "milan"  # :)
        random_age = randint(1, 100)
        self._user_repository.create_user(random_name, random_age)

    def list_all_users(self) -> Sequence[User]:
        return self._user_repository.get_all()
