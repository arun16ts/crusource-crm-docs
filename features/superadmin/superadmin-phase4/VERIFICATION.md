# Phase 4 verification

Status: **PASS after recorded reruns — local implementation and verification complete.** [Backend exits](backend-checks.json), [frontend exits](frontend-checks.json), [actual-route/API evidence](route-verification.json), [CRM frame comparison](crm-frame-verification.json) and [changed-source hashes](source-files.json) identify the reviewed working tree.

Local runners and raw logs are under `D:\GitHub\Crusource-CRM\validation\phase4`. Source snapshot environment files are excluded. Tests use CI Node 20 and the backend Python 3.12 venv, disposable PostgreSQL 17/Redis 7 and synthetic identities. Browser checks use installed headless Edge on Windows; the Linux CI workflow uses pinned Playwright Chromium.

Earlier validation attempts found Phase 3 head assertions, a Windows native-library installation lock, reused pytest-directory permissions and the extra CRM frame test's missing snapshot Git history. The head assertions were updated, a clean isolated install succeeded and dependencies were restored without stopping the app, fresh test directories were used, and read-only baseline history was supplied for the frame check. Final evidence distinguishes those attempts from successful reruns.

## Backend checks

| Check                                                         | Final result                                 |
| ------------------------------------------------------------- | -------------------------------------------- |
| Ruff across src/tests/scripts/Alembic                         | Passed                                       |
| Compileall                                                    | Passed                                       |
| Full committed history on fresh disposable PostgreSQL         | Passed, one head `20261011_platform_sales`   |
| Full pytest suite                                             | **2,001 passed, 70 skipped**, 1,939 warnings |
| Required Redis quotas/public AI group                         | **35 passed**                                |
| Required webhook/production PostgreSQL group                  | **59 passed**                                |
| Recovery/startup/import PostgreSQL group                      | **10 passed**                                |
| Platform invitation/auth/trial/demo races and migration group | **45 passed**                                |
| Schema drift against a distinct empty database                | **1 passed**                                 |
| Alembic check after upgrades                                  | Passed, no new upgrade operations            |

The ordinary suite's opt-in skips are not counted as service passes; the required groups above were run with their workflow flags. New sales tests include normalized public input/size/consent, accepted transaction/replay/conflict/repeat, role/origin/cookie/CSRF boundaries, owner grants/current revocation, filtered counts/cursors, versioned workflow/history/note atomicity, terminal/reopen/spam/schedule/follow-up rules, minimal notification content, permanent/transient failure, lease fencing/restart and six-attempt crash exhaustion. PostgreSQL exercises competing same-key intake/moves, mismatched replay, permission changes versus mutation/replay/assignment, spam versus assignment and concurrent delivery. Migration tests preserve staff/invitation state and refuse populated-table downgrade.

Backend fixture tests use fake mail; none sent a real SES message. CRM unit intake explicitly uses a synthetic Scope, while the additional browser/API test uses a genuine synthetic CRM JWT and the actual Scope dependency.

## Frontend checks

Successful clean offline lockfile installation in an isolated snapshot; changed-file Prettier check over 49 files; full lint (**0 errors, 1,482 warnings**); npm test including localization; spreadsheets; Loop/public contracts; type check; every browser command currently registered in CI; production build with test-only API/OAuth values; and dependency audit all passed after the documented rerun. The audit reports no high/critical runtime advisories and retains the repository's existing ESLint-only exception expiring 4 November 2026; it is not a claim of zero advisories across all dependencies.

Additional platform contracts/auth/session startup, public pages/analytics, CRM frame and actual Next/FastAPI demo/billing integration passed. The frame test compares five pixel-identical desktop/collapsed/tablet/mobile pairs against actual Git HEAD source. Its original run reproduced the documented antivirus-injected host; the test now blocks only that known injected host while retaining failures for unexpected application/API requests. The public-page test exposed the existing empty resource navigation, which was restored with localized desktop/mobile links.

The final complete frontend wrapper returned 1 solely for an overly strict label locator in the newly added sales-access editor regression. The corrected test passed on its focused rerun; `frontend-checks.json` retains `initial_exit_code: 1` and the final `exit_code: 0` for that command. There are no unresolved required local checks. This does not claim an unmodified wrapper run was entirely green, or that remote GitHub CI has run on these uncommitted changes.

Portable sales browsers cover uncertain identical-key retry, independently bounded 20/21-record columns, CSRF/versioned stage submission, list/detail, visible conflict, read-only controls, stale refresh, owner-editor command wiring, transport isolation and independent follow-up timezone retention. Actual routes exercise EN/NL public intake to persisted platform data, real platform MFA/cookie/CSRF, the real billing modal and CRM authenticated intake, assignment, scheduling, follow-up, notes, reload/URL persistence and real CSS at 1440/1024/768/390 pixels. Responsive checks wait for shared frame transitions and assert content bounds; see [captures](SCREENSHOTS.md).

## Environment and release limits

The initial native dependency replacement failed on a Windows CSS binary lock. The snapshot install succeeded and workspace dependencies were restored without replacing identical locked binaries. No user app process was stopped. npm reported unapproved optional install scripts; the installed native packages, browser bundles and production build all executed successfully. No environment files were copied into the snapshot/review package.

Graphify code refresh completed. A root `.graphifyignore` excludes validation copies, worktrees and storage from application context. Existing parser limitations for unrelated TSX/TOML/HCL are not compiler failures; application type/build/static checks above passed. No extra LLM extraction or dependency installation was performed for the graph.

Disposable test services are removed after verification. The original app services/data are preserved. The normal running app requires the additive migration before using the new credential/schema fields and a backend restart where reload is disabled. Approved staff grants/notification recipients, proxy identity, privacy copy/record retention, real Redis/SES/scheduler operation and actual ECS/Vercel commits/logs/customer flows remain release inputs and Phase 6 deployed acceptance. No application/stage database migration, push, deployment, real provider email or AWS/Vercel audit was performed.
