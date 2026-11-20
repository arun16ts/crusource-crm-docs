# Analytics Board UX, Unlimited Canvas & Zoho-Style Funnel Implementation Plan

**Date:** 19 November 2026  
**Product / Scope:** Crusource CRM (`crusource-crm-frontend` + `crusource-crm-backend`)  
**Status:** Draft — Pending Approval (no application source files modified)  
**Deployment Status:** Not deployed (design & implementation specification only)

---

## 1. Executive Summary & Problem Statement

A visual and architectural review of the CRM Analytics Board (`/dashboard/analytics`) against user testing screenshots and Power BI / Zoho CRM benchmarks identified five concrete usability, layout, and visualization gaps:

| # | Reported Issue / Feature Request | Observed Root Cause in Current Code | Target Outcome |
| --- | --- | --- | --- |
| **1** | **Floating 9-dots drag handle hides `"Pipeline"` label** on Sankey Flow and Cohort Heatmap widgets (`...ne [All pipelines v]`). | [Widget.tsx](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx#L451-L490) renders `.widget-drag-handle` with `position: absolute; top-2.5 left-2.5 z-30` directly on top of [WidgetPipelineSelector.tsx](../../../crusource-crm-frontend/src/components/analytics/WidgetPipelineSelector.tsx#L16), which itself sits outside the `h-full` widget body container and overflows downward. | Dedicated flex header strip for native analytics widgets with drag handle, title, pipeline selector, and action buttons in non-overlapping logical (`start`/`end`) flow. |
| **2** | **`AddWidgetModal` field order & separate search bar:** Ask Widget Name first (keeping smart default), and combine search into the Saved Report selector itself. | [AddWidgetModal.tsx](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx#L404-L716) places a standalone `Find a saved report` `<input>` above a native `<select>`, puts `Widget Display Title` at the bottom, and fails to update auto-title when switching reports once populated (`L570`). | Widget Name input first (auto-syncing default name until manually edited), followed by a single unified searchable `SavedReportCombobox` dropdown. |
| **3** | **`SankeyFlowWidget` cards overlap horizontally and waste surrounding canvas space.** | [SankeyFlowWidget.tsx](../../../crusource-crm-frontend/src/components/analytics/charts/SankeyFlowWidget.tsx) hardcodes `width = 860`, `height = 360`, `paddingX = 40`, `nodeWidth = 110`, yielding `availableWidth = 640`. Across 8 columns (`Lead -> Converted -> 5 Deal Stages -> Won/Lost`), column spacing is `640 / 7 = 91.4px < 110px`, causing `~18.6px` horizontal overlap, while `preserveAspectRatio="xMidYMid meet"` creates dead letterbox whitespace top/bottom. | Dynamic width/spacing calculation (`columnStep >= nodeWidth + minGap`), responsive fill when wide or horizontal smooth scroll when narrow, compact content-driven SVG height, and overflow containment. |
| **4** | **Analytics work area feels fixed/constrained** rather than an unlimited Power BI–style drafting canvas. | [AnalyticsBoard.tsx](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx) binds `ResponsiveGridLayout` strictly to viewport container width (`useContainerWidth()`), `12` columns, vertical compaction, and strict caps in [widgetLayoutConstraints.ts](../../../crusource-crm-frontend/src/components/analytics/widgetLayoutConstraints.ts) (`maxW <= 12`, `maxH <= 10`) + backend [widget_validator.py](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py#L182-L205) (`w <= 12`, `h <= 24`, `x + w <= 12`). | Power BI–style canvas controls: **Fit to Width / Wide Canvas (24-col horizontal scroll) / Fit to Page + Zoom (50%–150%)**, **Freeform vs Auto-Pack** placement, relaxed frontend/backend height & wide-grid caps, plus widget Focus Mode. |
| **5** | **Missing Zoho CRM–style Funnel View** showing stage drop-off, conversion rates, and deal/value progression. | Currently only `sankey_funnel` (raw state-transition ribbons) and `stage_zone` (current stage stuck-health bars in [StageZoneWidget.tsx](../../../crusource-crm-frontend/src/components/analytics/charts/StageZoneWidget.tsx)) exist. Neither backend nor frontend computes cumulative stage throughput, stage-to-stage conversion %, attrition/drop-off %, or dual Count + Amount funnel slices. | New `funnel` visualization (`FunnelWidget.tsx`) backed by a dedicated RBAC-scoped `GET /api/v1/stage-history/pipeline-funnel` endpoint (plus report-backed `funnel` compatibility for Deals stage / Leads status summary reports), offering Classic Tapered Funnel & Zoho Staircase/Stage Component views with drill-down. |

---

## 2. Architecture Verification & Dependency Map

### 2.1 Affected Frontend Files (`crusource-crm-frontend/`)

| File | Role & Planned Changes |
| --- | --- |
| [Widget.tsx](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx) | Refactor `isDashboardNative` shell (`L451–L490`) so analytics-native widgets (`sankey_funnel`, `cohort_heatmap`, `funnel`) render a dedicated flex header bar (`widget-drag-handle`, title, `WidgetPipelineSelector`, Focus/Fullscreen button, Remove button) above a `flex-1 min-h-0` body; add `funnel` case to `renderContent()` and drill-down support. |
| [WidgetPipelineSelector.tsx](../../../crusource-crm-frontend/src/components/analytics/WidgetPipelineSelector.tsx) | Compact pill styling inside card header (`py-1 px-2 text-xs`), accessible label, optional inline label hiding in tight widget headers while preserving `aria-label="Widget pipeline"`. |
| [AddWidgetModal.tsx](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx) | Reorder form fields: Source Tabs (now including **Funnel View**) → **Widget Name** (first input, auto-synced with `hasUserEditedTitle` flag) → **Unified Searchable Report Combobox** (`SavedReportCombobox`) → Visualization Type cards → Comparator / Target Value. |
| **NEW:** `src/components/analytics/SavedReportCombobox.tsx` | Accessible inline-searchable combobox (`role="combobox"`, `role="listbox"`, keyboard nav, RTL-safe Tailwind spacing, infinite `"Load more"` pagination, match highlighting, entity + report-type badges), following click-outside/keyboard conventions from [SearchableParentAccountCombobox.tsx](../../../crusource-crm-frontend/src/components/accounts/SearchableParentAccountCombobox.tsx). |
| [SankeyFlowWidget.tsx](../../../crusource-crm-frontend/src/components/analytics/charts/SankeyFlowWidget.tsx) | Replace fixed `860x360` canvas math with `ResizeObserver`-measured viewport + minimum column step (`nodeWidth + minGap`), dynamic height computed from max column row count, smooth `overflow-x-auto` fallback when narrow, and tight KPI ribbon spacing. |
| **NEW:** `src/components/analytics/charts/FunnelWidget.tsx` | Zoho CRM–inspired progressive funnel component supporting **Classic Tapered Funnel** and **Staircase / Drop-Off** layouts, **Cumulative Throughput** vs **Current Snapshot** toggle, **Count vs Monetary Amount** sizing, stage-to-stage conversion %, direct `Closed Won` / `Closed Lost` exit indicators, timeframe/pipeline filters, and record drill-down. |
| [AnalyticsBoard.tsx](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx) | Add Power BI–inspired Canvas Workspace toolbar (`Fit to Width`, `Wide Canvas`, `Fit to Page`, `Zoom %`, `Freeform` vs `Auto-Pack`), dynamic grid columns (`12` or `24`), zoom/pan viewport container with drafting-canvas grid background, smart 2D open-slot auto-placement on widget add, and Focus Mode modal overlay. |
| [widgetLayoutConstraints.ts](../../../crusource-crm-frontend/src/components/analytics/widgetLayoutConstraints.ts) | Raise vertical limits (`maxH` up to `40–60` for unrestricted downward expansion), widen `sankey_funnel` defaults (`defaultW: 8–12`, compact `defaultH: 4`), add `funnel` constraints (`minW: 4, minH: 4, maxW: 24, maxH: 40, defaultW: 6, defaultH: 6`), and parameterize `maxCols` cleanly (`12` or `24`). |
| [analyticsBoards.service.ts](../../../crusource-crm-frontend/src/services/analyticsBoards.service.ts) | Add `"funnel"` to `ChartType`; extend `WidgetSpec.config` cleanly (e.g., `funnel_mode`, `funnel_style`, `metric_by`, `date_range`) and optional board-level `canvas_settings` metadata (if persisted on board). |
| [stageHistory.service.ts](../../../crusource-crm-frontend/src/services/stageHistory.service.ts) | Add `PipelineFunnelResponse`, `FunnelStageMetrics`, and `StageHistoryService.getPipelineFunnel(params)`. |
| [widgetCompatibility.ts](../../../crusource-crm-frontend/src/lib/widgetCompatibility.ts) & [reportToChartData.ts](../../../crusource-crm-frontend/src/lib/reportToChartData.ts) | Add `"funnel"` to compatible chart types for Deals summary reports grouped by `stage` (and Leads grouped by `status`) with aggregates, plus `funnelData` transformer in `reportToChartData`. |
| Localization (`src/messages/{en,ar,nl}/analytics.json`) | Add translations for `addWidget.widgetName`, `addWidget.searchReportPlaceholder`, `addWidget.sources.funnel`, `chartTypes.funnel`, `board.canvas.*`, and `charts.funnel.*`. |

### 2.2 Affected Backend Files (`crusource-crm-backend/`)

| File | Role & Planned Changes |
| --- | --- |
| [analytics_boards_queries.py](../../../crusource-crm-backend/src/modules/analytics_boards/queries/analytics_boards_queries.py) | Add `"funnel"` to `ChartType` Literal; extend `NativeWidgetConfig` (formerly `NativePipelineConfig`) or `WidgetConfig` safely with validated optional funnel display fields (`pipeline_id`, `date_range`, `funnel_mode`, `funnel_style`, `metric_by`); review `WidgetLayout` bounds (`h: le=60`, `w: le=24` scoped to board canvas mode or `canvas_settings`). |
| [widget_validator.py](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py) | Allow `"funnel"` as both a native pipeline widget (validating `pipeline_id` via `validate_pipeline`) and optionally as a report-backed chart type when `spec.report_type == "summary"` + `stage`/`status` grouping; update `validate_widget_layouts` for board canvas column width (`12` vs `24`) and expanded vertical heights (`<= 60`). |
| [analytics_boards/repositories/models.py](../../../crusource-crm-backend/src/modules/analytics_boards/repositories/models.py) & handlers | *(Optional if persisting canvas zoom/width per board)* Add nullable JSONB column `canvas_settings` via Alembic migration, OR store board canvas preferences cleanly without breaking existing rows. Default must remain `12`-column compatible for existing boards and tests. |
| [stage_history_routes.py](../../../crusource-crm-backend/src/modules/stage_history/routes/stage_history_routes.py), [stage_history_handlers.py](../../../crusource-crm-backend/src/modules/stage_history/handlers/stage_history_handlers.py), **NEW** `services/funnel_analysis.py` | Implement `GET /api/v1/stage-history/pipeline-funnel` computing Zoho-style progressive funnel metrics from `Deal`, `PipelineStage`, and `StageHistory` strictly scoped via `apply_scope(query, Deal, scope)`. |

---

## 3. Detailed Phase-by-Phase Implementation Design

### Phase 1 — Fix Drag Handle Overlap & Native Widget Card Shell
**Goal:** Eliminate the `.widget-drag-handle` overlap over `Pipeline [All pipelines v]` and stop `WidgetPipelineSelector` from pushing widget bodies out of bounds (`...ne [All pipelines v]`).

1. **Separate Analytics-Native Headered Cards from Banner Cards in [Widget.tsx](../../../crusource-crm-frontend/src/components/analytics/Widget.tsx):**
   - Split native charts that carry interactive controls (`sankey_funnel`, `cohort_heatmap`, `funnel`) into an explicit card container matching report widgets (`bg-white border border-slate-200/90 rounded-xl shadow-2xs h-full flex flex-col overflow-hidden group`).
   - Build a unified `NativeAnalyticsCardHeader` (`shrink-0 px-3 py-2 border-b border-slate-200/80 bg-white flex flex-wrap items-center justify-between gap-2`):
     - **Start Group (`flex items-center gap-2 min-w-0 flex-1`):**
       - `.widget-drag-handle` in **normal flex flow** (`p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-md cursor-grab active:cursor-grabbing shrink-0`, hidden only when `!editable`), retaining `role="button"`, `tabIndex={0}`, `aria-label="Drag widget"`, and `title="Drag widget"`.
       - Widget title (`<h3 className="text-xs font-bold text-slate-900 truncate">` displaying `widgetTitle`).
     - **End Group (`flex items-center gap-1.5 shrink-0`):**
       - Inline [WidgetPipelineSelector.tsx](../../../crusource-crm-frontend/src/components/analytics/WidgetPipelineSelector.tsx) when `onPipelineChange` is provided for `["sankey_funnel", "cohort_heatmap", "funnel"]`.
       - Optional Focus/Expand toggle button (Phase 4).
       - Remove (`×`) button when `onRemove` is provided — placed inline instead of `absolute top-2.5 right-2.5` so it never collides with top-right toggles (like Cohort Heatmap's `Conversion Speed | Staleness` pills).
   - Wrap `{renderContent()}` inside `<div className="flex-1 min-h-0 w-full p-3 overflow-hidden">` so inner `h-full` layouts never overflow into adjacent grid rows.
   - For borderless full-bleed dashboard widgets (`welcome_banner`, `kpi_deck`, etc.), replace `left-2.5` / `right-2.5` with RTL-safe logical utilities (`start-2.5` / `end-2.5`) and give hover controls safe inset padding so nothing gets clipped.

2. **Tighten [WidgetPipelineSelector.tsx](../../../crusource-crm-frontend/src/components/analytics/WidgetPipelineSelector.tsx):**
   - Support a `compact?: boolean` prop (default `false` in modal, `true` inside `Widget` header).
   - In compact header mode, style as a crisp inline pill (`text-[11px] font-medium flex items-center gap-1.5 whitespace-nowrap`) with `<span className="text-slate-500 font-semibold">Pipeline</span>` cleanly to the right of the drag handle, zero padding bloat (`p-0` instead of `p-2`), and truncate long pipeline names gracefully (`max-w-[150px] truncate`).

---

### Phase 2 — Redesign `AddWidgetModal.tsx`: Widget Name First + Unified Searchable Report Combobox
**Goal:** Reorder modal controls so users name their widget first (with smart automatic defaults) and search/select their Saved Report from one unified searchable dropdown.

1. **Form Field Order Across All Source Tabs (`report`, `sankey`, `cohort`, `funnel`):**
   1. **Source Selector Tabs:** `Report Widget` | `Funnel View` | `Sankey Flow` | `Cohort Heatmap`.
   2. **Widget Name (First Form Field — Unified at Modal Body Top):**
      - Label: `Widget Name` (`addWidget.widgetName`) with live `0/80` character counter and inline invalid-character validation (`hasInvalidChars`).
      - **Auto-Default & Manual Override State Machine:**
        - Maintain `hasCustomTitleRef` / `isTitleManuallyEdited` boolean state (initially `false` on modal open).
        - Whenever `!isTitleManuallyEdited`:
          - On `report` tab: sync `customTitle` automatically to `selectedReport?.name ?? ""` whenever `selectedReport` loads or changes! (Fixes the current bug at [AddWidgetModal.tsx#L570](../../../crusource-crm-frontend/src/components/analytics/AddWidgetModal.tsx#L570) where switching from Report A to Report B left Report A's title stuck in the input.)
          - On `sankey` / `cohort` / `funnel` tabs: sync `customTitle` to the localized default title (`"Full Funnel Progression (Sankey Flow)"`, `"Cohort Aging Heatmap"`, `"Deal Stage Conversion Funnel"`).
        - Editing the text input sets `isTitleManuallyEdited = true` (if cleared back to `""`, reset `isTitleManuallyEdited = false` or fall back cleanly on submit).
        - Remove the duplicate display-title inputs currently duplicated inside the `sankey` and `cohort` cards (`AddWidgetModal.tsx` `L461–L548`).
   3. **Saved Report Combobox (for `report` tab — replaces separate Search Input + `<select>`):**
      - Create `SavedReportCombobox.tsx`:
        - Trigger looks like a clean form field displaying the currently selected report (`{name}` + entity/type badges, e.g. `CONTACTS • tabular`) and chevron, OR acts immediately as a type-to-filter input on focus/click.
        - Clicking opens a high-contrast popover menu (`z-50 max-h-64 overflow-y-auto`) containing an inline auto-focused search box (`placeholder="Search saved reports..."`, wired directly to `reportSearch` / `useDebouncedSearch`), live loading spinner when `isLoadingReports`, matching clickable report rows (`onClick` selects report ID, updates auto-title if unedited, closes menu), error/retry state, and `"Load more reports"` button if `hasNextPage` is true.
        - Full keyboard accessibility (`ArrowDown`, `ArrowUp`, `Enter` to select, `Escape` to close) and outside-click close (`mousedown` listener).
      - Reuse `SavedReportCombobox` for **Secondary Comparison Report** when `selectedChartType === "comparator"` as well.
   4. **Pipeline Selector (for native pipeline widgets: `funnel`, `sankey`, `cohort`):**
      - Shown cleanly right below Widget Name using `WidgetPipelineSelector`.
   5. **Widget Visualization Type & Conditional Goal Target (`target_meter`):**
      - Kept after Report selection since compatible chart types depend on the chosen report's `spec`.

---

### Phase 3 — Fix `SankeyFlowWidget.tsx` Card Collisions & Whitespace
**Goal:** Guarantee zero overlapping node cards regardless of pipeline stage count, eliminate top/bottom letterboxing, and remove excess horizontal margins.

1. **Dynamic Column Spacing & Non-Overlapping Card Width ([SankeyFlowWidget.tsx](../../../crusource-crm-frontend/src/components/analytics/charts/SankeyFlowWidget.tsx)):**
   - Replace hardcoded `const width = 860; const height = 360; const paddingX = 40; const nodeWidth = 110;` with measured geometry via `ResizeObserver` on the inner chart container (`viewportWidth`, `viewportHeight`).
   - Define strict geometry constants:
     - `NODE_WIDTH = 132` (wide enough that `"Needs Analysis"`, `"Value Proposition"`, `"Proposal/Price Quote"` rarely truncate cleanly at 1 line, or allow clean 2-line wrap with `line-clamp-2`).
     - `MIN_GAP_X = 48` -> minimum column pitch `MIN_STEP_X = NODE_WIDTH + MIN_GAP_X = 180`.
     - `PADDING_X = 20`.
   - Compute layout width dynamically:
     - Required width for `N = columns.length` columns: `minRequiredWidth = PADDING_X * 2 + (N - 1) * MIN_STEP_X + NODE_WIDTH`.
     - `svgWidth = Math.max(viewportWidth || minRequiredWidth, minRequiredWidth)`.
     - Column `x` position for column `c`: when `N > 1`, `colGap = (svgWidth - PADDING_X * 2 - NODE_WIDTH) / (N - 1)`, ensuring adjacent card edges always have `>= 48px` of clean Bézier ribbon visibility and **never collide**.
     - Wrap `<svg>` in `<div className="flex-1 min-h-0 w-full overflow-x-auto overflow-y-auto">` with `style={{ width: svgWidth, height: svgHeight }}`:
       - On wide dashboards (`viewportWidth >= minRequiredWidth`), the Sankey fills 100% of card width with no dead side gaps.
       - On narrower cards with 8+ stages, smooth horizontal scrolling keeps every stage readable without crushed text.

2. **Compact Content-Driven Vertical Height (Zero Dead Top/Bottom Space):**
   - Compute `requiredContentHeight` from the maximum stacked height among all columns:
     - `maxColHeight = Math.max(...columns.map(col => col.nodes.reduce((sum, n) => sum + n.height, 0) + (col.nodes.length - 1) * nodeGapY))`
     - `svgHeight = Math.max(maxColHeight + paddingY * 2, Math.min(viewportHeight || 240, maxColHeight + 48))` — instead of centering a tiny 2-row graph inside a rigid `360px` viewBox box with `preserveAspectRatio="xMidYMid meet"` margins!
   - Remove unnecessary outer blank padding (`p-4` / centered flex wrappers if redundant inside `Widget` card body) and keep the top KPI summary ribbon compact (`px-3 py-2 text-xs shrink-0`).
   - Adjust default widget layout constraints in [widgetLayoutConstraints.ts](../../../crusource-crm-frontend/src/components/analytics/widgetLayoutConstraints.ts#L35-L42):
     - Change `sankey_funnel` to `{ minW: 6, minH: 3, maxW: 24, maxH: 20, defaultW: 12, defaultH: 4 }` so new Sankey widgets immediately span full row width comfortably without vertical bloat.

---

### Phase 4 — Power BI–Style Expandable / "Unlimited" Analytics Board Canvas
**Goal:** Replace the rigid fixed-width 12-column page feel with a flexible, Power BI–inspired workspace supporting wide drafting canvases, zoom/fit scaling, freeform vs auto-packed positioning, unbounded downward scroll, and widget Focus Mode.

#### 4.1 Power BI Feature Parity Mapping for Crusource CRM

| Power BI Capability | Crusource Implementation Plan in [AnalyticsBoard.tsx](../../../crusource-crm-frontend/src/components/analytics/AnalyticsBoard.tsx) |
| --- | --- |
| **Page View: Fit to Width / Actual Size / Fit to Page** | Add a **Canvas View Selector** (`Fit Width`, `Wide Canvas (24-col)`, `Fit Page`) in the board toolbar. Default remains `Fit Width` (`12` responsive columns, zero horizontal scroll, infinite vertical growth). Switching to `Wide Canvas` expands logical grid columns from `12` to `24` inside a horizontally & vertically scrollable Power BI–style drafting mat (`min-w-[1680px]` or `2400px`) with subtle dot-grid background. |
| **Canvas Zoom Slider (`50%` – `150%` + Reset `Ctrl+0`)** | Apply clean CSS transform / zoomed container width + synchronized `transformScale={zoom}` prop passed to `react-grid-layout` (`ResponsiveGridLayout` / `GridLayout` supports `transformScale` natively!) so drag & resize math remains 1:1 under zoom without cursor drift! |
| **Freeform vs Auto-Pack Placement** | Add a **Layout Snap Mode** toggle when `editMode` is enabled: **Auto-Pack** (`compactType="vertical"`) vs **Freeform Canvas** (`compactType={null}`, `preventCollision={false}` or snap-to-grid with open whitespace preserved) so users can leave intentional spacing or build multi-zone sections just like Power BI. |
| **Unrestricted Vertical Workspace + Smart Add Placement** | Eliminate cramped `maxH: 8..10` caps in `WIDGET_CONSTRAINTS` (raise `maxH` to `40–60` depending on widget type). Replace the naive `y: maxY` placement in `AddWidgetModal.tsx` with a 2D first-fit placement helper (`findNextOpenSlot(existingWidgets, w, h, cols)`) that places widgets into open space horizontally before extending canvas rows downward. |
| **Focus Mode (Power BI Single-Visual Popout)** | Add an expand/focus icon (`Maximize2`) on every `Widget` header to inspect any dense Funnel, Sankey, Cohort, or Table in an instant full-viewport overlay (`Esc` to close) without altering its saved board layout. |

#### 4.2 Backend Contract & Persistence Alignment
Currently [analytics_boards_queries.py](../../../crusource-crm-backend/src/modules/analytics_boards/queries/analytics_boards_queries.py#L23-L28) and [widget_validator.py](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py#L182-L205) enforce hard limits (`1 <= w <= 12`, `1 <= h <= 24`, `x + w <= 12`), and [test_analytics_boards.py](../../../crusource-crm-backend/tests/test_analytics_boards.py#L297-L328) explicitly tests rejection of `w=13`, `h=25`, and `x+w > 12`.

To support wide/tall Power BI–style canvases **cleanly without silent clipping**:
1. **Board Canvas Metadata (`AnalyticsBoard` schema & optional DB column or user preference):**
   - **Recommended:** Add optional `canvas_config: Optional[BoardCanvasConfig]` (`cols: Literal[12, 24] = 12`, `view_mode: Literal["fit_width", "wide", "fit_page"] = "fit_width"`, `compact_mode: Literal["vertical", "free"] = "vertical"`, `zoom: int = 100`) on `AnalyticsBoard` (JSONB column `canvas_settings` via Alembic migration with `server_default='{}'`) + pass `board.canvas_settings.cols` into `validate_widget_layouts(widgets, max_cols=...)`.
   - **Bounds Upgrade:** Raise `WidgetLayout` Pydantic & validator upper limits to `w <= max_cols` (default `12`, up to `24` when board is in `24`-column Wide Canvas mode) and `h <= 60` (allowing tall multi-section tables, Sankeys, and Funnels while still rejecting abusive/corrupted payloads like `h=99999`).
   - **Viewport Zoom Persistence:** Persist user's per-board canvas view preference cleanly (`PATCH /analytics-boards/{id}` when saved in Edit mode, and local session fallback for quick view-only zooming).
   - **Test Coordination:** Update `test_analytics_boards.py::test_analytics_board_layout_validation` and `test_analytics_components.tsx` Test 8 assertions alongside the constraint bump (`h=61`, `w=13` on a `12`-col board vs valid `w=18` on a `24`-col board).

---

### Phase 5 — Zoho CRM–Style Funnel View (`FunnelWidget` + Backend Pipeline Funnel API)
**Goal:** Deliver a true executive **Stage Conversion & Drop-Off Funnel** inspired by Zoho CRM's Funnel & Stage Components and Zoho Analytics' Funnel Charts.

#### 5.1 Zoho CRM Funnel Capabilities & Metrics Breakdown

Based on Zoho CRM Dashboards (Funnel & Stage Component) and Zoho Analytics Funnel Charts:
1. **Cumulative Stage Throughput vs Current Stage Snapshot:**
   - **Cumulative Throughput (Default, Zoho Funnel standard):** A deal currently at `Proposal/Price Quote` is counted as having progressed through `Qualification` $\rightarrow$ `Needs Analysis` $\rightarrow$ `Value Proposition` $\rightarrow$ `Proposal/Price Quote` (reconstructed accurately from `StageHistory` transitions + current `Deal.stage_id`, tracking whether any stage was entered directly or skipped!).
   - **Snapshot Toggle:** Let users switch in-widget between **Cumulative Progression** (true historical funnel conversion) and **Current Pipeline Snapshot** (active open deals + Won/Lost at current stage).
2. **Core Zoho Funnel Metrics per Stage:**
   - **Stage Count (`count`)** and **Total Stage Value (`total_amount`, currency-normalized / org default currency via `OrgSettings`)**.
   - **Stage-to-Stage Conversion Rate (`step_conversion_pct`)**: Percentage advancing from Stage $i$ to Stage $i+1$ (`count[i+1] / count[i] * 100`).
   - **Drop-Off / Attrition (`dropoff_count`, `dropoff_pct`)** and **Direct Stage Exits (`won_from_stage_count`, `lost_from_stage_count`)**: Mirrors Zoho CRM's Stage Component by distinguishing *deals actively still in stage* vs *deals lost/abandoned directly out of stage $i$* vs *deals fast-tracked to Closed Won from stage $i$*.
   - **Overall Funnel Conversion Rate (`overall_conversion_pct`)**: `%` of top-of-funnel entered deals reaching `Closed Won`, plus **Average Days in Stage (`avg_duration_days`)**.
3. **Visual Presentations & Interactive Controls inside `FunnelWidget.tsx`:**
   - **Two Switchable Visual Styles:**
     - **Classic Tapered Funnel (Proportional Trapezoids):** Horizontally centered SVG/CSS funnel bands scaled smoothly by **Count** or **Amount** (with minimum readable band height & K/M/B compact currency formatting), stage labels on the left, conversion/drop-off connector chevrons (`↓ 64.2% conv • 35.8% drop`) on the right.
     - **Zoho Staircase / Stage Leakage View:** Step-down horizontal progress bars alongside explicit red *Lost at this stage* & emerald *Closed Won* exit badges for diagnosing exact bottlenecks (early vs mid vs late-funnel leakage).
   - **Header In-Widget Quick Controls:**
     - Timeframe pill (`All Time`, `30d`, `90d`, `YTD`)
     - Metric basis (`By Count` / `By Value $`)
     - Mode (`Cumulative` / `Snapshot`) + Style (`Funnel` / `Staircase`)
   - **Summary KPI Strip:** `Entered Deals`, `Closed Won (%)`, `Total Dropped / Lost`, `Won Revenue`, `Avg Cycle Days`.
   - **Click-to-Drill-Down:** Clicking any stage slice opens the underlying Deals breakdown (via `Widget.tsx` drill-down stack for report-backed funnels, or via deep-link / modal table query for native pipeline funnels using `pipeline_id` & `stage_id`).

#### 5.2 Backend Design: `GET /api/v1/stage-history/pipeline-funnel`
Add `crusource-crm-backend/src/modules/stage_history/services/funnel_analysis.py`, wire handler in `stage_history_handlers.py`, and expose endpoint in `stage_history_routes.py`:

- **Endpoint:** `GET /api/v1/stage-history/pipeline-funnel`
- **Query Params:**
  - `pipeline_id: Optional[str] = None` (defaults to org's default pipeline; `"all"` aggregates across pipelines by normalized `sort_order` / canonical stage type, or uses `default_pipeline` stages + summary buckets).
  - `mode: Literal["cumulative", "snapshot"] = "cumulative"`
  - `date_range: Literal["all", "30d", "90d", "180d", "ytd"] = "all"`
  - `entity_type: Literal["deal", "lead"] = "deal"` *(support Deals primary; optional Leads status funnel as clean secondary phase)*.
- **Strict Security & RBAC Rules:**
  - Query `Deal` via `apply_scope(query, Deal, scope)` so Rep/Manager/Admin tenant & hierarchy isolation matches `get_deal_stage_health` and `get_full_funnel_flow`.
  - Validate explicit `pipeline_id` UUID against `scope.org_id`.
- **Stage Reconstruction Logic (`cumulative` mode):**
  1. Fetch ordered `PipelineStage` rows (`sort_order ASC`) for the target pipeline. Separate open stages (`stage_type == "open"`), terminal `won` stage(s), and terminal `lost` stage(s).
  2. Query scoped `Deal` rows (respecting `date_range` on `Deal.created_at`) returning `(id, amount, currency, stage_id, created_at, closed_at)`.
  3. Query matching `StageHistory` entries (`entity_type="deal"`, `field_changed="stage"`, `entity_id.in_(deal_ids)`, ordered by `changed_at ASC`).
  4. For each deal:
     - Determine visited stages from `StageHistory` (`old_value`, `new_value`, `stage_id`) + current `Deal.stage_id`.
     - Identify highest open stage index reached (`max_open_idx`).
     - In **cumulative** mode: credit the deal's `1` count and `amount` to every sequential open stage `0..max_open_idx` (or explicitly mark visited vs inferred-through stages so `won` deals that closed early aren't misattributed silently; track `direct_won_from_stage[last_open_stage]` and `direct_lost_from_stage[last_open_stage]`).
     - Compute `step_conversion_pct`, `dropoff_count`, `dropoff_pct`, `avg_days_in_stage`, and `overall_conversion_pct`.
- **Response Schema (`PipelineFunnelResponse` in `stage_history_queries.py`):**
  ```json
  {
    "pipeline_id": "...",
    "pipeline_name": "Default Sales Pipeline",
    "entity_type": "deal",
    "mode": "cumulative",
    "date_range": "90d",
    "currency": "USD",
    "summary": {
      "total_entered_count": 120,
      "total_entered_amount": 840000.0,
      "won_count": 28,
      "won_amount": 245000.0,
      "lost_count": 46,
      "lost_amount": 290000.0,
      "open_count": 46,
      "overall_conversion_pct": 23.3,
      "avg_cycle_days": 18.4
    },
    "stages": [
      {
        "stage_id": "...",
        "name": "Qualification",
        "stage_type": "open",
        "sort_order": 1,
        "color": "#3B82F6",
        "count": 120,
        "amount": 840000.0,
        "pct_of_top": 100.0,
        "step_conversion_pct": 72.5,
        "dropoff_count": 33,
        "dropoff_pct": 27.5,
        "lost_here_count": 12,
        "won_here_count": 2,
        "stagnant_here_count": 19,
        "avg_days_in_stage": 4.2
      }
    ]
  }
  ```

#### 5.3 Supporting Report-Backed `"funnel"` Widgets Too
In addition to the zero-config native **Funnel View** tab in `AddWidgetModal`, register `"funnel"` as a compatible visualization in:
- Backend [widget_validator.py](../../../crusource-crm-backend/src/modules/analytics_boards/services/widget_validator.py) (`get_compatible_chart_types`): enabled for `summary` reports where `entity_type == "deals"` and `"stage" in spec.group_by` with aggregates (or `entity_type == "leads"` and `"status" in spec.group_by`).
- Frontend [widgetCompatibility.ts](../../../crusource-crm-frontend/src/lib/widgetCompatibility.ts) + [reportToChartData.ts](../../../crusource-crm-frontend/src/lib/reportToChartData.ts) (maps sorted stage/status rows into `FunnelWidget` props, preserving report filters, currency, and multi-level `Widget.tsx` drill-down!).
- Both paths reuse the same `FunnelWidget` presentation component cleanly.

---

## 4. Recommended Implementation Sequence & Dependency Order

1. **Step 1 — Backend Foundation (`crusource-crm-backend`):**
   - Update `analytics_boards_queries.py` & `widget_validator.py` (`"funnel"` `ChartType`, optional `canvas_settings` / relaxed `w`/`h` bounds, `funnel` compatibility rules).
   - Implement `funnel_analysis.py` + `GET /api/v1/stage-history/pipeline-funnel` route/handler + Alembic migration (only if persisting `canvas_settings` column on `analytics_boards`).
   - Add pytest coverage in `tests/test_analytics_boards.py` and stage-history funnel tests.
2. **Step 2 — Widget Chrome & Overlap Fix (`crusource-crm-frontend`):**
   - Refactor `Widget.tsx` native header bar & `WidgetPipelineSelector.tsx` compact header integration + RTL logical positioning.
   - Verify no visual overlap between `.widget-drag-handle`, `WidgetPipelineSelector`, and `onRemove`.
3. **Step 3 — `SankeyFlowWidget` & `AddWidgetModal` UX (`crusource-crm-frontend`):**
   - Fix `SankeyFlowWidget.tsx` dynamic column spacing (`>= nodeWidth + minGap`) and content-driven height + `widgetLayoutConstraints.ts` (`sankey_funnel` + `funnel` entries).
   - Build `SavedReportCombobox.tsx` and reorder `AddWidgetModal.tsx` (Widget Name first with `isTitleManuallyEdited` auto-sync, unified searchable Saved Report picker, **Funnel View** tab).
4. **Step 4 — `FunnelWidget.tsx` & Data Wiring (`crusource-crm-frontend`):**
   - Add `StageHistoryService.getPipelineFunnel`, `getCompatibleChartTypes` `"funnel"` rule, `reportToChartData` funnel mapper, and build `FunnelWidget.tsx` (Classic Funnel + Staircase views, tooltips, drill-down).
5. **Step 5 — Power BI Canvas Workspace (`AnalyticsBoard.tsx`):**
   - Implement Canvas View selector (`Fit Width`, `Wide Canvas 24-col`, `Fit Page`), Zoom slider (`50%–150%` with `transformScale`), Freeform vs Auto-Pack toggle, smart 2D open-slot add placement, and Focus Mode modal.
6. **Step 6 — i18n, Tests & Playwright Verification:**
   - Complete translations in `src/messages/{en,ar,nl}/analytics.json`.
   - Update/expand `tests/test_analytics_components.tsx`, `tests/e2e/test_analytics_interactive.ts`, and backend `pytest` suites; run live Playwright viewport checks (`1440px`, `1024px`, RTL `ar`, zoom & drag interactions) with screenshot inspection before completion.

---

## 5. Verification Plan (Checks Required After Implementation)

| Layer | Planned Check | Success Criteria |
| --- | --- | --- |
| **Backend Unit & API** | `pytest tests/test_analytics_boards.py tests/test_deals_phase5_analytics_e2e.py` (+ new `test_stage_history_funnel.py`) | `"funnel"` accepted for native & report-backed widgets; pipeline validation enforced; `pipeline-funnel` strictly RBAC-scoped (rep sees only visible deals; cross-org/unauthorized pipeline rejected); layout validation accepts `12`-col and `24`-col wide canvas boards cleanly. |
| **Frontend Component Tests** | `npx tsx tests/test_analytics_components.tsx` (plus updated assertions for `AddWidgetModal`, `Widget`, `SankeyFlowWidget`, `FunnelWidget`, `widgetLayoutConstraints`) | `Widget` drag handle renders inside header flex flow without overlapping `"Pipeline"`; `AddWidgetModal` renders Name field first and updates auto-title cleanly; `SankeyFlowWidget` column gaps `>= MIN_GAP_X`; `FunnelWidget` renders conversion % and drop-off counts. |
| **Typecheck & Lint** | `npm run typecheck` / `npm run lint` (`crusource-crm-frontend`) | Zero TypeScript errors across `en`/`ar`/`nl` types and `ChartType` switches. |
| **Browser Visual Verification** | Live Playwright desktop (`1440x900`) & tablet (`1024x768`) + RTL (`ar`) checks | 1. Native widget headers show clean `[::] Title ... [Pipeline v] [Expand] [×]` with zero overlap.<br>2. Sankey cards never overlap horizontally and fill card without dead vertical bands.<br>3. Add Widget modal shows `Widget Name` first + single searchable Saved Report combobox.<br>4. Switching canvas to Wide 24-col / Zoom 75% / Freeform drags smoothly.<br>5. Zoho Funnel View displays tapered conversion bars, step %, lost exits, and click drill-down. |
