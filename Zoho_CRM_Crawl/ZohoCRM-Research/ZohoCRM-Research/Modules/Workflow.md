# Module — Workflow (Workflow Rules)

> Primary source: https://help.zoho.com/portal/en/kb/crm/automate-business-processes/workflows/articles/configuring-workflow-rules

## WF.1 General Information

- **Edition**: Standard and above (Workflows & assignment rules — https://www.zoho.com/crm/zohocrm-pricing.html).
- **Permission**: "Manage Automation" profile permission required.
- **Two categories** in CRM:
  1. **Workflow Rules** — record-state-driven actions.
  2. **Workflow Approvals** — see `../Modules/Approvals.md`.

## WF.2 Components

1. **Trigger**.
2. **Conditions** (criteria).
3. **Actions** (Instant / Scheduled).

## WF.3 Trigger Options (verbatim)

1. **Record Action** — Created / Created or Edited / Edited (any, specific field, or any field in a section) / Deleted.
2. **Date Field** — fires on day of recurring date.
3. **Score Value** — Zia score increase / decrease / update.
4. **Day of Recommendation** — Zia next-best-experience.
5. **Note(s)** — created / modified / added-or-modified / deleted.
6. **Competitors** — Zia-detected competitor mention in email.

## WF.4 Conditions (verbatim)

> "Workflow Condition - You can create multiple conditions in a workflow rule. Each condition consists of two elements. One is specifying which records should be triggered i.e. all records or the records that match the criteria. Another is adding the criteria based on which it should be triggered. When there are multiple conditions, records will be validated against the criteria mentioned in each condition and when it meets a criteria, the other conditions that follow will be ignored for validation."

Multiple-conditions caps:
- Standard/Professional: up to 5.
- Enterprise/Ultimate: up to 10.

The catch-all "Records that do not meet any of the above conditions" condition is supported.

## WF.5 Instant Actions (verbatim list)

> "Add email notifications, tasks, field updates, webhooks, custom functions, create record, and send notifications via Cliq, Slack or Cisco Webex that will be triggered immediately when the rule is executed. On Edit or Field Update actions, you can also convert Leads, Quotes or Sales Orders."

Caps (from page):
- Email alerts: up to 5 per action set.
- Tasks: up to 5 per action set.
- Field updates: up to 5 per action set.
- Webhooks: up to 6 (1 instant + 5 scheduled).
- Custom Functions: up to 6 (1 instant + 5 scheduled).

## WF.6 Scheduled Actions (verbatim)

> "Add email notifications, tasks, field updates, webhooks, custom functions, and send notifications via Cliq, Slack or Cisco that will be scheduled and triggered based on a specified time."

Date-based firing: max **5,000 records every 10 minutes** (verbatim).

## WF.7 Trigger via API

Per https://help.zoho.com/portal/en/community/topic/kaizen-33-triggering-workflow-rules-approvals-and-blueprints-via-zoho-crm-api :

> "Activate your Workflow, Approval Process, or Blueprint through either the deluge script or Zoho CRM API during the creation, updating, or deletion of a record."

## WF.8 Cross References

- `../04_User_Journeys.md` §4.10.
- `../07_API_Research.md` §7.11 (Functions).
- `../Modules/Blueprint.md`.
- `../Modules/Approvals.md`.
