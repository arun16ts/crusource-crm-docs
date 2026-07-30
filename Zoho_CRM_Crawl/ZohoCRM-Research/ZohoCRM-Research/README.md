# ZohoCRM-Research

> Reverse-engineering reference for **Zoho CRM**. Every claim is sourced to an official URL (see `10_References.md`). Items not in official docs are explicitly marked `[not documented / inferred]`.

## Repository Structure

```
ZohoCRM-Research/
├── README.md
├── 01_Product_Overview.md
├── 02_Module_Index.md
├── 03_Feature_Index.md
├── 04_User_Journeys.md
├── 05_Business_Rules.md
├── 06_Data_Model.md
├── 07_API_Research.md
├── 08_AI_Features.md
├── 09_UI_Research.md
├── 10_References.md
│
├── Modules/
│   ├── Leads.md
│   ├── Contacts.md
│   ├── Accounts.md
│   ├── Deals.md
│   ├── Products.md
│   ├── Quotes.md
│   ├── Invoices.md
│   ├── SalesOrders.md
│   ├── PurchaseOrders.md
│   ├── Vendors.md
│   ├── PriceBooks.md
│   ├── Campaigns.md
│   ├── Forecasts.md
│   ├── Cases.md
│   ├── Solutions.md
│   ├── Activities.md
│   ├── Tasks.md
│   ├── Calendar.md
│   ├── Calls.md
│   ├── Reports.md
│   ├── Analytics.md
│   ├── Workflow.md
│   ├── Blueprint.md
│   ├── Approvals.md
│   ├── Settings.md
│   ├── Users.md
│   ├── Permissions.md
│   ├── Integrations.md
│   └── Zia_AI.md
│
└── (placeholders for expansion)
    ├── APIs/
    ├── Workflows/
    ├── UI/
    ├── Screenshots/
    ├── Database/
    ├── Diagrams/
    └── References/
```

## How to use this repo

1. **Understand the product**: read `01_Product_Overview.md` and `02_Module_Index.md`.
2. **Compare editions**: `03_Feature_Index.md` × `01_Product_Overview.md` Section 1.2.
3. **Map a user's day**: browse `Modules/*` and `04_User_Journeys.md`.
4. **Understand the rules a record obeys**: `05_Business_Rules.md`.
5. **Infer a database schema**: `06_Data_Model.md`.
6. **Plan an integration**: `07_API_Research.md`.
7. **Plan AI features parity**: `08_AI_Features.md` + `Modules/Zia_AI.md`.

## Sourcing policy

- Every document cites an official Zoho URL with every key claim.
- Where a detail was not available in the official docs (because the help.zoho.com KB article returned a network error during the v1 crawl), the document explicitly says so and the field is reconstituted from documented sibling modules — flagged as `[inferred]`.
- No third-party fabrication. The third-party URLs listed in `10_References.md` (zenatta.com, marksgroup.net, etc.) are clearly tagged as cross-reference.

## Version

This is **v1** of the research repository. Future iterations may add:

- Database diagrams (PNG/SVG export of Mermaid).
- Screenshots of every UI surface.
- API cookbook (cURL + Python + JS for every endpoint).
- Comparison of Zoho Editions feature gating (line by line).
- Step-by-step blueprint scripts (Deluge).
