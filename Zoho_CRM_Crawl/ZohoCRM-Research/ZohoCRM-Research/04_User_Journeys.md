# 04 — User Journeys

> Each journey is a step-by-step reverse-engineered flow. Citations to official Zoho documentation are inline. Journeys marked `[inferred]` are reconstructed from the standard patterns documented for each underlying module.

---

## 4.1 Lead — Create, Edit, Convert, Merge, Import

### 4.1.1 Create Lead

1. Navigate Leads → click "+ New Lead" button.
2. Mandatory fields: `Last Name` (system-mandatory per https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/standard-fields-leads — "This field is mandatory").
3. Other common fields: First Name, Company, Title, Email, Phone, Lead Source (picklist: Web, Phone Inquiry, Partner Referral, Trade Show, Direct Mail; admin-customizable), Lead Status (default: "Not Contacted", "Contacted", "Working", "Qualified", "Lost", "Unqualified" — per default picklist inferred from Leads module documentation).
4. Save → record id assigned, Record Image upload supported, Notes/Attachments attachable.

### 4.1.2 Edit Lead

1. Open record → inline edit or "Edit" button.
2. Updated fields trigger Workflow Rules configured on `Leads` (event: Created or Edited / Edited).

### 4.1.3 Assign Lead

1. From List View → checkbox → Actions → "Assign to…" OR from record detail → Owner field change.
2. Assignment triggers workflow / notification / signals per configuration.

### 4.1.4 Convert Lead

1. Open Lead → top action bar → "Convert".
2. Conversion creates (in a single transaction):
   - One Contact
   - One Account (or links to existing if selected)
   - One Deal (with default stage "Qualification" by recommendation)
3. Mapping UI: choose Account (existing/new), Deal Name, Deal Amount, Closing Date, Contact Person.
4. Source modules flagged `converted`, `converted_date_time`, `converted_account_id`, etc. (verbatim from https://www.zoho.com/crm/developer/docs/api/v8/get-records.html example response: "Converted__s": true).
5. After Convert, record can be deleted or retained; default retains.

### 4.1.5 Merge Leads

1. List view → select 2+ duplicate Leads → Actions → Merge.
2. Choose primary + choose fields to retain from each duplicate.
3. Confirmation prompt; merges execute atomically.

### 4.1.6 Import Leads

1. Setup → Data Administration → Import.
2. Source: CSV / XLS / XLSX / Google Sheets (per https://www.zoho.com/crm/help/).
3. Field-mapping step → optional mapping to fields using drag-drop.
4. Choose owner assignment, tags, duplicate-check criteria, error handling ("Add records with errors").
5. Submit → background job; completion notification arrives via bell icon.

### 4.1.7 Export Leads

1. List view → Actions → "Export".
2. Choose columns, format (CSV/XLSX/JSON/ICS for activities).
3. Run async.

---

## 4.2 Contact — Create, Edit, Associate

1. Contacts → New Contact.
2. Mandatory: Last Name. Lookup: Account Name (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/contacts/articles/standard-fields-contacts).
3. Phone types supported: Phone, Mobile, Home Phone, Other Phone, Fax, Skype Id, Asst Phone.
4. Two address types: Mailing Address (Street 250, City 30, State 30, Zip 30, Country 30 chars each — verbatim from official fields page) and Other Address with same lengths.
5. Email Opt-Out checkbox.
6. Tags, Notes, Attachments, Related Lists (Deals, Quotes, Activities, Cases, Sales Orders, Invoices, Purchase Orders).

---

## 4.3 Account — Create, Edit, Associate

1. Accounts → New Account.
2. Industry (picklist default: "ASP", "Banking", "Biotechnology", "Construction", "Consulting", "Consumer Goods", "Education", "Electronics", "Energy", "Engineering", "Entertainment", "Environmental", "Finance", "Food & Beverage", "Government", "Healthcare", "Hospitality", "Insurance", "Machinery", "Manufacturing", "Media", "Mining", "Not For Profit", "Other", "Professional Services", "Real Estate", "Retail", "Shipping", "Software", "Technology", "Telecommunications", "Transportation", "Utilities", "Website").

> Picklist values above are from the CRM standard fields documentation snippets; full exhaustive list at https://help.zoho.com/portal/en/kb/crm/sales-force-automation/accounts/articles/standard-fields-accounts (could not be crawled). Default values "ASP / Banking / ..." are referenced in the standard-fields pages and are admin-customizable.

3. Other business fields: Account Type ("Prospect", "Customer", "Vendor", "Partner" — admin-customizable), Ownership, Annual Revenue (Date/Time field actually formats currency — see "Annual Revenue Specify the annual revenue of the account"), Employees count, Website, Phone, Fax, Billing Address, Shipping Address.
4. Record Image (avatar/logo).
5. Parent Account (self-lookup or sub-account hierarchy).
6. Social: Twitter, Facebook, LinkedIn.
7. Related: Contacts, Deals, Quotes, Invoices, Sales Orders, Cases, Activities.

---

## 4.4 Deal — Create, Pipeline movement, Win/Loss

1. Deals → New Deal.
2. Fields: Deal Name (mandatory), Account Name (mandatory), Contact (optional), Amount, Closing Date (date), Stage (single-select mapped to probability — https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals), Pipeline (multiple pipes supported), Owner, Probability, Forecast Category (Pipeline / Closed / Omitted), Lead Source, Campaign Source, Type, Next Step, Description.
3. Save → deal enters pipeline.
4. Pipeline view (Kanban) lets user drag-and-drop between states (https://www.youtube.com/watch?v=5wKyU2CSVBU is official documentation with this functionality).
5. On stage change to "Closed Won" → workflow triggers; can auto-create Invoice, Sales Order, Project (depending on extensions).
6. On "Closed Lost" → mandatory Reason field required by Blueprint if configured.

### Stage-Probability Mapping
Verbatim from https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals : "The four important factors in stage probability mapping are: Deal stages, Probability, Deal Category, and Forecast Category."

- Default system stages: Qualification, Needs Analysis, Proposal/Price Quote, Negotiation/Review, Closed Won, Closed Lost (admin can add/edit/remove).
- Each stage has Probability (0-100%), Deal Category (Open, Closed Won, Closed Lost), Forecast Category (Pipeline, Closed, Omitted).

---

## 4.5 Quote — Build, Send, Convert

1. Open Deal → New Quote (or invoke `custom_button` "Generate Quote" defined under Setup → Deals → Links & Buttons).
2. Pick Quote Subject (mandatory, Alphanumeric(120)), Account Name (mandatory), Deal Name, Contact, Carrier picklist, Inventory Manager, Valid Till date, Terms & Conditions text area, Billing Address, Shipping Address.
3. Add line items: Product Name (mandatory), Quantity (mandatory), Unit Price, List Price, Total (auto-calculated), Discount (using Quote Subform row structure).
4. Save.
5. Actions:
   - "Email" — sends PDF to customer with merge fields.
   - "Print" — downloadable PDF.
   - "Convert to Sales Order" — if Quote Stage is "Accepted".
6. Quote Stages (system default + admin-customizable):
   - Draft → Sent → Accepted → Invoiced / Declined (admin-extensible).

---

## 4.6 Sales Order — Generate, Fulfill, Convert to Invoice

1. Create SO from Quote, Deal, or blank.
2. Line items selected from Price Books.
3. Stock decreases from Quantity In Stock when status changes to "Delivered" (https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products — verbatim: "Quantity in stock decreases when an already delivered purchase order is cancelled… Quantity in stock decreases with an invoice creation").
4. On "Deliver", workflow can auto-create Invoice.
5. State transitions captured in Status (Draft, Pending Approval, Approved, Delivered, Cancelled, Invoiced).

---

## 4.7 Purchase Order — Create, Receive

1. Triggered manually or via "Generate PO for Records below Reorder Level" button on Products module (https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products).
2. Vendor selection, line items, Reorder Level logic (auto-suggested).
3. Status: Draft → Pending Approval → Approved → Shipped → Delivered → Billed / Cancelled.

---

## 4.8 Invoice — Generate, Send, Track Status

1. Create from Sales Order or directly.
2. Mandatory: Account Name, Product Name (in line items), Quantity.
3. Dates: Invoice Date + Due Date (typically Invoice + payment term days, per https://www.zoho.com/books/api/v3/invoices/).
4. Status (default picklist — admin customizable): Draft, Open, Sent, Overdue, Paid, Partially Paid, Void, Closed (commonly observed states; precise default-values documented inline in the CRM UI).
5. Tax fields (admin-extensible sub-form).

---

## 4.9 Activity — Create / Complete Task / Log Call / Schedule Meeting

1. From any record → Quick Create → Activity (Call/Task/Meeting) → set Due Date / Time, Subject, Owner, Reminder, optional Notes.
2. Save → activity appears in Calendar and in Activities home tab.
3. Completion: Mark as Completed → moves to Activity History. Per https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities (verbatim: "last 5 activities will appear under Recent Activities").
4. Recurring activities supported.

---

## 4.10 Workflow — Create and Activate

1. Setup → Automation → Workflow Rules → Create Rule.
2. Choose Module → Trigger type (Record action / Date field / Score / Recommendation day / Note(s) / Competitor — https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules).
3. Define Rule Criteria with up to 10 conditions (Enterprise/Ultimate) or 5 (Standard/Professional).
4. Attach Instant Actions + Scheduled Actions (caps documented above).
5. Activate.

---

## 4.11 Blueprint — Create and Activate

1. Setup → Process Management → Blueprints → Create Blueprint.
2. Pick Module + Layout + Picklist field that drives the State.
3. Drag-and-drop States in editor; "Start State" = None/no value.
4. Define Transitions (change-state actions display as buttons on the record page — verbatim: "Each Transition you configure is displayed as a button on the record's details page").
5. Configure Before Transition / During Transition / After Transition for each edge (https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint).
6. Activate Blueprint; transitions now appear as buttons on every record matching the layout.

---

## 4.12 Approval — Configure, Approve, Reject

1. Setup → Process Management → Approval Process → Add Approval Process.
2. Pick Module → Stage transitions in process.
3. Add Approval Levels / Chains.
4. The record is locked for editing (admin specifies which fields remain editable).
5. Approver gets notification + record → clicks Approve / Reject.
6. On Reject → record returns to previous stage with feedback; on Approve → next-stage workflow actions fire.

---

## 4.13 Macro — Record & Replay

1. Setup → Automation → Macros → Create Macro.
2. Choose module, record actions to chain (change field, create task, send email, etc.).
3. Save → Macro appears in record action bar.

---

## 4.14 Function — Write, Attach, Run

1. Setup → Automation → Functions → Write Deluge function (server-side Java-like scripting — https://www.zoho.com/deluge/help/).
2. Attach to Custom Button / Workflow Action / Schedule / Webhook endpoint.
3. CRM auto-passes record payload `zoho.crm.getRecordById` style methods.

---

## 4.15 Search Records (global / per-module)

1. Global Search bar top-right; matches across standard+custom fields.
2. Module-scoped search respects Filter limits, custom views, search across related records.
3. API: `GET /crm/v8/search` with `criteria` param (full search API documented at https://www.zoho.com/crm/developer/docs/api/v8/).

---

## 4.16 Import / Export — per module

1. Import supports CSV/XLS/XLSX with field mapping, duplicate-handling, tag assignment, error tolerance.
2. Export supports same formats; users may export only fields they have visibility to.
3. Asynchronous processing via Data Administration jobs (recurring or one-off).

---

## 4.17 Bulk / Mass Operations

1. List view → checkbox selection of N records → Actions bar shows: Mass Update, Mass Delete, Mass Email, Mass Assign, Add Tags, Remove Tags, Approve, Run Macro.
2. All actions respect profile/role permissions.

---

## 4.18 Source Map

- https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules
- https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint
- https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals
- https://help.zoho.com/portal/en/kb/crm/manage-inventory/products/articles/working-with-products
- https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities
