# Backend Application (`app`)

This folder documents the FastAPI service defined in `app.py` along with its auxiliary files.

## Responsibilities
- Expose HTTP endpoints used by the frontend.
- Start and manage a Redis connection for job status and rate limiting.
- Launch background tasks that run the CO₂ estimation workflow from `food_co2_estimator`.

## Main File
### `app.py`
- Creates the FastAPI instance with CORS support.
- Provides `/estimate`, `/status/{uid}`, `/comparison` and optional rate limiting.
- Uses `RedisCache` to track job progress and to enforce request limits.
- The `run_estimator` task invokes `food_co2_estimator.main.async_estimator` and stores the result back in Redis.

## Supporting Files
- `start.sh` – Entry script used by Docker images.  It starts a local Redis server and runs `uvicorn`.
- `logging_config.yaml` – Configures log levels for the application and `uvicorn` server.
- `Dockerfile` and `cloudbuild.yaml` – Build and deployment configuration for running in containers or on Google Cloud Run.
- `template.env` – Example environment variables required for authentication and configuration.

These endpoints power the frontend in `foodprint/` and use the estimation logic described in the `food_co2_estimator` documentation.
