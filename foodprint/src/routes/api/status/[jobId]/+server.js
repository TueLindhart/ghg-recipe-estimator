import { env } from "$env/dynamic/private";
import { json } from "@sveltejs/kit";

/** @type {import('../$types').RequestHandler} */
export async function GET({ params }) {
  const { jobId } = params;
  // Check if jobId is provided
  if (!jobId) {
    return json({ error: "jobId is required" }, { status: 400 });
  }
  // Check if API_BASE is defined
  const API_BASE = env.API_BASE;
  if (!API_BASE) {
    return json({ error: "API_BASE is not defined" }, { status: 500 });
  }
  // Check if FOODPRINT_API_KEY is defined
  const FOODPRINT_API_KEY = env.FOODPRINT_API_KEY;
  if (!FOODPRINT_API_KEY) {
    return json({ error: "FOODPRINT_API_KEY is not defined" }, { status: 500 });
  }

  try {
    // Use the private API_BASE to securely call your backend API with the dynamic jobId
    const resp = await fetch(`${API_BASE}/status/${jobId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${FOODPRINT_API_KEY}`, // Use the private API key from environment variables
      },
    });
    if (!resp.ok) {
      return json(
        { error: `Error: ${resp.statusText}` },
        { status: resp.status }
      );
    }
    const data = await resp.json();
    return json(data);
  } catch (err) {
    return json({ error: `Error: ${err.message}` }, { status: 500 });
  }
}
