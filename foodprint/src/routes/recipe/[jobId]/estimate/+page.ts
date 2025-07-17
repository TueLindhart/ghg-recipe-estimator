// src/routes/recipe/[jobId]/estimate/+page.ts
import type { ComparisonResponse, RecipeCO2Output } from '$lib';
import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

/*
 * The loader runs first (both on the server and in the browser).
 * It receives the route parameter as params.jobId.
 *
 * Whatever this function returns becomes `data` in the Svelte page.
 */
export const load: PageLoad = async ({ params, fetch }) => {
        const jobId = params.jobId;
        // 1) Ask FastAPI for the job status and (if finished) the result
        const res = await fetch(`/api/status/${jobId}`);

	if (!res.ok) {
		// Tell SvelteKit to show its generic error page
		throw error(res.status, 'Kunne ikke hente resultater');
	}

	const statusData: { status: string; result?: string } = await res.json();

	// 2) If someone lands here too early, send them back to the status page
        if (statusData.status !== 'Completed') {
                throw redirect(307, `/recipe/${jobId}/status`);
        }

	// 3) Parse the JSON‑string that the API stored in result
	if (!statusData.result) {
		throw error(500, 'API svarede uden data');
	}

        const result: RecipeCO2Output = JSON.parse(statusData.result);

	const cmpRes = await fetch(
		`/api/comparison?kgco2=${result.co2_per_person_kg}`
	);
	if (!cmpRes.ok) throw new Error("Comparison service failed");
        const comparison: ComparisonResponse = await cmpRes.json();

	// 4) Hand the data to +page.svelte
        return { jobId, result, comparison };
};
