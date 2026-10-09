# Year Calendar and scoped export loading audit — 2026-10-09

## Scope and outcome

This follow-up addresses the two concrete loading limitations left by [Notes, dense Calendar and scale profiling](notes-calendar-scale-audit-2026-10-09.md): full CRM records downloaded for Year Calendar indicators, and whole-record arrays retained by explicit browser exports. It does not certify every application interaction or production capacity. Changes are local and uncommitted; nothing was deployed or pushed.

Frontend baseline: `2368c0b022de22aa8bfe45bfe6840dcaf6f14e8e`. Backend baseline: `a14423794bae55a160d340485aff8002dcc1faf4`. Graphify feature tracing was checked against source, including scoped repositories, export accessors, shared API authentication, query hooks, scheduler and worker registration.

## Calendar evidence and changes

The previously tested Year 2022 view loaded 8,632 imported Meetings through 44 full-record pages and one empty Tasks page. The year grid needed daily indicators, rather than every Meeting display object and related collections.

New POST `/api/v1/tasks/calendar-days` and `/api/v1/meetings/calendar-days` return scoped local-date counts, at most 366 entries. Repositories reuse existing tenant, assignment/team and soft-deletion scope and apply the Calendar's title search, active Task rules, time zone and Meeting calendar/source exclusions. Handlers enforce module and source-field visibility. A grouped PostgreSQL query replaces repeated page totals and display hydration for Year only; no new index was justified by this change.

TanStack Query keys include response-affecting parameters; queries execute only in Year for enabled CRM layers. Search is debounced. Meeting counts wait for Google calendar selection/live IDs before deduplication. YearView combines CRM counts with existing Google/SLA indicators. Clicking a day uses the existing detailed day queries. Month, Week, Day and Agenda retain complete visible-window loading.

| Actual localhost scenario | Before | After |
| --- | --- | --- |
| Year 2022 CRM activity reads | 45 full-record page requests | 2 aggregate requests; zero full activity page reads |
| Meeting completeness | 8,632 Meetings, 365 event days | Same 8,632 Meetings and 365 event days |
| Aggregate JSON payload | Not measured in baseline | Tasks 2 bytes; Meetings 5,841 bytes; combined 5,843 bytes |
| Click January 1, 2022 | Detailed records required | Tasks 0/0 and Meetings 15/15, scoped to that day; 200-row limits |

The account has no linked Google integration. Browser-only Google status/calendar/event responses were used to open the existing Calendar UI gate; actual CRM APIs and imported records were used. Those fixtures were removed afterward. This is not evidence of live Google OAuth/provider behavior.

Separately, Google Calendar reads now follow `nextPageToken`; the old single request could silently truncate after 250 events. Partial provider failures and repeated tokens fail visibly rather than return incomplete results. This follows [Google's pagination contract](https://developers.google.com/workspace/calendar/api/guides/pagination). Fixture tests cover 251 events, partial failures and repeated tokens; real integration remains to be verified.

## Export evidence and changes

Ordinary page loading did not invoke the old export helper. Explicit large exports fetched 200-row pages, retained all rows in browser memory and created another CSV/XLSX representation. The previous isolated test measured 27,861,028 additional heap bytes for 100,000 synthetic row objects before file serialization. Response pagination therefore did not bound total browser memory for an export.

Large Leads exports and Tasks, Meetings and Calls exports now create requester-owned jobs through `/api/v1/export-downloads`. The existing scheduler dispatches work outside the HTTP route, using the existing queue mode. Workers read scoped 200-row batches without recomputing the full dataset total for each batch, then write CSV incrementally or XLSX through openpyxl's write-only mode. CSV formula protection and XLSX literal strings are retained. XLSX sheets roll over at Excel's row limit. Filters, selected IDs, columns, formats, date preferences and time zones are validated; field visibility and existing export governance remain enforced. Bounded current-page/loaded-selection Lead exports retain the existing browser path.

An additive `20261009_export_downloads` migration creates durable job receipts; it does not alter imported business tables. It was applied only after checking that the development database was local PostgreSQL on port 5432 at the expected previous revision. No imported business records were edited by this audit.

Artifacts expire after 24 hours. Storage defaults to local development files; ECS/default deployment storage uses private S3, with an explicit configuration override. Downloads pass through the authenticated API rather than public/presigned links. Job ownership, current module/field/team policy and current record visibility are checked. A private ID manifest supports bounded 200-ID visibility checks before sending file bytes, so reassigned or deleted records invalidate a saved export even when role permissions have not changed. This adds legitimate indexed scope checks at download time; exports are not represented as database-free.

The manifest safeguard was added after the first four live downloads. A fresh Calls export was repeated after the final backend restart and passed through the updated route. Fixture regression tests separately verify a saved file is denied after record reassignment. Audit files generated before the safeguard have no manifest and fail closed after the restart; recreate them rather than bypassing authorization.

| Actual localhost export | Records verified in downloaded file | Columns | Artifact bytes |
| --- | ---: | ---: | ---: |
| Tasks, all, CSV | 41,401 | 17 | 6,874,076 |
| Meetings, all, XLSX | 35,445 | 18 | 2,922,314 |
| Leads, filtered by search and active pipeline, CSV | 295 | 25 | 65,476 |
| Calls, filtered/default scope, CSV | 9,201 | 19 | 1,368,357 |

The initial Meetings export used one POST, 13 small status reads and one file GET, with no legacy export-page requests. Its recent-exports panel made a read only when opened and stopped polling when closed. The final Calls export used one POST 202, three status GETs 200 and one download GET 200, preserving the same 9,201 rows and file size. Status polling runs only for explicit pending jobs; the recent panel is inert on page entry and polls only while open with pending jobs. Double invocation reuses the active frontend operation, and the backend idempotency/claim rules prevent duplicate job execution.

A separate serializer-only benchmark wrote 100,000 synthetic rows in 200-row batches: CSV 51,588,903 bytes in 1,624.18 ms with 484,629 traced peak allocation bytes; XLSX 1,055,773 bytes in 12,412.15 ms with 591,678 traced peak bytes. This excludes ORM, process, database and browser memory and is not a production throughput/capacity claim.

## Validation

Evidence is under workspace `.worktrees/calendar-export-20261009/`, including browser/file observations, serializer profile, isolated frontend snapshot and full CI logs. Files containing imported data are audit artifacts, not committed fixtures or report contents.

Frontend local CI parity passed: Node 20 clean lockfile install, corrected changed-file formatting comparison, full lint, unit/localization, spreadsheets, Loop/public checks, every workflow browser regression (including new Year Calendar and export-download tests), TypeScript, production build with dummy configuration and dependency audit. All 21 changed/new primary files matched the validated snapshot after normalizing line endings. Existing warnings/advisory exceptions are retained in the logs; this is not a warning-free claim.

The dense Calendar regression now explicitly covers Month's full 10,000-event completeness/retry behavior, while the new Year regression covers compact counts, Google deduplication, search/layers, error retry and day navigation. Backend fixtures cover all three roles, time-zone boundaries, field restriction, batching/formatting, job ownership/idempotency, formula protection and reassignment denial. Native PostgreSQL tests cover time-zone grouping and concurrent claim exclusion.

Final backend local CI parity passed after the manifest safeguard: Ruff, compilation, migrations, full pytest **1,927 passed / 27 skipped** (1,933 warnings), required Redis **33 passed**, webhook/production PostgreSQL **58 passed**, remaining PostgreSQL regressions **10 passed**, fresh empty-database migration drift **1 passed in 16.48 seconds**, and `alembic check` with no new upgrade operations. Ordinary-suite opt-in skips were exercised by their required service-backed runs; other skips and existing warnings remain in the logs. The fresh drift database was distinct from the migrated regression database, in disposable PostgreSQL on port 15432; disposable Redis used 16379.

Graphify refreshed successfully, exit 0: **23,203 nodes / 64,920 edges / 1,132 communities**. Optional-parser/partial-extraction and historical cache warnings remain; source is authoritative. Browser-only audit fixtures/listeners were removed. Final localhost readiness was HTTP 200 and Calls showed its normal 25-row page. Backend restart briefly caused connection-refused shell requests; the refreshed application recovered and the final export completed normally. An idle five-second browser observation after completion recorded zero export requests.

Both disposable audit containers and their volumes were removed after validation. Docker inspection confirmed only the original application PostgreSQL (5432) and Redis (6379) remained running.

## Remaining limits and rollout requirements

- The browser still buffers the final binary download Blob, although it no longer retains every fetched record and builds the workbook. Extremely large binary downloads may need another delivery design.
- Export reads use existing offset ordering, not a transactionally frozen dataset. Concurrent edits can shift continuation; deep offsets and long-running exports remain scale considerations. This change does not establish million-record capacity or sustained multi-user load.
- Detailed Calendar windows still load all full records in the selected window, and live Google Year data still uses provider event records. Real Google integration remains unverified.
- Legacy campaign-detail compatibility reads and large-team leaderboard aggregation remain documented separate work; they were not silently disabled here.
- Backend migration and compatible API must precede frontend rollout. Shared S3 access for API/workers, IAM get/put/list/delete, queue/scheduler behavior, stage configuration and actual deployed flows require deployment validation. Neither local CI nor localhost readiness proves stage works.
