# Crusource CRM Developer Console & Ecosystem Architecture Research

- **Date:** 26 November 2026
- **Status:** RESEARCH & ARCHITECTURE SPECIFICATION (Source-Verified Against Crusource Codebase)
- **Owning Repositories:**
  - `crusource-crm-backend/` (FastAPI, SQLAlchemy, Alembic — Public REST APIs, API Keys, OAuth 2.0 Provider, Transactional Webhook Outbox)
  - `crusource-crm-frontend/` (Next.js App Router — Tenant Admin Setup Hub `/dashboard/admin/developer/*` + OAuth Consent UI)
  - `crusource-admin/` & `crusource-vms-backend/` (`admin-crm` — Cross-tenant Marketplace App Verification & Ecosystem Governance)
  - `crusource-website/` / public developer docs portal (External Developer Portal & OpenAPI Reference)
- **Companion Documents:**
  - [`GOOGLE_ADS_INTEGRATION_PROPOSAL.md`](GOOGLE_ADS_INTEGRATION_PROPOSAL.md)
  - [`../analytics/VERCEL_ANALYTICS_MIXPANEL_SUPERADMIN_IMPLEMENTATION_PLAN.md`](../analytics/VERCEL_ANALYTICS_MIXPANEL_SUPERADMIN_IMPLEMENTATION_PLAN.md)
  - [`../superadmin/BUILT_IN_SUPERADMIN_RETIREMENT_PLAN.md`](../superadmin/BUILT_IN_SUPERADMIN_RETIREMENT_PLAN.md)

---

## 1. Executive Summary

To support external applications and partner integrations (Zapier, Make, n8n, Google Ads, Zoho, accounting/ERP systems, and custom customer backends), Crusource CRM needs a structured **Developer Console** rather than ad-hoc endpoints.

Comparative research into **HubSpot** and **Salesforce** shows that durable CRM developer platforms separate **two personas** and **two trust boundaries**:
1. **Single-Tenant Private Integrations (Org Admin inside CRM Settings):** Customer admins generating scoped API tokens and subscribing to real-time webhooks for their own workspace without needing OAuth ceremony.
2. **Multi-Tenant Public Apps (External Developers / ISVs + Customer Admin Consent + Platform Governance):** Third-party developers creating OAuth 2.0 applications (`client_id`/`client_secret`), testing in isolated Sandbox orgs, installing into customer workspaces only after explicit org-admin consent, and passing platform verification before public listing.

Crusource CRM already has strong security and UI foundations (`Scope` RBAC isolation, `EncryptedProviderToken` `MultiFernet` storage, Redis `RateLimiter` / `sliding_window`, OpenAPI generation, and `AdminSetupHub`), making a **3-phase incremental build** practical and low-risk.

---

## 2. Industry Benchmark: How HubSpot and Salesforce Do It

### 2.1 HubSpot Developer Platform Architecture

HubSpot separates single-org automation from commercial partner development across five pillars:

1. **Private Apps (Portal-Scoped):**
   - Created directly inside a customer's HubSpot portal Settings without setting up a public OAuth server.
   - Issues an opaque access token bound strictly to selected granular permission scopes (e.g., `crm.objects.contacts.read/write`) with rotation and audit controls.
2. **Developer Account & Projects (ISV/Partner-Scoped):**
   - Separate parent **Developer Account** for managing Public Apps, provisioning isolated **Test Accounts (Sandboxes)** simulated at different subscription tiers, and deploying CLI-managed projects (`app.json` / `hsproject.json`).
3. **OAuth 2.0 for Public Apps:**
   - Standard Authorization Code flow returning short-lived access tokens and long-lived refresh tokens bound to installed portal + granted scopes.
4. **Webhooks & Webhook Logs / Journal:**
   - Target URL subscriptions mapped to CRM domain events (`contact.creation`, `deal.updated`), plus **Webhook Logs / Traces** and the **Webhooks Journal API** so developers can inspect status codes, headers, retries, payloads, and replay missed events.
5. **Frontend Extensibility (UI Extensions & CRM Cards) + App Marketplace:**
   - Custom **CRM Cards** embedded into Deal/Contact/Company record sidebars and full-page *App Home* settings screens.
   - **App Marketplace** submission requires privacy policy, terms, scope justification, demo walkthrough, and security/UX approval.

### 2.2 Salesforce Developer Platform Architecture

Salesforce recently evolved legacy *Connected Apps* into **External Client Apps (ECAs)** inside **External Client App Manager**, specifically tightening zero-trust governance:

1. **External Client Apps (Developer vs. Admin Separation of Duties):**
   - **Developers** manage global app metadata (app name, callback URLs, requested OAuth scopes) cleanly in Setup / source control.
   - **Customer Org Admins** separately manage security policies (IP restrictions, permitted profiles/roles, install authorization, token revocation) and an ECA cannot shadow-authenticate against an org without explicit installation/definition.
2. **Multiple OAuth 2.0 Flows:**
   - **Authorization Code + PKCE:** SPAs, mobile, and native clients.
   - **Web Server Flow:** Confidential server backends holding a `client_secret`.
   - **Client Credentials / JWT Bearer (X.509):** Headless machine-to-machine or service integrations without interactive user sign-in.
3. **Granular Scopes:**
   - Explicit least-privilege scopes (`api`, `refresh_token`, `offline_access`, `web`, `sfap_api`) rather than blanket admin access.
4. **Platform Events & Pub/Sub API:**
   - Decoupled event bus enabling durable publish/subscribe delivery with replay IDs so external services handle bursts and reconnects without losing state.
5. **AppExchange & Security Review:**
   - Packaged namespaces to prevent naming collisions, License Management App (LMA) for install/trial tracking, and mandatory automated + manual security reviews before listing.

### 2.3 Key Design Lessons for Crusource CRM

| Capability | HubSpot Pattern | Salesforce Pattern | Best Fit for Crusource CRM |
| --- | --- | --- | --- |
| **In-house / single-org scripts** | Private Apps (scoped token inside portal) | Local External Client App | **Phase 1 Private Apps** inside CRM Admin Setup Hub (`/dashboard/admin/developer/api-keys`) |
| **3rd-party multi-tenant SaaS apps** | Public Apps + Developer Account | Packaged External Client App | **Phase 2 Public Apps** (`client_id`/`client_secret`, Authorization Code + PKCE) + Developer Console |
| **Org admin control** | Portal app connect/uninstall | Admin policy & install approval separated from developer metadata | **Strict installation consent boundary** (`app_installations` record controlled by CRM `require_manage_org()`) |
| **Event delivery** | Outbound Webhooks + Logs + Journal | Platform Events / Pub-Sub API with replay | **Transactional Outbox -> Async Worker -> HMAC Webhooks + Delivery Inspector & Replay UI** |
| **Developer testing** | Test Accounts (simulated tiers) | Scratch / Sandbox Orgs | Provision capped **Sandbox CRM Orgs** using existing `organization` + `sample_data` module |
| **Embedded CRM UI** | CRM Cards + React UI Extensions | Lightning Web Components / Canvas | **Phase 3 Structured JSON CRM Cards** first (avoiding arbitrary third-party JS injection early) |

---

## 3. Crusource Codebase Baseline Audit (Verified Existing Building Blocks)

Inspection of `crusource-crm-backend/` and `crusource-crm-frontend/` confirms several security and UX primitives already exist and should be reused rather than reinvented:

| Existing Module / File | Verified Capability | Role in Developer Console |
| --- | --- | --- |
| `crusource-crm-backend/src/shared/auth/guards.py` & `dtos.py` | `Scope(user_id, org_id, role, is_admin, ...)` + `PermissionDTO`, `require_manage_org()`, `SetupPermissionChecker` | Enforce tenant isolation and permission scoping identically across UI JWTs, Private API Keys, and OAuth tokens. |
| `crusource-crm-backend/src/shared/security/provider_credentials.py` | `EncryptedProviderToken` (`MultiFernet` using `INTEGRATION_ENCRYPTION_KEYS` / `INTEGRATION_ENCRYPTION_KEY`) | Encrypt outbound webhook HMAC signing secrets (`enc:v1:...`) and partner OAuth credentials at rest. |
| `crusource-crm-backend/src/modules/integrations/repositories/models.py` | `IntegrationCredential` (`org_id`, `provider`, encrypted tokens, `expires_at`, `metadata_json`) | Already established pattern for tenant external integration credentials (currently used by `zoho/` module). |
| `crusource-crm-backend/src/shared/security/rate_limiter.py`, `sliding_window.py`, `one_time_tokens.py`, `operation_leases.py` | Redis-backed admission/rate limiting (`redis==5.0.3` in `requirements.txt`) & single-use tokens | Power per-API-key / per-app rate limits (`X-RateLimit-*`) and single-use OAuth authorization codes. |
| `crusource-crm-backend/src/shared/events/workspace_stream.py` | SSE workspace event hints & stream admission | Internal UI hint pattern; must be complemented by a persistent **DB Webhook Outbox** for reliable external delivery. |
| `crusource-crm-backend/src/main.py` | FastAPI OpenAPI (`/docs`, `/redoc`, `/openapi.json` via `ENABLE_DOCS_IN_PROD`) | Foundation for generating filtered public OpenAPI documentation. |
| `crusource-crm-frontend/src/components/admin/setup/AdminSetupHub.tsx` & `src/constants/adminNav.constants.ts` | Category-driven Setup Hub (`Users & Access Control`, `Security & Audit`, `Customization`, `Data Administration`) | Natural home for customer-facing **Developer & Integrations** settings (`Private Apps`, `Webhooks`, `Connected Apps`). |
| `crusource-crm-frontend/src/app/dashboard/admin/automations/page.tsx` | Current `"Coming Soon"` stub | Do not overload; keep custom API/webhook developer tooling under a dedicated Developer Console section. |
| `crusource-admin/` & `crusource-vms-backend/` (`src/modules/admin-crm/`) | Central platform admin control plane across CRM organizations | Designated owner for **platform-wide ISV app verification, approval/suspension, and ecosystem telemetry** (not customer tenant settings). |

---

## 4. Architectural Split: CRM Tenant Boundary vs. Central Platform Boundary

Per repository ownership boundaries (`AGENTS.md`):
- **Customer CRM Workspace (`crusource-crm-frontend` + `crusource-crm-backend`):**
  - Owns Private Apps (API Keys), Outbound Webhooks & Delivery Logs, Public REST APIs (`/api/v1/public/*`), OAuth 2.0 `/oauth/authorize` consent & token endpoints, and tenant `app_installations`.
  - Every API token and installed OAuth token resolves strictly inside `org_id` + explicit granted scopes.
- **External Developer Portal (`crusource-website/` or dedicated `/developer` app/routes):**
  - Public OpenAPI Explorer, Guides, OAuth/Webhook quickstarts, and Public App registration portal (where ISVs create `client_id`/`client_secret` apps and spin up sandbox CRM orgs).
- **Central Super Admin (`crusource-admin/` + `crusource-vms-backend/`):**
  - Owns cross-tenant governance: reviewing submitted Public Apps (`Draft -> In Review -> Approved / Rejected -> Suspended`), overriding partner rate limits, and inspecting aggregate app adoption telemetry.

---

## 5. Phased Implementation Blueprint

### Phase 1 — Tenant Private Apps, Scoped Public APIs & Transactional Webhooks (CRM Setup Hub)

**Goal:** Enable customers and automation tools (Zapier/Make/n8n/custom backends) to integrate with a single CRM organization safely.

#### 5.1 Public API Contract Layer (`/api/v1/public/*`)
- **Separate public API schemas from internal UI BFF routes:** Internal dashboard endpoints change frequently with UI components; partner integrations require stability.
- Expose versioned REST endpoints under `/api/v1/public/` for core objects:
  - `leads`, `contacts`, `accounts`, `deals`, `notes`, `tasks`, `pipelines`, `webhooks`
- Support standard developer ergonomics:
  - Cursor-based pagination (`cursor`, `limit`, `next_cursor`)
  - Write idempotency (`Idempotency-Key` header backed by Redis/DB lease window)
  - Consistent error envelope (`error.code`, `error.message`, `correlation_id`, `details[]`)
  - Standard rate-limit response headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After` on `429`)

#### 5.2 Private Apps & Scoped API Keys
- **Data Model (`crusource-crm-backend` Alembic migration):**
  - `developer_private_apps`: `id`, `org_id`, `name`, `description`, `created_by_user_id`, `status` (`active` | `revoked`), `allowed_ips` (nullable CIDR list), `created_at`, `updated_at`.
  - `api_keys`: `id`, `org_id`, `private_app_id`, `key_prefix` (e.g., `cs_live_8f3a`), `key_hash` (SHA-256 hex), `scopes` (`TEXT[]` / `JSONB`), `last_used_at`, `expires_at`, `revoked_at`, `created_by_user_id`.
- **Security Controls:**
  - Raw API token shown **only once** at generation/rotation time; database stores only `key_prefix` + `SHA-256(token)`.
  - Dual-mode auth dependency (`resolve_public_api_scope()`): accepts `Authorization: Bearer cs_live_...`, verifies active app + non-expired/non-revoked key + optional IP allowlist + scope intersection with the org's plan & RBAC rules, and binds `Scope(org_id=...)` seamlessly.
  - Scope naming convention (`<resource>:<action>`): `leads:read`, `leads:write`, `contacts:read`, `contacts:write`, `accounts:read`, `accounts:write`, `deals:read`, `deals:write`, `pipelines:read`, `webhooks:manage`.

#### 5.3 Outbound Webhooks Engine (Transactional Outbox + Delivery Logs)
- **Data Model:**
  - `webhook_subscriptions`: `id`, `org_id`, `private_app_id` (nullable if global partner app in Phase 2), `developer_app_id` (nullable), `target_url`, `signing_secret_encrypted` (`EncryptedProviderToken`), `events` (e.g., `["lead.created", "deal.stage_changed", "deal.closed_won"]`), `status` (`active` | `paused` | `disabled_failing`), `consecutive_failures`, `created_at`.
  - `webhook_outbox`: `id`, `org_id`, `event_id` (UUID), `event_type`, `payload_json`, `status` (`pending` | `dispatched`), `created_at`.
  - `webhook_deliveries`: `id`, `subscription_id`, `outbox_event_id`, `attempt_number`, `http_status`, `latency_ms`, `response_snippet` (truncated <= 1 KB, scrubbed), `error_reason`, `delivered_at`, `next_retry_at`.
- **Delivery & Security Guarantees:**
  - Write `webhook_outbox` inside the **same SQLAlchemy DB transaction** as CRM entity writes so webhooks never fire for rolled-back transactions and never add latency to CRM UI requests.
  - Worker / scheduler picks up outbox rows and fans out signed HTTP `POST` requests:
    - Headers: `X-Crusource-Event`, `X-Crusource-Event-Id`, `X-Crusource-Timestamp`, `X-Crusource-Signature: t=<unix>,v1=<hmac_sha256(secret, f"{timestamp}.{raw_body}")>`.
  - **SSRF Protection:** Resolve target hostname DNS prior to TCP connect and reject private/loopback/link-local/metadata IPs (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, IPv6 `::1`, `fc00::/7`, `fe80::/10`), disable redirects on delivery, and enforce `https://` in production.
  - **Exponential Backoff & Auto-Disable:** Retry failed `5xx`/timeout deliveries with jittered backoff (e.g., 1m, 5m, 30m, 2h, 6h) and pause endpoint after sustained consecutive failures, alerting the org admin.
  - **Setup Hub UI (`/dashboard/admin/developer/*`):**
    - Add `"Developer & Integrations"` section in `adminNav.constants.ts` -> **Private Apps & API Keys**, **Webhooks**, and **Delivery Logs** (with one-click **"Send Test Event"** and **"Replay Delivery"**).

---

### Phase 2 — Public OAuth 2.0 Apps & External Developer Console

**Goal:** Enable third-party SaaS builders (including Crusource's own upcoming connectors like Google Ads closed-loop revenue attribution) to build one app that any customer org can install with a 1-click consent flow.

#### 5.4 Developer Portal & Public App Registry
- **Data Model:**
  - `developer_accounts`: `id`, `owner_email` / linked user identity, `organization_name`, `website_url`, `status`.
  - `developer_apps`: `id`, `developer_account_id`, `name`, `slug`, `client_id`, `client_secret_hash` (PBKDF2/Argon2 or SHA-256 + high-entropy prefix), `redirect_uris` (`TEXT[]`), `requested_scopes` (`TEXT[]`), `webhook_url`, `webhook_secret_encrypted`, `distribution_status` (`sandbox_only` | `in_review` | `published` | `suspended`), `max_sandbox_installs`.
  - `oauth_authorization_codes`: `code_hash`, `app_id`, `org_id`, `user_id`, `redirect_uri`, `granted_scopes`, `code_challenge`, `code_challenge_method` (`S256`), `expires_at` (60s–120s), `consumed_at`.
  - `app_installations`: `id`, `app_id`, `org_id`, `installed_by_user_id`, `granted_scopes`, `status` (`active` | `revoked`), `created_at`, `revoked_at`.
  - `oauth_tokens`: `id`, `installation_id`, `access_token_hash` (short-lived JWT or opaque token), `refresh_token_hash` (rotating on each use, reuse-detection revokes token family), `expires_at`.

#### 5.5 OAuth 2.0 Authorization Flow & Admin Separation (Salesforce ECA Pattern)
- **Authorization Code + PKCE (`S256` mandatory for public/SPA apps, strongly recommended for confidential backends):**
  - `GET /api/v1/oauth/authorize` redirects logged-in org admins (`require_manage_org()`) to a consent screen inside `crusource-crm-frontend` (`/oauth/consent`) listing the app's publisher verification badge, exact requested scopes, and target CRM organization.
  - Strictly enforce **exact redirect URI matching** (no wildcards; HTTPS required outside loopback dev URLs).
- **Org Admin Governance:**
  - Org admins view all active third-party apps under `/dashboard/admin/developer/connected-apps` and can revoke an `app_installation` in one click, immediately invalidating all access/refresh tokens and pausing app webhooks for that org without touching other customers.
- **Sandbox Developer Orgs:**
  - Allow registered developers in the Developer Portal to spin up 1–2 capped **Developer Sandbox Orgs** (using `organization` onboarding + `sample_data` seeding) pre-marked as non-billable sandbox workspaces so testing never requires paid seats or touches live client data.

#### 5.6 Multi-Tenant Webhook Fan-Out
- Extend the Phase 1 outbox dispatcher: when CRM event `E` commits for `org_id`:
  1. Deliver to matching active org `webhook_subscriptions`.
  2. Deliver to active global `developer_apps` installed on `org_id` (`app_installations.status = 'active'`) that requested event `E`, embedding `"org_id"` and `"installation_id"` in the signed envelope so partner backends route events safely per tenant.

---

### Phase 3 — Marketplace Directory, Super Admin Review & CRM Cards

1. **Super Admin Governance in `crusource-admin/` & `crusource-vms-backend/` (`admin-crm`):**
   - Route `/crm/developer-apps` (or `/crm/marketplace`) gated by Super Admin permission to inspect Public App submissions, verify privacy policy / scope minimization / webhook SSRF safety, and transition apps between `sandbox_only` (capped e.g. 5–10 installs), `published`, and `suspended`.
   - Display per-app API request volume, `429`/`5xx` error rates, webhook failure rates, and active org installs.
2. **Public Integrations Marketplace (`crusource-website/` + in-app CRM directory):**
   - Upgrade static integration listings into a dynamic directory of verified apps with **"Install in Crusource CRM"** OAuth launch links.
3. **Structured JSON CRM Cards (UI Extensibility):**
   - Allow approved Public Apps to register a sidebar data URL for `Lead`, `Contact`, `Account`, or `Deal` detail views.
   - `crusource-crm-backend` fetches a signed JSON schema card (title, key-value properties, status badge, external link/action button) from the partner app with strict timeouts (`<= 2s`) and renders native CRM UI components — providing HubSpot CRM Card ergonomics without third-party XSS risks.

---

## 6. Security & Threat Checklist

| Threat | Mitigation Required Before Launch |
| --- | --- |
| **Cross-tenant data access** | Derive `org_id` solely from validated API key / OAuth installation token (`app_installations.status = 'active'`), never from query/body parameters; pass through existing `Scope` filters. |
| **Token/Secret leakage in DB or logs** | Hash API keys, OAuth authorization codes, and refresh tokens (`SHA-256` / rotation + reuse revocation); encrypt webhook signing secrets using `EncryptedProviderToken`; scrub `Authorization` headers in structured logger. |
| **SSRF via Webhook URLs** | Validate URLs on save **and** re-validate resolved IP immediately before outbound connect (preventing DNS rebinding), block private/loopback/cloud-metadata IPs, disable HTTP redirects. |
| **Webhook spoofing & replay** | Sign raw JSON body + timestamp with HMAC-SHA256 (`X-Crusource-Signature`, `X-Crusource-Timestamp`, `X-Crusource-Event-Id`) and publish official verification snippets (Python/Node/Go). |
| **Open Redirect / CSRF in OAuth** | Exact URI match validation on `redirect_uri`; mandatory `state` parameter; mandatory PKCE `S256` challenge; verify user `manage_org` permission on consent approval. |
| **Noisy-neighbor / DoS bursts** | Separate Redis sliding-window rate limits per API key and per `client_id + org_id` installation so partner traffic spikes do not degrade interactive CRM UI latency. |
| **Unverified app abuse** | Cap unreviewed Public Apps (`sandbox_only`) to limited test org installs and require Super Admin review in `crusource-admin/` before public distribution. |

---

## 7. Summary Verification & Next Decision Gate

- **Verification:** Research verified against HubSpot and Salesforce platform documentation and inspected against current `crusource-crm-backend`, `crusource-crm-frontend`, and `crusource-admin`/`crusource-vms-backend` boundaries. No application source files were modified; all existing `crusource-crm-docs` conventions were preserved.
- **Recommended First Execution Slice:** Start with a dedicated implementation plan for **Phase 1 (Private Apps, Scoped API Keys, `/api/v1/public/*` starter endpoints for Leads/Contacts/Deals, and Transactional Outbound Webhooks + Logs UI)** in `crusource-crm-backend` and `crusource-crm-frontend`.
