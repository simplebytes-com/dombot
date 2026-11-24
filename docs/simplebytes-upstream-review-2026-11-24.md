# Simple Bytes upstream review — 2026-11-24

## Checkout status

- Tool: DomBot, upstream https://github.com/aoxborrow/dombot.
- Our instance: https://dombot.simplebytes-com.workers.dev (address from deployment documentation; runtime version not checked in this review).
- Our fork: https://github.com/simplebytes-com/dombot.
- Fetched both remotes and pulled the existing `feat/sales-analytics` branch with `--ff-only`; it was already current with its fork remote.
- Latest upstream checked out separately in `../dombot-upstream`, branch `review/upstream-2026-11-24`, based on `5c0711d` (2026-11-16). `git pull --ff-only` confirmed current.
- Latest published release: 2.2.2, 2026-11-10. Original checkout package version: 1.5.0.
- Original feature branch has 21 unique commits; upstream has 673 unique commits. A deployment upgrade needs reconciliation of the custom features and a data backup. This review does not deploy, push, close PRs, or post comments.

## What changed since our base

- 2.0: Afternic, Sedo and Atom marketplace integrations; listing, repricing and delisting; sale transfer steps; new Sales tab; preferred-currency totals using ECB monthly rates; pricing filters; revised Owned/Archive handling; marketplace and sales MCP tools.
- 2.1: Unstoppable Domains support, scrubbed local error logs, Namecheap fixes, large Afternic account sync fixes, longer API timeouts, clearer sync failures and currency display.
- 2.2: Spaceship SellerHub, Dynadot marketplace, copying asking prices from listings, Namefi registrar, and bulk selections restricted to visible rows.
- 2.2.2: fixed-IP proxy writes no longer fail with ECONNRESET.
- Changes after the release include folder ordering, filter-chip clearing, a registrar-default DNS option, registrar-client 1.3.0, and review workflow changes.

Sources: [2.0](https://github.com/aoxborrow/dombot/releases/tag/v2.0.0), [2.1](https://github.com/aoxborrow/dombot/releases/tag/v2.1.0), [2.2](https://github.com/aoxborrow/dombot/releases/tag/v2.2.0), [2.2.2](https://github.com/aoxborrow/dombot/releases/tag/v2.2.2), and fetched upstream Git history.

## Our discussions and proposed comment points

No open issues authored by or involving `julianengel` were returned; our outstanding contribution is a pull request. No open issues or pull requests were returned in our fork.

### Priority 1: [PR #183 — Sales analytics](https://github.com/aoxborrow/dombot/pull/183)

Open, conflicting, no submitted reviews or inline review comments. Last discussion update: 2026-10-30.

- Michael asked for purchase date and purchase cost in CSV, export beside date filters, and definitions beside metrics; he explicitly asked Julian to help with definitions.
- Aaron built a new Sales page incorporating some of the proposal, then chose preferred-currency reporting via [#220](https://github.com/aoxborrow/dombot/pull/220), merged 2026-10-31.
- Current source confirms CSV includes `Acquired on`, `Cost`, `Profit` and `Days held` (`src/shared/sales.ts`). The export button remains in the page header (`src/renderer/pages/Sales.tsx`), so the requested placement has not been adopted.
- Recommended response: acknowledge the new Sales page and currency approach; provide metric definitions; propose carrying the remaining work into #112 and #110 rather than rebasing the old dashboard wholesale. Confirm whether Aaron wants #183 closed as superseded after the remaining scope is tracked.

Suggested definitions to discuss, rather than claims about current calculations:

| Metric | Proposed meaning |
| --- | --- |
| Gross sale value | Full contract price before fees; separate pending contracts from completed sales. |
| Confirmed receipts | Money actually received, excluding scheduled or overdue payments. |
| Net receipts | Confirmed receipts minus fees actually paid. |
| Realized profit | Net receipts minus acquisition and recorded holding/renewal costs, only when payment and cost coverage meet the stated completion rule. |
| ROI | Realized profit divided by the corresponding complete recorded cost basis; exclude missing or zero cost and show coverage. |
| Holding period | Days from the acquisition starting this holding to sale; a buyback starts a new holding. |
| Opening-cohort sell-through | Names held at the period start that sell during the period, divided by names held at the start. New acquisitions are excluded from both counts. |

### Priority 2: [#112 — Dashboard: needs attention and financials](https://github.com/aoxborrow/dombot/issues/112)

Open; no comments. Explicitly credits #183 and already records its remaining scope: renewals in cost basis, monthly trends, folder breakdown, receipts/installments, sell-through and definitions.

- Recommend the opening-cohort sell-through definition above, with a clear label distinguishing it from upstream's current listed-plus-sold formula.
- Recommend cash reporting based on confirmed payments, with contract value separate; keep unknown costs unknown and show coverage counts.
- Identify history completeness as a limit: first sync is not an acquisition date, and absent renewal records do not prove zero spend.
- The issue still describes #213 as open, although the released Sales implementation now exists. A comment can request that dependency/status text be refreshed.

### Priority 3: [#110 — Installment terms on sales](https://github.com/aoxborrow/dombot/issues/110)

Open; no comments. The proposal derives receipts from a schedule and does not store individual payments. Late/missed payments are only notes.

- Recommend distinguishing expected receipts from confirmed receipts. A due date passing does not establish that cash arrived; schedule-only cash totals cannot substantiate the confirmed-receipts definition from #183.
- Request a confirmation/reconciliation mechanism or explicit estimated labeling before installment schedules feed cash reports.

### Optional: [PR #182 — For-sale tracking](https://github.com/aoxborrow/dombot/pull/182)

Closed unmerged on 2026-10-29 in favour of [#209](https://github.com/aoxborrow/dombot/pull/209). Aaron thanked Julian and said it prompted that work. No action required. An acknowledgment can mention that our separate flag supported names intended for sale before they have asking prices; upstream now derives For sale from pricing, so those semantics differ.

## Other open upstream reports worth checking during an upgrade

- [#291](https://github.com/aoxborrow/dombot/issues/291): uppercase marketplace names fail to match sold records.
- [#290](https://github.com/aoxborrow/dombot/issues/290): Archive rows reportedly remain visible after returning to Owned.
- [#289](https://github.com/aoxborrow/dombot/issues/289): Listings shows all owned names although its badge counts listed names.

These are other users' reports, not reproduced against our portfolio. Comment only with a verified reproduction or new evidence.

## Verification limits

Reviewed live GitHub issues, PR discussion/review metadata, release notes and fetched source. Confirmed the original working tree remains clean. No application code was changed, no tests were needed for this documentation-only review, and no browser/runtime or production data verification was performed.
