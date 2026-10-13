# Phase 1 migration and release runbook

9 October 2026. This is the future operational procedure. Local rehearsals used a disposable PostgreSQL database and generated test keys. Production rollout, live SES and deployed worker checks remain Phase 6 gates.

## Configuration

| Name | Requirement |
|---|---|
| `DATABASE_URL` | Intended application PostgreSQL database; confirm deployment target separately |
| `SUPERADMIN_MFA_KEY` | Preserve the existing Fernet key; migration must not rotate it |
| `SUPERADMIN_DELIVERY_KEY` | Dedicated Fernet key for delivery material, supplied through secret storage |
| `SUPERADMIN_DELIVERY_KEY_ID` | Current delivery key id, default `v1`, at most 80 characters |
| `SUPERADMIN_DELIVERY_PREVIOUS_KEYS` | JSON mapping old key ids to decrypting keys while outstanding jobs exist |
| `SUPERADMIN_FRONTEND_URL` | Platform origin only, no path/query/fragment/userinfo; HTTPS in production/staging |
| `ENVIRONMENT` | Correct production/staging setting for secure cookies and HTTPS validation |
| SES configuration | Existing `AWS_REGION`, `AWS_SES_FROM_EMAIL`, verified sender/identity and runtime AWS permissions |
| Redis/runtime | Existing Redis rate admission, application scheduler and normal backend configuration |

No secret values belong in documentation or process arguments. Generate delivery keys through the deployment secret manager. Never reuse the MFA key as a delivery key. Preserve previous delivery keys until their last outstanding jobs expire or terminate; the decrypting key id is stored per job. Missing/invalid delivery encryption or invalid platform origin blocks queue-producing commands with safe `503`, code `delivery_not_configured`, and no partial invite/reset. Phase 2 displays that known configuration failure directly; timeout/connection/other server failures retain the original action key/body for safe recovery. Restart or reload the backend after changing environment configuration.

The existing application scheduler automatically registers `platform_delivery_outbox` every 30 seconds. It is database-backed, independent of `QUEUE_MODE=sync`. There is no separate deployment flag in this change: pause all application instances/schedulers during migration and use the deployment maintenance/route controls to hold new privileged writes until smoke checks finish. Do not assume stopping `src/worker.py` alone pauses dispatch. Multiple API schedulers respect database leases; one active scheduler remains the simplest operational setup.

## Before migration

1. Review compatible backend and Phase 2 frontend together. Old access-management writes return `410`; an API-only deployment would leave the old owner UI unusable.
2. Confirm current Alembic head and database target. Expected parent is `20261008_webhook_receipts`; new head is `20261009_platform_invitations`. Reconcile any deployment drift before proceeding.
3. Inventory aggregate counts of owners, active/inactive operators, legacy statuses, live enrollments and normalized user/request collisions. Review opaque problem references in a restricted operator session. Never export credential/hash/email dumps to reports.
4. Run the actual migration on a representative restored staging database. Preflight stops on whitespace, duplicate Python/database normalized keys, differing Unicode collation, or ambiguous credential/legacy ownership. Remediate through reviewed data changes; do not silently merge or delete identities.
5. Take an encrypted consistent backup and rehearse restore with current credentials/revocations/history. Measure migration runtime, index lock duration and advisory-lock waits on representative volume. Local empty/fixture timings are not production estimates.
6. Confirm the exact HTTPS platform origin, trusted proxy/rewrite behavior, secure cookies, SES sender/runtime role, preserved MFA key and delivery keyring. Verify the deployed scheduler can reach PostgreSQL and SES.

## Cutover

1. Announce maintenance and pause privileged writers and every scheduler/API process. Drain in-flight work; stop the old approval/resend/revoke handlers from executing during schema/backfill.
2. From `crusource-crm-backend`, with the approved production configuration already supplied securely, run:

   ```powershell
   .\.venv\Scripts\python.exe -m alembic current
   .\.venv\Scripts\python.exe -m alembic upgrade head
   ```

3. Confirm the new head, new constraints/tables and aggregate backfill counts. No migration email should exist. Verify original owner id, active operator credentials, token digests and live enrollment session expiry/attempts remain intact, without printing their values.
4. Deploy compatible backend and Phase 2 frontend. Keep maintenance controls on queue-producing owner actions while checking owner login/MFA, existing operator access, legacy activation/resume, CRM signup/invite/OAuth and strict cross-auth isolation. Recheck no second old-format writer is running.
5. Enable privileged actions and dispatcher. Send a synthetic authorized staging invitation first; observe queued → provider accepted and complete password/MFA. Verify reset/revoke/cancel and an interrupted enrollment. Confirm retired endpoints produce no writes/mail.
6. Monitor delivery backlog/oldest age, retry/terminal failures, stale leases, identity conflicts, normalized-constraint errors, scheduler failures and auth failures. A provider-accepted message is not proof of mailbox delivery; verify SES bounce/complaint handling and inbox behavior separately.

Backfill is rerunnable by unique legacy-request lineage. It does not generate replacement credentials, extend links/sessions or send email. Pending/unverified/rejected public applications remain archived in the legacy table without invitation/access. Approved valid digests become pending; expired requests become expired history; active completed staff become accepted; revoked staff remain cancelled; eligible live enrollment retains its original session. Ambiguous CRM/owner lineage aborts the migration transaction. Keep legacy tables until separately reviewed removal.

## Failure and rollback

Before new-format use, an **empty** invitation schema can downgrade in rehearsal. Alembic refuses downgrade whenever any invitation lineage exists, including migrated history, because dropping it could erase revocation/enrollment authority. A populated migration rollback means restoring the rehearsed pre-cutover backup only before writes are enabled, under maintenance.

After invitations/revocations have been used, keep additive tables, authoritative lineage and current credentials/history. Pause queue-producing writes/delivery if necessary and deploy a compatible application rollback. Never re-enable old public approvals, drop populated invitation tables or restore a stale credential snapshot as routine recovery. Review any required data repair separately.

A worker crash before send leaves a reclaimable two-minute lease. A crash after provider acceptance can resend the same message after reclaim. Fenced completion cannot overwrite a newer lease/generation. Cancellation during a provider call may still allow an obsolete email to arrive, but redemption/MFA must reject its invalid lineage.

## Remaining release gates

Phase 6 must verify live SES permissions/sandbox status, rejection/bounce/complaint behavior, real inbox delivery, process restart across deployed schedulers, key rotation in secret storage, production-origin cookies/CSRF, backup restore and realistic migration/lock/runtime measurements. These checks are not replaced by local fake-provider or disposable PostgreSQL results.
