[![codecov](https://codecov.io/gh/sukovanej/python-persistence-abstraction-example/branch/master/graph/badge.svg?token=UH98O0UVCM)](https://codecov.io/gh/sukovanej/python-persistence-abstraction-example)

# Python architecture example with abstracted persistance layer

This repository contains a working Python codebase showing how to invert dependencies between
database module and the logic.

## What I want to achieve

 - the most important logic testable independently of the database
 - no cycles in the class diagram, single direction of dependencies
 - strict type check-ing for the whole codebase
 - tests working out of the box (no setup needed for triggering tests) with 100% test coverage

## Class design

![class diagram](assets/class-diagram.png)

## Technical details

### Mapping SQLAlchemy tables onto existing classes

Models are created indepdently of the SQLAlchemy and in the database module they are
mapped onto table definitions.

```python
from dataclasses import dataclass

from sqlalchemy import Column, Integer, MetaData, Table, Text
from sqlalchemy.orm import registry


metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text),
    Column("age", Integer, nullable=False),
)

mapper_registry = registry()


@dataclass
class User:
    id: int
    name: str
    age: int


mapper_registry.map_imperatively(User, users)
```

## Note on the repository pattern

The definition by Martin Fowler says that a repository is a collection-like interface for accessing domain objects.
Therefore when using this defition my repositories are not really repositories because they are not collection-like. On
the other side they work as a mediator between the data-mapping layer and the domain objects layer. So, what I call
a repository in this project is probably not a repository in the original sense but it does a similar job. The primary
goal is to create an abstract mediator that enables us to test and build the domain and infrastructure layer independently.

Something to read:

 - https://martinfowler.com/eaaCatalog/repository.html
 - https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design

### Database repositories testing

 - SQLite (SAVEPOINT)[https://www.sqlite.org/lang_savepoint.html]
 - TODO: test db module using nested transactions

## Static analysis and tests

 - **black** - 120 line-length
 - **isort** with black profile
 - **mypy** using the *strict* mode
 - **pytest** with *pytest-cov* for test-coverage
