# Enterprise CRM strategic features implementation plan

| Field | Value |
|---|---|
| Date | 22 October 2026 |
| Status | Proposed implementation plan; product decisions and implementation approval are still required. |
| Scope | Crusource CRM only: `crusource-crm-backend/` (FastAPI, SQLAlchemy, Alembic) and `crusource-crm-frontend/` (Next.js App Router, React). The separate platform frontend/backend are out of scope. |
| Features | Account hierarchy and group rollups; deal team collaboration and quota splits; explainable lead prioritization using the existing Gemini integration. |
| Deployment status | Not implemented or deployed by this document. |
| Verification | Baseline re-verified against CRM backend/frontend source on 22 October 2026 (second pass). Corrections from that pass are integrated below: deal-visibility projection points, account access path, queue deployment mode, permission-action limits, forecast attribution, Gemini client limits, and concrete frontend targets. |

## 1. Recommendation and product framing

Deliver the work as three independently releasable capabilities behind organization-level feature/configuration switches, with shared foundation work for authorization, migrations, audit, and operational limits. Do not make one large release depend on all three capabilities. The account hierarchy and deal team work can proceed independently after access and migration conventions are agreed. AI scoring should follow the product/privacy decision and must not block either CRM capability.

Treat an AI score as a **lead prioritization score**, not a statistically calibrated conversion probability. A generative model can produce useful explanations and a consistent rubric, but it does not become predictive merely because the prompt asks for a probability. Show the score, rubric version, timestamp, and reasons; let sales users make the decision. Do not use it as the only basis for eligibility, employment, credit, or other high-impact decisions.

The existing codebase already has account parent links, optimistic concurrency on account/deal/lead records, a CRM access-policy service, configured Gemini structured output, a queue abstraction, and frontend services/hooks/drawers. Extend these instead of introducing parallel clients, permission engines, state stores, or AI providers.

## 2. Verified repository baseline

The following are source observations as of the date above. Re-check them at implementation time because the application repositories can change independently of this document.

| Area | Current source evidence | Plan consequence |
|---|---|---|
| Account hierarchy | `Account.parent_account_id` already exists (self-FK, `ON DELETE SET NULL`, indexed). Create validates organization **and record team**; update validates organization and direct self-parenting only — it does **not** enforce the same record team (inconsistent with create) and does not prevent longer cycles. `AccountResponse` omits `parent_account_id`. No unique `(org_id, id)` key exists on `accounts` today. Soft-deleting a parent leaves children pointing at it because `SET NULL` fires only on hard delete. | Reuse parent link; make create and update apply one record-team rule; add cycle-safe reparenting, API contracts, a new `(org_id, id)` unique key before any composite FK, and explicit soft-delete/restore behavior for parents. |
| Account access path | Accounts are **not** in `RECORDS` (`record_registry.py`), so `resolve_record_access`/`resolve_record_policy` do not cover them. Account reads use `apply_scope` (`scope_guard.py`: org, soft-delete, record-team ceiling, then profile `can_view` own/team/all on `owner_id`) via `get_account_by_id_for_scope`, plus the record-team ceiling in `bind_record_read_boundary`. | Hierarchy and rollup reads must use `apply_scope(…, Account, scope)` for every linked account, not organization filtering or the deal policy service. |
| Record access | `resolve_record_policy` is used by record access/mutation/governance flows and applies module permission, record-team visibility, owner, profile-policy, and grant rules. Deals are additionally projected in three other places: (1) `apply_scope` personal lists filter **strictly** `deal_owner_id == scope.user_id`; (2) `bind_record_read_boundary` attaches a global `with_loader_criteria` ceiling (owner or record team) to **every** ORM select of `Deal`, including joins and counts; (3) `apply_record_team_scope`/`record_is_visible` for Teamspace. Existing `RecordPermission` grants are edit-only, require `expires_at`, are bound to the record team, and are consulted only under approval-based teammate policy. | A deal-team membership must be added to all four projection points in one shared predicate, or a member outside the record team is silently filtered out by the loader criteria even if the policy says "allow". `RecordPermission` is not a fit for persistent team membership without redesign. An early return in `resolve_record_policy` is unsafe and insufficient. |
| Permission actions | `require_permission(module, action)` accepts only `view`, `create`, `edit`, `delete`, `export`, `import`, `bulk_edit`; profile module permissions are fixed boolean/visibility columns. | A dedicated "manage deal team" or "run AI scoring" permission is a schema + profile-admin UI + default-profile migration change. Decide in §3 whether to add it or gate on existing `edit` plus an org-admin feature switch. |
| Deal model | Deals have `org_id`, `deal_owner_id`, `amount` (Float), `currency`, `stage_id`, soft deletion, team context, and optimistic `version`. Forecast summary, rep attribution, and forecast notifications group by `deal_owner_id` only. | Preserve current owner and approval semantics; split accounting must define currency and stage behavior. Splits will **not** affect forecast/quota numbers unless forecast queries are explicitly changed (see §3 decision 8). |
| Lead model/API | Leads have contact/company/profile fields, soft deletion, team context, and `version`; current `LeadResponse` has no scoring fields. An existing free-text `rating` field and `ratings` list filter already exist. | Extend model, query filters, API response, and frontend types together. Use distinct names (e.g. `ai_priority_score`, `ai_priority_band`) so the AI assessment is not confused with the user-maintained `rating`. |
| Gemini | `GeminiProvider.generate_structured()` is async-only (`client.aio`), uses the configured model, sets `response_mime_type="application/json"` but **no `response_schema`**, caps output at 2048 tokens and prompt at 64,000 characters. The shared client uses a 15 s timeout with a single attempt. No token-usage metadata is captured anywhere in `src`. `org_settings.loop_ai_model` and the provider fallback default to `gemini-2.5-flash`. | Extend the provider for schema-constrained output, usage metadata, and typed errors; retain application-side validation. Validate the configured model against `list_chat_models()` for the deployed key (the superadmin model route already does this) because 2.5 access is restricted for new Google projects. |
| Queue/jobs | `queue_service.enqueue()` supports `QUEUE_MODE` `sync`/`sqs`, and `src/worker.py` is an SQS consumer. **Stage and production Terraform both set `QUEUE_MODE=sync`**, where `enqueue()` runs the handler inline in the caller. Task handlers are synchronous callables. The proven durable pattern is Calls bulk jobs: a `CallBulkJob` table (idempotency key, payload hash, `claim_token`, `lease_until`) polled by an APScheduler dispatcher (`bulk_job_dispatcher.py`) so work runs outside the HTTP request in either mode. | Do not call `enqueue()` from a scoring route. Reuse the Calls durable-job pattern; bridge the async provider explicitly inside the sync handler. Do not treat in-process FastAPI background tasks as durable jobs. |
| AI rate/resource controls | `ai_chat/guards.py` uses `RateLimiter(..., fail_closed_in_production=True)` for per-user hourly AI drafting; `resource_admission.py` uses PostgreSQL advisory locks for per-org AI work slots. | Reuse these for scoring admission and per-org concurrency instead of a new limiter. |
| Frontend conventions | CRM API calls belong in `src/services/*`; server data uses TanStack Query, UI state uses Redux/local state, and shareable filters belong in URL state. Drawers are composed from tabs: `components/accounts/drawer/{AccountOverviewTab,AccountContactsTab,AccountTimelineTab}.tsx`, `components/leads/drawer/*`, `components/deals/DealDetailDrawer.tsx`. Lead list surfaces are `LeadList.tsx`, `LeadBoard.tsx`, `KanbanBoard.tsx`, `LeadCard.tsx`, and `FilterPanel.tsx` (there is no `LeadsTable.tsx`). Locales are `en`, `ar`, `nl`. | Add typed services and focused hooks; keep route/page entry points thin and update all three locales. |
| Tests | `tests/conftest.py` imports models explicitly before creating SQLite tables. | Import every new model (`deal_team_members`, `deal_splits`, scoring job) there or its table will not exist in unit tests. |
| CI | Backend CI includes Ruff, compile checks, PostgreSQL migration/integration tests, pytest and Alembic drift. Frontend CI includes formatting, lint, tests, typecheck, browser regressions, build and dependency audit. | Use the current full workflows for the affected repos before declaring an implementation phase complete. |

Source links: [Account model](../../../crusource-crm-backend/src/modules/accounts/repositories/models.py), [account create](../../../crusource-crm-backend/src/modules/accounts/handlers/create_account_handler.py), [account update](../../../crusource-crm-backend/src/modules/accounts/handlers/update_account_handler.py), [account schema](../../../crusource-crm-backend/src/modules/accounts/queries/account_queries.py), [record registry](../../../crusource-crm-backend/src/shared/auth/record_registry.py), [record policy](../../../crusource-crm-backend/src/modules/teamspace/services/record_policy.py), [read boundary](../../../crusource-crm-backend/src/shared/auth/record_read_boundary.py), [record team scope](../../../crusource-crm-backend/src/shared/auth/record_team_scope.py), [apply_scope](../../../crusource-crm-backend/src/shared/auth/scope_guard.py), [permission guard](../../../crusource-crm-backend/src/shared/auth/permission_guard.py), [Deal model](../../../crusource-crm-backend/src/modules/deals/repositories/models.py), [forecast repository](../../../crusource-crm-backend/src/modules/forecast/repositories/forecast_repository.py), [Lead model](../../../crusource-crm-backend/src/modules/leads/repositories/models.py), [Lead API schema](../../../crusource-crm-backend/src/modules/leads/queries/lead_queries.py), [Gemini provider](../../../crusource-crm-backend/src/modules/ai_chat/services/providers/gemini_provider.py), [AI guards](../../../crusource-crm-backend/src/modules/ai_chat/guards.py), [queue service](../../../crusource-crm-backend/src/shared/services/queue_service.py), [Calls bulk job model](../../../crusource-crm-backend/src/modules/calls/repositories/bulk_job_models.py), [Calls bulk dispatcher](../../../crusource-crm-backend/src/modules/calls/services/bulk_job_dispatcher.py), [stage Terraform](../../../crusource-crm-backend/terraform/environments/stage/main.tf), [frontend lead service](../../../crusource-crm-frontend/src/services/leads.service.ts), and [lead drawer](../../../crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx).

## 3. Decisions to record before implementation

Resolve these in a short product/architecture decision record before schema freeze. Defaults below are the recommended safe starting point.

1. **Account hierarchy scope:** Can an account parent and child belong to different record teams? Current create behavior requires the same record team. **Recommended v1:** preserve that restriction unless product explicitly authorizes cross-team linking and defines which users may see the relationship and aggregate data.
2. **Rollup currency:** Deals may use different currencies. **Recommended v1:** return per-currency totals; do not add unlike amounts or imply conversion. A future conversion feature needs dated exchange rates and explicit reporting policy.
3. **Split semantics:** **Recommended:** revenue splits represent total quota credit and must equal 100% when a deal is finalized/closed; allow an incomplete total while a deal is still being assembled, with a clear “unallocated” remainder. Overlay credit is tracked separately and does not reduce revenue credit. Include the deal owner as a participant with an explicit revenue split when split tracking is enabled.
4. **Team access semantics:** **Recommended:** an active same-organization team membership grants access to that deal only. Viewing still requires the module-level view permission. Editing additionally requires `read_write`, the user’s module edit capability, and existing immutable/approval/critical-action gates. Document whether it can intentionally cross record-team visibility; do not silently weaken that boundary.
5. **Scoring availability:** **Recommended:** AI scoring is opt-in per organization, uses an organization-approved paid provider configuration, and is disabled when provider/privacy configuration is absent. Decide which users may score, re-score, and bulk-score.
6. **Score meaning and recalculation:** Agree on a transparent rubric, stale-score behavior, triggers, and display language. Do not label scores “conversion probability” until calibration against representative outcome data demonstrates calibration and bias/performance acceptance.
7. **External data handling:** Confirm contract, data residency/retention expectations, paid-tier configuration, and tenant disclosure before sending lead fields to Google. Paid Gemini API terms state prompts/responses are not used to improve products; free-tier content may be used for improvement. This is not a substitute for the organization’s privacy/legal approval.
8. **Forecast and quota attribution:** Forecast summaries, per-rep rollups, and forecast notifications currently attribute 100% of a deal to `deal_owner_id`. **Recommended v1:** splits are stored, displayed, and reportable, but forecast numbers are unchanged and the UI says so. Changing forecast/quota to split-weighted credit is a separate, explicitly scoped change to the forecast handlers and their tests.
9. **New permission actions:** `require_permission` supports only `view/create/edit/delete/export/import/bulk_edit`. **Recommended v1:** gate deal-team management on deal `edit` + record-level edit decision + `deal_teams_enabled`, and AI scoring on lead `edit` + `lead_scoring_enabled` + org-admin opt-in. Add dedicated profile permissions only if product needs finer control, and then plan the profile schema, admin UI, and default-profile migration as part of Phase 1.
10. **Parent soft-delete/restore:** **Recommended:** soft-deleting an account with visible children is blocked (or requires explicit reparent/detach of children) so no live account points to a deleted parent; restore re-validates the parent link and cycle rules.

Record each decision, owner, date, and any exception. If the decision changes a permission boundary, update threat model and tests before coding.

## 4. Target architecture and invariants

### Shared rules

- Every lookup and mutation scopes by `scope.org_id`, soft-delete status, and the applicable record/team policy. Validate related users and accounts within the same organization; never trust UUIDs from the client.
- Use the existing command/query handlers, repositories, routes, permission dependencies, audit service, response schemas, optimistic concurrency, and API client. Register every new router in `src/main.py` if a separate router is created.
- Keep business invariants in backend command handlers/services and reinforce them with database constraints/transactions where possible. Frontend validation is for feedback, not authority.
- Add audit events for parent changes, deal membership/split changes, scoring requests, score completion/failure, and feature-setting changes. Audit metadata should identify actor and record without copying PII prompts or secrets.
- Make new read APIs apply record visibility, not just organization filtering. Aggregates can leak sensitive data even when individual rows are hidden.
- Add bounded pagination, input limits, rate/resource admission for expensive work, idempotency where retries can duplicate work, and safe error responses.
- Add migration/model parity and test registration. Keep schema changes additive where possible; deploy compatible backend before enabling frontend behavior.

### Feature switches

Add organization-level switches/configuration using the existing settings/configuration pattern after verifying its ownership and caching behavior. Suggested switches: `account_hierarchy_enabled`, `deal_teams_enabled`, `lead_scoring_enabled`; AI also needs an approved provider/model setting and per-org quota. Disabled features must reject write/trigger APIs server-side, not merely hide controls.

## 5. Feature A — Account hierarchy and corporate rollups

### Data model and integrity

1. Keep `parent_account_id` as the authoritative direct-parent edge.
2. Add `ultimate_parent_id` only as a **derived, transactionally maintained index aid** if the expected hierarchy/report workload justifies it. Define it consistently: root rows reference themselves; descendants reference their root. It is never an independent editable field and may be rebuilt from parent links.
3. Add a tenant-consistent database relationship: first add a unique `(org_id, id)` constraint on `accounts` (none exists today), then a composite `(org_id, parent_account_id)` reference to `(org_id, id)`. This blocks cross-organization edges even if a handler regresses. Preserve the existing `ON DELETE SET NULL` behavior intentionally and verify Alembic/PostgreSQL behavior (composite `SET NULL` would also null `org_id` unless the column list is restricted, which needs PostgreSQL 15+ syntax) before changing it.
4. Add indexes based on actual query shape, including organization, parent/root, and soft-delete filters. Avoid blindly copying the plan’s proposed index order; validate with query plans and existing index conventions.
5. Migration sequence: nullable derived column; detect/report pre-existing cycles or invalid links; backfill in bounded batches or a controlled migration; add constraints/indexes after validation; verify downgrade semantics. Never silently “repair” bad production relationships by choosing an arbitrary root.

### Parent-change command

- Apply the change only after existing account scope/access and expected-version checks pass.
- Validate parent exists, is active/not deleted, is allowed by the agreed record-team policy, and is in the same tenant. Apply the **same** record-team rule in `CreateAccountCommandHandler` and `UpdateAccountCommandHandler` (update currently checks organization only), and look up the parent through `apply_scope` so a user cannot link to an account they cannot see.
- Prevent self-parenting and ancestor cycles. Because two concurrent reparent operations can form a cycle even if each checks current state, serialize hierarchy writes per organization (transaction-scoped advisory lock or an equivalent proven mechanism) for the initial implementation. Bound traversal by a documented maximum depth and fail closed if corrupted legacy data is encountered.
- Recompute the moved account and all descendants’ ultimate-root value inside the same transaction. Batch large descendant updates, but never expose a partially updated root cache. If very large trees are expected, move to a closure table or another explicitly designed hierarchy representation rather than silently weakening consistency.
- Write the account mutation, version increment, root updates, and audit event atomically. If SQLAlchemy version conflict occurs, return the existing 409/428 contract.

### Read API and rollup contract

Add `GET /api/v1/accounts/{account_id}/hierarchy` in the accounts route family, with `require_permission("accounts", "view")` plus the same record-level check as `get_account_by_id_for_scope` (`apply_scope`; accounts are not covered by `resolve_record_policy`). Return a typed response with:

- current account summary, visible parent, visible ancestors, direct children, and paginated descendants (or a documented bounded tree payload);
- `root_account_id`, hierarchy depth, and a cycle/corruption indicator only for administrators/diagnostic surfaces;
- group account count with explicit inclusion semantics;
- open-deal count/value grouped by currency, closed-won count/revenue grouped by currency, and non-deleted contact count (contacts have no `is_active` flag);
- explicit freshness or calculation timestamp if rollups become cached.

All linked account names and metrics must be built from records visible under the caller’s access scope: accounts through `apply_scope(…, Account, scope)`, deals through the deal projection (including the read-boundary loader criteria), and contacts through their existing scope. If a visible child points to a parent the caller cannot view, do not reveal the parent’s name or rollups; return a redacted relationship indicator or omit it according to product decision. Query metrics in grouped aggregate queries, not one query per descendant. Use `PipelineStage.stage_type` (`open`/`won`/`lost`) and `is_deleted` to define open/won metrics. Define whether inactive accounts (`Account.is_active = false`) participate. Also add `parent_account_id` (and the derived root, if adopted) to `AccountResponse` and the frontend `Account` type.

### Frontend

- Add parent account autocomplete to `AddAccountModal` and the edit form if present. Use a backend scoped search endpoint/service, exclude self and descendants, show team/visibility constraints, and send `parent_account_id` through existing account create/update contracts.
- Add a Hierarchy tab to `AccountDetailDrawer` (alongside `AccountOverviewTab`, `AccountContactsTab`, `AccountTimelineTab` in `components/accounts/drawer/`). Fetch with a query key including account ID and relevant filters; invalidate affected account hierarchy queries after create/reparent/delete.
- Render accessible clickable parent/child nodes, loading/empty/error states, pagination for large groups, per-currency rollups, and an “add subsidiary” action that preselects the parent.
- Add translation keys to every supported locale (`en`, `ar`, `nl`) and tests for keyboard interaction and restricted-parent redaction.

### Acceptance criteria

- Direct and multi-level cycles fail; cross-org links fail at handler and database boundary; simultaneous updates cannot commit a cycle.
- Reparenting updates all descendant root values atomically and survives retry/restart; migration backfills verified acyclic data and surfaces invalid rows.
- Hierarchy and rollups cannot reveal inaccessible records through names, counts, totals, timing-sensitive errors, or search results.
- Open pipeline, closed-won revenue, and contacts are correctly scoped, soft-delete aware, and currency separated.
- API schemas, frontend types, create/edit flows, optimistic concurrency, audit events, and feature-off behavior are covered.
- Create and update enforce the same record-team parent rule; soft-deleting/restoring a parent follows the §3 decision and never leaves a live child pointing at a deleted parent unnoticed.

## 6. Feature B — Deal teams and splits

### Data model

Use separate membership and split concepts so one person can receive revenue and overlay credit without ambiguous duplicate membership rows:

- `deal_team_members`: `id`, `org_id`, `deal_id`, `user_id`, `role`, `access_level`, `created_by`, `created_at`, `updated_at`, active/removal state as required; unique `(deal_id, user_id)` and indexes for `(org_id,user_id)` and `(org_id,deal_id)`.
- `deal_splits`: `id`, `org_id`, `deal_id`, `user_id`, `split_type` (`revenue`/`overlay`), `percentage NUMERIC(5,2)`, audit timestamps; unique `(deal_id,user_id,split_type)`, check 0–100, and tenant-scoped supporting indexes.
- Use canonical enumerated/check-constrained values, not free-form strings. Validate active user and organization membership on every mutation. Decide how deal deletion/soft deletion and user deactivation affect memberships, historical splits, and reports.

Enforce per-deal/per-type aggregate totals transactionally. PostgreSQL cannot enforce a cross-row sum with a normal `CHECK`; lock the deal row (`SELECT ... FOR UPDATE`) before modifying splits, recompute totals in the same transaction, and reject totals above 100%. Enforce exactly 100% at the agreed lifecycle transition (e.g. close/finalize), not necessarily during draft collaboration. Define handling for deal amount/currency changes and historical quota reports. Never sum across different currencies. `Deal.amount` is a `Float` column: store split **percentages** as `NUMERIC(5,2)`, derive monetary credit at read time with `Decimal` and a documented rounding rule, and do not persist float-derived amounts as authoritative values. Forecast numbers remain owner-attributed in v1 (§3 decision 8).

### Authorization integration

- Resolve access using one shared deal-team membership service/policy that receives the already tenant-scoped deal and current `Scope`.
- The membership may grant deal-specific view despite ownership/record-team mismatch only if the product decision explicitly authorizes that exception. It must not grant module access, access to sibling records/related account/contact, approval authority, delete rights, export rights, or permission to manage team members automatically.
- `read_write` grants ordinary deal edits only when the user also has module edit capability and passes all existing critical-action, approval, version, subscription, and audit rules. `read_only` never edits. Role does not silently imply privilege.
- Integrate policy into individual access resolution, deal list/count/aggregate/export queries, bulk operations, field access, approvals/governed actions, and any dashboards/search that expose deals. Do not add a special-case early return that skips teamspace or governance checks. Concretely, one shared membership predicate (e.g. an `EXISTS` subquery on `deal_team_members` for `scope.user_id`) must be applied consistently in:
  - `resolve_record_policy` / `record_is_visible` (single-record decisions);
  - `apply_scope` in `scope_guard.py`, whose personal Deal projection is currently `deal_owner_id == scope.user_id` only (add an explicit "deals I collaborate on" view rather than silently widening "My deals");
  - `bind_record_read_boundary` in `record_read_boundary.py`, whose global `with_loader_criteria` ceiling on `Deal` would otherwise hide the deal from every ORM select, join, and count;
  - `apply_record_team_scope` for Teamspace projections, plus global search, dashboards, reports, forecast drill-downs, and export.
- Do not reuse `RecordPermission` for persistent membership: it is edit-only, time-limited (`expires_at`), record-team bound, and only consulted under approval-based teammate policy.
- Team-management endpoints require explicit capability (see §3 decision 9: deal `edit` + record-level edit decision + feature switch in v1, or a new profile permission if product requires it) and deal access. Prevent users from granting themselves/others higher rights without authorization. Log membership and split changes.

### API contract

Provide typed endpoints under `/api/v1/deals/{deal_id}/team`:

- `GET`: list members and split details visible to caller;
- `POST`: add a member and initial role/access/splits;
- `PATCH /{member_id}`: update membership fields with expected deal version or explicit membership version;
- `DELETE /{member_id}`: remove membership; preserve audited historical split records per product rule;
- split mutations can be separate nested endpoints or part of an atomic team update, but the invariant and response must be clear.

Use the CRM’s optimistic concurrency contract for concurrent team changes. Return an explicit conflict on stale versions or split-total races. Validate member IDs, role/access enums, percentage precision/range, user active/org status, and duplicate operations. Add bounded list responses if a deal can have large teams.

### Frontend

- Add a team section/tab to `DealDetailDrawer`, backed by typed service methods and TanStack Query hooks.
- Display each member’s role, access, revenue percentage/value, overlay percentage/value, and currency. Do not imply overlay percentages add to revenue allocation.
- Add/update/remove modal with accessible user search limited to eligible organization members and explicit confirmation for access changes.
- Show split totals, remaining allocation, over-allocation, and finalized-deal requirements immediately; backend response remains authoritative. Display role/access permission controls only to authorized managers.
- Invalidate the deal, team, access, list, forecast, and relevant aggregate queries after changes.

### Acceptance criteria

- Every read/write path sees the same policy result, including list, search, aggregates, bulk, approval, export, and stale-cache paths.
- Cross-org/non-active users cannot be added; membership only grants the explicitly approved deal-level rights.
- Concurrent split updates cannot exceed the permitted totals; finalization enforces the agreed completeness rule; overlay does not alter revenue totals.
- Deal owner, approval, module permission, version, audit, and record-team behaviors have explicit regression coverage.

## 7. Feature C — AI lead prioritization

### Product and provider design

- Present this as a **rubric-based prioritization assessment**, not a conversion probability. Define a deterministic rubric and score anchors (for example: ICP fit, role relevance, engagement evidence, data completeness, and disqualifying risks) and ensure inputs support each dimension. Avoid unsupported claims about budget, authority, intent, or identity.
- Keep score and explanation separate from core lead lifecycle status and rating. Store model/provider identifier, prompt/rubric version, score timestamp, result status, and source-field fingerprint so stale assessments can be detected. Store only the compact result needed by CRM; do not persist raw prompts/responses unless an approved retention requirement exists.
- Use the organization-configured model through existing `GeminiProvider`; choose and validate an approved stable model per account/config. Do not hardcode “Gemini 2.5 Flash” or assume every project has access — note that `org_settings.loop_ai_model` and the provider fallback currently default to `gemini-2.5-flash`, so validate the configured model against `list_chat_models()` for the deployed key before enabling scoring. Google currently lists 2.5 Flash at $0.30/1M standard input tokens and $2.50/1M output tokens (including thinking tokens); check the live price/model availability before launch and forecast from measured prompt and response usage. Google’s docs also state 2.5 availability is limited for new projects and recommend newer models. Pricing is not a fixed cost guarantee.
- Require paid Gemini API billing/configuration for CRM customer data. Google states paid-service prompts/responses are not used to improve products, while free-tier content may be; paid terms also describe limited abuse-monitoring logging. Confirm the applicable DPA, region, retention, and legal basis with the organization before enabling.
- Use structured output with a constrained schema where supported, followed by strict Pydantic semantic validation. `generate_structured()` currently sets only `response_mime_type="application/json"`; add an optional `response_schema` parameter and return usage metadata (`usage_metadata` token counts) without breaking existing callers. Enforce score bounds, allowed band enum, score-to-band mapping, list count/length bounds, non-empty action, and no unknown fields. Keep a local model/provider interface for deterministic tests and later provider changes.
- Keep the AI assessment distinct from the existing user-maintained `Lead.rating` field and `ratings` filter; use names such as `ai_priority_score`, `ai_priority_band`, `ai_priority_reasons`, `ai_priority_model`, `ai_priority_rubric_version`, `ai_priority_input_hash`, `ai_priority_scored_at`.

### Data flow and jobs

1. Authenticated user requests score/re-score or a bounded batch. Server validates subscription, feature switch, permission, tenant, record visibility, status, quota, and rate/admission limits.
2. Create an idempotent score-job record (`org_id`, requester, target lead IDs, status, attempt count, timestamps, model/rubric version, safe error code) modeled on `CallBulkJob`: unique `(org_id, requester_id, idempotency_key)`, `payload_hash`, `claim_token`, `lease_until`, and a dispatch index on `(status, lease_until)`. The route only persists the job and returns `202`; it must **not** call `enqueue()` directly, because stage and production run `QUEUE_MODE=sync`, where `enqueue()` executes the handler inline in the HTTP request. A scheduler dispatcher (same pattern as `bulk_job_dispatcher.py`) claims due jobs and calls `enqueue("lead_score_job", {"job_id": ...})` so work runs in the scheduler executor in sync mode and in `src/worker.py` in SQS mode. Payloads carry only identifiers; never place lead PII in queue payloads/logs.
3. Worker opens its own database session, re-loads each lead by `org_id` and `is_deleted=false`, and re-checks that the request is still valid/current. Build a minimal allowlisted feature set; exclude name, email, phone, notes, and other direct identifiers unless a documented scoring need approves them (an email **domain type** such as corporate/free can be derived locally without sending the address). Treat all free text as untrusted data, label it as data, and instruct the model to ignore embedded instructions. This reduces risk but is not a prompt-injection security boundary.
4. Call the configured provider with timeout, bounded output, retry policy for transient failures, and concurrency caps. Registered task handlers are synchronous, while `generate_structured()` is async; bridge explicitly (e.g. `asyncio.run` per job in the worker thread, or a sync client path) and do not nest event loops. The shared client uses a 15 s timeout and one attempt — make the job’s retry/backoff own transient failures. Reuse `resource_admission.py`-style per-org advisory-lock slots for concurrency. Validate output, normalize fields, and persist score/job result atomically. A stale lead fingerprint marks the assessment stale or discards it according to policy.
5. Expose status/results with scoped endpoints and safe error codes. Keep a deterministic non-AI fallback separate and visibly labeled only if product approves it; do not silently present a heuristic as an AI score.

Before enabling SQS for this task, confirm worker deployment, visibility timeout versus worst-case batch duration, and DLQ/`maxReceiveCount` configuration; `src/worker.py` leaves failed messages for redelivery. `QUEUE_MODE=sync` is the current stage/production setting; durability comes from the job table and lease reclaim, not from the queue. Do not use FastAPI `BackgroundTasks` for work whose completion must survive process restarts.

### API and frontend contract

- `POST /api/v1/leads/{lead_id}/score` returns `202 Accepted` with a job ID/status; require the §3 decision 9 capability and apply quota/rate limits (reuse `RateLimiter(..., fail_closed_in_production=True)` as in `ai_chat/guards.py`).
- `POST /api/v1/leads/score-batch` accepts a bounded list or explicit filtered selection with idempotency key; reject unbounded “all leads” requests. Return `202` plus job ID and accepted/rejected counts without leaking hidden record IDs.
- `GET /api/v1/leads/score-jobs/{job_id}` returns only caller/org-authorized progress and safe error state.
- Lead list filters may include score/grade only when the caller can see the underlying lead; query count, ordering, and pagination must use the same scope. Add score fields to response schema and frontend type only if the feature is enabled and field permissions allow them.
- Frontend adds a score badge to the lead list surfaces (`LeadList.tsx`, `LeadCard.tsx`/`KanbanBoard.tsx`), a band/score filter in `FilterPanel.tsx`, and a detail card in `components/leads/drawer/LeadOverviewTab.tsx`, through the existing lead service and TanStack Query hooks. Explain rubric, timestamp, stale state, and “AI-generated assessment”; never imply certainty. Add a manual re-score action with status, retry, and failure feedback. Keep filter state in URL and include all filter parameters in query keys.

### Cost, privacy, and quality controls

- Track token usage/cost per organization and model, with a configurable monthly/daily ceiling, per-user action limit, batch cap, concurrency limit, and kill switch. No token-usage capture exists in the backend today, so this requires a new usage table/ledger fed from provider `usage_metadata`. Alert before spend caps; provider failures must not create retry storms.
- Do not send customer fields to free-tier Gemini. Keep API keys in existing secret configuration; never log them, full prompts, responses, or lead PII. Retain only score, explanation, model/rubric versions, usage totals, and timestamps needed for product/support.
- Run an offline evaluation on representative, appropriately authorized historical data before broad enablement. Measure rank quality (e.g. precision@k), stability, calibration only if probability language is considered, subgroup error patterns, and score drift. Include human review and a feedback mechanism; do not train/evaluate on data without approved purpose and governance.
- Validate score quality separately from syntactic JSON validity. A schema-conforming output can still be unsupported or biased.

### Acceptance criteria

- Unauthenticated, cross-org, invisible, deleted, unauthorized, over-quota, and over-limit requests cannot trigger or retrieve scoring.
- Job retries are idempotent; worker restarts do not lose accepted jobs; failures expose a safe actionable state and never overwrite a newer assessment.
- No free-tier usage, PII queue payloads, prompt/response logs, unbounded batch, silent fallback, or uncontrolled spend path exists.
- Scores are typed, bounded, rubric-versioned, timestamped, marked stale after relevant input changes, and described accurately in UI/API.
- Quality, privacy, cost, and feature kill-switch checks pass before organization rollout.

## 8. Phased delivery and dependencies

| Phase | Deliverables | Exit gate |
|---|---|---|
| 0. Product/security decisions | Signed decisions in §3; field/permission matrix; threat model; user-visible semantics; model/privacy approval and cost ceiling. | No unresolved permission boundary, currency behavior, or external-data approval. |
| 1. Shared foundations | Feature switches; permission-action decision (§3 decision 9) and, if chosen, profile permission schema/admin UI/default migration; route/schema conventions; audit/event conventions; migration strategy; test fixtures; shared access-contract tests. | Existing behavior preserved; feature-off server checks verified. |
| 2A. Account hierarchy backend | `(org_id, id)` unique key, schema/migration/backfill, unified create/update parent rule, safe parent command, cycle serialization, root maintenance, parent soft-delete rule, `AccountResponse` parent fields, scoped hierarchy/rollups API. | PostgreSQL migration and concurrency/access regressions pass; one Alembic head and no drift. |
| 2B. Deal team backend | Membership/split tables, locked split transaction, shared membership predicate wired into `resolve_record_policy`, `apply_scope`, `bind_record_read_boundary`, and `apply_record_team_scope`; endpoints and audit. | Authorization matrix and PostgreSQL concurrent split tests pass on every access path. |
| 2C. Scoring backend | Durable score-job table + scheduler dispatcher (Calls bulk-job pattern), async-provider bridge, `response_schema`/usage support in provider, token-usage ledger, provider/model validation, quota/rate limits, schema validation, result APIs and observability. | Worker restart/retry/idempotency tests in both `QUEUE_MODE=sync` and `sqs`; provider mocks; privacy and spend gates verified. |
| 3. Frontend integration | Account/deal/lead components, service/hooks/types, translations, URL filters, permission states and accessibility. | Contract tests, focused component tests, and browser flows pass for enabled/disabled and permission-denied states. |
| 4. Hardening and rollout | Full affected-repo CI, migration rehearsal, load/resource checks, telemetry dashboards, operator runbook, staged org allowlist. | Rollback/disable path demonstrated; no unresolved high-severity access/privacy/cost issue. |

Phases 2A and 2B may run in parallel after Phase 1 if their schema migrations are coordinated and do not create conflicting Alembic heads. Phase 2C may run in parallel only after Phase 0’s provider/privacy decision. Do not combine unrelated schema changes into one opaque migration; preserve one intended Alembic head and test clean upgrades/downgrades.

## 9. Verification strategy

### Backend

- Unit tests: hierarchy root calculation, ancestor traversal, cycle/corruption handling, policy matrix, split arithmetic/rounding, score schema/grade coherence, stale-input behavior, quota admission, queue idempotency, provider failure mapping.
- PostgreSQL tests: composite tenant constraints, reparent serialization under concurrent transactions, subtree cache updates, split total lock/race, migration from current supported revisions and empty database, downgrade/re-upgrade where supported, `alembic check`, and migration schema drift.
- API tests: same-org and cross-org IDs, record-team boundaries, module and action permissions, deleted/hidden records, optimistic concurrency, rate/quota limits, field access, error shape, and audit event transaction boundaries.
- Provider tests use fakes/mocks only; do not call Google or incur token cost in CI.
- Register every new SQLAlchemy model in `tests/conftest.py`; otherwise SQLite unit tests run without the table.
- Deal-team regression: a member whose user is outside the deal’s record team can (or cannot, per decision) see the deal through detail, personal list, counts, search, and joined queries — proving `bind_record_read_boundary` and `apply_scope` agree with `resolve_record_policy`.
- Scoring route regression: under `QUEUE_MODE=sync`, the score endpoint returns `202` without invoking the provider inside the request.
- Follow current backend workflow, including Ruff, compile checks, full pytest suite, PostgreSQL regression groups, migrations and drift checks. Use disposable databases only.

### Frontend

- Contract/type tests for every new API request/response and UI permission state; component tests for hierarchy, split editing, score states and error/empty/loading flows.
- Browser regressions: create/reparent account and view rollups; add/remove team member and splits; team-member access/edit denial; request/observe AI scoring, batch limit, failed job, stale score and disabled feature.
- Check accessibility, keyboard interactions, translations, URL filter restoration, query invalidation, and optimistic concurrency conflict UX.
- Follow current frontend CI, including format check, full lint/test, spreadsheets, typecheck, all listed browser regressions, build, and dependency audit. Do not claim the affected repo is green from focused tests alone.

### Rollout and operational validation

- Rehearse migrations against an empty disposable PostgreSQL DB and a restored, sanitized copy representing supported prior schema/data; compare row counts and hierarchy/split invariants before/after.
- Deploy backend schema/API compatibly before enabling frontend switches. Keep feature switches off until backend and frontend versions are compatible.
- Enable by internal organization, then a small approved tenant cohort. Monitor hierarchy query latency, policy denials, split conflicts, job queue age/failures, provider errors/latency, token cost, stale-score rate, and user feedback.
- Provide kill switches: disable scoring triggers/provider calls; disable team-management writes without erasing existing access data; hide hierarchy UI while maintaining valid stored relationships. Define emergency policy for already granted deal-team access.
- Stage validation must use authorized accounts and isolated fixtures. Verify real sign-in, role/permission behavior, account grouping, deal-team access, scoring job lifecycle, and logs without exposing PII. A health endpoint or local CI does not prove these flows.
- Production promotion requires the CRM deployment audit and exact-commit CI/deployment gates in workspace `AGENTS.md`; this plan itself does not authorize deployment.

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Hidden-data leakage via hierarchy rollups or deal membership | Access policy matrix, scoped aggregate queries, cross-team decision, query-path parity tests, deny-by-default. |
| Cycles or stale root stamps from simultaneous account edits | Authoritative parent edge, serialized reparent, bounded validation, atomic descendant recompute, repair diagnostics. |
| Incorrect financial totals | Decimal percentages, locked transaction, lifecycle completeness rule, per-currency totals, explicit overlay separation. |
| AI score appears more certain than evidence supports | “Prioritization assessment” language, rubric/version/timestamp, human oversight, evaluation and feedback. |
| Prompt injection or PII exposure to provider/logs | Minimize fields, paid tier, approval, safe logging, no prompt payload in queue, output validation, data-handling review. |
| Provider outage or unexpected spend | Durable bounded jobs, idempotent retry, quota/cost caps, admission limits, monitoring and kill switch. |
| Migration locks, long backfill, or partial rollout | Additive rollout, measured backfill, compatibility window, migration rehearsal, feature flags and documented rollback limits. |

## 11. External research and assumptions

Prices and model availability can change. These links were checked 22 October 2026 and must be rechecked before enabling production use:

- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing): pricing distinguishes input/output, standard/batch/priority and free/paid tiers; current table lists Gemini 2.5 Flash paid standard rates at $0.30/1M input and $2.50/1M output including thinking tokens. Measure actual token use to forecast cost.
- [Gemini model list](https://ai.google.dev/gemini-api/docs/models): 2.5 model availability/access guidance and current recommendations. Model selection must remain configurable and validated.
- [Gemini API terms](https://ai.google.dev/gemini-api/terms): paid-service data handling differs from free-tier usage; confirm current terms and organization DPA before sending CRM data.
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output): schema-constrained output is supported, but semantic validation remains an application responsibility.
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): use data-flow and trust-boundary review for CRM-to-provider processing.

This document is a design and implementation plan, not proof of feature completeness, compliance, model accuracy, CI success, or deployment readiness. Revalidate source paths, prices, policies, and workflow commands at the start of each implementation phase.
