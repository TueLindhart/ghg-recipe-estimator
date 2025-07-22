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

## Frontend design notes
- The estimate page uses multiple custom Svelte components: `BudgetComparison.svelte`, `EquivalentComparison.svelte`, `NutritionChart.svelte`, and `OverviewCard.svelte`
- `EmissionBarChart.svelte` accepts a `metric` prop for displaying CO₂, energy or macronutrients
- All custom components rely on `flowbite-svelte` primitives (`Card`, `Chart`, `Tabs`, `TabItem`) for consistent styling
- **Component Architecture Pattern**: 
  - Components with info icons follow consistent pattern: Card has `relative` positioning and `p-4` padding
  - Info button is absolutely positioned (`absolute top-2 right-2`) as direct child of Card
  - Props focus on layout control (`cardClass="max-w-full"`), core styling stays in component
  - Text hierarchy: `text-2xl font-bold` for primary numbers, `text-sm mt-1` for labels
- **Layout Requirements**: 
  - Tabs should be positioned above content (vertical stack), not beside it
  - Use `flex flex-col` for main layout instead of `lg:flex-row` for tab positioning
  - Overview card should display `co2_per_person_kg` prominently with larger font size
