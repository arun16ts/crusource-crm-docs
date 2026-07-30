# Module — Contacts

> Self-contained module reference. All claims cite the official sources listed in `../10_References.md`. Items not found in official docs are marked.

## C.1 General Information

| Attribute | Value | Source |
|---|---|---|
| Module | Contacts | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/contacts/articles/standard-fields-contacts |
| API name | `Contacts` | https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html |
| OAuth scope | `ZohoCRM.modules.contacts.ALL` | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html |
| Purpose | Stores the people you have an established relationship with, typically linked to an Account | https://www.zoho.com/crm/help/ |
| Editions | Free and all paid editions | https://www.zoho.com/crm/zohocrm-pricing.html |
| Navigation | Left sidebar → Contacts | https://www.zoho.com/crm/help/ |

## C.2 User Interface

Standard List / Detail / Edit surfaces inherited. Custom views, group-by, filters available. Tags, Owner, Record Image supported.

### Standard Detail View Sections

- Contact Information block.
- Address Information block.
- Description / Key Notes.
- Right column: Contact Owner.

### Related Lists

- Activities (Tasks/Meetings/Calls)
- Deals (won + open)
- Quotes
- Sales Orders
- Invoices
- Cases
- Emails (Associated)
- Notes
- Attachments

## C.3 Data Model — Standard Fields

Verbatim from https://help.zoho.com/portal/en/kb/crm/sales-force-automation/contacts/articles/standard-fields-contacts (crawled successfully — full table included):

| Field Name | Description | Data type | Maximum Limit |
|---|---|---|---|
| Contact Owner | Lookup (User) | Lookup | — |
| Salutation | Pick list | Pick list | — |
| First Name | Text box | Text box | Alphanumeric(40) |
| **Last Name** | "This field is mandatory." | Text box | Alphanumeric(40) |
| Account Name | Lookup(Accounts) | Lookup | — |
| Vendor Name | Lookup(Vendors) | Lookup | — |
| Campaign Source | Lookup(Campaigns) | Lookup | — |
| Lead Source | Pick list | Pick list | — |
| Title | job position | Text box | Alphanumeric(50) |
| Department | Text box | Text box | Alphanumeric(30) |
| Date of Birth | Date | Date | — |
| Reporting To | Lookup(Contacts) | Lookup | — |
| Created By | Date/Time | Date/Time | — |
| Modified By | Date/Time | Date/Time | — |
| Email Opt Out | Check box | Check box | — |
| Skype Id | Text box | Text box | Alphanumeric(50) |
| Phone (office) | Text box | Text box | Alphanumeric(50) |
| Mobile | Text box | Text box | Alphanumeric(50) |
| Home Phone | Text box | Text box | Alphanumeric(50) |
| Other Phone | Text box | Text box | Alphanumeric(50) |
| Fax | Text box | Text box | Alphanumeric(50) |
| Email | Email | Email | Alphanumeric(100) |
| Secondary Email | Email | Email | Alphanumeric(100) |
| Assistant | subaddress field | | |
| Asst Phone | Text box | Text box | Alphanumeric(100) |
| Mailing Address | Compound | Street 250 / City 30 / State 30 / Code 30 / Country 30 |
| Other Address | Compound | same |
| Description | Text area (long text) | 32000 |

## C.4 System Fields

Same universal fields as Leads. See `../06_Data_Model.md` §6.1.

## C.5 User Actions

| Action | Source |
|---|---|
| Create / Read / Update / Delete via REST API | https://www.zoho.com/crm/developer/docs/api/v8/ |
| Bulk create/update via APIs | API V8 limits page |
| Convert Lead (auto-creates Contact) | Leads module |
| Send Email from record | UI |
| Schedule Activity (Task/Meeting/Call) | UI |
| Add Notes / Attachments | UI |
| Tag | UI / API |
| Mass Send Mail | list view action |
| Mass Update | list view action |
| Merge (across Contact records) | UI |
| Clone | UI More → Clone |

## C.6 Business Logic

- Mandatory Last Name (system rule).
- DNC: If `Email Opt Out` checked, no mass emails or marketing campaigns send to the contact (per Zoho email compliance standards).
- Account Name optional but strongly recommended for sales.
- Workflow rules / Blueprint / Approval Process applicable from Standard+.
- Permissions to edit specific fields can be controlled through profile-level field permissions.

## C.7 Automation

Workflow rules can fire on:

- Created
- Created or Edited
- Edited (any field or specific fields)
- Deleted
- Date field (recurring)
- Score change (Zia +)
- Day of Recommendation
- Notes events
- Competitor mentions (in related emails)

Actions: Email alerts, Tasks, Field updates, Webhooks, Custom functions, Create Records, Notifications, Tags.

## C.8 Reports

Default reports include:

- Contacts by Account
- Contacts by Owner
- Contacts Created over Time
- Top Customers by Revenue
- Birthday list
- Newsletter eligible (Email Opt Out = false)

## C.9 Technical

REST: `GET/POST/PUT/DELETE /crm/v8/Contacts`. Same auth, scopes, limits as Leads module (https://www.zoho.com/crm/developer/docs/api/v8/).

Related-records endpoints:

- `/crm/v8/Contacts/{id}/Deals`
- `/crm/v8/Contacts/{id}/Quotes`
- `/crm/v8/Contacts/{id}/Sales_Orders`
- `/crm/v8/Contacts/{id}/Invoices`
- `/crm/v8/Contacts/{id}/Cases`

## C.10 Cross References

- `../06_Data_Model.md` — Contacts entity.
- `../03_Feature_Index.md` — Activity management, email.
- `../08_AI_Features.md` — Data Enrichment (extract from email signature).
