# AI Codebase Audit Report — Crusource CRM

**Audit Type:** Read-only forensic review (no code modified)
**Audited:** `crusource-crm-backend` (Python / FastAPI / SQLAlchemy / PostgreSQL), `crusource-crm-frontend` (Next.js / TypeScript / Redux / TanStack Query)
**Audit Date:** 2026-09-08
**Method:** Manual file-by-file inspection of high-traffic and security-sensitive modules, cross-referenced across layers (routes → handlers → repositories → shared infrastructure).

---

## 1. Executive Summary

Crusource CRM is a multi-tenant AI CRM with a well-structured CQRS backend (FastAPI + SQLAlchemy) and a modern Next.js frontend. The overall architecture is sound: routing, command/query handlers, repositories, and shared infrastructure (auth, DB, storage) are cleanly separated. Authentication uses Argon2 password hashing and signed JWTs; RBAC is enforced server-side on most module routes.

However, the audit identified **1 critical, 4 high, and several medium/low** findings. The most urgent issues are **error-message information leakage** (full DB errors returned to the client), **unrestricted arbitrary file uploads**, and **several authenticated endpoints lacking authorization scoping**. Several rate limits are in-memory only (not distributed), and a few model/route shortcuts (missing permission guards, silent exception swallowing, duplicate imports) reduce robustness.

No severity-0 findings (RCE, exposure of production secrets in tracked code) were confirmed. The real credentials found in `.env` / `.env.local` are **not tracked by git** and are correctly git-ignored.

---

## 2. Scope & Methodology

- **In scope:** All `src/modules/*` routes/handlers/repositories for auth, user, leads, contacts, deals, tasks, notes, attachments, documents, notifications, dashboard, calls, meetings, saved_views, reports, analytics_boards, org_settings, organization, profiles, admin, campaigns, onboarding, approvals, audit_logs, billing, data_admin, template_studio, forecast, teams, search, skills, teamspace, inbox, integrations; `src/shared/*` (auth, database, security, services, handlers, exceptions); `src/main.py`; `src/worker.py`.
- **In scope (frontend):** `src/lib/*` (auth, api, httpClient), `src/services/*`, `src/hooks/usePermissions.ts`, `src/hooks/usePermissions.ts`, `src/store/*`, key `src/components/shared/*` (PermissionGuard).
- **Out of scope:** Third-party vendored code, infrastructure/deployment configs beyond env templates, migrations, tests (none found centralized).

### Validation approach
Each finding was traced across at least two files (e.g., route → handler → repository, or guard → schema) before being recorded, and re-checked in a second pass before final classification.

### Confidence levels
- **CONFIRMED** — directly observed in source with clear path.
- **LIKELY** — strong evidence but requires runtime or cross-env confirmation.
- **NEEDS REVIEW** — pattern suggests risk; requires product/design confirmation to classify as a defect.

---

## 3. Severity Classification

| Severity | Meaning |
|---|---|
| **CRITICAL** | Exploitable remotely, data loss / full compromise, or severe information disclosure without authentication. |
| **HIGH** | Significant security/robustness risk requiring immediate attention (auth bypass, arbitrary upload, data exposure). |
| **MEDIUM** | Data-integrity, scaling, or moderate security concern. |
| **LOW** | Code quality, maintainability, dead code. |
| **INFO** | Positive / informational / non-issue confirmation. |

---

## 4. Findings

### CRITICAL

#### C1. Database exception detail leaked to clients
- **File:** `crusource-crm-backend/src/shared/exceptions/global_handlers.py:21-24`
- **Severity:** CRITICAL
- **Confidence:** CONFIRMED
- **Description:**
  ```python
  return JSONResponse(
      status_code=500,
      content={"message": f"Database error: {str(exc)}"},
  )
  ```
  The global `SQLAlchemyError` handler returns the raw exception string (`str(exc)`) — including the underlying DB driver message — directly in the HTTP response body. This leaks SQL dialect details, table/column names, connection strings fragments, and potentially stack information to any client that triggers a DB error.
- **Impact:** Information disclosure; aids attacker in enumerating schema and adapting SQL-injection or other attacks. Also inconsistent with the sibling `global_exception_handler`, which correctly returns a generic message.
- **Recommendation:** Return a generic message (`"An unexpected server error occurred."`) and log the detail server-side only.

---

### HIGH

#### H1. Arbitrary file upload on documents (no MIME/extension validation)
- **File:** `crusource-crm-backend/src/modules/documents/handlers/upload_document_handler.py:39-48`
- **Severity:** HIGH
- **Confidence:** CONFIRMED
- **Description:** The document upload handler enforces only a 10MB size limit. It does **not** validate file extension or content MIME type. The file is stored via `document_storage_service.save_bytes(...)`. If storage target is local filesystem (fallback path in `document_storage_service.py`), this enables uploading arbitrary executable/script content which may be served back, leading to stored-XSS or RCE if served inline by the backend or any CDN.
- **Contrast:** The avatar upload handler (`update_avatar_handler.py:16-29`) **does** validate MIME type and extension — the document path should mirror this.
- **Recommendation:** Validate extension + MIME (and ideally magic bytes) against an allowlist before persisting.

#### H2. `/api/v1/users` lists all org users without explicit authorization guard
- **File:** `crusource-crm-backend/src/modules/user/routes/user_routes.py:50-53`
- **Severity:** HIGH
- **Confidence:** NEEDS REVIEW
- **Description:**
  ```python
  @router.get("", response_model=list[UserProfileResponse])
  def get_users(scope: Scope = Depends(get_user_scope), db: Session = Depends(get_db)):
      return list_users(db, str(scope.org_id))
  ```
  The endpoint is authenticated but has **no `require_permission`** guard, and returns the full `UserProfileResponse` (name, email, avatar, role) for **every user in the org** to any authenticated member. This is likely intentional for org-directory display, but it broadens data exposure and relies on the client to hide fields.
- **Recommendation:** Confirm intended scope. If all members genuinely need the list, at minimum exclude sensitive fields or add a `view_users` permission; otherwise gate with `require_permission("users", "view")`.

#### H3. Missing authorization / permission guards on several endpoints
- **File:** `crusource-crm-backend/src/modules/saved_views/routes/saved_views_routes.py:25-69` (all endpoints)
- **File:** `crusource-crm-backend/src/modules/documents/routes/documents_routes.py:89-103, 106-141, 153-179` (recycle bin, versions, binary content, share links)
- **File:** `crusource-crm-backend/src/modules/meetings/routes/meetings_routes.py:74-112` (google/ endpoints)
- **File:** `crusource-crm-backend/src/modules/notifications/routes/notifications_routes.py:17-33`
- **Severity:** HIGH
- **Confidence:** CONFIRMED (scope-containment present, authorization absent)
- **Description:** Multiple routes rely only on `get_user_scope` (which establishes org-scoping) but omit `require_permission(...)`. Examples:
  - Saved-views CRUD has no permission check (any authenticated user can create/delete saved views; delete handler still enforces ownership — needs confirmation).
  - Document recycle-bin restore/permanent-delete/empty, version download, and binary content endpoints have no `require_permission`.
  - Meetings Google Calendar endpoints (`/google/status`, `/google/free-busy`, `/google/calendars`, `/google/events`, `/google/disconnect`) lack permission guards.
  - Notifications/Inbox list and mark-read endpoints lack permission inspection related to inbox module.
- **Impact:** Authorization is only enforced via org-scoping, not by fine-grained module permissions. Combined with client-side-only UI hiding, this permits users to invoke operations the UI would normally hide.
- **Recommendation:** Add appropriate `require_permission` dependencies to each endpoint; confirm lower-privilege roles cannot reach destructive operations.

#### H4. In-memory rate limiter is process-local (not distributed)
- **File:** `crusource-crm-backend/src/shared/security/rate_limiter.py`
- **Severity:** HIGH
- **Confidence:** LIKELY
- **Description:** `RateLimiter` uses an in-memory `defaultdict` with a `threading.Lock`. With multiple workers/containers (typical Docker/uvicorn deployment) each process maintains its own counter, so the effective limit is multiplied by the number of processes. Also, the trust in `X-Forwarded-For` (line 40-42) can be spoofed if the proxy is misconfigured. OTP and login brute-force protection can thereby be bypassed at scale.
- **Recommendation:** Move rate limiting to a shared store (Redis) and validate/configure `X-Forwarded-For` trust at the proxy layer.

---

### MEDIUM

#### M1. Hardcoded default DB credentials
- **File:** `crusource-crm-backend/src/shared/database/core.py:9-12`
- **Severity:** MEDIUM
- **Confidence:** CONFIRMED
- **Description:**
  ```python
  SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL",
      "postgresql://admin:crusource_password@localhost:5432/crusource_db")
  ```
  Default credentials are baked into source. If `DATABASE_URL` is unset in a deployed environment, the app connects using these known credentials. Although `.env` supplies real values in dev, the fallback is risky.
- **Recommendation:** Fail fast when `DATABASE_URL` is absent in non-dev environments; never ship a named default with credentials.

#### M2. Public document share endpoints lack rate limiting / abuse controls
- **File:** `crusource-crm-backend/src/modules/documents/routes/documents_routes.py:181-203`
- **Severity:** MEDIUM
- **Confidence:** CONFIRMED
- **Description:** `GET /shared/{token}`, `GET /shared/{token}/content`, `GET /shared/{token}/download` are anonymous (no auth) and have no rate limiting. Although share tokens are UUID-like and unguessable, unauthenticated enumeration/abuse can be attempted freely.
- **Recommendation:** Add IP-based rate limiting to public share endpoints and consider token expiry.

#### M3. S3 storage service swallows some exceptions
- **File:** `crusource-crm-backend/src/shared/services/s3_storage_service.py:59-70, 77-95`
- **Severity:** MEDIUM
- **Confidence:** CONFIRMED
- **Description:** `get_presigned_url`, `delete_object` catch `Exception` and return `None`/`None` mostly silently (print only). Failures in deletion/copy are not surfaced to callers, which can silently leave orphaned objects or leave stale presigned URLs unresolved.
- **Recommendation:** Log failures via structured logger and, for delete/copy, propagate or explicitly handle as errors.

#### M4. New Google OAuth users provisioned as `admin` with `org_id=None`
- **File:** `crusource-crm-backend/src/modules/auth/handlers/google/google_callback_handler.py:134-154`
- **Severity:** MEDIUM
- **Confidence:** CONFIRMED
- **Description:** When a brand-new email signs in via Google, the user is created with `role=UserRole.admin` and `org_id=None`. This grants admin role globally until onboarding assigns an org, and any user who enters a Google email unbeknownst to the org can self-provision an admin account.
- **Recommendation:** Provision new Google users with a least-privilege role (or pending) and `org_id` resolved during onboarding; never default to `admin`.

#### M5. CORS allowed via wildcard methods/headers with credentials
- **File:** `crusource-crm-backend/src/main.py:135-141`
- **Severity:** MEDIUM
- **Confidence:** LIKELY
- **Description:** `allow_origins` is derived from `FRONTEND_URL` plus hardcoded localhost entries; `allow_methods=["*"]`, `allow_headers=["*"]`, `allow_credentials=True`. Credentials + wildcard methods/headers is common but should be tightened to explicit origins/methods matching the known frontends to reduce CSRF surface.
- **Recommendation:** Enumerate exact origins and methods; avoid `*` for methods/headers when credentials are allowed.

#### M6. `datetime.fromisoformat` on user-supplied date strings without validation
- **File:** `crusource-crm-backend/src/modules/campaigns/routes/campaign_routes.py:52-54, 72-74`
- **Severity:** MEDIUM
- **Confidence:** CONFIRMED
- **Description:** `date_from`/`date_to` query params are parsed with `datetime.fromisoformat` without try/except. Invalid input raises a `ValueError`, which is caught by the global `value_error_handler` and returned (400) — functionally OK, but the error handler echoes the raw exception; combined with C1 the boundaries are leak-prone. Signals inconsistent validation (other modules use Pydantic types).
- **Recommendation:** Use Pydantic/path types to validate date inputs.

---

### LOW

#### L1. Duplicate imports in route files
- **Files:** `leads_routes.py:2` and `contacts_routes.py:3`, etc.
- **Severity:** LOW
- **Confidence:** CONFIRMED
- **Description:** Duplicate `import status` / repeated imports degrade readability.
- **Recommendation:** Consolidate imports.

#### L2. Pagination `limit` unconstrained on several endpoints
- **Files:** `calls_routes.py:32-33`, `documents_routes.py:59-60`, `notifications_routes.py:18`, `meetings_routes.py:45-47`, `user_routes` list
- **Severity:** LOW
- **Confidence:** CONFIRMED
- **Description:** Many list endpoints accept `limit` with no `ge/le` bound (contrast `campaign_routes.py:66` which bounds 1–100). A client can request arbitrarily large pages.
- **Recommendation:** Add bounded `limit` constraints (e.g., `Query(..., le=100)`).

#### L3. Hardcoded localhost origins appended in CORS
- **File:** `src/main.py:131-133`
- **Severity:** LOW
- **Confidence:** CONFIRMED
- **Description:** Fixed `localhost:3000/3001/127.0.0.1:3000` origins are always allowed regardless of `FRONTEND_URL`.
- **Recommendation:** Derive origins solely from config in production.

#### L4. Auto-migration `ALTER TABLE` ad-hoc DDL at startup
- **File:** `src/shared/database/core.py:88-130` and `src/main.py:97-99`
- **Severity:** LOW
- **Confidence:** CONFIRMED
- **Description:** Startup issues ad-hoc `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` DDL and non-idempotent auto-migrations wrapped in try/except. This fragments schema management and can make deployments non-deterministic.
- **Recommendation:** Move to a versioned migration tool (Alembic).

#### L5. S3 service lazy `boto3` client with no server-side validation
- **File:** `s3_storage_service.py:31-40`
- **Severity:** LOW
- **Confidence:** CONFIRMED
- **Description:** Client instantiated lazily and reused; bucket/region defaults (`crusource-crm-dev-files`, `ap-south-1`) baked in. Acceptable for dev but should come from config in prod.

---

### INFO / Confirmed-as-OK

- **Argon2 password hashing** — confirmed in `src/shared/auth/security.py`. Good.
- **JWT config** — 30-min access / 7-day refresh tokens, HS256; reasonable (no confirmed defect).
- **Login hardening** — login flow records failures/success into `LoginHistory`, distinguishes user-not-found / deactivated / email-unverified / OAuth-password mismatch without trivially enumerating accounts (message "Incorrect email or password" reused for both not-found and bad password — good).
- **Onboarding token flow** — Google OAuth returns tokens via URL query params on redirect (`access_token`, `refresh_token`, `onboarding_token`). This is a known tradeoff for SPA OAuth flows but the tokens land in browser history/referrer. **NEEDS REVIEW** to balance convenience vs. token-exposure in URL; consider fragment or server-side POST.
- **Frontend token storage** — access/refresh tokens in `localStorage` (`auth.utils.ts`). Standard SPA approach but XSS-exposed; consider HttpOnly cookies if threat model demands.
- **Logout hygiene** — `performLogout()` clears Redux, TanStack cache, and multiple tenant-related localStorage keys to prevent multi-tenant state bleed. Good practice.
- **`.env` seeding** — real AWS/Google credentials present in `.env`/`.env.local` but are git-ignored and not tracked. Confirmed not committed.
- **RBAC** — `usePermissions` + `PermissionGuard` correctly treat frontend checks as display-only; server-side `require_permission` is the enforcement layer (with the H3 caveats).

---

## 5. Architecture Overview

### Backend (CQRS)
```
Request → Route (FastAPI APIRouter) → Command/Query → Handler → Repository → Model/DB
                                      └── shared guards (auth, scope, permission, subscription)
```
- **Entry:** `src/main.py` — CORS, exception handlers, scheduler (calendar poll 5min), ~40 routers mounted.
- **Shared layers:**
  - `src/shared/auth/*` — JWT signing/verification, token guard, scope resolution (30s TTL cache), RBAC role/permission checkers.
  - `src/shared/database/core.py` — engine/session, model registry, ad-hoc auto-migrations.
  - `src/shared/services/s3_storage_service.py` — S3 upload / presigned URLs / delete / copy.
  - `src/shared/security/rate_limiter.py` — in-memory per-process limiters.
  - `src/shared/exceptions/global_handlers.py` — global exception mapping (info leak, see C1).
- **Async worker:** `src/worker.py` — SQS-based for background tasks (campaign dispatch, etc.).

### Frontend (Next.js App Router)
- `src/lib/api.ts` + `src/lib/api/httpClient.ts` — `fetchWithAuth` with single-flight token refresh + request replay.
- `src/lib/auth.utils.ts` — token storage in `localStorage`, logout with cache/state clearing.
- `src/store/*` — Redux slices (auth, formatting, orgSettings).
- `src/hooks/usePermissions.ts` — client RBAC resolution mirroring backend modules.
- `src/components/shared/PermissionGuard.tsx` — UI gating wrapper.
- Domain modules via `src/services/*` + TanStack Query hooks.

---

## 6. Cross-Cutting Observations

1. **Authz consistency:** Module routes (leads, contacts, deals, tasks, campaigns, calls) consistently apply `require_permission` + org scope; but saved-views, documents (recycle/versions/share/Google), meetings Google, and notifications routes rely on scope-only. This inconsistency should be normalized.
2. **File-validation inconsistency:** Avatar upload validates (MIME+ext), document upload does not. Reconcile into a shared validation helper.
3. **Rate limiting:** auth endpoints are rate-limited (good); newer endpoints (public shares, Google) are not.
4. **Error handling:** two different philosophies — one handler leaks DB detail (C1), the other is generic. Unify to generic client messages + server-side logging.
5. **Frontend-backend parity:** frontend `usePermissions` exposes the same module names as backend permission resolution, but hidden endpoints (H3) mean the UI state may not match actual server capability.

---

## 7. Recommended Prioritized Remediation Roadmap

| Priority | Finding | Action | Effort |
|---|---|---|---|
| P0 | C1 | Return generic message on DB errors | S |
| P1 | H1 | Add MIME/ext/magic-byte validation on document upload | S–M |
| P1 | H3 | Add permission guards to scope-only endpoints | M |
| P1 | H2 | Confirm & gate `/api/v1/users` exposure | S |
| P1 | H4 | Move rate limiting to Redis / verify proxy trust of `X-Forwarded-For` | M |
| P2 | M4 | Least-privilege provisioning for new Google users | M |
| P2 | M1/M5/M6/M2/M3 | Config-driven defaults, tighten CORS, validate dates, rate-limit public shares, surface S3 errors | M |
| P3 | L1–L5 | Cleanup imports, bound pagination, migrations via Alembic | L |

---

## 8. Appendix — Key Files Referenced

| File | Role |
|---|---|
| `crusource-crm-backend/src/main.py` | App entry, CORS, routers, scheduler |
| `.../src/shared/auth/{security,token_guard,scope_guard,permission_guard,guards}.py` | Authn/Authz |
| `.../src/shared/exceptions/global_handlers.py` | Global error mapping (C1) |
| `.../src/shared/database/core.py` | DB config, auto-migrations (M1, L4) |
| `.../src/shared/services/s3_storage_service.py` | S3 storage (M3, L5) |
| `.../src/shared/security/rate_limiter.py` | Rate limiting (H4) |
| `.../src/modules/auth/handlers/google/google_callback_handler.py` | Google OAuth (M4) |
| `.../src/modules/documents/handlers/upload_document_handler.py` | Document upload (H1) |
| `.../src/modules/user/routes/user_routes.py` | User endpoints (H2) |
| `.../src/modules/{saved_views,documents,meetings,notifications}/routes/*` | Scope-only endpoints (H3) |
| `.../src/modules/user/handlers/update_avatar_handler.py` | Reference validation pattern |
| `crusource-crm-frontend/src/lib/{api,auth.utils}.ts` | Frontend auth/refresh |
| `.../frontend/src/hooks/usePermissions.ts`, `.../components/shared/PermissionGuard.tsx` | Client RBAC display |

*End of report.*
