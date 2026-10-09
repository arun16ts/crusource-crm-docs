# Super Admin Phase 1 implementation plan

Date: 9 October 2026. Status: **COMPLETE — local backend phase; production cutover awaits Phase 2/6.**

Implementation evidence, contract amendments and release boundaries: [Phase 1 review package](superadmin-phase1/README.md). Verification: 78 Phase 1 cases plus 61 targeted regressions passed; both existing browser suites passed. The design below is the approved implementation specification; final decisions are recorded in the review package.

Phase 1 delivers the backend for owner-invited platform staff: invitation, email activation, password setup, mandatory MFA, recovery and revocation. It establishes reliable delivery without changing customer organization onboarding. The CRM-aligned staff screens follow in Phase 2.

This plan builds on the [Phase 0 baseline](superadmin-phase0/BASELINE_REPORT.md), [contracts](superadmin-phase0/CONTRACTS.md), [migration checklist](superadmin-phase0/MIGRATION_CHECKLIST.md) and [overall delivery sequence](SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md). It adds explicit enrollment-resume and revoked-staff recovery requirements; these must be reflected in the implementation contracts before coding their handlers.

## 1. Required outcome

An authenticated platform owner creates an invitation. The application commits the invitation and a delivery job together. A dispatcher sends the activation email. The recipient sets a password and enrolls an authenticator; only successful MFA completion grants platform access. The owner can resend a pending invitation, cancel it, explicitly reset staff sign-in or revoke staff access.

The implementation must preserve existing owner/operator credentials, valid legacy activation links and live enrollment sessions. Database failure must not send an uncommitted invitation. Concurrent reset/revoke/cancel must not allow a stale enrollment or session to restore access.

This phase includes backend models, additive migrations/backfill, CQRS handlers, APIs, delivery dispatch, test fixtures and operational documentation. UI redesign, demo intake, support tickets, analytics and production deployment remain in their agreed later phases. CRM registration/invites/OAuth receive regression checks and only narrowly necessary identity-uniqueness integration; their user journeys remain unchanged.

## 2. Architecture and existing constraints

Use the existing FastAPI/SQLAlchemy/Alembic stack and `src/modules/platform_auth`. Follow SOLID with focused use cases and narrow dependencies:

```text
Route → request validation + authentication admission → command/query handler
Handler → repositories + focused domain/integration services
Command transaction → state + security event + idempotency result + delivery intent
Committed delivery intent → dispatcher → SES adapter
```

- Commands write; queries read. One handler per meaningful use case. Repositories own SQL and scoped persistence; reusable services own normalization, token/delivery crypto and transition policy. Do not add a generic workflow framework.
- Keep `routes.py` and `schemas.py` compatible with current module conventions; split growing concerns into focused files rather than restructuring unrelated authentication code.
- Preserve platform cookies, mandatory MFA, password validation, TOTP replay checks, origin/CSRF admission and CRM/platform identity isolation.
- The current [guard](../crusource-crm-backend/src/modules/platform_auth/services/sessions.py) commits its identity/last-seen transaction before the handler runs. New sensitive commands must revalidate the actor's current session/credential/owner authority inside their own transaction. An object returned by the guard is not a transaction-held authorization guarantee.
- The current [review handler](../crusource-crm-backend/src/modules/platform_auth/handlers/review_request.py) sends email before commit and combines resend with reset. Replace these behaviors through dedicated use cases.
- The current [MFA handler](../crusource-crm-backend/src/modules/platform_auth/handlers/verify_challenge.py) finds legacy requests by email. New enrollment must bind to invitation id and generation; do not leave completion dependent on an email lookup.
- Existing `RecordEffect` jobs require customer organization/record ownership. Add a focused platform-delivery outbox; preserve the existing outbox's constraints.
- The repository currently has no Graphify graph. Verify load-bearing decisions in source; use/update the graph when available. No semantic extraction/provider key is required for this plan.

Phase 2 frontend boundaries are already fixed: Next.js thin routes, service-first API calls, TanStack Query for server state, Redux Toolkit for shared UI preferences, URL parameters for shareable filters and local state for drafts. Phase 1 supplies the API/OpenAPI contracts and error semantics these layers need; it does not add Redux copies of server records.

## 3. Delivery order and review boundaries

Implement sequentially in small reviewable changes. Each change includes its meaningful tests; do not postpone all verification until the end.

| Step | Deliverable | Completion evidence |
|---|---|---|
| 1.1 | Final persistence, transaction and compatibility design | State/lock/identity rules documented; all existing identity writers identified |
| 1.2 | Additive schema and legacy backfill | Empty/legacy PostgreSQL upgrades pass; repeat backfill changes nothing |
| 1.3 | Owner invitation and staff-management commands/queries | Authorization, version, idempotency and lifecycle tests pass |
| 1.4 | Activation, MFA, resume and recovery integration | New/legacy enrollment, replay, cancellation and revocation scenarios pass |
| 1.5 | Durable delivery dispatcher and SES boundary | Commit failure, duplicate dispatch, timeout, stale-generation and restart tests pass |
| 1.6 | Retired public application/approval writers | Retired endpoints cannot create, approve, reset or email accounts |
| 1.7 | Full Phase 1 regression and PostgreSQL race matrix | Recorded passing results; no skipped required database checks |
| 1.8 | Phase 2 API handoff and release runbook | OpenAPI/examples, configuration names, migration/rollback steps and limitations documented |

Work on schemas/services in 1.1–1.4 may depend on a fake delivery adapter; the final end-to-end flow is not complete until 1.5–1.7 pass. Do not release a partially migrated authentication stack.

## 4. Step 1.1 — Freeze implementation decisions

Recheck nested Git states and Alembic heads before editing. Phase 0 observed backend HEAD `33a6ff4ae16b13c25e04af516a402b38f3d1afd1` and migration head `20261008_webhook_receipts`; these are starting references, not assumptions about the deployed database.

Resolve these details in code-facing DTO/domain definitions and a short architecture decision record:

1. **Provisioning authority:** owner only; invitation input cannot set owner, organization, capabilities or credentials. Owner bootstrap/recovery stays an operational command. Existing active operators retain access.
2. **Identity normalization:** one canonical email function. Inventory users, legacy requests and live invitations before adding normalized uniqueness. A CRM identity cannot be converted into platform staff by invitation.
3. **Database enforcement:** prove the chosen normalized email index/representation matches application normalization on PostgreSQL, including case, whitespace and supported Unicode/domain forms. Check all user-creation paths, including CRM signup, invitations and Google OAuth. Unresolved collisions stop migration; never choose a winner or silently merge accounts. A platform-only SELECT/advisory lock cannot protect against an unrelated CRM writer.
4. **Recovery target:** creating an invitation for an existing active/revoked staff identity returns a clear conflict directing the owner to reset-sign-in. Reset may target an eligible non-owner platform identity, including a revoked one; it never grants access until new activation/MFA finishes. A CRM identity, owner or credential-less Super Admin flag is ineligible.
5. **Concurrency:** publish one lock-order table covering actor authorization, normalized identity reservation, invitation/legacy lineage, credentials, sessions and delivery jobs. Include commands, login/MFA, owner recovery and dispatch. Acquire multiple same-type rows in stable order; never wait on an external provider while holding database locks. Verify the order with real PostgreSQL races.
6. **Contract amendments:** define an authenticated pending-enrollment resume query and the distinction between invitation link expiry and enrollment-session expiry. Freeze safe errors and response projections. Retain existing login/activation/MFA request/response compatibility.

**Done when:** every lifecycle action has an actor, permitted starting state, transaction boundary, invalidation rule and expected test. No unresolved identity-uniqueness race is deferred to frontend validation.

## 5. Step 1.2 — Persistence and migration

Use additive changes. Proposed model responsibilities:

| Model/change | Required data and constraints |
|---|---|
| `PlatformInvitation` | UUID; normalized email/display name; purpose `join` or `reset`; lifecycle status; version; generation; token digest; link expiry; enrollment expiry; inviter; target user; accepted user; unique nullable legacy-request lineage; UTC timestamps |
| `PlatformDelivery` | Invitation id + generation; delivery state; encrypted short-lived material + key id; attempts; next attempt; lease expiry/token; safe failure category; provider acceptance metadata; timestamps. Unique invitation/generation/template intent. |
| `PlatformCommandReceipt` | Principal/use-case/resource/key scope; request hash; committed response/status; expiry. Unique scoped idempotency key. Never stores raw activation/session tokens, passwords or MFA material. |
| Credential/session extensions | Administrative version for staff commands; invitation/generation lineage for enrollment; credential/session security generation if needed to reject superseded sessions consistently |
| Identity constraint | Database-enforced normalized user uniqueness after collision preflight and CRM compatibility verification; preserve display values and existing ownership |

Names may follow established conventions during implementation; responsibilities and constraints are required. Avoid redundant persisted status where it can be projected from the latest delivery job. Keep administrative version separate from routine TOTP/last-seen bookkeeping so an ordinary login does not unnecessarily invalidate a staff-management form.

Database constraints must enforce valid states, positive versions/generations, unique non-null activation digests, unique legacy lineage and at most one pending/enrolling invitation per normalized email. Materialize expiry before issuing replacements; do not place `now()` in a partial-index predicate.

Register new models in application model initialization and `tests/conftest.py`. Register any new router explicitly in `src/main.py`. Reuse the existing router prefix where practical.

Backfill requirements:

- Preserve owner id, encrypted secrets, password hashes, replay counters, active operators and eligible sessions. Do not generate replacement credentials or send emails.
- Map valid approved requests to pending invitations with original digest/expiry. Map expired requests to expired history.
- Bind live interrupted enrollment to its original user/session and new invitation lineage. Keep its original limits.
- Preserve failed-delivery visibility; a digest cannot reconstruct an old raw token. The owner issues a new generation through resend when needed.
- Archive pending/unverified/rejected public applications without granting access.
- Keep revoked accounts revoked; quarantine ambiguous/orphan/CRM-linked identities. A flag alone never becomes a credential.
- Make backfill rerunnable through unique lineage. Report aggregate counts and opaque problem references, not email lists or secret material.

Use separate schema/constraint/backfill revisions if this makes collision preflight or database lock duration safer. Rehearse rollback before enabling writes; do not equate Alembic downgrade with safe operational rollback after new invitations are used.

**Done when:** empty and representative legacy PostgreSQL upgrades succeed, collision fixtures fail safely, a second backfill is a no-op, and owner/operator/legacy-link/enrollment preservation is proven.

## 6. Step 1.3 — Invitation and staff use cases

Paths below include the existing `/api/v1/superadmin/auth` prefix.

| Endpoint | Input → result | Required behavior |
|---|---|---|
| POST `/invitations` | Name/email → 202 invitation | Owner only; pending invitation + delivery intent + event + receipt commit together |
| GET `/invitations` | Bounded filters/sort/page → invitation page | Owner only; server counts, stable sorting, no secret fields |
| POST `/invitations/{id}/resend` | Expected version → 202 invitation | Pending/unexpired only; rotate token/generation/48-hour link expiry; supersede old jobs |
| POST `/invitations/{id}/cancel` | Expected version/reason → invitation | Pending/enrolling only; invalidate links and associated enrollment sessions |
| GET `/staff` | Bounded page → staff page | Owner only; owner/active/revoked state and administrative version |
| POST `/staff/{id}/reset-sign-in` | Expected version/reason → 202 invitation | Explicit recovery: revoke sessions, invalidate old lineage, disable usable sign-in credentials and create a fresh reset invitation atomically |
| POST `/staff/{id}/revoke` | Expected version/reason → staff | Disable staff access; revoke sessions, invalidate live invitations and supersede delivery. Reject owner target. |

Use the Phase 0 field lengths and DTO projections. Unknown fields are rejected. All new privileged writes require a UUID `Idempotency-Key`; updates also require `expected_version`.

Command protocol:

1. Validate fields and browser admission. Start the use-case transaction and revalidate current owner/session authority.
2. Resolve the scoped idempotency receipt; same key/body replays the committed result, different body returns `409`. Reauthorize before replay. Database uniqueness chooses one winner for simultaneous duplicate keys.
3. Acquire the agreed locks and recheck target eligibility, lifecycle and expected version.
4. Perform exactly one state/version change; append a sanitized security event and delivery intent where applicable.
5. Store the response receipt and commit. Return only after successful commit. No provider call occurs here.

For any validation/conflict/commit failure, roll back the whole business operation. Replaying a completed command must not rotate another token, reset MFA again or enqueue another message. Keep successful receipts at least 24 hours with a bounded cleanup job. Map expected database conflicts to stable safe errors; do not expose SQL/provider exception text.

**Done when:** each command has positive, unauthorized, invalid-state, stale-version, duplicate-key and failed-commit coverage. Resend cannot reset an accepted staff member; reset/revoke cannot affect the owner or a CRM identity.

## 7. Step 1.4 — Activation, MFA, resume and recovery

Use a 48-hour single-use activation link and preserve the current 12–128-character activation password policy. Store only a token digest for redemption. Email links use a fragment, keeping tokens out of URL queries/access logs.

| State/action | Required result |
|---|---|
| Pending + valid token/password | Consume digest, bind/create eligible platform user, store encrypted MFA secret, create 10-minute enrollment session, move invitation to enrolling |
| Enrolling + valid non-replayed MFA | Atomically accept invitation, activate staff credentials/identity, consume pending session and issue authenticated session |
| Enrolling + reload/interruption | Resume using the existing valid pending session; do not recreate secret, reset attempts or extend expiry |
| Pending/enrolling + owner cancel/revoke/reset | Invalidate applicable generation/session; subsequent activation/MFA fails |
| Expired pending link/enrollment | Fail safely; require owner cancel/reissue or reset as appropriate |
| Accepted + old link/MFA/session | Token/session replay fails; no reactivation |
| Revoked staff + authorized reset | New recovery lineage permits re-enrollment; old credentials/sessions remain unusable; access returns only after MFA succeeds |

Add `GET /api/v1/superadmin/auth/enrollment` as a focused resume query. It accepts only an existing live `enroll` cookie bound to eligible current lineage, returns the minimum enrollment information needed to display setup again, and sets no-store headers. Enforce the platform read-origin/custom-header policy; never return enrollment material for an ordinary authenticated/challenge session, expired generation, cancelled invitation or another identity. Preserve the existing controlled owner-bootstrap enrollment case. No attempts, secrets or expiry are changed by this query.

Keep the existing full-session four-hour lifetime, 30-minute idle expiry, pending-session ten-minute expiry, five-attempt limit, rate admission, secure host-only HttpOnly/SameSite Strict cookie and CSRF behavior. Failed attempts must still persist their counters safely. Cookie issuance must follow a successful database commit; a failed commit cannot leave a successful authentication response.

The invitation becomes the authority for non-owner enrollment eligibility. Do not accidentally allow a revoked user to authenticate because reset temporarily adjusts flags; equally, do not block authorized recovery merely because the original revoked user is inactive. Test the complete flag/credential/session matrix explicitly.

Legacy compatibility is bounded by original expiries. Once a legacy request has new lineage, that lineage is authoritative: a rejected/cancelled new invitation must not fall back to an old approved request and reactivate. Maintain old link/session reads only where they are legitimately unmigrated and eligible. Preserve current login/activation/MFA wire shapes; add new idempotency requirements to the new owner command endpoints, not blindly to existing browser auth calls.

**Done when:** new and legacy activation, owner login/recovery, reload/resume, expired sessions, duplicate TOTP, cancelled enrollment, revoked-staff recovery and reset/MFA races all pass.

## 8. Step 1.5 — Durable platform email delivery

Implement a focused repository/dispatcher and injectable email adapter. Reuse the existing scheduler and SES client conventions. The current Boolean email helper cannot distinguish transient/permanent outcomes; add a narrow typed adapter result without changing unrelated CRM mail contracts.

Delivery sequence:

1. Scan a bounded set of due committed jobs. Claim each just before processing with a database-backed lease and unique attempt token; multiple scheduler processes must not claim the same lease.
2. Check current invitation generation/state/expiry. Obsolete jobs become superseded; no eligible send is attempted with expired material.
3. Decrypt short-lived material in memory and send through the adapter outside database locks.
4. Record provider acceptance or a sanitized failure category only if the lease/attempt still belongs to this worker. An old worker completion cannot overwrite a newer generation's status.
5. Retry transient timeout/throttle/provider failures with bounded exponential backoff/jitter. Permanent configuration/recipient rejection fails visibly; owner resend creates a new generation. Stop at token expiry or the retry budget.
6. Clear encrypted material after acceptance, terminal failure, expiry or supersession. Reconcile abandoned leases and expire invitation state through scheduled maintenance.

Initial tunable defaults: 30-second polling, at most 25 candidates per scan, at most five concurrent sends, a two-minute per-job lease, provider attempt budget below 30 seconds and at most six application attempts. Backoff starts at one minute and caps at four hours; total retry time is always bounded by invitation expiry. Document SDK retry settings so nested SDK retries cannot exceed the lease. Do not claim a large serial batch whose leases expire before its jobs start.

Use a dedicated authenticated-encryption delivery key/key-id configuration; preserve the existing MFA key. Keep the decrypting key available until its outstanding jobs expire. Missing configuration prevents a send-capable invitation from being reported as successfully queued. Local tests inject generated keys and fake adapters; no real mail or secret values in reports.

`202` means stored/queued. `sent` means provider accepted, not mailbox delivered. A crash after acceptance can cause duplicate mail; do not promise exactly-once delivery. Cancellation/resend may race with an already-running provider call, so an obsolete email can arrive, but its token must be unusable. Enforce that guarantee at redemption/MFA, not only in the dispatcher.

Register dispatch/maintenance with `src/shared/services/scheduler/scheduler_engine.py`. If worker/queue integration is needed, register a narrow task in the existing registry. The database outbox remains durable even when `QUEUE_MODE=sync`; in-process enqueue alone is insufficient. Fake mode must be explicit and forbidden as a silently successful production configuration.

**Done when:** failed commit sends nothing; two dispatchers respect leases; provider timeout/rejection and abandoned leases recover; old worker completion cannot corrupt current state; expired/superseded links never grant access; encrypted material is cleaned up.

## 9. Step 1.6 — Retire the public application writers

Retire writes to `/request-access`, `/verify-email` and `/requests/{id}/review`. Also retire the old `/operators/{id}/revoke` writer or route it through the same new transaction/invalidation implementation; it must not bypass expected-version/idempotency guarantees. Prefer an explicit `410` for obsolete privileged writes once cut over.

Legacy owner-only read endpoints may remain temporarily for the Phase 2 migration; bound and project them safely. Old public pages can remain temporarily visible but submissions must receive honest invitation-only guidance and perform no writes/email. Phase 2 removes those pages/links and developer branding.

Do not deploy retirement separately from a usable compatible owner workflow. Phase 1 completion is a tested backend boundary; the production cutover is coordinated with Phase 2 UI and Phase 6 release checks. Old approval/reset writers cannot remain active alongside new invitation writers without the shared lock/transaction protocol. Migration/backfill itself never sends email.

**Done when:** obsolete endpoints cannot create access requests, rotate credentials, approve accounts or send mail; valid old activation/enrollment reads still work only within their original limits.

## 10. Verification matrix — Step 1.7

| Area | Required cases |
|---|---|
| Authorization | Owner succeeds; operator, CRM token, forged owner fields, missing/invalid CSRF, untrusted origin and expired/revoked session fail; actor is rechecked in transaction |
| Lifecycle | Invite, resend, cancel, activation, enrollment, resume, acceptance, reset, revoke and expiry; invalid transitions have no side effects |
| Idempotency/version | Same-key retry; different-body conflict; simultaneous same-key commands; stale version; failed transaction leaves no completed receipt/job |
| Credentials | Password policy, encrypted MFA, TOTP replay and attempts, session expiry/idle, owner protection, revoked-staff recovery, no credential-less flag promotion |
| Migration | Empty/legacy schema, backfill twice, case collisions, orphan lineage, failed delivery, valid/expired links, active/revoked staff, original-session preservation |
| Delivery | Commit failure, provider timeout/rejection, double dispatch, lease expiry, stale completion, resend/cancel during send, key unavailable/rotation, payload cleanup |
| Isolation | CRM signup/invite/OAuth behavior preserved; platform tokens cannot authorize CRM access and CRM tokens cannot authorize platform access |
| API projection | Pagination totals/sort bounds; no secret/hash/activation URL in list, errors, receipts or logs; safe field validation |

Required PostgreSQL races: invite/invite; invitation activation/CRM identity creation; resend/activation; activation/cancel; MFA/revoke; reset/MFA; duplicate TOTP; duplicate idempotency key; worker/worker and dispatch/resend. Assert final row/session/job invariants as well as HTTP outcomes; use barriers and bounded lock timeouts, not timing-only sleeps.

Extend the existing PostgreSQL fixture carefully: it currently uses the globally configured engine and temporary schemas. Require an explicitly verified dedicated test database/role and safe cleanup boundaries. Do not enable its opt-in flag against an unknown application database. Include actual migrated constraints/indexes; the current minimal fixture omits some customer FKs and cannot alone prove the full migration.

Run targeted backend pytest files through `.venv\Scripts\python.exe`; add focused files for invitations, recovery, migration, outbox and PostgreSQL concurrency. Rerun the relevant existing platform-auth/superadmin-guard tests. Retired public-flow tests must be deliberately replaced with retirement assertions; do not keep asserting obsolete onboarding behavior.

The selected Phase 0 suite passed 58 tests. That number is a baseline, not a fixed Phase 1 target. Require all retained behavior plus the new matrix to pass. Do not report skipped PostgreSQL races as complete. Run frontend auth browser regressions where transport-compatible behavior can be exercised; invitation UI coverage arrives in Phase 2. A documentation-only plan change does not require rerunning the application test suites.

## 11. Files and integration points

| Area | Expected touchpoints |
|---|---|
| CQRS | `src/modules/platform_auth/commands`, `queries`, focused `handlers` for create/list/resend/cancel/reset/revoke/resume/dispatch |
| Persistence | Focused invitation/delivery/receipt model and repository files under `platform_auth/repositories`; existing credential/session models |
| Auth | Existing `activate.py`, `verify_challenge.py`, `login.py`, `recover.py`, `revoke.py`, session/crypto/rate services |
| API | `platform_auth/routes.py`, schemas/projections, OpenAPI registration |
| Delivery | Focused template/encryption/email-adapter/dispatcher services; existing scheduler/task registry integration |
| Migration | `alembic/versions`, app model initialization, `tests/conftest.py`; narrowly necessary global identity constraint integration |
| Verification | New focused pytest modules and dedicated PostgreSQL fixtures; retained auth/guard/CRM identity regressions |
| Documentation | Updated contracts, migration inventory/runbook, API examples and Phase 1 implementation report |

Do not import documentation fixture models into production. Move agreed shapes into application DTOs and verify the running OpenAPI against the reviewed contracts. Do not commit empty command/handler placeholders or claim a model/route alone proves a working feature.

## 12. Handoff, configuration and rollout — Step 1.8

Provide Phase 2 with invitation/staff DTOs, all endpoint examples, error codes, list defaults, version/idempotency behavior, delivery-state labels and the enrollment-resume contract. Document that the existing frontend platform POST helper needs a narrow way to pass `Idempotency-Key`; add it with service/hook integration in Phase 2, preserving CSRF and same-origin behavior. The client must retain a key for retries and use a new key for a new user action.

Development needs no provider API keys: generated test-only encryption keys, fake email and an isolated PostgreSQL database are sufficient. Real integration later needs the configured SES region/sender/identity and runtime role or credentials, exact platform/CRM HTTPS origins, preserved MFA key, delivery encryption key/key-id and a deployed dispatcher. Configure secrets through the environment/secret store; never include values in this plan, logs or source.

Release runbook must cover collision inventory, backup/restore rehearsal, migration lock/runtime measurement, paused privileged writers/delivery, schema/backfill, compatible API/UI deployment, single active writer design, smoke checks and monitored enablement. Keep legacy activation compatibility until original outstanding expiries pass. Retain the legacy audit tables until separately reviewed removal.

Rollback after new-format writes means a compatible application rollback with invitation writes/delivery paused if necessary. Keep additive tables, current revocations and history. Do not drop tables, re-enable public approvals or restore a stale credentials snapshot as routine rollback. Real SES/bounce behavior and deployed worker recovery remain Phase 6 release gates.

## 13. Phase 1 completion checklist

- [x] Additive PostgreSQL migrations and rerunnable backfill pass, with safe collision failure.
- [x] Owner-only invite/list/resend/cancel/staff/reset/revoke APIs work with typed contracts, expected versions and idempotency.
- [x] New and legacy activation/MFA/resume work; owner and existing operators remain compatible.
- [x] Revoked/cancelled/expired/superseded generations cannot restore access, including concurrent requests.
- [x] Durable encrypted delivery intents commit with the command; dispatcher passes restart/lease/failure tests.
- [x] Public application and obsolete privileged writers are retired without an alternate bypass.
- [x] Required PostgreSQL races and relevant CRM/platform regressions pass with recorded evidence.
- [x] No plaintext tokens, passwords, MFA secrets or activation URLs leak through tested persistence projections/logs/reports.
- [x] Phase 2 API handoff and the migration/rollback/configuration runbook are complete.
- [x] Remaining live-provider/deployment checks are explicitly listed as Phase 6 gates.

Local completion evidence is in [VERIFICATION.md](superadmin-phase1/VERIFICATION.md). The next implementation phase is Phase 2: CRM-aligned platform shell, staff sign-in and invitation/access screens. Deployment requires the separate release gates.
