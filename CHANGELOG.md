# Changelog

## 2026-10-15 — Simple Bytes self-hosting

- Prepared a private, password-protected Dombot Worker and dedicated D1 database in the Simple Bytes Cloudflare account.
- Keep account configuration in ignored local overrides or Cloudflare build variables; credentials remain outside Git.
- Added deployment and update instructions for this instance.
- Deployed Dombot 1.5.0 and verified password authentication and API access control.
- Connected the fork main branch to Cloudflare Builds with typecheck and test gates; disabled preview builds.
- Connected the first GoDaddy account with a dedicated domain-read-only PAT and verified a successful domain sync.
- Documented registrar least-privilege configuration and current authentication limitations.
