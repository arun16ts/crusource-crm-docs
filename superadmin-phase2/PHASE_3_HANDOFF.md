# Phase 3 handoff

Phase 2 completes the shared platform shell and staff-access UI. Phase 3 redesigns the contents of all existing Super Admin pages: overview, organizations/list/detail, login history, trial extensions and feedback. Use the approved [phase-wise scope](../SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md#phase-3--all-existing-super-admin-screens).

Reuse `WorkspaceFrame`, platform navigation/session context, shared headings/buttons/tables/dialogs and pure platform formatters. Keep thin route entries. Extend services before query hooks, retain identity-scoped keys and forward AbortSignal for reads. Server state belongs to TanStack Query, shareable filters belong in the URL, and Redux remains reserved for shared client UI state. Backend gaps go through existing query/command handlers and repositories with current guards.

Do not reintroduce CRM user-preference, billing, onboarding, notifications or SSE hooks into the platform wrapper. The existing CRM frame has a pixel comparison suite; preserve it when shared presentation changes. Keep real-route tests isolated from the normal application database.

## Current contract limits

- Invitation API does not expose purpose or enrollment deadline in its DTO. Do not infer/reset a countdown or present unsupported join/reset distinctions.
- Staff listing currently supports search and created ordering, not a server status filter or last-login field. Do not implement client-side filtering on one server page and call it complete.
- Staff capability arrays are not yet an owner capability editor. Capability administration arrives with demo/support access controls in later phases.
- Sent means provider acceptance; delivery retries/failures have separate status. The worker dispatch interval is 30 seconds. Owner actions are versioned and require idempotency keys; reset immediately disables existing staff sign-in and requires re-enrollment.
- The development missing-key incident has been repaired. Deployments must provide their own persistent dedicated delivery key and correct frontend origin alongside SES configuration; frontend error handling must never suppress a real provider/configuration issue.

Demo intake and a staged request board remain Phase 4. Customer-submitted support tickets and the Super Admin support workspace remain Phase 5. Existing master-plan analytics, Error Center and Logs retain their later phases. No placeholder navigation was enabled for these features.
