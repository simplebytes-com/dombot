# Simple Bytes deployment

This fork hosts the private Simple Bytes Dombot instance. Upstream is
https://github.com/aoxborrow/dombot. Application code is unchanged from upstream
commit `3c3831cefae70e750bc566bcecb52c2d12ce37ad`.

## Configuration

Worker and database names: `dombot`. Authentication mode: `password`.
Cloudflare account/database identifiers belong in build variables or ignored
`wrangler.local.json`; never commit credentials, data exports, or registrar keys.
Set `DOMBOT_SECRET` and `DOMBOT_PASSWORD` as Worker secrets. Back up the root key:
a database export cannot be decrypted after that key is lost.

## Build and deploy

Use the existing Worker and D1 database, rather than the Deploy button.

- Build: `npm run typecheck && npm test && npm run build`
- Deploy: `npm run deploy`
- Build variables: `DOMBOT_D1_DATABASE_ID` and `ELECTRON_SKIP_BINARY_DOWNLOAD=1`.
- Worker and database names use the upstream default `dombot`.
- Preview builds are disabled.
- Git branch: `main`.

Deployment applies D1 migrations before publishing. Sync an upstream release into
the fork, review the diff, and push only when ready to deploy. Native Cloudflare
builds run the validation commands above before deploying. Keep custom integration
work outside upstream application files where practical.

## Verification and recovery

Check the live login page, authenticated empty portfolio, unauthenticated API
rejection, and the current deployment revision. Before data/schema upgrades,
export an encrypted full backup and retain the matching application revision.
Reverting code does not necessarily reverse a database migration.

Initial setup does not import the old DD portfolio, attach registrar credentials,
or perform domain transfers. Those are separate migration steps.

## Live instance

https://dombot.simplebytes-com.workers.dev (Dombot 1.5.0).

Connected `simplebytes-com/dombot` main to Cloudflare Builds on 2026-10-15.
Initial local validation: typecheck and 933 tests passed (one skipped); production
password login, authenticated empty cache, and unauthenticated API denial verified.

## Registrar connection policy

Use a dedicated key per registrar account and read-only scopes for portfolio
tracking. GoDaddy uses `domains.domain:read`; the initial token has a 90-day
lifetime. Spaceship requires domain and DNS read scopes. Dynadot requires account
read for its connection test as well as domain read; pricing may need additional
read scopes or remain unavailable with restricted credentials. Do not grant
renewal, purchase, transfer, or DNS write permissions just to populate the portfolio.

The current deployment uses a shared password with 30-day signed sessions and
per-IP login throttling, not MFA. MCP stays disabled. All D1 document values are
application-encrypted, but a deployment administrator can access the runtime keys.
Protect GitHub and Cloudflare access accordingly. Cloudflare Access with MFA is a
recommended next hardening step; it has not been enabled.

Spaceship was connected and its read-only scopes verified in the registrar dashboard.
Production dependency audit on 2026-10-15 reported no known vulnerabilities
(`npm audit --omit=dev`); this does not establish that the application is vulnerability-free.
