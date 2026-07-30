# Module — Campaigns

## CM.1 General Information

- **API name**: `Campaigns` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **OAuth scope**: `ZohoCRM.modules.campaigns.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Track marketing campaigns (email, webinar, survey, social, ad, trade show) and the audience targeted by them.
- **Integration**: Zoho Campaigns (separate product) often used to send the actual emails; CRM Campaigns records their metadata.

## CM.2 Standard Fields

| Field | Type | Notes |
|---|---|---|
| Campaign Owner | Lookup(User) | yes |
| Campaign Name | Text | mandatory |
| Campaign Active | Checkbox | — |
| Type | Picklist | Email / Webinar / Survey / Social / Trade Show / Ad / Other |
| Status | Picklist | Planning / Active / Completed / Archived / Cancelled |
| Start Date | Date | — |
| End Date | Date | — |
| Expected Revenue | Currency | — |
| Budgeted Cost | Currency | — |
| Actual Cost | Currency | — |
| Expected Response (%) | Number | — |
| Actual Response (%) | Number | — |
| Num Sent | Integer | — |
| Parent Campaign | Lookup(Campaigns) | hierarchy |
| Description | TextArea | — |
| Product (targeted) | MultiLookup(Products) | — |

## CM.3 Related Lists

- Leads (targeted)
- Contacts (targeted)
- Activities (responses)
- Email Insights (if Zoho Campaigns integrated)
- Survey Responses (if Zoho Survey integrated)
- Notes, Attachments.

## CM.4 Cross References

- `../Modules/Leads.md`, `../Modules/Contacts.md`.
- `../06_Data_Model.md`.
