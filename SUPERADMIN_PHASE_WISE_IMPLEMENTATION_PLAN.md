# Super Admin phase-wise implementation plan — revised

Date: 9 October 2026

Status: EXECUTION STARTED. Phases 0–2 completed locally on 9 October 2026; see the [Phase 0 review package](superadmin-phase0/README.md), [Phase 1 review package](superadmin-phase1/README.md) and [Phase 2 review package](superadmin-phase2/README.md). Phases 3–9 remain planned. Local completion is not a production release or a claim of bug-free behavior.

This is the execution companion to [SUPERADMIN_MASTER_UPGRADE_PLAN.md](SUPERADMIN_MASTER_UPGRADE_PLAN.md). It incorporates the original [analytics, Error Center and Logs requirements](superadmin_upgrade_plan.md), staff invitations/UI parity, and the newly requested demo pipeline and customer support tickets. The phase sequence below replaces the earlier phase sequence in the master plan.

## Confirmed scope

- Platform staff join by owner-sent invitation, email activation and mandatory MFA. Customer organization invitations remain separate.
- Every Super Admin screen follows the current CRM UI components, tokens and layout conventions.
- Website visitors can request a demo. Every accepted request is stored and appears in a Super Admin pipeline board with tracked stages.
- **CRM users can submit and track their own support tickets.** Authorized platform staff manage the cross-tenant support queue and reply to customers.
- Vercel/Mixpanel analytics, automatic Error Center tickets and searchable application logs remain in the roadmap.

There are three distinct records: a demo request is a sales enquiry; a support ticket is a customer conversation; an Error Center issue groups instrumented application failures. Link them when useful, without combining their permissions, statuses or histories.

## Delivery sequence

| Phase | Outcome | Dependencies |
|---|---|---|
| 0 | Verified baseline, visual reference, contracts and migration inventory | None |
| 1 | Staff invitation/authentication backend and reliable email delivery | 0 |
| 2 | CRM-aligned platform shell, staff sign-in and access management | 1 contracts |
| 3 | Complete redesign and behavior correction of existing platform pages | 2 |
| 4 | Public demo form and working Super Admin pipeline board | 1 delivery foundation, 2 UI |
| 5 | Customer support tickets and platform support workspace | 1 delivery, 2 UI, 4 capability foundation |
| 6 | Staged migration, end-to-end verification and first operational release | 1–5 |
| 7 | Diagnostic hardening, measured health and observability permissions | Baseline; shared platform foundations |
| 8A | Error Center workflow with local fixtures | 7 contracts |
| 8B | Independent production capture and durable grouping | 7; AWS/deployment inputs |
| 8C | Searchable Logs UI and end-to-end Error Center | 8A and 8B |
| 9 | Analytics reporting, operational alerts and final rollout | 7–8; provider access |

Phases are completion boundaries, not large unreviewable changes. Implement small changes within each phase, verify the relevant behavior, then continue. Critical verified diagnostic exposure fixes from Phase 7 may ship earlier as isolated fixes; new monitoring infrastructure must not delay them. No calendar estimates are asserted before the baseline establishes actual dependencies and failures.

## Phase 0 — Baseline and contracts

**Status: COMPLETE (local baseline).** [Report](superadmin-phase0/BASELINE_REPORT.md), [visual references](superadmin-phase0/README.md#visual-references), [typed API/state contracts](superadmin-phase0/CONTRACTS.md), [migration checklist](superadmin-phase0/MIGRATION_CHECKLIST.md). Targeted backend: 58 passed; frontend types, lint (0 errors, existing warnings), selected browser/localization/invitation checks and production build passed. PostgreSQL/deployment checks remain Phase 1/6 gates.

**Purpose:** establish exactly what must be preserved before modifying authentication, shared UI or customer workflows.

Work:

1. Record frontend/backend/docs commit IDs and existing local changes. Use the nested repositories; preserve the pre-existing edit to `Superadmin login.md`.
2. Verify installed versions, current scripts, actual development origin, Super Admin host aliases, API rewrite behavior and migration head. Resolve the documented 3005 versus manifest 3000 development-port discrepancy.
3. Capture current CRM reference screens and platform screens using the same browser/font/locale at desktop, tablet and mobile widths.
4. Run targeted baseline authentication/page checks and record unrelated failures. Use fake delivery and synthetic accounts locally.
5. Inventory legacy access requests, owner/operator states and in-flight enrollment in a safe test dataset. Define backfill, collision and rollback behavior.
6. Finalize typed contracts for invitations, demo requests/stage transitions, support tickets/messages and list pagination. Define permitted fields, lengths, status transitions, expected versions and idempotency behavior.
7. Repair Graphify tooling if available; the previous query failed because its configured Python executable is missing and this checkout has no graph output. Source remains authoritative.

Source findings relevant to the added scope:

- `components/landing/PublicInformation.tsx` renders an informational contact page; it does not implement a request queue.
- `components/billing/ContactSalesModal.tsx` changes local state and shows a success toast without persistence. Reuse neither its submission behavior nor its unverified 24-hour response promise.
- Existing `UserFeedback` stores ratings/suggestions/issue reports, but its schema is not a support conversation or ticket lifecycle.
- `DashboardShell.tsx` allows only selected paths through trial-expiry lockout. The new support route needs an intentional exception so customers can ask for help.
- No demo/support-ticket-named implementation was found in the focused source search. Verify full registration and adjacent modules before adding new contracts.

**Deliverables:** baseline/check report, reference screenshots, API/state contracts and migration checklist. Update this plan only for material discoveries.

**Complete when:** sources and references are verified, proposed access rules are explicit, and the implementation has reproducible baseline checks. No provider API key is required for this phase.

## Phase 1 — Staff invitations and reliable delivery

Detailed execution companion: [SUPERADMIN_PHASE_1_IMPLEMENTATION_PLAN.md](SUPERADMIN_PHASE_1_IMPLEMENTATION_PLAN.md). **Status: COMPLETE (local backend).** Typed owner APIs, legacy migration, activation/MFA/resume/reset/revoke and durable delivery are verified. 139 targeted backend tests and both existing browser suites passed. Evidence and release limits: [Phase 1 review package](superadmin-phase1/README.md). Compatible UI follows in Phase 2; live-provider/deployment checks remain Phase 6.

**Purpose:** replace public access applications with owner-initiated onboarding while retaining platform security.

Implement in order:

1. Add a dedicated platform invitation model, additive Alembic migration and idempotent legacy backfill. Preserve owner identity, active operators, encrypted MFA secrets and compatible in-flight activation/enrollment.
2. Add focused create/list/resend/cancel/reset/revoke handlers and request/response DTOs. Retain owner-only provisioning, normalized-email collision checks and database constraints.
3. Adapt activation and MFA completion to invitation lineage; current MFA completion resolves legacy requests by email and cannot be left unchanged.
4. Preserve hashed single-use tokens, proposed 48-hour expiry, enrollment/challenge limits, session expiry, origin/CSRF checks and CRM/platform authentication separation.
5. Split **resend invitation** from **reset sign-in**. Cancelling pending enrollment and revoking an account must invalidate their applicable sessions/links, including concurrent requests.
6. Commit invitation, security event and delivery intent together. Dispatch after commit; encrypted short-lived delivery material, leases/retries and generation checks prevent plaintext-token persistence and stale resend behavior.
7. Retire public request-access/email-verification writes and the old approval write path during coordinated cutover. Keep compatible legacy activation reads until outstanding links/sessions expire.

Primary backend touchpoints: `src/modules/platform_auth/{commands,queries,handlers,repositories,services}`, `routes.py`, `schemas.py`, application/test model registration and `alembic/versions`. Reuse current crypto, sessions, guards and email integration.

**Verification:** owner-only/CSRF/origin negatives; CRM token rejection; expired/replayed/cancelled tokens; interrupted enrollment; owner recovery; existing staff compatibility; no email before commit; send rejection/timeout/restart; resend generations; real PostgreSQL invite/activate/cancel/reset/revoke races.

**Complete when:** the backend can invite, enroll, authenticate, recover and revoke staff safely; database failures cannot report a successful invitation email; public applications cannot create new access. Local implementation uses fake delivery. Real SES is verified in Phase 6 before release.

## Phase 2 — Shared CRM UI and staff access screens

Detailed execution companion: [SUPERADMIN_PHASE_2_IMPLEMENTATION_PLAN.md](SUPERADMIN_PHASE_2_IMPLEMENTATION_PLAN.md). **Status: COMPLETE — local implementation and verification.** [Review package, evidence and screenshots](superadmin-phase2/README.md). Steps 2.0–2.7 deliver the shared CRM frame, isolated platform sessions/transport, navigation, staff authentication and invitation/staff management. Full redesign of existing page contents remains Phase 3; production delivery/deployment checks remain release gates.

**Purpose:** establish one visual foundation before migrating every screen.

Implement in order:

1. Extract the smallest presentation-only workspace frame from the CRM shell. Reuse its Instrument Sans font, CSS tokens, 236px/64px sidebar modes, 64px header and inset white workspace.
2. Keep organization, billing, inbox, SSE, onboarding and AI effects in the CRM shell. Platform pages must not initiate those customer-session requests.
3. Add centralized typed platform navigation and platform-specific identity/profile actions. Handle short host aliases and configured CRM-origin links correctly.
4. Reuse existing buttons, page headings, table/pagination presentation, dialogs, OTP input, toast configuration and translations. Make only narrow compatibility changes required by async privileged actions, keyboard access and server pagination.
5. Build staff sign-in/activation/MFA and Platform Access Invitations/Staff screens. Replace developer terminology throughout the platform UI and bookmarked entry screens.
6. Add platform-explicit formatting and isolated UI preferences/query cleanup. Differentiate authentication failure, insufficient permission and network/service failure.

**Verification:** real-CSS/font visual comparison at 1440/1024/768/390px and 200% zoom; collapse/mobile navigation; keyboard focus/dialogs; pending/error actions; platform logout/account switching; no customer-session API requests; shared CRM shell regressions.

**Complete when:** an owner can complete the full invitation flow through the UI against the test API, an invited staff member completes MFA, and the shell matches the CRM reference. Functional mocked browser tests alone do not establish visual parity.

## Phase 3 — All existing Super Admin screens

Detailed execution companion: [SUPERADMIN_PHASE_3_IMPLEMENTATION_PLAN.md](SUPERADMIN_PHASE_3_IMPLEMENTATION_PLAN.md). **Status: COMPLETE — local implementation and verification, 3A–3E and integrated acceptance.** [Review evidence](superadmin-phase3/README.md), [Organizations/Login History](superadmin-phase3/ORGANIZATIONS_LOGIN_HISTORY.md), [trial review/Feedback/final checks](superadmin-phase3/TRIALS_FEEDBACK.md), and [Phase 4 handoff](superadmin-phase3/PHASE_4_HANDOFF.md). Operational release verification remains Phase 6; nothing has been deployed by this package.

**Purpose:** finish the current portal before adding sales/support workspaces.

Deliver these small work packages:

| Package | Screens | Required behavior |
|---|---|---|
| 3A | Overview | Shared cards/headings; truthful loading/errors; separate customer/staff metrics; remove literal healthy status; group financial totals by currency or omit invalid aggregate |
| 3B | Organizations and detail | Shared filters/table/drawer; server sort/pagination; URL search/filter/tab/page state; correct tenant detail |
| 3C | Login history and member drawer | Shared date controls; filtered export through a hook/service; timezone correctness; preserve CRM session check-in |
| 3D | Trial extensions | Shared status/table/dialogs; retain business review rules/notes/conflicts; URL filters; selected IDs instead of copied server entities in Redux |
| 3E | Feedback | Shared filters/list/stats/image viewer; explicit empty/error states and protected content |

Use focused screen components and hooks rather than large route files. TanStack Query owns server data; URLs own shareable view state; local/Redux state holds only appropriate UI state. Queries include all response parameters and operator boundaries.

**Verification:** direct navigation/reload/back/forward; page reset on filter changes; no double pagination/client filtering of server pages; accurate totals; retry/stale/error behavior; dialog action conflicts; export filter agreement; current customer CRM regression fixtures.

**Complete when:** every existing route and action works using the shared design, and no remaining developer branding or fabricated health claims appear. New Analytics/Errors/Logs links remain disabled/absent until usable screens exist.

## Phase 4 — Website demo requests and Super Admin pipeline

**Purpose:** visitors can submit a real enquiry and staff can track every accepted request through a sales process.

### 4A. Public form and durable intake

- Add a dedicated `/request-demo` page using the existing public marketing shell. Add **Request a demo** links to the actual landing navigation/hero/footer and relevant public pricing/contact surfaces without replacing customer signup/sign-in.
- Follow the website's English/Dutch conventions. Verify existing locale routing before choosing additional localized paths; do not assume `/nl/request-demo` works automatically.
- Proposed fields: required full name, email and company; optional phone, team-size range, use case/message and preferred contact window with timezone. A preferred window is a request, not a confirmed appointment.
- Validate and bound input on both client and server. Explain the purpose of contact using approved public copy. Do not add unsolicited marketing subscription or promise a response time that has not been established.
- Create a focused backend `demo_requests/{commands,queries,handlers,repositories,routes,services}` module with persistence and model registration. Requests are platform sales records, not customer-owned CRM leads or automatic organization accounts.
- Proposed public endpoint: `POST /api/v1/public/demo-requests`. This is anonymous intake with no anonymous list/detail endpoint. Add shared rate limits, body limits, honeypot/bot controls and bounded idempotency; return a receipt only after commit.
- A retried submission with the same idempotency key produces one record. Do not deduplicate every request forever by email: a later genuine enquiry is valid. Flag potential repeats for staff without revealing existing submissions to visitors.
- Public success never waits for staff email delivery. Queue an internal notification through the reliable delivery mechanism. A recipient acknowledgement is configurable and rate-limited to avoid turning the endpoint into an email relay.
- Reconcile the existing non-persisted billing sales modal: preferably route its authenticated enquiry through the same intake service with trusted source/context and its own sales enquiry type. If retained unchanged temporarily, remove false success claims and do not present it as wired to the demo board.

### 4B. Staff board and list

New route: `/superadmin/demo-requests`. Provide a board/list toggle, search, stage/assignee/date/source filters, server totals, details and activity history.

Proposed fixed stages for version one:

`New → Contacted → Qualified → Demo Scheduled → Demo Completed → Follow-up → Converted`

Provide **Not Proceeding** as a terminal alternative with a reason, and an audited Spam disposition. These stage names are proposed defaults, not an implemented configurable workflow builder.

Board behavior:

- Each card identifies the company/requester, assigned eligible staff member, age, next follow-up and stage. Staff can add internal notes and contact/scheduled-demo/follow-up details.
- Move cards by drag-and-drop and an accessible “Move to stage” control. The same server transition command validates allowed transitions and expected version for either action.
- Concurrent moves yield a visible conflict/reload rather than silent overwrites. Preserve actor/time/reason/history. Do not use array positions as persistent stage identity.
- Use per-column bounded loading/cursors and server counts; show truncation/loading clearly. A globally paginated list cannot masquerade as the complete board.
- Define reopening/backward moves explicitly. Marking Converted records sales outcome; it does not create an account, activate a subscription or prove paid revenue. Any organization link must be verified by staff/server access.

Proposed persistence: `DemoRequest` (fields, stage, assignee, source, follow-up, version), immutable `DemoRequestActivity` and internal notes. Index search/filter access patterns. Use shared delivery intents rather than an unrelated second mail queue.

### 4C. Platform access policy

Introduce a small explicit platform capability model, if not already present, before exposing sales data: `view_demo_requests` and `manage_demo_requests`. Owner has implicit authority and grants staff access. Invitation defaults do not automatically expose all sales records. Extend identity/query gating and enforce permissions at the API as well as navigation.

Proposed staff endpoints are under `/api/v1/superadmin/demo-requests`: list/board/detail queries and distinct assignment, transition, note and follow-up commands. Keep public intake entirely separate from platform-cookie endpoints.

**Verification:** website success/failure/validation/bot limits; persistence-before-receipt; retries create one request; no anonymous PII read; authorized staff visibility; unauthorized staff/CRM token rejection; per-column counts/loading; concurrent transitions; assignment eligibility/revoked assignee; timezone follow-ups; notification failure does not lose the enquiry; marketing text/analytics excludes entered personal data.

**Complete when:** a genuine test form submission appears in the authorized board, can be assigned and moved across stages, and its persisted activity survives reload. Form-only, toast-only or mocked board implementations do not complete this phase.

## Phase 5 — Basic customer support tickets

**Purpose:** customers can ask for help and follow a conversation; platform staff can triage and resolve it.

### 5A. Customer experience

- Add `/dashboard/support` and `/dashboard/support/[id]` using CRM layout/components. Add an intentional **Help & Support** navigation entry through the existing sidebar policy and a suitable help/contact link.
- Authenticated CRM users create tickets with subject, category, description and optional safe request reference/module context. Reporter identity and organization come from the authenticated scope, never submitted IDs.
- The default scope is **My tickets**: a requester can list/read/reply to their own tickets within their current organization. Organization administrators do not automatically gain visibility into colleagues' private support conversations. Broader organization-wide support access would require an explicit policy.
- Show ticket reference, customer-visible status, last activity and conversation. Allow customer replies and reopening a resolved ticket through a defined command. Customers cannot assign staff, set trusted priority or edit internal notes.
- Keep support usable for authenticated users with expired trials, without unlocking sales/customer business modules. Coordinate frontend lockout/navigation and backend subscription guards. Registration/account-recovery help remains outside this authenticated ticket flow.

### 5B. Super Admin support workspace

Add `/superadmin/support-tickets` and `/superadmin/support-tickets/[id]`. Use the shared CRM table/filter/detail patterns, not the sales demo board's domain model.

Basic version-one features:

- Unique human-readable ticket reference, requester/organization, category, subject, description, timestamps, optimistic version and assigned eligible platform staff.
- Server-backed status, priority, assignee, organization/date/search filters and counts. Priority defaults to Normal; staff can use Low/Normal/High/Urgent.
- Public replies and explicitly separate **internal notes**. Use distinct command/response contracts and prominent UI labels to prevent publishing a private note accidentally.
- Immutable activity for assignment, priority, status changes and reopening. Keep message order stable and paginated; do not discard conversation history during resolution.
- Configurable receipt/reply/status email notifications through durable delivery, with deduplication and safe deep links. Avoid embedding sensitive descriptions in notification subjects/bodies by default. Users read the protected portal for details; failed email does not lose the reply.
- Staff may create a ticket on behalf of an existing eligible customer via a separate platform command that validates the customer/organization association and records the actor.

Proposed workflow:

`Open → In Progress → Waiting for Customer → Resolved → Closed`

Allow an explicit Reopen transition to Open. Staff replies requesting information can set Waiting for Customer; a customer reply there returns it to Open. Replied-to resolved tickets reopen through the defined rule. Closed tickets require an explicit permitted reopen action. Define legal transitions centrally; do not let arbitrary strings update status.

Version one is a text conversation system. File attachments, inbound email parsing, automated SLA/escalation engines, live chat and AI replies are later enhancements unless separately added to scope. Safe textual request references and module context support the initial investigation flow.

### 5C. Backend and isolation

Create `support_tickets/{commands,queries,handlers,repositories,routes,services}` with `SupportTicket`, `SupportTicketMessage` and immutable `SupportTicketActivity` models/migrations. Use database uniqueness for ticket references and client operation IDs for duplicate submission/reply protection. Define behavior for account deletion and organization changes without granting access to former-organization conversations.

Customer API proposals under `/api/v1/support-tickets`: create, list mine, get permitted detail, add public reply and reopen. Reuse CRM `Scope` and protected browser-session transport. Repositories enforce requester **and** organization access on every lookup, message query and command.

Staff API proposals under `/api/v1/superadmin/support-tickets`: queue/detail plus assignment, priority, status, public reply, internal note and create-on-behalf commands. Extend Phase 4 capabilities with `view_support_tickets` and `manage_support_tickets`; retain platform sessions/MFA/CSRF and intentional cross-tenant authorization.

Internal messages must be excluded in customer query/serialization contracts, notification payloads and customer exports, not simply hidden in React. Customer errors must not reveal whether another tenant's ticket exists. Platform responses may expose only what the staff capability authorizes.

Feedback remains feedback. Add an audited, idempotent staff action to link/convert eligible feedback into a support ticket, preserving source provenance and requester eligibility; never migrate all ratings automatically. Later Phase 8 links support tickets to Error Center issues as many reports may describe one underlying failure. Customers see their support thread, not private stacks/logs or other reporters.

**Verification:** complete customer-create/staff-reply/customer-reply/resolve/reopen flow; cross-user and cross-tenant read/write/guess-ID denial; internal-note exclusion; forged reporter/priority rejection; non-privileged platform denial; duplicate replies/retry; concurrent edits; assigned account revocation; expired-trial support; notification failures; feedback conversion idempotency; CRM/platform transport separation.

**Complete when:** a customer can create and track their own ticket and exchange replies with authorized staff; internal notes never reach the customer; status/history survive reload; neither organization switching nor guessed IDs bypasses scope.

## Phase 6 — First operational release

**Purpose:** release the invited-staff, consistent-UI, demo and basic support workflows as verified working features.

Work:

1. Rehearse additive migrations and backfill on representative legacy data, inspect counts/collisions and confirm a single Alembic head. Keep a compatible rollback path.
2. Verify actual Super Admin/CRM/public origins, HTTPS cookies, API proxy, direct routes and aliases, browser refresh and idle expiry.
3. Test a controlled owner invitation through real SES: receipt, activation, password/MFA enrollment, later sign-in, resend/cancel/reset/revoke and owner recovery procedure.
4. Test a controlled website demo submission through persistence, staff assignment/stage moves and configured internal notification.
5. Test a customer support conversation across CRM and Super Admin, including internal notes, expired trial access and configured reply notifications.
6. Verify delivery dispatcher execution/cleanup and visible failures; complete UI comparison/accessibility and relevant CRM regression checks.
7. Update onboarding/support/demo runbooks and evidence-based feature inventory using the required status vocabulary. Document what is shipped versus still planned.

**Release gate:** all essential workflows work on staging with real proxy/email configuration and no new unresolved authorization/data-loss defects. Local mocked API tests are supporting evidence, not staging proof.

Deploy schema → compatible backend → frontend, with a coordinated access cutover and no dual lifecycle writers. If needed, rollback presentation or disable new creation while keeping compatible activation and existing support/demo records readable. Never reopen public staff applications or drop customer conversations as rollback.

No real invitation, customer message, provider infrastructure or deployment is performed merely by approving a planning document. Execute operational actions within the later authorized implementation/release scope.

## Phase 7 — Measured health and observability foundation

**Purpose:** make monitoring truthful and safe before collecting large diagnostic volumes.

- Fix/verify request IDs on unexpected 500s using request state, bounded header values, explicit traceback handling and response headers. Centralize recursive redaction before stdout, collection and export.
- Inventory intended business errors before changing blanket `ValueError` handling; preserve existing validation contracts while hiding internal diagnostics.
- Keep public probes minimal. Add guarded measured health for API/database/Redis, worker/scheduler heartbeat, collection backlog and provider freshness. Unknown data remains Unknown.
- Expand the existing platform capability model with `view_observability`, `manage_issues`, `export_diagnostics` and `configure_providers`. Do not replace sales/support capabilities or grant diagnostic access to all staff automatically.
- Define versioned telemetry/event schemas, source trust, release/environment IDs, grouping fingerprints and capture limits. Use installed Next.js reference docs for instrumentation/boundaries.
- Preserve the existing startup pipeline-data protection and test it; its old destructive caller is already absent in current source.

**Verification:** sanitized traceback and matching body/header reference; malformed IDs; concurrency isolation; nested secrets/SQL parameters absent; public diagnostics removed; capability/CSRF/revocation negatives; missing/stale worker signals; analytics outage does not mark the database down.

**Complete when:** health reflects measured observations, sensitive diagnostics are guarded, and capture contracts are safe. These correctness fixes are enabled fixes, not hidden behind analytics feature flags.

## Phase 8 — Error Center, durable collection and Logs

### 8A. Error Center metadata and UI

- Implement issue, occurrence, immutable activity and feedback-link persistence from the original plan. Add support-ticket-to-issue links without exposing diagnostic data to customers.
- Build All Failures, grouped issue list and issue detail: severity, assignee, comments, safe stack frames, trends, affected tenant counts, first/last occurrence, request/job logs and release verification.
- Preserve Open → Triaged → In Progress → Fix Deployed → Resolved and Reopened/Ignored/Duplicate transitions. Require reasons/duplicate targets/verification evidence where applicable.
- Implement versioned fingerprints, stable delivery IDs, atomic occurrence counts and expected-version edits. Expected 401/403/409/422 failures remain classified with manual promotion/configurable thresholds.
- Validate release chronology for reopening. Late failures from an older release cannot reopen a verified fix simply because they arrived later.

Local fixtures may complete the workflow UI, but automatic production capture stays off until 8B passes.

### 8B. Independent production collection

- Confirm AWS compute/region, approved resources and Vercel drain entitlement/signatures before provisioning. Use the prior independent collector/dedicated durable queue/log-store proposal as the design starting point and verify current provider requirements at implementation.
- Cover browser exceptions/rejections/boundaries, Next.js server/proxy failures, FastAPI requests, worker/scheduler jobs, integrations/webhooks, imports/exports/governance and infrastructure/deployments.
- Keep trust enrichment, redaction, quotas, stable event IDs, retries/dead-letter handling, private release source maps and worker correlation propagation consistent.
- Collect outside failed CRM transactions and independently of FastAPI availability. Prevent telemetry feedback loops and isolate collection from CRM business jobs.

### 8C. Logs and linked investigations

- Build Runtime Logs, Business Audit and Platform Security views, with time/environment/service/severity/organization/module/release/request/trace/job/issue filters.
- Include saved searches, bounded auto-refresh, error-context links, log-to-ticket promotion and audited protected exports. A promoted runtime failure becomes an Error Center issue; a customer conversation remains a support ticket.
- Use server-built constrained queries, start/poll/cancel, approved log groups, query budgets and operator-bound handles. Pagination uses bounded snapshots/cursors with explicit truncation rather than unlimited provider scrolling.
- Add retention/purge controls and visible lag/drop/freshness. Earlier planning defaults are 30 days searchable logs, 90 days occurrences and 12 months issue history, subject to confirmed policy; retain existing business-audit policy separately.

**Verification:** one thousand distinct occurrences of the same failure group correctly; replay counts once; conflicting edits return conflicts; old/new-release reopening is correct; FastAPI/database outages preserve accepted events; worker restart/retry is idempotent; no recursive collection; private diagnostics/cross-tenant authorization/export redaction; query cancellation/limits; saved-search privacy; support/feedback links preserve their source access rules.

**Complete when:** a synthetic real application failure reaches independent collection, appears in All Failures/grouped issues, links to bounded logs and can be triaged/resolved with a preserved history. Production enablement requires the outage/replay/retention checks, not just rendered screens.

## Phase 9 — Analytics, alerts and final operational rollout

**Purpose:** deliver the original usage/traffic goals and actionable operational oversight.

### 9A. Analytics contracts and collection

- Preserve and verify existing consent-aware public Vercel/Mixpanel integration. Do not reinstall SDKs or restore an unidentified older commit.
- Add curated events for onboarding, module views, import attempts/completions, governance actions, reports and subscription changes. Define authoritative post-commit backend events and delivery deduplication.
- Add demo form submission/stage outcomes and support aggregate events only as allowlisted non-content metadata; exclude names/emails/phones, form answers, ticket text, identifiers without an approved purpose and private notes.
- Keep opaque user/organization identities, production/preview separation, consent handling and identity reset on logout/tenant switching. No autocapture/session replay by default. Exclude platform authentication and sensitive routes, including short host aliases.

### 9B. Reports and controls

- Build `/superadmin/analytics` with traffic/page popularity/referrer/device reports, active users/organizations, module adoption, onboarding/import/conversion funnels, retention cohorts, import success/failure, governance/report usage and separate demo/support summaries.
- Distinguish provider-derived usage from operational database counts. Define reporting window/timezone, activity, conversion and freshness. Demo Converted is a sales stage, not proof of subscription revenue.
- Use server-only reporting credentials, bounded cached adapters, complete query keys, rate limits, timeouts and explicit unavailable/configuration/lag states.
- Provide authorized provider enable/disable controls, ingestion health, budget visibility and degraded-state indicators. Verify plan entitlements/reporting APIs before promising specific reports; missing entitlement is an explicit deployment dependency, not a fabricated chart.

### 9C. Alerts and operations

- Configure authorized recipients/channels and alerts for critical error rates, collector/mail lag, dead-letter backlog and measured service failure. Keep delivery disabled until recipients and integration configuration are verified.
- Verify purge/retention, diagnostic export audit, incident triage and access revocation across sales/support/observability. Keep independent provider-console/alert access during portal outages.
- Run synthetic traffic/funnel, failed-job and provider-outage scenarios, then enable features gradually in staging/production with distinct kill switches. Safety fixes remain enabled during telemetry rollback.

**Complete when:** provider reports reflect verified test events, configured alerts reach their intended destinations, blocked analytics cannot break login/demo intake/ticket replies/CRM writes, and the operational runbook and full feature inventory are accurate.

## Verification and completion rules across phases

Use the master plan's existing command inventory as the baseline. From the frontend, run focused ESLint during work and TypeScript/localization plus relevant Node/Playwright fixtures. Full lint/build are release checks. From the backend, use the existing venv and targeted pytest files; unit tests use SQLite/fake Redis. Use a verified test-only PostgreSQL database for concurrency/migration cases.

Extend current `test_platform_auth.py`, `test_platform_auth_postgres.py` and `test_platform_auth_browser.mjs`; retain relevant security assertions rather than leaving obsolete public access paths enabled. Add focused demo-intake/board and support-scope/conversation/delivery tests, plus real-CSS visual/browser flows for the new screens. Filenames for new tests are chosen during implementation and are not claimed to exist today.

Every phase completion report records:

1. Working user flows and API/migration changes.
2. Actual checks run and results, with existing failures distinguished from regressions.
3. Visual evidence where UI changed and authorization/concurrency evidence where applicable.
4. Remaining deployment/provider inputs and any feature deliberately disabled pending those inputs.
5. Updated runbooks/feature status and the next phase dependency.

After code changes run the required `graphify update .` once tooling is repaired. Planning/documentation-only changes require no graph refresh. Do not run broad unrelated suites repeatedly or create tests that merely duplicate CSS implementation details.

## Configuration needed by phase

| Input | Needed for | Local work without it |
|---|---|---|
| Existing MFA key and current owner/recovery state | Compatible deployed staff onboarding | Synthetic owner/key fixtures |
| SES sender/permissions, portal/CRM origins and running dispatcher | Phase 6 real staff/demo/support notification verification | Fake delivery and durable-intent tests |
| Approved staff grants, demo assignees and notification recipients | Phase 4–6 operational setup | Synthetic assignments and owner-only testing |
| Public contact/privacy copy and enquiry retention policy | Publishing Phase 4 form | Reviewable draft/local form |
| Support categories, authorized staff and retention policy | Phase 5–6 operational setup | Proposed category/workflow fixtures |
| AWS/Vercel infrastructure access, region, collection budget and retention | Phase 8 production collection | Local collectors/log adapters/fixtures |
| Vercel/Mixpanel project, region and reporting permissions | Phase 9 real reporting | Provider response fixtures |
| Alert destinations and channels | Phase 9 incident notifications | Disabled transport/recorded synthetic alerts |

Configure private values through local environment/deployment secret tooling. Plans, test output, browser bundles and messages must not contain those values. API keys are not a prerequisite for beginning Phases 0–5 with fixtures, but real delivery must be proven before declaring the related operational feature released.

## Feature coverage map

| Requirement | Delivery phase |
|---|---|
| Owner invitations, activation, MFA, resend/cancel/reset/revoke | 1–2; verified live in 6 |
| Complete CRM UI parity and current page behavior | 2–3 |
| Public Request a demo and persisted sales intake | 4A |
| Demo board/list, assignments, stages, follow-ups, history | 4B–4C |
| Customer create/track/reply/reopen support tickets | 5A–5C |
| Staff support queue, priorities, public replies/internal notes | 5B–5C |
| Reliable invitation/demo/support notifications | 1 foundation; 4–6 integration |
| Feedback-to-support and support-to-error relationships | 5 and 8 |
| Measured health, guarded diagnostics and capabilities | 4–5 domain access; 7 diagnostic access |
| All Failures, grouped issues, assignment/comments/status/fix verification | 8A–8C |
| Entire instrumented application capture and durable outage collection | 8B |
| Runtime/business/security logs, saved searches, refresh/context/promotion | 8C |
| Bounded log queries/cancel/export, retention/redaction/audit | 7–8C |
| Vercel traffic and Mixpanel adoption/funnels/retention | 9A–9B |
| Provider controls, freshness/budgets, alerts and operations | 9B–9C |
| Migration, security/concurrency checks, staged rollout and rollback | Every relevant phase; operational gates 6, 8 and 9 |

Optional later improvements from the original plan remain optional: trace waterfalls, formal availability/performance objectives, richer tenant-impact and cost dashboards, external issue-tracker integration. New optional improvements include configurable demo pipelines/calendar booking and support attachments/email ingestion/SLA automation. None substitutes for a required phase above.
