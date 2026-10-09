# Phase 3B and 3C — Organizations and Login History

Date: 9 October 2026. Status: **3B and 3C VERIFIED LOCALLY; Phase 3 remains in progress.**

This package combines Organizations (3B) and Login History/member profiles/export (3C). It preserves the committed Overview and trial partial-commit correction. Trial review concurrency/transactional authority/current-record dialogs (3D), Feedback (3E), and final integrated Phase 3 acceptance remain separate work.

## Evidence and environment

Starting application commits: frontend `70ee05da`, backend `151c28b`. Implementation remains local and uncommitted. The existing validation checkout was reused; no additional Git repository or worktree was created. No application database was migrated, seeded or cleared, and nothing was pushed or deployed.

The running localhost services answered readiness. Authenticated integration used actual Next.js routes and real FastAPI handlers with synthetic staff/customer identities, isolated in-memory SQLite and local fake delivery. Platform cookies, origin/custom-header admission and guards were real. CRM credentials were not treated as platform credentials. PostgreSQL performance and migration checks used separate disposable PostgreSQL 17 and Redis services on test ports. This is local integration evidence, not staging verification or a production-scale benchmark.

## Before and after

| Behavior | Before | After |
| --- | --- | --- |
| Default organization Members tab | Full 76-member response; inactive Login History request | Metadata plus at most 25 members; no inactive Login History read |
| Member login summaries | One latest-IP query for each member | One scoped window query for the visible member IDs |
| SQL for fixture organization detail | 79 statements; 76 returned members | 5 statements including metadata/existence/count/page/metrics; 25 returned members |
| Global Login History initialization | Organization selector fetched immediately | History and independent global statistics; organization lookup starts when opened |
| Organization lookup | First 100 organizations only | Searchable 25-row pages |
| CSV preparation | All ORM rows, dictionary list and full StringIO in memory | Repository batches of 500, formula-safe temporary file and owned cleanup |
| Export vs displayed page | Existing full matching dataset semantics | Preserved: 183 successful matching rows downloaded while table displays 25 |

The SQL comparison used the old committed implementation and current code against the same disposable 76-member/5,003-login fixture. Single-run elapsed times were 299.40 ms and 25.77 ms respectively; these are not an SLA. The 5,003-row export held at most 500 ORM objects. Counts/aggregates still require legitimate database work; fewer requests do not make them free.

Required global requests remain platform identity and the owner's pending-invitation navigation badge. Development captures include repeated Strict Mode attempts. The first before list capture overlaps the login redirect, and the baseline script separately probes the legacy detail payload. Compare route families/payload bounds, rather than presenting raw totals as production duplicate counts. No customer CRM feature endpoints were added to the platform shell.

## Contracts and architecture

- Routes are thin server entries with focused client screens, shared page header, server-mode DataTable, pagination, dialog, platform formatters, design tokens and EN/NL messages. No fetched entities are mirrored into Redux.
- URL owns search/filter/sort/page/page-size/tab and selected-profile identity. Search and role input are debounced; filter changes reset pagination atomically. Rapid successive updates use the pending URL state, preventing an old organization filter from being restored after Reset. Invalid pages/limits/UUIDs/sorts are normalized before requests.
- Additive `GET /api/v1/superadmin/organizations/{id}/summary` returns metadata without members. `GET .../{id}/members` returns `items,total,limit,offset`, default 25, maximum 200. Member sort fields are `created_at,name,email,role`, with UUID tie-breaking; organization/search/role/enabled filters run on the server.
- The original full-detail endpoint keeps its full-roster meaning. Its per-member SQL is corrected, but it remains unbounded for compatibility. Current UI no longer calls it. Caller inventory: the legacy service and hook remain exported, with no screen consumer found in `src`; inventory/deprecation of external consumers is future work.
- Member and organization-history reads are enabled only for a valid organization and active tab. Drawers load only the selected user, include organization context, forward cancellation and own bounded URL pagination. A user outside the supplied organization is rejected with 404; its history and profile summaries cannot silently resolve another tenant.
- History, profile and export share UTC calendar windows: `start_date` inclusive, additive `end_before` exclusive. A through date includes its entire UTC day; a single from date selects that day. Original `end_date` remains inclusive for compatibility. Global 7/30-day statistics remain rolling windows, are explicitly independent of table filters and use four SQL statements. Zero attempts show “No attempts”. Customer login telemetry remains separate from platform staff security events.
- CSV export uses committed filters without pagination. A dedicated TanStack mutation handles progress/failure/cancellation, prevents duplicate starts and aborts on session change/unmount. The existing platform client owns cookies/headers; CRM `sessionCheckin()` retains the CRM bearer client.
- FastAPI 0.111 closes yielded request dependencies before response-body delivery. Database iteration therefore finishes while the session is alive; FileResponse subsequently reads the temporary CSV. Generation and failed/cancelled delivery remove the owned file. Existing CSV formula protection is reused, and responses are private/no-store.

Backend/API contracts must reach the environment before this frontend; an older backend deliberately produces a visible read error rather than falling back to the full roster. No schema migration was introduced.

## Validation

Focused backend: 25 passed, covering bounded/stable member pages, fixed query growth, tenant-context rejection, exclusive UTC boundaries and legacy inclusive boundaries, multi-batch export agreement, empty statistics and file cleanup/formula escaping. Native PostgreSQL exercises the window summaries and 5,003-row bounded ORM iteration.

Backend full CI parity passed: Ruff, compile, committed migrations, **1,970 passed / 50 skipped**, required Redis **33 passed**, webhook/production PostgreSQL **59 passed**, recovery/startup/import PostgreSQL **10 passed**, fresh empty-database migration drift **1 passed**, Alembic check, and platform PostgreSQL **25 passed**. Required opt-in Redis/PostgreSQL groups were separately exercised with their flags. No application schema migration was added.

Portable browser and URL/date contract regressions are registered in frontend CI. Real-route tests additionally verify platform login, 25-row tables, active-tab loading, lazy search across organization pages, profile open/keyboard close, committed-filter CSV row counts, CRM bearer rejection on new reads/export, organization mismatch 404, date routes, and responsive widths. Supplementary checks cover real font, refresh/back/forward and scrolled mobile tables. CSS scaling captures are labelled as such, not a claim of testing every browser zoom configuration.

All current frontend workflow checks passed on the frozen source: clean lockfile installation, changed-file formatting, full lint (0 errors, 1,484 repository warnings), unit/localization/spreadsheet/Loop/public contracts, types, required browser suites, safe-config production build and dependency audit. Additional platform auth/contracts/real-route suites and CRM session startup passed. Local browser scripts use Edge on Windows; remote Linux/Chromium CI has not been run or claimed.

The wrapper returned 1 only for the extra unmodified deterministic CRM-frame test: local antivirus injected a request to `me.kis.v2.scr.kaspersky-labs.com`. A separate controlled comparison blocked only that injected host and used real pre-merge frame source; screenshots were identical at expanded/collapsed 1440, 1024, 768 and 390px. Application and antivirus settings were unchanged. This does not erase the raw extra-test failure. An initial old platform-route run also timed out during cold navigation; its bounded navigation allowance was increased to 60 seconds, and the final real-route run passed.

Evidence: [before routes](organizations-login-history/baseline/routes.json), [after routes](organizations-login-history/after/routes.json), [PostgreSQL comparison](organizations-login-history/postgres-profile.json), [frontend checks](organizations-login-history/frontend-checks.json), [backend checks](organizations-login-history/backend-checks.json) and [source-equality proof](organizations-login-history/frontend-source-proof.json). All 29 changed/new frontend files exactly matched the tested snapshot. Screenshots are alongside the route captures: list/detail/history (`1`–`4`), profile, responsive history widths and mobile table. The `200percent` capture uses CSS scaling.

Final Graphify update exited 0 and rebuilt the application code graph. Existing parser/dependency warnings for unrelated TSX/SQL/HCL files remain; generated graph context is not source truth. The two named disposable PostgreSQL/Redis test containers were removed after verification; the original application containers and data were preserved. Primary application HEADs remain `70ee05da` and `151c28b` with local edits; no push or deployment was performed.

## Remaining limits

Export processing is synchronous and temporary-file disk usage grows with the matching dataset. Cancelling the browser request prevents download and delivery cleanup runs, but it does not forcibly terminate a SQL worker already generating the file. Larger production exports need measured duration/disk budgets before deciding on a platform-authorized job design. The current fixture establishes bounded ORM loading, not arbitrarily large throughput.

Real deployed staff sessions, Vercel/ECS configuration and stage/customer flows remain release verification. Packages 3D, 3E and final integrated acceptance are still required before Phase 3 is complete.
