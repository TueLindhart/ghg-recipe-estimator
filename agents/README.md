# Agent Documentation Overview

This folder contains documentation aimed at LLM-based agents.  It explains how the repository is structured and how the major pieces of the application work together.

The repository provides a FastAPI backend together with a SvelteKit frontend.  The backend exposes an API for estimating the CO₂ footprint of recipes and relies on the `food_co2_estimator` library.  The frontend lives in `foodprint/` and interacts with these endpoints.

The following sub‑folders contain detailed explanations for each part of the code base:

- **food_co2_estimator/** – Library implementing the estimation logic
- **app/** – FastAPI application and supporting files
- **foodprint/** – SvelteKit user interface and frontend architecture
- **projects/** – Project-specific documentation and learnings

Additional files include a `CHANGELOG.md` describing repository updates and a `LEARNINGS.md` file where insights about the code base and coding style are collected. The documentation has been consolidated to eliminate conflicts and provide clear, unified guidance.
