# Backend Application (`app`)

This folder documents the FastAPI service defined in `app.py` along with its auxiliary files. The application serves as the HTTP interface between the frontend and the CO₂ estimation logic, managing background jobs, rate limiting, and real-time status updates.

## Core Responsibilities
- Expose HTTP endpoints used by the frontend
- Start and manage a Redis connection for job status and rate limiting
- Launch background tasks that run the CO₂ estimation workflow from `food_co2_estimator`
- Provide comparison data for frontend visualization components
- Handle CORS for frontend integration
- Manage async task execution with proper error handling

## API Architecture

### Job Management Pattern
The application uses a background job pattern with unique job IDs:
1. **Job Creation**: `POST /estimate` creates unique job ID and starts background processing
2. **Status Polling**: `GET /status/{uid}` allows frontend to poll for progress updates
3. **Job Cleanup**: `DELETE /status/{uid}` removes completed job data
4. **Real-time Updates**: Redis stores intermediate status updates for live frontend feedback

### Rate Limiting Strategy
- Redis-based rate limiting prevents abuse
- Configurable limits per user/IP
- Graceful degradation when limits exceeded
- Rate limit headers returned to frontend

## API Endpoints

### Core Estimation Endpoints
- **`POST /estimate`**: Start CO₂ estimation job
  - Accepts `EstimateRequest` with URL and cache settings
  - Returns `StartEstimateResponse` with unique job ID and status
  - Initiates background processing with real-time status updates

- **`GET /status/{uid}`**: Poll job status and retrieve results
  - Returns current job status (PROCESSING, EXTRACTING_TEXT, EXTRACTING_RECIPE, ESTIMATING_WEIGHTS, ESTIMATING_CO2, PREPARING_OUTPUT, COMPLETED, ERROR)
  - On completion, returns full `RecipeCO2Output` with nutritional and emission data

- **`DELETE /status/{uid}`**: Clean up completed job data

### Comparison Data Endpoint
- **`GET /comparison?kgco2={value}`**: Get comprehensive comparison data
  - Returns `ComparisonResponse` with multiple comparison types:
    - Diesel car kilometers equivalent
    - Flight comparisons (Copenhagen to Aalborg)
    - Washing machine cycles equivalent
    - Budget comparisons (meal/daily budgets from Concito research)
    - Average Danish person emission comparisons
  - Used by frontend "Sammenlign" and "Svare til" tabs
  - Provides all comparison data needed for visualization components

## Integration with Frontend Design

### Status Update Architecture
The API provides granular status updates that power the frontend progress indicators. Each status corresponds to a specific step in the estimation pipeline:

```
Frontend Polling → /status/{uid} → Redis Cache → Status Updates
     ↑                                              ↓
Frontend UI ← Status Display ← Job Status ← Background Processing
```

### Data Flow for Redesign Project
1. **Frontend submits URL** via `/estimate` endpoint
2. **Background job starts** with status PROCESSING
3. **Real-time updates** show progress through each estimation phase
4. **Completion** provides full recipe data including nutritional information
5. **Comparison data** fetched separately via `/comparison` endpoint
6. **Frontend tabs** display organized data using provided comparison metrics

### Frontend Component Integration
The API endpoints are specifically designed to support the redesign-estimate-page components:
- **OverviewCard**: Uses main CO₂ values from estimation results
- **BudgetComparison**: Uses budget comparison data from `/comparison` endpoint
- **EquivalentComparison**: Uses equivalent comparisons (car, flight, washing machine)
- **NutritionChart**: Uses nutritional data included in estimation results

## Configuration & Environment

### Required Environment Variables (template.env)
- **API Keys**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` for LLM access
- **Cache Settings**: `USE_CACHE`, `STORE_IN_CACHE` for Google Cloud Storage integration
- **Redis Configuration**: Connection settings for job tracking and rate limiting
- **Model Selection**: `LLM_VENDOR` to choose between OpenAI and Anthropic
- **CORS Settings**: Frontend URL configuration for cross-origin requests

### Deployment Configuration
- **Dockerfile**: Multi-stage build with Python dependencies and Redis
- **cloudbuild.yaml**: Google Cloud Run deployment configuration
- **start.sh**: Entry script that starts Redis server and FastAPI application
- **logging_config.yaml**: Structured logging for production monitoring

## Main Application File

### `app.py` Architecture
- **FastAPI Instance**: Creates the main application with CORS support for frontend integration
- **Endpoint Handlers**: Provides `/estimate`, `/status/{uid}`, `/comparison` with proper error handling
- **Redis Integration**: Uses `RedisCache` for job progress tracking and request rate limiting
- **Background Tasks**: The `run_estimator` function invokes `food_co2_estimator.main.async_estimator` asynchronously
- **Error Handling**: Comprehensive error states and graceful degradation
- **Rate Limiting**: Optional rate limiting to prevent abuse and manage resource usage

### Key Implementation Details
- **Async Design**: All endpoints use async/await for non-blocking operation
- **Job Management**: Unique UUIDs for job tracking with Redis persistence
- **Type Safety**: Full Pydantic model validation for request/response data
- **CORS Configuration**: Proper headers for frontend cross-origin requests
- **Background Processing**: Long-running estimation tasks don't block API responses

## Supporting Infrastructure Files

### Deployment & Operations
- **`start.sh`**: Entry script used by Docker images - starts Redis server and runs `uvicorn`
- **`Dockerfile`**: Multi-stage Docker build with Python dependencies and Redis server
- **`cloudbuild.yaml`**: Google Cloud Run deployment configuration with environment secrets
- **`logging_config.yaml`**: Configures log levels for application and `uvicorn` server
- **`template.env`**: Example environment variables required for authentication and configuration

### Development & Testing
- **Local Development**: Redis can run locally or use cloud Redis instance
- **Environment Configuration**: All settings configurable via environment variables
- **Logging**: Structured logging for debugging and production monitoring
- **Health Checks**: Basic health endpoints for deployment verification

## Development Context & Learnings

### Coding Standards (from RULES.md)
- **Type Hints**: All functions include comprehensive type hints
- **SOLID Principles**: Clean separation of concerns, single responsibility
- **Readability**: Code prioritizes clarity and maintainability
- **Async First**: Background processing for all intensive operations

### Performance Considerations
- **Redis Caching**: Reduces database load and improves response times
- **Background Jobs**: Prevents API timeouts on long-running estimations
- **Rate Limiting**: Protects against abuse while maintaining usability
- **Graceful Degradation**: Optional services don't break core functionality

### Integration Patterns
- **Frontend Communication**: RESTful API with polling for real-time updates
- **Component Data**: API responses structured to match frontend component needs
- **Error States**: Comprehensive error handling with user-friendly messages
- **Caching Strategy**: Multiple caching layers for optimal performance

These endpoints power the frontend in `foodprint/` and use the estimation logic described in the `food_co2_estimator` documentation. The application is designed for production deployment with proper monitoring, rate limiting, and error handling while maintaining development-friendly local setup.
