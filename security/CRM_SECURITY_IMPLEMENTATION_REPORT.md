# Crusource CRM security implementation report

**Date:** 13 October 2026  
**Scope:** CRM frontend/backend only; local changes, not committed or deployed.  
**Baseline:** [Audit](CRM_SECURITY_AUDIT.md) · [Approved plan](CRM_SECURITY_IMPLEMENTATION_PLAN.md)  
**Deployment instructions:** [CRM security rollout](../../crusource-crm-backend/docs/security-rollout.md)

## Changes

| Finding | Implemented behavior | Local evidence |
| --- | --- | --- |
| CRM-SEC-001 | Exact trusted HTTPS origins in deployed environments; arbitrary credentialed origin reflection removed. Invalid environment/origin configuration fails startup. | Real application CORS preflight/GET regression with trusted, unrelated, suffix, null, wrong-port and wrong-scheme origins. |
| CRM-SEC-002 | Import SSE requires setup permission, scopes delivery per organization, revalidates account/scope during the stream, and bounds lifetimes, queues, and cross-worker connection leases. | Anonymous rejection, organization isolation, concurrent subscription limits, and real Redis cross-worker delivery. |
| CRM-SEC-003 | Shared DOMPurify HTML boundary covers campaign, AI-draft, and DOCX previews. Mentions escape text/attributes and create labels with textContent. | Browser fixtures verify malicious HTML cannot execute and legitimate formatting remains visible. |
| CRM-SEC-004 | Callback accepts an exchange code only, removes sensitive URL state, and restricts return paths to CRM dashboard/onboarding screens. | Actual callback component browser fixture rejects direct tokens/JavaScript redirects; return-path regression checks. |
| CRM-SEC-005 | Opaque short-lived server references replace credential-bearing exchange JWTs. State/exchange references are one-use and tied to an HttpOnly browser nonce; account revision/session checked before redemption. | Mocked provider roundtrip, wrong-browser/replay rejection, and concurrent Redis atomic consumption. |
| CRM-SEC-006 | Zoho state binds current permitted user, organization, browser, and account revision; callback locks/rechecks authority before storing credentials. Configured HTTPS callback and known provider origins replace hardcoded/local or arbitrary targets. | Forged organization state rejected before provider request. |
| CRM-SEC-007 | Gmail verifies Google OIDC identity/audience, sender and subscription; Calendar verifies channel token hash, resource ID and expiry. Shared receipt deduplication and bounded admission precede registered sync jobs. | Unsigned Gmail rejection; sender/subscription cases; Calendar identity, expiry and duplicate-work regressions. |
| CRM-SEC-008 | Shared IP/email/global registration quotas; existing pending-account details and OTP are preserved without repeated mail. Auth bodies capped at 16 KiB before parsing/hashing. | Pending-account regression and body boundary checks; shared Redis quota CI tests. |
| CRM-SEC-009 | General bearer query-token authorization removed. Import events use authenticated fetch streaming; document failures do not fall back to bearer URLs. | Download/recovery regressions require header authorization and reject URL tokens. |
| CRM-SEC-010 | Google/Zoho credentials encrypted at rest through one shared SQLAlchemy type and dedicated key ring. Bounded transactional migration encrypts legacy values. | Raw DB ciphertext/ORM roundtrip, tamper/key rotation checks, seeded PostgreSQL migration and rollback-boundary test. |
| CRM-SEC-011 | Patched backend runtime dependencies, replaced python-jose with PyJWT, pinned universal runtime closure, and added blocking CI runtime audit/SBOM generation. | Final runtime advisory scan: no known vulnerabilities. Frontend project audit passes with its existing temporary ESLint exception; moderate npm advisories remain. |
| CRM-SEC-012 | Password verification precedes account-state disclosure; missing/passwordless users take a dummy verification path. Shared account/IP login quotas added. | Wrong-password enumeration regression; existing login/recovery tests updated to the generic failure contract. |

Additional fixes: refresh JWTs carry a random identifier to prevent identical same-second tokens; sensitive notification/OAuth fields are audit-redacted; exception logs no longer emit raw SQL/provider credentials; deployed document storage supports IAM role credentials and fails closed instead of silently using ephemeral files. Email content blocks external tracking images until the user explicitly loads them. CSP has an enforced baseline and a broader report-only policy.

## Validation

Evidence files are under `validation/security-audit/`; disposable fixtures use no staging/customer database.

| Check | Result |
| --- | --- |
| Backend Ruff and Python compileall | Passed. |
| Backend full pytest suite | 2,061 passed, 72 skipped. Required opt-in CI suites were run separately below. One additional stream-revocation test added after collection also passed in the focused three-test stream run. Initial failures were obsolete security-contract assertions, which were updated rather than weakening the fixes. |
| Required PostgreSQL/Redis CI regressions | 111 passed, including shared quotas, webhooks, recovery locking, pipeline startup, import races, and additional security boundaries. |
| Required platform PostgreSQL CI regressions | 45 passed in the guard-required isolated `platform_phase1_test` database. |
| Empty-database migration drift, upgrade, Alembic check | Passed; no new model upgrade operations detected. |
| Seeded provider encryption migration | Passed: missing-key failure is atomic; existing Google/Zoho credentials preserved; downgrade keeps ciphertext; upgrade can be repeated. |
| Extended security boundaries | 14 passed, including real Redis atomic consumption/cross-worker streams, sender/subscription checks, Calendar identity/replay/expiry, key-ring/tamper checks, and auth body limits. |
| Frontend clean lockfile installation | Passed in isolated copy with Node 20.20.2. |
| Frontend changed-file format, full lint, type check | Passed. Lint reports existing warnings and zero errors. The format check used worktree mode; a HEAD-to-HEAD base selects unrelated parent changes in this script. |
| Frontend aggregate tests, spreadsheets, Loop/public AI contracts | Passed. Windows sandbox user-lookup failure was resolved by rerunning with approved process access. |
| Frontend required browser/contract commands | All 32 passed, including new malicious-preview and callback regressions. |
| Frontend production build | Passed with dummy API/OAuth settings, without application secrets. |
| Dependency audits | Python: all 87 locked platform entries scanned, no known vulnerabilities; an 86-component SBOM for the applicable Windows runtime was also generated. Frontend project policy passed, with the existing ESLint-only exception expiring 4 November 2026. |
| Graphify refresh | Passed: 31,167 nodes, 80,137 relationships, all five repository roots retained; no validation sources indexed. Five existing TSX files have partial AST extraction warnings, and `pyproject.toml` yielded no nodes. TypeScript checking passed; graph parser warnings are not application syntax failures. |

Backend CI is now reusable, and the staging pipeline calls it before the existing successful-pipeline deployment trigger can proceed. Both pipelines install runtime dependencies against the same lockfile used by Docker. Local workflow structure checks passed; GitHub Actions has not been run remotely for these uncommitted changes.

## Release requirements and remaining limits

**Staging is not fixed by local changes.** No deployments, real provider notifications, authenticated staging flows, AWS/Vercel secret updates, or cloud IAM checks were performed. The earlier staging observation remains the deployed evidence until a new deployment is verified.

Before release, supply the dedicated provider encryption key to migrator/API/workers, configure exact CORS origins and shared Redis, configure authenticated Gmail Pub/Sub delivery, coordinate the encryption cutover with old instances, and recreate existing Calendar channels. The rollout document includes configuration, migration order, recovery constraints, and staging acceptance checks.

The stronger CSP is report-only pending real integration compatibility checks. Frontend dependency exceptions/moderate advisories remain tracked; no blanket vulnerability-free claim is made. Existing browser-held CRM bearer storage and MFA choices are unchanged. This remediation does not constitute an exhaustive endpoint authorization review or independent penetration-test sign-off.
