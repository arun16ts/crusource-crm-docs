# CRM Targeted Security Remediation Plan

**Status:** Local implementation applied; validation is in progress/completed as recorded below. No deployment is represented as complete.  
**Date:** 2026-10-22  
**Scope:** `crusource-crm-backend/` and `crusource-crm-frontend/`; documentation maintained in `crusource-crm-docs/`.

## Goal

Address the selected, source-confirmed security and reliability findings while preserving normal local development and user workflows. Each change must be implemented and verified in its owning application repository before promotion. This plan is not evidence of a deployment or a guarantee that the whole application is secure.

## Scope decisions

### Included in the next implementation

1. Fail closed when S3-backed document version/binary writes fail; never return a local-storage success in a protected environment.
2. Require a short-lived, one-time email OTP step-up before changing a user's MFA preference.
3. Disable public IP assignment for ECS migration tasks launched into the configured private subnets, after validating required private-subnet egress and service access.
4. Fail migration startup/release checks unless Alembic has exactly one intended head; remove exception-text fallback to `upgrade heads`.

### Tracked as a separate security project

Browser access and refresh tokens currently use `localStorage` in the CRM frontend. Retain this as a known residual risk and plan a separately reviewed BFF/secure-session migration. Do not combine a broad authentication architecture migration with the four targeted changes above. The separate project must cover token issuance/refresh, CSRF, cookie flags, session revocation, cross-origin deployment, compatibility/rollout, and removal of legacy storage.

### Explicitly excluded by the user

The DevOps-owned Terraform findings concerning tracked Redis credentials, production use of the RDS master credentials, and production secrets supplied as ECS environment values are excluded from this implementation scope. The owning infrastructure team should track and resolve them in its configuration path; this plan does not validate their remediation.

## Source basis

The plan was checked against the current CRM source and deployment workflow:

- `crusource-crm-backend/src/modules/documents/services/document_storage_service.py`: `save_bytes()` catches S3 upload errors and writes to local disk. Its `uses_s3()` independently checks environment names and omits `stage`. The shared `src/shared/security/environment.py` canonicalizes `stage` to `staging` and exposes `is_protected_environment()`.
- `crusource-crm-backend/src/modules/documents/handlers/version_handlers.py` and `update_binary_content_handler.py`: both call `save_bytes()` before committing document metadata, so storage failure must abort the request and database transaction. A later DB commit failure can leave an unreferenced S3 object and should be handled as a safe cleanup/operations concern.
- `crusource-crm-backend/src/modules/user/routes/user_routes.py` and `src/modules/user/handlers/security_preferences_handler.py`: the current authenticated PUT directly changes `mfa_enabled` and commits without a step-up challenge.
- `crusource-crm-backend/.github/workflows/deploy-stage.yml` and `deploy-production.yml`: migration tasks use subnet variables named `PRIVATE_SUBNET_IDS` while passing `assignPublicIp=ENABLED`.
- `crusource-crm-backend/scripts/run_migrations.py`: catches a failed `upgrade head`, infers multiple heads from exception text, then upgrades `heads`.
- `crusource-crm-frontend/src/lib/auth.utils.ts` and `src/lib/api.ts`: access and refresh tokens are read/written in `localStorage`; this remains deferred as described above.

Source paths are implementation evidence, not a claim that any environment has the same topology or has deployed these files.

## Implementation sequence

### Phase 0 — Baseline and contracts

1. Record the starting status of the CRM frontend and backend repositories and preserve unrelated working-tree changes.
2. Read each repository's current CI workflow and tests relevant to document storage, MFA, and migrations before editing.
3. Confirm storage configuration on local, stage, and production: `ENVIRONMENT`, `STORAGE_BACKEND`, bucket, IAM/task role, encryption, and whether deployed runtime uses task-role credentials. Do not print credential values.
4. Have the infrastructure owner verify the actual migration-task subnets, route tables/NAT or VPC endpoints, security-group egress, and access to ECR, CloudWatch Logs, Secrets Manager/SSM, and the database. A variable named `PRIVATE_SUBNET_IDS` alone does not prove the subnets are private or correctly routed.
5. Confirm current Alembic revisions and one intended head from the source tree. The release check must fail if a merge has introduced multiple heads.

**Gate:** Do not alter stage/production networking until the task's required egress and dependencies have been demonstrated. Do not use production databases for migration tests.

### Phase 1 — Fail-closed document storage

1. Change `DocumentStorageService` to use the shared `is_protected_environment()` policy rather than its own environment-name list. Ensure `stage` is treated as protected through canonical environment normalization.
2. In protected environments, require S3 and reject `STORAGE_BACKEND=local`; do not silently select local disk when S3 is unconfigured or unavailable. Keep local disk available only for explicitly supported local/development configuration.
3. In `save_bytes()`, propagate S3 upload failures. Remove its local fallback. Avoid raw provider details in client responses; log a structured server-side error with a request/correlation identifier and return an appropriate temporary storage failure response (normally HTTP 503).
4. Ensure callers do not commit document version/binary metadata after storage failure. On DB commit failure after a successful S3 upload, attempt a best-effort deletion of the newly created, unreferenced object or record it for cleanup; never remove an object that could be referenced by another committed version.
5. Review all paths that consume `local:` references and all document write paths, including streaming uploads and binary replacement, to ensure protected environments cannot create mixed local/S3 references. Preserve local development behavior.

**Acceptance criteria:** injected S3 failures cause a failed request and no metadata commit; no local file is created in protected environments; `ENVIRONMENT=stage` and `staging` both enforce S3; explicitly selecting local storage in protected environments fails at startup or on first service use with a clear operator error; normal local storage and successful S3 versioning still work.

### Phase 2 — Step-up for MFA preference changes

1. Replace the direct preference mutation flow with a two-step challenge/confirm flow. Bind each challenge server-side to the authenticated user, requested target state, and a dedicated purpose; never accept a client-supplied email destination.
2. Require the current email OTP as step-up for every state transition (enabling as well as disabling), so disabling MFA is protected against a stolen access token and enabling confirms the mailbox can receive login codes. If product policy later chooses a lower-friction enable path, document that decision separately; disabling must remain step-up protected.
3. Reuse the existing OTP delivery infrastructure only after verifying its storage and semantics. Store only a verifier/hash, use a cryptographically secure code, short expiry, single use, bounded attempts, resend throttling, and atomic consume/confirm behavior. Isolate this purpose from login, password reset, and account verification challenges.
4. Apply `mfa_enabled` only after valid confirmation. A challenge must not change the setting, and wrong, expired, replayed, or cross-user challenges must not change it. Avoid leaking user existence or challenge state in responses.
5. Add audit events for challenge requested, confirmed, expired/failed, and preference changed without logging OTPs or tokens. Keep the user's current authenticated session active unless a separate, explicit session policy requires revocation.
6. Update the settings UI and translations to request/send/confirm the code, prevent duplicate submissions, show expiry/retry feedback accessibly, and leave the existing preference unchanged on cancellation or failure.

**Acceptance criteria:** a valid fresh OTP completes the intended change; no access-token-only request can disable MFA; OTPs expire, cannot be replayed, are attempt-limited, and cannot be used for a different user or purpose; concurrent confirmation cannot consume one challenge twice; the UI handles delivery/rate-limit/expiry errors without falsely displaying a changed setting.

### Phase 3 — Private networking for migration tasks

1. After Phase 0 network validation, change `assignPublicIp=ENABLED` to `DISABLED` in both CRM stage and production migration-task workflows.
2. Confirm the migration task security group permits only required outbound traffic and database ingress is restricted to the task security group. Verify NAT or suitable VPC endpoints cover image pulls, logs, secrets, and other runtime dependencies.
3. Run the stage deployment/migration flow and verify task placement in the intended subnets, successful image pull, secret retrieval, database connection, migration logs, and clean task exit. Confirm failure propagates to the workflow and blocks API rollout.
4. Promote the same reviewed change to production only after stage evidence and approval. If a separate Terraform service definition is authoritative for migration tasks, have its owner reconcile the networking there; do not assume workflow edits affect Terraform-managed task launches.

**Acceptance criteria:** ECS migration tasks launch without public IPs in the intended private subnets, retain only required egress, complete migrations, and fail the deployment job if they cannot start or migrate. A successful health endpoint alone is insufficient evidence.

### Phase 4 — Fail-closed Alembic head enforcement

1. Before connecting/upgrading, inspect the migration graph with Alembic's `ScriptDirectory` and require exactly one head. If the count is zero or greater than one, log the safe revision identifiers and terminate; do not infer migration topology from exception text.
2. Run only `upgrade head` after the one-head precondition passes. Preserve bounded connection retries only for classified transient connectivity errors; migration/DDL, configuration, and multiple-head errors must fail immediately rather than being retried as if transient.
3. Add a release/CI check that detects multiple heads before building/deploying. Keep migration generation and drift checks aligned with the backend workflow.
4. Test the runner against a normal single-head graph and a deliberately-created multi-head fixture/disposable migration graph, verifying it refuses the latter without upgrading either branch.

**Acceptance criteria:** exactly one head upgrades successfully; zero/multiple heads stop before schema changes; error handling never falls back to `upgrade heads`; deployment receives a non-zero exit on the failed precondition.

### Phase 5 — Cross-repository verification and rollout

1. Add focused regression coverage for each behavior in the owning repository's existing test framework.
2. Run the full applicable backend and frontend CI checks documented in workspace `AGENTS.md`, plus migration checks against disposable PostgreSQL. Do not substitute SQLite-only results for PostgreSQL migration/locking checks.
3. Review API response contracts and frontend settings behavior together. Verify local development remains functional and that a storage/provider outage is surfaced as a controlled error rather than success.
4. Deploy to stage only from the exact CI-passing commit. Verify document upload/version/download, MFA enable/disable challenge flows, migration task networking and exit status, and API login/schema-dependent behavior. Review application and deployment logs for errors without exposing secrets.
5. Promote to production only after stage evidence, required owner review, successful migration, and a documented recovery plan. If any check is unavailable, record it as unverified rather than passing.

## Rollback and recovery

- **Document storage:** preserve already committed S3 objects and database references. Reverting code must not re-enable local fallback in protected environments. If S3 is unavailable, fail document writes and restore S3 connectivity; do not silently switch production to ephemeral disk.
- **MFA step-up:** retain the previous preference when challenge delivery/verification fails. A rollback must not restore the token-only disable endpoint; rollback the UI/API together or temporarily prevent preference changes while leaving existing login policy intact.
- **Networking:** if a private migration task cannot reach a required dependency, stop promotion and repair routes/endpoints/security groups. Do not re-enable public IP without explicit infrastructure review and documented risk acceptance.
- **Migrations:** take the normal deployment backup and follow the existing migration recovery policy. Do not downgrade production schema as an automatic rollback; use forward repair unless the migration has a reviewed, data-safe downgrade.

## Deferred risk and known limitations

- `localStorage` bearer tokens remain readable by same-origin injected JavaScript. No XSS was confirmed in the limited prior audit, but that does not remove the design risk. Track a separate BFF/session architecture project and reassess XSS, CSP, token lifetime/rotation, and session revocation before production hardening is considered complete.
- Email OTP is a step-up improvement over a bearer-token-only preference change, but it is not phishing-resistant MFA. A future authenticator/passkey option should be a separate product/security design.
- This plan excludes the three DevOps Terraform items at the user's direction and does not establish whether the related files are deployed or whether their credentials remain valid.
- No source changes, tests, cloud checks, or deployments are performed by creating this plan.

## Implementation and local validation record

The selected code and workflow changes have been applied in the CRM backend and frontend worktrees. The backend changes fail closed on protected-environment document storage errors, add email OTP step-up for MFA preference transitions, disable public IP assignment for migration tasks, and enforce a single Alembic head. The frontend now supports the OTP challenge and confirmation flow with localized feedback. Regression coverage was added in both repositories.

Local verification completed: backend Ruff, compile checks, migration-head check, and the full backend suite (`2288 passed, 94 skipped`); frontend lint, type checking, formatting, unit/contract checks, build, dependency audit, and dedicated MFA security browser regression passed. The CI browser sequence passed its checks through the AI draft flow, then `test:public-ai:browser` timed out loading `/faq` after 10 seconds. The isolated rerun and remaining browser checks are pending because the local command runner began failing to create processes. Treat browser validation as incomplete until those are rerun. The dependency audit reports no high/critical runtime advisories; the existing time-limited ESLint-only advisory exception expires 2026-11-04.

Not verified locally: PostgreSQL-backed migration/drift and opt-in integration checks requiring a disposable PostgreSQL service; actual stage/production subnet routing, NAT/VPC endpoints, security groups, ECS migration task execution, and deployed user flows. These checks remain rollout gates. No stage or production deployment has been performed. The deferred localStorage token risk and user-excluded Terraform findings remain outside this implementation.
