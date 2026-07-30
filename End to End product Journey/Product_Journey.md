# Crusource CRM — Version 1 Product Journey

**Scope:** How a user actually moves through the product, step by step, across the three roles: Admin, Sales Rep, and Sales Manager.

## Journey 1 — Admin: Organization & User Setup

*Happens once, before anyone else can log in.*

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | **Login** | Admin **logs in** with the org's first Admin account | Lands on Home |
| 2 | **Settings → Users** | **Click Add User** | User form opens |
| 3 | **Add User form** | **Enter** name, email; **select** Role | User is created |
| 4 | **Add User form** | **Select Reports To** | Rep scoped to Manager |

**Outcome:** Organization has an Admin, one or more Sales Managers, and Sales Reps each linked to a Manager. Roles are enforced from this point on — every screen a user sees from here is scoped by their role (see Users & Roles in the features doc).

## Journey 2 — Sales Rep: Lead to Closed Deal

*The core journey the whole product is built around.*

### Step 1 — Log In & Land on Home

| Screen | What the Rep sees |
|---|---|
| Login | Email + password |
| Home | KPIs: Open Deals, Untouched Deals, My Leads, My Calls Today. Widgets: My Open Tasks, My Meetings, Today's Leads, Leads Closing This Month — all scoped to "My" data only |

### Step 2 — A New Lead Comes In

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Leads (sidebar → Sales → Leads) | Click **Create Lead** (or lead arrives via CSV import) | Lead form opens |
| 2 | Create Lead form | Enter Lead Name, Company, Email, Phone, Source | Lead saved with Status = New |
| 3 | Leads list | Lead now appears under "My Leads" | Rep can open it |

### Step 3 — Rep Works the Lead

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Lead detail page | Click **Log Call** | Call logged: Subject, Call Type, Start Time, Duration, Contact Name, Owner — appears on the lead's activity timeline |
| 2 | Lead detail page | Click **Create Task** | Follow-up task created: Subject, Due Date, Priority, Contact Name, Owner |
| 3 | Lead detail page | Click **Create Meeting** | Discovery call scheduled: Title, From, To, Contact Name, Meeting Host |
| 4 | Leads list | Update Status to **Qualified** | Lead moves out of "New" view |

### Step 4 — Convert Lead to Deal

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Lead detail page | Click **Convert** | Convert form opens |
| 2 | Convert form | Confirm/enter Deal Name, Amount, Stage (starts at Qualification), Closing Date | On save: an **Account** and **Contact** are created (or linked if they already exist), and a **Deal** is created |
| 3 | — | Lead Status → Converted | Lead is now read-only; all further work happens on the Deal |

### Step 5 — Deal Moves Through the Pipeline

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Deals → Kanban View | Deal card sits in **Qualification** column | Rep drags card to next stage as work progresses |
| 2 | Deal detail page | Log calls, meetings, tasks against the deal (same pattern as Step 3) | Unified activity timeline builds up on the Deal |
| 3 | Deal detail page | Click **Upload Document** | Proposal/SOW attached, linked to the Deal |
| 4 | Deals → Kanban View | Drag card through Needs Analysis → Value Proposition → Id. Decision Makers → Proposal/Price Quote → Negotiation/Review | Stage field updates on each move |

### Step 6 — Deal Closes

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Deals → Kanban View | Drag card to **Closed Won** or **Closed Lost** | Deal marked closed; drops off "Open Deals" KPI |
| 2 | Home | "Open Deals" and "Leads Closing This Month" widgets update accordingly | Rep's dashboard reflects the closed deal |

**End state:** One Lead has become one Account + Contact + Deal, with a full activity trail (calls, meetings, tasks) and any uploaded documents — visible on the Account's detail page under Contacts / Deals / Activities tabs.

## Journey 3 — Sales Manager: Team Oversight

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Home | KPIs and widgets show **Team** data — the Manager's own records plus every Rep reporting to them | Manager sees team-wide open deals, leads, tasks |
| 2 | Leads / Deals / Accounts / Contacts | Browse any Rep's record on their team (not just their own) | Full visibility into team pipeline |
| 3 | Deals → Kanban View | View team's combined pipeline across all stages | Spot stalled deals across reps, not just their own |
| 4 | Reports | Open Pipeline by Stage / Win-Loss Rate reports | Scoped to team data |
| 5 | — | Cannot access Settings → Users | Role assignment stays Admin-only |

## Journey 4 — Admin: Ongoing Monitoring

| Step | Screen | Action | Result |
|---|---|---|---|
| 1 | Home | KPIs and widgets show organization-wide data | Full visibility across all reps and managers |
| 2 | Reports | Open any report from the report dashboard (Name, Description, Folder, Last Accessed, Created By) | Org-wide figures |
| 3 | Settings → Users | Deactivate a departing employee, or reassign a Rep to a different Sales Manager | Access revoked / reporting line updated |
| 4 | Any module | Full read/write access to every record in the org | Used for data cleanup, reassignment, or troubleshooting |
