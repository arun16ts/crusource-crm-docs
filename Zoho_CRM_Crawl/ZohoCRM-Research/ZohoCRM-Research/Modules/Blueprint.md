# Module — Blueprint

> Source: https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/design-a-blueprint

## BP.1 General Information

- **Edition**: Professional+ (Process automation — https://www.zoho.com/crm/zohocrm-pricing.html).
- **Purpose**: Visual state machine for guiding users through a structured process on a record.

## BP.2 Components

- **States** — picklist values; "Start State" = picklist value None.
- **Transitions** — buttons rendered on the record page that move the record between States.
- **Before Transition** — assignee + criteria.
- **During Transition** — field entries, checklists, attachments, related items.
- **After Transition** — automated actions.

## BP.3 Transition Settings (verbatim from official doc)

### Before
- "Specify people responsible for executing a Transition. This can be CRM or portal users."
- "Define criteria that dictates exactly when this Transition should be available for the records in a process."

### During
- "Add values for fields from the primary module and related modules, including multi-select lookup and multi-user fields. These can be validated."
- "Complete checklists."
- "Add associated items like notes, attachments, tasks, meetings, calls, and so on."
- "Add tags."
- "Perform actions in widgets."
- "Add Kiosks."

### After
- "Send email notification"
- "Assign tasks"
- "Create a meeting"
- "Schedule a call"
- "Update fields"
- "Create a record"
- "Trigger webhooks"
- "Trigger custom functions"
- "Add tags"
- "Convert Record (Applicable for the Leads and Quotes modules)"

## BP.4 Field Mandatory Logic (verbatim)

> "You can guide your sales reps to enter information required as part of your process by mandating fields at the appropriate stages. You can add optional fields to collect additional information that may be useful..."
> "Whether a transition field is marked as mandatory or optional depends on:
> 1. Whether the module field is mandatory or not
> 2. Whether a layout rule is marking a field as mandatory or not
> 3. Whether its set as mandatory in the blueprint transition setting.
> If at least one of these is mandatory, then the field is marked as mandatory."

## BP.5 Advanced

- **Automatic transitions** — fire after elapse of configured time. https://help.zoho.com/portal/en/community/topic/spotlight-7-automatic-transitions-in-blueprint
- **Common transitions** — shared by multiple states; documented in https://help.zoho.com/portal/en/kb/crm/process-management/blueprint/articles/parallel-and-multiple-transitions-configuration-and-usage
- **Parallel / Multiple transitions** — see same URL.

## BP.6 Cross References

- `../04_User_Journeys.md` §4.11.
- `../Modules/Workflow.md`.
