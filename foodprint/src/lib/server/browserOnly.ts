const ALLOWED_HOSTS = ['myfoodprint.dk', 'localhost:5173'];

/**
 * Rejects requests that do not appear to originate from a browser on
 * {@link ALLOWED_HOST}. The check relies on the presence of the
 * `Sec-Fetch-Site` header (which cURL does not send) and ensures the request
 * host matches the allowed domain.
 * NOTE: This is a basic check and may not be foolproof against all non-browser
 * clients. It is primarily intended to prevent automated tools or scripts from
 * accessing the API.
 */
export function rejectNonBrowser(request: Request): Response | null {
  const secFetchSite = request.headers.get('sec-fetch-site');
  if (!secFetchSite) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const host = request.headers.get('host');
  if (!host || !ALLOWED_HOSTS.some(allowed => host.endsWith(allowed))) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  return null;
}
