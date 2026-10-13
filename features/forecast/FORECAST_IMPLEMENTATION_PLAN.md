# Forecast — Bug Fixes and Improvement Plan

**Status:** Proposed implementation plan; application code unchanged.  
**Scope:** CRM Forecast frontend, FastAPI Forecast endpoints, shared permission integration, and regression coverage.  
**Evidence:** Source inspection and the existing Forecast backend tests: **28 passed**. Browser behavior and the affected test user's saved profile have not yet been reproduced or inspected. This is not a complete security audit or full CI result.

## 1. Reported issues

| Report                               | Verification                                                                                                                                                                                                                                                                                                                                                                                            | Planned change                                                                                                                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manager cannot see Target Management | The UI accepts only raw roles `admin` and `sales_manager`. It ignores resolved profile permissions and `can_lead_teams`. Backend creation also hard-codes `sales_manager`, although shared `Scope.is_manager` supports manager aliases and leadership capabilities. A raw `sales_manager` should already see the tab; confirm the affected user's actual role/profile before declaring the exact cause. | Use resolved permissions and management authority consistently in UI and API. Separate viewing targets from create/edit/delete rights.                                                                      |
| Admin cannot switch teams            | Confirmed missing capability: Forecast header, summary, deals, and target-list contracts have no team selection. Admin summary aggregates active organization users, not a selected team.                                                                                                                                                                                                               | Add a team selector and server-enforced team scope across summary, targets, assignees, and drilldowns.                                                                                                      |
| Stage Probabilities does not scroll  | The page has a flex-column scroll container, but the settings card can shrink and clips overflow; its table has only horizontal overflow handling. This is a plausible cause, not a browser-confirmed diagnosis.                                                                                                                                                                                        | Reproduce with a long stage list and short viewport. Establish one bounded vertical scroll region, prevent unintended flex shrinking, and keep Save reachable. Verify wheel, touch, and keyboard scrolling. |

## 2. Recommended access and team behavior

| User                           | Forecast access                    | Target management                                                                               | Team selection                                | Probability changes                         |
| ------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------- |
| Organization Admin             | All permitted organization records | All organization targets                                                                        | All teams, individual team, unassigned users  | Existing customization permission           |
| Manager / eligible team leader | Permitted managed scope            | View/create/edit targets for authorized managed users and self, subject to Forecast permissions | Authorized managed teams; own/reporting scope | Only with explicit customization permission |
| Standard profile               | Own permitted Forecast records     | Own target read-only by default; no management controls                                         | No organization-wide selection                | No changes by default                       |

Explicit profile denials remain effective. Manager status alone does not bypass permissions. Keep delete governed independently; current manager defaults deny Forecast delete.

Team membership and reporting hierarchy are different concepts. A team selection uses actual team membership, intersected with the caller's permitted scope. A user's presence in `visible_user_ids` is not by itself evidence that the caller manages them. Users in multiple teams must not be double-counted in the all-teams view.

Recommended UI: **Team → Member → Period → Pipeline → Currency**. Organization Admin's default is All Teams; a manager's default is their authorized managed scope. Preserve the chosen team across Overview and Target Management. Stage probabilities remain pipeline settings and are independent of team selection.

## 3. Additional findings

Priorities: **P1** access or materially wrong data/action; **P2** reliability and interaction; **P3** maintainability/performance.

| Priority | Finding and evidence                                                                                                                                                                                                                                                                                 | Remediation                                                                                                                                                                                                                                                                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1       | Forecast handlers use the broad `visible_user_ids` list directly. Shared scope resolution includes peer memberships, while module permissions can specify `own`, `team`, or `all`. Forecast reads do not apply that module-specific view scope. Target create treats visible users as managed users. | Introduce an explicit Forecast read-scope resolver and a separate target-management policy. Test own-only users with teammates and managers who have peer memberships. Potential object-authorization weakness: OWASP API1 / ASVS V4 / CWE-863; source-confirmed policy mismatch, exploitability requires endpoint regression verification. |
| P1       | Admin target listing uses `visible_user_ids`, while admin summary separately loads all active organization users. This can show an incomplete target table compared with summary totals.                                                                                                             | Resolve effective user IDs consistently for each use case; keep organization boundaries and view/write permissions.                                                                                                                                                                                                                         |
| P1       | POST target creation silently updates an existing target. The route requires create permission, so an existing target can be overwritten without the edit permission used by PUT. The handler docstring and drawer expect a duplicate conflict.                                                      | Make POST create-only with a structured 409 response. Edit existing targets through PUT and its permission checks. Handle concurrent creation against the existing unique constraint. Potential function-authorization weakness: OWASP API5 / ASVS V4 / CWE-862.                                                                            |
| P1       | An explicit invalid or foreign pipeline ID falls through to default-pipeline seeding in the repository. Probability writes can consequently address the caller's default pipeline rather than reject the requested resource.                                                                         | Validate explicit pipeline ownership/existence and return 404. Default resolution is allowed only when no ID was supplied. Never mutate another pipeline as a fallback.                                                                                                                                                                     |
| P1       | Currency filtering occurs after missing-date and slipped-deal banners are accumulated. The correction drawer does not receive selected currency. Targets have a currency column, but create/update payloads do not capture it; Forecast cards format totals using the user's display currency.       | Apply currency scope before all buckets, pass it to correction drawers, label monetary values with their actual currency, and compare attainment only for compatible target/deal currencies. Do not silently relabel or convert amounts. Establish a safe policy for existing currency-null targets.                                        |
| P2       | Backend probability validation relies on stage names, skips adjacent pairs containing “lost,” and does not enforce won=100/lost=0. Unknown stage names can be ignored by repository updates while returning success.                                                                                 | Use stage IDs and stage types. Validate known stages, reject duplicate/unknown IDs, enforce terminal probabilities, and compare consecutive open stages after excluding lost stages. Keep client validation helpful and server validation authoritative.                                                                                    |
| P2       | Probability forms replace edits whenever query data changes. Target lists/settings do not expose query failures distinctly from empty data.                                                                                                                                                          | Track dirty state, guard pipeline changes/refetch, support Reset, disable invalid/unchanged saves, and distinguish loading/empty/error/stale states.                                                                                                                                                                                        |
| P2       | An out-of-scope requested drilldown user silently falls back to the caller's own deals.                                                                                                                                                                                                              | Return an explicit denial or safe not-found response. Never display another scope under the requested user's label.                                                                                                                                                                                                                         |
| P2       | Manager team summary excludes self, but the member table receives all user summaries and team drilldown requests no explicit member set.                                                                                                                                                             | Define the rollup population once and reuse it for table rows, totals, and team drilldowns. Show the manager's personal metrics separately when excluded.                                                                                                                                                                                   |
| P2       | Quick close-date selection resets all deals when the target date changes. Its default date is the current month's end even when viewing a different month/quarter.                                                                                                                                   | Initialize once per opened scope, preserve manual selection, and default from the selected Forecast period.                                                                                                                                                                                                                                 |
| P2       | A previously selected restricted tab is stored in Redux; a user without its permission can get no visible content instead of Overview.                                                                                                                                                               | Resolve active tabs against current permissions; return to Overview after role/session changes.                                                                                                                                                                                                                                             |
| P3       | Target table fetches users again although its API already returns names/emails; target relationships are not eagerly loaded. Large targets/deals are returned without pagination.                                                                                                                    | Consume existing response metadata, use a focused authorized assignee query, eagerly load required target relationships, then add server pagination and aggregate queries where volume warrants it.                                                                                                                                         |

## 4. SOLID, CQRS, and DRY review

The module already has routes, command/query handlers, repositories, separate frontend query/mutation hooks, and shared deal classification. Keep these useful boundaries.

Specific improvements:

- **CQRS:** probability GET can seed pipelines and commit; the read repository can also create a pipeline. Move initialization into an explicit setup/provisioning command. Reads should return existing state or an explicit empty/not-found response.
- **Single responsibility:** handlers query users directly while repositories also own persistence. Move scoped user selection to repositories; keep authorization/domain decisions in focused policies/services.
- **DRY:** admin/manager selection differs between targets, summary, deals, and the frontend. Centralize policy decisions without merging read visibility and write authority into one flag. Share period conversion and probability rules within their respective layers.
- **Transaction ownership:** close-date updates commit inside the repository, while target commands commit in handlers. Use one command transaction boundary so updates and audit records succeed or roll back together. Probability changes also need audit coverage.
- **Frontend state ownership:** move shareable tab/team/member/period/pipeline/currency filters into URL state; keep server results in TanStack Query and drawer/UI state local or in existing Redux. Avoid keeping the same filter authoritative in two stores.
- **Dependency boundaries:** domain calculation/validation should not depend on HTTP exceptions or framework globals; translate domain failures at the application/API boundary during focused refactoring.

Do not introduce generic factories, interfaces for every function, or a module rewrite solely to claim SOLID compliance. No specific Liskov-substitution violation was established.

## 5. Implementation sequence

### Phase 1 — Reproduce and lock down policies

1. Inspect the affected manager's resolved role/profile, Forecast permissions, team leadership, and subscription state using authorized fixtures/accounts.
2. Reproduce the tab issue and stage scrolling with Admin, Manager, custom team leader, and Standard profiles.
3. Add failing endpoint regressions for own-only peer scope, unmanaged target users, create-without-edit overwrites, and invalid pipeline IDs.
4. Implement shared Forecast read scope and target-management policies, then use resolved frontend capabilities for each control. Reject unsupported actions at the API, not just in the UI.

### Phase 2 — Reported UI fixes and team selection

1. Fix Stage Probabilities scroll ownership and flex sizing; retain terminal-stage locks and accessible controls.
2. Reuse authorized team metadata and add team/member selection. Extend typed API parameters and query keys with every scope-affecting filter.
3. Apply the same selected team/member scope to summaries, targets, eligible assignees, banners, correction drawers, and drilldowns. Keep pipeline settings independent.
4. Add explicit all-teams/unassigned states, deduplicated membership resolution, permission-aware tab fallback, and proper loading/error/empty states.

### Phase 3 — Forecast correctness and command safety

1. Fix create-versus-edit semantics and duplicate-target handling; allow zero targets consistently or reject them consistently after confirming the business rule.
2. Align currency filtering/labels and target currency compatibility. Backfill only where historical currency is known; otherwise mark it for review.
3. Replace stage-name writes with stage-ID contracts on both sides; enforce typed terminal and ordering rules and atomic updates.
4. Preserve probability drafts and quick-close-date selections; align member tables, rollups, and drilldown totals.
5. Move seeding out of queries and transaction commits out of repositories; add command audit coverage.

### Phase 4 — Improvements

Choose these after the reported fixes and access/correctness findings are resolved:

| Upgrade                           | Benefit                                                                                               | Suggested order |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------- |
| Coverage and pacing indicators    | Show required pipeline coverage and whether actual results are keeping pace; identify missing targets | First           |
| Bulk target allocation            | Allocate a team quota across members, preview totals, and report per-row validation before saving     | First           |
| Target/probability change history | Show who changed an amount or weight, previous/new values, time, and reason                           | First           |
| Forecast snapshots and trends     | Compare this week's forecast with prior snapshots and show what changed                               | Next            |
| Risk explanations                 | Identify overdue dates, missing dates, stale opportunities, and concentration in a few deals          | Next            |
| Scenario preview                  | Preview alternative probabilities/targets without changing live settings; explicitly apply separately | Later           |

Coverage, snapshots, and scenarios must use compatible currencies and a documented scope. These are proposed upgrades, not existing capabilities.

## 6. Verification and completion criteria

- Admin can select organization teams and see matching members, targets, rollups, and drilldowns.
- Manager/custom leadership access follows resolved Forecast permissions and authorized managed scope; Standard own-only users cannot see peer Forecast records.
- API tests deny cross-organization, unmanaged-user, and invalid-pipeline requests. POST cannot bypass edit authorization.
- Long stage lists scroll at short desktop and mobile heights; the last row and Save remain reachable by wheel, touch, and keyboard.
- Terminal stages and arbitrary custom stage names/types validate correctly; invalid updates are atomic and auditable.
- Summary cards, banners, correction drawers, and drilldowns agree for the same filters; currency labels and target comparisons are accurate.
- Dirty forms survive refetch; changing a correction date preserves deal selection; restricted/stale tabs resolve safely.
- Add a named Forecast browser regression script to frontend CI; current Forecast coverage is primarily backend handlers with manually supplied scopes.
- Run the affected repositories' full applicable CI checks from their current workflows after implementation: frontend lockfile install, formatting, lint, tests, spreadsheets, type check, required browser regressions, build and audit; backend Ruff, compilation, full tests and required disposable PostgreSQL/migration checks. Run migration/backfill checks if schema changes are introduced.
- Refresh Graphify after code changes. Local verification does not establish stage success; deployment remains a separate authorized task.

## 7. Source references

- [Forecast role/tab state](../../../crusource-crm-frontend/src/components/forecast/hooks/useForecastPageState.ts)
- [Forecast page layout](../../../crusource-crm-frontend/src/app/dashboard/forecast/page.tsx)
- [Target management UI](../../../crusource-crm-frontend/src/components/forecast/TargetManagementView.tsx)
- [Stage probability form](../../../crusource-crm-frontend/src/components/forecast/StageProbabilitySettingsCard.tsx)
- [Quick close-date drawer](../../../crusource-crm-frontend/src/components/forecast/QuickCloseDateDrawer.tsx)
- [Frontend permission helpers](../../../crusource-crm-frontend/src/hooks/usePermissions.ts)
- [Forecast endpoint permissions](../../../crusource-crm-backend/src/modules/forecast/routes/forecast_routes.py)
- [Target handlers](../../../crusource-crm-backend/src/modules/forecast/handlers/target_handlers.py)
- [Summary handler](../../../crusource-crm-backend/src/modules/forecast/handlers/get_forecast_summary_handler.py)
- [Drilldown handler](../../../crusource-crm-backend/src/modules/forecast/handlers/get_forecast_deals_handler.py)
- [Forecast repository](../../../crusource-crm-backend/src/modules/forecast/repositories/forecast_repository.py)
- [Probability rules](../../../crusource-crm-backend/src/modules/forecast/services/forecast_service.py)
- [Probability update handler](../../../crusource-crm-backend/src/modules/forecast/handlers/update_stage_probabilities_handler.py)
- [Shared scope resolution](../../../crusource-crm-backend/src/shared/auth/scope_guard.py)
