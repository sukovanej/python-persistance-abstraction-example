from typing import Sequence

import pytest

from example_project.logic.user_logic import UserLogic
from example_project.repositories.models import User
from example_project.repositories.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data: list[User] = []

    def create_user(self, name: str, age: int) -> None:
        new_id = len(self._data) + 1
        self._data.append(User(id=new_id, name=name, age=age))

    def get_all(self) -> Sequence[User]:
        return self._data

    def get_by_id(self, user_id: int) -> User:
        return next(user for user in self._data if user.id == user_id)


@pytest.fixture
def user_repository() -> UserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def user_logic(user_repository: UserRepository) -> UserLogic:
    return UserLogic(user_repository)


@pytest.mark.parametrize(
    "ages, expected_average_age",
    [
        ([1, 2, 3], 2),
        ([10, 20, 30], 20),
        ([10, 20, 30, 40], 25),
        ([5, 6], 5.5),
    ],
)
def test_get_average_user_age(
    user_repository: UserRepository,
    user_logic: UserLogic,
    ages: list[int],
    expected_average_age: float,
) -> None:
    for age in ages:
        user_repository.create_user("name-doesnt-matter", age)

    assert user_logic.get_average_user_age() == expected_average_age


def test_add_random_user(user_logic: UserLogic) -> None:
    user_logic.add_random_user()
    all_users = user_logic.list_all_users()
    assert len(all_users) == 1

    user = all_users[0]
    assert 0 < user.age < 100
