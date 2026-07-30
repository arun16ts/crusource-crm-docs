# Module — Vendors

## V.1 General Information

- **API name**: `Vendors` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **OAuth scope**: `ZohoCRM.modules.vendors.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/vendors/articles/standard-fields-vendors

## V.2 Standard Fields (reconstructed from help namespace and API patterns)

| Field | Type | Max | Mandatory | Source |
|---|---|---|---|---|
| Vendor Owner | Lookup(User) | — | yes | standard |
| **Vendor Name** | Text | Alphanumeric(50) | **Yes** | https://help.zoho.com/portal/en/kb/crm/manage-inventory/vendors/articles/standard-fields-vendors (standard fields page) |
| Phone | Text | Alphanumeric(50) | No | standard |
| Email | Email | Alphanumeric(100) | No | Email support confirmed: https://www.facebook.com/groups/614098037282429/posts/749721720386726/ — cross-reference only |
| Website | URL | Alphanumeric(255) | No | — |
| Category | Picklist | — | No | — |
| Billing Address | Compound | 250/30/30/30/30 | No | — |
| Shipping Address | Compound | same | No | — |
| Description | TextArea | 32000 | No | — |

## V.3 UI / Workflow

- Related list per Vendor: Products (belonging to this Vendor), Purchase Orders, Contacts (mapped via Vendor→Contact relation), Notes, Attachments, Activities.

## V.4 Cross References

- `../06_Data_Model.md` — Vendors entity.
- `../Modules/PurchaseOrders.md`.
