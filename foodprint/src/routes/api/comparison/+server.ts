import { env } from "$env/dynamic/private";
import { json, type RequestHandler } from "@sveltejs/kit";
import { rejectNonBrowser } from "$lib/server/browserOnly";

/**
 * Proxy for GET /comparison?kgco2=<value> on the Python backend
 *
 *  – Keeps the same guard rails (env-checks) you use for /estimate
 *  – Preserves HTTP status codes from the backend
 *  – Returns plain JSON to the Svelte front-end
 */
export const GET: RequestHandler = async ({ url, fetch, request }) => {
  const forbidden = rejectNonBrowser(request);
  if (forbidden) return forbidden;
  /* ───── 1. Extract and validate input ───── */
  const kgco2 = url.searchParams.get("kgco2");
  if (!kgco2) {
    return json({ error: "Query param kgco2 is required" }, { status: 400 });
  }

  /* ───── 2. Verify required environment variables ───── */
  const API_BASE          = env.API_BASE;
  const FOODPRINT_API_KEY = env.FOODPRINT_API_KEY;

  if (!API_BASE) {
    return json({ error: "API_BASE is not defined" }, { status: 500 });
  }
  if (!FOODPRINT_API_KEY) {
    return json({ error: "FOODPRINT_API_KEY is not defined" }, { status: 500 });
  }

  /* ───── 3. Forward the request to the Python service ───── */
  try {
    const resp = await fetch(
      `${API_BASE}/comparison?kgco2=${encodeURIComponent(kgco2)}`,
      {
        headers: { Authorization: `Bearer ${FOODPRINT_API_KEY}` }
      }
    );

    if (!resp.ok) {
      return json(
        { error: `Error: ${resp.statusText}` },
        { status: resp.status }
      );
    }

    const data = await resp.json();
    return json(data);
  } catch (err) {
    console.error("Error fetching comparison:", err);
    return json({ error: `Error: ${err}` }, { status: 500 });
  }
};
