# Super Admin Phase 2 implementation plan

Date: 9 October 2026. Status: **COMPLETE — local implementation and verification.** See the [Phase 2 review package](superadmin-phase2/README.md) for source evidence, screenshots, verification and release limits. The specification below records the approved scope; the review package records the delivered implementation, including the narrow delivery-configuration incident fix.

Phase 2 delivers the CRM-aligned Super Admin workspace and the frontend for the completed Phase 1 invitation/authentication APIs. It follows the [phase-wise roadmap](SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md), [Phase 0 baseline](superadmin-phase0/BASELINE_REPORT.md) and [Phase 1 API handoff](superadmin-phase1/API_HANDOFF.md). The [registered-router OpenAPI snapshot](superadmin-phase1/platform-auth.openapi.json) and current source contracts take precedence over older design documents.

## 1. Required outcome and scope

The Super Admin portal uses the same font, design tokens, workspace geometry, navigation treatment, buttons, headings, tables, pagination and interaction conventions as the CRM. An owner invites staff from the application; the recipient activates the invitation, sets a password, enrolls MFA and signs in. The owner can inspect invitations and staff, resend/cancel eligible invitations, reset staff sign-in and revoke staff access.

The visible changes in this phase are:

- A CRM-aligned sidebar, header and inset workspace around every existing Super Admin page, with desktop collapse and mobile navigation.
- Redesigned staff sign-in, activation and MFA screens; invitation-only guidance replaces public access applications and developer-login language.
- A working **Platform Access** area with **Invitations** and **Staff** tabs, server-backed lists, invitation creation and safe management dialogs.
- Explicit session-loading, signed-out, forbidden, offline and service-unavailable states, including recovery from an unresponsive identity request.

The complete redesign of overview cards, organization lists/details, login history, trial-extension workflows and feedback contents remains **Phase 3**. This phase integrates those pages with the shared frame and necessary authentication/cache boundaries. Demo intake/board, support tickets, capability administration, analytics, Error Center and Logs retain their agreed later phases. Do not add enabled navigation to screens that do not exist.

Phase 2 is primarily frontend work. No database migration, dependency upgrade, new authentication mechanism or live provider key is planned. A verified backend contract gap must be recorded with its affected use case and addressed through the existing CQRS boundaries; it must not become an unrelated backend expansion.

## 2. Findings that determine the implementation

Paths in this table are relative to `crusource-crm-frontend/` unless stated otherwise. These are source findings, not assumptions drawn from screenshots alone.

| Current implementation | Consequence for Phase 2 |
|---|---|
| `src/app/layout.tsx` loads Instrument Sans and the shared providers; `src/app/globals.css` defines CRM tokens | Reuse these foundations. Do not create a separate platform stylesheet/theme or install another font. |
| `src/components/layout/DashboardShell.tsx` includes CRM billing, permissions, SSE, onboarding, lockout and AI effects | Extract the smallest pure presentation frame. Mounting the complete CRM shell in Super Admin would introduce inappropriate customer-session behavior. |
| `src/components/layout/Sidebar.tsx` and `Header.tsx` contain CRM-specific hooks, storage and actions | Share suitable presentation primitives; keep platform identity/navigation separate from the CRM wrappers. |
| `src/app/superadmin/layout.tsx` shows developer-language loading/authentication screens and treats identity errors alike | Introduce an explicit session boundary and bounded transport. A backend interruption must resolve to a retryable failure instead of an endless spinner or a misleading credential error. |
| `src/components/superadmin/auth/PlatformEntry.tsx` and existing entry hooks include public access-request behavior | Retire those forms and calls; preserve working login/activation/MFA contracts. |
| `src/components/superadmin/PlatformAccessManagement.tsx` uses the old requests/operators workflow | Replace it with the Phase 1 invitations/staff APIs. The retired write endpoints return `410`. |
| `src/lib/api/platformHttpClient.ts` owns cookie/CSRF transport, but `post` does not accept action headers and transport has no bounded identity timeout | Extend this client narrowly for typed errors, idempotency headers and cancellation/timeouts. Preserve separation from CRM bearer/refresh transport. |
| Existing platform query keys are not scoped to the staff identity | Migrate protected hooks to identity/session-scoped keys and selective cleanup; old responses must not populate a newly signed-in account's UI. |
| `src/components/shared/table/DataTable.tsx` slices rows through its pagination adapter | Add an explicit server-pagination path so an API page is never paginated a second time. Preserve the client-pagination default. |
| `src/components/shared/ConfirmModal.tsx` closes immediately after a destructive confirmation and lacks a complete dialog focus contract | Provide a compatible controlled-close option and accessible dialog behavior for privileged asynchronous actions. A failed revoke/reset must keep its explanation and form visible. |
| `src/hooks/useFormatting.ts` reads the CRM current user and synchronizes CRM preferences | Use pure shared formatters with explicit platform preferences instead of calling this hook from platform pages. |
| `src/proxy.ts` supports both `/superadmin/...` paths and short paths on the Super Admin host | Centralize route construction and test both forms, including a configured external CRM link. |

The inspected manifest/installation reports Next.js **16.3.8**, React **19.2.4**, TanStack Query **5.104.1** and Redux Toolkit **2.13.0**. Recheck these before editing; the repository map's Next.js 16.2 label is older. Use installed Next.js documentation and existing scripts rather than introducing an upgrade during this phase.

## 3. Architecture and state ownership

```text
Thin Next.js route
  → feature screen + focused interaction components
  → TanStack Query hooks + URL-state hooks
  → typed platform services
  → existing same-origin platform HTTP client
  → Phase 1 query/command API

CRM wrapper      → shared presentation frame ← platform wrapper
CRM domain hooks                            platform session/navigation
```

Keep route entries and server layouts thin. Put interactive behavior at focused client boundaries; protected cookie-based browser reads remain in the established client-session design. Do not put platform API requests inline in components or fetch protected records from a Server Component without an explicit authentication/cache design.

| State | Owner | Rules |
|---|---|---|
| Identity, invitations, staff, totals, delivery state and API errors/loading | TanStack Query | Services first; keys include identity, session scope and every response-affecting list parameter. No entity copies in Redux. |
| Active tab, search, filters, sorting and page/page size | URL/search parameters | One focused App Router hook; normalize invalid parameters; preserve browser back/forward. |
| Shared platform sidebar collapse/folds and UI preferences | Redux Toolkit, under a dedicated platform namespace | Persist only appropriate preferences using platform-specific storage keys. Do not change CRM sidebar preferences. |
| Mobile overlay, form drafts, field errors, OTP and current dialog action | Local component/feature state | Store only a selected record ID for actions; resolve the current server row from the query. Do not persist credentials or sensitive drafts. |
| Idempotency key and exact submitted command body | Local action controller | Retain together through an uncertain request outcome; do not expose them in URLs or persistent storage. |
| Activation token and MFA setup material | Auth-screen memory only | No durable Query persistence, Redux, storage, analytics or logging. Clear on completion/exit. |

Use SOLID through existing boundaries: components render/interact, hooks coordinate state, services define wire contracts, and shared primitives render presentation. Prefer narrow typed props and focused functions over a shell with unrelated boolean flags. Share real repeated behavior; do not build a generic administration framework.

If backend work becomes necessary, reads go through query handlers and writes through command handlers; repositories own persistence and services own reusable domain/integration behavior. Routes validate, authorize and delegate. Preserve Phase 1 transactional authorization, version/idempotency rules and delivery invariants.

## 4. Delivery sequence and review boundaries

Implement in the order below, in small reviewable changes. Each step includes its relevant verification before the next dependent step starts.

| Step | Deliverable | Dependency | Exit evidence |
|---|---|---|---|
| 2.0 | Confirmed contracts, route matrix and fresh visual baseline | Phase 1 | Sources, migration/API readiness and CRM reference states recorded |
| 2.1 | Typed transport, bounded session handling and cache isolation | 2.0 | Timeout/auth/outage/cancellation/account-switch cases pass |
| 2.2 | Shared presentation frame and compatible UI primitives | 2.0 | CRM reference still matches; server-table and async-dialog behavior verified |
| 2.3 | Platform shell, navigation, preferences and formatting | 2.1–2.2 | Platform frame matches CRM; no customer-session requests |
| 2.4 | Staff login, activation, enrollment and MFA screens | 2.1–2.3 | New and existing staff authenticate; interrupted enrollment resumes correctly |
| 2.5 | Invitations and Staff management UI | 2.1–2.4 | Owner completes every supported action against the test API |
| 2.6 | Legacy-entry cutover and existing-page integration | 2.3–2.5 | No retired writes/developer labels; both host forms and protected pages work |
| 2.7 | Integrated verification and review package | All steps | Functional, actual-route, visual and CRM regression gates recorded |

This is a delivery sequence, not a production rollout schedule. Estimates should be set after 2.0 confirms any changed source contracts and baseline failures.

## 5. Step 2.0 — Freeze the implementation baseline

1. Record nested repository revisions and local changes. Preserve unrelated edits, particularly `Superadmin login.md`; do not read credential values into reports.
2. Recheck registered routes, DTOs, current migration head and the Phase 1 handoff. The user has confirmed migration and application startup; verify readiness read-only instead of rerunning migrations as part of UI work.
3. Capture the CRM reference with actual compiled CSS and loaded fonts at 1440, 1024, 768 and 390px widths. Record browser version, viewport height, locale and collapse state. Include a table, page header, form and confirmation dialog.
4. Confirm full-path and short-host routes, API rewrites and trusted origins. Native development uses frontend 3000/backend 8000; production frontend start uses 3005; full Docker uses frontend 3001/backend 8001. Do not use the wrong host's API origin.
5. Record current lint/type/browser failures before changes. Verify the available browser harness rather than assuming there is a configured Playwright test runner.
6. Produce a brief source-backed contract checklist. Only advertise fields, filters and actions supported by the current API.

**Gate:** the shared-frame boundary and API/routing assumptions are reviewable before any CRM shell extraction.

## 6. Step 2.1 — Transport, session states and cache isolation

### Transport

- Keep `platformHttpClient` as the single same-origin platform-cookie transport. Extend `post` with narrow typed options for action headers and cancellation; preserve existing call signatures.
- Continue `credentials: same-origin`, no-store responses, `X-Platform-Request: 1`, trusted-origin admission and CSRF on authenticated writes. Do not invoke CRM token refresh for a platform `401`.
- Parse both flat Phase 1 errors and existing authentication `detail` errors into a typed error carrying status, code, safe message, request reference, field errors and current version where available. Avoid rendering or logging raw backend payloads.
- Give identity/bootstrap reads an explicit **12-second** timeout. Compose the caller's AbortSignal with the timeout and clean up resources. Test timeout during both the request and response handling. Privileged command timeouts represent an unknown outcome and retain their action key/body.
- Forward TanStack cancellation to fetch, including any CSRF bootstrap. Prevent a previous session's delayed bootstrap from restoring its CSRF token after a logout/account change.

### Session boundary

| State | Required UI/behavior |
|---|---|
| Initial identity check | Accessible loading message; no protected child requests; bounded request |
| Authenticated | Render platform workspace using the resolved identity |
| `401` | Clear protected platform data/CSRF, show staff sign-in; preserve the CRM session |
| `403` | Show insufficient-access guidance; hide owner-only areas; do not call it a password failure |
| Offline/paused request | Explain offline state and provide recovery; never leave an unexplained spinner |
| Timeout, connection reset, non-JSON proxy failure or `5xx` | Show temporary-unavailability state and Retry; do not declare the account invalid |
| Logout in progress | Disable protected queries/actions and prevent old content from flashing |

Do not repeatedly mount independent identity guards in the layout and sidebar. Consume one authoritative session query/boundary and pass narrow identity/navigation props where needed. Owner-only queries must be disabled for ordinary staff, including navigation badge queries.

Use a platform query-key factory, for example `['platform', staffId, sessionEpoch, 'invitations', normalizedParams]`. The epoch is a client scope marker, not a new server contract. Keep bootstrap identity separate until its principal is known. Never include CSRF, passwords, activation tokens or setup URIs in keys.

Update all protected platform hooks needed by existing pages, including login-history and badge hooks. On logout, identity loss or account transition, disable/cancel platform queries, remove current and legacy `superadmin`/`platform-auth` caches as appropriate, reset CSRF and clear sensitive mutations. Fence late responses with the session scope. Preserve unrelated CRM queries, cookies and preferences.

Logout is successful only after server confirmation or an already-signed-out response. A network failure cannot clear an HttpOnly cookie; keep the workspace blocked with a retryable logout state. Synchronize platform logout/account invalidation between tabs using a small platform-only notification channel; send no credential/session data through it. Revalidate on focus and handle server-side revocation through the same boundary.

**Gate:** simulate the reported backend disconnect and prove the spinner resolves, Retry works, and delayed results cannot expose another staff account's cached data.

## 7. Step 2.2 — Share CRM presentation safely

Extract a small workspace frame from `DashboardShell.tsx`, with typed sidebar/header/content slots and a forwarded workspace ref where required. The CRM wrapper keeps its billing, SSE, permissions, trial lockout, onboarding, global modals, progress indicators and AI behavior.

Match the actual CRM configuration:

- Instrument Sans through the existing `--font-sans` variable.
- Existing primary, background, surface, outline and text tokens from `globals.css`; no copied platform palette.
- Sidebar widths **236px expanded / 64px collapsed**, header **64px**, existing responsive outer spacing and rounded white workspace treatment.
- Existing spacing, icon sizing, typography, border/shadow treatment and scroll ownership. Preserve CRM welcome anchors, onboarding overlays, trial banner positioning and AI-panel sizing/ref behavior.

Reuse `Button`, `AdminPageHeader`, `OtpInput`, shared table/pagination and established toast/message conventions. Share sidebar/header presentation only where its dependencies are pure; do not mount CRM header actions, notifications, global search or AI controls in the platform workspace.

Make two focused shared-component changes:

1. **DataTable:** add explicit server pagination, server totals and controlled sorting support using a narrow typed contract. Already-paged API rows render directly. Existing client-pagination behavior remains the default. For platform lists, use only page sizes at or below the API limit of 100; do not expose the shared default of 200. Provide an accessible sorting control rather than a mouse-only clickable heading.
2. **ConfirmModal/dialog primitive:** support controlled closing after a successful async action, inline errors/reason fields, labelled dialog semantics, focus trap/restore, Escape policy and pending-state dismissal policy. Preserve existing callers' defaults. Disable the close icon as well as other dismissal paths during a sensitive pending action. Reuse an established accessible primitive if available; do not create a second dialog system.

**Gate:** compare the CRM frame before/after extraction and exercise existing CRM collapse, trial/onboarding, header and AI behavior. Verify server page two renders its rows once and failed destructive commands keep their dialog open.

## 8. Step 2.3 — Platform workspace and navigation

- Add a platform wrapper around the shared frame, with the authenticated staff identity, collapse control, mobile navigation and sign-out action. Use **Super Admin** and **Platform staff** terminology.
- Centralize typed navigation with route identity, translated label, icon and access predicate. Preserve existing working destinations; show Platform Access only to the owner. Protect direct owner-route entry as well as hiding its navigation item.
- Build a route helper for full `/superadmin/...` paths and short paths on the Super Admin hostname. Preserve safe query parameters through routing. Any return destination must be an allowed platform route, not an arbitrary external URL.
- Use a configured trusted CRM origin for **Open CRM**. On the Super Admin host, a bare `/dashboard` is rewritten to the platform dashboard and cannot serve as the customer CRM link.
- Replace the old access-request badge with an owner-only pending-invitation total from the new bounded endpoint. Count server totals independently from the current table's filters. Do not fetch whole lists just to count badges.
- Remove hardcoded health claims from the new shell. Full overview health/metrics corrections remain Phase 3.
- Keep platform UI preference keys separate from CRM keys. Add only preference fields that have a real UI; do not persist modal selection, record data, passwords, OTP or action bodies.
- Use pure `format*` helpers with explicit platform locale/timezone. Default platform timestamps to clearly identified UTC unless a validated platform-specific timezone preference is selected. Do not inherit customer organization currency or query its settings.
- Support the existing English/Dutch message catalogs. If a platform locale control is exposed, give it its own scope/provider and persistence; review `LocaleSynchronizer` so it does not overwrite CRM locale preferences through global storage. Do not invent additional supported languages.

**Gate:** owner and non-owner navigation work at all reference widths, keyboard/mobile focus is correct, and a network assertion finds no CRM current-user, billing, inbox, SSE or organization-settings requests initiated by platform rendering.

## 9. Step 2.4 — Staff authentication and enrollment

Build the following screens using the shared auth inputs/buttons, `OtpInput`, translations and CRM visual conventions. Keep platform authentication distinct from customer signup, OAuth and password recovery.

| Screen/state | Required behavior |
|---|---|
| Staff sign-in | Email/password validation, pending state, safe auth error and MFA handoff. Existing owner/staff credentials continue to work. |
| Invitation activation | Read the existing fragment token into memory and remove it from browser history immediately. Submit token/password through the existing activation API. Password policy remains 12–128 characters. |
| Authenticator enrollment | Render the setup QR/manual material using existing dependencies; explain setup and verification. Never render setup material on a protected workspace page. |
| MFA challenge | Six-digit input, paste/autofill/keyboard support, one submission path and disabled pending controls. Handle invalid/expired/replayed codes without duplicate requests. |
| Interrupted enrollment | With no fragment token on activation reload, call the existing enrollment query using its pending cookie. Resume the same setup; do not generate new material or extend server expiry. |
| Expired/cancelled/revoked invitation or enrollment | Show actionable guidance to contact the owner for a new invitation or sign-in reset, according to the server result. |
| Legacy request-access bookmark | Invitation-only explanation and staff sign-in link; no public application or email-verification form. |

Pending enrollment does not authorize `/me` or the workspace. Treat that expected `401` as an enrollment state only within the entry flow, never as permission to render protected content. An ordinary MFA challenge cannot use the enrollment-resume endpoint; if that challenge cannot be resumed after reload, return to sign-in instead of inventing a new API.

Use a narrowly scoped, non-persisted enrollment query with immediate garbage collection on unmount, no background/focus refetch and no ordinary record-cache reuse. Keep the URI available only while its setup screen is mounted; clear sensitive query/mutation results on exit/completion. Local state owns form/step interaction; TanStack owns request status. Do not log auth response bodies or send them to analytics.

The server retains the ten-minute enrollment window and five-attempt budget. The current enrollment response has no expiry timestamp: do not display a fabricated exact countdown. MFA completion alone unlocks the workspace. There is no new client-only enrollment cancellation/logout promise where the backend has no corresponding cookie-clearing endpoint.

**Gate:** a synthetic invitee activates, enrolls, reloads during setup, completes MFA and signs in again; cancelled/replayed links and revoked credentials fail safely. Owner bootstrap/recovery remains the established operational workflow.

## 10. Step 2.5 — Invitations and Staff

Use the existing Platform Access route and page entry where possible. The route remains thin; focused lists/forms/dialogs implement the feature. All API paths below are relative to `/api/v1/superadmin/auth`.

### Invitations tab

Show name/email, invitation status, separate delivery status, created/expiry timestamps and eligible actions. Search, invitation-status filter, sorting and pagination are URL-owned and server-backed.

| Action | API | UI contract |
|---|---|---|
| List | `GET /invitations` | Send normalized `limit, offset, search, status, sort_by, sort_order`; show the returned total. |
| Invite staff | `POST /invitations` | Name/email only. Confirm committed invitation and queued delivery; never claim mailbox receipt. |
| Resend | `POST /invitations/{id}/resend` | Only pending, live invitations; send expected version; explain that the previous link is replaced. |
| Cancel | `POST /invitations/{id}/cancel` | Live pending/enrolling invitations; required reason and confirmation; explain invalidation of applicable enrollment. |

Support statuses `pending`, `enrolling`, `accepted`, `cancelled`, `expired`; sort only by `created_at`, `email`, `expires_at`. Default limit 20, allowed limit 1–100, offset at most 100000, search at most 200 characters. Normalize unsupported URL values and reset page on search/filter changes. Show a legitimate empty result separately from loading/failure. If mutations shrink the last page, move to the nearest valid page without hiding errors.

Display delivery separately: queued, sending, retrying, sent, failed, superseded. **Sent means provider accepted**, not delivered/read. A failed delivery does not justify resetting a staff credential. Refetch after commands and allow explicit refresh; optional bounded polling runs only while relevant unsettled delivery rows are visible. Do not invent provider attempt counts or retry times absent from the DTO.

### Staff tab

Show name/email, Owner/Staff identity, Active/Inactive and supported timestamps only. Query `GET /staff` with `limit, offset, search, sort_order`; sorting is by creation date. The API does not provide a staff status filter or email/name sorting, so those controls are not part of this phase.

| Action | API | UI contract |
|---|---|---|
| Reset sign-in | `POST /staff/{id}/reset-sign-in` | Required reason/version; explain immediate loss of current access and required password/MFA setup. Eligible active or revoked non-owner staff only. |
| Revoke access | `POST /staff/{id}/revoke` | Required reason/version; warn about loss of access; honor server eligibility and keep the dialog open on failure. |

Owner rows have neither reset nor revoke through these APIs. Provisioning remains owner-only; there is no owner promotion or capability editor. `capabilities: []` is not a reason to block existing operators. `active: false` does not identify an exact inactive lifecycle; avoid labelling every inactive account as revoked or awaiting MFA.

### Commands, validation and conflicts

- Match server validation: trimmed name 1–255, email at most 255 with the server's supported normalization/format, trimmed reason 1–2000. Do not duplicate a subtly different identity-normalization policy; the server remains authoritative. Map `body.*` field errors to the form.
- Generate a UUID idempotency key per deliberate action and retain the exact body/key during transport uncertainty. All updates include the displayed `expected_version`. Disable repeated submission while pending; privileged actions are pessimistic.
- A successful replay may return an old committed snapshot. Refetch current invitations/staff and affected badge counts instead of treating the response as the latest list state.
- On `version_conflict`, refresh and explain the changed record, then require review before a new action. Never silently swap in a newer version or auto-repeat a destructive action.
- On an unknown network outcome, keep the same body/key for an explicit retry. Resolve or reconcile the prior action before allowing an edited submission with a new key. Do not silently mint a new key after a timeout.
- Handle validation, forbidden, missing record, invalid transition, idempotency conflict, rate limit and temporary failure distinctly. Preserve reason/draft on recoverable errors. Show a safe request reference when supplied.
- An existing-account collision is not a successful invitation. Existing staff use reset-sign-in; CRM users cannot be converted into platform staff through this form. Do not offer a reset unless a current eligible staff row is available.

The current invitation DTO has no purpose, target-user ID or enrollment-expiry field; Staff has no last-login field. Do not invent these columns, per-record detail endpoints or precise recovery labels from incomplete data.

**Gate:** owner completes create/list/search/page/resend/cancel/reset/revoke against the real test API; ordinary staff cannot access management. Concurrent updates and uncertain transport outcomes remain visible and recoverable.

## 11. Step 2.6 — Cutover and existing-page integration

1. Replace old request/operator management hooks and services where used by platform UI. Remove calls to retired public request-access, verify-email, review and legacy revoke writers. Retain backend historical reads only for their documented compatibility purpose.
2. Replace user-visible developer/DEV PORTAL terminology throughout platform entry, navigation, page titles, loading/error messages and associated translations. Keep internal technical module names unless a rename is needed for correctness.
3. Integrate overview, organizations/details, login history, trial extensions and feedback with the shared frame. Correct double-height/overflow containers caused by shell replacement; preserve functioning page actions. Their full internal redesign stays Phase 3.
4. Apply the session/query-key boundary to those pages so direct navigation, account switching and revocation cannot bypass protection. Do not migrate unrelated page state into Redux during this integration.
5. Test full and short aliases, refresh/deep links, owner-only direct URLs and sign-out return paths. The same route mapping drives navigation, active states and entry guards.
6. Preserve CRM registration, organization invitations, OAuth, MFA where applicable, password recovery and session check-in. Platform activation and management must not call those flows.

**Gate:** no rendered link leads to a retired workflow, no protected page appears before identity resolution, and all existing platform routes remain usable within the new frame.

## 12. Proposed file boundaries

These are intended boundaries; proposed names may be adjusted to fit the verified source tree. Do not create empty placeholders or duplicate existing implementations just to match this list.

| Existing area | Planned change |
|---|---|
| `src/components/layout/DashboardShell.tsx` and layout presentation | Extract a small `WorkspaceFrame.tsx` and only genuinely shared sidebar/header presentation; retain CRM wrappers/effects. |
| `src/app/superadmin/layout.tsx` | Thin composition around a client `PlatformSessionBoundary` and `PlatformWorkspace`. Keep public entry routes outside the protected workspace. |
| `src/components/superadmin/` | Platform shell/header/sidebar, typed navigation and focused Invitations/Staff components. Replace existing management/entry behavior rather than adding parallel versions. |
| `src/lib/api/platformHttpClient.ts` | Typed platform options/errors, cancellation, timeout and session-safe CSRF handling. |
| `src/services/` | Extend the current platform auth service; add focused access-management methods/types using the same client. |
| `src/hooks/queries/usePlatformAuth.ts` and existing platform hooks | Session boundary, identity-scoped keys, invitations/staff queries and focused command hooks; update legacy protected keys. |
| `src/hooks/usePlatformEntry.ts` | Login/activation/MFA coordination and sensitive-result cleanup; remove public application steps. |
| `src/lib/` / focused hooks | Platform query keys, route mapping, URL-state normalization and explicit formatting; no new generic framework. |
| `src/store/` | Register a small `platformUi` slice for shared platform preferences only. |
| `src/components/shared/table/`, `ConfirmModal.tsx` | Backward-compatible server pagination and controlled accessible async dialogs. |
| `src/i18n/`, message catalogs | Platform text and any narrowly necessary locale isolation; maintain existing translation contracts. |
| `src/proxy.ts` | Change only if route tests expose a real gap; preserve existing rewrite behavior. |
| `tests/` | Focused transport/state tests, browser workflows and actual-route visual/integration harness. |

## 13. Verification strategy

Use behavior-based checks for the material risks. Do not write tests that merely assert class-name strings or duplicate implementation branches.

| Risk | Required verification |
|---|---|
| Shared extraction breaks CRM | Before/after screenshots plus collapse/mobile, trial banner/lockout, onboarding, AI sizing, header and existing session-startup checks |
| Platform starts CRM effects | Browser network assertions on initial load, navigation, preference changes and logout |
| Endless/misleading session state | Never-resolving request, timeout, offline, connection reset, non-JSON 500, 401, 403 and retry recovery |
| Cached data crosses staff accounts | Delayed reads/mutations, logout/login, owner→operator switch, two-tab invalidation and revoked-session scenarios |
| Access management violates API contract | Headers, exact request bodies, owner negatives, server totals/page two, 409 conflicts and same-key retry after simulated lost response |
| Enrollment leaks or loses its lineage | Fragment removal, reload/resume, five-attempt/expiry behavior, cancelled/reset lineage, no storage/log/analytics exposure |
| Dialog/table compatibility breaks CRM | Existing client-pagination callers retain behavior; async failure stays open; focus trap/restore; keyboard sorting; disabled dismissal while pending |
| Shell looks similar only in mocks | Actual Next.js route captures with compiled CSS and loaded Instrument Sans, including both host forms |
| Provider isolation/formatting regresses | English/Dutch, explicit UTC/selected timezone, CRM preference preservation and no prohibited direct locale formatting |

Separate three levels of evidence:

1. **Focused service/hook tests:** typed errors, cancellation, parameter normalization, version/idempotency decisions and session-scope behavior. Use the existing node/assert + tsx approach.
2. **Functional browser tests:** extend `test:platform-auth:browser`; add focused workspace and access-management suites following the installed browser harness. If new named scripts are useful, register and document them before use; they do not exist yet. Mocked responses cover deterministic failures, not API integration or visual parity.
3. **Actual-route integration and visual checks:** run the Next application against an isolated backend/database with synthetic owner/staff accounts, fake Redis and fake mail delivery. Exercise cookie/origin/CSRF through the real proxy. Obtain test activation links through a fixture-only mechanism, never a production API/log. Capture the real CRM/platform routes at the reference widths, both sidebar modes and 200% zoom; wait for fonts and compare actual geometry/overflow as well as appearance. Never point a mutating browser suite at the normal application database.

The real-API owner→invitation→activation→MFA→staff-sign-in flow is required. Include reset/re-enrollment and revocation. Live SES/mailbox delivery is the Phase 6 release gate; fake delivery verifies Phase 2 workflow without API keys.

Run relevant existing checks from `crusource-crm-frontend/`:

```powershell
npx.cmd tsc --noEmit
npm.cmd run lint
npm.cmd run format:check
npm.cmd run test:platform-auth:browser
npm.cmd run test:session-startup:browser
npm.cmd run test:localization
npm.cmd run test:translations
npm.cmd run test:translations:browser
npm.cmd run test:invitations
npm.cmd run test:public:analytics
npm.cmd run build
```

Add targeted CRM shell/onboarding/AI and recovery checks when those boundaries change. Use the venv and affected test files for any backend change; do not run the entire backend suite casually or start Docker merely for unit tests. Record command results and pre-existing warnings separately. If build needs network-hosted font access, resolve the environment requirement instead of altering the design to force a pass.

After application code changes, run `graphify update .` from the orchestration root and verify load-bearing graph claims against source. Documentation-only planning does not require a graph update.

## 14. Completion and release gates

Phase 2 is complete locally only when all of the following are recorded:

- [ ] New platform shell visually matches the CRM reference with real CSS/font at all specified widths and zoom; no double scrolling or inaccessible mobile navigation.
- [ ] Owner creates, resends and cancels invitations and resets/revokes eligible staff through the real test API.
- [ ] Invitee activation, MFA setup/resume, sign-in and reset/re-enrollment succeed; invalid/cancelled/replayed flows fail correctly.
- [ ] Public access applications and developer terminology are gone from the platform experience; no UI calls retired writers.
- [ ] Session timeout/outage recovery, owner-only route/query gating, cache cancellation and account/tab transitions pass.
- [ ] Platform rendering produces no customer-session API requests and does not change CRM authentication or UI preferences.
- [ ] API pagination/filter/version/idempotency behavior and accessible pending/error dialogs pass.
- [ ] Required types, lint, localization, translation, browser/integration and production build checks pass or have explicitly documented pre-existing limitations. A missing required integration check blocks completion.
- [ ] Review screenshots and evidence clearly distinguish completed Phase 2 work from remaining Phase 3 page redesign and later features.

Produce `superadmin-phase2/README.md`, `ARCHITECTURE.md`, `VERIFICATION.md`, a screenshot index and a Phase 3 handoff. Record source revisions, changed files, commands/results, route/host matrix, known limitations and reproducible fixture setup. Update the phase-wise status only after these gates pass. Maintain the feature inventory's prescribed status vocabulary with wired UI/API evidence.

Production rollout remains coordinated with Phase 1 and Phase 6: deploy a compatible backend/frontend pair after environment, migration and live-delivery checks. Do not roll back to the old access UI against a backend whose writers return `410`. Preserve a known working UI that uses the new APIs, and keep CRM-frame changes small enough to revert independently. There is no Phase 2 database rollback because no schema change is planned.

The first implementation task is **2.0**, followed by **2.1**. The reviewable result of this plan is a visibly CRM-aligned, invitation-only staff portal with verified workflows and explicit failure handling; complete redesign of existing page contents begins in Phase 3.
