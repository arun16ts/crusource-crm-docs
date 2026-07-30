# Module — Quotes

> Verbatim citation source: https://help.zoho.com/portal/en/kb/crm/manage-inventory/quotes/articles/standard-fields-quotes (successfully crawled).

## Q.1 General Information

- **API name**: `Quotes` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **Scope**: `ZohoCRM.modules.quotes.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Build sales proposals with line items, attach PDF, send to customer, convert to Sales Order when accepted.
- **Edition**: Professional+ (Inventory Management).
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/quotes/articles/standard-fields-quotes

## Q.2 Standard Fields (full table from official page)

| Field Name | Description | Data type | Maximum Limit |
|---|---|---|---|
| Quote Owner | Lookup | Lookup | — |
| **Subject** | "This field is mandatory." | Text box | Alphanumeric(120) |
| Deal Name | Text box | Alphanumeric(40) |
| Quote Stage | Check box / picklist | — |
| Valid Till | Date | Date | — |
| Contact Name | Lookup | Lookup | — |
| Carrier | Pick list | — |
| Shipping | Text box | Alphanumeric(50) |
| Inventory Manager | Text box | Alphanumeric(50) |
| **Account Name** | "This field is mandatory." | Lookup | — |
| Created By | Date/Time | — |
| Modified By | Date/Time | — |
| Billing Address | Compound | 250/30/30/30/30 |
| Shipping Address | Compound | same |
| **Product Name (line item)** | "This field is mandatory." | Lookup | Product record |
| Quantity in Stock | Numeric | Integer |
| **Quantity (line item)** | "This field is mandatory." | Numeric | Integer |
| Unit Price | Currency | — |
| **List Price (line item)** | "This field is mandatory." | Lookup and Numeric | Integers |
| Total | Text box | Alphanumeric |
| Terms & Conditions | Text area | — |
| Description | Text area (long text) | 32000 |

## Q.3 Line-Item Subform Structure

Per the standard-fields page:

- Product Name (Lookup to Products)
- Quantity in Stock (read-only)
- Quantity
- Unit Price
- List Price (Lookup or Numeric)
- Total (calculated: Qty × List Price)
- Discount %
- Tax %
- Adjustments (free text)
- Subtotal / Net Total

## Q.4 UI

### List View

- Standard with filter chips for Quote Stage.
- Default Custom View: Active Quotes.

### Detail View

- Owner chip in header, Stage chip (Draft / Sent / Accepted / Invoiced / Declined — admin configurable).
- Action bar: Edit, Convert to Sales Order, Send Email, Print PDF, Clone, Delete.

### Quote Workflow

- Email template → send PDF to customer with merge fields.
- Stage controls: If accepted → "Convert" available; creates a Sales Order.

## Q.5 Reports

- Conversion rate Quote→Sale.
- Revenue by Quote Stage.
- Quotes Expired (Valid Till < Now).
- Margins = (List Price × Qty − Cost Price × Qty).

## Q.6 Technical

- `GET/POST/PUT/DELETE /crm/v8/Quotes`
- Custom function can be invoked on button "Generate Quote" via Deluge: `zoho.crm.create("Quotes", ...)` (https://help.zoho.com/portal/en/community/topic/custom-function-5-create-quotes-from-deals-with-just-the-click-of-a-button).

## Q.7 Cross References

- `../06_Data_Model.md` — Quotes entity.
- `../04_User_Journeys.md` §4.5.
- `../Modules/Products.md` — line-item source.
