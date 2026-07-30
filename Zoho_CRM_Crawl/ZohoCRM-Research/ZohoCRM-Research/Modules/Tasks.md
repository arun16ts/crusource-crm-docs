# Module — Tasks

> Sources: https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-tasks-module ; https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities

## T.1 General Information

- **API name**: `Tasks`
- **OAuth scope**: `ZohoCRM.modules.tasks.ALL`
- **Purpose**: To-do activities that can be linked to any record and carry due dates, status, priority.
- **Edition**: Free and all paid editions.

## T.2 Standard Data Model

| Field | Type | Notes |
|---|---|---|
| Task Owner | Lookup(User) | yes |
| Subject | Text | — |
| Due Date | Date | — |
| Status | Picklist | Not Started / Deferred / In Progress / Completed (admin-customizable) |
| Priority | Picklist | High / Normal / Low |
| Reminder | Checkbox + Integer | triggers reminder alert |
| Repeat | Picklist | None / Daily / Weekly / Monthly / Yearly |
| Related To | Lookup (polymorphic) | Lead / Contact / Account / Deal / etc. |
| Description | TextArea | — |
| Created By / Modified By | System | — |

## T.3 UI

- List view: My Tasks / Today's Tasks / All Tasks views + custom views.
- Calendar view supported via the Calendar integration.
- Inline Quick Create from any record.

## T.4 Customization

Per FAQ (verbatim) "Yes, you can customize the page layout for the tasks, events and calls. The following customizations are possible: Add new fields, Add or delete sections, Rename fields, Add required fields or hide the unwanted fields, Mark fields as mandatory or non mandatory, Reorder the fields, Change to one column or two column layout."

## T.5 Automation

- Workflow rules fire on Task Created / Edited / Created or Edited / Deleted.
- Tasks can be auto-created by Workflow rules / Blueprint / Custom Functions.

## T.6 Cross References

- `../Modules/Activities.md`.
- `../04_User_Journeys.md` §4.9.
