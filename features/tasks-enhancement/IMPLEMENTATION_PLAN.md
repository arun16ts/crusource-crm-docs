# Tasks Section — Bug Fixes, Hierarchy/Permission Hardening & UX Enhancement Plan

- **Date:** 2026-11-23
- **Status:** Draft / Ready for Implementation
- **Repositories in Scope:**
  - `crusource-crm-frontend/` (Next.js App Router, React, Redux, TanStack Query, Tailwind)
  - `crusource-crm-backend/` (FastAPI, SQLAlchemy, Pydantic, CQRS handlers)
- **Related Repositories:** `crusource-crm-docs/` (this plan)

---

## 1. Goals & Scope

This plan consolidates all verified bugs in the **Tasks** module (including hierarchy view, profiles, permissions, and Teamspace isolation) together with five product/UX changes requested after testing:

1. **Search Result Highlighting:** Highlight matching search terms in the Tasks table and Kanban cards using `<HighlightMatch>`, matching the Leads section.
2. **Remove Tags:** Remove passive `tag` / `tags` UI, import/export columns, and API payload fields (preserving the `tasks.tag` database column to avoid destructive migrations on existing data).
3. **Support Deals in Create/Edit Task & Remove Dead `Account` `related_to` Code:**
   - Allow creating and editing tasks linked to **Contact**, **Lead**, or **Deal**.
   - Auto-fill and persist `account_id` + `accountName` when a **Contact** or **Deal** with an associated Account is selected.
   - Remove dead code that treats `Account` as a `related_to_type` target in task creation/editing, while **keeping `Account` in Task Filters** so users can filter tasks by Account (matching `Task.account_id IS NOT NULL`, plus legacy `related_to_type == "Account"` rows).
4. **Remove Repeat Task:** Remove the non-functional `repeat` UI, `isRecurring` filter, import/export columns, and API payload fields (preserving `tasks.repeat` column in DB).
5. **Clean Up Auto-Linked Account UI:** Remove the redundant `"Auto-linked to contact"` label and its lock icon above the Account input in `TaskForm.tsx`, keeping only the lock icon inside the disabled input when auto-filled.
6. **Fix All Verified Bugs:**
   - Team Task Lead & Deal search leaking private/cross-team records (`linkable_for_create` + `team_id`).
   - Due Date (and Reminder) allowing past dates on creation.
   - Admin outside the selected team appearing in the Task Owner dropdown and failing with `422`.
   - Incomplete hierarchy filtering (`hierarchyLevel`, `reportsTo`, `TeamMembership`) in `ActivityAssigneeSelect` and `task_assignment_policy.py`.
   - Read-only profiles seeing the **Edit** action in `TasksTable` and `TaskModal`.
   - Editing a Deal-linked task silently corrupting `relatedTo.type` to `"Contact"`.
   - Minor mismatches: `TaskDetails.tsx` `"Medium"` vs `"Normal"` priority badge, and `delete_all_matching_tasks` passing `Task` instead of `"tasks"` to `require_bulk_targets`.

---

## 2. Detailed Changes by Workstream

### Workstream A: Teamspace-Scoped Target Search (`linkable_for_create` & `team_id` for Leads and Deals)

**Problem:**
- `TargetSearchInput.tsx` passes `linkableOptions` (`{ linkableForCreate: true, teamId: effectiveTeamId }`) to `useContactSearch` and `useAccountSearch`, but **not** to `useLeadSearch` or `useDealSearch`.
- Backend `GET /api/v1/leads` and `GET /api/v1/deals` do not support `linkable_for_create` or `team_id`, unlike `/contacts` and `/accounts` which use `scoped_linkable_query` (`src/shared/auth/record_links.py`).
- Result: In Team Task creation, `GET /leads` returns the Admin's private leads (`record_team_id = None`), and saving fails with `403: Related record is unavailable in this record's organization and team` from `require_record_links`.

**Backend Changes (`crusource-crm-backend/`):**
1. **`src/modules/leads/queries/lead_queries.py` & `src/modules/leads/routes/leads_routes.py`:**
   - Add `linkable_for_create: bool = False` and `team_id: Optional[UUID] = None` to `LeadFilterParams` (matching `contact_queries.py` / `account_queries.py`).
2. **`src/modules/leads/repositories/leads_repository.py`:**
   - In `get_leads_for_scope`, when `getattr(filters, "linkable_for_create", False)` or `getattr(filters, "team_id", None) is not None`, use `scoped_linkable_query(db, Lead, scope, team_id=filters.team_id)` as the base query instead of `apply_scope(db.query(Lead), Lead, scope)`.
3. **`src/modules/deals/queries/deal_queries.py` & `src/modules/deals/routes/deals_routes.py`:**
   - Add `linkable_for_create: bool = False` and `team_id: Optional[UUID] = None` to `DealFilterParams`.
4. **`src/modules/deals/repositories/deals_repository.py`:**
   - In `get_deals_for_scope`, when `getattr(filters, "linkable_for_create", False)` or `getattr(filters, "team_id", None) is not None`, use `scoped_linkable_query(db, Deal, scope, team_id=filters.team_id)` as the base query (preserving Deal Team collaboration visibility if applicable via `scoped_linkable_query` or `apply_record_team_scope`).
5. **Cross-module check (`Calls`, `Meetings`):**
   - `LogCallModal` / `CallInformationSection` and `MeetingModal` also use `TargetSearchInput` with `linkableForCreate`. Adding `linkable_for_create` + `team_id` to `/leads` and `/deals` automatically fixes Lead/Deal target search in Calls and Meetings too.

**Frontend Changes (`crusource-crm-frontend/`):**
1. **`src/hooks/useContactLeadSearch.ts`:**
   - Update `useLeadSearch(query: string, options?: LinkableEntitySearchOptions)` to accept `options`, include `linkableForCreate` and `teamId` in the React Query `queryKey`, and append `buildLinkableQuerySuffix(options)` to `/leads`.
   - Update `useDealSearch(query: string, options?: LinkableEntitySearchOptions)` similarly for `/deals`.
   - Verify `useDealSearch` returns `accountId` and `accountName` (already mapped from `d.account_id` and `d.account_name` at lines 210–211).
2. **`src/components/shared/TargetSearchInput.tsx`:**
   - Pass `linkableOptions` to `useLeadSearch` and `useDealSearch` (lines 57–64), matching `useContactSearch` and `useAccountSearch`.

---

### Workstream B: Deals Support, `account_id` Persistence, & Dead `Account` `related_to` Cleanup

**Problem:**
- `TaskForm.tsx`, `useTaskForm.ts`, `crmSchemas.ts`, and `EntityActivitiesModals.tsx` only allow `Contact | Lead` for `targetType`.
- Editing a Deal-linked task coerces `targetType` to `"Contact"` in `useTaskForm.ts` line 118, causing `400 Invalid related entity` on save.
- `useTaskForm.ts` and `tasks.service.ts` never store or send `account_id` (only `accountName` in UI state), so `Task.account_id` stays `NULL` even when a Contact with an Account is selected.
- `TaskFilterPanel` includes `Account` in `RELATED_TO_VALUES`, but `task_page_repository.py` checks `Task.related_to_type == "account"` instead of `Task.account_id.isnot(None)`.

**Frontend Changes (`crusource-crm-frontend/`):**
1. **`src/hooks/useTaskForm.ts`:**
   - Widen `targetType` in `TaskFormState` and `initialTarget` to `"Contact" | "Lead" | "Deal"`.
   - Add `accountId: string | null` to `TaskFormState`.
   - When initializing from `initialTask`: preserve `Deal` (`initialTask.relatedTo?.type === "Deal" ? "Deal" : initialTask.relatedTo?.type === "Lead" ? "Lead" : "Contact"`), and hydrate `accountId: initialTask.accountId ?? null` and `accountName: initialTask.accountName ?? ""`.
   - In `handleTargetSelect(item)`: when `prev.targetType === "Contact" || prev.targetType === "Deal"`, set `accountId: item.accountId || null`, `accountName: item.accountName || ""`, and `isAccountAutoFilled: Boolean(item.accountName)`. When cleared or `"Lead"`, reset `accountId: null`, `accountName: ""`, `isAccountAutoFilled: false`.
   - In `buildPayload()`: include `accountId: formState.accountId || undefined` (or `null` when cleared in edit mode).
2. **`src/services/tasks.service.ts`:**
   - Ensure `Task` and `RawTaskResponse` include `accountId?: string | null` and `accountName?: string | null` (mapped from `item.account_id` / `item.account?.account_name`).
   - In `serializeTaskCreate` and `updateTask`: send `account_id: payload.accountId ?? null` (when defined / on create).
3. **`src/components/dashboard/tasks/TaskForm.tsx`:**
   - Add `<option value="Deal">{relatedTypeLabel("Deal")}</option>` to the `Create task for` / `Related To` select (lines 263–275).
   - Reset `accountId: null` alongside `accountName: ""` on `targetType` change.
   - Update Account field `disabled` and placeholder logic so it applies to `Lead` (`"Not applicable for leads"`), and for `Contact` / `Deal` auto-fills and locks when `formState.isAccountAutoFilled` is true.
   - **Remove the `"Auto-linked to contact"` badge & lock icon** above the Account input (lines 315–322), keeping only the lock icon inside the disabled input (lines 342–346).
4. **`src/components/dashboard/tasks/TaskModal.tsx` & `src/components/shared/EntityActivitiesModals.tsx`:**
   - Widen `initialTarget.type` in `TaskModalProps` to `"Contact" | "Lead" | "Deal"`.
   - In `EntityActivitiesModals.tsx` line 82, allow `targetType === "Lead" || targetType === "Contact" || targetType === "Deal"`.
   - Verify `DealDetailDrawer.tsx` (if it has a "Create Task" action using `EntityActivitiesModals`) now passes `Deal` as `initialTarget` cleanly.
5. **`src/lib/validations/crmSchemas.ts`:**
   - Update `taskCreateSchema.targetType` to `z.enum(["Contact", "Lead", "Deal"], ...)`.
6. **Translation keys (`src/messages/{en,ar,nl}/activities/tasks.json`):**
   - Ensure `relatedTypes.Deal` exists and clean up any unused `form.autoLinked` key if no longer referenced anywhere else.

**Backend Changes (`crusource-crm-backend/`):**
1. **Remove dead `Account` `related_to_type` branches:**
   - In `src/modules/tasks/handlers/create_task_handler.py` (lines 86–87) and `src/modules/tasks/handlers/update_task_handler.py` (lines 93–94): remove `elif rel_type in ("account", "accounts"):` so `related_to_type` only accepts `Lead`, `Deal`, `Contact` (Account association is stored in `Task.account_id`).
2. **Fix Account filter in `src/modules/tasks/repositories/task_page_repository.py`:**
   - In `apply_filters` (lines 51–60), when `rt == "Account"`, filter by:
     `or_(Task.account_id.isnot(None), and_(Task.related_to_id.isnot(None), func.lower(Task.related_to_type) == "account"))`
     This ensures tasks auto-linked to an Account via Contact or Deal (as well as any legacy Account-linked tasks) appear when filtering by `Account`.
   - Also validate `Account` scope via `require_record_links` (already checks `account_id` in `src/shared/auth/record_links.py` line 66) and ensure `TaskResponse` returns `account_id` (already present in `task_queries.py` line 28).

---

### Workstream C: Due Date Validation (Prevent Past Dates on Create)

**Problem:**
- `TaskForm.tsx` has no `min` attribute on `dueDate` (or `reminderDateTime`).
- `useTaskForm.ts`, `crmSchemas.ts`, and `task_commands.py` allow creating tasks with past due dates.

**Frontend Changes (`crusource-crm-frontend/`):**
1. **`src/components/dashboard/tasks/TaskForm.tsx`:**
   - Compute today's ISO date in the user's configured timezone (`getISODateInTimezone(new Date(), timezone)`).
   - Set `min={todayIso}` on the `dueDate` `<input type="date">` when `!isEditMode` (in edit mode, only enforce `min={todayIso}` if the user changes `dueDate` or allow existing overdue tasks to be edited/completed without blocking status updates).
   - Similarly, set `min` on `reminderDateTime` (`${todayIso}T00:00`) when `!isEditMode`.
2. **`src/hooks/useTaskForm.ts`:**
   - Reject past `dueDate` (`formState.dueDate < todayIso`) in `isFormValid` when creating a new task (`!initialTask`) or when `dueDate` was modified to a past date on edit, and show an inline validation message in `TaskForm.tsx`.

**Backend Changes (`crusource-crm-backend/`):**
1. **`src/modules/tasks/handlers/create_task_handler.py`:**
   - Validate that `command.due_date` (when provided) is not in the past (comparing date in UTC or allowing same-day `>= today_utc_date` to avoid timezone boundary false rejections, since frontend normalizes date-only to `YYYY-MM-DDT12:00:00.000Z`). Return `422` with a clear message (`"Due date cannot be in the past"`).

---

### Workstream D: Hierarchy View, Profiles & Permissions Fixes

**Problem:**
1. `ActivityAssigneeSelect.tsx` unconditionally appends `user` to `rawMembers`, so an Admin who is **not** a member of the selected team appears in the Task Owner dropdown and fails with `422: Assignee must be an active member of the record's team`.
2. `ActivityAssigneeSelect.tsx` omits `hierarchyLevel` and `reportsTo` from `actor`, weakening client-side hierarchy checks in `taskAssignmentPolicy.ts`.
3. Backend `is_superior_in_reporting` (`task_assignment_policy.py`) only checks `actor_user.team_id` and misses `TeamMembership` teams.
4. `TasksTable.tsx` always shows the "Edit" row action and opens `TaskModal` without passing `canEdit` from `usePermissions("tasks")`.
5. `delete_all_matching_tasks` in `tasks_repository.py` passes `Task` (model class) instead of `"tasks"` (string) to `require_bulk_targets`.

**Frontend Changes (`crusource-crm-frontend/`):**
1. **`src/components/shared/ActivityAssigneeSelect.tsx`:**
   - When `teamId` is set (Team Task / team context), **do not** unconditionally append `user` to `rawMembers` unless `team` actually includes them (or `teamId` is null). Specifically: `const rawMembers = teamId ? [...(team?.members || []), ...(team?.head ? [team.head] : [])] : [...(team?.members || []), ...(team?.head ? [team.head] : []), ...(user ? [user] : [])];`.
   - Pass `hierarchyLevel: (user as any)?.hierarchy_level ?? null` and `reportsTo: (user as any)?.reports_to ?? null` into `actor` (and ensure `/auth/me` or `useCurrentUser` / `team.members` provides them).
2. **`src/components/dashboard/tasks/TasksTable.tsx`:**
   - Destructure `canEdit` from `usePermissions("tasks")`.
   - Gate the row dropdown **Edit** `<DropdownMenuItem>` on `canEdit` (lines 809–815).
   - Pass `canEdit={canEdit}` to `<TaskModal>` (lines 1087–1103).
   - Also check `TasksKanban.tsx` / `TaskCard.tsx`: if `!canEdit`, disable drag-and-drop status changes or show read-only feedback cleanly.

**Backend Changes (`crusource-crm-backend/`):**
1. **`src/modules/tasks/services/task_assignment_policy.py`:**
   - Update `is_superior_in_reporting` to check all active teams the actor belongs to (both `actor_user.team_id` and `TeamMembership` via `user_team_ids`), checking if `team.manager_id == target_user.id`.
2. **`src/modules/tasks/repositories/tasks_repository.py`:**
   - Line 86: change `require_bulk_targets(db, scope, Task, matching_ids)` to `require_bulk_targets(db, scope, "tasks", matching_ids)` for consistency with line 52 and `record_bulk.py`.

---

### Workstream E: Search Result Highlighting (`HighlightMatch`)

**Problem:**
- `LeadList.tsx` and `LeadCard.tsx` highlight matching search queries with `<HighlightMatch text={...} highlight={searchQuery} />`, whereas `TasksTable.tsx` / `taskColumns.tsx` / `TaskCard.tsx` do not.

**Frontend Changes (`crusource-crm-frontend/`):**
1. **`src/components/dashboard/tasks/taskColumns.tsx` & `TasksTable.tsx`:**
   - Pass `searchQuery` (the active `filters.searchQuery || filters.globalFilter`) into `taskColumns` / `TasksTable.tsx` cell renderers.
   - Wrap searchable text fields (`subject`, `relatedTo.name`, `contactName`, `taskOwner`, `description`) with `<HighlightMatch text={...} highlight={searchQuery} />` (matching `PoolTasksTable.tsx` line 88 and `LeadList.tsx`).
2. **`src/components/dashboard/tasks/TaskCard.tsx` & `TasksKanban.tsx`:**
   - Pass `searchQuery` down to `TaskCardUI` and wrap `task.subject`, `task.relatedTo?.name`, and `task.taskOwner` with `<HighlightMatch>`.

---

### Workstream F: Remove Passive Tags & Non-Working Repeat Task

**Approach:** Remove UI, filters, import/export columns, and API request/response usage cleanly, **without** dropping the `tasks.tag` or `tasks.repeat` database columns (no destructive Alembic migration needed; existing DB rows remain safe).

**Frontend Changes (`crusource-crm-frontend/`):**
1. **Forms & Details:**
   - `TaskForm.tsx`: Remove the **Repeat Task** toggle/section (lines 519–568) and the **Tags** input/section (lines 598–618). Rename `form.descriptionTags` header to `form.description`.
   - `TaskDetails.tsx`: Remove the **Tags** block (lines 136–154) and rename `details.descriptionTags` header to `details.description`. Also fix `getPriorityBadgeColor` (lines 14–25) to handle `"Normal"` instead of `"Medium"`.
   - `useTaskForm.ts`: Remove `tags`, `repeatEnabled`, `repeatFreq`, `repeatUntil`, `handleRepeatToggle`, and their serialization in `buildPayload()`.
   - `crmSchemas.ts`: Remove `repeatEnabled`, `repeatFrequency` from `taskCreateSchema`.
2. **Table, Columns, Filters & State:**
   - `TasksTable.tsx`: Remove the `tag` column definition (lines 745–769) and `isRecurring` from `pageFilters` and `currentFilters`.
   - `taskColumns.tsx`: Remove the `tag` column definition (lines 217–234).
   - `TaskFilterPanel.tsx`: Remove `localIsRecurring`, `setLocalIsRecurring`, `isRecurring` chip, and the Recurring `PillMultiSelect` (lines 345–362).
   - `TaskFilterChips.tsx`: Remove the `isRecurring` chip (lines 180–188).
   - `tasksSlice.ts`: Remove `isRecurring`, `setIsRecurringFilter`, and its `countActiveTaskFilters` increment.
3. **Import, Export & Service:**
   - `TaskBulkImportModal.tsx`: Remove `repeat` and `tag` from `TASK_IMPORT_FIELDS` and row mapping.
   - `src/lib/exportColumns.ts`: Remove `repeat` and `tag` from `TASK_EXPORT_RESOLVERS` and `ALL_TASK_EXPORT_COLUMNS`.
   - `src/services/tasks.service.ts`: Remove `repeat` and `tag` from `Task`, `RawTaskResponse`, `TaskPageParams`, `mapTaskResponse`, `serializeTaskCreate`, `updateTask`, and `bulkImportTasks`.
4. **Translations (`src/messages/{en,ar,nl}/activities/tasks.json`):**
   - Remove unused `repeat*`, `tag*`, and `recurring*` keys (keeping keys tidy across all 3 locales).

**Backend Changes (`crusource-crm-backend/`):**
1. **`src/modules/tasks/commands/task_commands.py` & `src/modules/tasks/queries/task_queries.py`:**
   - Remove `repeat` and `tag` from `TaskCreate`, `TaskUpdate`, `TaskImportItem`, and `TaskResponse` (or mark optional/ignored if backward compatibility with old clients is desired; removing from `TaskResponse` / `TaskCreate` / `TaskUpdate` keeps the API clean).
2. **`src/modules/tasks/handlers/bulk_import_tasks_handler.py`:**
   - Remove `repeat=item.repeat` and `tag=item.tag or []`.
3. **`src/modules/tasks/queries/task_page_queries.py` & `src/modules/tasks/repositories/task_page_repository.py`:**
   - Remove `is_recurring` filter parameter and `"tag"` from `TaskPageParams.sort_by` `Literal[...]` in `task_page_queries.py`, and remove `sort_by == "tag"` handling in `task_page_repository.py`.
4. **`src/shared/auth/field_response_route.py`:**
   - Check line 50 (`"is_recurring": "repeat"`): keep or clean up only if `tasks` field-level permissions no longer expose `repeat`.
5. **Preserve DB Columns:**
   - Keep `repeat` and `tag` columns on `Task` SQLAlchemy model (`src/modules/tasks/repositories/models.py`) or mark deprecated—no `DROP COLUMN` migration required.

---

## 3. Cross-Module Dependency Checklist

| Dependency Area | Verified Impact |
| --- | --- |
| **Calls & Meetings** (`TargetSearchInput`, `ActivityAssigneeSelect`) | `TargetSearchInput` gains `linkableOptions` on `useLeadSearch`/`useDealSearch` — also fixes teamspace scoping in `LogCallModal` & `MeetingModal`. `ActivityAssigneeSelect` fix also applies to Calls & Meetings when `teamId` is set. |
| **Teamspace Pool** (`PoolTasksTable.tsx`, `PoolDrawersContainer.tsx`, `TeamspaceCreateDialog.tsx`, `TeamspaceImportDialog.tsx`) | `PoolTasksTable` reuses `taskColumns` from `tasks` — removing `tag` from `taskColumns.tsx` updates both automatically. `TeamspaceImportDialog` imports `TASK_IMPORT_FIELDS` from `TaskBulkImportModal.tsx`. `TeamspaceCreateDialog` uses `TaskModal` + `serializeTaskCreate`. |
| **Saved Views** (`SavedViewsDropdown`, `tasksSlice.ts`) | Old saved views that had `isRecurring` will safely ignore the unknown key if `applySavedFilters` only reads known keys; verify `applySavedFilters` in `tasksSlice.ts`. |
| **Leads / Deals Drawers** (`EntityActivitiesModals.tsx`) | Widening `targetAsTask` in `EntityActivitiesModals.tsx` to include `"Deal"` enables creating tasks directly from `DealDetailDrawer` as well. |
| **Profile Field Permissions** (`field_response_route.py`, `usePermissions`) | Verify `tasks` module field permissions don't crash if `tag` or `repeat` are absent from `TaskResponse`. |

---

## 4. Verification Plan

1. **Backend Tests (`crusource-crm-backend/`):**
   - Run existing task & teamspace tests (`pytest tests/test_tasks_delegation_scoping.py tests/test_record_team_isolation.py tests/test_phase1_accounts_contacts_teamspace_foundation.py tests/test_unified_sales_teamspace_matrix.py`).
   - Add new unit/integration tests covering:
     - `GET /api/v1/leads?linkable_for_create=true&team_id=<team_id>` and `GET /api/v1/deals?linkable_for_create=true&team_id=<team_id>` filtering out private/other-team records.
     - `POST /api/v1/tasks` with `related_to_type="Deal"` and `account_id` auto-linked.
     - `POST /api/v1/tasks` with past `due_date` returning `422`.
     - `is_superior_in_reporting` checking `TeamMembership` teams.
     - Filtering tasks by `related_types=["Account"]` matching `Task.account_id IS NOT NULL`.
2. **Frontend Checks (`crusource-crm-frontend/`):**
   - Run `npm.cmd run build` / TypeScript typecheck (`npx.cmd tsc --noEmit`) and `tests/test_task_assignment_policy.ts` / `tests/test_task_cache_sync.ts`.
   - Manual / Playwright browser verification:
     - Create Team Task as Admin -> select Sales Team -> Task Owner dropdown excludes Admin if not in Sales Team -> Lead/Deal search only shows Sales Team records.
     - Select Contact or Deal with Account -> Account auto-fills and locks (no `"Auto-linked to contact"` text/lock above input).
     - Due Date rejects past dates on create.
     - Search in Tasks list & Kanban highlights matching text.
     - Tags and Repeat Task are absent from Create/Edit/Details/Filters/Import/Export.
     - Read-only profile cannot see Edit button in `TasksTable` or `TaskModal`.
