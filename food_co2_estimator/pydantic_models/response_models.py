from enum import Enum

from pydantic import BaseModel, Field


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
    EXTRACTING_TEXT = "Text"
    EXTRACTING_RECIPE = "Recipe"
    TRANSLATING = "Translating"
    ESTIMATING_WEIGHTS = "Weights"
    ESTIMATING_CO2 = "RAGCO2"
    ESTIMATING_SEARCH_CO2 = "SearchCO2"
    PREPARING_OUTPUT = "Preparing"


class JobResult(BaseModel):
    status: JobStatus
    result: str | None = None
