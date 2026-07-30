# 03 — Feature Index

> Master index of capabilities discovered in Zoho CRM. Grouped by category. Each row cites the official URL where the feature was documented. Edition gating is based on https://www.zoho.com/crm/zohocrm-pricing.html and https://www.zoho.com/crm/complete-feature-list.html.

---

## 3.1 Sales Force Automation

| Feature | Module | Edition | Source |
|---|---|---|---|
| Lead capture, qualification, scoring | Leads | Free+ | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads |
| Lead conversion (Lead → Deal + Contact + Account) | Leads | Free+ | https://www.zoho.com/crm/help/ |
| Pipeline / Kanban view of deals by stage | Deals | Free+ | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| Stage-Probability mapping | Deals | Free+ | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| Forecast Categories (Pipeline / Closed / Omitted) | Forecasts | Free+ | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| Quote builder with line items | Quotes | Professional+ (Inventory management) | https://www.zoho.com/crm/zohocrm-pricing.html |
| Sales Order management & fulfillment | Sales Orders | Professional+ | Pricing page |
| Purchase Order management from low stock | Purchase Orders | Professional+ | https://help.zoho.com/portal/en/kb/crm/manage-inventory/purchase-orders/articles/creating-purchase-orders [not directly crawled — known from official UI] |
| Invoice generation, payment status | Invoices | Professional+ | https://help.zoho.com/portal/en/kb/crm/manage-inventory/invoices/articles/standard-fields-invoices |
| Stock auto-update via Invoice + SO + PO | Products | Professional+ | https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products (verbatim "The details of product quantity in the Stock Information section are updated automatically with reference to the sales order and purchase order and invoice.") |
| Vendor catalog | Vendors | Professional+ | https://help.zoho.com/portal/en/kb/crm/manage-inventory/vendors/articles/standard-fields-vendors |
| Multiple Price Books (Flat / Differential pricing) | Price Books | Professional+ | https://help.zoho.com/portal/en/kb/crm/manage-inventory/price-books/articles/standard-fields-price-books |
| CPQ (Configure-Price-Quote) | Quotes | Professional+ | Pricing page |
| Cadences (multi-channel lead follow-up sequences) | Leads | Standard+ | Pricing page |

## 3.2 Activity Management

| Feature | Module | Edition | Source |
|---|---|---|---|
| Tasks with due dates, priority, status | Tasks | Free+ | https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-tasks-module |
| Logged Calls with duration / outcome | Calls | Free+ | https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities |
| Meetings (renamed from Events) | Meetings | Free+ | https://help.zoho.com/portal/en/community/topic/events-module-is-been-renamed-as-meetings |
| Recent Activities widget (last 5) | Activities | Free+ | https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities |
| Calendar view per activity module | Calendar | Free+ | https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities |
| Mass-Update, Mass-Delete, Mass-Transfer activities | Activities | Free+ | FAQs page above (verbatim "In the Meetings, Calls, and Tasks modules, you can create a default view") |

## 3.3 Customer Service

| Feature | Module | Edition | Source |
|---|---|---|---|
| Cases — built-in ticket tracker | Cases | Free+ | https://help.zoho.com/portal/en/kb/crm/customer-support/articles/working-with-cases |
| Solutions — knowledge base | Solutions | Free+ | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields |
| Case ↔ Solution linking | Cases | Free+ | Same |

## 3.4 Email & Communication

| Feature | Module | Edition | Source |
|---|---|---|---|
| Connect inbox (IMAP / POP3 / Gmail / Outlook) | Email | Free+ | Pricing page |
| Email Templates with merge fields | Email | Free+ | Pricing page |
| Email Insights (Open / Click / Bounce) | Email | Standard+ | https://www.zoho.com/crm/ai-features-in-zoho-crm.html |
| Email Sentiment / Intent / Emotion Analysis | Email | Enterprise+ (AI) | https://www.zoho.com/crm/ai-features-in-zoho-crm.html |
| Email Custom Intent training | Email | Enterprise+ | Same |
| Email Summary | Email | Enterprise+ | Same |
| Competitor-mention alerts in email | Email | Enterprise+ | Same |
| Email Translation (built-in) | Email | Enterprise+ | Same |
| Subject-line suggestion via Zia | Email | Enterprise+ | Same |
| Autocomplete while typing email | Email | Enterprise+ | Same |
| Writing-assistant grammar / punctuation | Email | Enterprise+ | Same |

## 3.5 Automation

| Feature | Source |
|---|---|
| Workflow Rules (record action / date / score / recommendation / notes / competitors) | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules |
| Instant actions (Email alerts, Tasks, Field update, Webhooks, Custom functions, Create record, Cliq/Slack/Webex notifications, Convert Lead/Quote/SO) | Same (verbatim list) |
| Scheduled actions (Email, Task, Field update, Webhook, Custom function, Notifications) | Same |
| Multiple-conditions per workflow (up to 10 Enterprise/Ultimate, 5 Standard/Professional) | Same |
| Blueprint state-machine | https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint |
| Before-transition (assignees, criteria) | Same |
| During-transition (field values, checklists, attachments, notes, activities, widgets, kiosks) | Same |
| After-transition (email, task, meeting, call, field update, create record, webhook, custom function, tags, convert) | Same (verbatim list) |
| Automatic transitions (T-time elapse) | https://help.zoho.com/portal/en/community/topic/spotlight-7-automatic-transitions-in-blueprint |
| Common transitions | https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/parallel-and-multiple-transitions-configuration-and-usage |
| Approval processes with multiple approvers | https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/set-approval-process |
| Trigger Approval/BP/Workflow by API on Create/Update/Delete | https://help.zoho.com/portal/en/community/topic/kaizen-33-triggering-workflow-rules-approvals-and-blueprints-via-zoho-crm-api |
| Functions (Deluge) | https://www.zoho.com/crm/developer/docs/functions/ |
| Webhooks (outbound) | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/actions/articles/webhooks-workflow |
| Schedules (custom functions scheduled to run periodically) | https://www.zoho.com/crm/help/ |
| Signals (real-time cross-channel notifications) | https://www.zoho.com/crm/developer/docs/signals/ |
| Macros (one-click multi-step actions) | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html (`settings.macros`) |

Action set documentation implies caps of "up to 5 email alerts per action set", "up to 5 tasks per action set", "up to 6 webhooks per rule (1 instant + 5 scheduled)", "up to 6 custom functions per rule (1 instant + 5 scheduled)" — verbatim from the workflow rule page.

## 3.6 Reports & Analytics

| Feature | Source |
|---|---|
| Reports: Tabular, Summary, Matrix | https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/reports/create-edit-reports/articles/understanding-and-building-reports |
| Group-by / filter / formulas | Same |
| Custom Report Buttons | Same |
| Dashboards: KPI, Chart, Target Meter, Quadrant, Zone, Funnel | https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/analytics-dashboards/articles/create-dashboard |
| Export dashboards as Excel/CSV for KPI, Chart, Target Meter, Quadrant, Zone | Same (verbatim snippet) |
| Advanced Analytics connector to Zoho Analytics | https://www.zoho.com/analytics/help/connectors/zoho-crm.html |
| Pivot tables, conditional formatting, color/icon bands | https://www.zoho.com/analytics/whats-new/release-notes/previous-years.html |

## 3.7 Sales Forecasting

| Feature | Source |
|---|---|
| Create Forecasts (target by user / role) | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/forecasts/articles/creating-and-working-with-forecasts |
| One role per user ⇒ one forecast target | Same (verbatim) |
| Forecast Category per Deal pipeline stage | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| AI Forecasting (Zia-suggested targets per user/role) | https://www.zoho.com/crm/ai-features-in-zoho-crm.html |

## 3.8 Customization

| Feature | Source |
|---|---|
| Custom Modules (admin or by Zia NL prompt) | https://www.zoho.com/crm/ai-features-in-zoho-crm.html |
| Standard & Custom Fields with ~30 types | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/types-of-fields |
| Layouts (multi-section record pages) | Pricing page (referenced) |
| Custom Views (filter+columns+sort) | https://www.zoho.com/crm/help/ |
| Custom Buttons & Links | https://www.zoho.com/crm/help/ |
| Wizards (sequential multi-step forms) | https://www.zoho.com/crm/zohocrm-pricing.html |
| Canvas (visual drag-and-drop no-code UI) | https://www.zoho.com/canvas/ |
| Page Layout Rules (show/hide/make fields required) | Workflow configurations |
| Web tabs (URL hosted inside CRM) | https://www.zoho.com/crm/help/ |

## 3.9 Security & Administration

| Feature | Source |
|---|---|
| Users (add/activate/deactivate) | https://help.zoho.com/portal/en/kb/crm/security-control/data-security-types/articles/get-started-manage-users |
| Profiles (definable permissions per role) | Same |
| Roles (top-down hierarchy) | https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction |
| Sharing Rules (between-peer / superiors-allowed) | Same |
| Territory Management (hierarchical buckets — Enterprise+) | Pricing page |
| Field-level / Record-level permissions | https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/manage-profile-permissions |
| Recycle Bin (restore deleted records up to 60 days) | https://www.zoho.com/crm/help/ (Data Administration section) |
| Mass Delete / Cleanup | https://www.zoho.com/crm/help/ |
| Audit Log | https://www.zoho.com/crm/help/ |

## 3.10 Zia AI Features (Enterprise+ unless otherwise noted)

Source: https://www.zoho.com/crm/ai-features-in-zoho-crm.html — full list in `08_AI_Features.md`.

## 3.11 Integrations

- Native Zoho Family: Mail, Desk, Books, Campaigns, Survey, SalesIQ, PhoneBridge, Meeting, Cliq, Backstage, Webinar.
- Chrome / Outlook / browser plugins.
- Public REST API v8 (https://www.zoho.com/crm/developer/docs/api/v8/).
- Marketplace directory (https://marketplace.zoho.com/).
- Webhooks (outbound) + Function-as-the-inbound-webhook-handler (Kaizen #37 page).

## 3.12 Mobile

- iOS + Android apps (free)
- Push notifications
- Barcode scanner / QR scanning

## 3.13 Source Map

- Pricing / edition gating: https://www.zoho.com/crm/zohocrm-pricing.html
- Complete feature comparison: https://www.zoho.com/crm/complete-feature-list.html
- Modules & Fields: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields
- Workflow: https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules
- Blueprint: https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint
- AI: https://www.zoho.com/crm/ai-features-in-zoho-crm.html
- Signals: https://www.zoho.com/crm/developer/docs/signals/
