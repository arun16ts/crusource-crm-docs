# Super Admin Phase 3 — implementation packages

Date: 9 October 2026. Status: **IN PROGRESS; 3A, 3B and 3C verified locally.**

Delivered: Overview (3A), [Organizations and Login History/member profiles/export (3B/3C)](ORGANIZATIONS_LOGIN_HISTORY.md), and the independently reproduced trial partial-commit correction. Phase 3 is not complete: full trial-review concurrency/authority/dialog work (3D), Feedback (3E) and integrated acceptance remain in the [implementation plan](../SUPERADMIN_PHASE_3_IMPLEMENTATION_PLAN.md).

The sections below preserve the first Overview package’s historical evidence. Its source edits were subsequently committed as frontend `70ee05da` and backend `151c28b`; the linked 3B/3C package records the newer local changes and verification.

## Baseline and environment

Source baseline: frontend `d9e13de4`, backend `48a98bc`, documentation `e045602`. Application repositories remain on `dev-arun`; changes are local and uncommitted. The existing validation checkout was reused, without adding another repository/worktree. No deployment or application-database migration was performed.

The running localhost backend answered readiness, but the browser did not have an authenticated platform session (`/superadmin/auth/me` returned 401). CRM credentials were not used as platform credentials. Before/after browser verification used actual Next.js routes, real FastAPI handlers, cookie/origin/custom-header/CSRF guards, in-memory SQLite and synthetic staff/customer identities. Delivery was fake and local. This is integration evidence, not a staging or real-mail claim.

Before captures and page text: [baseline/routes.json](baseline/routes.json). After evidence: [overview/routes.json](overview/routes.json). Desktop and mobile captures are saved alongside those files. The mobile test waits for the shared frame's existing animation and checks content bounds; a document-level overflow check alone cannot detect clipped content.

Initial route request families were:

| Route | Route data | Required shell data |
| --- | --- | --- |
| Overview | Dashboard KPIs | Platform identity; pending invitations for the owner's navigation badge |
| Organizations | Organization page | Same platform shell |
| Login history | Organization selector, history page and statistics | Same platform shell |
| Trial extensions | Trial request page | Same platform shell |
| Feedback | Feedback page and statistics | Same platform shell |

No customer CRM endpoints were requested by these platform pages. Raw development logs include repeated attempts around Strict Mode remounts; they do not establish production duplicate completions. The first baseline Overview capture also overlaps the sign-in redirect's initial reads. This package does not claim a frontend request-count reduction, nor that all page/tab/drawer reads have been audited. Organization selectors and other page dependencies require their later package's tracing.

## Overview changes

- A thin server route renders a focused client feature using the shared page header/button, design tokens, EN/NL platform messages, host-aware links and pure platform formatters. CRM shell and font configuration were preserved.
- Customer accounts and platform staff have separate totals. Staff classification uses the existing platform provider, platform roles, legacy super-admin flag or platform credential existence. A customer awaiting organization onboarding remains a customer; inactive/reset platform accounts remain staff.
- Enabled accounts are explicitly distinguished from recent activity. New-record counters retain the existing rolling 30-day UTC definition. Subscription and customer role/provider breakdowns remain server aggregates; entity counts retain existing soft-deletion behavior.
- The old unmeasured `healthy` literal is now `unknown`, and Overview does not display a health badge. No infrastructure monitoring is invented.
- The currency-blind Deal sum is no longer executed or displayed as dollars. The deprecated `total_pipeline_value` key is retained with `null`; existing all-account user totals/breakdowns remain available for compatibility. New customer/staff fields are additive.
- Loading and initial failure do not show fake zeros. Retry recovers, failed refreshes retain the last successful snapshot with a visible warning, and an old API without customer metrics is reported unavailable rather than guessed. Unrated feedback shows an unavailable rating, not zero stars.
- Session-scoped TanStack keys, cancellation, caching and guards remain unchanged. No additional Overview endpoint or whole-entity read was added.

Deploy the backend contract before the new frontend. An older frontend still interprets a null deprecated pipeline value as its old zero fallback; coordinate the UI update rather than presenting that transient old display as trustworthy. This package does not authorize deployment.

## Backend work and evidence

[PostgreSQL comparison](overview-postgres-profile.json) executes old committed and new aggregate implementations against the same synthetic tenant/customer/staff schema inside a disposable PostgreSQL 17 container, then removes that schema. SQL statements decreased **21 → 14** through consolidated organization/user/feedback counters and removal of the invalid amount sum. Aggregates remain server-side; no entity lists are hydrated for cards.

Single small-run timings were 64.39 ms before and 47.33 ms after. These timings are not a scale benchmark or SLA. Classification and SQL execution were checked on PostgreSQL as well as SQLite. Full scale profiling, index recommendations and caching decisions remain evidence-driven follow-up work.

The trial integrity regression simulated a history-write failure after approval. Before the fix, the request was already `approved` despite rollback. Repository review helpers now flush; handlers own the commit/rollback, so request, subscription/organization dates and SubscriptionHistory persist together. Rejection now explicitly commits in its handler as well. The regression checks pending status, original expiry, zero extension days and absence of history after failure. Existing successful/expired/already-reviewed business tests pass.

This is the partial-commit correction, **not completion of 3D**. Concurrent approve/approve or approve/reject locking, transactional revalidation after staff revocation, idempotent/conflict contracts and current-record action dialogs remain required. Existing admission guards and eligibility rules were preserved.

## Verification

Focused backend: **16 passed** across dashboard and trial tests; focused Ruff passed. Browser checks passed for real route/API identity separation, real Instrument Sans, 1440/1024/768/390px layouts, initial and refresh failure, retry, older API, navigation and absence of CRM reads. A portable frontend browser regression covers true empty results and platform transport and is registered in frontend CI. The actual-route test is separate because it requires the sibling backend/venv.

Backend full local CI parity passed: Ruff, compile, committed PostgreSQL migrations, **1,962 tests passed / 49 skipped**, required Redis **33 passed**, webhook/production PostgreSQL **58 passed**, recovery/startup/import PostgreSQL **10 passed**, migration drift **1 passed**, Alembic check (no new operations) and platform PostgreSQL **25 passed**. The skipped opt-in groups were explicitly exercised in their applicable separate runs. No schema migration was added by this package.

All checks listed in the frontend workflow passed: clean lockfile install, changed-file formatting, full lint (0 errors, 1,491 existing warnings), test suite, spreadsheets, Loop/public contracts, type check, all required browser suites, production build using test-only API/OAuth settings and dependency audit. The focused Overview browser test added to that workflow passed. Additional platform contract/auth/real-route tests passed. The wrapper runner returned 1 solely for the extra frame test described below; it is not reported as an entirely green unmodified run. See [frontend checks](frontend-checks.json) and [backend checks](backend-checks.json). The extra unmodified CRM-frame test failed when the deterministic fixture received a locally injected antivirus request, matching the previously recorded environment issue. A controlled rerun blocked that external injection and compared the real pre-merge shell source: expanded/collapsed desktop, 1024, 768 and 390px screenshots were identical. Application source and system antivirus settings were unchanged; this does not erase the unmodified test failure.

Graphify code update completed. It reported inaccessible pytest scratch directories, existing parser warnings and missing SQL/HCL parsers; the application-code update completed without installing unrelated dependencies. An earlier validation attempt was interrupted: runners disappeared and disposable containers stopped; partial logs were not counted as passes. Validation was restarted against the same isolated services, including a distinct empty database for migration drift. The application database and imported data were not modified.

Disposable Phase 3 PostgreSQL/Redis services were removed after checks; the original application containers/data were preserved. No changes were pushed or deployed. Your normal local backend needs a restart if it is running without reload to pick up the new API fields.

No stage deployment, CloudWatch/Vercel logs, production-scale workload or real staff-session verification is claimed. The remaining Phase 3 packages and final integrated baseline/authorization/visual checks must finish before Phase 3 is marked complete.
