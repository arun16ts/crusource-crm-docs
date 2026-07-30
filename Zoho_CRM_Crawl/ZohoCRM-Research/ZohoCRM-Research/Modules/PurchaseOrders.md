# Module — Purchase Orders

## PO.1 General Information

- **API name**: `PurchaseOrders` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **OAuth scope**: `ZohoCRM.modules.purchaseorders.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Order placed to a Vendor to acquire products; manages restocking.
- **Edition**: Professional+ (Inventory Management).

## PO.2 Standard Fields (cross-referenced from official wizard description)

| Field | Type | Notes |
|---|---|---|
| Purchase Order Owner | Lookup(User) | yes |
| Subject | Text | mandatory |
| Vendor Name | Lookup(Vendors) | mandatory |
| Requisition Number | Auto-Number | — |
| Tracking Number | Text | — |
| Purchase Order Date | Date | — |
| Delivery Date | Date | — |
| Status | Picklist | Draft / Pending Approval / Approved / Shipped / Delivered / Billed / Cancelled |
| Bill To Address | Compound | — |
| Ship To Address | Compound | — |
| Grand Total | Currency | calculated |
| Sub Total | Currency | calculated |
| Discount | Currency / % | — |
| Tax | Currency / % | — |
| Adjustment | Currency | — |
| Line Items | Subform | Product / Quantity / Unit Price / List Price / Total |
| Description | TextArea | 32000 |

## PO.3 Workflow Auto-Generation

Per `../04_User_Journeys.md` §4.7 and the Products module Workflow rule "Generate PO for Records below Reorder Level" (https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products):

> The "Generate PO for Record below Reorder Level" page lists products whose Quantity in Stock is below their Reorder Level. Admin selects Vendor + products → click Generate Purchase Order → Create Purchase Order page receives populated line items.

## PO.4 Auto-Create From Sales Order

Sales Order creation (via workflow custom function) can spawn a Purchase Order for backordered products (https://www.zoho.com/crm/resources/solutions/auto-create-purchase-order-from-sales-order.html).

## PO.5 Technical

- REST mirror schema: `GET/POST/PUT/DELETE /crm/v8/Purchase_Orders`.
- Webhooks: created/updated/deleted.
