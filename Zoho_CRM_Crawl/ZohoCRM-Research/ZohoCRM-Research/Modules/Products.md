# Module — Products

## P.1 General Information

- **API name**: `Products` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **Scope**: `ZohoCRM.modules.products.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Catalog of goods and services with on-hand inventory that can be referenced from Quotes, Sales Orders, Invoices, Purchase Orders.
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products

## P.2 Data Model

From the official page (https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products):

| Field | Type | Mandatory | Notes |
|---|---|---|---|
| Product Owner | Lookup(User) | Yes | Default |
| **Product Name** | Text | **Yes** | Cannot be removed |
| Product Code | Text | No | Admin custom |
| Product Active | Checkbox | No | Default ON |
| Product Category | Lookup(Product Categories - new) | No | Subform row option |
| Manufacturer | Text | No | — |
| Vendor Name | Lookup(Vendors) | No | — |
| Sales Start/End Date | Date | No | — |
| Support Start/End Date | Date | No | — |
| Unit Price | Currency | **Yes** | Maps to default Quote line price |
| List Price | Currency | No | — |
| Cost Price | Currency | No | — |
| Quantity in Stock | Integer | No | **Auto-calculated** |
| Reorder Level | Integer | No | Triggers PO generator |
| Quantity in Demand | Integer | No | **Auto-calculated** |
| Quantity Ordered | Integer | No | **Auto-calculated** |
| Description | TextArea | No | 32000 |

## P.3 Stock auto-update logic (verbatim from official docs)

Verbatim, https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products :

> "The details of product quantity in the Stock Information section are updated automatically with reference to the sales order and purchase order and invoice."

State Machine:
- **Quantity in Stock**: increases on PO Delivered; decreases on PO Cancellation; decreases on Invoice creation (incl. via Quote/SO conversion); increases on Invoice cancellation.
- **Quantity in Demand**: increases on Sales Order creation; decreases on Sales Order delivery/cancellation; decreases when SO converted to Invoice (and SO auto-status changes to "Delivered").
- **Quantity Ordered**: increases on PO creation; decreases on PO delivery/cancellation.

## P.4 UI

- List view with sortable columns: Product Name, Product Code, Unit Price, Qty in Stock, Vendor, Active.
- Detail view supports per-product Price Books (related list "Price Books", edit all list prices).
- Tabbed related lists: Price Books, Open Activities, Closed Activities, Cases, Solutions, Attachments, Leads, Contacts, Potentials (Deals), Accounts.

### P.4.1 Reorder-Level "Generate PO"

The Products module exposes an action to "**Generate PO for Records below Reorder Level**" (verbatim). It opens a wizard with vendor selection and full list of products under reorder level, then proceeds to Create Purchase Order.

## P.5 Reports / KSIs

- Stock on hand by Product.
- Stock value (Qty × Cost Price).
- Reorder-Level stock.
- Sales by Product.

## P.6 Technical

- REST endpoints mirror other modules.
- Custom field types allowed include Inventory Templates (subforms with components).

## P.7 Cross References

- `../06_Data_Model.md` — Products entity.
- `../05_Business_Rules.md` §5.13 (Stock Auto-Update Logic).
- `../04_User_Journeys.md` §4.7, 4.8.
