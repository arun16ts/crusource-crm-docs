# Forecast — Implementation and Validation

## Result

The reported Forecast fixes and related access/data-correctness changes are implemented locally. **Full frontend CI remains blocked by an existing editor-compatibility browser failure.** Nothing has been deployed.

The Superadmin design documents and VMS repositories were not changed.

## Changes

| Area                  | Resulting behavior                                                                                                                                                                                                                                                                      |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manager access        | Target Management uses resolved Forecast permissions and management authority, including custom team leaders and supported manager roles. Create, edit, and delete controls are independent.                                                                                            |
| Team selection        | Admins can choose all teams, a specific team, or unassigned users. Managers receive their managed team choices. Selection reaches summaries, targets, eligible assignees, banners, and drilldowns.                                                                                      |
| Read and write scope  | Own/team/all Forecast read permissions are respected. Assigning or changing another person's target requires an actual management relationship, not just visibility of that person.                                                                                                     |
| Target creation       | Duplicate creation returns 409 without overwriting a target. Editing uses the separately authorized update endpoint. Concurrent duplicate inserts are handled against the existing unique constraint.                                                                                   |
| Stage scrolling       | The settings card no longer shrinks and clips its content. The stage table has bounded vertical/horizontal scrolling and a keyboard-focusable region; Save remains reachable.                                                                                                           |
| Probabilities         | Writes identify stages by ID; legacy name requests remain supported. Unknown/duplicate stages, invalid ordering, and terminal values other than won=100/lost=0 are rejected before writes. Invalid pipeline IDs cannot fall back to the default pipeline.                               |
| Drafts and errors     | Probability refetch/pipeline changes protect unsaved edits. Targets, summaries, and probability settings distinguish failed requests from empty data. Restricted tabs fall back to Overview.                                                                                            |
| Currency              | Currency filters apply to hygiene banners and correction drawers. Values use their actual currency; mixed sums are labeled explicitly, and incompatible target comparisons are suppressed. New targets store their currency; currency-null legacy targets use the organization default. |
| Close-date correction | Changing a date preserves manual deal selection. The default date comes from the selected month/quarter. Scope changes remount the correction drawer.                                                                                                                                   |
| Rollups               | Manager rollups exclude personal metrics consistently from member rows and team drilldowns. Personal drilldowns are explicitly distinguished from team drilldowns.                                                                                                                      |
| Architecture          | The route delegates to a feature workspace. Shared scope policies use scoped repositories; new management queries have dedicated handlers. Forecast probability reads no longer seed pipelines. Close-date writes and audit records share a command transaction.                        |
| View state            | Shareable Forecast filters and tabs use URL state; drawer state remains in the existing UI store. Target rows use API-provided names instead of fetching the general user directory again.                                                                                              |

No database schema migration or dependency change was required. Existing currency values were not converted or backfilled.

## Validation evidence

| Check                                | Result                                                                                                                                                                                                                                  |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Focused Forecast backend regressions | 44 passed, including endpoint permission checks, own-only peer isolation, managed-user assignment, team membership deduplication, duplicate creation, pipeline rejection, terminal probabilities, read purity, and currency comparisons |
| Complete backend suite               | All 2,105 collected tests across 225 files were run in two independent batches: 2,035 passed and 70 skipped                                                                                                                             |
| Backend static checks                | Full Ruff check and Python compilation passed                                                                                                                                                                                           |
| Disposable service checks            | Committed migrations, required Redis regressions, PostgreSQL transaction/locking regressions, platform regressions, migration upgrade/downgrade checks, and Alembic model drift passed                                                  |
| Frontend dependency installation     | Clean lockfile installation passed in an isolated checkout using Node 20                                                                                                                                                                |
| Frontend standard checks             | Standard test scripts, spreadsheet regressions, Loop/public contracts, formatting, type checking, lint, production build, and dependency audit passed; lint retains existing repository warnings                                        |
| Forecast browser regression          | Passed against rendered components with generated Tailwind CSS: manager/team-leader controls, team filtering, scrolling/Save access, stage-ID payloads, failed-request messaging, selected-period dates, and preserved deal selection   |
| Required frontend browser checks     | Passed except the existing editor-compatibility test described below                                                                                                                                                                    |
| Graphify                             | Refreshed after implementation; existing TSX parser limitations remain                                                                                                                                                                  |

Backend test skips are reported explicitly. Required opt-in service checks were run separately against disposable local PostgreSQL and Redis, without using stage or production data.

The first sandboxed full backend run encountered temporary-directory access errors; approved reruns and the final full test batches passed.

## Remaining frontend CI blocker

`tests/test_editor_compatibility_browser.mjs` expects a hyperlink to be inserted into an existing rich-text note. The resulting HTML contains the formatted note but no expected hyperlink. This reproduces against unchanged editor code using Node 20 and is independent of the Forecast changes.

Evidence: [isolated CI failure](../../../validation/archive/historical-logs/forecast-frontend-test-editors-browser.log) and [unchanged editor reproduction](../../../validation/archive/historical-logs/forecast-editor-baseline.log).

Until that failure is resolved, this change must not be described as fully green for stage promotion. Browser checks used fixtures; the originally reported account and deployed stage application have not been verified.

## Upgrade queue

The optional product upgrades remain in [the implementation plan](FORECAST_IMPLEMENTATION_PLAN.md): pipeline coverage/pacing indicators, bulk target allocation, a dedicated change-history view, snapshots/trends, risk explanations, and scenario previews. Server pagination and broader domain-layer cleanup also remain separate follow-up work.

## Review entry points

- [Forecast UI](../../../crusource-crm-frontend/src/components/forecast/ForecastWorkspace.tsx)
- [Forecast URL filters](../../../crusource-crm-frontend/src/components/forecast/hooks/useForecastFilters.ts)
- [Stage probability settings](../../../crusource-crm-frontend/src/components/forecast/StageProbabilitySettingsCard.tsx)
- [Backend scope policy](../../../crusource-crm-backend/src/modules/forecast/services/forecast_scope.py)
- [Scoped repository](../../../crusource-crm-backend/src/modules/forecast/repositories/forecast_scope_repository.py)
- [Backend regressions](../../../crusource-crm-backend/tests/test_forecast.py)
- [Browser regression](../../../crusource-crm-frontend/tests/test_forecast_browser.mjs)
