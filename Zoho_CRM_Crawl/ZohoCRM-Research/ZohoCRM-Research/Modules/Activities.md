# Module — Activities (Tasks, Meetings, Calls)

> Verbatim from https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities and https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-tasks-module

## AC.1 General Information

The Activities cluster in Zoho CRM comprises three first-class modules plus one virtual aggregator:

| Sub-module | API name | Scope | Edition |
|---|---|---|---|
| Tasks | `Tasks` | `ZohoCRM.modules.tasks.ALL` | Free+ |
| Meetings (formerly "Events", renamed — https://help.zoho.com/portal/en/community/topic/events-module-is-been-renamed-as-meetings) | `Events` | `ZohoCRM.modules.events.ALL` | Free+ |
| Calls | `Calls` | `ZohoCRM.modules.calls.ALL` | Free+ |
| Aggregator (Activity History, Recent Activities) | n/a | `ZohoCRM.modules.activities.ALL` | Free+ |

## AC.2 Standard Fields

### AC.2.1 Tasks

| Field | Type | Notes |
|---|---|---|
| Task Owner | Lookup | yes |
| Subject | Text | — |
| Due Date | Date | — |
| Status | Picklist | Not Started / Deferred / In Progress / Completed |
| Priority | Picklist | High / Normal / Low |
| Reminder | Checkbox | — |
| Repeat | Picklist | None / Daily / Weekly / Monthly / Yearly |
| Description | TextArea | — |
| Related To | Lookup (any module) | polymorphic |
| Contacts | MultiLookup | association |

### AC.2.2 Meetings

| Field | Type | Notes |
|---|---|---|
| Meeting Owner | Lookup | yes |
| Title | Text | commonly old "Subject" |
| Start Date Time | DateTime | — |
| End Date Time | DateTime | — |
| Location | Text | physical address or meeting URL |
| Type | Picklist | Online / In-Person |
| Status | Picklist | Scheduled / Held / Cancelled |
| Participants | MultiLookup (Contacts/Users/Leads) | — |
| Related To | Lookup (any module) | — |
| Reminder | Number of minutes/hours | — |
| Description | TextArea | — |

### AC.2.3 Calls

| Field | Type | Notes |
|---|---|---|
| Call Owner | Lookup | yes |
| Call Type | Picklist | Inbound / Outbound |
| Call Status | Picklist | Completed / Scheduled / Missed |
| Call Duration | Integer | seconds |
| Call Start Time | DateTime | — |
| Subject | Text | — |
| Call Purpose | Picklist | Prospecting / Follow-up / Negotiation / Demo / Other |
| Call Agenda | TextArea | — |
| Related To | Lookup (any module) | — |
| Description | TextArea | — |
| Call Result | Picklist | admin-configurable |

## AC.3 Recent / Activity History (verbatim)

Verbatim from the FAQ page:

> "The last 5 activities will appear under Recent Activities. **The Closed Activities related list displays all the closed activities like tasks, calls, and meetings related to a record."**

## AC.4 User Actions

| Action | Notes |
|---|---|
| Create | Instant — UI Quick Create from any record. |
| Complete | "Mark Completed" surfaces in activity card. |
| Reschedule | UI reschedule. |
| Cancel | UI cancel. |
| Reminder | System-sent reminder. |
| Mass Update | list view |
| Convert (Calls → Tasks) | UI conversion (Call can be converted to Task). |

## AC.5 Business Logic

- Owner Change Permits Transfer of Open Activities: verbatim "If you change the owner of the records (leads, contacts, accounts, cases, etc.), all the open tasks/events get assigned to the new record owner" (https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities).
- Activities can NOT be assigned to a group of users (verbatim "you cannot currently assign a task or meeting to a group of users. Activities can only be assigned to individuals").
- Deleting tasks/calls/meetings requires Delete permission in the user's Profile (verbatim from the FAQ "Log in to Zoho CRM with administrator privileges. Go to Setup > Security Control > Profiles").

## AC.6 Reports / KPI

- Activities by Owner.
- Activities by Type (Call/Task/Meeting).
- Activities per Stage (on a Kanban).
- Activities per Account/Deal.

## AC.7 Cross References

- `../Modules/Tasks.md`, `../Modules/Calendar.md`, `../Modules/Calls.md`.
- `../06_Data_Model.md`.
- `../04_User_Journeys.md` §4.9.
