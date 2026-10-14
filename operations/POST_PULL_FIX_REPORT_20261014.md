# Repairs after the imported CRM changes

**Date:** 14 October 2026  
**Scope:** PP-01 through PP-08 in the [post-pull review](POST_PULL_REVIEW_20261014.md). CRM frontend/backend and supporting documentation.  
**State:** Repairs implemented in the working trees and applicable local checks passed. No commits, pushes, stage migrations or deployments were performed.
**Base commits:** Frontend `7a4bceb5ea0056c6cb730c9d3ba62c5e436078ac`, backend `13fffc64109d6513f9daf06d3bea44bd5c8fe55a`. The original pulled commits remain intact.

## What changed

| Review finding | Repair |
| --- | --- |
| PP-01 — Unsafe historical probability migration | The historical revision is unchanged. An Alembic safeguard snapshots existing matching stage probabilities only when crossing that revision, then restores them through the supported post-step callback before the migration transaction commits. Online upgrade/downgrade preserves existing values; unsafe offline SQL generation is rejected. |
| PP-02 — Provisioning resets Forecast settings | Existing-pipeline provisioning preserves stages and probabilities. Newly provisioned pipelines receive the default probabilities; Forecast can continue saving valid probability edits. |
| PP-03 — Name-based pipeline locking | Persisted `system_key` identifies system pipelines independently of display name and current-default selection. Commands and API responses use the same policy. Reserved names are rejected before custom create/rename can mutate data; legacy custom lookalikes can be renamed normally. |
| PP-04 — SmartSelect shows a stored value as None | The mounted select displays the actual matching option value while retaining the parent's existing value until the user edits it. A browser regression covers case variants, custom-option persistence and field clearing. |
| PP-05 — Tenant plan selection creates active entitlement | Valid paid plan selections now return 409 with no subscription, status, period or history mutation. Billing currently renders the beta notice and has no verified checkout/approval workflow; the repair closes the hidden activation endpoint rather than inventing a payment integration. Existing subscriptions are unchanged. |
| PP-06 — Formatting | Prettier was applied to 128 files in the reviewed frontend range, including the new browser regression. Working-tree line endings were normalized; the tracked frontend diff is limited to formatting repairs and the intended functional/workflow changes. Backend trailing whitespace and the extra test-file final blank line were removed. |
| PP-07 — Invalid attachment fixture | The fixture now creates an active organization. Real bearer-token download tests cover active, expired and missing organizations; query tokens and unauthenticated access remain rejected. |
| PP-08 — Stale implementation status | Added the [RA-01–RA-20 remediation matrix](../features/reports/REPORTS_ANALYTICS_REMEDIATION_REPORT.md), updated audit/plan/report backlinks and indexed this report. Historical findings are retained. The inventory now describes Billing Contact Sales as partially implemented because its modal/API exist but the current Billing route mounts only the beta notice. |

## Pipeline schema and data safety

The new migration [20261014_pipeline_identity](../../crusource-crm-backend/alembic/versions/20261014_pipeline_identity.py) follows the existing merge head. It adds a nullable identity with tenant uniqueness and module consistency constraints. New seeded pipelines receive identity at creation. Legacy backfill recognizes the expected name, description, module and full active stage fingerprint; probabilities are deliberately excluded from that fingerprint so saved Forecast values are not treated as identity. Nonmatching records remain custom and editable. Exact legacy clones cannot be proven to have distinct provenance from the old schema alone; inspect the intended backfill candidates before promotion if those conventions were reused for custom pipelines.

[The qualification safeguard](../../crusource-crm-backend/src/shared/database/qualification_migration_guard.py) takes the pipeline DDL lock before stage row locks, preventing a lock-order conflict with an in-flight Forecast edit. It does not take a data snapshot for ordinary schema checks or migrations that do not cross the historical rewrite. The [migration environment](../../crusource-crm-backend/alembic/env.py) installs it through Alembic's supported callback API. Offline execution across the risky revision is unavailable because it cannot capture real prior values; the deployment migration runner already uses online execution.

The populated PostgreSQL regression includes a configured Sales pipeline and a similarly named non-default Lead pipeline. Its negative control disables the safeguard and reproduces the old overwrite. The repaired path then preserves both probabilities through upgrade, identity backfill, downgrade and repeat upgrade, with model drift checks.

**Recovery limits:** Values already overwritten before installing the repair cannot be reconstructed from source. Recover those only from verified backups or audit evidence by stage ID. This implementation preserves the values present when the protected migration starts; it does not guess missing history. Likewise, paid subscriptions previously activated through tenant plan changes require review of their original authority/payment evidence; they were not automatically revoked or altered.

**Rollout requirement:** Apply the new schema migration successfully before running the repaired API, which now queries the identity column. Follow the workspace migration/deployment audit against the eventual CI-approved commits. No stage or production database was touched during this implementation.

## Local verification

Evidence lives in [the repair validation directory](../../validation/post-pull-repairs-20261014/). Earlier failed runs remain available and are not relabelled as passing.

- Behavioral regressions were run before the application repair: eight backend cases failed for the reported behavior, and the SmartSelect browser check failed on the blank selection. They then passed after the fixes. Migration coverage was added alongside the safeguard and includes an explicit negative control of the unchanged old SQL.
- Frontend verification used Node 20.20.2, a fresh locked `npm ci` in the owned isolated checkout, full lint, ordinary tests, Reports/spreadsheet/native-dialog/Loop AI/public contract checks, TypeScript, all named CI browser/contract scripts, production build with safe fixture API/OAuth configuration, and dependency audit. The demo routes script ran separately from the real sibling-repository layout it expects.
- Backend verification uses Python 3.12.10 and disposable PostgreSQL 17/Redis 7 services. It includes Ruff, compileall, clean migration upgrade, required PostgreSQL/Redis regressions, provider-encryption rollback boundaries, full pytest, schema drift and `alembic check`, and runtime dependency audit. Backend dependencies were unchanged and the existing venv was used; this was not a clean backend dependency installation.
- Real browser/API checks verified saved report pipeline scope, canonical stage drill/Back, native widget configuration round trips, actual demo intake/platform routes and the durable sales workflow.
- An initial combined migration run failed because the historical enum migration checks type names across schemas. The new isolated-schema preservation test is now ordered before the public-schema drift test in an empty disposable database. Both passed after that fixture-order correction. The final complete backend run also covers the later migration lock-order safeguard.
- Frontend audit reported no high/critical runtime advisories under the existing policy; its temporary ESLint-only exception expires on 4 November 2026. Backend lockfile audit reported no known vulnerabilities.

The final backend suite passed **2,162 tests**, with **75 optional tests skipped**. Required opt-in PostgreSQL/Redis checks passed separately, including **both** populated pipeline preservation and public-schema drift checks. All **45 named frontend test scripts** required by its workflow are covered, including the separately executed real-route demo test. Locked installation, full lint, type checking, build, both reviewed-range and working-tree formatting checks, and dependency audits passed.

See [final backend command results](../../validation/post-pull-repairs-20261014/backend-ci-final/results.json), [full pytest log](../../validation/post-pull-repairs-20261014/backend-ci-final/full-tests.log), [frontend command results](../../validation/post-pull-repairs-20261014/frontend-ci/results.json), [real demo-route log](../../validation/post-pull-repairs-20261014/demo-routes-browser.log), [Reports/API bridge log](../../validation/post-pull-repairs-20261014/reports-api-browser.log), and [source/validation manifest](../../validation/post-pull-repairs-20261014/final-evidence.json). The manifest verifies that changed frontend files match the checkout tested and records application base commits and file hashes. Local checks do not establish remote GitHub CI or actual stage/provider delivery; those remain unverified.

## Boundaries preserved

The two separate Nx/NestJS repositories were not changed. Historical `validation/phase4/` and `.worktrees/` copies were not used as implementation source. Current platform authentication challenge handling and its MFA behavior were not changed by these repairs. There was no repository reset, branch rewrite, dependency upgrade, application database cleanup or external issue modification.

Graphify was refreshed from the orchestration root. It preserves the five repository paths and excludes validation checkouts. Graph extraction can be partial for some TypeScript constructs; compiler/build evidence and actual source take precedence over parser warnings.
