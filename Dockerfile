
FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main

COPY . /code

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
