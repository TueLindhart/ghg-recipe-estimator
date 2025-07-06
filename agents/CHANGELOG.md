# Changelog

## 2024-06-05
- Added the `agents/` documentation directory.
- Created detailed README files for `app`, `food_co2_estimator`, and `foodprint`.
- Added `LEARNINGS.md` for accumulated insights about the code base.

## 2024-06-06
- Reduced metadata in CO₂ retrieval output and introduced new Pydantic models
  (`CO2Match` and `CO2Matches`).
- CO₂ emissions are now enriched with nutritional info after the LLM determines
  the best match.

## 2025-07-06
- Emission metadata is loaded from the `DK` sheet of `DBv2.xlsx` instead of a
  CSV export.
- Documented the spreadsheet layout in `LEARNINGS.md`.

## 2025-07-06 (2)
- Emission enrichment now loads the Excel sheet using pandas rather than `openpyxl`.
- Documented the `scripts/create_vector_store.py` helper in the library README.
