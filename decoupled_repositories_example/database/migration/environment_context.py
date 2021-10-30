from typing import Any, ContextManager, Optional, Protocol


class Config(Protocol):
    def get_main_option(self, value: str) -> Optional[str]:
        ...


class EnvironmentContext(Protocol):
    config: Config

    def begin_transaction(self) -> ContextManager[None]:
        ...

    def run_migrations(self) -> None:
        ...

    def configure(self, **kwargs: Any) -> None:
        ...
