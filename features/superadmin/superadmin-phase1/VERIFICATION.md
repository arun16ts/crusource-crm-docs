# Phase 1 verification

9 October 2026. **Local backend phase complete. Production release remains gated by Phase 2/6.**

Starting backend revision: `33a6ff4ae16b13c25e04af516a402b38f3d1afd1`; frontend: `0276a54` (unchanged by Phase 1). Changes remain local for review. The pre-existing edit to `Superadmin login.md` was preserved.

## Recorded results

| Check | Result and limits |
|---|---|
| Phase 1 auth/invitation/delivery/migration/identity/guard suite | **78 passed**, 4 dependency deprecation warnings, 52.91 seconds |
| Required real PostgreSQL checks within that suite | **25 passed, none skipped**: 12 concurrency/auth races and 13 actual migration/error fixtures |
| Targeted CRM and existing Super Admin regressions | **61 passed**, 45 dependency deprecation warnings, 42.16 seconds |
| Combined distinct backend cases | **139 passed** across the two suites |
| Empty database upgrade | Entire Alembic chain through `20261009_platform_invitations` succeeded in disposable PostgreSQL 17 |
| Legacy upgrade/backfill | Actual Alembic operations passed for old schemas, repeat backfill, original activation/MFA resume, collision/lineage refusal and downgrade safety |
| Existing frontend platform browser suite | Passed against simulated API; covers existing sign-in/MFA/activation/cookie/session isolation. Its old approval/revoke fixture does not establish new management compatibility. |
| Existing frontend CRM session browser suite | Passed: startup, refresh, retries, bounded waits, outage recovery and revoked-session redirects |
| Router contract export | Generated `platform-auth.openapi.json`, 18 registered paths; no application startup/provider call |
| Backend whitespace | `git diff --check` passed |
| Graphify | Code-only graph update completed; extraction warnings for unavailable Terraform/HCL parser, five existing TSX parser cases and non-code JSON/TOML outputs. Graph is generated orientation, not verification truth. |

No application database was migrated. PostgreSQL checks used a separately named disposable container on loopback and an explicit `platform_phase1_test` database. Temporary schemas were uniquely prefixed and removed by fixtures. Credentials/encryption keys were synthetic. No real SES, Google or other provider call was made. The temporary database is stopped after verification.

## Reproduction

From `crusource-crm-backend`, supply an explicitly isolated local PostgreSQL URL for database `platform_phase1_test`, test-only runtime configuration, unreachable/fake Redis and disabled EC2 credential metadata. Never use an application database. PostgreSQL fixtures reject non-loopback hosts and a different database name before creating schemas.

```powershell
$env:ENVIRONMENT='test'
$env:PLATFORM_POSTGRES_TESTS='1'
$env:AWS_EC2_METADATA_DISABLED='true'
# Supply DATABASE_URL securely for the dedicated disposable local test database.
# Supply REDIS_URL for the local test/fake configuration.
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth.py tests/test_platform_invitations.py tests/test_platform_delivery.py tests/test_platform_auth_postgres.py tests/test_platform_invitation_races.py tests/test_platform_invitation_migration.py tests/test_platform_crm_identity_compatibility.py tests/test_superadmin_guard.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_auth_security_tokens.py tests/test_auth_concurrency.py tests/test_password_recovery_proofs.py tests/test_admin_bulk_invite_e2e.py tests/test_google_auth_and_documents.py tests/test_invite_url_resolution.py tests/test_superadmin_dashboard.py tests/test_superadmin_feedback.py tests/test_superadmin_login_history.py tests/test_superadmin_organizations.py -q
```

From `crusource-crm-frontend`:

```powershell
npm.cmd run test:platform-auth:browser
npm.cmd run test:session-startup:browser
```

The disposable race schema intentionally omits unrelated customer FKs. Actual migrations against old schemas and the full empty upgrade separately verify schema integration. This does not replace a staging restore of representative deployed data. The full backend suite and a new frontend production build were not run for this backend phase; Phase 0 already established frontend build/type/lint baselines and frontend source is unchanged here.

## Covered invariants

- Owner-only creation/list/manage; CRM identities cannot be promoted; owner cannot be reset/revoked through staff APIs. Origin, CSRF, forged fields, missing configuration and current session authorization fail safely.
- Invite → committed job → activation → pending session → MFA → authenticated staff; no account before activation and no protected access before MFA. Resume retains setup and limits; cancellation prevents resumed MFA.
- Same-key replay, different-body conflict, stale versions, duplicate invitation/idempotency races and transactional actor revalidation, including replay after session revocation.
- Reset of revoked staff uses explicit recovery, preserves identity and requires new MFA. Old sessions/links fail. Real activation versus resend/cancel, MFA versus reset/revoke and duplicate TOTP races assert final database/session invariants.
- Competing CRM identity creation cannot create a second normalized account. Positive customer registration/OTP/onboarding, international-domain identity matching, Google provisioning/link isolation and organization invitation regressions pass.
- Commit failures create no usable cookie, invitation, receipt or sendable job. Database errors and both PostgreSQL email constraints produce safe responses without credential parameters in logs.
- Provider timeout/uncertain/rejected outcomes, retry backoff/budget, expired invitations, abandoned leases, double dispatch, key rotation and payload cleanup. Real dispatch versus resend/cancel tests fence stale completion; obsolete tokens fail redemption.
- Actual legacy migration preserves passwords, encrypted secrets, counters, owner identity, approved digests and enrollment sessions. Both migrated link activation and original pending-cookie MFA complete without reissue. Repeated backfill is a no-op. Ambiguous case/whitespace/Unicode/CRM/owner lineage aborts safely; populated downgrade refuses data loss.
- Public application/verification/approval/old revoke endpoints return `410` without requests, invitations, jobs or email side effects. Compatibility imports are also retired.

## Discoveries and release limits

Python/PostgreSQL Unicode case mapping differs for some historical addresses. Migration preflight now explicitly detects both database and Python collision groups and mismatched results; remediation is required before a deployed migration can proceed. It does not rewrite CRM identities. New mailbox-local validation and IDNA transport follow [AWS SES SendEmail requirements](https://docs.aws.amazon.com/ses/latest/APIReference/API_SendEmail.html).

The backend is ready for Phase 2 UI integration, with SOLID/CQRS boundaries and a typed API handoff. Live SES inbox/bounce/complaint behavior, deployed restarts, secret-store key rotation, HTTPS/proxy controls, representative migration/runtime measurements and backup/restore remain Phase 6 gates. Passing tests reduce risk; they are not a guarantee of zero bugs.
