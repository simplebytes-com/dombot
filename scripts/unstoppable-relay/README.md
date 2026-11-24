# Unstoppable portfolio-read relay

Production's Unstoppable API requests receive HTTP 418 directly from the
Cloudflare Worker; the same key succeeds from the workstation and the existing
DomainDetails server. This relay supplies ordinary server egress for two reads:
`ud_portfolio_list` and `ud_domain_get`. All other paths and methods are rejected.
It is not an open proxy and cannot send registrar writes.

The dedicated service lives in `/opt/dombot-unstoppable-relay` on the existing
DomainDetails server, on Docker's `coolify` network. Traefik routes only
`https://api.domaindetails.com/_dombot-registrar/` to it using the existing TLS
certificate; other API routes retain their existing service. No host port is
published. The container runs read-only with all capabilities dropped.

The service uses `node:22-alpine`, mounts `server.mjs` read-only, and reads a
random `RELAY_TOKEN` from a private `relay.env`. It retains no registrar key:
each authorized request carries that account's key over HTTPS and the relay
forwards it only to Unstoppable's fixed HTTPS API origin. Payloads and headers
are not logged. The runtime compose file and recovery artifacts are private in
`Creds/dombot-reconciliation-2026-11-24` outside Git.

Worker secrets `DOMBOT_UNSTOPPABLE_RELAY_URL` and
`DOMBOT_UNSTOPPABLE_RELAY_TOKEN` select this route. With neither configured,
upstream direct behaviour is unchanged. With it configured, Unstoppable's
nameserver/privacy/lock/DNS write calls fail explicitly as read-only.

Update the service by copying `server.mjs` to that directory and running
`docker compose -f relay-compose.json restart`. Roll back by restoring the
prior script, or stop the dedicated compose service; other containers and
routes are independent. Do not remove the relay while production relies on it.

Tests verify authentication, rejection of writes and arbitrary targets, and
forwarding only the two allowed reads. Live verification must additionally
check an authenticated portfolio response, account sync and history retention.
