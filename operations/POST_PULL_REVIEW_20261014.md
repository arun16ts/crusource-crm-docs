# CRM review after Antigravity work and the dev-advaith pull

**Date:** 14 October 2026  
**Outcome:** Changes preserved. Local verification found regressions and CI failures; this is not a clean release sign-off.  
**Scope:** CRM application commits, imported branch changes, Reports/Analytics remediation, and affected shared flows. No application fixes, resets, merges, pushes or deployments were performed during this review.

**Later repair work:** See the [implementation and fresh verification report](POST_PULL_FIX_REPORT_20261014.md). The findings and check results below remain the historical review baseline.

## Commits reviewed

| Repository | Earlier Reports audit baseline | Current reviewed commit |
| --- | --- | --- |
| CRM frontend | `063e8c3c` | `7a4bceb5ea0056c6cb730c9d3ba62c5e436078ac` |
| CRM backend | `3ef484a` | `13fffc64109d6513f9daf06d3bea44bd5c8fe55a` |
| CRM docs | Original Reports audit | `d2aece8a96fad414a7de551465ddebba206ad8bc` before this review document |

The frontend merge is `8a72c814`, with parents `0a0e7f66` and `431a2ac0`. The backend merge is `2b7df78`, with parents `3ce8073` and `6d22b18`. Review covered the complete difference from the audit baselines and the merge's first-parent differences separately, including later commits. Commit attribution is taken from Git history; the history does not identify which assistant authored each line.

The pull covers subscription enforcement, document search, standard pipeline restrictions, demo acknowledgement/delivery, native dialogs and shared UI behavior as well as Reports. The separate Nx/NestJS repositories were clean and were not modified or subjected to CRM tests.

All five application/document repositories had clean worktrees and no unmerged index entries at the review baseline. Application heads remained the commits above throughout verification. No conflict markers were found in the inspected CRM source, tests and migrations. Whitespace checks found issues; those are distinguished from merge conflicts.

GitHub MCP confirmed that both current CRM commits exist remotely. The Actions/status connector returned HTTP 404. The checked-out branch is `dev-arun` in both CRM repositories; their current CI push triggers do not include that branch. Remote CI results and deployment status remain unverified.

## Findings and repair plan

### PP-01 — High: the probability migration overwrites configuration based on a display name

**Evidence:** [Qualification migration](../../crusource-crm-backend/alembic/versions/20261014_standard_pipeline_qualification_win_prob.py), upgrade at line 11 and downgrade at line 21. The update matches pipelines named `Standard Sales Pipeline`, without restricting their module, system provenance or prior probability. The downgrade writes `20.00` for every match, rather than restoring each original value.

**Impact:** A pre-existing non-default/custom/Lead pipeline with that name and a Qualification stage is included. Previously customized probabilities on matching Sales pipelines are also replaced. Rollback is not a restoration of original configuration. This is established from the SQL predicate; a separate populated migration fixture was not executed because creation of the additional disposable database was declined. Schema upgrade and drift checks passed, which does not establish preservation of these values.

**Repair:** First inventory affected rows without modifying them. Restrict system pipeline updates using a stable identity and the correct module; change only an explicitly supported prior default if a default update is intended. Preserve customized values and document recovery limits. If the migration has already run in an environment, use a forward corrective migration and recover lost values only from authorized backups/audit evidence. Do not invent original probabilities or silently rewrite deployed migration history.

**Acceptance:** A canonical unchanged default can move to 10%; custom probabilities and similarly named pipelines in other modules survive. A rollback either restores recorded values or explicitly refuses an unsafe data rollback.

### PP-02 — Medium: provisioning overwrites values that Forecast still permits users to save

**Evidence:** [Pipeline provisioning](../../crusource-crm-backend/src/modules/pipelines/services/pipeline_seed_service.py), lines 48–59, and [Forecast probability command](../../crusource-crm-backend/src/modules/forecast/handlers/update_stage_probabilities_handler.py). A diagnostic saved Qualification at 15% through the real Forecast handler, then called provisioning again; the stored value became 10%.

**Impact:** Repeated provisioning/repair of an existing standard pipeline can discard saved Forecast configuration. This was reproduced through the domain functions; it is not a claim that every Forecast page load resets probabilities. Pipeline structure is locked in one command path while the Forecast path still accepts probability edits.

**Repair:** Keep existing-pipeline provisioning idempotent and separate structural immutability from configurable Forecast probabilities. Preserve saved values when initializing missing data. If probabilities must become fixed as a deliberate product rule, enforce that consistently in the Forecast API and UI and provide an explicit configuration migration rather than silently resetting values.

**Acceptance:** Saving a supported Forecast value and repeating initialization leaves it unchanged; both API entry points apply the same documented rule.

### PP-03 — Medium: renaming a custom pipeline can lock it permanently

**Evidence:** [System pipeline classification](../../crusource-crm-backend/src/modules/pipelines/services/pipeline_seed_service.py), lines 30–45; [pipeline commands](../../crusource-crm-backend/src/modules/pipelines/handlers/pipeline_lifecycle_handlers.py), lines 25 and 106; [response classification](../../crusource-crm-backend/src/modules/pipelines/schemas/pipeline_schemas.py), line 133.

**Reproduction:** Create an ordinary Lead pipeline, rename it to `Standard Sales Pipeline`, then rename it back. The first rename succeeds; the next returns HTTP 400 because the name alone now makes it standard. The same classification also blocks stage edits and deactivation. Cross-module names are accepted because duplicate checks are module-specific.

**Repair:** Persist a stable system identity independent of display name and the changeable default flag. Use one classification policy for commands and responses. Validate reserved names before create/rename, and provide a safe recovery path for already misclassified custom pipelines. Backfill ambiguous existing records through verified provenance, not a broad name match.

**Acceptance:** Genuine seeded pipelines retain intended protections after changing the default; a custom pipeline never acquires system privileges or restrictions merely by changing its name.

### PP-04 — Medium: SmartSelect hides existing values with different letter casing

**Evidence:** [SmartSelect](../../crusource-crm-frontend/src/components/shared/SmartSelect.tsx), lines 91, 178 and 233. Matching now ignores case, but the native select receives the original, case-sensitive value.

**Browser reproduction:** `options=['Finance','Healthcare']`, `value='finance'` renders the selected placeholder `-None-` and the DOM select value is empty. Before the new case-insensitive classification, an unmatched value was displayed in the custom input. The current behavior can make a populated field look cleared.

**Repair:** Resolve the matched option's actual value for display while preserving the intended submitted value contract, or retain custom input mode for an exact-value mismatch. Test the real component's transitions, including custom input, clearing, case variants and newly persisted options. The existing SSR test does not exercise mounted effects or this case variant.

**Acceptance:** Reopening a form with a stored case variant displays the existing value correctly and saving without edits does not silently clear or change it.

### PP-05 — High, pre-existing: tenant plan changes bypass payment/approval

**Evidence:** [ChangePlan handler](../../crusource-crm-backend/src/modules/billing/handlers/change_plan_handler.py), lines 67–88; [tenant billing route](../../crusource-crm-backend/src/modules/billing/routes/billing_routes.py); [subscription recovery allowlist](../../crusource-crm-backend/src/shared/auth/subscription_recovery.py).

**Reproduction:** An expired organization was denied by the entitlement service. Calling the real change-plan handler for an active paid plan changed its subscription to `active`, and entitlement was allowed, without a payment provider or platform approval. The tenant route authorizes billing setup access and remains deliberately reachable after expiry. This requires an authenticated user with billing permission; it is not an unauthenticated bypass. The activation handler is unchanged from the review baseline, so this is an existing gap made relevant by the new trial lock, not an Antigravity-introduced handler regression.

**Repair:** A tenant plan request should initiate checkout or a pending request. Activate entitlement only after verified payment or an explicitly authorized platform approval. Keep billing recovery reachable, but do not let a tenant mint active entitlement. Repeated requests, retries and signed webhook handling must be idempotent and audited. If billing is intentionally operating without payment integration, platform approval should govern paid activation until checkout exists.

**Acceptance:** An expired tenant cannot regain access through self-service plan selection alone; verified payment or authorized approval unlocks it exactly once.

### PP-06 — Medium, CI blocker: formatting fails across the reviewed frontend changes

`npm run format:check` with `FORMAT_BASE_SHA=063e8c3c` failed on **127 files**. The range covers the full pulled work being reviewed. Full lint and type checking still passed. Backend `git diff --check` also reported trailing whitespace in `report_queries.py` and an extra final blank line in `test_migration_heads.py`; the frontend diff reported an extra final blank line in the new Leads regression test.

**Repair:** Apply the repository's formatter only to the affected supported files, inspect the resulting diff, and rerun formatting and relevant checks. Preserve functional changes and avoid formatting unrelated repositories. The application files were not reformatted during this review.

### PP-07 — Medium, CI blocker: the attachment integration fixture no longer meets auth prerequisites

The full backend suite failed `test_download_attachment_with_bearer_and_query_token`: expected 307, received 404. [The fixture](../../crusource-crm-backend/tests/test_attachments_flow.py), line 18, creates an admin with a random organization ID but no Organization row. The new shared entitlement lookup correctly requires the organization to exist. A separate diagnostic ran the committed attachment test with an active Organization row added to the fixture: **all three attachment tests passed**.

**Repair:** Seed a realistic organization/subscription for the committed fixture. Retain real authorization and entitlement checks; do not bypass them to satisfy the test. Add assertions for entitled downloads and expired/missing-organization denial.

**Acceptance:** The unmodified full-suite command passes after the committed fixture is repaired. The diagnostic fixture pass does not turn the current committed full-suite failure into a CI pass.

### PP-08 — Low: Reports remediation documentation is stale

The [follow-up fix plan](../features/reports/REPORTS_ANALYTICS_FIX_IMPLEMENTATION_PLAN.md) and README still say fixes are proposed/unimplemented, although remediation is now committed. The prior implementation report also contains historical local-only verification wording; it must not be read as evidence for today's merged commits or stage.

**Repair:** Add a dated remediation/evidence matrix for RA-01 through RA-20 tied to the reviewed commits, and link it from the older audit/plan without erasing their original findings. Separate code presence, local verification, CI status and deployment status. This review records current evidence and blockers; it does not silently rewrite historical reports.

## Verification evidence

Raw logs and reusable diagnostics are retained outside the docs repository under [the review validation directory](../../validation/post-pull-review-20261014/). They use local disposable fixtures and contain no live credentials.

| Check | Result |
| --- | --- |
| Fresh focused backend checks for Reports/Analytics, subscriptions, pipelines, demo acknowledgement, document search and migration heads | **94 passed**; [log](../../validation/reports-fixes-20261014/post-pull-focused.log) |
| Backend complete suite on current commit | **2,143 passed, 74 skipped, 1 failed**, attachment fixture; [log](../../validation/post-pull-review-20261014/backend-ci/full-tests.log) |
| Backend Ruff and compileall | Passed |
| Clean PostgreSQL 17 migration upgrade | Passed, one head: `20261014_merge_advaith_arun` |
| Empty-database migration drift, supported downgrade boundaries and `alembic check` | Passed |
| PostgreSQL document search enum and Reports naming transactions | Passed |
| Redis shared quotas, production transactions, recovery/import/startup locking, platform authority/trial review/demo integration checks | Passed |
| Provider credential encryption migration, transactional failure and rollback boundaries | Passed in a separate empty disposable database |
| Existing Python environment | Python **3.12.10**, `pip check` passed; backend dependency manifests unchanged in reviewed range |
| Runtime backend dependency audit against committed lock | No known vulnerabilities found |
| Frontend isolated checkout, Node **20.20.2**, locked `npm ci` | Passed |
| Full frontend lint, regular tests, Reports, spreadsheet, native-dialog, Loop AI/public contracts, TypeScript | Passed |
| Frontend formatting over reviewed range | Failed; PP-06 |
| Frontend production build using safe API/OAuth fixture configuration | Passed |
| CI browser/contract regressions, including subscription lock, global search, dialogs, Reports, Forecast, Documents and platform sales recovery | Passed except the first demo routes run's checkout-layout failure, resolved by the rerun below |
| Platform Overview browser check | Passed separately; the initial command collector omitted the named single-line workflow step |
| Demo routes test: actual Next.js routes and real FastAPI fixture | Passed when rerun from the real sibling-repository layout; isolated clone initially expected a nonexistent sibling backend |
| Real Reports browser/API bridge | Saved pipeline scope, canonical stage drill/back, native widget configuration create/update/reload passed |
| Frontend dependency audit | No high/critical runtime advisories; repository's temporary ESLint-only exception remains until 4 November 2026 |
| Diagnostic issue reproduction | Three backend reproductions and the SmartSelect browser reproduction confirmed PP-02 through PP-05; a diagnostic pass means an issue reproduced |

Frontend and backend detailed command results are in [frontend results](../../validation/post-pull-review-20261014/frontend-ci/results.json) and [backend results](../../validation/post-pull-review-20261014/backend-ci/results.json). Separate rerun logs distinguish fixture/layout corrections from results of the original committed commands. The backend used its existing venv, not a newly installed clean environment. General-suite skips were followed by the workflow's required opt-in PostgreSQL and Redis checks; other skipped optional tests are not claimed as executed. No stage or production database was migrated, seeded or cleared.

## Reports/Analytics conclusions

The repaired source and current tests cover saved report scope, advanced filter preservation, canonical drill dimensions, SQL matrix totals, native pipeline settings, guarded suggestions/sharing references, export safety, legacy definition handling, report picker paging, URL parsing, read-only board controls and Calls/Meetings reference mapping. A real browser-to-API check verified the main saved-scope/drill/configuration round trip rather than relying only on mocked frontend requests.

These checks provide evidence for the repaired flows; they do not prove every UI combination or every existing customer report is valid. No cross-product integration was inferred from similarly named code. Standard pipeline changes still need the repairs above, and the committed CI blockers prevent a clean readiness claim.

## Recommended order

1. Resolve PP-01/PP-02 before running the imported migration against customer data; reconcile the intended standard-pipeline/Forecast rule.
2. Resolve PP-05 before relying on the trial lock for commercial entitlement enforcement.
3. Repair stable pipeline identity/name handling and SmartSelect display behavior with behavioral regressions.
4. Repair the committed attachment fixture and changed-file formatting, then rerun the complete applicable CI checks.
5. Update the remediation evidence matrix and obtain remote CI results for the exact promotion commits.
6. Before any deployment, follow the workspace's complete deployment audit and verify environment-specific migration history and affected stage flows.

The `validation/phase4/` and `.worktrees/` copies shown in the IDE are historical/test checkouts, not the active implementation. The actual `crusource-crm-backend/src/modules/platform_auth/handlers/verify_challenge.py` is unchanged across the reviewed range. No historical copy was copied over current source. Application code and all pulled commits remain intact.
