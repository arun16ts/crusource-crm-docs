# Bulk-data pagination audit: local development, 2026-10-08

This follows the [initial network/font audit](performance-audit-2026-10-08.md). The user imported bulk Sales and Activities data into the local application. Evidence comes from authenticated Playwright/Chrome runtime inspection and the corresponding frontend/backend source. Stage and production were not tested. No imported records were modified or deleted during browser verification.

## Confirmed problem and measured improvement

The Tasks and Meetings tables displayed 25 rows while downloading broad datasets and filtering/paginating them in the browser. Their Kanban boards also depended on those broad reads. A low request count would conceal this load.

| Screen | Before | After |
| --- | --- | --- |
| Tasks list | Full scoped list; 38,877,362 transferred bytes; approximately 10.3 seconds | 25 records out of 41,401; 23,929 transferred bytes; approximately 186 ms |
| Meetings list | 35,445 records requested with `limit=100000`; approximately 15.4 seconds | 25 records out of 35,445; 43,952 transferred bytes; approximately 196 ms |
| Tasks board | Full scoped list downloaded before limiting displayed cards | Up to 40 records per status column; observed 40 Not Started and one Deferred card, with accurate global column counts |
| Meetings board | Broad list downloaded before grouping cards | Up to 40 records per status column; another 40 fetched only when that column's Next Page control is used |

Times describe observed local requests, not a controlled PostgreSQL benchmark or a full-page rendering SLA. Meeting baseline transfer bytes were unavailable because Chrome evicted the large response from its inspector cache. GET measurements distinguish API work from CORS OPTIONS, development assets, and framework traffic.

A final cold Meetings capture recorded 16 successful API responses. Five served the route: its page, KPI summary, overdue reminder preview, saved views, and Google connection status. The remaining responses served the shell/session: current user, permissions, session check-in, organization, subscription/trial, onboarding, Inbox/reply badges, pending approvals, and the import-event stream. It did not download an unrelated Tasks, Deals, Contacts or Accounts list. Replacing one large list with several small purpose-specific reads can increase request count while substantially reducing work.

The unchanged default Sales lists also remained bounded with bulk data: Leads returned 50 of 14,000, Deals 50 of 16,000, Contacts 50 of 18,500, and Accounts 50 of 10,007. Calls returned 25 of 9,201 through its existing server-pagination API.

## Implementation

- Added typed, bounded Tasks/Meetings page APIs with server-side search, filters, timezone-aware date boundaries, stable sorting and total counts. List default is 25; maximum page size is 200. Existing array endpoints remain compatible with other callers.
- Added scoped aggregate APIs for global KPI cards. These calculate counts in SQL rather than downloading entities for JavaScript counting. Page changes reuse the same aggregate cache.
- Added independent TanStack infinite queries for board columns, loading 40 cards initially and on explicit load-more. List queries are disabled in board mode and column queries are disabled in list mode.
- Reused URL pagination and shared page-size preferences. Removed duplicate browser filtering, sorting and slicing of server pages. Corrected the shared table footer to use the server's total count.
- Added scoped detail lookup so a Task or Meeting deep link can resolve a record outside the currently loaded page. A live off-page Task link opened its detail drawer successfully.
- Preserved explicit export behavior through sequential batches of at most 200 records, with a count only on the first batch. Selected exports use selected IDs, including IDs outside the visible page. Explicit all-matching Task deletion resolves matching IDs before entering the existing deletion/approval workflow; it does not fetch all entity bodies merely to identify them.
- Replaced the overdue Meeting banner's dependency on the downloaded list with a scoped count plus at most three records. Dismiss-all obtains only the matching IDs when clicked.
- Preserved legacy Meeting array-cache optimistic updates while keeping page, summary, detail and infinite-query objects intact. Scoped invalidation refreshes the new cache shapes. Removed redundant Meeting invalidations from the shared success path.

Source: [TasksTable](../../crusource-crm-frontend/src/components/dashboard/tasks/TasksTable.tsx), [MeetingsTable](../../crusource-crm-frontend/src/components/dashboard/meetings/MeetingsTable.tsx), [column hook](../../crusource-crm-frontend/src/hooks/useActivityColumn.ts), [Task repository](../../crusource-crm-backend/src/modules/tasks/repositories/task_page_repository.py), [Meeting repository](../../crusource-crm-backend/src/modules/meetings/repositories/meeting_page_repository.py), and [shared validation](../../crusource-crm-backend/src/shared/queries/activity_pagination.py).

## Backend and authorization

All new reads retain `apply_scope`, organization/team/personal visibility, existing permission guards and field masking. Tests cover Admin, Sales Manager and Sales Rep scopes. No role was granted wider visibility. Hidden fields cannot be used as new filters/sorts; hidden-source aggregate counts are withheld.

A Task page executes a count and a limited row selection with eager scalar relationships. A populated Meeting page executes those two queries plus bounded select-in reads for attendees and action items, avoiding joined collection multiplication and per-row queries. Each KPI summary uses one aggregate query. SQL-count regressions verify this behavior. Counts and wildcard searches still require database work; bounded responses do not imply constant-time queries. No schema/index migration was introduced without PostgreSQL execution-plan evidence.

## Font

No new font change was needed in this batch. A fresh authenticated browser load confirmed Instrument Sans loaded, the body used Next's generated font-variable/fallback stack, and the text FontFace used `display: block`. Chrome's `CSS.getPlatformFontsForNode` confirmed the visible heading actually rendered in Instrument Sans Bold. The earlier independent audit reproduced the user's temporary fallback under a deliberately delayed font download and documented the existing fix.

## Verification

Live checks covered list totals, page two, Meeting sorting/search, board initial loading and load-more, an off-page Task deep link, Sales/Calls page bounds, and loaded typography. Selecting page one's 25 Tasks then moving to page two preserved 25 selected IDs while leaving page two's header and visible rows unchecked. Browser console inspection reported no errors. Actual record writes/deletions and live Sales Manager/Rep sessions were not exercised; isolated fixtures cover authorization and mutation behavior.

The [backend regressions](../../crusource-crm-backend/tests/test_activity_pagination.py) contain 32 passing cases for pagination, filters, timezone boundaries, scope, collection loading, hidden fields, overdue reads and export batches. The [browser regression](../../crusource-crm-frontend/tests/test_activity_pagination_browser.mjs) exercises real services/hooks and TanStack Query under Strict Mode: caching, bounded pages/columns, filtered results, selected exports, cache-compatible Meeting updates, footer totals and disabled-view invalidation.

Backend verification used isolated PostgreSQL 17 and Redis 7 on dedicated audit ports, without migrating the application database. Ruff, syntax compilation, committed migrations, all 10 opt-in PostgreSQL regressions, empty-database migration drift, and `alembic check` passed. Full unit suite: **1,651 passed, 18 skipped, eight failed**. The same eight failures were reproduced on the unmodified pulled baseline:

- `test_data_admin_import_validation.py::test_deal_import_reports_row_errors_from_shared_handler`
- `test_sales_activities_phase2.py::test_lead_conversion_migrates_tasks_calls_and_meetings`
- `test_sales_activities_phase2.py::test_bulk_import_deals_cross_tenant_and_soft_deleted_rejection`
- `test_sales_activities_phase3.py::test_bulk_import_deals_and_leads_records_initial_stage_history`
- `test_sales_production_hardening.py::test_deals_cross_tenant_fk_rejection`
- `test_ses_inbound_reply_detection.py::test_ses_sequence_followup_cadence`
- `test_status_import_export.py::test_deals_bulk_import_with_crm_stages_and_export`
- `test_teamspace_request_workflows.py::test_governed_pool_import_uses_bounded_queries_and_captures_recovery[deals-100]`

Frontend full validation passed on Node 20.20.2 in an isolated worktree matching the final source: clean lockfile installation, changed-file formatting against the pulled baseline, full lint (zero errors, 1,529 warnings), all `npm test` suites, spreadsheets, TypeScript, every browser command in CI, the session-startup browser regression, production build using safe test API/OAuth configuration, and the configured dependency audit. The audit found no high/critical runtime advisories and retained the existing temporary ESLint-only exception.

Graphify was updated after code changes: 22,317 nodes and 62,041 edges. Its existing missing Terraform/HCL/SQL parsers, empty pyproject extraction and partial parsing of five unrelated TSX files remain coverage limits; direct source verification supports this audit. The disposable backend test containers were removed after verification. Primary repositories retain uncommitted changes; temporary snapshot commits exist only in the isolated frontend validation worktree. Changes have not been pushed or deployed. Local checks do not establish stage readiness, especially with the unresolved backend suite failures.

Any eventual rollout must make the new backend endpoints available before deploying the frontend that uses them. The legacy endpoints are retained for compatibility. This audit does not authorize or verify a rollout.

## Remaining bulk-data paths

This batch does **not** establish that every screen/tab/dialog fetches only bounded current-view data. Source tracing confirmed these separate contracts still need work:

- Dashboard metrics download broad Tasks/Meetings lists for agendas and trends. Replace them with scoped trend/summary queries and bounded agenda reads; truncating lists would make counts/trends inaccurate.
- Calendar loads broad activity lists rather than querying the visible date window.
- Entity activity drawers and global timelines fetch broad Tasks/Meetings lists and match related IDs, contact names, attendee contact IDs and attendee emails locally. Scoped parent APIs must preserve those matching rules and support pagination.
- Meeting creation/editing uses the broad meetings hook for schedule conflicts and previous/next meeting context. A scoped schedule-context API is needed; replacing it with the first page would miss conflicts.
- Global search downloads Tasks/Meetings and all Calls pages when opened; use server-side searches with explicit result limits and continuation.
- Recent Activity widgets download Tasks before slicing three entries. The CalendarDropdown also contains a broad read, but source search found no active caller; its existence alone is not evidence of global runtime traffic.
- Leads/Deals Kanban retain their 10,000-record loading paths. Campaign recipient/composer views retain large Lead/Contact lookups. These require bounded stage queries and searchable recipient selection.

Explicit full exports legitimately read all matching records and remain potentially expensive. PostgreSQL query plans/index coverage, steady-state polling under representative concurrent users, and the eight baseline backend failures require separate follow-up. Lowering a cap and silently hiding records is not an acceptable optimization.
