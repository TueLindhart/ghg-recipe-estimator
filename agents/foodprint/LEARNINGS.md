# LEARNINGS.md

## Project Structure & Focus
- The project is a GHG (CO2e) recipe estimator, with a frontend (Svelte) and backend Python logic.
- The `foodprint` agent is responsible for the UI and user experience, including recipe CO2e calculations and visualizations.
- The `projects/redesign-estimate-page` folder contains design assets and screenshots for the redesign of the estimate page, showing various tab layouts and content states.

## UI/UX Observations
- The estimate page features an `OverviewCard` summarizing CO2e per person and per meal.
- To the right of the overview, there are tabs for: "Sammenlign" (Compare), "Svare til" (Equivalent), and "Næringsindhold" (Nutrition).
- The current implementation places the tabs to the right of the overview card (side-by-side, flex-row), but the design and user request require the tabs to be above the content (stacked vertically, flex-col).
- Each tab displays different content: budget comparison, equivalents, and nutrition info/chart.

## Next Steps
- Refactor the tab layout so that the tabs are above the content, not beside it. This will improve clarity and match the intended design.
- The change should be made in the Svelte file for the estimate page, specifically in the flex container that currently uses `lg:flex-row` for the overview and tabs.

---
*This file summarizes learnings about the project structure, design intent, and the required UI fix for the estimate page tabs.*
