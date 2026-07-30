# Module — Price Books

## PB.1 General Information

- **API name**: `PriceBooks` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **OAuth scope**: `ZohoCRM.modules.pricebooks.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/price-books/articles/standard-fields-price-books

## PB.2 Standard Fields

| Field | Type | Notes |
|---|---|---|
| Price Book Owner | Lookup(User) | — |
| Price Book Name | Text | mandatory (creation step) |
| Active | Checkbox | controls usability |
| Pricing Model | Picklist | **Flat** (single override) or **Differential** (multiplier vs base) |
| Currency | Picklist | per-org currency |
| Description | TextArea | — |

## PB.3 Price-Book Entries (Subform)

| Subform Field | Type |
|---|---|
| Product Name | Lookup(Product) |
| List Price | Currency |
| Min Quantity | Integer |
| Max Quantity | Integer |
| Discount % | Number |

## PB.4 Use-Cases

- "Wholesale Pricing" book.
- "VIP Customer" book with discounts.
- "Volume Pricing" book with banding.

## PB.5 UI

- List view shows Price Book Name, Active, Owner.
- Detail view has Price Book Entries subform row for quick edit all prices (https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products mentions "Update a Product's Multiple List Prices" flow).

## PB.6 Technical

- REST: `GET/POST/PUT/DELETE /crm/v8/Price_Books`.
- Linked line-items on Quotes / Sales Orders / Invoices look up Price Book at quote-creation time.
