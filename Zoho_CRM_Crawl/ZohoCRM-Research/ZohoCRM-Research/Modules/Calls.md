# Module — Calls

> Sources: https://help.zoho.com/portal/en/kb/crm/faqs/activity-management/articles/faqs-on-activities ; https://www.zoho.com/crm/ai-features-in-zoho-crm.html (for AI Call features)

## CL.1 General Information

- **API name**: `Calls`
- **OAuth scope**: `ZohoCRM.modules.calls.ALL`
- **Purpose**: Track logged calls (inbound/outbound) with type, duration, outcome and connection to any record.
- **Edition**: Free and all paid editions.

## CL.2 Standard Fields

| Field | Type | Notes |
|---|---|---|
| Call Owner | Lookup(User) | yes |
| Call Type | Picklist | Inbound / Outbound |
| Call Status | Picklist | Completed / Scheduled / Missed |
| Call Duration | Integer | seconds |
| Call Start Time | DateTime | — |
| Subject | Text | — |
| Call Purpose | Picklist | — |
| Call Agenda | TextArea | — |
| Call Result | Picklist | — |
| Related To | Lookup (polymorphic) | — |
| Description | TextArea | — |
| **Call Recording** | File upload | Required for AI transcription |
| Transcription | longtext | auto-generated |

## CL.3 Zia AI on Calls (verbatim)

Verbatim from https://www.zoho.com/crm/ai-features-in-zoho-crm.html :

> "Call transcription: The call transcription feature in Zoho CRM automatically transcribes call audio recordings into plain text in the Call Activity module."
> "Call intelligence: Zia analyzes and fetches important details about calls after transcribing them, such as Call sentiment, Call intent, Call emotion, Call summary."

## CL.4 Cross References

- `../Modules/Activities.md`.
- `../08_AI_Features.md`.
