from typing import Iterator
import pytest
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import RevisionStep
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from example_project.database.repositories import DatabaseUserRepository
from example_project.database_migration import run_migrations_from_engine
from example_project.repositories import UserRepository

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


def run_alembic_migrations(engine: Engine) -> None:
    config = Config()
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", IN_MEMORY_DATABASE_URL)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev: str, _: EnvironmentContext) -> list[RevisionStep]:
        return script._upgrade_revs("head", rev)

    with EnvironmentContext(config, script, fn=upgrade) as context:
        run_migrations_from_engine(context, engine)


@pytest.fixture(scope="session")
def in_memory_sqlalchemy_engine() -> Engine:
    return create_engine(IN_MEMORY_DATABASE_URL, echo=True)


@pytest.fixture(scope="session")
def in_memory_sqlalchemy_session(in_memory_sqlalchemy_engine: Engine) -> Session:
    run_alembic_migrations(in_memory_sqlalchemy_engine)
    return Session(in_memory_sqlalchemy_engine)


@pytest.fixture()
def safe_sqlalchemy_session(in_memory_sqlalchemy_session: Session, in_memory_sqlalchemy_engine: Engine) -> Iterator[Session]:
    # in_memory_sqlalchemy_engine.execute("SELECT * FROM users").all()
    in_memory_sqlalchemy_engine.execute("SAVEPOINT test_savepoint;")
    breakpoint()
    yield in_memory_sqlalchemy_session
    breakpoint()
    in_memory_sqlalchemy_engine.execute("RELEASE test_savepoint;")
    breakpoint()


@pytest.fixture
def user_repository(safe_sqlalchemy_session: Session) -> UserRepository:
    return DatabaseUserRepository(safe_sqlalchemy_session)


def test_user_repository(user_repository: UserRepository) -> None:
    user_repository.create_user("milan", 25)

    all_users = user_repository.get_all()
    assert len(all_users) == 1

    user_by_id = user_repository.get_by_id(all_users[0].id)
    assert user_by_id.name == "milan"
    assert user_by_id.age == 25


def test_user_repository_multiple_users(user_repository: UserRepository) -> None:
    user_repository.create_user("milan", 25)
    user_repository.create_user("prdel", 12)

    all_users = user_repository.get_all()
    assert len(all_users) == 2
