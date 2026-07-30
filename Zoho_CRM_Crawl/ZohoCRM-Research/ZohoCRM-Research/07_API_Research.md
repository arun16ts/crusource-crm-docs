# 07 — API Research

> Source of every claim: https://www.zoho.com/crm/developer/docs/api/v8/ and the V8 sub-pages. No memory-filled values; everything in this document traces to a URL in `10_References.md`.

---

## 7.1 Authentication

- **Protocol**: OAuth 2.0 (https://www.zoho.com/crm/developer/docs/api/v8/oauth-overview.html).
- **Header**: `Authorization: Zoho-oauthtoken {access_token}` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html, verbatim example header).
- **DC-aware accounts URL**: e.g. `https://accounts.zoho.com/oauth/v2/auth?...` (US data center). For `.eu`, `.in`, `.com.au`, `.jp`, the host changes accordingly.
- **Inline example** (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html):
  ```
  https://accounts.zoho.com/oauth/v2/auth?scope=ZohoCRM.modules.ALL,ZohoCRM.settings.ALL&client_id={client_id}&response_type=code&access_type={"offline"or"online"}&redirect_uri={redirect_uri}
  ```

## 7.2 Scope Grammar

Format `service_name.scope_name.OPERATION_TYPE`. Operation types: `ALL`, `CREATE`, `READ`, `UPDATE`, `DELETE`.

Full scope list (verbatim from https://www.zoho.com/crm/developer/docs/api/v8/scopes.html):

| Service name | Scope name | Operations |
|---|---|---|
| users | users | ALL |
| org | org | ALL |
| settings | settings / settings.territories / settings.custom_views / settings.related_lists / settings.modules / settings.variables / settings.tags / settings.tab_groups / settings.fields / settings.layouts / settings.macros / settings.custom_links / settings.custom_buttons / settings.roles / settings.profiles / settings.currencies | ALL / scoped |
| modules | modules.ALL, modules.approvals, modules.leads, modules.accounts, modules.contacts, modules.deals, modules.campaigns, modules.tasks, modules.cases, modules.events, modules.calls, modules.solutions, modules.products, modules.vendors, modules.pricebooks, modules.quotes, modules.salesorders, modules.purchaseorders, modules.invoices, modules.custom, modules.dashboards, modules.notes, modules.activities, modules.search, modules.services, modules.appointments, modules.appointments_rescheduled_history | ALL/CREATE/READ/UPDATE/DELETE |
| bulk | bulk.ALL, bulk.READ, bulk.CREATE | — |
| notifications | notifications.READ, notifications.CREATE, notifications.UPDATE, notifications.DELETE | — |
| coql | coql.READ | — |

Webflow-style explicit URL example (separating modules):

```
scope=ZohoCRM.modules.leads.ALL,ZohoCRM.modules.deals.ALL,ZohoCRM.settings.ALL
```

## 7.3 Base URL & API version

```
{api-domain}/crm/{version}/{module_api_name}
```

e.g. `https://www.zohoapis.com/crm/v8/Leads`.

## 7.4 Get Records

https://www.zoho.com/crm/developer/docs/api/v8/get-records.html :

### Endpoints

- `GET /crm/v8/{module_api_name}` — list records
- `GET /crm/v8/{module_api_name}/{record_id}` — single record

### Query Parameters (verbatim)

| Param | Mandatory | Description |
|---|---|---|
| `fields` | Yes (when fetching all records) | Comma-separated API names of fields. Max 50. |
| `cvid` | No | Custom view ID. |
| `ids` | No | Comma-separated record IDs. |
| `per_page` | No | Default 200, Max 200. |
| `page` | No | Valid up to 2000 records. |
| `page_token` | Yes (to fetch >2000) | Carry `next_page_token` from response. Allows up to 100,000 records. |
| `sort_order` | No | `asc` / `desc`. Default `desc`. |
| `sort_by` | No | `id` / `Created_Time` / `Modified_Time`. |
| `converted` | No | For Leads: `true` / `false` / `both`. |
| `territory_id` | No | Long, filters by territory. |
| `include_child` | No | Boolean, includes child territories. |

### Example response (verbatim)

```json
{
  "data": [
    {
      "Converted_Date_Time": "2022-11-21T15:12:13+05:30",
      "Email": null,
      "Last_Name": "test8000",
      "id": "3652397000009851001",
      "Record_Status__s": "Available",
      "Converted__s": true
    }
  ],
  "info": {
    "call": false,
    "per_page": 5,
    "next_page_token": "c8582xx9e7c7",
    "count": 5,
    "sort_by": "id",
    "page": 1,
    "previous_page_token": null,
    "page_token_expiry": "2022-11-21T15:08:14+05:30",
    "sort_order": "desc",
    "email": false,
    "more_records": true
  }
}
```

## 7.5 Get Related Records

`GET /crm/v8/{module_api_name}/{record_id}/{related_list_api_name}` — fetches related records, e.g. deals for a contact.

Required scopes (per `zoho/zohocrm-nodejs-sdk-6.0` GitHub README verbatim, cross-referenced with the official scopes page): `ZohoCRM.modules.ALL`, `ZohoCRM.settings.ALL`, `ZohoCRM.settings.related_lists.ALL`.

## 7.6 Get Modules

https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html :

- `GET /crm/v8/settings/modules`
- Returns list of modules with API names, supported operations, visibility status.

## 7.7 Update Records

`PUT /crm/v8/{module_api_name}` — body array of records. Each record has `id` + updated fields. Triggers can be passed in the request via `?trigger=workflow` etc.

## 7.8 Delete Records

`DELETE /crm/v8/{module_api_name}?ids={csv}`.

`GET /crm/v8/{module_api_name}/deleted` — returns id of recently deleted (https://help.zoho.com/portal/en/community/topic/get-details-of-a-delete-record-via-api).

## 7.9 API Limits (https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html)

### Credit-based system

- The limit is on **credits**, not raw API count.
- Credits are tracked in a rolling 24-hour window.

### Allowed credits & max per edition

| Edition | Allowed Credits Formula | Maximum Credits |
|---|---|---|
| Free Edition | 5,000 | 5,000 |
| Standard/Starter Edition | 50,000 + (Number of User licenses × 250) + Add-on credits | 100,000 |
| Professional | 50,000 + (Number of User licenses × 500) + Add-on credits | 3,000,000 |
| Enterprise/Zoho One | 50,000 + (Number of User licenses × 1,000) + Add-on credits | 5,000,000 |
| Ultimate/CRM Plus | 50,000 + (Number of User licenses × 2,000) + Add-on credits | Unlimited |

### Bulk limits

- Insert/Update/Upsert max 100 records per API call.
- Add/Remove Tags max 500 records per API call.
- Max credits deducted for these calls = 10.

### Concurrent API call limits

| Edition | Concurrent calls |
|---|---|
| Free | 5 |
| Standard/Starter | 10 |
| Professional | 15 |
| Enterprise/Zoho One | 20 |
| Ultimate/CRM Plus | 25 |

## 7.10 Notes / Attachments

- Notes API: `POST/GET/PUT/DELETE /crm/v8/Notes` (https://www.zoho.com/crm/developer/docs/api/v8/ — verified snippet).
- Attachments API mirrors notes with file-upload support.

## 7.11 Functions (Deluge)

https://www.zoho.com/crm/developer/docs/functions/ :

- Server-side scripting with Deluge.
- Functions are invoked from Workflow Rules, Standalone Custom Buttons, Related Lists, or Schedules.
- Method `zoho.crm.invokeUrl("GET"/"POST", url, headers, params)` to call REST APIs from Deluge.
- Maximum Standalone Functions per org: depends on edition (Ultimate has higher limits).

## 7.12 Webhooks

https://help.zoho.com/portal/en/kb/crm/automate-business-processes/actions/articles/webhooks-workflow :

- Outbound HTTP POST to configured URL.
- Payload includes the triggering record's data and event info.

Inbound webhooks:

- A custom function can declare an HTTP endpoint and be invoked when called; Kaizen #37 https://help.zoho.com/portal/en/community/topic/kaizen-37-webhooks-in-zoho-crm details.

## 7.13 Bulk Read

- The `bulk.read` API lets you queue + download large result sets asynchronously.

## 7.14 COQL (Zoho CRM Object Query Language)

Scope `coql.READ` per https://www.zoho.com/crm/developer/docs/api/v8/scopes.html.

- SQL-like syntax with `SELECT … FROM Module WHERE … LIMIT …`.
- Useful for custom ad-hoc queries.

## 7.15 SDKs

Official SDKs (per https://www.zoho.com/crm/developer/docs/api/v8/ page index and GitHub presence):

| Language | Repo |
|---|---|
| Java | `zoho/zohocrm-java-sdk` |
| Python | `zoho/zohocrm-python-sdk` |
| Node.js | `zoho/zohocrm-nodejs-sdk-6.0` |
| .NET / C# | `zoho/zohocrm-csharp-sdk` |
| PHP | `zoho/zohocrm-php-sdk` |
| Go | `zoho/zohocrm-go-sdk` |
| Ruby | — (third-party) |

## 7.16 Sample `curl` request — Get Leads

```bash
curl -X GET \
  'https://www.zohoapis.com/crm/v8/Leads?fields=Last_Name,First_Name,Email,Company,Lead_Status,Lead_Source&per_page=200' \
  -H 'Authorization: Zoho-oauthtoken 1000.abcdef...'
```

## 7.17 Sample `curl` request — Insert Lead

```bash
curl -X POST \
  'https://www.zohoapis.com/crm/v8/Leads' \
  -H 'Authorization: Zoho-oauthtoken 1000.abcdef...' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": [
      {
        "Last_Name": "Smith",
        "First_Name": "John",
        "Company": "Acme Co",
        "Lead_Status": "Not Contacted",
        "Lead_Source": "Web",
        "Email": "john@example.com"
      }
    ],
    "trigger": ["workflow"]
  }'
```

## 7.18 Source Map

- API V8 root: https://www.zoho.com/crm/developer/docs/api/v8/
- Modules: https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html
- Scopes: https://www.zoho.com/crm/developer/docs/api/v8/scopes.html
- Get Records: https://www.zoho.com/crm/developer/docs/api/v8/get-records.html
- Update Records: https://www.zoho.com/crm/developer/docs/api/v8/update-records.html
- Delete Records: https://www.zoho.com/crm/developer/docs/api/v8/delete-records.html
- Get Related Records: https://www.zoho.com/crm/developer/docs/api/v8/get-related-records.html
- API Limits: https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html
- OAuth 2.0: https://www.zoho.com/crm/developer/docs/api/v8/oauth-overview.html
- Functions: https://www.zoho.com/crm/developer/docs/functions/
- Signals: https://www.zoho.com/crm/developer/docs/signals/
