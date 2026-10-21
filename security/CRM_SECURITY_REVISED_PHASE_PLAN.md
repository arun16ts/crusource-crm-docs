# CRM Security Remediation: Revised Phase Plan

**Prepared:** 2026-10-21  
**Scope:** Crusource CRM only: `crusource-crm-frontend/` and `crusource-crm-backend/`  
**Status:** Implementation handoff for Antigravity; planning document, not proof of remediation or deployment.

## Purpose and operating rules

Use this plan to verify and close the security tester's reported findings against the current source, then validate the exact release in staging. Several controls exist in the local CRM source, but that does not establish that staging has those changes, migrations, configuration, or account settings. Begin each phase by recording the frontend and backend commit SHAs, deployment/image identity, environment, and test account/tenant. Do not label a finding remediated until its acceptance checks pass on the intended environment.

Work only in the CRM repositories. Do not copy secrets, bearer tokens, personal data, or unrestricted evidence into this plan, tickets, screenshots, or logs. Use authorized test accounts and synthetic records. Do not run load or brute-force tests against production or shared staging without an explicitly approved, bounded test window.

Treat the tester's dated evidence as evidence of behavior at the time it was collected, not as proof of current behavior. The CORS capture includes a bearer token and record details: restrict the original, revoke/rotate the exposed credential if it may still be valid, redact any shareable copy, and follow the repository's secret-exposure procedure if it was committed. The local evidence copies are under `Cyber-security/`; the externally linked Drive and Google Chat materials were not independently accessible during this review. Request accessible reproductions for any claims that depend on those materials.

## Phase 0 — Contain evidence exposure and establish a baseline

**Priority:** Immediate, before sharing evidence or testing credentials.

1. Restrict access to the unredacted CORS screenshot and preserve it only in the approved evidence location. Create a separately redacted copy for collaboration; do not embed the original in this plan.
2. Identify the account/token represented in that capture through the authorized owner. Revoke active sessions or rotate credentials as appropriate; do not assume an old token is still valid or harmless.
3. Check whether the screenshot or token entered Git history, tickets, chat, CI logs, or other shared storage. If so, use the organization's secret-exposure response process, including history cleanup only under repository-owner coordination.
4. Inventory evidence by finding and date. Record which source files are available locally and which Drive/Chat artifacts still need the tester to provide.
5. Record clean/dirty state, branch, commit SHA, deployed image/release identity, environment configuration version, and current migration revision for both CRM applications. Preserve pre-existing work.

**Exit checks:** Evidence access is restricted and shared copies are redacted; exposed credentials have been addressed or explicitly confirmed expired/revoked; baseline identities and evidence gaps are recorded.

## Phase 1 — Reproduce and close credential-stuffing risk

**Priority:** P0 until staging confirms the controls.

### Source review and implementation

- Verify login admission limits by both source IP and normalized account identifier, with a shared store across API instances. Use generic authentication errors so account existence is not disclosed.
- Ensure protected environments fail closed when the shared limiter is unavailable; alert on limiter/store failures. Confirm local-development behavior cannot be mistaken for the protected-environment policy.
- Set a clear account-wide MFA policy. The current source issues a token without an OTP challenge when `mfa_enabled` is false and allows a user to change that preference. Confirm whether this is intentional policy; for accounts requiring MFA, prevent self-service disablement from silently weakening the next login. Require reauthentication and an approved recovery/admin flow for policy changes.
- Apply equivalent MFA requirements to password and Google OAuth login, including account linking and recovery paths. Verify that OAuth cannot bypass an account's required second factor.
- Ensure OTP verification has shared, bounded per-account and per-IP admission, expiry, one-time use, replay rejection, and fail-closed behavior in protected environments. A per-email OTP limiter that falls back to a process-local limiter during Redis failure is not sufficient for a multi-instance deployment.
- Keep lockout behavior resistant to denial-of-service against a victim. Prefer progressive throttling and carefully designed recovery over indefinite attacker-triggerable lockout.

### Verification

- In isolated automated tests, exercise just-under/at/over thresholds across multiple backend instances and verify correct `429`/retry behavior without revealing whether an account exists.
- Simulate shared-store failure in protected configuration and verify login/OTP admission fails closed and produces a safe operational alert.
- Test MFA enabled/disabled policy transitions, OTP expiry, replay, wrong codes, recovery, password login, Google login, and account linking.
- In an approved staging window, use dedicated synthetic accounts and low-volume bounded attempts. Verify the effective deployed configuration and responses; stop at the agreed limit.

**Exit checks:** Required MFA policy is enforced across supported login paths; shared rate limits and outage behavior are demonstrated; tests and staging evidence are tied to the recorded release identity.

## Phase 2 — Restrict credentialed CORS and validate browser exposure

**Priority:** P0 until staging retest.

1. In protected environments, allow only exact, documented CRM frontend origins. Do not reflect arbitrary `Origin` values or use broad origin regular expressions with credentialed access.
2. Keep `Access-Control-Allow-Credentials: true` only where required and only with exact trusted origins. Review allowed methods/headers and preflight behavior. Confirm error responses and all relevant API routes use the same policy, including proxies/CDN/ingress layers.
3. Test absent, trusted, attacker-controlled, `null`, malformed, and lookalike origins. Verify attacker-controlled origins receive no permissive allow-origin response and that trusted frontend flows still work.
4. Separate what the evidence proves from the impact hypothesis: the Oct 11 capture shows an arbitrary origin reflected with credentials allowed and a manually supplied bearer token. Since the CRM stores bearer tokens in browser `localStorage`, establish independently whether any cookie or other ambient credential path allows cross-origin authenticated requests; do not claim the screenshot alone proves an attacker can read localStorage.
5. Check browser behavior with a dedicated synthetic user and verify no sensitive response is readable from an untrusted origin. Do not use the token from the tester's capture.

**Exit checks:** Deployed response headers match the allowlist for success, error, and preflight requests; trusted CRM origins work; untrusted origins cannot read authenticated responses in a real browser test.

## Phase 3 — Verify tenant authorization and reduce token exposure

**Priority:** P0 for any confirmed cross-account access; otherwise high priority hardening.

### Prove or disprove the cross-account claim

- Obtain the tester's full written reproduction and clarify the two account identities, endpoint, token provenance, and whether the accounts belong to different organizations. The local XSS videos and external links were not fully reviewed in this pass.
- Create two authorized synthetic users in separate organizations. With account A's token, attempt read and write operations against account B's records and organization-scoped endpoints, including representative list, detail, update, delete, export, and administrative routes.
- Verify server-side organization/record ownership and permissions on every operation. Do not rely on hidden UI controls or client-provided tenant IDs. Review JWT signature, token type, user/organization claims, credential revision, and the endpoint's scoped lookup together.
- Record redacted requests and responses and add regression tests for every confirmed bypass. If a cross-account operation succeeds, stop broader staging testing, preserve minimal evidence, and prioritize a targeted fix.

### Reduce browser token theft impact

- Current frontend source stores access/refresh tokens in `localStorage`; XSS can read these values. Assess a same-origin backend-for-frontend (BFF) with `HttpOnly`, `Secure`, appropriately `SameSite` cookies as a planned architectural migration, not a substitute for authorization fixes.
- If adopting a BFF, design CSRF protection, origin checks, session rotation/revocation, refresh handling, logout, OAuth callbacks, and compatibility rollout. HttpOnly storage limits direct token extraction but does not prevent injected same-origin JavaScript from issuing requests as the user.
- Before migration, reduce XSS likelihood and token lifetime where feasible, avoid logging tokens, and ensure refresh/revocation behavior is tested. Do not claim localStorage removal fixes a BOLA/authorization flaw.

**Exit checks:** Cross-tenant negative tests pass for read and write paths, with regression coverage; any confirmed authorization issue is fixed and independently retested. Token-storage migration has a reviewed compatibility and CSRF design before implementation.

## Phase 4 — Enforce a practical Content Security Policy

**Priority:** High; coordinate with frontend deployment and Google sign-in.

1. Review current `next.config.ts`: a minimal enforced policy is present while a broader report-only policy includes `script-src 'unsafe-inline'`. The historical scanner finding “no CSP” is not an accurate description of this local source state; verify actual staging headers.
2. Collect report-only violations on representative CRM flows, classify required Next.js and Google sign-in resources, and remove unnecessary sources.
3. Move to a nonce- or hash-based script policy compatible with the deployed Next.js rendering strategy. Do not promote a broad `unsafe-inline` script policy as the final fix. Keep `object-src 'none'`, a restrictive `base-uri`, and appropriate framing protections; review `connect-src`, `img-src`, `style-src`, and worker needs.
4. Validate the final policy on sign-in, authenticated navigation, forms, uploads, and error states. Watch CSP reports for regressions during staged rollout.

**Exit checks:** Enforced staging CSP is verified from response headers, representative flows work without broad script `unsafe-inline`, and observed violations are triaged.

## Phase 5 — Bound create abuse and make retries safe

**Priority:** High for abuse controls and data integrity.

- Verify authenticated admission quotas are enforced in the deployed shared store, including per-user and organization-level limits, and that protected environments fail safely on store failure.
- Exercise duplicate detection, idempotency receipts, and database concurrency in the create-submission path. Same-request retries should not create duplicate records; distinct intentional requests should follow documented product behavior.
- Review the UI's “Proceed & Create Anyway” path. Confirm it represents an explicit, authorized business action and cannot bypass server-side permission, quota, or duplicate rules accidentally.
- Test same idempotency key/same payload, same key/different payload, missing key, expired key, and concurrent requests. Test against isolated fixtures; do not replay mass-create requests against shared staging or customer data.
- Treat client-side debounce as usability only; server-side limits and transactional duplicate protection are the security controls.

**Exit checks:** Server-side quotas and idempotency behavior are demonstrated under concurrency; expected duplicate/intentional-create behavior is documented and covered by regression tests.

## Phase 6 — Prevent silent concurrent-edit data loss

**Priority:** High for data integrity.

1. Inventory all editable CRM records and write paths. Current source uses integer versioning through `RecordContextMixin` for some records, while Contact and Account use a different mixin without that version field; confirm actual model and bulk-update coverage.
2. Apply atomic optimistic concurrency consistently to affected entities and write paths. Use version columns or ETag/`If-Match` semantics that detect stale writes at the database boundary.
3. Translate stale writes into a clear `409 Conflict` (or consistently documented equivalent). The UI should explain that the record changed and offer reload/compare/merge. Do not silently overwrite or add a “force overwrite anyway” path as the default resolution.
4. Cover API updates, bulk edits, imports, background jobs, and any repository method that can bypass normal handlers.

**Exit checks:** Two-editor tests prove a stale update is rejected without losing the first user's changes; conflict handling is usable and all relevant write paths enforce the version check.

## Phase 7 — Release, staging retest, and evidence closure

**Priority:** Required before marking any item fixed.

- Read both CRM CI workflows and run the complete applicable frontend/backend checks in their owning repositories. Include the backend PostgreSQL migration, migration drift, and opt-in regression checks required by CI; use disposable services only. Record skipped checks and environment blockers rather than treating them as passes.
- Review frontend/backend deployment workflows and migration ordering. Deploy only the exact commits that passed required CI; migrations must complete successfully before API rollout. Confirm image SHA, frontend deployment commit, configuration version, and Alembic revision.
- Retest Phases 1–6 in staging with synthetic accounts/data and the approved test window. Verify login/MFA, CORS in a browser, cross-tenant authorization, CSP, create idempotency/rate limits, and concurrent edits.
- Review Vercel/AWS logs for limiter/Redis failures, auth errors, migration issues, CSP violations, and relevant API failures. Never include credential values in the evidence.
- Produce a closure table with finding, original evidence date, source change/commit, tests, deployed identity, staging result, residual risk, owner, and date. Keep historical reports intact; append new evidence rather than rewriting what the tester observed at the time.

**Exit checks:** Every finding is marked `Verified fixed`, `Not reproduced with scope`, or `Open`, with evidence and release identity. “Locally implemented” and “deployed and verified” remain separate statuses.

## Evidence and source references

- [Security audit baseline](CRM_SECURITY_AUDIT.md) — historical findings; confirm present behavior in source.
- [Security implementation plan](CRM_SECURITY_IMPLEMENTATION_PLAN.md) — earlier local repair sequence.
- [Security implementation report](CRM_SECURITY_IMPLEMENTATION_REPORT.md) — local implementation evidence and known staging limitations at its writing date.
- [Backend security rollout instructions](../../crusource-crm-backend/docs/security-rollout.md) — deployment-specific controls and verification.
- Tester evidence copies: `../Cyber-security/`. Handle restricted originals and redact before sharing.
- Application source of truth: `../../crusource-crm-backend/` and `../../crusource-crm-frontend/`.

This plan revises the implementation sequence and acceptance criteria for handoff. It does not replace source review, CI, deployment controls, or staging verification, and it does not assert that the reported vulnerabilities are currently present or remediated in staging.
