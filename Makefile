.PHONY: mypy test clean isort black

all_dirs = decoupled_repositories_example tests scripts alembic
all_type_checked_dirs = decoupled_repositories_example scripts

run = poetry run
mypy_args = --strict

mypy:
	$(run) mypy $(mypy_args) $(all_type_checked_dirs)

test:
	$(run) pytest --cov=decoupled_repositories_example tests

isort:
	$(run) isort $(all_dirs)

black:
	$(run) black $(all_dirs)

format: black isort

lint:
	$(run) black --check $(all_dirs)
	$(run) isort --check $(all_dirs)
	$(run) mypy $(mypy_args) $(all_type_checked_dirs)

clean:
	find $(all_dirs) -name "__pycache__" | xargs rm -rf
	rm -rf .pytest_cache
	rm -rf .mypy_cache
