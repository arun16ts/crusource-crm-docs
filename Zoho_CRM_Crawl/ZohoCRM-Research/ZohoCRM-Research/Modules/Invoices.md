# Module — Invoices

> Verbatim citation source: https://help.zoho.com/portal/en/kb/crm/manage-inventory/invoices/articles/standard-fields-invoices (successfully crawled).

## I.1 General Information

- **API name**: `Invoices` (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- **Scope**: `ZohoCRM.modules.invoices.ALL` (https://www.zoho.com/crm/developer/docs/api/v8/scopes.html)
- **Purpose**: Bill the customer after delivery; supports tax, discount and partial payment.
- **Edition**: Professional+ (Inventory Management).
- **Documentation**: https://help.zoho.com/portal/en/kb/crm/manage-inventory/invoices/articles/standard-fields-invoices

## I.2 Standard Fields (full table from official page)

| Field Name | Description | Data type | Maximum Limit |
|---|---|---|---|
| Invoice Owner | Lookup | — |
| Subject | "This field is mandatory." | Text box | Alphanumeric(50) |
| Sales Order | Lookup (Sales Orders) | — |
| Purchase Order | Text Box | — |
| Excise Duty | Numeric | Numeric |
| Invoice Date | Date |
| Due Date | Date |
| Sales Commission | Currency | Float |
| **Account Name** | "This field is mandatory." | Lookup | — |
| Deal Name | Lookup | — |
| Contact Name | Lookup | — |
| Status | Check box / picklist | — |
| Created By / Modified By | Date/Time | — |
| Billing Address | Compound | same as other modules |
| Shipping Address | Compound | same |
| **Product Name (line item)** | "This field is mandatory." | Lookup |
| Quantity in Stock | Numeric |
| **Quantity** | "This field is mandatory." | Numeric |
| Unit Price | Currency |
| **List Price** | "This field is mandatory." | Lookup/Numeric |
| Total | Currency |
| Terms & Conditions | Text area |
| Description | Text area (long text) | 32000 |

## I.3 Date Calculation

Verbatim from https://www.zoho.com/books/api/v3/invoices/ : "This date is typically calculated as invoice date + payment_terms days, but can be overridden with a custom date."

## I.4 Lifecycle / Status

A common status set (admin-customizable):
- Draft → Open (Unpaid) → Paid (full)
- Overdue (computed whenever Due Date passed and Invoice not fully Paid)
- Partially Paid
- Void
- Closed

## I.5 Automation

- Workflow on Invoice status change: Send Email "Payment Thanks", Update Deal Stage if tied.
- Blueprint can lock Invoice after Paid.

## I.6 Technical

- `GET/POST/PUT/DELETE /crm/v8/Invoices`
- Tax fields are admin-definable (Tax % / Per-Item).
- Refunds supported via Deluge custom function (record with negative amount).

## I.7 Cross References

- `../06_Data_Model.md` — Invoices entity.
- `../05_Business_Rules.md` §5.13 (Stock auto-decrease on Invoice Create).
- `../Modules/SalesOrders.md`.
