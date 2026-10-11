# Super Admin Phase 4 implementation plan

Date: 11 October 2026. Status: **COMPLETE — local implementation and verification, 4.0 and 4A–4F.** See the [review package](superadmin-phase4/README.md), [implemented contracts](superadmin-phase4/CONTRACTS.md), [verification](superadmin-phase4/VERIFICATION.md) and [Phase 5 handoff](superadmin-phase4/PHASE_5_HANDOFF.md). Deployed/provider acceptance remains Phase 6.

The sections below preserve the approved execution plan. The review package records final decisions: read-only assignee lookup supports filtering; preferred windows are bounded text with an IANA timezone; shared business notifications retain their own outbox alongside invitation delivery. No application database migration, push, deployment or real mail was performed.

This execution companion expands Phase 4 of [the phase-wise roadmap](SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md), using [the master plan](SUPERADMIN_MASTER_UPGRADE_PLAN.md), [Phase 0 design contracts](superadmin-phase0/CONTRACTS.md) and [the Phase 3 handoff](superadmin-phase3/PHASE_4_HANDOFF.md). Phase 3 is complete locally according to its review package; deployed verification remains separate. Current source takes precedence over historical design contracts.

## 1. Outcome and scope

A visitor submits an English or Dutch demo enquiry, receives a truthful acknowledgement after database commit, and authorized platform staff see it in a working sales board/list. Staff can assign it, record notes, schedule a demo, set follow-ups and move it through tracked stages. All changes survive reload and concurrent changes produce visible conflicts.

Deliver in this phase:

- Persisted public demo intake, actual website entry points and abuse protection.
- Owner-managed sales capabilities, enforced on the backend and frontend.
- Board/list, filters, request detail, assignment, scheduling, follow-up, notes and immutable activity.
- Durable internal notifications and truthful delivery states.
- Reconciliation of the billing Contact Sales modal's current simulated submission.
- Additive migrations, focused regression tests, full applicable CI and a review package.

Customer support is Phase 5; deployed operational acceptance is Phase 6. Configurable pipelines, calendar booking/invitations, attachments, automated reminder campaigns, CRM lead conversion, account provisioning and paid-revenue attribution are outside this phase. Follow-ups are stored dates and overdue indicators initially, not a promised reminder service.

## 2. Verified starting point

Reviewed local commit IDs: frontend `00008920`, backend `ec6a67f`, docs `be78fd9`. Record working-tree changes again at implementation start; these IDs identify the reviewed checkout, not deployment evidence.

| Source                                                                                        | Finding                                                                                      | Implementation consequence                                                                      |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `superadmin-phase3/PHASE_4_HANDOFF.md`                                                        | Shared frame, session isolation, URL state, bounded reads and guarded commands are available | Extend these foundations rather than rebuilding authentication or the CRM shell                 |
| Frontend `src/components/landing/PublicPageShell.tsx`                                         | Public shell includes marketing navigation, footer and public AI chat                        | Use it for the form; check that chat/analytics never receive form contents                      |
| Frontend `src/proxy.ts`                                                                       | Locale middleware handles `/`, `/nl` and `/nl/*`; Super Admin hosts rewrite short paths      | Add and verify real localized route entries; test public and platform hosts separately          |
| Frontend `src/components/billing/ContactSalesModal.tsx`                                       | Submission only sets local state and displays an unsupported 24-hour promise                 | Replace simulated success with a real sales enquiry flow                                        |
| Frontend `src/lib/platform/routes.ts`                                                         | Host-aware platform links already exist                                                      | Support both `/superadmin/demo-requests` and short-host `/demo-requests`                        |
| Backend `platform_auth/services/sessions.py`                                                  | Platform session, origin and CSRF checks are implemented                                     | Preserve them; add explicit sales authorization                                                 |
| Backend `platform_auth/services/owner_command.py`                                             | Commands revalidate identity under the platform security lock and commit receipts atomically | Add capability revalidation before receipt replay or mutation; preserve owner-only provisioning |
| Backend `platform_auth/repositories/invitation_models.py` and `handlers/dispatch_delivery.py` | Delivery requires invitation ID/generation and sends activation links                        | Demo notifications cannot be inserted into this table unchanged                                 |
| Backend `src/shared/security/rate_limiter.py`                                                 | Shared Redis admission and explicit outage policies exist                                    | Reuse shared admission with a demo-specific namespace and deliberate production outage policy   |
| Focused application source search                                                             | No demo-request module/routes or sales capability implementation found                       | Treat these as new behavior; recheck source and router registration before creating files       |

Graphify was queried for feature relationships; the findings above were verified in source. The Phase 0 contracts are design inputs, not evidence that demo endpoints exist.

## 3. Decisions to carry into implementation

Use the following defaults to make work actionable. Record any material change in the contract package before dependent implementation.

1. **Capability names:** use `demo.read` and `demo.manage`, matching Phase 0 typed contracts. The roadmap's `view_demo_requests`/`manage_demo_requests` are descriptive equivalents, not additional permissions. Manage implies read. Owner has implicit authority; existing and newly invited staff receive no sales grants by default.
2. **Granting:** owner edits sales grants for existing staff on Access Management. Granting capabilities during invitation is optional later work; it is not needed to make Phase 4 usable. Preserve existing invitation/reset/revoke authority.
3. **Public receipt:** `202` after genuine accepted intake commits. The response contains a neutral acknowledgement and opaque reference, without echoing entered PII or exposing a public lookup. Email failure never changes a committed enquiry into a failed submission. Obvious honeypot submissions receive a neutral response without creating a lead; rate limits and unavailable protection return explicit retryable errors.
4. **Retry window:** proposed 24-hour idempotency retention. Same key and normalized payload replay the original result; different payload with the same key returns `409`. New keys allow genuine repeat enquiries. Do not make email globally unique.
5. **Delivery:** add a focused shared business-notification outbox following existing adapter, lease, retry and scheduler conventions. Keep invitation token/generation delivery intact. Factor only genuinely reusable dispatch mechanics; do not weaken invitation invariants or build a general messaging framework.
6. **Billing enquiry:** persist through an authenticated CRM endpoint that delegates to the same intake use case. Derive requester/organization context from CRM Scope, use `enterprise_sales` as its enquiry type and trusted `crm_billing` source. Demo pipeline staff visibility follows the same capabilities. This requires a real company field or validated organization-name mapping in the modal.
7. **Privacy:** record contact-purpose acknowledgement, server timestamp and notice version; do not bundle marketing opt-in. Final public copy, sales recipients and retention duration are release inputs. No legal-compliance claim follows from this plan.

## 4. Delivery order and review boundaries

| Package | Deliverable                                                         | Dependency      | Exit evidence                                                                              |
| ------- | ------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| 4.0     | Source baseline, contracts, wireframes and test plan                | Phase 3 handoff | Route/locale/host decisions and schema/authorization contracts recorded                    |
| 4A      | Capability persistence, owner API/UI and identity/cache integration | 4.0             | Owner grant/revoke works; no-grant/read-only/manage cases and live-session revocation pass |
| 4B      | Demo persistence, shared notification delivery and intake APIs      | 4A contracts    | Commit, retry, abuse, notification-failure and migration tests pass                        |
| 4C      | Staff query/command APIs and workflow                               | 4A + 4B         | Real PostgreSQL races, query/count parity and transition rules pass                        |
| 4D      | Public EN/NL form, links and billing modal integration              | 4B contracts    | Actual route submission persists; validation/failure/retry and marketing regressions pass  |
| 4E      | Staff board/list/detail and workflow UI                             | 4C contracts    | Per-column loading, URL state, permissions and real route/API flows pass                   |
| 4F      | Integrated acceptance, complete CI and Phase 5 handoff              | 4A–4E           | Reproducible evidence and explicit local/stage limits recorded                             |

These are review boundaries, not one large implementation change. Run focused checks while iterating and complete applicable repository CI after each implementation before calling it ready for stage. Do not infer calendar estimates from phase numbers; estimate after 4.0 identifies the actual changes and blockers.

## 5. Package 4.0 — contracts and baseline

- Record nested repository branches/commits, dirty files, migration head and current workflow commands. Preserve existing edits and application data.
- Trace landing Navbar/MarketingNavbar, Hero, Footer, PricingSection, PublicInformation/contact and billing modal call sites. Identify every actual entry point and its locale behavior.
- Produce wireframes for public form/success/error, desktop board, list, mobile stage view and detail/actions. Reuse public marketing presentation and Phase 3 CRM-aligned platform components respectively.
- Reconcile Phase 0 DTOs with scheduling fields, source/date filters, capability revisions, activity pagination and board cursors. Publish one authoritative Phase 4 contract with examples and error codes.
- Define input limits, admission limits, receipt retention, supported team-size values, timezone validation, notification recipients and retention configuration. Proposed input bounds: name/company 200 characters, email 254, phone 40, message 4,000 and request body 16 KiB; verify consistency with shared validators.

## 6. Package 4A — platform sales authorization

Persist staff grants and a capability revision with database constraints; capability changes and their platform security audit entry commit together. Owner-only grant changes require expected version and operation ID. Avoid granting sales access through CRM roles or the legacy superadmin flag.

Extend platform identity and staff projections with effective capabilities/revision. Enforce `demo.read` on every demo query and `demo.manage` on every command. Revalidate grants inside the security transaction before replaying a receipt or changing a record. Use a consistent lock order: platform security authority, then demo aggregate; document it for future support commands.

Access Management shows a narrow sales grant editor. Navigation and queries wait for identity and use the effective grants. A revoked capability removes protected caches, cancels in-flight requests and closes privileged detail/actions. On `403`, refresh identity and clear affected data. Revalidate identity on window focus and a bounded interval so already-open tabs respond to grant changes; API denial is immediate regardless of UI refresh.

Assignment candidates must be active, authenticated-eligible platform staff with `demo.manage`, or the owner. Existing assignments to subsequently revoked/ineligible staff stay visible with an eligibility warning; new assignments fail. No silent reassignment or historical actor deletion.

## 7. Package 4B — persistence, intake and notifications

Create a focused `src/modules/demo_requests/{commands,queries,handlers,repositories,routes,services}` module. Register prefixed routers in `src/main.py` and models in application initialization, Alembic metadata and `tests/conftest.py`.

| Persistence                | Required content                                                                                                                                                                                                                                                      |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DemoRequest`              | UUID/reference, bounded contact/company fields, team size/message, enquiry type, trusted source/context, locale, privacy acknowledgement/version/time, stable stage, disposition, assignee, scheduled time/timezone, follow-up, optimistic version and UTC timestamps |
| `DemoRequestActivity`      | Immutable action, actor or system origin, timestamp, before/after values and bounded reason; creation and operational changes recorded                                                                                                                                |
| `DemoRequestNote`          | Plain text body, author, timestamp; append-only in v1, separately paginated                                                                                                                                                                                           |
| Public intake receipt      | Unique operation key, canonical payload digest, minimal response, expiry; separate from actor-required staff receipts                                                                                                                                                 |
| Shared notification outbox | Event/template and recipient identity, deduplication key, bounded payload, lease/fencing, attempts, due time, safe failure code and provider result                                                                                                                   |

Use additive migrations with stable constraints/indexes. Index stage/disposition/order, assignee and follow-up; verify source/date/search access patterns on PostgreSQL before adding speculative indexes. Use deterministic timestamp/ID ordering. Preserve records/history when staff deactivate; define foreign-key behavior explicitly.

Public intake accepts only lead fields, locale and contact acknowledgement. Never accept stage, assignee, CRM organization IDs or trusted source claims. Validate timezone-aware preferred windows; explain they are preferences, not bookings. Reject unknown fields and render customer text as plain text.

Enforce request size before full JSON parsing, bounded field validation, honeypot and shared admission. Proposed configurable starting limits: 5 attempts per IP per 10 minutes and 3 accepted new requests per normalized-email digest per hour; tune against legitimate shared-network traffic. Use trusted proxy IP extraction, not arbitrary forwarding headers. Configure fail-closed shared admission in stage/production; show a retryable `503` rather than silently disabling protection. Local tests use fake Redis; concurrency admission tests use disposable Redis.

Uniqueness/transaction handling must resolve simultaneous submissions into one authoritative receipt and lead. Creation, initial activity, receipt and configured notification intents commit atomically. Provider calls run after commit. No committed success on database failure; rollback leaves no sendable intent. Retrying after a lost response is safe within the receipt window.

Staff notifications contain a minimal reference and protected configured-host link, not full contact/message contents. Require approved eligible recipients; queue no mail to arbitrary public input. Customer email acknowledgement is disabled by default in v1. Expose queued/sent/failed internal delivery state to managers without leaking provider internals. Test lease expiry, worker restart, retry deduplication and configuration failure. Document that provider acceptance is not proof of inbox delivery and a crash can cause repeated email.

## 8. Package 4C — staff APIs and workflow

Paths below are relative to `/api/v1`; frontend services must not duplicate that prefix.

| Endpoint                                                                                  | Authorization/behavior                                                                                                                  |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `POST /public/demo-requests`                                                              | Anonymous protected intake; `202` only after accepted persistence, except documented neutral bot response                               |
| `POST /demo-requests/sales-enquiries`                                                     | Proposed CRM authenticated intake; Scope-derived context, no platform-session requirement; verify subscription-expiry policy explicitly |
| `GET /superadmin/demo-requests`                                                           | `demo.read`; bounded list or a single stage's cursor page                                                                               |
| `GET /superadmin/demo-requests/counts`                                                    | `demo.read`; all-stage counts using identical filters except pagination/stage                                                           |
| `GET /superadmin/demo-requests/assignees`                                                 | `demo.manage`; bounded minimal eligible staff projection                                                                                |
| `GET /superadmin/demo-requests/{id}`                                                      | `demo.read`; detail and permitted contact data                                                                                          |
| `GET /superadmin/demo-requests/{id}/notes` and `/history`                                 | `demo.read`; independent bounded pagination                                                                                             |
| `POST .../{id}/stage`, `/assignment`, `/follow-up`, `/schedule`, `/disposition`, `/notes` | `demo.manage`; distinct typed versioned commands and operation IDs                                                                      |

Register static routes before `{id}`. Capability administration belongs to owner-only platform access endpoints; finalize their shapes in 4.0. Add a schedule command because scheduling/rescheduling must be supported without forcing a stage change.

Support search over bounded name/company/email fields, stage, disposition, assignee/unassigned, enquiry type, source and created-date range. Implement filters once in repositories and reuse them for list, column pages and counts. Search is authorized and never logged with raw PII. Counts return every fixed stage, including zero. Do not filter/sort already-paginated data again in React.

Fixed stage progression:

`New → Contacted → Qualified → Demo Scheduled → Demo Completed → Follow-up → Converted`

| Action                        | Rule                                                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Adjacent forward move         | Allowed for normal nonterminal records; scheduled stage additionally requires a future scheduled time                                      |
| Skip forward or move backward | Require reason; validate target-specific prerequisites                                                                                     |
| Enter Demo Scheduled          | Require timezone-aware scheduled time strictly after server command time, supplied atomically or already stored                            |
| Reschedule                    | Future timezone-aware timestamp, expected version and audited change; no calendar event is created                                         |
| Converted / Not Proceeding    | Terminal; require reason, preserve history; no customer/account/subscription side effects                                                  |
| Reopen terminal record        | Only to Contacted, with reason                                                                                                             |
| Same stage                    | No-op after authorization/version validation; no duplicate activity                                                                        |
| Spam disposition              | Separate from stage, reason required; hide by default and exclude from normal counts; block operational changes until restored with reason |
| Follow-up                     | Nullable timestamp; clear explicitly; show past dates as overdue, retain original timezone for entry/display                               |

Every effective mutation increments aggregate version and writes activity in the same transaction; notes also increment parent version. Define the note/activity relationship to avoid duplicated note text in audit storage. Validate expected version under a PostgreSQL lock or compare-and-update, then commit receipt/history/entity together. A losing command returns `409` without partial changes. Receipt replay occurs before stale-version rejection but after current authorization checks.

## 9. Packages 4D/4E — public and platform UI

Public: implement `/request-demo` and a verified Dutch route, proposed `/nl/request-demo`, using existing locale conventions. Add actual links from navigation, hero, footer, pricing/contact. Keep signup/sign-in available. Use clear labels, field errors, privacy-purpose copy and a success state that promises receipt rather than a booked appointment or response deadline. Preserve one operation ID across uncertain retries; use a fresh ID for a new enquiry. Keep PII drafts out of URLs, localStorage, analytics and public AI context.

Billing: replace local-only submission with a focused service/hook using CRM transport and trusted context. Add company validation/mapping and truthful success/error/pending states. Remove the 24-hour promise. Preserve modal keyboard/focus behavior and current billing navigation.

Platform: add thin route entries for `/superadmin/demo-requests` and a deep-linkable detail route `/superadmin/demo-requests/[id]`. Use shared header, buttons, table, dialogs, sidebar and EN/NL platform messages. Use `platformHref` for short-host compatibility and platform transport for every protected request.

- Board/list toggle and normalized filters/sort/list pagination belong in URL state; changing filters resets pagination. Detail route preserves a safe return view.
- TanStack Query owns entities, mutations, history and counts. Keys include staff identity, capability revision and every response-affecting filter/cursor. No server records in Redux.
- Board loads each column independently, initially 20 cards with cursor-based Load more; counts show all matching records. Display loaded/total and per-column error/retry states. A single global list page must never populate the whole board.
- Cards show company/requester, eligible/ineligible assignee, stage age, created age and next follow-up. Stage age comes from persisted stage-entry data/history, not `updated_at` changed by a note.
- Use existing `@dnd-kit` where suitable, with a keyboard-accessible Move to stage action executing the same command. Reason/schedule dialogs precede required transitions. Prefer pessimistic movement in v1; disable duplicate actions while pending and refetch affected columns/counts/detail/history on success or conflict.
- Detail includes permitted contact information, preferred window, confirmed staff-recorded schedule, assignment, follow-up, notes, activity and manager-only notification status. Separate preferred contact windows from scheduled demos visually.
- Read-only staff see no write controls; denied deep links and direct API requests fail. Do not offer exports in v1 without a separate privacy/authorization contract.
- Preserve data during failed refresh with a visible warning; initial failure cannot look like an empty pipeline. Provide independent loading, empty, invalid-filter, conflict and permission-loss states.
- Verify 1440/1024/768/390px layouts, real fonts/CSS, focus containment/restoration, keyboard navigation and mobile usability. Use a stage selector/mobile column view where a wide board would clip cards.

## 10. Verification and completion gates

Add proposed backend test groups for demo intake, queries/commands, capabilities, notification delivery and PostgreSQL races/migrations. Register opt-in race tests in Backend CI; tests that always skip are not a completion gate. Add frontend Node/tsx contract tests and browser tests in the established repository style, plus actual Next.js route/FastAPI integration using synthetic identities. Register portable new regressions in Frontend CI; sibling-backend integration remains an explicitly documented additional check.

Required focused evidence:

- Accepted form → database record → authorized board → assignment → scheduled demo → stage change → history after reload.
- Concurrent same-key intake creates one record; changed-payload replay conflicts; different-key legitimate repeat is accepted. Rollback sends no email; lost response is safely retried.
- Anonymous/CRM bearer/no-grant staff cannot read platform PII; read-only staff cannot mutate; non-owner cannot grant access; revoked sessions/grants fail commands and receipt replay.
- Grant/revoke versus assignment/mutation races, two managers moving one request, spam/restore races and assignment eligibility changes are exercised on PostgreSQL.
- Date/source/search/assignee filters agree across board, list and counts; columns load independently without duplicates or omitted same-timestamp records in a stable dataset. Counts/pages are independent snapshots; refresh affected queries after writes rather than claiming a globally atomic board snapshot.
- Scheduling timezone/DST validation, overdue follow-ups, terminal/reopen rules, required reasons, plain-text note rendering and scheduling/receipt retries pass.
- Notification outage/restart leaves the lead intact, receipt truthful and duplicate dispatch bounded. Public receipt, errors, logs and analytics contain no entered PII.
- EN/NL routes, host aliases, deep links, back/forward, auth expiry, grant changes, mobile/keyboard actions, loading/empty/error/refresh failure and billing behavior pass.

After every implementation run the affected repository's complete applicable CI from its current workflow. Cross-repository work requires both. Current frontend baseline uses Node 20 and backend Python 3.12; confirm again before running.

Frontend: clean lockfile installation, changed-file formatting with correct `FORMAT_BASE_SHA`, full lint, `npm run test`, spreadsheets, Loop/public contracts, `npx tsc --noEmit`, **every browser command currently listed in CI**, production build with test-only API/OAuth values and dependency audit. Additionally run platform auth/session/frame and public pages/analytics regressions relevant to these changes. Use `npm.cmd`/`npx.cmd` on Windows.

Backend: dependency files and venv, Ruff over `src tests scripts alembic`, compileall, committed migrations on disposable PostgreSQL, full pytest, required shared Redis, webhook/production PostgreSQL, recovery/startup/import PostgreSQL, platform invitation/trial PostgreSQL groups, new demo/capability/delivery groups, migration drift on a separate empty database and `alembic check`. Verify one migration head, clean upgrade and upgrade from the current supported revision, preservation of invitations/staff/customer data and documented rollback limits. SQLite does not establish race or migration safety.

Do not migrate/seed application, stage or production databases for tests. Record exact check results, existing failures and blockers; never promote focused passes into full-CI claims. After code changes run `graphify update .`; documentation-only planning needs no graph refresh.

## 11. Release boundaries, recovery and handoff

Local Phase 4 completion requires the real synthetic end-to-end flow, full applicable verification and reviewable artifacts. Stage acceptance additionally requires exact successful-CI backend image/commit, matching frontend deployment, schema revision and migration logs, correct proxy/origins/CSRF/cookies, real configured Redis and a controlled provider notification. A ready health endpoint alone is insufficient.

Before any promotion perform the complete cross-stack deployment audit required by AGENTS.md, including deployment gating, secrets injection, worker execution, CloudWatch/Vercel logs and existing sign-in/refresh/onboarding/invited-user/permission/settings regressions. Run the migrator with `SKIP_MIGRATIONS=false` and `python scripts/run_migrations.py` before API rollout; verify the deployed revision against image heads. Deploy additive schema → compatible backend → frontend. Phase 6 retains integrated real-provider/customer/support release verification.

Recovery should disable new intake/notifications or roll back compatible UI/API while preserving lead data, activity and restrictive permissions. Do not drop populated tables as a routine rollback. Do not restore public staff applications. Rehearse invitation delivery compatibility after introducing shared business notifications.

Produce `superadmin-phase4/README.md`, authoritative API/architecture contracts, migration/recovery notes, verification results, screenshot index, notification/retention configuration notes and `PHASE_5_HANDOFF.md`. Phase 5 should reuse capability evaluation/revision and business notifications, while retaining separate support models and customer Scope.

Update the roadmap and feature inventory only to the evidence-supported state, using its exact status vocabulary. Distinguish local fixtures, actual local route/API integration and deployed verification. Planning does not authorize emails, provisioning, push or deployment.

**Phase 4 is complete when a real accepted test enquiry persists, authorized staff can manage it through the board with durable history, privacy/authorization/concurrency checks pass and all required local checks are accounted for. A form toast or mocked board alone does not meet this boundary.**
