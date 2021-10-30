.PHONY: mypy test clean isort black

all_dirs = example_project tests scripts alembic
all_type_checked_dirs = example_project scripts

run = poetry run
mypy_args = --strict

mypy:
	$(run) mypy $(mypy_args) $(all_type_checked_dirs)

test:
	$(run) pytest --cov=example_project tests

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
