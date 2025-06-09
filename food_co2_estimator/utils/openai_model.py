from typing import Any

from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

LLM_MODEL = "gpt-4.1-mini-2025-04-14"


def get_model(
    pydantic_model: type[BaseModel] | None = None,
    model_name: str | None = None,
    verbose: bool = False,
) -> ChatOpenAI | Runnable[Any, Any]:
    base_llm = ChatOpenAI(
        model=LLM_MODEL if model_name is None else model_name,
        temperature=0,
        verbose=verbose,
    )
    if pydantic_model is None:
        return base_llm
    structured_llm = base_llm.with_structured_output(pydantic_model)
    return structured_llm
