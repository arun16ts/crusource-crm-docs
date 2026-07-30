# Module — Reports

> Source: https://help.zoho.com/portal/en/kb/crm/analytics-and-dashboards/reports/create-edit-reports/articles/understanding-and-building-reports

## RP.1 General Information

- **API name**: `Reports` (accessed via `modules.dashboards` and `bulk.read` scopes, https://www.zoho.com/crm/developer/docs/api/v8/scopes.html).
- **Purpose**: Saved tabular/summary/matrix reports over one or more modules.
- **Edition**: Free and all paid editions; advanced analytics connector via Zoho Analytics is also available.

## RP.2 Report Types

| Type | Description |
|---|---|
| **Tabular** | Simple row-level dataset. |
| **Summary** | Grouped aggregation with chart (bar, pie, line, etc.). |
| **Matrix** | Both horizontal and vertical grouping (pivot). Dashboards now support Matrix panels (https://www.marksgroup.net/blog/zoho-crm-create-dashboards-matrix-reports/). |

## RP.3 Common Components

- **Primary Module** (one anchor)
- **Related Modules** (joined via lookup)
- **Columns / Summaries** (sum, avg, count, min, max)
- **Filters** (criteria, group filter via AND/OR logic)
- **Group By** (single or multi-level)
- **Charts** (bar, horizontal bar, line, stacked, pie, donut, table, funnel, area)
- **Custom Buttons** (drilldown to other reports)
- **Standard filters** (Date range, record owner etc.)

## RP.4 Schedule & Sharing

- Reports can be shared as a permalink (https://www.facebook.com/groups/1548636698800249/posts/4050081438655750/ cross-reference).
- Reports can be scheduled via email delivery.
- Reports can be subscribed-to from the dashboard.

## RP.5 Cross References

- `../Modules/Analytics.md`.
- `../03_Feature_Index.md` §3.6.
