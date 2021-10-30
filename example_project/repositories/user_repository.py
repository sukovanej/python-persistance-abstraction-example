from abc import ABC, abstractmethod
from typing import Sequence

from example_project.models import User


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, name: str, age: int) -> None:
        ...

    @abstractmethod
    def get_all(self) -> Sequence[User]:
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        ...
