# Module — Sales Orders

## SO.1 General Information

- **API name**: `SalesOrders` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **OAuth scope**: `ZohoCRM.modules.salesorders.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Confirmed customer order with delivery state; can convert to Invoice on delivery.
- **Edition**: Professional+ (Inventory Management).
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products (covers Stock auto-update logic); module help page also available in the inventory help namespace.

## SO.2 Standard Fields (inferred from cross-module inventory structure)

| Field | Type | Notes |
|---|---|---|
| Sales Order Owner | Lookup | Default |
| Subject | Text | Usually required |
| Account Name | Lookup(Accounts) | Mandatory |
| Contact Name | Lookup(Contacts) | Optional |
| Deal Name | Lookup(Deals) | Optional |
| Quote Name | Lookup(Quotes) | Optional (linkage) |
| Carrier | Picklist | — |
| Sales Order Date | Date | — |
| Status | Picklist | Draft / Pending Approval / Approved / Delivered / Invoiced / Cancelled |
| Due Date | Date | — |
| Tracking Number | Text | — |
| Billing/Shipping Address | Compound | — |
| Discount % / Total | Currency | — |
| Grand Total | Currency | calculated |
| Sub Total | Currency | calculated |
| Line Items | Subform | Product / Quantity / Unit Price / List Price / Discount / Tax |

## SO.3 Status-Driven Behaviour (verbatim from official docs)

Per https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products (Stock auto-updates):

> "Quantity in demand increases when a sales order is created. Quantity in demand decreases when a sales order is delivered or cancelled. Quantity in demand also decreases when a sales order is converted to an invoice. **The status of the sales order thus converted automatically changed to 'delivered'.**"

## SO.4 UI

- List view filterable by Status.
- Action button "Convert to Invoice" available when Status = Approved/Delivered.
- Action button "Fulfill / Mark Delivered" updates Status and decrements Stock Demand.

## SO.5 Technical

- REST: `GET/POST/PUT/DELETE /crm/v8/Sales_Orders`
- Status enum is configurable per org.
