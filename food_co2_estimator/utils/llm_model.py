import os
from enum import Enum
from typing import Any

from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

OPENAI_LLM_MODEL = "gpt-4.1-mini-2025-04-14"
GEMINI_LLM_MODEL = "gemini-2.5-flash-preview-05-20"


class ModelVendor(Enum):
    OPENAI = "openai"
    GOOGLE = "google"

    def __str__(self) -> str:
        return self.value


MODEL_VENDOR_ENV = os.getenv("MODEL_VENDOR", ModelVendor.GOOGLE.value).lower()
MODEL_VENDOR = (
    ModelVendor(MODEL_VENDOR_ENV)
    if MODEL_VENDOR_ENV in ModelVendor.__members__
    else ModelVendor.GOOGLE
)


class LLMFactory:
    def __init__(
        self,
        model_vendor: ModelVendor | None = None,
        output_model: type[BaseModel] | None = None,
        verbose: bool = False,
    ):
        self.model_vendor = model_vendor if model_vendor is not None else MODEL_VENDOR
        self.output_model = output_model
        self.verbose = verbose

    def get_model(
        self,
        model_name: str | None = None,
    ) -> Runnable[Any, Any]:
        if self.model_vendor == ModelVendor.OPENAI:
            return get_openai_model(
                model_name=model_name,
                output_model=self.output_model,
                verbose=self.verbose,
            )
        if self.model_vendor == ModelVendor.GOOGLE:
            return get_gemini_model(
                model_name=model_name,
                output_model=self.output_model,
                verbose=self.verbose,
            )
        raise ValueError(
            f"Unsupported model vendor: {self.model_vendor}. "
            "Supported vendors are: OPENAI, GOOGLE."
        )


def get_openai_model(
    model_name: str | None = None,
    output_model: type[BaseModel] | None = None,
    verbose: bool = False,
) -> Runnable[Any, Any]:
    base_llm = ChatOpenAI(
        model=OPENAI_LLM_MODEL if model_name is None else model_name,
        temperature=0,
        verbose=verbose,
    )
    if output_model is None:
        return base_llm
    structured_llm = base_llm.with_structured_output(output_model)
    return structured_llm


def get_gemini_model(
    model_name: str | None = None,
    output_model: type[BaseModel] | None = None,
    verbose: bool = False,
) -> Runnable[Any, Any]:
    base_llm = ChatGoogleGenerativeAI(
        model=GEMINI_LLM_MODEL if model_name is None else model_name,
        temperature=0,
        verbose=verbose,
        thinking_budget=0,
        include_thoughts=False,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    if output_model is None:
        return base_llm
    structured_llm = base_llm.with_structured_output(output_model)
    return structured_llm
