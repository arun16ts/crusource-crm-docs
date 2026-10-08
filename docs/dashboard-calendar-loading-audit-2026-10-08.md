# Dashboard and Calendar loading: local audit, 2026-10-08

Follow-up to [bulk-data pagination](bulk-data-pagination-audit-2026-10-08.md). This is a separate, uncommitted implementation batch. The earlier Tasks/Meetings list and board work was already committed in frontend `40b0578e` and backend `e75c57f` before this batch began. No application records were edited, deleted, imported, or migrated by this audit. Stage and production remain unverified.

## Runtime findings

Authenticated localhost browser inspection confirmed that the Calendar route fetched both broad activity collections while displaying **Connect your Calendar**. Chrome's completed transfer measurements were:

| Unnecessary request on disconnected Calendar | Transferred bytes |
| --- | ---: |
| `/api/v1/tasks` | 38,877,362 |
| `/api/v1/meetings` | 61,632,852 |
| Combined | 100,510,214 |

These bytes describe completed local development responses, not a production benchmark. Body-transfer timings were not total request timings. Reading the large response bodies through Chrome's inspector failed after eviction; no inferred response counts or latencies are presented as browser measurements.

The Dashboard also requested both broad lists. Source tracing tied them to `useDashboardMetrics`, which calculated counts/trends and produced agendas/work-queue items in JavaScript. Calendar tracing tied its reads to `useCalendarEvents`, mounted before the Google connection landing-page decision. Request count alone hid the size of these two requests.

After backend auto-reload, the application listener on port 8000 repeatedly stopped answering even `/health/ready`. A read-only PostgreSQL probe returned `SELECT 1` in approximately 29 ms, with no observed lock wait among the inspected connections. This narrows the live verification blocker to the API/reloader process; it does not establish that process's root cause. A backend restart was requested. **The final live HTTP/browser comparison is pending; fixture checks are not represented as that comparison.**

## Changes

- Added permission-guarded Tasks/Meetings `/dashboard-summary` endpoints. Their scoped SQL projections compute global counts and six local-calendar-day trend/throughput values without loading entities. Hidden-source values are withheld. Existing timezone boundaries and personal/team/tenant authorization remain in use.
- Dashboard Task agenda initially loads 50 active records with server ordering and an explicit continuation. The work queue uses scoped urgency filtering and bounded pages, with total counts independent of loaded rows. The future Meeting preview requests at most five records using its existing ordering semantics.
- Task page queries now rank narrow, scoped IDs before hydrating owner/creator/modifier relationships. Read-only PostgreSQL execution plans confirmed that the previous agenda plan joined 41,401 wide user-profile rows before its top-N sort. The revised plan sorts narrow IDs first and joins only the 50 selected records. Category-specific work-queue continuation advances only the selected activity kind.
- Standalone Tasks agenda uses its focused query. KPI-only widgets disable agenda/work-queue/preview reads; work-queue widgets disable summary/agenda/preview reads. Lead-source, Lead-message and pipeline widgets disable activity reads. Recent Activity requests three Tasks rather than downloading Tasks before slicing.
- Added parameter-complete TanStack infinite-query keys, one-minute activity freshness, cancellation signals and existing-root mutation invalidation compatibility. Repeated mounted consumers share matching keys. Disabled queries are excluded from manual activity refresh.
- Calendar activity/Google-calendar reads are gated by the existing connection decision and enabled layers. Task/Meeting and Google-event requests include the rendered date window: day, week, month grid, 14-day agenda, or year. CRM reads use pages of at most 200 and continue through the visible window so events are not silently dropped. Query failures surface a retry state.
- Extended page filters for scoped related-record matching in preparation for the drawer/timeline work. This batch does not rewire those consumers or claim they are optimized.

Source: [dashboard activity hook](../../crusource-crm-frontend/src/hooks/useDashboardActivities.ts), [dashboard metrics](../../crusource-crm-frontend/src/hooks/useDashboardMetrics.ts), [Calendar hook](../../crusource-crm-frontend/src/hooks/useCalendarEvents.ts), [date windows](../../crusource-crm-frontend/src/lib/calendar/calendarWindow.ts), [Task projection](../../crusource-crm-backend/src/modules/tasks/repositories/task_dashboard_repository.py), [Meeting projection](../../crusource-crm-backend/src/modules/meetings/repositories/meeting_dashboard_repository.py), and [trend boundaries](../../crusource-crm-backend/src/shared/queries/activity_trends.py).

## Actual imported-data checks

With the HTTP server unavailable, the new handlers were independently exercised against local PostgreSQL in a **read-only transaction**, using the supplied account's existing database-resolved authorization scope. This is actual imported-data evidence, but is not an end-to-end API/browser test.

| Handler | Total matched | Entity bodies returned |
| --- | ---: | ---: |
| Task dashboard summary | 41,401 | 0 |
| Meeting dashboard summary | 35,445 | 0 |
| Active Task agenda, first page | 41,401 | 50 |
| Urgent Task queue | 1 | 1 |
| Future Meeting preview | 0 | 0 |
| Current month Meeting window | 1 | 1 |

Initial handler observations showed dashboard summaries at approximately 55–187 ms and the agenda at 751–882 ms. Instrumentation isolated approximately 752–844 ms to the agenda row query. Read-only `EXPLAIN ANALYZE` identified wide joined rows ahead of sorting; after the ID-first change, the agenda handler took approximately 93–144 ms. A paired execution-plan capture measured the original query at approximately 666 ms and the revised query at 48 ms; it confirmed 41,401 joined records versus 50, with the inner sort width falling to 40 bytes. These are uncontrolled local observations, not a concurrency or full-page benchmark. SQL aggregates and the narrow-ID sort still scan matching data, and total counts still incur database work. No index or schema migration was needed for this confirmed query-shape issue.

## Verification

- Focused backend tests: **45 passed**, including the previous 32 page tests and 13 new dashboard/relationship/queue cases. They verify full counts, null-date trend semantics, a single aggregate statement per module, all three roles' existing scope, hidden fields, related-record fallback rules, urgency ordering, continuation, relation-name sorting and selected export IDs after ID-first hydration.
- New browser fixture passes against the actual hooks/services under React Strict Mode. It verifies zero activity/calendar requests while disconnected, parameterized windows, continuation beyond the first 200 records, layer disabling, global dashboard counts with 50 loaded rows, five-row preview bounds, absence of legacy global activity endpoints, and KPI-only invalidation gating. Google connection/profile settings and API responses are fixtures; no real Google account was connected.
- Strict Mode can cancel a signal-consuming query during its probe mount and start it again. The test distinguishes canceled requests from completed duplicate queries. This development behavior does not explain the independently confirmed broad collection downloads.
- Backend full checks: Ruff, compilation, committed migrations on disposable PostgreSQL 17, all **10 opt-in PostgreSQL tests**, empty-database schema-drift test, and `alembic check` passed. Final full suite: **1,664 passed, 18 skipped, eight failed**. Exact failed-case names match the unmodified baseline with zero differences; see the earlier audit for the list. Backend CI is therefore not green.
- Frontend final full checks passed on Node 20.20.2 in the matching isolated snapshot: clean lockfile installation, changed-file formatting, full lint (zero errors, 1,529 existing warnings), all `npm test` suites, spreadsheets, TypeScript, all current CI browser commands including the new dashboard/calendar regression, the session-startup browser regression, production build with safe test API/OAuth settings, and the configured dependency audit. No high/critical runtime advisories were found; the existing temporary ESLint-only exception remains.
- Graphify updated after final source edits: **22,365 nodes, 62,217 edges**. Existing missing HCL/SQL parsers, empty pyproject extraction and five unrelated partial TSX parses remain graph coverage limits.

Evidence scripts/logs are under `.worktrees/dashboard-calendar-20261008/`. Frontend validation uses Node 20 and a detached local snapshot of the final source. No changes have been pushed or deployed. New backend endpoints must precede a compatible frontend rollout; no rollout is authorized by this audit.

Both disposable audit containers were removed after final verification. The application PostgreSQL/Redis services and imported records were preserved. A final port-8000 readiness probe still timed out; the live verification blocker remains open.

## Still outstanding

1. Finish live Dashboard/Calendar before/after verification when localhost API readiness is restored, including cache reuse, navigation, errors and continuation with the imported data.
2. Optimize dense Calendar month/year overviews further. Date scoping prevents unrelated dates, but automatic continuation still loads every event in a populated visible window. Year/count-only and month-preview projections need a separate contract; this batch does not establish a fixed total response bound for those views. Calendar SLA markers also retain the existing first-page Lead limitation.
3. Rewire related activity drawers and global timelines to scoped pages with continuation, preserving linked contact, attendee and email matching. Meeting conflict/context validation requires its own complete scoped read.
4. Replace global-search collection downloads, Leads/Deals 10,000-record Kanban loading and campaign recipient/composer bulk lookups with appropriate searchable or stage-scoped contracts. Some standalone Sales widgets still share the bounded Lead/Deal metrics hook and warrant narrower reads.
5. Profile database query plans/indexes and realistic concurrent polling. Address the eight baseline backend failures separately. No new index/migration was introduced without plan evidence.

Typography was not changed in this batch. The independently reproduced temporary font fallback and prior fix remain documented in the initial audit. This batch does not claim that every section, dialog, dataset size or deployed environment is optimized.
