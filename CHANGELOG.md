# Changelog

## Unreleased — For sale

- Added a For sale / Not for sale domain filter with counts; clearing it shows all domains and it combines with the existing filters.

- Added a per-domain For sale checkbox and bulk marking, independent of asking price and registrar settings. Existing and new domains default to unchecked.
- Preserve the flag through sync, account moves, CSV import/export and full backups; deleting a domain removes its flag.


## Planned feature tracking

- Added `docs/feature-pr-tracker.md` for the proposed For sale controls and
  renewal view, plus appraisal integrations using provider API keys.

## 2026-10-15 — Simple Bytes self-hosting

- Prepared a private, password-protected Dombot Worker and dedicated D1 database in the Simple Bytes Cloudflare account.
- Keep account configuration in ignored local overrides or Cloudflare build variables; credentials remain outside Git.
- Added deployment and update instructions for this instance.
- Deployed Dombot 1.5.0 and verified password authentication and API access control.
- Connected the fork main branch to Cloudflare Builds with typecheck and test gates; disabled preview builds.
- Connected the first GoDaddy account with a dedicated domain-read-only PAT and verified a successful domain sync.
- Documented registrar least-privilege configuration and current authentication limitations.
- Verified the user-connected Spaceship account sync and read-only key scopes.
- Verified successful Dynadot synchronization with the restricted key after activation; all configured registrar accounts connect directly without a proxy.
- Connected Porkbun with a dedicated read-only key and verified successful synchronization in the live portfolio without a proxy.
- Added only Dynadot's `set_renew_option` write permission to the existing restricted key at the user's request, allowing auto-renew toggles while retaining the previous read permissions.
- Added a preparation-only DD migration script with duplicate, sale reconciliation, date, price, and note-length checks. Live registrar fields take precedence; unsupported financial and appraisal details are retained as dated notes.
- Applied and verified the DD portfolio migration through the supported import API, including acquisition and sale history, prices, notes, and Atom/Broker folders. Retained reconciliation alerts for missing registrar information and domains absent from connected accounts; saved private before/after backups.
