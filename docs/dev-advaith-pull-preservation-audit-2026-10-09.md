# dev-advaith pull and preservation audit — 2026-10-09

## Integration

Both application repositories started clean on `dev-arun`. Fetched `origin/dev-advaith`, merged in isolated worktrees, validated, then fast-forwarded the primary worktrees. No changes were pushed or deployed. The docs repository was not pulled.

| Repository | Pre-pull commit | Incoming dev-advaith | Final dev-arun |
| --- | --- | --- | --- |
| Frontend | `7e7c856e28ddfe6628d48230ec56793ff3fce1c5` | `0276a54d83c08507648dee964cbaaa602d62d5af` | `3852bdeb7406a6774bb30f842c316a5f4596147a` |
| Backend | `495d740c1332e8cd095c9738e670be918f457974` | `33a6ff4ae16b13c25e04af516a402b38f3d1afd1` | `da6780216cb9a2b618f12b161717e708c9e2d882` |

Both repositories have `backup/pre-advaith-pull-20261009-2` pointing to their pre-pull commits. The merges had no textual conflicts.

Git-blob comparisons verified **426 protected frontend files and 214 protected backend files unchanged**. These cover the previously optimized sales, activity, dashboard, campaign loading, Kanban, pagination, authorization/scope and font/layout paths. This verifies preservation of those paths; it is not a claim that every application interaction has been audited again.

## Integration corrections

- Retained the NextIntl plugin in Next configuration. The incoming configuration had removed it while the root layout still uses `next-intl/server`. Built English and Dutch previews both returned HTTP 200 without the configuration error.
- Changed Alembic logging initialization to `disable_existing_loggers=False`. Full-suite testing exposed scheduler warnings disappearing after migration tests disabled existing loggers. Added a regression assertion to the offline migration tests; the focused reproduction and full suite passed.
- Made the frontend public-knowledge check explicitly support read-only `--frontend-only` validation in frontend CI, where the separate backend repository is absent. The default check still verifies both repositories; standalone writes are rejected. Tested the isolated mode, strict missing-backend failure and write guard.
- Applied required formatting to two incoming frontend files. Normalized the local backend FAQ JSON line endings to match the source for the strict cross-repository check; canonical Git content was unchanged.

Incoming frontend changes chiefly concern Loop AI UI/hooks and markdown rendering. Backend changes include AI handlers, quotas, security, scheduler configuration and durable authenticated webhook receipt handling. These incoming changes were retained.

## Validation

Complete current frontend CI commands passed: clean lockfile installation, changed-file formatting, full lint, unit and spreadsheet checks, Loop AI/public contracts, every browser regression command listed in CI, TypeScript, production build and dependency audit. The preserved sales Kanban browser check and an additional session-startup check also passed. Lint reported 1,493 warnings and no errors; dependency audit reported no vulnerabilities.

Complete backend checks passed: Ruff, compilation, migrations, full pytest (**1,874 passed, 27 skipped**), required real-Redis checks (**33 passed**), webhook/production PostgreSQL checks (**54 passed**), remaining PostgreSQL regression checks (**10 passed**), migration drift against a separate empty disposable PostgreSQL database (**1 passed**), and `alembic check` with no new operations. The full suite reported 1,928 warnings. The first run's seven logging-related scheduler failures were fixed and the complete checks rerun successfully.

Evidence is retained under workspace `validation/advaith-pull-20261009/`: `frontend-results.txt`, `backend-results.txt`, check logs, `preservation.json`, and `local-migration-verification.json`. Tests used disposable PostgreSQL/Redis services, not stage or production services.

## Local application

Frontend dependencies were updated. The local-only additive migration advanced the database from `20261008_chat_response_kind` to `20261008_webhook_receipts`. Counts were unchanged for Leads, Deals, Contacts, Accounts, Tasks, Meetings, Calls, Campaigns and Campaign Recipients. These are database-wide preservation counts, not a user's authorized visibility totals.

After integration, browser refresh on `localhost:3000/dashboard/leads` displayed the authenticated Leads list and its 14,000-record pipeline total. Backend `/health/ready` returned HTTP 200. The isolated production preview also verified English and Dutch pages. No business records were changed by browser verification.

The user-owned backend process must be restarted to load the pulled Python code. A healthy existing process does not prove it has loaded that code. No stage verification or deployment was performed.

## Cleanup and graph

Temporary validation worktrees and this audit's disposable test containers were removed after validation; the user's application services and backup branches are retained. Graphify rebuilt the index (23,073 nodes, 64,218 edges, 1,116 communities). Its command returned status 1 despite writing the updated artifacts: warnings cover missing optional Terraform/SQL parsers, partial extraction of five TSX files, one empty extraction, and access restrictions on temporary pytest caches. An unrestricted retry was also attempted; some pytest cache ACL restrictions persisted. These graph coverage limitations do not replace the passing source, build and test checks. Both graph logs are retained with the validation evidence.
