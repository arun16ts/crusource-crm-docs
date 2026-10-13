# Crusource CRM — Product Requirements Document

| Field | Value |
| --- | --- |
| Product | Crusource CRM |
| Document type | Product Requirements Document (PRD) |
| Version | 1.1  |
| Status | Draft for product/stakeholder review |
| Prepared | 28 September 2026 |
## 1. Purpose and product definition

Crusource CRM is a multi-tenant sales workspace for capturing prospects, managing customer relationships and opportunities, coordinating sales activity, and giving teams controlled visibility into revenue work. It combines core CRM records with pipeline management, campaign outreach, documents, reports, collaboration, governance, and AI-assisted retrieval.

This PRD defines the product baseline represented by the current application. It is intentionally an **as-built PRD**: requirements marked **IMPLEMENTED** have an end-to-end UI/API flow in the codebase; **PARTIALLY IMPLEMENTED** capabilities need deliberate product completion; and **PLANNED / DOCUMENTED ONLY** items are proposals, not commitments. It is not a promise that every item advertised in public copy is available in every deployment—external features depend on configured credentials, storage, and providers.

### 1.1 Product vision

Give revenue teams one secure, organization-scoped system where a prospect can move from capture to qualified lead, account/contact, deal, activity, documented customer history, forecast, and close—without losing context or bypassing ownership and approval controls.

### 1.2 Problem statement

Sales teams commonly keep lead data, meeting history, inbox conversations, documents, and pipeline status in separate tools. This creates duplicate records, unclear ownership, weak handoffs, unreliable forecasts, and limited auditability. Administrators also need to govern access and recover data without making ordinary sales work cumbersome.

### 1.3 Product principles

1. **Customer context stays connected.** Leads, contacts, accounts, deals, activities, notes, documents, and communications must be linkable and discoverable from the relevant record.
2. **Tenant isolation and least privilege are non-negotiable.** Every protected operation is organization-scoped and subject to role, module, setup, and record-access rules.
3. **Sales work should be fast.** Lists, pipeline boards, quick actions, search, contextual drawers, bulk operations, and calendar views reduce needless navigation.
4. **Automation must remain observable.** Campaign processing, calendar synchronization, and AI responses should expose status, failures, and useful provenance.
5. **Configuration should be intentional.** Pipelines, permissions, roles, teams, templates, and organization settings are controlled through administrative surfaces.

## 2. Goals, non-goals, and success measures

### 2.1 Goals

- Provide a complete daily workspace for individual contributors to capture, qualify, organize, and progress sales work.
- Give managers visibility into pipeline health, activity, team work, and revenue forecasts.
- Give administrators secure organization, user, role, access, data-management, and governance controls.
- Support an auditable lead-to-revenue lifecycle and reduce duplicate/re-keyed information.
- Allow integrations and AI assistance to enrich CRM work while preserving tenant boundaries and user control.

### 2.2 Non-goals for this baseline

- Replace a full finance/ERP system, customer-support platform, marketing automation suite, or general-purpose file-drive product.
- Guarantee autonomous AI actions. Loop AI is an assistant/retrieval experience; it must not silently change CRM data.
- Promise a generic integration marketplace. Current verified product integrations are Google Workspace and All Buddy; Zoho OAuth endpoints exist but should be treated as integration work requiring validation, not a universally available marketplace feature.
- Offer unlimited data retention, storage, email delivery, or third-party-provider availability independent of plan/configuration.

### 2.3 Outcome metrics

Product owners should establish a baseline before setting targets. Suggested release measures are:

| Outcome | Measure | Initial target / guardrail |
| --- | --- | --- |
| Activation | Organizations completing setup and creating/importing a first record | Target defined after baseline |
| Sales velocity | Median time from new lead to first logged activity and to conversion | Improve quarter over quarter |
| Data quality | Duplicate detection rate, required-field completion, and records with owner | Trend upward; no tenant data leakage |
| Pipeline reliability | Share of active deals with stage, amount, owner, and expected close date | Target defined per organization |
| Collaboration | Access/reassignment requests resolved within agreed SLA | Target defined per organization |
| Reliability | API error rate, failed campaign sends, failed calendar syncs | Instrumented and reviewable |
| Security | Unauthorized cross-organization access incidents | Zero tolerated |

## 3. Users and permissions

| Persona | Primary needs | Typical access |
| --- | --- | --- |
| Sales representative | Capture leads, maintain customer context, work tasks/meetings/calls, progress deals | Assigned modules and owned/shared records |
| Sales manager | Inspect pipeline, coach team, reassign work, approve controlled changes | Team-lead and manager permissions |
| Organization administrator | Configure users, teams, roles, profiles, pipelines, organization settings, audit/recovery | Setup permissions or administrator role |
### 3.1 Authorization requirements

- The system shall associate protected data with an organization and resolve access through the authenticated user scope.
- The system shall gate navigation and backend actions by effective module permissions, administrative/setup permissions, and record/team rules.
- The system shall not treat a visible client-side control as sufficient authorization; APIs must enforce scope and permission checks.
- Administrators shall be able to manage users, roles/profiles, teams, and organization configuration within their organization.
- A user without access to a record shall use the Team Space request path where enabled, rather than receive an unscoped record response.
- Security-relevant administration and record changes should be auditable and recoverable where the feature supports it.

## 4. End-to-end product journeys

### Journey A — New organization to productive workspace

1. A prospective customer opens the public site and registers with email/password or Google sign-in.
2. The system verifies email by OTP where applicable, creates/joins the organization context, and starts onboarding.
3. An administrator completes organization setup, invites users, assigns roles/profiles and teams, and configures pipelines/settings.
4. A representative imports or creates leads and begins daily work from dashboard, pipeline, calendar, and task views.

**Acceptance criteria:** registration and login are rate-limited where configured; verification, password reset, token refresh/logout, invitation acceptance, and Google OAuth paths are available; protected dashboard routes require authenticated scope.

### Journey B — Prospect to qualified opportunity

1. A representative creates or imports a lead, or receives one through an approved integration.
2. They qualify the lead, set ownership/source/stage, add notes and follow-up activities, and can move it through a lead pipeline.
3. The representative checks for duplicates, collaborates through related records, and updates the activity history.
4. They convert the lead into a contact, account, and optionally a deal, retaining appropriate associations.
5. The deal progresses through configured stages with amount, expected close date, products, loss data, and activity context.

**Acceptance criteria:** users with appropriate rights can create, search/filter, edit, bulk-manage, reassign, import/export, stage-move, and convert leads; conversion produces linked CRM entities according to selected options; all retrieval is tenant-scoped.

### Journey C — Daily sales execution

1. The user opens Dashboard to review KPIs, recent work, upcoming tasks, meetings, calls, and deals.
2. They use global search or record views to find customer context.
3. They create tasks, schedule/log meetings and calls, attach notes or documents, and update related lead/contact/account/deal records.
4. Calendar consolidates scheduled work; Google-connected users can synchronize qualifying meeting changes.

**Acceptance criteria:** activities support CRUD within permission scope; activity relationships are surfaced in record context; calendar supports operational month/week/day work; meeting sync failures do not expose tokens and are logged for diagnosis.

### Journey D — Team collaboration and controlled handoff

1. A manager/team lead manages a shared lead pool and team dashboard.
2. A user requests access to, or reassignment of, a restricted record when needed.
3. Authorized reviewers approve or reject the request; access/reassignment is applied and traceable.
4. Managers use team and pipeline insight to redistribute work and coach the team.

**Acceptance criteria:** Team Space availability is permission-aware; access and reassignment requests have explicit status; resulting visibility follows record-access rules, not merely UI state.

### Journey E — Campaign outreach and response monitoring

1. An authorized operator creates a campaign, defines an audience from leads/contacts, and composes content.
2. They send immediately or schedule delivery.
3. The system processes recipients, records sent/failed/skipped state, and presents campaign-level send/open/bounce/complaint data where available.
4. The operator investigates failures and cancels campaigns when necessary.

**Acceptance criteria:** campaign delivery requires configured email infrastructure; processing is asynchronous when queue mode supports it (or synchronous in the configured local mode); no unsupported click-tracking, pause/resume, or delivery guarantee is implied.

### Journey F — Govern, report, and recover

1. Administrators review users, roles, profiles, teams, pipelines, templates, organization settings, audit data, and login history.
2. Managers create/run saved reports, review analytics boards and forecasts, and use data export/import tools subject to permission.
3. Administrators review recovery/recycle-bin and data-administration surfaces where enabled. eview plan and quota state and use supported subscription actions.

**Acceptance criteria:** sensitive administration routes are permission-gated; report/analytics/forecast results are organization-scoped; partial administration capabilities must clearly communicate their supported workflow rather than appear complete.

## 5. Functional requirements

Statuses reflect the present product baseline.

### 5.1 Identity, onboarding, and organization

| ID | Requirement | Status |
| --- | --- | --- |
| IAM-01 | Users can register, authenticate, refresh/logout sessions, verify OTP, resend verification, and reset forgotten passwords. | IMPLEMENTED |
| IAM-02 | Users can authenticate or link supported Google accounts through OAuth, with a secure callback flow. | IMPLEMENTED |
| IAM-03 | Organizations can invite users and users can accept invitations. | IMPLEMENTED |
| IAM-04 | The product provides personal and organization onboarding checklists/journeys. | IMPLEMENTED |
| IAM-05 | User-facing dates, times, currencies, and numbers honor configured formatting preferences. | IMPLEMENTED |
| IAM-06 | Organization and profile settings support tenant identity, user profile/avatar, and Google linkage as permitted. | IMPLEMENTED |

### 5.2 Core CRM records

| ID | Requirement | Status |
| --- | --- | --- |
| CRM-01 | Leads support create/read/update/archive-delete, import/export, duplicate checks, filters, search, pagination, assignment, bulk actions, and pipeline/list views. | IMPLEMENTED |
| CRM-02 | A lead can be converted into a contact, account, and optional deal with retained associations. | IMPLEMENTED |
| CRM-03 | Contacts support account relationships, communication/profile fields, duplicate-email checking, related activities/content, reassignment, and bulk operations. | IMPLEMENTED |
| CRM-04 | Accounts support company data, parent-child hierarchy, owner management, related contacts/deals/activities/content, and bulk actions. | IMPLEMENTED |
| CRM-05 | Deals support list/Kanban views, pipelines/stages, amount/currency/probability, expected close, loss data, products, owners/teams, and related work. | IMPLEMENTED |
| CRM-06 | Each primary record provides a contextual detail experience with relevant notes, documents, attachments, related records, and activity history where applicable. | IMPLEMENTED |
| CRM-07 | Saved views preserve supported user/reporting contexts without duplicating the server record source of truth. | IMPLEMENTED |

### 5.3 Pipeline, forecast, and revenue operations

| ID | Requirement | Status |
| --- | --- | --- |
| REV-01 | Administrators can configure and seed supported lead/deal pipelines and stages. | PARTIALLY IMPLEMENTED |
| REV-02 | Users can move leads/deals across authorized pipeline stages, including drag-and-drop UI flows. | IMPLEMENTED |
| REV-03 | Stage history is retained for supported pipeline entities. | IMPLEMENTED |
| REV-04 | Forecast provides pipeline value, weighted value, won value, and stage/owner breakdowns. | IMPLEMENTED |
| REV-05 | Analytics boards provide saved visual dashboards, widgets, and supported drill-downs. | IMPLEMENTED |
| REV-06 | Reports provide saved reports, builder/preview/filter/run/share flows. | IMPLEMENTED |

### 5.4 Activities, calendar, inbox, and notifications

| ID | Requirement | Status |
| --- | --- | --- |
| ACT-01 | Users can create, edit, complete, assign, filter, bulk-manage, and relate tasks to CRM records. | IMPLEMENTED |
| ACT-02 | Users can create, update, cancel, and review meetings, attendees, agendas, action items, and meeting history. | IMPLEMENTED |
| ACT-03 | Users can log and manage calls with disposition, duration, recording metadata, and related records. | IMPLEMENTED |
| ACT-04 | Calendar provides month/week/day planning across applicable tasks, meetings, and calls. | IMPLEMENTED |
| ACT-05 | Connected Google users can synchronize meeting information and attendee RSVP state with Google Calendar. | IMPLEMENTED (provider-dependent) |
| ACT-06 | Gmail-connected inbox experiences expose threads/messages and connect available email context to customer work. | IMPLEMENTED (provider-dependent) |
| ACT-07 | Header/drawer notifications support unread/read state and mark-one/mark-all flows. | IMPLEMENTED |
| ACT-08 | Global notes and record notes support scratchpad and record-context work, mentions/search/pagination where provided. | IMPLEMENTED |

### 5.5 Documents and templates

| ID | Requirement | Status |
| --- | --- | --- |
| DOC-01 | Users can upload, organize, update, download, assign, and remove documents within access scope. | IMPLEMENTED |
| DOC-02 | Documents support folders, version handling, recycle-bin workflows, and supported in-app spreadsheet/DOCX editing. | IMPLEMENTED |
| DOC-03 | Authorized users can create, revoke, and consume tokenized public share links. | IMPLEMENTED |
| DOC-04 | Administrators/users can manage reusable templates and create documents from them. | IMPLEMENTED |

### 5.6 Campaigns, search, AI, and integrations

| ID | Requirement | Status |
| --- | --- | --- |
| ENG-01 | Users can create, edit, send/schedule, cancel, and inspect email campaigns and recipient results. | IMPLEMENTED (delivery-dependent) |
| ENG-02 | Campaign statistics include supported sent, failed, opened, bounced, and complaint data. | IMPLEMENTED |
| ENG-03 | Global search returns grouped, entity/type-filterable, tenant-scoped CRM results; recent/saved searches are supported. | IMPLEMENTED |
| ENG-04 | Authenticated Loop AI streams answers grounded in retrieved CRM context, maintains user/session history, and returns citations metadata. | IMPLEMENTED (AI-provider-dependent) |
| ENG-05 | Public Loop AI answers marketing/product questions with rate limiting. | IMPLEMENTED |
| ENG-06 | Embedding synchronization can index organization CRM records for AI retrieval. | IMPLEMENTED (AI-provider-dependent) |
| ENG-07 | Google Workspace integration supports OAuth, calendar synchronization, and Gmail-linked experience where configured. | IMPLEMENTED (provider-dependent) |
| ENG-08 | All Buddy is presented as an event/card-scanning partner integration; operational lead ingestion requires an enabled partner integration contract. | DOCUMENTED ONLY |
| ENG-09 | Zoho OAuth connection/callback endpoints exist; full product UX, sync model, and operational readiness require validation before release commitment. | PARTIALLY IMPLEMENTED |

### 5.7 Collaboration, administration, billing, and governance

| ID | Requirement | Status |
| --- | --- | --- |
| ADM-01 | Admin Hub supports user, team, role, profile, and organization management. | IMPLEMENTED |
| ADM-02 | Roles/profiles define module CRUD and setup access; team leadership and record permissions narrow operational access. | IMPLEMENTED |
| ADM-03 | Team Space provides lead-pool work, dashboards, record-access requests, reassignment requests, and record-permission workflows. | PARTIALLY IMPLEMENTED |
| ADM-04 | Approvals manage controlled access and mass-change requests with approval/rejection history. | PARTIALLY IMPLEMENTED |
| ADM-05 | Data administration exposes supported CSV import/export, backup, storage, audit, login-history, and recovery/recycle-bin flows. | PARTIALLY IMPLEMENTED |
| ADM-06 | Billing presents plans, subscription status, usage/quotas, and supported change/cancel/resume/trial actions. | PARTIALLY IMPLEMENTED |
| ADM-07 | The platform records audit logs and login history for supported governance investigations. | PARTIALLY IMPLEMENTED |

## 6. Information architecture and UX requirements

### 6.1 Public experience

The public site shall provide landing, sign-in/registration, verification/recovery, invitation acceptance, integrations, FAQ/docs, unsubscribe, and public shared-document pages. Public pages must never expose private organization records. The public Loop AI endpoint must be rate-limited.

### 6.2 Authenticated navigation

The dashboard shell shall require authentication and present a permission-filtered sidebar:

| Navigation group | Destinations |
| --- | --- |
| Analytics | Reports, Analytics, Forecast |
| Sales | Leads, Contacts, Accounts, Deals, Documents, Campaigns |
| Activities | Tasks, Meetings, Calls; Calendar is additionally reachable in the workspace |
| Team Space | Teams Pool, Teams Dashboard, requests/pool work areas |
| Administration | Admin Hub, Organization, Billing and permitted child areas |

Global header/drawer surfaces may provide search, notifications, inbox, notes, and AI. A new module must have an intentional navigation and permission decision; a route alone is not a complete product feature.

### 6.3 Interaction standards

- Long CRM lists shall support server-side searching, filtering, sort, and pagination where the module provides them.
- List/pipeline mode, filters, sort, tabs, and pagination that users may share or revisit should use URL state.
- User-facing destructive actions must require explicit confirmation and use recoverable soft-delete/recycle patterns when the module supports them.
- Forms shall validate client inputs and APIs shall revalidate all requests.
- Loading, empty, permission-denied, and recoverable error states shall be explicit.
- The UI shall be responsive for supported browser widths and keyboard-accessible for core actions.

## 7. Non-functional requirements

### 7.1 Security and privacy

- Authentication uses access/refresh token flows with secure password handling and rate limiting on sensitive account endpoints.
- Production startup must reject insecure/default secret configuration; production API documentation is disabled unless expressly enabled.
- CORS origins must be configuration-controlled; broad development allowances must not become production defaults.
- Organization scope and permission guards are mandatory in repositories/handlers/routes for protected data access.
- OAuth, email, AI, storage, and database credentials must remain environment configuration and must never be logged or committed.
- Public document sharing must use unguessable/revocable tokens and expose only explicitly shared content.
- Audit trails and login history should support investigation of supported actions; retention and immutability policies require product/legal approval.

### 7.2 Reliability and operational behavior

- The API shall expose health checks and structured/correlation-aware logging.
- Startup shall verify database connectivity; production failures must fail safely.
- Background scheduling shall start and stop cleanly. Google Calendar polling is scheduled every five minutes in the current application and should tolerate revoked credentials and individual-user failures.
- Queue mode defaults to synchronous local execution; deployment owners must configure workers/Redis for asynchronous workloads as required.
- Email, calendar, AI, S3, and other third-party failures shall yield actionable status/errors without leaking secret values.
- Database schema changes shall use Alembic migrations and receive rollback/upgrade testing appropriate to risk.

### 7.3 Performance and scale

- The UI should avoid blocking full-page transitions for routine CRM actions; server state is cached/managed through TanStack Query.
- API queries must paginate collection results and include response-affecting filter/sort parameters in cache/query keys.
- Large imports, exports, campaign sends, document processing, embedding synchronization, and calendar polling must be bounded, observable, and moved to worker execution when operational scale requires it.
- Product performance targets (e.g., p95 API/list response, dashboard load, campaign queue latency) are pending production baselining and should be adopted before a GA SLA.

### 7.4 Accessibility, localization, and compatibility

- Core interaction must be operable by keyboard and use semantic labels, focus management, and adequate contrast.
- User-visible dates, times, numbers, and currencies shall use centralized formatting helpers rather than ad hoc browser formatting.
- The initial localization model is formatting-aware; full multilingual UI/content translation is PLANNED / DOCUMENTED ONLY.
- Supported browser/device matrix, accessibility conformance level, and formal data-retention policy require stakeholder sign-off.

## 8. Data model and lifecycle requirements

### 8.1 Core entities

| Domain | Key entities |
| --- | --- |
| Identity & tenancy | Organization, User, role/profile, team, permission, login history |
| CRM | Lead, Contact, Account, Deal, product, pipeline, pipeline stage, stage history, saved view |
| Activities | Task, Meeting, attendee, action item, meeting history, Call, Note, Notification |
| Content | Document, folder/version/share link, attachment, template |
| Engagement | Campaign, campaign recipient, tracked inbox thread/message |
| Governance | Audit log, approval/request, record permission, reassignment/access request, recovery data |
| Intelligence | AI chat history, embedding/indexed retrieval context |

### 8.2 Integrity rules

- Every business record that requires tenant separation shall carry or resolve an organization relationship.
- Leads, contacts, accounts, and deals shall retain explicit relationship records/foreign keys as defined by the domain.
- Conversion must avoid silently creating duplicate customer entities when matching/conflict handling is available.
- Activity, note, attachment, document, and communication links must validate their parent record access.
- Meeting end time must be later than start time; integrations shall correct or reject invalid temporal state.
- Soft-delete/recovery behavior must be consistent with the module’s recycle-bin contract and authorization policy.
- Tenant IDs, ownership, and audit attribution must never be client-authoritative.

## 9. Architecture and integration constraints

| Layer | Requirement |
| --- | --- |
| Frontend | Next.js App Router with React, Tailwind, service-layer API calls, TanStack Query for server state, Redux only for shared client/UI state. |
| Backend | FastAPI with SQLAlchemy and Alembic. Modules use commands, queries, handlers, repositories, routes, and services. |
| Data | PostgreSQL in deployed environments; tests use isolated/in-memory facilities where applicable. |
| Background work | Scheduler plus Redis/worker-capable queue model; local default may run synchronously. |
| Files | Configurable storage service with document/attachment authorization and public-share safeguards. |
| AI | Gemini provider and retrieval/embedding services; provider configuration and output quality must be monitored. |
| Google | OAuth-linked identity/calendar/email capabilities; consent scopes, token renewal, and provider availability are external dependencies. |
| Deployment | Docker Compose supports full-stack deployment; native frontend/backend development is also supported. |

The product shall preserve these boundaries: route functions validate/authorize/delegate; handlers represent meaningful use cases; repositories own persistence/query construction; integrations are isolated in services/modules; UI components do not embed API-base/token-refresh logic.

## 10. Release readiness and acceptance plan

### 10.1 Minimum release gates

1. **Security:** scoped authorization tests cover cross-organization access, role/module permission changes, document/attachment parent authorization, and public-link revocation.
2. **Core lifecycle:** a user can create/import a lead, manage it, convert it, create/progress a deal, and retrieve related customer history.
3. **Operational activities:** tasks, meetings, calls, calendar, and notifications work with permission-aware records.
4. **Governance:** administrator can invite/manage users and review supported roles/teams/audit/recovery surfaces.
5. **Quality:** focused backend pytest and frontend lint/type/test checks pass for changed modules; no new critical accessibility or security defect remains.
6. **Deployment:** production secrets, database migrations, CORS, storage, email, Google OAuth, AI provider, worker/scheduler, and observability settings are validated in the target environment.

### 10.2 Feature acceptance test matrix

| Scenario | Expected evidence |
| --- | --- |
| Authentication | Register, verify, login, refresh, logout, reset password, OAuth callback, invitation acceptance all give safe user feedback. |
| Tenant isolation | A user from Organization A cannot retrieve, mutate, attach to, search, or export Organization B data. |
| Lead conversion | Converted records and associations are created once, visible only to authorized users, and appear in relevant detail views. |
| Pipeline | Authorized stage moves update state/history; invalid/unpermitted moves are rejected. |
| Campaign | Audience validation, send/schedule/cancel state, recipient outcomes, and provider errors are visible; failed delivery is not reported as sent. |
| Documents | Authorized upload/download/share/revoke works; revoked token no longer grants public access. |
| Calendar integration | Connected user changes synchronize as designed; expired/revoked access is handled without crashing the job. |
| AI | Authenticated answer streams with citations; history is isolated by organization/user/session; unsafe provider failure is recoverable. |
| Administration | Permission changes take effect; protected setup/data endpoints reject unauthorized users. |

## 11. Risks, assumptions, and dependencies

| Area | Risk or assumption | Mitigation / decision needed |
| --- | --- | --- |
| External providers | Google, email, S3, Gemini, and partner services can be unavailable, rate-limited, or misconfigured. | Status visibility, retries where safe, configuration validation, provider monitoring, documented fallback. |
| PARTIALLY IMPLEMENTED modules | Analytics, reports, forecast, Team Space, approvals, data admin, billing, audit/recovery, pipelines, and integrations contain incomplete workflows. | Define completion criteria and hide/label unfinished actions; do not market incomplete features as complete. |
| AI accuracy | Retrieval or model output can be incomplete or wrong. | Ground answers in scoped context/citations; keep assistant read-only; capture feedback and evaluate quality. |
| Multi-tenancy | A scope/authorization regression is high impact. | Defense in depth in guards, handlers, repositories, tests, code review, and audit logging. |
| Background jobs | Sync/campaign work may behave differently in synchronous local mode versus worker deployment. | Test both execution paths; define idempotency, retry, and operational dashboards. |
| Data lifecycle | Retention, backup, deletion, and legal/compliance obligations are not fully specified here. | Obtain legal/security policy approval before GA. |
| Public product copy | Some copy makes performance/security claims that require measurable evidence. | Align marketing language with verified product SLOs and implemented controls. |

## 12. Source-of-truth and maintenance

This PRD is maintained documentation. Update it when a user-visible requirement changes, a partial capability is completed, or a launch decision is made. Status labels must use the following vocabulary exactly: `IMPLEMENTED`, `PARTIALLY IMPLEMENTED`, `BACKEND ONLY`, `INTERNAL`, `PLANNED / DOCUMENTED ONLY`.