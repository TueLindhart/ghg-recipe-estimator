# Library: `food_co2_estimator`

This package contains all logic for estimating the CO₂ footprint of a recipe.  It is used both by the FastAPI backend and by tests.

## Overview
1. **`main.py`** – Entry point for the estimation pipeline.  The `async_estimator` function orchestrates:
   - Converting recipe webpages to Markdown (`url/url2markdown.py`).
   - Extracting structured recipe data with an LLM (`chains/recipe_extractor.py`).
   - Estimating ingredient weights (`chains/weight_estimator.py`).
   - Looking up CO₂ emissions via a retrieval‑augmented chain (`chains/rag_co2_estimator.py`).
   - Generating final output models (`utils/output_generator.py`).
   The pipeline updates Redis with progress states defined in `pydantic_models.response_models`.

2. **`blob_caching.py`** – Optional caching layer storing estimation results in Google Cloud Storage.  Decorators allow results to be reused across runs.

3. **`rediscache.py`** – Async wrapper around Redis used for job status, caching and rate limiting.

4. **`co2_comparison.py`** – Utility to compare a CO₂ value against a reference trip, returned via a Pydantic model.

## Sub‑packages
- **`chains/`** – LangChain runnable chains for recipe extraction, weight estimation and emission retrieval.
- **`retrievers/`** – Helpers for vector database retrieval (`vector_db_retriever.py`) and web search retrieval (`search_retriever.py`).
- **`language/`** – Language detection using `langdetect`.
- **`pydantic_models/`** – Typed models describing recipes, emissions and API responses.
- **`utils/`** – Abstractions for choosing the LLM vendor (`llm_model.py`) and building the final response (`output_generator.py`).
- **`url/`** – Functions for parsing webpages and removing unwanted HTML prior to LLM processing.
- **`data/`** – Contains the vector store, SQLite DB and constants used by the retrievers.

The modules in this package are designed to be composable and mostly async so that the FastAPI app can run intensive tasks in the background without blocking.
