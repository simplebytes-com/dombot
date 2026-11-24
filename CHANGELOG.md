# Changelog

## 2026-11-24 — Production upgrade preparation

- Adopt upstream 2.2.2 and current main, retaining old fork history and feature branches.
- Use upstream pricing and Sales behaviour; retire the fork's independent for-sale UI as requested.
- Retain legacy for-sale flags and archive retired dropped events in database/full backups; use backup format v10 to prevent silent metadata loss in older builds.
- Back up production and rehearse migration and backup restore against its real data. Preserve deployment documentation and the DD preparation script.

## 2026-11-24 — Upstream review

- Checked out current upstream separately from the Simple Bytes feature branch.
- Documented changes from 1.5.0 through 2.2.2 and current upstream, contribution status, and recommended discussion points for PR #183 and issues #112 and #110.
- Preserved the existing fork checkout and production deployment.
