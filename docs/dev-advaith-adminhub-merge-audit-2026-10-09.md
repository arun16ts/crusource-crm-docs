# dev-advaith Admin Hub merge audit — 2026-10-09

## Changes and preservation

Fetched `origin/dev-advaith` for the separate frontend/backend repositories and reviewed the incoming commits before merging into local `dev-arun`. Both worktrees were clean; the prior Calendar/export improvements were already committed. Backup branches `backup/pre-advaith-20261009-adminhub` retain the original frontend `e4703db965013fa575672b2fe12185d80b54a7bb` and backend `5a20aef5f38025fc9fbc8b8ab1ed211b51cce9e3`.

Incoming frontend `d7d78ef5a3247801ed005622b14b353bbe33a1c6` contains platform access/session/invitation UI and extracts a presentation-only WorkspaceFrame shared with CRM. Incoming backend `f31673fd1e7bb0231491a61082d160bcd9fd497e` contains invitation/staff lifecycle, durable delivery, normalized-email uniqueness and an additive migration. Neither merge had text conflicts. Existing export registration/model imports/scheduler jobs were retained beside the new platform registrations.

Direct comparison confirms no changes to the Calendar aggregate hooks, export hooks/services and repositories, activity page repositories, shared record scope guard, Leads/Tasks/Meetings/Calls feature components, root font layout or global font CSS. Shared table/shell changes are covered by full existing browser regressions and a separate visual comparison. Both parent histories remain part of the merge rather than replacing our implementation with Advaith's branch.

## Integration corrections

1. The export and platform migrations both descend from `20261008_webhook_receipts`. Added the no-DDL merge revision `20261009_merge_exports_platform`, preserving both original published revision IDs and yielding one upgrade head. Fresh PostgreSQL databases were upgraded from each independent head, retaining an Organization fixture and both export/platform tables; `alembic check` passed on both paths.
2. The incoming User index declaration used `lower(trim(email))`, while PostgreSQL reflects the migrated expression as `lower(TRIM(BOTH FROM email))`. This caused false Alembic drop/recreate drift. A focused shared expression compiler emits PostgreSQL's canonical syntax and portable SQLite trim syntax. The existing unique constraint semantics and original migration remain intact; this does not suppress drift detection or rebuild an application index.
3. Three historical migration-plan tests attempted to run the new data-reading invitation migration through Alembic's offline mock connection. Their original offline SQL checks now stop at the earlier governance/auth merge; the remaining plan is inspected independently. Added upgrade-plan checks from each new branch, and verified actual upgrade/backfill behavior in disposable PostgreSQL. No data migration was bypassed.

## Validation evidence

Evidence is under `.worktrees/advaith-adminhub-20261009/`. Frontend validation used a clean Node 20 lockfile installation in a separate clone. All 61 incoming files matched the primary merged tree after line-ending normalization. Complete workflow checks passed: changed-file formatting, full lint (0 errors / 1,491 warnings), unit/localization, spreadsheets, Loop/public contracts, TypeScript, every existing workflow browser regression including Calendar/export/pagination checks, production build with dummy configuration and dependency audit. Added incoming platform contracts/auth/actual-route browser tests also passed.

The incoming extra CRM-frame test requires a documentation fixture and a production font build. Those prerequisites were supplied in the isolated checkout. A host antivirus-injected Kaspersky script initially failed its strict network assertion; the audit-only harness aborts that identified external script and continues to reject application API/external requests. No application source or system antivirus settings were changed for this workaround. The audit harness uses the actual pre-merge DashboardShell commit as its baseline, rather than the new snapshot's HEAD. Screenshots were byte-identical at 1440 expanded/collapsed, 1024, 768 and 390 pixels. Initial failures are retained alongside the successful rerun in the logs.

The actual Next.js platform-route test uses a separate in-memory fixture API, not local/stage imported records. It passed owner login, invitations/resend/activation/MFA/resume/reset/re-enrollment/revoke/cancel, owner guards, aliases, mobile/collapse and real font/CSS flows. Localhost CRM Calls was separately refreshed: 25 rows, HTTP 200 reads, Instrument Sans, no platform API calls. Global shell reads remain legitimate. Two bounded Calls page reads were observed during refresh; this audit does not represent that as zero duplicate reads or as a new whole-application performance certification.

Final backend checks passed after all corrections: Ruff, compilation, migrations, full pytest **1,958 passed / 49 skipped** (1,933 warnings), required Redis **33 passed**, webhook/production PostgreSQL **58 passed**, remaining PostgreSQL regressions **10 passed**, fresh empty-database migration drift **1 passed in 19.42 seconds**, `alembic check`, and incoming platform PostgreSQL migration/concurrency regressions **25 passed**. Opt-in skips were exercised through the corresponding required/supplementary runs; other skips and existing warnings remain recorded. Initial offline-test/index failures and their successful reruns are retained separately.

Local merge commits: frontend **`d9e13de4`**, backend **`48a98bc`**, both on `dev-arun`. Both original optimization commits and fetched `origin/dev-advaith` commits are verified ancestors of their respective merged HEADs. Both application worktrees are clean. No remote branch was pushed.

Graphify refresh succeeded (exit 0), 23,825 nodes / 66,417 edges / 1,128 communities. Existing optional-parser/partial-TSX/cache warnings remain; source is authoritative.

## Database and deployment boundaries

Only disposable PostgreSQL on port 15432 and Redis on 16379 were used for migrations, drift, locking and regression checks. The existing application database was not migrated or seeded, and imported records were not changed. The new platform migration performs identity preflight and deliberately rejects normalized-email collisions instead of silently rewriting customer identities. Its original safe-rollback guard is retained.

The disposable test containers and volumes were removed after validation; Docker inspection confirmed only the original application PostgreSQL and Redis remained.

Before running the new backend features against an application database, apply the reconciled migration head with the existing migration runner and verify its revision; before deployment, perform the established complete deployment audit. No push, stage/production deployment or application database migration was performed as part of this Git integration.
