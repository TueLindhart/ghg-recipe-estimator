# Build stage 1
FROM python:3.13-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.2
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY app.py comparison_api.py start.sh  logging_config.yaml ./
COPY food_co2_estimator/ food_co2_estimator/

# Build stage 2
FROM python:3.13-slim-bookworm

WORKDIR /app
COPY --from=builder /app /app

# Install redis-server in the runtime image.
# Not best practice, but the usage is minimal.
RUN apt-get update && apt-get install -y --no-install-recommends redis-server && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

RUN chmod +x start.sh

CMD ["./start.sh"]
