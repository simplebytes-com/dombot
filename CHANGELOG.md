# Changelog

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
