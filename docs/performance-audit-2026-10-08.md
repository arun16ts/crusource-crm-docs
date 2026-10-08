# Localhost request and font audit — 8 October 2026

Inspected the running localhost:3000 frontend and localhost:8000 API using Playwright MCP and Chrome DevTools Protocol. Used Graphify MCP first, then verified findings in source. Local credentials were used only against localhost. No backend, database schema, authorization rules, or stage deployment was changed.

## Browser evidence

Authenticated Leads list, default pipeline, filters and drawers closed; browser cache disabled; approximately five seconds after document navigation:

| Activity                                                | Before | After |
| ------------------------------------------------------- | -----: | ----: |
| CRM API requests, including import SSE                  |     24 |    14 |
| Session check-in                                        |      2 |     1 |
| Leads list                                              |      2 |     1 |
| Leads aggregates                                        |      4 |     0 |
| Unused shell tasks list                                 |      1 |     0 |
| Closed lead drawer: documents, approvals, Google status |      3 |     0 |

The initial baseline refresh capture contained 25 API calls because a reply-count poll from the outgoing document arrived immediately before reload. Two settled after-change refreshes each contained exactly 14 API calls; a preceding refresh captured one outgoing Leads request too. Navigation boundaries and polling affect raw Network-tab totals.

After-change settled five-second captures also had 48 localhost document/static requests, one route RSC request, 11 Kaspersky requests, and four other external requests: 78 total. The original longer baseline had dozens of development chunks plus Kaspersky XHR polling approximately every half-second. These requests do not query PostgreSQL. The running server uses Turbopack development chunks even though the default `dev` script specifies Webpack.

All baseline CRM responses that completed were successful. No retry storm was reproduced. Most feature and shell queries started in parallel after session bootstrap. Waiting for the pipeline before fetching Leads is an intentional dependency, preventing a broader discarded fetch.

## Request ownership and causes

| Request                                                     | Owner / reason                                                                                                  | Decision                                                                                    |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `/users/me`, `/users/me/permissions`                        | Session boundary, profile, authoritative access matrix                                                          | Keep; shared query keys deduplicate consumers                                               |
| `/auth/session-checkin`                                     | AuthGuard effect; development Strict Mode replay sent two pings                                                 | One ping per token per guard mount; auth verification still runs                            |
| `/organization/current`                                     | Header and formatting initialization                                                                            | Keep                                                                                        |
| `/billing/subscription`, `/billing/trial-extension-request` | Trial banner and subscription lockout                                                                           | Keep                                                                                        |
| `/teamspace/pending-counts`                                 | Sidebar badge                                                                                                   | Keep                                                                                        |
| `/onboarding/me`                                            | Onboarding shell and checklist                                                                                  | Keep; same cached query                                                                     |
| `/inbox?unread_only=false`                                  | Notification dropdown, including unread badge and new-event toasts                                              | Keep; this endpoint serves notifications, not a background fetch of email threads           |
| `/inbox/tracked-threads/reply-count`                        | Header reply badge                                                                                              | Keep                                                                                        |
| `/admin/data-import/events`                                 | Import completion SSE / cache invalidation                                                                      | Keep; one long-lived connection                                                             |
| `/saved-views?entity_type=leads`                            | Leads saved-view controls                                                                                       | Keep                                                                                        |
| `/admin/pipelines?target_module=leads&include_stages=true`  | Pipeline selector and board                                                                                     | Keep                                                                                        |
| `/leads`                                                    | Current filtered/paginated view                                                                                 | Wait for pipeline resolution; previously requested all pipelines, then the default pipeline |
| `/leads/aggregates` for industry and lead source            | Filter option lists                                                                                             | Load when Filters opens; retain five-minute cache                                           |
| `/leads/aggregates` for status                              | LeadBoard query whose returned value was never used                                                             | Remove; KanbanBoard's stage aggregate remains                                               |
| `/tasks`                                                    | Header's unused `useTasks()` result                                                                             | Remove from shell                                                                           |
| `/documents`, `/admin/approvals/requests`                   | Closed LeadDetailDrawer ran hooks before returning null; missing lead ID became an unfiltered documents request | Mount drawer only for an open selected lead                                                 |
| `/meetings/google/status`                                   | Closed drawer → useEntityActivities → disabled useMeetings → unconditional useGoogleStatus                      | Removed from initial Leads load by deferring drawer mounting                                |

Sources: [Header](../src/components/layout/Header.tsx), [AuthGuard](../src/components/auth/AuthGuard.tsx), [LeadBoard](../src/components/leads/LeadBoard.tsx), [LeadBoardModals](../src/components/leads/board/LeadBoardModals.tsx), [LeadDetailDrawer](../src/components/leads/LeadDetailDrawer.tsx), [useEntityActivities](../src/hooks/useEntityActivities.ts), [useMeetings](../src/hooks/useMeetings.ts), [useDocuments](../src/hooks/useDocuments.ts), [notifications service](../src/services/notifications.service.ts).

Global creation/import dialogs now use `next/dynamic`; the Leads add/import/detail implementations are also deferred. Add and import forms remain mounted after first use to preserve form/import lifecycle state, with closed Add Lead pipeline queries disabled. Shared activity forms mount only when their respective dialog opens.

## Caching and polling

[QueryClient](../src/lib/queryClient.ts) already supplies two-minute freshness, fifteen-minute garbage collection, no default window-focus refetch, and bounded retries. Hard refresh starts a new in-memory cache. Multiple hooks alone are not evidence of duplicate HTTP calls.

Profile and permission hooks intentionally override freshness/focus defaults (15 and 10 seconds respectively). Permission-revision changes cancel and reset cached feature data. These security-related behaviors were preserved. Notification polling remains every 10 seconds; reply and pending counts poll approximately every 30 seconds. A 22-second idle observation captured two notification polls and one each of pending/reply counts, with no Leads/documents/dashboard refetch cascade. Hidden-tab polling is not enabled by these queries.

## Backend and database implications

The [lead repository](../../crusource-crm-backend/src/modules/leads/repositories/leads_repository.py) applies `apply_scope` before filtering, counting, selecting or grouping. Owner data is eagerly joined for the list. One removed Leads list request eliminates its count and bounded selection; four removed initial aggregate requests eliminate four grouped queries. That is at least six avoided lead-data SQL statements, derived from source rather than measured PostgreSQL statement telemetry, plus the removed tasks/documents/approval requests and their authorization overhead.

No query scope was widened or cached across users. [Scope resolution](../../crusource-crm-backend/src/shared/auth/scope_guard.py), role checks, permission freshness, API services, mutation invalidation and backend contracts remain authoritative. There was no justification from the small local dataset for an index or migration change.

## Independent font investigation

[Root layout](../src/app/layout.tsx) defines Instrument Sans via `next/font/google`, preloaded and served locally as a WOFF2 under `/_next/static/media/`. It originally used `display: swap`. The external Google CSS/WOFF2 requests are Material Symbols icons, not the application text font.

Three cache-disabled login refreshes and repeated authenticated Leads refreshes loaded the text font successfully. Chrome's `CSS.getPlatformFontsForNode` confirmed Instrument Sans for the header, navigation and table text. In the initial capture the local font took approximately 16 ms. No permanent mismatch, font download failure, class replacement, or navigation/refresh configuration difference reproduced.

The user clarified that the wrong font corrects itself after loading. The global body CSS used a literal `"Instrument Sans", sans-serif`, bypassing Next's generated fallback stack. It now uses `var(--font-sans), sans-serif`, yielding `"Instrument Sans", "Instrument Sans Fallback", sans-serif` consistently.

With the local WOFF2 deliberately delayed 2.5 seconds, Chrome rendered Arial while `document.fonts.status` was `loading`, then Instrument Sans Bold after `document.fonts.ready`. This reproduces the transient fallback behavior described by the user. The text font now uses `display: block`: it briefly withholds text while the preloaded font loads instead of visibly swapping typography. Repeating the identical delay confirmed both FontFace descriptors were `block`; CDP paint captures showed the header text withheld while loading and rendered in Instrument Sans after completion. Normal local font loading was fast (approximately 16 ms in the baseline), so the intentional delay represents a stress test. If the font fails or exceeds the browser's block period, fallback remains available; indefinite blank text is not the policy.

## Verification and limits

Live localhost checks covered hard refresh, filters loading on demand, Add Lead, CSV upload/mapping preview and cancellation without importing records, list/Kanban switching, saved-view controls, and Contacts → Leads navigation. The local default pipeline returned zero leads, so record mutations and populated-record authorization cannot be claimed from these live observations. Browser fixtures separately verify scoped Leads query parameters, delayed enabling, Strict Mode check-in deduplication, session retry/recovery, and existing permission/deletion flows. The final CDP capture restricted requests to the new document's loader ID: all 14 API responses were HTTP 200, the local text font loaded in approximately 10 ms, and the rendered header font was Instrument Sans Bold.

The required frontend checks were run in a separate copy without local environment files so the running development app was not interrupted. Production build configuration uses `https://api.invalid` and a placeholder OAuth client. All applicable frontend checks passed under CI's Node 20.20.2:

- Clean `npm ci` from the lockfile; full lint (zero errors, 1535 existing warnings); `npm test`; spreadsheet regressions; TypeScript.
- All six CI browser commands: sales deletion, deals import, Teamspace pool scope, activity deletion, password recovery, and editor compatibility. The expanded session-startup browser regression also passed, including Strict Mode deduplication and deferred scoped Leads loading.
- Production build; dependency audit (no high/critical runtime advisories, existing time-limited ESLint exception); changed-file formatting against the current worktree, using the checker with `FORMAT_BASE_SHA` unset.

Initial sandbox checks encountered Node account lookup and SWC cache ownership blockers; authorized checks outside that sandbox cleared them. No required frontend check remains skipped or failing. No backend implementation changed, so backend migration/unit CI was not rerun. Remote GitHub CI, stage/Vercel/ECS, and a deployed production browser were not tested.

## Separate follow-ups

- Contacts navigation reproduced eager documents/deals/Google-status requests from its own feature tree. The global unused task fetch is fixed there too; other route drawer loading needs the same focused audit.
- Entity activity loading still downloads broad tasks/meetings lists and filters them in React; meetings requests default to `limit=100000`. A scoped entity-activity API should preserve related-contact and attendee-email matching before replacing this behavior.
- Leads Kanban requests up to 10000 records, while cards are limited only in the DOM. Server pagination per stage is a separate contract/UI change; lowering the cap would hide data.
- Ten-second notification polling remains a possible steady-state load target, but changing it alters notification latency. Measure with representative users/data before choosing batching, a badge endpoint, or a broader event stream.
- Quick draft restoration already has conflicting reset behavior in AddLeadModal/useFormDraft. No draft-policy change was bundled into this performance work.
- Font-download failure and non-Latin glyph coverage were not exercised. If a persistent mismatch is later observed, capture its computed font, actual rendered font and failed resources separately from transient loading.
- Graphify update completed at 22147 nodes/61492 edges, but reported missing Terraform/HCL/SQL parsers, an empty pyproject extraction, and partial parsing of five existing TSX files. Community labels were retained or replaced by hub names where clustering changed; semantic relabeling was not run. Those graph coverage limitations do not replace direct source verification.

The discarded list fetch, unused aggregates and eager drawer hooks can also run in production; these optimizations apply beyond development. Strict Mode replay, HMR/chunk counts and Kaspersky traffic should not be treated as deployed PostgreSQL traffic. No stage readiness or deployment approval is implied by this audit.
