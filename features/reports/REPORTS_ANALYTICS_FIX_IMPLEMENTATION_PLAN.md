# Reports and Analytics fix implementation plan

**Date:** 14 October 2026  
**Status:** Proposed fixes; not implemented.  
**Basis:** [Reports and Analytics audit](REPORTS_ANALYTICS_AUDIT.md), covering frontend `063e8c3c` and backend `3ef484a`.  
**Scope:** Complete and repair the agreed CRM Reports/Analytics work. Do not add report sharing UI or unrelated VMS functionality.

## Intended outcome

Saved report criteria control each report and widget independently. A user's pipeline/currency choices persist, chart clicks retain the saved scope, amounts have valid units, imported/exported definitions round-trip, and source permissions apply to every indirect read and write. Unsupported or legacy definitions must produce an actionable report-level state rather than break the entire section.

Report names and optional widget titles remain user controlled. Do not restore board-wide pipeline/currency overrides, add compulsory scope badges, convert currencies, or silently drop invalid criteria.

## Phase 1 — Close security gaps

**Findings:** RA-01–RA-04. Deliver this before wider functional changes.

1. Add a failing HTTP regression for suggestions with Reports access but denied Accounts/Contacts/source fields, own/team scopes, soft-deleted records and a foreign tenant. Include the real request ORM boundary, not only a mocked scope resolver.
2. Move suggestion query construction into a scoped repository/query use case. Enforce source module permission, field access and record visibility, including relationship labels. Metadata discovery must not leak values from a hidden field.
3. Remove the organization-only private-report fallback from assignment. Resolve the source report with an explicit edit/assign authority policy and the destination team with a separate management policy. Knowing a report UUID must not grant control.
4. Reuse one sharing-reference validator for create, edit, share and assignment. Validate active team/assignee organization, destination-team membership where needed and caller authority. Validate all inputs before changing model fields/default flags. Explicitly handle clearing optional references instead of interpreting every null as “no change.”
5. Sanitize all user-controlled XLSX matrix row labels as literal text, using the existing shared cell helpers. Cover row labels, headers, footer labels and both CSV/XLSX paths. Test cell `data_type`, not only its visible text; keep money/numeric cells numeric.

**Acceptance:** Unauthorized lookups/writes return consistent 403/404 without revealing names or mutating visibility; foreign team/user references are rejected; spreadsheet text such as `=1+1` is never a formula cell. Authorized existing flows continue to work.

**Review and recovery:** These repairs change access control. Review source and destination authorization separately and test current team-manager workflows before release. Roll back the code only if required; never restore cross-tenant references or private-report visibility as a workaround. No automatic sharing backfill is authorized by this plan.

## Phase 2 — Complete native widget persistence and legacy decoding

**Findings:** RA-05, RA-10; compatibility portion of RA-08.

1. Define explicit typed native widget configuration in the backend and frontend. Sankey/cohort support a scoped Deals pipeline ID or a canonical All-pipelines representation. Reject unsupported configuration instead of silently ignoring it.
2. Validate pipeline organization/module/availability when adding or editing configuration. Preserve configuration in command serialization, JSON persistence and response models. Inspect specialized stage-history endpoints as the final read boundary too.
3. Add real API create → response → reload → update tests, then a browser/API integration test where choosing pipeline A excludes pipeline B. Mock-only assertions that the callback receives an ID are insufficient.
4. Inspect existing widget JSON and saved report definitions in a read-only inventory before any repair migration. Decode harmless documented legacy shapes through a versioned normalizer; represent incompatible reports individually as “needs repair.” Running/exporting an incompatible report must return a safe, actionable error.
5. Preserve unsupported filters for review; never remove them and execute a broader report. Update list/board UI contracts to handle invalid entries without losing healthy entries. If a migration is necessary, specify a backup, dry-run report and rollback path after inspecting real data.

**Acceptance:** Native pipeline selection survives a full reload. One invalid report cannot prevent users listing, opening or repairing other reports. Existing valid widgets remain compatible.

## Phase 3 — Correct monetary and matrix calculations

**Findings:** RA-06, RA-14.

1. Test SUM, COUNT, AVG, MIN and MAX matrices with uneven group sizes, missing values, multiple currencies and more groups than one page.
2. Compute legitimate row/column/grand totals from the full scoped dataset using the aggregate's actual semantics. AVG needs underlying counts; do not average or sum pre-aggregated averages. Preserve missing-value semantics.
3. When currency is a grouping dimension, suppress totals spanning multiple currencies or return separate currency totals. A mixed-currency warning does not make a cross-currency sum valid.
4. Separate pivot pagination from complete-total calculation and describe what each response total counts: source records, aggregate groups or displayed cells. UI and exports must agree.
5. Correct the default revenue template using the domain's won-stage classification rather than a literal stage-name slug. Create monetary templates with an explicit currency policy and normal report admission validation.
6. Move template provisioning into an idempotent command. Avoid hidden writes in a read query and respect creation/subscription authority. Repair existing generated templates only when confidently identified; do not overwrite user-customized definitions.

**Acceptance:** USD and INR never become one total; averages/min/max are mathematically correct; pagination does not change a claimed full total; a first-time board shows the expected won revenue with its actual currency.

## Phase 4 — Make chart binding and drill-down explicit

**Findings:** RA-07–RA-09, RA-15.

1. Add response metadata distinguishing a canonical dimension value from its display label. Relationship IDs and enum values remain stable machine values. Add explicit dimension/metric bindings rather than relying on column positions or title text.
2. Define supported shapes for each chart in matching frontend/backend contract fixtures. Pie/Donut need a meaningful numeric metric and supported dimension shape; Bar/Line plot numeric metrics, not currency or owner-name columns. Grouped KPI/Target must be rejected or use a deliberate total aggregation, never the first bucket silently.
3. Use a focused drill-spec builder. Append typed criteria while retaining every saved filter. For matrices preserve both clicked coordinates and deliberately select the next supported report shape.
4. Replace hard-coded owner/source cycling with source-capability-aware transitions. Null buckets, duplicate names and terminal levels need explicit behavior; unsupported clicks should not issue an invalid query.
5. Forecast summary drill resolves user IDs and switches to a deal detail table with the same period/team/user/pipeline/currency scope. Keep Back/Refresh/revision handling and ignore stale requests.
6. Apply Forecast tabular/summary capabilities to button changes, quick-add, drag/drop, imports and saved-definition hydration. Disable or explain unsupported group transitions before preview/save.

**Acceptance:** Click tests use IDs/enums from real backend responses; matrix and Forecast drills show valid, scoped data; Back restores the original visual. Multi-dimensional reports either render correctly through explicit bindings or do not offer an unsupported chart.

## Phase 5 — Preserve specifications and make library/export behavior reliable

**Findings:** RA-11–RA-13, RA-16–RA-20.

1. Normalize one sort schema at API admission, supporting existing `dir`/`direction` aliases during compatibility handling. Use typed access throughout generic and Forecast queries; validate aggregate aliases consistently.
2. Preserve sorting and supported saved specification properties when a user changes a report's name or guided scope. Make preview/save compile from the same draft model; make limit/offset behavior explicit rather than dropping settings incidentally.
3. Validate real calendar dates, normalize whole-number page values, and define an inclusive end-day filter with an exclusive next-day API boundary. Handle reversed ranges and restored saved views. Follow existing user date formatting/time-zone conventions without adding a new timezone feature.
4. Decide bounded synchronous exports versus existing asynchronous export jobs. Above the safe synchronous limit, offer a full-data job or a clear rejection/confirmation; never return a partial file with an unqualified success toast. Preserve source/export permissions, scope, currency grouping and spreadsheet protection for the entire job.
5. Gate Analytics controls by their actual create/edit capability. Adding/removing a widget updates a board; deleting the board is a different operation. View-only users retain refresh and permitted drill viewing.
6. Show loading/failed states and retry for report counts. Source reference queries should distinguish unavailable references from temporary loading failures.
7. Catch known import validation errors only. Unexpected failures return a sanitized retryable server response, preserve transaction rollback and keep invalid-file/reference errors distinct from infrastructure errors.
8. Add server search/pagination for widget report selection and comparison. Do not assume the first 200 reports are the complete accessible list.
9. Resolve relationship reference fields from source metadata. Include Calls `call_owner_id` and Meetings `host_user_id` in backend validation and import mapping. Add missing/foreign UUID preview and revalidation tests for every supported source, including array filters.

**Acceptance:** End-day reports remain visible; invalid URLs cannot poison the list; sort order round-trips through import/edit/run; full export is complete or explicitly bounded; errors do not resemble zero data; users can select reports beyond page one.

## Testing and delivery

Use the existing backend pytest and frontend TSX/Playwright runners. Turn each diagnostic into a failing behavioral regression before applying its repair. Diagnostics that assert the current bug exists are evidence, not the final regression suite.

Minimum cross-layer journeys:

| Journey | Required assertions |
| --- | --- |
| New/edit report | Persist and reload name, module, pipeline, currency, advanced filters and sort; live matching data changes independently per report. |
| Analytics | Real board API round-trip; two widgets with different report scopes; native pipeline persistence; user/enum/matrix/Forecast clicks; Back/refresh after report edit. |
| Import/export | Definition version and duplicate strategies; foreign/deleted references; malformed items; bounded files; transaction failure; full-data CSV/XLSX and formula protection. |
| Permissions | Admin, team manager and standard/view-only profiles; hidden fields, denied modules, foreign tenant IDs and private report assignment. |
| Legacy/recovery | Valid old shapes, incompatible entries alongside healthy entries, source failures, missing pipeline, deleted report and unavailable counts. |
| Money | Single currency, grouped currencies, missing currency, uneven averages, pagination and full export totals. |

After each implementation batch, run complete applicable CI checks for the affected repositories according to their current workflows. Cross-repository contracts need both suites, including PostgreSQL/Redis opt-in and migration checks where applicable. Use disposable services/databases; preserve existing application data and running services. Build with safe fixture API/OAuth configuration, verify lockfile installation and dependency audits, refresh the workspace Graphify graph after application changes, and check conflicts before/after.

Before stage promotion, complete the workspace deployment audit against the exact CI-validated commits. Verify actual deployed UI/API contracts and authorized staging accounts. Passing mocked browser fixtures or a health endpoint is not stage verification.

## Completion criteria

- Every High finding is repaired and has meaningful behavioral regression coverage.
- Native widget configuration, typed drill-down and monetary totals are connected through real API contracts.
- All remaining findings have a verified repair or a clearly approved product limitation; no silently dropped configuration or partial-success downloads.
- Reports and Analytics expose only supported features for the user's permissions and source capabilities.
- The implementation report records fresh checks, skips, legacy-data repair decisions and deployment status accurately.

Sharing UI remains outside this plan. Its existing APIs are secured in Phase 1 without expanding the agreed feature scope.
