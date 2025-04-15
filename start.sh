#!/usr/bin/env bash
set -e

echo "PATH=$PATH"
which uvicorn || echo "uvicorn not found in PATH"

if [ "$ENV" = "dev" ]; then
    echo "Starting FastAPI in development mode with uvicorn (auto-reload enabled)..."
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
else
    echo "Starting FastAPI in production mode with uvicorn..."
    uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}
fi