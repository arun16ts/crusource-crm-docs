# Sales Kanban loading audit — 2026-10-09

## Scope

This follow-up addresses the confirmed Leads and Deals Kanban bulk-loading issues in [the campaign/read-work audit](campaign-read-work-audit-2026-10-09.md). It does not certify every application route, dialog or deployment. Frontend baseline: `e5fa25c2652e9076efdd7e41cd5306db8c1eef02`; backend baseline: `1a44cdb05c45049f7905943e21c8a887dfb6c604`. The earlier uncommitted campaign optimizations were retained. No primary-branch commit, push, deployment or application-data mutation was performed.

## Confirmed cause and implementation

Both parent pages requested up to 10,000 entities for Kanban. Column continuation only revealed more already-downloaded cards. Consequently, this was neither server pagination nor complete access to larger datasets. Deals column counts and currency subtotals also used downloaded cards rather than the full matching dataset.

- Added scoped `/leads/kanban-summary`, `/leads/kanban-column`, `/deals/kanban-summary` and `/deals/kanban-column` reads. Summary returns full matching counts and Deals currency subtotals. Card pages default to 40, reject limits above 100, apply existing filters and sorting, and add an ID tie-breaker.
- Reused `apply_scope`, module-view guards, organization-specific pipeline lookups, existing filter repositories and response field ceilings. Hidden grouping fields deny board access; hidden financial fields suppress currency aggregates. Existing Admin, Sales Manager and Sales Rep visibility remains authoritative.
- Preserved explicit Lead stage IDs, legacy status/name resolution, unassigned Lead fallback, and inactive-stage behavior. All-pipeline Lead headers retain the full scoped total while cards retain the previous default-pipeline/unassigned grouping. Deals continue mapping stage names to the selected board's definitions.
- Narrow paginated IDs are selected before wide record hydration. Card serialization eagerly loads required relationships; summaries hydrate no Lead/Deal entities. No read performs reconciliation or business writes.
- Added a focused API service and TanStack Query hooks. Each column loads additional server pages on demand; empty columns skip card reads. Query keys include module, pipeline, stage and filters, excluding list pagination. Existing module invalidation refreshes board cards and summaries. Cache freshness is 30 seconds; no polling was added.
- Disabled list reads while the board is mounted. Removed the redundant board aggregate reads and client grouping/subtotal calculations. Kept record detail, drag updates, stage confirmations and error/retry behavior. Lead drag carries the loaded card so it does not depend on a broad parent list.
- Browser filter verification exposed an existing Deals integration bug: choosing All Pipelines cleared the URL parameter and immediately selected the default pipeline. The selector now persists the explicit `all` URL value; the API receives no pipeline filter for that selection.

The endpoints are additive. Any later rollout must make the backend endpoints available before the new frontend consumes them. Deployment is outside this local task.

## Local Chromium comparison

The before figures were recorded in the preceding live audit against the imported localhost workspace. The after figures are new measurements of board activation against the same local data. They are decoded JSON body bytes, excluding application-shell calls, JS/CSS, and any earlier list-view request.

| Board | Before | After initial board activation |
| --- | --- | --- |
| Leads, 14,000 total | 10,000 cards; 10,354,810 bytes; 4,000 outside the response | 120 cards: three nonempty columns × 40, plus full summary; 124,528 bytes |
| Deals, 16,000 total | 10,000 cards; 9,155,116 bytes plus 2,713 aggregate bytes; 6,000 outside the response | 200 cards: five nonempty columns × 40, plus full summary; 184,250 bytes |

All new captured board responses were HTTP 200. Initial requests were one summary plus one card request per nonempty column, with no broad 10,000-row list or legacy aggregate request. This intentionally trades a single huge request for several bounded requests. Empty columns requested no cards. In each module, Show More increased a column from 40 to 80 with one `card_skip=40&card_limit=40` request. Leads continuation was 41,611 bytes; Deals continuation was 36,588 bytes.

Lead full column counts remained 7,097 / 0 / 3,361 / 0 / 3,542, totaling 14,000. Deal counts remained 3,435 / 0 / 0 / 0 / 3,215 / 2,746 / 4,589 / 2,015, totaling 16,000. Deal subtotals use the full matching amounts, not the amounts of 40 loaded cards.

Live checks covered empty currency results, an empty alternate pipeline, restoration of cards, and the corrected All Pipelines URL selection. A Deal retrieved from offset 4,000 in its column was absent from the initial cards; searching for it returned exactly one card through a server-filtered read. No imported record was dragged, edited or deleted. Drag behavior was verified in isolated browser fixtures.

Refreshing these routes currently returns to their existing List view: that view legitimately requests its server page. Board measurements above describe switching to Kanban, not a claim that a refresh preserves board mode. The font implementation was unchanged in this batch.

The reload worker repeatedly stopped answering readiness checks during source edits. After the user restarted without `--reload`, readiness and API reads succeeded. That local runtime interruption is separate from the confirmed board bulk-fetch cause.

The disposable PostgreSQL/Redis audit containers and their test volumes were removed after validation. The application remained ready (HTTP 200), with the Leads list showing its 50-row page.

## Disposable PostgreSQL volume check

Created 12,500 records per module only in disposable PostgreSQL on port 15432. Fixtures ran in an outer transaction that was rolled back. No local application, stage or production database was seeded or migrated for these checks.

| Read | Lead entities hydrated / elapsed | Deal entities hydrated / elapsed |
| --- | --- | --- |
| Old 10,000-card read | 10,000 / 596.91 ms | 10,000 / 769.55 ms |
| New summary | 0 / 27.43 ms | 0 / 24.95 ms |
| New first 40 cards | 40 / 33.01 ms | 40 / 29.67 ms |
| New 40 cards at offset 12,000 | 40 / 30.28 ms | 40 / 25.91 ms |

These are single local fixture observations, not a concurrency benchmark or production latency promise. Summary and card reads each used five SQL statements versus two for the old bulk list. Full counts and currency aggregates still scan matching records; stage-resolution CASE expressions and offset pagination still require database work. The established improvement is bounded hydration, much smaller responses, complete continuation beyond the old 10,000 cap, and no client-wide sales dataset for ordinary board viewing. This is not a claim that all PostgreSQL work is constant or every query count decreased.

## Validation and remaining work

Backend workflow checks passed: Ruff, compilation, committed migrations on disposable PostgreSQL, **1,741 tests passed / 18 skipped**, all **10 opt-in PostgreSQL tests**, the separate empty-database migration-drift test, and `alembic check` with no new upgrade operations. The full suite reported 1,849 warnings. Fifteen new regressions cover bounded continuation, stable ties, unloaded search, currency totals, all three role scopes, team/tenant isolation, hidden fields, legacy stage resolution, inactive stages and bounded eager serialization.

The isolated Chromium regression exercises actual board components, services and query hooks under Strict Mode: continuation through all 125 cards, server search, detail selection, next-page failure/retry without losing cards, fresh-cache remount, Deals drag mutation/invalidation and no refetch after closing the board. It is registered in frontend CI. Complete frontend workflow checks passed again after the final All Pipelines fix: clean lockfile installation, changed-file formatting, full lint, tests, spreadsheets, all workflow browser regressions, type-check, production build with dummy API/OAuth settings, and dependency audit. Additional session-startup and Loop AI regressions passed. Lint reported 1,494 warnings and zero errors. Checks ran in an isolated snapshot whose 13 changed files were compared with the primary checkout.

The final architecture review separated summary and card handlers into one file per use case, with shared field access under `src/shared/auth/sales_kanban.py`. Focused regressions passed after this file-only reorganization. Final independent backend checks passed again against the already-created disposable database: Ruff, compilation, committed migrations, **1,741 tests passed / 18 skipped**, all **10 opt-in PostgreSQL regressions**, and `alembic check` with no new upgrade operations. The venv dependency consistency check also passed. A fresh migration-drift database creation was rejected by the execution tool; that action was not bypassed. The earlier empty-database drift pass remains evidence before this reorganization, not a claim that the final complete CI was rerun. No schema or migration changed.

Evidence is under `.worktrees/kanban-20261009/`, including the isolated frontend CI checkout, backend logs, the rollback-only PostgreSQL profile and sanitized Deals network capture. Graphify was updated after the final source edits: 22,721 nodes and 63,289 edges, with the new handler nodes verified in the generated artifact. Its process still reports exit code 1 with successful graph rebuilding and coverage warnings for unavailable HCL/SQL parsers and five unrelated partial TSX extractions; this is not a clean Graphify exit claim.

Remaining separate work: Schedule Meeting still requests broad meeting context, parent Notes need pagination/batching, dense Calendar windows need volume checks, and counts, offset queries and accumulated exports need concurrency/query-plan profiling. Infinite-query boards retain the pages a user explicitly loads and may refetch those loaded pages after invalidation; bounded page size is not a promise of constant browser memory or refetch work after loading thousands of cards. Legacy campaign detail and per-representative leaderboard reads retain limitations documented in the preceding audit. Local passes do not establish stage behavior or remote CI success, and the unresolved final drift rerun prevents claiming complete CI readiness for stage.
