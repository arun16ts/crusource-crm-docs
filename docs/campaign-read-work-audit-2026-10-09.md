# Campaign read work and remaining loading audit — 2026-10-09

## Scope and status

This follow-up completes the campaign list/statistics/leaderboard read-work item from [campaign monitoring](campaign-monitoring-loading-audit-2026-10-08.md). It does **not** certify all remaining bulk-data views. The frontend baseline is `e5fa25c2652e9076efdd7e41cd5306db8c1eef02`; backend baseline is `1a44cdb05c45049f7905943e21c8a887dfb6c604`. Both application repositories were clean before this batch. Only backend implementation changed; no migration, frontend contract change, commit, push or deployment was performed.

Local services initially refused connections. After the user started them, backend readiness returned 200 and Chromium loaded the authenticated application on ports 3000/8000. Graphify tracing was checked against actual source.

## Confirmed cause and changes

`campaign_query_repository` invoked `sync_all_org_campaign_telemetry` before list, statistics and legacy single-campaign reads. The leaderboard did the same. The sync service hydrated every eligible sent/pending recipient in the organization, validated each email in Python, and could write failures/counts and commit during a GET. Thus two legitimate Campaigns requests could repeatedly perform organization-wide repair work. This was backend amplification, not an unnecessary pair of frontend calls.

- Removed reconciliation from those query paths. The legacy detail handler also no longer persists aggregate counters during reads; it returns the live aggregate values.
- Kept reconciliation in the existing explicit inbox-sync command and Google webhook workflows. Changed its audience iteration to stable UUID keyset batches of at most 500. This bounds recipient hydration; the explicit operation still scans the eligible organization audience and can run a long transaction. It is not a constant-time or fully asynchronous job.
- Both Gmail and SES sending workers retain their pre-send deliverability validation, including DNS checks. Historical invalid-recipient reconciliation remains available; no send validation was removed.
- Combined statistics into two aggregate SQL statements. Creator-filtered performance totals retain their creator filter; Gmail/SES daily quotas remain organization-wide and use sent timestamps since midnight UTC.
- Eager-loaded campaign creators to eliminate list serialization's per-creator lazy query, and added ID ordering to break equal creation-time ties.
- Replaced leaderboard campaign/recipient/deal materialization with scalar SQL aggregates and scoped `EXISTS` attribution. Duplicate recipients do not multiply deal revenue. Date filters and the fallback to stored counters when no recipients remain are preserved. An explicitly empty user filter returns no representatives. Existing handler Admin/team/own scope decisions and tenant/module guards remain in place.

List summary counters continue using the command-maintained campaign counters; statistics/detail/status aggregate actual recipients. This preserves the existing contract rather than silently changing legacy counter semantics.

## Browser comparison

The imported localhost workspace contains one campaign with ten recipients. Before and after, the campaign list returned 596 bytes, statistics returned 203 bytes, and the UI showed one campaign, ten total recipients and nine delivered. Both endpoints returned 200. The post-change leaderboard returned the existing scoped attribution totals: pipeline 1,375, won revenue 1,000, five deals and two won deals.

On a fresh Campaigns navigation, there was one list GET and one statistics GET, both 200; no repeated campaign GET during the subsequent 12-second observation. Shell requests are separate legitimate session, permissions, organization, billing, notification/inbox and import-event consumers. This batch did not remove those requests.

Individual local timings were list 75 ms/statistics 69 ms before and 84 ms/72 ms after. The ten-recipient live fixture is too small and uncontrolled to establish a speedup; response/functional correctness and the query-shape comparison below are stronger evidence.

Font configuration was not changed. Chromium reported `Instrument Sans` in the computed body family and loaded font faces after navigation. This is a loaded-state check, not a new throttled hard-refresh/font-flash certification.

## Disposable PostgreSQL volume comparison

An isolated PostgreSQL 17 fixture contained two campaigns and 20,000 valid recipients, half opened. The original repository and telemetry source from the baseline commit were compared with current code against the same fixture. The outer transaction was rolled back; no application records or email delivery were involved.

| Read | Original SQL statements | Revised SQL statements | Original recipient objects | Revised recipient objects |
| --- | ---: | ---: | ---: | ---: |
| Statistics | 8 | 2 | 20,000 | 0 |
| One-row campaign list including creator serialization | 4 | 2 | 20,000 | 0 |

Statistics returned the same 20,000 sent and 10,000 opened totals. One local execution took 594.51 ms before versus 10.81 ms after. This is a query-shape experiment, not a production latency/concurrency guarantee. Exact totals still scan matching SQL rows; no index migration or database-cache claim is made.

Local evidence: `.worktrees/remaining-performance-20261009/campaign-read-profile.json` and `profile_campaign_reads.py`, together with original-source snapshots. SQL capture reports statement counts and ORM hydration, without logging bind parameters or credentials.

## Validation

Complete backend applicable workflow checks passed: Ruff, compilation, committed migrations on disposable PostgreSQL, **1,726 tests passed / 18 skipped**, all **10 opt-in PostgreSQL regression tests**, the separate empty-database migration-drift test, and `alembic check` (no new upgrade operations). The full run reported 1,849 warnings, including warnings generated by the new bulk fixture; these are not test failures. Six new regression cases cover two-statement stats, creator counters versus org-wide quotas, read-only legacy detail, eager creator loading, all three leaderboard role scopes, dates, duplicate attribution, empty visibility and bounded tenant-specific reconciliation.

Frontend source/configuration is unchanged; its prior CI evidence is in the monitoring audit. No new frontend CI/build claim is made here. Local evidence and complete backend results are under `.worktrees/remaining-performance-20261009/`. Stage has not been verified.

The disposable audit PostgreSQL/Redis containers were stopped and removed after validation; local application readiness remained 200. Graphify generated updated graph/report/HTML artifacts with 22,614 nodes and 63,035 edges. Its process returned exit code 1 alongside coverage warnings and a successful rebuild message; the existing missing HCL/SQL parsers and five partial unrelated TSX parses remain limitations, not a clean Graphify execution claim.

## Reproduced remaining work

**Follow-up:** Items 1 and 2 below are historical baseline findings now addressed by [the sales Kanban audit](sales-kanban-loading-audit-2026-10-09.md). That follow-up records bounded card pages, full aggregates and its validation limits. The other items remain separate work.

1. **Leads Kanban:** Chromium downloaded 10,000 rows out of 14,000, **10,354,810 bytes**. `LeadBoard` requests `limit=10000`; column continuation increases the display limit over already-downloaded records. Four thousand records are outside the response. Replace this with scoped per-column server pagination, stable ordering and full column counts. Preserve legacy stage resolution, pipeline/filter semantics, drag updates and mutation invalidation; merely lowering the limit would lose more records.
2. **Deals Kanban:** Chromium downloaded 10,000 rows out of 16,000, **9,155,116 bytes**. Its aggregate response was 2,713 bytes, but rendered counts and currency subtotals are calculated from downloaded cards. Use server column aggregates and paginated cards together, preserving currencies, pipeline scoping and drag behavior. Six thousand records are outside the bulk response.
3. **Meeting scheduling:** Opening Schedule Meeting on the 35,445-record workspace triggers the legacy `/meetings?skip=0&limit=100000` request. `MeetingOverviewTab` calls `useMeetings()` to run client schedule-context analysis. This request was reproduced; the captured response did not provide a usable body, so no byte-size/returned-row claim is made. Move conflict/previous/next context to a scoped, time-specific server read; do not replace it with an arbitrary first page that misses conflicts.
4. **Notes and dense calendar:** Parent notes are still unpaged, and related-entity consumers need a batching audit. Calendar window pagination must be evaluated at dense overlapping-event volumes. These were source-traced, not completed in this batch.
5. Full legacy campaign detail still intentionally allows an unpaged audience/attributed-deal response for compatibility; current monitoring skips it. Leaderboard query count remains three aggregates per visible representative plus the user lookup. Very large teams, high-offset pages, counts and browser-accumulated exports still need concurrency/plan profiling. A strict cross-module chronological timeline cursor and unavailable historical-profile UI are separate improvements.

No imported business record was edited, no meeting was saved, and no email was dispatched during browser inspection. Kanban views were returned to List after inspection.
