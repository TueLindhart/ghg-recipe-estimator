# Learnings

This file collects observations about how the repository is organised and coding preferences that emerge over time.

- **Coding style** – Python code is formatted with [Ruff](https://github.com/astral-sh/ruff) and checked with `pyright`.  The `pyproject.toml` sets a line length of 88 characters.
- **Asynchronous design** – Many functions, especially in the estimator, are asynchronous.  Tests use `pytest` with `pytest-asyncio`.
- **Environment variables** – Configuration such as API keys, cache options and model vendor are read from the environment.  The provided `template.env` shows required keys.
- **Caching strategy** – Results can be cached in Google Cloud Storage and re-used by providing the `USE_CACHE` and `STORE_IN_CACHE` flags.

Further insights should be appended here as the code evolves.
