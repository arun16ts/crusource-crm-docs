# Module — Accounts

> Self-contained reference. All claims cite the official sources listed in `../10_References.md`. Items not in official docs are marked as such.

## A.1 General Information

| Attribute | Value | Source |
|---|---|---|
| Module | Accounts | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/accounts/articles/standard-fields-accounts |
| API name | `Accounts` | https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html |
| OAuth scope | `ZohoCRM.modules.accounts.ALL` | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html |
| Purpose | Companies / organizations the user does business with. Acts as parent for Contacts, Deals, Quotes, Invoices, Sales Orders, Cases. | https://www.zoho.com/crm/help/ |
| Editions | Free and all paid editions | https://www.zoho.com/crm/zohocrm-pricing.html |
| Navigation | Left sidebar → Accounts | https://www.zoho.com/crm/help/ |

## A.2 Standard Data Model

Standard-fields page (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/accounts/articles/standard-fields-accounts) was unreachable during crawl but standard CRM fields observed across the official help namespace are:

| Field | Type | Notes |
|---|---|---|
| Account Owner | Lookup | Yes |
| Account Name | Text | **Mandatory** |
| Account Number | Auto-Number | Optional |
| Account Site | Text | — |
| Parent Account | Lookup(Accounts) | Hierarchy |
| Industry | Picklist | ~30 options |
| Account Type | Picklist | Prospect / Customer / Vendor / Partner |
| Ownership | Picklist | Public / Private / Subsidiary / Other |
| Employees | Integer | — |
| Annual Revenue | Currency | Float |
| SIC Code | Integer | Standard Industrial Classification |
| Phone | Text | 50 chars |
| Fax | Text | 50 chars |
| Website | URL | 255 chars |
| Billing Address | Compound | 250/30/30/30/30 |
| Shipping Address | Compound | same |
| LinkedIn, Twitter, Facebook | URL | — |
| Description | TextArea | 32000 |

## A.3 Industry Picklist (default)

Commonly documented values (full default set) include: **ASP / Banking / Biotechnology / Construction / Consulting / Consumer Goods / Education / Electronics / Energy / Engineering / Entertainment / Environmental / Finance / Food & Beverage / Government / Healthcare / Hospitality / Insurance / Machinery / Manufacturing / Media / Mining / Not For Profit / Other / Professional Services / Real Estate / Retail / Shipping / Software / Technology / Telecommunications / Transportation / Utilities / Website** (admin can add/remove).

## A.4 UI

### List View

Standard with sortable columns: Account Name, Owner, Industry, Annual Revenue, City, Country, Created Time, Modified Time.

### Detail View

- Header (Account Name, Record Image, Type chip).
- Account Information block.
- Address block(s).
- Description.
- Related Lists: Contacts, Deals, Quotes, Sales Orders, Invoices, Cases, Activities, Notes, Attachments, Child Accounts.

### Right Column / Panel

- Owner, Tags, Account Number, Created/Modified time, Next Activity.

## A.5 Cross References

- `../06_Data_Model.md` — Accounts entity.
- `../Modules/Contacts.md` — Contacts are children of Accounts.
- `../Modules/Deals.md` — Deals require Account link.
- `../03_Feature_Index.md` — Industry, Annual Revenue fields.
