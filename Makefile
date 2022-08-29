.PHONY: mypy test clean isort black

all_dirs = example_project tests entrypoints alembic
all_type_checked_dirs = example_project tests entrypoints

run = poetry run

mypy:
	$(run) mypy $(all_type_checked_dirs)

test:
	$(run) pytest --cov=example_project tests

test-ci:
	$(run) pytest --cache-clear --cov=example_project --cov-report=xml --cov-report=term tests

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

run-api:
	$(run) uvicorn entrypoints.api.app:app

run-api-reload:
	$(run) uvicorn entrypoints.api.app:app --reload

create-database:
	$(run) cli create-database
