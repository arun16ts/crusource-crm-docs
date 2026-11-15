# Crusource CRM — Comprehensive Master Implementation Plan & Architecture Guide

> **Document Status**: WAVE 1 (EXCEPT SEC-01 & SEC-04), WAVE 2, AND FOLLOW-UP ENHANCEMENTS (CALLS/MEETINGS UI, ACCOUNTS, CONTACTS) IMPLEMENTED & VERIFIED LOCALLY  
> **Date**: November 15, 2026  
> **Target Repositories**: `crusource-crm-frontend/`, `crusource-crm-backend/`, `crusource-crm-docs/`  
> **Product Scope**: CRM only; see [workspace AGENTS.md](../AGENTS.md).  
> **Canonical Document Path**: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)

---

## 1. Executive Summary & Master Requirements Matrix

Following the executive presentation, live client meeting, and source review on November 15, twenty-eight (28) functional fixes and feature enhancements are tracked across **Wave 1** (14 initial presentation & meeting items, with 12 implemented locally and `SEC-01`/`SEC-04` awaiting product decision) and **Wave 2** (14 newly audited timeline continuity, form reactivity, full-record export, and lead status/stage synchronization fixes across the entire CRM — all implemented and verified locally), alongside follow-up Calls & Meetings UI, Accounts, and Contacts enhancements. Inclusion in this plan does not imply production deployment; `SEC-01` and `SEC-04` remain deferred.

### Wave 1 Master Scope Matrix (`SEC-01` .. `UX-01`)

| ID | Domain | Requirement / Bug Description | Origin | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | **Scoping & RBAC** | **Personal View Scope Behavior (Needs Product Decision)**: Verify whether profile `can_view` settings should widen personal Leads/Deals/Tasks/Calls/Meetings lists; current source explicitly keeps personal work assignment-based and separates Teamspace projections. | Client Meeting, Source Review | **Needs confirmation** | Deferred (Policy Decision) |
| **SEC-02** | **Admin Governance** | **Role Hierarchy-Gated User Deletion**: Managers and subordinates can currently delete equal or higher roles (including Admins). Must enforce hierarchy level gating in backend and frontend. | Client Meeting | **Critical** | Implemented Locally |
| **SEC-03** | **Admin Governance** | **Role Hierarchy-Gated User Invitations**: Users can invite candidates into roles higher than themselves. Must restrict invite dropdown and backend command by hierarchy level. | Client Meeting | **High** | Implemented Locally |
| **SEC-04** | **Data Governance** | **Teamspace Governed Export & Personal Export Policy**: Teamspace has an approval workflow; decide separately whether personal module exports need an approval flow. | Client Meeting, Source Review | **High** | Deferred (Policy Decision) |
| **SEC-05** | **Profile Access Control** | **Requests Inbox Permission Bypass**: The sidebar treats `teams_pool` as sufficient for the Requests item even when `teams_requests` is disabled; the direct Requests route is not gated by the profile permission. | User Report, Source Review | **High** | Implemented Locally |
| **SALES-01** | **Leads Lifecycle** | **Lead Progression Dynamic Sync**: Advancing a lead does not update list view or drawer status; requires stage/status synchronization and eager-loaded pipeline stage relationships. | Presentation | **High** | Implemented Locally |
| **SALES-02** | **Leads Lifecycle** | **Bidirectional Lead Stepping (Regress / Back Button)**: Users cannot move leads backward if advanced prematurely or if disqualification occurs. Must support backward stage transition. | Presentation | **Medium** | Implemented Locally |
| **ACT-01** | **Activities** | **Meeting Booking Start Time Reset & Guided Two-Step Flow**: Start time resets to default on re-renders; input must be refactored into a guided **Date first -> Time second** flow with duration presets. | Presentation | **High** | Implemented Locally |
| **DOC-01** | **Documents** | **Enterprise Document Types (SOW & PO/OP)**: Add Statement of Work (`sow`), Purchase Order (`po`), and Purchase of Work (`op`) to categories, models, and migrations. | Presentation | **Medium** | Implemented Locally |
| **ALIGN-01** | **Data Alignment** | **Leads vs Teamspace Pool Filters Alignment**: Standardize single-select static pool filters with multi-select, dynamic picklists, and pipeline stage filters. | Client Meeting | **Medium** | Implemented Locally |
| **ALIGN-02** | **Data Alignment** | **Leads Import vs Teamspace Governed Import Harmonization**: Harmonize column mapping schemas, aliases, and stage mapping validation across both import dialogs. | Client Meeting | **Medium** | Implemented Locally |
| **UI-01** | **Admin UI** | **Responsive Admin Users Toolbar**: "Add User" button wraps awkwardly on small screens; refactor with container queries to match Tasks toolbar. | Presentation | **Medium** | Implemented Locally |
| **FIN-01** | **Analytics** | **Pipeline Health Multi-Currency Fidelity**: Dashboard shows USD `$` instead of INR `₹` when Indian Rupee is selected; wire currency context to widget. | Presentation | **Medium** | Implemented Locally |
| **UX-01** | **Cross-Browser** | **Safari Browser Favicon & Apple Touch Icons**: Favicon blank on Safari iOS/macOS due to SVG touch icon rejection; add 180x180 PNG touch icon and metadata. | Presentation | **Low** | Implemented Locally |

---

### Wave 2 Master Scope Matrix (`TIME-01` .. `STAT-02`)

| ID | Domain | Requirement / Bug Description | Affected Modules | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TIME-01** | **Timeline & Notes** | **Stage Advance/Regress & System Events Shown as User Notes**: Advancing or regressing a lead stage logs `"System: Stage changed to ..."`, which `timelineUtils.ts` fails to match and renders as `"Note by <user>"` with a yellow note icon; Deal Closed-Lost notes and migrated `"*(Migrated from Lead)*\nSystem: ..."` notes also render as user notes; `"System:%"` notes cause 50-row page starvation in `note_page_repository.py` and leak into `PoolNotesTab.tsx`. | Leads, Deals, Contacts, Accounts, TeamSpace Pool Notes | **Critical** | Implemented & Verified Locally |
| **TIME-02** | **Timeline Timestamps** | **Meeting/Call/Task Action Timestamps vs Scheduled Future Times**: A meeting created at 3:30 PM for a 4:00 PM start time shows `4:00 pm` as the timeline event timestamp and sorts into the future above later 3:39 PM actions (`timelineUtils.ts:358,408` and `activity_timeline_service.py:133`). Scheduled Calls (`timelineUtils.ts:335`) and edited Tasks (`timelineUtils.ts:322`) exhibit the same timestamp/sorting flaw. | Leads, Deals, Contacts, Accounts, Meetings, Calls, Tasks, Global Timeline | **High** | Implemented & Verified Locally |
| **TIME-03** | **Timeline Audit Trail** | **Entity Field Updates Not Logged in Timeline**: Updating a Lead, Deal, Contact, or Account (`update_lead_handler.py`, `update_deal_handler.py`, `update_contact_handler.py`, `update_account_handler.py`) writes to `AuditLog` / `StageHistory` without creating a `"System: ..."` timeline note, and `cacheInvalidation.ts` omits `queryKeys.notes.all()`. | Leads, Deals, Contacts, Accounts | **High** | Implemented & Verified Locally |
| **TIME-04** | **Timeline Documents** | **Document Uploads, Edits & Deletions Not Updating in Timeline**: `useDocumentBatchUpload.ts` (`UploadDocumentModal` from `/dashboard/documents`), `DocumentsWidget.tsx:127,162-166,581-591` (`handleFilePicked`, `handleDelete`, `DocumentEditor` callbacks), `useDocuments.ts:99-130`, and `useDocumentMutations.ts:17-134,244-252` fail to invalidate `["notes"]` / `["timeline"]`; `assign_document_handler.py` omits `meeting_id`/`task_id`/`call_id`; content edits (`version_handlers.py`, `update_binary_content_handler.py`) and restores (`recycle_bin_handlers.py`) emit no system note; `alreadyHasNote` (`timelineUtils.ts:429`) suppresses fallback upload cards when any delete/update note exists. | Leads, Deals, Contacts, Accounts, Meetings, Tasks, Calls, Documents | **High** | Implemented & Verified Locally |
| **TIME-05** | **Timeline Continuity** | **Zero-Loss Timeline Continuity Across Lead Conversion**: Standard conversion (`artifact_migrator.py`) does not clone Lead notes to `Deal`, drops migrated Tasks (`task_page_repository.py:18-19` ignores `Task.account_id`) and Meetings (`artifact_migrator.py:71-72`) from `AccountDetailDrawer`, drops Calls from `AccountDetailDrawer` whenever a Deal exists (`elif account_id:` at L59), removes Tasks/Calls/Meetings from the converted Lead, filters by `record_team_id == lead.record_team_id` (silently skipping mismatched/null team records), writes unparsed `"System: Migrated ..."` / `"System: Document transferred ..."` notes, omits `email_history` on Account timeline, and Inbox conversion (`execute_conversion_handler.py`) skips `migrate_lead_activities` entirely. | Leads, Contacts, Accounts, Deals, Inbox | **Critical** | Implemented & Verified Locally |
| **FORM-01** | **Form Reactivity (Tasks)** | **Tasks Modal Form Reset & Date/Time/Reminder Glitches**: `useTaskForm.ts:54-120` lacks an `initializedKeyRef` guard and depends on `[initialTask, initialTarget]` object references passed inline by `LeadDetailDrawer`, `DealDetailDrawer`, and `EntityActivitiesModals`, wiping user input on background refetches; `TaskModal.tsx:57,99-107` fails to reset on Cancel/reopen in Create mode (`null -> null`) and omits `isOpen` from mode sync; toggling Reminder before Due Date leaves `reminderDateTime` empty with a silently disabled Save button (`TaskForm.tsx:40-43`); Calendar quick-create `selectedDate` (`QuickCreateEventPopover.tsx:97`) is ignored; `dueDate`/`reminder` ignore workspace timezone helpers and `taskOwner` submits `"Current User"` instead of UUID. | Tasks, Calendar, Leads/Deals/Contacts/Accounts Drawers | **High** | Implemented & Verified Locally |
| **FORM-02** | **Form Reactivity (Calls & Meetings)** | **Calls & Log-Meeting Form Reset & Mode Glitches**: `useCallForm.ts:182-349` and `useLogMeetingForm.ts:161-211` lack `initializedKeyRef` guards and reset all user fields when `users`, `currentUser`, `formatDateTimeLocal`, or inline `initialTarget`/`initialCallFor` references update; `CallsTable.tsx:462-473,678` opens "Log Call" in `"schedule"` mode because `callToEdit.id` is `""`; `CallLogModal.tsx:94-154` and `MeetingMinutesModal.tsx:56-99` lack `initializedKeyRef` guards on `[call]`/`[meeting]`. | Calls, Meetings, Dashboard Workqueue, Entity Drawers | **High** | Implemented & Verified Locally |
| **FORM-03** | **Form Reactivity (Sales Entities)** | **Lead, Deal, Contact & Account Form Reset & Draft Clobbering**: `AddLeadModal.tsx:192-257` and `AddDealModal.tsx:202-257` overwrite restored `useFormDraft` values on open; `AddLeadModal.tsx:257`, `ConvertLeadModal.tsx:93`, and `BulkConvertModal.tsx:94` reset user input when `usePipelines({ enabled: isOpen })` resolves; `AddContactModal.tsx:97-127`, `AddAccountModal.tsx:95-115`, and Inbox `CreateContactModal.tsx:40-83` lack `prevIsOpenRef`/`initializedKeyRef` guards and reset on background query refetches. | Leads, Deals, Contacts, Accounts, Inbox | **High** | Implemented & Verified Locally |
| **FORM-04** | **Form Reactivity (Campaigns, Email, TeamSpace & Admin)** | **Stale / Resetting Modals in Campaigns, Email, TeamSpace & Admin**: `ScheduleCampaignPopover.tsx:28-43,100` never syncs on reopen and parses UTC ISO strings as local time; `useEmailComposerState.ts:128-154` never clears `subject` or `editor` body on close/reopen; `useTemplateFormState.ts:84-113` lacks `prevIsOpenRef`; `CreateGoalModal.tsx:69-82`, `CreateStageModal.tsx:43-51`, and `CreateApprovalRuleModal.tsx:92-112` never reset on close/reopen; `CreateRoleModal.tsx:59-81`, `EditRoleModal.tsx:102-111`, `EditTeamModal.tsx:62-72`, `EditPipelineModal.tsx:36-43`, `TemplateEditorModal.tsx:87-120`, and `UserEditForm.tsx:77-90` lack initialization guards. | Campaigns, Email Composer, TeamSpace Goals, Admin | **Medium** | Implemented & Verified Locally |
| **EXP-01** | **Exports (Leads)** | **Leads Export HTTP 422 `"Invalid export columns"` & Full Form Field Coverage**: `LeadBoard.tsx:497` sends `ALL_COLUMNS` containing `ai_priority_score`, which is missing from backend `FIELDS["leads"]` in `export_columns.py:84-126`, causing 100% of backend Lead exports (`all`, `filtered`, `selectAllMatching`) to fail with HTTP 422; `export_columns.py:213` hardcodes `alternative_numbers` to `""`; `LEAD_COLUMN_ACCESSORS` (`exportColumns.ts`) is missing `alternative_numbers` and `ai_priority_score`; `ALL_COLUMNS` (`leadBoardConfig.ts`) and `FIELDS["leads"]` omit Add/Edit Lead & model fields (`first_name`, `last_name`, `owner_name`, `currency`, `updated_at`); Kanban view `current_view` export returns 0 rows because `useLeads` is disabled in Kanban mode. | Leads | **Critical** | Implemented & Verified Locally |
| **EXP-02** | **Exports (Deals, Contacts, Accounts)** | **Cross-Module Export Scope Bugs & Missing Form Fields**: In `deals/page.tsx:399`, `filtered` export sends raw `filters` (where `pipeline_id: "all"` triggers backend HTTP 422 UUID validation error) instead of `activeFilters`, and Kanban `current_view` exports 0 rows; `DEAL_ALL_COLUMNS` / `DEAL_COLUMN_ACCESSORS` omit `currency`, `win_probability`, `loss_reason`, `loss_notes`, `updated_at`; `contacts/page.tsx` and `contacts_routes.py` ignore `contact_source` and `searchBy` filters during table query and `filtered` export, and `CONTACT_ALL_COLUMNS` omits `first_name`, `last_name`, `updated_at`; `accounts/page.tsx:156-169` omits `status` and `parent_account_name` from `ALL_COLUMNS`. | Deals, Contacts, Accounts | **High** | Implemented & Verified Locally |
| **EXP-03** | **Exports (Activities & TeamSpace)** | **Calls, Meetings, Tasks & TeamSpace Export Gaps**: `CallsTable.tsx:513-520` bypasses `ExportOptionsModal`, hardcoding CSV and making `all`, `current_view`, and `xlsx` unreachable; `MeetingsTable.tsx:235-242` makes `current_view` identical to `filtered` and omits form fields (`timezone`, `reminder`, `google_meet_link`, `cancellation_reason`); `TeamspaceExportDialog.tsx` and `governed_actions.py:438-442` omit columns (`alternative_numbers`, `pipeline_id`, `stage_id`, `ai_priority_score`, `loss_reason`, `attendees`) and serialize foreign-key IDs as raw UUIDs and JSONB arrays as Python repr strings. | Calls, Meetings, Tasks, TeamSpace Pool | **Medium** | Implemented & Verified Locally |
| **STAT-01** | **Lead Status & Stage** | **Duplicate Lead Status Badges in `LeadList.tsx`**: `LeadList.tsx:587-602` renders both the `lead.status` badge (`[Contacted]`) and the `lead.stage_name` pill (`[Contacted]`) whenever `!visibleColumns.includes("stage") && lead.stage_name`, producing duplicate side-by-side badges (`[Contacted] [Contacted]`, `[Not Contacted] [Not Contacted]`) across both Sales Leads and TeamSpace Pool Leads (`PoolLeadsTab.tsx`). | Leads List, TeamSpace Pool Leads | **High** | Implemented & Verified Locally |
| **STAT-02** | **Lead Status & Stage** | **Conflicting Status vs Lifecycle Stage in Drawer, Creation & Outcome Transitions**: (1) `create_lead_handler.py:43-79` never infers `lead.status` from `stage_id` on creation, leaving `status="not_contacted"` even when created in `"Contacted"` or `"Qualified"`; (2) `update_lead_handler.py:160-180` leaves `stage_id` pointing to the old stage when `status` is set to an outcome status (`contact_in_future`, `not_qualified`, `lost_lead`, `junk_lead`), causing `LeadDetailDrawer.tsx:435` to show `CONTACT IN FUTURE` in the header while `LeadStageStepper.tsx:57-60` shows `Current: Attempted to Contact` and `LeadList.tsx` shows `[Contact in Future] [Attempted to Contact]`; (3) `FilterPanel.tsx:253` hides outcome statuses when pipeline stages exist, and `PoolFilters.tsx:43` omits `lost_lead`. | Leads Backend, LeadDetailDrawer, LeadStageStepper, FilterPanel, PoolFilters | **High** | Implemented & Verified Locally |

---

## 2. In-Depth Root Cause & Architectural Analyses (Wave 1)

### SEC-01: Personal View Scope Behavior (Needs Product Decision)
- **Primary Files**:
  - `crusource-crm-backend/src/shared/auth/scope_guard.py` (Lines 494–516)
  - `crusource-crm-backend/src/shared/auth/guards.py`
  - `crusource-crm-frontend/src/components/admin/profiles/tabs/ModulesTab.tsx`
- **Source Review**:
  `scope_guard.py` explicitly states that personal work is assignment-based, while Teamspace/monitoring uses a persistent-team projection; role/view-all must not turn personal lists into an organization-wide list. The previous diagnosis that an early return was necessarily a bug, and its proposed team/org expansion, were not supported by that architecture review.
  The remaining issue is a product-contract question: confirm whether the request concerns personal module lists or Teamspace/monitoring views. If personal lists should expand, define the permitted record sources, meeting attendee behavior, team membership semantics, soft-delete handling, and organization isolation before changing the guard. If assignment-based lists are intended, close this item as expected behavior with product confirmation.
- **Implementation Status**: Do not apply the former blanket query rewrite until the product decision above is recorded. If approved, update this section with the agreed record and tenant boundaries and add tests to the existing backend `tests/` suite.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Personal Leads, Deals, Tasks, Calls, Meetings; Teamspace remains a separate projection.
  - *Risk*: Data exposure if personal views expand beyond the intended assignment/team boundary.
  - *Verification*: Any approved change must preserve organization isolation and existing soft-delete filtering.

---

### SEC-02: Role Hierarchy-Gated User Deletion
- **Primary Files**:
  - `crusource-crm-backend/src/modules/admin/commands/users/delete_user_command.py` (Lines 31–75)
  - `crusource-crm-frontend/src/components/admin/users/UserRowActionMenu.tsx` (Lines 100–145)
  - `crusource-crm-frontend/src/components/admin/users/UsersTable.tsx`
  - `crusource-crm-frontend/src/components/admin/users/hooks/useUserBulkActions.ts`
- **Root Cause**:
  `delete_user_command.py` only checked whether target is self, founder, or the last active admin. It never inspected the actor's `RoleNode.hierarchy_level` relative to the target's `RoleNode.hierarchy_level`. A Manager (e.g. hierarchy level 3) could delete an Administrator (level 1) or another Manager. On the frontend, `UserRowActionMenu.tsx` displayed the "Delete User" button for every user row except the current user.
- **Architectural Solution**:
  1. **Backend**:
     - Lookup `actor_role = db.query(RoleNode).filter_by(id=actor.role_node_id).first()`.
     - Lookup `target_role = db.query(RoleNode).filter_by(id=target.role_node_id).first()`.
     - If actor is not an organization Administrator:
       - Enforce `target_role.hierarchy_level > actor_role.hierarchy_level` (in hierarchy trees, lower numerical level = higher authority, e.g. Level 1 Admin > Level 3 Manager).
       - Enforce target is not an Admin profile (`target.profile.is_admin_profile == False` and `target.role != 'admin'`).
       - If violated, raise `HTTPException(403, "You do not have permission to delete a user with an equal or higher role in the hierarchy.")`.
  2. **Frontend**:
     - Compute `canDeleteUser(actor, target)` helper.
     - Hide or disable "Delete User" in `UserRowActionMenu` when target has equal or higher rank.
     - In `UsersTable`, disable selection checkboxes for non-deletable users and exclude them in `useUserBulkActions`.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Team leadership reassignment (`Team.manager_id`), CRM record transfer (`user_admin_repository.reassign_all_crm_records`).
  - *Risk*: Cross-team transfer failing with 422 in `creation_team` if recipient is not in all of target's teams.
  - *Verification*: Ensure `reassign_all_crm_records` safely normalizes `record_team_id` or reassigns to the recipient's primary team.

---

### SEC-03: Role Hierarchy-Gated User Invitations
- **Primary Files**:
  - `crusource-crm-backend/src/modules/admin/commands/invites/invite_validator.py` (Lines 21–34)
  - `crusource-crm-backend/src/modules/admin/commands/invites/single_invite_command.py` (Lines 20–35)
  - `crusource-crm-backend/src/modules/admin/commands/invites/bulk_invite_command.py`
  - `crusource-crm-frontend/src/components/admin/users/bulk/BulkInviteModal.tsx` (Lines 64–70)
  - `crusource-crm-frontend/src/components/admin/users/bulk/SingleInviteForm.tsx` (Lines 580–615)
- **Root Cause**:
  `_validate_invite_role` in `invite_validator.py` only checked `if admin_role_str == "sales_manager" and role_clean == "admin"`. It completely ignored custom `RoleNode` hierarchy levels and did not prevent a manager from inviting peers or custom leadership roles. Frontend `BulkInviteModal.tsx` flattened the entire `roleTree` and passed all roles to the dropdown unconditionally.
- **Architectural Solution**:
  1. **Backend**:
     - In `_validate_invite_role`, accept `db`, `org_id`, `actor_user_id`, and `target_role_node_id`.
     - Non-admin inviter cannot invite any role where `target_role.hierarchy_level <= actor_role.hierarchy_level`.
     - Reject with `HTTPException(403, "You cannot invite users to a role equal to or higher than your own hierarchy level.")`.
  2. **Frontend**:
     - In `BulkInviteModal.tsx`, filter `roleOptions`:
       ```typescript
       const filteredRoles = useMemo(() => {
         const all = flattenRoleTree(roleTree);
         if (isAdmin) return all;
         return all.filter((r) => (r.hierarchy_level || 1) > (currentUserHierarchyLevel || 1));
       }, [roleTree, isAdmin, currentUserHierarchyLevel]);
       ```
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Profile auto-assignment on invite (`default_profile_id`), user onboarding tokens.
  - *Risk*: A subordinate role having no valid profile mapped, leading to unhandled null profiles on signup.
  - *Verification*: Confirm `RoleNode.default_profile_id` is always validated during invite creation.

---

### SEC-04: Teamspace Governed Export & Personal Export Policy
- **Primary Files**:
  - `crusource-crm-frontend/src/components/leads/board/useLeadExport.ts` (Lines 38–85)
  - `crusource-crm-frontend/src/app/dashboard/deals/page.tsx`
  - `crusource-crm-frontend/src/components/teamspace/TeamspaceExportDialog.tsx`
  - `crusource-crm-frontend/src/components/dashboard/tasks/TasksHeaderToolbar.tsx`
  - `crusource-crm-backend/src/modules/approvals/services/governed_actions.py` (Lines 151–260)
  - `crusource-crm-backend/src/modules/approvals/handlers/download_governed_export_handler.py`
- **Root Cause**:
  Leads and Deals pages generate exports in the browser. TeamSpace already has a governed export dialog and backend route, but its `export_mode` belongs to TeamSpace permissions; ordinary CRM module permissions expose a boolean `can_export`. The endpoint proposed in the previous draft (`/api/v1/approvals/actions`) does not exist, and the governed action command requires fields such as `reason`, `columns`, `selection_filters`, and `idempotency_key`.
- **Architectural Solution**:
  1. Keep direct export governed by the existing `can_export` check where no approval mode exists.
  2. For TeamSpace export requests, reuse `TeamspaceExportDialog`, `TeamspaceActionService`, and `POST /api/v1/teamspace/teams/{team_id}/{module}/actions`; preserve the existing command and approved-download contracts.
  3. Before adding approval-required export to personal Leads/Deals pages, decide whether that product flow is required and define its permission and API contract. Do not assume TeamSpace `export_mode` applies to ordinary CRM module permissions.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Approvals inbox, audit trail, governed actions journal.
  - *Risk*: A wrong permission model or route can bypass export policy or break existing direct exports.
  - *Verification*: Test direct exports for authorized users and the existing TeamSpace approval flow separately. Add personal-export approval tests only after its policy and contract are agreed.

---

### SEC-05: Requests Inbox Permission Bypass
- **Primary Files**:
  - `crusource-crm-frontend/src/components/layout/sidebar/sidebarConfig.ts`
  - `crusource-crm-frontend/src/components/layout/Sidebar.tsx`
  - `crusource-crm-frontend/src/components/teamspace/TeamspaceRequestsSection.tsx`
  - `crusource-crm-backend/src/modules/profiles/guards.py`
  - TeamSpace request and governed-action route modules under `crusource-crm-backend/src/modules/teamspace/routes/`
- **Root Cause**:
  The Requests sidebar item accepts either `teams_pool` or `teams_requests`. The Standard profile intentionally seeds `teams_pool=true` and `teams_requests=false`, so the fallback exposes the link. The `/dashboard/teamspace/requests` page does not check `teams_requests` before rendering, and request-list/count APIs do not require that setup permission.
- **Architectural Solution**:
  1. Gate the Requests navigation item and direct page by `teams_requests` (with the existing Administrator access behavior).
  2. Do not request inbox counts or load inbox data while that permission is denied.
  3. Apply the existing `require_setup_permission("teams_requests")` guard to request-inbox list, count, review, and history endpoints.
  4. Keep `teams_pool` and per-module TeamSpace action policies independent. This fix does not disable Team Pool access or change record-level request submission policy.
- **Verification**:
  Confirm a Standard profile with Team Pool enabled and Requests disabled sees no inbox navigation or inbox content, including on direct navigation, and receives 403 for guarded inbox APIs. Confirm profiles with `teams_requests` enabled and Administrators retain the existing inbox behavior.

---

### SALES-01 & SALES-02: Lead Progression Synchronization & Bidirectional Stepping
- **Primary Files**:
  - `crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx` (Lines 260–340)
  - `crusource-crm-frontend/src/components/leads/drawer/LeadQuickActions.tsx` (Lines 125–160)
  - `crusource-crm-frontend/src/components/leads/LeadList.tsx` (Lines 89–95, 580–595)
  - `crusource-crm-frontend/src/hooks/mutations/useLeadMutations.ts` (Lines 114–240)
  - `crusource-crm-backend/src/modules/leads/handlers/update_lead_handler.py` (Lines 110–145)
  - `crusource-crm-backend/src/modules/leads/repositories/leads_repository.py` (Lines 155–165)
- **Root Cause**:
  1. `handleAdvanceStage` only transmitted `stage_id`. The backend updated `lead.stage_id` but left `lead.status` untouched.
  2. In `leads_repository.py`, `get_leads_for_scope` omitted `joinedload(Lead.pipeline_stage)`. Detached model responses fell back to `lead.status` (`not_contacted`).
  3. `LeadList.tsx` default columns rendered `lead.status` instead of dynamic `lead.pipeline_stage.name`.
  4. Only forward stepping (`handleAdvanceStage`) was supported; no back-stepping mechanism existed.
- **Architectural Solution**:
  1. **Backend**:
     - In `update_lead_handler.py`: when `stage_id` is supplied, lookup `PipelineStage` lifecycle category and synchronize `lead.status` automatically.
     - In `leads_repository.py`: add `joinedload(Lead.pipeline_stage)` to `get_leads_for_scope`.
  2. **Frontend**:
     - In `useUpdateLeadStage`: update TanStack Query caches for `['lead', id]` and `['leads', ...]` optimistically and on success.
     - In `LeadDetailDrawer.tsx`: implement `handleRegressStage` (moving to `pipelineStages[currentIndex - 1]`).
     - In `LeadQuickActions.tsx`: add a **"Regress Stage"** (`arrow_back`) button next to "Advance Stage".
     - In `LeadList.tsx`: render `lead.pipeline_stage?.name || lead.status` with stage badges, and add "Advance" and "Regress" shortcuts in the row action menu.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Deal conversion triggers (when stage reaches "Converted"), stage document validation rules.
  - *Verification*: Confirm regressing from "Qualified" back to "Contacted" clears conversion triggers without data corruption.

---

### ACT-01: Meeting Booking Start Time Reset & Guided Two-Step Flow
- **Primary Files**:
  - `crusource-crm-frontend/src/components/dashboard/meetings/modal/MeetingOverviewTab.tsx` (Lines 178–250)
  - `crusource-crm-frontend/src/components/dashboard/meetings/modal/form/MeetingScheduleFields.tsx` (Lines 140–200)
- **Root Cause**:
  `MeetingOverviewTab.tsx` had an unstable `useEffect` depending on `initialTarget`. Parent re-renders created a new object reference, resetting `formData.start_time` back to `defaultStart`. Furthermore, the native `datetime-local` input created confusing mobile/desktop formatting issues.
- **Architectural Solution**:
  1. Guard modal initialization with `initializedMeetingIdRef = useRef<string | null>(null)`. Only reset state when `initialTarget?.id` changes, never on re-render.
  2. Refactor `MeetingScheduleFields.tsx` into a guided two-step flow:
     - **Step 1: Date Picker**: Dedicated date input (`<input type="date">`) for meeting day.
     - **Step 2: Time Selector & Duration**: Dedicated time input (`<input type="time">`) followed by quick duration chips: `30 min`, `45 min`, `1 hr`, `Custom`.
     - Automatically compute `end_time = start_time + duration`.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Calendar sync, ICS calendar link generation (`calendarLinkUtils.ts`), timezone conversions.
  - *Verification*: Verify meeting start time is preserved when toggling between tabs (Overview, Attendees, Notes) in the modal.

---

### DOC-01: Enterprise Document Types (SOW, PO, OP)
- **Primary Files**:
  - `crusource-crm-backend/src/modules/documents/repositories/models.py` (Lines 13–18)
  - `crusource-crm-backend/alembic/versions/` (New Migration)
  - `crusource-crm-frontend/src/services/documents.service.ts` (Line 4)
  - `crusource-crm-frontend/src/components/documents/UploadDocumentModal.tsx`
  - `crusource-crm-frontend/src/messages/{en,ar,nl}/documents.json`
- **Root Cause**:
  The Python `DocumentCategory` enum and PostgreSQL `document_category_enum` were strictly limited to `proposal`, `msa`, `nda`, `kyc`, and `other`. Uploading a Statement of Work or Purchase Order resulted in 422 validation errors or forced fallback to `other`.
- **Architectural Solution**:
  1. Update `DocumentCategory` in `models.py`: add `sow = "sow"` (Statement of Work), `op = "op"` (Purchase of Work), `po = "po"` (Purchase Order).
  2. Generate and run Alembic migration:
     ```sql
     ALTER TYPE document_category_enum ADD VALUE IF NOT EXISTS 'sow';
     ALTER TYPE document_category_enum ADD VALUE IF NOT EXISTS 'op';
     ALTER TYPE document_category_enum ADD VALUE IF NOT EXISTS 'po';
     ```
  3. Update frontend type union, upload dropdown options, document list filters, and localization strings.
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: `StageDocumentRule` (stage-gated required documents for Deals).
  - *Verification*: Confirm SOW and PO can be selected in pipeline stage document requirements.

---

### ALIGN-01 & ALIGN-02: Leads vs Teamspace Pool Filters & Import Alignment
- **Primary Files**:
  - `crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx`
  - `crusource-crm-frontend/src/components/teamspace/TeamspaceImportDialog.tsx`
  - `crusource-crm-frontend/src/lib/teamspace/importRecords.ts`
  - `crusource-crm-backend/src/modules/teamspace/repositories/pool_sales_query_repository.py`
- **Root Cause & Architectural Alignment**:
  1. **Filters Alignment**:
     - *Divergence*: Main Leads supports multi-select arrays (`statuses`, `stage_ids`, `industries`, `ratings`), dynamic picklists, and pipeline stage selectors. Teamspace Pool used single-value selects and hardcoded static lists.
     - *Harmonization*: Upgrade `PoolFilters.tsx` when `activeTab === "leads"` to support multi-select status and dynamic lead sources; update `build_teamspace_leads_query` to accept `statuses: Optional[List[str]]` and `stage_ids: Optional[List[str]]`. Retain teamspace-specific allocation controls (`isUnassigned`, `selectedOwnerId`).
  2. **Import Alignment**:
     - *Divergence*: Main Leads import directly ingests all columns into the user's account. Teamspace import enforces governance (`policy.import_mode`), strips `owner_id` from the spreadsheet to prevent cross-team assignment bypassing, masks restricted fields via FLS, and validates stage mappings.
     - *Harmonization*: Standardize field header aliases across both dialogs while strictly preserving teamspace governance boundaries (`owner_id` dialog gating and `record_team_id` enforcement).
- **Dependency Impact & Prevention**:
  - *Dependent Modules*: Team pool allocation queries, bulk reassignment workflows.
  - *Verification*: Test that filtering pool leads by multiple statuses returns records accurately within the team boundary.

---

### UI-01, FIN-01, UX-01: Admin Toolbar, Currency Fidelity & Safari Favicon
- **UI-01 (Admin Users Toolbar)**:
  - File: `crusource-crm-frontend/src/components/admin/users/UsersToolbar.tsx`
  - Solution: Adopt container query pattern from `TasksHeaderToolbar.tsx` (`flex-col @4xl/toolbar:flex-row`). On viewports `< 1024px`, stack the title and search/filter rows, and position the "Add User" CTA in a clean, full-width or dedicated action row.
- **FIN-01 (Pipeline Health Currency)**:
  - Files: `DashboardHome.tsx`, `PipelineHealthWidget.tsx`, `PipelineChart.tsx`
  - Solution: Pass `dashboardCurrency={dashboardCurrency}` from `DashboardHome` down to `PipelineHealthWidget`. Replace hardcoded `$` fallbacks with `useFormatting().formatCurrency(amount, dashboardCurrency)`, rendering `₹` correctly for INR.
- **UX-01 (Safari Favicon)**:
  - Files: `crusource-crm-frontend/src/app/layout.tsx`, `/public/apple-touch-icon.png`
  - Solution: Generate standard 180x180 px PNG `apple-touch-icon.png` and update Next.js metadata in `layout.tsx` to reference PNG icons and Safari pinned tab SVG mask.

---

## 2B. Wave 2 In-Depth Root Cause & Architectural Analyses (`TIME-01` .. `STAT-02`)

### TIME-01: Stage Advance/Regress & System Events Shown as User Notes
- **Primary Files**:
  - `crusource-crm-frontend/src/hooks/mutations/useLeadMutations.ts` (Lines 188–192, 296–303)
  - `crusource-crm-frontend/src/lib/timelineUtils.ts` (Lines 190–305)
  - `crusource-crm-frontend/src/components/deals/DealDetailDrawer.tsx` (Lines 243–247, 276–280, 354–358)
  - `crusource-crm-frontend/src/components/deals/kanban/useDealsKanbanState.ts` (Lines 208–218)
  - `crusource-crm-frontend/src/components/deals/DealsTable.tsx` (Lines 130–155)
  - `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolNotesTab.tsx` (Lines 59–74)
  - `crusource-crm-backend/src/modules/notes/repositories/note_page_repository.py` (Lines 9–21)
- **Root Cause**:
  1. `useUpdateLeadStage` (`useLeadMutations.ts:188–192`) logs `"System: Stage changed to ${stageName}"`, whereas `timelineUtils.ts:195` only matches `note.content.startsWith("System: Stage advanced to")`. Every stage advance/regress note falls through to `else` (`timelineUtils.ts:286–303`), rendering as `"Note by <user>"` with the yellow sticky-note icon (`bg-yellow-100 text-yellow-700`).
  2. `useUpdateLeadStatus` (`useLeadMutations.ts:299–303`) always writes `"System: Stage advanced to ${statusLabel}"` even for regressions or outcome statuses (`Contact In Future`, `Lost`, `Junk`).
  3. Deal Kanban (`useDealsKanbanState.ts:210–214`) creates `"Deal moved to Closed Lost. Reason: ..."` **without** a `"System:"` prefix (leaking into `DealNotesTab` and showing as a user note), while `DealDetailDrawer.tsx:357` writes `"System: Deal marked as Closed Lost (Reason: ...)"` (unmatched in `timelineUtils.ts`).
  4. Migrated Lead notes have `"*(Migrated from Lead)*\n"` prepended (`artifact_migrator.py:131,146`), which is only stripped at line 289 inside the `else` branch — so **every migrated system note** on Contact/Account/Deal fails `startsWith("System:")` and becomes `"Note by <user>: System: ... (Migrated)"`.
  5. `note_page_repository.py:9–21` does not exclude `System:%` notes in SQL when loading the Notes tab (`LeadNotesTab`, `DealNotesTab`, `NotesSection`), risking 50-row page-1 starvation; `PoolNotesTab.tsx:59–74` does not filter `"System:"` notes at all.
- **Architectural Solution**:
  1. Strip any leading `"*(Migrated from Lead)*\n"` prefix **before** checking `cleanContent.startsWith("System:")` in `timelineUtils.ts:193`, tracking `isMigrated` to label migrated system events cleanly.
  2. Parse all `"System: Stage advanced to"`, `"System: Stage regressed to"`, `"System: Stage changed to"`, `"System: Lead status updated to"`, `"System: Deal marked as Closed Lost"`, `"Deal moved to Closed Lost"`, `"System: Owner changed to"`, `"System: <Entity> updated:"`, `"System: Migrated "`, `"System: Document transferred from Lead:"`, `"System: Document restored:"`, and add a catch-all `else if (cleanContent.startsWith("System:"))` (`type: "system"`) so no system log can ever render as `"Note by <user>"`.
  3. Standardize system prefixes on Deal Closed-Lost/stage changes and add `exclude_system` SQL filtering in `note_page_repository.py` + `"System:"` filtering in `PoolNotesTab.tsx`.

---

### TIME-02: Meeting, Call & Task Action Timestamps vs Scheduled Future Times
- **Primary Files**:
  - `crusource-crm-frontend/src/lib/timelineUtils.ts` (Lines 61–79, 308–423, 459)
  - `crusource-crm-backend/src/shared/services/activity_timeline_service.py` (Lines 131–148)
- **Root Cause**:
  1. `generateTimeline` uses a single timestamp argument (`rawDateStr`) in `addEvent` (`timelineUtils.ts:61–79`) for both the right-hand event timestamp badge and descending sort order (`b.rawTime - a.rawTime`, L459).
  2. For Meetings (`timelineUtils.ts:358,396,402,408`) and in `ActivityTimelineService` (`activity_timeline_service.py:133`), `scheduled`, `rescheduled`, and `in_progress` meetings use `meeting.start_time || meeting.created_at`. A meeting created at 3:30 PM for a 4:00 PM start time displays `4:00 pm` on the timeline card and sorts into the future above later 3:39 PM actions!
  3. For Calls (`timelineUtils.ts:335`), `call.callStartDateTime || call.callStartDate || call.createdTime` similarly sorts future scheduled calls into the future and labels every call `"Call Logged: ..."`.
  4. For Tasks (`timelineUtils.ts:322`), `task.closedTime || task.modifiedTime || task.createdTime` shifts a task's original creation timeline card to its latest edit timestamp whenever any field is edited, and `meetings`/`calls`/`tasks` overwrite their creation event when completed or cancelled.
- **Architectural Solution**:
  - Use the actual action timestamp for sorting and card time:
    - Scheduled Meetings & Scheduled Calls: sort/timestamp by `created_at` (`createdTime`), while keeping `"Scheduled for <start_time>"` inside the description text.
    - Rescheduled Meetings: use `updated_at || created_at`.
    - Completed / Cancelled Meetings and Completed Tasks: emit the completion/cancellation event at `completed_at` / `cancelled_at` / `closedTime`, AND preserve the original `"Meeting Scheduled"` / `"Task Created"` event at `created_at` / `createdTime`.
  - Apply the same `m.created_at or m.start_time` rule for scheduled meetings in `activity_timeline_service.py:133`.

---

### TIME-03: Entity Field Updates Not Logged in Timeline
- **Primary Files**:
  - `crusource-crm-backend/src/modules/leads/handlers/update_lead_handler.py` (Lines 55–226)
  - `crusource-crm-backend/src/modules/deals/handlers/update_deal_handler.py` (Lines 53–278)
  - `crusource-crm-backend/src/modules/contacts/handlers/update_contact_handler.py` (Lines 37–98)
  - `crusource-crm-backend/src/modules/accounts/handlers/update_account_handler.py` (Lines 39–84)
  - `crusource-crm-frontend/src/lib/cacheInvalidation.ts` (Lines 63–186)
  - `crusource-crm-frontend/src/hooks/mutations/useLeadMutations.ts` (Lines 188–192, 299–303)
- **Root Cause**:
  All four entity update handlers record field diffs only in `AuditLog` (`audit_entity_mutation`) and stage changes in `StageHistory` (`log_stage_change`), creating zero `Note` records. Meanwhile, all four entity drawers (`LeadDetailDrawer`, `DealDetailDrawer`, `ContactDetailDrawer`, `AccountDetailDrawer`) construct timelines strictly via `generateTimeline({ entity, notes, tasks, calls, meetings, documents })`. Additionally, `invalidateLeads`, `invalidateDeals`, `invalidateContacts`, and `invalidateAccounts` (`cacheInvalidation.ts`) do not invalidate `queryKeys.notes.all()`.
- **Architectural Solution**:
  1. Introduce a lightweight shared backend helper `record_entity_update_timeline_note(...)` (under `crusource-crm-backend/src/shared/audit/timeline_note_logger.py`) called inside the update handlers for Leads, Deals, Contacts, and Accounts whenever fields, owner, stage, or status change.
  2. Emit deterministic backend `"System: ..."` notes on:
     - Stage transitions (`"System: Stage advanced to ..."` / `"System: Stage regressed to ..."` / `"System: Stage changed to ..."` using `PipelineStage.sort_order`) and Lead status changes (`"System: Lead status updated to ..."`), removing redundant frontend `NotesService.createNote` calls so transitions cannot double-log or fail silently.
     - Owner transfers (`"System: Owner changed to <Name>"`) and field edits (`"System: Lead updated: <Field List>"`, `"System: Deal updated: <Field List>"`, `"System: Contact updated: <Field List>"`, `"System: Account updated: <Field List>"`).
  3. Invalidate `queryKeys.notes.all()` and `queryKeys.timeline.all()` across `invalidateLeads`, `invalidateDeals`, `invalidateContacts`, `invalidateAccounts`, and `invalidateLeadConversion` in `cacheInvalidation.ts`.

---

### TIME-04: Document Uploads, Edits & Deletions Not Updating in Timeline
- **Primary Files**:
  - `crusource-crm-frontend/src/hooks/useDocumentBatchUpload.ts` (Lines 11–21)
  - `crusource-crm-frontend/src/app/dashboard/documents/page.tsx` (Lines 406–412)
  - `crusource-crm-frontend/src/components/documents/DocumentsWidget.tsx` (Lines 111–167, 560–593)
  - `crusource-crm-frontend/src/hooks/useDocuments.ts` (Lines 99–131)
  - `crusource-crm-frontend/src/hooks/queries/documents/useDocumentMutations.ts` (Lines 17–135, 244–253)
  - `crusource-crm-frontend/src/lib/timelineUtils.ts` (Lines 249–286, 425–456)
  - `crusource-crm-backend/src/modules/documents/handlers/assign_document_handler.py` (Lines 50–65)
  - `crusource-crm-backend/src/modules/documents/handlers/version_handlers.py` (Lines 84–137)
  - `crusource-crm-backend/src/modules/documents/handlers/update_binary_content_handler.py` (Lines 23–91)
  - `crusource-crm-backend/src/modules/documents/handlers/recycle_bin_handlers.py` (Lines 17–27)
- **Root Cause**:
  1. `useDocumentBatchUpload.ts:19` (used by `UploadDocumentModal`) only invalidates `["documents"]`; when uploading from `/dashboard/documents` (`page.tsx:410`), `["notes"]` and `["timeline"]` remain stale for `LeadDetailDrawer` (`staleTime: 30_000` in `useParentNotesPage.ts:59`).
  2. Inside `DocumentsWidget.tsx`: `handleDelete` (`L162–166`), `DocumentEditor` callbacks (`L581–591`), and fallback `handleFilePicked` (`L111–134`, which also hardcodes `"other"` for non-deals) do not invalidate `["notes"]` or `["timeline"]`. Likewise, `useDocuments.ts:99–130` (`updateMutation`, `deleteMutation`, `restoreMutation`) and `useDocumentMutations.ts:17–134,244–252` fail to invalidate `["notes"]`.
  3. On the backend, `assign_document_handler.py:50–55` omits `meeting_id`, `task_id`, and `call_id` when logging `"System: Document assigned: ..."`; `version_handlers.py` and `update_binary_content_handler.py` never emit `"System: Document modified: ..."` notes; and `recycle_bin_handlers.py` never emits `"System: Document restored: ..."`.
  4. In `timelineUtils.ts:429–431`, `alreadyHasNote = notes.some((n) => n.content && n.content.includes(doc.file_name))` suppresses the Section 8 upload fallback if any delete/update/transfer note mentions `doc.file_name`.
- **Architectural Solution**:
  - Invalidate `["documents"]`, `["notes"]`, `["timeline"]`, `["globalTimeline"]`, `["leads"]`, `["deals"]`, `["contacts"]`, and `["accounts"]` consistently across `useDocumentBatchUpload.ts`, `DocumentsWidget.tsx`, `useDocuments.ts`, and `useDocumentMutations.ts`.
  - Complete backend document timeline notes for `assign_document_handler.py` (include `Meeting`, `Task`, `Call`), `version_handlers.py` / `update_binary_content_handler.py` (`"System: Document modified: ..."`), and `recycle_bin_handlers.py` (`"System: Document restored: ..."`).
  - Tighten `alreadyHasNote` in `timelineUtils.ts:429` so it checks specifically for an existing upload note mentioning `doc.file_name`.

---

### TIME-05: Zero-Loss Timeline Continuity Across Lead Conversion
- **Primary Files**:
  - `crusource-crm-backend/src/shared/services/lead_conversion/artifact_migrator.py` (Lines 16–243)
  - `crusource-crm-backend/src/shared/services/lead_conversion/service.py` (Lines 104–162)
  - `crusource-crm-backend/src/modules/leads/handlers/convert_lead_handler.py` (Lines 89–121)
  - `crusource-crm-backend/src/modules/leads/handlers/bulk_convert_handler.py` (Lines 81–113)
  - `crusource-crm-backend/src/modules/tasks/repositories/task_page_repository.py` (Lines 16–25)
  - `crusource-crm-backend/src/modules/meetings/repositories/meeting_page_repository.py`
  - `crusource-crm-backend/src/modules/calls/repositories/calls_repository.py`
  - `crusource-crm-backend/src/modules/inbox/handlers/execute_conversion_handler.py` (Lines 58–105)
  - `crusource-crm-backend/src/modules/inbox/services/lead_conversion_service.py` (Lines 86–119)
  - `crusource-crm-frontend/src/components/accounts/AccountDetailDrawer.tsx` (Lines 67–99)
  - `crusource-crm-frontend/src/lib/cacheInvalidation.ts` (Lines 86–101)
- **Root Cause**:
  1. `ArtifactMigrator.migrate_lead_notes` (`artifact_migrator.py:104–174`) clones notes to `Contact` and `Account` only — **not to `Deal`** — and writes `"Lead was converted to Contact and Account."` only on `Contact`.
  2. `ArtifactMigrator.migrate_lead_activities` (`L18–102`) filters Tasks, Calls, and Meetings by `record_team_id == lead.record_team_id` (silently skipping activities with mismatched or null team IDs), and `migrate_lead_documents` (`L194`) has the same `record_team_id` filter.
  3. Overwriting `related_to_id = contact_id` (`Task`, `Meeting`) and `call_for_id = contact_id` (`Call`) causes three losses:
     - Viewing the converted **Lead** (`LeadDetailDrawer`) loses its Tasks, Calls, and Meetings.
     - Viewing the **Account** (`AccountDetailDrawer`) loses Tasks (`task_page_repository.py:18–19` checks `Task.related_to_id == params.parent_id` and ignores `Task.account_id`, unlike `activity_timeline_service.py:57`), loses Meetings (`artifact_migrator.py:71–72` links only to Contact), loses Calls whenever a Deal is created (`elif account_id:` at L59), and lacks `email_history`.
  4. Lead creation origin (`lead.created_at` and `lead_source`) is lost on Contact/Account/Deal timelines.
  5. **Inbox conversion (`execute_conversion_handler.py:58–105`)** never calls `ArtifactMigrator.migrate_lead_activities` and only copies notes to Contact!
- **Architectural Solution**:
  1. Pass `deal_id` to `migrate_lead_notes`; clone all Lead notes to `Contact`, `Account`, **and `Deal`**; preserve `created_at` and `created_by`; add an origin system note (`created_at=lead.created_at`) and conversion note on all involved entities.
  2. Remove the restrictive `record_team_id == team_id` filter in `artifact_migrator.py` queries (keep `org_id` isolation). Ensure migrated Tasks set `account_id = account_id`, Calls query `related_to_type == "Lead"` as well as `call_for_type == "Lead"`, and `task_page_repository.py` + `meeting_page_repository.py` + `calls_repository.py` surface Account-associated and Account-Contact-associated activities cleanly without losing them when a Deal exists. Store or preserve Lead->Contact/Account/Deal links (or clone historical summary/activities non-destructively) so the converted Lead timeline also stays intact.
  3. Unify Inbox conversion (`execute_conversion_handler.py`) to delegate to `ArtifactMigrator` so Tasks, Calls, Meetings, Notes, and Documents migrate identically from Inbox threads.
  4. Expand `invalidateLeadConversion` (`cacheInvalidation.ts:86–101`) to also invalidate `notes`, `tasks`, `calls`, `meetings`, and `documents`.

---

### FORM-01 & FORM-02: Task, Call & Meeting Form Resets & Date/Time Glitches
- **Primary Files**:
  - `crusource-crm-frontend/src/hooks/useTaskForm.ts` (Lines 28–235)
  - `crusource-crm-frontend/src/components/dashboard/tasks/TaskModal.tsx` (Lines 39–117)
  - `crusource-crm-frontend/src/components/dashboard/tasks/TaskForm.tsx` (Lines 40–43, 198–205)
  - `crusource-crm-frontend/src/components/dashboard/calendar/popovers/QuickCreateEventPopover.tsx` (Lines 95–100)
  - `crusource-crm-frontend/src/hooks/useCallForm.ts` (Lines 182–349)
  - `crusource-crm-frontend/src/components/dashboard/calls/CallsTable.tsx` (Lines 462–473, 675–680)
  - `crusource-crm-frontend/src/components/dashboard/calls/CallLogModal.tsx` (Lines 94–154)
  - `crusource-crm-frontend/src/components/dashboard/meetings/hooks/useLogMeetingForm.ts` (Lines 161–211)
  - `crusource-crm-frontend/src/components/dashboard/meetings/MeetingMinutesModal.tsx` (Lines 56–99, 236–240)
  - `crusource-crm-frontend/src/components/shared/EntityActivitiesModals.tsx` (Lines 54–96)
  - `crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx` (Lines 825–835)
  - `crusource-crm-frontend/src/components/deals/DealDetailDrawer.tsx` (Lines 613–623)
  - `crusource-crm-frontend/src/components/dashboard/sections/DashboardModals.tsx` (Lines 54–64)
  - `crusource-crm-frontend/src/components/dashboard/widgets/DashboardPriorityWorkqueueWidget.tsx` (Lines 79–96)
- **Root Cause**:
  1. **Tasks**: `useTaskForm.ts:54–120` runs `useEffect(..., [initialTask, initialTarget])` without an `initializedKeyRef` guard (contrast `MeetingOverviewTab.tsx:177–182`). `LeadDetailDrawer.tsx:826`, `DealDetailDrawer.tsx:614`, and `EntityActivitiesModals.tsx:60` construct inline `target` / `initialTarget` object literals on every render, resetting the open Task form on any background refetch. Conversely, `TaskModal.tsx:57` passes `isOpen && taskToEdit ? taskToEdit : null`, which stays `null -> null` across closing and reopening "Create Task", leaving cancelled edits stale; `TaskModal.tsx:99–107` also locks `mode` on reopen if `taskToEdit` ref didn't change, and `TaskForm.tsx:40–43` has dead-code `isReminderInvalid` that hides why Save is disabled when `reminderEnabled` is checked before picking `dueDate`.
  2. **Calls & Meetings**: `useCallForm.ts:182–349` and `useLogMeetingForm.ts:161–211` depend on `[..., users, currentUser, defaultOwnerId, formatDateTimeLocal]` without `initializedKeyRef`, wiping user-entered subject, dates, times, and minutes when async queries or inline targets update. `CallsTable.tsx:678` turns `callToEdit.id = ""` into `null`, opening "Log Call" in `"schedule"` mode. `CallLogModal.tsx` and `MeetingMinutesModal.tsx` reset on parent `[call]`/`[meeting]` refetches.
- **Architectural Solution**:
  - Adopt the `initializedKeyRef` pattern from `MeetingOverviewTab.tsx:177–182` across `useTaskForm`, `useCallForm`, `useLogMeetingForm`, `CallLogModal`, and `MeetingMinutesModal`, resetting the ref when `!isOpen` so Create/Edit always initializes once per open and resets cleanly on reopen.
  - Memoize `target` props in `EntityActivitiesModals`, `LeadDetailDrawer`, `DealDetailDrawer`, `DashboardModals`, and `DashboardPriorityWorkqueueWidget`.
  - Fix `TaskForm.tsx` reminder validation display, auto-fill `reminderDateTime` when `dueDate` is picked after checking Reminder, honor `calendar.selectedDate` for Tasks, use `currentUser?.id` for default task owner, and pass explicit `defaultMode` from `CallsTable.tsx`.

---

### FORM-03 & FORM-04: Sales, Campaigns, Email, TeamSpace & Admin Modal Reactivity
- **Primary Files**:
  - `crusource-crm-frontend/src/components/leads/AddLeadModal.tsx` (Lines 192–268)
  - `crusource-crm-frontend/src/components/deals/AddDealModal.tsx` (Lines 202–257)
  - `crusource-crm-frontend/src/components/leads/ConvertLeadModal.tsx` (Lines 78–93)
  - `crusource-crm-frontend/src/components/leads/BulkConvertModal.tsx` (Lines 83–94)
  - `crusource-crm-frontend/src/components/contacts/AddContactModal.tsx` (Lines 97–127)
  - `crusource-crm-frontend/src/components/accounts/AddAccountModal.tsx` (Lines 95–115)
  - `crusource-crm-frontend/src/components/dashboard/inbox/CreateContactModal.tsx` (Lines 40–83)
  - `crusource-crm-frontend/src/components/campaigns/composer/popovers/ScheduleCampaignPopover.tsx` (Lines 28–44, 94–103)
  - `crusource-crm-frontend/src/components/shared/email-composer/hooks/useEmailComposerState.ts` (Lines 128–154)
  - `crusource-crm-frontend/src/components/shared/template-modal/hooks/useTemplateFormState.ts` (Lines 84–113)
  - `crusource-crm-frontend/src/components/teamspace/dashboard/CreateGoalModal.tsx` (Lines 69–82)
  - Admin modals: `CreateRoleModal.tsx` (`L59–81`), `EditRoleModal.tsx` (`L102–111`), `EditTeamModal.tsx` (`L62–72`), `pipeline/EditPipelineModal.tsx` (`L36–43`), `pipeline/CreateStageModal.tsx` (`L43–51`), `CreateApprovalRuleModal.tsx` (`L92–112`), `TemplateEditorModal.tsx` (`L87–120`), `UserEditForm.tsx` (`L77–90`)
- **Root Cause**:
  - `AddLeadModal.tsx` and `AddDealModal.tsx` overwrite restored `useFormDraft` values immediately on open, and `AddLeadModal` / `ConvertLeadModal` / `BulkConvertModal` reset user inputs when lazy `usePipelines({ enabled: isOpen })` resolves.
  - `AddContactModal`, `AddAccountModal`, Inbox `CreateContactModal`, `CreateRoleModal`, and Edit modals reset on background refetches or omit `isOpen` guards, leaving cancelled form values stale on reopen (`ScheduleCampaignPopover`, `useEmailComposerState`, `CreateGoalModal`, `CreateStageModal`, `CreateApprovalRuleModal`, `EditPipelineModal`).
- **Architectural Solution**:
  - Apply `prevIsOpenRef` / `initializedKeyRef` guards consistently, separate async default selection (`setValue("pipeline_id", ...)` when still empty) from full-form `reset(...)`, preserve `useFormDraft` restores on open, clear `useEmailComposerState` `subject`/editor on close/open, and use workspace timezone formatting in `ScheduleCampaignPopover`.

---

### EXP-01, EXP-02 & EXP-03: Export 422 Fix, Full-Record & Full-Field Exports
- **Primary Files**:
  - `crusource-crm-backend/src/modules/exports/services/export_columns.py` (Lines 84–158, 192–235)
  - `crusource-crm-frontend/src/components/leads/LeadBoard.tsx` (Lines 473–543)
  - `crusource-crm-frontend/src/components/leads/board/leadBoardConfig.ts` (Lines 16–53)
  - `crusource-crm-frontend/src/lib/exportColumns.ts` (Lines 17–105, 175–255)
  - `crusource-crm-frontend/src/app/dashboard/deals/page.tsx` (Lines 379–448)
  - `crusource-crm-frontend/src/app/dashboard/contacts/page.tsx` (Lines 235–317) & `crusource-crm-backend/src/modules/contacts/routes/contacts_routes.py`
  - `crusource-crm-frontend/src/app/dashboard/accounts/page.tsx` (Lines 156–169, 252–334)
  - `crusource-crm-frontend/src/components/dashboard/calls/CallsTable.tsx` (Lines 305–331, 513–520)
  - `crusource-crm-frontend/src/components/dashboard/meetings/MeetingsTable.tsx` (Lines 226–255)
  - `crusource-crm-frontend/src/components/teamspace/TeamspaceExportDialog.tsx` & `crusource-crm-backend/src/modules/approvals/services/governed_actions.py` (Lines 417–446)
- **Root Cause**:
  1. **`422 "Invalid export columns"`**: `LeadBoard.tsx:497` sends `ALL_COLUMNS` containing `ai_priority_score` (`leadBoardConfig.ts:41`) to `POST /api/v1/export-downloads`, while `FIELDS["leads"]` in `export_columns.py:84–126` lacks `ai_priority_score`, causing `allowed_columns()` (L148) to raise HTTP 422 on all backend Lead exports (`all`, `filtered`, `selectAllMatching`).
  2. **Missing/Empty Lead Fields**: `export_columns.py:213` hardcodes `if key == "alternative_numbers": return ""`, `LEAD_COLUMN_ACCESSORS` (`exportColumns.ts:17–44`) omits `alternative_numbers`, `ai_priority_score`, `currency`, `owner_name`, and `updated_at`, and `ALL_COLUMNS` (`leadBoardConfig.ts`) omits separate `first_name`, `last_name`, `currency`, `owner_name`, and `updated_at` needed to include every field from `AddLeadModal.tsx` and the `Lead` model (`models.py:48–118`). (Note: `Lead` model uses `Lead.company`, not `company_name`.)
  3. **Other Modules**:
     - `LeadBoard.tsx:509` and `deals/page.tsx` export 0 rows on `current_view` in Kanban mode because list queries are disabled.
     - `deals/page.tsx:399` sends raw `filters` (`pipeline_id: "all"`) instead of `activeFilters` (causing 422 UUID validation error) and omits `win_probability`, `loss_reason`, `loss_notes`, `updated_at`.
     - `contacts` table/export ignores `contact_source` and `searchBy` filters and omits `first_name`, `last_name`, `updated_at`.
     - `accounts/page.tsx:156–169` omits `status` and `parent_account_name` from `ALL_COLUMNS`.
     - `CallsTable.tsx:513–520` skips `ExportOptionsModal` (hardcoding CSV and blocking `all`, `current_view`, `xlsx`); `MeetingsTable.tsx:235–242` makes `current_view` identical to `filtered` and omits meeting form fields; `governed_actions.py:438–442` exports raw UUIDs and Python list repr strings.
- **Architectural Solution**:
  - Synchronize `FIELDS["leads"]`, `LEAD_COLUMN_ACCESSORS`, and `ALL_COLUMNS` (`leadBoardConfig.ts`) with all `AddLeadModal` & `Lead` model fields, fix `alternative_numbers` serialization (`export_columns.py:213`), support `owner_name` and `ai_priority_score`, and route Kanban `current_view` exports properly.
  - Fix Deals `activeFilters`, Accounts missing `status`/`parent_account_name`, Contacts filter/export parity, Calls `ExportOptionsModal`, Meetings `current_view` & fields, and TeamSpace governed export formatting.

---

### STAT-01 & STAT-02: Duplicate Lead Status Badges & Status/Stage Desynchronization
- **Primary Files**:
  - `crusource-crm-frontend/src/components/leads/LeadList.tsx` (Lines 587–609)
  - `crusource-crm-frontend/src/components/leads/drawer/LeadStageStepper.tsx` (Lines 51–101)
  - `crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx` (Lines 212–232, 378–390, 430–437)
  - `crusource-crm-frontend/src/components/leads/FilterPanel.tsx` (Lines 253–285)
  - `crusource-crm-frontend/src/components/teamspace/pool/PoolFilters.tsx` (Lines 43–51)
  - `crusource-crm-backend/src/modules/leads/handlers/create_lead_handler.py` (Lines 43–83)
  - `crusource-crm-backend/src/modules/leads/handlers/update_lead_handler.py` (Lines 54–60, 144–180)
- **Root Cause**:
  1. `LeadList.tsx:597–601` renders a second gray `lead.stage_name` pill whenever `!visibleColumns.includes("stage") && lead.stage_name`, without checking whether `lead.stage_name` already matches the status badge (`Contacted` / `Not Contacted`), producing `[Contacted] [Contacted]` in Sales Leads and TeamSpace Pool Leads (`PoolLeadsTab.tsx`).
  2. `create_lead_handler.py:43–83` never calls `_infer_lead_status_from_stage(stage_obj)` when a Lead is created with an explicit `stage_id`, leaving `status = "not_contacted"` even when created in `"Contacted"` or `"Qualified"`.
  3. `update_lead_handler.py:160–180` leaves `stage_id` pointing at the old pipeline stage when `status` is set to an outcome status (`contact_in_future`, `not_qualified`, `lost_lead`, `junk_lead`), and `LeadDetailDrawer.tsx:385` only updates `{ status: newStatus }`, so the drawer header shows `CONTACT IN FUTURE` while `LeadStageStepper.tsx:57–60` shows `Current: Attempted to Contact`.
- **Architectural Solution**:
  - Deduplicate the status + stage cell in `LeadList.tsx:587–602` so the secondary stage pill renders only for non-outcome leads whose custom stage name differs (case/slug-insensitive) from the rendered status label.
  - Reuse `_infer_lead_status_from_stage` inside `create_lead_handler.py` when `stage_id` is supplied without explicit `status`.
  - When `lead.status` is a non-pipeline outcome status (`contact_in_future`, `not_qualified`, `lost_lead`, `junk_lead`), display that outcome state accurately in `LeadStageStepper.tsx` and keep `stage_id` intact for "Reopen Lead" recovery, while surfacing outcome status filters in `FilterPanel.tsx` and adding `lost_lead` to `PoolFilters.tsx`.

---

## 3. Eight-Phase Master Implementation Roadmap

```mermaid
flowchart TD
    subgraph Wave 1: Presentation & Governance Baseline
        W1P1["Phase 1: SEC-01 Decision, SEC-02/03/05, DOC-01"]
        W1P2["Phase 2: SALES-01/02, ACT-01"]
        W1P3["Phase 3: SEC-04 Decision, ALIGN-01/02"]
        W1P4["Phase 4: UI-01, FIN-01, UX-01"]
        W1P1 --> W1P2 --> W1P3 --> W1P4
    end

    subgraph Wave 2: Timeline, Forms, Exports & Lead Status Fidelity
        P5["Phase 5: Timeline Continuity (TIME-01 to TIME-05)"]
        P6["Phase 6: CRM-Wide Form Reactivity (FORM-01 to FORM-04)"]
        P7["Phase 7: Full-Field & Full-Record Exports (EXP-01 to EXP-03)"]
        P8["Phase 8: Status/Stage Deduplication & Sync (STAT-01 to STAT-02)"]
        P5 --> P6 --> P7 --> P8
    end

    W1P4 --> P5
```

---

## 4. Comprehensive Dependency & Cross-Module Verification Audit

### Double-Check Verification Matrix (Wave 1 + Wave 2)

| Fix ID | Target Component | Dependent Modules To Verify | Potential Regression Risk | Planned Guard / Verification |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Scope behavior decision; only then the affected query boundary | • Personal lists<br>• Meetings and attendees<br>• Teamspace pool<br>• Recycle Bin soft-delete | Expanding personal view could expose records outside the intended assignment/team boundary | Confirm product semantics first. Keep personal assignment scope and Teamspace projection separate unless an approved contract defines otherwise. |
| **SEC-02** | `delete_user_command.py` | • `user_admin_repository.reassign_all_crm_records`<br>• `Team.manager_id` | HTTP 422 on deleting user who owns records in multiple teams | Verify `reassign_all_crm_records` safely normalizes `record_team_id` (`test_roles_hierarchy.py`). |
| **SEC-03** | `single_invite_command.py` | • `RoleNode.default_profile_id`<br>• Invitation email dispatcher | Invited user has null profile | Validate `default_profile_id` during invite creation (`test_invitations`). |
| **SEC-04** | Export controls | • TeamSpace governed actions<br>• Personal module export permissions | Wrong permission model bypasses export policy | Reuse existing TeamSpace governed-action contract; decide personal approval policy separately. |
| **SEC-05** | Requests Inbox route & APIs | • Profile setup permissions<br>• Sidebar count badge<br>• Access/reassignment requests | `teams_pool` accidentally exposes inbox | Require `teams_requests` at navigation, page, and API boundaries (`test:teamspace:requests:browser`). |
| **TIME-01** | `timelineUtils.ts`, `update_*_handler.py`, `note_page_repository.py` | • `LeadNotesTab`, `DealNotesTab`, `NotesSection`, `PoolNotesTab`<br>• `timeline` filters (`all`, `system`, `note`, `document`) | Hiding real user notes or showing `"System: ..."` notes in Notes tabs; duplicate stage notes if both frontend & backend create notes | Apply `exclude_system` SQL param only to Notes tab queries (keep `False` for Timeline); move stage/update note creation to backend and remove redundant frontend `NotesService.createNote` calls; strip `*(Migrated from Lead)*` before checking `startsWith("System:")`. |
| **TIME-02** | `timelineUtils.ts`, `activity_timeline_service.py` | • `LeadDetailDrawer`, `DealDetailDrawer`, `ContactDetailDrawer`, `AccountDetailDrawer`<br>• Global `/timeline` feed & `useGlobalTimeline` | Completed meetings/tasks hiding their original creation date, or past meetings losing end times | Emit separate creation vs completion/cancellation events when timestamps differ; keep `"Scheduled for ..."` in description while sorting/timestamping scheduled activities by `created_at`. |
| **TIME-03** | `update_lead_handler.py`, `update_deal_handler.py`, `update_contact_handler.py`, `update_account_handler.py`, `cacheInvalidation.ts` | • Bulk update / import commands<br>• Stage progression rules<br>• Approval-gated updates | Flooding timeline with internal metadata noise (e.g. `version`, `stage_entered_at`, `updated_at`) | Whitelist meaningful business/profile fields in `timeline_note_logger.py` and keep concise field labels per patch; invalidate `queryKeys.notes.all()` and `queryKeys.timeline.all()` across entity invalidators. |
| **TIME-04** | `useDocumentBatchUpload.ts`, `DocumentsWidget.tsx`, `useDocuments.ts`, `useDocumentMutations.ts`, `assign_document_handler.py` | • `StageDocumentRule` checklist on Deal<br>• Recycle Bin restore<br>• Document versions | Suppressing upload timeline cards when a document is later updated/deleted; missing `meeting_id`/`task_id`/`call_id` assignment notes | Check upload-specific note matching in `timelineUtils.ts:429`; invalidate `["notes"]` & `["timeline"]` on every upload, edit, assign, delete, and restore mutation. |
| **TIME-05** | `artifact_migrator.py`, `task_page_repository.py`, `meeting_page_repository.py`, `calls_repository.py`, `execute_conversion_handler.py` | • Standard & Inbox lead conversion<br>• Teamspace RBAC (`apply_scope`)<br>• Converted Lead read-only drawer | Exposing records across org boundaries when loosening `record_team_id` filter; breaking Deal-Contact activity deduplication | Always keep `org_id == org_id` and `apply_scope` enforcement; use distinct record queries in `AccountDetailDrawer` so Contact + Account activities don't duplicate or vanish when a Deal exists; route Inbox conversion through `ArtifactMigrator`. |
| **FORM-01..04** | `useTaskForm.ts`, `useCallForm.ts`, `useLogMeetingForm.ts`, `AddLeadModal.tsx`, `AddDealModal.tsx`, Admin modals | • `useFormDraft` localStorage persistence<br>• Calendar quick-create (`selectedDate`)<br>• Save & New reset flow | Cancelled form state leaking across opens, OR async query resolution overwriting user edits mid-typing | Key `initializedKeyRef` on `isOpen` + entity ID + target ID; reset ref on close; check localStorage draft presence before resetting defaults in `AddLeadModal`/`AddDealModal`; update empty async defaults (like `pipeline_id`, `defaultOwnerId`) cleanly without full `reset()`. |
| **EXP-01..03** | `export_columns.py`, `exportColumns.ts`, `leadBoardConfig.ts`, `deals/page.tsx`, `contacts/page.tsx`, `accounts/page.tsx`, `CallsTable.tsx`, `TeamspaceExportDialog.tsx` | • Backend FLS (`field_access` masking)<br>• Governed TeamSpace exports (`governed_actions.py`)<br>• TeamSpace Pool exports (`usePoolColumns.ts`) | FLS mask accidentally stripped if backend column mapping doesn't map export column ID to underlying FLS field name | Map every added export column in `FIELDS[module]` (`export_columns.py`) to its FLS field tuple (e.g., `ai_priority_score=("ai_priority_score",)`, `owner_name=("owner_id",)`, `currency=("currency",)`, `updated_at=("updated_at",)`). |
| **STAT-01..02** | `LeadList.tsx`, `LeadDetailDrawer.tsx`, `LeadStageStepper.tsx`, `create_lead_handler.py`, `update_lead_handler.py`, `FilterPanel.tsx`, `PoolFilters.tsx` | • `PoolLeadsTab.tsx`<br>• `KanbanBoard.tsx` stage queries<br>• `Reopen Lead` flow | Outcome statuses (`contact_in_future`, `lost_lead`) losing recovery stage reference if `stage_id` is cleared prematurely | Preserve `stage_id` in DB for `Reopen Lead` recovery while rendering the outcome status clearly in `LeadStageStepper` and suppressing duplicate/conflicting stage pills in `LeadList`. |

---

## 5. Step-by-Step Implementation Guide (Wave 1 Baseline + Wave 2 Pending Plan)

### Phases 1–4: Wave 1 Reference Steps (Status: Implemented Locally Except `SEC-01` & `SEC-04`)
- **Phase 1**: `SEC-01` (Deferred pending product confirmation), `SEC-02` (`delete_user_command.py` & `UserRowActionMenu.tsx`), `SEC-03` (`invite_validator.py` & `BulkInviteModal.tsx`), `SEC-05` (`sidebarConfig.ts`, `Sidebar.tsx`, `TeamspaceRequestsSection.tsx`, `profiles/guards.py`), `DOC-01` (`models.py`, Alembic enum migration, `documents.service.ts`, `UploadDocumentModal.tsx`).
- **Phase 2**: `SALES-01` (`update_lead_handler.py`, `leads_repository.py`, `useLeadMutations.ts`, `LeadList.tsx`), `SALES-02` (`LeadDetailDrawer.tsx`, `LeadQuickActions.tsx`), `ACT-01` (`MeetingOverviewTab.tsx`, `MeetingScheduleFields.tsx`).
- **Phase 3**: `SEC-04` (Deferred pending personal export policy), `ALIGN-01` (`PoolFilters.tsx`, `pool_sales_query_repository.py`), `ALIGN-02` (`TeamspaceImportDialog.tsx`, `importRecords.ts`).
- **Phase 4**: `FIN-01` (`DashboardHome.tsx`, `PipelineHealthWidget.tsx`, `PipelineChart.tsx`), `UI-01` (`UsersToolbar.tsx`), `UX-01` (`apple-touch-icon.png`, `app/layout.tsx`).

---

### Phase 5 (Wave 2): Timeline Continuity, System Event Parsing & Document Sync

#### Step 5.1: Fix System Event vs User Note Classification & Notes Tab Filtering (`TIME-01`)
1. **Frontend `crusource-crm-frontend/src/lib/timelineUtils.ts` (Lines 190–305)**:
   - Before running system prefix checks at L195:
     ```ts
     const isMigrated = note.content.startsWith("*(Migrated from Lead)*\n") || note.content.includes("*(Migrated from Lead)*");
     const cleanContent = note.content.replace(/^\*\(Migrated from Lead\)\*\s*/g, "").trim();
     ```
   - Match all system event prefixes on `cleanContent` and emit `type: "system"` / `"document"` / `"conversion"` (never `"note"`):
     - `System: Stage advanced to ` -> `"Stage Advanced"` (`trending_up`, blue)
     - `System: Stage regressed to ` -> `"Stage Regressed"` (`trending_down`, amber)
     - `System: Stage changed to ` -> `"Stage Updated"` (`swap_horiz`, blue)
     - `System: Lead status updated to ` -> `"Status Updated"` (`flag`, purple)
     - `System: Deal marked as Closed Lost` or `Deal moved to Closed Lost` -> `"Deal Closed Lost"` (`cancel`, rose)
     - `System: Lead updated:` / `Deal updated:` / `Contact updated:` / `Account updated:` -> `"${entityLabel} Updated"` (`edit_note`, slate)
     - `System: Owner changed to ` -> `"Owner Changed"` (`person_check`, indigo)
     - `System: Lead created` -> `"Lead Created"` (`person_add`, green)
     - `System: Migrated ` -> `"Activities Migrated from Lead"` (`sync_alt`, emerald)
     - `System: Document transferred from Lead:` -> `"Document Transferred from Lead"` (`type: "document"`, `folder_shared`, teal)
     - `System: Document restored:` -> `"Document Restored"` (`type: "document"`, `restore_from_trash`, emerald)
     - Catch-all `else if (cleanContent.startsWith("System:"))` -> `"System Activity"` (`info`, slate) so no `"System: ..."` message can ever fall through to `"Note by <user>"`.
2. **Backend & Frontend Notes Tab Filtering**:
   - In `crusource-crm-backend/src/modules/notes/routes/notes_routes.py`, `queries/note_page_queries.py`, and `repositories/note_page_repository.py:9–21`, add optional `exclude_system: bool = False`. When `True`, add SQL `~Note.content.like("System:%")` and `~Note.content.like("*(Migrated from Lead)*\nSystem:%")`. Enable `exclude_system: true` from `LeadNotesTab`, `DealNotesTab`, and `NotesSection`, while leaving the default `exclude_system: false` for Timeline queries.
   - In `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolNotesTab.tsx:59–74`, exclude `"System:"` notes from the Notes tab display.
   - In `crusource-crm-frontend/src/components/deals/kanban/useDealsKanbanState.ts:210–218` and `DealDetailDrawer.tsx:354–358`, standardize Closed Lost notes to start with `"System: Deal marked as Closed Lost..."`.

#### Step 5.2: Fix Meeting, Call & Task Timeline Timestamps (`TIME-02`)
1. **Frontend `crusource-crm-frontend/src/lib/timelineUtils.ts` (Lines 308–423)**:
   - **Meetings (L352–423)**:
     - Emit `"Meeting Scheduled: ${meeting.title}"` at `meeting.created_at || meeting.start_time` (so the 3:30 PM scheduling action for a 4:00 PM meeting sorts at 3:30 PM and shows `3:30 pm` on the right, with `Scheduled for 4:00 pm` in the description).
     - When `normStatus === "rescheduled"`, emit at `meeting.updated_at || meeting.created_at || meeting.start_time`.
     - When `normStatus === "completed"` or `"cancelled"`, emit the completion/cancellation event at `meeting.completed_at` / `meeting.cancelled_at` / `meeting.updated_at`, AND if `meeting.created_at` exists and differs by > 1s, also emit the original `"Meeting Scheduled"` event at `meeting.created_at`.
   - **Calls (L330–350)**:
     - If `call.outgoingCallStatus?.toLowerCase() === "scheduled"`, title `"Call Scheduled: ${call.subject}"`, put `"Scheduled for ${formatDateFn(call.callStartDateTime)}"` in description, and use `call.createdTime || call.callStartDateTime` as `rawDateStr`. Otherwise use `call.createdTime || call.callStartDateTime`.
   - **Tasks (L308–327)**:
     - Always emit `"Task Assigned: ${task.subject}"` at `task.createdTime` (showing `Due: ...` in description).
     - If `task.status === "Completed"` and `task.closedTime`, emit a separate `"Task Completed: ${task.subject}"` event at `task.closedTime`.
2. **Backend `crusource-crm-backend/src/shared/services/activity_timeline_service.py` (Line 133)**:
   - Use `m.created_at or m.start_time` as the primary event `timestamp` for scheduled meetings and include `scheduled_for` in metadata.

#### Step 5.3: Log Entity Field Updates & Consolidate Backend Stage/Update Notes (`TIME-03`)
1. Create `crusource-crm-backend/src/shared/audit/timeline_note_logger.py` with `record_entity_update_timeline_note(...)`:
   - Inspects `old_state` vs `update_data` for business/profile fields (excluding noisy system columns `version`, `updated_at`, `stage_entered_at`, `ai_priority_*`).
   - Emits `"System: Owner changed to <new_owner_name>"` when `owner_id` / `deal_owner_id` changes.
   - Emits `"System: Stage advanced to <name>"` / `"System: Stage regressed to <name>"` / `"System: Stage changed to <name>"` (comparing `PipelineStage.sort_order`) or `"System: Lead status updated to <label>"` when stage/status changes; when `stage_id` changes in `update_lead_handler.py` and `_infer_lead_status_from_stage` simultaneously syncs `status`, emit only the stage note (never duplicate status/field-update notes), and when a Deal transitions to `closed_lost`, combine `loss_reason` into `"System: Deal marked as Closed Lost (Reason: <reason>)"`.
   - Emits `"System: <Entity> updated: <Humanized Field List>"` when any remaining non-stage profile/business fields change.
2. Call `record_entity_update_timeline_note` in:
   - `update_lead_handler.py` (`UpdateLeadCommandHandler.handle`)
   - `update_deal_handler.py` (`UpdateDealCommandHandler.handle` — also covering `DealsTable.tsx:130–155` quick stage actions automatically)
   - `update_contact_handler.py` (`UpdateContactCommandHandler.handle`)
   - `update_account_handler.py` (`UpdateAccountCommandHandler.handle`)
3. Remove redundant frontend `NotesService.createNote` / `createNoteMutation` calls in `useLeadMutations.ts:188–192,299–303`, `DealDetailDrawer.tsx:243–247,276–280,354–358`, and `useDealsKanbanState.ts:210–218` to prevent duplicate notes and keep Table/Kanban/Drawer stage updates consistent.
4. Update `crusource-crm-frontend/src/lib/cacheInvalidation.ts`: invalidate `queryKeys.notes.all()` and `queryKeys.timeline.all()` in `invalidateLeads`, `invalidateDeals`, `invalidateContacts`, and `invalidateAccounts`.

#### Step 5.4: Live Document Sync in Timelines (`TIME-04`)
1. **Frontend Cache Invalidation**:
   - In `crusource-crm-frontend/src/hooks/useDocumentBatchUpload.ts:19`, invalidate `["documents"]`, `["notes"]`, `["timeline"]`, `["globalTimeline"]`, `["leads"]`, `["deals"]`, `["contacts"]`, and `["accounts"]`.
   - In `crusource-crm-frontend/src/components/documents/DocumentsWidget.tsx:127,162–166,581–591`, invalidate `["notes"]` and `["timeline"]` after `handleFilePicked`, `handleDelete`, `onDocumentUpdated`, and `onContentUpdated`.
   - In `crusource-crm-frontend/src/hooks/useDocuments.ts:99–130` and `src/hooks/queries/documents/useDocumentMutations.ts:51–134,249–251`, invalidate `["notes"]` and `["timeline"]` on metadata update, content save, soft delete, and restore.
   - In `crusource-crm-frontend/src/lib/timelineUtils.ts:429–431`, restrict `alreadyHasNote` to match upload/assign/transfer notes (`"Document uploaded:"`, `"Uploaded document"`, `"Document assigned:"`, or `"transferred from Lead:"`) mentioning `doc.file_name` so later modify/delete/restore notes never suppress the original upload entry.
2. **Backend Document Notes**:
   - In `assign_document_handler.py:50–55`, include `("Meeting", update_data.get("meeting_id"))`, `("Task", update_data.get("task_id"))`, and `("Call", update_data.get("call_id"))`.
   - In `version_handlers.py:84–137` and `update_binary_content_handler.py:23–91`, log `"System: Document modified: {doc.file_name}"` notes for all linked parents.
   - In `recycle_bin_handlers.py:17–27`, log `"System: Document restored: {doc.file_name}"` notes for all linked parents.

#### Step 5.5: Zero-Loss Lead Conversion Timeline Continuity (`TIME-05`)
1. **Backend `crusource-crm-backend/src/shared/services/lead_conversion/artifact_migrator.py` & `service.py`**:
   - Add `deal_id: Optional[uuid.UUID] = None` (keeping `include_deal: bool = False` for backward compatibility) to `migrate_lead_notes(...)`, and update all callers (`convert_lead_handler.py:90`, `bulk_convert_handler.py:82`, `inbox/services/lead_conversion_service.py:94`) to pass `deal_id=deal_id`. Clone all Lead `Note` rows (`created_at`, `created_by` preserved) to `Contact`, `Account`, **and `Deal`**; create a baseline Lead creation origin note (`created_at=lead.created_at`) and conversion note on all involved entities.
   - In `migrate_lead_activities(...)` and `migrate_lead_documents(...)`: remove the overly strict `record_team_id == team_id` SQL filter (preserve `org_id` filter) so activities/documents with differing or null team IDs are never silently dropped; also include Calls linked via `Call.related_to_type == "Lead"`.
   - Preserve Lead timeline visibility on converted Leads non-destructively (do **not** clone active `Task`, `Call`, or `Meeting` DB rows onto Contact/Account/Deal, which would duplicate active work items; instead preserve historical Lead Notes + conversion timeline visibility) and propagate activities to Account even when a Deal is created:
     - In `task_page_repository.py:18–19`: match `or_(Task.related_to_id == params.parent_id, Task.account_id == params.parent_id)` so `AccountDetailDrawer` displays Tasks owned via `account_id`.
     - In `calls_repository.py` and `meeting_page_repository.py` (and/or `AccountDetailDrawer.tsx`): allow Account timelines/drawers to include Calls and Meetings linked to the Account's Contacts and converted Deals without hiding them when a Deal exists.
2. **Backend Inbox Conversion (`crusource-crm-backend/src/modules/inbox/handlers/execute_conversion_handler.py` & `inbox/services/lead_conversion_service.py`)**:
   - Delegate note, document, and activity migration to `ArtifactMigrator.migrate_lead_activities`, `migrate_lead_notes`, and `migrate_lead_documents` so Inbox conversion never leaves Tasks/Calls/Meetings or Deal/Account notes behind.
3. **Frontend `crusource-crm-frontend/src/lib/cacheInvalidation.ts:86–101`**:
   - Add `notes`, `tasks`, `calls`, `meetings`, and `documents` invalidation inside `invalidateLeadConversion`.

---

### Phase 6 (Wave 2): CRM-Wide Form Reset Prevention & Scheduling UX

#### Step 6.1: Fix Task Modal Form Reset & Reminder/Date UX (`FORM-01`)
1. Update `crusource-crm-frontend/src/hooks/useTaskForm.ts` and `src/components/dashboard/tasks/TaskModal.tsx`:
   - Pass `isOpen` and Redux `state.calendar?.selectedDate` into `useTaskForm`.
   - Guard initialization with `initializedKeyRef = useRef<string | null>(null)` keyed on `${initialTask?.id || "new"}:${initialTarget?.type || ""}:${initialTarget?.id || ""}:${calendarSelectedDate || ""}`; reset `initializedKeyRef.current = null` when `!isOpen` so closing and reopening Create Task resets the form cleanly and background refetches never wipe typing.
   - In `TaskModal.tsx:99–107`, depend on `[isOpen, taskToEdit?.id, initialMode]` so reopening the same task resets `mode` back to `initialMode`.
   - When creating a task with `reminderEnabled = true` and empty `dueDate`, automatically set `reminderDateTime = "${newDueDate}T09:00"` when `dueDate` is later chosen, without clobbering custom `reminderDateTime` values.
   - Expose `isReminderInvalid` from `useTaskForm` to `TaskForm.tsx` (replacing the dead code at L40–43) and display inline validation feedback on the Reminder date/time field.
   - Use workspace timezone helpers and `currentUser?.id` for `dueDate`/`reminderDateTime`/`taskOwner`.

#### Step 6.2: Fix Calls & Log-Meeting Form Resets (`FORM-02`)
1. Add `initializedKeyRef` guards in `useCallForm.ts:182–349`, `useLogMeetingForm.ts:161–211`, `CallLogModal.tsx:94–154`, and `MeetingMinutesModal.tsx:56–99` (plus targeted effect to fill `callOwnerId` if still empty when `defaultOwnerId` arrives).
2. Fix `CallsTable.tsx:462–473,675–680` to pass explicit `defaultMode` (`"log"` vs `"schedule"`) so clicking "Log Call" opens in Log mode.
3. Memoize inline `target` / `initialCallFor` props in `EntityActivitiesModals.tsx`, `LeadDetailDrawer.tsx:825–835`, `DealDetailDrawer.tsx:613–623`, `DashboardModals.tsx:54–64`, and `src/components/dashboard/widgets/DashboardPriorityWorkqueueWidget.tsx:79–96`.

#### Step 6.3: Fix Sales Entity, Campaign, Email & Admin Modals (`FORM-03`, `FORM-04`)
1. Add `prevIsOpenRef` / `initializedKeyRef` guards and preserve `useFormDraft` restores in `AddLeadModal.tsx`, `AddDealModal.tsx`, `ConvertLeadModal.tsx`, and `BulkConvertModal.tsx` (setting default `pipeline_id` via `setValue` only while empty).
2. Add `prevIsOpenRef` / `initializedKeyRef` and clean close resets in `AddContactModal.tsx`, `AddAccountModal.tsx`, Inbox `CreateContactModal.tsx`, `ScheduleCampaignPopover.tsx` (with workspace timezone conversion), `useEmailComposerState.ts` (clearing `subject` and `editor` on open), `useTemplateFormState.ts`, `CreateGoalModal.tsx`, and the 8 Admin modals (`CreateRoleModal`, `EditRoleModal`, `EditTeamModal`, `pipeline/EditPipelineModal`, `pipeline/CreateStageModal`, `CreateApprovalRuleModal`, `TemplateEditorModal`, `UserEditForm`).

---

### Phase 7 (Wave 2): Full-Record & Full-Field Exports Across CRM

#### Step 7.1: Fix Lead Export HTTP 422 & Export All Form/Model Fields (`EXP-01`)
1. Edit `crusource-crm-backend/src/modules/exports/services/export_columns.py`:
   - Add `"ai_priority_score": ("ai_priority_score",)`, `"ai_priority_band": ("ai_priority_band",)`, `"currency": ("currency",)`, `"owner_name": ("owner_id",)`, and `"updated_at": ("updated_at",)` to `FIELDS["leads"]`.
   - Remove line 213's hardcoded `if key == "alternative_numbers": return ""` so `item.alternative_numbers` serializes comma-joined values cleanly (`L287–289`).
   - Return `item.owner_name or ""` for `owner_name` in `cell()`.
2. Edit `crusource-crm-frontend/src/components/leads/board/leadBoardConfig.ts` and `src/lib/exportColumns.ts`:
   - Add `first_name`, `last_name`, `currency`, `owner_name`, and `updated_at` to `ALL_COLUMNS` (or full export columns) so every Add/Edit Lead form & model field is exported.
   - Add accessors for `alternative_numbers`, `ai_priority_score`, `currency`, `owner_name`, and `updated_at` to `LEAD_COLUMN_ACCESSORS`.
   - Fix `LeadBoard.tsx` Kanban `current_view` export so it exports active matching rows instead of an empty `leadsList`.

#### Step 7.2: Cross-Module Export Scope & Field Parity (`EXP-02`, `EXP-03`)
1. **Deals (`src/app/dashboard/deals/page.tsx:399`, `dealColumns.ts`, `exportColumns.ts`)**: use `activeFilters` in `filtered` export (eliminating `pipeline_id=all` HTTP 422), pass `currentViewCount`, handle Kanban `current_view`, and add `win_probability`, `loss_reason`, `loss_notes`, `updated_at`.
2. **Contacts (`src/app/dashboard/contacts/page.tsx`, `contacts/constants.ts`, `contacts_routes.py`)**: support `contact_source` and `searchBy` in query/export and add `first_name`, `last_name`, `updated_at`.
3. **Accounts (`src/app/dashboard/accounts/page.tsx:156–169`, `exportColumns.ts`)**: add `status`, `parent_account_name`, and `updated_at` to `ALL_COLUMNS` and `ACCOUNT_COLUMN_ACCESSORS`.
4. **Calls (`CallsTable.tsx`) & Meetings (`MeetingsTable.tsx`)**: wire `ExportOptionsModal` into `CallsTable.tsx`; separate `current_view` from `filtered` in `MeetingsTable.tsx` and add missing Meeting/Call model fields to `FIELDS` & `exportColumns.ts`.
5. **TeamSpace (`TeamspaceExportDialog.tsx` & `governed_actions.py:438–442`)**: add missing exportable columns (`alternative_numbers`, `pipeline_id`, `stage_id`, `ai_priority_score`, `loss_reason`, `attendees`) and format foreign-key display names and list arrays instead of raw UUIDs / Python repr strings.

---

### Phase 8 (Wave 2): Duplicate Lead Status Elimination & Lifecycle Stage Synchronization

#### Step 8.1: Deduplicate `LeadList.tsx` Status & Stage Badges (`STAT-01`)
- Edit `crusource-crm-frontend/src/components/leads/LeadList.tsx:587–602`:
  - Render the secondary `lead.stage_name` pill **only** when `!visibleColumns.includes("stage") && Boolean(lead.stage_name)` AND normalized `lead.stage_name` differs from both `lead.status` and the translated `statusText` AND `lead.status` is not an outcome status (`contact_in_future`, `not_qualified`, `lost_lead`, `junk_lead`, `converted`).

#### Step 8.2: Synchronize Lead Creation, Outcome Status Transitions & Filters (`STAT-02`)
1. Edit `crusource-crm-backend/src/modules/leads/handlers/create_lead_handler.py`:
   - After `resolve_lead_pipeline` resolves `stage_id`, if `status` was not explicitly provided in `lead_data`, look up `PipelineStage` and set `status` via `_infer_lead_status_from_stage(stage_obj)` before creating the Lead.
2. Edit `crusource-crm-frontend/src/components/leads/drawer/LeadStageStepper.tsx:57–61` and `LeadDetailDrawer.tsx:378–390`:
   - In `LeadStageStepper.tsx`, when `lead.status` is a non-pipeline outcome status (`contact_in_future`, `not_qualified`, `lost_lead`, `junk_lead`, `converted`), show `Current: ${statusLabel(lead.status)}` instead of a stale pipeline stage name (`Attempted to Contact`), while preserving `stage_id` on the backend for `Reopen Lead`.
   - In `LeadDetailDrawer.tsx:381–385` (`handleSetStatus`), apply the full API response to `onLeadUpdated`.
3. Edit `crusource-crm-frontend/src/components/leads/FilterPanel.tsx:253–285` and `src/components/teamspace/pool/PoolFilters.tsx:43–51`:
   - Add `{ value: "lost_lead", label: "Lost Lead" }` to `PoolFilters.tsx` and expose outcome status filter chips alongside pipeline stage filters in `FilterPanel.tsx`.

---

## 6. Testing, Verification & Regression Test Matrix

| Test Suite / Area | Command / Tool | Success Criteria |
| :--- | :--- | :--- |
| **SEC-01 Scope Decision** | Product decision first; if approved, add focused tests to `crusource-crm-backend/tests/` | Verify chosen personal-vs-Teamspace boundary, org isolation, and soft-delete behavior. |
| **User Hierarchy (Wave 1)** | `crusource-crm-backend/tests/test_roles_hierarchy.py`, `test_admin_bulk_invite_e2e.py`, frontend `test:admin-users`, `test:invitations` | Verify hierarchy enforcement on delete/invite and responsive toolbar. |
| **Document Categories (Wave 1)** | `crusource-crm-backend/tests/test_documents_and_s3.py`, `test_deal_stage_document_requirements.py` | Verify `sow`, `op`, `po` persistence and stage document rules. |
| **Requests Inbox Permission (Wave 1)** | Frontend `npm.cmd run test:teamspace:requests:browser`; backend `tests/test_teams_setup_permissions.py`, `test_teamspace_access_requests.py`, `test_teamspace_reassignment_requests.py`, `test_governed_teamspace_actions.py` | Standard with `teams_pool=true`, `teams_requests=false` cannot view or query inbox data. |
| **Timeline & Lead Conversion (Wave 2)** | Backend `pytest` tests for `update_*_handler`, `artifact_migrator`, `execute_conversion_handler`, `note_page_repository`, `task_page_repository`, `activity_timeline_service`; frontend unit + browser tests (`test:parent-notes:browser`, `test:global-timeline:browser`, `test:related-activities:browser`) | Stage changes render as System events (never `"Note by <user>"`); scheduled meetings sort/timestamp by `created_at`; edits/uploads/deletes appear immediately; Converted Leads retain continuity across Contact, Account, and Deal. |
| **Form Reactivity (Wave 2)** | Frontend `npm.cmd run test:leads:modal`, `test:meeting-schedule:browser`, plus new Tasks/Calls/Sales form refetch/reopen tests | Open Tasks, Calls, Meetings, and Sales forms never reset on background query refetches and cleanly reset/sync on close & reopen. |
| **Exports & Status Deduplication (Wave 2)** | Backend `pytest` export column/row tests (Leads, Deals, Contacts, Accounts, Meetings, Calls, TeamSpace); frontend `test:export-downloads:browser` & `test:sales-kanban:browser` | Zero `422 Invalid export columns`; all Add/Edit Lead & CRM form/model fields including `alternative_numbers`, `owner_name`, `ai_priority_score` export; zero duplicate badges (`[Contacted] [Contacted]`) and synced drawer header/stepper. |
| **Full Frontend & Backend CI** | Frontend: `npx.cmd tsc --noEmit`, `npx.cmd eslint`, CI test scripts in `crusource-crm-frontend/.github/workflows/ci.yml`; Backend: `.venv/Scripts/python.exe -m ruff check src`, `.venv/Scripts/python.exe -m pytest -q` | Report actual post-edit pass/fail counts across targeted and full suites without skipping failing assertions. |

### Observed Verification Runs (Post-Final Code Edits)

- **Backend Static & Migration Checks**:
  - `.\.venv\Scripts\python.exe -m ruff check src tests scripts alembic` — `All checks passed!`
  - `.\.venv\Scripts\python.exe -m compileall -q src scripts alembic` — exited `0`
  - `.\.venv\Scripts\python.exe scripts\check_migration_heads.py` — `Single Alembic migration head validated: 20261115_add_sow_op_po_doc_categories`
- **Backend Pytest Domain Batches (`585` total test runs across 5 targeted batches, with overlap across shared regression files)**:
  - **Batch A** (`tests/test_data_admin_import_validation.py tests/test_roles_hierarchy.py tests/test_admin_bulk_invite_e2e.py tests/test_documents_and_s3.py tests/test_deal_stage_document_requirements.py`): `37 passed, 2 warnings in 20.31s`
  - **Batch B** (`tests/test_teams_setup_permissions.py tests/test_teamspace_access_requests.py tests/test_teamspace_reassignment_requests.py tests/test_governed_teamspace_actions.py tests/test_notes_pagination.py`): `55 passed, 2 warnings in 35.46s`
  - **Batch C** (`tests/test_wave2_timeline_exports_status.py tests/test_export_downloads.py tests/test_csv_export.py tests/test_entity_meeting_timeline.py tests/test_leads_conversion.py tests/test_leads_filtering.py tests/test_deals_filtering.py tests/test_deals_stage_machine.py tests/test_global_notes.py tests/test_notes_parent_authorization.py tests/test_meeting_schedule_context.py tests/test_meeting_timezones.py tests/test_calls.py tests/test_contacts_enhancement.py tests/test_accounts_enhancement.py tests/test_data_admin_import_validation.py tests/test_bulk_import_all_modules.py tests/test_saved_views.py tests/test_deal_required_fields.py tests/test_binary_content_handlers.py tests/test_pipeline_leads_and_stage_deletion.py`): `263 passed, 4 warnings in 33.05s`
  - **Batch D** (`tests/test_sales_activities_phase2.py tests/test_sales_production_hardening.py tests/test_audit_logs.py tests/test_crm_api_endpoints.py tests/test_phase6_concurrency_control.py tests/test_calls_pagination.py tests/test_calls_remediation.py tests/test_calls_import_notes.py tests/test_calls_import_link_validation.py tests/test_activity_pagination.py tests/test_related_activity_loading.py tests/test_dashboard_activity_loading.py tests/test_sales_delete_regressions.py tests/test_cqrs_bulk_delete_all_entities.py tests/test_wave2_timeline_exports_status.py tests/test_leads_conversion.py`): `155 passed, 3 warnings in 29.55s`
  - **Batch E** (`tests/test_teamspace_import_stages.py tests/test_teamspace_api_endpoints.py tests/test_teamspace_request_workflows.py tests/test_lead_import_batches.py tests/test_status_import_export.py tests/test_deals_import_export.py`): `75 passed, 2 warnings in 18.91s`
- **Frontend Static, Unit & Build Checks**:
  - `npx.cmd tsc --noEmit` — `0` errors
  - `npm.cmd run lint` — `0` errors
  - `npm.cmd run test` (including `test:localization` / `verify-localization.mjs` + all 7 localization suites) — exited `0`
  - `npm.cmd run build` (`next build`, after installing `jspdf@4.2.1` matching `package-lock.json` via `--no-save`) — `✓ Compiled successfully in 16.6s`, `93/93` static pages generated, exited `0`
- **Frontend Playwright Browser Regression Suites (11 suites — all exited `0`)**:
  - `test:export-downloads:browser`, `test:sales-kanban:browser`, `test:meeting-schedule:browser`, `test:parent-notes:browser`, `test:related-activities:browser`, `test:global-timeline:browser`, `test:teamspace:tables:browser`, `test:teamspace:requests:browser`, `node tests/test_calls_meetings_ui_browser.mjs`, `node tests/test_account_enhancement_browser.mjs`, `node tests/test_contacts_enhancement_browser.mjs`
- **Playwright MCP Live Browser Verification (against live backend `127.0.0.1:8000` `/health` + `/health/ready` `200`, PostgreSQL `5432` & Redis `6379`)**:
  - Verified `/login` renders cleanly, exercises `/api/v1/auth/login`, returns Pydantic validation on invalid `.local` email domains, and enforces mandatory 6-digit email MFA challenge (not bypassed).
  - Verified `/` landing page renders with `0` console errors and `200` HTTP responses for `/favicon.png`, `/favicon.ico`, `/website-assets/crusource-mark.svg`, and `/apple-touch-icon.png` (`UX-01`).

---

## 7. Rollout & Safety Strategy

1. **Zero Database Downtime & No Schema Risk in Wave 2**:
   - All Wave 2 fixes (`TIME-01`..`STAT-02`) reuse existing tables (`notes`, `tasks`, `calls`, `meetings`, `documents`, `leads`, `deals`, `contacts`, `accounts`, `stage_history`, `audit_logs`) — zero breaking schema migrations required.
2. **Fail-Closed Security & FLS Posture**:
   - Permission, hierarchy, and field-level security (`allowed_columns` in `export_columns.py`, `apply_scope` in repositories, `require_record_mutation` in handlers) remain strictly enforced across every modified export and timeline query.
3. **Repository Isolation**:
   - Keep CRM changes strictly inside `crusource-crm-backend/`, `crusource-crm-frontend/`, and `crusource-crm-docs/`. Preserve existing local changes and verify each repository's `git status --short` independently.
