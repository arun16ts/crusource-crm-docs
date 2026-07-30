# Module — Deals (formerly Potentials / Opportunities)

> All claims cite official sources listed in `../10_References.md`.

## D.1 General Information

| Attribute | Value | Source |
|---|---|---|
| Module | Deals | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| API name | `Deals` | https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html |
| OAuth scope | `ZohoCRM.modules.deals.ALL` | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html |
| Purpose | Track selling opportunities through a pipeline of stages | https://www.zoho.com/crm/help/ |
| Editions | Free and all paid editions | https://www.zoho.com/crm/zohocrm-pricing.html |
| Navigation | Left sidebar → Deals | https://www.zoho.com/crm/help/ |

## D.2 User Interface

### List View

- "All Deals" default view; admins can clone into custom views.
- Tabs: Active Deals / All / My Deals / Recently Created / Recently Modified / Untouched.

### Kanban / Pipeline View

- Cards visualised by Stage (columns).
- Card content: Deal Name, Amount, Closing Date, Next Step, Owner.
- Drag-and-drop between columns triggers stage update.
- The Kanban view is built-in (mentioned widely in official tutorial videos).

### Detail View

- Header: Deal Name, Record Image, Stage chip, Probability chip, Forecast Category chip.
- Action bar: Edit, Clone, Convert to Quote, Convert to Sales Order, Schedule activities, Send Mail.
- Sections: Deal Information, Pipeline / Stage / Probability, Date / Amount, Contact, Source.
- Right column: Deal Owner, Created/Modified info.
- Related lists: Quotes, Sales Orders, Invoices, Activities, Notes, Attachments, Emails, Tasks, Events.

## D.3 Data Model

| Field | Type | Mandatory? | Source |
|---|---|---|---|
| Deal Owner | Lookup(User) | Yes | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals |
| Deal Name | Text | **Yes** | Same |
| Account Name | Lookup(Accounts) | **Yes** | Same |
| Contact Name | Lookup(Contacts) | — | Same |
| Amount | Currency | — | Same |
| Closing Date | Date | — | Same |
| Stage | Picklist | Yes | Same |
| Probability | Number % | Auto from Stage | Same |
| Forecast Category | Picklist | Auto (Pipeline / Closed / Omitted) | Same |
| Pipeline | Picklist | Multi-pipeline support | Same |
| Lead Source | Picklist | — | — |
| Campaign Source | Lookup(Campaigns) | — | — |
| Type | Picklist | New Business / Existing Business | — |
| Next Step | Text | — | — |
| Reason for Loss | Picklist | Required on Closed Lost via Blueprint | — |
| Description | TextArea | 32000 | — |

### D.3.1 Stage-Probability Mapping (verbatim from official docs)

Quoted from https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals :

> "The four important factors in stage probability mapping are: Deal stages, Probability, Deal Category, and Forecast Category."

Default system-defined deal stages include **qualification, needs analysis, negotiation, closed won, closed lost**.

Each stage has:
- A **Deal Category**: Open / Closed Won / Closed Lost.
- A **Forecast Category**: Pipeline / Closed / Omitted.
- A **Probability** (0–100 %) used in forecast rollups.

## D.4 User Actions

| Action | Source |
|---|---|
| Create / Read / Update / Delete via REST | https://www.zoho.com/crm/developer/docs/api/v8/ |
| Move Stage via drag-drop (Kanban) | https://www.youtube.com/watch?v=5wKyU2CSVBU |
| Convert to Quote | Custom button or action |
| Convert to Sales Order | Same |
| Clone | UI |
| Bulk Stage Change | list view action |
| Mass Update / Mass Delete / Mass Mail | list-view |
| Schedule Activities | UI |
| Big Deal Alerts | Built-in feature (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals references "Big Deal Alerts") |

## D.5 Business Logic

1. Probability auto-updates when Stage changes, **unless** admin has set the field to be manually editable. Quote the docs: "Map Stage-Probability values".
2. When Stage changes to Closed Won/Closed Lost, Forecast Category auto-upgrades to "Closed", driving rolling forecast numbers.
3. Reason for Loss is commonly enforced via Blueprint (Transition Exclusivity).
4. Workflow Rule on Stage change can auto-create Invoice/SO.

## D.6 Automation

Applicable: Workflow Rules, Blueprints, Approvals, Functions (Deluge), Webhooks, Cadences (Standard+).

## D.7 Reports

Default reports (illustrative): Deals by Stage, Deals by Owner, Deals Closing in 30 days, Deals Lost Reason, Deals Forecast vs Achieved, Deals by Pipeline, Won Deals This Quarter.

## D.8 Technical

- API: `GET/POST/PUT/DELETE /crm/v8/Deals`
- `?custom_view_id` for filtered list.
- Webhook triggers: created/updated/deleted; full payload includes previous vs new field values.

## D.9 Cross References

- `../06_Data_Model.md` — Deals entity.
- `../04_User_Journeys.md` §4.4.
- `../05_Business_Rules.md` §5.2.
- `../03_Feature_Index.md` — Forecasts.
