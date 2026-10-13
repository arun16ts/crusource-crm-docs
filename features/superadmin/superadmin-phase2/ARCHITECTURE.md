# Phase 2 architecture

## Boundaries

`src/app/superadmin/layout.tsx` is a thin server entry. `PlatformLayout` selects public entry screens or the protected session/workspace boundaries. `WorkspaceFrame` contains presentation slots and layout geometry only. Both CRM `DashboardShell` and `PlatformWorkspace` compose it; CRM billing, onboarding, SSE, permission and AI behavior remains in the CRM wrapper.

Platform navigation lives in `platformNavigation.ts`. The sidebar reuses CRM `SidebarBrandHeader` and `SidebarNavItem`. Mobile navigation and action dialogs use the installed Base UI dialog implementation. Shared `DataTable` retains its default client-pagination behavior and adds an explicit server-pagination contract plus keyboard sorting and an optional focusable scroll region.

## State ownership

| State | Owner and implementation |
|---|---|
| Identity and API entities | TanStack Query through `usePlatformAuth`, `usePlatformAccess`, existing Super Admin hooks and typed services |
| Protected cache scope | Staff ID and session epoch in every protected query key; complete response-affecting list parameters included |
| Tab, search, invitation status, sort, page and page size | URL through `usePlatformAccessView`; invalid values normalized, history preserved |
| Shared sidebar collapse | Redux `platformUi` slice and a dedicated platform localStorage preference |
| Mobile overlay, drafts, selected action/record ID | Local component state |
| Idempotent command retry | Local exact submitted body plus UUID key; no automatic privileged write retries |

No fetched entities are mirrored in Redux. No credentials, invitation tokens, MFA material or command bodies are persisted in browser storage. Activation fragments are captured once and removed immediately, including React StrictMode's repeated effect setup. Enrollment material is nonpersistent, has zero cache retention and is cleared on exit.

## API and backend

Feature components call focused hooks; hooks use services; services use `platformHttpClient`. The platform transport uses same-origin cookies, `X-Platform-Request`, CSRF for authenticated writes and `Idempotency-Key` for access commands. It never invokes CRM bearer-token refresh. Typed errors retain safe request references and field/version details; requests and response-body reads have a bounded timeout and AbortSignal support.

The backend's existing commands, queries, handlers, repositories and services remain the domain owners. No business rules moved into React. Commands include expected versions and reasons where required, invalidate lists after completion and never optimistically claim a privileged write succeeded. A lost response retains the exact action body/key. A 409 version/idempotency conflict requires a refreshed review. The narrow backend change distinguishes precommit delivery-configuration rejection from ambiguous failures.

## Session isolation

`PlatformSessionBoundary` separates loading, signed-out, forbidden, offline and service failure. A sign-out attempt blocks the workspace until confirmed, and can be retried. Selective cleanup cancels/removes platform queries and mutation records while preserving CRM state. Cross-tab platform session notifications invalidate other platform views. Query and mutation 401 failures clear platform access; scoped keys and cancellation prevent old identity responses from becoming another staff account's UI.

Platform pages use pure shared formatters with explicit UTC/date/number preferences, avoiding the CRM user-preference hook. Nested platform EN/NL messages inherit the application locale. Marketing analytics explicitly exclude platform hosts, including short `/` aliases.

## Test infrastructure

The functional harness bundles real feature components/providers with compiled Tailwind CSS and deterministic API doubles. The separate route suite runs real Next.js routing/proxy and real FastAPI guards/handlers against an in-memory SQLite database and fake mail/rate admission. A fixture-only keyed control endpoint obtains activation material in memory; it is never registered in the application. Requests are serialized in that SQLite fixture because it shares one connection; PostgreSQL concurrency evidence remains in Phase 1.

`NEXT_DIST_DIR` and `NEXT_TSCONFIG_PATH` isolate test build/type output from a running development server. Normal defaults remain `.next` and `tsconfig.json`. `NEXT_PUBLIC_CRM_ORIGIN` may explicitly configure the header's CRM destination; existing trusted host mapping provides the development fallback.
