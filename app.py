import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from food_co2_estimator.logger_utils import logger
from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.estimator import LogParams, RunParams
from food_co2_estimator.pydantic_models.response_models import (
    EstimateRequest,
    JobResult,
    JobStatus,
    StartEstimateResponse,
)
from food_co2_estimator.rediscache import RedisCache

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI to manage Redis connection.
    """
    # Initialize Redis connection pool
    redis = await RedisCache.create()
    app.state.redis = redis
    yield
    # Cleanup on shutdown
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        # You can configure LogParams as needed
        logparams = LogParams(
            logging_level=logging.INFO
        )  # TODO: Remove LogParams - not used.
        success, result = await async_estimator(
            runparams=runparams, logparams=logparams, redis_client=redis_client
        )
        status = JobStatus.COMPLETED if success else JobStatus.ERROR
        result = result if success else None
        await redis_client.update_job_status(
            runparams.uid,
            status=status,
            result=result,
        )

        logger.info(
            f"Completed CO2 estimation for UID={runparams.uid} URL={runparams.url}"
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
    return JobResult.model_validate_json(job)


@app.delete("/status/{uid}")
async def clear_status(uid: str):
    """
    Optional: Clear the job result from memory once you have retrieved it.
    """
    redis_client: RedisCache = app.state.redis
    await redis_client.delete(uid)
    return {"status": "Cleared"}


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI on port 8000 (for example)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.DEBUG)
