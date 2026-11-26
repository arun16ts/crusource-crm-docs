# Vercel Analytics, Mixpanel Telemetry & Super Admin CRM Dashboard Implementation Plan

- **Date:** 25 November 2026
- **Status:** PROPOSED IMPLEMENTATION PLAN (Source-Verified Against Latest Codebase; Audited in Section 7)
- **Target Repositories:**
  - `crusource-crm-frontend/` (Next.js App Router — public landing + authenticated CRM workspace telemetry)
  - `crusource-crm-backend/` (FastAPI — authoritative server-side Mixpanel completion events & internal CRM stats)
  - `crusource-vms-backend/` (NestJS/Fastify + Drizzle/PostgreSQL — Central Super Admin backend, analytics reporting adapters, DB snapshot cache, RBAC)
  - `crusource-admin/` (Nx/Next.js `apps/superadmin` — Central Super Admin CRM dashboard & `/crm/analytics` reporting UI)
  - `crusource-crm-docs/` (Documentation registry only)
- **Applies Skills:** `analytics`, `code-security`, `api-security`, `threat-modeling`, `verification-before-completion`
- **Supersedes (on Analytics / Super Admin Reporting Ownership):**
  - [`../superadmin/superadmin_upgrade_plan.md`](../superadmin/superadmin_upgrade_plan.md) (authored Oct 2026 before built-in CRM `/superadmin/**` was retired into `crusource-admin/` + `crusource-vms-backend/`)
  - [`../public-pages/public_analytics_setup.md`](../public-pages/public_analytics_setup.md) (stale baseline claim that `@vercel/analytics` and `mixpanel-browser` were uninstalled)
- **Companion Documents:**
  - [`../superadmin/BUILT_IN_SUPERADMIN_RETIREMENT_PLAN.md`](../superadmin/BUILT_IN_SUPERADMIN_RETIREMENT_PLAN.md)
  - [`../billing/SUPERADMIN_BILLING_AI_CREDITS_AND_STORAGE_IMPLEMENTATION_PLAN.md`](../billing/SUPERADMIN_BILLING_AI_CREDITS_AND_STORAGE_IMPLEMENTATION_PLAN.md)
  - [`../public-pages/landing_public_pages_upgrade_plan.md`](../public-pages/landing_public_pages_upgrade_plan.md)
  - [`../public-pages/landing_public_pages_implementation_report.md`](../public-pages/landing_public_pages_implementation_report.md)

---

## 1. Executive Summary & Reconciled Architecture

Earlier plans in `crusource-crm-docs/` targeted the now-retired built-in `/superadmin/**` UI inside `crusource-crm-frontend` and a Python `platform_observability` module inside `crusource-crm-backend`. Inspection of the latest codebase confirms that architectural split has already happened:

1. **Built-in CRM Super Admin is retired:** `crusource-crm-frontend/src/app/superadmin` and `src/components/superadmin` no longer exist.
2. **Central Super Admin Frontend is `crusource-admin/`:** Hosted at `apps/superadmin`, with CRM domain code under `libs/domains/crm/src/`.
3. **Designated Central Super Admin Backend is `crusource-vms-backend/`:** CRM endpoints live in `src/modules/admin-crm/` and fetch live CRM operational data from `crusource-crm-backend/src/modules/superadmin/routes/internal_organization_routes.py` (`/api/v1/internal/admin/crm/*`) using short-lived RS256 service delegation JWTs (`crm-admin-delegation+jwt`).
4. **Public marketing analytics in `crusource-crm-frontend` ALREADY EXISTS (partially):** `@vercel/analytics` (`^2.0.1`) and `mixpanel-browser` (`^2.83.0`) are installed and wired for opt-in consent on public routes via `PublicAnalyticsProvider` and `publicAnalyticsService.ts`, verified offline by `tests/test_public_analytics_browser.mjs`. However, it contains several route/locale/UI/CSP/funnel bugs, and **authenticated CRM product tracking, server-side Mixpanel ingestion, backend reporting adapters, and live Super Admin analytics UI do not yet exist**.

### Target End-to-End Data Flow

```text
+-----------------------------------------------------------------------------+
| 1. crusource-crm-frontend (Next.js App Router)                              |
|  - Public Routes (opt-in consent): Vercel <Analytics /> + Mixpanel          |
|    ("publicMarketing" instance) + demo/enquiry funnel events                |
|  - Authenticated /dashboard/** (workspace session): Vercel <Analytics />    |
|    + Mixpanel ("crmProduct" instance) w/ opaque user_id/org_id + reset()    |
+------------------------------------+----------------------------------------+
                                     |
          +--------------------------+--------------------------+
          v                                                     v
+------------------------+                         +-------------------------+
| Vercel Web Analytics   |                         | Mixpanel Project (EU/US)  |
| (Pageviews, Visitors,  |                         | (Marketing Funnels +    |
|  Web Routes, Devices)  | <----+           +----> |  Authenticated Product  |
+------------------------+      |           |      |  Usage + Server Events) |
                                |           |      +------------+------------+
                                |           |                   ^
                                |           |                   |
+-------------------------------+-----------+-------------------+-------------+
| 2. crusource-crm-backend (FastAPI + httpx)                                  |
|  - Non-blocking Mixpanel /import API emitter for authoritative milestones:  |
|    org signup, demo/enquiry intake, trial extension req/approve/reject,     |
|    deal closed-won, bulk import completed, AI credit/report usage           |
|  - Fixes internal dashboard stats (real growth deltas, real period buckets) |
+-----------------------------------+-----------------------------------------+
                                    | Internal RS256 Delegation JWT
                                    v
+-----------------------------------------------------------------------------+
| 3. crusource-vms-backend (NestJS/Fastify + PostgreSQL/Drizzle)              |
|  - Note: No Redis client exists in crusource-vms-backend; caching uses a    |
|    Drizzle table `admin_analytics_snapshots` + in-process singleflight!     |
|  - VercelAnalyticsAdapter -> GET /v1/query/web-analytics/{visits,events}/*  |
|  - MixpanelQueryAdapter   -> /api/2.0/segmentation & /api/query/insights    |
|    (respecting 60 queries/hour, max 5 concurrent project rate limit)        |
|  - CRM Admin Endpoints: GET /api/v1/admin/crm/analytics/overview,           |
|    /funnels, /adoption, /health (gated by crm.analytics.read)               |
+-----------------------------------+-----------------------------------------+
                                    | Authenticated Super Admin Session
                                    v
+-----------------------------------------------------------------------------+
| 4. crusource-admin (Nx/Next.js apps/superadmin)                             |
|  - /crm (Dashboard): Live KPIs, real period deltas on CrmOrgGrowthChart,    |
|    no hardcoded '+15.0%', no fake math fallback when data is empty          |
|  - /crm/analytics (New Section): Web Traffic (Vercel), Conversion Funnels,  |
|    Feature Adoption, Active Tenants/DAU/WAU, Integration Sync Health        |
+-----------------------------------------------------------------------------+
```

---

## 2. Current-State Codebase Audit & Verified Bug Inventory

Every item below was directly observed in the current repositories and MUST be fixed as part of this implementation.

### Bug 1 — Public Route Allowlist Drops Localized Subpaths & Demo/Enquiry Pages
- **Observed Code:** `crusource-crm-frontend/src/lib/marketing/publicAnalyticsPolicy.ts` lines 6–21 builds a flat `Set` containing `"/"`, `"/en"`, `"/nl"`, `"/ar"`, `"/docs"`, `"/faq"`, `"/integrations"`, `"/privacy"`, `"/terms"`, `"/security"`, `"/contact"`, plus `/docs/<id>` and `/integrations/<id>`.
- **Defect:**
  1. Missing `/request-demo` and `/enquiry` (which exist in localized/public marketing navigation).
  2. Missing locale prefixes for subpaths (`/nl/docs`, `/ar/faq`, `/nl/integrations/...`, `/ar/request-demo`, `/nl/enquiry`, etc.). Visiting any non-English public subpage silently suppresses all public Vercel Analytics and Mixpanel events.
- **Required Fix:** Normalize the pathname in `isAllowedPublicAnalyticsRoute(pathname)` by stripping any leading `/en`, `/nl`, or `/ar` prefix via `PUBLIC_PREFIXED_ROOTS` (from `src/lib/marketing/publicNavigation.ts`) before matching against canonical public route roots and dynamic `/docs/[slug]` + `/integrations/[id]` prefixes, and include `/request-demo` and `/enquiry`.

### Bug 2 — Arabic (`"ar"`) Locale Silently Coerced to `"en"` in Public AI Chat Telemetry
- **Observed Code:**
  - `crusource-crm-frontend/src/hooks/ai/usePublicAIChat.ts` line 57: `locale: locale === "nl" ? "nl" : "en"`
  - `crusource-crm-frontend/src/hooks/ai/usePublicAIChatStream.ts` line 116: `locale: locale === "nl" ? "nl" : "en"`
  - By contrast, `crusource-crm-frontend/src/components/landing/PublicFAQ.tsx` already uses `publicLocale(useLocale())`.
- **Defect:** Arabic visitors asking public AI chat questions are misattributed to English (`"en"`) in Mixpanel.
- **Required Fix:** Replace ternary coercion in both hooks with `publicLocale(locale)` imported from `src/lib/marketing/publicAnalyticsPolicy.ts` (ensuring `publicLocale` preserves `"en" | "nl" | "ar"`).

### Bug 3 — Floating Analytics Banner Placement, Missing Debug CSP & Missing Funnel Conversion Events
- **Observed Code:**
  - `crusource-crm-frontend/src/components/providers/PublicAnalyticsProvider.tsx` places a persistent floating `"Analytics preferences"` button at `bottom-2 start-2 z-40`.
  - `crusource-crm-frontend/src/proxy.ts` lines 14–20 sets `script-src 'self' 'nonce-${nonce}' https://accounts.google.com${isDevelopment ? " 'unsafe-eval'" : ""}`. Meanwhile `@vercel/analytics/dist/react/index.mjs` dynamically loads `/_vercel/insights/script.js` in production and `https://va.vercel-scripts.com/v1/script.debug.js` in development.
  - `crusource-crm-frontend/src/components/demo-requests/GyanDemoForm.tsx` and `src/components/enquiries/EnquiryForm.tsx` emit no analytics events on submission success/failure.
- **Defect:**
  1. In development/staging previews, CSP blocks `va.vercel-scripts.com` unless allowlisted or nonce-tagged.
  2. The persistent floating button at `bottom-2 start-2` overlaps footer links/mobile navigation controls; consent management belongs in a subtle Footer link/trigger plus first-visit non-blocking banner.
  3. Conversion events (`demo_form_submitted`, `enquiry_form_submitted`) are absent, leaving top-of-funnel conversion rates unmeasurable.
- **Required Fix:**
  1. Allow `https://va.vercel-scripts.com` in `proxy.ts` `script-src` when `isDevelopment` is true (and pass CSP `nonce` attribute when supported or verify `/_vercel/insights/script.js` executes under `'self'`). Ensure Mixpanel API ingestion hosts (`https://api.mixpanel.com`, `https://api-eu.mixpanel.com`) and Vercel vitals endpoints are permitted in `connect-src`.
  2. Move the `"Analytics preferences"` reopen trigger into the public Footer (preserving the first-visit consent banner until a decision is stored under `PUBLIC_ANALYTICS_CONSENT_KEY`).
  3. Instrument `GyanDemoForm.tsx` and `EnquiryForm.tsx` **strictly without PII** (never send `email`, `phone`, `fullName`, `description`, `companyName`; send only `product_interest`, `company_size_bucket`, `locale`, `source`, and a non-PII `submission_status`).

### Bug 4 — Zero Authenticated CRM Product Tracking & Lifecycle Reset
- **Observed Code:**
  - `crusource-crm-frontend/src/components/layout/DashboardClientLayout.tsx`, `src/hooks/useWorkspaceBootstrap.ts`, `src/lib/sessionIdentity.ts`, and `src/lib/auth.utils.ts` (`performLogout`) have zero Vercel Analytics or Mixpanel integration.
  - `crusource-crm-backend` has zero Mixpanel `/import` ingestion emitters.
- **Defect:** Product adoption, active tenant count (DAU/WAU/MAU), AI credit usage funnel, and feature usage per module cannot be tracked or shown in Super Admin.
- **Required Fix:** Build `crmAnalyticsService.ts` + `CrmAnalyticsProvider.tsx` scoped to `/dashboard/**`, keyed by opaque IDs from `sessionIdentity()` / `useWorkspaceBootstrap.ts` (`distinct_id = opaque user HMAC/UUID`, `org_id = opaque org ID`), calling `mixpanel.reset()` inside `performLogout()` (`src/lib/auth.utils.ts`) and on session mismatch, paired with server-side Mixpanel `/import` emission in `crusource-crm-backend`.

### Bug 5 — `CrmOrgGrowthChart` Hardcodes `+15.0%`, Ignores Period Toggle on Live Data & Falls Back to Fake Numbers
- **Observed Code:** `crusource-admin/libs/domains/crm/src/dashboard/components/CrmOrgGrowthChart.tsx` lines 45–62:
  - When `apiGrowth && apiGrowth.length > 0`, returns hardcoded `growthRate: '+15.0%'` and does not slice/bucket by `activePeriod` (`7` / `30` / `90` days) if the API returns a fixed window.
  - When `apiGrowth` is empty (e.g., new environment or 0 signups in window), falls back to `getGrowthData(effectiveDate, totalOrgs, activePeriod)` in `data/crm-dashboard-data.ts`, which fabricates synthetic counts (`Math.round(totalOrgs * 0.3)` etc.).
- **Defect:** Super Admin operators see fabricated percentages (`+15.0%`) and synthetic curves presented as real production telemetry.
- **Required Fix:**
  1. Update backend `GET /api/v1/admin/crm/dashboard` (and internal CRM endpoint) to accept `days=7|30|90` (strict UTC closed windows `[start_utc, end_utc)`) and return prior-period baseline counts so `growthRatePct` is computed accurately (or `null` / `"New"` when previous baseline is `0`).
  2. Delete synthetic fallback math (`getGrowthData` fake ratios) in `CrmOrgGrowthChart.tsx` and render a clean empty state ("No new organizations in selected UTC window") when `data.every(v => v === 0)`.

### Bug 6 — Static Hardcoded Zeroes & Fake Subtitles in `CrmMetricsSummaryBar` & `CrmDashboardHandler`
- **Observed Code:**
  - `crusource-vms-backend/src/modules/admin-crm/application/queries/dashboard.handler.ts` sets `revenue: null` and does not expose prior-period deltas for organizations, members, demos, or enquiries.
  - `crusource-admin/libs/domains/crm/src/dashboard/components/CrmMetricsSummaryBar.tsx` and `data/crm-dashboard-data.ts` display `'0'` or static fallback strings (`'0 today'`, `'0 this month'`).
- **Defect:** Top KPI cards fail to answer operational questions (weekly active tenants, web traffic-to-demo conversion, product adoption, real trend comparisons).
- **Required Fix:** Replace hardcoded `"0 today"`/`"0 this month"` placeholders with backend-computed UTC period deltas and integrate external Vercel Analytics + Mixpanel KPI cards cleanly alongside internal operational metrics, showing `"Not configured"` / `"Unavailable"` badges rather than `'0'` when external providers are disabled or degraded.

### Bug 7 — Missing Analytics RBAC Permission in `admin-crm`
- **Observed Code:** `crusource-vms-backend/src/modules/admin-crm/domain/crm-permissions.ts` and `presentation/crm-admin.guard.ts` lines 40–53 explicitly allowlist exact permission strings (`CRM_READ`, `CRM_EXPORT`, `CRM_MEMBERS_READ`, `CRM_AUDIT_READ`, `CRM_FEEDBACK_READ`, `CRM_BILLING_READ`, `CRM_TRIAL_EXTEND`, `CRM_ORG_UPDATE`, `CRM_ORG_DEACTIVATE`).
- **Defect:** Adding analytics routes without registering a dedicated permission either leaves telemetry unguarded or triggers `ForbiddenException` in `CrmAdminGuard`.
- **Required Fix:** Add `CRM_ANALYTICS_READ = 'crm.analytics.read'` to `crm-permissions.ts`, add it to `CrmAdminGuard` allowlist and RBAC role seeders, and gate all `/api/v1/admin/crm/analytics/*` routes with `@RequireCrmPermission(CRM_ANALYTICS_READ)`.

---

## 3. Privacy, Security & Data Governance Model

Applying `analytics`, `code-security`, `api-security`, and `threat-modeling` skills establishes non-negotiable boundaries:

### 3.1 Strict Zero-PII & URL/Param Redaction Rules
- **Banned Properties (Client & Server Scrubbing Hook):** Both Mixpanel (`before_send_events`) and Vercel Analytics (`beforeSend`) MUST strip or block any property key matching `email`, `phone`, `name`, `full_name`, `address`, `token`, `password`, `secret`, `query`, `search`, `message`, `description`, `notes`, `lead_name`, `contact_name`, `deal_name`, `subject`, `body`, `authorization`.
- **URL Sanitization:** Strip query strings (`?email=`, `?token=`, `?code=`, `?q=`), hash fragments (`#...`), and raw database UUID/slug detail paths where customer-identifying names might appear:
  - Example normalized route template in Vercel `beforeSend` and Mixpanel `$current_url`: `/dashboard/leads/[id]`, `/dashboard/deals/[id]`, `/dashboard/accounts/[id]`.
- **Opaque Identifiers Only:**
  - `distinct_id`: HMAC-SHA256 (or Mixpanel project-scoped opaque user UUID from `sessionIdentity()`/`user_id`) — NEVER email, username, or raw domain.
  - `org_id` Group / Super-Property: Opaque CRM organization UUID (`ORG-...` code or internal UUID hash), never `company_name`.
  - Mixpanel UI/People profiles: Do **not** call `mixpanel.people.set({ $email, $name })`. Set only non-PII tenant metadata (`plan_tier`, `locale`, `role_category`, `region`, `trial_status`).

### 3.2 Consent & Session Separation (`publicMarketing` vs `crmProduct`)
- Keep two separate Mixpanel instances in `crusource-crm-frontend`:
  1. `publicMarketing` (public marketing pages only): **Strictly opt-in** via `PUBLIC_ANALYTICS_CONSENT_KEY`, disabled by default until user clicks `"Allow"`. Calls `mixpanel.opt_out_tracking()` + `reset()` on decline/revoke.
  2. `crmProduct` (authenticated `/dashboard/**` only): Subject to workspace contractual telemetry policy / opt-out toggle in workspace settings, initialized only when `NEXT_PUBLIC_CRM_PRODUCT_ANALYTICS_ENABLED === "true"` and an authenticated session is established in `DashboardClientLayout`. Never leaks `publicMarketing` anonymous state into another tenant on the same shared browser: `performLogout()` in `src/lib/auth.utils.ts` MUST synchronously call `resetCrmAnalyticsSession()` (`mixpanel.reset()`) BEFORE redirecting to `/login`, and `DashboardSessionBoundary` MUST compare current `user_id`/`org_id` with the active analytics identity and call `reset()` on mismatch.

### 3.3 Server-Side Credentials & Upstream API Constraints
- **Secrets Stay in `crusource-vms-backend` & `crusource-crm-backend` ONLY:**
  - Never expose `VERCEL_API_TOKEN`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`, or `MIXPANEL_PROJECT_SECRET` via `NEXT_PUBLIC_*` env vars.
- **Verified External API Specifications & Quotas:**
  1. **Vercel Web Analytics Query API** (available on Vercel **Pro** / **Enterprise** plans; 1-month window on Pro, 12 months with Web Analytics Plus, 24 months on Enterprise):
     - Base URL: `https://api.vercel.com/v1/query/web-analytics/`
     - Endpoints: `GET /visits/count`, `GET /visits/aggregate`, `GET /events/count`, `GET /events/aggregate`
     - Query params: `projectId` (`VERCEL_CRM_PROJECT_ID`), optional `teamId` (`VERCEL_TEAM_ID`), `since`, `until`, `by` (e.g. `day`, `requestPath`, `country`, `deviceType`), optional `filter`.
     - Auth: `Authorization: Bearer <VERCEL_API_TOKEN>` (read-only scoped team/project token).
     - **Degraded/Hobby fallback rule:** If Vercel returns `402`/`403` (plan limit) or token is unconfigured, record snapshot state `status: 'plan_restricted' | 'not_configured'` and surface a clear status badge in `crusource-admin` instead of showing `0` or throwing 500s.
  2. **Mixpanel Query API** (Service Account Basic Auth, EU `https://eu.mixpanel.com/api/...` or US `https://mixpanel.com/api/...` configurable via `MIXPANEL_API_HOST`):
     - **Strict Rate Limit:** **60 queries/hour per Mixpanel project, max 5 concurrent queries** (HTTP `429` if exceeded).
     - **Critical API Constraint (Verified against Mixpanel Docs):**
       - `/api/query/insights` ONLY accepts `project_id`, `workspace_id`, and `bookmark_id` (executes saved Insights reports; **does NOT accept dynamic `from_date`/`to_date` filters**).
       - `/api/2.0/segmentation` (maintenance mode but currently active) and `/api/2.0/funnels` / `/api/2.0/retention` accept dynamic `from_date`, `to_date`, `unit`, `type`, `on`, and `where`.
     - **Design Choice:** Use **saved Insights `bookmark_id` env mapping** for complex curated executive reports (weekly funnel / cohort retention), AND `/api/2.0/segmentation` for dynamic `7d / 30d / 90d` single-event time series (`crm_dashboard_viewed`, `deal_stage_updated`, `ai_chat_completed`), strictly bounded behind our database snapshot cache so Mixpanel receives **at most ~6–12 requests/hour**, never exceeding 60 req/hr even with multiple Super Admin operators clicking refresh.

### 3.4 PostgreSQL Snapshot Cache (Replaces Assumed Redis in `crusource-vms-backend`)
- **Verified Fact:** `crusource-vms-backend/package.json` and `src/libs/infrastructure/infrastructure.module.ts` contain **no Redis dependency or cache service** (only PostgreSQL/Drizzle, SQS, S3, SES).
- **Architecture:** Create a Drizzle table `admin_analytics_snapshots` (in `src/libs/infrastructure/database/schema/`) keyed uniquely by `(provider, metric_key, window_days, environment)` with columns:
  - `id`, `provider` (`'vercel' | 'mixpanel' | 'crm_internal'`), `metric_key`, `window_days`, `environment`, `window_start_utc`, `window_end_utc`, `payload_json` (`jsonb`), `status` (`'ok' | 'stale' | 'not_configured' | 'rate_limited' | 'error'`), `error_code`, `fetched_at`, `expires_at`.
- **Singleflight & Stale-While-Error Policy:**
  - Cache TTL: `15 minutes` (900s) for `7d/30d` windows, `60 minutes` for `90d` windows.
  - Manual `"Refresh Analytics"` button in `crusource-admin` enforces a per-metric cooldown of `5 minutes` (unless `status === 'error'`) and uses an in-memory `Map<string, Promise<Snapshot>>` singleflight lock so 10 concurrent admins trigger only 1 upstream call.
  - On upstream `429` or `5xx` timeout (`>= 5s` abort signal), serve the last valid `payload_json` marked `status: 'stale'` with `fetched_at` timestamp so Super Admin dashboards stay responsive.

### 3.5 Closed UTC Window Alignment (`analytics` Skill Rule)
- Every rate metric (Conversion Rate = Demo Requests / Unique Public Landing Visitors; Trial-to-Active Org Rate; Deal Win Rate) MUST divide counts from **identical closed UTC day boundaries**: `window_start_utc` (`00:00:00Z`) through `yesterday 23:59:59Z` (excluding today's partial UTC day for rate denominators, or clearly labeling `"Today (partial UTC)"` on live counters without computing period-over-period % rates against partial days).

---

## 4. Event Dictionary & Authoritative Emitter Matrix

Follow `snake_case` **Object-Action** naming (`<object>_<past_tense_action>`). Each event has ONE authoritative emitter (never emit the same milestone from both frontend and backend without `$insert_id` deduplication).

### 4.1 Public Marketing Funnel (`crusource-crm-frontend` -> Vercel + Mixpanel `"publicMarketing"`)
| Event Name | Status | Trigger Location | Authoritative Properties (Zero-PII) | Notes |
| --- | --- | --- | --- | --- |
| `public_page_viewed` | **Existing** | `PublicAnalyticsProvider.tsx` route transition | `path`, `locale`, `environment` | Fix Bug 1 for `/request-demo`, `/enquiry`, and `/nl/*` & `/ar/*` subpaths |
| `faq_answered` | **Existing** | `PublicFAQ.tsx`, `usePublicAIChat.ts`, `usePublicAIChatStream.ts` | `path`, `locale`, `faq_id`, `surface` | Fix Bug 2 (`publicLocale()` preserving `"ar"`) |
| `public_ai_answer_viewed` | **Existing** | Public AI FAQ answer component | `path`, `locale`, `faq_id` | Already scrubbed by `publicAnalyticsService.ts` |
| `public_cta_clicked` | **New (allowlist)** | Landing CTAs (`DemoLink.tsx`, hero/pricing buttons) | `path`, `locale`, `cta_id`, `target_route` | Must be added to `publicAnalyticsPolicy.ts` allowlist |
| `demo_form_submitted` | **New (allowlist)** | `GyanDemoForm.tsx` on submit success/error | `locale`, `product_interests` (array), `company_size_bucket`, `outcome` (`success` \| `validation_error` \| `rate_limited`) | Zero PII |
| `enquiry_form_submitted` | **New (allowlist)** | `EnquiryForm.tsx` on submit success/error | `locale`, `topic_tags` (array), `company_size_bucket`, `outcome` | Zero PII |

### 4.2 Authenticated CRM Product Events (`crusource-crm-frontend` -> Vercel + Mixpanel `"crmProduct"`)
Every authenticated event auto-attaches Super Properties: `app: "crm"`, `org_id` (opaque), `user_role_category`, `plan_tier` (`trial` \| `paid` \| `unknown`), `locale`, `release_env`.

| Event Name | Trigger Location | Authoritative Properties (Zero-PII) |
| --- | --- | --- |
| `crm_session_started` | `DashboardClientLayout.tsx` (once per browser session after bootstrap) | `locale`, `plan_tier`, `trial_days_remaining_bucket` |
| `crm_module_viewed` | Route listener inside `DashboardClientLayout.tsx` | `route_template` (e.g., `/dashboard/leads`), `module` (`leads` \| `deals` \| `contacts` \| `reports` \| `analytics` \| `ai` \| `billing`) |
| `crm_ai_assistant_invoked` | Authenticated AI chat / scoring / summary actions | `feature` (`chat_copilot` \| `lead_scoring` \| `email_draft`), `outcome` (`completed` \| `quota_exceeded` \| `error`) |
| `crm_bulk_import_initiated` | Import wizard confirm click | `entity_type` (`leads` \| `contacts` \| `accounts`), `row_count_bucket` (`1-50` \| `51-500` \| `500+`) |
| `crm_report_exported` | Reports export trigger | `export_format` (`csv` \| `xlsx` \| `pdf`), `report_type` |

### 4.3 Authoritative Backend Milestones (`crusource-crm-backend` -> Mixpanel `/import` HTTP API)
Server-side events use `httpx.AsyncClient` against Mixpanel `/import` API (`strict=1`, `compression=gzip`, deterministic `$insert_id = sha256(f"{event}:{entity_id}:{iso_minute}")` to prevent duplicates on retries, timeout `2.0s`, fire-and-forget background task so CRM API latency is never impacted).

| Event Name | Trigger Location in `crusource-crm-backend` | Properties (`distinct_id` / `org_id` opaque only) |
| --- | --- | --- |
| `org_created` | Organization onboarding completion handler | `org_id`, `plan_tier: "trial"`, `signup_source` |
| `demo_request_recorded` | Public demo request intake handler | `org_id: "public"`, `reference_id`, `product_tags`, `company_size_bucket`, `source` |
| `enquiry_recorded` | Public enquiry intake handler | `org_id: "public"`, `reference_id`, `topic_tags`, `company_size_bucket` |
| `trial_extension_requested` | Billing trial extension request handler | `org_id`, `requested_days`, `current_remaining_bucket` |
| `trial_extension_decided` | Internal superadmin approve/reject handler | `org_id`, `decision` (`approved` \| `rejected`), `granted_days` |
| `deal_closed_won` | Deals stage transition handler when stage category is Closed Won | `org_id`, `deal_stage`, `currency`, `amount_bucket` |
| `ai_quota_consumed` | AI credit/token debit service (aligns with Billing/AI plan) | `org_id`, `feature_key`, `units_consumed` |

---

## 5. Repo-by-Repo File & Symbol Implementation Plan

### 5.1 `crusource-crm-frontend/`

1. **Fix Public Policy & Locale Telemetry (Bugs 1 & 2):**
   - `src/lib/marketing/publicAnalyticsPolicy.ts`:
     - Refactor `isAllowedPublicAnalyticsRoute(pathname)` to strip `/en`, `/nl`, `/ar` prefixes using `PUBLIC_PREFIXED_ROOTS` from `src/lib/marketing/publicNavigation.ts`, then match canonical routes (`/`, `/docs`, `/docs/*`, `/faq`, `/integrations`, `/integrations/*`, `/privacy`, `/terms`, `/security`, `/contact`, `/request-demo`, `/enquiry`).
     - Ensure `publicLocale(locale)` returns `"en" | "nl" | "ar"` cleanly.
   - `src/hooks/ai/usePublicAIChat.ts` & `src/hooks/ai/usePublicAIChatStream.ts`:
     - Replace `locale === "nl" ? "nl" : "en"` with `publicLocale(locale)`.
2. **Fix Public UI, CSP & Demo/Enquiry Funnels (Bug 3):**
   - `src/proxy.ts`:
     - Update `createCsp(nonce)` so `script-src` allows `https://va.vercel-scripts.com` when `isDevelopment` is true (keeping `'self' 'nonce-${nonce}'` strict in production for `/_vercel/insights/script.js`), and ensure `connect-src` covers Mixpanel ingestion endpoints cleanly.
   - `src/components/providers/PublicAnalyticsProvider.tsx` & `src/components/landing/Footer.tsx`:
     - Keep the first-visit consent banner when `PUBLIC_ANALYTICS_CONSENT_KEY` is unset; replace the overlapping floating `bottom-2 start-2` `"Analytics preferences"` pill with a Footer link/button trigger (`"Analytics preferences"`) in `Footer.tsx` backed by shared UI state/custom DOM event so `PublicAnalyticsProvider` opens the preference bar cleanly. Preserve fallback trigger rendering when `Footer` is absent so standalone harnesses (`tests/test_public_analytics_browser.mjs`) continue passing without regressions.
     - Guard `<Analytics />` rendering in `PublicAnalyticsProvider` so it ONLY mounts `<Analytics />` on allowed public routes (`isAllowedPublicAnalyticsRoute(pathname)` && consent granted). That avoids injecting duplicate `/_vercel/insights/script.js` tags when `CrmAnalyticsProvider` mounts `<Analytics />` inside `/dashboard/**`, and note cleanly that `/_vercel/insights/script.js` only populates when hosted on Vercel (local/Docker non-Vercel builds must degrade silently if `/_vercel/insights/*` returns `404`).
   - `src/components/demo-requests/GyanDemoForm.tsx` & `src/components/enquiries/EnquiryForm.tsx`:
     - Emit `demo_form_submitted` and `enquiry_form_submitted` via `trackPublicEvent` with zero PII (and extend the allowlist in `publicAnalyticsPolicy.ts` / `publicAnalyticsService.ts`).
3. **Add Authenticated CRM Product Analytics (Bug 4):**
   - Create `src/lib/analytics/routeSanitizer.ts`: maps authenticated `/dashboard/...` URLs to parameterized route templates (`/dashboard/leads/[id]`, etc.) and strips all query strings/hashes.
   - Create `src/services/crmAnalyticsService.ts`:
     - Separate Mixpanel instance `mixpanel.init(token, { ... }, "crmProduct")` gated by `NEXT_PUBLIC_CRM_PRODUCT_ANALYTICS_ENABLED === "true"` and `NEXT_PUBLIC_MIXPANEL_CRM_TOKEN`.
     - Zero-PII `before_send_events` scrubber (same forbidden key list + URL redactor).
     - `identifyCrmSession({ userId, orgId, roleCategory, planTier, locale })`, `trackCrmEvent(name, props)`, `resetCrmAnalyticsSession()`.
   - Create `src/components/providers/CrmAnalyticsProvider.tsx` and mount inside `src/components/layout/DashboardClientLayout.tsx`:
     - Reads user/workspace identity from `sessionIdentity()` / `useWorkspaceBootstrap.ts` and `authSlice.ts`.
     - Renders `@vercel/analytics/next` `<Analytics beforeSend={sanitizeVercelEvent} />` cleanly without double-counting route transitions when inside `/dashboard/**`.
     - Calls `resetCrmAnalyticsSession()` if user/org changes unexpectedly.
   - Update `src/lib/auth.utils.ts` inside `performLogout()`:
     - Synchronously call `resetCrmAnalyticsSession()` alongside `resetSessionReads()` before clearing storage and redirecting to `/login`.
   - Add `.env.crm-analytics.example` (never real credentials) documenting `NEXT_PUBLIC_CRM_PRODUCT_ANALYTICS_ENABLED`, `NEXT_PUBLIC_MIXPANEL_CRM_TOKEN`, `NEXT_PUBLIC_MIXPANEL_REGION`.

### 5.2 `crusource-crm-backend/`

1. **Non-Blocking Server-Side Mixpanel Ingestion Client:**
   - Create `src/shared/analytics/mixpanel_client.py`:
     - Async helper backed by `httpx==0.28.1` (already installed in `requirements.txt` — no new package required).
     - Calls Mixpanel `/import?project_id=<MIXPANEL_PROJECT_ID>&strict=1` authenticated with **Mixpanel Service Account HTTP Basic Auth** (`MIXPANEL_SERVICE_ACCOUNT_USERNAME` + `MIXPANEL_SERVICE_ACCOUNT_SECRET`), because legacy Project Secret auth is deprecated by Mixpanel (scheduled retirement March 3, 2027) and unavailable on newer projects.
     - Reads `MIXPANEL_SERVER_INGEST_ENABLED` (default `false`), `MIXPANEL_INGEST_HOST` (`https://api-eu.mixpanel.com` or `https://api.mixpanel.com`), `MIXPANEL_PROJECT_ID`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`.
     - Strips forbidden PII keys recursively, computes deterministic `$insert_id = sha256(f"{event}:{entity_id}:{iso_minute}")`, posts batched JSON events (`Content-Type: application/json`), sets a `2.0s` timeout, and swallows network/HTTP errors gracefully with structured warning logs (`correlation_id`, never secret/payload dump).
2. **Instrument Server-Side Milestones:**
   - Wire background `BackgroundTasks` / `asyncio.create_task` calls into:
     - Organization onboarding completion (`org_created`)
     - Public demo request & enquiry intake endpoints (`demo_request_recorded`, `enquiry_recorded`)
     - Trial extension request + internal superadmin approve/reject handlers (`trial_extension_requested`, `trial_extension_decided`)
     - Deals Closed-Won transition (`deal_closed_won`)
     - AI credit consumption handler (`ai_quota_consumed`)
3. **Fix Internal Dashboard Stats Endpoint (`internal_organization_routes.py`):**
   - Update `GetInternalDashboardHandler` (`src/modules/superadmin/handlers/get_internal_dashboard_handler.py`) and `OrganizationDashboardRepository` (`repositories/organization_dashboard_repository.py`):
     - Accept query param `growth_days: Literal[7, 30, 90] = 30`.
     - Compute exact UTC closed series for `7`, `30`, or `90` days AND return `prior_period_new_orgs`, `new_orgs_current_window`, `growth_rate_pct` (null when prior = 0), and closed-window counts for active workspaces (7d / 30d) so `crusource-vms-backend` does not guess or hardcode `+15.0%`.

### 5.3 `crusource-vms-backend/` (Central Super Admin Backend)

1. **Permissions & Guard Allowlist (Bug 7 Fix):**
   - Update `src/modules/admin-crm/domain/crm-permissions.ts`: add `CRM_ANALYTICS_READ: 'crm.analytics.read'`.
   - Update `src/modules/admin-crm/presentation/crm-admin.guard.ts`: add `CRM_PERMISSIONS.CRM_ANALYTICS_READ` to the explicit allowlist array and assign it to seeded Super Admin roles in `AdminAuthorityRepository`.
2. **Configuration (`src/config/`):**
   - Create `src/config/analytics.config.ts` (`registerAs('analytics', ...)`):
     - `VERCEL_ANALYTICS_API_ENABLED`, `VERCEL_API_TOKEN`, `VERCEL_CRM_PROJECT_ID`, `VERCEL_TEAM_ID`
     - `MIXPANEL_QUERY_API_ENABLED`, `MIXPANEL_API_HOST`, `MIXPANEL_PROJECT_ID`, `MIXPANEL_WORKSPACE_ID`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`, `MIXPANEL_FUNNEL_BOOKMARK_ID`, `MIXPANEL_RETENTION_BOOKMARK_ID`
     - `ANALYTICS_SNAPSHOT_TTL_SECONDS` (default `900`), `ANALYTICS_REFRESH_COOLDOWN_SECONDS` (default `300`)
   - Register `analyticsConfig` in `ConfigModule.forRoot({ load: [...] })` inside `src/apps/api/api.module.ts` (`ApiModule`, which currently loads `appConfig`, `databaseConfig`, `jwtConfig`, `googleConfig`), and keep CRM analytics controllers/services isolated inside `src/modules/admin-crm/` so they never collide with the existing VMS `src/modules/analytics/analytics.module.ts`.
3. **Drizzle Snapshot Cache Schema & Migration (No Redis Assumption):**
   - Create `src/libs/infrastructure/database/schema/admin-analytics-snapshots.schema.ts`:
     - Table `admin_analytics_snapshots`: `id` (uuid pk), `provider` (text), `metric_key` (text), `window_days` (integer), `environment` (text), `window_start_utc` (timestamp with tz), `window_end_utc` (timestamp with tz), `status` (text), `error_code` (text nullable), `payload_json` (jsonb), `fetched_at` (timestamp with tz), `expires_at` (timestamp with tz).
     - Unique index `(provider, metric_key, window_days, environment)`.
   - Re-export from `src/libs/infrastructure/database/schema/index.ts`.
   - Generate migration cleanly with `npm run db:generate` (sequentially following `0095_enquiry_metadata.sql`; never hand-edit Drizzle journal hashes).
4. **Provider Adapters, Singleflight Repository & Use Cases (`src/modules/admin-crm/`):**
   - `infrastructure/analytics-snapshot.repository.ts`: Drizzle read/upsert + in-process `Map<string, Promise<...>>` singleflight + manual refresh cooldown check.
   - `infrastructure/vercel-analytics.client.ts`: calls `https://api.vercel.com/v1/query/web-analytics/visits/count`, `/visits/aggregate` (`by=day`, `by=requestPath`, `by=country`, `by=deviceType`), `/events/count`, with 5s timeout, mapping `401`/`403`/`402`/`429` cleanly without crashing.
   - `infrastructure/mixpanel-query.client.ts`: HTTP Basic Auth client calling `/api/2.0/segmentation` (dynamic UTC dates for `crm_module_viewed`, `crm_session_started`, `demo_form_submitted`, `enquiry_form_submitted`, `deal_closed_won`) and `/api/query/insights` (`bookmark_id` for saved conversion/retention cohorts), honoring 60 req/hr + max 5 concurrent cap via sequential queue + DB snapshot cache.
   - `domain/analytics-contract.ts` & `domain/dashboard-contract.ts`: Extend `CrmDashboardResponse` with `growthSummary` (`currentWindowOrgs`, `priorWindowOrgs`, `growthRatePct`, `averageWeekly`) and explicit `analyticsAvailability`; define typed analytics contracts (`AnalyticsOverviewResponse`, `AnalyticsFunnelsResponse`, `AnalyticsAdoptionResponse`).
   - `application/queries/dashboard.handler.ts`: Pass `days` (`7 | 30 | 90`) through `CrmOrganizationClient` -> `/api/v1/internal/admin/crm/dashboard`, attach Mixpanel/Vercel summary snapshot cards (gracefully degraded if unconfigured).
   - `presentation/analytics.controller.ts` (under `@Controller('admin/crm/analytics')` + `@UseGuards(CrmAdminGuard)` + `@RequireCrmPermission(CRM_PERMISSIONS.CRM_ANALYTICS_READ)`):
     - `GET /overview?days=7|30|90&refresh=false`
     - `GET /funnels?days=7|30|90`
     - `GET /adoption?days=7|30|90`
     - `POST /refresh` (explicit cooldown-protected cache warm)

### 5.4 `crusource-admin/` (Central Super Admin Frontend)

1. **Fix Existing Dashboard Bugs (Bugs 5 & 6):**
   - `libs/domains/crm/src/dashboard/dashboard.types.ts` & `dashboard.api.ts`:
     - Accept `days: 7 | 30 | 90` in `fetchCrmDashboard(days)`.
     - Add typed `growthSummary`, `kpiDeltas`, and optional `telemetrySnapshot` fields.
   - `libs/domains/crm/src/dashboard/components/CrmOrgGrowthChart.tsx`:
     - Remove hardcoded `growthRate: '+15.0%'`; render exact `growthSummary.growthRatePct` (formatted e.g. `+12.4%` or `Baseline: 0` when prior window is 0).
     - Remove fake ratio fallback (`getGrowthData` in `data/crm-dashboard-data.ts`); trigger real `onPeriodChange(days)` refetch and render a crisp empty state when series is all-zero.
   - `libs/domains/crm/src/dashboard/components/CrmMetricsSummaryBar.tsx` & `CrmDashboardScreen.tsx`:
     - Replace hardcoded `'0 today'` / `'0 this month'` trend copy with real closed-window deltas or explicit `"No activity yet"`.
     - Add two telemetry strip cards on `/crm` Dashboard linking to `/crm/analytics`: **Public Web Visitors & Views (Vercel, Closed 7d/30d)** and **Active CRM Workspaces / DAU-WAU (Mixpanel)** with freshness timestamp and `"Not configured"` / `"Stale"` badges when upstream is offline.
2. **Add Dedicated CRM Analytics View (`/crm/analytics`):**
   - Reuse the already-defined `'chart'` (`ChartLineUp`) variant of `AdminIconName` in `libs/ui/admin/src/Icon.tsx` (`crusource-admin/libs/ui/admin/src/Icon.tsx`) and add `{ path: 'analytics', label: 'Analytics', ..., icon: 'chart' }` to `crmSections` in `libs/domains/crm/src/navigation.ts`.
   - Dynamically load `CrmAnalyticsScreen` inside `libs/domains/crm/src/components/CrmSectionScreen.tsx` when `section.path === 'analytics'` (`apps/superadmin/src/app/crm/[...section]/page.tsx` resolves `crmSections` automatically).
   - Create `libs/domains/crm/src/analytics/`:
     - `analytics.types.ts`, `analytics.api.ts`, `useCrmAnalytics.ts`
     - `components/CrmAnalyticsScreen.tsx`:
       1. Window switcher (`7d`, `30d`, `90d` UTC closed windows) + `"Refresh"` button showing last `fetchedAt` and snapshot `status` banner (`live`, `stale`, `not_configured`, `plan_restricted`).
       2. **Acquisition & Web Traffic (Vercel Analytics):** Visits/Pageviews trend chart, Top Public Routes, Country & Device breakdown.
       3. **Marketing-to-CRM Funnel (Mixpanel):** Public Page Viewed -> CTA Clicked -> Demo/Enquiry Submitted -> Trial Org Created -> Trial Activated (`org_created` + `crm_session_started`).
       4. **CRM Feature Adoption & Retention (Mixpanel):** Module usage distribution (`leads`, `deals`, `contacts`, `reports`, `ai`), AI Assistant invocations, Deal Closed-Won server events, Active Workspaces WAU/MAU.

---

## 6. Verification Plan, Rollout Order & Env Checklist

### 6.1 Environment Variables Matrix (Credential-Free Template Keys)
- **`crusource-crm-frontend`**: `NEXT_PUBLIC_PUBLIC_ANALYTICS_ENABLED`, `NEXT_PUBLIC_VERCEL_ANALYTICS_ENABLED`, `NEXT_PUBLIC_MIXPANEL_PUBLIC_TOKEN`, `NEXT_PUBLIC_MIXPANEL_REGION`, `NEXT_PUBLIC_CRM_PRODUCT_ANALYTICS_ENABLED`, `NEXT_PUBLIC_MIXPANEL_CRM_TOKEN`
- **`crusource-crm-backend`**: `MIXPANEL_SERVER_INGEST_ENABLED`, `MIXPANEL_INGEST_HOST`, `MIXPANEL_PROJECT_ID`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`
- **`crusource-vms-backend`**: `VERCEL_ANALYTICS_API_ENABLED`, `VERCEL_API_TOKEN`, `VERCEL_CRM_PROJECT_ID`, `VERCEL_TEAM_ID`, `MIXPANEL_QUERY_API_ENABLED`, `MIXPANEL_API_HOST`, `MIXPANEL_PROJECT_ID`, `MIXPANEL_WORKSPACE_ID`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`, `MIXPANEL_FUNNEL_BOOKMARK_ID`, `MIXPANEL_RETENTION_BOOKMARK_ID`, `ANALYTICS_SNAPSHOT_TTL_SECONDS`, `ANALYTICS_REFRESH_COOLDOWN_SECONDS`

### 6.2 Staged Rollout Sequence
1. **Stage 1 — `crusource-crm-frontend` Public Fixes + Authenticated Instrumentation:** Deploy telemetry with server-disabled flags first, verify CSP + PII scrubbing + logout `reset()` + `tests/test_public_analytics_browser.mjs`.
2. **Stage 2 — `crusource-crm-backend` Mixpanel `/import` + Real Dashboard Growth Window:** Verify zero PII payloads in mocked unit tests and real `growth_days=7|30|90` SQL queries.
3. **Stage 3 — `crusource-vms-backend` Drizzle Snapshot Table, Permissions & Adapters:** Generate & migrate `admin_analytics_snapshots`, verify `CrmAdminGuard` permission tests + mocked Vercel/Mixpanel adapter 429/timeout/singleflight tests.
4. **Stage 4 — `crusource-admin` Dashboard Bug Fixes + `/crm/analytics` UI:** Verify `CrmOrgGrowthChart` real deltas, zero fake fallback numbers, degraded/unconfigured UI states, and end-to-end Playwright inspection on port `3003` (avoiding collision with VMS `apps/admin`).

### 6.3 Required Verification Commands Per Repository
- `crusource-crm-frontend`:
  - `npm.cmd run test:public:analytics` (`node tests/test_public_analytics_browser.mjs` — expand with localized `/nl/docs`, `/ar/faq`, `/request-demo`, `ar` AI chat locale, demo/enquiry funnel zero-PII tests)
  - Add authenticated test `node tests/test_crm_analytics_browser.mjs` verifying route sanitization, forbidden-key scrubbing, and `mixpanel.reset()` on `performLogout()`.
  - `npm.cmd run build` (and project lint/typecheck scripts).
- `crusource-crm-backend`:
  - Python 3.12 venv `pytest` covering `mixpanel_client.py` PII scrubbing / `$insert_id` idempotency / timeout resilience and `GetInternalDashboardHandler` `7/30/90`-day closed UTC windows.
- `crusource-vms-backend`:
  - Node 22: `npm.cmd run db:generate` + migration check on disposable DB, `npx.cmd eslint "{src,test}/**/*.ts"`, unit tests (`npm.cmd test`) covering `CrmAdminGuard`, `AnalyticsSnapshotRepository` singleflight/cooldown, `VercelAnalyticsClient`, and `MixpanelQueryClient`, plus `npm.cmd run build`.
- `crusource-admin`:
  - Node 20.9+: `npm.cmd run lint` and `npm.cmd run build`, plus Playwright verification of `/crm` and `/crm/analytics` in normal, unconfigured, stale-cache, and empty-data states.

---

## 7. Plan Re-Verification & Audit Log

Performed an end-to-end verification pass against actual source trees across `crusource-crm-frontend`, `crusource-crm-backend`, `crusource-vms-backend`, `crusource-admin`, `crusource-crm-docs`, and current Vercel / Mixpanel API requirements. All discrepancies uncovered during audit were corrected directly in Sections 1–6 above:

1. **Mixpanel `/import` Authentication Correction:** Initial draft referenced only `MIXPANEL_CRM_PROJECT_TOKEN` for server ingestion. Re-verification confirmed Mixpanel `/import?project_id=...&strict=1` requires **Service Account HTTP Basic Auth** (`MIXPANEL_PROJECT_ID`, `MIXPANEL_SERVICE_ACCOUNT_USERNAME`, `MIXPANEL_SERVICE_ACCOUNT_SECRET`) because Project Secret auth is deprecated (retirement March 3, 2027). Corrected Section 5.2 and Section 6.1.
2. **Mixpanel Query API Constraints Verified:** Confirmed `/api/query/insights` accepts only `project_id`, `workspace_id`, and `bookmark_id` (no dynamic date params), whereas `/api/2.0/segmentation` accepts dynamic `from_date`/`to_date`, and both share a **60 queries/hour, max 5 concurrent** project-wide rate limit. Plan pairs dynamic segmentation queries with saved Insights `bookmark_id`s behind a PostgreSQL snapshot cache + in-process singleflight lock.
3. **Vercel Web Analytics Query API Verified:** Confirmed exact REST endpoints (`/v1/query/web-analytics/visits/count`, `/visits/aggregate`, `/events/count`, `/events/aggregate`), Pro/Enterprise availability, and explicit `plan_restricted` / `not_configured` handling for Hobby or non-Vercel local/Docker deployments.
4. **`crusource-vms-backend` Infrastructure & Config Path Corrected:** Verified `src/libs/infrastructure/infrastructure.module.ts` and `package.json` have **no Redis client** (replaced assumed Redis cache with Drizzle table `admin_analytics_snapshots` following latest migration `0095_enquiry_metadata.sql`), verified `ConfigModule.forRoot` lives in `src/apps/api/api.module.ts` (`ApiModule`), and separated CRM analytics inside `src/modules/admin-crm/` from the existing VMS `src/modules/analytics/analytics.module.ts`.
5. **Existing Public Event Contract & Browser Test Compatibility Verified:** Inspected `tests/test_public_analytics_browser.mjs` and confirmed the existing allowlisted events are `public_page_viewed`, `faq_answered`, and `public_ai_answer_viewed` (while `public_cta_clicked`, `demo_form_submitted`, and `enquiry_form_submitted` must be added to `publicAnalyticsPolicy.ts` / `publicAnalyticsService.ts`). Also preserved compatibility for the `"Analytics preferences"` button asserted in `test_public_analytics_browser.mjs` when relocating the visible trigger to `Footer.tsx`.
6. **Single Vercel `<Analytics />` Script Guard:** Verified `src/app/layout.tsx` mounts `PublicAnalyticsProvider` globally while `DashboardClientLayout.tsx` wraps `/dashboard/**`; scoped `<Analytics />` inside `PublicAnalyticsProvider` to allowed public routes so adding `<Analytics />` inside `CrmAnalyticsProvider` never injects duplicate scripts.
7. **`crusource-admin` Routes & Icons Verified:** Confirmed `AdminIconName` lives in `crusource-admin/libs/ui/admin/src/Icon.tsx` and already provides `'chart'` (`ChartLineUp`), and confirmed `apps/superadmin/src/app/crm/[...section]/page.tsx` resolves new entries registered in `crmSections` + `CrmSectionScreen.tsx`.
8. **Locale Route Paths Verified:** Confirmed `crusource-crm-frontend/src/app/[locale]/` contains `contact`, `docs`, `enquiry`, `faq`, `integrations`, `privacy`, `request-demo`, `security`, and `terms`, validating Bug 1 root-cause diagnosis.
