# CRM built-in super-admin retirement plan

**Status:** Proposed implementation plan; no application code, API, database, or deployment changes have been made.

**Reviewed:** 17 November 2026

**Scope:** `crusource-crm-frontend/` and `crusource-crm-backend/`; the central portal in `crusource-admin/` is a protected dependency and is not a retirement target.

## 1. Goal and safety rule

Retire the standalone super-admin experience embedded in the CRM frontend and retire its CRM-only platform-user features when their current responsibilities have an approved central-admin replacement. Preserve ordinary organization-scoped CRM administration and the service-to-service CRM APIs the central portal uses.

“Super-admin” currently refers to several different mechanisms. A path or symbol containing `admin` or `superadmin` is not enough to classify it for deletion. Implement this plan by tracing each route, caller, authorization mechanism, database dependency, test, and operational consumer. Do not remove a dependency until its replacement is deployed and its contract is verified.

## 2. Verified architecture and dependency boundary

The CRM frontend contains a standalone `/superadmin` application area: routes under `src/app/superadmin/`, a `PlatformLayout`, platform session/auth components, and service modules calling `/api/v1/superadmin/*`. This is distinct from the central portal, which is the separate `crusource-admin/` repository and uses a central administrator session.

The central portal's CRM Organizations feature calls its own `/admin/crm/organizations…` client paths. Its CRM service boundary maps those calls to CRM backend `/api/v1/internal/admin/crm/organizations…` and `/api/v1/internal/admin/crm/trial-extensions…` routes. These routes use short-lived RS256 service-delegation JWTs, a central-admin actor claim, explicit scopes, limits, and no-store responses. They do not use the CRM browser's platform cookie or `require_super_admin`. Preserve these contracts during UI retirement.

The CRM backend mounts those central-service routes from files under `src/modules/superadmin/`. Their current directory name is misleading: the route guards and caller contract make them a central-admin integration boundary. Move or rename them only after mapping every central portal API call and keeping the wire contract compatible.

The CRM platform-auth subsystem is also used by the built-in portal. It manages CRM platform staff accounts, MFA/session state, owner grants, sales capabilities, and platform demo-request workflows. The central portal has its own login, session, permissions, and backend. Replacing the CRM UI alone does not replace platform-auth-dependent workflows; keep that subsystem until each consumer is either retired or migrated to a central-admin contract.

## 3. Scope classification

| Area | Decision | Evidence and boundary |
|---|---|---|
| CRM frontend `/superadmin/**` pages and shell | Retire after central replacement/ownership is confirmed | `crusource-crm-frontend/src/app/superadmin/**`, `src/components/superadmin/**` render the standalone CRM platform workspace. |
| CRM frontend platform login/session/access UI and API clients | Retire with the CRM platform-auth workflows that depend on them | `platformAuth.service.ts`, `platformAccess.service.ts`, `platformHttpClient.ts`, `PlatformSessionBoundary`, `PlatformSessionContext`, and related hooks/state call `/superadmin/auth/*`. |
| CRM frontend super-admin organization, dashboard, feedback, trial and login-history clients/screens | Retire only the standalone CRM portal surface | `superadmin.service.ts`, `superadminLoginHistory.service.ts`, and `platformFeedbackImages.service.ts` serve `/superadmin/**`. Confirm no ordinary CRM page imports them before deletion. |
| CRM internal organization and trial-extension service routes | Preserve | `internal_organization_routes.py` and `internal_trial_extension_routes.py` expose service-delegated central CRM functionality. The central portal calls these capabilities. Keep signed delegation, scopes, limits, and response contracts. |
| CRM browser platform auth (`/api/v1/superadmin/auth/**`) and platform staff records | Defer retirement until workflow migration is complete | `platform_auth_router` is mounted separately from the super-admin feature routers. CRM demo-request management, owner capability management, and platform staff sessions depend on it. |
| `is_super_admin` on CRM `users`, auth DTO/scope/bootstrap and billing paths | Preserve until all consumers are removed or migrated; drop only in a later forward migration | Current code uses the flag in platform-auth eligibility, user/session scope, bootstrap, subscription checks, user mapping, and service/demo workflows. It is not just a display bit. |
| CRM organization-scoped Admin UI/API (`/admin/**`) | Preserve | This is tenant administration for CRM organizations, separate from cross-organization platform administration. Keep its role/profile/team/user permission behavior. |
| Central portal (`crusource-admin/`) and VMS backend | Out of scope for deletion | Do not edit, replace, or couple its authentication to CRM tenant tokens. Keep central admin login and per-request authorization intact. |
| Historical migrations, docs, archived screenshots and audit evidence | Preserve as history | Do not rewrite old migration files or erase historical evidence. Add forward migrations only if a later approved cleanup requires schema changes. |

## 4. Implementation sequence

### Phase 0 — Baseline and complete dependency inventory

1. Confirm clean/known Git state in each owning repository and inspect unmerged entries and conflict markers before editing. Preserve unrelated work.
2. Capture the current CRM frontend/backend CI workflows, lockfiles, Python environment, migration heads, and deployment configuration. Record exact versions and commands from the current repositories rather than relying on old docs.
3. Build a route and symbol inventory from source, not just names. Include frontend pages, imports, navigation/redirects, API clients, analytics/robots/host handling, backend mounts, middleware, guards, schemas, models, migrations, jobs, environment flags, tests, fixtures, seeds, and runbooks.
4. Trace each central portal CRM API call end to end: UI/API module → central API client/session → VMS backend CRM service adapter → CRM internal route → CRM service-delegation guard → query/command. Record method, path, required scope, request/response schema, actor, and current call site.
5. Confirm whether any staff currently sign in directly to the CRM-hosted portal and enumerate platform accounts, active sessions/credentials, pending invitations, audit history, CRM product demo enquiries, and trial-extension workflows. Use authorized read-only production inspection when available; never copy secrets or personal data into the plan or logs.
6. Freeze this inventory as the retirement baseline and agree which platform workflows remain in CRM, move to the central portal, or are intentionally discontinued. Do not begin destructive removals while ownership is unresolved.

### Phase 1 — Central portal contract and authorization readiness

1. Verify the central portal has working CRM screens for every capability intended to replace a CRM page. Route existence is not sufficient; exercise real API calls with an authorized isolated test account and permitted fixtures.
2. For organization directory, metrics/dashboard, detail, members, exports, audit, feedback, billing and trial extension, verify whether the central portal calls the CRM service endpoints and identify the exact required scope for each call.
3. Verify service delegation end to end: accepted issuer/audience/type/product/actor, RS256 key ID allowlist, 60-second maximum token lifetime, `jti`, required base read scope, per-operation scope, rate limits, fail-closed configuration, no-store response, logging without credentials, and behavior for invalid/expired/wrong-product/wrong-scope tokens.
4. Confirm the central portal's refresh/logout/session revocation and product authorization remain owned by its own backend/session. No browser tenant JWT, CRM platform cookie, or `is_super_admin` claim may become the central portal's authorization source.
5. If the central portal lacks a workflow that the CRM portal currently owns, implement and validate that central workflow in its owning repositories first. This retirement plan does not authorize silently dropping that workflow.

### Phase 2 — Retire only the standalone CRM portal surface

1. Remove CRM frontend navigation, links, route entries, portal-only layouts and screens after the replacement is confirmed. Decide explicitly whether old `/superadmin/**` URLs should return 404 or a neutral redirect to the central portal; do not redirect with CRM cookies, credentials, or tokens.
2. Remove portal-only frontend API clients, hooks, query keys, platform state, labels/translations, and imports only after repository-wide reference checks show they have no ordinary CRM consumers. Preserve global `AuthGuard`, regular admin services/slices, and organization-level `/admin/**` components.
3. Update robots, sitemap, host/subdomain handling, analytics exclusions, route-loading heuristics, CSP/proxy rules and deployment rewrites that specifically assume the CRM `/superadmin` pages. Do not remove generic `/api` proxying or central portal configuration.
4. Deploy frontend and backend changes in a compatibility-safe order. Keep backend APIs available while any deployed CRM frontend still calls them. Monitor the exact retired endpoints for stale clients before backend removal.

### Phase 3 — Separate central service endpoints from legacy module naming

1. Move the service-delegated organization and trial-extension routes, schemas, queries and handlers out of the legacy `modules/superadmin` namespace into a clearly named CRM internal-admin/service module, or document why only route ownership is renamed. Keep public URL paths and serialized contracts stable for this refactor.
2. Keep `require_crm_service_actor`, explicit scopes, RS256 verification, limits, cache controls and audit behavior. Do not replace them with `require_super_admin`, a tenant role check, or a shared `/api/v1` prefix assumption.
3. Update router registration and imports atomically, then run central-admin contract tests and CRM route/auth tests. Confirm every endpoint is mounted once, protected once, and rejects a CRM tenant bearer token and a CRM platform cookie.
4. Only remove the old route module after static import search, route enumeration, test coverage, and central-admin integration checks prove that all consumers use the preserved service API.

### Phase 4 — Retire CRM platform staff auth and dependent workflows, if approved

1. Migrate or explicitly discontinue each platform-auth consumer: platform staff login/MFA, staff invitations/activation/revocation, sales capabilities, CRM demo request access/actions, demo follow-up notifications, internal trial-review paths, and platform-specific audit events. Identify any public intake or CRM customer sales flow that must remain; these may depend on shared `demo_requests` logic without needing the old portal.
2. Replace platform identity with the central-admin backend's server-to-server delegated actor and narrowly scoped contracts where the central portal is the chosen owner. Apply central session authorization on every request and preserve actor attribution, idempotency, audit, CSRF/browser protections at their correct trust boundary, and capability revocation semantics.
3. Do not let central-admin browser JWTs call CRM directly. The central backend must sign short-lived, product-scoped delegation tokens; CRM must verify them with configured public keys and reject absent/invalid keys in protected environments.
4. Remove the CRM platform-auth router and platform frontend code only after all platform-only workflows have a verified owner and production usage has been checked. If any such workflow remains intentionally CRM-owned, retain its minimum required auth and explicitly revise the scope instead of claiming full retirement.

### Phase 5 — Data and schema cleanup (last, separate approval/release)

1. First disable new provisioning/invitations and revoke or expire sessions through supported application commands. Preserve the evidence needed for audit and incident response.
2. Inventory platform users, credentials, invitations, delivery rows, sessions, security events and foreign-key relationships. Establish retention/legal holds and export only approved, minimal metadata. Do not delete rows merely because the UI is gone.
3. Search every runtime and migration consumer of `users.is_super_admin`, including auth/session DTOs, `scope_guard`, bootstrap, subscription access, admin user mapping, deletion flows, demo eligibility, seed scripts and tests. Replace each with the correct explicit realm/permission model before schema change.
4. Add a new forward Alembic migration only after application code no longer expects the column. Make downgrade behavior safe and explicit; retain the historical migration unchanged. Validate upgrade/downgrade on disposable PostgreSQL snapshots and supported prior revisions, with row counts and representative records preserved.
5. Drop `is_super_admin` and platform-auth tables only when no live central service route, CRM feature, retained audit process, or supported rollback image requires them. Prefer a separate later release for destructive DDL; define backup/restore and rollback limits before execution.

## 5. Mandatory acceptance and security gates

### CRM frontend

- No unintended `/superadmin/**` route, portal navigation, dead import, client call, login widget, or stale hostname/SEO handling remains.
- Normal CRM sign-in, session refresh, dashboard, organization-scoped admin, permissions, invitations, role/profile/team/user management, billing and CRM sales intake remain correct.
- The frontend no longer attempts to authenticate to CRM platform endpoints after their approved retirement. Existing tenant auth and central portal auth remain separate.
- Run the complete applicable CRM frontend CI from its current workflow: clean lockfile install in an isolated checkout where feasible, formatting check with correct base SHA, full lint, all registered tests and spreadsheet tests, TypeScript, all CI browser regressions, production build with safe test config, and audit. Include focused route/import/API regressions for this change.

### CRM backend and database

- Existing CRM tenant `/admin/**` authorization and organization isolation remain unchanged.
- The central service routes continue to serve authorized central portal organization/trial workflows and reject missing, malformed, expired, wrong-issuer/audience/product/actor, wrong-key, wrong-scope and oversized delegation tokens. They remain fail-closed when disabled or key configuration is invalid.
- CRM platform routes are either deliberately retained for remaining consumers or consistently unavailable after their owner migration; no route is accidentally public or silently falls back to tenant bearer authentication.
- Preserve all demo intake, notification, trial, billing and audit behavior selected as still supported. Verify data retention and foreign-key handling before cleanup.
- Run backend CI parity from the current workflow, including Ruff, compileall, full pytest, PostgreSQL opt-in tests, committed migration tests, empty-database drift check, Alembic check, and migration upgrade from supported revisions on disposable PostgreSQL. Never use stage/production databases for validation.

### Central portal and release

- Run the central-admin tests/build and verify all CRM Organizations and trial operations with an isolated central administrator and fixtures; check CRM and VMS product isolation.
- Deploy compatible central API/backend support before removing CRM-owned UI/API behavior. Preserve a rollback path that does not restore an insecure authorization path or break the central portal.
- Verify deployed commit identities, CI gates, API configuration, public-key rotation/readiness, migration completion and relevant logs. Local success is not stage verification.
- Observe old CRM `/superadmin` page/API traffic and platform-auth usage for an agreed observation period. Set a measured removal criterion and owner; no guessed zero-usage assumption.

## 6. Explicit non-goals and prohibited shortcuts

- Do not remove or rename the separate `crusource-admin/` central portal or its `/login`, shared auth, CRM/VMS/screens routes, central backend, or service session.
- Do not delete the CRM's ordinary tenant Admin module or conflate it with platform administration.
- Do not bulk-delete every file containing `admin`, `superadmin`, `platform`, or `is_super_admin`.
- Do not drop `is_super_admin`, platform tables, CRM Organizations service routes, demo intake, or trial data in the same change as frontend route removal.
- Do not edit old Alembic migrations, reset databases, rotate or expose secrets in logs, provision test staff in shared databases, or deploy without the required owning-repository CI and release authorization.
- Do not describe central-admin integration as complete solely because route names or `/api/v1` prefixes match; verify authentication, authorization, scopes, tenant/product boundary and real responses.

## 7. Source evidence checked

These source paths were inspected while preparing this plan. Current source and current CI remain authoritative when implementation begins.

- CRM frontend portal routes: [`src/app/superadmin`](../../../crusource-crm-frontend/src/app/superadmin)
- CRM frontend platform UI: [`src/components/superadmin`](../../../crusource-crm-frontend/src/components/superadmin)
- CRM frontend portal API clients: [`superadmin.service.ts`](../../../crusource-crm-frontend/src/services/superadmin.service.ts), [`platformAuth.service.ts`](../../../crusource-crm-frontend/src/services/platformAuth.service.ts), [`platformAccess.service.ts`](../../../crusource-crm-frontend/src/services/platformAccess.service.ts), [`platformHttpClient.ts`](../../../crusource-crm-frontend/src/lib/api/platformHttpClient.ts)
- CRM backend router mounts and registration: [`src/main.py`](../../../crusource-crm-backend/src/main.py)
- CRM backend central service routes: [`internal_organization_routes.py`](../../../crusource-crm-backend/src/modules/superadmin/routes/internal_organization_routes.py), [`internal_trial_extension_routes.py`](../../../crusource-crm-backend/src/modules/superadmin/routes/internal_trial_extension_routes.py)
- CRM backend service-token verification: [`service_delegation_guard.py`](../../../crusource-crm-backend/src/shared/auth/service_delegation_guard.py)
- CRM backend platform staff auth: [`platform_auth/routes.py`](../../../crusource-crm-backend/src/modules/platform_auth/routes.py), [`platform_auth`](../../../crusource-crm-backend/src/modules/platform_auth)
- CRM backend shared flag consumers: [`users model`](../../../crusource-crm-backend/src/modules/user/repositories/models.py), [`scope_guard.py`](../../../crusource-crm-backend/src/shared/auth/scope_guard.py), [`subscription_access.py`](../../../crusource-crm-backend/src/modules/billing/services/subscription_access.py)
- Central portal CRM API callers: [`organizations.api.ts`](../../../crusource-admin/libs/domains/crm/src/api/organizations.api.ts), [`trial-extensions.api.ts`](../../../crusource-admin/libs/domains/crm/src/api/trial-extensions.api.ts)
- Central portal login and service-boundary description: [`central-admin-login.md`](../../../crusource-admin/docs/central-admin-login.md)
- Earlier super-admin contracts and handoff: [`phase 4 API contracts`](superadmin-phase4/CONTRACTS.md) and [`phase 5 handoff`](superadmin-phase4/PHASE_5_HANDOFF.md). These are historical evidence; verify all present-tense claims against current source.

## 8. Audit note

This is a source-based implementation plan, not evidence that removal has been implemented, that the central portal currently covers every CRM platform workflow, or that production has no direct CRM super-admin users. The remaining required decisions are the workflow ownership matrix and authorized live usage/data inventory described in Phase 0. Application CI, browser flows, PostgreSQL migrations, and stage verification are intentionally pending until code changes are authorized and made.
