// src/routes/recipe/[uid]/estimate/+page.ts
import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

/*
 * The loader runs first (both on the server and in the browser).
 * It receives the route parameter as params.uid.
 *
 * Whatever this function returns becomes `data` in the Svelte page.
 */
export const load: PageLoad = async ({ params, fetch }) => {
	// 1) Ask FastAPI for the job status and (if finished) the result
	const res = await fetch(`/api/status/${params.uid}`);

	if (!res.ok) {
		// Tell SvelteKit to show its generic error page
		throw error(res.status, 'Kunne ikke hente resultater');
	}

	const statusData: { status: string; result?: string } = await res.json();

	// 2) If someone lands here too early, send them back to the status page
	if (statusData.status !== 'Completed') {
		throw redirect(307, `/recipe/${params.uid}/status`);
	}

	// 3) Parse the JSON‑string that the API stored in result
	if (!statusData.result) {
		throw error(500, 'API svarede uden data');
	}

	const result = JSON.parse(statusData.result);

	const cmpRes = await fetch(
		`/api/comparison?kgco2=${result.total_co2_kg}`
	);
	if (!cmpRes.ok) throw new Error("Comparison service failed");
	const comparison = await cmpRes.json();

	// 4) Hand the data to +page.svelte
	return { uid: params.uid, result, comparison };
};
