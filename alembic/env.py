from alembic import context
from decoupled_repositories_example.database.migration import run_migrations_offline, run_migrations_online

if context.is_offline_mode():
    run_migrations_offline(context)
else:
    run_migrations_online(context)
