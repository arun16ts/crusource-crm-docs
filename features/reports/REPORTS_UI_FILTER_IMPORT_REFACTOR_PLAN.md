# Reports Module Refactor Implementation Plan (Saved Views, Table Export, Import UI & Right-Side Filters)

**Date:** 18 November 2026  
**Status:** Proposed & Verified Against Codebase  
**Target Repositories:** `crusource-crm-frontend`, `crusource-crm-backend`, `crusource-crm-docs`  
**Owner Area:** Reports & Query Library (`/dashboard/reports`)

---

## 1. Executive Summary & Verified Problems

A full audit of the CRM Reports module (`ReportsHome`, `ReportsSavedViews`, `ReportsTable`, `ImportReportsModal`, `ReportsFilterPanel`, `useReportLibraryState`, `reportsSlice`, and backend `src/modules/reports`) confirmed four structural UI/UX and functional defects:

1. **Inconsistent Saved Views UI (`ReportsSavedViews.tsx`):**
   - Currently renders a raw HTML `<details>`/`<summary>` toggle with unstyled `<select>`, `<input>`, plain text `<button>` controls, and `useAppDialogs()`.
   - Every other core CRM module (Leads, Calls, Meetings, Tasks, TeamSpace Pool) uses [`SavedViewsDropdown`](../crusource-crm-frontend/src/components/shared/SavedViewsDropdown.tsx) with `@radix`/`DropdownMenu`, a styled Save View modal, and `ConfirmModal`.

2. **Duplicate Export Button in Table Selection Bar (`ReportsTable.tsx` vs `ReportsHome.tsx`):**
   - `ReportsHome.tsx` already provides a global header **Export** button that dynamically displays `Export` or `Export (N)` when rows are selected and opens `ExportReportsModal` (supporting both selected IDs and filtered query export).
   - `ReportsTable.tsx` renders a redundant **Export Selected** button (`onExportSelected`) inside the table selection command bar, creating duplicate export controls in the same view.

3. **Outdated, Inconsistent Import UI (`ImportReportsModal.tsx` & `ImportReferenceMappings.tsx`):**
   - `ImportReportsModal.tsx` uses a bare native HTML `<dialog>`, raw browser `<input type="file">`, unstyled native selects/inputs, no drag-and-drop dropzone, no sample JSON template download, and no multi-step visual progression.
   - Other modules follow the unified Bulk Import dialog architecture (`GenericBulkImportModal` + `BulkImportUploadStep` + `BulkImportValidationStep` + `BulkImportResultStep`) with branded headers, drag-drop upload cards, validation count cards, and styled conflict/mapping workflows.

4. **Legacy, Broken & Misaligned Filters (`ReportsFilterPanel.tsx`, `useReportLibraryState.ts`, `ReportTableHeader.tsx`, Backend `ListSavedReportsQuery`):**
   - **Old Popover UI:** `ReportsFilterPanel.tsx` uses an old `absolute top-full` floating popover instead of the unified right-side [`FilterDrawer`](../crusource-crm-frontend/src/components/shared/filters/FilterDrawer.tsx) (`FilterSection`, `PillMultiSelect`, `FilterSelect`, `DateRangePresetFilter`, `FilterSortControl`).
   - **Dead `visibility` Filter:** `VISIBILITIES` (`private`, `team`, `org`) is declared in `ReportsFilterPanel.tsx` (lines 56–61) but **never rendered** in JSX, and `useReportLibraryState.ts` hardcodes `visibilityFilter: null` and actively deletes `"visibility"` from the URL (line 111) — even though backend `ListSavedReportsQuery.visibility` and `reports_repository.py` support it.
   - **Incomplete `owner_scope`:** `ReportsFilterPanel.tsx` only exposes `all` and `mine`, omitting `shared` ("Shared with Me") and `org` ("Organization Wide"), even though both backend (`reports_repository.py`) and `ReportsActiveFilterChips.tsx` implement them.
   - **Date Serialization Bug:** `ReportsFilterPanel.tsx` converts `<input type="date">` values via `new Date(...).toISOString()` while `useReportLibraryState.ts` (`calendarDate`) strictly validates `YYYY-MM-DD`, causing date filters to break across URL reloads and Saved Views.
   - **Legacy Entity Exclusions:** `ReportsHome.tsx` (lines 169–171) still checks `selectedEntityType !== "activities" && selectedEntityType !== "matrix_summary"`, while `ReportsKpiDeck.tsx` shows 7 modules + All (omitting `forecast` even though `forecast` is a valid `EntityType` in `ReportsService`, `ReportsFilterPanel`, and backend).
   - **Missing Useful Report Library Filters & Broken Sort Headers:** No filters exist for **Report Origin** (`is_default` system default vs custom), **Created Date**, multi-select **Modules / Report Types / Visibilities**, or **Creator**; and clicking `Report Type`, `Config`, `Created By`, or `Status` column headers in `ReportTableHeader.tsx` sends `sort_field` values that `reports_repository.py` (lines 179–188) ignores and silently falls back to `updated_at`.

---

## 2. Architecture & Design Plan

### 2.1 Phase 1 — Backend Filter, Multi-Select & Sort Alignment (`crusource-crm-backend`)

Ensure the backend `/api/v1/reports` paged listing and `/export-definitions` endpoints remain 100% backward-compatible for existing callers (`AddWidgetModal`, `useGlobalSearchQueries`, `export_report_definitions_handler`, `list_reports_handler`) while supporting richer, accurate filtering and sorting.

#### Target Files
- `src/modules/reports/queries/report_queries.py` (`ListSavedReportsQuery`)
- `src/modules/reports/queries/library_criteria.py` (`report_library_criteria`)
- `src/modules/reports/repositories/reports_repository.py` (`get_saved_reports_paged_for_scope`)
- `src/modules/reports/services/saved_spec.py` (audit compatibility only)

#### Changes
1. **Extend `ListSavedReportsQuery` (Backward-Compatible):**
   - Keep existing single-value fields: `entity_type`, `report_type`, `owner_scope`, `visibility`, `updated_from`, `updated_to`, `q`, `search_scope`, `limit`, `offset`, `sort_field`, `sort_direction`.
   - Add multi-value and report-metadata fields:
     - `entity_types: Optional[List[str]] = None` (accepts repeated query params or comma-separated string in `report_library_criteria`)
     - `report_types: Optional[List[str]] = None`
     - `visibilities: Optional[List[str]] = None`
     - `is_default: Optional[bool] = None` (filter System Default vs Custom reports)
     - `created_from: Optional[datetime] = None`
     - `created_to: Optional[datetime] = None` (with `inclusive_end_day` validator matching `updated_to` and date-order validation)
     - `assigned_to_me: Optional[bool] = None` (filters `SavedReport.assigned_to_user_id == scope.user_id`)
2. **Update `report_library_criteria` (`library_criteria.py`):**
   - Parse both single query values (`request.query_params.get`) and repeated/list query params (`request.query_params.getlist`) for `entity_types`, `report_types`, and `visibilities` (supporting comma-separated fallback `a,b` as well).
3. **Update `reports_repository.get_saved_reports_paged_for_scope`:**
   - Apply `SavedReport.entity_type.in_(params.entity_types)` when `entity_types` is non-empty (falling back to `params.entity_type`).
   - Apply `cast(SavedReport.spec["report_type"].astext, String).in_(params.report_types)` when `report_types` is non-empty (falling back to `params.report_type`).
   - Apply `SavedReport.visibility.in_(params.visibilities)` when `visibilities` is non-empty (falling back to `params.visibility`).
   - Apply `SavedReport.is_default.is_(params.is_default)` when `is_default is not None`.
   - Apply `SavedReport.assigned_to_user_id == scope.user_id` when `assigned_to_me is True`.
   - Apply `SavedReport.created_at >= params.created_from` and `SavedReport.created_at <= params.created_to`.
   - Extend `search_scope` (`all` and `creator_name`) to match creator `User.name` via outer join when searching.
   - **Fix Sorting & PostgreSQL `COALESCE` Type-Mismatch Bug:**
     - **Verified Bug in `reports_repository.py` lines 179–193:** Currently `order_by(direction_fn(func.coalesce(sort_col, SavedReport.created_at)))` wraps every `sort_col` (including `varchar` columns like `SavedReport.name`, `SavedReport.entity_type`, and `SavedReport.visibility`) in `COALESCE(..., SavedReport.created_at)`. On PostgreSQL, coalescing `varchar` with `timestamptz` raises a type mismatch error.
     - Only `updated_at` should coalesce with `SavedReport.created_at`; all string columns (`name`, `entity_type`, `report_type`, `visibility`, `created_by`) must sort directly via `direction_fn(func.lower(func.coalesce(sort_col, "")))` (or nullable direct column order):
       - `name` -> `func.lower(SavedReport.name)`
       - `entity_type` -> `func.lower(SavedReport.entity_type)`
       - `report_type` -> `func.lower(func.coalesce(cast(SavedReport.spec["report_type"].astext, String), ""))`
       - `created_by` -> `func.lower(func.coalesce(User.name, ""))` (1:1 outerjoin on `SavedReport.user_id == User.id`, counting via `func.count(SavedReport.id)`)
       - `visibility` -> `func.lower(SavedReport.visibility)`
       - `created_at` -> `SavedReport.created_at`
       - `updated_at` -> `func.coalesce(SavedReport.updated_at, SavedReport.created_at)`

---

### 2.2 Phase 2 — Remove Duplicate Table Export & Clean Header Toolbar (`ReportsTable.tsx` & `ReportsHome.tsx`)

#### Target Files
- `src/components/reports/table/ReportsTable.tsx`
- `src/components/reports/ReportsHome.tsx`

#### Changes
1. **Remove Duplicate Table Export:**
   - Remove `onExportSelected` prop and the `<Download />` **Export Selected** button block (`lines 138–148`) from `ReportsTable.tsx` selection command bar.
   - Keep `Delete Selected` and `Deselect All` (`Clear Selection`) in the selection bar.
   - Remove `onExportSelected={...}` from `<ReportsTable>` in `ReportsHome.tsx`.
2. **Preserve Single Global Export Entry Point:**
   - Header **Export** button in `ReportsHome.tsx` (desktop + mobile overflow menu) continues opening `ExportReportsModal`, which automatically shows `"Export Selected (N)"` when `selectedReportIds.length > 0` or `"All matching accessible reports"` when nothing is selected.

---

### 2.3 Phase 3 — Saved Views UI Refactor (`ReportsSavedViews.tsx`)

#### Target Files
- `src/components/reports/ReportsSavedViews.tsx`
- `src/components/shared/SavedViewsDropdown.tsx` (verify/preserve compatibility without breaking Leads/Calls/Meetings/Tasks/TeamSpace)

#### Changes
1. **Adopt `SavedViewsDropdown` Chrome & Behavior:**
   - Refactor `ReportsSavedViews.tsx` to wrap [`SavedViewsDropdown`](../crusource-crm-frontend/src/components/shared/SavedViewsDropdown.tsx) (`entityType="reports"`) instead of the custom `<details>`/`<summary>` HTML block and `useAppDialogs()`.
   - Keep two Reports-specific features intact inside the wrapper:
     - **Permission gating:** `if (!usePermission("saved_views", "view")) return null;` (note: verify `SavedViewsDropdown` also handles `canCreate`/`canDelete` gracefully or passes them cleanly).
     - **Auto-apply default view on mount:** Preserve the `useEffect` in `ReportsSavedViews.tsx` that applies `savedViews.find(v => v.is_default)` once when `!window.location.search`.
     - **Serialized Filter State:** Pass `currentFilters` derived from `stripReportPagination(libraryState)` (excluding `page` and `pageSize`) and apply saved views via `applyView(savedFilters)`.
   - Ensure `SavedViewsDropdown` accepts optional `canCreate` / `canDelete` props (defaulting to `true` so all existing callers stay unchanged) so Reports RBAC (`saved_views: create/delete`) is respected.
2. **Localization:**
   - Use `common.controls` (`savedViews`, `yourViews`, `noSavedViews`, `saveCurrentFilters`, `saveView`, `viewName`, `makeThisMyDefaultView`, `deleteSavedView`) consistent with Leads, Calls, Meetings, and Tasks.

---

### 2.4 Phase 4 — Import Reports UI Complete Refactor (`ImportReportsModal.tsx` & `ImportReferenceMappings.tsx`)

#### Target Files
- `src/components/reports/modal/ImportReportsModal.tsx`
- `src/components/reports/modal/ImportReferenceMappings.tsx`
- (Cleanup) Remove unused legacy files if unreferenced: `src/components/reports/modal/ImportExportReportsModal.tsx`, `src/components/reports/table/ReportsFilterBar.tsx`

#### Changes
Transform `ImportReportsModal.tsx` from a raw `<dialog>` into a 3-step CRM-standard modal matching the design language of `GenericBulkImportModal`, `BulkImportUploadStep`, `BulkImportValidationStep`, and `BulkImportResultStep`:

1. **Modal Shell & Header:**
   - Styled overlay (`fixed inset-0 z-50 bg-black/50 backdrop-blur-xs p-4`) and card container (`bg-white rounded-2xl shadow-2xl border border-outline w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden`).
   - Header with branded `UploadCloud` icon badge (`bg-primary/10 text-primary`), title (`Import Report Definitions`), subtitle, and 3-step progress pill indicator (`1. Upload JSON` → `2. Validate & Map` → `3. Summary`).
2. **Step 1 — Upload & Sample Template:**
   - **Sample Definition Template Banner** (matching `BulkImportUploadStep` orange-tinted banner): explains JSON format exported from **Export Definitions** and includes a **Download Sample JSON** button generating a valid minimal CRM report definition envelope (`version: "2.0"`).
   - **Drag-and-Drop Dropzone:** Dashed border upload zone (`UploadCloud`, click-to-browse + drag/drop support for `.json` files up to 5 MiB).
   - Preserves client-side envelope validation (`version` `"1.0"`/`"2.0"`, 1–100 reports, forecast v2.0 rule) and displays a styled inline error banner (`AlertCircle`) on invalid files or CSV/XLSX attempts.
3. **Step 2 — Validation Preview, Conflict Resolution & Reference Mapping:**
   - **3 Summary Metric Cards:** `Ready` (emerald), `Name Conflicts` (amber), `Invalid` (rose) — matching `BulkImportValidationStep.tsx`.
   - **Per-Definition Review List:** Styled cards showing report name, `entity_type` badge, status badge (`Valid`, `Conflict`, `Invalid`), and detailed reason.
     - Inline **Report Name** input (styled CRM input) when `status === "conflict"` or `"invalid"`.
     - **Refactored `ImportReferenceMappings.tsx`:** Styled `grid` rows with CRM `<select>` controls (`border border-outline rounded-lg px-3 py-2 text-xs bg-white focus:border-primary`) for destination `owner`, `pipeline`, `stage`, `team`, and `user`.
     - **Skip button** (`Trash2` / `Skip`) to exclude individual invalid definitions and automatically re-validate remaining items.
   - **Duplicate Name Strategy Selector & Re-validate Bar:** Clean segmented/select control (`Create with a new name`, `Skip duplicates`, `Cancel if duplicate exists`) and a `"Re-validate Changes"` button when `dirty === true`.
4. **Step 3 — Import Result Summary:**
   - Success card (`CheckCircle2`) displaying `Imported count` and `Skipped count`, plus `"Done"` button closing the modal and refreshing `["reports"]` and `["reports", "counts"]`.
5. **Accessibility & Test Hooks:**
   - Keep `aria-labelledby="import-reports-title"`, `aria-label="Report definition file"`, `aria-label="Duplicate name handling"`, `aria-label="Close import"`, `"Confirm import"` button label, and `role="alert"` / `role="status"` semantics so screen readers and Playwright checks work reliably.

---

### 2.5 Phase 5 — Right-Side Reports Filter Drawer & State Refactor

#### Target Files
- `src/components/reports/filter/ReportsFilterPanel.tsx`
- `src/hooks/useReportLibraryState.ts`
- `src/store/slices/reportsSlice.ts`
- `src/components/reports/table/ReportsActiveFilterChips.tsx`
- `src/components/reports/table/ReportTableHeader.tsx`
- `src/components/reports/kpi/ReportsKpiDeck.tsx`
- `src/components/reports/ReportsHome.tsx`
- `src/services/reports.service.ts`
- `src/messages/{en,ar,nl}/reports.json` (plus `tests/test_reports_product_browser.mjs` locale message loading / `src/i18n/locales/en.json` parity if referenced by browser fixtures)

#### Changes
1. **Replace Floating Popover with Shared Right-Side `FilterDrawer`:**
   - Refactor `ReportsFilterPanel.tsx` to use [`FilterDrawer`](../crusource-crm-frontend/src/components/shared/filters/FilterDrawer.tsx) (`searchableFields={true}`, draft state cloned on open, live `draftChips`, `Clear All` keeping drawer open, `Apply` committing filters and closing, `Escape` / `Ctrl+Enter` support).
   - Organize controls into 4 collapsible [`FilterSection`](../crusource-crm-frontend/src/components/shared/filters/FilterSection.tsx) groups matching actual `SavedReport` data:
     - **Module & Format:**
       - **Target Module** (`PillMultiSelect`): `leads`, `deals`, `contacts`, `accounts`, `tasks`, `calls`, `meetings`, `forecast` (synced bidirectionally with `ReportsKpiDeck` single-click shortcut!).
       - **Report Structure** (`PillMultiSelect`): `tabular`, `summary`, `matrix`.
       - **Report Origin** (`FilterSelect`): `all`, `custom` (`is_default: false`), `system` (`is_default: true`).
     - **Ownership & Visibility:**
       - **Ownership Scope** (`FilterSelect`): `all`, `mine` (Created by Me), `shared` (Shared with Me), `org` (Organization Wide).
       - **Visibility** (`PillMultiSelect`): `private`, `team`, `org`.
       - **Assignment** (`checkbox`/toggle): `Assigned to Me` (`assigned_to_me: true`).
     - **Dates:**
       - **Last Updated** (`DateRangePresetFilter`): `YYYY-MM-DD` presets (`today`, `last_7_days`, `last_30_days`, `this_month`, `this_quarter`) + custom From/To inputs.
       - **Created Date** (`DateRangePresetFilter`): `YYYY-MM-DD` presets + custom From/To inputs.
     - **Sort Order:**
       - **Sort By** (`FilterSortControl`): `updated_at`, `created_at`, `name`, `entity_type`, `report_type`, `visibility`, `created_by` + Ascending/Descending toggle.
2. **Unify URL, Redux & KPI State (`useReportLibraryState.ts`, `reportsSlice.ts`, `ReportsKpiDeck.tsx`, `ReportsHome.tsx`):**
   - Support multi-select arrays (`entityTypes`, `reportTypes`, `visibilities`) alongside URL params (`modules`, `types`, `visibilities`, `origin`, `assigned_to_me`, `created_from`, `created_to`, `from`, `to`, `owner`, `sort`, `order`, `q`), keeping legacy single param reads (`module`, `type`, `visibility`) backward-compatible for old bookmarks/links.
   - Fix `YYYY-MM-DD` date handling (eliminate `new Date(...).toISOString()` mismatch in `ReportsFilterPanel`).
   - Add `forecast` card (or sync `selectedEntityTypes.length === 1` highlight) in `ReportsKpiDeck.tsx` and remove legacy `"activities"` / `"matrix_summary"` exclusions in `ReportsHome.tsx`.
   - Update `ReportsActiveFilterChips.tsx` to display removable chips for every active filter (including `visibility`, `is_default`, `assigned_to_me`, `created_from/to`, multi-selected modules/types, and `sort`).
   - Align `ReportTableHeader.tsx` sortable columns strictly to backend-supported sort fields (`name`, `entity_type`, `report_type`, `created_by`, `updated_at` — removing silent non-sorting `config` / `status` triggers or marking them non-sortable).
3. **Remove Dead/Redundant Files:**
   - Remove unused `src/components/reports/table/ReportsFilterBar.tsx` (and its export from `table/index.ts`) and deprecated `src/components/reports/modal/ImportExportReportsModal.tsx` after confirming zero imports.

---

## 3. Dependency & Impact Matrix

| Dependent Module / File | How It Relies on Reports | Compatibility Action / Guard |
| --- | --- | --- |
| `components/analytics/AddWidgetModal.tsx` | Calls `ReportsService.listReports({ q, search_scope: "name", limit: 100, offset })` | Keep existing `ListSavedReportsQuery` scalar parameters (`q`, `search_scope`, `limit`, `offset`) 100% unchanged. |
| `hooks/useGlobalSearchQueries.ts` | Calls `ReportsService.listReports({ limit: 100 })` | Unchanged default query contract returns same `PaginatedSavedReportsResponse`. |
| `handlers/export_report_definitions_handler.py` | Accepts `query: Optional[ListSavedReportsQuery]` and calls `get_saved_reports_paged_for_scope` | Works seamlessly with extended `ListSavedReportsQuery`; update `ExportReportsModal` `queryParams` so exporting filtered results respects new filters (`entity_types`, `visibilities`, `is_default`, etc.). |
| `modules/saved_views` (`SavedViewsService`, `useSavedViews.ts`) | Stores arbitrary JSON `filters` under `entity_type="reports"` | Preserve `stripReportPagination` when saving; support both legacy saved view keys (`selectedEntityType`, `reportTypeFilter`) and new array keys (`entityTypes`, `reportTypes`, `visibilities`, `isDefault`, etc.) inside `applyView`. |
| `modules/reports/handlers/report_routes.py` (`GET /api/v1/reports`) | Uses `Depends(report_library_criteria)` when `paged=true` | Update `report_library_criteria` to handle both single and multi-value query params (`getlist` + comma split). |
| `components/reports/ReportRunModal.tsx` & `ReportBuilder.tsx` | Uses `runReport` / `exportReportFullData` (CSV/XLSX) and `updateReport`/`createReport` | Untouched; separate from report library Saved Views / JSON Definition Import / Definition Export. |
| `tests/test_reports_product_browser.mjs` & `tests/test_reports_product_contracts.tsx` | Tests `ReportsHome` Saved Views DOM, Import Reports flow, Export Definitions flow | Update Playwright/fixture selectors in `test_reports_product_browser.mjs` for `SavedViewsDropdown`, refactored `ImportReportsModal`, right-side `FilterDrawer`, and single Export button; expand coverage for all new filters & sorting. |

---

## 4. Verification Plan

1. **Backend (`crusource-crm-backend`):**
   - Add pytest cases covering `entity_types`, `report_types`, `visibilities`, `is_default`, `assigned_to_me`, `created_from/to`, `updated_from/to`, creator search, and sorting by `report_type`, `created_by`, `visibility`, `entity_type`, `name` — plus `export-definitions` with filtered `query`.
   - Run `pytest` on `tests/test_reports.py`, `tests/test_reports_remediation.py`, `tests/test_reports_audit_fixes.py`, `tests/test_reports_product_scope.py`, and `tests/test_filter_contract.py`.
2. **Frontend (`crusource-crm-frontend`):**
   - Run `npx tsc --noEmit`, ESLint on all touched Reports & shared files, and `npm run test:localization` (`test_translation_contracts.ts` across `en`, `ar`, `nl`).
   - Run `npm run test:reports` and `npm run test:reports:browser` (updated Playwright suite verifying Saved Views dropdown, single Export flow, 3-step Import UI with conflict + reference mapping, right-side `FilterDrawer` draft/apply/clear-all/chips/sorting, KPI card sync, and URL reload persistence).
