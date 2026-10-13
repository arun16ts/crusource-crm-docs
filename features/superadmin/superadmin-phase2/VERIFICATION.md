# Phase 2 verification

9 October 2026. Tests use synthetic identities; credentials and activation material are excluded from artifacts.

## Completed checks

| Check | Result / scope |
|---|---|
| `npx.cmd tsc --noEmit` | Passed |
| Focused ESLint on changed/new TS, TSX and MJS | Passed with warnings; no errors |
| `npm.cmd run lint` | No errors; 1,509 repository warnings at the full-lint checkpoint |
| `npm.cmd run format:check` | Passed; all 60 changed files at checkpoint were formatted |
| `npm.cmd run test:platform:contracts` | Pagination bounds, typed/non-JSON errors, request/body timeout, CSRF fencing, headers and selective CRM-preserving cache cleanup |
| `npm.cmd run test:platform-auth:browser` | StrictMode, server page two/history, owner gating, same-key/body retry after lost response, conflict review, cancel/reset/revoke, cross-tab logout, login/MFA/resume and outage recovery; known configuration failures remain editable/dismissible |
| `npm.cmd run test:platform:routes:browser` | Real Next.js/API invite/resend/activate/MFA/resume/reset/re-enroll/revoke/cancel; actual existing platform routes/details; owner-only access; full and short path aliases; real font/CSS and responsive captures |
| `npm.cmd run test:platform:crm-frame:browser` | Five before/after CRM presentation captures were pixel-identical: 1440 expanded/collapsed, 1024, 768 and 390px |
| `npm.cmd run test:session-startup:browser` | Passed |
| `npm.cmd run test:localization` | Passed, including shared date/number/currency and activity/audit/campaign checks |
| `npm.cmd run test:translations` | Passed: 2,371 keys and 1,593 source references at verification checkpoint |
| `npm.cmd run test:invitations` | Passed |
| `npm.cmd run test:public:analytics` | Passed; platform host exclusion is included |
| `npm.cmd run build` | Production compilation, TypeScript and route generation passed |
| Targeted backend auth/invitation/compatibility/guard tests | **44 passed**, four dependency deprecation warnings |

**Existing test limitation:** `npm.cmd run test:translations:browser` fails at the landing-page language control: its `a[href="/"][title]` selector no longer matches the existing dropdown. A temporary selector adaptation also hit a landing navigation/hydration wait, so it was reverted; this phase leaves that unrelated test source unchanged. A further attempt against the normal dev origin encountered port 3000 unavailable. This check is not reported as passing. Platform English/Dutch rendering and the Dutch invitation dialog passed in the actual-route suite, and translation/localization contract checks passed. No new landing-page application change is part of this phase.

## Reproduce safely

From `crusource-crm-frontend/`, with installed dependencies, backend venv and a locally installed Edge/Chrome browser:

```powershell
npm.cmd run test:platform:contracts
npm.cmd run test:platform-auth:browser
npm.cmd run test:platform:routes:browser
npm.cmd run test:platform:crm-frame:browser
npm.cmd run format:check
npx.cmd tsc --noEmit
npm.cmd run build
```

The actual-route runner requires free ports 3107 and 3108, starts its own hidden child processes and terminates only those processes on completion. It uses `superadmin.localhost:3107` for platform cookies and aliases, and `.next-phase2/` for separate Next output. Normal application credentials/database/providers are not used. The CRM presentation comparison uses the baseline `DashboardShell` from frontend Git HEAD, deterministic CRM domain effects and the loaded Instrument Sans font; it does not claim live CRM backend integration.

From `crusource-crm-backend/`:

```powershell
$env:DATABASE_URL='postgresql://synthetic:synthetic@127.0.0.1:9/synthetic'
$env:REDIS_URL='redis://127.0.0.1:9/0'
$env:ENVIRONMENT='test'
$env:AWS_EC2_METADATA_DISABLED='true'
.\.venv\Scripts\python.exe -m pytest tests/test_platform_invitations.py tests/test_platform_auth.py tests/test_platform_crm_identity_compatibility.py tests/test_superadmin_guard.py -q
```

Tests include missing/invalid delivery keys and invalid activation URLs, asserting 503 `delivery_not_configured` with no invitation, delivery or command receipt persisted. Phase 1 retains separate PostgreSQL migration/race and dispatcher failure/lease/key-rotation evidence; this phase did not rerun the entire backend suite.

## Evidence and limits

- [Route metrics](route-verification.json): real API, zero CRM API requests from the platform contexts, no page errors, no document overflow at 1440/1024/768/390px; 236/64px sidebar and 64px header.
- [CRM comparison metrics](crm-frame-verification.json): all five captures identical. [Image index](SCREENSHOTS.md) includes Dutch, mobile navigation, collapsed sidebar and CSS 200% zoom captures.
- Dialog/browser checks cover Base UI interactions, Escape, pending/error controls and keyboard-accessible sorting/scroll regions. This is not an exhaustive assistive-technology audit or an OS-level zoom certification.
- Development SES sender/sending/quota/production-access checks are read-only. The user's retry subsequently produced a **sent** delivery and an **enrolling** invitation, verified through aggregate read-only queries. No real email was initiated by the agent. Completed recipient MFA, mailbox placement, staging TLS cookie/origin deployment and production rollout remain unverified.
- Existing content styling and workflows remain Phase 3; new demo/support/observability features are not claimed complete.
