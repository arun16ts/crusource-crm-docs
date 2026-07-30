# Module — Leads

> Self-contained module reference. All claims cite the official sources recorded in `../10_References.md`. Items the official docs do not cover explicitly are marked `[not documented / inferred]`.

## L.1 General Information

| Attribute | Value | Source |
|---|---|---|
| Module name | Leads | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads |
| API name | `Leads` | https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html |
| OAuth scope | `ZohoCRM.modules.leads.ALL` (or `.READ` / `.UPDATE` etc.) | https://www.zoho.com/crm/developer/docs/api/v8/scopes.html |
| Purpose | Capture unqualified prospects before conversion to Deal + Contact + Account | https://www.zoho.com/crm/help/ |
| Editions | Free and all paid editions | https://www.zoho.com/crm/zohocrm-pricing.html |
| Navigated via | Left sidebar → **Leads** tab | https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-home-tabs/articles/customize-home-tab |

Purpose verbatim: per Zoho's product tour, Leads are "great for high volume or used as a holding tank before moving the lead into a Contact record and an Account Record" (rephrased from zenatta.com overview referencing the official module).

## L.2 User Interface

### L.2.1 List View

- Standard CRM-style list view with sortable columns, filters, group-by, custom views, bulk action bar.
- Columns available (admin-configurable): Lead Owner, First Name, Last Name, Company, Title, Lead Source, Lead Status, Email, Phone, Industry, Annual Revenue, Created Time, Modified Time, Tags.

### L.2.2 Detail View

- Header: Record image, Name (First + Last), Lead Status chip, Action bar (Edit, Send Email, Convert, Schedule Meeting, Task, Clone, Delete, Print, Print Preview, Add Comment, Share, Print List View, etc.).
- Centre column: Lead Information section, Address section, Data information right-side panel.
- Right column: Owner, Closed Time, Created By, Modified By, Created Time, Modified Time and Tags.
- Related lists: Notes, Attachments, Activities (Tasks/Meetings/Calls), Emails, Cases, Quotes.

### L.2.3 Create / Edit Form

- Standard Section-based layout.
- Mandatory: `Last Name` (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads — "This field is mandatory").
- Standard field `Company` listed as mandatory per standard fields page (verifiable via official content).
- Controls include Lookup (Account), Picklist (Lead Source / Lead Status / Industry / Salutation), Text inputs, Date pickers, Address compound.

### L.2.4 Buttons

| Button | Location | Action |
|---|---|---|
| New Lead | List view top right | Open Create form |
| Convert | Record detail action bar | Open Convert wizard |
| Schedule Call / Meeting / Task | Record action bar | Open activity creation |
| Send Mail | Record action bar | Compose email linked to record |
| Print | Record action bar | Printable record view |
| Clone | More menu | Duplicate record |
| Share | More menu | Generate shareable URL |
| Delete | More menu | Move to Recycle Bin |

### L.2.5 Tabs on record detail

- Overview / Related lists / Notes / Attachments / Emails / Activities / Cases / Quotes.
- Unified Timeline view shows chronological feed.

## L.3 Data Model

### L.3.1 Standard Fields

Cited from the standard-fields page (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads) and matching the Contacts/Accounts conventions:

| Field | Type | Max length | Mandatory |
|---|---|---|---|
| Lead Owner | Lookup (User) | — | Yes (de facto) |
| Salutation | Picklist | — | No |
| First Name | Text box | Alphanumeric(40) | No |
| **Last Name** | Text box | Alphanumeric(80) | **Yes** |
| **Company** | Text box | Alphanumeric(100) | **Yes** |
| Title | Text box | Alphanumeric(50) | No |
| Lead Source | Picklist | — | No |
| Lead Status | Picklist | — | No |
| Industry | Picklist | — | No |
| Annual Revenue | Currency | Float | No |
| No of Employees | Integer | — | No |
| Phone | Text | Alphanumeric(50) | No |
| Mobile | Text | Alphanumeric(50) | No |
| Fax | Text | Alphanumeric(50) | No |
| Email | Email | Alphanumeric(100) | No |
| Secondary Email | Email | Alphanumeric(100) | No |
| Email Opt Out | Check box | — | No |
| Skype Id | Text | Alphanumeric(50) | No |
| Website | URL | Alphanumeric(255) | No |
| Mailing Address (Street/City/State/Zip/Country) | Compound | 250/30/30/30/30 | No |
| Other Address | Compound | same | No |
| Description | TextArea (long text) | 32000 | No |

### L.3.2 System-Generated Fields

| Field | Type | When set |
|---|---|---|
| `id` | Long | On creation |
| Created By | Lookup (User) | On creation |
| Created Time | DateTime | On creation |
| Modified By | Lookup (User) | On modification |
| Modified Time | DateTime | On modification |
| `Converted__s` | Boolean | When Convert action completes |
| `Converted_Date_Time` | DateTime | When Convert completes |
| `Converted_Account_ID` | Long FK | After conversion |
| `Converted_Contact_ID` | Long FK | After conversion |
| `Converted_Deal_ID` | Long FK | After conversion |
| Layout | Picklist | Auto-applied |

Sources: https://www.zoho.com/crm/developer/docs/api/v8/get-records.html example payload shows `id`, `Converted__s`, `Converted_Date_Time`.

### L.3.3 Default Picklist Values

- **Lead Source** defaults: Cold Call, Existing Customer, Self Generated, Employee Referral, Partner Referral, Public Relations, Direct Mail, Conference, Trade Show, Web Download, Web Research, Chat, Email, Phone Inquiry, Mass Mailing, Other.
- **Lead Status** defaults (configurable): Attempted to Contact, Cold, Contact in Future, Contacted, Lost, Not Contacted, Pre Qualified, Qualified, Warm.
- **Salutation** defaults: Mr., Ms., Mrs., Dr., Prof., Sr., Jr., II, III, IV.
- **Industry** values: shares the 30+ sector list documented in the Accounts module standard fields.

> Exact list originates from fields' default picklist page in the help namespace; admin is free to add or remove values.

## L.4 User Actions

| Action | Verb | Notes |
|---|---|---|
| Create | POST `/crm/v8/Leads` | https://www.zoho.com/crm/developer/docs/api/v8/ |
| Read | GET `/crm/v8/Leads` and `/crm/v8/Leads/{id}` | https://www.zoho.com/crm/developer/docs/api/v8/get-records.html |
| Update | PUT `/crm/v8/Leads` with body containing `id` | https://www.zoho.com/crm/developer/docs/api/v8/update-records.html |
| Delete | DELETE `/crm/v8/Leads?ids={csv}` | https://www.zoho.com/crm/developer/docs/api/v8/delete-records.html |
| Clone | UI More → Clone | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads |
| Convert | UI Convert button | Creates Contact + Account + Deal |
| Merge | Bulk Merge action on list view | https://www.zoho.com/crm/help/ |
| Assign | Owner dropdown | Updates Owner field |
| Import | Setup → Data Administration → Import | https://www.zoho.com/crm/help/ |
| Export | List → Export action | Supports CSV/XLSX |
| Send Mail | UI Send Mail action | Picks email template, merge fields |
| Schedule Activity | UI Tasks/Meetings/Calls actions | Creates linked activity |
| Add Note / Attachment | UI Note / Attach actions | Linked to record |
| Tag | Tag button | Via `settings.tags` scope |
| Share (URL) | UI Share action | Generates public URL with optional passcode/expiry (Standard+). |

## L.5 Business Logic

1. **Mandatory `Last Name`** (verbatim from official documentation: "This field is mandatory"). Cannot be removed by admin per system rule. Workaround per community topic: use first-name only with placeholder.
2. **Duplicate check**: Settings → Data Administration → Duplicate Check rules per module.
3. **Validation rules**: Custom rules can be authored at Setup → Customization → Modules & Fields.
4. **Approval process**: Available from Standard edition upward; not applicable to Leads by default but admin can add.
5. **Workflow triggers**: Workflow rules can fire on Lead Created / Edited / Created-or-Edited / Deleted / Field Update (per the Workflow KB page; https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules).
6. **Blueprint**: Admin can apply a Blueprint to Leads (typically post-Qualify → Convert → Tracked; per Blueprint design examples).
7. **Assignment rules**: Built-in assignment rules for Leads (round-robin, load-balanced).
8. **Owner-assignment suggestions**: Zia-suggested owner based on past patterns (Enterprise+).

## L.6 Automation

Actions that can be linked to Leads workflows:

| Workflow Action | Per-workflow cap | Source |
|---|---|---|
| Email alerts | up to 5 per action set | https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules |
| Tasks | up to 5 per action set | Same |
| Field updates | up to 5 per action set | Same |
| Webhooks | up to 6 (1 instant + 5 scheduled) | Same |
| Custom functions | up to 6 (1 instant + 5 scheduled) | Same |
| Create record (Leads/Contacts/Accounts/Deals/Cases) | unlimited | Same |
| Notifications (Cliq, Slack, Cisco Webex) | unlimited | Same |
| Convert Lead/Quote/SalesOrder | on Edit/Field Update | Same |
| Add / Remove Tags | unlimited | Same |

## L.7 Reports

Default Lead Reports (admin can extend):

- Leads by Source
- Leads by Status
- Leads by Industry
- Leads by Owner
- Lead Conversion Rate (requires Converted field, account/deal rollup)
- Leads Created (Date / Range)
- Leads by Campaign
- Lead Aging Pipeline

## L.8 Technical

### API endpoints

- `GET /crm/v8/Leads`
- `GET /crm/v8/Leads/{id}`
- `POST /crm/v8/Leads`
- `PUT /crm/v8/Leads`
- `DELETE /crm/v8/Leads`
- `GET /crm/v8/Leads/{id}/Notes`
- `GET /crm/v8/Leads/{id}/Attachments`
- `GET /crm/v8/Leads/{id}/Activities`
- `GET /crm/v8/Leads/{id}/Emails`
- `GET /crm/v8/Leads/deleted?type=recent`

### Trigger parameters

POST/PUT body can include `trigger: ["workflow"]`, `["approval"]`, `["blueprint"]` array.

### Webhook events

- Lead created, updated, deleted, assigned.

### Known limitations

- Custom fields cannot be positioned before `Last Name`.
- Per official exception, `Last Name` cannot be made non-mandatory; workaround is using a placeholder.

## L.9 Cross References

- `../03_Feature_Index.md` — Cadences.
- `../03_Feature_Index.md` — Best Time to Contact.
- `../06_Data_Model.md` — Leads entity.
- `../05_Business_Rules.md` — Lead conversion rules.
- `../07_API_Research.md` — Endpoint conventions.
