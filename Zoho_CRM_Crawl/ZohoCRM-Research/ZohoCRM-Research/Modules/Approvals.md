# Module — Approvals

> Source: https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/set-approval-process ; https://help.zoho.com/portal/en/kb/crm/process-management/approval-process/articles/add-approval-process

## AP.1 General Information

- **Permission**: Manage Automation.
- **Edition**: Standard-edition workflows & approval rules (Pricing page).

## AP.2 Conceptual model

- Multi-step approval chain.
- Each step has Approver(s) (User / Role / Owner of a related record).
- Approve / Reject actions.
- Approval state is stored on the record; record goes through states like "Pending Approval" → "Approved" → "Rejected".
- Approval can coexist with Workflows and Blueprints.

## AP.3 Configuration Steps

1. Setup → Process Management → Approval Processes.
2. Click Add Approval Process.
3. Specify Name, Description.
4. Choose Module.
5. Define rule criteria / entry-trigger.
6. Choose Approvers (per level).
7. Define Approve / Reject actions.
8. Optionally set Editable fields while in approval state.

## AP.4 Use-Cases (from official doc context)

> "Sales reps offering product discounts to customers need the approval of their manager before they do so. Marketers planning a campaign may need the approval of the Marketing head as well as the Finance head to go ahead with the campaign."

## AP.5 Triggering Approval via API

Per https://help.zoho.com/portal/en/community/topic/kaizen-33-triggering-workflow-rules-approvals-and-blueprints-via-zoho-crm-api :

> Approval can be triggered via Deluge or REST API when inserting/updating/upserting records by including `trigger: ['approval']`.

## AP.6 Cross References

- `../Modules/Workflow.md`, `../Modules/Blueprint.md`.
- `../04_User_Journeys.md` §4.12.
