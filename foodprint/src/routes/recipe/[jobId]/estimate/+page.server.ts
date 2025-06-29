// src/routes/recipe/[jobId]/estimate/+page.server.ts
import { error, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import type { PageServerLoad } from './$types';
import type { RecipeCO2Output, ComparisonResponse } from '$lib';

/*
 * The loader runs first (both on the server and in the browser).
 * It receives the route parameter as params.jobId.
 *
 * Whatever this function returns becomes `data` in the Svelte page.
 */
export const load: PageServerLoad = async ({ params, fetch }) => {
        const jobId = params.jobId;
        const API_BASE = env.API_BASE;
        const API_KEY = env.FOODPRINT_API_KEY;
        if (!API_BASE || !API_KEY) {
                throw error(500, 'Missing API configuration');
        }
        // 1) Ask FastAPI for the job status and (if finished) the result
        const res = await fetch(`${API_BASE}/status/${jobId}` , {
                headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${API_KEY}`
                }
        });

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
                `${API_BASE}/comparison?kgco2=${result.total_co2_kg}`,
                {
                        headers: { Authorization: `Bearer ${API_KEY}` }
                }
        );
        if (!cmpRes.ok) throw new Error('Comparison service failed');
        const comparison: ComparisonResponse = await cmpRes.json();

	// 4) Hand the data to +page.svelte
        return { jobId, result, comparison };
};
