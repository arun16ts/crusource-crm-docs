# Campaign audience loading audit — 2026-10-08

## Confirmed behavior before changes

Graphify traced RecipientSelector, useCampaignComposerState and useCampaignReviewState to the shared Lead/Contact list hooks. Source verification confirmed each requested a 100,000-row limit and then filtered/paginated locally.

The actual localhost New Campaign wizard downloaded **14,000 Leads and 18,500 Contacts** even though its active Leads table showed 50 rows. Both calls returned HTTP 200. Response bodies were **14,497,150 + 12,713,818 = 27,210,968 bytes**, excluding headers/CORS. The inactive Contacts tab caused the second large read. Composer/review relied on those same full collection caches to find selected recipients.

Lowering their limits alone would have broken all-matching selection, searches beyond the first page, preview reachability and campaign submission. This batch changes the contracts instead.

## Implementation

- Added scoped read use cases on the existing Campaign router: POST `recipient-page` and POST `recipient-ids`. These are read operations using JSON request bodies for potentially large selected-ID lists; they do not create campaigns or send messages.
- Audience repositories apply existing organization, profile, assignment, team and soft-delete scope before filters, count and pagination. Browsing supports name/email/company/title search, status and case-insensitive source filtering, with stable created-at/ID ordering and a maximum 500-row page. Search treats `%` and `_` literally.
- Distinct custom sources remain available across pages. The frontend retains them in TanStack Query and avoids repeating the facet query on subsequent fresh pages. No inactive entity list is prefetched.
- Recipient selection remains client workflow state containing IDs. Explicit “select all matching” requests only scoped IDs with an email, then merges them into the existing selection. It does not silently select only the visible page. Normal browsing never enumerates all IDs.
- Composer/review use selected-ID pages of 50 per selected entity type, with continuation, one-minute freshness, cancellation, retry and shared cache keys. Lead-only campaigns do not read Contacts. Review search executes against the whole selected set, including unloaded rows.
- Sending serializes **all selected IDs**, independent of loaded previews or the current search. The backend resolves names/emails; the new frontend does not need every entity downloaded to construct a complete send payload.
- Campaign creation now delegates batch entity resolution to a scoped repository instead of tenant-only handler queries. The personal Lead assignment rule also applies to Admin personal lists; Contact profile visibility and team ceilings remain intact. Existing provider authentication, quota, suppression, deduplication and scheduling logic remain.
- Reused module permissions and field ceilings. Hidden filters/search are rejected consistently; hidden source fields are removed from responses and source facets. ID eligibility cannot inspect hidden email fields. Audience pages omit unused email-history payloads.
- The former unbounded “All rows” display option was replaced by bounded pages; every row and all-matching selection remain reachable. Existing 25/50/100/250/500 page sizes remain. The inactive tab does not show a misleading zero or incur a separate global count just for its label.
- Loading/errors remain visible. Review does not show an empty-match message while its search is loading. No new Redux entity cache or database migration was introduced.

## Actual localhost comparison

| Scenario | Before | After |
| --- | --- | --- |
| New Campaign, Leads active | 32,500 full records across both modules; 27.2 MB | 50 Lead records; **53,824 bytes**; no Contact collection read |
| Select all Leads explicitly | Selected IDs derived from fully downloaded entities | **14,000 IDs**, **546,009 bytes**, HTTP 200 |
| Open composer with all selected | Relied on full entity collections | 50 selected Leads, **53,738 bytes**, total 14,000 |
| Continue previews | Full collections already resident | Next 50 Leads on demand, **53,720 bytes** |
| Open review | Full entity collection lookup | Reused the 100 loaded previews while retaining 14,000 selected IDs |
| Search selected recipient outside loaded review | Local filtering required all entities | One matching row, **1,147 bytes**, HTTP 200 |
| Activate Contacts | Already downloaded all 18,500 | 50 records, then another 50 on request; total 18,500 |

To verify the outside-page search, a separate authenticated **one-record** Lead GET at skip 13,999 obtained a target email. It was absent from the loaded review, then appeared through the selected-recipient search. This manual audit read was not an application-generated page request.

On a development hard refresh, two initial page POST attempts appeared: one failed with `net::ERR_ABORTED`, and one completed HTTP 200 with 50 rows. Cancellation is retained. This evidence distinguishes a canceled lifecycle request from two completed full responses; it does not prove that no server work began for the canceled request. No production-runtime claim is made from the development request count.

The local draft was canceled back to the Campaign list. The existing campaign remained present. **No campaign was launched and no email was sent.** Imported business data was not edited.

A final mixed-selection check chose one real Lead and one real Contact. Each selected-recipient read returned exactly one record, HTTP 200; composer showed two preview options and review retained two recipients. This draft was also canceled.

## Database evidence and limits

A read-only local PostgreSQL plan for the former Lead row request returned **14,000 rows in 32.61 ms**; the bounded request returned **50 rows in 0.371 ms**. Its scoped count took **8.413 ms**. These are individual local plan samples, not production latency guarantees; they omit application serialization, network time and facet work.

The main reductions are bounded ORM materialization/serialization, omission of email history, elimination of inactive Contact reads, selected-only previews and avoiding repeat source facets during pagination. Counts still perform database work. Explicit all-matching selection legitimately enumerates IDs, and sending legitimately resolves selected records on the server.

ID selections and create payloads still scale with selected recipient count. This batch avoids full-record downloads but does not introduce a compact server-held selection token or change the delivery queue. Very large selections may eventually warrant that separate design, alongside quota-first validation and bounded worker processing.

## Validation

- Nine new backend regressions verify stable 50/50/25 pages, shared filtered counts, source/search semantics, empty/explicit selections, ID-only lookup, the HTTP page ceiling, hidden fields/module denial and all three roles' assignment/team/tenant/deletion boundaries. The scoped batch resolver is tested against unauthorized IDs.
- Eight existing campaign delivery cases used ownerless Lead fixtures. After applying the same scope as the picker to send resolution, those fixtures now assign the sender explicitly. Their original provider, quota, suppression and follow-up assertions remain. All 64 focused campaign tests passed.
- Full backend: **1,714 passed / 18 skipped**, Ruff, compilation, committed migrations on isolated PostgreSQL 17, ten opt-in PostgreSQL regressions, the separate empty-database migration-drift test and `alembic check` passed. Existing warnings remain.
- The real Chromium regression exercises the actual selector and composer/review hooks with fixture responses and a mocked send mutation. It covers lazy entity tabs, cached source facets, failed browse/preview retry, retained previews, all-matching selection excluding missing email, selected-page continuation, outside-page search and a complete 124-ID submission while one result is displayed.
- Final frontend snapshot **8e4a45cc** passed clean lockfile installation under Node 20, changed-file formatting against pre-batch commit `1a884e50`, full lint, unit/spreadsheet tests, TypeScript, every current CI browser command including the new campaign regression, additional session/Loop AI checks, safe production build and the configured dependency audit. All twelve modified/new frontend files match the tested snapshot byte for byte. Existing 1,512 lint warnings remain; there were no lint errors. The final results were written after the final clean installation and build, and the earlier run's logs were retained separately.
- Evidence/scripts are under `.worktrees/campaign-audience-20261008/`. Test services on 15432/16379 are isolated from application services on 5432/6379. No stage database is used.
- Both disposable CI containers were removed after verification. Application services were left running; the final backend readiness recheck returned HTTP 200.
- Graphify updated after final changes: **22,553 nodes / 62,844 edges**. Existing missing HCL/SQL parsers and partial unrelated TSX extraction remain coverage limitations.
- Font configuration is unchanged. No push, deployment or stage verification. Deploy the new backend recipient read contracts before the frontend consumer; existing list/create contracts remain compatible.

## Remaining work

Follow-up: [Campaign detail monitoring and recipient loading](campaign-monitoring-loading-audit-2026-10-08.md) implements the bounded monitoring contract described in item 1 below and records its live/fixture validation and separate remaining campaign work.

1. **Existing Campaign detail monitoring** still loads its complete recipient breakdown and polls at 3 seconds while sending/draft or 10 seconds otherwise. Separate lightweight status/aggregate polling from paginated recipient rows, while retaining live opens/replies and retry/cancel controls. The inspected local campaign has only ten recipients, so that is not a large-volume runtime validation.
2. Lead/Deal Kanban still needs per-column pagination and preserved counts/aggregates/drag behavior.
3. Contact Deal-note batching and parent-note pagination remain.
4. Meeting conflict/context reads and dense connected Calendar need bounded windows without missing conflicts or events.
5. Continue count/relationship/concurrency profiling. Unified chronological timeline cursors, production/stage runtime checks and native reload/SSE diagnosis remain separate.
