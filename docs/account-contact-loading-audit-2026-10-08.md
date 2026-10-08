# Account related-Contacts loading audit — 2026-10-08

## Scope and confirmed cause

This batch follows the global timeline audit. It fixes Account related-Contacts loading and rechecks the current global search path. It does not complete every remaining large-data consumer.

Graphify identified AccountDetailDrawer → useContacts → ContactsService and the Contact route/handler/repository. Source verification and the real localhost browser confirmed that refreshing an Account detail URL on Overview requested `/contacts?skip=0&limit=50`. The drawer filtered that first global page by Account ID in React. This unnecessarily loaded unrelated Contacts and could omit matching Contacts outside the first global page. The old badge counted that incomplete subset.

## Implementation

- Added optional UUID `account_id` to the existing Contacts list contract. Existing callers and limits remain compatible. The handler delegates to one shared scoped/search/Account filter used before both SQL count and page loading. Stable created-at/ID ordering and joined Account serialization remain intact.
- Added a focused TanStack infinite-query hook under the existing Contacts query-key root, with 50-row pages, Account-specific keys, one-minute freshness, cancellation signals and module permission gating.
- Account drawers enable this query only on the Contacts tab. Removed local filtering of the global page. The badge uses the matching server total after it becomes available; opening Overview does not issue a separate badge-count request.
- Added continuation, visible loading/errors and retry. Failed continuation retains loaded Contacts and retries the failed page. Empty-state text waits until loading succeeds. Existing Contact navigation remains wired.
- No authorization/scoping shortcut, imported-data edit, database migration or font change was made.

## Live localhost evidence

The supplied local account was already authenticated. Both local processes were started by the user after initial connection-refused checks. These are local observations, not stage results.

| Scenario | Before | After |
| --- | --- | --- |
| Account detail hard refresh, Overview | One unfiltered global Contacts page | No Contacts request |
| Open Contacts | Filtered the cached global first page locally | One Account-filtered GET, limit 50 |
| Return from Overview to Contacts while fresh | Used incomplete global data | No additional GET; retains scoped pages |
| More than 50 related Contacts | No related-list continuation | Explicit continuation, skip 50, limit 50 |

An imported Account with **3,149** visible linked Contacts returned 50 rows for skip 0 and another 50 for skip 50, both HTTP 200. The combined pages contained **100 distinct Contact IDs**. Response bodies were 34,361 and 34,458 bytes respectively, excluding headers/CORS. The other 3,049 rows were not downloaded. The badge displayed the matching total, 3,149. Fresh tab switching issued no additional Contact request.

Clicking a loaded Contact navigated to its `/dashboard/contacts?id=...` URL and opened the correct Contact drawer with its existing Account relationship and details.

A second imported Account had no linked Contacts; its scoped response was HTTP 200 with a 42-byte body and the expected empty state. The browser fixture uses 125 matching Contacts to verify all pages, failed-page retry, retained data, navigation, closed-consumer invalidation and isolation between Accounts.

## Database observations

Read-only local PostgreSQL plans compared the former global query with the inspected empty Account relation, against 18,500 visible Contacts. The global count scanned 18,500 rows; the Account-filtered count and page used existing `ix_contacts_org_account`. In the recorded sample, count execution was 3.313 ms globally versus 0.047 ms for that empty relation. These are warm local plan observations, not production latency promises or timings for every populated Account.

Filtering before count/page reduces matching work and serialization. Overview avoids the Contact page and count entirely. Counts still run for each requested related page; this batch does not claim all database work has disappeared.

## Global search correction

The current `useGlobalSearch` already calls `SearchService.globalSearch` after a 300 ms debounce, only while open with at least two characters, with limit 5 and a two-minute cache. Task and Meeting providers apply existing scope and SQL LIMIT before materialization. They do not download their full collections into the browser.

The real browser search for `Review` made one `/search/global?q=Review&category=all&limit=5` request, HTTP 200, with five Deal and five Meeting results. No broad Task/Meeting collection GET occurred. Provider counts describe returned capped results, not a full database match count. Search query-plan/cache profiling remains possible separate work; the older broad-download warning is not accurate for this current global-search path. No search code change was needed.

## Validation and limits

- Backend: full Ruff and compilation; committed migrations on disposable PostgreSQL 17; **1,705 passed, 18 skipped** in the full suite; ten opt-in PostgreSQL regressions; separate empty-database migration-drift test; `alembic check` all passed. Thirteen new focused tests cover stable 50/50/25 pages, search combined with Account filtering, HTTP UUID validation and Admin/Sales Manager/Sales Rep own/team/all/none visibility, tenant isolation, team boundaries and deletion.
- Frontend: clean lockfile installation using Node 20, full lint, unit/spreadsheet tests, TypeScript, all current CI browser commands including the new Account Contacts regression, extra session/Loop AI checks, safe production build and configured dependency audit passed. Existing 1,519 lint warnings remain. Changed-file formatting passed against the current pre-batch commit `e8872642`; the initial runner inherited an older baseline and reported formatting warnings in earlier work, so that check was rerun with this batch's correct baseline. Original and rerun logs are retained.
- The seven changed/new frontend files match isolated validation snapshot `88cf86cc` byte for byte. Evidence/scripts are under `.worktrees/account-contacts-20261008/`. Test PostgreSQL/Redis on 15432/16379 are separate from application services on 5432/6379.
- The two named disposable CI containers were removed after checks. The application backend readiness recheck returned HTTP 200; application services were left running.
- Graphify was updated: 22,501 nodes / 62,668 edges. Existing missing HCL/SQL parsers and partial unrelated TSX extraction remain coverage limits.
- No push, deployment or stage verification. Deploy the optional backend Account filter before its frontend consumer; an older API would silently ignore that parameter.

## Remaining work

Follow-up: [Campaign audience audit](campaign-audience-loading-audit-2026-10-08.md) addresses recipient browsing, all-matching ID selection, composer and review loading from item 1 below. Existing Campaign detail monitoring and very large selection/worker scaling remain separate.

1. Campaign recipient/composer/review paths still contain 100,000-row Lead/Contact reads. Replace them with searchable bounded lookups and an explicit server-side all-matching selection contract; merely lowering the limit would silently drop recipients.
2. Lead/Deal Kanban still needs bounded per-column loading while preserving totals, filters, drag-and-drop and aggregate values.
3. Contact Deal-note fan-out and unpaged parent notes need a scoped batching/pagination contract.
4. Meeting conflict/context reads and dense connected Calendar need bounded window/availability queries without missing conflicts or events.
5. Continue representative count/relationship-plan and concurrency profiling. A unified strict chronological timeline cursor and the previously observed native reload/SSE lifecycle remain separate investigations.
