import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic.config import Config
from alembic.environment import EnvironmentContext
from alembic.runtime.migration import RevisionStep
from alembic.script import ScriptDirectory
from example_project.database.migration import run_migrations_from_engine
from example_project.database.repository import UserRepositorySql
from example_project.repositories.repository import UserRepository

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


def run_alembic_migrations(engine) -> None:
    config = Config()
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", IN_MEMORY_DATABASE_URL)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev: str, _: EnvironmentContext) -> list[RevisionStep]:
        return script._upgrade_revs("head", rev)

    with EnvironmentContext(config, script, fn=upgrade) as context:
        run_migrations_from_engine(context, engine)


@pytest.fixture(scope="session")
def in_memory_sqlalchemy_session() -> Session:
    engine = create_engine(IN_MEMORY_DATABASE_URL)
    run_alembic_migrations(engine)
    session = Session(engine)
    return session


@pytest.fixture
def user_repository(in_memory_sqlalchemy_session: Session) -> UserRepository:
    return UserRepositorySql(in_memory_sqlalchemy_session)


def test_test_user_repository(user_repository: UserRepository) -> None:
    user_repository.create_user("milan", 25)

    all_users = user_repository.get_all()
    assert len(all_users) == 1

    user_by_id = user_repository.get_by_id(all_users[0].id)
    assert user_by_id.name == "milan"
    assert user_by_id.age == 25
