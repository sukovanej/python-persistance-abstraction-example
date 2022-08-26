from example_project.logic.user_logic import UserLogic

from .models import AverageUserAgeResponse, StatusResponse, UserListResponse


class UserController:
    def __init__(self, user_logic: UserLogic) -> None:
        self._user_logic = user_logic

    def add_random_user(self) -> StatusResponse:
        self._user_logic.add_random_user()
        return StatusResponse(message="random user added")

    def list_all_users(self) -> UserListResponse:
        users = self._user_logic.list_all_users()
        return UserListResponse.from_users(users)

    def get_average_user_age(self) -> AverageUserAgeResponse:
        average_age = self._user_logic.get_average_user_age()
        average_age_rounded = round(average_age, 2)
        return AverageUserAgeResponse(average_age=average_age_rounded)
