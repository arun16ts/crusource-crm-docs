# Crusource CRM — Build Roadmap

## Phase 1 — Foundation, Access Control & Core Sales Records

**Duration:** 12 days

**Why this comes here:** Every other module needs to know who is logged in and what they're allowed to see, and Leads, Contacts, Accounts, and Deals are what a sales rep spends their day in. Access control and the core sales data model are combined into a single foundation phase, since nothing downstream (activities, reports, AI) means anything without both existing first.

**What ships**

- Single-organization login (email + password)
- Admin can add users and assign roles: Admin / Sales Manager / Sales Rep
- Role-based visibility rules (Own / Team / Full) — the backbone every later module plugs into
- Sales Rep → Sales Manager reporting structure ("Reports To")
- Left sidebar navigation shell and top bar (search, quick-create, notifications, calendar, profile — placeholders wired up, populated in later phases)
- Leads — create, import (CSV), list + Kanban (by status) views, New → Qualified → Converted → Junk lifecycle
- Lead Conversion — one-click conversion that creates/links an Account, Contact, and Deal
- Contacts — create, import, linked to Accounts; AI-generated conversation summary on a contact's history
- Accounts — create, import, detail page with tabs for Contacts/Deals/Activities
- AI-powered duplicate detection on Accounts — flags likely-duplicate companies at creation time and asks the rep to confirm before a new record is made
- Deals — create, import, 6-stage pipeline (Qualification → Discovery → Proposal → Negotiation → Closed Won/Lost) with built-in win probabilities; list + Kanban (by stage) views with per-column totals; stage names, order, and win probabilities are Admin-configurable
- Deals surface next follow-up and last interaction dates on every record, so a rep or manager can see at a glance when a deal was last touched
- Filtering, sorting, and bulk actions across all four modules

**Stakeholder demo at end of phase:** Log in as three different role types and show each sees a correctly scoped view; walk a lead from creation through conversion into a Deal, dragging it across pipeline stages on the Kanban board, and show the duplicate-account check firing on a repeat company name.

## Phase 2 — Activities, Documents, Dashboards & Reporting

**Duration:** 12 days

**Why this comes here:** Once Deals and Contacts exist, the day-to-day work of engaging with them (calls, meetings, tasks, notes) needs a home — and that same activity and pipeline data is what makes dashboards and reporting meaningful rather than empty or fake. These two phases are combined since reporting is built directly on top of the activity data shipped earlier in the same phase.

**What ships**

- Tasks — subject, due date, status, priority, linked to any record
- Meetings — title, time range, host, linked to any record;
- Calls — inbound/outbound, duration, linked to any record
- Notes — free-form notes attachable to any Lead, Contact, Account, or Deal, shown on the shared timeline
- Activity Timeline — unified, date-ordered history on every Lead/Contact/Account/Deal page
- Documents — upload, list, and link files to Accounts or Deals (version control remains a post-launch roadmap item)
- Home Dashboard — KPI widgets, My Open Tasks, My Meetings, Today's Leads, Deals Closing This Month (auto-scoped to Own/Team/Full by role)
- Reports — six pre-built reports across Lead, Deal, and Activity folders; custom report building remains a future-version capability, not V1
- Analytics Dashboard — org-wide health snapshot (Open Deals, Pipeline by Stage, Leads This Month, Activity Stats)
- Platform polish — global search across Leads/Contacts/Accounts/Deals, quick-create (+) menu, notifications, calendar view

**Stakeholder demo at end of phase:** Open a Deal and show its full timeline of calls, meetings, tasks, notes, and attached documents in one scroll; then show a manager logging in and immediately seeing team health at a glance, without asking a rep for a status update.

## Phase 3 — AI Capabilities

**Duration:** 12 days

**Why this comes here:** Every AI feature here is a layer on top of real behavioral data — lead source/response time, deal activity gaps, call/meeting notes. Building AI first would mean scoring and flagging against empty records, which produces meaningless (or untestable) output. This phase is also explicitly designed so the AI never acts unilaterally — it scores, drafts, flags, and summarizes, but a person always makes the final call, and it never grants access beyond what a user could already see.

**What ships**

- Smart Lead Scoring — 0–100 score with plain-language reasoning, refreshed automatically overnight and instantly on status/activity changes; scoring weights are Admin-tunable
- AI-Drafted Follow-up Emails — editable drafts generated from record + activity history, never auto-sent
- Deal Risk Alerts — flags stalled or at-risk deals (no activity in ~a week, or an approaching close date without progress) with a specific reason; visible on the Deals list, pipeline board, and the Home dashboard's Untouched Deals widget; dismissible by a rep
- Meeting & Call Summarization — AI summary + suggested next step from pasted notes/transcripts, shown by default on the shared Activity Timeline (full original notes one click away); one-click conversion of the next step into a follow-up task
- Conversational AI Assistant (RAG Chatbot) — chat panel available anywhere in the CRM, answers grounded in the org's own CRM data (deals, activities, contacts, documents), scoped to the same Own/Team/Full visibility rules, with every answer linking back to its source record

**Stakeholder demo at end of phase:** Show a rep's lead list re-sorting itself by AI score, a stalled deal getting flagged with a clear reason, and a rep asking the chatbot a plain-language question about their pipeline.

---

Total V1 build time: 36 days across three phases (12 days each).

Note: this document sequences features by dependency, not by calendar time beyond the stated per-phase durations. Actual delivery dates depend on team velocity and staffing.
