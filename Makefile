install:
	poetry install --with test --no-interaction

lint:
	poetry run ruff check --fix .

format:
	poetry run ruff format

type-check:
	poetry run pyright

test:
	poetry run pytest -s -x -n auto --cov=food_co2_estimator --cov-report=term-missing --cov-fail-under=60

all: install lint format type-check test

