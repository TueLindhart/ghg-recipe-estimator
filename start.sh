#!/usr/bin/env bash
set -e

# start redis server
# NOTE: If it is needed to run multiple containers then we need to move redis
# out to its own instance.
redis-server --daemonize yes --maxmemory 50mb --maxmemory-policy allkeys-lfu

if [ "$ENV" = "dev" ]; then
    echo "Starting FastAPI in development mode with uvicorn (auto-reload enabled)..."
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
else
    echo "Starting FastAPI in production mode with uvicorn..."
    uvicorn app:app --workers 2 --host 0.0.0.0 --port ${PORT:-8080} 
fi