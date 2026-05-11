# Training App

Telegram-бот для відстеження тренувань і прогресії навантаження.

## Стек

- Python 3.12 + uv
- aiogram 3.x (Telegram бот)
- FastAPI (health + майбутній API)
- PostgreSQL + SQLAlchemy async + alembic
- Docker + docker-compose

## Локальний запуск

```bash
# Залежності
uv sync

# Скопіювати env
cp .env.example .env

# Підняти базу
make db-up

# Накатити міграції
make db-migrate

# Запустити бот
make bot

# Запустити API (опціонально)
make run
```

## Корисні команди

```bash
make lint          # ruff check
make format        # ruff format
make test          # pytest
make db-up         # postgres у docker
make db-down       # зупинити postgres
make db-migrate    # alembic upgrade head
make db-revision msg="name"  # нова міграція
make db-seed       # заповнити базу вправами
```

## Структура

```
app/        FastAPI (health endpoint)
bot/        aiogram бот — хендлери, FSM, клавіатури
db/         SQLAlchemy сесія + alembic міграції
models/     ORM моделі
services/   бізнес логіка
seeds/      початкові дані (вправи)
tests/      тести
docker/     Dockerfile + docker-compose
```
