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

Registrar connections and the DD portfolio migration were completed separately
after deployment. Domain transfers remain separate registrar operations.

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

The Dynadot key now additionally allows `set_renew_option`, explicitly requested
for auto-renew toggles. Its Domains scope is Custom: the original 15 read commands
plus this one write command; Account and TLDs remain Read. Other write and admin
commands remain disabled. Dynadot advises allowing 10 minutes for permission
updates to propagate. Saving this scope does not change any domain's renewal setting.

Porkbun uses a dedicated read-only API key and secret. Connection and portfolio
sync were verified directly from the Worker without a proxy. Listing domains did
not require enabling the account-wide domain API-access toggle.

The current deployment uses a shared password with 30-day signed sessions and
per-IP login throttling, not MFA. MCP stays disabled. All D1 document values are
application-encrypted, but a deployment administrator can access the runtime keys.
Protect GitHub and Cloudflare access accordingly. Cloudflare Access with MFA is a
recommended next hardening step; it has not been enabled.

Spaceship was connected and its read-only scopes verified in the registrar dashboard.
Production dependency audit on 2026-10-15 reported no known vulnerabilities
(`npm audit --omit=dev`); this does not establish that the application is vulnerability-free.

## DD migration

The 2026-10-15 migration used DD's Backup CSV and Sales CSV plus the displayed
appraisal history. `scripts/prepare-dd-migration.py` prepares normalized rows;
it never applies them. The supported `previewDomainImport` and `importDomains`
APIs performed the migration after a full private backup and stale-state check.
Financial amounts retain DD's USD denomination. Atom and Broker statuses map to
folders, while sold/dropped names go to Archive. Registrar-synced data stays
authoritative; only imported active names receive DD renewal-price overrides.

Unsupported appraisal, commission, net-sale and installment details are dated
notes. LTO sale amounts are contract totals, not verified receipts. Actual drop
dates are unavailable in the export and are identified as such in the notes.
Imported auto-renew state is unknown; the migration does not mutate registrars.
Read-back verification compared every mapped field and confirmed that repeating
the preview makes no changes. Source exports, audit artifacts and full backups
are private files outside the repository; full backups contain credentials.

Imported domains are snapshots until a supported account reports them. Missing
registrars and names absent from connected accounts retain review alerts. Live
appraisal comparisons, marketplace rules and installment accounting have no
native equivalent; DD has not been shut down. Existing sync settings were kept.
