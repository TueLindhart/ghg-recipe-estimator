import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from food_co2_estimator.co2_comparison import compare_co2
from food_co2_estimator.logger_utils import logger
from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.estimator import RunParams
from food_co2_estimator.pydantic_models.response_models import (
    ComparisonResponse,
    EstimateRequest,
    JobResult,
    JobStatus,
    StartEstimateResponse,
)
from food_co2_estimator.rediscache import RedisCache

load_dotenv()

# Rate limiting configuration
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "300"))  # requests
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds (1 minute)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get client IP address (support X-Forwarded-For for proxies)
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.client.host if request.client else "unknown"

        # Extract API key from Authorization header if present
        api_key = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            api_key = auth_header[7:].strip()

        redis_client: RedisCache = request.app.state.redis

        # Check rate limit per (api_key, IP)
        is_allowed, remaining = await redis_client.check_rate_limit(
            ip_address, RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW, api_key=api_key
        )

        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {RATE_LIMIT_WINDOW} seconds.",
            )

        response = await call_next(request)

        # Add rate limit headers to response
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_MAX_REQUESTS)
        response.headers["X-RateLimit-Window"] = str(RATE_LIMIT_WINDOW)

        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI to manage Redis connection.
    """
    # Initialize Redis connection pool
    redis = await RedisCache.create()
    await redis.clear()
    app.state.redis = redis
    yield
    # Cleanup on shutdown
    await redis.clear()
    await redis.aclose()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "www.myfoodprint.dk",
    "myfoodprint.dk",
    "https://www.myfoodprint.dk",
    "https://myfoodprint.dk",
    # Add other allowed origins here
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)


security = HTTPBearer()


def get_token():
    token = os.getenv("FOODPRINT_API_KEY")
    if token is None:
        raise ValueError("FOODPRINT_API_KEY environment variable not set.")
    return token


def verify_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    expected_token: Annotated[str, Depends(get_token)],
) -> bool:
    if (
        credentials.scheme.lower() != "bearer"
        or credentials.credentials != expected_token
    ):
        logging.warning("Invalid or missing API token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
    return True


async def run_estimator(
    runparams: RunParams,
    redis_client: RedisCache,
):
    """
    Background task that executes your async_estimator function.
    """
    logger.info(f"Starting CO2 estimation for UID={runparams.uid} URL={runparams.url}")
    try:
        success, result = await async_estimator(
            runparams=runparams, redis_client=redis_client
        )
        status = JobStatus.COMPLETED if success else JobStatus.ERROR
        await redis_client.update_job_status(
            runparams.uid,
            status=status,
            result=result,
        )

        if success:
            logger.info(
                f"Completed CO2 estimation for UID={runparams.uid} URL={runparams.url}"
            )
        else:
            logger.error(
                f"CO2 estimation failed for UID={runparams.uid} URL={runparams.url}: {result}"
            )
    except Exception as e:
        logger.exception("Background estimation failed.")
        await redis_client.update_job_status(
            runparams.uid,
            status=JobStatus.ERROR,
            result=str(e),
        )


@app.post("/estimate", response_model=StartEstimateResponse)
async def start_estimation(
    request: EstimateRequest,
    background_tasks: BackgroundTasks,
    access: Annotated[bool, Depends(verify_token)],
):
    """
    1) Generates a unique UID
    2) Saves 'Processing' status in memory
    3) Schedules the run_estimator function in the background
    4) Returns {uid, status="Processing"}
    """
    if not access:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Create your RunParams from the request
    runparams = RunParams(url=request.url)
    redis_client: RedisCache = app.state.redis
    await redis_client.update_job_status(
        runparams.uid,
        JobStatus.PROCESSING,
    )

    # Kick off the background task
    background_tasks.add_task(run_estimator, runparams, redis_client)

    return StartEstimateResponse(uid=runparams.uid, status=JobStatus.PROCESSING)


@app.get("/status/{uid}")
async def get_status(uid: str, access: Annotated[bool, Depends(verify_token)]):
    """
    Polling endpoint to check job status: 'Processing', 'Completed', or 'Error'
    """
    if not access:
        raise HTTPException(status_code=401, detail="Unauthorized")

    redis_client: RedisCache = app.state.redis
    job = await redis_client.get(uid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job_obj = JobResult.model_validate_json(job)
    if job_obj.status == JobStatus.ERROR:
        raise HTTPException(status_code=400, detail=job_obj.result)
    return job_obj


@app.delete("/status/{uid}")
async def clear_status(uid: str):
    """
    Optional: Clear the job result from memory once you have retrieved it.
    """
    redis_client: RedisCache = app.state.redis
    await redis_client.delete(uid)
    return {"status": "Cleared"}


@app.get("/comparison", response_model=ComparisonResponse)
async def comparison_endpoint(kgco2: float):
    """
    Compare <kgco2> to 100 % of a CPH→NYC flight.

    Query params
    ------------
    kgco2 : float   Amount of CO₂ (kg) you wish to compare.
    """
    try:
        return compare_co2(kgco2)
    except ValueError as exc:
        # Translate domain error → HTTP 422 for FastAPI clients
        raise HTTPException(status_code=422, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI on port 8000 (for example)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.DEBUG)
