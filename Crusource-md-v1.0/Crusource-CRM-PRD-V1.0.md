# Crusource CRM — Product Requirements Document

| Field | Detail |
| --- | --- |
| Product | Crusource CRM |
| Document Type | Product Requirements Document (PRD) |
| Version | 1.0 |
| Status | Draft for Stakeholder Review |
| Date | July 30, 2026 |
| Prepared For | Product, Engineering, Design & Executive Stakeholders |

*Confidential — Internal Use Only*

---

## Table of Contents

1. Introduction
    - 1.1 Purpose of This Document
    - 1.2 Product Summary
2. Problem Statement & Purpose
3. Target Users
4. Business Goals & Objectives
5. Product Scope
    - 5.1 In Scope
    - 5.2 Out of Scope
6. Key Features
    - 6.1 Navigation & Workspace
    - 6.2 Core Sales Modules
    - 6.3 Reporting & Analytics
    - 6.4 Administration
7. AI Capabilities
8. Roles & Access Control
9. Key User Journeys
    - 9.1 Admin — Organization & User Setup (One-Time)
    - 9.2 Sales Rep — Lead to Closed Deal (Core Journey)
    - 9.3 Sales Manager — Team Oversight
    - 9.4 Admin — Ongoing Monitoring
10. Business Rules
11. Success Metrics
12. Risks & Assumptions
    - 12.1 Risks
    - 12.2 Assumptions
13. Future Enhancements (Post-V1 Roadmap)
14. Glossary

## 1. Introduction

### 1.1 Purpose of This Document

This Product Requirements Document (PRD) defines the vision, scope, features, and success criteria for Crusource CRM, a B2B sales CRM platform. It is intended to align business stakeholders, product managers, designers, and engineering teams on what the product does, why it exists, and the value it delivers.

### 1.2 Product Summary

Crusource CRM is a web-based system that helps a sales organization manage the entire sales process in one place — from the moment a potential customer is identified through to closing the deal, with a complete record of every interaction along the way. The platform combines a standardized sales workflow with a set of AI-assisted capabilities designed to reduce manual work while keeping a human in control of every decision. Every organization operates inside a single, isolated shared workspace — there is no mixing of data between customers of the platform. New organizations start with a 14-day free trial with full feature access; continued use after the trial requires an active paid subscription.

## 2. Problem Statement & Purpose

Sales teams without a structured CRM lose revenue in predictable ways: leads go uncaptured or unfollowed, deal context lives in individual inboxes and notebooks, pipeline visibility depends on manually chasing reps for updates, and managers only learn a deal is at risk after it is already lost.

Crusource CRM exists to close these gaps by giving every organization:

- A single source of truth for leads, contacts, accounts, and deals.
- A consistent, repeatable sales process that scales as the team grows.
- Automatic visibility into pipeline health and rep performance, without manual status reporting.
- AI assistance that removes repetitive work (scoring, drafting, summarizing) while leaving all judgment calls to the human seller.
- Role-based access so data is only ever visible to the people who should see it.

## 3. Target Users

Crusource CRM is built for small-to-mid-sized B2B sales organizations. Within a customer organization, the product serves three groups of users, each with different day-to-day priorities. (How each group's access is enforced in the product is covered separately in Section 8, Roles & Access Control.)

| User Group | Day-to-Day Priorities | What They Need From the Product |
| --- | --- | --- |
| Front-line Sellers | Working a personal book of leads, contacts, accounts, and deals; hitting individual quota. | A focused view of their own work, fast data entry, and AI help with routine tasks like drafting and summarizing. |
| Sales Leadership | Accountable for a team's pipeline and performance; coaching and unblocking reps. | Real-time visibility into every deal their team is working, without chasing reps for status updates. |
| Organizations | Keeps the CRM configured correctly and the team's access accurate as it grows and changes. | Simple control over onboarding, configuration, and org-wide reporting, without engineering involvement. |

## 4. Business Goals & Objectives

Crusource CRM is designed to deliver measurable business outcomes for the organizations that adopt it:

- **Capture more revenue opportunity** — ensure no lead goes unlogged or unfollowed by making capture and qualification a structured, mandatory step.
- **Increase win rates** — standardize the sales pipeline and surface at-risk deals before they stall, so reps act sooner.
- **Reduce administrative overhead** — use AI to handle repetitive work (scoring, drafting, summarizing) so reps spend more time selling.
- **Improve forecasting accuracy** — a consistent, stage-based pipeline with built-in win probabilities gives leadership a reliable read on revenue.
- **Enable data-driven management** — give Sales Managers and Admins real-time visibility into team and organizational performance without manual reporting.
- **Protect data integrity as the team scales** — role-based access and clean ownership transfer keep records accurate through hiring, promotions, and departures.

## 5. Product Scope

### 5.1 In Scope

delivers the full core sales cycle plus a first layer of AI-assisted capabilities:

- Lead capture, qualification, and conversion to Account / Contact / Deal.
- Account and Contact management with a unified 360° relationship view.
- A standardized, configurable six-stage deal pipeline (list and kanban views).
- Activity tracking — Tasks, Meetings, Calls, and Notes — with a unified activity timeline per record.
- Document storage linked to Accounts and Deals.
- Six pre-built reports plus an organization-wide analytics dashboard.
- Role-based user and access management (Admin, Sales Manager, Sales Rep).
- AI-assisted lead scoring, email drafting, deal risk alerts, meeting/call summarization, duplicate-account detection, and a conversational CRM assistant.
- In-app feedback and feature request submission.

### 5.2 Out of Scope

A small number of capabilities were deliberately deferred beyond Version 1 to keep the initial release focused. These are listed in full in Section 13, Future Enhancements.

## 6. Key Features

The table below summarizes each functional area at a business level. Full workflow, field, and screen-level detail is maintained in the supporting Features and User Story documentation.

### 6.1 Navigation & Workspace

| Capability | What It Does | Business Value |
| --- | --- | --- |
| Home Dashboard | A personal, role-aware landing page showing key numbers, open tasks, upcoming meetings, today's leads, and deals closing soon. | Every user starts the day knowing exactly what needs attention — no separate reporting required. |
| Global Search | Searches across Leads, Contacts, Accounts, and Deals from a single bar. | Users find any record instantly without knowing which module it lives in. |
| Quick-Create (+) | Creates a new Lead, Contact, Account, Deal, Document, Task, Meeting, or Call from anywhere in the system. | Removes friction from logging work in the moment, improving data completeness. |
| Workqueues | A prioritized working list of records needing attention. | Helps reps and managers focus on what matters most, rather than browsing full lists. |
| Notifications & Calendar | Alerts on due tasks and assignments; at-a-glance view of upcoming meetings and deadlines. | Reduces missed follow-ups and dropped commitments. |

### 6.2 Core Sales Modules

| Module | What It Does | Business Value |
| --- | --- | --- |
| Leads | Captures and qualifies potential customers through a New → Qualified → Converted (or Junk) status flow, with manual entry, bulk import, and list or pipeline-board views. One-click conversion creates the linked Account, Contact, and Deal. | Ensures no interest goes untracked and standardizes how raw interest becomes a real opportunity. |
| Contacts | Manages the individual people a rep works with, linked to their company (Account), with AI-summarized conversation history. | Preserves relationship context even when a rep changes territory or leaves the company. |
| Accounts | A single page per company showing every related Contact, Deal, and Activity, with AI-powered duplicate detection on creation. | Gives anyone a complete, instant view of a customer relationship and prevents fragmented duplicate records. |
| Deals | Tracks active sales opportunities through a standardized, configurable six-stage pipeline with built-in win probabilities, list and kanban views, and next-follow-up tracking. | Keeps pipeline and revenue forecasting consistent across every rep and manager. |
| Documents | A file library linking proposals, contracts, and other files directly to the Account or Deal they belong to. | Keeps paperwork accessible to the whole team instead of scattered across email or personal drives. |
| Activities (Tasks, Meetings, Calls, Notes) | Logs all day-to-day selling work, each linked to the record it relates to and shown on a unified activity timeline. | Gives anyone picking up a relationship — a manager, or a colleague covering — the complete engagement history in one view. |

### 6.3 Reporting & Analytics

| Capability | What It Does | Business Value |
| --- | --- | --- |
| Pre-Built Reports | Six ready-made reports covering lead sources and status, pipeline distribution and win/loss rate, outstanding and overdue activities, and individual Sales Rep performance. | Gives the team instant answers to common sales questions without manual reporting. |
| Analytics Dashboard | An organization-level view of open deals, pipeline by stage, monthly lead trends, and activity statistics. | Gives leadership a real-time pulse on sales health so problems surface early enough to act on. |

### 6.4 Administration

| Capability | What It Does | Business Value |
| --- | --- | --- |
| User & Role Management | Admins add users, assign roles, edit details, deactivate access, assign reps to managers, and transfer record ownership between users. | Lets the organization manage access safely as the team grows or changes, without ever losing historical data. |
| Feedback & Feature Requests | Any user can submit feedback or request a feature directly from within the system. | Gives the product team a direct channel to the people using the CRM every day. |

## 7. AI Capabilities

A guiding principle governs every AI feature in Crusource CRM: the AI never acts on its own. It scores, drafts, flags, and summarizes — but a person always reviews and decides before anything is sent, dismissed, or acted on. AI features also introduce no new access rules: users only ever see AI output for records they could already see.

| Capability | What It Does | Human Control |
| --- | --- | --- |
| Smart Lead Scoring | Automatically scores every open lead 0–100 based on source, follow-up speed, and status, with a plain-language reason. Refreshes overnight and on record change; scoring weights are Admin-configurable. | Informs prioritization only — reps still choose how to act. |
| AI-Drafted Follow-up Emails | Generates an editable draft follow-up email from a Lead, Contact, or Deal's details and recent activity. | Nothing is ever sent automatically; the rep edits, regenerates, or discards before sending. |
| Deal Risk Alerts | Flags deals that have gone quiet or are approaching their closing date without progress, with a specific reason, surfaced on the Deals list, pipeline board, and Home dashboard. | Reps can dismiss a flag as a false alarm or resolve it by logging an activity. |
| Meeting & Call Summarization | Turns pasted notes or a transcript into a short summary and a suggested next step, shown by default on the activity timeline. | Full original notes remain one click away; the suggested next step becomes a task only if the rep chooses. |
| AI Duplicate Detection | Flags likely duplicate Accounts at creation and asks the rep to confirm before a new record is saved. | Rep makes the final call on whether it's a duplicate or a genuinely new account. |
| Conversational AI Assistant | A chat panel, available anywhere in the CRM, that answers plain-language questions using the organization's own CRM data, with every answer linked to its source record. | Answers are scoped to what the asking user can already see (Own / Team / Full), matching standard access rules. |

Additional AI capabilities planned beyond Version 1 — including proactive reminders and an automatic daily Workqueue — are listed in Section 13, Future Enhancements.

## 8. Roles & Access Control

Access follows one consistent rule across every module in the system, so the same screen shows different amounts of data depending on who is logged in — without separate systems or manual reporting.

| Role | Data Visibility | Key Permissions |
| --- | --- | --- |
| Sales Rep | Only records they personally own. | Manage own leads, contacts, accounts, deals, and activities; use all AI features and the chatbot scoped to their own data. |
| Sales Manager | Own records plus every record owned by Sales Reps who report to them. | Everything a Sales Rep can do, plus: open any report's individual dashboard, act on a rep's behalf, assign tasks to reps, and run team-level reports. |
| Admin | Full organization — every user, role, and record, with no restrictions. | Everything above, plus: manage users and roles, configure pipeline stages and lead-scoring weights, and the only role able to manage other users. |

## 9. Key User Journeys

The four journeys below summarize how each role experiences the product end to end. Detailed step-by-step flows are maintained in the supporting Product Journey documentation.

### 9.1 Admin — Organization & User Setup (One-Time)

Before anyone else can log in, the Admin creates each teammate's account and assigns a role. Sales Reps are linked to a Sales Manager via a "Reports To" relationship, which determines what that manager can see as their team. From this point on, every screen a user sees is automatically scoped by their role.

### 9.2 Sales Rep — Lead to Closed Deal (Core Journey)

This is the journey the product is built around. A rep logs in to a personal Home dashboard, then works a new lead — logging calls, creating tasks, scheduling meetings — and updates its status as it's qualified. Converting the lead automatically creates the linked Account, Contact, and Deal. The rep then drags the deal through the pipeline, logging activities and attaching documents along the way, until it closes as Won or Lost. The result: one lead becomes a fully documented Account, Contact, and Deal, with a complete activity trail and any related documents all visible in one place.

### 9.3 Sales Manager — Team Oversight

A Sales Manager's Home dashboard and every module automatically reflect their whole team's data, not just their own. They can browse any rep's records, view the team's combined pipeline on the kanban board to spot stalled deals, and run team-scoped Pipeline and Win-Loss reports — all without needing access to Settings → Users, which remains Admin-only.

### 9.4 Admin — Ongoing Monitoring

On an ongoing basis, the Admin's Home dashboard and reports reflect the entire organization. Admins deactivate departing employees or reassign reps to a different manager as the team changes, and retain full read/write access to every record for data cleanup, reassignment, or troubleshooting — all without ever deleting a departed user's historical data.

## 10. Business Rules

| Area | Rule |
| --- | --- |
| Tenancy | Each organization operates in a single, isolated shared workspace; there is no mixing of data across organizations. |
| Provisioning | There is no self-service sign-up. Only an Admin can add a new user, and every new user is assigned one of exactly three roles at creation. |
| Subscription | Every new organization receives a 14-day free trial with full platform access; continued use requires an active paid subscription. |
| Lead Lifecycle | A lead moves through New → Qualified → Converted, or is marked Junk. Once converted, a lead becomes read-only and all further work happens on the resulting Deal. |
| Lead Conversion | Converting a lead automatically creates or links an Account and a Contact, and creates a new Deal — this is the single mechanism by which a lead becomes an opportunity. |
| Pipeline Stages | Deals move through six stages (Qualification, Discovery, Proposal, Negotiation, Closed Won, Closed Lost) each with a built-in win probability; an Admin may customize stage names, order, and probabilities. |
| Access Model | Visibility is strictly Own (Sales Rep) / Own + Team (Sales Manager) / Full Organization (Admin), enforced consistently across every module, report, and the AI assistant. |
| User Deactivation | Deactivating a user immediately revokes login access but never deletes the records or activity history they created. |
| Ownership Transfer | A user's leads, contacts, accounts, deals, and activities can be reassigned to another user, keeping ownership clean through role changes, territory changes, or departures. |
| AI Governance | No AI capability acts autonomously — every AI output (score, draft, alert, summary) requires human review before it affects a record or is sent externally. AI never expands what a user can already see. |

## 11. Success Metrics

Success will be measured across four categories, spanning adoption, sales efficiency, AI impact, and business outcomes.

| Category | Metric | What It Tells Us |
| --- | --- | --- |
| Adoption | Daily/weekly active users by role | Whether reps and managers have made the CRM part of their daily workflow. |
| Adoption | % of trial organizations converting to paid subscription | Whether the product delivers enough value during the trial to justify payment. |
| Sales Efficiency | Lead response time and lead-to-conversion rate | Whether structured lead capture and qualification are shortening the path to a real opportunity. |
| Sales Efficiency | Average deal cycle time and win rate by stage | Whether a standardized pipeline is improving deal velocity and outcomes. |
| Sales Efficiency | % of deals with no activity logged in 7+ days | Whether deals are being actively worked or left to go stale. |
| AI Impact | AI-drafted email adoption rate and edit rate | Whether AI drafts are genuinely saving rep time versus being discarded. |
| AI Impact | % of flagged at-risk deals resolved vs. dismissed | Whether risk alerts are accurate and actionable. |
| Business Outcome | Forecast accuracy (predicted vs. actual closed revenue) | Whether the standardized pipeline is producing a reliable revenue signal for leadership. |
| Business Outcome | Sales Manager time spent compiling status reports | Whether built-in reporting is reducing manual reporting overhead. |

## 12. Risks & Assumptions

### 12.1 Risks

| Risk | Potential Impact | Mitigation |
| --- | --- | --- |
| Low data-entry discipline by reps | Incomplete records undermine AI scoring, reporting accuracy, and manager visibility. | Quick-create tools, bulk import, and a low-friction activity logging flow reduce the effort required to keep records current. |
| Over-reliance on AI outputs | A rep acts on an AI score, draft, or alert without verifying it, sending inaccurate information externally. | Human-in-the-loop design: nothing is sent or changed automatically; every AI output requires explicit review and action. |
| Fixed six-report set feels limiting to larger teams | Power users may feel unable to answer bespoke questions without a custom report builder. | Custom report builder is scoped for a future release; V1 reports are designed to cover the most common questions. |
| Role model may not fit every org structure | Some organizations use flatter or more complex hierarchies than Rep/Manager/Admin. | The three-role model covers the majority of B2B sales org structures; more granular permissions can be considered post-V1. |
| Trial-to-paid conversion risk | Organizations experience the product only during a 14-day window before needing to commit financially. | Full feature access during trial ensures the evaluation reflects the real product value. |

### 12.2 Assumptions

- Each customer organization is a single company operating as one shared workspace, with no need for sub-organizations or business units.
- The three-tier role model (Admin, Sales Manager, Sales Rep) is sufficient to represent target customers' sales team structures.
- Users have a reliable internet connection and access the platform via a standard web browser.
- Organizations are willing to have AI-generated content (scores, drafts, summaries) reviewed and approved by a human before it is acted upon, rather than requiring full automation.
- Reports and dashboards refresh on a schedule appropriate for daily sales operations, not real-time trading-style updates.

## 13. Future Enhancements (Post-V1 Roadmap)

The following capabilities are acknowledged in current product direction but are explicitly out of scope for Version 1:

- **Custom Report Builder** — allow users to build their own reports from scratch, beyond the six pre-built reports.
- **Document Version Control** — track updates to uploaded files and allow earlier versions to be revisited.
- **Proactive AI Assistant** — daily task reminders, on-demand data summaries, and an automatic next-day Workqueue generated from a rep's end-of-day chat wrap-up.
- **Expanded Integrations** — native email and calendar sync, and marketing automation connections, to reduce duplicate data entry.

## 14. Glossary

| Term | Definition |
| --- | --- |
| Lead | A potential customer who has shown interest but has not yet been qualified as a real sales opportunity. |
| Contact | An individual person a sales rep works with, linked to the company (Account) they belong to. |
| Account | The company or organization a deal is ultimately made with. |
| Deal | An active, in-progress sales opportunity tracked through the pipeline. |
| Activity | A Task, Meeting, Call, or Note logged against a Lead, Contact, Account, or Deal. |
| Workqueue | A prioritized working list surfacing records that need a user's attention. |
| Pipeline | The standardized sequence of stages a Deal moves through from Qualification to Closed Won/Lost. |
