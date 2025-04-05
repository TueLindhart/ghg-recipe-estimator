import logging
import uuid

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import your existing async_estimator and models
# (Adjust these imports to match your package structure)
from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.estimator import LogParams, RunParams


app = FastAPI()

origins = [
    "http://localhost:5173",
    # Add other allowed origins here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# In-memory store for job results; in production, consider Redis or a DB
job_results = {}


class EstimateRequest(BaseModel):
    url: str
    use_cache: bool = Field(
        default_factory=lambda: True, description="Use cached results if available"
    )
    store_in_cache: bool = Field(
        default_factory=lambda: True,
        description="Store results in cache for future use",
    )


class EstimateResponse(BaseModel):
    uid: str
    status: str


async def run_estimator(uid: str, runparams: RunParams):
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
        if success:
            job_results[uid] = {"status": "Completed", "result": result}
        else:
            job_results[uid] = {"status": "Error", "result": result}
    except Exception as e:
        logging.exception("Background estimation failed.")
        job_results[uid] = {"status": "Error", "result": str(e)}


@app.post("/estimate", response_model=EstimateResponse)
async def start_estimation(request: EstimateRequest, background_tasks: BackgroundTasks):
    """
    1) Generates a unique UID
    2) Saves 'Processing' status in memory
    3) Schedules the run_estimator function in the background
    4) Returns {uid, status="Processing"}
    """
    uid = str(uuid.uuid4())
    job_results[uid] = {"status": "Processing", "result": None}

    # Create your RunParams from the request
    runparams = RunParams(
        url=request.url
    )

    # Kick off the background task
    background_tasks.add_task(run_estimator, uid, runparams)

    return EstimateResponse(uid=uid, status="Processing")


@app.get("/status/{uid}")
async def get_status(uid: str):
    """
    Polling endpoint to check job status: 'Processing', 'Completed', or 'Error'
    """
    job = job_results.get(uid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JSONResponse(content=job)


@app.delete("/status/{uid}")
async def clear_status(uid: str):
    """
    Optional: Clear the job result from memory once you have retrieved it.
    """
    job_results.pop(uid, None)
    return {"status": "Cleared"}


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI on port 8000 (for example)
    uvicorn.run(app, host="127.0.0.1", port=8000)
