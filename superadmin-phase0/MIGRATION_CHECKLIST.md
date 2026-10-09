# Platform invitation migration checklist

Phase 0 design baseline, 9 October 2026. **No application migration or deployed-data backfill was executed.** This checklist is a Phase 1 implementation requirement and a Phase 6 release gate.

Phase 1 update: an empty full-chain upgrade and synthetic legacy upgrades/backfill were executed in disposable PostgreSQL. No application/deployed database was changed. See [verified results](../superadmin-phase1/VERIFICATION.md) and the [release runbook](../superadmin-phase1/RELEASE_RUNBOOK.md); the starting-state observations below describe Phase 0.

## Verified starting point

- Repository migration head: `20261008_webhook_receipts` (one head, `alembic heads`). This is repository state, not the deployed database revision.
- Existing platform tables originate in `alembic/versions/20261004_platform_auth.py`: credentials, access requests, sessions and security events. Preserve the partial unique owner index and the owner user id.
- Sources: [models](../../crusource-crm-backend/src/modules/platform_auth/repositories/models.py), [activation handler](../../crusource-crm-backend/src/modules/platform_auth/handlers/activate.py), [MFA handler](../../crusource-crm-backend/src/modules/platform_auth/handlers/verify_challenge.py), [review handler](../../crusource-crm-backend/src/modules/platform_auth/handlers/review_request.py), [repository](../../crusource-crm-backend/src/modules/platform_auth/repositories/repository.py).
- MFA completion currently finds the legacy request through the user's email. New invitation lineage must replace that dependency deliberately, with a compatible legacy branch during cutover.
- `User.email` and legacy request email have ordinary unique constraints. Repository lookups use case-insensitive comparison. Case-sensitive uniqueness can permit ambiguous identities; the synthetic inventory demonstrates this risk in the actual SQLite model schema. PostgreSQL collation/index behavior still requires verification.
- The [existing outbox](../../crusource-crm-backend/src/shared/services/record_effect_outbox.py) is organization/record scoped. Preserve it; add platform delivery separately.

## Safe rehearsal completed

[inventory-legacy.py](inventory-legacy.py) imports the actual application model registrations and uses the existing in-memory SQLite test engine. It forces unreachable synthetic application DB/Redis URLs before app imports and verifies that its working database is `sqlite:///:memory:`. It never opens a deployed database or invokes email delivery.

Generated [legacy-inventory.json](legacy-inventory.json) contains aggregate counts only:

| Fixture | Count / purpose |
|---|---|
| Users | 6 synthetic users; all organization-free |
| Owner credentials | 1; preserve identity and owner uniqueness |
| Active operator credentials | 1; preserve existing access |
| Inactive credentials | 2; one revoked user, one live enrollment with active user but inactive credential |
| Super Admin flag without credential | 2; must never gain access by backfill |
| Legacy requests | 10: unverified 1, pending 3, approved 3, enrolling 1, activated 1, rejected 1 |
| Approved activation links | 2 live, 1 expired; one live link has failed delivery |
| Normalized-email collision groups | 1 in users and 1 in access requests |
| Sessions | 5: active owner/operator, live enrollment, revoked and expired |

This rehearsal validates inventory coverage, not a future migration algorithm. No real account counts, raw tokens, hashes, encrypted MFA secrets or credentials appear in the report. Synthetic credential secrets are absent because the fixture inventories states; authentication behavior is exercised by the separate platform-auth tests.

## Before implementing the migration

- [ ] Start from the current single migration head; recheck before generating a revision because other features can advance it.
- [ ] Add a dedicated invitation model, platform delivery model, idempotency persistence and the minimum version/lineage fields needed for concurrency. Use explicit constraints/FKs/indexes and register all models in app initialization/tests.
- [ ] Keep application logic in CQRS handlers/repositories/services. Alembic performs schema/data changes without importing live application email/queue code.
- [ ] Define one normalized-email function and enforce consistent identity uniqueness for every identity writer. Rehearse a functional normalized unique index on `users` only after proving normalization/collation behavior, resolving every collision, and verifying CRM registration/invites/OAuth. Do not rely on a platform-only preflight SELECT: simultaneous CRM creation is also a race. Do not silently merge/delete CRM accounts to make the index succeed.
- [ ] Keep display email values stable unless an approved collision remediation explicitly changes them. A normalized constraint must protect future writes as well as migrated rows. Unresolved collisions make the migration stop safely with counts, not chosen winners.
- [ ] Add unique legacy lineage so backfill can be rerun without duplicate invitations/history. Expire live-state rows explicitly before creating replacement invitations; partial-index predicates must not depend on wall-clock time.
- [ ] Define and test a consistent lock order for invitation/legacy lineage, credential and session. Commands affecting the same principal must share it. Never acquire new row locks in an order that reverses activation/reset/MFA order.

## Legacy mapping

| Existing state | Required mapping / behavior |
|---|---|
| Owner user + credential | Preserve id, owner flag, activation state, encrypted MFA secret, replay counter and eligible sessions. No invitation required; no second owner created. |
| Active platform operator | Preserve user id, password/MFA, active credential and eligible sessions. Record accepted legacy invitation lineage where an activated request exists; no email sent by backfill. |
| Revoked/inactive operator | Preserve revocation and session invalidation. Never reactivate from an old request or `is_super_admin` flag. Require explicit owner reset/reissue for future recovery. |
| Legacy approved, valid token | Map to pending invitation with original digest and expiry intact. Maintain legacy activation read compatibility. Never rotate the token merely to migrate it. |
| Legacy approved, failed email | Preserve state/digest/expiry and failed delivery visibility. The original raw token is unavailable; do not manufacture a delivery payload from its hash. Owner resend rotates a fresh generation through the new outbox. |
| Legacy approved, expired token | Map to expired invitation/history. Do not extend validity or send email automatically. |
| Legacy enrolling + valid enrollment cookie | Link accepted user/pending session to invitation lineage; preserve password/MFA setup and allow the existing enrollment to finish. MFA completion updates new lineage atomically and compatible legacy state while needed. |
| Legacy enrolling + expired/no valid enrollment | Preserve audit history; mark recovery required/expired through reconciliation. Owner cancel/reissue/reset is explicit. Do not invent a usable session. |
| Legacy pending/unverified | Archive as legacy applications. No staff access, no automatic invitation and no email. Owner may issue a fresh invitation intentionally. |
| Legacy rejected | Retain rejected history; no invitation or access automatically created. |
| Ambiguous email, CRM-owned identity, flag without credential, orphan/mismatched lineage | Stop or quarantine the affected identity for remediation; no privilege grant, account transfer or implicit merge. |

Compatible old links last no longer than their original 48-hour expiry; pending sessions last their original 10 minutes. Track actual outstanding expiry maxima rather than adding an arbitrary new compatibility window. Keep legacy history read-only until an independently reviewed retention/removal migration.

## Implementation and rehearsal gates — Phase 1

- [ ] Test upgrade against an empty database, the synthetic state matrix and a sanitized representative PostgreSQL snapshot. Run backfill twice and compare row counts, lineage, state and digests.
- [ ] Prove unchanged owner/operator login and MFA replay protection before and after migration. Confirm revoked/expired sessions remain unusable.
- [ ] Prove old valid links and live enrollment complete once, with new lineage updated. Expired/replayed/cancelled links fail safely.
- [ ] Use dedicated PostgreSQL test configuration for concurrent invite-vs-invite, invite-vs-CRM identity creation, resend-vs-activate, activate-vs-cancel, enrollment-vs-revoke and reset-vs-MFA. SQLite is insufficient.
- [ ] Inject commit failure: no delivery job becomes dispatchable and no message is sent. Restart the worker during lease/send; duplicate mail cannot make stale/replayed tokens valid.
- [ ] Verify constraint/conflict failures produce stable safe API responses and do not leak account details publicly. New successful creation cannot accept owner/org/capability fields from the client.
- [ ] Disable public request-access/verify-email writes and old approval/reset writes at coordinated cutover. Retired routes return a clear non-writing response (410 with staff-invitation guidance); remove public application links in Phase 2.
- [ ] Ensure only one active writer design during rollout: old approval/resend cannot run alongside new invitation mutations without the shared transaction/lock protocol. A feature flag alone is not database-level protection.

## Deployment inventory and rollback gates — Phase 6

- [ ] On the actual target database, record revision/head alignment, account/state counts, collision counts, orphan counts and maximum outstanding link/session expiry. Export counts and opaque issue references only, without token/secret/PII fields.
- [ ] Verify backup restoration, migration runtime/locks, key availability and decryptability, SES configuration, trusted browser origins, exact CRM/platform domains and scheduler/worker deployment. Never rotate MFA encryption keys incidentally.
- [ ] Pause privileged writes and drain/lease-protect delivery during the schema/backfill deployment. Deploy the compatible API before enabling new UI writes; remove the old public entry points as part of that coordinated release.
- [ ] Smoke-test owner login, existing operator login, new invitation, interrupted enrollment, resend, cancel, recovery and revoke using designated staging accounts. Customer CRM invitations/OAuth/trial/subscription flows must still pass.
- [ ] Roll back application code only to a compatibility build that understands new invitation state, revocations and sessions. Freeze invitation writes/delivery if needed; keep additive tables/history. Do not re-enable the old public application/approval writers automatically.
- [ ] After new-format writes occur, do not downgrade/drop new tables or restore a stale account snapshot as routine rollback. A destructive restore needs a separately reviewed recovery procedure that preserves revoked credentials and identifies mail already accepted by the provider.
- [ ] Observe delivery failures, stale jobs, MFA failures and enrollment completion during a limited rollout. Remove compatibility branches only after all original links/sessions expire and their scenarios pass again.

Phase 0 is complete with this safe inventory and explicit mapping. Production revision/counts, concurrency and deployed delivery remain later-phase gates, not implied successes.
