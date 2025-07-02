const ALLOWED_HOST = 'myfoodprint.dk';

/**
 * Rejects requests that do not appear to originate from a browser on
 * {@link ALLOWED_HOST}. The check relies on the presence of the
 * `Sec-Fetch-Site` header (which cURL does not send) and ensures the request
 * host matches the allowed domain.
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
  if (!host || !host.endsWith(ALLOWED_HOST)) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  return null;
}
