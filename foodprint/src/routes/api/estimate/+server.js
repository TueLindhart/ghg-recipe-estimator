import { env } from "$env/dynamic/private";
import { json } from "@sveltejs/kit";

export async function POST({ request }) {
  const { url } = await request.json();

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
    const resp = await fetch(`${API_BASE}/estimate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${FOODPRINT_API_KEY}`,
      },
      body: JSON.stringify({ url }),
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
    console.error("Error fetching estimate:", err);
    return json({ error: `Error: ${err}` }, { status: 500 });
  }
}
