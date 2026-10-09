# Super Admin Phase 0 baseline

9 October 2026. **Phase 0 complete: local baseline, visual references, executable design contracts and migration checklist.** Later application phases remain planned. No authentication migration, demo form or support feature has been installed by this phase.

## Repository snapshot

The workspace root is an orchestration directory. Git commands were run against the three nested repositories.

| Repository | Starting HEAD | Starting working tree |
|---|---|---|
| Frontend | `0276a54d83c08507648dee964cbaaa602d62d5af` | Clean |
| Backend | `33a6ff4ae16b13c25e04af516a402b38f3d1afd1` | Clean |
| Docs | `af481069a8a4f9677b6247166825fbe4d370e911` | Existing modified `Superadmin login.md`; untracked master and phase-wise plans |

The existing login-document edit was preserved. Phase 0 adds this directory, updates both plans' execution status and corrects the native port description in root `AGENTS.md`. Frontend/backend tracked source remained clean after verification. No Git commit, deployment or real invitation was performed.

## Installed environment and routing

| Tool/package | Observed version |
|---|---|
| Node / npm | 26.10.0 / 11.19.1 |
| Next.js / React | 16.3.8 / 19.2.4 |
| Tailwind | 4.3.3 |
| TanStack Query / Redux Toolkit | 5.104.1 / 2.13.0 |
| Playwright / esbuild | 1.62.1 / 0.28.2 |
| Python | 3.12.10, backend `.venv` |
| FastAPI / SQLAlchemy / Alembic | 0.111.1 / 2.0.28 / 1.13.1 |
| Pydantic / Redis client / pytest | 2.13.5 / 5.0.3 / 9.1.1 |

These are observed installed versions, not dependency upgrades made in Phase 0. Read the matching Next.js Server/Client Components and proxy documentation under the installed `next/dist/docs` before implementation.

The [manifest](../../crusource-crm-frontend/package.json) resolves the port discrepancy: `npm run dev` uses Webpack on **3000**, `dev:turbo` uses Turbopack on **3000**, and `npm start` uses **3005**. Use 3000 for native development until an intentional script change. Root `AGENTS.md` was corrected to match those scripts. Docker frontend host port 3001 is a separate execution mode; no Docker stack was started for this baseline.

[Proxy behavior](../../crusource-crm-frontend/src/proxy.ts): on a `superadmin.*` host, `/` rewrites to `/superadmin/dashboard`; short paths rewrite under `/superadmin`. Already-prefixed paths pass through. Static/API/public paths bypass that rewrite. Thus a relative `/dashboard` link on the platform host remains on the platform, rather than opening the commercial CRM. Phase 2 must use an explicit validated CRM origin for that action.

[Next rewrites](../../crusource-crm-frontend/next.config.ts) forward `/api/*` and `/public/*` to the backend. The [platform transport](../../crusource-crm-frontend/src/lib/api/platformHttpClient.ts) deliberately uses same-origin `/api/v1`, host-local cookies, no CRM Authorization token, no-store fetches, platform request header and CSRF. Preserve that isolation. Backend development admission supports localhost/127.0.0.1/superadmin.localhost on 3000, 3001 and 3005. Deployment origins were not inferred from secret files and still require explicit release configuration.

Repository Alembic head: **`20261008_webhook_receipts`**, a single head. `alembic current` was not run against an application database; deployed revision and data counts are unverified.

## Executed checks

| Check | Result | Practical limit |
|---|---|---|
| Eight targeted backend test files | **58 passed**, 31 warnings, 16.97s | In-memory SQLite, fake Redis/email; not PostgreSQL race proof |
| `npx.cmd tsc --noEmit` | Passed | Existing tsconfig excludes e2e tests |
| `npm.cmd run lint` | Passed: 0 errors, **1,509 existing warnings** | Warnings remain baseline debt; no bulk cleanup |
| `npm.cmd run test:platform-auth:browser` | Passed | Actual components/hooks/transport against simulated API |
| `npm.cmd run test:session-startup:browser` | Passed | Synthetic startup/refresh/outage/revocation scenarios |
| `npm.cmd run test:localization` | Passed | Formatting/localization boundary and registered scripts |
| `npm.cmd run test:invitations` | Passed | Existing customer invitation assignment checks |
| `npm.cmd run test:public:analytics` | Passed | Consent, redaction, route exclusions, SDK failure isolation |
| `npm.cmd run build` | Passed | Next production compile, type check and generation of 85 pages; no deployed-stack validation |
| Phase 0 DTO checks | **17 passed**, **46 schemas exported** | Shape/boundary examples, not domain/API integration tests |
| Synthetic legacy inventory | Passed | Actual ORM schema, synthetic states; no migration executed |
| UI baseline capture | **25 screenshots**, no browser page errors or external origins | Actual presentation components with synthetic services and disabled CRM effects |
| Graphify runtime repair | Passed, same `graphifyy==0.9.41` on Python 3.12 | Graph query unavailable because this checkout has no graph |

Backend test files:

```text
tests/test_platform_auth.py
tests/test_superadmin_guard.py
tests/test_superadmin_dashboard.py
tests/test_superadmin_organizations.py
tests/test_superadmin_login_history.py
tests/test_superadmin_feedback.py
tests/test_startup_pipeline_data_preservation.py
tests/test_startup_preserves_pipelines.py
```

Backend warnings are existing dependency deprecations, including Starlette/AnyIO, httplib2/pyparsing, Passlib/Argon2 and jose datetime handling. No assertion failed in the selected suite. No full backend suite was run.

## Visual reference and verified gaps

See [the screenshot index](README.md#visual-references) and machine-readable [capture manifest](ui-captures.json). Captures share Edge **154.0.4258.62**, en-US/UTC, actual Instrument Sans Latin WOFF2, real compiled global Tailwind CSS, device scale 1 and reduced motion. Widths: 1440, 768 and 390 pixels; CRM also has a collapsed desktop capture. No external network request was needed. The capture harness checks font and image loading and rejects browser exceptions.

The CRM reference mounts the actual `DashboardShell`, `Sidebar`, `Header` and `AdminPageHeader` around a labelled synthetic sample body. It is a component reference, not a screenshot of a shipped `/dashboard/reference` route. Platform captures mount the actual layout and seven existing page components. The harness explicitly lists disabled CRM hooks/effects in its manifest, including billing, organization, SSE, onboarding, AI side panel and notifications. It does not establish full Next routing, middleware, authentication, mobile navigation or real API behavior.

Observed/source-backed work for Phases 2/3:

1. CRM sidebar is 236px expanded / 64px collapsed. Platform remains 256px, including at 390px width. The mobile platform screenshots show severe squeezed/clipped content. A document-width-only overflow test would miss this defect.
2. CRM has a 64px header and inset white workspace with shared tokens; platform has a separate full-height shell, custom metadata labels and hardcoded colors. [CRM shell](../../crusource-crm-frontend/src/components/layout/DashboardShell.tsx), [platform shell](../../crusource-crm-frontend/src/app/superadmin/layout.tsx), [platform sidebar](../../crusource-crm-frontend/src/components/superadmin/SuperAdminSidebar.tsx).
3. Platform overview/sidebar make fixed “ALL SYSTEMS HEALTHY”, “ONLINE” and “CONNECTED” claims without those displays being driven by measured health data. Replace with measured/unknown states in the planned health work; do not carry decorative claims into the redesign.
4. Platform layout treats failed identity reads as authentication failure, including service/network errors. Distinguish these states before privileged UI work.
5. Existing Super Admin query keys omit platform identity/capability revision and some hooks are always enabled. Add identity gating and cache lifecycle rules rather than copying these patterns to new features. [Current hooks](../../crusource-crm-frontend/src/hooks/queries/useSuperAdmin.ts).
6. Organization/feedback/login filters use local state; trial-extension filters use Redux. Move shareable filters/pagination to URL state in the page-refactor phase. TanStack remains the server-state owner.
7. Shared table/dialog compatibility requires review: server pagination must not slice a loaded server page again; privileged async dialogs must stay open on failure. Reuse primitives with focused options rather than copying an entire organization-dependent shell.

## Authentication, delivery and added feature findings

- Platform is already a separate cookie/password/MFA identity domain. Removing developer terminology/public applications must preserve that boundary, not replace it with ordinary CRM login. [Sessions/guards](../../crusource-crm-backend/src/modules/platform_auth/services/sessions.py).
- The legacy approval handler combines resend with sign-in reset for activated users and calls email before commit. Split resend/reset and introduce a committed platform-delivery intent. A successful current test is not proof that the existing email/transaction boundary is reliable.
- Activation and MFA completion depend on legacy access-request status/email lineage. Preserve valid links/enrollment during migration and migrate completion explicitly. [Migration checklist](MIGRATION_CHECKLIST.md).
- Existing organization-owned RecordEffect delivery cannot accept organization-free platform invitation work without violating its current contracts. Reuse scheduler/lease/retry patterns through a focused platform outbox.
- `PublicInformation.tsx` is informational; `ContactSalesModal.tsx` shows local success without a persisted demo request. Neither establishes a demo queue/board. Add the requested public form in Phase 4, including honest acknowledgement after storage.
- Existing UserFeedback is a rating/suggestion/issue record, not a support conversation. Phase 5 needs scoped tickets/messages and separate customer/platform DTOs. Customer internal-note isolation must happen before serialization and pagination.
- CRM trial-expiry lockout currently permits selected billing/organization/platform paths. Support needs an intentional route/API exception while retaining identity/tenant authorization.

## Graphify

The installed launcher referenced a removed Python 3.10 executable. It was reinstalled at the same package version, 0.9.41, with installed Python 3.12; `graphify --help` succeeds. The post-repair focused query correctly reports missing `graphify-out/graph.json`. No graph was claimed or regenerated, and no provider key/semantic extraction was used. Source inspection supplied the load-bearing evidence. Future source work must run the project Graphify update workflow when a graph is available.

## Remaining release evidence

Real PostgreSQL migrations/races, deployed database state, staging domains, real SES acceptance/bounce/retry, worker restart/recovery, full routed invitation/demo/support flows, accessibility and the Phase 2/3 visual acceptance matrix remain later-phase checks. The opt-in PostgreSQL auth tests were not enabled against an unverified database. This phase makes implementation reviewable and reproducible; it does not promise absence of all future bugs.
