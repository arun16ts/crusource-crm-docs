# Phase 4 layout and interaction reference

These wireframes describe the delivered layout; [actual captures](SCREENSHOTS.md) are the visual acceptance evidence.

## Public form

```text
Marketing navigation: brand / resources / Request a demo / account links
Introduction: heading + preferred-window explanation
┌──────────────────────────────────────────────────────┐
│ Name                  Email                          │
│ Company               Phone (optional)                │
│ Team size                                            │
│ Use case / message                                   │
│ Preferred contact window                             │
│ Timezone                                             │
│ Contact-purpose acknowledgement / privacy link        │
│ Send enquiry                                         │
└──────────────────────────────────────────────────────┘
Public footer
```

Small screens stack field pairs. Success replaces the form with a saved-enquiry acknowledgement, opaque reference and Send another enquiry. Validation stays next to the form. An uncertain result shows Retry and locks input, preserving its operation key; it does not claim a lost submission or invent a booking.

## Staff board and list

```text
Platform sidebar | Shared header / principal
                 | Demo requests + Refresh
                 | Board / List
                 | Search / stage / source / enquiry type / assignee
                 | Disposition / created range / list sort
                 | New | Contacted | Qualified | Scheduled | ...
                 | loaded / total per independently loaded column
                 | company / requester / assignee / ages / follow-up
                 | Move to stage / per-column Load more
```

Desktop columns scroll inside their workspace. Mobile shows the selected stage, default New, with the filter allowing another stage; cards keep the explicit keyboard-accessible move action. List replaces columns with a shared table and server pagination. Filters/view/sort/page survive reload/back/forward through URL state. Initial errors show Retry rather than empty data; failed refreshes preserve the last successful data with a warning.

## Detail and actions

```text
Back to enquiries, preserving return view
Company / reference / current stage                         Refresh
┌───────────────────────────┬─────────────────────────────────────┐
│ Contact + submitted needs │ Stage / disposition / assignee      │
│ Preferred window/timezone │ Scheduled demo + follow-up/timezones │
│ Related enquiry warning   │ Manage actions, if authorized        │
└───────────────────────────┴─────────────────────────────────────┘
Manager-only internal delivery status
┌───────────────────────────┬─────────────────────────────────────┐
│ Append-only internal notes│ Activity, actor/time/reason/changes  │
│ Independent paging        │ Independent paging                  │
└───────────────────────────┴─────────────────────────────────────┘
```

Shared ActionDialog contains only fields relevant to the selected command, optional/required reason, Cancel and Save. Schedule entry explicitly uses UTC and records IANA timezone. A follow-up edit retains its own timezone. Pending operations disable duplicate submission/closing. Uncertain results retain input/key; version conflict requires closing/refetching/retrying with a current version. Read-only staff have no write controls. Permission loss hides privileged content and current server authorization prevents stale actions.

Owner Access Management adds Sales access per non-owner staff account, with None/Read/Manage choices and versioned save. A grant does not bypass existing platform enrollment/MFA eligibility.
