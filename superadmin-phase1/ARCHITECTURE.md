# Phase 1 architecture decisions

9 October 2026. Source is authoritative; paths below are relative to `crusource-crm-backend`.

## CQRS and responsibility boundaries

`src/modules/platform_auth/invitation_routes.py` validates typed commands/queries, delegates to one handler per use case and normalizes safe errors. Repositories construct SQL. Focused services own identity normalization, authorization/transaction orchestration, lifecycle transitions, encryption and mail delivery. Existing `routes.py` includes the new router, retaining its registered `/api/v1/superadmin/auth` prefix.

`PlatformInvitation` holds lifecycle and legacy/user lineage. `PlatformDelivery` holds one encrypted delivery intent per invitation/generation. `PlatformCommandReceipt` holds a committed response for an actor/action/resource/key. Credential administrative versions change for enrollment/reset/revocation, independently of routine login/TOTP/last-seen bookkeeping.

## Serialization and authorization

All platform security transactions acquire PostgreSQL transaction advisory lock `(187202610, 1)` before row locks. This deliberately serializes a small internal staff domain. SQLite has no equivalent guarantee; real PostgreSQL tests supply concurrency evidence.

| Writer | Lock and transaction sequence |
|---|---|
| Guard | Advisory lock → credential → session → current user/lineage; commit last-seen |
| Owner command | Advisory lock → re-read actor/session/owner authority → receipt → target credential/invitation/session/job → event/receipt → commit |
| Activation/MFA/login | Advisory lock → current identity/invitation/credential/session → consume/update/create → commit → cookie |
| Reset/revoke/server recovery | Advisory lock → current credentials → invitation/session/job invalidation → event → commit |
| Delivery claim/completion | Advisory lock → job/invitation → lease/fenced result → commit |
| Delivery provider call | No database transaction or lock held |

The shared advisory lock precedes every platform row-lock sequence, preventing lock-order inversions between these writers. It does not serialize CRM writers. The functional unique index `uq_users_normalized_email` on `lower(trim(email))` prevents a competing CRM writer from creating the same normalized user. If CRM creation wins, activation conflicts safely and cannot promote that account. This index changes global identity uniqueness deliberately; collision preflight is mandatory.

The guard commits before handlers execute. Owner commands therefore reauthorize inside their own transaction, including idempotent replay. A previously authorized response object cannot grant authority after logout/recovery. API dependencies retain origin/custom-header/CSRF admission; handler authorization is an additional current-state check.

This coarse lock favors correctness over throughput. Measure lock waits before expanding to larger support/demo workloads; those features must not automatically acquire this lock for every record operation.

## Identity compatibility and supported mailboxes

`services/identity.py` centralizes platform `strip().lower()` normalization. Existing CRM registration, OTP/password recovery, Google callback and organization invitation writers already normalize email; their journeys are not rewritten. The migration independently freezes its normalization logic rather than importing mutable application code.

Actual PostgreSQL testing found that Python lowercasing `İ` produces `i` plus a combining dot, while the database produces `i`. Preflight rejects existing whitespace, duplicate Python/database keys and differing normalization results before schema changes. It never chooses a winner, rewrites CRM email values or prints the affected addresses. Remediate ambiguous legacy records under a reviewed data change before deployment.

New invitations require an ASCII mailbox local part because SES does not support SMTPUTF8. International domains remain in the same normalized Unicode spelling produced by CRM EmailStr validation; the SES adapter encodes the domain using IDNA only when sending. Do not store a second punycode identity representation. Stable legacy internationalized identities are preserved; delivery to unsupported legacy mailbox names requires operational remediation. Unicode display names remain supported.

## Enrollment and recovery

Non-owner pending sessions bind to invitation UUID, generation and target user. A live enrolling invitation plus inactive credential and encrypted secret is required, independent of the user's old active flags. This permits authorized recovery of revoked staff while blocking ordinary login until MFA succeeds. Owner bootstrap remains a controlled exception without invitation lineage.

Cancellation, reset, revoke and expiry invalidate the applicable sessions/tokens and supersede jobs. Resend is restricted to a live pending invitation; accepted/enrolling staff require explicit reset or enrollment resume. New invites cannot convert existing CRM identities or recover existing staff implicitly.

Migrated legacy digests are redeemed through the invitation table. There is no fallback to old approvals after cancellation. Backfill binds existing enrollment sessions without changing their attempt counters, secrets or expiry.

## Durable delivery and confidentiality

Invitations, delivery intent, security event and idempotency result commit atomically. No SES call occurs within an owner command. The scheduler polls every 30 seconds, reconciles expiry/receipts and considers at most 25 jobs. Dispatch is serial per scan, within the approved maximum of five sends; each lease is claimed immediately before its send.

Leases last two minutes. The SES client uses five-second connect/ten-second read timeouts and one SDK attempt. Application retries stop after six attempts or invitation expiry; backoff starts at one minute, grows by five, caps at four hours and adds up to 20% jitter. Retryable provider errors and uncertain results retry; permanent rejection is terminal. Lease tokens fence stale completion. A crashed worker is reclaimed after lease expiry.

Redemption stores only token digests. Delivery material is Fernet-encrypted using a dedicated key/id, separate from MFA. Terminal/superseded/expired jobs clear material. DTOs and receipts contain no hashes, credentials or activation URL. Platform route database failures emit a safe request id without logging SQL parameters. Global normalized-identity conflicts return safe `409` responses.

Provider acceptance is `sent`, not proof of mailbox delivery. A crash after acceptance can duplicate mail; a resend/cancel racing an in-flight call can still deliver an obsolete email. Generation/state checks guarantee its obsolete token cannot grant access.
