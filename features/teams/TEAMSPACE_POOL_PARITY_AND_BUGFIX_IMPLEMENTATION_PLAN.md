# Teams Pool UI Parity, Feature Alignment & Bug-Fix Implementation Plan

- **Date:** 2026-11-26
- **Product / Repositories:** Crusource CRM (`crusource-crm-frontend`, `crusource-crm-backend`, `crusource-crm-docs`)
- **Status:** `DRAFT IMPLEMENTATION PLAN (NOT YET IMPLEMENTED)`
- **Deployment Status:** `NOT DEPLOYED`
- **Supersedes:** Historical baseline [team_pool_upgrade_plan.md](team_pool_upgrade_plan.md)

---

## 1. Executive Summary & User-Reported Issues Traceability

This document is the source-backed audit and phased implementation plan to bring the **Teams Pool** (`/dashboard/teamspace` and `/dashboard/teamspace/pool`) into full UI, UX, filter, view, export, bulk import, and backend query parity with the individual/private CRM modules (**Leads, Accounts, Contacts, Deals, Tasks, Meetings, Calls**), while preserving TeamSpace governance, permissions, team scoping, and ownership workflows.

### User-Reported Issues Traceability Matrix

| # | User-Reported Issue | Verified Root Cause in Current Code | Target Fix Phase |
|---|---|---|---|
| 1 | **Tab count badges show `0` until clicked**, then update after entering the tab; no real use case | [TeamsPoolSection.tsx:638-694](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L638-L694) only enables the query for `activeTab`; [PoolTabBar.tsx:19-87](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolTabBar.tsx#L19-L87) renders `counts` pills defaulting to `0` (`TeamsPoolSection.tsx:1416-1424`). | **Phase 1** (Remove count badges completely from `PoolTabBar`) |
| 2 | **Pipeline & Currency selectors are floating outside the table card**, separated from the table by Quick Filters (and duplicated in Deals Kanban) | [TeamsPoolSection.tsx:1427-1465](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1427-L1465) renders Pipeline & Currency above `PoolQuickFilters` outside the card; [PoolDealsKanban.tsx:572-599](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx#L572-L599) renders a second Pipeline selector inside Kanban. Private `LeadBoard.tsx:373-404` and `deals/page.tsx:846-893` place Pipeline/Currency inside the top strip of the white table card below `QuickFilterBar`. Also Deals forces a single currency (`includeAllOption={false}` at L1459). | **Phase 1 & Phase 3** |
| 3 | **TeamSpace uses an outdated filters section** instead of the latest Filters drawer, QuickFilterBar + active filter chips, and Saved Views | [PoolFilters.tsx:321-924](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx#L321-L924) uses a legacy `360px` absolute dropdown with native `<select>`s, no `FilterDrawer`, no `QuickFilterBar` active chips, no `activeFilterCount` badge ([TeamsPoolSection.tsx:1351](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1351)), and omits `SavedViewsDropdown` on Leads, Accounts, and Contacts ([TeamsPoolSection.tsx:1095-1114](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1095-L1114)). | **Phase 0 & Phase 2** |
| 4 | **Deals has a Grid view in Teams Pool that does not exist in Private Deals** | [poolSectionColumns.ts:83](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/poolSectionColumns.ts#L83) configures `deals: ["table", "grid", "kanban"]` and renders [PoolDealsGrid.tsx](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsGrid.tsx). Private `deals/page.tsx:154-156` only supports `list` and `kanban`. | **Phase 1** (Remove `PoolDealsGrid` & `"grid"` mode) |
| 5 | **View switcher is in the wrong place** (inside card bar instead of top toolbar next to Search) **and Leads lacks a Kanban view** | [PoolViewModeBar.tsx:14-52](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolViewModeBar.tsx#L14-L52) renders view buttons inside the card for Deals/Tasks/Meetings/Calls instead of passing `viewMode`/`onViewModeChange` to [EntityActionBar.tsx:157-188](../../../crusource-crm-frontend/src/components/shared/EntityActionBar.tsx#L157-L188). `POOL_VIEW_MODES` omits `leads` completely. | **Phase 1 & Phase 3** |
| 6 | **Export method differs and is broken** compared to individual sections | [TeamspaceExportDialog.tsx:19-336](../../../crusource-crm-frontend/src/components/teamspace/TeamspaceExportDialog.tsx#L19-L336) forces a 2-step flow, mandatory business reason even for admins/direct exports, raw `snake_case` checkboxes/CSV headers, broken Deals default columns (`stage`, `status`, `win_probability` → HTTP 422), missing BOM, client-side CSV→XLSX re-wrap, `teams_requests` 403 gate on direct downloads, and `admin_private` legacy `/teamspace/export/pool` 50-row truncation + Leads 500 + blank Calls columns. | **Phase 5** |
| 7 | **Bulk Import columns, values, templates, and UI are outdated/missing** compared to individual sections | [TeamspaceImportDialog.tsx:37-294](../../../crusource-crm-frontend/src/components/teamspace/TeamspaceImportDialog.tsx#L37-L294) replaces `BulkImportModal` (Leads) and `MeetingBulkImportModal` (Meetings) with `GenericBulkImportModal`, strips fields, uses minimal header-only samples (`tasks`, `calls`, `meetings`), treats Accounts & Contacts as activities (blocking unassigned import), crashes Meetings on `"other"` / blank `meeting_type` (HTTP 422), drops `skipped_count`/`failed_count`/`errors`, and fails batches all-or-nothing. | **Phase 6** |

---

## 2. Exhaustive Side-by-Side Parity Audit (Private vs. Current Teams Pool vs. Target)

### 2.1 Global Chrome & Shell Comparison

| UI / Feature Element | Private CRM Modules (Reference Standard) | Current Teams Pool (`TeamsPoolSection.tsx`) | Target Parity State |
|---|---|---|---|
| **Toolbar Container** | `EntityActionBar` (`LeadBoardActionBar` wraps `EntityActionBar`) | `EntityActionBar` (`TeamsPoolSection.tsx:1345-1410`) | `EntityActionBar` with full prop parity |
| **View Switcher Placement & Style** | Top toolbar **immediately left of Search** (`EntityActionBar.tsx:157-188`): Material icons (`format_list_bulleted`, `view_kanban`), `bg-slate-100 p-1 rounded-lg` | **Omitted from `EntityActionBar`**. Rendered inside table card via `PoolViewModeBar.tsx` with text labels (`Table`/`Grid`/`Kanban`) for Deals/Tasks/Meetings/Calls; **absent** on Leads | Pass `viewMode` (`"list" \| "kanban"`) & `onViewModeChange` to `EntityActionBar` for **Leads, Deals, Tasks, Meetings, Calls**; omit on Accounts & Contacts; **delete `PoolViewModeBar.tsx`** |
| **Team Scope & Refresh Controls** | N/A | Stuffed into `savedViewsToggle` slot (`TeamsPoolSection.tsx:1117-1169, 1364-1369`), which `EntityActionBar.tsx:202` hides on `<640px` (`hidden sm:flex`) | Render in a dedicated visible row/slot (e.g. `toolbarSecondaryActions` or dedicated Pool scope bar above/next to tabs) so mobile admins never lose team switching or refresh |
| **Saved Views** | `SavedViewsDropdown` on **all 7 modules** saving full filter object minus pagination | `PoolSectionSavedViews.tsx` rendered **only** for `deals`, `tasks`, `meetings`, `calls`; drops `pipeline_id`, `currency`, `lead_source`, `industry`; saves `search: ""`; debounced double-fetch on apply | Render `PoolSectionSavedViews` (`entityType="teamspace_pool_<tab>"`) on **all 7 tabs**, persisting the full module filter schema + atomic URL apply |
| **Filter Button Badge** | Passes both `isFilterActive` AND `activeFilterCount` → renders numeric pill (`EntityActionBar.tsx:229-232`) | Passes only `isFilterActive` (`TeamsPoolSection.tsx:1351`) → tiny dot only; `countActivePoolFilters` also counts outside-panel `selectedPipelineId` | Pass accurate `activeFilterCount` (panel + quick filters, excluding outside pipeline/currency controls) |
| **Filter Panel UX** | Portal slide-over `FilterDrawer` (`460px`): field search, collapsible `FilterSection`s, multi-select pills/search, numeric/date range pickers, draft chips, **Apply Filters** | Absolute `360px` popover (`PoolFilters.tsx:322-663`) with single native `<select>`s (except Lead status pills) | Slide-over `FilterDrawer` per module reusing private filter components + Pool `Owner / Unassigned` section |
| **Quick Filters & Active Chips** | `QuickFilterBar`: rounded-full quick view presets + removable **Active Filter Chips** strip + **Clear All** | `PoolQuickFilters`: compact `text-[11px]` chips only; `"Open Unassigned Pool"` wipes all other filters & forces Admin to `"all"`; **no active filter chips row** | Shared `QuickFilterBar` with module-matching presets + `Open Unassigned Pool` (non-destructive!) + removable Active Filter Chips + `Clear All` |
| **Module Tabs (`PoolTabBar`)** | None | 7 tabs (`Leads`, `Accounts`, `Contacts`, `Deals`, `Tasks`, `Meetings`, `Calls`) with count badges showing `0` until clicked | Keep 7 tabs; **remove count badges completely** from `PoolTabBar.tsx` |
| **Pipeline & Currency Strip** | **Inside top of white table/kanban card** (`border-b bg-slate-50/60`) | Floating **outside** the card above `PoolQuickFilters` (+ duplicate bar inside `PoolDealsKanban.tsx`) | Move inside the white card header (`border-b bg-slate-50/70`) for Leads & Deals; remove duplicate bar in `PoolDealsKanban.tsx`; add `"All Currencies"` support on Deals |
| **Add Button Label & Flow** | Direct modal (`Add Lead`, `Add Account`, `Add Contact`, `Add Deal`, `Create Task`, `Schedule Meeting` + `Log Meeting`, `Schedule Call` + `Log Call`) | `TeamspaceCreateDialog` (2-step: Assignee + mandatory Reason → modal). Deals button says `"Create Deal"`; Calls says `"Log Call"` but opens `"schedule"` mode | Align labels (`Add Deal`, `Schedule Meeting` / `Log Meeting`, `Schedule Call` / `Log Call`); make Business Reason conditional on `create_mode === "approval_required"` |
| **Error & Permission States** | `canView === false` access guard + `QueryErrorState` with Retry | **Missing** `canView` check & `error` UI — errors render empty state (`"No Team ... Found"`) | Add `canView` guard + `QueryErrorState` with Retry across all 7 tabs |

---

### 2.2 Per-Module Parity Matrix (All 7 Modules)

#### A. Leads (`LeadBoard.tsx` vs `PoolLeadsTab.tsx`)

| Area | Private Leads | Current Teams Pool Leads | Target Parity Changes |
|---|---|---|---|
| **Views** | `list` (Table) + `kanban` (`KanbanBoard.tsx`) | Table only (no Kanban) | Add `PoolLeadsKanban` powered by server kanban endpoints + top `EntityActionBar` toggle |
| **Pipeline Bar** | Inside card (`Standard Lead Pipeline (Default)` selected by default; Kanban locks to single pipeline) | Floating outside card (`All Pipelines` default); `usePipelines(..., includeStages=false)` | Inside card; default to org default pipeline (with `All Pipelines` option in List view); fetch stages (`includeStages=true`) |
| **Quick Filters** | `Qualified`, `Hot Leads (AI)`, `Created Last 7 Days`, `Include Converted` + Active Filter Chips | `⚡ Open Unassigned Pool` (wipes filters), `Qualified Leads`, `Fresh / Not Contacted` | Add `Hot Leads (AI)`, `Created Last 7 Days`, `Include Converted`, keep non-destructive `Open Unassigned Pool` + Active Filter Chips |
| **Filter Panel** | 16 controls (`stage_ids[]`, `statuses[]`, `include_converted`, `ai_priority_bands[]`, `score_min/max`, `ratings[]`, `lead_sources[]`, `industries[]`, `currencies[]`, `revenue_min/max`, `employees_min/max`, `countries[]`, `states[]`, `cities[]`, `created_from/to`, `updated_from/to`, `search_by`, `sort`+`dir`) | 5 single `<select>`s + status multi-pills (`owner_id/unassigned`, `status`, `lead_source` w/ phantom legacy labels, `industry`, `date_preset`) | Full `FilterPanel` parity + Pool `Owner / Unassigned` multi-select filter |
| **Table & Columns** | 31 columns in `leadBoardConfig.ts`; `OVERDUE` uses org `leadSlaHours`; no duplicate Owner column | Appends extra always-visible `owner` column even though `owner_name` is in `ALL_COLUMNS` → **2 owner columns** if `Lead Owner` toggled; omits `leadSlaHours`; `Stale: Xd` badge checks invalid `"lost"`/`"dead"`; page-local AI score sort only | Unify `owner_name` rendering via `PoolOwnerCell` (or suppress duplicate `owner_name` in picker), pass `leadSlaHours`, fix terminal status check (`lost_lead`, `junk_lead`, `not_qualified`), server-side sort |
| **Row & Bulk Actions** | Row: `Advance Stage`, `Previous Stage`, `Edit`, `Delete`/`Request Delete`; Bulk: `Task`/`Meeting`/`Call` (1 selected), `Enroll in Campaign`, `Convert Selected`, `Score with Loop AI`, `Delete` | Row: `View`, `Assign Lead`, `Delete`; Bulk: `Request record update`, `Assign to`, `Update selected`, `Request ownership`, `Request temp access`, `Enroll in Campaign`, `Delete`. **`LeadDetailDrawer` `onDelete` silently does nothing!** | Fix `LeadDetailDrawer` delete (`BUG-04`), wire `Edit`/stage actions under governance, pass `allMatching` to `Enroll`/`Assign`/`Update`, gate `canBulkEdit` |

#### B. Accounts (`accounts/page.tsx` vs `PoolAccountsTab.tsx`)

| Area | Private Accounts | Current Teams Pool Accounts | Target Parity Changes |
|---|---|---|---|
| **Views** | Table only | Table only | Keep Table only |
| **Quick Filters** | `Active Only`, `Parent Accounts`, `Created Last 7 Days` + Active Chips | `⚡ Open Unassigned Pool` only (renders bare label if `owner_id` hidden) | Add `Active Only`, `Parent Accounts`, `Created Last 7 Days` + non-destructive `Open Unassigned Pool` + Active Chips |
| **Filter Panel** | `AccountsFilterPanel` (`status`, `industries[]`, `currencies[]`, `employees_min/max`, `revenue_min/max`, `hierarchy_role`, `parent_account_ids[]`, `countries[]`, `states[]`, `cities[]`, `created_from/to`, `updated_from/to`, `search_fields[]`, `sort`+`dir`) | 3 `<select>`s (`owner_id/unassigned`, `industry`, `date_preset`) — even though `/teamspace/accounts/filter-options` already returns `currencies`, `countries`, `states`, `cities` | Full `AccountsFilterPanel` parity + Pool `Owner / Unassigned` filter |
| **Table & Drawer** | 15 FLS-filtered columns + server sort; Shift-click select; `AccountDetailDrawer` w/ `onNavigateAccount` & `?id=` sync | Reuses `AccountsTable` + always-on `owner` column; ignores `searchQuery`; no sort; drops Shift-click; `PoolDrawersContainer` **omits `hideDelete` & `onNavigateAccount`** and edits directly via `AddAccountModal` | Pass `hideDelete`, `onNavigateAccount`, `?id=` URL sync, governed edit, Shift-click support, server sort, fix `AccountsTable` `onMouseLeave` |

#### C. Contacts (`contacts/page.tsx` vs `PoolContactsTab.tsx`)

| Area | Private Contacts | Current Teams Pool Contacts | Target Parity Changes |
|---|---|---|---|
| **Views** | Table only | Table only | Keep Table only |
| **Quick Filters** | `Linked to Account`, `Has Email`, `Created Last 7 Days` + Active Chips | `⚡ Open Unassigned Pool` only | Add `Linked to Account`, `Has Email`, `Created Last 7 Days` + non-destructive `Open Unassigned Pool` + Active Chips |
| **Filter Panel** | `ContactsFilterPanel` (`account_ids[]`, `has_account`, `contact_sources[]`, `titles[]`, `departments[]`, `has_email`, `has_phone`, `countries[]`, `states[]`, `cities[]`, `created_from/to`, `updated_from/to`, `search_by`, `sort`+`dir`) | 3 `<select>`s (`owner_id/unassigned`, `contact_source` **hijacking `?lead_source=`**, `date_preset`) — even though `/filter-options` returns `titles`, `departments`, `countries`, `states`, `cities` | Full `ContactsFilterPanel` parity + dedicated `?contact_source=` URL param + Pool `Owner / Unassigned` |
| **Table & Drawer** | 20 FLS-filtered columns; Shift-click select; `ContactDetailDrawer` w/ `?id=` sync | **NO FLS filtering** in `usePoolColumns.ts:144-145`; untranslated labels; `PoolContactsTab` uses `poolLeadsTab.columns.owner` key; drops Shift-click; `PoolDrawersContainer` **omits `hideDelete`** | Apply `useContactFieldAccess()` FLS filtering + `tContacts("columns.*")` i18n + `hideDelete` + governed edit + Shift-click + server sort |

#### D. Deals (`deals/page.tsx` vs `PoolDealsTab.tsx`)

| Area | Private Deals | Current Teams Pool Deals | Target Parity Changes |
|---|---|---|---|
| **Views** | `list` + `kanban` (top `EntityActionBar` toggle). **No Grid view.** | `table` + **`grid` (`PoolDealsGrid`)** + `kanban` in `PoolViewModeBar` inside card | **Remove `PoolDealsGrid` & `"grid"` mode**; move `list`/`kanban` toggle to top `EntityActionBar` |
| **Pipeline & Currency** | Inside top of card; default pipeline selected; Currency includes **`"All Currencies"`** (`"all"` default); `"Total Deals: N"` | Outside card (`All Pipelines` default) + duplicate bar inside Kanban; Currency **forces single currency** (`includeAllOption={false}`); summary shows `deals.length` | Inside card; default pipeline (w/ All Pipelines in Table); Currency w/ `"All Currencies"` (`includeAllOption={true}`); show `totalItems`; remove duplicate Kanban bar |
| **Quick Filters** | `Open Deals`, `Closing This Month`, `Overdue Closing`, `Include Collaborating` + Active Chips | `⚡ Open Unassigned Pool`, `> $50k High Value` (hardcoded `$`), `In Negotiation` (exact match `"Negotiation/Review"` fails on custom stages) + no Active Chips | Add `Open Deals`, `Closing This Month`, `Overdue Closing`, non-destructive `Open Unassigned Pool`, Active Chips; fix stage matching |
| **Filter Panel** | `DealsFilterPanel` (`pipeline_id`, `stage_types[]`, `stages[]`/`stage_ids[]`, `amount_min/max`, `currencies[]`, `lead_sources[]`, `account_ids[]`, `contact_ids[]`, `closing_after/before`, `created_from/to`, `updated_from/to`, `sort`+`dir`) | 5 `<select>`s (`owner_id`, `stage` by name, `lead_source`, `date_preset`, `min_amount` w/ hardcoded `$`); omits `max_amount`, closing date, stage types, account/contact | Full `DealsFilterPanel` parity + Pool `Owner / Unassigned` + dynamic currency formatting |
| **Table** | 18 columns (`DEAL_COLUMNS`), server sort; row actions `Advance/Previous Stage`, `Edit`, `Mark Closed Won/Lost`, `Delete` | Menu exposes 18 columns **with no FLS**, but `PoolDealsTable.tsx` only renders **14** (missing `win_probability`, `loss_reason`, `loss_notes`, `updated_at`); `PoolColumnTable` desc sort puts nulls first | Implement all 18 FLS-filtered columns; fix desc null sort; server sort; fix Private `DealsTable.tsx:745-776` bonus ternary bug |
| **Kanban** | Server-backed `useSalesKanbanSummary` + infinite `useSalesKanbanColumn`; `win_probability%` + `CurrencySubtotals`; `ClosedLostModal` + `ConfirmModal` Won + feedback pulse | Page-only (max 50 deals); dumps cross-pipeline deals into column 0; hardcoded legacy roles (`sales_manager`/`manager`); skips `ClosedLostModal` & Won confirm; omits `pipeline_id`/`stage_type`/`win_probability`; non-UUID fallback `stage_id` | Server-backed Kanban per column; filter inactive stages; `CurrencySubtotals`; `ClosedLostModal` & Won confirm; `poolAccess` + governance permission check |

#### E. Tasks (`TasksTable.tsx` vs `PoolTasksTable.tsx` & `PoolTasksKanban`)

| Area | Private Tasks | Current Teams Pool Tasks | Target Parity Changes |
|---|---|---|---|
| **Views** | `list` + `kanban` in top `EntityActionBar` | `table` + `kanban` in `PoolViewModeBar` inside card | Move `list`/`kanban` toggle to top `EntityActionBar` |
| **Quick Filters** | `Active`, `Due Today`, `Overdue`, `High`, `Has Reminder`, `Completed` + Active Chips | `⚡ Open Unassigned Pool`, `🚨 Overdue Tasks`, `Due Today`, `High Priority` | Align with Private presets + `Open Unassigned Pool` + Active Filter Chips |
| **Filter Panel** | `TaskFilterPanel` (multi-select `statuses[]`, `priorities[]`, `related_types[]`, `has_reminder`, `ActivityDateRangeFilter` w/ `Tomorrow` + target `dueDate`/`createdTime`/`closedTime` + custom range) | 4 `<select>`s (`owner_id/unassigned`, `status`, `priority`, `date_preset` where `this_month` is **ignored by backend**); no FLS check on `status`/`priority` | Full `TaskFilterPanel` parity + Pool `Owner / Unassigned` + FLS checks + fix `this_month` |
| **Table & Kanban** | Highlighting across 5 columns; server sort; per-column Kanban queries; `canEdit` & `searchQuery` passed | Highlights `subject` only; omits `isUnassigned`/`TeamspaceAccessBadge`; page-only Kanban; **missing `canEdit` & `searchQuery`** on `TasksKanban` → unauthorized backward drag triggers Stage Down modal before failing | Add `TeamspaceAccessBadge` & `isUnassigned`, pass `canEdit` & `searchQuery` to `TasksKanban`, server-backed Kanban & sort |

#### F. Meetings (`MeetingsTable.tsx` vs `PoolMeetingsTable.tsx` & `PoolMeetingsKanban`)

| Area | Private Meetings | Current Teams Pool Meetings | Target Parity Changes |
|---|---|---|---|
| **Views & Create** | `list` + `kanban` in top `EntityActionBar`; `Schedule Meeting` + `Log Meeting` | `table` + `kanban` in `PoolViewModeBar`; single `Schedule Meet` button | Move toggle to top `EntityActionBar`; add `Schedule Meeting` + `Log Meeting` parity |
| **Quick Filters** | `Upcoming`, `Today`, `Has Google Meet`, `Minutes Logged`, `Completed` + Active Chips + Google Calendar Sync | `Today's Meetings`, `Upcoming` | Align with Private presets + Active Filter Chips |
| **Filter Panel** | `MeetingFilterPanel` (`statuses[]`, `meeting_types[]`, `related_types[]`, `minutes_logged`, `has_google_meet`, `ActivityDateRangeFilter` w/ `startTime`/`createdAt` + custom range) | 3 `<select>`s (`host_id`, `status`, `date_preset` where `this_month` is **ignored** and backend-supported `meeting_type` & `past` are **unwired**) | Full `MeetingFilterPanel` parity + Pool `Host` filter + fix `this_month` |
| **Table, Kanban & Drawer** | Interactive `MeetingStatusBadge`; deduplicated attendees; `MeetingDetailDrawer`; row actions (`Complete`, `Log Minutes`, `Edit`, `Reschedule`, `Delete`); server Kanban | `MeetingStatusBadge` without `onChange` shows **wrong `"Cancelled meetings cannot be modified"` tooltip** on Scheduled/In Progress; raw `attendees.length`; **row click opens raw `MeetingModal` edit form** with no `canEdit`; backward Kanban drag shows Stage Down modal before toast | Fix `MeetingStatusBadge` read-only tooltip; deduplicate attendees; open **`MeetingDetailDrawer`** with `hideDelete`/`canEdit`/governed actions; fix Kanban card drag disable when status change is governed |

#### G. Calls (`CallsTable.tsx` vs `PoolCallsTable.tsx` & `PoolCallsKanban`)

| Area | Private Calls | Current Teams Pool Calls | Target Parity Changes |
|---|---|---|---|
| **Views & Create** | `list` + `kanban` in top `EntityActionBar`; `Schedule Call` + `Log Call` | `table` + `kanban` in `PoolViewModeBar`; single `"Log Call"` button that opens `"schedule"` mode | Move toggle to top `EntityActionBar`; wire `Schedule Call` + `Log Call` (`defaultMode="log"`) |
| **Quick Filters** | `Scheduled`, `Today`, `Outbound`, `Inbound`, `Positive`, `High` (`High`+`Urgent`) + Active Chips | `Logged Today` (filters `created_at`!), `Interested Leads` (`status=Interested`) | Align with Private presets + `Interested` + Active Filter Chips; fix `today` to use `call_start_time` |
| **Filter Panel** | `CallFilterPanel` (`statuses[]`, `call_types[]`, `call_priorities[]` [`Urgent`/`High`/`Medium`/`Low`], `call_results[]` w/ `Wrong Number`, `call_purposes[]`, `call_sentiments[]`, `duration_min/max`, `related_types[]`, `ActivityDateRangeFilter`) | **BROKEN**: Shares Task priority values (`High`/`Normal`/`Low` — `"Normal"` matches 0 calls, `"Urgent"`/`"Medium"` impossible); merges Status+Outcome without `Wrong Number`; backend `call_type` unwired; `this_month` & `date_preset` filter wrong column | Full `CallFilterPanel` parity + Pool `Owner` filter + fix priority enum (`Urgent`/`High`/`Medium`/`Low`) + filter `call_start_time` |
| **Table, Kanban & Drawer** | Priority rank sort; `CallDetailDrawer`; `CallsKanban` rolls back when `onStatusChange` returns `false` | `PoolCallsTable` sorts `callPriority` **alphabetically**; **row click opens raw `CallModal` edit form**; **`PoolCallsKanban` `onStatusDrop` does NOT return `false` → cards optimistically move columns without saving!** | Priority rank sort; open **`CallDetailDrawer`** with `hideDelete`/`canEdit`; fix `onStatusDrop` (`return false`) and disable drag for non-editable cards; server-backed Kanban |

---

### 2.3 Export Comparison Matrix

| Dimension | Private CRM (`/export-downloads` & Client `exportData`) | Current Teams Pool (`TeamspaceExportDialog` & `admin_private`) | Target Parity State |
|---|---|---|---|
| **Modal Steps** | 1 step (`ExportOptionsModal`) | **2 steps** (or **3 steps** from All Teams: team picker → `TeamspaceExportDialog` → `ExportOptionsModal`). `admin_private` has **0 steps** (instant broken CSV download) | **1-step `ExportOptionsModal`** for direct/admin exports (team picker first only when `All Teams` needs governed team attribution, or support cross-team export for admins); inline optional/required Business Reason banner inside `ExportOptionsModal` ONLY when `approval_required` |
| **Business Reason** | Never asked (approval fallback broken) | **Mandatory `*`** even for Admins and `export_mode="direct"` | Required **only** when `!isAdmin && export_mode === "approval_required"` |
| **Column Picker & Labels** | Uses visible table columns with human-readable localized headers (`"Lead Owner"`, `"Email"`, `"Stage"`, etc.) | Hardcoded `snake_case` columns; checkboxes render `{col.replaceAll("_", " ")}`; **Deals includes invalid `stage`, `status`, `win_probability` → HTTP 422**; missing key columns across all 7 modules (`lead_name`, `account_name`, `contact_name`, `location`, `call_sentiment`, `google_meet_link`, etc.); `useState(visible)` goes stale if permissions load late | Reuse shared module export column definitions (`export_columns.py` / `exportColumns.ts`), localized human labels, FLS-filtered dynamically, default to current visible table columns |
| **File Generation & Format** | UTF-8 BOM CSV + native `openpyxl` XLSX (server) or SheetJS XLSX (client), formatted dates in user `timezone` + `date_format`, resolved FKs (`account_name`, `owner_name`) | Backend returns **CSV without BOM**; XLSX parsed client-side via `Papa.parse` (`governedExportDownload.ts:13-29`); raw UUIDs (`account_id`, `parent_account_id`), raw UTC timestamps, raw enums (`not_contacted`, `True`/`False`); format discarded when `pending` | Use unified server export formatter (`export_columns.py` + `export_file.py`) with UTF-8 BOM CSV & native XLSX, user timezone/date format, resolved FKs, persisted `format` on approval requests |
| **Permission & Scope Bugs** | Private approval fallback (`submitPersonal`) fails 422 on 3 checks; Private Deals bypasses `export_mode` | Direct download route `/action-requests/{id}/download` requires `teams_requests` → **403**; `isSelectAllMatching` exports only current page; `admin_private` truncates at **50 rows**, **500s on Leads** (`personal_email`), exports **blank Calls** (`call_status`/`duration_seconds`) | Fix download permission guard (`teams_pool` OR `teams_requests` for requester), support `all_matching` + `selection_filters`, retire legacy `/teamspace/export/pool` 50-row handler |

---

### 2.4 Bulk Import Comparison Matrix

| Module | Private Import Modal & Behavior | Current Teams Pool (`TeamspaceImportDialog.tsx`) | Key Gaps & Confirmed Bugs to Fix |
|---|---|---|---|
| **Leads** | `BulkImportModal.tsx`: grouped `EXPECTED_FIELD_GROUPS`, strict `mapLeadImportColumns`, AI mapping, 3000-row chunks, CSV+XLSX templates, skipped/failed report download | `GenericBulkImportModal`: flat list, substring matching, strips `owner_id`, CSV-only sample w/ legacy `"New"` status, drops `skipped_count`/`failed_count`/`errors` | Adopt `BulkImportModal` (or parity grouped mapper + XLSX templates + stage mapping UI + full skip/error telemetry) |
| **Accounts** | `GenericBulkImportModal`: `ACCOUNT_IMPORT_FIELDS`, skips duplicate account names | `TeamspaceImportDialog`: treats Accounts as non-sales (`sales = module === "leads" \|\| module === "deals"`) → **requires `owner`**, throws `"Select an activity assignee"`, breaks manager assignment; **409 duplicate aborts entire batch** | Fix `sales` set (`leads`, `accounts`, `contacts`, `deals`), support per-row/unassigned owner, skip duplicates + return telemetry |
| **Contacts** | `GenericBulkImportModal`: `CONTACT_IMPORT_FIELDS`, `autoSplitName`, skips duplicates | Treated as non-sales → **requires `owner`**, throws `"Select an activity assignee"`; 409 aborts entire batch; strict same-team exact-1 account match (422 otherwise) | Fix `sales` set, allow unassigned/per-row owner, graceful duplicate skipping + org/team account link policy |
| **Deals** | `DealsBulkImportModal` (`GenericBulkImportModal`): auto-creates missing Accounts/Contacts, skips duplicates, fuzzy stage resolution | Sample CSV header-only w/ stripped `Deal Owner`/`Created At`; requires pre-existing exact-1 Account+Contact in same team (422); **409 duplicate aborts batch** | Update `DEAL_SAMPLE_CSV`, support stage mapping + graceful duplicate handling + clear validation feedback |
| **Tasks** | `TaskBulkImportModal` (`GenericBulkImportModal`): 12-col template, org-wide graceful link fallback | 5-header sample CSV (missing `Related To Type/Name`, `Contact Name`, `Account Name`, `Reminder`); exact-1 same-team link check (422) | Use `TaskBulkImportModal` field/sample config; relax non-ambiguous link handling; return per-row skip/error report |
| **Calls** | `CallBulkImportModal`: 15-col + 2-row sample, defaults (`15` min, `Medium`, auto-fills phone, auto `call_result="Completed"`) | 5-header empty sample; defaults `duration=0`, `priority=None` → **422 `validate_call_completion()`** on any `"Completed"` row missing duration/result/description | Use `CallBulkImportModal` field/sample config + completion defaults parity |
| **Meetings** | Dedicated 4-step `MeetingBulkImportModal`: `autoMapMeetingColumns`, `parseDurationString`, 15-col CSV+XLSX templates, `notes`, optional external attendees | `GenericBulkImportModal` + strict `MeetingCreate`: **422 whenever `meeting_type` blank or `"Other"`** (`custom_type_label` required); `Number("1:30")` → `NaN` crash; `end_time <= start_time` 422; strips `notes` & `host_email`; 40-char ASCII title limit | Use `MeetingBulkImportModal` / lenient `MeetingImportItem` validation (`custom_type_label` handling, `parseDurationString`, `end_time` adjustment, `notes`, optional external attendees) |
| **Cross-Cutting** | No Business Reason; chunked batching; returns `imported_count`, `skipped_count`, `failed_count`, `errors` | Forced `Business reason *` even for admins/direct; approval-required sends entire file in 1 request; `serialize_import_receipt` drops `skipped_count`/`failed_count`/`errors` | Business Reason only when `approval_required`; return full receipt counts & row errors; chunked/async handling |

---

## 3. Complete Bug & Security Defect Register

### P0 — Security, Data Loss & Total Feature Failure

| ID | Location | Root Cause | Impact | Target Phase |
|---|---|---|---|---|
| **BUG-01** | [teamspace_pool_routes.py:192,233,264,293](../../../crusource-crm-backend/src/modules/teamspace/routes/teamspace_pool_routes.py#L192-L293) | `/teamspace/deals`, `/tasks`, `/meetings`, `/calls` have **no `dependencies=[Depends(require_permission(...)), Depends(require_setup_permission("teams_pool"))]`** (unlike `/leads`, `/accounts`, `/contacts`). `apply_record_team_scope` never checks `teams_pool` setup permission and returns 200 empty instead of 403. | Users whose role/profile disables `teams_pool` can query all 4 endpoints and retrieve team records. | **Phase 0** |
| **BUG-02** | All 7 pool handlers in [pool_sales_query_repository.py](../../../crusource-crm-backend/src/modules/teamspace/repositories/pool_sales_query_repository.py), [list_teamspace_accounts_handler.py](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_accounts_handler.py), [list_teamspace_contacts_handler.py](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_contacts_handler.py), [team_activities_handler.py](../../../crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py) | Missing `require_visible_filters()` and hidden-field exclusion from `search` (unlike private `/leads`, `/tasks/page`, `/meetings/page`, `/calls/page`). | Users with FLS-hidden fields (`office_email`, `phone`, `industry`, `lead_source`, `amount`, etc.) can probe/infer hidden values via filters or `search`. | **Phase 0** |
| **BUG-03** | [usePoolColumns.ts:144-145](../../../crusource-crm-frontend/src/components/teamspace/pool/columns/usePoolColumns.ts#L144-L145), [usePoolSectionPreferences.tsx](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/usePoolSectionPreferences.tsx), [PoolSectionColumnsMenu.tsx](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionColumnsMenu.tsx), [PoolDealsTable.tsx](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsTable.tsx) | Frontend FLS bypass: Contacts skips `useContactFieldAccess()`; Deals, Tasks, and Calls never check `getModuleFields(...)` in `PoolSectionColumnsMenu`, `PoolDealsTable`, `PoolDealsKanban`. Also `PoolFilters.tsx:375-377,571-587` ignores `isHidden` for Task/Meeting/Call `status` and `priority`. | Hidden fields remain exposed in Columns pickers, table headers, and filter dropdowns. | **Phase 0** |
| **BUG-04** | [TeamsPoolSection.tsx:1752-1755](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1752-L1755), [PoolDrawersContainer.tsx:99](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx#L99), [LeadDetailDrawer.tsx:327-331](../../../crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx#L327-L331) | `PoolDrawersContainer` passes `onDelete={onLeadDeleted}` which only closes the drawer and invalidates caches without calling `deleteLead` or `GovernedActionDialog`. `LeadDetailDrawer` skips its own `deleteLead` whenever `onDelete` is defined. | **Deleting a Lead from its detail drawer in Teams Pool silently does nothing** — the Lead stays in the database. | **Phase 0** |
| **BUG-05** | [PoolDrawersContainer.tsx:104-125](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx#L104-L125), [TeamsPoolSection.tsx:1762-1783,1823-1845](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1762-L1783) | `AccountDetailDrawer` and `ContactDetailDrawer` support `hideDelete?: boolean` specifically for Teams Pool governance, but `PoolDrawersContainer` omits `hideDelete` and `TeamsPoolSection` passes direct `onDelete`/`onEdit` opening raw `AddAccountModal`/`AddContactModal`. | **Governance bypass:** users can trigger direct deletes (and see `"Share / Move to TeamSpace"`) and raw edits from Pool Account/Contact drawers. | **Phase 0** |
| **BUG-06** | [TeamspaceExportDialog.tsx:92-110](../../../crusource-crm-frontend/src/components/teamspace/TeamspaceExportDialog.tsx#L92-L110), [governed_actions.py:271-276](../../../crusource-crm-backend/src/modules/approvals/services/governed_actions.py#L271-L276) | `columnsByModule.deals` pre-selects `"stage"`, `"status"`, and `"win_probability"`, none of which exist on `Deal.__table__.columns`. | **Teams Pool Deals Export ALWAYS fails with HTTP 422** `"Select supported export columns"` by default. | **Phase 5** |
| **BUG-07** | [teamspace_action_routes.py:59-64](../../../crusource-crm-backend/src/modules/teamspace/routes/teamspace_action_routes.py#L59-L64) | `GET /api/v1/teamspace/action-requests/{id}/download` requires `require_setup_permission("teams_requests")`. | Non-admin users with `teams_pool` + `export_mode="direct"` (without `teams_requests`) get **HTTP 403** immediately when downloading their own direct export. | **Phase 5** |
| **BUG-08** | [useLeadBoardActions.ts:234-263](../../../crusource-crm-frontend/src/hooks/leads/useLeadBoardActions.ts#L234-L263), [accounts/page.tsx:460-485](../../../crusource-crm-frontend/src/app/dashboard/accounts/page.tsx#L460-L485), [contacts/page.tsx:450-475](../../../crusource-crm-frontend/src/app/dashboard/contacts/page.tsx#L450-L475) | Private approval-required export fallback calls `submitPersonal` with `all_matching=True`, non-empty `data`, and UI column names. | Fails HTTP 422 on 3 separate checks in `governed_actions.py:165-276`. | **Phase 5** |
| **BUG-09** | [export_teamspace_handler.py:166-324](../../../crusource-crm-backend/src/modules/teamspace/handlers/export_teamspace_handler.py#L166-L324), [TeamsPoolSection.tsx:968-976](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L968-L976) | Legacy `GET /api/v1/teamspace/export/pool` (used by Admin Private): calls `list_teamspace_*` without `limit=None` (defaults to `50`), accesses non-existent `Lead.personal_email` (**500**), reads wrong `Call.call_status` / `duration_seconds` (always blank), ignores all filters/selection/format. | Admin Private export truncates at 50 rows, crashes 500 on Leads, exports blank Call columns, ignores filters. | **Phase 5** |
| **BUG-10** | [importRecords.ts:83-104](../../../crusource-crm-frontend/src/lib/teamspace/importRecords.ts#L83-L104), [meeting_commands.py:171-179](../../../crusource-crm-backend/src/modules/meetings/commands/meeting_commands.py#L171-L179) | `normalizeMeetingType(row.meeting_type \|\| "other")` omits `custom_type_label`, which `MeetingCreate` mandates when `meeting_type == "other"`. `Number(row.duration_minutes \|\| 30)` turns `"1:30"`/`"45 mins"` into `NaN` (`RangeError`); `end_time <= start_time` not adjusted. | **Teamspace Meetings import fails 422** whenever `meeting_type` is omitted or `"Other"`, and crashes on formatted durations. | **Phase 6** |
| **BUG-11** | [TeamspaceImportDialog.tsx:97,121-124,165,227-236](../../../crusource-crm-frontend/src/components/teamspace/TeamspaceImportDialog.tsx#L97-L236), [importRecords.ts:28-29](../../../crusource-crm-frontend/src/lib/teamspace/importRecords.ts#L28-L29) | `sales` is defined as `leads \|\| deals`, omitting `accounts` and `contacts` (unlike `TeamspaceCreateDialog.tsx:45-50`). | Blocks importing Accounts/Contacts into the Unassigned pool, forces `"Assignee *"`, and checks activity permission flag instead of `assign_mode`. | **Phase 6** |
| **BUG-12** | [PoolActivitiesTab.tsx:43-44](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolActivitiesTab.tsx#L43-L44), [PoolActivityKanbans.tsx:69-87](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolActivityKanbans.tsx#L69-L87), [CallsKanban.tsx:148-157](../../../crusource-crm-frontend/src/components/dashboard/calls/CallsKanban.tsx#L148-L157) | `onStatusDrop` returns a toast ID string instead of `false`. `CallsKanban` checks `if (res !== false)` and mutates `localCalls`. | Dragging a Call card in Teams Pool Kanban displays a blocked-action toast **yet moves the card to the target column in the UI** without saving! | **Phase 4** |
| **BUG-13** | [TeamsPoolSection.tsx:985-989,1078-1080,1227-1234](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L985-L1234), [GovernedActionDialog.tsx:319-321](../../../crusource-crm-frontend/src/components/teamspace/GovernedActionDialog.tsx#L319-L321), [PoolModalsContainer.tsx:242-250](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolModalsContainer.tsx#L242-L250) | `isSelectAllMatching` is ignored by `bulk_update` (omits `all_matching` & `selection_filters`), `Export` (`allMatching` not passed), `BulkTransferModal` (`recordIds` only), and `Enroll in Campaign` (`currentListIds` only). | User clicks *"Select all matching N records"* across pages, but **only the current page (max 50)** is updated, exported, transferred, or enrolled. | **Phase 0 & Phase 5** |
| **BUG-14** | [PoolDrawersContainer.tsx:152-167](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx#L152-L167), [TeamsPoolSection.tsx:1806-1817](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1806-L1817) | Meetings and Calls open raw `MeetingModal`/`CallModal` edit forms instead of `MeetingDetailDrawer`/`CallDetailDrawer`, with no `canEdit`/`accessDecisions` check and unconditional refetch on close. | Read-only team members land in active edit forms (bypassing governance or hitting 403), and lose drawer features (minutes, outcomes, stage stepper, access requests). | **Phase 4** |

### P1 — High-Severity Functional, Query & UX Bugs

| ID | Location | Root Cause | Impact | Target Phase |
|---|---|---|---|---|
| **BUG-15** | [PoolDealsTable.tsx:77-345](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsTable.tsx#L77-L345) vs [poolSectionColumns.ts:41-42](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/poolSectionColumns.ts#L41-L42) | `PoolSectionColumnsMenu` exposes 18 Deal columns, but `PoolDealsTable` only defines 14. | `win_probability`, `loss_reason`, `loss_notes`, and `updated_at` can be checked in the menu but never render in the table. | **Phase 3** |
| **BUG-16** | [TeamsPoolSection.tsx:335-338,538,1459](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L335-L338) | `activeDealsCurrency` defaults to `userCurrency \|\| "USD"` with `includeAllOption={false}`. | Multi-currency Deals cannot be viewed together; clearing filters still forces a single currency. | **Phase 3** |
| **BUG-17** | [PoolFilters.tsx:571-587](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx#L571-L587), [teamspacePool.json:644-648](../../../crusource-crm-frontend/src/messages/en/teamspacePool.json#L644-L648) | Pool Calls shares Task priority options (`High`, `Normal`, `Low`) instead of Call priorities (`Urgent`, `High`, `Medium`, `Low`). | `"Normal"` matches 0 calls; `"Urgent"` and `"Medium"` cannot be filtered at all. | **Phase 2 & Phase 4** |
| **BUG-18** | [PoolFilters.tsx:613-615](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx#L613-L615), [team_activities_handler.py:94-105,173-186](../../../crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py#L94-L186) | Tasks and Meetings `date_preset=this_month` is offered in the UI but not handled in backend `if/elif` chains; Calls `date_preset` filters `Call.created_at` instead of `Call.call_start_time`; all 7 pool handlers use rolling UTC 7d/30d windows instead of user timezone calendar boundaries. | `"This Month"` silently returns unfiltered rows for Tasks/Meetings; Calls `"Today"` filters creation date instead of call time. | **Phase 0 & Phase 2** |
| **BUG-19** | [pool_sales_query_repository.py:89-94,170-175](../../../crusource-crm-backend/src/modules/teamspace/repositories/pool_sales_query_repository.py#L89-L175), [list_teamspace_accounts_handler.py:55-60](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_accounts_handler.py#L55-L60), [list_teamspace_contacts_handler.py:53-58](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_contacts_handler.py#L53-L58), [team_activities_handler.py:87-92](../../../crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py#L87-L92) | `if is_unassigned is True: ... elif is_unassigned is False: ... elif owner_id: ...` | Sending `is_unassigned=false` with `owner_id` silently discards `owner_id`. | **Phase 0** |
| **BUG-20** | [list_teamspace_records_handler.py:46,96](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_records_handler.py#L46-L96), [list_teamspace_contacts_handler.py:93](../../../crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_contacts_handler.py#L93), [team_activities_handler.py:114,197,286](../../../crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py#L114-L286) | Queries order only by timestamp with no `id` tie-breaker (only Accounts includes `Account.id.asc()`). | Bulk-imported rows with equal timestamps duplicate or disappear across page boundaries. | **Phase 0** |
| **BUG-21** | [PoolDealsTab.tsx:78-86](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsTab.tsx#L78-L86), [PoolDealsKanban.tsx:305-327,556-559](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx#L305-L559), [PoolActivitiesTab.tsx:54-141](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolActivitiesTab.tsx#L54-L141) | Pool Kanbans only receive the single active Table page (`limit=50`) with no pagination or column queries; `PoolDealsKanban` does not filter inactive stages and dumps unmatched cross-pipeline deals into `stages[0]`. | Records past page 1 are invisible in Kanban; cross-pipeline deals appear in the wrong stage column. | **Phase 3 & Phase 4** |
| **BUG-22** | [PoolDealsKanban.tsx:277-280,436-456,524-528](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx#L277-L528) | `canDragDeal` checks hardcoded legacy roles (`sales_manager`/`manager`) instead of `canLeadTeams` + `poolAccess`; skips `ClosedLostModal` (loss reason) and `ConfirmModal` for Closed Won; sends incomplete PATCH payload (and non-UUID fallback `stage_id`). | Temporary-access teammates cannot drag; managers can drag view-only deals (403); Closed Lost skips loss reason; fallback mode fails UUID validation. | **Phase 3** |
| **BUG-23** | [TeamsPoolSection.tsx:232-256](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L232-L256) | `handleAssignmentChange` checks `if (unassigned === true)` and wipes `search`, `status`, `priority`, `lead_source`, `industry`, `date_preset`, `min_amount`, and forces `team_id: isAdmin ? "all" : activeTeamId`. | Cannot combine `Unassigned` with any filter; admins are switched into read-only `"all"` mode, disabling Assign/Add/Bulk Update. | **Phase 2** |
| **BUG-24** | [TeamsPoolSection.tsx:1095-1114](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1095-L1114), [PoolSectionSavedViews.tsx:8-59](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionSavedViews.tsx#L8-L59) | Saved Views omitted on `leads`/`accounts`/`contacts`; `FILTER_KEYS` drops `pipeline_id`, `currency`, `lead_source`, `industry`, `contact_source`, `max_amount`, `meeting_type`, `call_type`; saves `search: ""`; non-atomic `onApply` splits `search` through debounced `useSearchDraft` causing double fetches. | Incomplete saved views, stale URL params after view apply, and search race conditions. | **Phase 2** |
| **BUG-25** | [PoolColumnTable.tsx:48-57,79-88](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolColumnTable.tsx#L48-L88) | `compareValues` places empties last (`1`/`-1`), then line 86 multiplies by `direction` (`-1` for `desc`); `sort` state persists when sorted column is hidden. | **Descending sort pushes `null`/empty rows to the top** across Deals, Tasks, Meetings, and Calls. | **Phase 0 & Phase 3** |
| **BUG-26** | [PoolMeetingsTable.tsx:228](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolMeetingsTable.tsx#L228), [MeetingStatusBadge.tsx:42-56](../../../crusource-crm-frontend/src/components/dashboard/meetings/table/MeetingStatusBadge.tsx#L42-L56) | `MeetingStatusBadge` without `onChange` assumes status is either `"completed"` or `"cancelled"`. | Hovering over `Scheduled` or `In Progress` meeting badges in Teams Pool displays `"Cancelled meetings cannot be modified"`. | **Phase 4** |
| **BUG-27** | [PoolActivityKanbans.tsx:33-65](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolActivityKanbans.tsx#L33-L65), [TasksKanban.tsx](../../../crusource-crm-frontend/src/components/dashboard/tasks/TasksKanban.tsx), [MeetingsKanban.tsx](../../../crusource-crm-frontend/src/components/dashboard/meetings/MeetingsKanban.tsx) | `PoolTasksKanban` omits `canEdit` (defaults `true`); `PoolMeetingsKanban` leaves cards draggable while passing `onStatusDrop` to `onStatusChange`. | Backward drags open a `"Stage Down"` confirmation modal before failing with a governed-notice toast. | **Phase 4** |
| **BUG-28** | [PoolDealsGrid.tsx:168-182](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsGrid.tsx#L168-L182) | Uses `<MoreVertical />` (`⋮`) button as an immediate Delete click, ignores `deleteRequiresApproval`, omits `onAssignDeal`, and ignores `deal.stage_color`. | Misleading icon triggers immediate delete confirmation. (Resolved by removing Grid view in Phase 1.) | **Phase 1** |
| **BUG-29** | [TeamsPoolSection.tsx:1363,1386-1390](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1363-L1390), [PoolLeadsTab.tsx:83](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolLeadsTab.tsx#L83), [PoolAccountsTab.tsx:55](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolAccountsTab.tsx#L55), [PoolContactsTab.tsx:55](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolContactsTab.tsx#L55) | `canBulkEdit` is hardcoded `true` on `EntityActionBar` and passed as `Boolean(onToggleSelect)`. | Users without `can_bulk_edit` still see bulk checkboxes, `Select all matching`, and `Enroll in Campaign`. | **Phase 0** |
| **BUG-30** | [TeamsPoolSection.tsx:633-694,1476-1738](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L633-L694) | `error`/`isError` from all 7 `useTeamspace*` queries is never read; no top-level `canView === false` module gate. | 403/500/network failures silently render `"No Team ... Found"` with no Retry button. | **Phase 0** |
| **BUG-31** | [PoolLeadsTab.tsx:50-56,115-117](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolLeadsTab.tsx#L50-L117), [TeamsPoolSection.tsx:726-728](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L726-L728) | `Stale: Xd` checks invalid statuses (`"lost"`, `"dead"` instead of `"lost_lead"`, `"junk_lead"`, `"not_qualified"`); `transformBackendLead(raw)` omits `leadSlaHours`; `rows` sort ignores `sort.field` and always sorts `ai_priority_score` (`-1` for nulls). | Closed/junk/disqualified leads show false `"Stale"` tags; `OVERDUE` badge diverges from Private Leads SLA; unscored leads sort before 0. | **Phase 3** |
| **BUG-32** | [pool_sales_query_repository.py:41-117,162-164](../../../crusource-crm-backend/src/modules/teamspace/repositories/pool_sales_query_repository.py#L41-L164) | Pool Leads lacks `include_converted` (defaulting `false` in Private Leads); Pool Deals `stage` uses exact case-sensitive `PipelineStage.name == stage.strip()`, breaking `"In Negotiation"` quick filter (`"Negotiation/Review"`) on custom/renamed stages. | Converted leads clutter the open Leads pool; `"In Negotiation"` returns 0 deals if stage is named `"Negotiation"`. | **Phase 0 & Phase 3** |
| **BUG-33** | [governed_actions.py:117-120,231,361-363](../../../crusource-crm-backend/src/modules/approvals/services/governed_actions.py#L117-L363), [GenericBulkImportModal.tsx:506-507](../../../crusource-crm-frontend/src/components/shared/GenericBulkImportModal.tsx#L506-L507), [import_record_preparation.py:42-46](../../../crusource-crm-backend/src/modules/approvals/services/import_record_preparation.py#L42-L46), [completion_validation.py:4-14](../../../crusource-crm-backend/src/modules/calls/services/completion_validation.py#L4-L14) | `serialize_import_receipt` drops `skipped_count`/`failed_count`/`errors`; non-Lead imports roll back atomically on any 1 duplicate/422; approval-required import sends entire file in 1 request; exact-1 same-team link resolution fails on 0/>1 matches; Calls lacks completion defaults. | Partial imports fail completely with opaque errors, large approval imports risk timeouts, and skipped-row export is dead. | **Phase 6** |

### P2 & P3 — Medium/Low Parity & Polish Bugs (Plus Shared/Private Bugs Found)

| ID | Location | Summary of Issue | Target Phase |
|---|---|---|---|
| **BUG-34** | [PoolTabBar.tsx:19-87](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolTabBar.tsx#L19-L87), [TeamsPoolSection.tsx:1416-1424](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1416-L1424) | Inactive tab count badges show `0` until visited. (Resolved by removing counts per user request.) | **Phase 1** |
| **BUG-35** | [TeamsPoolSection.tsx:1427-1465](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1427-L1465), [PoolDealsKanban.tsx:572-599](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx#L572-L599) | Duplicate Pipeline Selector bars in Pool Deals Kanban with conflicting defaults (`All Pipelines` vs `defaultPipeline`). | **Phase 1 & Phase 3** |
| **BUG-36** | [PoolLeadsTab.tsx:91-109](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolLeadsTab.tsx#L91-L109), [leadBoardConfig.ts:40](../../../crusource-crm-frontend/src/components/leads/board/leadBoardConfig.ts#L40) | Pool Leads renders duplicate owner columns when `Lead Owner` (`owner_name`) is enabled in ColumnsDropdown alongside always-on `extraColumns.owner`. | **Phase 3** |
| **BUG-37** | [TeamsPoolSection.tsx:197-204,813-824](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L197-L204), [PoolAccountsTab.tsx:52-53](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolAccountsTab.tsx#L52-L53), [PoolContactsTab.tsx:52-53](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolContactsTab.tsx#L52-L53) | Changing page does not clear `selectedRecordIds` → stale indeterminate/checked header checkbox on page 2; Shift-click range selection is discarded in `PoolAccountsTab` & `PoolContactsTab`. | **Phase 3** |
| **BUG-38** | [TeamsPoolSection.tsx:1364-1369](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1364-L1369), [EntityActionBar.tsx:202](../../../crusource-crm-frontend/src/components/shared/EntityActionBar.tsx#L202) | `poolScopeControls` (admin Team dropdown + Refresh) is hidden below `640px` (`hidden sm:flex` in `savedViewsToggle`). | **Phase 1** |
| **BUG-39** | [TeamsPoolSection.tsx:1351](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1351), [PoolFilters.tsx:81](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx#L81), [PoolDealsTab.tsx:71](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsTab.tsx#L71) | `activeFilterCount` omitted on `EntityActionBar`; `countActivePoolFilters` counts outside `selectedPipelineId`; `PoolDealsTab` summary shows `deals.length` instead of `pagination.totalItems`. | **Phase 1 & Phase 2** |
| **BUG-40** | [PoolCallsTable.tsx:51-56,189](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolCallsTable.tsx#L51-L189), [PoolMeetingsTable.tsx:202](../../../crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolMeetingsTable.tsx#L202) | `PoolCallsTable` sorts `callPriority` alphabetically; `startOf()` includes time-only `callStartTime` (`NaN` risk); `PoolMeetingsTable` doesn't deduplicate attendees by email; all 3 activity tables omit `isUnassigned` and `TeamspaceAccessBadge`. | **Phase 4** |
| **BUG-41** | [PoolDrawersContainer.tsx:104-113](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx#L104-L113), [TeamsPoolSection.tsx:1485-1667](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L1485-L1667) | Missing `onNavigateAccount` on Pool `AccountDetailDrawer`; no `?id=` URL drawer deep-linking; Calls create button says `"Log Call"` but opens `"schedule"` mode; `GovernedActionDialog` renders free-text `<input>` for Meeting/Call enums & strips `account_name`. | **Phase 3, Phase 4 & Phase 7** |
| **BUG-42** | [PoolFilters.tsx:108-113,455-470,530-531,704-721](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx#L108-L721), [team_activities_handler.py:252-258](../../../crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py#L252-L258) | `PoolFilters` renders bare `"Quick Filters:"` label when `owner_id` hidden; splits single-select strings on `,`; Contacts hijacks `?lead_source=`; Lead Source injects phantom legacy options; backend `ILIKE` lacks wildcard escaping (`%`/`_`) and `list_teamspace_meetings` uses `joinedload` instead of `selectinload`. | **Phase 0 & Phase 2** |
| **BUG-43** | [PoolSectionColumnsMenu.tsx:33,63-114](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionColumnsMenu.tsx#L33-L114), [usePoolColumnVisibility.ts:44-61](../../../crusource-crm-frontend/src/components/teamspace/pool/columns/usePoolColumnVisibility.ts#L44-L61), [usePoolSectionPreferences.tsx:40-56](../../../crusource-crm-frontend/src/components/teamspace/pool/sections/usePoolSectionPreferences.tsx#L40-L56) | Calls checklist ignores `onReset`; empty `localStorage` violates `minVisible: 1`; `usePoolSectionPreferences` flashes Table → Kanban on reload (`useEffect` hydration); `PoolContactsTab.tsx:59` uses `poolLeadsTab.columns.owner` i18n key; `PoolSectionColumnsMenu` only toasts reset for Deals/Leads. | **Phase 1 & Phase 4** |
| **BUG-44** | [TeamsPoolSection.tsx:741-747,1338-1343,1477-1478](../../../crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx#L741-L1478), [PoolModalsContainer.tsx:96-191,266-364](../../../crusource-crm-frontend/src/components/teamspace/pool/PoolModalsContainer.tsx#L96-L364) | `deals`/`tasks`/`meetings`/`calls` omit `canReadPool` guard; `isLoading` renders table skeleton in Kanban; `TeamspaceAccessBadge` shifts layout above `EntityActionBar`; `PoolModalsContainer` holds dead legacy delete/import branches; hardcoded `$` symbols and untranslated English strings across Pool modals/badges. | **Phase 1, Phase 6 & Phase 7** |
| **BUG-45** | **Bonus (Private Deals):** [DealsTable.tsx:745-776](../../../crusource-crm-frontend/src/components/deals/DealsTable.tsx#L745-L776) | `!deal.stage_type ? deal.stage !== "closed_lost" : deal.stage_type !== "lost" && (<DropdownMenuItem ... />)` — ternary precedence evaluates to boolean when `stage_type` is null, hiding `"Mark Closed Lost"` / `"Mark Closed Won"`. | **Phase 3** (or cleanup) |
| **BUG-46** | **Bonus (Private/Shared):** [export_deals_handler.py:82](../../../crusource-crm-backend/src/modules/deals/handlers/export_deals_handler.py#L82), [AccountsTable.tsx:180-186,341,357-367](../../../crusource-crm-frontend/src/components/accounts/AccountsTable.tsx#L180-L367), [ContactsTable.tsx:177-183](../../../crusource-crm-frontend/src/components/contacts/ContactsTable.tsx#L177-L183) | `export_deals_handler` checks `owner_id` instead of `deal_owner_id` for FLS; `AccountsTable`/`ContactsTable` lack `onMouseLeave={handleMouseUp}`, `AccountsTable` renders blank for empty location and `"-"` for `0` employees/revenue; `SavedViewsDropdown` `is_default` is never auto-applied. | **Phase 3 & Phase 5** |

---

## 4. Target Architecture & Governance Boundary

### Design Principles
1. **Single Source of Truth for Filters, Tables, Drawers, Export & Import:** Rather than maintaining forked Pool clones (`PoolFilters.tsx`, `PoolViewModeBar.tsx`, `PoolDealsGrid.tsx`, `TeamspaceExportDialog.tsx`), Teams Pool composes the **same** private UI primitives (`EntityActionBar`, `FilterDrawer` panels, `QuickFilterBar`, `SavedViewsDropdown`, `ExportOptionsModal`, module Kanban/Table components, module Detail Drawers, and module Import modals), parameterized for Pool scope.
2. **Backend Query & Security Symmetry:** Teamspace Pool list/filter/kanban/export/import handlers must delegate to shared filter-clause builders, FLS validators (`require_visible_filters`), deterministic `id` tie-breaker sorts, timezone-aware date range helpers, and shared export/import formatters.
3. **Clear Pool vs. Private Boundary:**

| Capability | Identical to Private CRM | TeamSpace / Pool-Specific Behavior Preserved |
|---|---|---|
| **Toolbar & View Switcher** | `EntityActionBar` top `list`/`kanban` toggle left of Search, `SavedViewsDropdown`, `Filters (N)`, `Columns`, `Export`, `Import All`, Primary/Secondary Add buttons | `PoolTabBar` (7 tabs, **no count badges**), Admin Team Switcher (`All Teams` / `Admin Private` / `<Team>`) + Refresh button (mobile-accessible), `allTeamsReadOnly` status banner |
| **Filters & Saved Views** | Slide-over `FilterDrawer` + `QuickFilterBar` + Active Filter Chips + `SavedViewsDropdown` | Adds `Owner / Unassigned` filter section + `⚡ Open Unassigned Pool` quick chip (non-destructive); saves views under `entity_type = "teamspace_pool_<tab>"`; pool-only `localStorage` keys for column/view preferences |
| **Table, Kanban & Drawers** | Same columns, cell badges, SLA (`leadSlaHours`), currency subtotals, `ClosedLostModal`, detail drawers (`LeadDetailDrawer`, `AccountDetailDrawer`, `ContactDetailDrawer`, `DealDetailDrawer`, `TaskModal` view, `MeetingDetailDrawer`, `CallDetailDrawer`), `?id=` URL sync | Pool `Owner` / `Assignee` / `Host` cell with `You` / `Unassigned` pills + `TeamspaceAccessBadge`; `hideDelete` + governed delete/edit/transfer/access-request actions; `Assign` & `Request Ownership` / `Request Temporary Access` |
| **Export & Bulk Import** | Single-step `ExportOptionsModal` + server `export_columns.py` / `export_file.py`; module bulk import wizards, templates, stage mapping, duplicate handling, and error/skip telemetry | Team attribution (`team_id`) + governed `approval_required` routing when policy requires leadership approval (only showing Business Reason when `approval_required`) |

---

## 5. Phased Implementation Plan (Phases 0 – 8)

### Phase 0: Security Hardening, Critical Data-Loss Fixes & Backend Query Foundation
- **Objective:** Close all authorization/FLS security holes, fix silent data-loss/deletion bugs, and upgrade backend `/api/v1/teamspace/*` pool endpoints to match private list filtering, sorting, and pagination contracts.
- **Dependencies:** None (must land before Phases 2–6).
- **Files to Modify:**
  - Backend:
    - `crusource-crm-backend/src/modules/teamspace/routes/teamspace_pool_routes.py`
    - `crusource-crm-backend/src/modules/teamspace/routes/teamspace_pool_contacts_routes.py`
    - `crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_records_handler.py`
    - `crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_accounts_handler.py`
    - `crusource-crm-backend/src/modules/teamspace/handlers/list_teamspace_contacts_handler.py`
    - `crusource-crm-backend/src/modules/teamspace/handlers/team_activities_handler.py`
    - `crusource-crm-backend/src/modules/teamspace/repositories/pool_sales_query_repository.py`
    - Shared filter helpers in `src/modules/{leads,accounts,contacts,deals,tasks,meetings,calls}/repositories/*`
  - Frontend:
    - `crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/columns/usePoolColumns.ts`
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/usePoolSectionPreferences.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionColumnsMenu.tsx`
    - `crusource-crm-frontend/src/components/teamspace/GovernedActionDialog.tsx`
    - `crusource-crm-frontend/src/services/teamspace/teamspacePoolService.ts`
- **Implementation Changes:**
  1. **Route Guards (`BUG-01`):** Add `dependencies=[Depends(require_permission("<module>", "view")), Depends(require_setup_permission("teams_pool"))]` to `/teamspace/deals`, `/teamspace/tasks`, `/teamspace/meetings`, `/teamspace/calls`.
  2. **Backend FLS & Wildcard Escaping (`BUG-02`, `BUG-42`):** Enforce `require_visible_filters()` on all 7 pool list endpoints, exclude FLS-hidden fields from `search` columns, and escape `\`, `%`, `_` in all `ILIKE` filters (reuse `activity_pagination.py` escaping helper). Switch `list_teamspace_meetings` from `joinedload` to `selectinload`.
  3. **Frontend FLS & Permission Gates (`BUG-03`, `BUG-29`, `BUG-30`):**
     - Call `useContactFieldAccess()` in `usePoolColumns.ts` for Contacts.
     - Filter `POOL_COLUMN_SECTIONS` in `usePoolSectionPreferences.tsx` / `PoolSectionColumnsMenu.tsx` using `getModuleFields(section)`.
     - Gate `canBulkEdit` on `TeamsPoolSection` using `isAdmin || Boolean(modPerm?.can_bulk_edit && modPerm?.can_edit)` instead of hardcoded `true`.
     - Add top-level `canView === false` guard and `QueryErrorState` + Retry handling for `isError`/`error` on all 7 `useTeamspace*` queries.
  4. **Fix Silent Lead Delete & Drawer Governance Bypasses (`BUG-04`, `BUG-05`):**
     - Pass `hideDelete` to `AccountDetailDrawer`, `ContactDetailDrawer`, `LeadDetailDrawer`, and `DealDetailDrawer` in `PoolDrawersContainer.tsx` when rendered inside Teams Pool, OR wire drawer `onDelete` directly to `handleDeleteLead`/`handleDeleteAccount`/`handleDeleteContact`/`handleDeleteDeal` (`GovernedActionDialog`) and `onEdit` to governed edit when `edit_own_mode === "approval_required"` (instead of silent no-op or raw edit).
  5. **Fix `is_unassigned=False` + `owner_id` & Deterministic Sort Tie-Breaker (`BUG-19`, `BUG-20`):**
     - Replace `elif is_unassigned is False:` branch so `owner_id` (and multi-owner `owner_ids[]`) is never dropped; always append `Model.id.asc()` tie-breaker to `.order_by(...)` in all 7 pool handlers.
  6. **Fix `allMatching` in `GovernedActionDialog` (`BUG-13`):** Include `all_matching: true, selection_filters` for `action === "bulk_update"` as well as `export`/`delete`/`bulk_delete`, and wire `allMatching` into `BulkTransferModal` and campaign enrollment (via `/leads/selection` or `all_matching` endpoint).
  7. **Backend Filter, Sort & Date Parity (`BUG-18`, `BUG-32`):**
     - Expand all 7 `/api/v1/teamspace/*` list endpoints (and `TeamspacePoolService`) to accept the full private filter & sort parameter sets (multi-select arrays `statuses[]`, `stage_ids[]`, `owner_ids[]`, `industries[]`, `currencies[]`, `countries[]`, `states[]`, `cities[]`, numeric ranges, custom `date_from`/`date_to` + `date_field` + `timezone`, `include_converted` for Leads, `search_by`, `sort`/`dir` / `sort_by`/`sort_dir`).
     - Fix Tasks/Meetings `this_month` preset, fix Calls `date_preset` to filter `Call.call_start_time`, normalize Deals `stage` matching like `deals_repository.py`, and add server-backed `/teamspace/{leads,deals,tasks,meetings,calls}/kanban-summary` and `/kanban-column` (or `team_id`/`pool_scope` filter support on existing kanban endpoints).
- **Acceptance Criteria & Verification:**
  - Users without `teams_pool` receive HTTP 403 on all 7 pool endpoints.
  - FLS-hidden filter params return 403/422 and never match via `search`.
  - Deleting a Lead/Account/Contact/Deal from its Pool drawer executes governance and deletes/requests deletion cleanly.
  - Verification: `pytest` in `crusource-crm-backend/tests/` for new + existing teamspace pool/security tests (`test_teamspace_*.py`).

---

### Phase 1: Teams Pool Shell, `PoolTabBar`, Toolbar View Switcher & Pipeline Bar Layout
- **Objective:** Align the visual hierarchy of Teams Pool with the individual CRM modules (remove tab counts, move view switcher to `EntityActionBar`, remove Deals Grid view, move Pipeline/Currency inside the card, fix mobile admin controls & loading skeletons).
- **Dependencies:** None (UI shell can proceed alongside Phase 0).
- **Files to Modify / Delete:**
  - Modify:
    - `crusource-crm-frontend/src/components/teamspace/pool/PoolTabBar.tsx`
    - `crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/poolSectionColumns.ts`
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/usePoolSectionPreferences.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsTab.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolActivitiesTab.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx`
    - `crusource-crm-frontend/src/components/shared/EntityActionBar.tsx` (if adding a non-hidden slot for Pool team scope controls on mobile)
  - Delete:
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolViewModeBar.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsGrid.tsx`
- **Implementation Changes:**
  1. **Remove Tab Counts (`BUG-34`):** Remove `counts` prop and count pill `<span>` from `PoolTabBar.tsx` and `TeamsPoolSection.tsx`.
  2. **Remove Deals Grid View (`BUG-28`):** Change `PoolSectionViewMode` to `"list" | "kanban"` (mapping persisted `"table"` → `"list"` and `"grid"` → `"list"` seamlessly); set `POOL_VIEW_MODES` for `leads`, `deals`, `tasks`, `meetings`, `calls`; delete `PoolDealsGrid.tsx`.
  3. **Move View Switcher to Top `EntityActionBar`:** Pass `viewMode` & `onViewModeChange` directly to `EntityActionBar` for `leads`, `deals`, `tasks`, `meetings`, `calls` (and omit for `accounts`, `contacts`). Delete `PoolViewModeBar.tsx` and initialize `viewModes` synchronously from `localStorage` (guarded for SSR) to avoid hydration flash (`BUG-43`).
  4. **Move Pipeline & Currency Inside the Card (`BUG-35`):**
     - Remove the floating Pipeline/Currency strip from `TeamsPoolSection.tsx:1427-1465` and the duplicate bar in `PoolDealsKanban.tsx:572-599`.
     - Render the unified Pipeline (+ Currency + `Total Records: N`) header bar **inside** the top of the `bg-white border border-outline rounded-xl` container for `leads` and `deals`, styled identically to `LeadBoard.tsx:373-404` and `deals/page.tsx:846-893`.
  5. **Fix Mobile Scope Controls, Loading Skeleton & Layout Shift (`BUG-38`, `BUG-44`):**
     - Move `poolScopeControls` (admin Team selector + Refresh) out of `savedViewsToggle` (`hidden sm:flex`) into a dedicated mobile-visible bar or `toolbarSecondaryActions` so admins can switch teams on `<640px`.
     - Render `<LoadingState variant={viewMode === "kanban" ? "kanban" : "table"} />` in Kanban mode.
     - Relocate `TeamspaceAccessBadge` into the selection bar / inline slot rather than pushing `EntityActionBar` down on single selection.
- **Acceptance Criteria & Verification:**
  - Zero count pills on `PoolTabBar`.
  - View toggle (`List` / `Kanban` Material icons) sits immediately left of Search in `EntityActionBar` for Leads, Deals, Tasks, Meetings, Calls; absent on Accounts & Contacts.
  - No `Grid` button anywhere in Deals.
  - Pipeline & Currency bar sits inside the top border of the table/kanban card below `QuickFilterBar`.

---

### Phase 2: Modern Filters, QuickFilterBar, Active Filter Chips & Saved Views Across All 7 Tabs
- **Objective:** Replace `PoolFilters.tsx` (`PoolFilterPanel` + `PoolQuickFilters`) with the modern slide-over `FilterDrawer` panels, `QuickFilterBar` + active chips, `activeFilterCount` badge, and full `SavedViewsDropdown` across all 7 tabs.
- **Dependencies:** Phase 0 (backend filter params), Phase 1 (shell layout).
- **Files to Modify / Create / Delete:**
  - Modify:
    - `crusource-crm-frontend/src/hooks/useTeamspaceUrlState.ts` and `src/lib/teamspaceUrl.ts` (support full per-module filter & sort URL/state serialization)
    - `crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx`
    - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionSavedViews.tsx`
    - Private filter panels (add optional Pool `Owner / Unassigned` `SearchableMultiSelect` section prop so one component serves both Private and Pool):
      - `src/components/leads/FilterPanel.tsx`
      - `src/components/accounts/AccountsFilterPanel.tsx`
      - `src/components/contacts/ContactsFilterPanel.tsx`
      - `src/components/deals/DealsFilterPanel.tsx`
      - `src/components/dashboard/tasks/TaskFilterPanel.tsx`
      - `src/components/dashboard/meetings/MeetingFilterPanel.tsx`
      - `src/components/dashboard/calls/CallFilterPanel.tsx`
    - Quick-filter / chip builders (export reusable chip builders from `src/app/dashboard/*/page.tsx` or `src/features/*/filters.ts` + add optional Pool `Open Unassigned Pool` chip)
  - Retire / Replace:
    - `crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx` (retire legacy popover once all 7 tabs migrate to `FilterDrawer` + `QuickFilterBar`)
- **Implementation Changes:**
  1. **Filter Drawer Parity (`BUG-17`, `BUG-18`, `BUG-42`):**
     - Mount each module's `FilterPanel` inside `TeamsPoolSection` with `ownerOptions` (`myTeamData.members` + `Unassigned`) enabled.
     - Contacts uses `?contact_source=` (stop hijacking `?lead_source=`).
     - Calls uses real Call priorities (`Urgent`, `High`, `Medium`, `Low`) and `Wrong Number` outcome.
     - Lead Source uses `LEAD_SOURCE_VALUES` without phantom legacy renames.
     - Single-select values are never split on commas.
  2. **QuickFilterBar & Active Filter Chips (`BUG-23`, `BUG-39`):**
     - Render shared `QuickFilterBar` with each module's private quick presets PLUS non-destructive `⚡ Open Unassigned Pool` (toggles `is_unassigned=true` **without** wiping active filters, search, or kicking Admins to `"all"` teams!).
     - Render removable Active Filter Chips + `Clear All` button.
     - Pass exact `activeFilterCount` to `EntityActionBar` so the Filters button displays the numbered badge.
  3. **Saved Views on All 7 Tabs (`BUG-24`):**
     - Enable `PoolSectionSavedViews` for `leads`, `accounts`, `contacts`, `deals`, `tasks`, `meetings`, `calls` (`entity_type = "teamspace_pool_<tab>"`).
     - Persist the full module filter bag (excluding pagination and empty strings); perform an atomic `urlState.updateParams` + `setSearchDraft` sync on apply so there is no double-fetch race.
- **Acceptance Criteria & Verification:**
  - Opening Filters on any of the 7 Pool tabs opens the exact slide-over `FilterDrawer` used in the private module, plus the `Owner / Unassigned` section.
  - Quick filters, Active Filter Chips, `Filters (N)` count badge, and `Saved Views` work identically across all 7 tabs.

---

### Phase 3: Sales Modules Parity (Leads, Accounts, Contacts, Deals)
- **Objective:** Complete table, column, badge, sorting, drawer, and Kanban parity for the 4 sales modules in Teams Pool.
- **Dependencies:** Phases 0, 1, 2.
- **Files to Modify / Create:**
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolLeadsTab.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolLeadsKanban.tsx` *(New)*
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolAccountsTab.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolContactsTab.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsTab.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/deals/PoolDealsTable.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolDealsKanban.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolColumnTable.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/columns/usePoolColumns.ts`
  - `crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx`
  - `crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx`
  - Bonus shared fixes: `src/components/deals/DealsTable.tsx:745-776`, `src/components/accounts/AccountsTable.tsx`, `src/components/contacts/ContactsTable.tsx`
- **Implementation Changes:**
  1. **Pool Leads Kanban (`PoolLeadsKanban.tsx`):**
     - Implement Kanban view reusing `KanbanBoard.tsx` / `LeadKanbanColumn.tsx` / `LeadCard.tsx` backed by server Kanban summary & per-column pagination queries scoped to `team_id` / `pool_scope`, locking to a selected pipeline, gating drag by `isAdmin || accessDecisions[id]?.can_edit` (or opening governed update prompt when `approval_required`), passing `leadSlaHours`.
  2. **Pool Leads Table Fixes (`BUG-31`, `BUG-36`):**
     - Pass `state.orgSettings?.leadSlaHours` into `transformBackendLead`.
     - Fix `Stale: Xd` terminal status list to `["converted", "qualified", "lost_lead", "junk_lead", "not_qualified"]`.
     - Eliminate duplicate `Owner` / `Lead Owner` columns by rendering `PoolOwnerCell` inside `LeadList`'s `owner_name` slot (or excluding `owner_name` from `usePoolColumns` when `extraColumns.owner` is pinned).
     - Wire server-side sorting instead of un-clearable page-local `ai_priority_score` sort.
  3. **Pool Accounts & Contacts Fixes (`BUG-37`, `BUG-41`, `BUG-43`, `BUG-46`):**
     - Support `shiftKey` range selection (`PoolAccountsTab`, `PoolContactsTab`) and clear `selectedRecordIds` on page change.
     - Pass `onNavigateAccount` to `AccountDetailDrawer`; add `?id=` URL deep-linking across all Pool drawers.
     - Translate Contact column labels in `usePoolColumns.ts` using `tContacts("columns.*")` and fix `PoolContactsTab.tsx:59` i18n key.
     - Fix shared `AccountsTable`/`ContactsTable` missing `onMouseLeave={handleMouseUp}`, `0` employee/revenue formatting, and empty location `"-"`.
  4. **Pool Deals Table & Kanban Fixes (`BUG-15`, `BUG-16`, `BUG-21`, `BUG-22`, `BUG-25`, `BUG-45`):**
     - Add missing 4 columns (`win_probability`, `loss_reason`, `loss_notes`, `updated_at`) to `PoolDealsTable.tsx`.
     - Enable `"All Currencies"` in Pool Deals (`includeAllOption={true}`, default `"all"`).
     - Fix `PoolColumnTable` descending sort null/empty ordering (`aEmpty ? 1 : -1` BEFORE applying `direction`) and clear sort if sorted column is hidden.
     - Upgrade `PoolDealsKanban` to server-backed per-column queries (matching `DealsKanban.tsx`), filter inactive stages, show `win_probability%` + `CurrencySubtotals`, enforce `poolAccess`/`canLeadTeams` drag permissions, wire `ClosedLostModal` (loss reason) and Won confirmation + feedback pulse, send complete stage update payload, and fix `PoolDealsTab` summary banner to use `pagination.totalItems`.
     - Fix Private `DealsTable.tsx:745-776` operator precedence bug.

---

### Phase 4: Activity Modules Parity (Tasks, Meetings, Calls)
- **Objective:** Align Pool Tasks, Meetings, and Calls tables, Kanbans, drawers, creation modes, and inline/row actions with Private CRM.
- **Dependencies:** Phases 0, 1, 2.
- **Files to Modify:**
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolActivitiesTab.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolTasksTable.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolMeetingsTable.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/activities/PoolCallsTable.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolActivityKanbans.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/sections/PoolSectionColumnsMenu.tsx`
  - `crusource-crm-frontend/src/components/teamspace/pool/columns/usePoolColumnVisibility.ts`
  - `crusource-crm-frontend/src/components/teamspace/pool/PoolDrawersContainer.tsx`
  - `crusource-crm-frontend/src/components/teamspace/TeamspaceCreateDialog.tsx`
  - `crusource-crm-frontend/src/components/dashboard/meetings/table/MeetingStatusBadge.tsx`
  - `crusource-crm-frontend/src/components/teamspace/GovernedActionDialog.tsx`
- **Implementation Changes:**
  1. **Detail Drawers for Meetings & Calls (`BUG-14`):**
     - Replace raw `MeetingModal`/`CallModal` in `PoolDrawersContainer.tsx` with `MeetingDetailDrawer` and `CallDetailDrawer` (with `hideDelete`, `canEdit` derived from `isAdmin || poolAccess[id]?.can_edit`, and governed delete/edit callbacks). Remove unconditional refetch-on-close when no edit occurred.
  2. **Fix Kanban Drag & Server-Backed Boards (`BUG-12`, `BUG-21`, `BUG-27`):**
     - Make `onStatusDrop` return `false` (`PoolCallsKanban`) so `CallsKanban` never mutates `localCalls` optimistically when blocked.
     - Disable card dragging (`canDrag={false}`) on `MeetingsKanban` / `CallsKanban` / `TasksKanban` when the user lacks direct edit permission or status changes require approval — or route drops to `GovernedActionDialog` without triggering misleading `"Stage Down"` modals first.
     - Pass `searchQuery` to `PoolTasksKanban` and add search highlighting to `PoolTasksTable` columns.
     - Back Pool Activity Kanbans with server per-column queries (or show all matching columns cleanly without truncating at page 1).
  3. **Fix Table Cell, Sort & Menu Bugs (`BUG-26`, `BUG-40`, `BUG-43`):**
     - Fix `MeetingStatusBadge.tsx:42-56` read-only tooltip so `scheduled`/`in_progress` rows do NOT claim `"Cancelled meetings cannot be modified"`.
     - Deduplicate Meeting attendees by normalized email in `PoolMeetingsTable.tsx`.
     - Fix `PoolCallsTable` `callPriority` sort using severity rank (`Urgent: 4, High: 3, Medium: 2, Low: 1`) and fix `startOf()` to exclude formatted time-only `callStartTime`.
     - Pass `accessDecisions` and `isUnassigned` to `PoolAssigneeCell` in Tasks, Meetings, and Calls tables.
     - Add `"Reset to default view"` to Calls `PoolSectionColumnsMenu` checklist and enforce `minVisible: 1` fallback in `usePoolColumnVisibility.ts`.
  4. **Create Modes & `GovernedActionDialog` Dropdowns (`BUG-41`):**
     - Expose `Schedule Meeting` + `Log Meeting` (for Meetings) and `Schedule Call` + `Log Call` (`defaultMode="log"` / `"schedule"`) for Calls.
     - Add `<select>` options for Meeting (`status`, `meeting_type`) and Call (`outgoing_call_status`, `call_type`, `call_priority`, `call_result`, `call_purpose`) in `GovernedActionDialog.tsx`.

---

### Phase 5: Unified Export Flow & Governed Export Fixes
- **Objective:** Unify Teams Pool export onto the single-step `ExportOptionsModal` UX and shared server export formatter (`export_columns.py` / `export_file.py`), fixing all 422/403/50-row/formatting bugs across both Pool and Private approval fallbacks.
- **Dependencies:** Phases 0, 2.
- **Files to Modify:**
  - Backend:
    - `crusource-crm-backend/src/modules/teamspace/routes/teamspace_action_routes.py`
    - `crusource-crm-backend/src/modules/approvals/services/governed_actions.py`
    - `crusource-crm-backend/src/modules/teamspace/handlers/export_teamspace_handler.py` (deprecate/fix legacy `/export/pool`)
    - `crusource-crm-backend/src/modules/deals/handlers/export_deals_handler.py` (`BUG-46`)
  - Frontend:
    - `crusource-crm-frontend/src/components/teamspace/TeamspaceExportDialog.tsx`
    - `crusource-crm-frontend/src/components/teamspace/TeamsPoolSection.tsx`
    - `crusource-crm-frontend/src/services/teamspace/governedExportDownload.ts`
    - `crusource-crm-frontend/src/hooks/leads/useLeadBoardActions.ts`, `src/app/dashboard/accounts/page.tsx`, `src/app/dashboard/contacts/page.tsx` (`BUG-08`)
- **Implementation Changes:**
  1. **Fix 422, 403 & Legacy 50-Row Bugs (`BUG-06`, `BUG-07`, `BUG-08`, `BUG-09`):**
     - Fix `columnsByModule.deals` (or map via shared `export_columns.py` column keys).
     - Update `GET /teamspace/action-requests/{id}/download` permission dependency to allow the requester with `teams_pool` (when `export_mode="direct"`) OR `teams_requests`.
     - Replace `submitPersonal` export payload bugs in Private Leads/Accounts/Contacts (send valid DB columns, empty `data`, supported scope/filters).
     - Retire `admin_private` legacy `/teamspace/export/pool` bypass in `TeamsPoolSection.tsx` (route `admin_private` through standard `/export-downloads` or fixed export pipeline; also fix `limit=None`, `secondary_email`, `outgoing_call_status`, `call_duration_seconds` in `export_teamspace_handler.py` if retained for backwards compatibility).
  2. **1-Step Export UX & Conditional Business Reason (`BUG-13`, `BUG-44`):**
     - Render `ExportOptionsModal` directly (with optional/conditional Business Reason input inside `ExportOptionsModal` ONLY when `!isAdmin && export_mode === "approval_required"`, auto-supplying an audit reason for direct/admin exports).
     - Pass `allMatching: isSelectAllMatching` + `selectionFilters` cleanly; add `Export Selected (N)` to `EntityActionBar` selection bar.
     - Persist chosen `format` (`csv` | `xlsx`) on governed export requests so approval downloads honor it.
  3. **Formatter Parity:**
     - Reuse `export_columns.py` + `export_file.py` in `governed_actions.py` export rendering so governed exports produce UTF-8 BOM CSV and native `openpyxl` XLSX with localized human headers, user `timezone` + `date_format`, resolved foreign keys (`account_name`, `owner_name`, `parent_account_name`), and human enum labels.
     - Snapshot export rows/metadata at approval submission (or relax `version` 409 check on read-only export downloads).

---

### Phase 6: Unified Bulk Import Flow & Backend Import Parity
- **Objective:** Align Teams Pool bulk import UI, templates, expected fields, validation rules, duplicate handling, and error/skip telemetry with Private CRM for all 7 modules.
- **Dependencies:** Phase 0.
- **Files to Modify:**
  - Backend:
    - `crusource-crm-backend/src/modules/approvals/services/governed_actions.py`
    - `crusource-crm-backend/src/modules/approvals/services/import_record_preparation.py`
    - `crusource-crm-backend/src/modules/approvals/services/sales_import.py`
    - `crusource-crm-backend/src/modules/teamspace/schemas/action_execution_schemas.py`
  - Frontend:
    - `crusource-crm-frontend/src/components/teamspace/TeamspaceImportDialog.tsx`
    - `crusource-crm-frontend/src/lib/teamspace/importRecords.ts`
    - `crusource-crm-frontend/src/constants/bulkImportFields.constants.ts`
    - `crusource-crm-frontend/src/components/teamspace/pool/PoolModalsContainer.tsx` (remove dead import branches)
- **Implementation Changes:**
  1. **Fix Critical Accounts/Contacts/Meetings/Calls Bugs (`BUG-10`, `BUG-11`, `BUG-33`):**
     - Set `sales = ["leads", "accounts", "contacts", "deals"].includes(module)` in `TeamspaceImportDialog.tsx` and `importRecords.ts` so Accounts & Contacts allow Unassigned pool and manager `assign_mode`.
     - Fix Meetings import: support `parseDurationString`, auto-fix `end_time <= start_time`, populate `custom_type_label` (or use `MeetingImportItem` validation parity), allow `notes`, and make external attendees optional when host is present.
     - Fix Calls import: apply Private Calls defaults (`duration=15`, `priority="Medium"`, auto `call_result="Completed"`, phone lookup) so valid `"Completed"` rows don't 422.
  2. **Modal, Field & Sample CSV/XLSX Parity:**
     - Align Leads import with `BulkImportModal` grouped mapper (`EXPECTED_FIELD_GROUPS`) + XLSX template + `ImportStageMappingControls`.
     - Align Tasks, Calls, and Meetings sample CSV/XLSX templates with Private modals (full columns + realistic sample rows; remove stripped `Deal Owner` / `Created At` from `DEAL_SAMPLE_CSV` in Teamspace).
     - Make Business Reason conditional on `import_mode === "approval_required"`.
  3. **Partial Success, Duplicate Handling & Telemetry Parity (`BUG-33`):**
     - Support per-row duplicate skipping (`skipped_count`, `failed_count`, `skipped_records`, `errors`) in `governed_actions.py` (`serialize_import_receipt`) and surface them in `GenericBulkImportModal` / `BulkImportModal` with failed-row CSV/XLSX download.
     - Allow configurable/graceful Account/Contact linking (matching org-visible records or auto-creating where Private does) instead of failing 422 on non-exact-1 same-team links.
     - Chunk approval-required imports cleanly or process asynchronously to avoid single-request timeouts.

---

### Phase 7: Cleanup, i18n, Shared Table Polish & Graphify Update
- **Objective:** Remove dead code, eliminate hardcoded English strings and `$` currency icons, polish shared `AccountsTable`/`ContactsTable`, and update documentation/Graphify.
- **Dependencies:** Phases 1–6.
- **Files to Modify / Delete:**
  - Delete dead code in `PoolModalsContainer.tsx` (legacy `activeImportTab` / `deleteConfirmation` branches if unused) and retired `PoolFilters.tsx`.
  - Clean unused props (`formatDate` in `PoolLeadsTab`, `PoolDealsKanban`, `PoolTasksTable`, `PoolMeetingsTable`, `PoolCallsTable`; `searchQuery` highlighting in `PoolAccountsTab` & `PoolContactsTab`).
  - Move all hardcoded strings in `TeamspaceExportDialog`, `TeamspaceCreateDialog`, `TeamspaceImportDialog`, `TeamsPoolSection` (`aria-label="Team"`), `DealDueBadge.tsx`, and `LeadList.tsx` (`"Private"`) into `src/messages/{en,ar,nl}/teamspacePool.json` and module message files.
  - Replace hardcoded `$` icons/labels in Deals filters/cards with dynamic currency formatting (`formatCurrency`).
  - Run `graphify update .` in workspace root after code changes complete.

---

### Phase 8: Full Regression Verification & Test Suite Updates
- **Objective:** Update parity tests to match the unified UI/API architecture and verify full frontend & backend test suites pass with fresh evidence.
- **Verification Commands (Post-Implementation):**
  - Backend: `crusource-crm-backend/.venv/Scripts/python.exe -m pytest tests/test_teamspace_*.py` (plus export/import/activities suites)
  - Frontend TypeScript & Unit: `npm --prefix crusource-crm-frontend run typecheck` and `npm --prefix crusource-crm-frontend test`
  - Frontend Browser Parity Suites (Playwright): run all updated `test_teamspace_*_browser.mjs` suites listed in Section 6.

---

## 6. Existing Tests Impacted & New Tests Required

### Existing Frontend Tests Impacted (`crusource-crm-frontend/tests/`)

| Test File | Why It Will Require Updates |
|---|---|
| [test_teamspace_pool_tables_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_pool_tables_browser.mjs) | Line 193 clicks `"Grid"` on Pool Deals; clicks `"Table"`/`"Kanban"` text buttons inside `PoolViewModeBar`. Must update for Grid removal and top `EntityActionBar` icon toggle. |
| [test_teamspace_pool_parity_leads_contacts_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_pool_parity_leads_contacts_browser.mjs) | Lines 376–411 interact with `<select>` inside legacy `PoolFilterPanel` popover. Must update to open slide-over `FilterDrawer` + click `Apply Filters`. |
| [test_teamspace_pool_parity_other_sections_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_pool_parity_other_sections_browser.mjs) | Lines 508–511 use legacy `<select>` filter; lines 559, 576 click `"Kanban"`/`"Table"` in `PoolViewModeBar`; asserts read-only activity badges. Must update for `FilterDrawer`, `EntityActionBar` toggle, and updated `MeetingStatusBadge` tooltip. |
| [test_teamspace_pool_scope_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_pool_scope_browser.mjs) | Verify mobile team-scope visibility, non-destructive `Open Unassigned Pool`, and error/403 rendering. |
| [test_teamspace_governance_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_governance_browser.mjs) | Update for conditional Business Reason, `hideDelete` in Account/Contact/Lead drawers, and `allMatching` `bulk_update`. |
| [test_teamspace_drawer_and_history_gating_browser.mjs](../../../crusource-crm-frontend/tests/test_teamspace_drawer_and_history_gating_browser.mjs) | Update Meetings & Calls click assertions from raw `MeetingModal`/`CallModal` to `MeetingDetailDrawer`/`CallDetailDrawer`. |
| [test_teamspace_import_records.ts](../../../crusource-crm-frontend/tests/test_teamspace_import_records.ts), [test_teamspace_components.tsx](../../../crusource-crm-frontend/tests/test_teamspace_components.tsx), [test_teamspace_url.ts](../../../crusource-crm-frontend/tests/test_teamspace_url.ts), [test_teamspace_pool_table_model.ts](../../../crusource-crm-frontend/tests/test_teamspace_pool_table_model.ts), [test_unified_sales_teamspace_browser.mjs](../../../crusource-crm-frontend/tests/test_unified_sales_teamspace_browser.mjs) | Update unit/component/E2E assertions for `PoolTabBar` (no counts), expanded `useTeamspaceUrlState` params, `PoolColumnTable` null-last descending sort, Accounts/Contacts `sales` import flag, and Meetings/Calls import transforms. |

### New Tests to Add
- **Backend (`crusource-crm-backend/tests/`):**
  - `test_teamspace_pool_security_and_fls.py`: Verify 403 without `teams_pool` on `/deals`, `/tasks`, `/meetings`, `/calls`; verify FLS filter/search blocking on all 7 endpoints; verify `is_unassigned=False` + `owner_id` and deterministic `id` pagination tie-breaking.
  - `test_teamspace_pool_filters_and_dates.py`: Verify `this_month` (Tasks/Meetings), Calls `call_start_time` date filtering, timezone-aware boundaries, Leads `include_converted`, Deals case-insensitive stage filter, and wildcard-escaped `ILIKE`.
  - `test_teamspace_export_import_parity.py`: Verify Deals governed export defaults pass 200 (BOM CSV + XLSX), `teams_pool` direct download permission, fixed `admin_private`/export paths, Meetings `"Other"`/`custom_type_label` + duration import, Calls completion defaults, and `skipped_count`/`errors` telemetry.
- **Frontend (`crusource-crm-frontend/tests/`):**
  - `test_teamspace_pool_leads_kanban_browser.mjs`: Verify Pool Leads Kanban view toggle, pipeline locking, drag governance, and SLA badges.
  - `test_teamspace_pool_export_import_browser.mjs`: Verify 1-step `ExportOptionsModal`, `Select all matching` export/bulk-update, and Accounts/Contacts/Meetings/Calls import flows.

---

## 7. Open Product & Governance Decisions for Sign-Off

Before starting implementation, please confirm these 5 product decisions:

| # | Decision Area | Recommended Option | Alternative |
|---|---|---|---|
| 1 | **Business Reason on Direct / Admin Actions** (Export, Import, Create) | **Require Business Reason ONLY when `*_mode === "approval_required"`** (and auto-supply an audit reason or omit for direct/admin actions so UX matches Private CRM). | Keep Business Reason mandatory on all Teamspace Export/Import/Create actions even for admins. |
| 2 | **Default Pipeline in Pool Leads & Deals** | **Default to the organization's Default Pipeline** (matching Private Leads & Deals), keeping `"All Pipelines"` selectable in Table view and locking to a specific pipeline in Kanban view. | Keep `"All Pipelines"` as the initial Table default and only auto-select the default pipeline when switching to Kanban. |
| 3 | **Kanban Drag-and-Drop under `approval_required`** | Allow direct drag-and-drop when `isAdmin \|\| accessDecisions[id]?.can_edit` (and direct edit allowed); **disable drag** on view-only rows; open a governed update dialog on drop if `can_request` (no misleading Stage-Down modal first). | Disable drag-and-drop completely in Teams Pool Kanban and force edits exclusively through row selection + `"Request record update"`. |
| 4 | **5 Top KPI Cards on Tasks / Meetings / Calls** | **Omit the 5 top KPI summary cards** in Teams Pool (Teams Pool already has `PoolTabBar`, Team Scope controls, and the dedicated `Teams Dashboard` route), relying on `QuickFilterBar` presets (`Overdue`, `Due Today`, `Upcoming`, `Completed`, `Scheduled`). | Render the 5 KPI summary cards inside each Activity tab in Teams Pool too (adds vertical height under `PoolTabBar`). |
| 5 | **Bonus Private Bugs Found During Audit** (`DealsTable.tsx:745-776` ternary bug, `export_deals_handler.py:82` FLS key, `AccountsTable`/`ContactsTable` `onMouseLeave`) | **Include these fixes** alongside Phase 3 / Phase 5 since they share components/files with Teams Pool. | Track them in a separate follow-up PR outside the Teams Pool scope. |
