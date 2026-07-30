# Module — Cases

> Source (could not be crawled — fields reconstructed from snippets in help namespace and the Zoho Cases-vs-Zoho-Desk community topic): https://help.zoho.com/portal/en/kb/crm/customer-support/articles/working-with-cases

## CS.1 General Information

- **API name**: `Cases`
- **OAuth scope**: `ZohoCRM.modules.cases.ALL`
- **Purpose**: Built-in support ticket tracker inside Zoho CRM.
- **Edition**: Free and all paid editions.
- **Distinct from**: Zoho Desk (separate product, integrated with CRM).

## CS.2 Standard Fields

| Field | Type | Notes |
|---|---|---|
| Case Owner | Lookup(User) | yes |
| Case Number | Auto-Number | Unique |
| Subject | Text | mandatory |
| Related To | Lookup(Account/Deal/Contact) | optional |
| Product Name | Lookup(Products) | optional |
| Solution | Lookup(Solutions) | agent chooses KB article |
| Status | Picklist | default set per help doc: "Active – New / Active – Escalated / Pending – On hold / Closed" |
| Priority | Picklist | High / Medium / Low |
| Type | Picklist | Question / Problem / Feature Request / Others |
| Case Origin | Picklist | Email / Phone / Web / Twitter / Facebook / Chat / Forum / Other |
| Reported By | Lookup or string | contact or free text |
| Reason | Picklist | — |
| Description | TextArea | 32000 |

## CS.3 Workflow / Blueprint

- Case status machine is commonly vis-à-vis Blueprint: New → In Progress → Escalated → On Hold → Closed.
- Approval is uncommon on Cases but supported.

## CS.4 Desk Integration (verbatim context)

Quoted (from the help community) when CRM Cases is compared to Zoho Desk:

> "Cases refers to the built-in, plain-vanilla Cases module in CRM. Support refers to the separate Zoho Support service that can be integrated with CRM."

## CS.5 Cross References

- `../Modules/Solutions.md`.
- `../06_Data_Model.md`.
- `../08_AI_Features.md` — VoC analytics.
