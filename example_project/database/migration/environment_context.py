from typing import Any, Optional, Protocol, overload


class Config(Protocol):
    @overload
    def get_main_option(self, value: str) -> Optional[str]:
        ...

    @overload
    def get_main_option(self, value: str, default: str) -> str:
        ...


class EnvironmentContext(Protocol):
    config: Config

    def begin_transaction(self) -> Any:
        ...

    def run_migrations(self) -> None:
        ...

    def configure(self, **kwargs: Any) -> None:
        ...
