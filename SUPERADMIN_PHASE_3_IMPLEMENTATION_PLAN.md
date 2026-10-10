# Super Admin Phase 3 implementation plan

Date: 10 October 2026. Status: **COMPLETE — 3A–3E and integrated local acceptance verified. Operational release verification remains separate.**

This is the execution companion for Phase 3 of [the phase-wise roadmap](SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md). It builds on [Phase 1](superadmin-phase1/README.md), [Phase 2](superadmin-phase2/README.md), their architecture/verification packages and the [Phase 3 handoff](superadmin-phase2/PHASE_3_HANDOFF.md). Current source takes precedence over historical specifications. Reviewed baseline: frontend `d9e13de4`, backend `48a98bc`, docs `e045602`.

Implementation evidence and remaining work: [Phase 3 review package](superadmin-phase3/README.md). Overview and the separately reproduced trial partial-commit fix are recorded in the initial package. [Organizations and Login History (3B/3C)](superadmin-phase3/ORGANIZATIONS_LOGIN_HISTORY.md) are now verified locally. [Trial review, Feedback and integrated acceptance (3D/3E/3.6)](superadmin-phase3/TRIALS_FEEDBACK.md) are now verified locally; [Phase 4 handoff](superadmin-phase3/PHASE_4_HANDOFF.md) is recorded.

## 1. Outcome and boundaries

Finish the contents and behavior of every existing protected platform page using the shared CRM design. The completed portal must display truthful metrics, load bounded data, preserve view state across navigation, handle errors explicitly and execute trial reviews safely.

Included routes: `/superadmin/dashboard`, `/superadmin/organizations`, `/superadmin/organizations/[id]`, `/superadmin/login-history`, `/superadmin/trial-extensions` and `/superadmin/feedback`, including their member drawers, image viewer, filters, export and review dialogs. Test equivalent short routes on the platform host through the existing route helpers.

Phase 1 invitations/MFA/durable delivery and Phase 2 shell/access management are foundations to preserve, not rebuild. Demo requests, support tickets, capability administration, Analytics, Error Center, Logs and measured infrastructure health keep their later phases. Do not add tenant suspension, billing-plan editing, impersonation, bulk destructive actions or unsupported controls merely because they fit an admin screen.

This phase includes necessary backend corrections. It is not a CSS-only task and should not be treated as one small unreviewed change. Local completion remains distinct from the Phase 6 operational release.

## 2. Baseline source findings that determine the work

Paths below are relative to the owning application repository.

| Finding | Source evidence | Phase 3 consequence |
| --- | --- | --- |
| KPI response returns literal `system_status: "healthy"`; User counts include all users; pipeline value sums amounts without grouping currency | Backend `src/modules/superadmin/repositories/superadmin_dashboard_repo.py` | Correct the source/definition of metrics; do not manufacture service health or label the sum as revenue. |
| Dashboard renders the pipeline sum with a literal dollar sign | Frontend `src/app/superadmin/dashboard/page.tsx` | Omit the invalid total by default; only display separate currency groups when source currency is trustworthy. |
| Organization list is already server paginated, but page/search/sort are local state | Frontend organizations route; backend `superadmin_org_repo.py` | Preserve server pagination while moving shareable state to the URL and adding stable ordering. |
| Organization detail returns all members, aggregates logins across the roster and queries the latest IP separately for each member | Backend `get_organization_with_members` in `superadmin_org_repo.py` | Add a bounded member query and set-based login summaries; avoid whole-roster hydration and per-member reads. |
| Organization detail mounts login history regardless of active tab; its hook is enabled for any authenticated platform session | Frontend organizations detail route; `src/hooks/queries/useSuperAdminLoginHistory.ts` | Enable tab reads only when the tab and organization are valid; never fall back to an unfiltered platform query while an ID is missing. |
| Login-history export uses repository `.all()`, builds a full list and full StringIO response; its UI calls the service directly | Backend `superadmin_login_history_repo.py` / `login_history_handler.py`; frontend login-history route | Move orchestration into a focused export hook and make server CSV generation bounded. A CSV response is not currently a streaming implementation. |
| Login screen shows 100% success for a period with zero attempts and uses local-only filters | Frontend login-history route | Show “No attempts”/not applicable and define URL/time-window semantics. |
| Trial UI stores filters and a copied `selectedRequest` in Redux | Frontend `trialExtensionsUiSlice.ts` and trial-extensions route | URL owns list state; actions select an ID and resolve current data from TanStack Query. |
| Trial approval's repository helper commits before the handler writes SubscriptionHistory; reads are not locked for competing reviews | Backend `approve_trial_extension_handler.py` and `superadmin_trial_extension_repo.py` | Review and correct transaction/concurrency behavior before polishing action dialogs. |
| Feedback list supports several server filters, while stats accept only organization ID | Backend feedback routes/handlers; frontend feedback route | Label global statistics explicitly or extend stats with the same typed filter contract; do not imply they describe the filtered list. |

These were planning-time source findings. The linked implementation packages record local runtime reproductions, contract decisions and before/after browser/PostgreSQL verification.

## 3. Foundations to retain

- Reuse `WorkspaceFrame`, `PlatformWorkspace`, navigation/host helpers, session boundary, Instrument Sans, design tokens, shared buttons/tables/pagination/dialogs and pure platform formatting. Keep customer billing, inbox, onboarding, SSE, AI and CRM-preference hooks in the CRM wrapper.
- Thin route entries delegate to focused feature screens. Components render, hooks coordinate, services call `platformHttpClient`, handlers execute one use case and repositories construct queries. Avoid a new generic admin framework.
- TanStack Query owns entities, totals, read/mutation status and invalidation. Protected keys retain staff ID/session epoch plus every response-affecting parameter. Forward AbortSignal; old-session responses cannot populate another account's cache.
- URL parameters own search, filters, sort, page size, page and shareable detail tabs. Normalize invalid input; change filters and reset pagination together, avoiding a request for a stale high offset. Debounce committed search, not every keystroke into a new history entry.
- Redux holds only appropriate shared UI preferences. Drawers/dialogs use selected IDs and local drafts. Do not persist privileged command bodies, personal content or fetched rows.
- Preserve platform cookie/origin/custom-header/CSRF admission and current platform guards. CRM bearer tokens must fail on platform reads and writes. Preserve owner-only access administration separately; Phase 3 does not grant new staff capabilities or change customer role scopes.

Use current per-feature query freshness policies as the baseline rather than globally disabling refetches. No new periodic polling for ordinary pages. Refresh the active view and affected summaries after a successful action; do not invalidate every platform module.

## 4. Delivery order

| Step | Deliverable | Exit evidence |
| --- | --- | --- |
| 3.0 | Runtime/source baseline and contract decisions | Route/action matrix, screenshots, network and SQL findings, authorization and metric definitions recorded |
| 3A | Truthful Overview | Correct customer/staff counts, no fabricated health or mixed-currency total, real empty/error/retry states |
| 3B | Organizations list/detail | URL state, server table, bounded members and active-tab reads, correct organization identity |
| 3C | Login history/member drawer/export | Time-zone/filter agreement, bounded export, no drawer reads while closed, CRM check-in preserved |
| 3D | Trial review integrity and UI | Atomic review/history, concurrent-review conflicts, current-record dialogs and targeted invalidation |
| 3E | Feedback list/stats/viewer | Clear statistic scope, protected content, bounded filtering and accessible viewer |
| 3.6 | Integrated verification and review package | Full applicable CI, actual-route/browser/visual/scale evidence and release limits recorded |

Implement small frontend/backend changes within each package. Review the trial transaction defect during 3.0; its integrity fix may be brought forward as a separate tested patch if it is reproduced. Do not wait for the visual sequence to finish to address confirmed partial commits. No calendar estimate is asserted before baseline measurements and contract decisions.

## 5. Step 3.0 — Baseline and decisions

1. Record all three repository revisions and local edits. Confirm the merged migration head and API contracts read-only; do not automatically migrate the application database during a redesign baseline.
2. Exercise each route through real Next.js routing and an isolated API with synthetic owner/operator accounts. Use the running local platform with authorized staff credentials where available. The provided CRM login is not a platform credential.
3. Capture loaded Instrument Sans and compiled CSS at 1440/1024/768/390px, collapsed/expanded/mobile navigation and 200% zoom. Include each page, drawer, confirmation and loading/error state.
4. Record API paths/parameters, payload rows/bytes, cancelled/completed duplicates, tab/drawer requests and idle activity. Distinguish needed identity/CSRF requests, development lifecycle attempts and genuine redundant reads.
5. Profile relevant SQL against disposable PostgreSQL: member count/roster/login summaries, filtered history/export, dashboard aggregates and trial review. Record query count, plans and memory where meaningful; propose indexes only when plans justify them.
6. Freeze a contract matrix: supported filters/sorts/page limits, global versus filtered statistic scope, customer/staff classification, date boundary/time zone, allowed trial transitions, current error/conflict semantics and protected image delivery.

Proposed decisions: retain platform UTC as the default; preserve customer login telemetry separately from platform security events; omit the invalid financial total unless valid currency groups are available; keep trial eligibility/duration rules unchanged unless a specific inconsistency is reviewed. Check how already-paid/cancelled subscriptions interact with trial approval before changing that business policy.

## 6. Package 3A — Overview

Move presentation into an Overview feature screen with shared headings/cards and independent data states. Initial failure must not become a dashboard full of zeros. During refresh, retain the last successful values with an updating/stale indication; show a retry action for failure. Display zero only when an authoritative query returned zero, and avoid describing an active account as a recently active user.

Define customer accounts and platform staff from the existing identity model; do not use non-null organization alone to classify every possible onboarding account. Separate their totals/role/provider breakdowns so percentages use the correct denominator. Explicitly label the existing 30-day window and definition of “active.” Apply intended soft-deletion semantics consistently to activity/entity counts.

Remove the unmeasured healthy badge. Phase 7 will provide measured operational health; Phase 3 must not substitute `/health/ready` for infrastructure/worker availability. Pipeline amounts are sales values, not paid revenue. If grouping by `Deal.currency`, handle missing/invalid currency visibly and do not apply invented exchange rates or silently assign USD.

Keep aggregates server-side, consolidate compatible counts where measured useful and avoid fetching whole entity lists for cards. Record backend SQL cost separately from frontend request count. If caching is introduced, give it an explicit TTL/source freshness and preserve authorization; do not turn stale operational values into real-time claims.

**Accept when:** fixture totals distinguish customers/staff, empty datasets and mixed currencies are truthful, API failure remains visible, and route entry fetches only Overview data plus required platform identity.

## 7. Package 3B — Organizations and detail

Reuse shared server-mode DataTable with server search, subscription/active filters, supported sorting and stable UUID tie-breaking. URL state survives direct links, refresh and back/forward. Count queries operate on matching organizations without unnecessary display projections; profile sorting by member count separately. Do not paginate or filter an API page again in React.

Split organization summary from a bounded Members query, preferably additive to preserve existing API consumers. Default to 25 or 50 members using established limits and allowlisted sort/filter fields. Request login summaries only for visible members, using grouped/window/subquery reads rather than one latest-IP lookup per member. Keep member totals accurate without loading the complete roster.

The existing full-detail contract needs an explicit compatibility decision: use an additive summary/member endpoint or an opt-in omission parameter, not silently return a truncated `members` array under its existing meaning. Give the obsolete full-roster path a documented caller inventory before deprecation.

Members and Logins tabs have independent URL pagination and explicit enablement. Opening Members must not fetch Logins; switching tabs requests only that tab. Drawer queries run only for the chosen user and are cancelled/reset when the selected tenant/user changes. Keep user/organization relationship validation server-side where a tenant-context route promises that relationship.

**Accept when:** a large tenant returns at most one requested member page, SQL reads do not grow per visible member, inactive tabs do not read, and a deleted/invalid organization shows a deliberate 404 state rather than another tenant's data.

## 8. Package 3C — Login history and member drawer

Use shared date/filter/table controls and a focused URL hook. Support existing organization, user, status, method and search filters; filter changes reset the page. Resolve calendar-date windows in the stated platform time zone with an explicit inclusive/exclusive boundary contract, including end-of-day, DST and UTC boundaries. Preserve the existing API semantics or coordinate any correction across service/query/list/export consumers.

Label current all-time/30-day statistics separately from the filtered list, or add a matching filtered-stat query. Zero attempts produce not-applicable rates. Identify this customer login-history dataset clearly; do not silently combine it with Phase 1 platform security events. Preserve `sessionCheckin()`'s CRM bearer transport and ordinary CRM AuthGuard behavior.

Move export status/cancellation/error handling into a dedicated hook using the existing service boundary. Export the full matching dataset rather than the visible page, with the exact committed filters and date boundaries. On the backend, replace `.all()` and full-file StringIO with bounded repository iteration and CSV production, stable ordering, formula protection and cleanup on cancellation. Confirm stream/database-session lifetime against the installed FastAPI version. If measured exports exceed a safe request duration, use a platform-authorized job design sharing suitable file primitives; do not route staff cookies through the CRM-only export job authorization or create another unrelated mail/work queue.

The member drawer fetches current profile/history only while open, with its own bounded history pagination, retry and missing-user state. Retain original authorization and avoid exposing additional credential/session material in a new UI or export.

**Accept when:** downloaded row count/filters match the server result across multiple pages, memory is bounded during server generation, dates agree across table/drawer/export and CRM session startup/check-in regressions pass.

## 9. Package 3D — Trial extensions

First make review persistence atomic: request state, organization/subscription expiration and SubscriptionHistory commit together. Repositories flush rather than independently commit an in-progress approval. Use an established locking/conditional-update strategy so competing approve/approve and approve/reject requests produce one business outcome and one matching history entry. Revalidate current actor authority for the write transaction through existing platform boundaries; a previously returned guard object is not sufficient after revocation.

Retain requested/approved day bounds, review notes and the existing rule of extending from a future expiration or from now after expiry. Do not accidentally double-extend on retries. Define stale-review `409` handling and safe uncertain-outcome retry; add expected-version/idempotency contracts where needed before claiming that retry is safe. Reuse suitable existing mechanisms without automatically applying the global staff-auth lock to every business read.

Move list filters/page/sort into the URL. Replace Redux entity copies with selected IDs and local drafts; obtain the authoritative request from the cache or a guarded detail query. If another reviewer has completed it, refresh and present the conflict instead of submitting obsolete data. Pending/error dialogs retain notes, accessible focus and actionable explanations; success closes only after confirmed completion.

Label `total_matching` and the existing global pending count separately. Invalidate relevant trial lists/details, affected organization/billing summaries and Overview only where its displayed fields changed; no blanket platform refetch.

**Accept when:** PostgreSQL competing-review tests and injected commit failures prove atomicity/no duplicate extension, actor revocation blocks writes, invalidation updates affected views, and ordinary customer trial-request/lockout flows still work.

## 10. Package 3E — Feedback

Use a focused screen, shared server-filter controls, pagination, rating/status treatment and accessible image viewer. Search/category/rating/organization/date filters belong in the URL. Either label the current summary cards “Platform-wide”/“Organization-wide” or extend stats to the exact list filters; do not derive complete statistics from one page.

Distinguish no feedback, no matches, initial failure and stale refresh failure. Render content as text and validate attachment metadata. Verify actual storage authorization before choosing image delivery: approved private media must not become an arbitrary external URL or permanent public download. Preserve access on refresh and provide deliberate expired/missing image states. The viewer supports keyboard close/navigation, focus restoration, mobile sizing and localized labels.

Do not convert feedback to a support conversation or Error Center issue in this phase; those relationship workflows remain later work. Preserve ordinary CRM feedback collection, tenant isolation and existing trigger behavior.

**Accept when:** filtered totals/stat labels agree, protected content is unavailable without a valid platform session, malicious content/URLs are handled safely and CRM feedback regressions pass.

## 11. Verification and completion gates

For every package, test direct navigation/reload/back/forward, invalid URL parameters, page reset and stable ordering, current-session cache boundaries, retry/abort/outage, empty/stale states and forbidden access. Use multi-page synthetic fixtures and representative bulk volumes in disposable PostgreSQL. Record before/after SQL reads and network payload sizes without inventing a universal request-count target.

Use real CSS/fonts at the reference widths and zoom; keyboard-test controls, table scrolling, focus and dialogs. Preserve the pre-change CRM frame comparison and current Calendar, activity pagination, export and session regression commands. No application/stage data is cleared or seeded. Browser-only responses are labelled fixtures, not evidence of a live provider or deployment.

Existing backend suites to extend include `test_superadmin_dashboard.py`, `test_superadmin_organizations.py`, `test_superadmin_login_history.py`, `test_trial_extensions.py`, `test_superadmin_feedback.py` and `test_superadmin_guard.py`. Retain Phase 1 platform races/delivery and Phase 2 contracts/auth/real-route/CRM-frame checks. Add behavior regressions for new pagination/export/review contracts; file names are chosen during implementation, not claimed to exist now.

After each implementation run the owning repositories' complete applicable CI as required by current AGENTS.md and workflows: clean lockfile install, changed-file formatting, full lint/unit/localization/spreadsheet/public/Loop/browser checks, types/build/audit; backend Ruff/compile/full suite, required Redis/PostgreSQL flags, committed migrations, fresh empty-database drift and Alembic check. Cross-repository packages require both sides. Record pre-existing failures and blocked checks accurately; focused checks alone do not establish readiness. Update Graphify after code changes.

Phase 3 is complete locally only when all five packages have their wired UI/API behavior, accepted contracts, visual evidence, role/session/concurrency tests and full checks recorded. There must be no fabricated health, developer branding, full-roster/default export arrays, double pagination or server entities mirrored into Redux in these flows. Current customer authorization/data scopes and required functions remain intact.

Produce `superadmin-phase3/README.md`, architecture/contract notes, verification results, screenshot index and a Phase 4 handoff. Update the phase-wise status only after evidence passes. Preserve the feature inventory's required status vocabulary and distinguish fixtures, localhost and deployed verification.

Before operational release, Phase 6 still verifies actual migration state, compatible frontend/backend timing, platform origins/TLS cookies, durable delivery and stage/customer flows. Keep new APIs additive where possible; do not roll back to a Phase 0 UI against retired invitation writers. Phase 3 planning introduces no automatic deployment or application-database migration.

**First implementation:** 3.0, followed by the 3A metric contract/UI corrections and the confirmed trial-integrity patch as an independently verified change.
