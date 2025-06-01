# Arbitrage-Navigator 🏹

## Быстрый старт

```bash
# 1) клонируем репозиторий и создаём .env
cp .env.example .env

# 2) разработка локально
make dev       # poetry install + pre-commit + uvicorn в режиме hot-reload

# 3) полный стек (Postgres, Redis, RabbitMQ)
docker compose up --build

# 4) тесты
make tests
