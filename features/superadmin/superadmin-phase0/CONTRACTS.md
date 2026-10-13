# Phase 0 implementation contracts

9 October 2026. **Design baseline for later phases; these endpoints are not live.**

Phase 1 implementation update: staff endpoints now exist in the local backend. Use the [Phase 1 API handoff](../superadmin-phase1/API_HANDOFF.md) and generated OpenAPI for the implemented contract, including enrollment resume, explicit recovery of revoked staff and supported mailbox validation. Demo/support contracts below remain designs. This file preserves the Phase 0 baseline.

The executable DTO definitions are [contracts.py](contracts.py); generated schemas are [contracts.schema.json](contracts.schema.json). The schemas specify request/response shapes. Authorization, state transitions, idempotency, persistence and delivery below are additional mandatory handler requirements. Passing DTO checks does not prove those behaviors.

## Architecture and state ownership

Use Next.js App Router with thin page entries and Server Components by default. Put browser session interaction in focused client boundaries. Do not fetch protected platform-cookie data from Server Components until forwarding, cache isolation and authorization are explicitly designed. Follow the installed Next.js documentation rather than older middleware examples; this application uses `src/proxy.ts`.

| Concern | Owner | Implementation rule |
|---|---|---|
| API transport | `src/services/*`, existing authenticated clients | Platform calls use `platformHttpClient`; CRM support uses `fetchWithAuth` through existing CRM client. Relative paths exclude `/api/v1`. |
| Server records and mutations | TanStack Query, focused hooks | No fetched records, list results or mutation responses in Redux. Include authenticated identity, effective capability revision, tenant where applicable and all response-affecting parameters in keys. |
| Shared UI preferences | Redux Toolkit | Platform sidebar/collapse/drawers only; namespace platform preferences separately from CRM. |
| Filters, search, sort, pagination, selected view | URL/search parameters | One focused hook parses/validates defaults and updates via App Router. Reset offset on filter changes. Do not mirror in Redux. |
| Form draft, dialog pending state | Component state | Keep local; clear on success or explicit discard. Show failure without closing privileged dialogs. |
| Backend reads | Queries → one-use-case handlers → repositories | Scoped persistence and projection belong in repositories; read routes authorize and delegate. |
| Backend writes | Commands → one-use-case handlers → repositories/services | A transaction owns entity change, history/security event, idempotency result and delivery intent. Integrations run after commit. |
| Cross-cutting checks | Existing shared guards/services | Preserve Scope, record access, CRM subscription behavior and platform origin/CSRF rules. Do not introduce unscoped fallback queries. |

Apply SOLID through narrow components, service methods, DTOs and focused handlers. Reuse established boundaries and validators. Avoid a generic workflow framework for these three different domains. Register every new prefixed router explicitly in `src/main.py` and every model in application initialization and `tests/conftest.py`.

Proposed key shapes:

```ts
['platform', staffId, capabilityRevision, 'invitations', normalizedParams]
['platform', staffId, capabilityRevision, 'demo-requests', normalizedParams]
['platform', staffId, capabilityRevision, 'demo-column', stage, normalizedParams]
['platform', staffId, capabilityRevision, 'support-tickets', normalizedParams]
['crm', userId, orgId, 'support-tickets', normalizedParams]
['crm', userId, orgId, 'support-ticket', ticketId, 'messages', cursor]
```

Gate queries until identity is resolved. Remove protected platform caches on logout, authentication loss and identity changes; cancel in-flight queries so late responses cannot restore old-account data. Invalidate affected detail, list, board count and history keys after mutations. Prefer pessimistic privileged writes; board drag may use a scoped optimistic update with rollback and refetch on `409`. Retries of writes reuse the same idempotency key.

## Shared API conventions

- JSON uses snake_case, UUID identifiers and timezone-aware ISO 8601 UTC timestamps. Body/URL identifier shapes must be validated before persistence.
- Schemas forbid unknown body fields. Trim surrounding whitespace; required strings reject whitespace-only input. Names/company: 1–255 characters; email: validated, maximum 255; reason: 1–2,000; ticket subject: 1–200; notes/messages: 1–10,000; demo message: at most 2,000; phone: at most 32, optional and never used as identity. Render stored text as text, without interpreting HTML.
- Normalize invitation emails with `strip().lower()` using one shared function. Do not rewrite CRM emails in a platform migration. Check collisions across users, invitations and legacy requests; a CRM identity is never automatically promoted to platform staff.
- Offset list envelope: `{items, total, limit, offset}`. Defaults: limit 20, offset 0; limit 1–100; offset 0–100,000; search at most 200 characters. `total` is the server's count after the same filters/authorization. Sorts are enumerated; add UUID as the stable tie-breaker. Never sort or paginate only the loaded page in React.
- Messages use `{items, next_before_id, has_more}` with default limit 30, maximum 100. Resolve `before_id` inside the already-scoped ticket; use `(created_at,id)` keyset ordering and return each page chronologically. A customer cursor cannot refer to an internal note. Counts/cursors must not reveal hidden messages.
- Every command updating an existing aggregate requires `expected_version >= 1`. Lock/recheck the row or use a conditional update, then increment exactly once on a successful change. No-op writes return the current aggregate without a version increment. Validation/authorization/conflict failures change nothing.
- Every create/write command requires `Idempotency-Key: <UUID>`. Store a request hash and committed response in the same transaction, scoped by authenticated principal, endpoint/use case and resource. Anonymous demo submission uses endpoint + key. Same key/body replays the committed result; different body gives `409 idempotency_conflict`. Keep successful results at least 24 hours; retain client keys for retries. Reauthorize before replay. Keys do not replace rate limits or optimistic versions. One transaction wins simultaneous duplicate keys through a unique constraint.
- Errors use `ApiError` for new endpoints: `code`, safe `message`, `request_id`, optional `current_version`, `field_errors`. Do not globally change existing APIs. Map 401 authentication, 403 capability/owner, 404 missing/out-of-scope resource, 409 version/idempotency/transition conflict, 422 invalid fields, 429 admission limit with `Retry-After`, 503 unavailable. No SQL, secrets, token fragments or provider messages in responses.
- Error bodies must be integrated with the frontend error parser; keep existing transport token-refresh behavior. Owner-only/capability guards run on every relevant handler, including lists and history, regardless of navigation visibility.

## Staff invitations — Phase 1

Provisioning remains **owner-only**. Owner bootstrap/recovery remains an operational workflow; no public endpoint creates an owner. Existing active operators retain current access during migration. Future demo/support capabilities are explicit and default-deny for non-owners; owners have all platform capabilities. Capability administration is a separate owner-only use case in Phase 4; creation of a staff invitation cannot set `is_owner`, organization, password or capabilities.

All paths below are relative to `/api/v1`. Existing login/activation/MFA/session transport stays under `/superadmin/auth`.

| Method/path | Request → response | Authority/transaction |
|---|---|---|
| POST `/superadmin/auth/invitations` | `InviteStaff` → 202 `Invitation` | Owner; create pending invitation + delivery intent. |
| GET `/superadmin/auth/invitations` | `InvitationQuery` → `InvitationPage` | Owner; filtered, bounded list. |
| POST `/superadmin/auth/invitations/{id}/resend` | `ResendInvitation` → 202 `Invitation` | Owner; rotate generation/token for pending invitation. |
| POST `/superadmin/auth/invitations/{id}/cancel` | `CancelInvitation` → `Invitation` | Owner; cancel pending/enrolling and invalidate related sessions. |
| GET `/superadmin/auth/staff` | `PageQuery` → `StaffPage` | Owner; include active/revoked states without secret fields. |
| POST `/superadmin/auth/staff/{id}/reset-sign-in` | `ResetStaffSignIn` → 202 `Invitation` | Owner; explicit recovery intent, revoke sessions, clear usable sign-in credentials and create new enrollment generation atomically. |
| POST `/superadmin/auth/staff/{id}/revoke` | `RevokeStaff` → `Staff` | Owner; revoke sessions/invitations and deactivate. Prevent owner self-revoke/last-owner loss. |

Use a dedicated invitation table with immutable lineage to legacy request and accepted user where applicable, explicit `version`, `generation`, normalized email and hashed activation token. Partial uniqueness permits at most one pending/enrolling invitation per normalized email. Expiry must materialize the terminal state before a new invite can be created; never use `now()` in a partial index predicate. Accepted/cancelled history is retained. Validate eligible identity under transaction/constraints, not solely with a preflight SELECT.

| Current state | Permitted action | Result |
|---|---|---|
| none | Owner invite | pending; token valid 48 hours; delivery queued |
| pending, unexpired | Resend | pending; increment generation, rotate token and 48-hour expiry; obsolete old delivery jobs |
| pending, unexpired | Redeem token with valid password | enrolling; consume link; create 10-minute enrollment session |
| enrolling, live | Complete valid non-replayed MFA | accepted; activate credential; issue authenticated session |
| pending or enrolling | Cancel | cancelled; invalidate token/enrollment sessions and supersede delivery |
| pending past link expiry; enrolling past enrollment expiry | Expiry reconciliation | expired; require owner-issued new enrollment |
| accepted | Resend | 409; use explicit reset-sign-in |
| expired or cancelled | Resend | 409; owner creates a new invitation with new lineage |
| enrolling | Resend | 409; resume enrollment or cancel and reissue |

Preserve valid **legacy** interrupted enrollment behavior during the bounded compatibility window. The new stricter lifecycle must not silently invalidate an already-issued legacy enrollment. Failed delivery is a separate delivery status; it does not grant access or change invitation state. Do not deactivate an existing active user merely because a pending invitation expires.

Preserve current password validation/hashing, mandatory encrypted TOTP secret, replay protection, five-attempt pending challenge limit, 10-minute pending session, four-hour full session with 30-minute idle expiry, host-only HttpOnly cookie, SameSite Strict, secure cookie in staging/production, origin admission, `X-Platform-Request` and CSRF checks. CRM bearer tokens cannot authorize platform routes. Invitation token is sent in the URL fragment, consumed in the activation client and removed from browser history; no token in analytics, logs or GET query parameters. Activation/MFA request DTOs and response shapes must remain compatible with the current auth service during the Phase 1 migration.

## Reliable delivery

`202` means **stored and queued**, never confirmed email receipt. The UI displays delivery status and the invitation state separately. A successful provider call means provider acceptance, not mailbox delivery.

The existing `RecordEffect` outbox in `src/shared/services/record_effect_outbox.py` requires organization/module/record ownership and domain authorization. Add a focused platform-delivery outbox rather than loosening its invariants. Follow its scheduler/retry conventions. A platform invitation, security event, idempotency response and delivery intent commit together; no provider call inside that transaction.

Persist the token hash for redemption and authenticated-encrypted short-lived mail material for delivery; never plaintext. Dispatch must verify invitation id, current generation/state and expiry, claim with a lease, retry transient failures with bounded backoff and mark permanent failure safely. A crash after provider acceptance can cause a duplicate email; exactly-once delivery is not promised. Duplicate mail cannot permit token reuse. Expiry/cancel/reset supersedes stale jobs. Clear encrypted material when sent, superseded or expired according to a documented retention job. Do not persist/render activation URLs in staff list DTOs.

Use an explicitly configured encryption key and key identifier with an operational rotation procedure; retain compatible decryption keys for live sessions/secrets. Do not derive a new incompatible key during migration. Database failure leaves neither a committed invitation nor sendable delivery job. Real SES, bounce behavior, key rotation and worker restart are Phase 6 release checks.

## Demo requests — Phase 4

The public form submits only lead fields, locale and consent. Identity, owner, stage, disposition, timestamps and history are server-owned. Capture the server's consent timestamp and privacy notice version. Do not expose applicant email existence or record details through public receipt lookup. Admission uses request-size limits, rate limits and a honeypot; suspicious submissions receive a neutral acknowledgement without polluting the board. Genuine accepted submissions persist before success. Never discard legitimate repeat requests by email alone; idempotency handles transport retries.

| Method/path | Request → response | Access |
|---|---|---|
| POST `/public/demo-requests` | `SubmitDemo` → 202 `DemoReceipt` | Anonymous, rate-limited; no cross-site credentials required. |
| GET `/superadmin/demo-requests` | `DemoQuery` → `DemoRequestPage` | `demo.read` |
| GET `/superadmin/demo-requests/counts` | `DemoQuery` excluding pagination/stage → `DemoCounts` | `demo.read`; one total per stage. Register before `{id}` route. |
| GET `/superadmin/demo-requests/{id}` | → `DemoRequest` | `demo.read` |
| POST `/superadmin/demo-requests/{id}/stage` | `MoveDemo` → `DemoRequest` | `demo.manage` |
| POST `/superadmin/demo-requests/{id}/assignment` | `AssignRecord` → `DemoRequest` | `demo.manage`; eligible active staff only |
| POST `/superadmin/demo-requests/{id}/follow-up` | `SetDemoFollowUp` → `DemoRequest` | `demo.manage` |
| POST `/superadmin/demo-requests/{id}/disposition` | `SetDemoDisposition` → `DemoRequest` | `demo.manage`; audited reason |
| POST `/superadmin/demo-requests/{id}/notes` | `AddDemoNote` → `DemoNote` | `demo.manage`; increment parent version, invalidate/refetch detail. |
| GET `/superadmin/demo-requests/{id}/notes` | `PageQuery` → `DemoNotePage` | `demo.read` |
| GET `/superadmin/demo-requests/{id}/history` | `PageQuery` → `HistoryEntryPage` | `demo.read` |

Stages are `new → contacted → qualified → demo_scheduled → demo_completed → follow_up → converted`; `not_proceeding` is also terminal. Staff may move among nonterminal stages, but skipping forward/backward requires a reason; the adjacent forward move does not. Entering `demo_scheduled` requires a timezone-aware scheduled time, strictly after command time, supplied now or already stored. Entering a terminal stage requires a reason. Reopening a terminal stage is allowed only to `contacted` with a reason. Moving to the same stage is a no-op. Past follow-up dates remain visible as overdue; nullable follow-up explicitly clears it.

`spam` is an audited disposition independent of stage; hide it by default. A spam request cannot be moved/assigned until restored to normal with a reason. Marking spam supersedes its operational reminders. Converting does not create an organization/account, subscription or CRM user.

The board uses the same filtered backend query for each stage, bounded pages and server counts. Add a counts endpoint/projection for all stages with the same authorization/filter set rather than loading every lead. Drag/drop and a keyboard-accessible stage selector execute the same command. Stage changes increment the aggregate version and append immutable history in the same transaction; failed/conflicting moves roll back the UI and refetch affected columns. Board ordering is created_at/id initially; manual ranking is outside v1.

## Support tickets — Phase 5

CRM customers may submit and read **their own tickets in their current organization**. Resolve requester and organization from the authenticated session; neither is accepted in customer requests. Organization administrators receive no automatic access to other users' tickets. Support remains available during trial/subscription expiry through an explicit support-route/API exception that still requires a valid active CRM identity and organization. It must not grant access to unrelated modules.

Platform `support.read` can inspect the queue/public conversations/internal notes. `support.manage` can assign, reply, add internal notes and change states. Manage implies read; guard and capability revision updates are atomic. Cross-tenant platform access never uses a CRM token. Deactivated staff cannot remain eligible for new assignments; existing assignments remain visible until explicitly reassigned.

| Method/path | Request → response | Scope |
|---|---|---|
| POST `/support/tickets` | `CreateTicket` → 201 `CustomerTicket` | Current user + current organization; create ticket and first public message together. |
| GET `/support/tickets` | `CustomerTicketQuery` → `CustomerTicketPage` | Same scope; server filters. |
| GET `/support/tickets/{id}` | → `CustomerTicket` | Same scope; otherwise 404. |
| GET `/support/tickets/{id}/messages` | `MessageQuery` → `CustomerMessagePage` | Public messages only, filtered before pagination/count. |
| POST `/support/tickets/{id}/replies` | `ReplyToTicket` → `CustomerTicket` | Same scope; message + status/version change together. |
| POST `/support/tickets/{id}/reopen` | `ReopenTicket` → `CustomerTicket` | Same scope; explicit reason/history. |
| GET `/superadmin/support/tickets` | `PlatformTicketQuery` → `PlatformTicketPage` | `support.read`; org/assignee filters server-side. |
| GET `/superadmin/support/tickets/{id}` | → `PlatformTicket` | `support.read` |
| GET `/superadmin/support/tickets/{id}/messages` | `MessageQuery` → `PlatformMessagePage` | `support.read`; public + internal. |
| POST `/superadmin/support/tickets/{id}/replies` | `ReplyToTicket` → `PlatformTicket` | `support.manage`; always public reply. |
| POST `/superadmin/support/tickets/{id}/internal-notes` | `AddInternalNote` → `PlatformTicket` | `support.manage`; immutable internal visibility. |
| POST `/superadmin/support/tickets/{id}/assignment` | `AssignRecord` → `PlatformTicket` | `support.manage`; eligible active staff only. |
| POST `/superadmin/support/tickets/{id}/status` | `ChangeTicketStatus` → `PlatformTicket` | `support.manage` |
| POST `/superadmin/support/tickets/{id}/reopen` | `ReopenTicket` → `PlatformTicket` | `support.manage` |
| GET `/superadmin/support/tickets/{id}/history` | `PageQuery` → `HistoryEntryPage` | `support.read` |

Customer serialization uses its own DTO/projection. It must exclude internal note bodies, authors, identifiers, counts, cursors, assignee identities and internal audit details. There is no client-supplied `visibility` switch for customer replies; public replies and internal notes are distinct commands. No general message edit/delete in v1; never mutate an internal note into a public reply.

| Trigger | Permitted transition |
|---|---|
| Create | open |
| Staff begins work/replies to open ticket | open → in_progress |
| Staff status command | open → in_progress/resolved; in_progress → waiting_customer/resolved; waiting_customer → in_progress/resolved; resolved → closed |
| Customer public reply | open stays open; in_progress stays in_progress; waiting_customer/resolved → in_progress |
| Reply to closed | 409; explicit reopen first |
| Explicit customer or staff reopen | resolved/closed → open, with reason |
| Staff internal note or assignment | status unchanged; version/history still change |

Resolving/closing requires a reason. Staff replies to resolved/closed tickets require reopening first; replies to waiting_customer leave its status unless a separate explicit status command follows. Future notification jobs contain identifiers and recipient-safe public content only; no internal-note email. Use the durable delivery boundary, rate-limited retries and templates without claiming email delivery on mutation success.

V1 includes text conversations, categories, status, assignment, history, filters and bounded pagination. Attachments, inbound email, SLA timers, chat, user impersonation and automatic organization creation are outside this delivery. Keep links to Error Center issues explicit and capability-checked; customer support is not automatic error ingestion.

## Implementation acceptance checks

1. Phase 1: migration/backfill idempotence; single-owner preservation; old/new activation lineage; PostgreSQL concurrent invite/resend/activate/cancel/reset/revoke; failed commit means no send; stale generation never delivers usable old link; CRM/platform identity separation.
2. Phase 2/3: same actual CSS/font, desktop/tablet/mobile and 200% zoom; keyboard navigation; real async failure; identity/capability cache reset; no CRM-session requests from platform shell; URL back/forward and server list totals.
3. Phase 4: accepted form appears on board; public abuse admission; idempotent retries; simultaneous stage edits produce conflict; bounded columns and count consistency; reload preserves notes/assignment/follow-up/history.
4. Phase 5: customer A cannot read/reply/cursor-page customer B's ticket, within or across organizations; internal notes absent from every customer payload/count/notification; trial-expired support works without unlocking other modules; reply/status/reopen races are atomic.

Provider keys and production configuration are unnecessary for Phase 0. Phase 6 validates actual PostgreSQL, SES, deployed domains, workers and recovery before release.
