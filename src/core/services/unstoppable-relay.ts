/** Read-only egress for Unstoppable when its API rejects Worker fetches. */
let route: { url: string; token: string } | null = null;
const ACTIONS = new Set(['ud_portfolio_list', 'ud_domain_get']);
export function configureUnstoppableRelay(url?: string, token?: string): void {
  if (!url && !token) {
    route = null;
    return;
  }
  if (!url || !token || new URL(url).protocol !== 'https:')
    throw new Error('Unstoppable relay requires an HTTPS URL and token.');
  route = { url: url.replace(/\/$/, ''), token };
}
export function unstoppableRelayFetch(): typeof fetch | undefined {
  if (!route) return undefined;
  const configured = route;
  return async (input, init) => {
    const request = new Request(input, init);
    const url = new URL(request.url);
    const action = url.pathname.split('/').at(-1)!;
    if (
      url.origin !== 'https://api.unstoppabledomains.com' ||
      url.pathname !== `/mcp/v1/actions/${action}` ||
      request.method !== 'POST' ||
      !ACTIONS.has(action)
    )
      throw new Error(
        'This Unstoppable connection permits portfolio reads only.',
      );
    return fetch(`${configured.url}/${action}`, {
      method: 'POST',
      redirect: 'manual',
      signal: request.signal,
      headers: {
        Authorization: `Bearer ${configured.token}`,
        'X-Unstoppable-Authorization':
          request.headers.get('Authorization') ?? '',
        'Content-Type': 'application/json',
      },
      body: await request.text(),
    });
  };
}
