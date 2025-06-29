import { env } from '$env/dynamic/private';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const API_BASE = env.API_BASE;
  const API_KEY = env.FOODPRINT_API_KEY;
  if (!API_BASE || !API_KEY) {
    return { jobId: params.jobId, status: 'Error', result: 'Missing API configuration' };
  }
  const resp = await fetch(`${API_BASE}/status/${params.jobId}`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${API_KEY}`
    }
  });

  if (!resp.ok) {
    let detail = resp.statusText;
    try {
      const err = await resp.json();
      if (err?.error) detail = err.error;
    } catch {}
    return { jobId: params.jobId, status: 'Error', result: detail };
  }

  const data: { status: string; result?: string } = await resp.json();
  return { jobId: params.jobId, ...data };
};
