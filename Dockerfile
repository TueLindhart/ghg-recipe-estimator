FROM python:3.13-slim

# Install required tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# Setup working directory
WORKDIR /app

# Add poetry config
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev,test --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY app.py comparison_api.py start.sh ./
COPY food_co2_estimator/ food_co2_estimator/

EXPOSE 8080

CMD ["poetry", "run", "bash", "./start.sh"]
