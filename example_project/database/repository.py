from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from example_project.repositories.models import User
from example_project.repositories.repository import UserRepository

from .models import users


class UserRepositorySql(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_user(self, name: str, age: int) -> None:
        stmt = insert(users).values(name=name, age=age)
        self._session.execute(stmt)
        self._session.commit()

    def get_all(self) -> Sequence[User]:
        stmt = select(User)
        all_rows = self._session.execute(stmt).all()
        return [row for (row,) in all_rows]

    def get_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)

        # TODO: one() is returning Any instead of User
        return self._session.execute(stmt).one()[0]  # type: ignore
