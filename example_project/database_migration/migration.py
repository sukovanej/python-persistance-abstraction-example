from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import Engine

from example_project.database.models import metadata


def _get_url_from_context(context: EnvironmentContext) -> str:
    url = context.config.get_main_option("sqlalchemy.url")

    if url is None:
        raise ValueError("sqlalchemy.url not set")

    return url


def run_migrations(context: EnvironmentContext) -> None:
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_from_engine(context: EnvironmentContext, engine: Engine) -> None:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        run_migrations(context)


def run_migrations_offline(context: EnvironmentContext) -> None:
    url = _get_url_from_context(context)
    context.configure(target_metadata=metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}, url=url)
    run_migrations(context)


def run_migrations_online(context: EnvironmentContext) -> None:
    url = _get_url_from_context(context)
    engine = create_engine(url, poolclass=pool.NullPool)
    run_migrations_from_engine(context, engine)
