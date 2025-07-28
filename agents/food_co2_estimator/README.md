# Library: `food_co2_estimator`

This package contains all logic for estimating the CO₂ footprint of a recipe. It is used both by the FastAPI backend and by tests. The module is designed for composable, async operations that support real-time status tracking and comprehensive nutritional analysis.

## Overview
1. **`main.py`** – Entry point for the estimation pipeline. The `async_estimator` function orchestrates:
   - Converting recipe webpages to Markdown (`url/url2markdown.py`)
   - Extracting structured recipe data with an LLM (`chains/recipe_extractor.py`)
   - Estimating ingredient weights (`chains/weight_estimator.py`)
   - Looking up CO₂ emissions via a retrieval‑augmented chain (`chains/rag_co2_estimator.py`)
   - Generating comprehensive output models with nutritional data (`utils/output_generator.py`)
   - Real-time status updates to Redis for frontend progress tracking

2. **`blob_caching.py`** – Optional caching layer storing estimation results in Google Cloud Storage. Decorators allow results to be reused across runs.

3. **`rediscache.py`** – Async wrapper around Redis used for job status, caching and rate limiting with job status tracking for multi-step processes.

4. **`co2_comparison.py`** – Utility to compare CO₂ values against multiple reference points:
   - Diesel car emissions (km equivalent)
   - Flight emissions (Copenhagen to Aalborg)
   - Washing machine usage (wash cycles)
   - Budget comparisons (meal/daily budgets from Concito research)
   - Average Danish person emissions

5. **`scripts/create_vector_store.py`** – Builds both Danish and English vector stores from the `DBv2.xlsx` spreadsheet using pandas.

## Sub‑packages
- **`chains/`** – LangChain runnable chains for recipe extraction, weight estimation and emission retrieval:
  - `recipe_extractor.py`: Extracts structured recipe data from web content
  - `weight_estimator.py`: Estimates ingredient weights with multi-language support and improved accuracy
  - `rag_co2_estimator.py`: CO₂ emission lookup via vector database retrieval
- **`retrievers/`** – Helpers for vector database retrieval (`vector_db_retriever.py`) and web search retrieval (`search_retriever.py`)
- **`language/`** – Language detection using `langdetect` for multi-language recipe support
- **`pydantic_models/`** – Typed models describing recipes, emissions and API responses:
  - `response_models.py`: Comprehensive job status tracking with states (PROCESSING, EXTRACTING_TEXT, EXTRACTING_RECIPE, ESTIMATING_WEIGHTS, ESTIMATING_CO2, PREPARING_OUTPUT, COMPLETED, ERROR)
  - `estimator.py`: Recipe and estimation parameters
  - All models include nutritional data (energy_kj, fat_g, carbohydrate_g, protein_g)
- **`utils/`** – Abstractions for choosing the LLM vendor (`llm_model.py`) and building comprehensive final response (`output_generator.py`)
- **`url/`** – Functions for parsing webpages and removing unwanted HTML prior to LLM processing
- **`data/`** – Contains the vector store, SQLite DB and constants used by the retrievers

## Technical Architecture & Design Principles

### Asynchronous Design Philosophy
- All estimation functions are async to support non-blocking background processing
- FastAPI app can handle multiple concurrent requests without blocking
- Redis-based job tracking enables real-time progress updates to frontend
- `pytest-asyncio` used for testing async functions

### Error Handling & Reliability
- Comprehensive error states in job status tracking
- Graceful degradation when optional services (cache, Redis) are unavailable
- Caching strategies reduce API calls and improve response times
- Rate limiting prevents abuse and manages resource usage

### Language Support
- Danish and English vector stores built from `data/DBv2.xlsx`
- Language detection automatically routes to appropriate processing chains
- Multi-language recipe parsing and ingredient matching

### Data Flow Architecture
```
URL → Markdown → Recipe Extraction → Weight Estimation → CO₂ Lookup → Output Generation
 ↓        ↓             ↓               ↓              ↓           ↓
Redis Status Updates: TEXT → RECIPE → WEIGHTS → CO2 → PREPARING → COMPLETED
```

## Integration with Redesign Project

### Frontend Status Tracking
The estimation pipeline provides granular status updates that power the frontend progress indicators:
- **PROCESSING**: Initial job received
- **EXTRACTING_TEXT**: Converting webpage to readable format
- **EXTRACTING_RECIPE**: LLM parsing recipe structure
- **ESTIMATING_WEIGHTS**: Calculating ingredient quantities
- **ESTIMATING_CO2**: Looking up emission factors
- **PREPARING_OUTPUT**: Generating final response with comparisons
- **COMPLETED**: Results ready with full data structure
- **ERROR**: Processing failed with error details

### Comparison Data Generation
The `co2_comparison.py` module generates all comparison data used by frontend tabs:
- **Budget Comparisons**: Percentage of meal/daily CO₂ budgets based on Concito research
- **Equivalent Comparisons**: Car kilometers, flight distances, appliance usage equivalents
- **Average Person**: Danish average emissions for context

### Nutritional Data Pipeline
Extended data models provide complete nutritional information:
- Energy values in both kJ and kcal for different user preferences
- Macronutrient breakdown (fat, carbohydrates, protein) for chart visualization
- Per-person calculations for realistic serving assessments
- Per-ingredient nutritional details for ingredient-level analysis

## Configuration & Environment

### Required Environment Variables
- **API Keys**: OpenAI, Anthropic for LLM access
- **Cache Configuration**: `USE_CACHE`, `STORE_IN_CACHE` for Google Cloud Storage
- **Redis**: Connection settings for job tracking and rate limiting
- **Model Selection**: Choice of LLM vendor (OpenAI, Anthropic)

### Coding Standards
- Type hints on all functions following project `RULES.md`
- SOLID principles with functional approach where appropriate
- Ruff formatting with 88-character line length
- `pyright` type checking for reliability

The modules in this package are designed to be composable and mostly async so that the FastAPI app can run intensive tasks in the background without blocking.
