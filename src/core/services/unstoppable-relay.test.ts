import { afterEach, expect, it, vi } from 'vitest';
import {
  configureUnstoppableRelay,
  unstoppableRelayFetch,
} from './unstoppable-relay';
afterEach(() => {
  configureUnstoppableRelay();
  vi.unstubAllGlobals();
});
it('sends only portfolio reads to the configured HTTPS relay', async () => {
  const fetcher = vi.fn(async () => new Response('{"domains":[]}'));
  vi.stubGlobal('fetch', fetcher);
  configureUnstoppableRelay(
    'https://relay.example.com/_dombot-registrar',
    'relay-secret',
  );
  const read = unstoppableRelayFetch()!;
  await read(
    'https://api.unstoppabledomains.com/mcp/v1/actions/ud_portfolio_list',
    {
      method: 'POST',
      headers: { Authorization: 'Bearer ud_mcp_test' },
      body: '{"limit":1}',
    },
  );
  expect(fetcher).toHaveBeenCalledWith(
    'https://relay.example.com/_dombot-registrar/ud_portfolio_list',
    expect.objectContaining({
      headers: expect.objectContaining({
        Authorization: 'Bearer relay-secret',
        'X-Unstoppable-Authorization': 'Bearer ud_mcp_test',
      }),
      body: '{"limit":1}',
      redirect: 'manual',
    }),
  );
  for (const url of [
    'https://api.unstoppabledomains.com/mcp/v1/actions/ud_dns_records_update',
    'https://other.example.com/mcp/v1/actions/ud_portfolio_list',
  ])
    await expect(read(url, { method: 'POST', body: '{}' })).rejects.toThrow(
      'portfolio reads only',
    );
  expect(fetcher).toHaveBeenCalledTimes(1);
});
