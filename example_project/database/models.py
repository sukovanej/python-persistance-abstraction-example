from sqlalchemy import Column, Integer, MetaData, Table, Text
from sqlalchemy.orm import registry

from example_project.repositories.models import User

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text),
    Column("age", Integer, nullable=False),
)

mapper_registry = registry()

mapper_registry.map_imperatively(User, users)
