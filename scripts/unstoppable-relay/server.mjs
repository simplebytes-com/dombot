import http from 'node:http';
import { timingSafeEqual } from 'node:crypto';
import { pathToFileURL } from 'node:url';
export const PREFIX = '/_dombot-registrar';
const ACTIONS = new Set(['ud_portfolio_list', 'ud_domain_get']);
export function createRelay(token, upstreamFetch = fetch) {
  if (!token || token.length < 32)
    throw new Error('Relay token must have at least 32 characters');
  return http.createServer(async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const supplied = Buffer.from(req.headers.authorization ?? ''),
      expected = Buffer.from(`Bearer ${token}`);
    if (
      supplied.length !== expected.length ||
      !timingSafeEqual(supplied, expected)
    ) {
      res.writeHead(401).end();
      return;
    }
    if (req.method === 'GET' && req.url === `${PREFIX}/health`) {
      res
        .writeHead(200, { 'Content-Type': 'application/json' })
        .end('{"ok":true}');
      return;
    }
    const action = req.url?.slice(PREFIX.length + 1);
    if (
      req.method !== 'POST' ||
      req.url !== `${PREFIX}/${action}` ||
      !ACTIONS.has(action)
    ) {
      res.writeHead(403).end();
      return;
    }
    const authorization = req.headers['x-unstoppable-authorization'];
    if (
      typeof authorization !== 'string' ||
      !authorization.startsWith('Bearer ud_mcp_')
    ) {
      res.writeHead(400).end();
      return;
    }
    try {
      let size = 0;
      const chunks = [];
      for await (const chunk of req) {
        size += chunk.length;
        if (size > 1024 * 1024) {
          res.writeHead(413).end();
          return;
        }
        chunks.push(chunk);
      }
      const response = await upstreamFetch(
        `https://api.unstoppabledomains.com/mcp/v1/actions/${action}`,
        {
          method: 'POST',
          redirect: 'manual',
          signal: AbortSignal.timeout(90000),
          headers: {
            Authorization: authorization,
            'Content-Type': 'application/json',
          },
          body: Buffer.concat(chunks),
        },
      );
      const body = Buffer.from(await response.arrayBuffer());
      if (body.length > 2 * 1024 * 1024) {
        res.writeHead(502).end();
        return;
      }
      res
        .writeHead(response.status, { 'Content-Type': 'application/json' })
        .end(body);
    } catch {
      res
        .writeHead(502, { 'Content-Type': 'application/json' })
        .end('{"error":"Registrar relay request failed"}');
    }
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href)
  createRelay(process.env.RELAY_TOKEN).listen(8080, '0.0.0.0');
