FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.3.2

WORKDIR /app

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock README.md ./
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "mkdocs", "serve", "--dev-addr=0.0.0.0:8080", "--no-livereload"]
