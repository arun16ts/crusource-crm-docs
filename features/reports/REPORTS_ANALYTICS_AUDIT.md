# Reports and Analytics audit

**Date:** 14 October 2026  
**Status:** Audit findings; application fixes have not been applied.  
**Scope:** CRM Reports, Analytics boards, report-backed charts, definition imports/exports, saved views and Forecast reports. The separate VMS applications are outside this audit.  
**Next steps:** [Fix implementation plan](REPORTS_ANALYTICS_FIX_IMPLEMENTATION_PLAN.md).

## Assessment

Yesterday's work is substantially connected across the UI and API, but it is not ready to describe as complete and free of broken flows. This audit identifies **20 findings: 7 High, 11 Medium and 2 Low**. Four concern security boundaries or spreadsheet output. Others concern persistence, financial calculations, drill-down, legacy compatibility and error handling.

The strongest example of a half implementation is the native widget pipeline selector: the frontend sends the selected pipeline in `widget.config`, while the backend widget schema has no `config` field and silently discards it. The selected pipeline does not survive saving. Passing compilation and the existing mocked browser fixtures did not catch that contract mismatch.

This is a source review and local fixture audit, not a staging penetration test or a guarantee that every possible defect has been found. No stage or production data was read or modified.

## Baseline and method

- Frontend: `063e8c3c`, compared with `177ee485`; yesterday's commit changes 42 files.
- Backend: `3ef484a`, compared with `c8a04ff`; yesterday's commit changes 23 files.
- Both application repositories began clean. The docs repository already had an uncommitted change to `REPORTS_IMPLEMENTATION_REPORT.md`; it was preserved.
- Graphify was queried first for feature relationships. Findings were then verified in application source, not inferred from the graph or the previous implementation report.
- Traced UI → service → route → handler → persistence/query → response → visualization for each feature below. Reviewed actual CI workflows and manifests: frontend Next.js 16.3.8 / React 19.2.4, CI Node 20; backend CI Python 3.12.
- Applied the installed Graphify, systematic-debugging, code-security, API security, secure-code-review, React, browser testing and verification guidance. The API security skill's referenced `docs/fixer-policy.md` is absent from this workspace; repository authorization and preservation rules govern this audit. That missing reference is a tooling limitation, not permission to change application code.
- Created disposable diagnostic scripts under [audit evidence](../../../validation/reports-analytics-audit-20261014/). They use isolated test fixtures and exercise defects deliberately. A passing diagnostic means the defect was reproduced, not repaired.

## Implementation coverage

| Capability | UI and API coverage | Audit conclusion |
| --- | --- | --- |
| Create/edit/name reports; saved pipeline and currency | Builder → Reports service → create/update handlers → stored specification → run | Connected. Independent saved scope has regression coverage. Sorting/settings preservation and legacy handling still need repairs. |
| Library search, highlighting, filters, pagination | URL state → list API → scoped repository → table/highlight | Connected. Date boundaries and malformed URL input are faulty. |
| Saved library views | Reports control → shared hook/service → saved-view API | Connected, with failure/retry and explicit-URL precedence. A saved view changes the library list, not report data criteria. |
| Definition JSON export/import | Mounted modals → service → registered routes → validation/import/export handlers | Connected. Name conflicts, versions, quotas and private imports are present. Reference mapping misses Calls/Meetings ownership fields, and unexpected exceptions are handled incorrectly. |
| Report results and CSV/XLSX | Run modal → run/export routes → scoped source query → downloadable file | Connected. Silent 10,000-row truncation and matrix XLSX formula injection remain. |
| Forecast reports | Builder/source settings → Forecast adapter → existing authorized Forecast queries | Connected for tabular and summary. Drag/drop can select unsupported matrix mode; chart drill-down does not switch to the detail presentation it produces. |
| Report-backed Analytics | Add widget → stored report ID → run saved report → chart mapper | Connected. Board-wide selectors are removed as agreed. Multi-dimensional charts and typed drill-down remain faulty. |
| Native Sankey/cohort pipeline selection | New selector → `config.pipeline_id` → board API | **PARTIALLY IMPLEMENTED:** frontend exists; backend drops configuration. |
| Internal sharing / team assignment | Existing routes/services; unused Reports sharing modal/callback; team display exists | Sharing controls were intentionally deferred by the approved plan. Do not label their absence as an accidental failure of yesterday's delivery. Existing write endpoints still require security fixes. |
| Backend grouped KPI compatibility | Backend permits grouped KPI/target; frontend now permits only ungrouped totals | Contract disagreement. Resolve through the chart contract work in RA-08; grouped results must not become a first-row-only total. |
| Other native dashboard chart types | Frontend's shared widget union includes welcome/task/activity widgets; Analytics board API accepts a narrower union | Existing contract distinction. These are not offered in the Analytics Add Widget flow; do not enable them there without an explicit supported contract. |

## Findings

### RA-01 — High — Suggestions expose data from a denied module

**Origin:** Existing defect, uncovered by the broader audit.  
**Impact:** A user allowed to view Reports but denied Accounts can obtain account names through `GET /reports/fields/accounts/account_name/suggestions`.

The suggestions handler scopes generic values and relationship lookups by organization alone. The request-wide ORM boundary does not add Accounts module visibility. A local HTTP probe, with that boundary explicitly active, returned a restricted account name with status 200 while the canonical Accounts scope returned no records.

**Source:** [suggestions handler](../../../crusource-crm-backend/src/modules/reports/handlers/get_field_suggestions_handler.py), [record read boundary](../../../crusource-crm-backend/src/shared/auth/record_read_boundary.py).  
**Security mapping:** OWASP API1/API3:2023; ASVS V4.1.3/V4.2.1; CWE-862. Authentication and tenant filtering alone are insufficient. Apply source-module, record and field permissions before returning values, including linked names and emails.

### RA-02 — High — Team assignment bypasses private report access

**Origin:** Existing defect.  
**Impact:** A team manager with Reports edit capability can reassign another user's private report using its ID, despite being denied its normal lookup.

The assignment handler falls back from the scoped report lookup to an organization-only lookup, then authorizes based on destination team management. The probe reproduced a denied lookup followed by a successful change from private to team visibility. This reveals the private definition and grants subsequent editing through `assigned_by_id`.

**Source:** [assignment handler](../../../crusource-crm-backend/src/modules/reports/handlers/assign_team_report_handler.py).  
**Security mapping:** OWASP API1/API5:2023; ASVS V4.2.1; CWE-639. Require authority over the source report and destination team independently. Team management must not imply control over every private report in the organization.

### RA-03 — High — Write references can cross organizations

**Origin:** Existing defect.  
**Impact:** Create/edit/share/assignment paths accept team or assignee IDs without consistently resolving them in the caller's organization and destination team. A report creation probe accepted a foreign-organization assignee and returned that user's name in its response.

Scope validation added yesterday checks IDs inside the report's data filters. It does not validate outer sharing/assignment fields. Joined response mapping can expose the foreign name even with the request record boundary active.

**Source:** [create](../../../crusource-crm-backend/src/modules/reports/handlers/create_report_handler.py), [update](../../../crusource-crm-backend/src/modules/reports/handlers/update_report_handler.py), [share](../../../crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py), [mapper](../../../crusource-crm-backend/src/modules/reports/handlers/mapper.py).  
**Security mapping:** OWASP API1/API3:2023; ASVS V4.2.1; CWE-862. The demonstrated leak is a foreign user's name; this audit does not claim arbitrary foreign record contents are readable.

### RA-04 — Medium — Matrix XLSX row labels remain executable formulas

**Origin:** Existing defect incompletely addressed by yesterday's spreadsheet hardening.  
**Impact:** An exported matrix can contain an executable spreadsheet formula from a record's text value.

Headers and numeric cells are sanitized, but the first cell of each matrix data row is appended as raw text. A real report/export probe using `lead_source='=1+1'` produced XLSX cell A2 with value `=1+1` and `data_type='f'`, rather than literal text. Actual execution depends on the spreadsheet reader; arbitrary code execution was not demonstrated.

**Source:** [result export handler](../../../crusource-crm-backend/src/modules/reports/handlers/export_report_results_handler.py).  
**Security mapping:** ASVS V5.3.1; CWE-1236. Apply the same text-cell protection to every matrix label, header and footer; preserve numeric cells as numbers.

### RA-05 — High — Native widget pipeline configuration is discarded

**Origin:** Yesterday's frontend addition lacks its backend contract.  
**Impact:** Sankey/cohort widgets revert to All pipelines after saving or reloading, so selecting a pipeline still fails to control the visualization reliably.

The Add Widget and inline selector write `config.pipeline_id`. Backend `WidgetSpec` has no `config`; Pydantic ignores it and handlers serialize the reduced model. A create-board probe confirmed the returned and persisted widget contains no configuration.

**Source:** [frontend widget contract](../../../crusource-crm-frontend/src/services/analyticsBoards.service.ts), [Add Widget](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx), [backend widget schema](../../../crusource-crm-backend/src/modules/analytics_boards/queries/analytics_boards_queries.py), [board update](../../../crusource-crm-backend/src/modules/analytics_boards/handlers/update_board_handler.py).

### RA-06 — High — Matrix totals are mathematically unsafe

**Origin:** Existing calculation defect; currency grouping is now an explicitly supported way to save monetary reports.  
**Impact:** Reports, widgets and downloads show misleading totals.

The matrix builder sums displayed cells regardless of aggregate function or unit. Probes produced a grand total of 300 from USD 100 and INR 200, and a total of 30 from averages 10 and 20. Averaged groups require weights; minima and maxima require their own reducers. Pagination occurs before pivot construction, so displayed totals can also describe only the returned group page.

**Source:** [query builder](../../../crusource-crm-backend/src/modules/reports/services/report_query_builder.py), `_build_matrix_data` and grouped pagination. Suppress totals across incompatible currencies and derive legitimate totals from the full scoped data, rather than adding visible cells.

### RA-07 — High — Drill-down values do not round-trip

**Origin:** Existing problems plus yesterday's stricter UUID validation exposing an existing name/ID mismatch.  
**Impact:** Clicking legitimate chart buckets can produce an error or an empty breakdown.

Three reproduced failures:

1. Owner grouping returns a display name under `deal_owner_id`; the chart sends that name back, while the new scope validator requires a UUID: HTTP 400.
2. Enum grouping displays `Not Contacted`; filtering for that display label fails to match stored `not_contacted`: no records.
3. Matrix drill replaces two group dimensions with one while retaining `report_type='matrix'`: rejected by the backend.

**Source:** [Widget drill builder](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx), [row serialization/query builder](../../../crusource-crm-backend/src/modules/reports/services/report_query_builder.py), [scope validator](../../../crusource-crm-backend/src/modules/reports/services/report_scope.py). Preserve canonical bucket values separately from labels, both matrix coordinates and all saved criteria.

### RA-08 — Medium — Chart compatibility allows data the mapper cannot render

**Origin:** Existing mapper limitation; backend and frontend compatibility rules also diverge after yesterday's KPI change.  
**Impact:** Valid reports can display zero or misleading values in an offered chart.

A summary grouped by source and currency is offered Pie/Donut. The mapper treats the second column (`currency`) as the metric, turning INR into zero despite `amount_sum=200`. Bar/Line treat every column after the first as a metric, including string dimensions. KPI selects the first numeric metric/row, while backend validation still permits grouped KPI reports.

**Source:** [chart mapper](../../../crusource-crm-frontend/src/lib/reportToChartData.ts), [frontend compatibility](../../../crusource-crm-frontend/src/lib/widgetCompatibility.ts), [backend compatibility](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py). Chart bindings must explicitly distinguish dimensions, metrics and their units.

### RA-09 — Medium — Forecast drill produces details but keeps the summary chart

**Origin:** Yesterday's addition.  
**Impact:** Clicking a Forecast summary returns a tabular deal result but keeps Bar/Pie/Donut rendering. The drill plots amount and weighted amount together, plus string currency/stage/owner columns, regardless of the original selected metric.

**Source:** [Widget](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx), [mapper](../../../crusource-crm-frontend/src/lib/reportToChartData.ts). The frontend diagnostic reproduced the generated series list. Render Forecast deal drill results as a detail table, or construct an explicit supported breakdown rather than feeding detail columns into the original chart. Back must restore the summary chart and scope.

### RA-10 — High — An incompatible legacy definition breaks the library

**Origin:** Newly tightened schema exposes legacy-data risk.  
**Impact:** One saved definition rejected by current `ReportSpec` validation can cause HTTP 500 for the whole report list, get/export, or board metadata decoding.

Stored definitions are decoded without a compatibility/error boundary in the mapper and several handlers. A local list HTTP probe with a legacy extra specification field produced 500. Yesterday's schema newly forbids extra fields and tightens filter values. No deployed legacy record was inspected, so the number of affected real reports is unknown.

**Source:** [report schemas](../../../crusource-crm-backend/src/modules/reports/queries/report_queries.py), [mapper](../../../crusource-crm-backend/src/modules/reports/handlers/mapper.py), [run handler](../../../crusource-crm-backend/src/modules/reports/handlers/run_report_handler.py). Provide safe legacy normalization and per-report invalid status; do not erase unsupported criteria or broaden execution silently.

### RA-11 — Medium — Calendar end dates and URL validation are incomplete

**Origin:** Existing date boundary defect; malformed URL acceptance is new.  
**Impact:** Selecting an end day hides reports updated later that day. Edited/bookmarked URLs can cause request validation errors.

`updated_to='2026-10-13'` becomes midnight and is applied with `<=`; a report updated at 14:00 on that date is excluded. The URL parser also accepts page 1.5 and impossible dates such as 2026-99-99, forwarding them to integer/datetime API parameters.

**Source:** [library URL hook](../../../crusource-crm-frontend/src/hooks/useReportLibraryState.ts), [list repository](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py). Define inclusive calendar-day behavior with an exclusive next-day boundary and normalize integer pagination and real dates.

### RA-12 — Medium — “Full data” export silently stops at 10,000 rows

**Origin:** Existing defect.  
**Impact:** Users receive a successful download and success toast while matching records are omitted.

The export handler requests 10,000 rows. The server returns total rows in `X-Total-Rows`, but the frontend's Blob method discards this metadata. A bounded handler probe returned 10,000 downloaded rows for a 10,001-row result. This probe stubbed the source result to isolate export behavior; it did not create 10,001 database records.

**Source:** [export handler](../../../crusource-crm-backend/src/modules/reports/handlers/export_report_results_handler.py), [frontend service](../../../crusource-crm-frontend/src/services/reports.service.ts), [run modal](../../../crusource-crm-frontend/src/components/reports/ReportRunModal.tsx). Use the existing export-job design for full results, or reject/explain the cap before success. Do not remove the safety limit without resource controls.

### RA-13 — Medium — Sort contracts conflict and edits drop saved settings

**Origin:** Existing ordinary-sort mismatch; Forecast uses a new incompatible interpretation.  
**Impact:** Sorted imports/API reports reject requests or run in the wrong order; opening and saving a report can remove its sorting.

Frontend sends `dir`; backend `ReportSortSpec` documents `direction`; generic validation expects dictionary `dir`; Forecast execution reads `direction`. Probes showed generic `direction='desc'` rejected and Forecast `dir='desc'` silently executed as ascending. Builder initializes columns/criteria but reconstructs a specification without preserving `sort`, `limit` or `offset`.

**Source:** [schemas](../../../crusource-crm-backend/src/modules/reports/queries/report_queries.py), [Forecast source](../../../crusource-crm-backend/src/modules/reports/services/forecast_report_source.py), [builder](../../../crusource-crm-frontend/src/components/reports/ReportBuilder.tsx). Adopt one normalized typed sort contract with legacy aliases. Decide explicit builder execution defaults and preserve supported saved settings during unrelated edits.

### RA-14 — Medium — Default revenue widget uses an incorrect won predicate

**Origin:** Existing seed-template defect.  
**Impact:** A newly created Analytics board's Total Revenue widget can show no value despite won deals.

The seed filters the stage name by `closed_won`, but the query resolves `stage` to `PipelineStage.name`; a legitimate `Closed Won` stage does not match. A fixture with a USD 100 won deal yielded `amount_sum=None`. Monetary templates also bypass the new currency-save admission rules because the default-board query writes models directly.

**Source:** [default board seed handler](../../../crusource-crm-backend/src/modules/analytics_boards/handlers/get_or_create_default_board_handler.py), [stage filter resolution](../../../crusource-crm-backend/src/modules/reports/services/report_query_builder.py). Resolve won status through the domain's stage type and seed templates through the same validated creation policy.

### RA-15 — Medium — Forecast drag/drop bypasses the matrix restriction

**Origin:** Yesterday's addition did not guard all interaction paths.  
**Impact:** Although the Matrix button is disabled for Forecast, dropping a second group field sets matrix mode. The backend then rejects preview/save because Forecast supports tabular/summary only.

**Evidence level:** Source-verified control flow; no automated pointer-drag reproduction was run.  
**Source:** [builder](../../../crusource-crm-frontend/src/components/reports/ReportBuilder.tsx), `handleDragEnd`; [Forecast source validation](../../../crusource-crm-backend/src/modules/reports/services/forecast_report_source.py). Apply source capabilities to every mode transition, including drag/drop and imported definitions.

### RA-16 — Medium — Analytics exposes edits to view-only users

**Origin:** Existing UI permission gap, also affecting yesterday's inline pipeline edit.  
**Impact:** Users see Add/Remove/drag/resize/pipeline controls and receive forbidden errors when persisting changes.

The board checks only Analytics view permission, whereas API create/edit/delete guards are distinct. Existing server checks prevent this from being an API authorization bypass.

**Evidence level:** Source-verified UI/API mismatch.  
**Source:** [Analytics board](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx), [routes](../../../crusource-crm-backend/src/modules/analytics_boards/routes/analytics_boards_routes.py). Match each visible control to its actual endpoint capability; removing a widget edits a board rather than deleting the board resource.

### RA-17 — Low — Count failures appear as genuine zeros

**Origin:** Yesterday's count-query addition.  
**Impact:** KPI cards display zero while summary counts are loading or failing, without indicating unavailable counts or offering retry.

**Evidence level:** Source-verified error-state omission.  
**Source:** [Reports home](../../../crusource-crm-frontend/src/components/reports/ReportsHome.tsx), count query/defaults. Preserve a distinction between unknown/loading/failed and an actual zero.

### RA-18 — Medium — Import preview treats server failures as invalid user files

**Origin:** Existing broad exception handling is now reachable through yesterday's registered import routes.  
**Impact:** Database/service exceptions are converted into per-definition invalid-specification messages, potentially reflecting internal exception detail and sending users into unnecessary reference repairs.

**Evidence level:** Source-verified catch of `Exception` and interpolation of `str(e)`; an actual outage or production secret leak was not simulated.  
**Source:** [import handler](../../../crusource-crm-backend/src/modules/reports/handlers/import_report_definitions_handler.py). Catch known user validation failures; return a sanitized retryable server failure for infrastructure errors. Keep diagnostic details in protected logs. Security mapping: ASVS V7.4.1; CWE-209.

### RA-19 — Low — Widget report picker stops at 200 accessible reports

**Origin:** Existing limitation.  
**Impact:** Reports outside the first 200 cannot be selected for a new widget or comparison, despite being available in the Reports library.

**Evidence level:** Source-verified `listReports({limit:200})` with no next-page/search fetch.  
**Source:** [Add Widget](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx). Add scoped server search and pagination to both primary and secondary selection.

### RA-20 — Medium — Calls/Meetings ownership references miss validation and mapping

**Origin:** Yesterday's reference handling is incomplete for activity sources.  
**Impact:** Imported Calls or Meetings reports containing missing/foreign owner IDs are marked valid, with no mapping controls to repair them. They can import successfully and subsequently return no matching data.

The backend scope validator and frontend mapping UI handle `owner_id`, `deal_owner_id` and `host_id`. Actual report fields are `call_owner_id` for Calls and `host_user_id` for Meetings. A preview probe supplied nonexistent UUIDs in both actual fields; both definitions were classified valid. Field-registry validation confirms the fields exist but does not validate those references.

**Source:** [field registry](../../../crusource-crm-backend/src/modules/reports/services/field_registry.py), [scope validator](../../../crusource-crm-backend/src/modules/reports/services/report_scope.py), [import mapping UI](../../../crusource-crm-frontend/src/components/reports/modal/ImportReferenceMappings.tsx). Build reference validation/mapping from the actual source field metadata rather than maintaining mismatched hard-coded field lists. This is a functional import gap; the probe did not demonstrate disclosure of foreign activity data.

## Architecture observations

- Narrow command/query handlers and services are largely present, and Forecast calculations reuse existing domain queries. Do not rewrite those calculations independently to repair chart presentation.
- Chart capability logic is duplicated in frontend/backend and has diverged (RA-08). Sort parsing also has three interpretations (RA-13). A typed contract and shared fixtures are more useful than adding more conditional branches.
- The default-board query performs writes and bypasses normal report creation validation (RA-14). Separate read resolution from idempotent template provisioning commands.
- Builder transient editing state is appropriate locally, but the selected fetched report is stored in Redux as a server snapshot. Follow-up cleanup should store its ID and load current metadata through TanStack Query, with a deliberate draft/revision policy; do not claim an actual concurrent-edit loss was reproduced here.
- Import validation/execution share a file and the route module contains late imports/dependency parsing. Refactor only alongside functional fixes, preserving transaction and permission behavior.

## Verification and limits

| Fresh check | Result |
| --- | --- |
| Existing backend Reports/Analytics/Forecast group | 116 passed. |
| New backend diagnostics | 15 cases reproduced; 1 diagnostic-plugin warning. See [script](../../../validation/reports-analytics-audit-20261014/audit_backend.py) and [log](../../../validation/reports-analytics-audit-20261014/backend-diagnostics.log). |
| Frontend diagnostic helper checks | Four cases reproduced: multi-dimensional chart bindings, Forecast detail series, malformed URL state. See [script](../../../validation/reports-analytics-audit-20261014/audit_frontend.ts) and [log](../../../validation/reports-analytics-audit-20261014/frontend-diagnostics.log). |
| Frontend Node 20.20.2 checks | Full `npm run test`, Reports contracts, spreadsheets, full lint and TypeScript all passed. |
| Browser fixtures | Reports and Forecast browser regressions passed. They render real components with mocked services; they are not a real frontend-to-deployed-API integration check. |
| Backend Ruff / compilation | Passed. |
| Full backend general suite | Retry outside sandbox: **2,076 passed, 85 skipped, 1,735 existing warnings**, exit 0. Initial sandbox run had 2,053 passes and 23 setup errors, all caused by denied pytest temp-directory access. See [final suite log](../../../validation/reports-analytics-audit-20261014/backend-full-suite-retry.log). |
| Documentation and conflicts | 331 local references resolve; finding counts checked. Application repositories remain clean; no unmerged entries or source conflict markers found. Docs `git diff --check` passed. The pre-existing implementation-report edit remains preserved. |

The audit does not refresh dependencies, run a production build, re-run every unrelated frontend browser suite, or claim complete CI/deployment parity. PostgreSQL migration/locking groups, Redis opt-in groups, fresh dependency audits, and staging account/browser flows were not revalidated here. Yesterday's recorded CI evidence remains historical evidence, not a substitute for those checks before a fix is promoted. No new application migration was required by this read-only audit.

No application source, existing test, credential, database schema or deployment was changed. The diagnostic files and this documentation are the audit deliverables. Existing documentation changes were preserved.
