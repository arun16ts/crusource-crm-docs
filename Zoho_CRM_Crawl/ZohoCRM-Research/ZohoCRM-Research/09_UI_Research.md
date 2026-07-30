# 09 — UI Research

> Reverse-engineered from official screenshots and documentation. Each artefact is source-linked.

---

## 9.1 Global UI Layout (default)

- **Top Bar (header)**: Organisation switcher (top-left), Search (global), Add + bell-icon (Notifications/Signals), User avatar (profile).
- **Sidebar (left, primary navigation)**: Modules list. User can reorder, group into Tabs (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-home-tabs/articles/customize-home-tab).
- **Workspace pane (centre)**: List view, Detail view, Edit form, Canvas surface.
- **Right Panel**: Tabs (Timeline / Notes / Activities / Attachments / Related Lists / Emails).

## 9.2 Home / Dashboard tab

- Composed of **Components** (https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/analytics-dashboards/articles/create-dashboard):
  - KPI
  - Chart (bar / horizontal / line / stacked / pie / donut / table / funnel / area — per https://www.glionconsulting.com/dashboards-in-zoho-crm/)
  - Target Meter
  - Quadrant
  - Zone
- Layout: grid, drag-resize.
- Export as Excel/CSV: supported for KPI, Chart, Target Meter, Quadrant, Zone (verbatim from https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/analytics-dashboards/articles/create-dashboard).

## 9.3 Sub-tab navigation

- Standard sub-tabs grouping (configurable via Tabs):
  - Sales: Leads, Contacts, Accounts, Deals, Quotes, Sales Orders, Invoices.
  - Inventory: Products, Price Books, Vendors, Purchase Orders.
  - Service: Cases, Solutions.
  - Marketing: Campaigns.
  - Activities: Tasks, Meetings, Calls.
  - Automation: Workflows, Blueprints, Approvals, Functions, Webhooks, Signals, Macros.
  - Analytics: Reports, Dashboards, Forecasts.
  - Administration: Users, Profiles, Roles, Roles & Sharing.

## 9.4 List View UI

- Header bar: filter chip, sort chip, group-by chip, search, view selector, "+ Create".
- Columns: standard + custom.
- Row actions: checkbox → bulk action bar appears.
- Record Image column (left, optional).
- Status icons (open/closed, owner indicators).
- Color-coded row tinting per row rules.
- Pagination footer: Page X of Y, links to download export.

## 9.5 Detail View

- **Header**: Record Image, Record Name, Breadcrumb (Module › Record), Status chip, Action buttons (Edit, Clone, Delete, More).
- **Right column**: Owner dropdown, Summary, Tags.
- **Centre column**: Single-column or two-column layout. Sections with title bars.
- **Related Lists**: per record. E.g. on Account → Contacts, Deals, Quotes, Sales Orders, Invoices, Activities, Cases, Notes, Attachments.
- **Timeline tab**: chronological feed of Notes, Emails, Calls, Tasks, Stage changes, Field Updates, Web hooks fired.
- **Emails tab**: Sent + Received emails linked to that record.
- **Activities tab**: Open + Closed activities sub-lists.
- **Notes tab**: Free text + image attachments.
- **Attachments tab**: file list with download links.

## 9.6 Create / Edit Form

- Layout editor-driven; sections → fields.
- Field types expose different controls:
  - Picklist → dropdown
  - Multi-select picklist → chip box
  - Lookup → modal search with type-ahead
  - Subform → inline rows (Add Row / Delete Row)
  - Image → drag-drop
- Save bar at top/bottom: Save, Save & New, Cancel, Save & Run Macro, Save as Draft.

## 9.7 Dialogs / Modals

- Lookup Modal: Search & select from target module.
- Confirm Modal: Yes / Cancel pattern.
- Message Modal: notification of success/error.
- Wizard Modal: multi-step sequential data entry (Enterprise+).

## 9.8 Kanban (Pipeline view)

- Columns render Stages; cards render Deal Name + Amount + Owner + Next Step + Closing Date.
- Drag-and-drop between columns triggers stage update + any workflow.

## 9.9 Calendar views

- Day / Week / Month / Agenda views.
- Color-codes per module (Tasks vs Meetings vs Calls).
- Drag-and-drop to reschedule.

## 9.10 Canvas surfaces

- Visual design of List View and Record Form.
- Drag-and-drop fields, headers, images, KPIs onto a blank canvas.

## 9.11 Notifications & Signals panel

- Bell icon dropdown.
- Real-time updates: Signal event per channel (email open/click/bounce, missed call, survey response, SalesIQ chat, Desk ticket — per https://www.zoho.com/crm/developer/docs/signals/).

Reference table — Signal types (verbatim from https://www.zoho.com/crm/developer/docs/signals/):

| Signal for | Displayed when |
|---|---|
| Incoming Email | "Mails are received from leads, contacts, or potential customers. The Incoming checkbox will be selected by default on enabling Email." |
| Email Insights | "A lead, contact, or potential customer opens an email sent from CRM, clicks a link in the email, or when the email has bounced. The status of the email can be 'Opened', 'Clicked', or 'Bounced'." |
| Call | "Missed calls are received from leads, contacts, or potential customers." |
| Survey | "Survey responses are received from leads, contacts, or potential customers." |
| Campaign | "A lead, contact, or potential customer opens an email sent from an email campaign, clicks a link in the email, or when the email has bounced." |
| SalesIQ | "You receive missed chats from leads, contacts, or potential customers." |
| Desk | "New support tickets, comments, or responses are received… You will also receive SalesSignals notifications for support tickets that are overdue or escalated or when a new rating is provided by a customer for a support personnel." |
| Backstage | "You receive a notification when tickets are purchased and when the attendee checks in to the event or if the ticket is cancelled." |
| Webinar | "You receive a notification when registrations are made." |

## 9.12 Settings pages

- General: Profile, Personal Settings, Email Settings, Calendar Settings, Notification Settings, Keyboard Shortcuts.
- Security Control: Users, Profiles, Roles, Roles & Sharing, Territories, Data Sharing Rules, Field Permissions.
- Customization: Modules, Fields, Layouts, Buttons & Links, Web Tabs, Wizards, Page Layout Rules, Custom Modules.
- Automation: Workflow Rules, Blueprints, Approvals, Functions, Schedules, Webhooks, Macros.
- Data Administration: Import, Export, Recycle Bin, Mass Delete, Audit Log, Cleanup.
- Integrations / Marketplace: app listing.
- Developer Space: API Console, Functions, Webhooks.

## 9.13 Search & Filter UI

- Filter dialog exposed from List View.
- Filter by field and condition.
- Save as Custom View.
- Across modules via Global Search top bar returns contextual suggestions grouped by module.

## 9.14 Empty states and loading patterns

- Empty list views display a friendly prompt + "Create your first X" button.
- Loading states use skeleton / shimmer placeholders.

## 9.15 Validations / Messages

- Inline field validation (red border, helper text).
- Form-level validation summary at top of form.
- Toast notifications on save/update.
- Permission denial banner if user lacks permission.

## 9.16 Responsive behaviour

- Browsers: latest 2 versions of Chrome, Firefox, Safari, Edge.
- Tablet: layout collapses to single-column flow.
- Mobile: app-only; web mobile mode displays limited module subset and list views.

## 9.17 Source Map

- Customizing Home Tab: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-home-tabs/articles/customize-home-tab
- Dashboard create: https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/analytics-dashboards/articles/create-dashboard
- Signals: https://www.zoho.com/crm/developer/docs/signals/
- Standard fields: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields
