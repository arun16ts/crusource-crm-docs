# Campaign detail monitoring and recipient loading — 2026-10-08

## Scope and observed cause

This batch follows [campaign audience selection](campaign-audience-loading-audit-2026-10-08.md). It changes campaign detail monitoring, not dispatch, quotas, email providers, or the imported Sales/Activities data.

The running localhost application has one completed campaign with 10 recipients. Before changes, opening its detail page produced three successful full detail responses over about 22 seconds, each **8,532 bytes** and including all 10 recipients. The frontend polls every 3 seconds for sending/draft campaigns and every 10 seconds otherwise. Both Email Content and Recipients shared this full response.

Source tracing confirmed the detail repository also ran organization-wide telemetry synchronization: it materialized every sent/pending recipient in the organization, validated email syntax, and could write failed statuses/counts. The detail handler separately materialized the selected campaign's complete recipient collection, calculated counts in Python, and sometimes committed corrected counts. A/B analytics loaded full recipient records; deal attribution first loaded all recipient entity IDs into Python. This is costly work even if the Network tab shows only one request.

Evidence: `useCampaignDetailQuery`, `CampaignDetail`, `get_campaign_handler.py`, `campaign_query_repository.get_campaign_by_id`, `campaign_telemetry_service`, and `campaign_analytics_repository`; Graphify relationships verified against source and the live browser.

## Changes

- The detail UI now fetches metadata with `include_recipients=false&include_analytics=false`, refreshed every 60 seconds. Content, sequence preview and cloning remain available. Source inspection confirmed that this view does not render deal/A-B analytics, and its attributed-deals modal has no open action wired up, so those unused calculations are skipped explicitly. The existing full-detail/analytics defaults remain compatible with older clients.
- A dedicated `/{campaign_id}/status` endpoint returns delivery/engagement counts and status using one SQL aggregation, without recipients, email bodies, organization-wide email correction, or writes.
- `/{campaign_id}/recipients` returns a stable server page, normally 50 rows; maximum 500. Name/email/type search, delivery status, and opened filtering run in SQL. Query keys include campaign, filters, offset and limit. Search is debounced and changed filters start at offset zero.
- Live status retains the existing 3/10-second cadence. Only the visible Recipients tab polls its current bounded page. Hidden browser tabs retain TanStack Query's background-polling pause. Metadata updates have the slower 60-second cadence; Refresh Stats refreshes all currently relevant queries immediately.
- New monitoring reads do not perform email validation or commit data corrections. Existing send validation, provider/webhook processing, legacy read paths, retry and cancel remain intact. This batch does not remove organization-wide synchronization from the campaign list/statistics endpoints.
- A/B analytics use grouped SQL aggregates; deal attribution uses a correlated recipient `EXISTS` instead of downloading the entire audience's IDs. The legacy/full analytics contract still returns unpaged attributed deal rows; that is a separate follow-up before wiring a large drilldown.
- CSV export explicitly retrieves all matching records in batches of 500 when requested, rather than exporting only the visible page. Selected rows persist across pages. Select-all matching supports excluding individual rows and exporting the remaining complete set. Failure does not produce a misleading successful partial download.
- Counts remain campaign-wide, separately from filtered page totals. Errors expose retry controls; loading does not masquerade as a successful empty result. Mutation invalidation still refreshes monitoring queries under the campaign detail key.

## Authorization and compatibility

All new routes retain the existing `campaigns/view` permission guard and campaign organization lookup. Existing campaign detail visibility is organization-wide behind that guard; this batch deliberately retains that contract for Admin, Sales Manager and Sales Rep, and rejects another organization's campaign with 404. It does not grant access to otherwise unauthorized Lead/Contact detail drawers: those retain their existing entity APIs and scope checks.

The new metadata option is additive and defaults to the old full detail response. The backend supporting the new endpoints must precede frontend rollout. Nothing was deployed or pushed in this batch. Local tests do not verify stage behavior.

## Browser comparison

| Scenario | Before | After |
| --- | --- | --- |
| Initial detail, actual 10-recipient campaign | One full 8,532-byte response | Metadata 984 bytes, status 342 bytes, page 5,957 bytes (7,283 bytes combined), without unused analytics |
| Recipients visible | Full 8,532-byte response each 10 seconds | Status 342 bytes plus current page 5,957 bytes each 10 seconds; no full audience reload |
| Email Content visible | Full detail/recipient response each 10 seconds | Two successful 342-byte status responses over 21.5 seconds; no recipient page requests |
| Search `arun.k` | Browser filters complete collection | Server returns the correct matching recipient, 619-byte page response |
| Bulk browser regression | No bounded detail table | Fixture with 625 recipients: pages of 50, search beyond loaded rows, complete export over two 500-row batches, selection across pages, all-matching export with exclusions |

The live page still displays 10 recipients, 9 sent and 1 failed, including its original failure message and profile actions. Email Content remains correct. A final actual View Lead action returned 404: a read-only local PostgreSQL check confirmed that the referenced Lead exists but is soft-deleted, with its historical campaign recipient retained. This is an existing historical-link case, not a new pagination error; the record-access guard remains intact. A clearer unavailable-profile indicator is a separate UI follow-up.

The isolated browser exercises actual detail/table/query/mutation code with fixture APIs; retry and cancel execute only against mocks. No email was sent, existing campaign retried/cancelled/deleted, or imported business record changed. The browser was left on `about:blank` after live checks.

The native backend stopped responding once during reload, including `/health/ready` outside the restricted network profile. After the user restarted it, successful polling and tab comparisons were repeated. Hanging requests before that restart were not treated as proof that polling had stopped.

## Database volume evidence

An isolated PostgreSQL 17 database, migrated from committed migrations, received a transactional fixture with **10,000 recipients in the selected campaign and another 10,000 in an unrelated campaign**. The repository monitoring check returned correct selected-campaign counts, fetched the final 50-row page at offset 9,950, made four SELECT statements, and performed no monitoring writes. Setup fixtures were rolled back.

Single local measurements: campaign lookup plus aggregation **20.86 ms**; filtered count plus final-page query **33.96 ms**. These are fixture measurements, not production/API latency guarantees. The combined repository check reused its campaign lookup; separate HTTP status/page endpoints each validate campaign access. SQL aggregates and filtered totals still inspect matching rows; bounded responses do not make database work constant-time. High-offset pages still incur offset/sort work; no index migration was added without wider plan evidence.

## Validation

Validation evidence is stored locally under `.worktrees/campaign-monitor-20261008/`. Complete frontend/backend checks passed after the final analytics-skipping option was implemented.

Final frontend snapshot **93eb8d38** passed clean lockfile installation under Node **20.20.2**, changed-file formatting against pre-batch commit `9a88fed2`, full lint, unit/spreadsheet tests, TypeScript, all current CI browser commands (including the new monitoring regression), additional session/Loop AI checks, production build with safe test API/OAuth settings, and the configured dependency audit. The complete checks were rerun after the final formatter and analytics-option changes. All seven frontend files match the tested snapshot byte for byte. Final results were written after the latest clean installation and build; earlier logs are retained separately. Existing **1,510 lint warnings**, zero errors; no high/critical runtime dependency advisories, with the existing temporary ESLint-only exception unchanged.

Focused checks passed: six monitoring API/database regressions covering stable pages, search/filters, limits, read-only SQL, aggregate A/B counts, tenant isolation for all three roles and permission denial; ten A/B analytics regressions; the Chromium monitoring regression covering paging, full and selected export, all-matching exclusions, live status, inactive tab, error recovery, retry and cancel; TypeScript and Ruff. The final focused integration run passed **35 campaign/analytics tests**.

Two old A/B winner tests initially failed because their mocks supplied full recipient objects to the former query shape. The four analytics cases now use real database-backed recipient fixtures with the original winner, tie and zero-division assertions intact. The final complete suite passed **1,720 tests, 18 skipped, 822 existing/deprecation warnings** after this correction and the final analytics option. Ruff and compile checks passed; committed migrations applied to disposable PostgreSQL; all **10 opt-in PostgreSQL regressions** and the separate empty-database migration-drift test passed; `alembic check` reported no new upgrade operations. No migration was added.

Both disposable audit containers on ports 15432/16379 were removed after final verification; application services on their normal ports were retained. Final readiness returned HTTP 200. Graphify updated after the final code changes: **22,605 nodes / 62,993 edges**. Existing missing HCL/SQL parsers and partial unrelated TSX extraction remain graph coverage limitations. Font configuration is unchanged. No primary-repository commit, push, deployment or stage verification was performed.

## Remaining work

1. Follow-up completed: [Campaign read work audit — 2026-10-09](campaign-read-work-audit-2026-10-09.md) removes organization-wide repair from list/statistics/leaderboard/detail reads, preserves explicit reconciliation and send validation, and records the new bulk-data browser evidence. See that report for current remaining work.
2. The backend/full analytics contract returns unpaged attributed deals, while the current detail modal has no open action. If that UI is wired up, separate aggregate KPIs from a lazy, scoped, paginated drilldown. The new monitoring metadata does not fetch those unused analytics.
3. Recipient SQL counts, high offsets, and explicit very large exports need plan/concurrency profiling at representative production volumes. CSV export is bounded per request but accumulates the requested export in browser memory; a streaming/snapshot export is a separate improvement.
4. The backward-compatible full-detail endpoint and old exported query hook remain available for older clients. Upgraded UI uses the new endpoints. Remove compatibility paths only after callers and rollout are verified.
5. Lead/Deal Kanban, related notes, meeting conflict/context reads, dense Calendar windows and stage verification remain separate audit batches. This report does not certify the entire application as optimized.
6. Historical recipients can reference soft-deleted entities. Their profile API correctly returns 404; indicate unavailable profiles clearly without bypassing authorization or deletion guards.
