# Crusource CRM security implementation plan

**Date:** 13 October 2026  
**Status:** Approved for local implementation; progress and evidence in the [implementation report](CRM_SECURITY_IMPLEMENTATION_REPORT.md). No application changes deployed.  
**Evidence and finding IDs:** [Security audit](CRM_SECURITY_AUDIT.md)

## Delivery order

Repair the exposed trust boundaries first. Keep each change reviewable, with a behavioral regression that demonstrates the current defect before the repair. Use disposable local fixtures; do not attack, seed, or alter staging customer data to validate fixes.

| Batch                                      | Findings      | Deliverable                                                     | Primary owner                         |
| ------------------------------------------ | ------------- | --------------------------------------------------------------- | ------------------------------------- |
| P0 — first                                 | 001           | Exact staging/production CORS allowlist                         | Backend + deployment configuration    |
| P0 — first                                 | 002           | Authenticated, tenant-scoped and bounded import stream          | Backend + frontend                    |
| P0 — first                                 | 003, 004      | Safe HTML previews and auth-callback navigation                 | Frontend + backend content validation |
| P0 — first, independent compatibility work | 011           | Patched compatible Python runtime and dependency gate           | Backend/platform engineering          |
| P1 — next                                  | 005, 006, 009 | Opaque OAuth codes/state and removal of normal tokens from URLs | Backend + frontend                    |
| P1 — next                                  | 007, 008, 012 | Verified Google callbacks; registration/login abuse controls    | Backend + provider configuration      |
| P2 — follow-up                             | 010           | Encrypted recoverable integration credentials                   | Backend + cloud key management        |
| Follow-up verification                     | All           | Authenticated staging regressions and AWS/edge evidence         | QA/security + deployment owner        |

Containment is separate from a verified repair. If a safe temporary restriction is needed before a batch can ship, prepare an exact route/origin rule and its compatibility impact for deployment review. Do not deploy a permissive regex as a rollback. No production action is authorized or performed by this plan.

## 1. CORS and startup configuration — CRM-SEC-001

**Implementation**

- Move origin parsing/validation to a narrow shared configuration helper; `main.py` only wires middleware.
- Staging/production: trusted canonical origins from explicit configuration, without an origin regex. Accept only complete origin values, with no credentials, paths, query strings, wildcards, or `null`; require HTTPS where appropriate. Reject absent/invalid protected-environment configuration instead of silently trusting localhost.
- Keep development localhost/tunnel behavior explicitly development-only. Validate environment names to avoid accidentally enabling development defaults in a deployed task.
- Determine the exact CRM and Superadmin frontend origins from deployed configuration. Add each explicitly rather than accepting any `superadmin.*` host.
- Preserve credentials support for legitimate paths until the cookie/public-visitor flows have been tested. Changing CORS is not a substitute for authorization or platform origin/CSRF guards.

**Regression first**

Test trusted/untrusted preflight and actual success/error responses, no-Origin server-to-server calls, `null`, HTTP versus HTTPS, wrong port, arbitrary subdomains, suffix lookalikes, and invalid startup configuration. Exercise CRM sign-in/refresh, Superadmin authentication, and public sharing.

**Done**

Repeat the original staging headers probe against the exact deployed commit: untrusted origins receive no `Access-Control-Allow-Origin`, trusted frontends continue working, and existing auth guards remain intact. Get an authorized authenticated test account to assess the tester's full data-read claim.

**Rollback**

Correct a missing legitimate exact origin without reintroducing global trust. Record approved origins as configuration, never include credential values in review artifacts.

## 2. Import-event privacy and reliability — CRM-SEC-002

**Implementation**

- Authorize `data-import/events` with current user scope and the setup `data_import` permission before opening the stream.
- Add organization/job/user scope to the event contract and publishing service. The server chooses scope from the job; a client-supplied organization ID must never grant access.
- Partition subscribers and enforce the current user's permitted job scope. Recheck account/permission revocation during long-lived streams, including on heartbeat/events.
- Replace native EventSource with authenticated fetch streaming through the existing API/auth service layer; remove the URL bearer token. Keep stream lifecycle in a focused hook and TanStack invalidation in its existing owner.
- Bound connections, per-user/per-organization subscriptions, queues, and idle duration. Disconnect or coalesce slow consumers rather than accumulating unbounded messages.
- If jobs/API run in separate processes, use the existing shared queue/Redis architecture to deliver scoped events across workers. Do not present a process-local publisher as a multi-worker solution.

**Regression first**

Anonymous rejection; organization A cannot observe B; a user without import permission cannot subscribe; same-tenant permitted completion still invalidates the appropriate queries. Test disconnect cleanup, slow consumers, authorization revocation, and separate-worker delivery.

**Done**

Staging anonymous subscription is rejected; isolated organization fixtures prove event segregation. Event payloads expose only needed metadata and no credential-bearing URLs appear in browser/network logs.

## 3. HTML and callback safety — CRM-SEC-003/004

**Implementation**

- Introduce a maintained shared HTML sanitization boundary for campaign, AI-draft, and DOCX preview output. Inventory every `dangerouslySetInnerHTML`, `innerHTML`, and generated-HTML URL, rather than fixing only one component.
- Explicitly allow supported formatting while blocking executable attributes/elements and unsafe URL protocols. Keep backend validation for persisted HTML separate from browser rendering protection.
- Treat generated AI HTML and document conversion output as untrusted. For previews that need greater isolation, use a sandboxed document frame without script capability; preserve accessible scrolling/zoom/links.
- Add a focused return-path validator used by callback and OAuth initiation. Allow approved same-origin relative destinations only; reject schemes, `//`, backslashes, control characters, and normalization/encoding bypasses.
- Remove legacy direct access/refresh/onboarding token parameters from the callback. Only a successful exchange can establish a CRM session. Remove sensitive callback parameters from history promptly.
- Introduce CSP carefully: inventory existing scripts/frames, test a report-only policy, then enforce. Avoid breaking auth, document previews, or calendar integration. CSP complements sanitization, not replaces it.

**Regression first**

Use harmless marker payloads against actual components/routes with fake data: HTML event handlers, SVG, JavaScript links in DOCX, nested/encoded unsafe URLs, and normal formatted emails. Test callback navigation with malicious destinations and invalid legacy token parameters; verify legitimate onboarding/dashboard returns. No real token exfiltration is needed.

**Done**

The fixtures that currently execute benign markers no longer execute them in application previews/callbacks. Normal rich formatting, preview interactions, and login behavior remain functional. Confirm with an isolated staging organization once deployment is authorized.

## 4. Dependency upgrades and sustainable audit gates — CRM-SEC-011

**Implementation**

- Generate separate SBOMs for the exact frontend deployment and backend runtime image. The local venv is only a diagnostic snapshot.
- Resolve a compatible updated FastAPI/Starlette/python-multipart set, using current upstream advisories. FastAPI 0.111.1 constrains Starlette; do not override that constraint to force an unsupported installation.
- Upgrade affected runtime packages and Requests' manifest pin. Triage ecdsa/python-jose by actual HS256/crypto paths, dotenv by environment-loading use, urllib3 by outbound usage, and Starlette/parser findings by reachable request paths.
- Assess the KEV-listed Starlette Host/path issue against actual Vercel/load-balancer/direct API ingress behavior. Use dependency upgrades and validated host handling; do not assume the proxy neutralizes it without evidence.
- Add a reproducible Python dependency lock/constraints workflow and a backend vulnerability CI gate. Keep runtime and test dependencies distinguishable, and record approved time-limited exceptions with owner, reason, affected path, and expiry.
- Update frontend chains where compatible patches exist. Track the existing ESLint-only braces exception before 4 November 2026 and review moderate Mammoth-related dependencies rather than calling a high-only gate a clean full scan.
- Enrich advisories with aliases, severity, EPSS, and KEV. Deduplicate scanner records before reporting. Repeat against current advisories during implementation; today's snapshot is not a future guarantee.

**Regression first**

Pin current behavior with login/form/upload/document and middleware regressions. Upgrade in an isolated environment, then run all backend CI/migration checks; browser HTML tests and document parsing should also run on the updated frontend dependencies. Do not run resource-exhaustion payloads against shared staging.

**Done**

Both deployment SBOMs are accounted for, reachable high-risk advisories are remediated, remaining exceptions have verified preconditions and expiry, and the actual workflow audit gates pass honestly.

## 5. OAuth codes, Zoho state, and download tokens — CRM-SEC-005/006/009

**Implementation**

- Replace Google exchange JWTs containing credentials with cryptographically random opaque codes. Store a hash with the session/account reference, expiry, purpose, and consumed status; consume atomically and verify the account's current credential revision.
- Bind OAuth initiation and return state to the initiating browser/user, provider, organization, permission, and expiry. Use a server-side one-time nonce rather than treating an organization UUID as proof of intent.
- Require integration-management permission at Zoho initiation and verify state before provider calls or credential writes. Revalidate membership/permission after callback where applicable; never derive the tenant directly from an unchecked query parameter.
- Use environment-specific configured callback URLs. Put client secrets/provider token fields in supported POST bodies, not request URLs; redact errors/logs.
- Migrate download/navigation clients to authenticated fetch or narrowly scoped, expiring resource tickets. Remove the global normal-access-token query fallback after affected clients are updated.
- Coordinate frontend/backend contracts. The existing frontend exchanges a `code` for a token response, so an opaque-code backend can preserve that contract. Do not maintain a permanent fallback accepting credential-bearing legacy codes.

**Regression first**

Parallel/replayed/expired exchange, user revocation between code creation and redemption, wrong provider/tenant/browser state, permissions revoked during OAuth, callback retry, and successful normal linking. For downloads, unauthorized callers fail and a scoped ticket cannot become a general API token.

**Done**

URL contents cannot reveal full API credentials; second redemption fails; forged state causes no provider call/tenant write; all ordinary API authentication is carried in supported headers/session mechanisms.

**Migration/recovery**

Keep changes additive where possible, test PostgreSQL locking, and deploy migrations before dependent code. Old unredeemed callback codes can expire or be invalidated with an explicit sign-in retry. If incident evidence shows actual leaked refresh credentials, prepare targeted revocation separately; broad unplanned session invalidation is not part of this review.

## 6. Google callbacks and authentication abuse — CRM-SEC-007/008/012

**Implementation**

- Configure Gmail Pub/Sub authenticated push and validate JWT issuer, audience, service-account identity, expiry, and allowed subscription context before decoding trusted event fields.
- For Calendar watches, create/store a per-channel secret and verify channel token, resource ID, expiration, and expected state. Google Calendar push is not the same authentication scheme as Pub/Sub; use provider-specific verification.
- Bound callback payload size, deduplicate notification IDs, throttle admission, and enqueue synchronization using existing worker services. Return minimal errors with request IDs; never return raw provider/database exceptions.
- Share verification infrastructure where appropriate, following the already bounded/authenticated SES receiver design; do not treat a sender-provided email/header as identity.
- Add shared registration IP/email limits, OTP cooldown, and global email quota before Argon2/database/email work. Prevent the register endpoint from bypassing resend limits or repeatedly replacing pending credentials/OTPs.
- Normalize authentication failures externally and expose account status only after correct credentials. Add account plus IP admission controls and conservative retry/cooldown behavior without enabling account-lockout abuse.

**Regression first**

Forged/missing/wrong-audience notification, wrong Calendar secret/resource, replay, oversized body, disabled user, Redis outage, and valid provider notification. Use fake transport: rejected inputs must not call Google or send email. Test repeated register/resend combinations and unknown/unverified/deactivated accounts with incorrect passwords returning indistinguishable outward failures.

**Done**

Provider callbacks only schedule work after verification, public authentication flows have tested shared abuse controls, and intended Google integration/login/recovery flows still work.

## 7. Provider credential encryption — CRM-SEC-010

**Implementation**

- Centralize provider credential storage behind a narrow repository/service boundary. Encrypt recoverable values with authenticated encryption and a versioned key reference; use separate managed key material and least-privilege decrypt access.
- Inventory Google/Zoho refresh/access tokens and any other provider credentials before migrating. Hashing is appropriate for opaque session identifiers, but not for provider tokens that must be sent back to the provider.
- Stage the database change and backfill with dry-run counts, error recovery, and verification. Retain encrypted backups and restrict old plaintext backup access; encrypting current rows does not repair old backups automatically.
- Plan key rotation and provider-token revocation without printing values. Update integration services to decrypt only when required.

**Regression first**

Encryption/decryption, tamper rejection, key version migration, missing key fail-closed behavior, provider calls, interrupted backfill, and backup/restore compatibility.

**Done**

New and migrated rows are encrypted, integration behavior is retained, and database/backup access alone does not disclose usable provider tokens without separate key access.

## 8. Operational and UI follow-ups

- Verify document storage in an IAM-role-only task; use explicitly selected S3/local storage and boto3's credential chain. Fail clearly on unavailable storage instead of switching silently to ephemeral disk.
- Reject unknown environment names at deployment/startup.
- Offer remote-image controls for inbound email; retain the existing script-disabled sandbox.
- Replace clickable email divs with keyboard-operable controls and report real download failures rather than premature success.
- Keep query state and invalidation in TanStack/focused hooks; avoid a second Redux/server-data source while changing streaming or preview behavior.

## Review gates, validation, and release

Authentication/authorization, encryption, tenant-stream scope, and OAuth changes need a reviewer with the relevant security/domain ownership. CORS configuration changes need the deployment owner to verify exact origins and affected frontends. Dependency major upgrades need compatibility review. The skill package's referenced shared fixer-policy document is missing; resolve that policy reference before implementation review rather than inventing an approval rule.

For every batch:

1. Read current owning-repository instructions/workflows and preserve unrelated changes. Write the behavioral regression first when practical; confirm failure for the expected defect.
2. Keep routes thin, reads in query handlers, mutations in command handlers, persistence in repositories, and reusable security/configuration in shared services. Reuse existing Scope, permissions, record access, API clients, and queue design.
3. Run focused regressions while iterating, then complete applicable CI parity for each changed repository. Backend: Ruff, compileall, full tests, disposable PostgreSQL migrations/drift/locking, required Redis/PostgreSQL regressions, and Alembic check. Frontend: clean locked install, formatting, full lint/tests/spreadsheets/types, every current CI browser command, safe build, and audit.
4. Run Graphify update after code changes. Documentation-only audit/planning does not need an application graph rebuild.
5. Before any requested promotion, perform the complete CRM deployment audit: successful CI/exact image commit, migration completion before API rollout, configuration compatibility, Vercel/backend alignment, and credentials-safe logs.
6. Verify the deployed staging flow with authorized isolated fixtures and capture redacted evidence. Source or local fixture success alone is not a staging pass.

### Remaining evidence needed

Deployed frontend/backend commit and image SBOM; an authorized staging test account and two isolated organizations; exact CRM/platform origins; Google/Zoho callback settings; proxy/edge header handling; AWS IAM/S3/RDS/network/logging/WAF configuration exports. CIS AWS identity, storage, logging, monitoring, and networking remain unverified until that evidence is available. Missing evidence does not mean those controls failed.

### Final completion criteria

- The original arbitrary-origin staging test fails safely while legitimate origins work.
- Anonymous/wrong-tenant event access fails, with bounded revocation-aware streaming.
- Actual preview and callback regressions reject active content/unsafe navigation.
- No ordinary API credentials appear in generated URLs or opaque exchange codes.
- Wrong-tenant/provider state and forged notifications cause no side effects.
- Public registration/login abuse controls are tested across workers/outages.
- Deployed dependency exposure is remediated or explicitly triaged with expiring exceptions.
- Provider credential migration and operational storage behavior are verified.
- Full affected CI and authenticated staging evidence are recorded, with unresolved cloud/deployment checks clearly identified.
