# Super Admin master upgrade plan

Date: 9 October 2026  
Status: EXECUTION STARTED — Phase 0 completed locally; later application phases remain planned. See the [Phase 0 review package](superadmin-phase0/README.md).  
Scope: platform staff invitations, the complete Super Admin UI, website demo requests with a sales pipeline board, customer support tickets, and integration of the existing analytics, Error Center and Application Logs roadmap.

Revision: added demo intake/board and customer-submitted support tickets on 9 October 2026. The detailed delivery sequence is in [SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md](SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md).

## 1. Intended result and confirmed scope

Super Admin should feel like another Crusource CRM workspace: the same typography, colors, navigation treatment, workspace frame, controls, tables, dialogs, spacing and interaction conventions. Its data and authorization remain platform-specific.

The user confirmed that invite-only onboarding applies to **Super Admin staff only**. Customer organization membership, organization administrator invitations, public CRM signup and customer authentication are outside this change. The user additionally confirmed that **CRM users submit and track their own support tickets**, with authorized Super Admin staff managing the support queue.

Website visitors will submit demo requests through a real persisted form. Staff will assign and move requests through tracked stages in a Super Admin board. Demo sales enquiries, customer support conversations and automatic Error Center issues are separate features, linked where appropriate.

The target staff journey is:

1. The authorized platform owner opens **Platform Access → Invite staff**.
2. The owner enters the staff member's name and dedicated internal email.
3. The application records the invitation and schedules its activation email.
4. The recipient opens the invitation, sets a password and completes authenticator enrollment.
5. Only successful MFA verification grants access to the platform workspace.
6. Subsequent sign-ins use the staff email, password and authenticator.

Remove the public request-access journey and all developer-login branding. Keep a clearly named **Super Admin sign-in** screen for invited staff and the owner. Removing a developer label must not remove authentication or MFA.

Proposed initial access policy: retain the existing **owner-only** authority to invite, reset and revoke staff. An ordinary platform operator cannot grant access. Delegating staff administration would be a separate, explicit permission decision; it must never be inferred from the word “superadmin.”

This document is the proposed delivery order. [superadmin_upgrade_plan.md](superadmin_upgrade_plan.md) remains the detailed observability reference, subject to the source corrections below. [Superadmin login.md](Superadmin%20login.md) contains the previous onboarding instructions and has pre-existing local edits; this planning task leaves it intact.

No plan can promise zero bugs. The approach here reduces the risk through explicit contracts, additive migration, small releases, negative authorization tests, concurrency tests and staging exit gates.

## 2. Source-checked baseline

Evidence paths in this document are relative to the indicated repository. Implementation claims describe the source inspected on 9 October, not deployed configuration or successful runtime tests.

| Area | Current source behavior | Consequence for this upgrade |
|---|---|---|
| Platform identity | Dedicated users have `auth_provider="platform"`, no organization, platform credentials, sessions and security events | Extend this boundary; do not turn customer accounts into staff accounts |
| Access onboarding | Public request, email OTP, owner review, activation link, password and TOTP enrollment | Replace the entry and invitation lifecycle, preserving proven session/MFA mechanisms |
| Staff administration | Owner-only access page; requests and operators each limited to the latest 200 | Add direct invitations and bounded server pagination/search |
| Activation | Hashed 48-hour activation links; activation consumes the link and issues a 10-minute enrollment session | Retain single-use behavior; explicitly support interrupted enrollment |
| Reset | `ReviewRequestHandler` uses `decision="resend"` both for invitation resend and active-account password/MFA reset | Split resend and reset contracts to prevent an email retry from revoking an active account |
| Email | SES is called inside review handling before the database commit; transport returns a Boolean | Commit invitation and delivery intent together, then dispatch; distinguish acceptance from delivery |
| Authorization | `require_super_admin` depends on the platform session, then checks the flag | A CRM JWT or `is_super_admin` flag alone must remain insufficient |
| Sessions | Separate HttpOnly, host-only, SameSite Strict cookie scoped to `/api/v1/superadmin`; four-hour expiry, 30-minute idle expiry, CSRF and origin checks | Preserve these guarantees throughout UI and API changes |
| UI frame | Super Admin has a fixed 256px sidebar and long page containers; CRM has 236px/64px sidebar modes and an inset workspace surface | Use the CRM presentation structure and scroll ownership |
| Branding/health | “DEV PORTAL,” “Developer Login,” “Developer Controls,” literal ONLINE/CONNECTED and ALL SYSTEMS HEALTHY labels | Replace terminology and remove unmeasured operational claims |
| Page organization | Several route pages contain substantial rendering/state logic and bespoke controls | Thin route entries, focused screens/hooks and shared CRM presentation components |
| View state | Organizations, feedback and login history use local filters; trial extensions use Redux filters and a selected server record snapshot | Move shareable view state to URLs; keep selected IDs rather than duplicated entities |
| Error presentation | Several screens default missing results to zero/empty lists without consuming query errors | Add explicit failed, unavailable, empty, loading and stale states |
| Formatting | Root font and CSS are shared, but several Super Admin components use separate dates, number/currency formatting and extensive monospace labels | Use shared formatters with explicit platform formatting context |
| Metrics | Dashboard user aggregates count the whole `users` table; pipeline value sums amounts without grouping by currency; `system_status` is literal `healthy` | Define customer/staff metrics and currency semantics before relabeling cards |
| Observability | Existing JSON logging, correlation middleware, public health routes and audit/security tables | Harden and extend these; do not claim complete capture or searchable logs already exist |
| Public demo/contact | Contact page is informational; the billing Contact Sales modal shows local success without saving an enquiry | Implement persisted intake and wire actual website entry points; remove unsupported submission/response-time claims |
| Support | Feedback stores ratings and reports, but does not provide customer ticket conversations or a support lifecycle | Add scoped customer tickets and a guarded platform support workspace; preserve feedback |

Primary evidence:

- Backend: `src/modules/platform_auth/{routes.py,schemas.py,repositories/models.py,repositories/repository.py}`, handlers `review_request.py`, `activate.py`, `verify_challenge.py`, `revoke.py`, services `sessions.py`, `email.py`, `rate_limits.py`; `src/shared/auth/superadmin_guard.py`.
- Frontend: `src/app/superadmin/layout.tsx`, all current `src/app/superadmin/**/page.tsx`, `src/components/superadmin/SuperAdminSidebar.tsx`, `auth/PlatformEntry.tsx`, `auth/PlatformAccessManagement.tsx`, `src/hooks/usePlatformEntry.ts`, `src/hooks/queries/usePlatformAuth.ts`, `src/services/platformAuth.service.ts`, `src/lib/api/platformHttpClient.ts`.
- State/data: `src/hooks/queries/useSuperAdmin.ts`, `useSuperAdminLoginHistory.ts`, `src/services/superadmin.service.ts`, `superadminLoginHistory.service.ts`, `src/store/slices/trialExtensionsUiSlice.ts`.
- Dashboard semantics: backend `src/modules/superadmin/repositories/superadmin_dashboard_repo.py`, `src/modules/deals/repositories/models.py`.
- Demo/support baseline: frontend `src/components/landing/PublicInformation.tsx`, `PublicPageShell.tsx`, `MarketingNavbar.tsx`, `Navbar.tsx`, `Hero.tsx`, `Footer.tsx`, `src/components/billing/ContactSalesModal.tsx`, `src/components/layout/DashboardShell.tsx`, `src/i18n/routing.ts`; backend `src/modules/feedback/routes/feedback_routes.py`, `src/modules/feedback/repositories/models.py`.

### Corrections to the previous plan

| Older claim | Current evidence | Updated action |
|---|---|---|
| Analytics SDKs/provider/test are absent | Frontend dependencies include Vercel Analytics and Mixpanel; `PublicAnalyticsProvider.tsx`, `publicAnalyticsService.ts`, `publicAnalyticsPolicy.ts` and `tests/test_public_analytics_browser.mjs` exist | Preserve and verify public analytics. Add authenticated product events and platform reporting separately; do not reinstall or restore an unidentified commit |
| Startup calls `reset_all_org_lead_pipelines()` | Current backend `src/main.py` startup contains no such call; pipeline preservation tests exist | Keep the fix and regression coverage; do not schedule its removal again |
| Next.js baseline is 16.2.12 | Current frontend manifest declares Next.js/ESLint config 16.3.8, React 19.2.4 and Tailwind 4 | Check installed package versions and bundled Next.js docs before implementation |
| Native frontend development always uses port 3005 | Current `dev`/`dev:turbo` scripts specify 3000; `start` specifies 3005 | Resolve the discrepancy with root instructions during environment setup; use the actual origin consistently in email, proxy and CSRF tests |
| Existing health/error handling is a finished safety foundation | Public detailed health/readiness still return diagnostics; correlation IDs are unchecked and depend on ContextVars; exception logging still interpolates raw exception text | Retain these as open hardening work; reproduce error-path behavior before changing contracts |

The earlier synthetic 500 test results are historical evidence from that document. This analysis did not rerun them. Likewise, source presence does not prove analytics is enabled, SES is configured, migrations are deployed or an owner account exists.

Graphify was attempted first. The CLI points to a missing Python 3.10 executable and `graphify-out/` is absent in this checkout. This plan therefore uses direct source tracing. Repair graph tooling before the first code change; documentation-only work does not require a graph update.

## 3. UI standard: exact CRM reuse

### Authoritative reference

Use the live CRM components and CSS as the implementation standard. The docs file `designSystem.md` is titled “HRMS Design System Reference,” recommends an icon package absent from the frontend manifest and differs from current CRM shadows/radii. Reconcile it with source rather than treating it as executable configuration.

| Concern | CRM source to reuse or extract | Target requirement |
|---|---|---|
| Font | `src/app/layout.tsx` | Instrument Sans through `--font-sans`; no separate platform font |
| Colors | `src/app/globals.css` | Shared `primary`, `background`, `sidebar`, `surface`, `outline`, `on-surface`, `on-surface-variant` and accent tokens |
| Workspace | `components/layout/DashboardShell.tsx` | Same inset padding (`p-2.5 md:p-3`), white rounded workspace, outline border, subtle shadow and height/overflow behavior |
| Sidebar | `components/layout/Sidebar.tsx`, `layout/sidebar/*` | Same 236px expanded/64px collapsed widths, density, logo, icon sizes, active/hover/focus treatment and profile placement |
| Header | `components/layout/Header.tsx` | Same 64px header and spacing; platform title/breadcrumbs and staff profile actions |
| Page headings | `components/admin/shared/AdminPageHeader.tsx` | Reuse its title/subtitle/action hierarchy where applicable; consistent page body padding |
| Buttons | `components/ui/button.tsx` | Existing variants, sizes, disabled/pending states and icon treatment; no custom orange variants per page |
| Tables | `components/shared/table/DataTable.tsx`, `DataTablePagination.tsx` | Same row/header density, sticky treatment, sorting indicators and pagination layout |
| Server pagination | `hooks/useServerPagination.ts`, `useServerPosition.ts` | Adapt server pages without slicing results again; preserve total and page correction semantics |
| Forms | Current CRM invitation/profile forms and `components/auth/OtpInput.tsx` | Same labels, inputs, validation placement and verification control behavior |
| Dialogs/drawers | `components/shared/ConfirmModal.tsx`, existing CRM drawer/dialog patterns | Same overlay, header/footer, spacing and action hierarchy, with safe asynchronous behavior |
| Feedback | Root `react-hot-toast` configuration and shared inline states | Consistent toast placement/duration; inline actionable errors remain visible |
| Dates/numbers | `src/lib/formatters.ts` | Existing format helpers with explicit platform context and currency metadata |
| Localization | Root `next-intl` provider and existing message catalogs | Add platform strings through the established translation structure |

Colors currently include primary `#FF7700`, background/sidebar `#F5F7FA`, surface `#FFFFFF`, outline `#E5E7EB`, main text `#111827` and secondary text `#6B7280`. Consume their existing token names; do not reproduce the hex values throughout new components.

### Reuse boundaries and necessary compatibility work

1. Extract a small presentation-only workspace frame used by CRM and Super Admin. Keep CRM billing, SSE, onboarding, inbox, notes, AI and permissions behavior in its existing shell.
2. Do not mount `DashboardShell`, `Sidebar`, `Header` or `FormattingInitializer` wholesale inside Super Admin: they call customer-session APIs. Reuse narrow presentation pieces and supply platform identity/navigation data.
3. Centralize platform navigation in a typed configuration with required access policy, labels, icons and active-route rules. Preserve CRM navigation policy in `sidebarConfig.ts`/`Sidebar.tsx`; platform grants must not become CRM permission flags.
4. Shared primitives needing change should receive narrow typed options, with existing defaults preserved. For example, route matching must accept platform aliases without adding unrelated CRM conditionals.
5. Review focus/radius tokens used by `Button`: classes reference tokens not defined in the inspected `globals.css`. Verify computed styles before claiming focus parity; fix necessary shared gaps with CRM regression checks.
6. `ConfirmModal` currently closes immediately for `danger` actions. Privileged async actions must retain the dialog and errors until success. Add a narrowly scoped compatibility option or use a suitable existing accessible dialog implementation; preserve existing callers.
7. Existing tables support client sorting/slicing. Platform lists must use manual server sorting and the server-pagination adapter. Do not sort just the visible page or apply two rounds of pagination.
8. `formatters.ts` can inherit persisted CRM formatting state. Supply a complete platform formatting config explicitly, initially UTC for operational timestamps with timezone labels and current UI locale for numbers. Do not fetch a customer organization to initialize staff formatting. Customer financial amounts retain their currency codes; never imply conversion.
9. Use the current light CRM theme. Do not introduce dark mode, another component library, a new icon set or a parallel CSS theme in this upgrade.
10. Add keyboard focus, dialog focus containment/restoration, Escape behavior, labels, accessible status messages and mobile navigation where missing. A UI parity requirement does not justify copying an accessibility defect.

### Visual acceptance

Compare CRM and Super Admin side by side with the same viewport, browser, locale and font loading. Check expanded/collapsed navigation, workspace inset, header, page headings, buttons, filters, tables, empty/error/loading states, drawer and confirmation dialog.

Capture desktop at 1440px, compact desktop at 1024px, tablet at 768px and mobile at 390px. These are verification viewports, not new design breakpoints. Use the CRM's existing responsive rules and provide usable platform navigation below `md`, where CRM's desktop sidebar is hidden. Test 200% zoom and long names/emails. Tables may scroll inside their container; the page must not unexpectedly overflow or trap scrolling.

## 4. Invitation and account lifecycle

### Separate states and commands

Keep account lifecycle separate from email delivery:

| Lifecycle | Meaning | Permitted next actions |
|---|---|---|
| Invited | Owner authorized access; activation remains available | Resend, cancel, expire, activate |
| Enrolling | Invitation consumed; password set; MFA incomplete | Complete valid enrollment or owner restarts enrollment |
| Active | MFA completed; eligible for full sessions | Sign in, owner resets sign-in, owner revokes |
| Expired | Unused invitation passed its expiry | Owner issues a fresh generation |
| Cancelled | Owner withdrew the invitation/enrollment | Remains unusable; any later invitation is explicit |
| Revoked | Staff account disabled and all sessions invalidated | No automatic reactivation through resend/reset |

Delivery independently records Queued, Accepted by email provider, Failed and, if verified provider events are connected, Delivered/Bounced. SES send success means acceptance for sending; it does not prove inbox delivery. [AWS SES sending process](https://docs.aws.amazon.com/ses/latest/dg/send-email-concepts-process.html).

Proposed initial rules:

- Preserve the current 48-hour invitation expiry, 10-minute challenge/enrollment session, five-attempt challenge limit, four-hour full session and 30-minute idle timeout.
- The recipient email is fixed by the invitation. Link possession verifies access to that mailbox for this flow; no public access-request OTP is needed. Forwarding a link transfers that possession, so links must be single-use and the email must state who the invitation is for. Changing the recipient requires cancellation and a new invitation.
- Activation link opening/preview performs no mutation. Only the explicit password submission consumes a valid token; email security scanners must not use up an invitation.
- Use a cryptographically random token, store its digest as the authentication verifier, rotate on explicit resend and reject previous generations. Bound token size and expiry. These mirror established token practices in [OWASP's token guidance](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
- Continue fragment-based activation links; capture the token in transient client memory, clear the fragment with history replacement and never put it in URL filters, persisted state, analytics, console/error reports or ordinary API responses.
- Require a valid enrollment-purpose session to resume after password setup. If it expires or is lost, show a clear owner-assisted restart flow. The QR secret must not become available to authenticated operators or anonymous refreshes.
- Resend applies only to eligible unactivated invitations. **Reset sign-in** is a distinct, confirmed action that revokes sessions and creates a password/MFA recovery invitation. It must not silently reactivate a revoked account.
- Cancelling an enrolling invitation also invalidates its pending sessions. Revocation must defeat simultaneous activation/MFA verification and invalidate outstanding recovery links.
- Block existing CRM emails, the owner's email, active staff duplicates and case/whitespace duplicates. Dedicated staff accounts remain organization-free. Do not merge identities.
- Repeated invite submissions with the same idempotency key return the same result. A different request for an already open invitation returns a clear conflict with resend/cancel guidance.
- Use existing shared rate-limit infrastructure with deliberate account/IP/owner/recipient limits. Define fail-closed production behavior for security-sensitive commands when shared admission is unavailable; do not silently rely on per-process fallback across replicas.

### Persistence recommendation

Add a focused `PlatformInvitation` lifecycle rather than creating fictional public requests or synthetic “reason” values. Retain `PlatformAccessRequest` as legacy history during migration. Adapt the existing crypto/session/enrollment machinery to the new lifecycle.

Proposed invitation fields:

| Field group | Required content |
|---|---|
| Identity | Invitation ID, normalized recipient email, display name, optional linked staff user ID |
| Authorization | Inviter ID, invitation purpose (`onboarding` or `signin_reset`), server-authorized grants if capabilities are introduced |
| Lifecycle | Status, token digest, expiry, generation/version, creation/acceptance/cancellation/completion timestamps |
| Delivery reference | Current delivery generation and attempt/message references; safe status and failure code |
| Migration provenance | Optional unique legacy request ID, preserving original reviewer/timestamps |

Add database constraints for legal states, unique token digests and at most one actionable invitation per normalized email/purpose. Account for expiration explicitly: a uniqueness condition cannot depend on the passage of wall-clock time. Supersede/expire the previous row transactionally before inserting another. Audit case-insensitive uniqueness of the shared user table and related account writers; if it needs a schema change, inventory collisions first and never auto-merge accounts.

Preserve a consistent lock order across invitation, credential and session commands. In particular, current MFA completion finds `PlatformAccessRequest` by email. It must be updated to resolve the correct invitation/enrollment lineage; adding an invitation table without that change leaves new staff stuck in enrollment. Test owners, legacy staff and reset paths separately.

Add focused command/query DTOs, handlers and repository methods under `src/modules/platform_auth/`. Routes authorize, validate and delegate. Register any new router explicitly in `src/main.py`. Import new models in both application model initialization and `tests/conftest.py`.

### Reliable email dispatch

Current sending-before-commit can deliver an unusable link if commit fails, and holds locks while SES responds. Replace that ordering with a transactional delivery intent/outbox. Reuse a compatible existing mechanism if source discovery finds one; otherwise add the smallest focused dispatcher. The [transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) addresses the database/message dual-write gap.

1. Commit invitation, token generation, audit event and delivery intent in one database transaction.
2. Store any raw token needed for delayed sending only as short-lived encrypted delivery material, with a narrowly scoped key, expiry and purge. The invitation's verifier remains a digest; do not put plaintext activation URLs into a generic queue or outbox.
3. Dispatch after commit using the existing worker/scheduler architecture and explicit leases/attempt counters. A synchronous development drain may run after commit, but pending intents must remain recoverable. `QUEUE_MODE=sync` is not durable asynchronous delivery.
4. Retry the same delivery generation with bounded backoff and stable delivery identity; do not rotate the invitation on every worker retry. SES may accept a message before a timeout, so exactly-once email delivery cannot be assumed. Duplicate deliveries must carry the same still-valid link.
5. On explicit owner resend, rotate the token/generation, cancel obsolete pending intents and prevent stale workers from publishing success for the current generation. A late obsolete email must still fail safely at activation.
6. Show queued/accepted/failed separately. Keep visible retry guidance when dispatch is unavailable. Never show “email delivered” from a Boolean transport result.
7. Stop retries for cancelled/revoked/expired generations, purge encrypted material and audit failures without tokens, passwords or MFA secrets.

Use a branded CRM email template with inviter/platform name, recipient, expiry, activation action and ignore/contact guidance. Configure and smoke-test the existing SES sender, production send permissions, suppression/bounce handling and exact HTTPS portal origin. No real invitations are sent as part of writing or reviewing this plan.

### Proposed API contracts

Paths below are relative to the existing `/api/v1` base and are proposals, not current endpoints.

| Method/path | Purpose and guard |
|---|---|
| `POST /superadmin/auth/invitations` | Owner creates invitation; CSRF/origin, validation, idempotency, rate limits |
| `GET /superadmin/auth/invitations` | Owner lists/searches lifecycle and delivery states with bounded pagination |
| `POST /superadmin/auth/invitations/{id}/resend` | Owner rotates an eligible onboarding generation; expected version |
| `POST /superadmin/auth/invitations/{id}/cancel` | Owner invalidates invitation/pending enrollment; expected version |
| `GET /superadmin/auth/operators` | Extend current list with pagination/search; version response contract intentionally |
| `POST /superadmin/auth/operators/{id}/reset-signin` | Owner-confirmed recovery; separate from invitation resend |
| `POST /superadmin/auth/operators/{id}/revoke` | Preserve owner protection and session invalidation |
| `POST /superadmin/auth/activate` | Adapt current activation to invitation lineage; no full access until MFA |
| `POST /superadmin/auth/verify` | Preserve challenge purpose, replay protection and full-session issuance |
| `/superadmin/auth/login`, `/me`, `/logout` | Preserve existing identity/session contracts unless a documented additive change is needed |

Retire public `request-access` and `verify-email` writes at the backend. Removing a link is insufficient. Return a deliberate retired-route response (for example 410), with tests proving no mail, request row or session is created. The old review endpoint must not remain an alternate approval path.

Keep the old frontend request-access URL as a sign-in redirect or clear invitation-required information screen for bookmarked links. It must not render a request form. Update both prefixed routes and short aliases on the Super Admin host, public command allowlists, tests and documentation.

## 5. Migration and compatibility

Use additive Alembic migrations from the actual current head. Do not reuse the old plan's recorded migration head. Verify one head before/after and record the deployed revision separately.

| Existing state | Proposed treatment |
|---|---|
| Owner | Keep identity, encrypted MFA secret, password and recovery/bootstrap CLI; never recreate or invite a second owner |
| Active operator | Keep credentials and sessions unless a specific security correction requires invalidation; link legacy provenance without requiring fresh enrollment |
| Approved request with unexpired link | Backfill an invitation preserving the digest/expiry and make the old emailed link resolve through the compatible activation handler |
| Enrolling request | Backfill enrollment lineage and preserve valid pending sessions so MFA can complete |
| Unverified/pending public request | Archive as legacy history; no automatic access grant. Owner explicitly invites if appropriate |
| Rejected request | Preserve history; no activation |
| Expired approved request | Represent expired history; owner sends a fresh invitation explicitly |
| Revoked operator | Preserve revocation; reset/resend must not restore it |

Backfill must be idempotent with counts and collision reports. Preserve security history and reviewer attribution. Never overwrite the MFA encryption key, copy it into documentation or regenerate it as routine setup.

During cutover there must be one authoritative lifecycle writer. Use either a short maintenance window for platform onboarding commands or a rigorously tested bridge; do not allow the old approval path and new invitation path to diverge. Existing CRM traffic need not stop.

Deploy schema first, then compatible backend, then frontend. Remove old writes when the new flow is available. Keep old tables/compatibility reading until outstanding legacy links/sessions have expired and retention requirements permit cleanup. Schema rollback must not delete invitations or users; prefer rolling back presentation and disabling new invite creation while retaining compatible activation/reset support. Never reopen public requests as an emergency workaround.

## 6. Page-by-page UI delivery

| Page/surface | Required work | Behavior to preserve/clarify |
|---|---|---|
| Sign-in | CRM branding, shared inputs/buttons, clear MFA step/errors, invitation-required guidance | Platform password/TOTP flow, no CRM or Google-login fallback |
| Activation | Invitation-specific copy, password confirmation, safe token capture, enrollment progress and recovery guidance | Fixed recipient, single-use token, no full session before MFA |
| Shell/sidebar | Shared frame, collapse/mobile navigation, staff profile, platform header and centrally configured sections | Owner visibility, explicit active-route matching, isolated platform sign-out |
| Overview | CRM metric cards and headings; explicit loading/errors/freshness; remove literal health | Customer and staff counts distinguished; account enabled is not product activity |
| Organizations | CRM table/filter/search/pagination pattern and URL state | Server filters/sort/total, active/subscription filters and detail links |
| Organization detail | CRM summary/tabs/member table and profile drawer | URL tab/login pagination; correct tenant context; 404 distinct from permission/network failure |
| Login history | Shared date filters/table/pagination/export controls and URL state | CRM login events remain distinct from platform security events; matching list/export filters |
| Trial extensions | Shared table/stats/status/actions and dialogs | Server approval rules, notes, repeat-review conflicts and badge invalidation |
| Feedback | Shared list/cards/filters and image viewer | Category/rating/search, attachment access, explicit unavailable statistics |
| Platform Access | Invitations and Staff tabs; primary Invite staff action; shared table and dialogs | Owner-only UI/API; lifecycle/delivery status, cancel/resend/reset/revoke with distinct confirmations |
| Website Request a demo | Public marketing form with real validated persistence and receipt | Anonymous intake only; no public requester list/detail; truthful delivery/scheduling copy |
| Demo Requests | Shared CRM board/list, filters, details and activity | Staff capabilities, server-backed stages, assignment, follow-up, concurrency and bounded column loading |
| Customer Help & Support | CRM create/list/detail/conversation and navigation | Requester/organization scope, public replies and reopening; usable during trial expiry |
| Platform Support Tickets | Shared queue/detail, assignment/priority/status and conversation | Capability-gated cross-tenant staff access; internal notes never serialized to customers |
| Forbidden/unavailable/not found | CRM-compatible status panels with useful next actions | 401 sign-in, 403 insufficient access, network/503 retry; no “invalid credentials” label for every outage |
| Analytics, Errors, Logs | Use the same shell and screen patterns when their APIs are ready | No enabled navigation to empty stubs; capability checks and provider unavailable states |

Rename developer wording throughout the platform routes/components and related entry links, including loading and error copy. Replace the profile fallback “Developer” with a staff/account label. Remove static port text. Any “Open CRM” link must use the configured CRM origin: on a Super Admin hostname, `/dashboard` is rewritten into the platform route tree by `src/proxy.ts`. It must not imply the platform session grants customer access.

### State and data rules

- TanStack Query owns platform reads, mutations, retries, errors and invalidation. Services use `platformHttpClient`; components do not perform API calls directly.
- URL/search parameters own search, filters, sorting, pagination, date ranges and tabs. Use a focused hook and validated allowlisted values; reset page atomically when filters change and debounce requests without breaking back/forward navigation.
- Redux may retain shared drawer/modal/UI preferences. Replace trial-extension selected entity snapshots with IDs resolved from query data, and move its filters/pagination to URL state. Local form input remains local where sharing is unnecessary.
- Include every response-affecting parameter and relevant operator/session boundary in query keys. Cancel/remove platform queries on expiry, logout, account change or access loss before another operator can see cached tenant data. Do not clear customer CRM credentials or its independent caches.
- Privileged mutations should use server-confirmed results, per-action pending state and version/conflict handling. Avoid optimistic approval/revocation displays that can imply success after failure.
- Move login-history CSV orchestration from the route component into a focused hook; preserve the existing service's CRM `sessionCheckin` use by `AuthGuard` or move that call to a CRM service with all callers updated.
- Keep server-side filters authoritative. Never filter an already paginated response again in React. Update badges, current lists, details and relevant totals after successful commands.

### Dashboard data corrections

Define customer organization users and internal staff separately in the API and labels. Current `active_users` reflects account `is_active`, not recent usage; do not label it daily/monthly active usage. Product activity requires defined events and reporting windows.

Current pipeline value sums `Deal.amount` despite a per-deal currency field. Group by currency (including an explicit unknown-currency bucket) or remove the combined currency card until a verified conversion policy exists. Formatting a mixed-currency sum does not correct it. This is a metric correction, not platform subscription revenue.

Replace `system_status="healthy"` with actual measured status/freshness, or remove the health contract/card until the guarded health query exists. A successful KPI fetch proves that request succeeded; it does not prove all services are healthy.

### Added feature: demo requests and sales pipeline

Add a public `/request-demo` page with the existing marketing shell and English/Dutch conventions. Proposed required fields are name, email and company; phone, team size, use case and preferred contact window/timezone are optional. Persist before acknowledging success, bound and validate input, rate-limit anonymous submissions and protect against retries creating duplicates. Do not expose anonymous list/detail endpoints or imply that a preferred window is a booked meeting.

Add `/superadmin/demo-requests` with board/list views, server filters/counts, assignment, notes, next follow-up and immutable stage history. Proposed stages: New → Contacted → Qualified → Demo Scheduled → Demo Completed → Follow-up → Converted, with Not Proceeding and an audited Spam disposition. Provide drag-and-drop and an accessible stage selector using the same version-checked server command. Load cards per column with explicit bounds; do not claim a paginated subset is the whole pipeline. Converted does not automatically create a customer organization or prove revenue.

Add a focused `demo_requests` backend module and `view_demo_requests`/`manage_demo_requests` platform capabilities, owner-granted with no automatic staff exposure. Reuse reliable delivery intents for configured notifications. Reconcile the non-persisted sales modal with the intake service or remove its false success behavior. Detailed persistence/API/testing contracts are in Phase 4 of the implementation plan.

### Added feature: basic customer support tickets

Add CRM `/dashboard/support` list/create and detail/conversation routes, with Super Admin `/superadmin/support-tickets` queue/detail routes. Customers submit subject/category/description and can read/reply/reopen their own tickets in their current organization. Server scope supplies reporter/organization. Do not automatically give organization administrators visibility into other users' conversations. Keep Help & Support usable during trial expiry while preserving other subscription restrictions.

Staff with `view_support_tickets`/`manage_support_tickets` triage, assign, prioritize, reply publicly, add internal notes and track immutable history. Proposed workflow: Open → In Progress → Waiting for Customer → Resolved → Closed, with explicit reopening. Internal notes are excluded from customer queries/serialization and notifications, not just hidden visually. Use idempotent submissions/replies, version-checked updates and durable notification delivery.

Add a focused `support_tickets` module with ticket, message and activity models. Feedback-to-support conversion is explicit and idempotent; later support-to-Error-Center linking preserves access boundaries. A support ticket remains a customer conversation, not a runtime issue. Version one is text-based; attachments, inbound-email parsing, SLA engines, live chat and AI replies are optional later work. Detailed contracts and tests are in Phase 5 of the implementation plan.

## 7. Retained analytics, Error Center and Application Logs roadmap

The existing plan's three product goals remain in scope for the overall roadmap. Deliver invite-only access, UI parity, demo intake/board and basic customer support as the first operational release. Observability follows separate gates so AWS/provider decisions do not block these workflows.

### Foundation and capabilities

Reproduce and fix correlation IDs on unexpected 500s, preserve IDs in request state and attach safe IDs in outer error responses. Validate/bound request and correlation headers. Sanitize nested data, SQL diagnostics and exception messages before logging or export. Replace blanket internal `ValueError` disclosure only after inventorying intentional business-validation contracts; keep appropriate 422/domain errors.

Public liveness/readiness return minimal status only. Detailed health is platform-authorized and sanitized. Worker/scheduler health requires remote heartbeat/freshness; S3 configuration is not a reachability check. Use Unknown, Degraded, Unavailable and Healthy with observation times; never infer health from missing data.

Before sensitive observability release, add owner-managed capabilities such as `view_observability`, `manage_issues`, `export_diagnostics` and `configure_providers`. Preserve `is_owner` for access management. Existing non-owner staff receive no new diagnostic privileges automatically. Validate grants on the server, include them in identity/cache behavior and enforce revocation on active sessions.

### Error Center

Retain the earlier issue/occurrence/activity/feedback-link design, grouping fingerprint version, stable event delivery IDs and immutable workflow history. Provide All Failures plus grouped tickets, assignment, comments and statuses: Open → Triaged → In Progress → Fix Deployed → Resolved, with Reopened/Ignored/Duplicate transitions.

Expected authorization/validation failures are classified, not automatically treated as defects. Distinguish untrusted browser claims from server-enriched identity. Deduplicate delivery separately from grouping, count occurrences atomically and handle concurrent edits with expected versions. Reopening must use verified deployment chronology, not commit-hash string sorting.

### Application Logs and durable capture

Preserve the earlier independent collector proposal and guarded log-store adapter. AWS CloudWatch remains a planning option from the prior plan; confirm compute, region, resources, costs, Vercel drain support and retention before provisioning. Capture must survive FastAPI/CRM database outages through a separate durable ingestion path. An in-process buffer or synchronous CRM queue is only a local development aid.

Cover browser/Next.js, FastAPI, workers, scheduler, integrations and deployments with a sanitized envelope and bounded payloads. Keep private release source maps outside public assets. Prevent collector diagnostics from generating capture loops.

Logs UI provides Runtime Logs, Business Audit and Platform Security views, explicit filters/freshness, bounded server-built searches, query handles/poll/cancel and audited protected exports. Do not expose arbitrary provider query execution or mix runtime logs into organization audit rows.

### Analytics

Preserve existing consent-aware public Vercel/Mixpanel collection. Its allowlisted route policy excludes authenticated/platform paths. Test short Super Admin host aliases as well as `/superadmin/*`: a rewritten host root must not be mistaken for the public marketing home page.

Add curated authenticated product events, opaque user/organization identity and reset on logout/tenant switching. Committed backend completions are authoritative; browser submissions are attempts. Analytics failures must not block authentication or business writes. Add server-only reporting adapters and platform aggregates with defined periods/timezones, permissions, cache keys and freshness. Verify real provider account/reporting access before promising available reports.

Carry forward retention/budget, redaction, export audit, alert routing and production kill-switch requirements from the older plan. Reconfirm hosting/provider/account facts with the owner; older documented hosting choices are planning context, not a deployment audit. Never enable collection before its required infrastructure and access controls are ready.

## 8. Delivery phases and review gates

| Phase | Deliverable | Required exit evidence |
|---|---|---|
| 0 — Baseline | Pin commit IDs/installed versions; capture current CRM/platform screens; map routes/contracts; inspect migration state and legacy access counts; repair graph tooling | Approved visual reference, measured baseline failures, documented migration cases and no exposed configuration values |
| 1 — Invitation backend | Add invitation/delivery models, command/query handlers, constraints, reliable dispatch, compatible activation/MFA/reset/revoke and retirement of public requests | Targeted auth tests plus PostgreSQL races pass; no mail-before-commit; legacy owner/staff/enrollment work |
| 2 — Shared UI foundation | Extract presentation frame/navigation pieces and necessary safe dialog/table compatibility; build platform shell/auth/access screens | CRM shell regression checks pass; visual parity approved; platform screens issue no customer-session API calls |
| 3 — Existing screens | Refactor overview, organizations/detail, login history/drawer/export, trial extensions/modals and feedback | URL-state/browser checks, accurate metrics, loading/error/empty states and page behavior inventory pass |
| 4 — Demo requests | Public persisted form, sales board/list, stages, assignment/follow-up/history and platform capabilities | Anonymous abuse/PII protection, idempotency, authorized staff visibility, versioned transitions and column counts pass |
| 5 — Support tickets | Customer own-ticket flow and platform queue, messages, internal notes, priority/status/history and notifications | Cross-user/tenant isolation, internal-note exclusion, expired-trial access, replies/reopening and delivery-failure tests pass |
| 6 — First operational release | Stage migration, real controlled SES flows, HTTPS/proxy tests, frontend/backend cutover and rollback rehearsal | Staff invitation, demo submission/stage tracking and customer/staff support conversation work; public staff applications remain closed |
| 7 — Observability foundation | Correlation/redaction/minimal probes, measured guarded health, diagnostic capabilities and capture contracts | Sanitized 500s/headers/logs, capability negatives, measured freshness and unchanged pipeline preservation |
| 8A–8C — Error Center, collector and Logs | Issue workflow, independent production capture, durable grouping and complete log search/context/promotion/export | Outage/replay/concurrency/retention tests pass before production automatic tickets or capture are enabled |
| 9 — Analytics and operations | Product/traffic reports, funnels/retention, demo/support aggregates, provider controls, alerts and retention | Synthetic funnel/completion dedupe, provider outage isolation and configured incident delivery verified |

Phases 1 and 2 may be implemented against agreed contracts in separate changes, but neither is release-ready without the other. Every phase produces functioning behavior; empty files or disabled stub pages are not completed features. Review one representative list page and its dialogs before applying the design across all pages.

Recommended change boundaries: invitation schema/backfill; invitation commands/dispatch/auth compatibility; shared presentation extraction; staff access/auth UI; existing page migrations in small groups; first-release operational cutover; then independent observability work. Do not combine a global CRM redesign with the platform work.

Demo intake/pipeline and customer support each add focused model/migration, backend-use-case, UI and verification changes before the first operational cutover. Capability infrastructure starts with sales/support access and expands for diagnostics. The implementation companion details each work package and its exit criteria.

## 9. Verification plan

### Required security and lifecycle cases

- Anonymous visitors and CRM JWTs cannot invite/list staff or access platform data. A CRM user with a superadmin flag still cannot authenticate through the platform boundary.
- Non-owner operators cannot invite, cancel, resend, reset, revoke or grant themselves capabilities through direct API requests.
- Missing/untrusted origin, missing request header and invalid CSRF are rejected for protected commands. Cookie path/host/Secure settings and proxy behavior remain correct.
- Password-only, expired challenges, excessive attempts and replayed TOTP cannot create full sessions. Existing idle/full-session expiry and trusted-server owner recovery still work.
- Duplicate normalized emails and concurrent invitations create one authoritative result. CRM/staff identity collision never merges accounts.
- Replayed/expired/tampered/cancelled/old-generation links fail; activation GET previews do not consume tokens.
- Activation versus resend/cancel/revoke/reset races cannot produce an unauthorized active account. Test real PostgreSQL row locks/constraints; SQLite does not establish race safety.
- Enrolling users can complete valid enrollment or restart through the owner; refreshing/lost cookies/expired enrollment have clear outcomes. Legacy owner enrollment still works without an invitation.
- Reset and resend are separate; delivery retry never resets an active account. Revoked accounts cannot be restored accidentally.
- Database commit failure sends no email. Worker restart, SES rejection/timeout and repeated delivery attempts preserve the right generation and truthful status.
- Tokens, passwords, CSRF values and MFA secrets are absent from logs, analytics, exports, URL filters and persisted UI state. Encrypted delivery material is purged.

### Required UI and regression cases

- Real screens/components/hooks use the shared CSS and font for visual checks; functional mocked fixtures alone do not prove parity.
- All routes and Super Admin host aliases work for direct load, reload, browser back/forward, auth expiry and deep links.
- Search, filters, sort, page, page size and tabs survive URL navigation; invalid values are normalized; changing filters resets page; server pages are not sliced or sorted twice.
- Errors cannot become “no records,” zero totals or healthy badges. Stale data is labeled; refresh failure remains visible.
- Invite modal validates recipient/name, prevents duplicate submission and distinguishes queued email from failure. Reset/revoke/cancel dialogs identify the target and retain errors.
- Trial extension approval/rejection preserves notes, conflicts and badge/list invalidation. Selected IDs resolve fresh data rather than stale Redux copies.
- Login CSV export matches filters, handles failure and stays platform-authorized; ordinary CRM session check-in still works.
- Feedback image viewers/drawers/dialogs have focus containment, keyboard dismissal, focus restoration and usable narrow layouts.
- Staff sign-out/expiry clears platform caches and transient privileged state while preserving a separate CRM session. Account changes do not expose prior cached tenant information.
- Platform formatting is stable with and without a persisted CRM session; midnight/timezone boundaries, invalid dates, no-data values and mixed-currency amounts render accurately.
- Shared UI extraction preserves CRM navigation, billing/trial behavior, onboarding, inbox, locale and customer authentication.
- Demo form commits before success, survives notification failure, prevents duplicate retry records and exposes no anonymous PII reads. Board transitions/assignments are authorized, versioned and persisted, with accurate per-column totals.
- Customer support tickets reject cross-user/tenant access, exclude internal notes from every customer payload, permit scoped replies/reopening and remain usable during trial expiry. Notification retries do not duplicate messages or lose conversations.

### Repository commands and test additions

Run from each nested repository. These are implementation/release checks; they were not executed for this documentation-only analysis.

Backend baseline/targeted regressions:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth.py tests/test_superadmin_guard.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_superadmin_dashboard.py tests/test_superadmin_organizations.py tests/test_superadmin_login_history.py tests/test_superadmin_feedback.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_startup_pipeline_data_preservation.py tests/test_startup_preserves_pipelines.py -q
.\.venv\Scripts\python.exe -m alembic heads
```

Extend `test_platform_auth.py` for invitation behavior while retaining applicable existing security tests. Add focused invitation/delivery/migration test files and extend `test_platform_auth_postgres.py` for the listed races. Do not keep obsolete approval tests passing by leaving public approval enabled.

PostgreSQL concurrency verification requires a verified test-only database and inspection of its fixtures before opting in:

```powershell
$env:PLATFORM_POSTGRES_TESTS='1'
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth_postgres.py -q
```

Inspect migration upgrade/backfill using representative legacy states in a disposable database; test rerun safety, one migration head and a compatible code rollback. Add observability-targeted tests with those later phases. Unit tests use SQLite/fake Redis and do not require starting Docker.

Frontend:

```powershell
npx.cmd tsc --noEmit
npm.cmd run lint
npm.cmd run test:localization
npm.cmd run test:platform-auth:browser
npm.cmd run test:session-startup:browser
npm.cmd run test:invitations
npm.cmd run test:public:analytics
npm.cmd run build
```

Use focused ESLint during each change and full lint at the release gate. Current browser authentication tests use real components/hooks/transport against a simulated API; extend them for owner-sent invitations, retired requests, error handling and session isolation. Add a focused platform UI/URL-state/visual browser test using the repository's existing Node/Playwright style. Confirm browser binaries and real CSS/font fixtures before running it. There is no assumed Jest/Vitest suite or project Playwright config to invoke.

For the shared frame change, run the relevant existing CRM browser fixtures after inspecting their coverage, including Teamspace theme and session startup, plus manual billing/onboarding navigation smoke checks. These do not replace full Next.js route/proxy and staging HTTPS smoke tests.

Record existing unrelated lint/build failures separately, with exact reproduction; a phase must not introduce new ones or claim a blocked check passed. After code changes, run the required `graphify update .` from the workspace once tooling is repaired. Documentation-only changes need no graph refresh.

## 10. Release and rollback checklist

Before first production release:

- [ ] Plan scope and owner-only invitation policy reviewed.
- [ ] Current owner/recovery access verified without exposing credentials.
- [ ] Database backup and additive migration/backfill rehearsal completed.
- [ ] Exact frontend origin, CRM origin, API proxy and deployment order confirmed.
- [ ] Shared UI and all current pages pass parity review and required regression checks.
- [ ] Real controlled SES invitation reaches the designated test staff mailbox; activation/MFA/login/reset/revoke verified on staging HTTPS.
- [ ] Invitation worker dispatch/retry/cleanup is actually running; queued/failed states and retry limits are visible.
- [ ] Legacy active staff and in-flight enrollment/link compatibility verified.
- [ ] Public request/verification/review creation paths are retired in deployed backend and UI.
- [ ] Public demo form → persisted enquiry → staff board assignment/stage movement verified; no fake sales submission success remains.
- [ ] Customer ticket → staff public reply/internal note → customer response/resolution/reopen verified; other customers cannot access it.
- [ ] Rollback retains compatible activation and never restores public self-service access.
- [ ] Separate later-release flags protect production telemetry, automatic ticket creation and provider reports until prerequisites pass.

A small invited test cohort should exercise first onboarding before broader staff rollout. Monitor activation failure, MFA failure, queued-mail age, dispatch failures, 401/403/503 rates and frontend errors with sanitized diagnostics. Keep the owner recovery procedure available during portal outages.

## 11. Review decisions and implementation deliverables

Confirmed: **Super Admin staff only** for invitation changes; remove developer branding/public request onboarding; refactor the complete UI to the current CRM standard; add website demo requests with a Super Admin pipeline board; allow **CRM users to submit and track their own support tickets**, managed by authorized platform staff; provide a revised plan for review before coding.

Proposed defaults for approval with this plan:

1. Only the platform owner invites/resets/revokes staff in the first release.
2. Retain dedicated staff email/password plus mandatory authenticator MFA; no platform Google sign-in is added.
3. Retain 48-hour invitation expiry and current session/challenge limits.
4. Add a dedicated invitation lifecycle and reliable delivery intent; preserve legacy data and compatible in-flight onboarding.
5. Use the current CRM light UI and shared presentation primitives, with explicit UTC operational timestamps initially.
6. Ship invitation access, complete existing-page UI parity, demo intake/board and basic customer support as the first operational release; preserve analytics, Error Center and Logs as subsequent releases with their own prerequisites.
7. Use fixed initial demo stages and a text-based basic support conversation; configurable pipelines, calendar booking, attachments, email ingestion and SLA automation are later additions.

Implementation-time deployment inputs: authorized staff recipients, actual owner state, correct portal/CRM origins, SES sender/permissions, current database revision and legacy counts, worker execution mode, and later AWS/provider/retention/budget choices. Obtain configuration through deployment tooling; never paste credential values into this plan.

Final implementation artifacts should include:

- Invitation/access API contracts, additive migrations and backfill report.
- Updated staff sign-in/activation/access UI and all existing platform screens.
- Persisted public demo intake and staff pipeline board with stage/assignment/follow-up history.
- Scoped customer support UI/API and staff queue with public replies, private notes, lifecycle and reliable notifications.
- Reused shared CRM presentation pieces with compatibility regression evidence.
- Security, concurrency, migration, functional and visual verification results.
- Revised staff onboarding/recovery instructions and deployment/rollback runbook.
- Reconciled observability roadmap and evidence-based feature inventory updates using exactly `IMPLEMENTED`, `PARTIALLY IMPLEMENTED`, `BACKEND ONLY`, `INTERNAL`, or `PLANNED / DOCUMENTED ONLY`.

Review of this plan authorizes no accounts, invitation emails, provider provisioning or deployment by itself. Those actions belong to the later implementation and operational scope.
