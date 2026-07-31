# Phase 1 — Foundation, Access Control & Core Sales Records

## Overview

Phase 1 establishes the foundation of the CRM by implementing authentication, access control, navigation, and the core sales modules. This phase enables users to securely access the system and manage the primary sales entities: Leads, Contacts, Accounts, and Deals.

---

## Epic 1: Authentication & Access Control

### Features

- Single-organization login (email + password)
- Admin can add users and assign roles (Admin / Sales Manager / Sales Rep)
- Role-based visibility rules (Own / Team / Full)
- Sales Rep → Sales Manager reporting structure ("Reports To")

---

## Epic 2: Navigation Shell

### Features

- Left sidebar navigation shell
- Top bar
  - Search
  - Quick Create
  - Notifications
  - Calendar
  - Profile
  - *(Placeholders for future implementation)*

---

## Epic 3: Leads

### Features

- Create and edit a Lead
  - Name
  - Company
  - Email
  - Phone
  - Source
- Import Leads in bulk via CSV
- Leads list view with filtering and sorting
- Leads Kanban view grouped by status
- Lead status lifecycle
  - New
  - Qualified
  - Converted
  - Junk
- One-click Lead Conversion
  - Creates or links an Account
  - Creates or links a Contact
  - Creates a Deal

---

## Epic 4: Contacts

### Features

- Create and edit a Contact linked to an Account
- Import Contacts in bulk
- Contacts list view with filtering and sorting
- AI-generated conversation summary on Contact history

---

## Epic 5: Accounts

### Features

- Create and edit an Account
- Import Accounts in bulk
- Accounts list view with filtering and sorting
- Account detail page with tabs
  - Contacts
  - Deals
  - Activities
- AI-powered duplicate detection during Account creation

---

## Epic 6: Deals

### Features

- Create and edit a Deal
- Import Deals in bulk
- Deals list view with filtering and sorting
- Deals Kanban view grouped by stage with per-column totals
- Six-stage sales pipeline
  1. Qualification
  2. Discovery
  3. Proposal
  4. Negotiation
  5. Closed Won
  6. Closed Lost
- Admin-configurable
  - Stage names
  - Stage order
  - Win probabilities
- Surface next follow-up and last interaction date on each Deal

---

## Epic 7: Cross-Module Utilities

### Features

- Filtering across
  - Leads
  - Contacts
  - Accounts
  - Deals
- Sorting across
  - Leads
  - Contacts
  - Accounts
  - Deals
- Bulk actions across
  - Leads
  - Contacts
  - Accounts
  - Deals

---

## Phase Deliverables

At the completion of Phase 1, the CRM will provide:

- Secure authentication and role-based access control
- Organization and user management
- Core navigation shell
- Complete Lead management workflow
- Contact management
- Account management
- Deal pipeline management
- Cross-module filtering, sorting, and bulk operations

This phase serves as the foundation for all subsequent CRM functionality, including Activities, Documents, Reporting, Dashboards, and AI capabilities.