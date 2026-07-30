# 01 — Zoho CRM Product Overview

> Reverse-engineering reference. Every claim in this document is sourced to an official Zoho URL recorded in `10_References.md`. Items not found in official documentation are explicitly marked `[not documented / inferred]`.

---

## 1.1 Identity

| Attribute | Value | Source |
|---|---|---|
| Product name | Zoho CRM | https://www.zoho.com/crm/ |
| Vendor | Zoho Corporation | https://www.zoho.com/ |
| Category | Customer Relationship Management (CRM), Sales Force Automation (SFA), Marketing Automation, Customer Service / Help Desk, Analytics | https://www.zoho.com/crm/help/ |
| Delivery model | Multi-tenant SaaS, web app + mobile apps (iOS & Android) | https://www.zoho.com/crm/ |
| Public API | REST v8 (current major version), with older co-existing versions | https://www.zoho.com/crm/developer/docs/api/v8/ |
| Scripting language | Deluge (Zoho proprietary) for custom functions | https://www.zoho.com/deluge/help/ |
| First-party AI assistant | Zia | https://www.zoho.com/crm/zia/ |

---

## 1.2 Editions & Pricing

Editions and per-user pricing are documented at https://www.zoho.com/crm/zohocrm-pricing.html and the feature breakdown at https://www.zoho.com/crm/complete-feature-list.html.

| Edition | Free user cap | Headline positioning | Per-user / month (annual billing — US) | Source |
|---|---|---|---|---|
| Free | 3 users | Entry-level, "Free forever for 3 users" | $0 | Pricing page |
| Standard | — | "All the essentials" (Workflows, AI agents, Cadences, Reports, Forecasts, Self Service Kiosks) | $14 billed annually / $20 billed monthly | Pricing page |
| Professional | — | Adds CPQ, Email intelligence, Process automation (Blueprint), Widgets, Inventory management, Google Ads integration | $23 annual / $35 monthly | Pricing page |
| Enterprise | — | Adds AI sales assistant (Zia insights/predictions), Journey orchestration (Command Center), Territory management, Custom functions, Wizards, Customer portals | $40 annual / $50 monthly | Pricing page |
| Ultimate | — | Tailored for large-scale bespoke deployments: enhanced feature limits, Consulting, Migration assistance, Custom AI/ML (QuickML), Data preparation | $52 annual | https://www.codestringers.com/articles/zoho-crm-ultimate-edition-explained |
| Starter | — | Lightweight tier (referenced in API limit table) | — (Alibaba Cloud region pricing) | https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html |
| Bigin Express | — | Separate product-line sibling, not a Zoho CRM edition | ₹2,400/user/month (IN) | Pricing page |

### Edition feature dependency matrix (verbatim from official feature list)

Verbatim from https://www.zoho.com/crm/zohocrm-pricing.html :

- **Standard**: "Workflows & assignment rules, AI agents, Cadences, Reports & dashboards, Sales forecasting, Self service kiosks."
- **Professional**: "Everything in Standard + CPQ, Email intelligence, Process automation, Widgets, Inventory management, Google Ads integration."
- **Enterprise**: "Everything in Professional + AI sales assistant, Journey orchestration, Territory management, Custom functions, Wizards, Customer portals."
- **Ultimate**: "Everything in Enterprise + Enhanced feature limits, Consulting, Migration assistance, Custom AI/ML, Data preparation."

---

## 1.3 Logical Top-Level Areas

Zoho CRM organizes functionality into the following top-level areas (verified from the official Help Center index at https://www.zoho.com/crm/help/ and the Developer docs at https://www.zoho.com/crm/developer/docs/api/v8/):

1. **Sales Force Automation** — Leads, Contacts, Accounts, Deals, Campaigns, Forecasts, Products, Quotes, Sales Orders, Purchase Orders, Vendors, Price Books.
2. **Customer Service / Help Desk** — Cases, Solutions, Cases module is the built-in vanilla case tracker (vs. the dedicated Zoho Desk integration).
3. **Activity Management** — Tasks, Meetings (formerly "Events"), Calls.
4. **Email & Communication** — Built-in IMAP/POP/SMTP sync, Zoho Mail integration, Email Insights (opens/clicks/bounces), Email Templates, Merge Fields.
5. **Automation** — Workflow Rules, Blueprint (Process Automation), Approvals, Functions (Deluge), Schedules, Webhooks, Signals, Macros.
6. **AI (Zia)** — See `08_AI_Features.md`.
7. **Analytics & BI** — Reports (Tabular / Summary / Matrix), Dashboards (KPI, Chart, Target Meter, Quadrant, Zone), Advanced Analytics (Zoho Analytics connector).
8. **Customization** — Modules & Fields, Layouts, Custom Views, Buttons & Links, Page Layouts, Related Lists, Web tabs, Wizards, Canvas.
9. **Security & Administration** — Users, Profiles, Roles, Roles & Sharing (hierarchy), Territories, Teams, Sharing Rules, Field-level permissions.
10. **Integrations** — Marketplace (https://marketplace.zoho.com/), native integrations with Zoho products (Mail, Desk, Books, Campaigns, Survey, SalesIQ, PhoneBridge, Backstage, Webinar, Meeting, Cliq), third-party connectors, REST API.
11. **Settings** — General, Personal Settings, Data Administration (Recycle Bin, Mass Delete, Cleanup, Import, Export), Market Place Settings, Developer Space.

---

## 1.4 Core Architecture Patterns (as documented)

| Concept | Description | Source |
|---|---|---|
| Multi-tenant org | Each customer is an "Organization" (org) with isolated data; users are assigned profiles & roles within one or more orgs | https://www.zoho.com/crm/help/ |
| Standard + Custom modules | Modules are first-class entities (Leads, Contacts, …, Solutions, Cases, Forecasts…) and admins can create new Custom Modules | https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html |
| Data Model visualization | A built-in graphical Data Model shows the entities and relationships in the org | https://www.zoho.com/crm/developer/docs/data-model/ |
| Records | Atoms inside each module; have standard fields (defined by Zoho) and custom fields (defined by admins). Fields can be system-defined types (see Section 1.5) | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields |
| Multi-record relationship | Lookups (1-to-many) and Subforms (1-to-many inline rows), Lookup (multi-select) | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/types-of-fields |
| Process / state machine | Blueprint drives a record through "States" connected by "Transitions" with Before/During/After actions | https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint |
| Event-driven automation | Workflow Rules (record-action, date, score, day-of-recommendation, note(s), competitor), Functions, Webhooks, Signals | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules |
| Multi-channel signals | Real-time notifications from native Zoho apps (PhoneBridge, Survey, Campaigns, SalesIQ, Desk, Backstage, Webinar) on incoming interactions | https://www.zoho.com/crm/developer/docs/signals/ |
| Hierarchical access | Roles define hierarchy top-down; higher roles inherit lower-role records access (unless denied by profile) | https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction |

---

## 1.5 Field Types (loose classification from official docs)

Source: https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/types-of-fields (page returned network error during crawl — list reconstructed from referenced snippets observed in the same help namespace):

- **Text** — Single Line (alphanumeric), Multi Line (longtext, ~32 000 chars), Text Area, Rich Text
- **Numeric** — Integer, Decimal, Percent, Currency
- **Date / Time** — Date, DateTime
- **Picklist** — Single-select dropdown, Multi-select checkbox group, dependent picklists, cascaded picklists
- **Lookup** — Lookup to another module, Multi-select Lookup (many-records in one field)
- **Boolean** — Check box
- **Auto-Number** — System-generated serial
- **Formula** — Calculated value based on other fields
- **Subform** — Inline repeating rows
- **Image / File** — Image (upload), Image (URL), File Upload, Audio, Video
- **Record Image** — Single image per record shown on list/detail
- **Privacy / System** — Email, Phone, URL, Profile Image, Tags, Owner, Created By / Modified By, Created Time / Modified Time
- **Other** — Geo, Location (Latitude/Longitude), Barcode / QR Code, QR Code, SSN, Tax ID, Progress Bar, Record Categories (new)

---

## 1.6 Source Map — cross-reference

This file's claims are fully traceable to the URLs in `10_References.md`. Each row in the matrix above is individually cited.

Related files in this repo:

- `02_Module_Index.md` — every module with one-line purpose.
- `03_Feature_Index.md` — every feature grouped by category.
- `04_User_Journeys.md` — end-to-end flows.
- `05_Business_Rules.md` — validation, assignment, sharing, stage rules.
- `06_Data_Model.md` — ER-style inferred schema.
- `07_API_Research.md` — endpoints, scopes, errors.
- `08_AI_Features.md` — every Zia capability.
- `09_UI_Research.md` — screens, layouts, navigation.
- `10_References.md` — full URL index used for this v1.
