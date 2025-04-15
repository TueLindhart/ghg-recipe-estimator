import { env } from "$env/dynamic/private";
import { json } from "@sveltejs/kit";

console.log("Dynamic API_BASE:", env.API_BASE);

export async function POST({ request }) {
  const { url } = await request.json();
  const API_BASE = env.API_BASE;
  console.log("API_BASE:", API_BASE);

  try {
    const resp = await fetch(`${API_BASE}/estimate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
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
    return json({ error: `Error: ${err.message}` }, { status: 500 });
  }
}
