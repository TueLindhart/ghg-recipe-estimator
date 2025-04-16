import logging
import os
import uuid
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated

import aioredis
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

# Import your existing async_estimator and models
# (Adjust these imports to match your package structure)
from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.estimator import LogParams, RunParams

load_dotenv()


async def redis_pool():
    return aioredis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        encoding="utf-8",
        decode_responses=True,
        ex=3600,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI to manage Redis connection.
    """
    # Initialize Redis connection pool
    redis = await redis_pool()
    app.state.redis = redis
    yield
    # Cleanup on shutdown
    await redis.close()


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


class EstimateRequest(BaseModel):
    url: str
    use_cache: bool = Field(
        default_factory=lambda: True, description="Use cached results if available"
    )
    store_in_cache: bool = Field(
        default_factory=lambda: True,
        description="Store results in cache for future use",
    )


class StartEstimateResponse(BaseModel):
    uid: str
    status: str


class JobStatus(str, Enum):
    ERROR = "Error"
    COMPLETED = "Completed"
    PROCESSING = "Processing"


class JobResult(BaseModel):
    status: JobStatus
    result: str | None = None


async def run_estimator(
    uid: str,
    runparams: RunParams,
    redis_client: aioredis.Redis,
):
    """
    Background task that executes your async_estimator function.
    """
    logging.info(f"Starting CO2 estimation for UID={uid} URL={runparams.url}")
    try:
        # You can configure LogParams as needed
        logparams = LogParams(logging_level=logging.INFO)
        success, result = await async_estimator(
            runparams=runparams, logparams=logparams
        )
        status = JobStatus.COMPLETED if success else JobStatus.ERROR
        jobresult = JobResult(status=status, result=result)

        if success:
            # job_results[uid] = {"status": "Completed", "result": result}
            await redis_client.set(
                uid,
                jobresult.model_dump_json(),
            )
        else:
            # job_results[uid] = {"status": "Error", "result": result}
            await redis_client.set(
                uid,
                jobresult.model_dump_json(),
            )
        logging.info(f"Completed CO2 estimation for UID={uid} URL={runparams.url}")
    except Exception as e:
        logging.exception("Background estimation failed.")
        await redis_client.set(
            uid,
            JobResult(status=JobStatus.ERROR, result=str(e)).model_dump_json(),
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
    uid = str(uuid.uuid4())
    redis_client: aioredis.Redis = await app.state.redis
    await redis_client.set(
        uid,
        JobResult(status=JobStatus.PROCESSING).model_dump_json(),
    )

    # Create your RunParams from the request
    runparams = RunParams(url=request.url)

    # Kick off the background task
    background_tasks.add_task(run_estimator, uid, runparams, redis_client)

    return StartEstimateResponse(uid=uid, status=JobStatus.PROCESSING)


@app.get("/status/{uid}")
async def get_status(uid: str, access: Annotated[bool, Depends(verify_token)]):
    """
    Polling endpoint to check job status: 'Processing', 'Completed', or 'Error'
    """
    if not access:
        raise HTTPException(status_code=401, detail="Unauthorized")

    redis_client: aioredis.Redis = await app.state.redis
    job = await redis_client.get(uid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JSONResponse(content=JobResult.model_validate_json(job))


@app.delete("/status/{uid}")
async def clear_status(uid: str):
    """
    Optional: Clear the job result from memory once you have retrieved it.
    """
    redis_client: aioredis.Redis = await app.state.redis
    await redis_client.delete(uid)
    return {"status": "Cleared"}


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI on port 8000 (for example)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.DEBUG)
