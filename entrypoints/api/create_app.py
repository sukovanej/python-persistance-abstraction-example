from typing import Any, Callable, Coroutine, cast

from fastapi import FastAPI, Response

from example_project.logic.user_logic import UserLogic

from .controller import UserController
from .models import AverageUserAgeResponse, StatusResponse, UserListResponse


def cast_router_func(func: Callable[..., Any]) -> Callable[..., Coroutine[Any, Any, Response]]:
    """FastAPI has incorrect typing for the func parameter in app.add_api_route, need to cast it unfortunately."""
    return cast(Callable[..., Coroutine[Any, Any, Response]], func)


def create_app(user_logic: UserLogic) -> FastAPI:
    user_controller = UserController(user_logic)

    app = FastAPI()

    app.add_api_route(
        "/user/add-random",
        cast_router_func(user_controller.add_random_user),
        response_model=StatusResponse,
        methods=["POST"],
    )
    app.add_api_route(
        "/user/list",
        cast_router_func(user_controller.list_all_users),
        response_model=UserListResponse,
        methods=["GET"],
    )
    app.add_api_route(
        "/user/average-age",
        cast_router_func(user_controller.get_average_user_age),
        response_model=AverageUserAgeResponse,
        methods=["GET"],
    )

    return app
