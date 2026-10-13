# Crusource Superadmin — Product Requirements

**Status:** Draft for designer review  
**Audience:** Product owner and UI/UX designer  
**Companion:** [User-facing data flows](SUPERADMIN_DFD.md)  
**Scope:** First release of the unified Crusource Superadmin portal for CRM and VMS

---

## Contents

1. [Purpose](#1-purpose)
2. [Background and problem](#2-background-and-problem)
3. [Goals and non-goals](#3-goals-and-non-goals)
4. [Vocabulary](#4-vocabulary)
5. [The most important design requirement: topbar product switcher](#5-the-most-important-design-requirement-topbar-product-switcher)
6. [Users and roles](#6-users-and-roles)
7. [Sign-in, session, and staff access](#7-sign-in-session-and-staff-access)
8. [Navigation and screen requirements](#8-navigation-and-screen-requirements)
9. [Screen-by-screen requirements](#9-screen-by-screen-requirements)
10. [Key interactions](#10-key-interactions)
11. [States the designer must cover](#11-states-the-designer-must-cover)
12. [Content, privacy, and data presentation rules](#12-content-privacy-and-data-presentation-rules)
13. [First-release scope](#13-first-release-scope)
14. [Reviewable defaults and open questions](#14-reviewable-defaults-and-open-questions)
15. [Designer handoff](#15-designer-handoff)
16. [Acceptance checklist](#16-acceptance-checklist)

---

## 1. Purpose

Create **one internal Crusource portal** where Crusource staff can track and manage customer organizations, customer users, subscriptions, requests, and product operations for both **CRM** and **VMS**.

- **Crusource** is the product and portal name.
- **CRM** and **VMS** are the two platforms within Crusource.
- Customer administrators continue to use their own CRM or VMS applications. This portal is for Crusource staff only.
- The existing separate per-platform Superadmin portals will be retired once the unified portal has been validated.

This document describes the **desired experience**. It does not imply that every feature already exists in either application. Placeholder screens are not evidence that a feature works.

---

## 2. Background and problem

Today, staff manage each platform through a separate Superadmin portal. This causes several problems:

| Problem                                      | Effect on staff                                                             |
| -------------------------------------------- | --------------------------------------------------------------------------- |
| Separate sign-ins and separate navigation    | Staff switch between portals and relearn layouts for each platform.         |
| No view of customers that use both platforms | Staff cannot easily see that one organization uses CRM and VMS.             |
| Billing spread across platforms              | Staff cannot see an organization's full subscription position in one place. |
| Different labels and metrics per platform    | Numbers are hard to compare and easy to misread.                            |
| Separate staff access management             | Granting or revoking internal access must be repeated per platform.         |

The unified portal solves these by giving staff **one sign-in, one navigation template, one switcher, common billing, and shared staff access**, while keeping each platform's customer data clearly separate.

---

## 3. Goals and non-goals

### 3.1 Goals

1. **One place for both platforms:** staff manage CRM and VMS from the same portal and the same account.
2. **Predictable navigation:** every platform screen looks and behaves the same for CRM and VMS; only the data changes.
3. **Clear platform context:** staff always know which platform's information they are viewing and which platform an action will affect.
4. **Common billing:** each organization's CRM and VMS subscriptions, invoices, payments, trials, and renewals are visible together.
5. **Safe administration:** every change states its exact target, requires confirmation and a reason, shows a true result, and is recorded.
6. **Trustworthy information:** loading, stale, unavailable, and empty states are never confused with real values.

### 3.2 Non-goals for the first release

- An “All Products” view that mixes CRM and VMS data on platform screens.
- Customer-facing features; customers never use this portal.
- Exposing customer business content (deals, candidates, documents) on summary screens.
- Second-person approval workflows.
- Dark mode and multilingual variants.
- Roles beyond Super Admin and Sub Admin.

---

## 4. Vocabulary

| Term                        | Meaning                                                                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Platform**                | CRM or VMS.                                                                                                                            |
| **Selected platform**       | The platform chosen in the topbar switcher.                                                                                            |
| **Platform screen**         | A screen showing selected-platform data: Overview, Organizations, Users, Requests & Feedback, Activity & Security, Product Operations. |
| **Shared screen**           | A screen unaffected by the switcher: Billing, Pricing & Plans, Staff & Access, or Integrations.                                        |
| **Staff**                   | Internal Crusource employees using this portal.                                                                                        |
| **Customer**                | An organization or person using CRM, VMS, or both.                                                                                     |
| **Combined profile**        | One confirmed organization or person, shown once, with separate CRM and VMS memberships.                                               |
| **Platform membership**     | A customer's role, access status, member count, subscription state, and activity within one platform.                                  |
| **Administrative activity** | The record of staff actions: actor, platform, customer, action, result, time, and reason.                                              |
| **Stale information**       | The last successfully loaded information, shown with its timestamp while a fresh update is unavailable.                                |

---

## 5. The most important design requirement: topbar product switcher

> **Place a prominent CRM / VMS switcher in the topbar on every signed-in screen. Switching changes the platform data; the menu template and equivalent screen remain the same. Billing is common and does not change. Pricing & Plans, Staff & Access, and Integrations are also shared screens. There is no “All Products” option.**

### 5.1 Conceptual layout

Placement and behaviour only — not a prescribed visual design:

```text
CRUSOURCE       Product: [ CRM | VMS ]       Search       Staff profile
                         ^
                         Always clearly show the selected platform

Menu                    Selected screen
Overview                CRM organizations and CRM users
Organizations           Switch to VMS → same screen, VMS data
Users
Billing                 Common billing for CRM and VMS  (Shared)
Pricing & Plans         CRM and VMS plan catalog  (Shared)
Contact Us              Selected-platform inquiries
Requests & Feedback     Separate tabs: Demos, Trial Requests, Feedback
Activity & Security
Product Operations
Staff & Access          Internal staff for both platforms  (Shared)
Integrations            Gmail and Google Calendar  (Shared)
```

### 5.2 Why this matters

Staff frequently move between platforms while investigating the same customer. Keeping the screen and template constant while swapping only the data means staff never lose their place, and comparisons between platforms are straightforward. The switcher must therefore be **always visible, always accurate, and never ambiguous**.

### 5.3 Switcher behaviour

| Situation                                         | Required behaviour                                                                |
| ------------------------------------------------- | --------------------------------------------------------------------------------- |
| Overview: CRM → VMS                               | Stay on Overview; replace CRM metrics with VMS metrics in the same positions.     |
| Organizations: CRM → VMS                          | Stay on Organizations; show only organizations using VMS.                         |
| Users: CRM → VMS                                  | Stay on Users; show only accounts belonging to VMS.                               |
| Requests, activity, or operations: CRM → VMS      | Stay on the equivalent screen; replace the platform-specific records.             |
| Billing: CRM → VMS                                | Remain on Billing; keep the same combined billing records.                        |
| Staff & Access: CRM → VMS                         | Keep the same internal staff records; staff serve both platforms.                 |
| Organization/user detail exists in both platforms | Keep the same combined profile open; activate the selected platform's section.    |
| Search/filter valid in both platforms             | Keep the search, shared filters, and sorting; reset pagination to the first page. |

### 5.4 Loading and accuracy rules

- The selected label changes **immediately** when staff switch.
- Previous-platform values are cleared at once and replaced with loading placeholders.
- **Never display CRM values under a VMS label, or VMS values under a CRM label**, even briefly.
- Both switcher options are visible to Super Admin and Sub Admin. Product visibility is shared; permitted actions follow the role and assigned permission profile.

### 5.5 Accessibility expectations

- The switcher must be operable by keyboard and clearly announce the selected platform.
- The selected state must not rely on colour alone.
- The switcher must remain reachable on narrow screens.

---

## 6. Users and roles

The first release has exactly two internal roles.

| Role            | Who                                      | Responsibility                                                                                                           |
| --------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Super Admin** | The first designated owner of the portal | All product and billing actions; invites, manages, and revokes Sub Admins.                                               |
| **Sub Admin**   | Internal staff, including developers     | Views both platforms; administers organizations and users, handles requests, troubleshoots, reads operational summaries. |

### 6.1 Starting permission defaults

| Area                    | Action                                     | Super Admin | Sub Admin    |
| ----------------------- | ------------------------------------------ | ----------- | ------------ |
| Navigation              | See both CRM and VMS                       | Yes         | Yes          |
| Organizations and users | Search and view profiles                   | Yes         | Yes          |
| Organizations and users | Change customer memberships                | Yes         | Yes          |
| Organizations and users | Suspend or reactivate                      | Yes         | No           |
| Organizations and users | Confirm shared customer links              | Yes         | No           |
| Billing                 | Inspect                                    | Yes         | Yes          |
| Billing                 | Extend trials                              | Yes         | Yes          |
| Billing                 | Plan changes, discounts, refunds, renewals | Yes         | No           |
| Requests & Feedback     | Assign, resolve, approve, reject           | Yes         | Yes          |
| Activity & Security     | View and export permitted summaries        | Yes         | Yes          |
| Product Operations      | Inspect status and usage                   | Yes         | Yes          |
| Product Operations      | Feature changes and provisioning           | Yes         | As permitted |
| Support access          | Start a support session                    | Yes         | As permitted |
| Staff & Access          | Invite, cancel, re-send, revoke            | Yes         | No           |
| Staff & Access          | Change the Super Admin account             | —           | No           |

The Sub Admin column above represents starting grants, not fixed entitlements. The Super Admin configures action permissions through the profiles in section 9.11. Internal access management stays owner-only.

### 6.2 Role rules

- Customer membership changes never grant internal Superadmin access.
- A Sub Admin cannot alter the Super Admin account.
- No second-person approval is required. Sensitive actions still require confirmation and a reason.
- When an action is not permitted, the portal explains which permission is required rather than hiding the action without explanation.

---

## 7. Sign-in, session, and staff access

### 7.1 Sign-in

- One internal account serves both platforms.
- Sign in using **email and password only**. No MFA enrolment, challenge, or second verification step is included.
- Include forgot-password/reset-password, session expiry after inactivity, and sign-out from the staff profile menu. Email invitation and password-reset links are account setup/recovery, not additional login factors.
- Invalid details produce a clear error that does not reveal which part was wrong.
- After sign-in, staff land on **Overview** with their last selected platform (first-time default: CRM).
- Staff accounts and customer accounts must be visibly separate. Customer credentials are never accepted here.

### 7.2 Session expiry and revocation

- An expired session returns staff to sign-in without completing any pending action.
- Revoked staff lose access to both platforms immediately; any open session ends with an explanation.
- After signing in again, staff return to the screen they were on where practical.

### 7.3 Staff invitation lifecycle

| Status        | Meaning                                        | Available actions (Super Admin) |
| ------------- | ---------------------------------------------- | ------------------------------- |
| **Pending**   | Invitation sent, not yet activated             | Cancel, re-send                 |
| **Expired**   | Invitation not used within its validity period | Re-send                         |
| **Active**    | Account activated; access to both platforms    | Revoke                          |
| **Revoked**   | Access removed for both platforms              | —                               |
| **Cancelled** | Invitation withdrawn before activation         | —                               |

All staff-access changes are recorded in shared staff-access history.

---

## 8. Navigation and screen requirements

All items remain in the same order for CRM and VMS. Shared screens carry a clear **“Shared across CRM and VMS”** label. Colours, icons, detailed spacing, and responsive layouts are the designer's responsibility.

| Menu item           | Type     | Purpose and content                                                                                    | Main actions                                                                                                              |
| ------------------- | -------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Overview            | Platform | Same metric layout for the selected platform; attention list and recent activity                       | Open an organization, user, or request                                                                                    |
| Organizations       | Platform | Selected-platform customers, product badges, account status, owner/contact, member count               | Search/filter; open profile; permitted suspension/reactivation                                                            |
| Users (not needed)  | Platform | Selected-platform customer accounts, organization, membership role, status, last activity              | Search/filter; open combined profile; permitted membership/access changes                                                 |
| Billing             | Shared   | Common organization billing, CRM/VMS line items, plans, invoices, payment status, renewals, and trials | Review invoices/payments; manage plans, renewals, trials, discounts, and refunds according to role and permission profile |
| Requests & Feedback | Platform | Selected-platform feedback, demo requests, and trial-extension requests                                | Inspect, assign, resolve, approve/reject as applicable                                                                    |
| Activity & Security | Platform | Selected-platform customer login history and administrative activity                                   | Search/filter; inspect event details; export permitted summaries                                                          |
| Product Operations  | Platform | Selected-platform availability, refresh status, administrative usage, and feature settings             | Inspect status; permitted feature changes and provisioning                                                                |
| Staff & Access      | Shared   | Internal staff directory, roles, invitation status, and access status                                  | Super Admin invites, cancels, re-sends, or revokes Sub Admins                                                             |

Additional navigation items, in the same order under both product selections:

| Menu item                               | Type                                    | Purpose                                                    | Main actions                                         |
| --------------------------------------- | --------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| Pricing & Plans (after Billing)         | Shared                                  | Dynamic CRM/VMS plan catalog and revisions                 | Draft, preview, publish, archive with permission     |
| Contact Us (before Requests & Feedback) | Platform plus labelled unassigned queue | General and sales inquiries, separate from feedback        | Assign, reply, resolve, create demo request          |
| Integrations (after Staff & Access)     | Shared                                  | Gmail and Google Calendar connections and booking defaults | Super Admin connects/configures; permitted staff use |

Requests & Feedback has separate Demos, Trial Requests, and Feedback tabs. Staff & Access includes personal staff profiles and reusable permission profiles.

The topbar also includes a **search** entry point and the **staff profile** menu (name, role, sign-out).

---

## 9. Screen-by-screen requirements

### 9.1 Overview

**Purpose:** a quick, trustworthy summary of the selected platform and a starting point for follow-up work.

**Metrics** — same labels and positions for CRM and VMS:

| Metric                               | Recommended definition                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| Total and active organizations       | Active = enabled for the selected platform; subscription state shown separately |
| Total and active customer accounts   | Active = signed in within the last 30 days                                      |
| New organizations (last 30 days)     | Organizations added to the selected platform in the period                      |
| New customer accounts (last 30 days) | Accounts added to the selected platform in the period                           |
| Trials ending within seven days      | Selected-platform trials ending in the next seven days                          |
| Pending requests, by type            | Unresolved feedback and demo requests; trial extensions awaiting a decision     |

**Additional content**

- **Attention list:** items needing action, such as trials about to end or pending requests.
- **Recent activity:** latest administrative actions for the selected platform.

**Rules**

- Show each metric's period and last-updated time.
- Billing totals belong on the Billing screen.
- Never add CRM and VMS account counts together and label the result as unique people.
- An unavailable metric shows “Unavailable”, never zero.

### 9.2 Organizations

**List columns:** organization name, CRM/VMS usage badges, account status for the selected platform, owner/primary contact, member count.

**Filters:** status, plan or subscription state, created date, and text search. Filters that exist only in one platform are cleared when switching.

**Rules:** only organizations using the selected platform appear.

### 9.3 Organization profile

**One organization profile with two platform sections is the recommended design.**

- **Shared header:** organization name, customer reference, primary contact, CRM/VMS usage badges, and a link to common billing.
- **Detail template** (same in both platforms): **Summary, Members, Requests, Activity**.
- **Platform sections:** clearly identified CRM and VMS sections. The topbar selection controls which section is active; selecting the other section updates the topbar.

| Organization uses | Appears in              | Inside the profile                            |
| ----------------- | ----------------------- | --------------------------------------------- |
| Both              | CRM and VMS directories | Two active platform memberships               |
| CRM only          | CRM directory only      | VMS section shows “Not in use” (not an error) |
| VMS only          | VMS directory only      | CRM section shows “Not in use” (not an error) |

**Rules**

- Platform-specific member counts, subscription state, usage, and suspension status remain separate.
- Suspending CRM access must not silently suspend VMS or cancel billing.
- Provisioning the other platform is an explicit, permitted action with its own result.

### 9.4 Billing (shared)

**Recommended design:** one organization billing profile with separate CRM and VMS subscription items.

- **Billing list:** organizations with their CRM and VMS subscription status, payment status, and next renewal or trial end.
- **Line-item filter:** an optional CRM/VMS filter belonging to Billing. The global switcher does not change this filter or billing results.
- **Organization billing profile:**
  - Separate CRM and VMS subscription items, each with its own plan, status, trial, and renewal date.
  - Invoices and payment history. Where supported, an invoice groups both product line items. Existing separate invoices remain visible with their original product and reference.
- **Actions:** review invoices and payments; manage plans, renewals, trials, discounts, and refunds according to role and permission profile.

**Rules**

- Common billing does not mean a single combined plan, shared renewal date, or shared trial.
- New amounts, dates, or plans appear only after a successful result.
- If one platform's billing information is incomplete, identify the missing portion and do not present totals as complete.

### 9.5 Requests & Feedback

Keep **Feedback** in its own tab, separate from Demos and Trial Requests. **Contact Us is a separate navigation item**, not a feedback category. See section 9.10 for the demo booking experience.

| Request type    | Information shown                                                     | Actions                                   |
| --------------- | --------------------------------------------------------------------- | ----------------------------------------- |
| Feedback        | Message, attachments, organization, submitter, status, assignee       | Assign, resolve                           |
| Demo request    | Contact details, organization, requested time, stage, assignee, notes | Assign, schedule, add notes, update stage |
| Trial extension | Organization, platform, current end date, proposed end date, reason   | Approve or reject                         |

**Rules**

- Approval extends only the named product's trial for the named organization.
- Rejection records the decision without changing the trial.
- Each action keeps the platform and organization that were displayed when it began.

### 9.6 Activity & Security

- **Customer login history:** user, organization, time, result, and context.
- **Administrative activity:** staff member, platform, customer, action, result, time, and reason.
- Platform-specific actions appear under their platform. Billing history appears on billing profiles; staff-access history appears in Staff & Access. Shared events shown in a platform view are labelled **“Shared”**.

### 9.7 Staff & Access (shared)

- Directory of internal staff: name, email, role, assigned permission profile, invitation status, access status, last sign-in.
- Super Admin actions: invite, cancel, re-send, revoke.
- Shared staff-access history.

See section 9.11 for Sub Admin profiles and configurable permissions. The role tables above are starting defaults; the assigned permission profile determines each Sub Admin's allowed actions.

### 9.8 Pricing & Plans (shared)

**Purpose:** staff set up and maintain pricing without changing application code or hard-coded price lists.

The catalog covers CRM and VMS, with each plan clearly labelled by platform. It is a shared screen, unchanged by the topbar switcher. Its own CRM/VMS filter is independent of that switcher, just like Billing's line-item filter.

| Screen           | What the designer should show                                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plan catalog     | Platform, plan name, currency, billing interval, price, status, current revision, and number of subscribed organizations                                                              |
| Plan editor      | Name, description, platform, currency, amount, monthly/annual billing options, billing basis (organization or seat), included features, usage limits, trial rules, and effective date |
| Preview          | Customer-facing plan card, included features and limits, and example billing summary; make the currency and billing interval explicit                                                 |
| Publish review   | Changes from the current revision, effective date, and whether the change affects new subscriptions or named existing subscriptions                                                   |
| Revision history | Previous prices and features, author, date, reason, and publication status                                                                                                            |

**Lifecycle:** Draft → Published → Archived. Drafts can be edited; changing a published plan creates a new revision. Archived plans cannot be chosen for new subscriptions but remain visible on existing customer billing records.

**Rules**

- Published plans drive the relevant public pricing, subscription selection, and billing experience. A failed publication leaves the last published revision in use.
- CRM and VMS can have different prices, features, limits, and trial rules. A common catalog does not automatically create a combined bundle.
- Existing subscriptions retain their agreed plan revision by default. Changing their price or benefits requires a separate reviewed action identifying the affected customers and effective date; never silently change existing agreements.
- Prevent deletion of plans referenced by subscriptions or invoices. Archiving does not cancel subscriptions.
- Validate required fields, amounts, intervals, limits, and effective dates before publication. Show a clear free-plan label when the amount is zero.
- Super Admin owns publication by default. An explicitly granted Sub Admin permission may allow drafting, publishing, or archiving separately. Record every publication and subscription migration in activity history.
- Billing links each subscription to its agreed plan revision and shows any scheduled plan change.

### 9.9 Contact Us (separate from Feedback)

**Purpose:** handle sales questions, general inquiries, and customer contact messages independently from product feedback.

- **List:** sender name/email, company or linked organization if known, subject, platform, source, received time, assignee, and status.
- **Detail:** original message, contact details, conversation history, internal notes, assignment, and status.
- **Actions:** assign, add an internal note, draft/send a Gmail reply with permission, and resolve/reopen.
- Recommended statuses: **New → In progress → Resolved**. A reply updates conversation history; it does not automatically resolve the inquiry.
- Offer **Create demo request** when relevant, retaining a link to the original inquiry. It does not book a meeting or send an email by itself.
- CRM/VMS-tagged inquiries follow the topbar switcher. Inquiries without a platform remain in a clearly labelled **Unassigned platform** queue within Contact Us, available under either selection; staff can classify them. Do not discard messages from people who are not yet customers.
- Feedback retains its own message/category, submitter, organization if known, status, assignee, and resolution history. Contact and feedback counts remain distinct.

### 9.10 Demo requests and one-click booking

Within **Requests & Feedback → Demos**, show requester name/email, company, platform, requested slot and time zone, assignee, status, notes, and linked contact inquiry if any.

**Primary action: Book demo.** It performs the booking using the saved sender, calendar, duration, meeting location, and confirmation template. The button's nearby summary must show the time, attendee, organizer, and that a customer confirmation will be sent.

- One click is available when a customer-confirmed slot, required details, assigned organizer, current availability, permissions, Gmail connection, and Calendar connection are ready.
- Otherwise show **Choose time / Complete details** or **Reconnect integration**, as appropriate. Review the final slot before booking. Never treat an unconfirmed preferred time as an accepted appointment.
- On booking, check availability again, create the Calendar meeting, include a meeting link where configured, send one booking confirmation through Gmail, and record the meeting against the request.
- Coordinate Calendar invitations and Gmail confirmation so the customer does not receive duplicate confirmations. Templates clearly state the platform, date, time zone, duration, organizer, meeting link/location, and rescheduling contact.
- Recommended statuses: **New, Awaiting details, Ready to book, Booking, Booked, Confirmation pending, Completed, Cancelled**.
- If the Calendar booking fails, do not send a booking-success message. If the meeting exists but email fails, show **Booked — confirmation pending** and offer **Retry confirmation** without creating another meeting.
- If the result is unknown, check the existing booking before retrying. Prevent repeated clicks or concurrent staff actions from producing duplicate events/emails.
- A conflicting slot shows **Choose another time**. Reschedule and cancel are explicit actions with customer notification and activity history; closing a request alone does not cancel its meeting.

### 9.11 Sub Admin profiles and permissions (shared)

There are still only **Super Admin** and **Sub Admin** roles. A **permission profile** is a reusable set of allowed actions assigned to a Sub Admin; it is not another role. Keep it visually distinct from the staff member's personal profile.

- **Staff profile:** name, email, role, assigned permission profile, access status, last sign-in, and activity history. Staff can update permitted personal details; they cannot grant themselves permissions.
- **Permission profile editor:** name, description, and grouped action controls for Organizations, Billing, Pricing & Plans, Contact Us, Feedback, Demos, Activity, Product Operations, Support Access, and integration use.
- Use relevant controls such as view, edit, assign/resolve, approve trial extensions, export, draft/publish/archive plans, send replies, book/reschedule/cancel demos, and support access. Avoid a single unrestricted “Manage everything” checkbox.
- Super Admin creates/edits profiles, assigns one profile when inviting a Sub Admin, and can reassign it later. New profiles start with viewing enabled for administrative summaries and write/export actions disabled until granted.
- Suggested editable starter profiles: **Developer**, **Support**, and **Billing**. They remain Sub Admin accounts, and the owner reviews the actual action grants before assignment.
- Both products and the same navigation remain visible to all staff. Profiles control actions across CRM and VMS; they do not hide either switcher option.
- Show the affected staff count and action changes before saving an edited profile. Changes take effect for active sessions, including permission checks on pending actions, and are recorded in shared history.
- Internal invitations, permission-profile management, access revocation, and managing shared Google connections remain reserved for Super Admin. No profile can grant Super Admin ownership or change/remove the designated owner.
- Restricted actions explain the missing permission and direct staff to the Super Admin.

### 9.12 Integrations (shared)

**Purpose:** connect an authorized Crusource work account to **Gmail** and **Google Calendar** for contact replies and demo booking.

- Show Gmail and Calendar separately: connected account, connection status, selected sender/calendar, last successful use, and Connect/Reconnect/Disconnect actions.
- Super Admin authorizes connections and sets booking defaults: organizer/calendar, sender, duration, meeting location/link setting, and editable confirmation template. Show a preview before saving a template.
- Staff use integrations only through their assigned permissions. Connection credentials are never displayed in profiles or screens.
- Google account authorization connects these services; it is **not portal sign-in**. Portal authentication remains email/password without MFA. Google's own authorization experience is external to Crusource.
- Use only the mail/calendar access needed for the chosen features. The portal need not expose the entire Gmail inbox or unrelated calendar event contents.
- Show **Disconnected, Connected, Reconnect required, Temporarily unavailable** and partial states where only one service works. Keep contact and demo requests available even when booking is blocked.
- Disconnecting blocks new integration actions and clearly explains the impact. Existing sent messages and scheduled meetings are not silently deleted or cancelled.

---

## 10. Key interactions

| Interaction                       | Requirements                                                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trial extension**               | Show organization, platform, current end date, proposed end date, reason, and decision. Approval updates only the named trial.                                      |
| **Suspension/reactivation**       | Show the exact organization and platform affected, the impact, and a required reason before confirmation.                                                           |
| **Customer membership change**    | Show the target person, organization, platform, current and proposed role or access. Never grants internal portal access.                                           |
| **Staff invitation**              | Super Admin enters staff details, assigns a permission profile, and invites a Sub Admin. The invitee activates one internal account for both platforms.             |
| **Support access**                | Requires a permission check, reason, visible support-session banner, time limit, exit action, and recorded activity. Never presented as an ordinary customer login. |
| **Exports**                       | Export the current permitted scope and filters; label the platform and export time. Shared billing exports are explicitly labelled shared.                          |
| **Feature settings/provisioning** | Show the target organization/platform and current state, then confirm the proposed change. Enabling another platform requires an explicit provisioning result.      |

---

## 11. States the designer must cover

| State                                | Expected experience                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Loading                              | Selected platform stays visible; use placeholders rather than misleading values                                |
| No customers/results                 | Explain “No organizations use VMS yet” or “No results match these filters”; offer clear filters where relevant |
| Platform unavailable                 | Show unavailable status and retry; other platform and independent shared screens remain usable                 |
| Stale data                           | Label the last successful update and that the data is stale; disable actions needing current data              |
| Permission restriction               | Both products remain visible; unavailable actions explain which permission is required                         |
| Action in progress                   | Show progress; prevent duplicate submission                                                                    |
| Successful change                    | Confirm the organization, platform, and completed action                                                       |
| Failed change                        | Explain the failure and keep entered information; do not show success                                          |
| Result unknown                       | Explain that the outcome is unknown; check current state before retrying                                       |
| Data changed by another staff member | Refresh the current record and ask the user to review before resubmitting                                      |
| Session expired                      | Return to sign-in without completing an unauthorized action                                                    |
| Access revoked                       | End the session and explain that access was removed                                                            |
| Unsupported profile after switch     | Return to the equivalent list with an explanation                                                              |

A CRM problem must not block VMS, and a VMS problem must not block CRM.

---

## 12. Content, privacy, and data presentation rules

- Show **administrative summaries**. Do not expose full customer deals, candidate records, documents, or other business content on overview screens.
- Show only permitted administrative summaries; exporting requires a separate grant in the assigned permission profile.
- Use consistent, unambiguous dates. Identify the time context wherever it affects an expiry, trial, renewal, or audit event.
- Clearly label shared information as shared, and platform information with its platform.
- Never combine CRM and VMS counts in a way that implies unique customers or people.
- Product health reports service availability, not a guarantee that every workflow functions.

---

## 13. First-release scope

The first release includes the existing administrative screens plus dynamic Pricing & Plans, separate Contact Us handling, Sub Admin personal and permission profiles, email/password sign-in and recovery, and Gmail/Google Calendar connections with demo booking. These are requirements for the unified portal, not claims of existing implementation.

## 14. Reviewable defaults and open questions

Recommended defaults for this draft: CRM on first sign-in; remembered product afterward; one reusable permission profile per Sub Admin; Super Admin manages staff access and shared connections; published plan changes apply to new subscriptions unless an explicit existing-customer change is reviewed.

The product owner will confirm exact prices, currencies, billing basis, feature limits, permission-template grants, sender/calendar account, booking duration, and email wording before implementation. No specific commercial values or Google account are assumed here. Portal login is email/password only; MFA is excluded by the product decision.

## 15. Designer handoff

Keep the CRM/VMS topbar switcher prominent and the menu consistent across both selections. The designer chooses visual layout, colours, and styling. Use the [companion flows](SUPERADMIN_DFD.md) for the journeys and failure states.

Required additions: plan catalog/editor/preview/history; Contact Us list/detail/reply; Sub Admin personal profile and permission-profile editor/assignment; email/password sign-in and recovery; integration connections/defaults; ready-to-book demo and confirmation-pending state.

## 16. Acceptance checklist

- [ ] Topbar contains only CRM and VMS; equivalent platform screens change data without changing the menu template.
- [ ] Billing, Pricing & Plans, Staff & Access, and Integrations are labelled shared and unaffected by the topbar selection.
- [ ] Contact Us is separate from Feedback; messages from prospective customers remain available without requiring an organization record.
- [ ] Plans can be drafted, previewed, published, revised, and archived without editing application code. Existing subscribed prices do not change silently.
- [ ] Sub Admin profiles control actions without adding roles or hiding either product; current permissions are checked when an action runs.
- [ ] Portal sign-in uses email/password only and includes recovery; there are no MFA screens.
- [ ] Google authorization is shown as an integration connection, separate from portal authentication.
- [ ] A ready demo request can be booked in one click, with visible attendee/time/sender details and customer-notification intent.
- [ ] Missing details, conflicts, disconnected services, unknown results, and failed confirmations have clear recovery paths without duplicate meetings or emails.
- [ ] Administrative changes and customer communications show their true outcomes and appear in activity history.
