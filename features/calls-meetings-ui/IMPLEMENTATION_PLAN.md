# Calls & Meetings UI Consistency, Drawer Separation & Field Streamlining Plan

> **Owner repositories:** `crusource-crm-frontend/` (primary), `crusource-crm-docs/` (documentation)
> **Backend impact:** None expected — `crusource-crm-backend/src/modules/calls/` already supports `outgoing_call_status = "Scheduled" | "Completed" | "Cancelled"`, optional `call_purpose`, `reminder="None"`, `follow_up_date`, `tags`, and strict completion validation (`validate_call_completion`) when status is `Completed`.

---

## 1. Verified Problems & Root Causes

| # | Issue Reported | Verified Root Cause in Codebase |
|---|---|---|
| 1 | **Calls & Meetings toolbars look inconsistent with the rest of the CRM** | All other CRM list/board pages (`Leads` via `LeadBoardActionBar.tsx`, `TasksTable.tsx`, `ContactsPage`, `AccountsPage`, `DealsPage`, `TeamsPoolSection.tsx`) render `<EntityActionBar />`. `CallsHeader.tsx` and `MeetingToolbar.tsx` implement custom toolbars with mismatched button heights (`h-8 size="sm"` vs `py-2`), inconsistent borders (`border-slate-200` vs `border-outline`), mixed icons (Lucide `Filter`/`List`/`Kanban` vs `material-symbols-outlined` `format_list_bulleted`/`view_kanban`/`filter_list`), and duplicate selection banners (`CallsTable.tsx:557` + `CallsHeader.tsx:66`). |
| 2 | **Search bar visually overlaps `Saved Views`** | Both `CallsHeader.tsx:185` and `MeetingToolbar.tsx:181` wrap `<ModuleSearchInput width="w-full @2xl/toolbar:w-44 @5xl/toolbar:w-52 @7xl/toolbar:w-64" />` inside `<div className="min-w-[110px] flex-1 sm:flex-initial max-w-[240px]">`. On `@7xl/toolbar`, Tailwind sets the inner input to `w-64` (`256px`), overflowing its `max-w-[240px]` wrapper right onto `Saved Views`. (`EntityActionBar.tsx:181` uses `max-w-[260px]`, and even that can squeeze if inner container-query widths exceed wrapper width.) |
| 3 | **`Export` & `Import` hidden inside `... Actions` only in Calls & Meetings** | `CallsHeader.tsx:281-322` and `MeetingToolbar.tsx:227-294` hide `Export` and `Import` inside a desktop `Actions` dropdown menu at all breakpoints, whereas `EntityActionBar` exposes `Export` and `Import` directly as bordered buttons (`hidden md:flex`) with an overflow menu only on small screens (`md:hidden`). |
| 4 | **`Log Call` is combined inside the `Add/Schedule Call` drawer** | `Meetings` separates `Schedule Meeting` (`MeetingModal`) from `Log Meeting` (`LogMeetingModal`, triggered from a dedicated `Log Meeting` button in `MeetingToolbar`) and reserves `MeetingMinutesModal` for completing an existing meeting. Meanwhile, `CallsHeader` only renders a single `+ Add a call` button (`CallsTable.tsx:479` had `handleLogNewCall` unwired!), `CallForm.tsx:46-73` stuffs a `Schedule Call` vs `Log a Call` toggle inside `CallModal`, and `CallLogModal.tsx:167` only works when an existing `call` row is passed (`if (!isOpen || !call) return null`). |
| 5 | **Schedule Call drawer asks too many irrelevant / premature fields** | Creating an upcoming call in `CallModal` renders ~15 fields at once: (a) a mode toggle, (b) a padlocked disabled `Call Status = Scheduled` select, (c) a disabled `Account — Not applicable for leads` input when `Lead` is selected, (d) single `<input type="datetime-local">` instead of separate Date -> Start Time fields, (e) post-call `Follow-up Date`, (f) a 3-field `Create follow-up task` card that only makes sense after a call occurs, plus (g) always-expanded `Call Direction`, `Call Purpose`, `Reminder`, `Google Calendar Sync`, and `Tags`. |

---

## 2. Target UX & Architecture Design

### Phase 1 — Standardize Calls & Meetings Toolbars on `EntityActionBar`

#### 1.1 Harden `EntityActionBar` (`src/components/shared/EntityActionBar.tsx`)
- **Search overlap mathematical fix:** Replace the `max-w-[260px]` outer wrapper + separate inner `@2xl/@5xl/@7xl` widths with matching wrapper sizing and `width="w-full"` on `<ModuleSearchInput />`:
  - Wrapper: `className="w-full min-w-[140px] flex-1 sm:flex-initial sm:w-44 @5xl/toolbar:w-52 @7xl/toolbar:w-64"`
  - Inner `<ModuleSearchInput width="w-full" ... />`
  - Because `ModuleSearchInput` always fills `100%` of its flex item, it can never paint outside its flex box onto `Saved Views` at any viewport width.
- **Add clean non-breaking extension slots to `EntityActionBarProps`:**
  - `toolbarSecondaryActions?: React.ReactNode` — rendered right before the primary `onAddClick` button (used for `Log Call` in Calls and `Google Calendar` indicator + `Log Meeting` in Meetings).
  - Keep existing props untouched so `Leads`, `Deals`, `Contacts`, `Accounts`, `Tasks`, and `Teamspace` continue working identically.

#### 1.2 Migrate `CallsHeader.tsx` & `CallsTable.tsx` to `EntityActionBar`
- **`CallsHeader.tsx`:** Wrap `<EntityActionBar />` directly instead of duplicating layout markup:
  - View toggle (`List` | `Kanban`), Search (`Search calls...`), `<SavedViewsDropdown entityType="calls" />`, `<CallFilterPanel />`, `<ColumnsDropdown />`, direct desktop `Export` & `Import` buttons (`hidden md:flex` + `md:hidden` overflow), **`Log Call`** secondary button (`toolbarSecondaryActions`, Material icon `assignment_turned_in` / outline styling matching `Log Meeting`), and primary **`Schedule Call`** orange CTA (`addLabel={t("header.scheduleCall")}`, fallback clear phrasing).
  - Uses `EntityActionBar`'s unified `BulkSelectionBanner` executive bar (`selectedCount`, `pageCount`, `totalCount`, `isSelectAllMatching`, `onSelectAllMatching`, `onClearSelection`, `onExportSelected` if needed, `onDeleteSelected` -> `"Delete (N)"`).
  - **Clean up `CallsTable.tsx`:** Remove the redundant second `<BulkSelectionBanner>` at `CallsTable.tsx:557` and pass `pageCount`, `totalCount`, `isSelectAllMatching`, `onSelectAllMatching` directly into `CallsHeader` -> `EntityActionBar`.

#### 1.3 Migrate `MeetingToolbar.tsx` & `MeetingsTable.tsx` to `EntityActionBar`
- **`MeetingToolbar.tsx`:** Wrap `<EntityActionBar />` directly:
  - View toggle (`List` | `Kanban`), Search (`Search meetings...`), `<SavedViewsDropdown entityType="meetings" />`, `<MeetingFilterPanel />`, optional `<ColumnsDropdown />` (using `DEFAULT_MEETING_COLUMNS` / `ALL_MEETING_COLUMNS` in `meetingColumns.tsx`), direct desktop `Export` & `Import` buttons (`hidden md:flex` + `md:hidden` overflow).
  - Replace the bespoke desktop `... Actions` menu (which previously only existed to hide Export, Import, and Google Calendar):
    - Export & Import are now direct CRM-standard buttons.
    - `Google Calendar` status/connect moves to a clean compact toolbar pill button in `toolbarSecondaryActions` (`border-outline bg-white py-2 px-3 rounded-lg text-[13px] font-semibold`, showing green dot when connected or `Connect Calendar` linking to `/dashboard/settings`).
    - `Log Meeting` renders cleanly in `toolbarSecondaryActions` with unified CRM height/radius/typography (`py-2 px-3.5 rounded-lg text-[13px] font-semibold`) beside primary `+ Schedule Meeting`.
  - Unifies `MeetingsTable` bulk selection bar to the same `BulkSelectionBanner` inside `EntityActionBar`.

#### 1.4 Responsive KPI Strip Parity
- `CallsKpiCards.tsx` & `MeetingKPIs.tsx` & `TasksKpiCards.tsx`: Keep identical card padding/typography (`p-3 rounded-xl`, `text-[10px]`, `text-xl`), using `grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-4` so 5 cards never squash below `lg`.

---

### Phase 2 — Separate "Log Call" Drawer from "Schedule Call" Drawer

#### 2.1 Clear 3-Drawer Model Matching `Meetings`
| Purpose | Meetings Module | Calls Module (Target) |
|---|---|---|
| Schedule upcoming / Edit call | `MeetingModal` (`+ Schedule Meeting`) | `CallModal` (`+ Schedule Call` + Edit call) |
| Standalone Log completed activity | `LogMeetingModal` (`Log Meeting`) | **`LogCallModal` (`Log Call`)** *(new right-drawer)* |
| Complete an existing scheduled activity | `MeetingMinutesModal` | `CallLogModal` *(preserved for scheduled -> completed transitions & existing test contract)* |

#### 2.2 Dedicated `LogCallModal` (`src/components/dashboard/calls/LogCallModalNew` -> `LogCallDrawerModal.tsx` or `modal/LogCallModal.tsx`) + `useLogCallForm` hook
- Right-hand slide-over drawer (`w-[840px] max-w-[calc(100%-1.5rem)]`, matching `LogMeetingModal` & `CallModal`).
- Header: Phone/Clipboard icon badge, `"Log a Call"` title + `"COMPLETED"` badge, subtitle, close `X` button.
- Focused fields exclusively for recording a call that took place:
  1. **Recipient & Phone**: `Call For` (`Contact` | `Lead` + `TargetSearchInput`), `Phone Number` (`PhoneInputWithCountry`), auto-linked Account chip (only when Contact has Account), `Call Owner` (`ActivityAssigneeSelect`).
  2. **Subject & Direction**: `Subject` (`required`, auto-suggested `"Call with {name}"`), `Direction` segmented toggle (`Outbound` | `Inbound`).
  3. **Call Date, Time & Actual Duration**:
     - **Step 1: Call Date** (`type="date"`, defaults to today)
     - **Step 2: Call Time** (`type="time"`, defaults to 1 hour earlier in workspace timezone via `useFormatting`)
     - **Actual Duration**: `mins` + `secs` inputs with quick presets (`5m`, `15m`, `30m`, `45m`), validating total duration > 0 per backend `validate_call_completion`.
  4. **Call Outcome & Summary (`required` by backend)**:
     - Quick outcome pills (`Connected`, `Interested`, `Left Voicemail`, `No Answer`, `Busy`, `Wrong Number`, `Follow-up Required`, `Not Interested`, `Other` + custom input).
     - `Call Notes / Summary` textarea (`required`, `maxLength=2000`).
  5. **Follow-up & Categorization (Clean Optional Row + Optional Task)**:
     - `Priority` (`Medium` default), `Purpose`, `Follow-up Date`, `Tags`.
     - Toggleable `Create Follow-up Task` (Subject, Due Date, Priority) wired to `useTasksMutations().createTask` after `createCall` succeeds (`outgoingCallStatus: "Completed"`).
- **Wiring across Calls & Cross-Entity Drawers**:
  - `CallsTable.tsx`: Clicking `Log Call` in `CallsHeader` opens `<LogCallModal />` (never opens `CallModal` in log mode).
  - `EntityActivitiesModals.tsx` & `LeadDetailDrawer.tsx` / `ActivitiesTab.tsx`: Support `isLogCallOpen` / `LogCall` alongside `LogMeeting` where quick actions already distinguish `Meeting` vs `LogMeeting`.
  - Remove unused `callModalMode` toggle state from `CallsTable.tsx`.

---

### Phase 3 — Declutter & Streamline "Schedule Call" (`CallModal` / `CallForm`)

#### 3.1 Field-by-Field Streamlining in `useCallForm`, `CallForm`, `CallInformationSection`, `CallScheduleSection`, `CallDescriptionSection`
- **Removed from Create/Schedule mode (no longer asked prematurely):**
  1. **Remove `Schedule call` / `Log a call` internal pill toggle** from `CallForm.tsx` (Create mode is always scheduling an upcoming call; `Log Call` is its own drawer).
  2. **Hide disabled `Call Status` (`Scheduled` + padlock)** when `!isEditMode`. **Keep editable `Call Status` (and conditional `Call Outcome`) ONLY when `isEditMode === true`** so editing an existing call to `Completed` or `Cancelled` works seamlessly and preserves `test_calls_remediation_browser.mjs`.
  3. **Remove disabled `Account — Not applicable for leads` input box** when `callForType === "Lead"`. Show a compact read-only auto-linked Account indicator (or input) only when `Contact` is selected and linked/editable.
  4. **Remove `Follow-up Date` and the 3-field `Automated Follow-up Task` card** from Schedule Create mode (these belong post-call in `LogCallModal` and `CallLogModal`; in Edit mode only show `followUpDate` if `outgoingCallStatus === "Completed"` or `initialCall.followUpDate` is already set).
- **Split `Call Date & Time` into Step 1: Date + Step 2: Time**:
  - Replace `<input type="datetime-local">` in `CallScheduleSection.tsx` with separate **Step 1: Call Date** (`type="date"`) and **Step 2: Start Time** (`type="time"`), formatted & parsed in workspace timezone (`useFormatting`), preventing browser `datetime-local` reset bugs and matching `MeetingScheduleFields.tsx`.
  - Default new scheduled call time sensibly (e.g., next rounded 30-min slot or current hour+1 via helper) without resetting edited dates.
- **Primary vs Collapsible "More Options" Structure in Schedule Call**:
  - **Always visible (clean 6 essential inputs):**
    1. `Subject` (`required`, auto-suggested on contact/lead select)
    2. `Call For` (`Contact` | `Lead` + search) & `Phone Number`
    3. `Schedule`: **Call Date** (`Step 1`) + **Start Time** (`Step 2`) + `Planned Duration` pills (`15m`, `30m`, `45m`, `60m`, `Custom`)
    4. `Priority` (`Medium` default) & `Call Owner`
    5. `Notes / Preparation Agenda` (optional textarea)
    6. `Add to Google Calendar` toggle (only shown when `!isEditMode && googleConnected`, so unconnected users don't see noisy dead options — or concise hint matching Meetings)
  - **Collapsed by default under `"Additional options (Direction, Purpose, Reminder, Tags)"`** *(auto-expanded in Edit Mode whenever an existing call has non-default `callType !== "Outbound"`, `callPurpose`, `reminder !== "None"`, or `tags.length > 0`)*:
    - `Direction` (`Outbound` default / `Inbound`)
    - `Call Purpose`
    - `Reminder` (`None`, `5m`, `15m`, `30m`, `1h`, `Custom`)
    - `Tags`

---

### Phase 4 — Localization, Documentation & Automated Verification

1. **Localization (`en`, `nl`, `ar`):**
   - Update `src/messages/{en,nl,ar}/activities/calls.json` and `meetings.json` with keys for `header.scheduleCall`, `header.logCall`, `form.callDate`, `form.callTime`, `form.moreOptions`, `logCall.*`, `toolbar.connectCalendar` / `toolbar.calendarSynced`, `columns.*`.
   - Zero raw `.toLocaleDateString` / `.toLocaleTimeString` calls (all via `useFormatting`).
2. **Automated Tests:**
   - **Browser regression tests (Playwright via `browserFixture.mjs`):**
     - New `tests/test_calls_meetings_ui_browser.mjs`: verifies `CallsTable` and `MeetingsTable` side-by-side layout using `<EntityActionBar>`:
       - Assert search input right edge (`rect.right`) NEVER overlaps `Saved Views` left edge (`savedViewsRect.left`) at `1024px`, `1280px`, and `1440px` viewports!
       - Assert `Export` and `Import` buttons are directly visible in both Calls and Meetings toolbars (not buried inside `... Actions`).
       - Assert Calls toolbar has separate `Log Call` and `Schedule Call` buttons.
       - Assert clicking `Schedule Call` opens `CallModal` without mode toggle, without disabled `Scheduled` status lock, without `Not applicable for leads` Account box when `Lead` is selected, without `Automated follow-up task`, and WITH separate `Date` and `Time` inputs + collapsible `Additional options`.
       - Assert clicking `Log Call` opens `LogCallModal` and validates outcome + duration > 0 + notes before calling `POST /calls` with `outgoing_call_status: "Completed"`.
   - Re-run all existing Calls & Meetings unit + browser tests (`test_calls_remediation_browser.mjs`, `test_calls_notes_browser.mjs`, `test_calls_pagination_browser.mjs`, `test_calls_bulk_jobs_browser.mjs`, `test_calls_service.ts`, `test_meetings_filters.ts`, `test_meetings_timezone.ts`, `test_meeting_schedule_context_browser.mjs`) plus `npx.cmd tsc --noEmit`, `npm.cmd run lint`, `npm.cmd run test`, `npm.cmd run test:localization`.

---

## 3. Double-Pass Plan Audit & Review Log

### Audit Pass 1 — Backwards Compatibility & Existing Test Contracts
- **Finding 1.1 (`test_calls_remediation_browser.mjs:210-234`):** The browser test opens `<CallOverviewTab callToEdit={...} />`, selects `Completed` in Status dropdown, clicks Outcome `"Interested"`, clicks `"Custom"`, fills `5`, verifies Submit is disabled until textarea notes are filled, and clicks `Save changes`.
  - *Resolution built into plan:* Hiding `Call Status` ONLY applies when `!isEditMode`. In Edit Mode (`callToEdit != null`), `Call Status` stays interactive and triggers `Outcome` + required notes just as before. Also `CallLogModal` remains intact for completing an existing call.
- **Finding 1.2 (`test_calls_remediation_browser.mjs:96-104`):** Bulk deletion test clicks `"Select all calls"` -> `"Delete (2)"` -> `"Delete 2 calls"`.
  - *Resolution built into plan:* `EntityActionBar`'s `BulkSelectionBanner` renders `Delete (2)`, and `useConfirmModal` uses `header.deleteSelectedTitle` (`Delete 2 calls`). Notice `EntityActionBar` `onDeleteSelected` triggers `CallsTable`'s `handleBulkDelete` which invokes `confirm(...)` with `Delete 2 calls` — 100% preserved!
- **Finding 1.3 (`CallDetailDrawer.tsx:663`, `Leads`, `Teamspace` callers of `CallModal`):** `DashboardModals`, `PoolDrawersContainer`, `TeamspaceCreateDialog`, `LeadBoardModals`, `EntityActivitiesModals` render `<CallModal ... />`.
  - *Resolution built into plan:* Keeping `CallModal`'s external props (`isOpen`, `onClose`, `callToEdit`, `initialCallFor`, `initialRelatedTo`, `onSave`, `isSaving`) compatible guarantees zero breaking changes for external callers while optional `defaultMode` can remain deprecated or default to `"schedule"`.

### Audit Pass 2 — UI, Accessibility, Timezone, RBAC & Data Integrity
- **Finding 2.1 (Search Bar Width at Intermediate Breakpoints):** In `@4xl/toolbar:flex-row`, when left side has Title + Subtitle AND right side has `List|Kanban`, `Search`, `Saved Views`, `Filters`, `Columns`, `Export`, `Import`, `Log Call`, `Schedule Call`, buttons already use `flex-wrap items-center`. Adding `Log Call` increases right-side items by 1 button, so allowing clean `flex-wrap` and keeping the `ModuleSearchInput` width locked to its flex container (`w-full` inside `sm:w-40 @5xl/toolbar:w-48 @7xl/toolbar:w-56` or `w-44`/`w-52`/`w-64`) ensures clean wrapping onto row 2 at narrow widths with **zero collision/overlap**.
- **Finding 2.2 (Split Date & Time State Sync in `useCallForm`):** Unlike simple `datetime-local` strings, if the user clears Time or Date independently, partial state (`"2026-11-16T"` or `"T09:30"`) must not throw `Invalid time value` in `formatDateTimeLocal` or `parseDateTimeLocal`.
  - *Resolution built into plan:* Store `callStartDate: string` (`YYYY-MM-DD`) and `callStartTime: string` (`HH:mm`) cleanly in `useCallForm` (and `useLogCallForm`), combine `${callStartDate}T${callStartTime}` only when both parts are present before calling `parseDateTimeLocal(...)`, and validate both parts in `isFormValid` / Zod validation.
- **Finding 2.3 (Backend Payload Parity When Optional Fields Are Hidden/Collapsed):** `callCreateSchema` (`crmSchemas.ts`) requires `subject`, `callForType`, `callForName`, `callForId`, `callPriority`. `call_type` defaults `"Outbound"`, `reminder` defaults `"None"`, `callDurationMinutes` defaults `15`.
  - *Resolution built into plan:* Hidden fields keep clean defaults (`callType: "Outbound"`, `outgoingCallStatus: "Scheduled"`, `reminderPreset: "None"`, `callPriority: "Medium"`, `callDurationMinutes: 15`) so `buildPayload()` always satisfies both `callCreateSchema` and FastAPI `CallCreate`.
- **Finding 2.4 (`Meetings` Export + `ColumnsDropdown` Consistency):** `MeetingsTable.tsx:556` passes `visibleColumnsCount={columns.length}` to `ExportOptionsModal`, and `handleExport` currently uses `ALL_MEETING_EXPORT_COLUMNS`. If we keep `ColumnsDropdown` in `MeetingsTable` with `DEFAULT_MEETING_COLUMNS` matching current visible columns (all visible by default) and wire `visibleColumns` into `MeetingsListView` + `ExportOptionsModal`, existing tests (`useMeetingsPage`) aren't disturbed and Meetings gains parity with Calls & Tasks.
