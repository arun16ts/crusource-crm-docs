# Crusource CRM Security: Verified Findings and Updated Implementation Plan

**Prepared:** 2026-10-22
**Scope:** CRM only: `crusource-crm-backend/`, `crusource-crm-frontend/`, and `crusource-crm-docs/`.
**Compared against:** `CRM_SECURITY_REVISED_PHASE_PLAN.md` and Antigravity's `cyber_security_open_issues_and_remediation_plan.md`.
**Source snapshot:** backend `ad487d1`; frontend `03104801`. These are the current local HEADs checked during this review. No application code was changed and no tests or deployments were run.

## Executive assessment

The Antigravity plan contains useful, source-confirmed issues, but it mixes security defects, compatibility questions, test-environment concerns, and unverified staging/evidence work. Do not execute it verbatim. In particular, do not add a client-controlled version-check bypass, do not run its proposed credential-revocation SQL until the affected identity and deployed schema are confirmed, and do not treat a BFF migration as a small patch.

The current local source confirms:

- Access and refresh tokens are stored in browser `localStorage`; reducing token theft exposure is a valid hardening objective.
- Account and contact updates currently require `expected_version` and return 428 when it is missing. This is a deliberate compatibility change that needs caller inventory and communication, not an authorization bypass.
- The listed lead, deal, task, call, and meeting update handlers do not currently enforce `expected_version`. The broad OCC gap is real for these checked paths; verify model version columns, write paths, product/quote coverage, and UI callers before deciding exact scope.
- The login resend UI supports login OTP verification, but the backend resend handler only accepts `register` and `forgot_password`, defaulting other values to registration. Login OTP resend is a real functional gap.
- `src/proxy.ts` skips paths containing any dot before injecting CSP. This can omit CSP and other `protect()` response behavior on dotted application routes. The exact impact is missing middleware policy, not an authenticated-route or authorization bypass.
- Login and OTP rate limiters use Redis-backed admission and are configured to fail closed in protected environments. Process-local fallback exists for other limiters and for non-protected environments. Treat limiter behavior as per-use-case and verify the remaining protected endpoints; do not describe all rate limiting as absent.
- The Redis test is explicitly skipped when `REDIS_URL` is unset and is an integration check when configured. If the variable is set but Redis is unavailable, it fails. That is a test-environment/reporting issue, not evidence that production limiter behavior is broken.

The local source does not establish current staging behavior, whether historical captured credentials remain valid, whether any CORS response is still misconfigured in deployment, or whether cross-tenant access is exploitable. Those require controlled staging evidence. Antigravity's claimed test results were not rerun in this review and should be treated as reported, not independently verified.

## Finding disposition

| Antigravity item | Assessment | Decision |
|---|---|---|
| Flag 1: 428 breaks integrations | **Behavior confirmed; impact unproven.** The handlers enforce `expected_version`; no supported external integration/API contract was established by the plan. | Inventory documented and real callers. Keep stale-write protection. If compatibility is needed, version it or provide a controlled server-to-server contract; never accept a caller-set `X-Bypass-Version-Check`. Prefer `If-Match`/ETag only as a documented API evolution, with a deprecation window and atomic compare-and-update. |
| Flag 2: OCC incomplete | **Gap confirmed in listed update handlers.** Model/API/UI coverage must be mapped before expanding. | Prioritize data-loss-prone interactive edits. Add atomic database-level compare-and-update, consistent conflict responses, and UI conflict handling. Do not rely only on read-then-compare in Python, which can race. Include imports, bulk operations, background jobs, and alternate write paths. |
| Flag 3: login MFA resend absent | **Confirmed.** `ResendOtpCommandHandler` maps unsupported purposes to `register`; login page has an OTP verification state but no demonstrated resend action. | Add login-purpose resend only after verifying an eligible pending challenge. Reuse shared limiter, generic responses, cooldown, one-time replacement/expiry semantics, and tests for enumeration, replay, and abuse. |
| Flag 4: Redis test failure | **Conditionally confirmed.** Test skips without `REDIS_URL`; with it set but no reachable Redis, the assertion fails. | Keep as an explicitly marked Redis integration test requiring a disposable Redis service, or make it mock-backed if it is intended to be a unit test. Never silently skip required CI coverage. Do not change production behavior just to make this test pass. |
| Flag 5: dotted-path proxy skip | **Confirmed.** `pathname.includes(".")` bypasses CSP setup for dotted routes. | Narrow the matcher to actual static asset namespaces/extensions while retaining coverage for application routes. Confirm matcher behavior using dotted route segments and normal static files. |
| Item A: localStorage to BFF | **Exposure confirmed; migration is an architectural option.** LocalStorage tokens are accessible to same-origin injected script. This does not itself establish an exploitable XSS or cross-tenant flaw. | Keep as a planned security architecture project. First inventory all token consumers and OAuth/onboarding flows; design session lifecycle, refresh/revocation, CSRF/origin checks, API forwarding, caching, and rollout compatibility. HttpOnly cookies reduce token extraction but do not stop injected script from acting as the user. |
| Item B: tester credentials/evidence | **Not verified.** Evidence artifacts exist in the docs tree, but this review did not inspect or reproduce embedded credentials. Proposed SQL assumes schema/identity details. | Restrict access to originals, avoid copying token material, identify the user/session through authorized operators, verify schema and deployed revision, then revoke through supported mechanisms. Redact shared evidence; history rewrite only after repository exposure/retention impact is established and an authorized owner approves. |
| Item C: staging verification | **Necessary, not completed.** Local source cannot prove deployed release/configuration. | Retain as a required verification phase tied to immutable frontend/backend release identities and migration revision. |
| Item D: distributed limiter/alerting | **Partly implemented locally; deployment/coverage uncertain.** Login/OTP fail closed in protected configuration; other controls differ by limiter. The plan's quotas and CloudWatch/Sentry details are proposals, not verified requirements. | Inventory sensitive endpoints, limiter key dimensions, storage behavior, and outage policy. Set thresholds from product/abuse requirements. Add alerting through the existing observability conventions; do not hard-code speculative alarms or send alerts to unapproved destinations. |

## Updated implementation sequence

### Phase 0 — Preserve evidence and establish the release baseline

1. Keep original tester evidence access restricted. Create redacted working copies before sharing or attaching evidence to issues.
2. For each finding, record discovery date, environment, endpoint, affected account/tenant, request/response evidence, and whether the test used a synthetic account. Do not place bearer tokens or secrets in this plan.
3. Record backend/frontend commit IDs, dirty state, deployed release/image IDs, effective environment/configuration version, and database Alembic revision. The source snapshot above is local only.
4. Have an authorized operator determine whether a captured token is still valid. Revoke via the supported session/token mechanism after confirming the user and deployed schema. Do not run hand-written SQL based solely on the proposed table/column assumptions.

**Exit:** Evidence is protected and redacted; active-credential status is resolved or explicitly open; local and deployed identities are recorded separately.

### Phase 1 — Close confirmed low-scope code gaps

1. **Login OTP resend:** add an explicit login-purpose branch with pending-challenge and account eligibility checks. Preserve generic responses and use the existing resend limiter; add cooldown and regression coverage.
2. **Proxy CSP coverage:** replace the broad dot check with a narrow static-asset exclusion consistent with the actual Next.js matcher. Ensure application paths with dots receive CSP and normal proxy logic.
3. **Redis test classification:** document the Redis integration prerequisite and make the required CI job provide disposable Redis. If local unit execution is required, isolate a mock-backed unit test from the real Redis integration test.

**Exit:** Tests cover valid/invalid login resend, abuse limits, dotted application routes, static assets, and both Redis-available/unavailable test setup outcomes.

### Phase 2 — Complete concurrency protection without weakening it

1. Inventory editable entities and every write path. Confirm which models have a persisted version field and which callers expose/pass it.
2. Keep 428 for missing preconditions during this work. Inventory first-party UI, imports, jobs, integrations, and documented API consumers to determine whether a compatibility change is actually required.
3. Implement atomic version predicates at the persistence boundary for in-scope writes. A matching version must be part of the update condition; a stale/missing version must not silently overwrite.
4. Standardize stale-write response semantics (documented 409 or 412) and make the UI explain conflict/reload behavior. Cover leads, deals, tasks, calls, meetings, and separately assess products/quotes and bulk paths.
5. If external compatibility is needed, publish a versioned or explicitly authenticated server-to-server contract with a deprecation window. Never allow an untrusted request header to disable concurrency checks.

**Exit:** Two concurrent updates prove that the stale writer is rejected; all covered API/UI/background/bulk paths have explicit behavior and regression coverage.

### Phase 3 — Validate authentication, MFA, CORS, and tenant boundaries

1. Confirm account-level MFA policy and permitted changes. Trace password, Google OAuth, account linking, recovery, and invite flows. Require a deliberate policy decision before changing behavior.
2. Verify login, OTP verification, resend, and recovery admission across multiple backend instances using disposable Redis. Exercise protected-environment Redis outage behavior and operational alerting. Avoid attacker-triggerable indefinite account lockout.
3. Audit exact credentialed CORS origins in source and effective staging responses, including preflight and errors. Retest absent, trusted, untrusted, `null`, and lookalike origins with synthetic users in a real browser.
4. Reproduce the cross-tenant claim using two authorized synthetic tenants and scoped read/write/list/export paths. Fix only confirmed authorization defects and add regression tests. UI visibility is not authorization evidence.

**Exit:** Auth/MFA/rate-limit policies are demonstrated; untrusted origins cannot read authenticated responses; negative cross-tenant tests pass for the covered endpoints. Mark untested endpoints as open.

### Phase 4 — Prioritize token exposure and CSP architecture

1. Keep the current `localStorage` token flow documented as residual risk. Inventory every access/refresh/onboarding token read/write, auth initialization, API client, Google callback, invite, and logout path.
2. Validate current enforced CSP in local and staging responses. The source already sets a nonce-based `script-src`; therefore “missing CSP” is not an accurate statement about current local source. The dot-path exclusion is a distinct confirmed gap. Review CSP compatibility on login, Google sign-in, dashboard navigation, forms, and uploads.
3. Prepare a separately reviewed BFF/session design before implementation: cookies, CSRF defense, origin checks, token refresh/rotation/revocation, logout, OAuth callback, caching, proxy trust, and gradual migration/rollback. Confirm framework-version-specific Next.js behavior before coding.
4. Treat XSS remediation and server authorization as independent controls. A BFF is not a substitute for output safety or tenant authorization.

**Exit:** CSP is observed in deployed response headers and representative flows work; BFF design has an approved compatibility and threat review before migration begins.

### Phase 5 — Verify create-abuse and idempotency controls

1. Map the specific create endpoints and reproduce the reported duplicate/rate-limit behavior with synthetic records.
2. Verify server-side permission, tenant scope, quotas, transactional duplicate/idempotency behavior, and concurrent retries. Client debounce is only a usability measure.
3. Preserve intentional duplicate creation where product rules allow it; ensure any “create anyway” action is authorized and explicitly represented server-side.

**Exit:** Same-key/same-payload retries, conflicting payloads, missing/expired keys, and concurrent submissions have documented and tested outcomes.

### Phase 6 — Release and closure evidence

1. Run the complete applicable CI checks for both CRM repositories, including migration checks against disposable PostgreSQL and the frontend browser regressions currently required by CI. Record blockers and skipped checks.
2. Deploy only commits that passed their required CI. Confirm backend migration completion before API rollout, and verify the deployed Alembic revision against image heads.
3. Retest only with authorized synthetic staging accounts/data. Record frontend/backend release identities, effective config, test evidence, and residual risks.
4. Close each audit item as `Verified fixed`, `Not reproduced with scope`, or `Open`; do not equate local implementation with deployed verification.

**Exit:** Every finding has an owner, evidence, release identity, test result, and residual-risk disposition. Deployment remains unverified until the corresponding staging checks run.

## Source references checked

- Backend concurrency: `src/modules/accounts/handlers/update_account_handler.py`, `src/modules/contacts/handlers/update_contact_handler.py`, and update handlers under `leads`, `deals`, `tasks`, `calls`, and `meetings`.
- MFA resend: `src/modules/auth/handlers/otp_handler.py`; frontend `src/app/login/page.tsx`.
- Rate limiting: `src/shared/security/rate_limiter.py`; `tests/test_auth_brute_force_mfa.py`.
- CSP middleware: frontend `src/proxy.ts`; token storage paths include `src/lib/auth.utils.ts`, `src/lib/api.ts`, auth mutations, and OAuth callback.
- Existing planning references: `CRM_SECURITY_REVISED_PHASE_PLAN.md`, `CRM_SECURITY_AUDIT.md`, and `CRM_SECURITY_IMPLEMENTATION_REPORT.md`.

This document is a verified planning update, not a claim that fixes were implemented or staging was tested. Historical audit evidence remains historical; new verification should be appended with its own date and release identity.

## Implementation progress — 2026-10-22

This section records work applied after the review above. The historical source-snapshot statement above describes the review at the time it was written; it does not describe the current dirty worktree.

### Implemented locally

- **Login OTP resend:** added an explicit login-purpose path. It requires an unexpired pending login or Google-login challenge and an active, verified, non-platform account; keeps responses generic when no eligible challenge exists; replaces only the matching challenge; and uses the resend controls. Added backend coverage for replacement, purpose isolation, generic responses, and limiter admission. The login UI now provides a resend action with a cooldown and translations in English, Dutch, and Arabic.
- **Resend admission:** retained identity-based hourly limits using a normalized, hashed identity key and added a separate per-IP hourly limit. The Redis integration test retains its existing failure behavior when `REDIS_URL` is configured but Redis is unreachable.
- **CSP proxy coverage:** replaced the broad dotted-path skip with a static-asset extension allowlist. Added checks showing that dotted application paths receive protection headers while static SVG assets remain excluded.
- **Optimistic concurrency:** added required HTTP version preconditions for update routes covering leads, deals, tasks, calls, meetings, and meeting minutes. The persistence layer checks the expected model version and maps SQLAlchemy stale-write races to a structured 409 response. Updated response schemas and first-party frontend service, mutation, and edit flows to send the version and surface missing-version/reload handling. Added stale and concurrent writer regression tests.

The optimistic concurrency request field remains optional in internal command models so non-HTTP internal callers retain their existing invocation contract. The public update routes require it and reject missing versions with 428. Products/quotes, bulk operations, imports, background writes, and external integrations were not included in the implemented scope and still need a write-path inventory before claiming complete coverage.

### Local verification

- Backend full suite: `pytest -q --basetemp=...` passed **2,277 tests; 94 skipped** in 344.75 seconds. A fresh focused auth/concurrency run passed **39 tests**. Backend `ruff check src tests scripts alembic` and `compileall` passed. The skips include environment-gated integration tests; the full CI Redis/PostgreSQL service checks did not run because Docker is unavailable in this environment.
- Frontend `npm run test`, `npm run test:reports`, `npm run test:spreadsheets`, `npm run test:native-dialogs`, `npm run test:loop-ai`, `npm run test:public -- --frontend-only`, platform contract suites, and the full CI browser matrix passed. The browser checks cover the CSP proxy, login/recovery, lead/deal/activity workflows, platform route flows, and other CI browser regressions. Two existing browser fixtures were updated to include the version field returned by the API. `npx tsc --noEmit`, `npm run lint`, `npm run format:check`, `npm run audit`, and production `npm run build` with CI's safe placeholder API/OAuth configuration passed. Lint reported 1,466 warnings and zero errors.
- Local verification used Node 24.19.0 while CI pins Node 20. `npm ci` was not run because this frontend repository has no tracked lockfile. Remote CI has not run in this pass.

### Open before release

- **Staging:** verify effective credentialed CORS/preflight/error responses, CSP on representative app routes, authentication/MFA flows, Redis behavior, and tenant isolation using authorized synthetic accounts and the exact deployed frontend/backend identities. This environment was not accessed in this pass.
- **Credential evidence:** determine through an authorized operator whether captured historical credentials remain valid and revoke through the supported session mechanism. No token material or evidence credentials were copied into this plan.
- **BFF/token storage:** localStorage token exposure remains. The BFF/session migration is still a separate architecture project requiring an approved compatibility, CSRF, OAuth, refresh/revocation, caching, and rollback design.
- **Concurrency coverage:** inventory all remaining write paths and API consumers; update coverage claims only after their version behavior is tested. Do not add a client-controlled bypass.
- **Release:** do not interpret these local checks as staging or production safety evidence. Run the required repository CI and release/migration procedure before deployment.
