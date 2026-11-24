# Simple Bytes deployment

## 2026-11-24 marketplace setup

Dedicated Atom Seller Marketplace and Afternic keys are stored encrypted in
DomBot. Both Spaceship SellerHub accounts reuse their existing registrar
connections. First completed syncs returned:

| Account | Listings | Provider sale records |
| --- | ---: | ---: |
| Atom ImpactOf | 332 | 3 |
| Afternic ImpactOf | 322 | 3 |
| Spaceship ImpactOf | 145 | 1 |
| Spaceship SimpleBytes | 0 | 0 |
| Dynadot Master | 0 | Not supported by this integration |

These are 799 account listing snapshots across 359 distinct names, not 799
owned domains. Marketplace reads do not replace registrar ownership data.
Julian authorized the dedicated keys, including their provider write scopes;
setup invoked connection tests and read-only syncs, with no listing, pricing,
purchase or delisting actions. Existing provider keys were retained.

Dynadot Master is linked to its existing registrar key. Its initial sync failed
because the restricted key lacked `other_registrar_domain_list`. After Julian
unlocked the account, exactly that read command was added and the provider
confirmed the save. After about eight minutes of API propagation, the
other-registrar read returned all 261 entries and the production sync completed
successfully, with zero active marketplace listings. The 27 registrar-held
domains also reported none for sale. No write command was added. Sedo was explicitly
skipped: the saved partner pair still requires the seller login password.

The provider history exposed two reports of `ovenue.com`: Afternic reports
USD 10,000 on September 21, Atom USD 12,999 on September 23. Both raw reports
are retained as source history. Julian confirmed on 2026-11-24 that Afternic's
USD 10,000 report is correct and Atom's USD 12,999 report is incorrect. This
discrepancy is resolved; the imported Afternic contract remains authoritative
in the ledger. Cross-account overlapping reports now count once in the ledger,
Sales summaries and CSV; a subsequent sync removes a redundant sync event.
Matching uses the existing 14-day window and requires no acquisition between
the reports, so a documented repurchase remains a separate sale.

Production retains all eight original sales, their IDs, amounts, fees and
imported terms: gross contract USD 111,590; fees USD 19,497.50; net contract
USD 92,092.50. Afternic supplies payout dates for `ovenue.com` and `swarmos.com`;
the remaining six records still have unconfirmed receipts. All unrelated
namespaces, including registrar credentials, notes, asking prices, folders,
imports and legacy flags, compare equal to the pre-connection backup.

Validation: 1,811 tests pass (one skipped), four security regression tests
pass, typecheck and scoped ESLint pass. Production desktop, reload and mobile
Sales checks and a downloaded CSV confirm eight rows, one `ovenue.com` and
the exact original contract totals. Markets desktop, reload and mobile checks
also pass with no browser/API errors. All five market accounts report complete
syncs without errors. Manually deployed Worker version:
`1b45a6ec-74b4-4f05-b71f-3c440ae06212`; application commit `5e0cb82`.
Private before/after full backups and browser evidence are in
`../Creds/dombot-marketplaces-2026-11-24/`. Full backups contain credentials.

## 2026-11-24 registrar and sales reconciliation

Unstoppable is connected as ImpactOf and synced successfully: 194 live ICANN
domains, with 174 imported records taken over by sync. Twenty of the live names
were not in the old imported set. The UI shows 428 Owned and 11 Archive.
All 97 folder assignments, asking prices, historical acquisition events and
17 notes remain intact. Imported records fall from 217 to 43: 15 older
Unstoppable records not returned by this account, 17 Atom, eight Spaceship and
three unknown-registrar names. No unmatched record was deleted or relabeled.
The private `remaining-imported-domains.csv` identifies the records to review.

Direct Worker requests to Unstoppable returned HTTP 418, while the same key
worked locally and from the existing server. A dedicated authenticated HTTPS
relay permits only portfolio-list and domain-detail reads; see
`scripts/unstoppable-relay/README.md`. The API key was created with Julian's
explicit approval because the provider does not offer read-only key scopes.
Its broad provider permissions do not expand the relay's two allowed reads.
Unstoppable registrar writes through this connection are intentionally denied.

Restored fees, venue, sale method and exported LTO terms on all eight historical
sales through `setSale`, preserving sale IDs, dates, amounts and unrelated data.
Gross contract value is USD 111,590; net contract value USD 92,092.50; recorded
fees USD 19,497.50. Both LTO contracts and the other imported sales have
unconfirmed receipts. They are not presented as confirmed cash or included in
profit/ROI. Source installment amounts are retained as exported, without
assuming payments occurred. Re-running the reconciliation plans zero changes.

The source CSV, before/after full backups, private relay runtime config, key,
sync reconciliation and browser artifacts are outside Git in
`../Creds/dombot-reconciliation-2026-11-24/`. Temporary copied browser cookies
were removed after setup. Full backups contain credentials.

Validation: typecheck and ESLint pass; 1,807 tests pass (one skipped), including
relay authentication/read-only routing, source contract handling and backup
round trips. Four security regression tests pass. Final production browser
checks cover Domains, Renewals, Sales, Settings, reload and mobile, with no
page errors or failed requests on the completed configuration. A failed secret
update briefly left the relay configuration incomplete; the missing token was
set and all checks were repeated after recovery. The existing DomainDetails
API health remained successful. Worker version after secret configuration:
`61efdf04-c6bb-47b2-8346-905afdc66d58`; application commit `52b635d`.

At this registrar-reconciliation checkpoint marketplace accounts were still
unconfigured; see the subsequent marketplace setup above. The Unstoppable registrar connection
does not create marketplace listing feeds. Listings are fetched through each
connected market API on manual or scheduled sync and compared with stored
asking prices. The current scheduled interval is seven days, checked by the
Worker's hourly cron; this is not an independent public-web listing search.

## 2026-11-24 upgrade

Deployed and verified on 2026-11-24. Current Worker version:
`af8236b2-3cce-4031-b57c-9f1ebe8ae383`; application/fix commit `94a2208`.
Fork main contains the upgrade. The initial deployment exposed intermittent
cross-request promise failures; the follow-up fix caches completed boot data
and releases idle request/write queues rather than retaining request promises.

Final validation: TypeScript and ESLint pass; 1,802 unit tests pass (one skipped)
and four security regression tests pass. Production Chrome/Playwright checks
cover Domains, Renewals, Sales, Settings, reload and a 390px viewport, with
no page errors or failed requests on the fixed build. Three rounds of the five
startup API reads passed; the live tail recorded 38 fixed-build requests with
no errors or 5xx responses. Unauthenticated API access returns 401.

Post-deployment full-backup comparison confirms all accounts/credentials,
imported domains, notes, prices, folders and old flags are unchanged. All
619 pre-upgrade events are retained across active and legacy namespaces.
The UI now shows 408 Owned and 11 Archive versus the old 410 Active and
12 Archive: two imported names are over 90 days past expiry and upstream
classifies them as archived; the three retired dropped-only records are
preserved in the legacy archive rather than rendered as domain rows.

The old production source is tagged remotely as
`backup/production-before-2.2.2-2026-11-24`. Existing sales feature branches
remain unchanged. The fork retains its existing GitHub workflows because the
available Git credential cannot publish upstream's new workflow changes.

The production upgrade adopts upstream 2.2.2 plus upstream main through
`5c0711d`. The old fork main and all sales-analytics feature branches remain
in Git history; the original checkout remains on `feat/sales-analytics`.

At Julian's request the UI uses upstream behaviour: Pricing → For sale means
an asking price exists. The old independent checkbox, its bulk actions and
the scoped renewal lists are retired. The custom Sales dashboard was never
deployed; upstream's Sales page is used instead.

The only application customization retained is backup compatibility:
`domain-for-sale` stays stored/exported with no UI or pricing effect, and
the three old `dropped` events are archived in `legacy-domain-events`
before upstream schema migration 5 removes them from the active ledger.
Full backups use format v10, accept v1–v9 input, and require this compatible
fork to restore without losing legacy metadata. Stock upstream v9 refuses
v10 files. The original dropped decisions are recoverable from that archive,
but no longer drive ownership state in the upstream UI.

Pre-upgrade encrypted D1 SQL, the full application bundle, the existing Worker
version metadata, and verification logs are retained privately in
`../Creds/dombot-upgrade-2026-11-24/`. Full bundles contain registrar secrets;
do not add them to Git. Pre-upgrade Worker version:
`c183b8f8-84b5-4dd7-8955-a741dac14b89`.

Rehearsal against the actual production bundle preserved all five registrar
accounts and credentials, 217 imported domains, 17 notes, 354 legacy flags,
prices and folders. All 619 events remained recoverable: 616 active and 3
archived. A full-backup restore was also rehearsed without registrar calls.

Code rollback alone does not restore schema semantics. If rollback is needed,
restore the pre-upgrade data snapshot together with the pre-upgrade Worker,
after checking for new user changes that must be retained.

## Historical deployment record (1.5.0)

This fork hosts the private Simple Bytes Dombot instance. Upstream is
https://github.com/aoxborrow/dombot. The fork includes the For sale feature on top of upstream
commit `3c3831cefae70e750bc566bcecb52c2d12ce37ad`, submitted upstream as PR #182.

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

## 2026-10-16 for-sale release

Merged persistent sale flags, bulk controls, domain filters, and scoped renewal views. Validation: 944 tests passed (1 skipped), type checks, scoped lint, and production build. A private full backup was taken before deployment. Existing domains default to unchecked; this release does not infer marketplace listing status.

DD snapshot note blocks were subsequently removed from all 365 migrated domains, preserving 17 original notes and structured purchase/sale records. Historical appraisals remain in the private migration backup. Atom Premium is the remaining portfolio folder; Broker was removed and its domains left ungrouped.
