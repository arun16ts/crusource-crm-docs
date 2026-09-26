# Crusource CRM — Modules & Features
## Product & Capability Overview

**Product:** Crusource CRM  
**Snapshot:** 26 September 2026

## 1. Application Overview

Crusource CRM is a multi-tenant web application for managing sales prospects, customer relationships, deals, campaigns, activities, documents, analytics, collaboration, and organization administration.

| Area | Description |
|---|---|
| Application type | Multi-tenant CRM web application |
| Frontend | Next.js application with an authenticated dashboard and public account/integration pages |
| Backend | FastAPI application exposing REST APIs, background schedulers, and integration endpoints |
| Primary users | Sales representatives, sales managers, team leads, administrators, and organization members |
| Main business objects | Leads, contacts, accounts, deals, campaigns, tasks, meetings, calls, notes, documents, users, teams, and organizations |
| Data scope | Records are associated with organizations and access is further controlled by module, setup, team-lead, and administrative permissions |
| Repository snapshot | Reviewed on 2026-09-26 from the current frontend and backend source, cross-checked against the generated `graphify-out` knowledge graph |

The authenticated product is organized around a permission-filtered dashboard sidebar. Some destinations and tools, such as Calendar, Inbox, the global notes drawer, Team Space request management, and individual record detail drawers, are reached from other screens or the header rather than being permanent sidebar entries.

Implementation evidence: `crusource-crm-frontend/src/app`, `crusource-crm-frontend/src/components/layout/Sidebar.tsx`, `crusource-crm-frontend/src/components/layout/sidebar/sidebarConfig.ts`, `crusource-crm-backend/src/main.py`.

## 2. Application Navigation

### Public and account-access routes

| Route | Purpose | Status |
|---|---|---|
| `/` | Public landing page | IMPLEMENTED |
| `/login` | Sign in | IMPLEMENTED |
| `/forgot-password` | Request a password reset | IMPLEMENTED |
| `/reset-password` | Set a new password | IMPLEMENTED |
| `/signin` | Sign in | IMPLEMENTED |
| `/sign-in` | Sign-in alias/entry page | IMPLEMENTED |
| `/register` | Create an account | IMPLEMENTED |
| `/accept-invite` | Accept an organization invitation | IMPLEMENTED |
| `/auth/callback` | OAuth callback route | IMPLEMENTED |
| `/verify-email` | Email verification flow | IMPLEMENTED |
| `/onboarding` | Public onboarding entry page | IMPLEMENTED |
| `/unsubscribe` | Email unsubscribe page | IMPLEMENTED |
| `/shared/document/[token]` | Public shared-document view | IMPLEMENTED |
| `/integrations` | Public integrations and supported-setup page | IMPLEMENTED |
| `/docs` | Public product/help area | IMPLEMENTED |
| `/faq` | Public frequently asked questions page | IMPLEMENTED |

### Main dashboard navigation

The sidebar definition is in `crusource-crm-frontend/src/components/layout/sidebar/sidebarConfig.ts:40`; permission filtering and dynamic visibility are applied in `crusource-crm-frontend/src/components/layout/Sidebar.tsx:59-78`.

| Section | Destination | Access behavior |
|---|---|---|
| Dashboard | `/dashboard` | Always shown in the dashboard shell |
| Analytics | Reports — `/dashboard/reports` | Requires effective `reports` or `analytics_boards` view access |
| Analytics | Analytics — `/dashboard/analytics` | Requires effective `analytics` or `analytics_boards` view access |
| Analytics | Forecast — `/dashboard/forecast` | Requires effective `forecast` view access |
| Sales | Leads — `/dashboard/leads` | Requires effective `leads` view access |
| Sales | Contacts — `/dashboard/contacts` | Requires effective `contacts` view access |
| Sales | Accounts — `/dashboard/accounts` | Requires effective `accounts` view access |
| Sales | Deals — `/dashboard/deals` | Requires effective `deals` view access |
| Sales | Documents — `/dashboard/documents` | Requires effective `documents` view access |
| Sales | Campaigns — `/dashboard/campaigns` | Requires effective `campaigns` view access |
| Activities | Tasks — `/dashboard/tasks` | Requires effective `tasks` view access |
| Activities | Meetings — `/dashboard/meetings` | Requires effective `meetings` view access |
| Activities | Calls — `/dashboard/calls` | Requires effective `calls` view access |
| Team Space | Teams Pool — `/dashboard/teamspace` | Available to admins, team leads, and users with team/teamspace access; shows pending-request count |
| Team Space | Teams Dashboard — `/dashboard/teamspace/dashboard` | Available to admins, team leads, and users with team/teamspace access |
| Administration | Admin Hub — `/dashboard/admin/users` | Available to admins or users with the applicable setup permissions |
| Administration | Organization — `/dashboard/organization` | Organization-settings access |
| Administration | Billing — `/dashboard/billing` | Billing/setup access |

### Additional destinations

| Area | Routes | Navigation behavior | Status |
|---|---|---|---|
| Calendar | `/dashboard/calendar` | FullCalendar month/week/day work | IMPLEMENTED |
| Inbox | `/dashboard/inbox` | Gmail-powered inbox and message-detail workspace | IMPLEMENTED |
| Settings | `/dashboard/settings` | Reached from the sidebar profile menu | IMPLEMENTED |
| Settings | `/dashboard/settings/feedback` | In-product feedback form | IMPLEMENTED |
| Settings | `/dashboard/settings/onboarding` | Personal onboarding checklist | IMPLEMENTED |
| Organization onboarding | `/dashboard/organization/onboarding` | Organization setup journey | IMPLEMENTED |
| Team Space requests | `/dashboard/teamspace/requests` | Record-access and reassignment requests | IMPLEMENTED |
| Team Space pool | `/dashboard/teamspace/pool` | Lead-pool work area | IMPLEMENTED |
| Administration | `/dashboard/admin`, `/dashboard/admin/teams`, `/dashboard/admin/roles`, `/dashboard/admin/profiles`, `/dashboard/admin/templates` | Admin-hub child destinations | IMPLEMENTED |
| Administration | `/dashboard/admin/pipeline`, `/dashboard/admin/approvals` | Pipeline and approval configuration/work areas | PARTIALLY IMPLEMENTED |
| Administration | `/dashboard/admin/automations` | Placeholder page only; the `automations` setup permission currently gates the approvals API | PARTIALLY IMPLEMENTED |
| Administration | `/dashboard/admin/data-import`, `/dashboard/admin/data-export` | CSV import and export administration | PARTIALLY IMPLEMENTED |
| Administration | `/dashboard/admin/data-backup`, `/dashboard/admin/storage` | Data and storage administration areas | PARTIALLY IMPLEMENTED |
| Administration | `/dashboard/admin/audit`, `/dashboard/admin/login-history`, `/dashboard/admin/recycle-bin` | Security, history, and recovery areas | PARTIALLY IMPLEMENTED |

Implementation evidence: `crusource-crm-frontend/src/app`, `crusource-crm-frontend/src/components/layout/sidebar`, `crusource-crm-frontend/src/hooks/queries/useMyPermissions.ts`.

## 3. Module Overview

| Module | Purpose | Main Features | Status |
|---|---|---|---|
| Dashboard | Daily CRM work overview | KPIs, recent leads, activities, tasks, meetings, calls, deals, quick actions | IMPLEMENTED |
| Analytics | Visual performance analysis | Saved charts, dashboards, KPI widgets, drill-downs | PARTIALLY IMPLEMENTED |
| Reports | Operational and sales reporting | Saved reports, report builder, preview, filters, run/share APIs | PARTIALLY IMPLEMENTED |
| Forecast | Pipeline and revenue visibility | Pipeline value, weighted value, won values, stage and owner breakdowns | PARTIALLY IMPLEMENTED |
| Leads | Prospect management | List and pipeline views, qualification, assignment, conversion | IMPLEMENTED |
| Contacts | Stakeholder management | Contact directory, company relationships, engagement history, activities | IMPLEMENTED |
| Accounts | Company management | Account hierarchy, contacts, deals, activities, documents, bulk actions | IMPLEMENTED |
| Deals | Opportunity and pipeline management | Kanban/list views, pipelines, products, activities, forecasting, saved views | IMPLEMENTED |
| Campaigns | Bulk outreach management | Campaign creation, recipients, email sending, statistics, automated statuses | IMPLEMENTED |
| Pipelines | Sales-stage configuration | Lead and deal stages, standard lead-pipeline seed, stage history | PARTIALLY IMPLEMENTED |
| Tasks | Follow-up work management | Tasks, priorities, due dates, assignment, bulk actions, notes | IMPLEMENTED |
| Meetings | Meeting and action-item management | Calendar events, attendees, agendas, action items, Google Calendar sync | IMPLEMENTED |
| Calls | Call-log management | Call records, dispositions, duration, recording metadata, related records | IMPLEMENTED |
| Calendar | Cross-activity scheduling | Month/week/day calendar, task, meeting, and call visualization | IMPLEMENTED |
| Global Notes | Global scratchpad and record notes | Header-opened notes drawer/notepad, notes on CRM records, inline mentions, search, pagination | PARTIALLY IMPLEMENTED |
| Documents | File and knowledge management | Upload, folders, versions, sharing, public links, recycle bin, in-app spreadsheet/DOCX editing | IMPLEMENTED |
| Search | Cross-module discovery | Global search modal, grouped results, entity/type filters, recent and saved searches | IMPLEMENTED |
| AI Features | AI-assisted CRM work | Public Loop AI, authenticated Loop AI panel, streaming routes, history, embedding sync | PARTIALLY IMPLEMENTED |
| Inbox and Email | Email-based customer work | Gmail UI, threads, messages, telemetry, campaign/email integrations | IMPLEMENTED |
| Notifications | User and system alerts | Header badge, notification drawer, read/unread state, mark-one/mark-all | IMPLEMENTED |
| Team Space | Team lead-pool collaboration | Lead pool, record requests, reassignment requests, permissions, dashboard | PARTIALLY IMPLEMENTED |
| Authentication and Users | Identity and access management | Login, registration, OAuth, OTP, invitations, user administration, login history | IMPLEMENTED |
| Organization and Profile | Tenant and personal context | Organization details, profile, avatar, role/profile display, table view mode, Google linkage | IMPLEMENTED |
| Roles, Profiles, and Permissions | Authorization configuration | Role hierarchy, module CRUD rights, profiles, record permissions | IMPLEMENTED |
| Teams | Team membership and leadership | Team management, membership, team-lead permissions | IMPLEMENTED |
| Approvals | Controlled record changes | Record-access and mass-change requests, approvals/rejections, audit trail | PARTIALLY IMPLEMENTED |
| Templates | Reusable document structures | Template library, create/edit/delete, categories, document creation | IMPLEMENTED |
| Settings | Personal preferences and utilities | Profile/avatar, table view mode, Google linkage, feedback | IMPLEMENTED |
| Data Administration | Import, export, backup, and storage | CSV import, export, backup APIs, storage overview, activity/record templates | PARTIALLY IMPLEMENTED |
| Billing | Subscription and quota visibility | Plan, usage, quotas, status, and upgrade/payment workflow | PARTIALLY IMPLEMENTED |
| Onboarding | Guided setup | Personal checklist and organization onboarding | IMPLEMENTED |
| Audit and Recovery | Governance and recovery | Audit logs, login history, record recycle bins, approvals history | PARTIALLY IMPLEMENTED |
| Integrations | External-service connectivity | Google OAuth/calendar, Gmail email, S3 storage, AI providers | PARTIALLY IMPLEMENTED |

## 4. Sales / CRM

### 4.1 Leads

**Purpose:** Capture, qualify, route, and convert prospects into customer opportunities.

**Main views**

- Leads table/list at `/dashboard/leads`.
- Kanban pipeline with drag-and-drop stage changes.
- Lead detail drawer with summary, contact/account/deal associations, activity timeline, notes, tasks, meetings, calls, attachments, and email context.
- Team Space lead-pool access for authorized managers and team leads.

**Features**

- Create, view, edit, archive/delete, and bulk-manage leads.
- Search, sort, filter, and server-paginate leads by status, source, owner, industry, rating, stage, and created date.
- Pipeline and list-mode switching, pipeline selection, and drag-based stage movement.
- Lead qualification fields, rating, industry, source, notes, and contact/account associations.
- Owner assignment, bulk owner reassignment, and Team Space pool membership.
- Lead conversion into a contact, account, and optional deal, with association handling and related-record linking.
- Copy lead data to clipboard, native share, and contextual contact/account creation.

**User actions**

- Add, edit, qualify, reassign, move, convert, archive, import, and export leads.
- Attach notes, tasks, meetings, calls, files, and related CRM records.
- Open the dashboard Loop AI panel for an authenticated AI chat experience.

**Related entities:** Contact, Account, Deal, Task, Meeting, Call, Note, Document, Team Space pool, User, Pipeline.

**Status:** IMPLEMENTED. Lead conversion, assignment, pool, and bulk management are wired to the leads module. The module does not provide a lead score column, scoring service, or bulk score API, so scoring is not listed as a feature.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/leads/page.tsx`, `crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx`, `crusource-crm-frontend/src/components/leads`, `crusource-crm-frontend/src/services/leads.service.ts`, `crusource-crm-backend/src/modules/leads/routes/leads_routes.py`, `crusource-crm-backend/src/modules/leads/handlers`.

### 4.2 Contacts

**Purpose:** Manage people associated with customer organizations and their sales engagements.

**Main views**

- Contact directory/table.
- Contact detail drawer with account, deals, activities, notes, documents, attachments, and email context.
- Create/edit form supporting account relationships, communication fields, mailing address, title/department, and a LinkedIn profile.

**Features**

- Contact creation, editing, archive/delete, bulk import, and duplicate email checks.
- Search, sorting, filtering, server-side pagination, and account-based organization.
- Account relationships, contact source, title/department, mailing address, and LinkedIn profile.
- Related deals, tasks, meetings, calls, notes, documents, and engagement timeline.
- Contact reassignment and Team Space record-access requests for restricted records.
- Contextual creation from Leads, Accounts, and related records.

**User actions**

- Add, edit, link to an account, communicate with, attach content to, and archive a contact.
- Start or review related activities and opportunities.

**Related entities:** Account, Lead, Deal, Task, Meeting, Call, Note, Document, Team Space.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/contacts/page.tsx`, `crusource-crm-frontend/src/components/contacts/ContactDetailDrawer.tsx`, `crusource-crm-frontend/src/components/contacts`, `crusource-crm-frontend/src/services/contacts.service.ts`, `crusource-crm-backend/src/modules/contacts`.

### 4.3 Accounts

**Purpose:** Manage companies, account hierarchies, stakeholders, opportunities, and related customer work.

**Main views**

- Account directory/table.
- Account detail drawer.
- Account create/edit form.
- Hierarchical account views for parent-child relationships.

**Features**

- Create, edit, view, archive/delete, duplicate, and bulk-import accounts.
- Search, sort, filter, and pagination by industry, owner, and active state; account fields include employees, revenue, and billing address.
- Parent-child account hierarchy and related-record visibility.
- Associated contacts, deals, activities, notes, documents, attachments, and engagement timeline.
- Bulk owner reassignment and Team Space record-access workflows.
- Account-related email, contextual record creation, and share/copy actions.

**User actions**

- Add or update an account, assign an owner, link contacts and deals, and manage customer-facing activity.

**Related entities:** Parent/child Account, Contact, Lead, Deal, Task, Meeting, Call, Note, Document, Team Space.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/accounts/page.tsx`, `crusource-crm-frontend/src/components/accounts/AccountDetailDrawer.tsx`, `crusource-crm-frontend/src/components/accounts`, `crusource-crm-frontend/src/services/accounts.service.ts`, `crusource-crm-backend/src/modules/accounts`.

### 4.4 Deals

**Purpose:** Track opportunities from qualification through negotiation and close.

**Main views**

- Deal pipeline/Kanban and deal table.
- Deal detail drawer.
- Deal create/edit form with products, activities, notes, documents, and related records.

**Features**

- Create, edit, view, archive/delete, duplicate, import, and export deals.
- List and Kanban modes with drag-and-drop stage movement.
- Multiple pipelines, stage configuration, stage history, amounts, currencies, stage win-probability, products, expected close date, and loss reason/notes.
- Contact/account relationships, owner and team assignment, and role-based access.
- Tasks, meetings, calls, notes, documents, attachments, and unified activity context.
- Forecast and analytics relationships for pipeline value, weighted value, stage distribution, and win outcomes.
- Product management for deal line items.
- Conversion utilities and bulk record operations.

**User actions**

- Create and update a deal, change pipeline/stage, add products, manage close details, and review forecast information.

**Related entities:** Pipeline, Pipeline Stage, Contact, Account, Product, Task, Meeting, Call, Note, Document, User, Team.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/deals/page.tsx`, `crusource-crm-frontend/src/components/deals/DealDetailDrawer.tsx`, `crusource-crm-frontend/src/components/deals`, `crusource-crm-frontend/src/services/deals.service.ts`, `crusource-crm-backend/src/modules/deals`, `crusource-crm-backend/src/modules/pipelines`.

### 4.5 Campaigns

**Purpose:** Create and send targeted email campaigns to selected lead or contact recipients.

**Main views**

- Campaign list at `/dashboard/campaigns`.
- Campaign workspace with recipient selection, content, and campaign statistics.
- Campaign detail/state management for draft, scheduled, sending, completed, failed, and cancelled processes.

**Features**

- Create, edit, archive/delete, and list campaigns.
- Select lead/contact recipients and define audience segments.
- Compose email content and track sent, failed, opened, bounced, and complaint statistics.
- Schedule campaigns, process sending in the background, and automatically update campaign and recipient statuses.
- Track per-recipient sent, failed, or skipped state with separate open and bounce metadata; click tracking is not exposed in the campaigns module.
- Manage sends, cancellations, and failures; a pause/resume endpoint is not present.

**User actions**

- Build an audience, compose content, schedule or send a campaign, and review the available send, open, bounce, and failure metrics.

**Related entities:** Lead, Contact, Email Delivery, Campaign Recipient, User.

**Status:** IMPLEMENTED. The repository contains a complete campaign UI, APIs, models, and background sending worker; delivery depends on configured email infrastructure.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/campaigns/page.tsx`, `crusource-crm-frontend/src/components/campaigns/CampaignDetail.tsx`, `crusource-crm-frontend/src/components/campaigns`, `crusource-crm-frontend/src/services/campaigns.service.ts`, `crusource-crm-backend/src/modules/campaigns`.

## 5. Activities

### Tasks

**Purpose:** Manage individual follow-up and operational work.

**Features**

- Create, edit, view, complete, reopen, archive/delete, and bulk-manage tasks.
- Title, description, assignee, priority, status, start/due dates, related CRM record, and notes.
- Views for all, pending, overdue, completed, and team tasks.
- Search, filtering, sorting, and task-detail panels.
- Optional recurrence/repeat configuration and organization-level task templates.
- Team Space record linking where permitted.

**User actions:** Assign, reschedule, complete, reopen, and relate a task to a lead, contact, account, or deal.

**Status:** IMPLEMENTED. Basic recurring-task configuration is present, but a fully implemented automatic recurrence execution path could not be conclusively determined.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/tasks/page.tsx`, `crusource-crm-frontend/src/components/dashboard/tasks/TaskDetails.tsx`, `crusource-crm-frontend/src/components/dashboard/tasks`, `crusource-crm-frontend/src/services/tasks.service.ts`, `crusource-crm-backend/src/modules/tasks`.

### Meetings

**Purpose:** Plan meetings, capture attendee information, and track resulting action items.

**Features**

- Create, edit, view, archive/delete, and bulk-manage meetings.
- Title, description, location, start/end times, organizer, attendees, status, recurrence, reminders, and related records.
- Agenda, attendee list, meeting history, and action items.
- Google Calendar OAuth and synchronization.
- Calendar polling, watch-channel management, and event-change tracking.
- Meeting status derived from the current time and user calendar context.

**User actions:** Schedule a meeting, add attendees, attach an agenda/CRM record, create action items, and synchronize with Google Calendar.

**Status:** IMPLEMENTED. The meeting experience and calendar sync are wired; some calendar synchronization endpoints are intended for provider/webhook administration rather than direct end-user use.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/meetings/page.tsx`, `crusource-crm-frontend/src/components/dashboard/meetings/MeetingDetailDrawer.tsx`, `crusource-crm-frontend/src/components/dashboard/meetings`, `crusource-crm-frontend/src/services/meetings.service.ts`, `crusource-crm-backend/src/modules/meetings`.

### Calls

**Purpose:** Record and review customer calls linked to CRM records.

**Features**

- Create, edit, view, delete, and bulk-delete call logs.
- Call subject/notes, direction, status, start/end or duration, recording URL/metadata, and related record.
- Filter and manage call history from Calls and related CRM record timelines.

**User actions:** Log a call, update its outcome, link it to a record, and review call history.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/calls/page.tsx`, `crusource-crm-frontend/src/components/dashboard/calls`, `crusource-crm-frontend/src/services/calls.service.ts`, `crusource-crm-backend/src/modules/calls`.

### Activity Timeline

**Purpose:** Present a unified activity history across related CRM records.

**Features**

- Combined display of tasks, meetings, calls, notes, emails, and related record context on lead, contact, account, and deal detail experiences.
- Entity-specific activity tabs and chronological history.
- Common interaction patterns for creating or opening activities from a record.

**Status:** PARTIALLY IMPLEMENTED. The customer-facing timeline is assembled primarily in the frontend from record-specific services rather than exposed as one fully independent backend timeline resource.

Implementation evidence: `crusource-crm-frontend/src/components/leads/drawer/LeadTimelineTab.tsx`, `crusource-crm-frontend/src/components/contacts/drawer`, `crusource-crm-frontend/src/components/accounts/drawer`, `crusource-crm-frontend/src/components/deals`.

### Activity Import

**Purpose:** Bring activity and CRM data into the system in bulk.

**Features**

- CSV data-import workflows for supported CRM/activity datasets.
- Template downloads, column mapping/validation feedback, and organization-scoped import processing.
- Import-related activity templates and administrative data-management screens.

**Status:** PARTIALLY IMPLEMENTED. Import APIs and a data-import administration page exist, but this is not presented as a normal user-facing activity-module page.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/admin/data-import/page.tsx`, `crusource-crm-backend/src/modules/data_admin/routes/data_import_routes.py`, `crusource-crm-backend/src/modules/data_admin/routes/data_export_routes.py`.

### Calendar

The Calendar at `/dashboard/calendar` provides a combined FullCalendar work area with day/week/month views and task, meeting, and call display. It is a cross-module scheduling view rather than a separate record type.

**Status:** IMPLEMENTED.

## 6. Global Notes

**Purpose:** Store notes on CRM records and in a global scratchpad so users can share context across sales work.

**Where notes appear**

- A global notes drawer opened from the dashboard header (notepad + overview tabs).
- Leads.
- Contacts.
- Accounts.
- Deals.
- Team Space pool, via a pool notes tab.

**Features**

- Create, view, edit, and delete notes on a parent record; archive and pin/unpin are not exposed.
- Global notes list with search, filtering, sorting, and server pagination.
- Inline `@` mentions of other users, parsed in the client.
- Parent-record authorization so notes cannot be accessed independently of an allowed related record.
- Minimizable/restoreable global drawer plus a notepad editor with entity attachment.
- Rich note presentation and note sections within activity timelines.

**User actions:** Add a note to a record, use the global notepad, mention a teammate, and find earlier notes.

**Status:** PARTIALLY IMPLEMENTED. Notes are attached to parent records with CRUD, search, sorting, and pagination, and a global notes/notepad drawer exists. Pinning, sharing/visibility, note-to-note linking, and archive behavior are not exposed by the notes model or routes.

Implementation evidence: `crusource-crm-frontend/src/services/notes.service.ts`, `crusource-crm-frontend/src/components/notes/global/GlobalNotesDrawer.tsx`, `crusource-crm-frontend/src/components/notes/global/WindowsNotepadPad.tsx`, `crusource-crm-frontend/src/components/notes/global/NotesOverviewSection.tsx`, `crusource-crm-frontend/src/components/teamspace/pool/tabs/PoolNotesTab.tsx`, `crusource-crm-frontend/src/components/leads/LeadDetailDrawer.tsx`, `crusource-crm-frontend/src/components/contacts/ContactDetailDrawer.tsx`, `crusource-crm-frontend/src/components/accounts/AccountDetailDrawer.tsx`, `crusource-crm-frontend/src/components/deals/DealDetailDrawer.tsx`, `crusource-crm-backend/src/modules/notes`.

## 7. Dashboard & Analytics

### Dashboard

**Purpose:** Give each user a concise overview of current CRM work and performance.

**Features**

- Home dashboard with KPI cards, recent activity, tasks, meetings, calls, leads, and deal summaries.
- Quick actions for common CRM operations.
- Role/permission-aware modules and empty states.
- User-specific navigation and activity data.

**Status:** IMPLEMENTED for the primary dashboard. Persistent dashboard-layout preferences and some dashboard customization services are not fully connected to the main user experience.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/page.tsx`, `crusource-crm-frontend/src/components/dashboard`, `crusource-crm-frontend/src/services/dashboard.service.ts`, `crusource-crm-backend/src/modules/dashboard`.

### Analytics

**Purpose:** Explore performance using charts, dashboards, and saved analytical views.

**Features**

- Analytics overview and visualizations.
- Lead, deal, revenue, activity, and source performance views.
- Dashboards made of KPI, chart, and related widgets.
- Save/update/delete analytics boards and cards.
- Date range, grouping, drill-down, chart-type, and visualization configuration.
- Multiple chart libraries and a visual dashboard canvas.

**Status:** PARTIALLY IMPLEMENTED. Core analytics and board APIs are registered, and the frontend supports analytics experiences, but some board-management services are not consistently exposed as a complete user-management flow.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/analytics/page.tsx`, `crusource-crm-frontend/src/components/analytics`, `crusource-crm-frontend/src/services/analyticsBoards.service.ts`, `crusource-crm-backend/src/modules/analytics_boards`.

### Reports

**Purpose:** Save, run, and share operational CRM reports.

**Features**

- Saved report list and report detail.
- Report builder with dimensions, measures, filters, grouping, and visualization.
- Report preview with tabular/chart output.
- Search/filtering of report definitions and report runs.
- Ad-hoc report runs and report sharing.

**Status:** PARTIALLY IMPLEMENTED. Report creation, retrieval, run, share, and ad-hoc run routes are registered and the frontend builder is present. Export, import, bulk delete, and field-suggestion handlers exist only as empty stubs, and the corresponding frontend filter/import-export components are empty, so those operations are not user-facing.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/reports/page.tsx`, `crusource-crm-frontend/src/components/reports/ReportsHome.tsx`, `crusource-crm-frontend/src/components/reports`, `crusource-crm-frontend/src/services/reports.service.ts`, `crusource-crm-backend/src/modules/reports`.

### Forecast

**Purpose:** Give sales teams a view of pipeline value, weighted pipeline, likely outcomes, and stage distribution.

**Features**

- Pipeline value and weighted-value summaries.
- Won, open, and projected totals.
- Stage distribution and pipeline breakdowns.
- Owner/team filters and stage filters.
- Date-range and period-based forecast analysis.
- Connections to deals and pipeline/stage data.

**Status:** PARTIALLY IMPLEMENTED. Forecast data and user-facing forecast pages are implemented, while broader configuration and all planned analytics operations are not uniformly exposed.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/forecast/page.tsx`, `crusource-crm-frontend/src/components/forecast`, `crusource-crm-frontend/src/services/forecast.service.ts`, `crusource-crm-backend/src/modules/forecast`.

## 8. Search

**Purpose:** Find CRM data quickly from the dashboard shell through the global search experience.

**Features**

- Global command-palette/search modal opened from the dashboard header.
- Search across CRM records, documents, and other supported indexed providers.
- Result grouping, snippets/highlights, and entity links.
- Type/entity filters and natural-language or power-syntax query support.
- Typo tolerance and “did you mean” suggestions.
- Recent searches and saved search presets.
- Backend provider architecture for contacts, accounts, leads, deals, and other supported search sources.
- Search click telemetry and autocomplete APIs.

**User actions:** Open global search, enter a term, filter by result type, inspect a result, and open the related record.

**Status:** IMPLEMENTED for indexed core CRM search. Search coverage depends on the records that have been indexed and the configured providers.

Implementation evidence: `crusource-crm-frontend/src/components/search/GlobalSearchModal.tsx`, `crusource-crm-frontend/src/components/layout/header/HeaderGlobalSearch.tsx`, `crusource-crm-frontend/src/hooks/useGlobalSearch.ts`, `crusource-crm-frontend/src/services/search.service.ts`, `crusource-crm-backend/src/modules/search/routes/search_routes.py`, `crusource-crm-backend/src/modules/search/providers`.

## 9. AI Features

**Purpose:** Provide AI-assisted CRM research and guidance through public and authenticated Loop AI chat experiences.

**Features**

- Public Loop AI chat on the landing page and the `/integrations`, `/docs`, and `/faq` pages.
- Authenticated Loop AI trigger in the dashboard header and side panel.
- Streaming chat routes and CRM-context retrieval/citation components.
- Authenticated chat history retrieval and clearing by session.
- CRM record embedding/index synchronization from the assistant.
- Hybrid retrieval services for CRM context and document/record text.
- Suggested questions and Markdown-formatted AI responses.
- Public-chat query limiting for unauthenticated visitors.

**User actions:** Open Loop AI, ask a question, review or clear conversation history, and synchronize CRM knowledge.

**Status:** PARTIALLY IMPLEMENTED. The public Loop AI chat path is implemented. For the authenticated path, the dashboard trigger, side panel, service, routes, chat history, and embedding synchronization are present, but the authenticated CRM-context streaming flow is not verified as working end-to-end, so CRM-context citations are not counted as a finished feature. The repository also does not establish separate user-facing lead/deal prediction, AI drafting, or AI insight workflows.

Implementation evidence: `crusource-crm-frontend/src/components/layout/Header.tsx`, `crusource-crm-frontend/src/components/layout/DashboardShell.tsx`, `crusource-crm-frontend/src/components/ai/LoopAISidePanel.tsx`, `crusource-crm-frontend/src/components/landing/PublicLoopAIChat.tsx`, `crusource-crm-frontend/src/services/aiChatService.ts`, `crusource-crm-backend/src/modules/ai_chat/routes/ai_routes.py`, `crusource-crm-backend/src/modules/ai_chat/services`, `crusource-crm-backend/src/modules/ai_chat/repositories/models.py`.

## 10. Notifications

**Purpose:** Keep users informed about CRM events, requests, and related system notifications.

**Features**

- Header notification bell and unread count.
- Notification dropdown/drawer with recent notifications.
- Notification list with read/unread state.
- Mark one notification as read.
- Mark all notifications as read.
- `related_entity_id` linkage for navigating to a related record.

**User actions:** Review alerts, open a related item, and mark one or all notifications read.

**Status:** IMPLEMENTED for the notification list, unread count, and read/mark-all-read operations. The notifications module exposes only list, mark-read, and read-all routes; no notification SSE stream, organization announcement/broadcast workflow, or notification recycle bin is present. The only SSE listener in the frontend is mounted for data-import progress events.

Implementation evidence: `crusource-crm-frontend/src/components/layout/Header.tsx`, `crusource-crm-frontend/src/components/layout/NotificationDropdown.tsx`, `crusource-crm-frontend/src/services/notifications.service.ts`, `crusource-crm-frontend/src/hooks/useSSEListener.ts`, `crusource-crm-backend/src/modules/notifications`.

## 11. Documents

**Purpose:** Store, organize, share, and work with files related to CRM activity.

**Main views**

- Documents page at `/dashboard/documents`.
- Document list and grid/folder views.
- Document detail/edit experience.
- Public shared-document view.

**Features**

- Upload and download files.
- Create, rename, move, categorize, and delete documents.
- Organize documents in folders/categories.
- Associate documents with leads, contacts, accounts, deals, and other record types.
- Version history and version management.
- Assign documents to users and manage ownership.
- Share with authorized users.
- Create public share links with token validation and rate limiting.
- Recycle bin with restore and permanent-delete workflows.
- Preview for common document types (PDF, DOCX, images, code/text, spreadsheets).
- In-app spreadsheet and DOCX editing backed by the backend `/content` and `/content/binary` routes.
- S3-compatible object storage.

**User actions:** Upload, browse, preview, download, share, version, relate, edit, recycle, and restore a document.

**Status:** IMPLEMENTED. The document lifecycle is user-facing, and spreadsheet/DOCX editing is implemented in-app. There is no OnlyOffice or Collabora integration; document conversion for other office formats is not exposed.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/documents/page.tsx`, `crusource-crm-frontend/src/components/documents/FileDetails.tsx`, `crusource-crm-frontend/src/components/documents/DocumentEditor.tsx`, `crusource-crm-frontend/src/components/documents/strategies/strategyRegistry.ts`, `crusource-crm-frontend/src/components/documents/spreadsheet/SpreadsheetEditor.tsx`, `crusource-crm-frontend/src/services/documents.service.ts`, `crusource-crm-backend/src/modules/documents/routes/documents_routes.py`.

## 12. Authentication & Users

### Authentication

**Features**

- Email/password login and registration.
- Forgot-password and reset-password flows.
- One-time-password verification.
- Google OAuth authentication and callback handling.
- Email verification.
- Organization invitation acceptance.
- Session persistence and logout.
- Public invitation routes.
- Authenticated application shell and redirect handling for protected pages.

**Status:** IMPLEMENTED for the current password, OTP, Google, invitation, and email-verification routes.

Implementation evidence: `crusource-crm-frontend/src/app/login/page.tsx`, `crusource-crm-frontend/src/app/signin/page.tsx`, `crusource-crm-frontend/src/app/sign-in/page.tsx`, `crusource-crm-frontend/src/app/register/page.tsx`, `crusource-crm-frontend/src/app/forgot-password/page.tsx`, `crusource-crm-frontend/src/app/reset-password/page.tsx`, `crusource-crm-frontend/src/app/accept-invite/page.tsx`, `crusource-crm-frontend/src/app/auth/callback/page.tsx`, `crusource-crm-backend/src/modules/auth`, `crusource-crm-backend/src/modules/admin/routes/invitation_routes.py`.

### Users and access administration

**Features**

- User list with search and status information.
- Create, update, activate/deactivate, and delete user accounts.
- Role assignment and user-profile assignment.
- User hierarchy and reporting/manager relationships.
- Team creation, membership, and team-lead designation.
- User module CRUD permissions and setup permissions.
- Lead/deal record-permission grants with active/expired/revoked status and access-request handling.
- Login history for users and administrators.
- Profile pages and personal account settings.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/admin/users/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/teams/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/roles/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/profiles/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/login-history/page.tsx`, `crusource-crm-backend/src/modules/user`, `crusource-crm-backend/src/modules/admin`, `crusource-crm-backend/src/modules/profiles`, `crusource-crm-backend/src/modules/login_history`.

## 13. Settings & Administration

### Personal settings

**Features**

- Avatar upload with crop, full name, and read-only email.
- Read-only assigned role and security/permission profile.
- Default table view mode (pagination vs infinite scroll, stored in browser localStorage).
- Google account linkage (Calendar sync, Gmail sending, free/busy availability checks).
- Feedback submission and onboarding checklist/tour.

**Status:** IMPLEMENTED for the personal settings currently exposed. There is no in-settings password-change form, no notification-preference editor, no browser-language selector, and no generic organization-level CRM configuration editor.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/settings/page.tsx`, `crusource-crm-frontend/src/app/dashboard/settings/layout.tsx`, `crusource-crm-frontend/src/components/dashboard/settings/TableDisplaySettingsCard.tsx`, `crusource-crm-frontend/src/components/dashboard/settings/GoogleAccountCard.tsx`, `crusource-crm-frontend/src/app/dashboard/settings/feedback/page.tsx`, `crusource-crm-frontend/src/app/dashboard/settings/onboarding/page.tsx`, `crusource-crm-backend/src/modules/profiles`, `crusource-crm-backend/src/modules/feedback`, `crusource-crm-backend/src/modules/onboarding`.

### Organization administration

**Features**

- Organization information and organization-level settings.
- Organization onboarding.
- Admin Hub overview.
- Data import and export administration.
- Backup API and backup administration screen.
- Storage usage/administration.
- Activity and record templates.
- Billing and quota information.
- Audit logs and administrative recycle bin.

**Status:** PARTIALLY IMPLEMENTED. Organization, billing, import/export, audit, and settings APIs are present, while several data-administration areas have backend capability without a complete equivalent user workflow.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/organization/page.tsx`, `crusource-crm-frontend/src/app/dashboard/organization/onboarding/page.tsx`, `crusource-crm-frontend/src/app/dashboard/billing/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/data-import/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/data-export/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/data-backup/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/storage/page.tsx`, `crusource-crm-backend/src/modules/organization`, `crusource-crm-backend/src/modules/org_settings`, `crusource-crm-backend/src/modules/billing`, `crusource-crm-backend/src/modules/data_admin`.

### Roles, profiles, and teams

**Features**

- Role hierarchy and role-based access levels.
- Module-level view/create/edit/delete permissions.
- Setup permissions for organization functions.
- Profile management and user-profile assignment.
- Team membership and team-lead permissions.
- Permission-aware sidebar and page access.

**Status:** IMPLEMENTED.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/admin/roles/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/profiles/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/teams/page.tsx`, `crusource-crm-frontend/src/hooks/queries/useMyPermissions.ts`, `crusource-crm-backend/src/modules/profiles`, `crusource-crm-backend/src/modules/admin`.

### Pipelines and approvals

**Features**

- Pipeline and stage management APIs.
- Standard lead-pipeline seeding/reset on application startup.
- Pipeline/stage history support.
- Record-access requests.
- Reassignment requests.
- Record-change/mass-change approval requests.
- Approve/reject operations and approval history/audit context.

**Status:** PARTIALLY IMPLEMENTED. Core request and approval APIs are available and the UI exposes related pages, but pipeline/approval administration is not equally complete across all intended configuration workflows.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/admin/pipeline/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/approvals/page.tsx`, `crusource-crm-frontend/src/app/dashboard/teamspace/requests/page.tsx`, `crusource-crm-backend/src/modules/pipelines`, `crusource-crm-backend/src/modules/approvals`, `crusource-crm-backend/src/modules/teamspace`.

### Templates and audit/recovery

**Features**

- Template list and Template Studio.
- Create, edit, delete, categorize, and use templates for documents/records.
- Audit-log browsing with filters and action/entity context.
- Login-history browsing.
- Administrative recycle-bin views for lead, deal, contact, account, and document soft-deletes.

**Status:** PARTIALLY IMPLEMENTED. Templates, audit logs, and login history are implemented. Recycle bin coverage is limited to lead, deal, contact, account, and document record types; there is no notification or user recycle bin.

Implementation evidence: `crusource-crm-frontend/src/app/dashboard/admin/templates/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/audit/page.tsx`, `crusource-crm-frontend/src/app/dashboard/admin/recycle-bin/page.tsx`, `crusource-crm-backend/src/modules/templates`, `crusource-crm-backend/src/modules/audit_logs`.

## 14. Cross-Module Relationships

### Lead lifecycle

`Lead → Contact → Account → Deal`

- A lead is the prospecting record.
- Conversion can create or link a Contact, Account, and optional Deal.
- The converted records retain source/relationship information.
- Activities, notes, files, and email context can be associated with the resulting records.

### Account-centered customer view

`Account → Contacts + Deals + Activities + Notes + Documents + Email`

- Accounts are the company-level container.
- Contacts represent stakeholders.
- Deals represent commercial opportunities.
- Tasks, meetings, calls, notes, documents, and email provide the shared customer interaction history.

### Deal and pipeline relationship

`Deal → Pipeline → Pipeline Stage → Stage History → Forecast/Analytics`

- A deal belongs to a pipeline and stage.
- Stage changes update stage history.
- Deal amounts and stages feed Forecast and Analytics.
- Deal data is intended to be available to the authenticated Loop AI context path once CRM embeddings are synchronized, but that authenticated retrieval flow is not verified as working end-to-end.

### Activity-to-record relationship

`Task / Meeting / Call / Note / Document → Lead, Contact, Account, or Deal`

- Activity records can be created from and displayed in CRM record detail experiences.
- Calendar combines tasks, meetings, and calls into a shared schedule.
- Record-level activity timelines combine activity and communication context.

### Search, AI, and notifications

`CRM Record / Document → Search Index or AI Context → Search Results or Loop AI`

- Search uses provider-specific indexes for CRM records and documents.
- Notifications are generated from user actions and system events and are read through the notification list API.
- The Loop AI module includes organization-scoped CRM context retrieval and citations; only the public chat path is currently counted as fully implemented.
- The Inbox supplies email context for record timelines and communication workflows.

### Team Space relationship

`Lead / Contact / Account / Deal → Team Pool / Access Request / Reassignment Request / Permission`

- Authorized team members can work with pooled leads.
- Users can request `edit` access to restricted lead or deal records, and approved grants carry active/expired/revoked status.
- Leads and deals can be submitted for reassignment.
- Approved actions are recorded for audit and team oversight.

### Administration relationship

`Organization → Users → Roles / Profiles / Teams → Module Permissions → CRM Data`

- Organization membership establishes the tenant context.
- Users receive roles, profiles, team memberships, and module/setup permissions.
- Those permissions determine sidebar visibility, page access, record access, and administrative actions.

## 15. Feature Status Summary

| Feature | Module | Status | Evidence |
|---|---|---|---|
| Lead list and detail | Leads | IMPLEMENTED | `crusource-crm-frontend/src/app/dashboard/leads`, `crusource-crm-frontend/src/components/leads`, `crusource-crm-backend/src/modules/leads` |
| Lead Kanban pipeline | Leads | IMPLEMENTED | `crusource-crm-frontend/src/components/leads` lead pipeline components and backend stage routes |
| Lead filtering and pagination | Leads | IMPLEMENTED | Lead list query/filter components and `crusource-crm-backend/src/modules/leads/routes/leads_routes.py` |
| Lead conversion | Leads | IMPLEMENTED | `/convert` and `/bulk-convert` routes plus conversion UI |
| Contact management | Contacts | IMPLEMENTED | Contacts pages, components, and backend module |
| Account management | Accounts | IMPLEMENTED | Accounts pages, components, and backend module |
| Account hierarchy | Accounts | IMPLEMENTED | Parent/child account fields and hierarchy components |
| Deal pipeline and Kanban | Deals | IMPLEMENTED | Deal page, pipeline components, and deal routes |
| Deal products | Deals | IMPLEMENTED | Product/deal-product components and services |
| Deal stage history | Deals | IMPLEMENTED | Stage-history module and deal detail integrations |
| Pipeline configuration | Deals / Pipelines | PARTIALLY IMPLEMENTED | Pipeline routes and admin page |
| Campaign creation | Campaigns | IMPLEMENTED | Campaign pages/components and campaign routes |
| Campaign sending worker | Campaigns | INTERNAL | Campaign worker and scheduler integration |
| Campaign delivery metrics | Campaigns | IMPLEMENTED | Campaign counters, recipient sent/failed/skipped state, open and bounce metadata; no click tracking |
| Task management | Activities | IMPLEMENTED | Tasks pages, components, routes |
| Automatic recurring-task execution | Activities | PARTIALLY IMPLEMENTED | Repeat field/configuration exists; full execution could not be conclusively determined |
| Meeting management | Activities | IMPLEMENTED | Meetings pages, components, routes |
| Google Calendar sync | Activities / Integrations | IMPLEMENTED | Calendar sync service and OAuth routes |
| Call logging | Activities | IMPLEMENTED | Calls page, components, routes |
| Combined Calendar | Activities | IMPLEMENTED | FullCalendar dashboard route and components |
| Unified activity timeline | Activities | PARTIALLY IMPLEMENTED | Frontend record timelines; no independent user-facing timeline resource |
| Global notes | Notes | PARTIALLY IMPLEMENTED | Global notes drawer/notepad, notes service, record integrations, and notes routes |
| Note mentions and search | Notes | IMPLEMENTED | Notes drawer behavior, client-side mention rendering, and notes list/filter APIs |
| Document lifecycle | Documents | IMPLEMENTED | Documents pages, services, and routes |
| Document versions | Documents | IMPLEMENTED | Document version components and APIs |
| Public document sharing | Documents | IMPLEMENTED | Share-token and public document routes |
| Document editing | Documents | IMPLEMENTED | In-app spreadsheet/DOCX editor strategies plus backend `/content` and `/content/binary` routes; no OnlyOffice/Collabora integration |
| Dashboard KPIs and activity | Dashboard | IMPLEMENTED | Dashboard page, components, and routes |
| Analytics dashboards | Analytics | PARTIALLY IMPLEMENTED | Analytics pages/components and analytics-board APIs |
| Saved reports | Reports | PARTIALLY IMPLEMENTED | Report pages, builder, and report APIs |
| Forecast | Forecast | PARTIALLY IMPLEMENTED | Forecast page/components and forecast APIs |
| Global search | Search | IMPLEMENTED | Global search modal, header trigger, search hooks/services, search routes/providers |
| Search result type filters | Search | IMPLEMENTED | Search UI and provider response metadata |
| Public Loop AI chat | AI | IMPLEMENTED | Public chat component, service, and `/ai/public-chat` route |
| Authenticated Loop AI chat | AI | PARTIALLY IMPLEMENTED | Header trigger, side panel, stream service, and `/ai/chat/stream` route; CRM-context streaming not verified end-to-end |
| CRM-context citations | AI | PARTIALLY IMPLEMENTED | Authenticated CRM retrieval and citation events; tied to the unverified authenticated stream |
| Authenticated chat history | AI | IMPLEMENTED | History get/clear endpoints and chat state |
| CRM embedding synchronization | AI | IMPLEMENTED | Assistant sync action and `/ai/sync-embeddings` route |
| Notifications | Notifications | IMPLEMENTED | Header bell, notification components, list/read routes |
| Gmail inbox | Inbox / Email | IMPLEMENTED | Inbox page and Gmail integration; requires a connected Google account |
| Email telemetry | Inbox / Email | INTERNAL | Email event worker and backend telemetry processing |
| Team lead pool | Team Space | PARTIALLY IMPLEMENTED | Team Space pages, pool services, and request routes |
| Record access requests | Team Space / Approvals | IMPLEMENTED | Request pages and approval routes |
| Password authentication | Authentication | IMPLEMENTED | Auth pages, auth routes, and session handling |
| Google OAuth | Authentication | IMPLEMENTED | OAuth callback and backend OAuth routes |
| Invitation lifecycle | Authentication / Users | IMPLEMENTED | Invitation acceptance page and admin invitation routes |
| User administration | Users | IMPLEMENTED | Admin users page and user-admin APIs |
| Team management | Users / Teams | IMPLEMENTED | Admin teams page and team APIs |
| Roles and profiles | Administration | IMPLEMENTED | Role/profile pages and permission APIs |
| Organization settings | Administration | IMPLEMENTED | Organization pages and organization-settings routes |
| Personal settings | Settings | IMPLEMENTED | Settings page and profile APIs |
| Data import | Data Administration | PARTIALLY IMPLEMENTED | Data-import page and import routes |
| Data export | Data Administration | PARTIALLY IMPLEMENTED | Data-export page and export routes |
| Data backup | Data Administration | PARTIALLY IMPLEMENTED | Backup page and backup API |
| Billing | Administration | PARTIALLY IMPLEMENTED | Billing page and billing routes |
| Templates | Administration | IMPLEMENTED | Templates page, Template Studio, and template routes |
| Audit logs | Administration | IMPLEMENTED | Audit page and audit-log routes |
| Login history | Administration | IMPLEMENTED | Login-history page and login-history routes |
| Recycle bin | Administration | PARTIALLY IMPLEMENTED | Recycle bin covers lead, deal, contact, account, and document soft-deletes; no notification or user recycle bin |
| Onboarding | Settings / Organization | IMPLEMENTED | Personal and organization onboarding pages/routes |
| Feedback | Settings | IMPLEMENTED | Feedback page and feedback route |
| Automation administration | Administration | PARTIALLY IMPLEMENTED | Placeholder page only; the `automations` setup permission currently gates the approvals API |

## 16. Implementation Notes

1. **Frontend and backend separation.** The main frontend uses Next.js App Router. The backend is a FastAPI service. The frontend proxy configuration routes `/api/:path*` and `/public/:path*` to the backend in `crusource-crm-frontend/next.config.ts:71`.

2. **Backend registration.** The backend registers the CRM, activity, analytics, administration, integration, AI, Team Space, and health routers in `crusource-crm-backend/src/main.py:225`.

3. **Permission model.** Navigation is filtered dynamically using resolved user permissions, administrator status, team-lead capability, and setup permissions. The primary filtering logic is in `crusource-crm-frontend/src/components/layout/Sidebar.tsx:59-78`.

4. **Standard lead pipeline.** Backend startup includes standard lead-pipeline reset/seeding behavior in `crusource-crm-backend/src/main.py:120`. This is an internal initialization behavior rather than a separate user workflow.

5. **Background processing.** The backend starts schedulers during application startup in `crusource-crm-backend/src/main.py:140`. Calendar polling and campaign/email processing run outside normal request-response interactions and are therefore documented as internal capabilities.

6. **Activity timeline design.** Customer-facing activity timelines are mostly composed by frontend record-detail experiences. This is why timeline functionality is marked PARTIALLY IMPLEMENTED rather than treating it as a fully independent backend activity module.

7. **AI availability.** The repository contains a public Loop AI chat path plus authenticated chat UI, streaming routes, CRM-context retrieval components, citations, chat history, and embedding synchronization. The public chat path is implemented; the authenticated CRM-context streaming path is present but is not verified as working end-to-end, and no separate prediction, drafting, or insight workflow is established.

8. **External integrations.** Google Calendar, Gmail, S3, and AI services are represented by backend integration code. Their availability in a deployed environment depends on the corresponding service configuration.

9. **Source-of-truth rule.** A route, model, or service is not automatically treated as a user-facing feature. The status labels in this document reflect the current combination of frontend UI, backend API, and wired integration behavior.

10. **Uncertain capabilities.** Where the repository contains a field, service, or route but does not establish a complete end-to-end user workflow, the capability is marked PARTIALLY IMPLEMENTED or BACKEND ONLY rather than being presented as a finished feature.

11. **Marketing copy versus implemented behavior.** Public landing content in `crusource-crm-frontend/src/components/landing/AIWorkflowsShowcase.tsx` and `crusource-crm-frontend/src/data/publicKnowledgeBase.ts` advertises duplicate auditing, pipeline health checks, and natural-language CRM answers. These are public product claims; the current source inventory does not establish them as dedicated user-facing workflows, so they are not credited as implemented features in this document.

12. **Empty stubs are not features.** Several backend handlers and frontend components exist as zero-byte placeholders (for example the report export/import/bulk-delete handlers and the report filter/import-export components). A file existing in the tree is not treated as evidence of a working capability.

13. **Inventory verification method (2026-09-26).** Statuses were rechecked against the current `src/app` routes, frontend component/service/hook wiring, backend router registration in `src/main.py`, and backend module routes/handlers. Graphify was used to locate relationships, but source remains authoritative. The workspace root is not a Git worktree; the frontend and backend are separate nested repositories, so inventory status is not inferred from root-level Git state.

14. **Architecture conventions.** The frontend uses Next.js App Router, TanStack Query for server state, and Redux Toolkit for shared client UI state. The backend follows module-level CQRS conventions with route, handler, repository, and service boundaries. These conventions are recorded in `AGENTS.md`; a feature is not upgraded to IMPLEMENTED merely because a file follows the directory pattern.
