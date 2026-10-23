# User Testing Issues — Implementation Plan

**Status:** Proposed; implementation has not started
**Scope:** The 15 issues reported during CRM user testing
**Owning applications:** `crusource-crm-frontend/` and `crusource-crm-backend/`
**Related design:** [Enterprise CRM Strategic Features Implementation Plan](ENTERPRISE_CRM_STRATEGIC_FEATURES_IMPLEMENTATION_PLAN.md)
**Verified against source:** 23 October 2026 — every baseline claim cross-checked with the live codebase

This plan translates the reported observations into an ordered, source-aware implementation sequence. It is not a claim that each behavior has been reproduced, that the reported cause is known, or that any fix has shipped. Reproduce each issue against the current branch and record its result before changing behavior. Keep the separate Crusource platform repositories out of scope.

## 1. Goals and working rules

- Fix user-visible defects while preserving existing tenant, permission, optimistic concurrency, import, and job-processing boundaries.
- Reuse the CRM's existing lead score jobs, shared table patterns, confirmation dialogs, API client, and TanStack Query cache instead of adding parallel systems.
- Establish evidence for ambiguous reports (especially 429 responses, the 41k-row CSV, and layout differences) before selecting a root-cause fix.
- Keep feature work and schema changes limited to what source inspection and reproduction show is necessary. No database migration is presumed by this plan.
- For each issue, capture browser steps, expected/actual behavior, request/response shape with secrets and personal data removed, and affected permissions/data state.

## 2. Source baseline and confidence

Initial inspection on 23 October 2026 found the following verified implementation points:

- **Lead scoring** is implemented as a separate AI priority score system in `src/modules/leads/services/lead_scoring_service.py` with single-lead (`POST /{lead_id}/score`), batch (`POST /score-batch`, capped at 50 leads), and job lifecycle routes (`GET /score-jobs/{job_id}`). Scores persist as `ai_priority_score`, `ai_priority_band`, `ai_priority_reasons`, `ai_priority_model`, `ai_priority_rubric_version`, `ai_priority_input_hash`, and `ai_priority_scored_at` columns directly on the `Lead` model. The `Lead` model uses `RecordContextMixin`, which declares `version_id_col = cls.version` — this means **every** `db.commit()` that touches a Lead row (including AI score persistence) increments the lead's `version` field. This is the confirmed root cause of the 409 stale-version conflict reported in Issue 2.
- **Lead sort** is supported server-side: `LEAD_SORTABLE_FIELDS` in `leads_repository.py` includes `ai_priority_score`, `ai_priority_band`, and `ai_priority_scored_at`. The backend `LeadFilterParams` accepts `sort` and direction. However, the **frontend `LeadsService.getAll`** passes `filters` through `buildQueryString` without a typed sort parameter, and `LeadList.tsx` has no interactive sort controls on column headers — sort-by-score must be wired end-to-end.
- **Lead stage writes** pass through `useUpdateLeadStage` in `src/hooks/mutations/useLeadMutations.ts`, which calls `expectedVersionFromCache()` to derive the lead's `expected_version`. After scoring, this cached version is stale because the score write incremented it on the backend without invalidating the frontend query cache for the individual lead.
- **Account hierarchy** has a backend service with tenant/team validation, cycle/depth protection, and rollup responses. The account editor, hierarchy view, and drawer already exist in `src/components/accounts/`. The parent account picker in `AddAccountModal.tsx` is currently a native `<select>` — not searchable, confirmed unusable at scale.
- **Deal team UI** exists in `src/components/deals/drawer/DealTeamTab.tsx`. Member removal (line 316) fires the mutation directly on icon click with **no confirmation dialog** — the `person_remove` icon is the only affordance, and clicking it immediately sends the DELETE request. The CRM has a shared `ConfirmModal` at `src/components/shared/ConfirmModal.tsx` that should be reused.
- **Pipeline DnD** error maps to `src/components/admin/pipeline/PipelineStagesList.tsx`, where line 205 reads `sensors={isStandard ? [] : sensors}`. This switches between an empty array literal and a `useSensors()` result, producing the React hook dependency-size warning as `DndContext` sees `[]` then `[PointerSensor, KeyboardSensor]`. DnD Kit version is `@dnd-kit/core` `^6.3.1`.
- **Calls 429 root cause (confirmed):** `GET /api/v1/calls/bulk-jobs` is classified by the admission system (`request_admission.py` line 124–126) as `expensive_minute` because the path segment `bulk-jobs` matches `part.startswith("bulk-")`. The `expensive_minute` budget is **5 requests per user per minute**. The frontend `useCallBulkJobs` hook polls at `refetchInterval: 2000` (every 2 seconds = 30 requests/minute) with `refetchIntervalInBackground: true`. This **guarantees** hitting the 5/min limit within 10 seconds of any active call job. The fix is two-part: (1) exempt the GET list/detail from the `expensive_minute` bucket (it is a cheap read, not a job start), and (2) add adaptive polling with backoff and page-visibility awareness to the frontend hook.
- **Search result highlighting** already has a reusable component: `src/components/search/HighlightMatch.tsx` (used by Reports in `ReportRow.tsx`). It safely escapes user input, supports multi-word splitting, and strips structured operators. This component should be adopted for Lead and Deal list search results.
- **Export downloads panel** is mounted inline below tables in: `CallsTable.tsx`, `MeetingsTable.tsx`, `TasksTable.tsx`, and `LeadBoard.tsx`. Shared component is `src/components/shared/ExportDownloadsPanel.tsx`.
- **Import parser** enforces a **100,000 row** limit in `SPREADSHEET_LIMITS` (`src/lib/parsers/boundedWorkbook.ts`). The 41k-row CSV failure at parse time suggests the problem is not a row cap, but likely file size, encoding, memory, or malformed content. The parser checks `SPREADSHEET_LIMITS.bytes`, column count, cell count, sheet count, and quoted-field integrity.
- **AI chat lead serializer** (`src/modules/ai_chat/services/record_serializers.py` line 32) references `getattr(lead, 'lead_score', 'N/A')` — this is the **old** field name and will always return `'N/A'` since the actual field is `ai_priority_score`. This must be corrected for Issue 8 (Loop AI answering "top leads and scores"). The AI chat service does **not** currently have a structured query tool for "top scored leads" — it relies on record serialization through the retrieval/context pipeline.
- **Filter options** in `src/components/leads/FilterPanel.tsx` use `renderCheckboxGroup` which renders all options statically without checking data availability. The AI Priority Band filter (line 209) renders `Hot`, `Warm`, `Cold` — these are valid enum values, not data-dependent, so the issue is likely about other filter groups with empty server-provided options.
- The CRM frontend CI uses **Node 20**, and the lockfile `package-lock.json` **is tracked in git** (`git ls-files package-lock.json` returns it). CI uses `npm ci` successfully. Next.js is `16.3.8`, React is `19.2.4`.

## 3. Priorities and sequencing

| Batch | Issues | Priority | Rationale |
|---|---:|---|---|
| A. Data integrity and blocked actions | 2, 12, 15 | P0 | A stale-write flow blocks stage changes; the confirmed 429 blocks call-job access; the React hook warning indicates unstable hook input and must be fixed safely. |
| B. Core usability and destructive actions | 3, 4, 7, 14 | P1 | Account selection/navigation and filter semantics impede everyday work; team removal needs explicit confirmation. |
| C. Lead workflow and search feedback | 1, 5, 6, 8 | P1 | Scoring is present but needs a usable batch/rank/explanation flow and consistent visual/search feedback. |
| D. Scale and page consistency | 9, 10, 11, 13 | P1/P2 | Large imports need a clear supported envelope; exports and inconsistent task/call layouts consume space or depart from established patterns. |

Recommended implementation order is A1 (issue 15), A2 (issue 2), A3 (issue 12), B, C, then D. Work may be split into reviewable pull requests by issue or tightly related component, but do not combine unrelated schema/API changes. Fix any shared foundation once and reuse it.

## 4. Issue-by-issue plan

### 4.1 Bulk lead scoring, rank, score explanation (Issue 1)

**Observed request:** Select multiple leads, score them, rank the list by score, replace the star-like score indicator with the Loop AI mark, and show a concise explanation on hover.

**Current baseline:** Backend batch score endpoint (`POST /leads/score-batch`) already exists with a 50-lead cap, idempotency key, and job lifecycle. Frontend `LeadsService.scoreBatch()` exists in `leads.service.ts` but **no bulk action button** is wired in `LeadList.tsx`. The existing AI priority score is distinct from user-maintained lead `rating`; preserve that distinction. Lead list column headers have no interactive sort controls.

**Plan:**

1. Add a "Score with AI" bulk action button to `LeadList.tsx` that appears when leads are selected. Wire it to `LeadsService.scoreBatch()` with the existing 50-lead cap. Show queued/running/completed/partial/failed states by polling `LeadsService.getScoreJobStatus()` at bounded intervals, and display the server's batch limit before submission.
2. Add score sort controls to lead list column headers. Wire `sort=ai_priority_score` and direction to `LeadsService.getAll` filters and persist in URL search params. Server-side sort is already supported via `LEAD_SORTABLE_FIELDS`. Define null-score ordering (backend currently defaults to `created_at desc`; add explicit `nulls_last` for score sort). Ensure sorting is fully server-side since pagination is server-side.
3. Replace the `auto_awesome` Material icon score badge with the Loop AI brand icon (reuse from `src/components/ai/LoopAIChatHeader.tsx`), retaining the numeric score and accessible text label.
4. Provide score rationale via a keyboard-accessible tooltip/popover on the score badge (in both list and card views). Include score, band, short reasons from `ai_priority_reasons`, rubric version, scored timestamp, and stale indicator. Bound displayed text and avoid presenting the assessment as a conversion probability.
5. Invalidate lead list/detail queries after batch job completion. Keep score-specific state in TanStack Query, not Redux.

**Acceptance:** Batch scoring is permission-checked and capped; jobs remain asynchronous; score sort works across pagination and can be restored from URL; null and stale scores are understandable; rationale is accessible and sourced from persisted score fields; ordinary lead rating behavior is unchanged.

### 4.2 Stale-version conflict when advancing a lead (Issue 2)

**Observed evidence:** Stage mutation returned HTTP 409 `conflict_stale_update` after scoring. The browser frame points to `useUpdateLeadStage` in `src/hooks/mutations/useLeadMutations.ts`.

**Confirmed root cause:** `Lead` inherits `RecordContextMixin` which declares `version_id_col = cls.version`. When `lead_scoring_service.py` writes `lead.ai_priority_score` (and related fields) and calls `db.commit()`, SQLAlchemy auto-increments the lead's `version`. The frontend's `LeadOverviewTab.tsx` invalidates `["leads"]` queries after scoring (line 152), but `expectedVersionFromCache()` in `useUpdateLeadStage` reads the cached version which may not yet reflect the invalidation/refetch — especially if the stage advance happens before the invalidated query resolves.

**Plan:**

1. **Primary fix:** After score completion in `LeadOverviewTab.tsx`, `await` the query invalidation and ensure the individual lead detail query is refetched and settled before re-enabling stage advance controls. This ensures `expectedVersionFromCache()` reads the updated version.
2. **Secondary safeguard:** In `useUpdateLeadStage` (and `useUpdateLead`), handle 409 `conflict_stale_update` gracefully: refetch the lead, compare the server's current state with the user's intended change, and if the only difference is AI score fields (no conflicting user edits), auto-retry with the fresh version. If there are conflicting field changes, show a conflict dialog with refreshed server values and require user review.
3. Do not auto-retry a stale stage transition against a new version without revalidating that the stage transition is still allowed. Do not remove backend version checks.
4. Add regression tests for: score-then-stage flow, concurrent user edit during scoring, rejected stale update with real conflict, and list/detail cache coherence after scoring.

**Acceptance:** The score-then-stage workflow succeeds when the stage change is valid; true concurrent edits still produce a recoverable conflict; no stale update overwrites another actor's change.

### 4.3 Searchable parent account picker (Issue 3)

**Current baseline:** Account create/edit supports `parent_account_id`. `AddAccountModal.tsx` uses a native `<select>` element. A reusable searchable combobox exists at `src/components/ui/Combobox.tsx` (used by `EntitySearchCombobox`, `CallEntityPickers`, `MeetingAttendeePicker`, etc.).

**Plan:** Replace the native `<select>` with `Combobox.tsx` or the `EntitySearchCombobox` pattern. Search only accounts the current user is allowed to see, debounce remote queries, show loading/empty/error states, selected parent and clear action, and exclude the account being edited plus its descendants from eligible choices. Keep submitted IDs and backend validation authoritative.

**Acceptance:** Users can find a parent by name among large account sets; keyboard selection and clear work; unauthorized, inactive, self, descendant, and cross-team parents cannot be selected or accepted by API.

### 4.4 Open a child account from hierarchy view (Issue 4)

**Current baseline:** `AccountHierarchyTab.tsx` renders hierarchy nodes (parent, current, subsidiaries) as styled cards. `AccountDetailDrawer.tsx` is the standard detail surface opened by selecting an account row.

**Plan:** Make ancestor/subsidiary account cards in `AccountHierarchyTab.tsx` clickable. Clicking a node should update the URL query parameter `?id=<account_id>`, which the accounts page already uses to open `AccountDetailDrawer.tsx` for that account. Support keyboard focus/activation (`role="button"`, `tabIndex`, Enter/Space). Do not make restricted placeholder nodes navigable.

**Acceptance:** Clicking or keyboard-activating an authorized child/parent opens its standard drawer; restricted/placeholder nodes remain non-actionable; hierarchy totals/selection context update correctly after navigation.

### 4.5 Search result highlighting in Leads and Deals (Issue 5)

**Current baseline:** `HighlightMatch` component already exists at `src/components/search/HighlightMatch.tsx` and is actively used in Reports (`ReportRow.tsx` line 78). It safely escapes search text, splits multi-word queries, strips structured operators, and renders `<mark>` tags.

**Plan:** Import `HighlightMatch` into `LeadList.tsx`/`LeadCard.tsx` and the corresponding Deal list components. Wrap the name/company/email cells with `<HighlightMatch text={cellValue} highlight={searchTerm} />`. Pass only the user's current search query; do not apply highlighting to fields that are not part of the search. Preserve diacritics/case behavior as established in Reports.

**Acceptance:** Lead and deal search matches are visibly highlighted without changing result membership; search remains debounced/URL-restorable; keyboard/screen-reader output remains coherent; adversarial search text is rendered as text.

### 4.6 Lead AI score column alignment (Issue 6)

**Current baseline:** `LeadList.tsx` renders the AI score badge inline within each row using `inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[10px]`. Column headers use `px-3 py-1.5 text-xs font-bold` with no dedicated AI score column header — the badge is appended after the lead name cell. There is a dedicated `#` index column, checkbox column, and sticky actions column.

**Plan:** Reproduce at supported viewport widths. If the score badge causes name column width variance, consider: (a) giving the AI score its own thin column with a dedicated header, or (b) fixing the name column's `min-width`/`max-width` so the badge does not shift alignment. Check horizontal scroll, column visibility toggles (if any), and responsive hiding. Correct the single source of column sizing rather than compensating with per-header offsets.

**Acceptance:** Every visible header aligns with its cells at supported widths, with and without scored leads in view.

### 4.7 Deal team member removal confirmation (Issue 7)

**Current baseline:** `DealTeamTab.tsx` line 316 fires `removeMemberMutation.mutate(member.id)` immediately on clicking the `person_remove` icon button. No confirmation dialog is shown. The CRM's standard destructive confirmation dialog is `src/components/shared/ConfirmModal.tsx`.

**Plan:**

1. Add a `showRemoveConfirm` state to `DealTeamTab.tsx` tracking the member ID pending removal.
2. Clicking the remove icon sets this state instead of mutating immediately.
3. Render `ConfirmModal` with the member name, deal name, destructive styling (red confirm button), and a clear explanation of what removal means (access revocation, split removal if applicable).
4. Confirm submits the existing `removeMemberMutation`; cancel clears the state. Prevent duplicate submits by disabling the confirm button while the mutation is pending.
5. Preserve current permission enforcement, audit behavior, and cache invalidation.

**Acceptance:** No removal occurs before explicit confirmation; keyboard and focus behavior matches other destructive dialogs; unauthorized users cannot invoke the action; success and failure states are visible.

### 4.8 Loop AI answers "top leads and scores" (Issue 8)

**Current baseline:** CRM Loop AI UI is under `src/components/ai/`; backend chat behavior uses retrieval (`context_builder.py`, `lexical_retriever.py`, `vector_retriever.py`), analytics (`crm_analytics_service.py`, `metric_calculator.py`), and Gemini provider. The record serializer (`record_serializers.py` line 32) references `getattr(lead, 'lead_score', 'N/A')` — this is the **wrong field name**. The actual field is `ai_priority_score`. The AI chat system does not currently have a structured "top scored leads" query tool.

**Plan:**

1. **Fix the serializer immediately:** Change `record_serializers.py` line 32 from `lead_score` to `ai_priority_score`. Also include `ai_priority_band`, `ai_priority_scored_at`, and `ai_priority_is_stale` in the lead serialization so the model has accurate score context.
2. Add a bounded, read-only "top leads by AI priority score" retrieval path in the context builder or analytics service. Query leads ordered by `ai_priority_score DESC NULLS LAST`, scoped by org/team/record visibility, capped at 10–20 results, excluding unscored leads. Return only permitted lead fields plus score/band/reason summary/timestamp.
3. Ensure the model's system prompt or function descriptions make this query path discoverable for "top leads", "highest scored", "best leads" intents.
4. Respect current permission/feature switches. Never send unbounded lead data or PII to the model.

**Acceptance:** Asking for top leads returns the highest visible scored leads with accurate stored scores and links/identifiers; different users receive only records they may view; empty/scored-out states and unsupported requests are handled honestly; no PII or unbounded lead list is sent to the model unnecessarily.

### 4.9 CSV import failure at 41,000 rows (Issue 9)

**Observed symptom:** CSV is reported as "Failed to parse file. Please verify it is a valid spreadsheet." The exact file size, delimiter, encoding, header shape, columns, line endings, and memory/network failure point are unknown.

**Current baseline:** `SPREADSHEET_LIMITS` in `boundedWorkbook.ts` allows up to **100,000 rows**, 256 columns, **25 MiB**, and 1,000,000 cells. The reported 41k rows are below the row cap, but the byte or total-cell cap could still be exceeded. `importFileParser.ts` parses CSV in the browser with Papa Parse after reading the entire file as text, accumulates all rows in memory, and rejects quote/field-mismatch errors. The reported generic toast does not identify which constraint or parser error occurred; trace the actual import entry point and error mapping during reproduction.

**Plan:**

1. Reproduce using a synthetic CSV with 41,000 representative rows and no real customer data. Record bytes, columns, encoding/BOM, delimiter, quoted multiline fields, maximum field length, browser memory, parse duration, request body size, and backend response.
2. Trace the affected import entry point → `parseImportFiles` → PapaParse/SheetJS → validation. Determine whether failure occurs in browser memory (large array allocation), parse timeout, byte size or total-cell limit, malformed content, request body size, or backend rejection.
3. Improve error diagnostics: distinguish malformed-file errors (with row/column locations) from size/encoding/memory errors. Surface the specific `SPREADSHEET_LIMITS` constraint that was exceeded. Preserve actionable remediation without dumping imported contents into logs.
4. If 41k exceeds safe interactive browser parsing limits (memory/time), implement bounded chunk upload with job progress, or clearly enforce a documented maximum with preflight size/row estimate and a supported split path. Use existing import/job patterns; do not create one unbounded transaction or let retries duplicate rows.
5. Ensure preview and row-level error state stay bounded (virtualized/paginated preview), and cancellation/partial failures have an explicit recovery contract.

**Acceptance:** A documented, measured maximum or supported 41k-row path exists; bad CSV is distinguished from oversized CSV; retries/cancellation cannot silently duplicate records; tenant permissions, validation, and import auditing remain enforced.

### 4.10 Remove "Recent exports" panels below tables (Issue 10)

**Current baseline:** `ExportDownloadsPanel.tsx` is mounted inline below tables in:
- `src/components/dashboard/calls/CallsTable.tsx`
- `src/components/dashboard/meetings/MeetingsTable.tsx`
- `src/components/dashboard/tasks/TasksTable.tsx`
- `src/components/leads/LeadBoard.tsx`

**Plan:** Remove the inline panel from all four mounting points. Preserve access to active/completed export downloads through the existing export control button's dropdown or a compact, explicitly opened location (e.g., a popover or modal triggered from the export button). Do not delete export job data or break download links. Check role/tenant filtering and mobile layouts. Verify `ExportDownloadsPanel` itself is not deleted if other surfaces reference it.

**Acceptance:** No inline Recent exports block occupies table height on the affected pages; users can still find/download authorized export jobs through the chosen existing entry point; exports themselves still work.

### 4.11 Tasks view appears zoomed out (Issue 11)

**Current baseline:** Tasks table rows use `text-sm` for most content (e.g., `TasksTable.tsx` line 526: `text-sm font-semibold`, line 570: `text-sm`). Meetings table uses different container styling (`rounded-xl` vs `rounded-lg`, different padding patterns). Both use Tailwind tokens, but they were developed independently with slightly different spacing and sizing choices.

**Plan:** Compare Tasks at the same browser zoom, viewport, font settings, and density as Meetings and another reference list (e.g., Leads). Inspect actual CSS tokens: typography scale, table row height (`py-*`), control sizing (`w-4 h-4` checkboxes), container max width, and page scaling/transforms. Identify the concrete mismatch before changing styles. Normalize Tasks to established CRM tokens without making Meetings larger or overriding browser zoom/accessibility font scaling.

**Acceptance:** At equal browser conditions, Tasks control/text density matches the chosen CRM reference within documented design tokens; responsive and browser zoom behavior remains usable; no clipping or horizontal overflow is introduced.

### 4.12 Calls page visual refactor (Issue 13)

**Current baseline:** Calls has 26 dedicated components under `src/components/dashboard/calls/` including: `CallsTable.tsx`, `CallsTableView.tsx`, `CallsKanban.tsx`, `CallCard.tsx`, `CallColumn.tsx`, `CallFilterPanel.tsx`, `CallFilterChips.tsx`, `CallsHeader.tsx`, `CallsKpiCards.tsx`, `CallBulkJobsPanel.tsx`, `CallBulkImportModal.tsx`, `CallDetailDrawer.tsx`, `CallLogModal.tsx`, `CallModal.tsx`, and modal form subcomponents. The Calls page is one of the most component-rich sections.

**Plan:** Inventory Calls list, board, filters, empty/loading/error states, toolbar, bulk jobs, and detail drawer. Compare against shared CRM page/table primitives and the agreed Leads/Deals/Meetings design tokens. Refactor incrementally to shared table/header/filter/dialog patterns where contracts match; preserve call-specific fields, lifecycle actions, permissions, pagination, bulk job status/retry, and accessibility. Avoid a visual rewrite of data operations.

**Acceptance:** Calls uses consistent typography, spacing, colors, table headers/rows, toolbar, and states; all call operations and bulk job lifecycle still work; responsive and keyboard behavior is at least as complete as before.

### 4.13 Filter options with no values look selectable (Issue 14)

**Current baseline:** `FilterPanel.tsx` uses `renderCheckboxGroup` (line 118) which renders all provided `options` as checkboxes unconditionally. Static enums like `STATUS_OPTIONS` and `AI_PRIORITY_BANDS` always have values. The issue likely applies to filter groups whose options come from server data (e.g., lead sources, industries, pipelines) — when the server returns no values, the empty group header still renders with an empty list, or a stale option appears selectable.

**Plan:** Trace the lead filter option source for each group. For server-provided option groups, hide the group entirely or show a disabled "No options available" message when the options array is empty. For static enums, ensure each value maps to a valid API filter. When the server has no choices, do not render a checkbox that appears active. Keep explicit "is empty" semantics as a separate filter operator only if supported by the API. Ensure selected filters can be cleared and translated labels remain correct.

**Acceptance:** An unavailable/empty option cannot be checked as if it filters records; supported filters remain explicit and send the correct API value; URL state and reset behavior remain coherent.

### 4.14 Pipeline DnD `useEffect` dependency-size warning (Issue 15)

**Observed evidence:** React reports the `DndContext` hook argument changed from `[]` to `[PointerSensor, KeyboardSensor]`. `PipelineStagesList.tsx` line 205 passes `sensors={isStandard ? [] : sensors}` and conditionally disables drag handlers. Sensors are created via `useSensors(useSensor(PointerSensor, ...), useSensor(KeyboardSensor, ...))` at lines 77–84.

**Confirmed root cause:** The empty array `[]` and the `sensors` array are different JavaScript references with different lengths. When `isStandard` toggles, `DndContext` receives a new sensors array with different length, triggering React's hook dependency check.

**Plan:** Always pass the fixed `sensors` array to `DndContext`. Disable sorting at the item level with `useSortable({ id, disabled: isStandard })`, and retain a defensive no-op in the drag handler for standard pipelines. The current `SortableStageItem` already receives `isStandard`, so this can be done without introducing a second context or conditionally shaped sensor array. Do not rely on a `disabled` prop on `DndContext`; keep the installed DnD Kit API contract authoritative.

**Acceptance:** Switching modes never produces dependency-size/order warnings; standard stages cannot be reordered; custom stages remain draggable by pointer and keyboard; no conditional hook calls are introduced.

### 4.15 Call bulk-jobs endpoint returns HTTP 429 (Issue 12)

**Observed evidence:** A request to `GET /api/v1/calls/bulk-jobs` receives 429 `"Too many requests. Please wait before trying again."` with a `Retry-After` header.

**Confirmed root cause (two-part):**

1. **Backend admission misclassification:** `request_admission.py` line 124–126 classifies any path containing a segment starting with `bulk-` as `expensive_minute`. The `expensive_minute` budget is **5 requests per user per 60 seconds** (line 38). A `GET /api/v1/calls/bulk-jobs` (a cheap status-list read) shares this budget with actual expensive operations like `POST /calls/bulk-jobs/import` and `POST /calls/bulk-jobs/delete`.
2. **Frontend over-polling:** `useCallBulkJobs.ts` polls at `refetchInterval: 2000` (every 2 seconds) with `refetchIntervalInBackground: true`. This means 30 requests per minute — 6× the per-user budget. The hook will hit 429 within 10 seconds of any active call job.

**Plan:**

1. **Backend:** Exempt `GET` requests to `bulk-jobs` (and `bulk-jobs/{job_id}`) from the `expensive_minute` policy. The admission system already distinguishes methods (line 104: `method not in ("GET", "HEAD", "OPTIONS")`), but the `expensive_operation` check (line 120–131) does not exclude GETs for `bulk-*` paths. Add an explicit method check: only classify `bulk-*` as `expensive_minute` for non-GET methods. The baseline `baseline_burst` (120/10s) and `baseline_minute` (600/60s) budgets already protect GET endpoints.
2. **Frontend:** Replace the fixed 2-second polling with adaptive polling: start at 2s, increase to 5s after 30 seconds, 10s after 2 minutes, and stop when all jobs are terminal. Pause polling when the page is hidden (`document.hidden`). Respect `Retry-After` header from 429 responses. Remove `refetchIntervalInBackground: true`.
3. Show a recoverable "temporarily limited" state and next retry time rather than treating the job list as a failed operation. Ensure retries do not resubmit bulk mutations.
4. Add API tests for legitimate GET reads at polling cadence, configured limits, retry headers, and mutation admission; add a browser regression for one active job polling lifecycle.

**Acceptance:** Normal use of the calls page does not exhaust admission through status polling; abusive/excess mutation traffic remains bounded; client honors retry guidance; job mutations remain idempotent and are never silently repeated.

## 5. Cross-cutting implementation requirements

### Frontend

- Read `crusource-crm-frontend/AGENTS.md`, package manifest, and current CI workflow before edits. Installed versions: Next.js `16.3.8`, React `19.2.4`, `@dnd-kit/core` `^6.3.1`, Node `20` (CI).
- Keep page routes thin; API calls in existing service modules; server data in TanStack Query; shareable sort/search/filter state in URL where established.
- Follow established CRM dialogs (`ConfirmModal.tsx`), comboboxes (`Combobox.tsx`), icon assets (Loop AI brand from `LoopAIChatHeader.tsx`), translations (all 3 locales: `en`, `ar`, `nl`), table primitives (`HighlightMatch.tsx`), and accessibility patterns. Keep visual changes scoped to CRM frontend.
- Handle API errors by status and safe code. Do not suppress 409/429 globally or log sensitive record data.

### Backend

- Read current backend workflow and module route/service/repository conventions. Preserve tenant scoping, permissions, soft-delete rules, audit, resource admission, idempotency, and optimistic concurrency (`RecordContextMixin.version` / `version_id_col`).
- Do not add migrations unless the confirmed design needs persisted schema changes. If required, preserve a single intended Alembic head and test against disposable PostgreSQL.
- Never send unbounded lead data or PII to Loop AI; use scoped structured query results, limits, and existing AI/data-governance controls. Fix the stale `lead_score` reference in `record_serializers.py` regardless of other changes.

### Test and verification plan

Add regression coverage for each meaningful fix in the repository's current runners. At minimum:

- **Frontend focused coverage:** score selection/status/sort/tooltip; 409 conflict handling and auto-retry logic; searchable account combobox and hierarchy navigation; safe highlight rendering via `HighlightMatch`; `ConfirmModal` confirmation dialog; import preflight/error cases with synthetic 41k CSV; export panel removal from all 4 mount points; layout consistency (Tasks vs Meetings); filter empty-state for server-provided option groups; stable DnD sensors across pipeline mode switch; calls polling backoff and 429 recovery with `Retry-After`.
- **Backend focused coverage:** scoring route/job and tenant permission behavior; score-write/version-increment interaction; account parent scope and cycle prevention; AI chat lead serializer field name fix; Loop AI top-leads bounded scoped query; CSV limits/chunk/idempotency where introduced; calls admission policy: GET bulk-jobs excluded from `expensive_minute`, POST bulk-jobs included; `Retry-After` header behavior.
- **Browser flows:** lead score batch through completion then stage advance without 409; parent search combobox and child drawer click-through; confirmed deal-team removal via `ConfirmModal`; Loop AI "top leads" query with accurate scores; large CSV import path; Calls active-job polling across retry without 429; pipeline standard/custom mode switch and reorder; no inline exports panel below tables.
- **Full required checks:** Follow the then-current frontend and backend CI workflows in their respective repositories. The frontend lockfile (`package-lock.json`) is tracked; use `npm ci` for reproducible installs. Use disposable PostgreSQL/service instances for backend CI parity and do not use stage/production data.
- Do not report a check as passing unless it was freshly run and its full result inspected. Distinguish local checks from remote CI and stage behavior.

## 6. Rollout and completion gates

1. Create a reproduction record for all 15 issues. Mark each as reproduced, not reproduced, environment-specific, or needs more data; preserve the reporter's original evidence.
2. Confirm source contracts and select the smallest safe implementation for each reproduced issue. Record any product decision needed (e.g. import supported maximum, score sort scope, export entry point) before coding that dependent behavior.
3. Implement in the batches above with reviewable changes, focused regression coverage, and current full CI for every affected repository.
4. For backend schema changes, rehearse clean upgrade and supported upgrade paths on disposable PostgreSQL, check drift and one intended head, and document rollback limits.
5. Verify local behavior with isolated fixtures. If stage verification is later requested, follow the full CRM deployment audit; a local pass or healthy endpoint is not stage evidence.
6. Close an issue only when its acceptance criteria, regression evidence, and any unresolved limitation are recorded.

## 7. Open decisions and unknowns

- ~~The maximum accepted lead-import rows/bytes and whether chunked import is required: measure first, then set and document a supported service envelope.~~ **Resolved:** Frontend allows 100k rows; the 41k failure is likely parse-time memory/encoding, not a row cap. Reproduce with synthetic data to confirm.
- Whether score sorting should cover all filtered leads or only a page: **Resolved:** backend sort is server-side across all filtered results (pagination is server-side). Frontend must wire the `sort` query parameter.
- Where export history should remain accessible after removing inline panels: preserve the existing authorized download path via the export button and verify discoverability.
- ~~The cause and rate policy behind the reported Calls 429: inspect request cadence and server admission before changing limits.~~ **Resolved:** GET `bulk-jobs` shares `expensive_minute` (5/min) with POST mutations; frontend polls at 30 req/min. Two-part fix specified in 4.15.
- The source of Tasks density mismatch: compare computed styles and shared design tokens before adjusting.
- ~~Whether score persistence advances the same version field as lead edits: inspect the write transaction and concurrency contract before choosing the issue 2 fix.~~ **Resolved:** Yes — `RecordContextMixin.version` is the `version_id_col`, and any `db.commit()` touching a Lead (including AI score writes) increments it. Fix specified in 4.2.

## 8. Explicit non-goals

- Rebuild AI scoring, account hierarchy, or call bulk jobs from scratch; these systems already have substantial backend foundations.
- Remove backend concurrency checks or broadly relax rate limits to hide symptoms.
- Change unrelated platform repositories, deployment workflows, pricing, CRM security policy, or production data.
- Claim external AI accuracy, support for arbitrary CSV sizes, CI success, or deployment readiness from this plan alone.
