# Базовый образ с Python 3.12 (минимальный slim)
FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2

# ── Установка Poetry ───────────────────────────────────────────────────
RUN pip install "poetry==$POETRY_VERSION"

# ── Устанавливаем зависимости по pyproject.toml отдельно,
#    чтобы кэшировать слой при изменении кода ───────────────────────────
WORKDIR /code
COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main

# ── Копируем исходники ─────────────────────────────────────────────────
COPY . /code

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
