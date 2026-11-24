import { afterEach, expect, it, vi } from 'vitest';
import { once } from 'node:events';
import { createRelay, PREFIX } from './server.mjs';
let server;
afterEach(async () => {
  if (server) await new Promise((resolve) => server.close(resolve));
});
it('requires its token, denies writes and arbitrary targets, and forwards only read JSON', async () => {
  const upstream = vi.fn(async () => new Response('{"domains":[]}'));
  const token = 'a'.repeat(40);
  server = createRelay(token, upstream);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const root = `http://127.0.0.1:${server.address().port}${PREFIX}`;
  expect((await fetch(root + '/health')).status).toBe(401);
  const headers = {
    Authorization: `Bearer ${token}`,
    'X-Unstoppable-Authorization': 'Bearer ud_mcp_test',
  };
  expect(
    (
      await fetch(root + '/ud_dns_records_update', {
        method: 'POST',
        headers,
        body: '{}',
      })
    ).status,
  ).toBe(403);
  expect(
    (
      await fetch(root + '/ud_portfolio_list?target=https://evil.example', {
        method: 'POST',
        headers,
        body: '{}',
      })
    ).status,
  ).toBe(403);
  expect(
    (
      await fetch(root + '/ud_portfolio_list', {
        method: 'POST',
        headers,
        body: '{"limit":1}',
      })
    ).status,
  ).toBe(200);
  expect(upstream).toHaveBeenCalledTimes(1);
  expect(upstream.mock.calls[0][0]).toBe(
    'https://api.unstoppabledomains.com/mcp/v1/actions/ud_portfolio_list',
  );
});
