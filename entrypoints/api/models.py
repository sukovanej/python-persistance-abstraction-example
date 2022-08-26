from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel

from example_project.models.user import User


class StatusResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    @classmethod
    def from_user(cls, user: User) -> UserResponse:
        return cls(id=user.id, name=user.name, age=user.age)


class UserListResponse(BaseModel):
    users: Sequence[UserResponse]

    @classmethod
    def from_users(cls, users: Sequence[User]) -> UserListResponse:
        user_responses = [UserResponse.from_user(user) for user in users]
        return UserListResponse(users=user_responses)


class AverageUserAgeResponse(BaseModel):
    average_age: float
