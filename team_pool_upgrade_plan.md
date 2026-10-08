# Team Pool Upgrade Implementation Plan

This document outlines the phase-wise implementation plan for upgrading the Team Pool section. The upgrade involves transitioning to high-performance pagination, adding delete/bulk-delete capabilities, introducing targeted imports, enabling advanced filters, and adding "Assigned To" / "Owner" columns.

## Phase 1: Backend Infrastructure (Pagination, Filters, & Endpoints)

**1. Pagination & Filtering Logic**

- **Target Routes:** Update `src/modules/teamspace/routes/teamspace_pool_routes.py` (`/leads`, `/deals`, `/tasks`, `/meetings`, `/calls`).
- **Implementation:** Transition from returning standard lists (`List[LeadResponse]`) to a paginated wrapper (`PaginatedResponse`).
- **Query Params:** Introduce `skip` (or `page`), `limit`, and dynamic filter parameters (e.g., `status`, `owner_id`, `created_after`).
- **Handlers:** Update `list_teamspace_records_handler.py` to accept these parameters, applying SQLAlchemy `.filter()`, `.limit()`, and `.offset()` queries for efficient database execution.

**2. Delete & Bulk Delete Capabilities**

- **Target Routes:** DO NOT create new delete endpoints in `teamspace_pool_routes.py`. Instead, reuse the existing core endpoints (e.g., `DELETE /api/v1/leads/{id}`, `POST /api/v1/deals/bulk-delete`).
- **Permission Checks:** The existing backend route guards (e.g., `require_permission("leads", "delete")`) and scope resolution already handle team-based access securely. No backend changes are required here; the frontend simply needs to wire these up in the Team Pool context.

**3. Response Models (Columns)**

- **Data Models:** Ensure `owner_id` and an `assigned_to` field (or their relationship names like `owner_name`) are exposed in the serialization schemas for all Team Pool queries. Ensure the backend properly resolves user names for these fields if not already doing so.

---

## Phase 2: Frontend State Management & API Hooks

**1. TanStack Query Pagination**

- **File:** `src/hooks/queries/teamspace/useTeamPoolQueries.ts`
- **Implementation:** Refactor the existing hooks (e.g., `useTeamspaceLeads`, `useTeamspaceDeals`) to accept `page`, `limit`, and `filters` arguments.
- **Optimization:** Use `placeholderData: keepPreviousData` to ensure a smooth, flicker-free UX when transitioning between pages.

**2. State Management for Filters & Pagination**

- **Implementation:** Implement URL-based state management (using `useSearchParams`, `useRouter`, `usePathname`) for pagination and filters. This ensures deep-linking works and state is preserved on page refresh, adhering to the application's URL state conventions.

**3. Mutations Hook**

- **Implementation:** Do not create duplicate mutations. Reuse existing hooks from `src/hooks/mutations/` (e.g., `useLeadMutations`, `useDealMutations`) which provide the delete and bulk-delete functions.
- **Cache Invalidation:** Ensure that these existing mutations are configured to call `queryClient.invalidateQueries` for the relevant `TEAMSPACE_QUERY_KEYS` when triggered from within the Team Pool views.

---

## Phase 3: Frontend UI Components (Table, Columns, Filters)

**1. High-Performance Paginated Tables**

- **Target Files:** `PoolLeadsTab.tsx`, `PoolDealsTab.tsx`, `PoolActivitiesTab.tsx`, etc.
- **Implementation:** Strip out infinite-scroll wrappers. Introduce a standard pagination footer component (Page 1 of X, Next/Prev buttons, Rows per page selector).
- **New Columns:** Add `<th className="px-4 py-3">Owner</th>` and `<th className="px-4 py-3">Assigned To</th>` to the table headers, and populate the corresponding `<td>` elements in the row mapping.

**2. Filter & Action Bar (`PoolTabBar.tsx` & `PoolSearchBar.tsx`)**

- **Filters:** Add filter dropdowns (Status, Owner, Date Range) next to the search bar.
- **Bulk Actions:** When rows are selected (`selectedIds.length > 0`), display a "Bulk Delete" button alongside the existing actions. Ensure a confirmation modal is triggered before execution.
- **Single Delete:** Add a "Delete" option to the individual row action menus (e.g., three-dot menu).

---

## Phase 4: Import Capability Integration

**1. Targeted Import Actions**

- **Target File:** `PoolTabBar.tsx`
- **Implementation:** Add dynamic conditional rendering for the "Import" button. It should only render when the active tab is **Deals, Tasks, Meetings, or Calls**. It must **not** render for Notes or Reports.
- **Integration:** Wire the Import button to the existing bulk import modals/wizards (e.g., CSV upload workflows). Ensure the imported data automatically assigns the current `teamId` so it correctly appears in the Team Pool.

---

## Phase 5: QA, Performance Tuning & Final Polish

**1. Data Load Testing (15k+ Records)**

- Ensure the database indexes are hit correctly when using `limit` and `offset`.
- Validate that frontend rendering time is fast (pagination limits DOM nodes, preventing the lag caused by massive infinite scroll lists).

**2. Functional Integrity Verification**

- **Assignments:** Test assigning records to ensure "Owner" and "Assigned To" columns update dynamically.
- **Visibility:** Confirm that permissions (View, Edit, Delete) are strictly enforced in the new paginated lists.
- **Exports:** Ensure the export functionality respects the newly applied filters and pagination (or prompts for "Export All" vs "Export Current Page").
