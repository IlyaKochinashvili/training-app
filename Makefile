UV := uv

.PHONY: venv install run bot lint format-check format test build pre-commit-install health \
        db-up db-down db-logs db-migrate db-revision db-seed

venv:
	$(UV) venv

install:
	$(UV) sync

run:
	$(UV) run uvicorn app.main:app --reload

bot:
	$(UV) run python -m bot.main

lint:
	$(UV) run ruff check .

format-check:
	$(UV) run ruff format --check .

format:
	$(UV) run ruff format .

test:
	$(UV) run pytest

build:
	docker build -f docker/Dockerfile -t training-app .

pre-commit-install:
	$(UV) run pre-commit install

health:
	curl http://127.0.0.1:8000/health

db-up:
	docker compose -f docker/docker-compose.yml up db -d

db-down:
	docker compose -f docker/docker-compose.yml down

db-logs:
	docker compose -f docker/docker-compose.yml logs -f db

db-migrate:
	$(UV) run alembic upgrade head

db-revision:
	$(UV) run alembic revision --autogenerate -m "$(msg)"

db-seed:
	$(UV) run python -m seeds.run_seed
