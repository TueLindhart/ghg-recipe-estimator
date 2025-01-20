install:
	poetry install --with test --no-interaction

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format

type-check:
	poetry run pyright

test:
	poetry run pytest -s --cov=food_co2_estimator --cov-report=term-missing --cov-fail-under=80

all: install lint format type-check test

