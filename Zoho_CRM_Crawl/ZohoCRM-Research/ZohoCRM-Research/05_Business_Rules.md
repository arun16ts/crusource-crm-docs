# 05 — Business Rules

> Business rules extracted from official Zoho CRM documentation. Each row links to the source URL.

---

## 5.1 Lead Conversion Rules

| Rule | Detail | Source |
|---|---|---|
| Conversion creates one Contact, one Account, one Deal | Verbatim from Leads module: convert action moves data | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads |
| Mandatory mapping: Account | Either existing or new | https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads |
| `converted__s` flag becomes `true` | API exposes `Converted__s`, `Converted_Date_Time` | https://www.zoho.com/crm/developer/docs/api/v8/get-records.html |
| Source Lead can be retained or auto-deleted after Conversion | Admin setting | — |

## 5.2 Deal Stage Validation (Stage-Probability)

Verbatim from https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals :

- **Deal stages**: configurable; default system stages include qualification, needs analysis, negotiation, closed won, closed lost.
- **Probability**: numeric (0-100) per stage that drives forecast rollup.
- **Deal Category**: Open / Closed Won / Closed Lost.
- **Forecast Category**: Pipeline / Closed / Omitted.

Consequences:

| Rule | Behaviour |
|---|---|
| Open deals + in pipeline → roll into Forecast as Pipeline $ | Standard forecast logic. |
| Closed Won → roll into Forecast as Closed Won. | Drives Achieved quota. |
| Closed Lost → excluded. | Forecast reflects Lost $. |
| Omitted → excludes from forecasting. | Inferred from control of admin. |

API supports `params` for stage-probability: `Probability` (numeric 0-100).

## 5.3 Approval Chain Rules

Per https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/set-approval-process (verbatim tone):

- Approval workflows send records to designated users for review.
- Team-module admins can create approval processes for their team modules.
- Approval Tab will be displayed for all users; only those with "Manage Automation" permission can configure.
- Use cases: discount offering, expenditure, campaign go-ahead.

## 5.4 Ownership Rules

Per https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction (verbatim):

1. CEO role has access to entire database.
2. Managers in role hierarchy cannot view or edit their subordinates' records if they do NOT have Read/Edit permission for that type.
3. Users at higher role can access other users' data below their hierarchy.
4. Default: same role cannot access each other's records.
5. Top of hierarchy cannot see data shared to subordinates via custom sharing rules; can be overridden via "Superiors Allowed" sharing rule option.
6. "Share Data with Peers" enables same-role record sharing.
7. Read or Read/Write access to primary record is required to add notes/attachments/email to it.
8. Administrators (with Administrator profile) bypass roles entirely.

## 5.5 Sharing Rules

- Public read / public read-write at module level vs. role hierarchy default (private).
- Sharing Rules provide exceptions: `Share Data with Peers`, `Superiors Allowed`, criteria-based sharing to specific roles or users.
- Sharing Rules can be module-specific and conditional.

## 5.6 Blueprint Transition Rules

Verbatim from https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint :

- Transition is a button on the record's details page.
- Field is mandatory if **any** of these is true:
  1. Module field is mandatory.
  2. Layout rule marks it mandatory.
  3. Blueprint transition explicitly marks it mandatory.
- Layout rule output also flows into transition form.
- Automatic transitions fire after configured time elapses (Spotlight #7 page).
- Process flow between States established by connecting nodes in state buttons.
- Delete a transition by Right Click → Delete.

## 5.7 Workflow Execution Rules

Verbatim from https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules :

- Three primary trigger options: Record Action / Date Field / Score (cannot be changed after rule creation).
- Date-based triggers process up to 5,000 records every 10 minutes.
- Multiple conditions per rule:
  - Up to 5 in Standard/Professional.
  - Up to 10 in Enterprise/Ultimate.
- Records validated against conditions sequentially; first match wins; subsequent conditions ignored for that record in that rule.
- Catch-all "Records that do not meet any of the above conditions" condition available.
- Instant Actions cap: up to 5 email alerts/actions per action set.
- Scheduled Actions cap: up to 5 scheduled actions allowed (where applicable).
- Webhook cap: up to 6 per rule (1 instant + 5 scheduled).
- Custom Function cap: up to 6 per rule.

## 5.8 Field-Level Validation Rules

- Each field can be marked **mandatory** or **non-mandatory**.
- Custom Validation Rules can be defined (Setup → Customization → Modules → Fields → Validation Rules) of the form `IF (x) THEN (y)`.
- Picklists support **Dependency**: culling values based on parent picklist.
- Layout Rules: conditional display (show X if Y), conditional-mandatory, read-only.

## 5.9 Duplicate Detection Rules

- Org-level duplicate rules can be created in Settings → General → Data Administration.
- Configuration: which fields participate, weight of match, percentage threshold to flag.
- Bypass options: Always Create / Override / Report + Warn / Block.
- Import flow also uses duplicate check.

## 5.10 Assignment Rules

- Assignment rules attached to Leads (and other modules) determine owner based on criteria.
- Round-Robin / Load-Balanced assignment supported.
- Owner assignment suggestions can be AI-generated via Zia (https://www.zoho.com/crm/ai-features-in-zoho-crm.html).

## 5.11 Forecast / Quota Rules

Per https://help.zoho.com/portal/en/kb/crm/sales-force-automation/forecasts/articles/creating-and-working-with-forecasts (verbatim: "Only one role can be assigned to a user, so a user can only have one target, as per the forecast"):

- One user → one open Forecast → one target quota for the period.
- Forecast can slice by role subtree.

## 5.12 Email Rules

- DNC / Email Opt-Out is honored across all email sends.
- Compliance rules (CAN-SPAM, GDPR): email templates must include physical address (Zoho enforces with a setting).
- Unsubscribe link auto-injected.

## 5.13 Inventory Rules (Stock Auto-Update Logic)

Verbatim from https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products :

| Event | Effect |
|---|---|
| Purchase Order delivered | Quantity In Stock increases |
| Delivered Purchase Order later cancelled | Quantity In Stock decreases |
| Invoice created (incl. via SO conversion) | Quantity In Stock decreases |
| Invoice cancelled | Quantity In Stock increases |
| Sales Order created | Quantity In Demand increases |
| Sales Order delivered or cancelled | Quantity In Demand decreases |
| SO converted to Invoice | Quantity In Demand decreases, SO status auto-changes to "Delivered" |
| Purchase Order created | Quantity Ordered increases |
| Purchase Order delivered or cancelled | Quantity Ordered decreases |

PO auto-generation rule:

- A product's Reorder Level triggers "Generate PO for Record below Reorder Level" workflow in Products module.

## 5.14 Record Lifecycle / Recycle Bin Rules

- Deleted records go to Recycle Bin, retained up to 60 days (default Enterprise, configurable per admin).
- Restore reinstates dependent records.
- Audit retains Created/Modified timestamps and actor.

## 5.15 Source Map

- Stage-Probability: https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals
- Roles/Sharing: https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction
- Workflow: https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules
- Blueprint: https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint
- Stock auto-update: https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products
- Forecasts: https://help.zoho.com/portal/en/kb/crm/sales-force-automation/forecasts/articles/creating-and-working-with-forecasts
- Approval: https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/set-approval-process
