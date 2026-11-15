# Contacts Mandatory Fields & Saved Views Plan

> **Owner repositories:** `crusource-crm-frontend/`, `crusource-crm-backend/`, `crusource-crm-docs/`
> **Scope guard:** Mandatory Contact fields (**First Name**, **Last Name**, **Company Name**, **Email**, **Phone**) match Lead creation parity and apply to **Contacts creation & bulk import**, without breaking Lead Conversion (`ContactCreator`), Deal CSV auto-stubbing (`ImportDealsService`), Zoho/Data Admin migration defaults (`record_import_service.py`), or partial `PATCH /api/v1/contacts/{id}` edits on legacy Contacts.

---

## 1. Verified Problems & Root Causes

| # | Requirement / Gap | Verified Root Cause in Codebase |
|---|---|---|
| 1 | **Contacts form marks fields with `*` yet only validates Last Name** | `AddContactModal.tsx` renders red `*` on `First Name *` (via `PersonNameFields.tsx:48-51`), `Email *` (line 215), and `Phone *` (line 236), and renders `Company Name` without `*` (line 297). However, `contactBase` (`crmSchemas.ts:98-118`) defines `first_name: personNameSchema.optional()`, `email: emailSchema.optional()`, `phone: phoneSchema.optional()`, `company: companyNameSchema.optional()`, leaving only `last_name: requiredPersonNameSchema("Last name")` mandatory — unlike `leadBase` (`crmSchemas.ts:53-60`), which requires `first_name`, `last_name`, `company`, `office_email`, and `phone`. |
| 2 | **Backend & Bulk Import allow incomplete Contacts** | `ContactCreate` (`crusource-crm-backend/src/modules/contacts/commands/contact_commands.py:18-37`) leaves `first_name`, `email`, `phone`, and `company` as `Optional[str] = None`. Similarly, `CONTACT_IMPORT_FIELDS` (`bulkImportFields.constants.ts:41-47`) only marks `last_name` with `required: true` (`first_name`, `email`, `phone`, and `company` are unstarred/optional). |
| 3 | **Contacts page lacks Saved Views** | `contacts/page.tsx:376-418` passes `columnsToggle`, export/import, filters, and search into `<EntityActionBar>`, but omits `savedViewsToggle={<SavedViewsDropdown entityType="contacts" ... />}` that Accounts, Deals, Leads, Calls, Meetings, and Tasks already use. Backend `saved_views` routes (`saved_views_routes.py`) and commands (`saved_view_commands.py`) already accept arbitrary `entity_type` strings such as `"contacts"` without schema changes. |
| 4 | **Saved View / Filter fidelity gaps on Contacts** | 1) `ContactsFilterPanel.tsx:114` exposes `<option value="designation">`, yet `_filtered_contacts` (`contacts_repository.py:31-62`) does not handle `normalized_search_by == "designation"` against `Contact.title` (nor include `title`/`Account.account_name` cleanly when applying Saved Views with `searchBy: "designation"`). 2) `ContactsFilterPanel.tsx:128-145` builds `<select>` options solely from the current page's `availableContactSources`, so applying a Saved View whose `contact_source` is missing from the current result page drops the visible selected label in the filter panel. |

---

## 2. Phase-Wise Implementation Plan

### Phase 1 — Align Mandatory Contact Fields with Leads (`crusource-crm-frontend` + `crusource-crm-backend`)

#### 1.1 Frontend Validation, Form Asterisks & Bulk Import (`crusource-crm-frontend`)
1. **`src/lib/validations/crmSchemas.ts`**:
   - Update `contactBase` (`contactCreateSchema`) to require the exact same 5 mandatory Lead fields:
     - `first_name: requiredPersonNameSchema("First name")`
     - `last_name: requiredPersonNameSchema("Last name")`
     - `company: requiredCompanyNameSchema`
     - `email: requiredEmailSchema("Email")`
     - `phone: requiredPhoneSchema("Phone")`
   - Keep `middle_name` (`(Optional)`), `alternative_number`, `title`, `department`, `contact_source`, `linkedin`, `website`, `mailing_*`, `description`, `account_id` optional.
2. **`src/components/contacts/AddContactModal.tsx`**:
   - Add `<span className="text-red-500">*</span>` beside `{t("form.company")}` (line 297) so all 5 mandatory fields (`First Name *`, `Last Name *`, `Email *`, `Phone *`, `Company Name *`) carry consistent visual indicators and red border + error text on invalid submit.
   - Preserve existing edit-mode prefill (`editContact.account?.account_name || editContact.company || ""`) so editing Contacts already linked to an Account pre-populates `Company Name *` automatically.
3. **`src/constants/bulkImportFields.constants.ts`**:
   - Update `CONTACT_IMPORT_FIELDS`:
     - `{ key: "first_name", label: "First Name *", required: true }`
     - `{ key: "last_name", label: "Last Name *", required: true }`
     - `{ key: "email", label: "Email *", type: "email", required: true }`
     - `{ key: "phone", label: "Phone *", required: true }`
     - `{ key: "company", label: "Company Name *", required: true }`

#### 1.2 Backend Schema Enforcement & Migration/Conversion Safety (`crusource-crm-backend`)
1. **`src/modules/contacts/commands/contact_commands.py`**:
   - Change `ContactCreate` fields:
     - `first_name: str`
     - `last_name: str`
     - `email: str`
     - `phone: str`
     - Keep `company: Optional[str] = None` and `account_id: Optional[UUID4] = None` in signature, and enforce via `@model_validator(mode='after')` (`_require_mandatory_contact_fields`):
       - `first_name`, `last_name`, `email`, `phone` must all be non-empty strings after stripping/cleaning (with clear validation messages matching Leads).
       - Require company identification: either `company` is non-empty (`>= 2` chars) **or** `account_id` is provided (protecting programmatic/bulk-import API callers linking an existing `account_id`).
   - Note for `BulkContactImportRequest`: if `target_account_id` is supplied on the bulk-import parent request, `BulkImportContactsCommandHandler` already links rows to `target_account_id`; if `ContactCreate` rejects omitted `company` when row-level `account_id` is None, document/pass `company` in CSV rows (already required in `CONTACT_IMPORT_FIELDS`).
   - In `ContactUpdate`: keep all fields `Optional[str] = None` so unrelated partial `PATCH` updates on legacy Contacts succeed, **and** add `@model_validator(mode='after')` (`_prevent_clearing_required_fields`) inspecting `model_fields_set` so explicitly setting `first_name`, `last_name`, `email`, `phone` to `None`/empty string fails validation (`422`), and explicitly clearing `company=""` when no `account_id` is retained fails validation (`422`).
2. **Preserve ORM `nullable=True` & Legacy Importers**:
   - Keep `Contact` ORM columns (`src/modules/contacts/repositories/models.py`) `nullable=True` for `first_name`, `email`, `phone`, `account_id` so `ContactCreator.create_contact_from_lead`, `ImportDealsService` stub Contacts, and existing DB records continue working seamlessly.
   - Update `_fill_contact_defaults` (`src/modules/data_admin/services/record_import_service.py`) so Zoho/Data Admin imports missing `first_name`, `email`, `phone`, or `company` backfill safe defaults when absent (while still rejecting invalid values such as `"not-an-email"`), matching `_fill_lead_defaults`.
3. **Update Existing Backend Test Payloads**:
   - Update Contact test fixtures that omitted `first_name`, `phone`, or `company` (`tests/test_accounts_enhancement.py`, `tests/test_sales_production_hardening.py`, `tests/test_audit_logs.py`, `tests/test_create_submission_postgres.py`, `tests/test_sales_activities_phase2.py`), and add dedicated negative/positive tests for Contact required fields.

---

### Phase 2 — Saved Views in the Contacts Section (`crusource-crm-frontend` + `crusource-crm-backend`)

1. **`crusource-crm-frontend/src/app/dashboard/contacts/page.tsx`**:
   - Import `SavedViewsDropdown` from `@/components/shared/SavedViewsDropdown`.
   - Pass `savedViewsToggle` to `<EntityActionBar>`:
     ```tsx
     savedViewsToggle={
       <SavedViewsDropdown
         entityType="contacts"
         currentFilters={{
           search: filters.search,
           searchBy: filters.searchBy,
           contact_source: filters.contact_source,
         }}
         onApplyView={(savedFilters) =>
           setFilters((prev) => ({
             search:
               typeof savedFilters.search === "string"
                 ? savedFilters.search
                 : "",
             searchBy:
               typeof savedFilters.searchBy === "string"
                 ? savedFilters.searchBy
                 : "all",
             contact_source:
               typeof savedFilters.contact_source === "string"
                 ? savedFilters.contact_source
                 : "",
             page: 1,
             pageSize: prev.pageSize,
           }))
         }
       />
     }
     ```
2. **`crusource-crm-frontend/src/components/contacts/ContactsFilterPanel.tsx`**:
   - Merge `CRM_CONTACT_SOURCES`, `availableContactSources`, and `localFilters.contact_source` (when non-empty) into a sorted, deduplicated option list so any Saved View source filter always displays and stays selectable in the panel even if the filtered page has zero rows.
3. **`crusource-crm-backend/src/modules/contacts/repositories/contacts_repository.py`**:
   - Add `elif normalized_search_by == "designation":` inside `_filtered_contacts` to match `Contact.title.ilike(...)`, and include `Contact.title.ilike(...)` in the default `"all"` search branch so Contacts Search + Filter + Saved Views work accurately across every `searchBy` option shown in `ContactsFilterPanel`.

---

### Phase 3 — Verification Plan
1. **Backend (`crusource-crm-backend/.venv/Scripts/python.exe -m pytest`)**:
   - New dedicated test coverage in `tests/test_contacts_enhancement.py`:
     - `POST /api/v1/contacts` rejects missing/blank `first_name`, `last_name`, `email`, `phone`, and missing `company` (when `account_id` absent) with `422`.
     - `POST /api/v1/contacts` succeeds with valid 5 mandatory fields (or `account_id` linking company); `PATCH /api/v1/contacts/{id}` allows partial unrelated updates and blocks explicit empty clears (`422`).
     - `GET/POST/DELETE /api/v1/saved-views` works with `entity_type="contacts"` and persists/applies `{search, searchBy, contact_source}`; `GET /api/v1/contacts?searchBy=designation&q=...` filters by `Contact.title`.
   - Re-run regression suites: `test_saved_views.py`, `test_data_admin_import_validation.py`, `test_bulk_import_all_modules.py`, `test_sales_activities_phase2.py`, `test_sales_production_hardening.py`, `test_audit_logs.py`, `test_crm_api_endpoints.py`, `test_phase6_concurrency_control.py`, `test_accounts_enhancement.py`.
2. **Frontend (`crusource-crm-frontend`)**:
   - `npx.cmd tsc --noEmit`
   - `npx.cmd eslint` on modified files
   - `npx.cmd tsx tests/test_translation_contracts.ts`
   - `npx.cmd tsx tests/test_enterprise_crm_features.tsx`
   - New Playwright E2E browser test `tests/test_contacts_enhancement_browser.mjs`:
     - Opens `/dashboard/contacts` -> opens `Add New Contact` -> clicks `Save Contact` empty -> verifies all 5 mandatory fields show red validation errors (`First name is required`, `Last name is required`, `Company is required (min 2 characters)`, `Email is required`, `Phone is required`) and `Company Name` renders `*`.
     - Fills valid fields -> creates contact cleanly.
     - Opens `Saved Views` dropdown on `/dashboard/contacts` Toolbar -> verifies no search/Saved Views overlap -> saves current filters (`search`, `searchBy`, `contact_source`) -> clears filters -> applies saved view and verifies filter state + filtered rows reload via `/api/v1/contacts` -> deletes saved view cleanly.
3. **Knowledge Graph**: Run `graphify update .` at workspace root.

---

## 3. Audit Review Log (2 Passes)

### Pass 1 — Schema Symmetry, Edit Mode & Import Compatibility Audit
1. **Verified Contact vs Lead Schema Parity:** Checked `atomicSchemas.ts` and `crmSchemas.ts` (`leadBase` vs `contactBase`). Using `requiredPersonNameSchema("First name")`, `requiredPersonNameSchema("Last name")`, `requiredCompanyNameSchema`, `requiredEmailSchema("Email")`, and `requiredPhoneSchema("Phone")` inside `contactBase` ensures identical validation rules and error messages as Leads, while leaving `Middle Name (Optional)` optional.
2. **Verified Contact Edit Flow & Programmatic API Safety:** Checked `AddContactModal.tsx:123-126` (`editContact.account?.account_name || editContact.company || ""`). Existing contacts linked to an Account auto-fill `company`. On backend `ContactCreate`, allowing non-empty `company` **or** `account_id` prevents breaking API/internal integrations that pass `account_id` directly, while UI & CSV bulk import require `Company Name *`.
3. **Found Zoho / Data Admin Import & Existing Test Gaps:** Inspected `record_import_service.py:78-81` and `test_data_admin_import_validation.py:92-109`. `_fill_contact_defaults` must backfill omitted `first_name`, `email`, `phone`, `company` ONLY when absent/empty so invalid email tests (`not-an-email`) still fail cleanly while Zoho/CSV rows with optional fields omitted still migrate without regression. Also inventoried all 5 existing backend test files omitting `phone`/`first_name`/`company` on `ContactCreate`.

### Pass 2 — Saved Views Filter Normalization, Dropdown Source List & Backend Query Audit
1. **Caught Stale Filter Leakage & Pagination Reset:** In `contacts/page.tsx`, passing `{ search, searchBy, contact_source }` (instead of dumping `page`/`pageSize`) into `SavedViewsDropdown.currentFilters` and explicitly normalizing missing keys to defaults (`search: ""`, `searchBy: "all"`, `contact_source: ""`, `page: 1`) on `onApplyView` prevents stale filter carryover or out-of-range page numbers when switching Saved Views.
2. **Caught Filter Dropdown Option Loss & `designation` Search Gap:** `ContactsFilterPanel.tsx` previously showed only page-derived `availableContactSources`; merging `CRM_CONTACT_SOURCES` + `availableContactSources` + active `localFilters.contact_source` ensures applied Saved View sources always render cleanly. Adding `normalized_search_by == "designation"` -> `Contact.title.ilike(...)` in `contacts_repository.py` ensures Saved Views using `Designation` return real matches.
3. **Verified Toolbar Layout Integrity:** `EntityActionBar.tsx` renders `savedViewsToggle` inside `@container/toolbar` with `shrink-0` and responsive width on `ModuleSearchInput`, avoiding search bar/Saved Views overlap on desktop widths.
