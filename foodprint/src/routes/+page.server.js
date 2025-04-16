import { fail } from "@sveltejs/kit";

const API_BASE = "/api";

export const actions = {
  // POST ?/startEstimation
  startEstimation: async ({ request, fetch }) => {
    const data = await request.formData();
    const url = data.get("url");

    if (!url) return fail(400, { error: "Missing url" });

    const upstream = await fetch(`${API_BASE}/estimate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!upstream.ok) {
      return fail(upstream.status, { error: upstream.statusText });
    }

    const { uid } = await upstream.json();
    return { jobId: uid }; // <-- plain object
  },

  // POST ?/pollStatus
  pollStatus: async ({ request, fetch }) => {
    const data = await request.formData();
    const jobId = data.get("jobId"); // <-- lower‑case key

    if (!jobId) return fail(400, { error: "Missing jobId" });

    const upstream = await fetch(`${API_BASE}/status/${jobId}`);

    if (!upstream.ok) {
      return fail(upstream.status, { error: upstream.statusText });
    }

    const res = await upstream.json();
    // everything here is JSON‑serialisable
    return { status: res.status, result: res.result };
  },
};

export const load = () => ({});
