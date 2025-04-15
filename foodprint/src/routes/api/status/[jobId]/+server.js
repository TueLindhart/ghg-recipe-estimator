import { env } from "$env/dynamic/private";
import { json } from "@sveltejs/kit";

/** @type {import('../$types').RequestHandler} */
export async function GET({ params }) {
  const { jobId } = params;
  const API_BASE = env.API_BASE; // Use the private API_BASE from environment variables
  console.log("Received jobId:", jobId);

  try {
    // Use the private API_BASE to securely call your backend API with the dynamic jobId
    const resp = await fetch(`${API_BASE}/status/${jobId}`);
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
