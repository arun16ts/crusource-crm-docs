# Reports improvements and Analytics scope implementation plan

**Date:** 13 October 2026  
**Status:** Approved plan; application changes are implemented locally. See the [implementation report](REPORTS_IMPLEMENTATION_REPORT.md) for final validation and deployment status.  
**Scope:** CRM Reports, report-backed Analytics widgets, and Forecast reporting. The separate VMS repositories are unaffected.

Backend baseline: `c8a04ff3622e215897e293680bd1d4b758ae3a8d`. Frontend baseline: `177ee4855a6d3b14ceaae8aefad579b2607ca062`. Verification used actual source, router registration, schema probes, and 26 existing backend Reports tests. No authenticated staging/browser test was performed for this review.

## Agreed product behavior

- Users choose pipeline and currency while creating or editing a report, using easy controls rather than requiring them to assemble technical filter expressions.
- Save the criteria with the report specification. Running a saved report uses current matching data; saving criteria does not freeze a snapshot.
- Keep report names and optional Analytics widget titles editable through their existing naming controls. Do not add compulsory pipeline/currency badges to Analytics widgets.
- Remove the Analytics board-wide pipeline and currency selectors. Report-backed widgets can intentionally use different saved scopes on the same board.
- Drill-down retains every saved criterion and adds the clicked criterion. Back navigation restores the earlier report result.
- Currency selects matching records. No currency conversion is included. Monetary totals must be for one currency or separated by currency.

## Verification of the testing list

| Item                               | Verified state                                                                                                                                                                                                                      | Implementation decision                                                                                                                                                                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wrong export icon                  | **Confirmed in report results.** `ReportRunModal` uses Lucide `Upload` for Export. The Reports library and JSON export modal already use `Download`.                                                                                | Use the existing download/export convention for all export actions; reserve Upload for import. Keep explicit labels and accessible names.                                                                                                     |
| Search highlighting                | Name search is debounced and sent to the server. `ReportRow` renders the name as ordinary text and receives no search term.                                                                                                         | Highlight matching text only in returned report names, using a quiet static treatment. Keep row height, selection, sorting and keyboard focus stable.                                                                                         |
| Sharing Visibility without sharing | **Confirmed UI gap, not absent backend capability.** The filter is shown, a share endpoint and modal exist, but `ReportsHome` does not pass `onShareReport` or mount the sharing modal.                                             | For this scope, hide Sharing Visibility and the unavailable sharing-specific ownership options. Preserve existing backend visibility/access rules and already shared/system reports. Adding internal/public sharing is not part of this plan. |
| Import exported reports            | Definition export is connected. Frontend import service methods and backend validation/execution handlers exist, but there are **no registered import routes**. `ImportExportReportsModal` merely re-exports the export-only modal. | Complete JSON definition export/import round-trip with validation, conflict handling, reference resolution, and clear results. CSV/XLSX report-result downloads are data exports and are not report-definition imports.                       |
| Saved views                        | Shared saved-view UI, hook and API exist; the Reports page does not use them. The backend accepts an entity namespace string.                                                                                                       | Add Reports library saved views using the existing service with a `reports` namespace. A saved view organizes the report list; it does not modify a saved report's data criteria.                                                             |
| Consistent filter icon             | Reports toolbar uses Lucide `Filter`, while other list sections such as Tasks use `filter_list`; Reports' own filter-panel header already uses `filter_list`.                                                                       | Match the established list-section icon, dimensions, focus/active treatment, badge and accessible toggle behavior.                                                                                                                            |
| Forecast reports                   | Current report schemas support seven record entities and reject `forecast`. Existing Forecast summary/deal queries already calculate targets, actuals, weighted pipeline and attainment.                                            | Add a supported Forecast report source with typed settings and reuse Forecast calculations and access scope. It is more than adding a new label to the module dropdown.                                                                       |
| Analytics pipeline/currency        | Currency remains local to `AnalyticsBoard`; report execution ignores board pipeline and its query key has neither filter.                                                                                                           | Implement saved report scope in the builder; remove the toolbar selectors and retain saved criteria in visualization, comparison, drill-down and export.                                                                                      |

Evidence: [Reports home](../../../crusource-crm-frontend/src/components/reports/ReportsHome.tsx), [report results/export icon](../../../crusource-crm-frontend/src/components/reports/ReportRunModal.tsx), [report rows](../../../crusource-crm-frontend/src/components/reports/table/ReportRow.tsx), [filter panel](../../../crusource-crm-frontend/src/components/reports/filter/ReportsFilterPanel.tsx), [export modal](../../../crusource-crm-frontend/src/components/reports/modal/ExportReportsModal.tsx), [import/export alias](../../../crusource-crm-frontend/src/components/reports/modal/ImportExportReportsModal.tsx), [sharing modal](../../../crusource-crm-frontend/src/components/reports/modal/ShareReportModal.tsx), [report routes](../../../crusource-crm-backend/src/modules/reports/routes/report_routes.py), and [report schemas](../../../crusource-crm-backend/src/modules/reports/queries/report_queries.py).

## Additional issues to fix within this work

1. **Drill-down sends an invalid operator.** `Widget.tsx` sends `equals`; the backend enum accepts `eq`. A schema probe rejects `equals`. Correct the typed contract and test actual drill-down requests before relying on retained saved filters.
2. **Definition export can silently become incomplete.** On an API error or empty response, `ExportReportsModal` builds JSON from `availableReports`, which is the current paginated list. It can export only one page while displaying “All Reports”, or omit selected reports from other pages. Remove this success fallback; use an authoritative scoped export and show errors/retry.
3. **Report module and specification can disagree.** `SavedReportCreate` currently accepts outer `entity_type=leads` with a Deals specification. Creation stores the specification without calling the field/structure validator. Enforce source/module consistency and specification validation for create, edit and import.
4. **Import version is not enforced.** The validation schema accepts an unsupported `version='999'`. Validate supported versions and migrate known versions explicitly; reject unknown formats without creating reports.
5. **Saved-view retrieval hides failures.** `useSavedViews` catches API errors and returns an empty list. Show failure/retry distinctly from “no saved views”, and respect saved-view permissions when integrating it into Reports.
6. **Reports library state needs a clear owner.** Search, filters, sort and pagination currently live in Redux. Follow the workspace convention: URL owns shareable list state, TanStack Query owns fetched data, Redux owns modal/selection UI. Applying a view must reset pagination and incompatible row selection.
7. **Library counts and empty-state flags are incomplete.** KPI cards count at most the first 500 reports; `hasAnyFilters` only checks module/search. Obtain scoped count summaries without an arbitrary list cap and include every active list filter in the empty-state/reset behavior.
8. **Export permissions need alignment.** Current definition/data export routes require `reports.view`, although `canExport` exists in the frontend permission hook. Agree and enforce the Reports export capability in both UI and API; import requires the appropriate import/create capabilities. Preserve organization/record/field access at execution time.

Evidence: [Analytics Widget](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx), [saved-view hook](../../../crusource-crm-frontend/src/hooks/useSavedViews.ts), [create handler](../../../crusource-crm-backend/src/modules/reports/handlers/create_report_handler.py), [update handler](../../../crusource-crm-backend/src/modules/reports/handlers/update_report_handler.py), [command schemas](../../../crusource-crm-backend/src/modules/reports/commands/report_commands.py), and [report query builder](../../../crusource-crm-backend/src/modules/reports/services/report_query_builder.py).

## Phase 1 — Save report scope and make Analytics use it

### User flow

`New/Edit Report → choose module → name report → choose pipeline/currency where applicable → configure columns/metrics → preview → save → select report when adding an Analytics widget → optionally name widget`.

Add a compact **Report scope** section near the module/name controls:

- Pipeline: names from the current organization's compatible module pipelines, with All Pipelines available. Store the UUID and friendly label, not the pipeline name as the query value.
- Currency: use the existing CRM currency selector only when the selected data source supports currency. Explain briefly that it filters records.
- Modules without those fields should not show irrelevant controls.
- Monetary sum/average/target reports require one currency or explicit currency grouping. Counts can use All Currencies. Legacy mixed-currency reports must not be silently relabeled as one currency or silently converted.
- Existing simple saved filters populate these controls when editing. Complex pipeline/currency conditions remain visible in advanced criteria; do not erase or rewrite them merely to populate a simple dropdown.
- If a saved pipeline is deleted, inaccessible or incompatible with the module, show an actionable error instead of dropping the condition and broadening the report.

### Implementation

1. Use existing `spec.filters` as the canonical storage for ordinary record reports: `pipeline_id eq <uuid>` and `currency eq <code>`. Pipeline/currency already exist as filterable fields for Leads/Deals. All means absence of that guided restriction; other advanced restrictions remain intact.
2. Build the execution/save specification once in a shared typed helper. The builder currently assembles similar specifications separately for preview and save. Reuse the helper for preview, create/edit, and export/import validation.
3. Validate field availability, UUID/module consistency, currency and compatible aggregation on the backend. Reuse the existing field registry and scoped report query builder. Do not trust UI filtering for authorization.
4. Keep current name validation and existing optional widget title. A widget's title is independent of the report's name; neither changes the stored criteria.
5. Remove `selectedPipelineId`, `selectedCurrency`, their toolbar controls and the default-pipeline reset effect from `AnalyticsBoard`.
6. Run report-backed widgets from the saved specification. Comparators execute each selected report with its own saved scope. Do not add board overrides or mutate saved reports while viewing a board.
7. Fix drill-down to use `eq`, retain the original filters, preserve currency formatting, and clear/recompute drilled results when the underlying saved report changes. Ignore stale in-flight responses from an earlier report revision. Reset cached report runs and referenced board results after a report edit.
8. Return/use monetary context for chart axes, tooltips, KPI values, tables and exports. The existing KPI formatter defaults to user/org currency, so filtering INR records alone is insufficient to ensure INR display. Do not add compulsory widget scope badges.

**Existing native widgets:** welcome/activity/task widgets have their own APIs and are not saved-report visualizations. Pipeline-aware native stage-health/funnel/cohort widgets currently depend on the board pipeline prop. When removing the toolbar, preserve their pipeline context in `widget.config` and expose it through their own Add/Edit Widget configuration. Do not accidentally remove their filtering or imply they are driven by an unrelated saved report. This compatibility handling is limited to native widgets; report-backed widget criteria remain owned by Reports.

Sources: [builder](../../../crusource-crm-frontend/src/components/reports/ReportBuilder.tsx), [field registry](../../../crusource-crm-backend/src/modules/reports/services/field_registry.py), [Analytics board](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx), [run hook](../../../crusource-crm-frontend/src/hooks/useRunReport.ts), [comparator](../../../crusource-crm-frontend/src/components/analytics/charts/ComparatorWidget.tsx), [KPI formatter](../../../crusource-crm-frontend/src/components/analytics/charts/KPICardWidget.tsx), and [stage-history service](../../../crusource-crm-frontend/src/services/stageHistory.service.ts).

**Acceptance:** save Pipeline A/INR, reopen it, and get the same matching criteria. Add another report for Pipeline B/USD to the same board and see independent totals. Edit the first report and its widgets update. Drill-down never introduces another pipeline/currency. Unauthorized records remain excluded in preview, run, drill-down and export.

## Phase 2 — Reports list usability and saved views

1. Correct the result-export icon and align the filter toggle with the established list-section convention. Provide accessible labels, focus behavior and expanded state.
2. Pass the applied, debounced name-search term into report rows. Use safe React text segments and a subtle static `<mark>` treatment. No flashing, auto-scrolling, whole-row highlighting or layout shift; clear highlights when search is cleared. Escape regex characters and test punctuation/unicode. The existing [HighlightMatch](../../../crusource-crm-frontend/src/components/search/HighlightMatch.tsx) can be reused after checking its literal-matching behavior; it currently compares escaped terms to displayed chunks, which needs care for punctuation.
3. Hide Sharing Visibility and unsupported sharing-specific ownership controls. Clear their stale persisted UI values and remove obsolete filter chips/counts so hidden filters cannot keep narrowing the list. Keep backend visibility metadata and permission checks unchanged. This does not implement public links or an internal Share & Assign flow.
4. Add the shared Saved Views control for `entity_type='reports'`. Save library search, module/source, report type, supported ownership, date filters, sorting and page size. Do not save current page, selected row IDs or open modal state. Do not confuse this with a saved report definition.
5. Implement default-view loading, applying, naming, updating and deleting with the existing per-user/org saved-view service. Apply through one list-state adapter, reset to page one, and honor read/create/edit/delete permissions. Surface loading and failures.
6. Move shareable list state into a focused URL hook with backward-compatible defaults. Reuse existing TanStack list queries; avoid duplicating server entities in Redux.
7. Fix full-filter empty-state handling and KPI count completeness. Use a scoped count query rather than loading every report into the browser.

UX checks follow the [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md), particularly semantic controls, accessible names, stable layout, focus and URL state. Scope is the Reports interactions above, not an unrelated application-wide redesign.

**Acceptance:** a saved view restores the library state after reload; it never changes report criteria. Name matches are readable without shifting rows. All filter combinations show the correct reset/empty behavior. Sharing controls are absent while existing accessible reports remain accessible.

## Phase 3 — Complete report-definition import/export

### User flow

`Export definitions as JSON → Import Reports → choose JSON → validate → resolve duplicate names and unavailable references → confirm import → show imported/skipped/invalid results → open imported report`.

Keep the two export purposes explicit:

- **Report definitions (JSON):** report names, sources, specification and saved criteria; supported for round-trip import.
- **Report data (CSV/XLSX):** current result rows; cannot reconstruct a report specification and is not accepted by Import Reports.

### Implementation

1. Keep definition export authoritative and scoped on the server. Support selected IDs across pages, and a clearly stated All Accessible / Current Filter export scope. Do not label a current-page fallback as All Reports. Surface authorization/network failures instead of producing an apparently successful partial file.
2. Add an actual import UI. The current `ImportExportReportsModal` alias is export-only; do not treat it as an implemented importer.
3. Register `/api/v1/reports/import-definitions/validate` and `/api/v1/reports/import-definitions` with appropriate permissions. Thin routes delegate to a validation query and import command; repositories own reads/writes. Refactor existing functional handlers where necessary rather than duplicating them.
4. Validate the versioned envelope, source/module consistency, names, columns, operators, supported aggregates and typed Forecast configuration. Reject arbitrary executable expressions or unknown schema features. Add concrete request/file limits: proposed first-release limits are one JSON file, at most 5 MiB and 100 definitions, with documented bounds for filters/columns and nesting.
5. Provide rename, skip and cancel choices for duplicate names. Handle duplicate names within the upload as well as existing reports. Recheck on execution; a preview is not an authorization or uniqueness reservation.
6. Resolve pipeline/stage/user/team references against the destination organization. For another organization's exported UUID, require a compatible destination mapping or mark the definition invalid. Never silently drop a filter or share grant to make an import succeed.
7. Imported reports default to private, receive fresh IDs and belong to the importing user/org. Source IDs and exported visibility do not confer authority in the destination. Reject attempts to promote an imported report to a system default without an authorized explicit operation.
8. Use an atomic confirmed import batch: schema-invalid items must be corrected or explicitly skipped before execution; an execution failure rolls back the batch. Preserve the existing duplicate strategy semantics, provide a clear imported/skipped summary and refresh report-list counts/cache.
9. Review concurrency-safe naming guarantees and migration needs before adding a uniqueness constraint. Existing create and import name checks differ in case handling and visibility scope; adopt one explicit policy without exposing another user's private report names.

Sources: [frontend report service](../../../crusource-crm-frontend/src/services/reports.service.ts), [definition export handler](../../../crusource-crm-backend/src/modules/reports/handlers/export_report_definitions_handler.py), [existing import handlers](../../../crusource-crm-backend/src/modules/reports/handlers/import_report_definitions_handler.py), and [existing direct-handler tests](../../../crusource-crm-backend/tests/test_reports_remediation.py).

**Acceptance:** exporting then importing retains names, columns, grouping, criteria and Forecast settings. API route tests—not only direct handler tests—exercise validation and execution. CSV/XLSX result files, unsupported versions, foreign/unmapped references, oversized uploads and permission failures produce actionable errors without partial unauthorized creations.

## Phase 4 — Forecast as a Reports source

Add **Forecast** to the source picker, filter/KPI categories, report list, import/export schemas and compatible Analytics widget selection.

Recommended first-release templates:

| Template              | User choices                                                    | Output                                                                                                                       |
| --------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Target vs Actual      | Period, compatible pipeline, one currency, permitted users/team | Target, closed-won actual, remaining gap and attainment.                                                                     |
| Weighted Pipeline     | Period, pipeline, currency and permitted scope                  | Open weighted amount and projected total using current stage probabilities.                                                  |
| Forecast by User/Team | Same scope controls; user/team grouping                         | Authorized user summaries and correctly calculated team totals.                                                              |
| Forecast Deal Details | Period, pipeline, currency and supported Forecast bucket        | Deal amounts, weighted amounts, stage, owner and close-date details, including supported missing/slipped-close-date buckets. |

Implementation:

1. Add a typed Forecast specification and execution adapter alongside existing record reports. Proposed shape: `entity_type='forecast'`, existing report presentation type, and a validated `forecast` configuration containing view/template, period type/key, pipeline, currency, permitted team/user selection and supported deal bucket where applicable. Preserve existing ordinary report schemas and stored definitions.
2. Extend strict API/frontend unions, field metadata and all related create/edit/run/export/import validators deliberately. Do not route Forecast into the generic SQL `MODEL_MAP` as though it were a single database table.
3. Reuse the existing Forecast summary/deal query use cases, `forecast_service` period/deal classification, scope helpers and repositories. Extract reusable calculations if needed; do not copy weighted probability, terminal-stage, slipped-date or target math into Reports handlers/components.
4. Require Reports permissions and Forecast read permission; resolve current organization/user/team scope at execution time, including exports and drill-down. Saving or importing a report does not grant access to additional users or targets.
5. Save selected period type/key explicitly. Results remain live within that saved period. Defaults and period boundaries follow Forecast's existing rules; no new snapshot/history feature is included.
6. Require one currency for money templates. Reuse Forecast mixed-currency safeguards for supported count/grouped views. Missing targets remain missing, and attainment cannot divide by zero. Aggregate percentages from their underlying totals rather than averaging user percentages.
7. Respect existing target semantics: targets are currently user/period/currency based, not pipeline-specific. A pipeline-filtered actual must not be presented as having a newly defined pipeline target. Explain this in the report builder; do not invent or split targets.
8. Return compatible report tables/series and source/currency metadata for Analytics. Enable only meaningful chart/group/drill combinations for each template. Forecast drill-down uses the corresponding authorized Forecast detail query rather than the generic record-report dimension cycle.
9. Add a supported definition format version for Forecast settings, while retaining explicit import support for existing ordinary-report JSON version 1.0. Use additive migrations only if storage/constraint changes require them; the current specification is already JSON.

Sources: [Forecast summary handler](../../../crusource-crm-backend/src/modules/forecast/handlers/get_forecast_summary_handler.py), [Forecast deal handler](../../../crusource-crm-backend/src/modules/forecast/handlers/get_forecast_deals_handler.py), [Forecast domain service](../../../crusource-crm-backend/src/modules/forecast/services/forecast_service.py), [Forecast scope](../../../crusource-crm-backend/src/modules/forecast/services/forecast_scope.py), and [Forecast result contracts](../../../crusource-crm-backend/src/modules/forecast/queries/forecast_queries.py).

**Acceptance:** a Forecast report matches the Forecast screen for the same period, pipeline, currency and authorized scope. Stage probability/target/deal changes update live results. Users cannot infer other organizations' or unauthorized users' targets. Export/import, report names and optional widget titles work for Forecast reports as well.

## Architecture and validation

Keep pages thin, builder controls focused, service contracts typed, TanStack Query responsible for server state, URL hooks responsible for library view state, and Redux responsible for modal/selection state. One specification compiler/validator and one set of Forecast calculations should serve the affected flows. Routes validate/authorize/delegate; query/command handlers coordinate use cases; repositories construct database queries.

Write behavioral regressions before each implementation batch:

- Builder scope persistence, editing legacy/advanced filters, preview/save equivalence, supported modules and deleted/inaccessible pipelines.
- Real report-backed chart requests, comparator independence, currency formatting, drill-down `eq`, retained criteria, report edits and stale-response races.
- Export icon/accessibility, safe literal search highlighting, unchanged row layout, all-filter empty states, saved-view round-trip/default/errors/permissions and navigation history.
- HTTP definition import/export round-trip, selection across pagination, failed export behavior, version validation, duplicate/conflicting names, destination mappings, batch rollback, limits and permission enforcement.
- Forecast parity, period boundaries, terminal-stage probabilities, mixed currencies, null/zero targets, correct weighted/percentage aggregation and current user/team scope.
- Native widget compatibility after removing the board toolbar.

Run each affected repository's full applicable CI after implementation, including frontend browser/type/build/audit checks and backend PostgreSQL migration/locking/drift checks if schema work is introduced. Focused tests used for this plan are not a full implementation CI pass. Use disposable fixtures; do not import test definitions into customer organizations or change staging targets to prove behavior.

## Delivery and completion

Deliver Phase 1 first because it establishes report-owned data scope and fixes the confirmed Analytics defect. Phase 2 improves everyday report discovery. Phase 3 completes portable definitions. Phase 4 adds Forecast once save/run/import contracts are consistent.

Done means every testing-list item has a verified user-facing flow, saved criteria survive preview/save/edit/run/export/import, Forecast reports agree with existing Forecast calculations, Analytics has no board-wide selectors or compulsory scope badges, native widgets retain valid behavior, and required CI checks pass. Implementation evidence and deployment status are recorded in the linked implementation report.
