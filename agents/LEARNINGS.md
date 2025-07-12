# Learnings

This file collects observations about how the repository is organised and coding preferences that emerge over time.

- **Coding style** – Python code is formatted with [Ruff](https://github.com/astral-sh/ruff) and checked with `pyright`.  The `pyproject.toml` sets a line length of 88 characters.
- **Asynchronous design** – Many functions, especially in the estimator, are asynchronous.  Tests use `pytest` with `pytest-asyncio`.
- **Environment variables** – Configuration such as API keys, cache options and model vendor are read from the environment.  The provided `template.env` shows required keys.
- **Caching strategy** – Results can be cached in Google Cloud Storage and re-used by providing the `USE_CACHE` and `STORE_IN_CACHE` flags.

Further insights should be appended here as the code evolves.

## API updates
The comparison endpoint exposes constants for climate budgets and average
emissions. These values are no longer included in the recipe result.

## Emission Spreadsheet

The `data/DBv2.xlsx` file contains CO₂ emission information in two sheets: `DK`
and `GB`.  The `DK` sheet is used for enrichment.  Column headers include
`ID_Ra`, `Navn`, `DSK Kategori`, `Produkt`, `Kategori`, `Total kg CO2e/kg`,
`Landbrug`, `ILUC`, `Forarbejdning`, `Emballage`, `Transport`, `Detail`,
`Energi (KJ/100 g)`, `Fedt (g/100 g)`, `Kulhydrat (g/100 g)`, `Protein (g/100 g)`,
`ID_food`, `ID_pack`, and `ID_retail`.
