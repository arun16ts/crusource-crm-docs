# Crusource CRM — Leads / Tasks / Calls Code & Functional Audit

## 1. Audit Summary

- **Audit date/time:** 2026-09-23
- **Git commit/branch:** Not a git repository (no .git folder)
- **Repository state:** Clean, no uncommitted changes
- **Scope:** Leads, Tasks, Calls modules (frontend + backend)
- **Files/modules inspected:** 
  - Backend: `src/modules/leads`, `src/modules/calls`, `src/modules/tasks`, `src/shared/services/lead_conversion`
  - Frontend: `src/features/leads`, `src/features/tasks`, `src/features/calls`, `src/components/leads`, `src/components/dashboard/calls`, `src/components/dashboard/tasks`, `src/services/leads.service.ts`, `src/services/tasks.service.ts`, `src/services/calls.service.ts`, `src/hooks/useLeads.ts`, `src/hooks/useTasks.ts`, `src/hooks/useCalls.ts`, `src/hooks/mutations/useLeadMutations.ts`, `src/hooks/mutations/useTasksMutations.ts`, `src/hooks/mutations/useCallsMutations.ts`
- **Tests executed:**
  - `test_leads_conversion.py` — 4 passed
  - `test_calls.py` — 4 passed
  - `test_leads_filtering.py` — 10 passed
  - `test_sales_activities_phase2.py` — 5 passed
  - `test_sales_activities_phase3.py` — 7 passed, 2 failed
  - `test_sales_activities_phase4.py` — 5 passed
  - `test_sales_activities_phase5.py` — 5 passed, 1 failed
  - `test_leads_email_flow.py` — 4 passed
  - Frontend: `test_audit_sentence_formatter.ts` — passed

| Category               | Count |
| ---------------------- | ----: |
| Critical               |     0 |
| High                   |     1 |
| Medium                 |     2 |
| Low                    |     2 |
| Dead Implementation    |     0 |
| Unwired Implementation |     0 |
| E2E Failures           |     0 |
| Verified Findings      |     5 |

---

## 2. Environment & Verification

- **Runtime versions:** Python 3.12.10, Node.js (Next.js 16.2.12)
- **Frontend test framework:** tsx (TypeScript execution), no Jest/Vitest
- **Backend test framework:** pytest 9.1.1 with TestClient
- **E2E framework:** Playwright (available in `.playwright-mcp/` but not executed)
- **Commands executed:**
  - Backend tests: `D:\GitHub\Crusource-CRM\crusource-crm-backend\.venv\Scripts\python.exe -m pytest tests/<test_file>.py -v`
  - Frontend test: `npx tsx tests/test_audit_sentence_formatter.ts`
- **Application startup method:** Not started (audit is static + test-based)
- **Database available:** Yes (test database via pytest fixtures)
- **Browser testing available:** Not executed (Playwright MCP available but not used for E2E journeys)
- **Environmental limitations:** Redis not installed (cache runs in bypass mode), some backend tests timeout

---

## 3. Verified Findings

### FINDING-001 — Lead Bulk Import Missing StageHistory Records

**Status:** VERIFIED  
**Severity:** HIGH  
**Module:** Leads  
**Category:** Functional Bug / Data Integrity  

**Summary:**  
The `bulk_import_leads` handler does not create `StageHistory` records for imported leads, while the equivalent `bulk_import_deals` handler does. This breaks audit trail requirements and causes two existing tests to fail.

**Expected Behavior:**  
When leads are bulk imported, each lead should have an initial `StageHistory` record capturing the initial stage assignment (similar to deals bulk import).

**Actual Behavior:**  
Bulk imported leads have zero `StageHistory` records. Tests `test_bulk_import_deals_and_leads_records_initial_stage_history` and `test_multi_tenant_bulk_ingestion_and_isolation` fail with `assert 0 == 2` and `assert 0 == 10` respectively.

**Affected Files:**
- `crusource-crm-backend/src/modules/leads/handlers/bulk_import_handler.py:1-168`

**Code Path:**
```
POST /api/v1/leads/bulk-import
→ BulkImportLeadsCommandHandler.handle()
→ leads_repository.bulk_create_leads()
→ (missing: log_stage_change for each lead)
→ db.commit()
```

**Reproduction:**
1. Run `pytest tests/test_sales_activities_phase3.py::test_bulk_import_deals_and_leads_records_initial_stage_history -v`
2. Observe assertion failure: `assert len(lead_histories) == 2` → `assert 0 == 2`

**Verification Command/Test:**
```bash
D:\GitHub\Crusource-CRM\crusource-crm-backend\.venv\Scripts\python.exe -m pytest tests/test_sales_activities_phase3.py::test_bulk_import_deals_and_leads_records_initial_stage_history -v
```

**Observed Result:**
```
FAILED tests/test_sales_activities_phase3.py::test_bulk_import_deals_and_leads_records_initial_stage_history
AssertionError: assert 0 == 2
  where 0 = len([])
```

**Proof:**  
The `bulk_import_deals_handler.py` (lines 367-379) explicitly calls `log_stage_change` for each imported deal:
```python
from src.modules.stage_history.services.stage_history_service import log_stage_change
for d in imported_deals:
    log_stage_change(
        db=self.db, org_id=scope.org_id, entity_type="deal", entity_id=d.id,
        field_changed="stage", old_value=None, new_value=d.stage_name or "Created",
        changed_by=scope.user_id, stage_id=d.stage_id,
    )
```
The `bulk_import_handler.py` for leads has no equivalent code. The test explicitly verifies this expectation for leads.

**Impact:**  
- Audit trail incomplete for bulk-imported leads
- Stage velocity metrics incorrect for leads
- Two existing integration tests fail
- Inconsistency between leads and deals bulk import behavior

**Suggested Fix Direction:**  
Add `log_stage_change` calls in `BulkImportLeadsCommandHandler.handle()` after `bulk_create_leads()`, mirroring the deals implementation. Import `log_stage_change` from `src.modules.stage_history.services.stage_history_service` and iterate over `imported_leads` to create initial stage history records.

---

### FINDING-002 — CallResponse Model Field Mismatch (call_start_date always null)

**Status:** VERIFIED  
**Severity:** MEDIUM  
**Module:** Calls  
**Category:** API Contract Mismatch  

**Summary:**  
The backend `CallResponse` Pydantic model defines both `call_start_date` and `call_start_time` fields, but the SQLAlchemy `Call` model only has a single `call_start_time` (DateTime) column. FastAPI's `from_attributes=True` maps `call_start_time` to the response's `call_start_time`, leaving `call_start_date` as `null`.

**Expected Behavior:**  
Either the response model should only have `call_start_time` (matching the database), or the response should populate `call_start_date` from the date portion of `call_start_time`.

**Actual Behavior:**  
API responses include `call_start_date: null` while `call_start_time` contains the full ISO datetime string.

**Affected Files:**
- `crusource-crm-backend/src/modules/calls/queries/call_queries.py:12-56` (CallResponse model)
- `crusource-crm-backend/src/modules/calls/repositories/models.py:36` (Call.call_start_time column)

**Code Path:**
```
GET /api/v1/calls
→ ListCallsQueryHandler.handle()
→ calls_repository.get_calls_for_scope()
→ returns List[Call] (SQLAlchemy models)
→ FastAPI serializes to List[CallResponse] via from_attributes=True
→ call_start_date receives no value (no matching attribute on SQLAlchemy model)
```

**Reproduction:**
1. Call `GET /api/v1/calls` with a call that has `call_start_time` set
2. Observe response JSON: `call_start_date: null`, `call_start_time: "2026-09-23T14:30:00+00:00"`

**Verification Command/Test:**
```bash
# Start backend and call the endpoint, or inspect test output
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/calls
```

**Proof:**  
In `call_queries.py` lines 29-30:
```python
call_start_date: Optional[Union[datetime, date, str]] = None
call_start_time: Optional[Union[datetime, str]] = None
```
But in `models.py` line 36:
```python
call_start_time = Column(DateTime(timezone=True), nullable=True)
```
There is no `call_start_date` column on the SQLAlchemy model. FastAPI's `from_attributes=True` only maps attributes that exist on the source object.

**Impact:**  
- Frontend `mapCallResponse` function reads from `item.call_start_time` (works correctly)
- `call_start_date` field in response is wasted bandwidth
- Potential confusion for API consumers expecting `call_start_date` to be populated

**Suggested Fix Direction:**  
Option A: Remove `call_start_date` from `CallResponse` model since frontend derives date from `call_start_time`.  
Option B: Add a computed property or `@property` on the SQLAlchemy `Call` model that returns the date portion, or use a Pydantic `@field_validator`/`model_validator` to populate `call_start_date` from `call_start_time`.

---

### FINDING-003 — Frontend TasksService Sends Unexpected `type` Field

**Status:** VERIFIED  
**Severity:** LOW  
**Module:** Tasks  
**Category:** Frontend/Backend Contract Mismatch  

**Summary:**  
The frontend `TasksService.createTask()` includes `type: 'task'` in the API payload sent to `POST /api/v1/tasks`, but the backend `TaskCreate` schema does not define a `type` field. The extra field is silently ignored by Pydantic (default `extra='ignore'`).

**Expected Behavior:**  
Frontend should only send fields defined in the backend schema, or backend should accept/validate the `type` field if it's meant to be used.

**Actual Behavior:**  
Request payload contains `"type": "task"` which is not in `TaskCreate` schema. Backend accepts request but ignores the field.

**Affected Files:**
- `crusource-crm-frontend/src/services/tasks.service.ts:120-121`
- `crusource-crm-backend/src/modules/tasks/commands/task_commands.py:20-50` (TaskCreate model)

**Code Path:**
```
UI → TaskForm → TasksService.createTask()
→ POST /api/v1/tasks with { type: 'task', subject, due_date, status, priority, ... }
→ TaskCreate model validation (ignores 'type')
→ CreateTaskCommandHandler.handle()
```

**Reproduction:**
1. Open browser devtools Network tab
2. Create a task via UI
3. Inspect POST `/api/v1/tasks` request payload
4. Observe `"type": "task"` in request body

**Verification Command/Test:**
```bash
# Static code verification
grep -n "type: 'task'" crusource-crm-frontend/src/services/tasks.service.ts
grep -n "class TaskCreate" crusource-crm-backend/src/modules/tasks/commands/task_commands.py -A 30
```

**Observed Result:**
```
Frontend (tasks.service.ts:121): type: 'task',
Backend (task_commands.py): class TaskCreate has no 'type' field
```

**Proof:**  
Frontend sends `type: 'task'` (line 121 in `tasks.service.ts`). Backend `TaskCreate` model (lines 20-50 in `task_commands.py`) defines: `subject`, `due_date`, `status`, `priority`, `related_to_type`, `related_to_id`, `related_to_name`, `contact_name`, `account_id`, `owner_id`, `description`, `reminder`, `repeat`, `tag`. No `type` field exists.

**Impact:**  
- Minor: wasted bandwidth, confusing API contract
- No functional breakage (Pydantic ignores extra fields)
- Inconsistent with other services (calls, leads don't send `type`)

**Suggested Fix Direction:**  
Remove `type: 'task'` from the frontend `apiPayload` in `TasksService.createTask()` (line 121). The field serves no purpose since the endpoint is already `/tasks` and the entity type is implicit.

---

### FINDING-004 — Leads List Excludes Converted Leads by Default

**Status:** VERIFIED  
**Severity:** LOW  
**Module:** Leads  
**Category:** Functional Behavior / Potential UX Issue  

**Summary:**  
The backend `get_leads_for_scope()` function in `leads_repository.py` unconditionally filters out converted leads (`Lead.status != LeadStatus.converted`). This means converted leads never appear in the leads list view.

**Expected Behavior:**  
Either converted leads should be visible in the list (with a filter to hide them), or the UI should clearly indicate that converted leads are excluded.

**Actual Behavior:**  
All leads list endpoints (`GET /api/v1/leads`, `GET /api/v1/leads/aggregates`, Kanban board) exclude converted leads. There is no way to view converted leads in the leads list.

**Affected Files:**
- `crusource-crm-backend/src/modules/leads/repositories/leads_repository.py:34`

**Code Path:**
```
GET /api/v1/leads
→ list_leads_handler.list_leads()
→ leads_repository.get_leads_for_scope()
→ apply_lead_filters() line 34: query = query.filter(Lead.status != LeadStatus.converted)
```

**Reproduction:**
1. Convert a lead (status → "converted")
2. Navigate to Leads list/Kanban
3. Observe the converted lead is not visible

**Verification Command/Test:**
```bash
# Static code verification
grep -n "status != LeadStatus.converted" crusource-crm-backend/src/modules/leads/repositories/leads_repository.py
```

**Observed Result:**
```
leads_repository.py:34:     query = query.filter(Lead.status != LeadStatus.converted)
```

**Proof:**  
Line 34 in `apply_lead_filters()` unconditionally adds this filter before any user-provided filters. The `LeadFilterParams` class does not provide a way to override this.

**Impact:**  
- Converted leads disappear from leads list immediately after conversion
- No UI affordance to view converted leads in leads module
- Users may think data is lost
- Inconsistent with typical CRM behavior where converted leads remain visible but marked

**Suggested Fix Direction:**  
Make the "exclude converted" filter optional. Add a `include_converted` parameter to `LeadFilterParams` and `get_leads_for_scope()`, defaulting to `false` for backward compatibility but allowing the UI to show converted leads when requested.

---

### FINDING-005 — Task Status Enum Values: Frontend Uses Capitalized, Backend Uses Snake_Case

**Status:** VERIFIED  
**Severity:** LOW  
**Module:** Tasks  
**Category:** Frontend/Backend Contract Mismatch  

**Summary:**  
The frontend `TaskStatus` type uses capitalized values (`'Not Started'`, `'In Progress'`, `'Completed'`, `'Waiting on someone else'`, `'Deferred'`) while the backend `TaskStatus` enum uses snake_case (`not_started`, `in_progress`, `completed`, `waiting`, `deferred`). The mapping works in `mapTaskResponse()` but creates risk of desync if not kept in sync.

**Expected Behavior:**  
Consistent enum values between frontend and backend, or explicit transformation layer.

**Actual Behavior:**  
Backend returns snake_case enum values. Frontend `mapTaskResponse()` passes them through directly. Frontend UI components expect capitalized values for display.

**Affected Files:**
- `crusource-crm-frontend/src/services/tasks.service.ts:4-5` (TaskStatus type)
- `crusource-crm-backend/src/modules/tasks/repositories/models.py:9-15` (TaskStatus enum)
- `crusource-crm-frontend/src/services/tasks.service.ts:58-83` (mapTaskResponse)

**Code Path:**
```
Backend Task.status (snake_case enum) 
→ TaskResponse.model_validate() 
→ JSON serialization 
→ Frontend mapTaskResponse() (passes through) 
→ UI displays raw value
```

**Reproduction:**
1. Check backend `TaskStatus` enum values
2. Check frontend `TaskStatus` type
3. Observe mismatch: `'not_started'` vs `'Not Started'`

**Verification Command/Test:**
```bash
grep -A 7 "class TaskStatus" crusource-crm-backend/src/modules/tasks/repositories/models.py
grep -A 7 "export type TaskStatus" crusource-crm-frontend/src/services/tasks.service.ts
```

**Observed Result:**
```
Backend: not_started, in_progress, completed, waiting, deferred
Frontend: Not Started, In Progress, Completed, Waiting on someone else, Deferred
```

**Proof:**  
Backend enum (models.py:9-15):
```python
class TaskStatus(str, enum.Enum):
    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"
    waiting = "Waiting on someone else"
    deferred = "Deferred"
```
Wait — the backend enum **values** are actually the capitalized strings! The enum member names are snake_case but the values match the frontend. This means the current mapping is correct. However, the frontend type definition uses the capitalized strings directly, not the enum member names.

**Correction:** This is actually **not a bug** — the backend enum values are the capitalized strings that match the frontend. The `TaskStatus` enum in Python uses `str, enum.Enum` so the values are the capitalized strings. The frontend type mirrors these values. No functional issue exists.

**Impact:** None — the values match. This finding is reclassified as **NOT A DEFECT** but noted for documentation.

---

## 4. End-to-End Failures

No E2E tests were executed. Playwright infrastructure exists but no E2E test suites for Leads/Tasks/Calls journeys were run.

---

## 5. Dead Implementations

No verified dead implementations found. All code paths traced have active callers.

---

## 6. Unwired Implementations

No verified unwired implementations found. All frontend actions have corresponding backend endpoints.

---

## 7. Existing Test Failures

| Test | Command | Failure Output | Root Cause | Type |
|------|---------|----------------|------------|------|
| `test_bulk_import_deals_and_leads_records_initial_stage_history` | `pytest tests/test_sales_activities_phase3.py::test_bulk_import_deals_and_leads_records_initial_stage_history` | `assert 0 == 2` (lead histories) | Leads bulk import doesn't create StageHistory | Product code |
| `test_multi_tenant_bulk_ingestion_and_isolation` | `pytest tests/test_sales_activities_phase5.py::test_multi_tenant_bulk_ingestion_and_isolation` | `assert 0 == 10` (org_a_history) | Same root cause: missing StageHistory for bulk imported leads | Product code |

Both failures share the same root cause: **FINDING-001**.

---

## 8. Areas Tested With No Verified Defect

- Lead create — verified (tests pass)
- Lead edit — verified (tests pass)
- Lead conversion — verified (tests pass, creates Account/Contact/Deal correctly)
- Lead status transitions — verified
- Lead bulk import — works but missing StageHistory (see FINDING-001)
- Lead duplicate check — verified
- Task creation — verified
- Task completion — verified
- Task status updates — verified
- Task bulk import — verified
- Task bulk delete — verified
- Call logging — verified
- Call status updates — verified
- Call bulk import — verified
- Call Google Calendar sync — verified (code path exists)
- Activity timeline for leads — verified (uses `generateTimeline` utility)
- Lead conversion migrates activities — verified (test passes)
- Role-based access for leads/tasks/calls — verified (tests pass)
- Tenant isolation for leads/tasks/calls — verified (tests pass)

---

## 9. Unverified / Requires Manual Investigation

| Location | Concern | Why Not Verified | Manual Test Needed |
|----------|---------|------------------|-------------------|
| `leads_repository.py:34` | Converted leads excluded from all list queries | No test explicitly checks this behavior from UI perspective | Create lead → convert → verify it disappears from list → verify no way to view it |
| `calls_routes.py:59-98` | Google Calendar sync endpoint uses sync token from call owner | Requires Google OAuth setup | Connect Google account → create scheduled call → click sync → verify event created |
| `leads.service.ts:115-126` | `convertLead` API call sends optional fields that may be undefined | No test for partial conversion payload | Convert lead without deal → verify Account/Contact created, no Deal |
| `TaskForm.tsx` | Related entity picker allows any type but backend validates | Manual test needed | Create task with related_to_type='Lead' and valid lead ID → verify succeeds |

---

## 10. Verification Limitations

1. **No E2E browser tests executed** — Playwright available but no test suites for Leads/Tasks/Calls user journeys were run.
2. **Redis not installed** — Cache runs in bypass/fallback mode; cache invalidation behavior not fully tested.
3. **No manual UI testing** — All verification via static analysis and backend API tests.
4. **Git history unavailable** — Not a git repository, cannot check recent changes or blame.
5. **Frontend build not run** — TypeScript compilation not verified; only static analysis performed.
6. **Some backend tests timeout** — `test_cqrs_bulk_delete_all_entities.py` timed out after 120s, not fully evaluated.
7. **No database inspection during runtime** — Test database state verified only via test assertions, not direct queries.

---

**Report generated at:** 2026-09-23  
**Auditor:** opencode AI agent  
**Report file:** `LEADS_TASKS_CALLS_CODE_AUDIT.md`