# 02 — Module Index

> Every module is a first-class entity (standard or custom) in Zoho CRM. The list below starts with the Standard Modules enumerated in https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html and https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields, then adds the system Modules (Activities cluster, etc.) that appear in the UI but are exposed via the `modules.leads`, `modules.tasks`, `modules.events`, `modules.calls`, `modules.notes`, `modules.activities`, `modules.search` scopes at https://www.zoho.com/crm/developer/docs/api/v8/scopes.html.

---

## 2.1 Standard Modules (Sales & Service)

| # | Module | API name | One-line purpose | Stand-alone doc |
|---|----|---------|------------------|------------------|
| 1 | **Leads** | `Leads` | Unqualified contacts/prospects before conversion to Deal + Contact + Account | `Modules/Leads.md` |
| 2 | **Contacts** | `Contacts` | People you have an established relationship with; always linked to an Account | `Modules/Contacts.md` |
| 3 | **Accounts** | `Accounts` | Companies/organizations you do business with | `Modules/Accounts.md` |
| 4 | **Deals** (a.k.a. Potentials, Opportunities) | `Deals` | Revenue opportunities tracked through a sales pipeline | `Modules/Deals.md` |
| 5 | **Campaigns** | `Campaigns` | Marketing campaigns (email/direct mail etc.) and audience segmentation | `Modules/Campaigns.md` |
| 6 | **Forecasts** | `Forecasts` | Quota / revenue target tracking by user / role | `Modules/Forecasts.md` |
| 7 | **Cases** | `Cases` | Built-in support tickets (vanilla Cases; distinct from Zoho Desk) | `Modules/Cases.md` |
| 8 | **Solutions** | `Solutions` | Knowledge-base articles attached to Cases | `Modules/Solutions.md` |
| 9 | **Products** | `Products` | Goods/services catalog with stock and pricing | `Modules/Products.md` |
| 10 | **Price Books** | `PriceBooks` | Pricing matrix per product/customer segment | `Modules/PriceBooks.md` |
| 11 | **Quotes** | `Quotes` | Sales proposal with line items | `Modules/Quotes.md` |
| 12 | **Sales Orders** | `SalesOrders` | Confirmed customer order, can convert to Invoice | `Modules/SalesOrders.md` |
| 13 | **Purchase Orders** | `PurchaseOrders` | Order placed with a Vendor to buy stock | `Modules/PurchaseOrders.md` |
| 14 | **Invoices** | `Invoices` | Bill issued to the customer | `Modules/Invoices.md` |
| 15 | **Vendors** | `Vendors` | Suppliers you buy from | `Modules/Vendors.md` |

Source: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields and https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html (verbatim: "standard modules such as Leads, Accounts, Contacts, Deals, Forecasts, and Activities, along with custom modules").

---

## 2.2 Activity Modules

| # | Module | API scope | One-line purpose | Stand-alone doc |
|---|----|---------|------------------|------------------|
| 16 | **Tasks** | `modules.tasks` | To-dos that can be linked to any record | `Modules/Tasks.md` |
| 17 | **Meetings** (renamed from "Events") | `modules.events` | Scheduled meetings/events | `Modules/Calendar.md` |
| 18 | **Calls** | `modules.calls` | Logged inbound/outbound calls | `Modules/Calls.md` |

> Note: "Events" was renamed to "Meetings" in Zoho CRM — see https://help.zoho.com/portal/en/community/topic/events-module-is-been-renamed-as-meetings.

---

## 2.3 System / Container Modules

| # | Module | Purpose | Source |
|---|----|---------|---------|
| 19 | **Dashboard / Home Tab** | Personalised landing page composed of KPI, Charts, Funnels, Custom Views, Pipeline views, Widgets, Kiosks | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-home-tabs/articles/customize-home-tab |
| 20 | **Reports** | Saved Tabular / Summary / Matrix reports | https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/reports/create-edit-reports/articles/understanding-and-building-reports |
| 21 | **Dashboards** | Composite canvases of components (KPI, Chart, Target Meter, Quadrant, Zone, Funnel) | https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/analytics-dashboards/articles/create-dashboard |
| 22 | **Notes** | Free-text annotations attached to any record | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html (`modules.notes`) |
| 23 | **Attachments** | Files linked to records (one-to-many list) | https://www.zoho.com/crm/developer/docs/api/v8/ |
| 24 | **Activities** | Virtual aggregator / pivot for Tasks+Meetings+Calls grouped under a record | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html (`modules.activities`) |
| 25 | **Search Module** | Cross-module unified search endpoint | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html (`modules.search`) |

---

## 2.4 Automation & Configuration Modules (UI surfaces, not data modules)

| # | Module / Surface | Purpose | Source |
|---|----|---------|---------|
| 26 | **Workflow** | Rules that trigger instant or scheduled actions on record events | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules |
| 27 | **Blueprint** | Visual state-machine for guided processes | https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint |
| 28 | **Approvals** | Multi-step approval chain with Approve / Reject actions | https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/set-approval-process |
| 29 | **Functions (Deluge)** | Server-side scripts invoked from actions/workflows | https://www.zoho.com/crm/developer/docs/functions/ |
| 30 | **Webhooks** | Outbound HTTP calls to third-party services | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/actions/articles/webhooks-workflow |
| 31 | **Macros** | Pre-recorded multi-step user actions to repeat common tasks | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html (`settings.macros`) |
| 32 | **Signals** | Real-time cross-channel interaction notifications | https://www.zoho.com/crm/developer/docs/signals/ |
| 33 | **Canvas** | No-code UI designer for record and list views | https://www.zoho.com/canvas/ |
| 34 | **Command Center** | Cross-module journey orchestration | https://www.zoho.com/crm/tutorials/commandcenter/overview.html |
| 35 | **Zia** | AI assistant (predictions, recommendations, NLP, vision, etc.) — Enterprise+ | https://www.zoho.com/crm/zia/ |
| 36 | **Wizard** | Sequential guided data-entry form (Enterprise+) | https://www.zoho.com/crm/zohocrm-pricing.html |
| 37 | **Kiosk** | Self-service data-entry screen for visitors (Standard+) | https://www.zoho.com/crm/zohocrm-pricing.html |
| 38 | **Customer Portal** | External access for customer/partner/vendor (Enterprise+) | https://www.zoho.com/crm/zohocrm-pricing.html |
| 39 | **Territories** | Hierarchical assignment buckets (Enterprise+) | https://www.zoho.com/crm/zohocrm-pricing.html |
| 40 | **Journey Orchestration** | End-to-end journey map (Enterprise+) | https://www.zoho.com/crm/zohocrm-pricing.html |
| 41 | **Integrations / Marketplace** | Apps directory | https://marketplace.zoho.com/ |
| 42 | **Settings** | Admin Settings: Users, Profiles, Roles, Roles&Sharing, Territories, Pipelines, Modules, Fields, Layouts, Webhooks, Functions, Workflows, Blueprints, Approvals, Automation, Data Admin, Personal Settings | https://www.zoho.com/crm/help/ |

---

## 2.5 Custom Modules

Custom Modules can be created at runtime by administrators or by Zia (Module Creation by Zia — Natural-language module creation in https://www.zoho.com/crm/ai-features-in-zoho-crm.html). Each custom module supports:

- Standard system fields (Owner, Created By, Modified By, Created Time, Modified Time, Record Image)
- Custom fields (any of the types in Section 1.5)
- Custom layouts
- Custom views
- Related lists (lookups pointing back)
- Workflow rules, Blueprint, Approvals (subject to edition)
- API access via `modules.custom` scope (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)

---

## 2.6 List-View of Modules and API endpoint conventions

Per https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html :

- `GET /settings/modules` — returns the list of modules installed in an org (standard + custom + system).
- A module's records are then reachable at `GET /crm/v8/{module_api_name}` (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html).
- The Get Records endpoint requires the matching module scope, e.g. `ZohoCRM.modules.leads.ALL`.

---

## 2.7 Source Map

- Module list: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields
- Module API names: https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html
- Scopes mapping: https://www.zoho.com/crm/developer/docs/api/v8/scopes.html
- Pricing/edition gating: https://www.zoho.com/crm/zohocrm-pricing.html
