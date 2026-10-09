# Active activity timelines and post-pull validation — 2026-10-08

## Confirmed behavior

This follows the entity activity audit and the merges from `dev` and `dev-advaith`. The earlier performance changes remain present. The local chat database was already at `20261008_chat_response_kind`; the guarded migration check verified the column and unchanged business/chat record counts. No schema change was needed in this batch.

Authenticated localhost inspection reproduced broad reads when opening the Timeline of an existing Task linked to a deleted Contact. `useGlobalTimeline` fetched scoped collections and filtered them in JavaScript, outside TanStack Query. Its effect could repeat these reads after remounting or formatting changes.

| Timeline collection | Observed before | Current implementation |
| --- | --- | --- |
| Tasks | `/tasks` without a page limit | Related `/tasks/page`, limit 50 |
| Meetings | `/meetings?skip=0&limit=100000` | Related `/meetings/page`, limit 50 |
| Calls | Automatically traversed related 500-row pages | Related 50-row pages with explicit continuation |
| Deals | Unfiltered global first page, even for non-Contact parents | Contact-only server filter and 50-row continuation |

The old unfiltered Deals request transferred 69,164 bytes in this Task scenario. This capture did not measure completed bytes for the broad Task/Meeting responses; the earlier entity audit's 100 MB measurement is a different scenario and is not reused as this batch's before measurement.

## Changes and preservation

- The shared timeline now composes cached entity, note, related-activity and Contact-Deal queries. Task, Call and Meeting modals/drawers expose loading, errors, retry and continuation. The Meeting detail drawer now gates the timeline on its active tab too.
- Parent IDs, legacy Contact-name matching, normalized attendee email, attendee Contact/User matching and Contact Deal notes remain supported. Deleted-parent 404s do not block visible activity reads; other request failures remain visible.
- The new optional `contact_id` Deal filter is applied before count and pagination using the existing scoped repository. Stable ID ordering breaks timestamp ties. Existing personal assignment, team, tenant, deletion and field-permission rules are retained. No authorization shortcut or bulk endpoint limit change was introduced.
- Contact detail drawers use these related Deal pages only on Timeline, replacing the first-global-page filter that could omit later related Deals.
- Queries retain module-root invalidation, one-minute freshness for related pages, and cancellation signals on entity, note and collection requests. Closing a consumer disables new reads; formatting events no longer trigger a fetching effect.
- A failed continuation retries that page and retains already loaded data. Contact Deal notes are cached per loaded Deal; consolidating that fan-out remains separate work.

## Browser evidence

The same existing Task timeline now requests related collections with limits of 50. A deleted parent remains a valid empty-timeline case. Switching Overview → Timeline again generated no additional requests in the fresh-cache interval.

A real imported Contact's Timeline made four related collection GETs, all successful: Tasks, Meetings, Calls and Contact-filtered Deals. This Contact had no matching children; their response bodies totaled **88 bytes**, excluding headers, CORS and shell requests. The Contact creation event remained visible, and switching away/back generated no additional collection GETs.

Imported records inspected here do not demonstrate populated continuation. The browser regression separately uses 65 Tasks/Calls/Meetings and 51 related Deals, with a complete 50-Deal first page. It verifies continuation, Deal notes, retained data on a failed next page, retry, closed-consumer invalidation and no Deal reads for a Lead timeline. Backend fixtures cover 125 matching Deals after 80 newer unrelated Deals, tied timestamps and all three roles. These fixtures are not stage evidence.

No imported business records were edited. The live chat greeting check added a greeting to local chat history and verified persistence across refresh. Closed chat made no history request; opening history and streaming both returned 200.

## Validation

Eight baseline backend failures were reproduced, then corrected in the test fixtures: seven used incomplete Deal/conversion inputs, and one SES fixture lacked required thread metadata. Required fields, authorization checks and the SES missing-metadata safeguard were retained. All 87 focused tests passed. The API contract expectations were also updated for the intentional `contact_id` query parameter.

- Final backend: Ruff, compilation, committed migrations, **1,692 passed / 18 skipped** in the full suite, ten opt-in PostgreSQL regressions, the separate empty-database migration-drift test and `alembic check` passed.
- Final frontend snapshot `fcc45e05` passed clean lockfile installation, changed-file formatting, full lint, all unit/spreadsheet tests, TypeScript, every current CI browser command including the expanded 51-Deal regression, additional session-startup/Loop AI checks, safe production build and dependency audit. All modified/new frontend files match that isolated snapshot byte for byte. The interrupted installation was restarted; final results were written after the successful rerun.
- Frontend incoming style issues were formatted; lint still reports existing warnings. Backend deprecation warnings remain. These are successful local CI-parity checks, not remote CI/deployment results.

Checks use Node 20 and the Python 3.12 venv. PostgreSQL/Redis test services on 15432/16379 and separate disposable test/drift databases are isolated from the application's 5432/6379 services. Evidence is under `.worktrees/post-pull-validation-20261008/` and `.worktrees/global-timeline-20261008/`.

The two named disposable audit containers were removed after validation. Graphify's code graph was updated after source/test changes. Existing missing HCL/SQL parsers, an empty pyproject extraction and five unrelated partial TSX parses remain coverage limitations.

The final readiness recheck after the interruption found no listener on localhost:8000, including outside the restricted network profile. The successful live Task, Contact and chat checks above occurred before that interruption; further running-application checks require the backend to be started again.

## Database findings and remaining work

Page reads now materialize related rows instead of downloading the full Task/Meeting datasets. Matching Deal filters affect both count and rows before serialization. Counts still require database work: a read-only PostgreSQL `EXPLAIN ANALYZE` for the inspected empty meeting relation took **246.48 ms**, scanning the scoped meeting data and attendee subplans. No index or planner-setting change was made without further profiling.

Remaining priorities:

Follow-up: [Account Contacts audit](account-contact-loading-audit-2026-10-08.md) fixes item 2 below and verifies that the current global-search path already uses bounded server queries. The list below records the earlier batch's remaining state.

1. Batch or page Contact Deal notes to reduce per-Deal requests when many Deals are related. Notes for one parent are also not uniformly paginated.
2. Replace Account related-Contacts' first-global-page filter with a scoped paginated contract.
3. Bound Kanban columns, campaign recipient/composer lookups, global search and meeting conflict/context reads; complete dense connected Calendar and concurrency checks.
4. Profile count/relationship queries with representative volumes before selecting indexes or changing count behavior.
5. A unified chronological event cursor remains separate: module pages are sorted and merged locally, and derived event timestamps can differ from each module's ordering. Continuation keeps matched records reachable but does not promise one global chronological cursor.
6. Native `--reload` temporarily stopped responding with the audit browser open during source updates; releasing the browser restored readiness. The SSE/reload lifecycle needs separate diagnosis; this does not establish a production failure.

Font configuration was unchanged in this batch; the earlier self-hosted Instrument Sans fix remains present. No push, deployment or stage verification was performed. Deploy the backend `contact_id` contract before its frontend consumers.
