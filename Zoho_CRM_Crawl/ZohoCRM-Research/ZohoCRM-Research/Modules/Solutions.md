# Module — Solutions

> Reconstructed from snippets across help namespace + https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields (page unreachable); https://help.zoho.com/portal/en/kb/crm/customer-support/articles/working-with-cases (Case-Solution link).

## SL.1 General Information

- **API name**: `Solutions`
- **OAuth scope**: `ZohoCRM.modules.solutions.ALL`
- **Purpose**: Knowledge-base articles attached to Cases; administrators and support agents curate reuseable answers.
- **Edition**: Free and all paid editions.

## SL.2 Standard Fields

| Field | Type | Notes |
|---|---|---|
| Solution Number | Auto-Number | Unique |
| Solution Owner | Lookup(User) | — |
| Title | Text | mandatory |
| Status | Picklist | Draft / Published / Rejected |
| Type | Picklist | Manual / Automated / Known Error / FAQ |
| Product Name | Lookup(Products) | — |
| Keywords | multi-select | search tags |
| Resolution | TextArea (long text) | body of KB article |
| Add to KB (Public Portal) | Checkbox | controls portal visibility |

## SL.3 UI

- Search by keyword from Case form.
- Suggest Solution in related list of Case detail.

## SL.4 Cross References

- `../Modules/Cases.md`.
- `../06_Data_Model.md`.
