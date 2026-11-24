# Changelog

## 2026-11-24 — Marketplace connections

- Record the owner's confirmation that the Afternic USD 10,000 sale of `ovenue.com` is correct; retain Atom's conflicting report only as source history. Production already uses the correct Afternic contract.
- Connect both Spaceship SellerHub accounts and dedicated Atom seller and Afternic accounts; retain the existing registrar credentials.
- Connect Dynadot Marketplace using the existing restricted key; add only the approved `other_registrar_domain_list` read permission and verify successful production sync after provider propagation. Leave Sedo disconnected at the owner's request.
- Prevent overlapping sales reported by different marketplace accounts from creating duplicate ledger events. Preserve the raw provider records and the original imported contract; repair a duplicate sync event on the next sync. An intervening acquisition or dates outside the existing 14-day matching window remain separate sales.
- Apply the same overlap rule to Sales summaries and CSV, so a retained provider report does not reappear as a second contract without a ledger event.

## 2026-11-24 — Sales reconciliation

- Preserve original sale marketplace, method and installment terms from the DD export through the supported sale API and full backups.
- Mark imported payment evidence as unconfirmed, show LTO contracts explicitly, and exclude unconfirmed receipts from profit and ROI. Label monetary summaries as contract values.
- Extend the sales CSV with payment evidence and source installment terms.
- Add a guarded, idempotent DD sales reconciliation script that plans by default, matches existing sale IDs/dates/amounts, backs up and verifies applied changes.
- Restore fees, original venues and contract terms for all eight historical sales; preserve two LTO contracts with receipts unconfirmed. Repeated reconciliation makes zero changes.
- Add an authenticated HTTPS read relay for Unstoppable portfolio sync, because direct requests from the Cloudflare Worker return 418 while the same key works from ordinary egress. Both ends permit only portfolio list and domain-detail reads.

## 2026-11-24 — Production upgrade

- Adopt upstream 2.2.2 and current main, retaining old fork history and feature branches.
- Retain the fork's existing GitHub workflows; upstream's new Claude review and release-workflow changes require OAuth permissions absent from this checkout. Application updates are unaffected.
- Use upstream pricing and Sales behaviour; retire the fork's independent for-sale UI as requested.
- Retain legacy for-sale flags and archive retired dropped events in database/full backups; use backup format v10 to prevent silent metadata loss in older builds.
- Back up production and rehearse migration and backup restore against its real data. Preserve deployment documentation and the DD preparation script.
- Fix intermittent Worker startup/API failures observed during live verification: retain boot values instead of completed-request promises, and release idle request/write queues.
- Deploy and verify 2.2.2 in production: authenticated desktop/mobile UI, startup APIs, preserved data and unauthenticated API denial. Retain pre-upgrade source and data recovery artifacts.

## 2026-11-24 — Upstream review

- Checked out current upstream separately from the Simple Bytes feature branch.
- Documented changes from 1.5.0 through 2.2.2 and current upstream, contribution status, and recommended discussion points for PR #183 and issues #112 and #110.
- Preserved the existing fork checkout and production deployment.
