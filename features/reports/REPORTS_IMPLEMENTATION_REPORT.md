# Reports and Analytics implementation

**Date:** 14 October 2026

**Scope:** CRM frontend/backend. No VMS application changes.

**Status:** Implemented locally and verified. Nothing deployed or pushed.

## What users can do

- Choose a compatible pipeline and currency when creating/editing a report. Accounts revenue reports also support currency. Advanced saved criteria remain intact; the guided selectors explain when advanced criteria own the selection.
- Preview, save, reopen and run the same report criteria against live records. Money aggregates require one currency or grouping by currency. Amounts are never converted.
- Name reports and widgets independently. Analytics no longer has board-wide pipeline/currency selectors. Report-backed widgets use their saved reports, including stage breakdowns; native funnel/cohort widgets have their own pipeline configuration.
- Drill into an Analytics group while retaining the saved scope. Editing the report clears old drill results and invalidates its run cache. Monetary chart/table formatting follows result currency, including custom widget titles. Legacy missing/mixed currency codes carry a warning; counts can span currencies. Missing target values remain unavailable instead of becoming zero.
- Search report names with subtle, literal text highlighting; use the standard filter control without unavailable sharing filters.
- Bookmark report-library filters, sorting and pagination through URL state. Save, apply, update or delete personal library views and choose a default. Views never alter report definitions. Explicit URL criteria take precedence over a default view.
- Export selected definitions across pages or all definitions matching the current library filters. Failed exports produce an error and no fallback file.
- Import exported definitions as JSON, inspect validation results, rename duplicates, map unavailable pipeline/stage/Forecast user/team references, explicitly skip invalid items and validate changes before confirming. Imported reports receive new IDs and are private.
- Build Forecast summary/detail reports for a saved month or quarter, currency, pipeline and permitted team/user. Results reuse the existing Forecast calculations and remain live. Missing targets remain missing; percentages cannot be summed or averaged. Pipeline filtering does not redefine the user/period target.

## Limits and access

Definition imports accept one JSON file, at most **5 MiB** and **100 reports**. Ordinary definitions use version **1.0**; Forecast definitions use **2.0**. CSV/XLSX exports contain results and cannot recreate report definitions. Definition export is also limited to 100 items; narrow the library filters or select fewer reports.

Specifications allow at most 100 columns/filters, 10 grouping/sort fields, 20 aggregates and 100 values per filter. Filter text is bounded. Preview identifies schema-invalid items; confirmed execution validates the complete batch and rolls back on failure. Admission permits 30 import/validation requests per minute per authenticated organization/user/client IP and fails closed in production if the shared limiter is unavailable.

Names are case-insensitive within the creator and module. Create, rename and import serialize writes on the owner row in PostgreSQL. Another user's private report names are not used to disclose naming conflicts.

Reports import requires explicit import and create capabilities, and confirmed writes use the existing active-subscription guard. It does not use the approval-submission permission fallback retained by other modules. Definition/data exports require export. Existing organization/record scope remains in force. Forecast execution additionally requires Forecast view access and resolves current team/user access each time. Saved views respect their own view/create/edit/delete capabilities.

Legacy source/specification mismatches produce an actionable error during run/definition export. Monetary CSV/XLSX column and matrix headers identify the known, mixed or unspecified unit. Matrix headers and XLSX text cells escape spreadsheet formula prefixes, including user-entered names.

### Changed REST boundaries

All paths below are under `/api/v1/reports`, authenticated through the existing CRM session/scope guards. Definitions contain names and query criteria; results can contain CRM records, personal data and financial/target amounts. No public access or cross-product endpoint was added.

| Operation | Access and behavior |
| --- | --- |
| `GET /summary-counts` | Reports view; existing organization/report access filter; no first-500 cap. |
| `POST /import-definitions/validate` | Explicit Reports import + create; bounded/rate-limited read; item-level schema/reference errors. |
| `POST /import-definitions` | Explicit Reports import + create and active subscription; same admission limits; atomic private writes. |
| `POST /export-definitions` | Reports export; selected accessible IDs or current scoped library criteria; errors do not become partial files. |
| `POST /{id}/export-data` | Reports export and existing applicable source/action checks; Forecast additionally requires its read scope. |
| Existing create/edit/run routes | Typed source consistency, saved reference validation, current record scope and monetary result context. |

## Implementation evidence

- [Shared specification compiler](../../../crusource-crm-frontend/src/lib/reports/reportScope.ts), [guided scope controls](../../../crusource-crm-frontend/src/components/reports/builder/ReportScopeControls.tsx), and [builder](../../../crusource-crm-frontend/src/components/reports/ReportBuilder.tsx).
- [Library URL state](../../../crusource-crm-frontend/src/hooks/useReportLibraryState.ts), [saved-view flow](../../../crusource-crm-frontend/src/components/reports/ReportsSavedViews.tsx), and [import flow](../../../crusource-crm-frontend/src/components/reports/modal/ImportReportsModal.tsx).
- [Analytics board](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx), [widget execution/drill-down](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx), and [monetary result mapping](../../../crusource-crm-frontend/src/lib/reportToChartData.ts).
- [HTTP routes](../../../crusource-crm-backend/src/modules/reports/routes/report_routes.py), [scope validation](../../../crusource-crm-backend/src/modules/reports/services/report_scope.py), [definition import handlers](../../../crusource-crm-backend/src/modules/reports/handlers/import_report_definitions_handler.py), and [Forecast adapter](../../../crusource-crm-backend/src/modules/reports/services/forecast_report_source.py).
- [Backend product regressions](../../../crusource-crm-backend/tests/test_reports_product_scope.py), [PostgreSQL naming race](../../../crusource-crm-backend/tests/test_reports_postgres.py), [frontend contracts](../../../crusource-crm-frontend/tests/test_reports_product_contracts.tsx), and [browser flow](../../../crusource-crm-frontend/tests/test_reports_product_browser.mjs). Both CI workflows register the new regressions.

## Validation and deployment

Validation used the CRM workflow commands, Node 20.20.2 and the backend Python 3.12 venv. All frontend checks ran in an isolated checkout with a successful clean `npm ci`; the running application's dependencies were preserved.

| Verification | Result |
| --- | --- |
| Frontend workflow parity | 42 checks passed: changed-file formatting, full lint, tests, spreadsheet/Reports/AI contracts, TypeScript, all registered CI browser regressions, production build and configured dependency audit. |
| Full backend suite | 2,088 passed; 73 opt-in/environment-specific tests skipped in this general run. Required integration groups were exercised separately below. |
| Backend static checks | Ruff and compilation passed. |
| PostgreSQL/Redis integration | Reports naming race 1 passed; shared quotas/security 49; production transactions 59; recovery/import locking 10; platform 45. All used isolated local test services/schemas. |
| Migrations | Committed upgrade passed; empty-database migration drift 1 passed; encryption migration/rollback 1 passed; final `alembic check` passed. No application schema migration was added for Reports JSON settings. |
| Dependency audits | Backend pinned-runtime audit found no known vulnerabilities. Frontend audit found no high/critical runtime advisories; its existing temporary ESLint advisory exception remains, expiring 4 November 2026. |
| Graphify | Workspace code graph refreshed; existing CRM and VMS roots retained. Five pre-existing partial TSX extraction warnings remain; TypeScript/build checks passed. |
| Documentation/conflicts | Local links checked; no missing references or unmerged entries in the affected repositories; `git diff --check` passed. |

The backend emits existing deprecation warnings; frontend lint also contains existing warnings. These passing checks do not claim a warning-free repository. A frontend audit attempt failed to fetch registry advisory data and passed on retry. Earlier test runs exposed obsolete invalid-spec fixtures and a validation harness that reused an already-populated migration fixture; those were corrected before the final passing run.

Detailed local logs are under `validation/reports-implementation/` in the orchestration workspace, including `backend-ci/full-tests-currency.log`, integration logs, `frontend-ci/results.json`, `frontend-ci/audit.log` and `backend-ci/audit-network.log`. This directory is excluded from Graphify. Disposable test services were removed after validation.

This task did not issue a commit, push, merge, deployment, staging account mutation or production database operation. During the work the application repositories acquired commits `063e8c3c` (frontend) and `3ef484a` (backend); no reset or alteration of that Git history was performed. All 1,598 tracked frontend files match the tested CI snapshot after normalizing line endings. Local fixture/browser checks do not establish staging behavior. A deployment request still requires the workspace's complete deployment audit.
