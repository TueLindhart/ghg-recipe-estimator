import { env } from '$env/dynamic/private';
import { fail, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request, fetch }) => {
    const { url } = await request.json();
    if (!url) {
      return fail(400, { error: 'URL is required' });
    }
    const API_BASE = env.API_BASE;
    const API_KEY = env.FOODPRINT_API_KEY;
    if (!API_BASE || !API_KEY) {
      return fail(500, { error: 'Missing API configuration' });
    }
    const resp = await fetch(`${API_BASE}/estimate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      },
      body: JSON.stringify({ url })
    });
    if (!resp.ok) {
      let detail = resp.statusText;
      try {
        const err = await resp.json();
        if (err?.error) detail = err.error;
      } catch {}
      return fail(resp.status, { error: detail });
    }
    const data = await resp.json();
    return { uid: data.uid };
  }
};
