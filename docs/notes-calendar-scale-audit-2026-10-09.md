# Parent Notes, dense Calendar and scale audit — 2026-10-09

## Scope and evidence

This continues the remaining work in the [meeting scheduling audit](meeting-scheduling-context-audit-2026-10-09.md) and [Kanban audit](sales-kanban-loading-audit-2026-10-09.md). It covers parent Notes pagination, Contact/Deal timeline batching, dense Calendar loading, SQL plans, deep offsets, four-reader concurrency and accumulated export memory. It does not establish that every application feature is fully optimized.

Graphify was queried first; repository source and localhost browser behavior were used to verify the findings. The starting frontend commit was `e40ff9411ccb125b8aa9d9da8dd17ce91b72a511`; the backend was `cf396e98c195dc76ba075ade0d6254ad3daf79eb`. Changes remain in the primary working trees. Nothing was pushed or deployed, and no application records were imported, edited or deleted during this audit.

## Confirmed problems and implementation

The legacy parent Notes route returned at most 75 notes, without exposed continuation. Visible sorting in the shared Notes section sorted only the downloaded subset. Some drawers loaded notes while displaying Overview. The shared Contact timeline fetched a separate Notes collection for every loaded Deal, producing up to 51 Notes reads for a Contact plus its first 50 Deals.

An additive `POST /api/v1/notes/parent-page` now accepts a parent, optional secondary parent, linked Contact-Deal inclusion, sorting and bounded pagination. The frontend requests 50 notes; the API allows at most 100. A `limit + 1` sentinel returns `has_more` and `next_offset`, without a count query. Stable creation-time and ID ordering supports both recent and oldest sorting. Existing parent authorization and Teamspace record-access resolution are reused. Linked Deals are a scoped SQL ID subquery, rather than hydrated Deal objects or individual Notes requests. Hidden Contact relationships and missing Deal-view permission prevent linked-note reads; an inaccessible secondary Contact does not suppress the permitted primary parent's notes. Existing GET routes remain available for compatibility.

Parent Notes hooks now share an infinite-query cache while retaining existing mutation-invalidation prefixes. Notes load when the relevant Notes or Timeline view is active. Drawers and the shared Notes section expose continuation and explicit loading/error/retry status. Older records are reachable rather than silently truncated. The shared global timeline includes Notes continuation alongside activity and Deal continuation. Its Contact path uses one bounded Notes query for Contact and scoped linked Deal notes.

Dense Calendar testing confirmed that a failed Tasks continuation previously made Retry refetch already successful Tasks pages, the healthy Meetings stream, and Google reads. Retry now resumes a failed next page, or retries an initial failed query, without refetching healthy streams. Loading state stops while a failed stream waits for retry; successful loaded data remains in the query cache.

Scale profiling found that Meetings display joins carried wide user data into the full sort/offset operation. `meeting_page_repository.get_page` now selects scoped, filtered, sorted page IDs first and then loads the same display relationships for those IDs. The response contract, totals, selected-ID exports, field validation and ordering are preserved. No migration or index was added. The narrow ID query retains existing personal-assignment/team/tenant scoping; the outer display query cannot introduce IDs absent from that scoped page.

## Browser observations

| Scenario | Before | After / verification |
| --- | --- | --- |
| Live Riley Khan Lead drawer, Overview | Requested the Lead's Notes collection | No Notes request |
| Open that drawer's Notes tab | Legacy fixed collection | One `parent-page` request, `skip=0`, `limit=50`; HTTP 200, zero notes for that real parent |
| Older Notes and the actual drawer control | No parent continuation beyond the legacy cap | Browser-only 125-note response fixture: offsets 0, 50 and 100; all 125 rendered; continuation button disappeared at the end |
| Shared Contact timeline with 51 related Deals | Contact Notes plus per-Deal Notes collections | Isolated actual-hook fixture: one completed scoped Notes-page request initially; continuation includes remaining notes; no `/notes/Deal/...` fan-out |
| Failed continuation | Broad Calendar refetch | 10,000-event actual-hook fixture: retry resumed Tasks at offset 600; healthy Meetings and successful Tasks pages were not reread |
| Calendar year 2022, imported localhost Meetings | Complete year loaded through bounded pages | Before and after Meetings SQL optimization: 8,632 Meetings through 44 requests, limit 200, offsets 0–8,600; final page 32 rows; 365 event-day indicators |

The actual account is not connected to Google. For the Calendar UI comparison only Google status/calendars/events reads were intercepted in the browser; CRM Tasks and Meetings reads used the authenticated local backend and its imported data. The year contained zero matching active Tasks, so that stream made one empty page request. The final comparison had 45 activity page requests, no duplicate Meeting offsets and no failed pages. All Google and Notes response fixtures were removed and the page reloaded afterward. No external Google integration was connected or modified; real OAuth/Google synchronization remains unverified here.

The 125-note live-page check used synthetic browser responses because the selected actual Lead had no notes. Backend continuation and authorization were tested independently against database fixtures. Browser-only fixtures are not represented as real imported Notes. Restarting the backend briefly put the application shell into its existing profile/permissions retry state; its Try again action restored the workspace.

## Disposable PostgreSQL scale results

Profiling used a separate, migrated PostgreSQL 17 database in a temporary audit container. The dataset contained 25,000 Tasks, 25,000 Meetings, 50,000 Notes and 1,000 linked Deals. Neither the local application database nor stage/production was used. Values below are individual local measurements, not production latency targets.

| Read | Before Meetings optimization | After | SQL reads after |
| --- | ---: | ---: | ---: |
| Meetings first 50 | 85.81 ms | 54.52 ms | 4 |
| Meetings offset 24,000, 50 rows | 269.37 ms | 29.78 ms | 4 |
| Meetings Calendar window, 200 rows | 78.26 ms | 52.04 ms | 4 |
| Explicit 25,000-Meeting export, 200-row batches | 13,951.93 ms | 5,193.61 ms | 376, including one count |
| Explicit 25,000-Task export, 200-row batches | 2,790.25 ms | 2,712.91 ms | 126, including one count |
| Combined Contact/Deal Notes first 50 | 16.22 ms | 12.92 ms | 1, no count |
| Combined Notes offset 24,000 | 22.11 ms | 25.36 ms | 1, no count |

EXPLAIN ANALYZE confirmed the improvement in the main Meetings display SQL: first-page execution fell from 43.744 to 5.846 ms; deep-offset execution from 112.799 to 13.692 ms; Calendar-page execution from 41.839 to 11.672 ms. Counts remained approximately 2–4 ms on this fixture. Existing indexes were retained. The two attendee/action-item relationship reads remain legitimate and bounded to the selected page; there are no per-row serialization reads.

Four warmed connections completed 40 deep Task-page reads in 281.38 ms overall, median 23.35 ms, maximum 37.10 ms. The earlier cold-pool run had a 2,083.9 ms maximum, dominated by connection establishment; it is retained in the evidence rather than attributed to the query optimization. This small concurrency check does not establish production capacity, connection-pool tuning or sustained load behavior.

The existing export pagination helper was also executed in an isolated Chromium fixture. Retaining 50,000 synthetic rows used approximately 13,932,036 additional heap bytes; 100,000 used 27,861,028. It made 250/500 explicit 200-row batches. This measures retained row objects before CSV/XLSX serialization, which requires additional memory; synthetic string sharing means the result is not an upper bound for real payloads. Ordinary page entry does not invoke this helper.

## Validation

Evidence is retained under workspace `.worktrees/remaining-performance-20261009/`: complete check summaries and logs, isolated frontend validation snapshot, PostgreSQL plans in `scale-profile.json` / `scale-profile-after.json`, and `export-memory-profile.json`. Profiling helpers assert the dedicated container port and profiling database name before seeding. The frontend snapshot was compared with all 26 changed/new primary files and matched after validation.

Frontend complete local CI parity passed: clean lockfile installation, changed-file formatting, full lint, unit/localization and spreadsheet checks, Loop/public AI checks, TypeScript, every current workflow browser regression including the new parent Notes and dense Calendar scripts, production build with dummy API/OAuth settings, and dependency audit. Lint reported zero errors and 1,492 warnings; warnings are not represented as a warning-free run. New browser regressions are registered in `package.json` and the CI workflow.

Final backend complete local CI parity passed after the Meetings optimization: Ruff, compilation, committed migrations, full pytest (**1,903 passed / 23 skipped**, 1,928 warnings), required Redis (**33 passed**), webhook/production PostgreSQL (**54 passed**), remaining PostgreSQL regressions (**10 passed**), fresh empty-database migration drift (**1 passed in 20.81 seconds**) and `alembic check`. The empty drift database was distinct from the migrated regression and populated profiling databases. Existing opt-in skips in the ordinary suite were covered by the corresponding required runs; other skips remain recorded in the logs. Focused parent Notes/authorization checks passed 75 tests; the final activity-pagination/Meeting-visibility run passed 37 tests, including stable host sorting within the existing scope.

Graphify updated successfully (exit 0): **23,160 nodes / 64,483 edges / 1,133 communities**. Its log still records optional parser/partial TSX extraction and historical pytest-cache access warnings, so source remains authoritative.

The two disposable audit containers and their temporary volumes were removed after validation. A final Docker inspection confirmed that only the original local application PostgreSQL and Redis containers remained.

Both backend edits were verified after the user restarted localhost. The new Notes endpoint and the optimized Meetings API returned HTTP 200. Fresh year-window UI loading after the final restart returned the same complete 8,632 Meetings and all event-day indicators. Local checks do not establish remote CI or stage deployment behavior. Backend availability of the additive Notes endpoint must precede a future frontend rollout.

## Remaining limitations and separate work

- A Year Calendar view still downloads every full event in the visible year, rather than a compact daily aggregate. Pagination bounds each response; it does not make an 8,632-event year cheap. Each ordinary activity page also recomputes its scoped total. The current measurements do not justify claiming these reads are free. A compact Calendar-specific projection/aggregation and count-once or cursor continuation are potential follow-ups that must preserve Google deduplication, visible-window completeness and navigation to individual events.
- Explicit exports retain all rows and create an additional file representation in browser memory. Very large CSV/XLSX exports need a separate scoped streaming/background-download design. This audit measured the existing behavior; it did not introduce arbitrary export caps or remove formats.
- Deep offsets still scale with preceding rows, and offset-based continuation can shift under concurrent edits. Measurements at this volume were acceptable after the display-join optimization; they are not proof at millions of records.
- Shared infinite queries retain loaded pages and can reread them after legitimate invalidation. Notes batching removes per-Deal fan-out but does not promise constant memory after loading every note.
- The legacy campaign-detail and per-representative leaderboard limitations documented in earlier audits, real Google integration, sustained production load and stage verification remain separate. No deployment was performed.

The listed Notes implementation, dense Calendar checks and local scale profiling are complete. These results should not be described as “the entire application has no remaining performance work.”
