# Meeting scheduling context audit — 2026-10-09

## Prerequisite migration-drift check

The previously pending final Kanban migration-drift rerun was completed during dev-advaith integration. Backend commit `da6780216cb9a2b618f12b161717e708c9e2d882` includes the final Kanban handler reorganization. The drift test passed against the newly created empty disposable `crusource_pull_final_drift` database: **1 passed in 20.48 seconds**. The later complete backend validation also passed `alembic check`. The [Kanban audit](sales-kanban-loading-audit-2026-10-09.md) now records this follow-up; its older pending statement is historical.

## Confirmed root cause

Opening Schedule Meeting on the running localhost Meetings page triggered `GET /api/v1/meetings?skip=0&limit=100000`. `MeetingOverviewTab` mounted `useMeetings()` solely to run the client-side `analyzeScheduleContext` after form validation. The imported workspace showed 35,445 visible meetings. The broad request was unnecessary before a proposed time was submitted, and historical records outside its overlap/day context were unnecessary for the advisory.

This observation establishes the attempted bulk read; no successful before-response byte count was captured. It should not be represented as a measured 35,445-row download.

## Implementation

- Added the read-only `POST /api/v1/meetings/schedule-context` use case, using a validated query body consistent with other existing POST read APIs. The route delegates to a dedicated handler and repository.
- Reused existing `apply_scope` through `scoped_meetings`, module permission guards and response-field ceilings. Hidden start time, end time or status denies the advisory rather than exposing derived counts. No role/team/tenant access was broadened.
- SQL selects compact scalar fields, a full conflict count, up to 40 conflicts per page (maximum 100), and at most one nearest previous/next meeting on the proposed day. No attendee/action-item collections or full Meeting entities are hydrated. Strict overlaps include meetings that started on previous days; cancelled meetings and the edited meeting are excluded. Stable ID ties support continuation. Completed records remain eligible as in the previous advisory.
- The form no longer mounts a bulk meeting query. A focused TanStack infinite query runs only after valid submission; subsequent conflict pages are loaded explicitly. The modal displays the complete conflict count and supports continuation and retry without discarding already loaded conflicts.
- Kept the existing transition warnings and explicit scheduling confirmation. A failed advisory request prevents silent saving. Create-only users retain the previous behavior when they have no meeting-view permission; backend write authorization remains authoritative.
- Query keys include start/end, day timezone and excluded meeting ID. Checks use zero stale time so submitting a proposal checks current data. Existing browser-local advisory day boundaries and existing visible-calendar scope were preserved; this does not introduce a new assignee-specific visibility policy.

The endpoint performs no business writes. No migration or new index was added. The existing `(org_id, start_time, end_time)` index is available, but exact counts, scoped filters, offset continuation and neighbor sorting still require database work. This is bounded materialization, not a concurrency or constant-time query claim. Rechecking an identical proposal may refetch explicitly loaded conflict pages; this is distinct from loading the entire meeting dataset on form mount.

## Browser observations

After the user restarted the backend without reload:

| Scenario | Observation |
| --- | --- |
| Open Schedule Meeting | No meeting-data requests; form rendered normally |
| Read-only context check against imported data | HTTP 200; seven conflicts, two neighbors; **2,661 decoded JSON bytes** |
| Close form | Returned to the Meetings list |
| Meetings page 2 | HTTP 200; `skip=25&limit=25`; exactly 25 rows, full total 35,445; 43,505 decoded JSON bytes |

The context endpoint check was a direct authenticated read from the browser. Form save/confirmation/error scenarios were exercised with isolated fixtures, not mutations of imported records. The fixture mounts actual form, services and query hooks under React Strict Mode, verifies no context read on mount, 40-row continuation through 125 conflicts, full counts, nearest neighbors, excluded edit ID, next-page failure/retry, confirmation before save and failed-read protection. It is registered in frontend CI.

## Validation

Focused backend regressions: **14 passed**, covering bounded scalar reads and four SQL statements, continuation, strict/overnight overlap, cancelled/excluded records, nearest neighbors, DST boundaries, invalid inputs, all three roles, team/tenant isolation, hidden fields and module denial. TypeScript and the focused Chromium regression passed.

Complete CI validation passed and is recorded under workspace `.worktrees/meeting-schedule-20261009/` (`frontend-results.txt`, `backend-results.txt` and individual logs). The frontend used an isolated snapshot of all 11 changed/new files, a clean lockfile install and safe dummy API/OAuth build configuration. All current workflow checks passed, including formatting, full lint (1,491 warnings, zero errors), unit/spreadsheet/public/AI checks, every registered browser regression, production build, TypeScript and dependency audit. The snapshot's 11 files were compared with the primary checkout after validation and matched.

Backend Ruff, compilation, committed migrations, full pytest (**1,892 passed / 23 skipped**, 1,928 warnings), required Redis (**33 passed**), webhook/production PostgreSQL (**54 passed**), remaining PostgreSQL regressions (**10 passed**), and `alembic check` all passed. The final migration-drift check was run again for this implementation against the untouched default `postgres` database in the newly created disposable test container, distinct from the database used by other checks: **1 passed in 22.28 seconds**. It asserts the database is empty before migrating. No local application, stage or production database was used for these checks.

The endpoint is additive; a later rollout must make it available on the backend before deploying the new frontend. Complete deployment/environment verification is separate from these local CI checks.

The disposable test containers and their volumes were removed after validation. Graphify rebuilt its artifacts with **23,115 nodes / 64,330 edges / 1,093 communities**. It still returned exit code 1 with coverage warnings for optional parser dependencies, partial TSX extraction and temporary pytest cache access; the successful rebuild is not represented as a clean command exit. Source changes remain local and are preserved in the primary working trees; the isolated frontend validation snapshot is retained for evidence.

## Remaining scope

Notes pagination/batching, dense Calendar volume checks, and concurrency/query-plan/accumulated-export profiling remain separate work. Legacy campaign-detail and per-representative leaderboard limitations remain as previously documented. Local tests do not establish stage behavior. No push or deployment was performed.


### Follow-up: Notes, dense Calendar and scale audit

The [Notes, Calendar and scale audit](notes-calendar-scale-audit-2026-10-09.md) completed parent Notes pagination/batching, dense imported-data Calendar checks and local SQL/concurrency/export-memory profiling. It also optimized Meetings display joins after profiling, and passed both repositories' complete local CI checks, including a fresh final migration-drift rerun. It records remaining year-window payload, accumulated-export memory and production-verification limitations explicitly. This supersedes the corresponding pending work above; it is not a claim that all application performance work is finished.
