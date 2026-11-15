# Accounts Mandatory Fields, Deals Summary & Click-Through, and Timeline Sync Plan

> **Owner repositories:** `crusource-crm-frontend/`, `crusource-crm-backend/`, `crusource-crm-docs/`
> **Scope guard:** Mandatory **Industry** and **Billing Address** apply **only to Accounts** (`AccountCreate` / `AddAccountModal` / `ACCOUNT_IMPORT_FIELDS`). Leads, Contacts, Lead Conversion (`AccountResolver`), and Deal Import stub-account creation (`ImportDealsService`) remain untouched and non-blocking.

---

## 1. Verified Problems & Root Causes

| # | Requirement / Gap | Verified Root Cause in Codebase |
|---|---|---|
| 1 | **Make Address & Industry mandatory for Accounts alone** | `accountCreateSchema` (`crusource-crm-frontend/src/lib/validations/crmSchemas.ts:122-136`) marks `industry: cleanString(100).optional()` and reuses optional `addressStreetSchema`, `addressCitySchema`, `addressStateSchema`, `addressZipSchema`, `addressCountrySchema` from `atomicSchemas.ts`. `AddAccountModal.tsx` does not pass `required` to Industry `SmartSelect` or `AddressLookupSection`. Backend `AccountCreate` (`crusource-crm-backend/src/modules/accounts/commands/account_commands.py:18-33`) leaves `industry` and all `billing_*` fields `Optional[str] = None`. Additionally, `ACCOUNT_IMPORT_FIELDS` (`bulkImportFields.constants.ts:32`) misnames `billing_zip_code` as `billing_postal_code` and omits `required: true` for `industry` and billing address fields. |
| 2 | **Show company Deals + current status + stats in Account drawer** | `AccountDetailDrawer.tsx` only has `overview \| hierarchy \| timeline \| contacts \| notes \| documents` tabs. There is no `Deals` tab, no `useAccountDealPages` hook, and no Account-scoped Deal stats panel. Meanwhile, on the backend, `DealFilterParams` (`deal_queries.py:111`) declares `account_id: Optional[UUID] = None`, **but `apply_deal_filters` (`deals_repository.py:43-81`) omits `if filters.account_id: query = query.filter(Deal.account_id == filters.account_id)`**, causing `GET /api/v1/deals?account_id=...` and `GET /api/v1/deals/aggregates?account_id=...` to ignore `account_id`! |
| 3 | **Clicking a Deal in Account drawer opens its Detail Drawer in Deals section** | `/dashboard/deals` (`crusource-crm-frontend/src/app/dashboard/deals/page.tsx:303-309,729-740`) already supports deep-linking via `?id=<deal.id>` and fetches standalone via `useDeal(dealId)`, just like `/dashboard/contacts?id=<contact.id>` used by `AccountContactsTab.tsx:51-54`. Account drawer simply needs a clickable Deals list calling `onClose()` and `router.push(\`/dashboard/deals?id=\${deal.id}\`)`. |
| 4 | **Update Account Timeline on Deal events** | Backend `CreateDealCommandHandler`, `UpdateDealCommandHandler`, `DeleteDealCommandHandler`, `BulkDeleteDealsCommandHandler`, and `DealCreator` (Lead Conversion) never emit `System:` timeline notes onto `parent_type="Account"`, whereas `UpdateAccountCommandHandler` and Lead/Contact/Deal drawers rely on `timeline_note_logger.py` + `useEntityNotes`. Frontend `AccountDetailDrawer.tsx` also does not pass `deals` into `generateTimeline(...)`, and `timelineUtils.ts:168` gates deal creation events behind `entityType === "Contact"`. |

---

## 2. Phase-Wise Implementation Plan

### Phase 1 — Mandatory Industry & Billing Address for Accounts Only

#### 1.1 Frontend Validation & Form UI (`crusource-crm-frontend`)
1. **`src/lib/validations/atomicSchemas.ts`**:
   - **Preserve** existing optional `addressStreetSchema`, `addressCitySchema`, `addressStateSchema`, `addressZipSchema`, `addressCountrySchema` so `leadBase` (`leads`) and `contactBase` (`contacts`) behavior never changes.
   - Add reusable required variants specifically for required-address entities (`requiredIndustrySchema`, `requiredAddressStreetSchema`, `requiredAddressCitySchema`, `requiredAddressStateSchema`, `requiredAddressZipSchema`, `requiredAddressCountrySchema`), ensuring trimmed non-empty strings + keeping the existing character/format constraints (max lengths & regexes).
2. **`src/lib/validations/crmSchemas.ts`**:
   - Update `accountCreateSchema` to use the new required schemas for `industry`, `billing_street`, `billing_city`, `billing_state`, `billing_zip_code`, `billing_country`.
   - Keep `parent_account_id`, `no_of_employees`, `annual_revenue`, `website`, `description`, `is_active` optional.
3. **`src/components/shared/AddressLookupSection.tsx`**:
   - Add optional prop `required?: boolean` (default `false`).
   - When `required === true`, render `<span className="text-red-500 ml-0.5">*</span>` next to Street, Zip/Pincode, City, State, and Country labels. Leads (`AddLeadModal.tsx`) and Contacts (`AddContactModal.tsx`) omit `required`, so their labels stay unchanged.
4. **`src/components/accounts/AddAccountModal.tsx`**:
   - Pass `required` to Industry `<SmartSelect required ... />` and `<AddressLookupSection required ... />`.
   - Ensure validation errors under the Billing Address section and Industry field surface clearly inside the modal form (displaying `errors.billing_street`, `errors.billing_zip_code`, `errors.billing_city`, `errors.billing_state`, `errors.billing_country`, `errors.industry` via `AddressLookupSection` / `FormFieldError`). Verify `AddressLookupSection` renders field-level errors cleanly! *(Check in Audit Pass 1.)*
5. **`src/constants/bulkImportFields.constants.ts`**:
   - Fix `billing_postal_code` -> `billing_zip_code` in `ACCOUNT_IMPORT_FIELDS`.
   - Mark `industry`, `billing_street`, `billing_city`, `billing_state`, `billing_country`, `billing_zip_code` with `required: true` and `*` labels.
   - Update `ACCOUNT_SAMPLE_CSV` to include `Billing Street` and `Billing Postal / ZIP Code` columns with complete sample values.
6. **Translations (`src/messages/{en,nl,ar}/accounts.json`)**:
   - Add any new validation or section keys needed in `en`, `nl`, `ar` identically.

#### 1.2 Backend Account Validation (`crusource-crm-backend`)
1. **`src/modules/accounts/commands/account_commands.py`**:
   - In `AccountCreate`, enforce mandatory non-empty values for `industry`, `billing_street`, `billing_city`, `billing_state`, `billing_zip_code`, and `billing_country` using Pydantic validation (`str` without `None` default, cleaned & rejected with clear message if blank/whitespace).
   - Keep database columns in `src/modules/accounts/repositories/models.py` (`Account`) `nullable=True` so:
     - `AccountResolver.resolve_or_create_account` (Lead Conversion when a Lead lacks address/industry) continues creating or linking accounts seamlessly.
     - `ImportDealsService` (Deal CSV import auto-creating stub accounts by company name) continues working seamlessly.
     - Legacy accounts with empty address/industry remain readable.
   - In `AccountUpdate` (`PATCH /api/v1/accounts/{account_id}`), keep fields `Optional[str] = None` so unrelated partial updates (e.g., changing `is_active` or `parent_account_id`) on legacy records continue succeeding, **while** rejecting explicit blank/empty clears if `"industry"` or `"billing_*"` is explicitly passed in `model_fields_set` as `""` / `None`.
2. **Existing Backend & Frontend Test Fixtures**:
   - Update existing test payloads creating Accounts via `AccountCreate` or `POST /api/v1/accounts` / `/bulk-import` (`tests/test_enterprise_crm_features.py`, `tests/test_sales_production_hardening.py`, `tests/test_crm_api_endpoints.py`, `tests/test_audit_logs.py`, `tests/test_create_submission_postgres.py`, `tests/test_bulk_import_all_modules.py`, and frontend `tests/test_enterprise_crm_features.tsx`) to supply valid `industry` + `billing_*` fields, plus add dedicated negative tests confirming Leads & Contacts do NOT require address/industry while Accounts do.

---

### Phase 2 — Backend `account_id` Deal Filtering & Account Timeline Sync

#### 2.1 Fix `account_id` Filter on Deals & Aggregates (`crusource-crm-backend`)
1. **`src/modules/deals/queries/deal_queries.py`**:
   - Add `account_id: Optional[UUID] = Query(None)` to `DealFilterParams.__init__` and assign `self.account_id`.
2. **`src/modules/deals/repositories/deals_repository.py`**:
   - In `apply_deal_filters(query, filters, joined_stage=False)`, add:
     ```python
     if filters.account_id:
         query = query.filter(Deal.account_id == filters.account_id)
     ```
   - Verify both `get_deals_for_scope` (`GET /api/v1/deals`) and `get_deals_aggregates_for_scope` (`GET /api/v1/deals/aggregates`) invoke `apply_deal_filters` so both lists and stats reflect strictly the requested `account_id` within RBAC scope.

#### 2.2 Account Timeline Sync for Deal Events (`crusource-crm-backend`)
1. **`src/shared/audit/timeline_note_logger.py`** *(or dedicated helper called by Deal handlers)*:
   - Add small shared helpers (preserving existing `Note` `System:` format parsed by `timelineUtils.ts`):
     - `record_account_deal_timeline_note(db, scope, account_id, message)` (guards `account_id is not None`, verifies `Account` exists in `scope.org_id`, persists `Note(parent_type="Account", parent_id=account_id, content=f"System: {message}", ...)` without breaking if account was deleted).
   - Emit concise `System:` timeline notes onto `parent_type="Account"` when:
     - **Deal Created** (`CreateDealCommandHandler` when `new_deal.account_id`):
       `System: Deal created — "{deal_name}" ({stage_name}, {amount_display})` *(clean readable message)*.
     - **Deal Created from Lead Conversion** (`DealCreator.create_deal_from_lead` when `account_id` is set):
       `System: Deal created from lead conversion — "{deal_name}" ({stage_name}, {amount_display})`.
     - **Deal Updated / Stage Changed / Won / Lost / Account Linked or Unlinked** (`UpdateDealCommandHandler`):
       - If `account_id` changed from `old_account_id` to `new_account_id`:
         - On `old_account_id`: `System: Deal unlinked — "{deal_name}"`
         - On `new_account_id`: `System: Deal linked — "{deal_name}" ({stage_name})`
       - Otherwise if `deal.account_id` is present:
         - If `stage_changed`: `System: Deal "{deal_name}" stage changed from {old_stage_name} to {new_stage_name}` (with Won/Lost outcome highlighted when `active_stage.stage_type` is `won`/`lost`).
         - If meaningful fields (`amount`, `closing_date`, `deal_name`, `deal_owner_id`, `contact_id`) changed: summarize the updated fields onto `Account` timeline (e.g., `System: Deal "{deal_name}" updated: amount, closing date`).
     - **Deal Deleted / Bulk Deleted** (`DeleteDealCommandHandler`, `BulkDeleteDealsCommandHandler`):
       - On `deal.account_id` (before delete flush/commit): `System: Deal deleted — "{deal_name}"`.
   - Note: `get_unified_entity_timeline(..., entity_type="account")` (`activity_timeline_service.py:208-213`) queries `Note` where `parent_id == entity_id` and `parent_type in ["account", "Account"]`, so emitting `parent_type="Account"` `System:` notes updates **both** the drawer Notes-derived Timeline and the backend `/timeline` endpoint automatically!

---

### Phase 3 — Frontend Account Deals Tab, Stats, Click-Through & Timeline UI

#### 3.1 Account Deals Data Hooks & Cache Invalidation (`crusource-crm-frontend`)
1. **`src/hooks/useAccountDealPages.ts`** *(new hook mirroring `useAccountContactPages.ts` / `useContactDealPages.ts`)*:
   - Uses `useInfiniteQuery` against `DealsService.getAll({ account_id: accountId, limit: 50, skip: pageParam })`.
   - Enabled only when `enabled && Boolean(accountId) && canView && permissions?.fields?.deals?.account_id !== "hidden"`.
   - Returns `{ ...query, items, total }`.
2. **`src/hooks/useAccountDealStats.ts`** *(or inside `useAccountDealPages` / `AccountDealsTab`)*:
   - Fetches `DealsService.getAggregates({ account_id: accountId })` via `useQuery` (`queryKey: [...queryKeys.deals.aggregates(), "account", accountId]`, `enabled: enabled && Boolean(accountId) && canView`).
   - Derives accurate Account-level stats across ALL pages + currencies:
     - **Total Deals** (`sum(count)`)
     - **Open Pipeline** (`sum(amount)` for `stage_type === "open"`, broken down cleanly per currency when multiple currencies exist, plus open count)
     - **Closed Won** (`sum(amount)` for `stage_type === "won"`, plus won count)
     - **Win Rate** (`wonCount / (wonCount + lostCount) * 100`, or `—` if no closed deals yet) & **Closed Lost** count.
3. **`src/lib/cacheInvalidation.ts` & `src/hooks/useParentNotesPage.ts`**:
   - Ensure `invalidateDeals` (`cacheInvalidation.ts:114-135`) already invalidates `queryKeys.deals.all()` (covers `["deals", ...]` including `useAccountDealPages` and `["deals", "aggregates", ...]`), `queryKeys.notes.all()`, and `queryKeys.timeline.all()`; also add `queryClient.invalidateQueries({ queryKey: queryKeys.accounts.all() })` (or hierarchy query key) when deals change so Account hierarchy rollup stats stay fresh too!

#### 3.2 `AccountDealsTab` & `AccountDetailDrawer` (`crusource-crm-frontend`)
1. **`src/components/accounts/drawer/AccountDealsTab.tsx`** *(new component matching `AccountContactsTab.tsx` styling)*:
   - **Stats Summary Strip** (`grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4`):
     - Total Deals (count)
     - Open Pipeline (formatted currency total / multi-currency badges + open deal count)
     - Closed Won (formatted currency total + won count)
     - Win Rate (`%` of closed deals won + lost count subtitle)
   - **Deals List**:
     - Shows each Deal row as an interactive accessible card (`role="button"`, `tabIndex={0}`, `Enter`/`Space` + click):
       - Deal Name (`font-bold text-sm text-slate-800 group-hover:text-primary`) + external affordance (`open_in_new` / chevron)
       - Current Stage / Status Pill (`stage_name || stage || "Open"`), colored by `stage_type` (`won` -> emerald, `lost` -> rose, `open` -> sky/amber/indigo)
       - Formatted Deal Value (`formatCurrency(deal.amount, deal.currency)`) + Closing Date (`formatDate(deal.closing_date)`) + Owner (`deal.deal_owner_name`)
     - On click: `onOpenDeal(deal)` -> closes the Account drawer (`onClose()`) and calls `router.push(\`/dashboard/deals?id=\${deal.id}\`)` so the Deals page opens that Deal's Detail Drawer immediately (whether on page 1 or any page).
   - **Pagination & Error States**: Reuses the exact `Next Page` / `Retry` / loading / empty state UX from `AccountContactsTab.tsx`.
   - **Overview/Lazy Fetch Integrity**: Keeping `useAccountDealPages` and `useAccountDealStats` gated on `isOpen && (activeTab === "deals" || activeTab === "timeline")` ensures opening `AccountDetailDrawer` on `overview` triggers zero premature API calls (preserving `test_account_contacts_loading_browser.mjs`).
2. **`src/components/accounts/AccountDetailDrawer.tsx`**:
   - Extend `Tab` union to include `"deals"`: `"overview" | "hierarchy" | "deals" | "contacts" | "timeline" | "notes" | "documents"`.
   - Add `{ id: "deals", label: t("drawer.tabs.deals"), badge: dealsPages.total > 0 ? dealsPages.total : undefined }` tab when user has `deals:view` permission (or show empty/restricted nicely — wait: let's check if `AccountContactsTab` hides tab or renders; in `AccountDetailDrawer.tsx`, tabs are static and permission checks happen in `useAccountContactPages`; gating `useAccountDealPages` with `canView` matches `useAccountContactPages` cleanly!).
   - Pass `deals: accountDeals` into `generateTimeline({ entity: account, entityType: "Account", notes, deals: accountDeals, tasks, calls, meetings, documents }, formatDate)` so existing/legacy deals without `System:` notes also surface accurately.
3. **`src/lib/timelineUtils.ts`**:
   - Allow `entityType === "Account"` (not just `"Contact"`) to format Deal timeline creation entries when a deal has no matching `"Deal created"` `System:` note, **deduplicating** if a matching `"System: Deal created"` note already exists so no duplicate creation cards ever appear!
4. **Translations (`src/messages/{en,nl,ar}/accounts.json`)**:
   - Add `drawer.tabs.deals` and `dealsTab.*` keys (`title`, `empty`, `stats.*`, `openDeal`, `stageFallback`, etc.) across all 3 locales cleanly.

---

### Phase 4 — Verification Plan
1. **Backend (`crusource-crm-backend/.venv/Scripts/python.exe -m pytest`)**:
   - Accounts, Deals, Timeline, Lead Conversion, Bulk Import, Audit Logs, Sales Production Hardening tests.
   - New targeted tests covering:
     - `AccountCreate` rejects missing `industry` and missing `billing_*` (422) while Leads (`POST /api/v1/leads`) & Contacts (`POST /api/v1/contacts`) and Lead Conversion without address/industry still succeed.
     - `GET /api/v1/deals?account_id=...` and `GET /api/v1/deals/aggregates?account_id=...` filter strictly by `account_id`.
     - Deal create / stage change / won / update / unlink-relink / delete emit `System:` timeline notes onto the Account timeline.
2. **Frontend (`crusource-crm-frontend`)**:
   - `npx.cmd tsc --noEmit`
   - `npx.cmd tsx tests/test_translation_contracts.ts`
   - `npx.cmd tsx tests/test_enterprise_crm_features.tsx`
   - `node tests/test_account_contacts_loading_browser.mjs`
   - New Playwright browser test `tests/test_account_enhancement_browser.mjs`: verifies `AddAccountModal` requires Industry + all Billing Address fields (while Lead/Contact modals remain unaffected), verifies `AccountDetailDrawer` Deals tab shows stats + status badges + navigates to `/dashboard/deals?id=<deal_id>`, and verifies Account Timeline renders Deal events cleanly.
3. **Knowledge Graph**: Run `graphify update .` after all edits.

---

## 3. Audit Review Log (2 Passes)

### Pass 1 — Boundary, Schema & Import Alignment Audit
1. **Verified Lead / Contact isolation:** Checked `atomicSchemas.ts` vs `crmSchemas.ts` (`leadBase`, `contactBase`). Keeping existing `address*Schema` optional and adding separate `required*Schema` exports strictly for `accountCreateSchema` guarantees Leads and Contacts are unaffected. Adding optional `required?: boolean` (`false` default) to `AddressLookupSection.tsx` preserves `*`-free labels in `AddLeadModal.tsx` and `AddContactModal.tsx`.
2. **Found Bulk Import field mismatch & Admin parity:** Verified `crusource-crm-backend/src/modules/data_admin/services/record_import_service.py:148-149` validates Data Admin Account imports through `BulkAccountImportRequest` -> `list[AccountCreate]`, matching `Accounts` page bulk import (`ACCOUNT_IMPORT_FIELDS`). Discovered `bulkImportFields.constants.ts:32` used `billing_postal_code` instead of `billing_zip_code`; fixing this key + marking `industry` and all 5 `billing_*` fields `required: true` keeps both import wizards consistent with `AccountCreate`.
3. **Verified Lead Conversion & Deal Import safety:** Checked all direct `Account(...)` instantiation sites (`lead_conversion/account_resolver.py`, `deals/services/import_deals_service.py`, `contacts/handlers/*`). Because `Account` ORM columns remain `nullable=True`, those internal flows stay unblocked when a Lead or Deal CSV lacks address/industry.

### Pass 2 — Aggregates Deduplication, Lazy Fetching & Timeline Deduplication Audit
1. **Found `/deals/aggregates` 3x key aliasing trap:** `get_deals_aggregates_for_scope` (`deals_repository.py:178-180`) writes every stage under `str(stage_id)`, `stage_name`, and `normalized_stage_name`. Summing `Object.values(aggregates)` directly would triple-count totals. `AccountDealsTab` (or a small helper) MUST filter to canonical stage UUID keys (with safe fallback if tests supply non-UUID keys) before computing Total Deals, Open Pipeline, Closed Won, Lost, and Win Rate across `by_currency`.
2. **Verified lazy tab fetch preserves `test_account_contacts_loading_browser.mjs`:** That test asserts zero non-permission requests when `AccountDetailDrawer` opens on `overview`. Gating `useAccountDealPages` and `useDealsAggregates` on `isOpen && (activeTab === "deals" || activeTab === "timeline")` guarantees zero premature fetches on drawer open while loading deals lazily when viewing Deals or Timeline.
3. **Verified no duplicate Timeline creation cards:** `DealCreator` and `CreateDealCommandHandler` will emit `System: Deal created...` notes onto `parent_type="Account"`. In `timelineUtils.ts`, fallback Deal creation cards for `entityType === "Account"` must skip any deal that already has a matching `"Deal created"` `System:` note on the Account timeline.
4. **Verified cache invalidation:** Updating `invalidateDeals` (`cacheInvalidation.ts`) to also invalidate `["accounts", "hierarchy"]` keeps both the Account `Deals` tab, `Timeline`, and `Hierarchy` rollup synchronized after any Deal mutation.
