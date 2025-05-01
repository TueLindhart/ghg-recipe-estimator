import { env } from '$env/dynamic/private';
import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';

const { API_BASE, FOODPRINT_API_KEY } = env;

/** Block until the external job finishes, then return the payload */
async function waitForResult(jobId: string): Promise<unknown> {
	while (true) {
		const r = await fetch(`${API_BASE}/status/${jobId}`, {
			headers: { Authorization: `Bearer ${FOODPRINT_API_KEY}` }
		});
		if (!r.ok) throw new Error(`status ${r.status} – ${await r.text()}`);

		const data = await r.json() as { status: string; result?: string; message?: string };

		if (data.status === 'Completed') return JSON.parse(data.result ?? '{}');
		if (data.status === 'Error')  throw new Error(data.message ?? 'job failed');

		// give the API a breather
		await new Promise(res => setTimeout(res, 1_000));
	}
}

export const actions: Actions = {
	default: async ({ request }) => {
		if (!API_BASE || !FOODPRINT_API_KEY) {
			return fail(500, { error: 'Server env vars missing' });
		}

		const form = await request.formData();
		const url = form.get('url');

		if (typeof url !== 'string' || !url.trim()) {
			return fail(400, { error: 'Udfyld feltet med en gyldig URL' });
		}

		/** kick off estimate */
		const start = await fetch(`${API_BASE}/estimate`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${FOODPRINT_API_KEY}`
			},
			body: JSON.stringify({ url })
		});

		if (!start.ok) {
			return fail(start.status, { error: `API-fejl: ${start.statusText}` });
		}

		const { uid: jobId } = await start.json() as { uid: string };

		const result = await waitForResult(jobId);

		return { result };
	}
};
