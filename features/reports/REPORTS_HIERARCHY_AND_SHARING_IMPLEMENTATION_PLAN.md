# Reports Hierarchy Visibility & Scoped Sharing Implementation Plan

**Date:** 19 November 2026  
**Status:** Implemented locally and verified (`pytest`: 85 passed across reports + analytics suites; frontend: `tsc --noEmit`, `eslint` 0 errors, `test:localization`, `test:reports`, `test:reports:browser` all passed; uncommitted)  
**Scope:** `crusource-crm-backend` (`reports`, `analytics_boards` validation integration, `profiles` `can_view` alignment), `crusource-crm-frontend` (`reports` UI, `ShareReportModal`, row/run action gating), and `crusource-crm-docs`. Separate VMS repositories are unaffected.

---

## 1. Confirmed Requirements & Product Behavior

1. **Hierarchy Visibility in Reports:**
   - **Administrator (`scope.is_admin = True`):** Sees all reports across the organization (`private`, `team`, `org`, assigned), unchanged.
   - **Reporting Manager (non-admin with `reports.can_view` = `"team"` or `"all"` and leadership/hierarchy authority):** Sees their own reports, reports assigned to or by them, team-shared reports for teams they belong to/manage, org-wide reports (`visibility = "org"`), **and reports created by or assigned to their subordinates** (both via `User.reports_to` direct/skip-level chains and active members of teams where `Team.manager_id == manager.id`).
   - **Downward Admin Isolation (Preserved):** Neither Managers nor Standard users can see Admin-created `"private"` (non-`org`, non-shared) reports—even if an Admin is listed on a team or `reports_to` chain.
   - **Peer Isolation (Preserved):** Standard users on the same team **cannot** see each other's `"private"` reports (or their Manager's `"private"` reports).
   - **Read-Only Subordinate Access (Confirmed):** When a Manager views a subordinate's report (not created by or assigned by the Manager), access is **read-only**—the Manager can **view, run, export results, export definitions, and attach to Analytics widgets**, while **only the owner (`user_id`), original assigner (`assigned_by_id` for edit/share), or Admin (`is_admin`)** can **Edit, Share, or Delete** it.
2. **Profiles & Permissions Answer (No-Code Workaround Verdict):**
   - **Cannot be fixed via Profiles & Permissions UI alone.**
   - In [`profile_seed_service.py`](../../../crusource-crm-backend/src/modules/profiles/services/profile_seed_service.py#L165-L200), `Manager` already defaults to `reports.can_view = ViewScope.team` (`can_lead_teams = True`), `Standard` defaults to `ViewScope.own`, and `Administrator` has `ViewScope.all`.
   - However, [`reports_repository.py`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L76-L99) currently **ignores `reports.can_view`** (`own` vs `team` vs `all`) and checks `scope.visible_user_ids` **only against `SavedReport.assigned_to_user_id`**, never `SavedReport.user_id`.
   - Furthermore, [`scope_guard.py`](../../../crusource-crm-backend/src/shared/auth/scope_guard.py#L192-L226) populates `scope.visible_user_ids` with **same-team peers** as well as subordinates, so blindly applying `SavedReport.user_id.in_(scope.visible_user_ids)` would leak private reports among Standard teammates.
3. **Re-Enabling & Scoping Report Sharing (`Share & Assign`):**
   - The **Filter Reports** drawer (`Ownership & Scope`, `Sharing Visibility`, `Assigned to Me`) and [`ShareReportModal.tsx`](../../../crusource-crm-frontend/src/components/reports/modal/ShareReportModal.tsx), [`share_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py), and [`report_access.py`](../../../crusource-crm-backend/src/modules/reports/services/report_access.py) already exist, but sharing was previously hidden from [`ReportsHome.tsx`](../../../crusource-crm-frontend/src/components/reports/ReportsHome.tsx) (`onShareReport` and `<ShareReportModal />` omitted).
   - Bringing sharing back requires enforcing strict hierarchy rules:
     - **Organization-Wide (`visibility = "org"`): Admins ONLY** (backend rejects non-admins with `403`; UI hides/disables the `Organization` option for non-admins).
     - **Team Sharing (`visibility = "team"`):**
       - **Admin:** Any active team in `org_id`.
       - **Manager / Standard:** Only active teams the user belongs to or manages (`get_user_team_ids`).
     - **Direct User Assignment (`assigned_to_user_id`):**
       - **Admin:** Any active user in `org_id`.
       - **Manager (`can_lead_teams` / manages team / has reporting descendants):** Only non-Admin subordinate / managed-team members (plus team-membership check if `visibility == "team"`).
       - **Standard (`!is_admin && !can_lead_teams`):** Cannot assign reports upward to Managers/Admins or cross-team (`403` in backend; direct-assignment UI hidden for non-leaders).

---

## 2. Source Diagnosis & Security Findings

| Area | Current State & Source Evidence | Risk / Defect | Target Fix |
| --- | --- | --- | --- |
| Report list & single fetch scoping | [`_apply_scope_access_filter`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L76-L99) & [`get_saved_report_by_id_for_scope`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L240-L271) check `SavedReport.assigned_to_user_id.in_(scope.visible_user_ids)` only | Reporting managers cannot see subordinates' `"private"` reports; duplicated access logic between list and get-by-id; peer assignments via `visible_user_ids` leak to peers | Resolve subordinate IDs separately (`User.reports_to` tree + managed `Team.manager_id` members minus Admins); unify `_apply_scope_access_filter` across list, counts, get-by-id, and team reports; honor `reports.can_view` |
| Team reports endpoint | [`get_saved_reports_for_team`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L290-L300) only checks `org_id` and `team_id` | Non-admin user knowing a `team_id` UUID can query another team's reports | Apply `_apply_scope_access_filter` and validate `team_id in user_team_ids` for non-admins |
| Single delete handler | [`DeleteSavedReportCommandHandler`](../../../crusource-crm-backend/src/modules/reports/handlers/delete_report_handler.py#L16-L22) deletes any report returned by `get_saved_report_by_id_for_scope` | Unlike `bulk_delete_reports_handler.py`, `update_report_handler.py`, and `require_report_edit`, single `DELETE /{report_id}` lacks owner/admin check—managers viewing subordinates' reports could delete them | Require `scope.is_admin or view.user_id == scope.user_id` (`403` otherwise) |
| Sharing validation | [`validate_sharing_references`](../../../crusource-crm-backend/src/modules/reports/services/report_access.py#L11-L31) & [`share_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py#L39-L43) | Non-admins can set `visibility="org"` and assign `assigned_to_user_id` to Admins or cross-team users; `assigned_by_id` is not cleared when unassigning | Restrict `"org"` to Admins; restrict `assigned_to_user_id` by hierarchy; clear `team_id`/`assigned_by_id` cleanly when switching back to `private`/`org` |
| Sharing & row-action UI | [`ReportsHome.tsx`](../../../crusource-crm-frontend/src/components/reports/ReportsHome.tsx#L645-L675), [`ShareReportModal.tsx`](../../../crusource-crm-frontend/src/components/reports/modal/ShareReportModal.tsx#L34-L305) | `<ShareReportModal />` & `onShareReport` are unmounted; modal shows `Organization` and all org users (`useUsers`) to everyone; `ReportsHome` shows Edit/Delete triggers on non-owned visible reports | Add `/api/v1/reports/share-targets`, wire `ShareReportModal` in `ReportsHome`, restrict Edit/Share/Delete UI to authorized owners/admins, open read-only reports in `ReportRunModal` |

---

## 3. Detailed Implementation Plan

### Phase 1 — Backend Hierarchy & Profile ViewScope Enforcement

**Files to modify:**
1. [`crusource-crm-backend/src/modules/reports/services/report_access.py`](../../../crusource-crm-backend/src/modules/reports/services/report_access.py)
2. [`crusource-crm-backend/src/modules/reports/repositories/reports_repository.py`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py)

**Implementation details:**
1. **`report_access.py` — Hierarchy & Admin Exclusion Helpers:**
   - Add `_admin_user_ids(db: Session, org_id: uuid.UUID) -> set[uuid.UUID]`:
     - Returns active/org user IDs where `User.role == UserRole.admin` **or** bound `Profile.is_admin_profile == True` (resolving via `User.profile_id`, matching `User.profile` fallback or `RoleNode.default_profile_id` similarly to `_resolve_user_scope`, kept lightweight with batch queries on `User`, `Profile`, and `RoleNode`).
   - Add `resolve_report_view_scope(scope: Scope) -> str`:
     - Reads `perm = scope.get_module_permission("reports")`.
     - If `scope.is_admin`: returns `"all"`.
     - If `perm` exists: returns normalized `str(perm.can_view)` (`"none"`, `"own"`, `"team"`, `"all"`).
     - Fallback (e.g., synthetic test `Scope` without `permissions` populated): returns `"team"` if `scope.can_lead_teams or len(scope.visible_user_ids) > 1` else `"own"`.
   - Add `get_subordinate_creator_ids(db: Session, scope: Scope) -> set[uuid.UUID]`:
     - Returns `set()` immediately if `scope.is_admin` (not needed) or `resolve_report_view_scope(scope) in ("none", "own")`.
     - Evaluates whether actor has managerial authority in the org:
       - `managed_team_ids = [row[0] for row in db.query(Team.id).filter(Team.org_id == scope.org_id, Team.is_active.is_(True), Team.manager_id == scope.user_id).all()]`
       - `tree_descendants = get_reporting_descendant_ids(db, scope.org_id, scope.user_id)`
       - Notice: only if actor is actually a manager/leader (`scope.can_lead_teams`, `managed_team_ids`, or `tree_descendants` is non-empty) do we populate subordinate IDs; a Standard rep without subordinates never expands beyond their own/shared/assigned reports even if a custom profile accidentally sets `"team"`.
       - Combines:
         1. `tree_descendants` (`User.reports_to` chain).
         2. Active users in `managed_team_ids` via `TeamMembership.user_id` and `User.team_id` (`User.org_id == scope.org_id`, `User.is_active.is_(True)`).
       - Subtracts `{scope.user_id}` and `_admin_user_ids(db, scope.org_id)` so Admin-owned reports are never exposed downward.
2. **`reports_repository.py` — Unified `_apply_scope_access_filter`:**
   - Replace inline logic inside [`_apply_scope_access_filter`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L76-L99):
     - Always filter `SavedReport.org_id == scope.org_id`.
     - If `scope.is_admin`: return immediately.
     - Evaluate `view_scope = resolve_report_view_scope(scope)`:
       - If `view_scope == "none"`: return `query.filter(false())`.
     - Always allow own & explicit shares/assignments:
       - `SavedReport.user_id == scope.user_id`
       - `SavedReport.assigned_to_user_id == scope.user_id`
       - `SavedReport.assigned_by_id == scope.user_id`
       - `SavedReport.visibility == "org"`
       - If `user_team_ids`: `and_(SavedReport.visibility == "team", SavedReport.team_id.in_(user_team_ids))`
     - When `view_scope in ("team", "all")`:
       - Compute `subordinate_ids = get_subordinate_creator_ids(db, scope)`.
       - If `subordinate_ids`:
         - `SavedReport.user_id.in_(subordinate_ids)` (reporting managers see reports created by subordinates)
         - `SavedReport.assigned_to_user_id.in_(subordinate_ids)` (managers also see reports assigned to subordinates, without exposing peer-to-peer assigned reports to Standard users)
     - When `view_scope == "all"` (explicit non-admin custom profile override):
       - Additionally allow non-admin org reports: `~SavedReport.user_id.in_(admin_ids)` (if `admin_ids` is non-empty, else unfiltered non-admin org view) — keeping Admin private reports hidden even if a custom profile grants `reports.can_view="all"`.
   - Refactor [`get_saved_report_by_id_for_scope`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L240-L271) to delegate filtering to `_apply_scope_access_filter(query, db, scope)` so list, counts, get-by-id, run, export, and widget validation share one policy implementation.
   - Update [`get_saved_reports_for_team`](../../../crusource-crm-backend/src/modules/reports/repositories/reports_repository.py#L290-L300):
     - Require `team_id in get_user_team_ids(db, scope.user_id, scope.org_id)` when `not scope.is_admin` (returning `[]` or raising `403` cleanly — check handler expectation; returning `_apply_scope_access_filter(query, db, scope)` and checking team access enforces both team and report boundaries).

---

### Phase 2 — Hierarchy-Enforced Report Sharing, Share-Targets API & Delete Guard

**Files to modify:**
1. [`crusource-crm-backend/src/modules/reports/services/report_access.py`](../../../crusource-crm-backend/src/modules/reports/services/report_access.py)
2. [`crusource-crm-backend/src/modules/reports/queries/report_queries.py`](../../../crusource-crm-backend/src/modules/reports/queries/report_queries.py)
3. [`crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py)
4. [`crusource-crm-backend/src/modules/reports/handlers/update_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/update_report_handler.py)
5. [`crusource-crm-backend/src/modules/reports/handlers/create_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/create_report_handler.py)
6. [`crusource-crm-backend/src/modules/reports/handlers/delete_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/delete_report_handler.py)
7. [`crusource-crm-backend/src/modules/reports/routes/report_routes.py`](../../../crusource-crm-backend/src/modules/reports/routes/report_routes.py)

**Implementation details:**
1. **Tighten `validate_sharing_references(db, scope, visibility, team_id, assignee_id, *, manage_team=False)`:**
   - **Organization-wide rule (Admins only):**
     - If `visibility == "org"` and `not scope.is_admin`: raise `HTTPException(403, "Only administrators can share reports organization-wide")`.
   - **Team rule:**
     - If `visibility == "team"` and `not team_id`: raise `HTTPException(400, "Choose a destination team")`.
     - If `team_id`: verify `active_team(db, scope, team_id)`. When `not scope.is_admin`, verify `team.id in repository.get_user_team_ids(db, scope.user_id, scope.org_id)` (`403` otherwise); when `manage_team=True`, keep `team.manager_id == scope.user_id or (member and scope.can_lead_teams)`.
   - **Direct User Assignment rule:**
     - If `assignee_id`: verify `active_user(db, scope, assignee_id)` (`400` otherwise).
     - When `not scope.is_admin`:
       - Compute `subordinate_ids = get_subordinate_creator_ids(db, scope)` using managerial authority (`can_lead_teams` / `Team.manager_id` / `reports_to` descendants, independent of `can_view` dropdown override or gated on `can_lead_teams` — i.e., Standard users cannot directly assign to subordinates because they have none!).
       - Verify `assignee_id in subordinate_ids` (never Admins, never peers, never managers, never unrelated teams); raise `HTTPException(403, "You can only assign reports to your reporting subordinates or managed team members")`.
       - Wait — also check existing tests in [`test_report_sharing.py`](../../../crusource-crm-backend/tests/test_report_sharing.py#L90-L151): `test_report_direct_assignment` uses `admin_scope` (`is_admin=True`), which remains permitted for any active user in the org!
     - If `team` is specified, continue verifying `assignee_id in repository.team_user_ids(db, scope, team)`.
2. **Add `GET /api/v1/reports/share-targets` (`ReportShareTargetsResponse` in `report_queries.py` + `report_routes.py`):**
   - Protected by `Depends(require_permission("reports", "view"))` (or `"edit"` / `"create"` — using `require_permission("reports", "view")` avoids blocking read-only inspection while modal actions still require edit).
   - Returns:
     - `can_share_org: bool` (`scope.is_admin`)
     - `can_share_team: bool` (`len(eligible_teams) > 0`)
     - `can_assign_users: bool` (`scope.is_admin or len(assignable_users) > 0`)
     - `teams: List[ShareTargetTeam]` (`id`, `name`, `member_count` — all active org teams for Admin; `get_user_team_ids` teams for non-admins)
     - `assignable_users: List[ShareTargetUser]` (`id`, `name`, `email`, `role`, `team_ids` — all active non-self org users for Admin; non-Admin subordinates/managed team members via `get_subordinate_creator_ids` for Managers; `[]` for Standard users).
3. **Clean Handler Assignment Hygiene:**
   - In [`share_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/share_report_handler.py#L39-L43), [`create_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/create_report_handler.py#L41-L54), and [`update_report_handler.py`](../../../crusource-crm-backend/src/modules/reports/handlers/update_report_handler.py#L77-L84):
     - Clear `report.team_id = command.team_id if visibility == "team" else None` (prevents stale `team_id` when changing `"team"` -> `"org"` or `"private"`).
     - Set `report.assigned_by_id = scope.user_id` only when `assigned_to_user_id` or `team_id` is present; set `assigned_by_id = None` when cleared (`visibility == "private"` and `not assigned_to_user_id` and `not team_id`).
4. **Close Single Delete Security Gap:**
   - Update [`DeleteSavedReportCommandHandler.handle`](../../../crusource-crm-backend/src/modules/reports/handlers/delete_report_handler.py#L16-L22):
     - After `view = reports_repository.get_saved_report_by_id_for_scope(self.db, command, scope)`:
     - Require `if not scope.is_admin and view.user_id != scope.user_id: raise HTTPException(status_code=403, detail="You do not have permission to delete this report")`.

---

### Phase 3 — Frontend UI: Restore `ShareReportModal` & Subordinate Read-Only UX

**Files to modify:**
1. [`crusource-crm-frontend/src/services/reports.service.ts`](../../../crusource-crm-frontend/src/services/reports.service.ts)
2. [`crusource-crm-frontend/src/hooks/useReportsQueries.ts`](../../../crusource-crm-frontend/src/hooks/useReportsQueries.ts)
3. [`crusource-crm-frontend/src/components/reports/modal/ShareReportModal.tsx`](../../../crusource-crm-frontend/src/components/reports/modal/ShareReportModal.tsx)
4. [`crusource-crm-frontend/src/components/reports/ReportsHome.tsx`](../../../crusource-crm-frontend/src/components/reports/ReportsHome.tsx)
5. [`crusource-crm-frontend/src/components/reports/table/ReportsTable.tsx`](../../../crusource-crm-frontend/src/components/reports/table/ReportsTable.tsx) & [`ReportRow.tsx`](../../../crusource-crm-frontend/src/components/reports/table/ReportRow.tsx) & [`ReportRowActions.tsx`](../../../crusource-crm-frontend/src/components/reports/table/ReportRowActions.tsx)
6. [`crusource-crm-frontend/src/messages/{en,ar,nl}/reports.json`](../../../crusource-crm-frontend/src/messages/en/reports.json)

**Implementation details:**
1. **Service & Hook (`reports.service.ts` + `useReportsQueries.ts`):**
   - Add `ReportShareTargetsResponse` and `ReportsService.getShareTargets()` (`GET /reports/share-targets`).
   - Add `useReportShareTargetsQuery(options?: { enabled?: boolean })`.
   - In `useShareReportMutation`, also invalidate `["reports", "counts"]` and `["savedReportsAll"]` so KPI counts and Analytics selector widgets refresh immediately after sharing changes.
2. **Hierarchy-Aware `ShareReportModal.tsx`:**
   - Replace `useAllTeamsQuery` and `useUsers` with `useReportShareTargetsQuery({ enabled: Boolean(isOpen && report) })`.
   - Enforce capabilities returned from the server:
     - Render **Organization** visibility card only if `shareTargets?.can_share_org` (Admin only); if disabled/hidden, prevent switching non-admins to `org` (and show `Private` / `Team` cleanly in a responsive 2-col or 3-col grid).
     - Render **Team** visibility card with `disabled={!canShareTeam}` + subtle empty-team note when the user belongs to no teams.
     - Render **Assign to a specific Sales Rep / Member** section only when `can_assign_users` (`is_admin || subordinates exist`).
     - When `visibility === "team"` and `selectedTeamId` is picked, filter `assignable_users` to users whose `team_ids` include `selectedTeamId` (matching backend `team_user_ids` constraint) and reset `selectedUserId` if the previous assignee is not in the chosen team.
3. **Wire Sharing & Per-Row Read-Only Ownership Gating in `ReportsHome.tsx` + Table Components:**
   - Fetch current user profile / admin flag (`useAuth()` or `UserService.getCurrentUser()` query / existing auth hook — verify the standard hook used across pages before coding).
   - Compute per-report capabilities:
     - `canModifyReport(report)`: `isAdmin || report.user_id === currentUserId || report.assigned_by_id === currentUserId`
     - `canDeleteReport(report)`: `isAdmin || report.user_id === currentUserId`
   - In `ReportsHome.tsx`:
     - Select `shareModalReport` from `state.reports`, pass `onShareReport={(report) => dispatch(openShareModal(report))}`, and mount `<ShareReportModal isOpen={Boolean(shareModalReport)} report={shareModalReport} onClose={() => dispatch(closeShareModal())} />`.
     - Update row click (`onSelectReport`): if `canEdit && canModifyReport(report)`, open `ReportBuilder` (or `RepairReportModal` if `validation_error`); otherwise open `ReportRunModal` (`handleRunReport(report)`) so clicking a subordinate's or shared read-only report opens results smoothly rather than failing inside the builder.
     - Pass `canEditReport={(report) => canEdit && canModifyReport(report)}`, `canShareReport={(report) => canEdit && canModifyReport(report)}`, and `canDeleteReport={(report) => canDelete && canDeleteReport(report)}` cleanly to `ReportsTable` -> `ReportRow` -> `ReportRowActions` (or keep backward-compatible boolean/callback props).
     - In `ReportRunModal`, pass `onEdit={activeReport && canEdit && canModifyReport(activeReport) ? ... : undefined}` so `Edit Builder` is hidden on read-only reports.
   - Surface report visibility/origin clearly in `ReportRow.tsx` (using compact pill or [`ReportOriginBadge.tsx`](../../../crusource-crm-frontend/src/components/reports/table/ReportOriginBadge.tsx) indicator alongside creator name so Private, Team, Org, and Assigned states match the Filter Drawer!).
   - Surface `not_deleted` warnings in `handleBulkDeleteConfirm` if mixed selections are submitted for bulk deletion.
   - Add any new UI labels (`readOnlyHint`, `noTeamsAvailable`, `orgAdminOnly`, etc.) across `src/messages/{en,ar,nl}/reports.json` with 1:1 key parity.

---

## 4. Cross-Module Dependency Verification

| Dependent Module | Interaction | Impact & Safeguards |
| --- | --- | --- |
| **Report Execution (`report_query_builder.py`, `forecast_report_source.py`)** | [`run_saved_report`](../../../crusource-crm-backend/src/modules/reports/handlers/run_report_handler.py#L60) runs `apply_scope(..., scope)` using the **viewer's** `Scope` | Safe: Manager running a subordinate's report only queries CRM Leads/Deals/Contacts/Accounts/Tasks/Calls/Meetings/Forecast records visible to the Manager—no data-row escalation |
| **Analytics Boards ([`widget_validator.py`](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py#L59), [`AddWidgetModal.tsx`](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx))** | Calls `get_saved_report_by_id_for_scope` & `ReportsService.listReports` | Managers can attach subordinates' & team-shared reports to their Analytics widgets; Analytics Boards remain isolated per `AnalyticsBoard.user_id` |
| **Teams & User Admin ([`delete_team_command.py`](../../../crusource-crm-backend/src/modules/admin/commands/teams/delete_team_command.py#L103-L110), `team_membership_commands.py`)** | Deleting a team resets `team_id = None` and `"team"` -> `"private"`; team/user mutations call `clear_user_scope_cache` | Subordinate ID queries read live `Team`, `TeamMembership`, and `User.reports_to` tables on each request—hierarchy reassignments apply immediately |
| **Profiles (`ModulePermission.can_view`)** | [`ModulesTab.tsx`](../../../crusource-crm-frontend/src/components/admin/profiles/tabs/ModulesTab.tsx#L303-L343) edits `reports.can_view` (`none`/`own`/`team`/`all`) | Backend now honors `reports.can_view` without requiring profile schema/UI changes |
| **AI Chat (`report_nlp_service.py`) & Global Search** | Loop AI creates own private reports; Search has no `SavedReport` provider | Safe and unaffected |

---

## 5. Verification Plan

### Backend Tests (`crusource-crm-backend`)
Create `tests/test_reports_hierarchy.py` and extend `tests/test_report_sharing.py`:
1. **Manager Subordinate Visibility:**
   - Manager via `Team.manager_id` sees Standard members' `"private"` and `"team"` reports across `GET /reports?paged=true`, `GET /reports/summary-counts`, `GET /reports/{id}`, `POST /reports/{id}/run`, `POST /reports/{id}/export`, and `POST /reports/export-definitions`.
   - Manager via `User.reports_to` (direct report AND skip-level descendant) sees subordinates' reports even without `Team.manager_id`.
   - Filter interoperability: `owner_scope=shared` and `search_scope=creator_name` return subordinate-created reports cleanly.
2. **Strict Isolation Boundaries:**
   - Standard Peer A in Team X **cannot** see Standard Peer B's `"private"` reports (or Manager's `"private"` reports).
   - Standard and Manager **cannot** see Admin-created `"private"` reports (even when Admin is assigned to a team or `reports_to`).
   - Manager of Team X **cannot** see `"private"` reports of Standard users in unrelated Team Y.
   - Manager with Profile `reports.can_view = "own"` **cannot** see subordinates' `"private"` reports.
3. **Read-Only Subordinate Protection:**
   - Manager gets `403` on `PATCH /reports/{id}`, `POST /reports/{id}/share`, `POST /reports/teams/{team_id}/assign`, and **`DELETE /reports/{id}`** for subordinate's report; `POST /reports/bulk-delete` keeps subordinate's report intact in `not_deleted`.
4. **Scoped Sharing Validation (`validate_sharing_references` + `GET /reports/share-targets`):**
   - `GET /reports/share-targets` returns `can_share_org=True` + org teams/users for Admin; managed/member teams + subordinate users + `can_share_org=False` for Manager; member teams only + `can_assign_users=False` for Standard.
   - Manager/Standard attempting `visibility="org"` via `POST /share` or `PATCH` gets `403`.
   - Manager assigning directly to Admin or out-of-team/peer user gets `403`; assigning to direct subordinate or managed team member succeeds (`200`), sets `assigned_by_id`, and clearing assignment resets `assigned_by_id` to `None`.
   - Verify all existing tests in `test_reports*.py`, `test_report_sharing.py`, and `test_analytics_boards*` remain green.

### Frontend Checks (`crusource-crm-frontend`)
1. Extend [`tests/test_reports_product_browser.mjs`](../../../crusource-crm-frontend/tests/test_reports_product_browser.mjs):
   - Owner/Admin row shows **Edit Report**, **Share & Assign**, **Delete**, and opens **ShareReportModal** (`GET /reports/share-targets`, role-gated `Organization`/`Team`/`Assign` controls, `POST /reports/{id}/share`).
   - Non-owned subordinate report row hides **Edit Report**, **Share & Assign**, and **Delete** in `ReportRowActions`, opens `ReportRunModal` on row click, and hides `Edit Builder` inside `ReportRunModal`.
2. Run `tsc --noEmit`, `eslint` on modified files, `npm run test:localization`, `npm run test:reports`, and `npm run test:reports:browser`.
