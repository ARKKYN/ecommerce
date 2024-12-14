FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN poetry install --no-interaction --no-ansi

RUN ENVIRONMENT=test poetry run coverage run --source=shop -m pytest -s

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "shop.app:app", "--host", "0.0.0.0", "--port", "8000"]
