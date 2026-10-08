# Entity activity loading audit — 2026-10-08

## Confirmed issue and scope

Authenticated inspection of localhost:3000 against the restarted localhost:8000 API reproduced broad activity downloads when opening a Lead **Overview**. The shared `useEntityActivities` hook downloaded all scoped Tasks and up to 100,000 Meetings, then filtered by the selected record in JavaScript. Related Calls were already server filtered, but the hook automatically continued every 500-record page.

The same hook is wired into Lead, Deal, Contact and Account drawers. This audit changes those consumers. It does not claim that every application view or active activity-modal timeline is optimized.

| Same selected Lead | Before | After |
| --- | --- | --- |
| Overview Task/Meeting entity downloads | 100,510,214 transferred bytes | None |
| Overview activity information | Full collections, filtered locally | Two related count/latest-date summaries, 950 transferred bytes combined |
| Activities | Collections already loaded by Overview | Related Task/Meeting pages and Calls list, each limited to 50 |
| Activities → Timeline | Used global collections | Reuses the related-page cache; zero additional activity GETs observed |

Chrome completed-transfer measurements include response headers and describe the local development run. Before, Task and Meeting requests completed in approximately 15.4 and 17.8 seconds respectively. After, the empty related Task/Meeting pages transferred 470 bytes each, and the empty Calls response 449 bytes. Real selected records had no related activity rows; this live check cannot demonstrate continuation beyond 50. A browser fixture with 65 records per activity kind exercises that separately.

The captures distinguish GETs from CORS OPTIONS. React Strict Mode canceled probe requests before successful replacements. OPTIONS and canceled probes are not represented as duplicate completed entity responses.

## Implementation

- Related Tasks and Meetings use the existing server page contracts and scoped repository filters. Direct parent links, linked Contact links, contact-name fallback and normalized attendee-email matching remain available. Calls use the existing server relation filters with stable 50-record offset pages and explicit continuation rather than automatically reading all pages.
- Lead and Deal activity reads are enabled only on Activities/Timeline; Contact and Account reads only on Timeline. Disabled or closed consumers do not refetch these pages on mutation invalidation. Keys include response-affecting parent/filter parameters, use one-minute freshness and keep the existing module-root invalidation behavior. Network cancellation signals are preserved.
- Activities continuation advances the selected kind; All advances only kinds with more rows. Lead/Deal Timeline filters similarly advance the selected activity kind. Contact/Account timelines expose combined continuation. No fixed total cap silently truncates related activities. An exact multiple of 50 Calls can require one final empty request because the legacy Calls list has no total-count envelope.
- Loading and query failures have visible states and retry controls. Previously loaded rows can remain visible when a later page fails.
- When a security profile hides a date field, the hook uses the endpoint's existing permitted default ordering rather than requesting an unavailable explicit date sort. The browser regression covers this fallback without changing backend field ceilings.
- Lead Overview still displays the full Calls Made count and latest contact date. New permission-guarded Calls/Meetings related summaries compute count and maximum activity timestamp in SQL without hydrating entity relationships. They reuse existing relation filters and role scope. Hidden relationship filters are rejected; a derived timestamp is withheld when a source date is hidden. Lead timestamps and email history still contribute to Last Contacted.
- Task, Meeting and Call modals and Call detail drawers now enable the existing global timeline only when open on Timeline. This prevents inactive timeline effects from downloading unrelated collections. The active global timeline's collection/deal-note loading is deliberately left for the next contract-focused batch.

Source evidence: [entity pages](../../crusource-crm-frontend/src/hooks/useEntityActivities.ts), [Lead summaries](../../crusource-crm-frontend/src/hooks/useEntityActivityOverview.ts), [Activities continuation](../../crusource-crm-frontend/src/components/shared/ActivitiesTab.tsx), [Calls aggregate/filter reuse](../../crusource-crm-backend/src/modules/calls/repositories/calls_repository.py), [Meeting aggregate/filter reuse](../../crusource-crm-backend/src/modules/meetings/repositories/meeting_page_repository.py), and [existing global timeline](../../crusource-crm-frontend/src/hooks/useGlobalTimeline.ts).

## Backend work avoided

The drawers no longer serialize/hydrate 41,401 Tasks and 35,445 Meetings merely to find activities for a single record. Summary endpoints return scalar projections; activity pages hydrate only returned rows and necessary relationships. Scoped counts and related-record filters still incur SQL work. This batch adds no index or migration and makes no concurrency/production benchmark claim. Existing Admin, Sales Manager and Sales Rep data rules remain enforced by the backend.

## Verification

- Live Lead Overview/Activities/Timeline comparison above; no legacy global Task/Meeting endpoints after the change.
- Live Deal, Contact and Account Overview: no Task/Meeting/Call collection GETs. Timeline: only parent-filtered pages with limit 50. Existing notes/documents and shell requests remain. Contact Overview also performs the existing Google connection-status request.
- Live Task and Call Overview smoke checks showed no new activity collection reads. The imported records selected in those checks were unlinked, so those checks alone do not establish behavior for every linked activity-modal timeline.
- Ten focused backend tests passed: counts above 50, latest-date and fallback semantics, single aggregate statement per module, normalized attendee matching without duplicate counts, input validation, hidden fields and all three roles' existing scope.
- New browser regression passed against real hooks/services under Strict Mode with fixture responses: Overview summaries without collection loading, 50-row first pages, 65-row continuation, per-kind continuation, parent/filter parameters, tab cache reuse, closed-consumer invalidation, parent changes, error/retry and denied-module refetch gating. Fixture data is distinguished from the actual imported-data run.
- Backend full checks: Ruff, compilation, committed migrations, ten opt-in PostgreSQL regressions, an empty-database migration-drift check and `alembic check` passed. The full unit run recorded **1,672 passed, 18 skipped, eight failed and two temporary-directory setup errors**. All nine filter-contract tests passed on a permission-corrected retry, including the two blocked cases. The eight failed-case names exactly match the unmodified baseline, with zero differences. Backend CI is still not green; these failures are not removed or waived.
- Frontend final full checks passed on Node **20.20.2**, snapshot **d7ea1c1a**: clean lockfile installation, changed-file formatting, full lint (zero errors, 1,528 warnings), every `npm test` suite, spreadsheets, standalone TypeScript, every CI browser command including the new related-activity regression, the additional session-startup regression, production build with safe test API/OAuth configuration and the configured dependency audit. No high/critical runtime advisories were found; the existing temporary ESLint-only exception remains. All 21 changed source/config/test files match the isolated snapshot. Earlier restricted-process Windows profile and SWC native-cache failures were resolved by permission-corrected execution; the final full run returned zero for every command.
- Evidence is under `.worktrees/entity-activities-20261008/`. Backend checks used disposable PostgreSQL/Redis on ports 15432/16379, separate from application services; both disposable containers were removed afterward. The application API still returned readiness 200 after cleanup.
- Final live Lead Overview/Activities smoke check had zero page errors and retained Lead details, Calls Made and the activity empty state. Chrome's platform-font inspector confirmed that heading glyphs were actually rendered with the custom **Instrument Sans** font, in addition to the earlier font-loaded checks.
- Graphify was updated after the final source changes: **22,400 nodes, 62,355 edges**. Existing missing HCL/SQL parsers, an empty pyproject extraction and five unrelated partial TSX parses remain coverage limits. Source inspection and browser evidence support the claims above.

No imported business records were modified for browser inspection. No push or deployment was performed. Local browser success is not stage verification. Any eventual rollout must expose the new backend summaries before deploying the frontend consumers.

## Remaining work

1. Replace the active `useGlobalTimeline` broad reads with scoped pages and continuation, including Contact-related Deals and their notes. Modal gating alone does not optimize a timeline once opened.
2. Audit the existing Contact related-Deals and Account related-Contacts consumers; their first-page global lists can omit related records outside that page.
3. Continue the earlier dense Calendar, Kanban, campaign recipient/composer and global-search work. Bound response size independently of request count.
4. Address the baseline backend test failures separately, and profile related-filter execution plans before choosing indexes. Font configuration was unchanged in this batch.
5. Timelines merge the currently loaded module pages and reorder as continuation adds records. They are not a unified server event cursor: derived Task/Call event timestamps can differ from each module's page ordering. A strict chronological timeline across modules needs its own scoped contract; every matched activity remains reachable through continuation.
