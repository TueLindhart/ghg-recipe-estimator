# Frontend (`foodprint`)

The `foodprint` directory contains the SvelteKit based user interface.  It communicates with the FastAPI backend via `/api/*` endpoints exposed from the SvelteKit server side.

## Structure
- `src/routes` – API routes and pages.  For example `api/estimate/+server.ts` proxies a POST request to the backend `/estimate` endpoint.
- `src/lib` – Reusable components and TypeScript types used across the application.  Notable components include `IngredientCard.svelte` and `EmissionBarChart.svelte`.
- `static` – Static assets such as icons.
- `svelte.config.js` and `vite.config.ts` – Build configuration.
- `package.json` – Declares npm scripts and dependencies.  Tailwind CSS and Flowbite provide the UI styling.

The frontend expects the environment variables `API_BASE` and `FOODPRINT_API_KEY` to be supplied when running locally or in Docker.  It forwards user input to the backend and displays the resulting emission estimates and progress information.
