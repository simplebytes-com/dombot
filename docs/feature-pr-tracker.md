# Dombot feature PR tracker

Created: 2026-10-15

Track proposed improvements for replacing the DD portfolio. These are planned
PRs; no GitHub PRs have been opened for them yet.

## PR 1: For-sale checkbox, filter, and renewals view

Status: Implemented on `feat/for-sale-portfolio`; PR pending
PR link: Pending

- [x] Add a per-domain **For sale** checkbox, independent of registrar, folder,
  ownership status, and whether a BIN price is entered.
- [x] Persist the flag across registrar syncs and account transfers.
- [x] Support bulk changes to the flag.
- [x] Add a domain-list filter: **All / For sale / Not for sale**.
- [x] Add a dedicated **For sale** view in Renewals, showing renewal costs,
  upcoming expiry dates, and monthly totals for only those domains.
- [x] Include the flag in CSV import/export and full backups.
- [x] Verify that changing this checkbox only updates portfolio metadata;
  it does not publish or remove marketplace listings.

Decisions to resolve:

- Existing and newly synced/imported domains default to not for sale.
- Renewals includes All domains, For sale, and Not for sale views.

Acceptance: marking a domain For sale makes it appear in the matching filter
and renewal view; clearing it removes it from both. Counts and costs agree,
and the setting survives sync and backup/restore.

## PR 2: Appraisals using provider API keys

Status: Planned  
PR link: Pending

- [ ] Research major appraisal providers with an officially available API.
  Initial candidates to assess: GoDaddy, EstiBot, Atom, Humbleworth, and
  Appraise.net. This list does not imply that each currently offers API access.
- [ ] Record each provider's API availability, access requirements, pricing,
  rate limits, and permitted use before selecting integrations.
- [ ] Allow the user to supply an API key for each supported provider and test
  its connection. Store keys encrypted and keep them out of logs and exports
  intended for sharing.
- [ ] Fetch appraisals for an individual domain and selected domains in bulk.
- [ ] Show provider, valuation, currency, appraisal date, and any available
  range or confidence score.
- [ ] Preserve appraisal history and distinguish stored results from newly
  fetched results.
- [ ] Provide a comparison view across providers without treating appraisals
  as asking prices or guaranteed sale prices.
- [ ] Handle rate limits, partial failures, and chargeable requests clearly.
- [ ] Include appraisal history in backups and provide a data export.
- [ ] Plan a structured import of the DD appraisal history currently preserved
  in dated domain notes and the private migration backup.

Decisions to resolve:

- Which providers can be supported with the user's available API access.
- Manual refresh initially versus optional scheduled refresh, with cost limits.
- Whether provider comparison belongs on each domain, a dedicated Appraisals
  page, or both.

Acceptance: a configured provider can return and save a timestamped appraisal;
errors are visible without losing earlier results, and keys remain confidential.

## Progress log

- 2026-10-15: Recorded both PR proposals. Implementation has not started.

- 2026-10-15: Implemented PR 1 in separate checkbox, filter, and renewal-view commits. Appraisals remain planned.
