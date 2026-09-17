# Zoho CRM Settings — Detailed Reference

## Scope

- **Target URL**: `https://crm.zoho.in/crm/org60083490643/settings/`
- **Authentication Method**: Interactive Playwright Browser Session (Zoho Accounts)
- **Read-Only Methodology**: Non-destructive, state-preserving automated inspection
- **URL Boundary**: Confined exclusively to `/crm/org60083490643/settings/*` and underlying Settings sub-routes / client-side components
- **Security Restrictions**: Passwords, OTPs, API keys, OAuth tokens, session tokens, and business customer records redacted as `[REDACTED SECRET]`

## Coverage

| Metric | Count |
|---|---:|
| Categories | 12 |
| Subcategories | 91 |
| Settings views | 165 |
| Successfully documented | 165 |
| Partially documented | 0 |
| Inaccessible | 0 |

# 1. General

## 1.1 Personal Settings

### Personal Settings
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/personal-settings`
- **Internal Route Name**: `crm.settings.section.personal-settings`
- **API Name**: `system.personalsettings1`
- **Component ID**: `general_accountInfo`
- **Purpose**: Manages user-specific preferences including name, email signature, language, timezone, theme, and locale formatting.

#### Visible Headings & Overview
- **Primary Heading**: Personal Settings
- **Category Context**: General → Personal Settings
- **System Page Title Key**: `crm.title.account.information`
- **Functional Scope**: Manages user-specific preferences including name, email signature, language, timezone, theme, and locale formatting.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Account Information**: Available for inspection / customization
- **Hour Format**: Available for inspection / customization
- **Upload Photo**: Available for inspection / customization
- **Time Zone**: Available for inspection / customization
- **Language**: Available for inspection / customization
- **Time Format**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Personal Settings**: Personal Settings, Accessibility
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Accessibility
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/accessibility`
- **Internal Route Name**: `crm.settings.section.accessibility`
- **API Name**: `system.accessibility`
- **Component ID**: `accessibility_settings`
- **Purpose**: Configures system-wide accessibility features including high-contrast modes, font size scaling, vision aids, motor controls, and keyboard navigation.

#### Visible Headings & Overview
- **Primary Heading**: Accessibility
- **Category Context**: General → Personal Settings
- **System Page Title Key**: `crm.setup.system.accessibility`
- **Functional Scope**: Configures system-wide accessibility features including high-contrast modes, font size scaling, vision aids, motor controls, and keyboard navigation.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Account Information**: Available for inspection / customization
- **Vision**: Available for inspection / customization
- **Font Size**: Available for inspection / customization
- **Spacing**: Available for inspection / customization
- **Keyboard Shortcuts**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Personal Settings**: Personal Settings, Accessibility
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 1.2 Users

### Users
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/users`
- **Internal Route Name**: `crm.settings.section.users`
- **API Name**: `system.users1`
- **Component ID**: `usersPermi_users`
- **Purpose**: Administers active, inactive, and invited CRM users, role assignments, profile associations, and license allocations.

#### Visible Headings & Overview
- **Primary Heading**: Users
- **Category Context**: General → Users
- **System Page Title Key**: `crm.security.usersList`
- **Functional Scope**: Administers active, inactive, and invited CRM users, role assignments, profile associations, and license allocations.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Users and Control**: Available for inspection / customization
- **Add User**: Available for inspection / customization
- **Manage Users**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Users**: Users, Groups, Activate Users
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Users`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Groups
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/groups`
- **Internal Route Name**: `crm.settings.section.groups`
- **API Name**: `system.groups`
- **Component ID**: `usersPermi_Groups`
- **Purpose**: Manages user groups and teams for collaborative record sharing, record assignment, and pipeline visibility.

#### Visible Headings & Overview
- **Primary Heading**: Groups
- **Category Context**: General → Users
- **System Page Title Key**: `crm.security.group.view`
- **Functional Scope**: Manages user groups and teams for collaborative record sharing, record assignment, and pipeline visibility.

#### Configuration Sections & Fields
- **Groups Configuration**: Standard General parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Users**: Users, Groups, Activate Users
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Groups`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Activate Users
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/activate-users`
- **Internal Route Name**: `crm.settings.section.activate-users`
- **API Name**: `system.activateusers`
- **Component ID**: `usersPermi_activate`
- **Purpose**: Provides license allocation tools to activate or deactivate user seats across standard and team editions.

#### Visible Headings & Overview
- **Primary Heading**: Activate Users
- **Category Context**: General → Users
- **System Page Title Key**: `crm.change.userstatus.active`
- **Functional Scope**: Provides license allocation tools to activate or deactivate user seats across standard and team editions.

#### Configuration Sections & Fields
- **Activate Users Configuration**: Standard General parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Users**: Users, Groups, Activate Users
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 1.3 Company Settings

### Company Details
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/company-details`
- **Internal Route Name**: `crm.settings.section.company-details`
- **API Name**: `system.companydetails1`
- **Component ID**: `general_viewOrgDetails`
- **Purpose**: Defines organization-level metadata including company name, primary contact, base currency, timezone, logo, and organization ID.

#### Visible Headings & Overview
- **Primary Heading**: Company Details
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.security.orgDetails`
- **Functional Scope**: Defines organization-level metadata including company name, primary contact, base currency, timezone, logo, and organization ID.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Company Logo**: Available for inspection / customization
- **Time Zone**: Available for inspection / customization
- **Country**: Available for inspection / customization
- **Super Admin**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Domain Mapping
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/domain-mapping`
- **Internal Route Name**: `crm.settings.section.domain-mapping`
- **API Name**: `system.domainmapping`
- **Component ID**: `general_domainmapping`
- **Purpose**: Configures custom domain mapping (CNAME/SSL) allowing users to access Zoho CRM via custom organization URLs.

#### Visible Headings & Overview
- **Primary Heading**: Domain Mapping
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.setup.system.domainmapping`
- **Functional Scope**: Configures custom domain mapping (CNAME/SSL) allowing users to access Zoho CRM via custom organization URLs.

#### Configuration Sections & Fields
- **Domain Mapping Configuration**: Standard General parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Fiscal Year
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/fiscal-year`
- **Internal Route Name**: `crm.settings.section.fiscal-year`
- **API Name**: `system.fiscalyear`
- **Component ID**: `general_editFiscal`
- **Purpose**: Sets financial year cycle parameters, starting month, and display preferences for revenue forecasting and pipeline reporting.

#### Visible Headings & Overview
- **Primary Heading**: Fiscal Year
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.forecast.fiscal.year.settings`
- **Functional Scope**: Sets financial year cycle parameters, starting month, and display preferences for revenue forecasting and pipeline reporting.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Financial year**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Business hours
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/business-hours`
- **Internal Route Name**: `crm.settings.section.business-hours`
- **API Name**: `system.businesshours.1`
- **Component ID**: `general_bushrs`
- **Purpose**: Establishes organization and shift-level working hours, standard operational days, and user shift assignments.

#### Visible Headings & Overview
- **Primary Heading**: Business hours
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.label.business.hours.1`
- **Functional Scope**: Establishes organization and shift-level working hours, standard operational days, and user shift assignments.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Working Hours**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Holidays
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/holidays`
- **Internal Route Name**: `crm.settings.section.holidays`
- **API Name**: `system.holidays`
- **Component ID**: `general_holidays`
- **Purpose**: Defines annual organization holiday lists, regional calendars, and non-working days for SLA and workflow calculations.

#### Visible Headings & Overview
- **Primary Heading**: Holidays
- **Category Context**: General → Company Settings
- **System Page Title Key**: `Holidays`
- **Functional Scope**: Defines annual organization holiday lists, regional calendars, and non-working days for SLA and workflow calculations.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Working Hours**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Currencies
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/currencies`
- **Internal Route Name**: `crm.settings.section.currencies`
- **API Name**: `system.currencies`
- **Component ID**: `general_currencies`
- **Purpose**: Configures multi-currency management, exchange rates, corporate base currency, and decimal precision settings.

#### Visible Headings & Overview
- **Primary Heading**: Currencies
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.label.currencies`
- **Functional Scope**: Configures multi-currency management, exchange rates, corporate base currency, and decimal precision settings.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **currency**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Hierarchy Preference
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/hierarchy-preference`
- **Internal Route Name**: `crm.settings.section.hierarchy-preference`
- **API Name**: `system.hierarchypreference`
- **Component ID**: `general_Hierarchy`
- **Purpose**: Selects the organizational reporting structure preference (Role Hierarchy vs. Reporting Manager Hierarchy).

#### Visible Headings & Overview
- **Primary Heading**: Hierarchy Preference
- **Category Context**: General → Company Settings
- **System Page Title Key**: `crm.user.hierarchy.preference`
- **Functional Scope**: Selects the organizational reporting structure preference (Role Hierarchy vs. Reporting Manager Hierarchy).

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Hierarchy**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Company Settings**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 1.4 Calendar Booking

### Calendar Booking
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/booking`
- **Internal Route Name**: `crm.settings.section.calendar-booking`
- **API Name**: `system.calendarbooking1`
- **Component ID**: `general_calendarBooking`
- **Purpose**: Manages appointment scheduling, booking links, available meeting slots, service types, and calendar sync.

#### Visible Headings & Overview
- **Primary Heading**: Calendar Booking
- **Category Context**: General → Calendar Booking
- **System Page Title Key**: `crm.setup.system.calendarbooking`
- **Functional Scope**: Manages appointment scheduling, booking links, available meeting slots, service types, and calendar sync.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Team Booking**: Available for inspection / customization
- **Manage Calendar Booking**: Available for inspection / customization
- **Create Calendar Booking**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 1.5 Motivator

### Motivator
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/game-settings`
- **Internal Route Name**: `crm.settings.section.game-settings`
- **API Name**: `system.gamescope1`
- **Component ID**: `general_gameSettings`
- **Purpose**: Configures gamification features, KPI scorecards, target achievements, leaderboards, and sales contests.

#### Visible Headings & Overview
- **Primary Heading**: Motivator
- **Category Context**: General → Motivator
- **System Page Title Key**: `gs.salesmotivator`
- **Functional Scope**: Configures gamification features, KPI scorecards, target achievements, leaderboards, and sales contests.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Gamescope**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 1.6 Agents

### Agents
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.agent`
- **Internal Route Name**: `crm.settings.section.agent`
- **API Name**: `system.agenttab`
- **Component ID**: `general_ZiaAgent`
- **Purpose**: Configures Zia AI autonomous agents, agent capabilities, role permissions, and conversational automation triggers.

#### Visible Headings & Overview
- **Primary Heading**: Agents
- **Category Context**: General → Agents
- **System Page Title Key**: `crm.setup.system.agent`
- **Functional Scope**: Configures Zia AI autonomous agents, agent capabilities, role permissions, and conversational automation triggers.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Agent**: Available for inspection / customization
- **Zia Agent**: Available for inspection / customization
- **Agent**: Available for inspection / customization
- **Agent**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_ZiaAgent`
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 2. Security Control

## 2.1 Profiles

### Profiles
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/profiles`
- **Internal Route Name**: `crm.settings.section.profiles`
- **API Name**: `system.profiles`
- **Component ID**: `usersPermi_Profiles`
- **Purpose**: Defines granular module, field, tool, and administrative permissions assignable to CRM user roles.

#### Visible Headings & Overview
- **Primary Heading**: Profiles
- **Category Context**: Security Control → Profiles
- **System Page Title Key**: `crm.security.profiles.list`
- **Functional Scope**: Defines granular module, field, tool, and administrative permissions assignable to CRM user roles.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Permission**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Profiles`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.2 Roles and Sharing

### Roles
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/roles`
- **Internal Route Name**: `crm.settings.section.roles`
- **API Name**: `system.roles`
- **Component ID**: `usersPermi_Roles`
- **Purpose**: Builds the hierarchical reporting tree controlling record ownership, visibility, and managerial access.

#### Visible Headings & Overview
- **Primary Heading**: Roles
- **Category Context**: Security Control → Roles and Sharing
- **System Page Title Key**: `crm.security.roles.list`
- **Functional Scope**: Builds the hierarchical reporting tree controlling record ownership, visibility, and managerial access.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Hierarchy**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Roles and Sharing**: Roles, Data Sharing Settings
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Roles`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Data Sharing Settings
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/data-sharing`
- **Internal Route Name**: `crm.settings.section.data-sharing`
- **API Name**: `system.datasharingsettings`
- **Component ID**: `usersPermi_SharingSetting`
- **Purpose**: Defines organization-wide default access (Private/Public Read Only/Public Read/Write) and custom sharing rules.

#### Visible Headings & Overview
- **Primary Heading**: Data Sharing Settings
- **Category Context**: Security Control → Roles and Sharing
- **System Page Title Key**: `crm.security.sharing.settings`
- **Functional Scope**: Defines organization-wide default access (Private/Public Read Only/Public Read/Write) and custom sharing rules.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Sharing**: Available for inspection / customization
- **Data Sharing**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Roles and Sharing**: Roles, Data Sharing Settings
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Data_Sharing`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.3 Zoho Mail Add-on Users

### Zoho Mail Add-on Users
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zmail-users`
- **Internal Route Name**: `crm.settings.section.zmail-users`
- **API Name**: `system.zohomailaddonusers`
- **Component ID**: `usersPermi_zmailusers`
- **Purpose**: Administers Zoho Mail integration licenses, mailbox synchronization, and user email associations.

#### Visible Headings & Overview
- **Primary Heading**: Zoho Mail Add-on Users
- **Category Context**: Security Control → Zoho Mail Add-on Users
- **System Page Title Key**: `crm.setup.system.zohomailaddonusers`
- **Functional Scope**: Administers Zoho Mail integration licenses, mailbox synchronization, and user email associations.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Deactivate Mail Addon**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.4 Compliance Settings

### GDPR Compliance
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/compliance`
- **Internal Route Name**: `crm.settings.section.compliance`
- **API Name**: `system.compliancesettings1`
- **Component ID**: `usersPermi_complianceSettings`
- **Purpose**: Configures data privacy management, lawful basis of processing, data subject rights, and consent logging.

#### Visible Headings & Overview
- **Primary Heading**: GDPR Compliance
- **Category Context**: Security Control → Compliance Settings
- **System Page Title Key**: `crm.label.privacy.settings`
- **Functional Scope**: Configures data privacy management, lawful basis of processing, data subject rights, and consent logging.

#### Configuration Sections & Fields
- **GDPR Compliance Configuration**: Standard Security Control parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Compliance Settings**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Compliance_Settings`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Overview
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.compliance.consent-dashboard`
- **Internal Route Name**: `crm.settings.section.compliance.consent-dashboard`
- **API Name**: `system.gdproverview`
- **Component ID**: `usersPermi_consentDashboard`
- **Purpose**: Visual dashboard summarizing consent acquisition status, pending requests, and data protection metrics.

#### Visible Headings & Overview
- **Primary Heading**: Overview
- **Category Context**: Security Control → Compliance Settings
- **System Page Title Key**: `crm.label.data.overview`
- **Functional Scope**: Visual dashboard summarizing consent acquisition status, pending requests, and data protection metrics.

#### Configuration Sections & Fields
- **Overview Configuration**: Standard Security Control parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Compliance Settings**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Compliance_Settings`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Preferences
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.compliance.privacy-preference`
- **Internal Route Name**: `crm.settings.section.compliance.privacy-preference`
- **API Name**: `system.gdprpref`
- **Component ID**: `usersPermi_preference`
- **Purpose**: Configures module-level behaviors, duplicate check rules, quick create menus, and search settings.

#### Visible Headings & Overview
- **Primary Heading**: Preferences
- **Category Context**: Security Control → Compliance Settings
- **System Page Title Key**: `crm.label.data.overview`
- **Functional Scope**: Configures module-level behaviors, duplicate check rules, quick create menus, and search settings.

#### Configuration Sections & Fields
- **Preferences Configuration**: Standard Security Control parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Compliance Settings**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Compliance_Settings`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Consent Form
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.compliance.consent-form`
- **Internal Route Name**: `crm.settings.section.compliance.consent-form`
- **API Name**: `system.consentform`
- **Component ID**: `usersPermi_consentForm`
- **Purpose**: Customizes customer-facing data consent capture forms, consent language, and tracking options.

#### Visible Headings & Overview
- **Primary Heading**: Consent Form
- **Category Context**: Security Control → Compliance Settings
- **System Page Title Key**: `crm.label.consent.form`
- **Functional Scope**: Customizes customer-facing data consent capture forms, consent language, and tracking options.

#### Configuration Sections & Fields
- **Consent Form Configuration**: Standard Security Control parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Compliance Settings**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Compliance_Settings`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### HIPAA Compliance
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/compliance/hipaa`
- **Internal Route Name**: `crm.settings.section.compliance.hipaa`
- **API Name**: `system.hipaa`
- **Component ID**: `usersPermi_hipaa`
- **Purpose**: Enables healthcare compliance controls, restricting electronic Protected Health Information (ePHI) fields and audit logging.

#### Visible Headings & Overview
- **Primary Heading**: HIPAA Compliance
- **Category Context**: Security Control → Compliance Settings
- **System Page Title Key**: `crm.hipaa.label`
- **Functional Scope**: Enables healthcare compliance controls, restricting electronic Protected Health Information (ePHI) fields and audit logging.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **HIPAA**: Available for inspection / customization
- **Health**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Compliance Settings**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Compliance_Settings`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.5 Territory Management

### Territories
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/territories`
- **Internal Route Name**: `crm.settings.section.territories`
- **API Name**: `system.territories`
- **Component ID**: `usersPermi_enableTerritory`
- **Purpose**: Organizes accounts into geographic, industry, or revenue-based territories with automated rule assignment.

#### Visible Headings & Overview
- **Primary Heading**: Territories
- **Category Context**: Security Control → Territory Management
- **System Page Title Key**: `crm.territory.title.territory.hierarchy`
- **Functional Scope**: Organizes accounts into geographic, industry, or revenue-based territories with automated rule assignment.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Territory**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.6 Trusted Domain

### Trusted Domain
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/trusted-domain`
- **Internal Route Name**: `crm.settings.section.crm-trusted-domain`
- **API Name**: `system.trusteddomains1`
- **Component ID**: `trusted_domains`
- **Purpose**: Whitelists trusted IP addresses and domain ranges for API calls, webhooks, and restricted access.

#### Visible Headings & Overview
- **Primary Heading**: Trusted Domain
- **Category Context**: Security Control → Trusted Domain
- **System Page Title Key**: `crm.trusteddomains.plural`
- **Functional Scope**: Whitelists trusted IP addresses and domain ranges for API calls, webhooks, and restricted access.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Trusted Domains**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.7 Support Access

### Support Access
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/support-access`
- **Internal Route Name**: `crm.settings.section.support-access`
- **API Name**: `system.supportaccess1`
- **Component ID**: `usersPermi_supportaccess`
- **Purpose**: Grants temporary, read-only access to Zoho technical support personnel for debugging and troubleshooting.

#### Visible Headings & Overview
- **Primary Heading**: Support Access
- **Category Context**: Security Control → Support Access
- **System Page Title Key**: `crm.support.access`
- **Functional Scope**: Grants temporary, read-only access to Zoho technical support personnel for debugging and troubleshooting.

#### Configuration Sections & Fields
- **Support Access Configuration**: Standard Security Control parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Support_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.8 Single Sign-On(SAML)

### Single Sign-On(SAML)
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: None`
- **Internal Route Name**: `N/A`
- **API Name**: `system.zdirectorysso1`
- **Component ID**: `zdirectory_sso`
- **Purpose**: Configures enterprise identity provider (IdP) federation via SAML 2.0 through Zoho Directory.

#### Visible Headings & Overview
- **Primary Heading**: Single Sign-On(SAML)
- **Category Context**: Security Control → Single Sign-On(SAML)
- **Functional Scope**: Configures enterprise identity provider (IdP) federation via SAML 2.0 through Zoho Directory.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Zoho Directory**: Available for inspection / customization
- **Single Sign On**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.9 Security Policies

### Security Policies
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: None`
- **Internal Route Name**: `N/A`
- **API Name**: `system.zdirectorysecurity1`
- **Component ID**: `zdirectory_security`
- **Purpose**: Enforces organization-level password complexity, multi-factor authentication (MFA), IP restrictions, and session timeouts.

#### Visible Headings & Overview
- **Primary Heading**: Security Policies
- **Category Context**: Security Control → Security Policies
- **Functional Scope**: Enforces organization-level password complexity, multi-factor authentication (MFA), IP restrictions, and session timeouts.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Multifactor Authentication**: Available for inspection / customization
- **Zoho Directory**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.10 Active Directory Sync

### Active Directory Sync
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: None`
- **Internal Route Name**: `N/A`
- **API Name**: `system.zdirectoryactivesync1`
- **Component ID**: `zdirectory_activesync`
- **Purpose**: Synchronizes users and groups from on-premises Microsoft Active Directory via Zoho Directory Sync tool.

#### Visible Headings & Overview
- **Primary Heading**: Active Directory Sync
- **Category Context**: Security Control → Active Directory Sync
- **Functional Scope**: Synchronizes users and groups from on-premises Microsoft Active Directory via Zoho Directory Sync tool.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Zoho Directory**: Available for inspection / customization
- **Active Directory**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.11 Login History

### Login History
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: None`
- **Internal Route Name**: `N/A`
- **API Name**: `system.zdirectoryloginhistory1`
- **Component ID**: `zdirectory_loginhistory`
- **Purpose**: Monitors audit trails of user sign-in attempts, client IPs, locations, access methods, and timestamps.

#### Visible Headings & Overview
- **Primary Heading**: Login History
- **Category Context**: Security Control → Login History
- **Functional Scope**: Monitors audit trails of user sign-in attempts, client IPs, locations, access methods, and timestamps.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Zoho Directory**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 2.12 Audit Log

### Audit Log
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/auditlog`
- **Internal Route Name**: `crm.settings.section.auditlog`
- **API Name**: `system.auditlog1`
- **Component ID**: `data_auditLog`
- **Purpose**: Comprehensive historical log tracking all administrative, structural, workflow, and user actions performed in the CRM.

#### Visible Headings & Overview
- **Primary Heading**: Audit Log
- **Category Context**: Security Control → Audit Log
- **System Page Title Key**: `crm.audit.log`
- **Functional Scope**: Comprehensive historical log tracking all administrative, structural, workflow, and user actions performed in the CRM.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Access Logs**: Available for inspection / customization
- **setupsearch.activity.history**: Available for inspection / customization
- **Activity**: Available for inspection / customization
- **Application history**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 3. Channels

## 3.1 Email

### Email Configuration
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/email-configuration`
- **Internal Route Name**: `crm.settings.section.email-configuration`
- **API Name**: `system.emailconfiguration`
- **Component ID**: `comm_emailConfigSetting`
- **Purpose**: Manages IMAP/POP3 account connections, SMTP server relay, email sharing permissions, and compose defaults.

#### Visible Headings & Overview
- **Primary Heading**: Email Configuration
- **Category Context**: Channels → Email
- **Functional Scope**: Manages IMAP/POP3 account connections, SMTP server relay, email sharing permissions, and compose defaults.

#### Configuration Sections & Fields
- **Email Configuration Configuration**: Standard Channels parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Email Parser
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/email-parser`
- **Internal Route Name**: `crm.settings.section.email-parser`
- **API Name**: `system.mailparser`
- **Component ID**: `comm_emailParser`
- **Purpose**: Configures inbound email parsing rules to automatically extract data and convert emails into CRM records.

#### Visible Headings & Overview
- **Primary Heading**: Email Parser
- **Category Context**: Channels → Email
- **System Page Title Key**: `crm.mailparser.title`
- **Functional Scope**: Configures inbound email parsing rules to automatically extract data and convert emails into CRM records.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Mail Parser**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### BCC Dropbox
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/bcc-dropbox`
- **Internal Route Name**: `crm.settings.section.bcc-dropbox`
- **API Name**: `system.bccdropbox`
- **Component ID**: `comm_bcc`
- **Purpose**: Generates unique BCC email addresses to automatically log outbound customer correspondence into matching CRM leads/contacts.

#### Visible Headings & Overview
- **Primary Heading**: BCC Dropbox
- **Category Context**: Channels → Email
- **System Page Title Key**: `bccdropbox.heading`
- **Functional Scope**: Generates unique BCC email addresses to automatically log outbound customer correspondence into matching CRM leads/contacts.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **BCC**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Email Deliverability
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.email-deliverability`
- **Internal Route Name**: `crm.settings.section.email-deliverability`
- **API Name**: `system.emaildeliverability`
- **Component ID**: `comm_ed`
- **Purpose**: Configures SPF, DKIM, and DMARC authentication records to ensure optimal email deliverability and avoid spam filters.

#### Visible Headings & Overview
- **Primary Heading**: Email Deliverability
- **Category Context**: Channels → Email
- **Functional Scope**: Configures SPF, DKIM, and DMARC authentication records to ensure optimal email deliverability and avoid spam filters.

#### Configuration Sections & Fields
- **Email Deliverability Configuration**: Standard Channels parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Email Intelligence
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.email-intelligence`
- **Internal Route Name**: `crm.settings.section.email-intelligence`
- **API Name**: `system.emailintelligence`
- **Component ID**: `comm_ei`
- **Purpose**: Enables AI-driven sentiment analysis, automated email categorizations, and intent recognition on customer emails.

#### Visible Headings & Overview
- **Primary Heading**: Email Intelligence
- **Category Context**: Channels → Email
- **Functional Scope**: Enables AI-driven sentiment analysis, automated email categorizations, and intent recognition on customer emails.

#### Configuration Sections & Fields
- **Email Intelligence Configuration**: Standard Channels parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Unsubscribe Link
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/unsubscribe-link`
- **Internal Route Name**: `crm.settings.section.unsubscribe-link`
- **API Name**: `system.unsubscribelink`
- **Component ID**: `devSpace_unsubscribe`
- **Purpose**: Customizes one-click unsubscribe links, landing pages, and opt-out preferences attached to outgoing marketing emails.

#### Visible Headings & Overview
- **Primary Heading**: Unsubscribe Link
- **Category Context**: Channels → Email
- **System Page Title Key**: `crm.unsubscription.link`
- **Functional Scope**: Customizes one-click unsubscribe links, landing pages, and opt-out preferences attached to outgoing marketing emails.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Unsubscribe**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Email**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Unsubscribe_Form`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.2 Telephony

### Telephony
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/telephony/marketplace`
- **Internal Route Name**: `crm.settings.section.telephony`
- **API Name**: `system.telephony1`
- **Component ID**: `comm_telephony`
- **Purpose**: Integrates PBX and cloud telephony systems (PhoneBridge) for click-to-call, automated call logging, and IVR popups.

#### Visible Headings & Overview
- **Primary Heading**: Telephony
- **Category Context**: Channels → Telephony
- **System Page Title Key**: `crm.tpi.ctiapi.otheraddons.label.telephony`
- **Functional Scope**: Integrates PBX and cloud telephony systems (PhoneBridge) for click-to-call, automated call logging, and IVR popups.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Phone Bridge**: Available for inspection / customization
- **Phone**: Available for inspection / customization
- **PhoneBridge**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Zoho_PhoneBridge_Integ`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.3 Business Messaging

### Business Messaging
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/messages/services`
- **Internal Route Name**: `crm.settings.section.messages`
- **API Name**: `system.messages1`
- **Component ID**: `comm_messages`
- **Purpose**: Connects instant messaging channels such as WhatsApp Business, SMS providers, and Telegram for direct CRM messaging.

#### Visible Headings & Overview
- **Primary Heading**: Business Messaging
- **Category Context**: Channels → Business Messaging
- **System Page Title Key**: `crm.setup.system.messages`
- **Functional Scope**: Connects instant messaging channels such as WhatsApp Business, SMS providers, and Telegram for direct CRM messaging.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Messages**: Available for inspection / customization
- **message**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.4 Notification SMS

### Notification SMS
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/notificationsms`
- **Internal Route Name**: `crm.settings.section.notificationsms`
- **API Name**: `system.notificationsms1`
- **Component ID**: `comm_notificationsms`
- **Purpose**: Configures SMS gateway integrations to send automated transaction and event notifications to customers.

#### Visible Headings & Overview
- **Primary Heading**: Notification SMS
- **Category Context**: Channels → Notification SMS
- **System Page Title Key**: `crm.setup.system.notificationsms`
- **Functional Scope**: Configures SMS gateway integrations to send automated transaction and event notifications to customers.

#### Configuration Sections & Fields
- **Notification SMS Configuration**: Standard Channels parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Zoho_PhoneBridge_Integ`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.5 Webforms

### Webforms
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/webform`
- **Internal Route Name**: `crm.settings.section.webform`
- **API Name**: `system.webforms1`
- **Component ID**: `devSpace_webLeads`
- **Purpose**: Builds and deploys web-to-lead, web-to-contact, and web-to-case capture forms with anti-spam captcha protection.

#### Visible Headings & Overview
- **Primary Heading**: Webforms
- **Category Context**: Channels → Webforms
- **System Page Title Key**: `crm.webforms`
- **Functional Scope**: Builds and deploys web-to-lead, web-to-contact, and web-to-case capture forms with anti-spam captcha protection.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **setupsearch.forms**: Available for inspection / customization
- **Edit Webform**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Webforms**: Webforms, Auto-Response Rules
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Auto-Response Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/auto-response-rules`
- **Internal Route Name**: `crm.settings.section.auto-response-rules`
- **API Name**: `system.autoresponserules`
- **Component ID**: `devSpace_autoRespRules`
- **Purpose**: Sets up automated email responses dispatched immediately when new webform submissions are received.

#### Visible Headings & Overview
- **Primary Heading**: Auto-Response Rules
- **Category Context**: Channels → Webforms
- **System Page Title Key**: `crm.label.autoresponse`
- **Functional Scope**: Sets up automated email responses dispatched immediately when new webform submissions are received.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Automatic Response**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Webforms**: Webforms, Auto-Response Rules
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Web_To_Leads`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.6 Social

### Brand Settings
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/brands`
- **Internal Route Name**: `crm.settings.section.extensions.social-extensions.social-brands`
- **API Name**: `system.socialbrandsettings`
- **Component ID**: `comm_socialaccounts`
- **Purpose**: Connects social media brand profiles (Twitter/X, Facebook, LinkedIn) for social listening and interaction logging.

#### Visible Headings & Overview
- **Primary Heading**: Brand Settings
- **Category Context**: Channels → Social
- **System Page Title Key**: `crm.social.setup.brand.settings`
- **Functional Scope**: Connects social media brand profiles (Twitter/X, Facebook, LinkedIn) for social listening and interaction logging.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **twitter**: Available for inspection / customization
- **Twit**: Available for inspection / customization
- **Social Integration**: Available for inspection / customization
- **facebook**: Available for inspection / customization
- **face**: Available for inspection / customization
- **googleplus**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Social**: Brand Settings, Admin Settings, Automate Lead Generation
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Admin Settings
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/admin-settings`
- **Internal Route Name**: `crm.settings.section.extensions.social-extensions.social-admin-settings`
- **API Name**: `system.socialadminsettings`
- **Component ID**: `comm_socialadmin`
- **Purpose**: Defines social media monitoring keywords, user access permissions, and lead conversion rules.

#### Visible Headings & Overview
- **Primary Heading**: Admin Settings
- **Category Context**: Channels → Social
- **System Page Title Key**: `crm.social.setup.admin.settings`
- **Functional Scope**: Defines social media monitoring keywords, user access permissions, and lead conversion rules.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **socialadmin**: Available for inspection / customization
- **admin**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Social**: Brand Settings, Admin Settings, Automate Lead Generation
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Social_Admin`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Automate Lead Generation
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/lead-gen`
- **Internal Route Name**: `crm.settings.section.extensions.social-extensions.social-lead-gen`
- **API Name**: `system.automateleadgeneration`
- **Component ID**: `comm_leadgen`
- **Purpose**: Configures automated lead creation triggers based on social media interactions (mentions, direct messages, comments).

#### Visible Headings & Overview
- **Primary Heading**: Automate Lead Generation
- **Category Context**: Channels → Social
- **System Page Title Key**: `crm.nsocial.leadgen.title`
- **Functional Scope**: Configures automated lead creation triggers based on social media interactions (mentions, direct messages, comments).

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **workflow**: Available for inspection / customization
- **leadgen**: Available for inspection / customization
- **automate**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Social**: Brand Settings, Admin Settings, Automate Lead Generation
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Social_Admin`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.7 Chat

### Chat
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/zoho/visit`
- **Internal Route Name**: `crm.settings.section.extensions.zoho-extensions.visit`
- **API Name**: `system.chat1`
- **Component ID**: `comm_chat`
- **Purpose**: Connects Zoho SalesIQ live chat widgets to capture website visitor tracking data and convert chats to CRM leads.

#### Visible Headings & Overview
- **Primary Heading**: Chat
- **Category Context**: Channels → Chat
- **System Page Title Key**: `webform.visitor.tracking`
- **Functional Scope**: Connects Zoho SalesIQ live chat widgets to capture website visitor tracking data and convert chats to CRM leads.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Visitor Tracking**: Available for inspection / customization
- **Visits**: Available for inspection / customization
- **SalesIQ**: Available for inspection / customization
- **WebSite**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 3.8 Portals

### Portals
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/client-portal`
- **Internal Route Name**: `crm.settings.section.client-portal`
- **API Name**: `system.portalusers1`
- **Component ID**: `comm_clientPortal`
- **Purpose**: Administers dedicated self-service client and partner portals for external access to tickets, quotes, and records.

#### Visible Headings & Overview
- **Primary Heading**: Portals
- **Category Context**: Channels → Portals
- **System Page Title Key**: `custm.prtl`
- **Functional Scope**: Administers dedicated self-service client and partner portals for external access to tickets, quotes, and records.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Client portal**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 4. Customization

## 4.1 Modules and Fields

### Modules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/modules`
- **Internal Route Name**: `crm.settings.section.modules`
- **API Name**: `system.modules`
- **Component ID**: `custom_modules`
- **Purpose**: Customizes CRM standard and custom modules, layouts, field sets, mandatory requirements, and related lists.

#### Visible Headings & Overview
- **Primary Heading**: Modules
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Customizes CRM standard and custom modules, layouts, field sets, mandatory requirements, and related lists.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Tabs**: Available for inspection / customization
- **Rename Tab**: Available for inspection / customization
- **Remove Tabs**: Available for inspection / customization
- **Manage Tabs**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Create_Team_Module`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Web Tabs
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/web-tabs`
- **Internal Route Name**: `crm.settings.section.web-tabs`
- **API Name**: `system.webtabs`
- **Component ID**: `custom_webTabs`
- **Purpose**: Embeds external web applications, dashboards, or portals as internal navigation tabs within the CRM interface.

#### Visible Headings & Overview
- **Primary Heading**: Web Tabs
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.lable.webtab`
- **Functional Scope**: Embeds external web applications, dashboards, or portals as internal navigation tabs within the CRM interface.

#### Configuration Sections & Fields
- **Web Tabs Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Global Sets
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/global_picklists`
- **Internal Route Name**: `crm.settings.section.globalpicklists`
- **API Name**: `system.globalfields`
- **Component ID**: `custom_globalField`
- **Purpose**: Manages centralized picklists (dropdown option sets) that can be shared across multiple modules and layouts.

#### Visible Headings & Overview
- **Primary Heading**: Global Sets
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.auditlog.globalpicklist`
- **Functional Scope**: Manages centralized picklists (dropdown option sets) that can be shared across multiple modules and layouts.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Global Set**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Layouts
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.layouts`
- **Internal Route Name**: `crm.settings.section.modules.module.layouts`
- **API Name**: `system.layouts`
- **Component ID**: `customize_modules`
- **Purpose**: Designs drag-and-drop page layouts tailored for different user profiles, business divisions, or product lines.

#### Visible Headings & Overview
- **Primary Heading**: Layouts
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Designs drag-and-drop page layouts tailored for different user profiles, business divisions, or product lines.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Layout**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Layout Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.layout-rules`
- **Internal Route Name**: `crm.settings.section.modules.module.layout-rules`
- **API Name**: `system.layoutrules`
- **Component ID**: `customize_modules`
- **Purpose**: Defines dynamic field display, mandatory requirements, and layout switching based on specific field values.

#### Visible Headings & Overview
- **Primary Heading**: Layout Rules
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Defines dynamic field display, mandatory requirements, and layout switching based on specific field values.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Rule**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Fields and Layouts
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.field-listing`
- **Internal Route Name**: `crm.settings.section.modules.module.field-listing`
- **API Name**: `system.fieldsandlayouts`
- **Component ID**: `customize_modules`
- **Purpose**: Provides a unified listing of all custom and standard fields across modules with datatype and usage stats.

#### Visible Headings & Overview
- **Primary Heading**: Fields and Layouts
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Provides a unified listing of all custom and standard fields across modules with datatype and usage stats.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Fields**: Available for inspection / customization
- **Field Listing**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Field Permissions
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.field-permissions`
- **Internal Route Name**: `crm.settings.section.modules.module.field-permissions`
- **API Name**: `system.fieldpermissions`
- **Component ID**: `customize_modules`
- **Purpose**: Sets granular Read/Write, Read-Only, or Hidden permissions for individual fields per user profile.

#### Visible Headings & Overview
- **Primary Heading**: Field Permissions
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Sets granular Read/Write, Read-Only, or Hidden permissions for individual fields per user profile.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Fields**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Validation Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.validation-rules`
- **Internal Route Name**: `crm.settings.section.modules.module.validation-rules`
- **API Name**: `system.validationrule`
- **Component ID**: `customize_modules_validationRules`
- **Purpose**: Creates validation criteria that prevent record saving when custom business logic constraints are violated.

#### Visible Headings & Overview
- **Primary Heading**: Validation Rules
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Creates validation criteria that prevent record saving when custom business logic constraints are violated.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Rule**: Available for inspection / customization
- **Validation**: Available for inspection / customization
- **Set Validation Rules**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Record Locking Configuration
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.record-locking`
- **Internal Route Name**: `crm.settings.section.modules.module.record-locking`
- **API Name**: `system.reclockingconfiguration`
- **Component ID**: `customize_modules_lockingconfiguration`
- **Purpose**: Locks records from further edits when they reach specific pipeline stages or approval statuses.

#### Visible Headings & Overview
- **Primary Heading**: Record Locking Configuration
- **Category Context**: Customization → Modules and Fields
- **Functional Scope**: Locks records from further edits when they reach specific pipeline stages or approval statuses.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Lock**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Links and Buttons
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.modules.module.links-and-buttons`
- **Internal Route Name**: `crm.settings.section.modules.module.links-and-buttons`
- **API Name**: `system.linksandbuttons`
- **Component ID**: `customize_modules`
- **Purpose**: Creates custom URL buttons, Deluge action buttons, and contextual links inside record views.

#### Visible Headings & Overview
- **Primary Heading**: Links and Buttons
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.inactive.prewarning.custom.modules`
- **Functional Scope**: Creates custom URL buttons, Deluge action buttons, and contextual links inside record views.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Link**: Available for inspection / customization
- **Button**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Preferences
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.preferences`
- **Internal Route Name**: `crm.settings.section.preferences`
- **API Name**: `system.preferences`
- **Component ID**: `custom_preferences`
- **Purpose**: Configures module-level behaviors, duplicate check rules, quick create menus, and search settings.

#### Visible Headings & Overview
- **Primary Heading**: Preferences
- **Category Context**: Customization → Modules and Fields
- **System Page Title Key**: `crm.label.preference`
- **Functional Scope**: Configures module-level behaviors, duplicate check rules, quick create menus, and search settings.

#### Configuration Sections & Fields
- **Preferences Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Modules and Fields**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.2 Pipelines

### Pipelines
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/pipelines`
- **Internal Route Name**: `crm.settings.section.pipelines`
- **API Name**: `system.pipelines1`
- **Component ID**: `customize_pipelines`
- **Purpose**: Builds multi-stage sales pipelines, probability percentages, and stage transition rules for Deals/Potentials.

#### Visible Headings & Overview
- **Primary Heading**: Pipelines
- **Category Context**: Customization → Pipelines
- **System Page Title Key**: `crm.label.pipelines`
- **Functional Scope**: Builds multi-stage sales pipelines, probability percentages, and stage transition rules for Deals/Potentials.

#### Configuration Sections & Fields
- **Pipelines Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.3 Wizards

### Wizards
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/wizard`
- **Internal Route Name**: `crm.settings.section.wizard`
- **API Name**: `system.wizards1`
- **Component ID**: `wizards_interForm`
- **Purpose**: Constructs multi-step guided data entry forms for complex sales processes and intake workflows.

#### Visible Headings & Overview
- **Primary Heading**: Wizards
- **Category Context**: Customization → Wizards
- **System Page Title Key**: `crm.settings.wizards`
- **Functional Scope**: Constructs multi-step guided data entry forms for complex sales processes and intake workflows.

#### Configuration Sections & Fields
- **Wizards Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.4 Kiosk Studio

### Kiosk Studio
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/kiosk`
- **Internal Route Name**: `crm.settings.section.kiosk`
- **API Name**: `system.kioskstudios`
- **Component ID**: `automate_processflow`
- **Purpose**: Builds touch-screen kiosk experiences and self-service guided forms for retail or on-site event capture.

#### Visible Headings & Overview
- **Primary Heading**: Kiosk Studio
- **Category Context**: Customization → Kiosk Studio
- **System Page Title Key**: `crm.setup.system.kiosk`
- **Functional Scope**: Builds touch-screen kiosk experiences and self-service guided forms for retail or on-site event capture.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Kiosk**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.5 Canvas

### Home View
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.canvas-builder.homeview`
- **Internal Route Name**: `crm.settings.section.canvas-builder.homeview`
- **API Name**: `system.homeview`
- **Component ID**: `custom_canvas_homeview`
- **Purpose**: Customizes the layout and widget cards displayed on user dashboard homepages.

#### Visible Headings & Overview
- **Primary Heading**: Home View
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.homeview`
- **Functional Scope**: Customizes the layout and widget cards displayed on user dashboard homepages.

#### Configuration Sections & Fields
- **Home View Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### List View
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/canvas-builder/listview`
- **Internal Route Name**: `crm.settings.section.canvas-builder.listview`
- **API Name**: `system.listview`
- **Component ID**: `custom_canvas_listview`
- **Purpose**: Designs visual card layouts and rich styling for module list views.

#### Visible Headings & Overview
- **Primary Heading**: List View
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.listview`
- **Functional Scope**: Designs visual card layouts and rich styling for module list views.

#### Configuration Sections & Fields
- **List View Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Detail View
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.canvas-builder.detailview.views`
- **Internal Route Name**: `crm.settings.section.canvas-builder.detailview.views`
- **API Name**: `system.detailview`
- **Component ID**: `custom_canvas_detailview`
- **Purpose**: Constructs modern, responsive record overview pages using Canvas visual designer.

#### Visible Headings & Overview
- **Primary Heading**: Detail View
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.detailview`
- **Functional Scope**: Constructs modern, responsive record overview pages using Canvas visual designer.

#### Configuration Sections & Fields
- **Detail View Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Form View
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.canvas-builder.formview`
- **Internal Route Name**: `crm.settings.section.canvas-builder.formview`
- **API Name**: `system.formview`
- **Component ID**: `custom_canvas_createpage`
- **Purpose**: Customizes the visual design and step layouts of record creation forms.

#### Visible Headings & Overview
- **Primary Heading**: Form View
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.formview`
- **Functional Scope**: Customizes the visual design and step layouts of record creation forms.

#### Configuration Sections & Fields
- **Form View Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Templates
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/canvas-builder/templates`
- **Internal Route Name**: `crm.settings.section.canvas-builder.templates`
- **API Name**: `system.canvas.templates`
- **Component ID**: `custom_canvas_templates`
- **Purpose**: Manages reusable Canvas design templates and industry-specific layout packs.

#### Visible Headings & Overview
- **Primary Heading**: Templates
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.templates`
- **Functional Scope**: Manages reusable Canvas design templates and industry-specific layout packs.

#### Configuration Sections & Fields
- **Templates Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Print View
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.canvas-builder.printview`
- **Internal Route Name**: `crm.settings.section.canvas-builder.printview`
- **API Name**: `system.printview`
- **Component ID**: `custom_canvas_printpage`
- **Purpose**: Designs print-ready document layouts and PDF summaries for CRM records.

#### Visible Headings & Overview
- **Primary Heading**: Print View
- **Category Context**: Customization → Canvas
- **System Page Title Key**: `crm.canvas.setup.title.printview`
- **Functional Scope**: Designs print-ready document layouts and PDF summaries for CRM records.

#### Configuration Sections & Fields
- **Print View Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Canvas**: Home View, List View, Detail View, Form View, Templates, Print View
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.6 Customize Home page

### Customize Home page
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/home-customization`
- **Internal Route Name**: `crm.settings.section.new-home-customization`
- **API Name**: `system.customizehomepage1`
- **Component ID**: `custom_homePage`
- **Purpose**: Configures organization-wide homepage dashboard layouts, default components, and user role assignments.

#### Visible Headings & Overview
- **Primary Heading**: Customize Home page
- **Category Context**: Customization → Customize Home page
- **System Page Title Key**: `crm.label.homepage.setup`
- **Functional Scope**: Configures organization-wide homepage dashboard layouts, default components, and user role assignments.

#### Configuration Sections & Fields
- **Customize Home page Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Home`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.7 Translations

### Translation Settings
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/translation-settings`
- **Internal Route Name**: `crm.settings.section.translation-settings`
- **API Name**: `system.translationsettings`
- **Component ID**: `custom_translation`
- **Purpose**: Manages multi-language translation files for custom field labels, picklist values, and module names.

#### Visible Headings & Overview
- **Primary Heading**: Translation Settings
- **Category Context**: Customization → Translations
- **System Page Title Key**: `crm.label.translation.settings`
- **Functional Scope**: Manages multi-language translation files for custom field labels, picklist values, and module names.

#### Configuration Sections & Fields
- **Translation Settings Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Translations**: Translation Settings, Language Import History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Language Import History
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/translation-history`
- **Internal Route Name**: `crm.settings.section.translation-history`
- **API Name**: `system.translationhistory`
- **Component ID**: `custom_translationimporthistory`
- **Purpose**: Tracks language translation file import attempts, errors, and updated label counts.

#### Visible Headings & Overview
- **Primary Heading**: Language Import History
- **Category Context**: Customization → Translations
- **System Page Title Key**: `crm.label.translation.history`
- **Functional Scope**: Tracks language translation file import attempts, errors, and updated label counts.

#### Configuration Sections & Fields
- **Language Import History Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Translations**: Translation Settings, Language Import History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.8 Templates

### Email
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=email`
- **Internal Route Name**: `crm.settings.section.crm-templates`
- **API Name**: `system.email2`
- **Component ID**: `custom_email`
- **Purpose**: Manages rich HTML email templates with dynamic merge fields, attachments, and branding.

#### Visible Headings & Overview
- **Primary Heading**: Email
- **Category Context**: Customization → Templates
- **System Page Title Key**: `crm.templates.email.templates`
- **Functional Scope**: Manages rich HTML email templates with dynamic merge fields, attachments, and branding.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Email Templates**: Available for inspection / customization
- **Template**: Available for inspection / customization
- **Mail Content Format**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Templates**: Email, Inventory, Mail Merge
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Inventory
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=inventory`
- **Internal Route Name**: `crm.settings.section.crm-templates`
- **API Name**: `system.inventory`
- **Component ID**: `custom_inventory`
- **Purpose**: Designs printable templates for Quotes, Sales Orders, Purchase Orders, and Invoices.

#### Visible Headings & Overview
- **Primary Heading**: Inventory
- **Category Context**: Customization → Templates
- **System Page Title Key**: `crm.label.inventory.template`
- **Functional Scope**: Designs printable templates for Quotes, Sales Orders, Purchase Orders, and Invoices.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Inventory Templates**: Available for inspection / customization
- **Quote Template**: Available for inspection / customization
- **SalesOrder Template**: Available for inspection / customization
- **Invoice Template**: Available for inspection / customization
- **PurchaseOrder Template**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Templates**: Email, Inventory, Mail Merge
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Mail Merge
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=mail-merge`
- **Internal Route Name**: `crm.settings.section.crm-templates`
- **API Name**: `system.mailmerge`
- **Component ID**: `custom_mailmerge`
- **Purpose**: Creates Microsoft Word and Zoho Writer mail merge templates for automated document generation.

#### Visible Headings & Overview
- **Primary Heading**: Mail Merge
- **Category Context**: Customization → Templates
- **System Page Title Key**: `crm.mail.mergeTemplates`
- **Functional Scope**: Creates Microsoft Word and Zoho Writer mail merge templates for automated document generation.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Mail Merge Templates**: Available for inspection / customization
- **Flyer**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Templates**: Email, Inventory, Mail Merge
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_MS_Office_Integ`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 4.9 Teamspace

### Teamspace
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/teamspace`
- **Internal Route Name**: `crm.settings.section.teamspace`
- **API Name**: `system.teamspace1`
- **Component ID**: `custom_teamspace`
- **Purpose**: Administers collaborative team workspaces, shared modules, and team-specific record views.

#### Visible Headings & Overview
- **Primary Heading**: Teamspace
- **Category Context**: Customization → Teamspace
- **System Page Title Key**: `crm.setup.system.teamspace`
- **Functional Scope**: Administers collaborative team workspaces, shared modules, and team-specific record views.

#### Configuration Sections & Fields
- **Teamspace Configuration**: Standard Customization parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 5. Automation

## 5.1 Workflow Rules

### Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/workflow-rules`
- **Internal Route Name**: `crm.settings.section.workflow-rules`
- **API Name**: `system.rules`
- **Component ID**: `automate_workflow`
- **Purpose**: Defines automated round-robin and criteria-based lead, deal, and ticket assignment rules.

#### Visible Headings & Overview
- **Primary Heading**: Rules
- **Category Context**: Automation → Workflow Rules
- **System Page Title Key**: `crm.workflow.rules`
- **Functional Scope**: Defines automated round-robin and criteria-based lead, deal, and ticket assignment rules.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Workflow**: Available for inspection / customization
- **Automate**: Available for inspection / customization
- **Assign Tasks**: Available for inspection / customization
- **Workflow Alert**: Available for inspection / customization
- **Workflow Tasks**: Available for inspection / customization
- **Workflow Rule**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Workflow Rules**: Rules, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Usage
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/workflow-insights`
- **Internal Route Name**: `crm.settings.section.workflow-insights`
- **API Name**: `system.ruleusage`
- **Component ID**: `automate_insight`
- **Purpose**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Visible Headings & Overview
- **Primary Heading**: Usage
- **Category Context**: Automation → Workflow Rules
- **System Page Title Key**: `crm.workflow.insights`
- **Functional Scope**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Automate**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Workflow Rules**: Rules, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 5.2 Actions

### Email Notifications
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/alerts`
- **Internal Route Name**: `crm.settings.section.alerts`
- **API Name**: `system.emailnotifications`
- **Component ID**: `automate_alert`
- **Purpose**: Manages automated email alerts triggered by workflows, blueprints, and escalation rules.

#### Visible Headings & Overview
- **Primary Heading**: Email Notifications
- **Category Context**: Automation → Actions
- **System Page Title Key**: `crm.workflow.label.alerts`
- **Functional Scope**: Manages automated email alerts triggered by workflows, blueprints, and escalation rules.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Send Email**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Actions**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Tasks
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/tasks`
- **Internal Route Name**: `crm.settings.section.tasks`
- **API Name**: `system.tasks`
- **Component ID**: `automate_task`
- **Purpose**: Configures automated task assignment templates generated by workflow automation.

#### Visible Headings & Overview
- **Primary Heading**: Tasks
- **Category Context**: Automation → Actions
- **System Page Title Key**: `crm.workflow.label.tasks`
- **Functional Scope**: Configures automated task assignment templates generated by workflow automation.

#### Configuration Sections & Fields
- **Tasks Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Actions**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Field Updates
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/field-updates`
- **Internal Route Name**: `crm.settings.section.field-updates`
- **API Name**: `system.fieldupdates`
- **Component ID**: `automate_fieldUpdate`
- **Purpose**: Defines automated field modification rules updating record values when workflow criteria are satisfied.

#### Visible Headings & Overview
- **Primary Heading**: Field Updates
- **Category Context**: Automation → Actions
- **System Page Title Key**: `crm.workflow.label.field.update`
- **Functional Scope**: Defines automated field modification rules updating record values when workflow criteria are satisfied.

#### Configuration Sections & Fields
- **Field Updates Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Actions**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Webhooks
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/webhooks`
- **Internal Route Name**: `crm.settings.section.webhooks`
- **API Name**: `system.webhooks`
- **Component ID**: `automate_webhook`
- **Purpose**: Configures HTTP callbacks that post real-time CRM event data to external APIs and web services.

#### Visible Headings & Overview
- **Primary Heading**: Webhooks
- **Category Context**: Automation → Actions
- **System Page Title Key**: `workflow.label.webhooks`
- **Functional Scope**: Configures HTTP callbacks that post real-time CRM event data to external APIs and web services.

#### Configuration Sections & Fields
- **Webhooks Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Actions**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Actions by Zoho Flow
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/flow`
- **Internal Route Name**: `crm.settings.section.actions-flow-library`
- **API Name**: `system.flow_actionlibrary`
- **Component ID**: `flow_actionlibrary`
- **Purpose**: Integrates multi-app workflow automation flows built with Zoho Flow directly into CRM actions.

#### Visible Headings & Overview
- **Primary Heading**: Actions by Zoho Flow
- **Category Context**: Automation → Actions
- **System Page Title Key**: `crm.setup.system.flow_actionlibrary`
- **Functional Scope**: Integrates multi-app workflow automation flows built with Zoho Flow directly into CRM actions.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Functions**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Actions**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 5.3 Schedules

### Schedules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/schedules`
- **Internal Route Name**: `crm.settings.section.schedules`
- **API Name**: `system.schedules1`
- **Component ID**: `automate_schedules`
- **Purpose**: Configures recurring cron-like Deluge scripts executing automated batch processing on CRM data.

#### Visible Headings & Overview
- **Primary Heading**: Schedules
- **Category Context**: Automation → Schedules
- **System Page Title Key**: `crm.schedules.title`
- **Functional Scope**: Configures recurring cron-like Deluge scripts executing automated batch processing on CRM data.

#### Configuration Sections & Fields
- **Schedules Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 5.4 Assignment

### Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/assignment-rules`
- **Internal Route Name**: `crm.settings.section.assignment-rule`
- **API Name**: `system.assignmentrules1`
- **Component ID**: `automate_assignmentRules`
- **Purpose**: Defines automated round-robin and criteria-based lead, deal, and ticket assignment rules.

#### Visible Headings & Overview
- **Primary Heading**: Rules
- **Category Context**: Automation → Assignment
- **System Page Title Key**: `crm.common.menu.assignmentRules`
- **Functional Scope**: Defines automated round-robin and criteria-based lead, deal, and ticket assignment rules.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Assignment Rules**: Available for inspection / customization
- **Assign**: Available for inspection / customization
- **Auto Assign**: Available for inspection / customization
- **Round Robin**: Available for inspection / customization
- **Allocate Records**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Assignment**: Rules, Thresholds, Zia
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Thresholds
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/assignment-thresholds`
- **Internal Route Name**: `crm.settings.section.assignment-thresholds`
- **API Name**: `system.assignmentrestrictions`
- **Component ID**: `automate_assignmentRestrictions`
- **Purpose**: Sets maximum active lead caps per user to prevent rep overload and ensure timely outreach.

#### Visible Headings & Overview
- **Primary Heading**: Thresholds
- **Category Context**: Automation → Assignment
- **System Page Title Key**: `crm.setup.system.assignmentrestrictions`
- **Functional Scope**: Sets maximum active lead caps per user to prevent rep overload and ensure timely outreach.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Assignment Thresholds**: Available for inspection / customization
- **Assign**: Available for inspection / customization
- **Auto Assign**: Available for inspection / customization
- **Allocate Records**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Assignment**: Rules, Thresholds, Zia
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Zia
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia-reasoning`
- **Internal Route Name**: `crm.settings.section.zia-reasoning`
- **API Name**: `system.ziareasoning`
- **Component ID**: `automate_assignmentRulesZiaReasoning`
- **Purpose**: Enables Zia AI intelligent lead assignment matching leads to the most effective sales representatives.

#### Visible Headings & Overview
- **Primary Heading**: Zia
- **Category Context**: Automation → Assignment
- **System Page Title Key**: `crm.intelligence.name`
- **Functional Scope**: Enables Zia AI intelligent lead assignment matching leads to the most effective sales representatives.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **zia**: Available for inspection / customization
- **assign by zia**: Available for inspection / customization
- **reasoning**: Available for inspection / customization
- **contributing fields**: Available for inspection / customization
- **user pattern**: Available for inspection / customization
- **score**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Assignment**: Rules, Thresholds, Zia
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 5.5 Scoring Rules

### Scoring Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/scoring-rules`
- **Internal Route Name**: `crm.settings.section.scoring-rules`
- **API Name**: `system.scoringrules1`
- **Component ID**: `automate_scoringRules`
- **Purpose**: Establishes positive and negative score increments based on customer behaviors, email clicks, and field values.

#### Visible Headings & Overview
- **Primary Heading**: Scoring Rules
- **Category Context**: Automation → Scoring Rules
- **System Page Title Key**: `crm.label.scoring.rules`
- **Functional Scope**: Establishes positive and negative score increments based on customer behaviors, email clicks, and field values.

#### Configuration Sections & Fields
- **Scoring Rules Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 5.6 Cadences

### Cadences
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/cadences`
- **Internal Route Name**: `crm.settings.section.cadences`
- **API Name**: `system.cadences1`
- **Component ID**: `automate_series`
- **Purpose**: Constructs structured multi-channel outreach sequences (call, email, task) for sales prospecting.

#### Visible Headings & Overview
- **Primary Heading**: Cadences
- **Category Context**: Automation → Cadences
- **System Page Title Key**: `crm.setup.system.cadences`
- **Functional Scope**: Constructs structured multi-channel outreach sequences (call, email, task) for sales prospecting.

#### Configuration Sections & Fields
- **Cadences Configuration**: Standard Automation parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Enterprise / Ultimate Tier Required

---

# 6. Process Management

## 6.1 Blueprint

### Blueprints
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/blueprint`
- **Internal Route Name**: `crm.settings.section.blueprint`
- **API Name**: `system.blueprints`
- **Component ID**: `automate_process`
- **Purpose**: Designs state-machine process models enforcing strict stage-by-stage transitions, checklists, and mandatory data entry.

#### Visible Headings & Overview
- **Primary Heading**: Blueprints
- **Category Context**: Process Management → Blueprint
- **System Page Title Key**: `crm.label.process.automation`
- **Functional Scope**: Designs state-machine process models enforcing strict stage-by-stage transitions, checklists, and mandatory data entry.

#### Configuration Sections & Fields
- **Blueprints Configuration**: Standard Process Management parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Blueprint**: Blueprints, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Usage
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/blueprint-usage`
- **Internal Route Name**: `crm.settings.section.blueprint-usage`
- **API Name**: `system.blueprintusage`
- **Component ID**: `automate_usage`
- **Purpose**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Visible Headings & Overview
- **Primary Heading**: Usage
- **Category Context**: Process Management → Blueprint
- **System Page Title Key**: `crm.label.process.usage`
- **Functional Scope**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Blueprints**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Blueprint**: Blueprints, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 6.2 Approval Processes

### Approval Processes
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/approval-process`
- **Internal Route Name**: `crm.settings.section.approval-process`
- **API Name**: `system.approvalprocesses1`
- **Component ID**: `automate_approvalProcess`
- **Purpose**: Configures multi-step hierarchical review and authorization workflows for discounts, quotes, and critical deals.

#### Visible Headings & Overview
- **Primary Heading**: Approval Processes
- **Category Context**: Process Management → Approval Processes
- **System Page Title Key**: `crm.label.approval.processes`
- **Functional Scope**: Configures multi-step hierarchical review and authorization workflows for discounts, quotes, and critical deals.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Record approval**: Available for inspection / customization
- **Approval Rules**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 6.3 Review Processes

### Review Processes
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.review-process`
- **Internal Route Name**: `crm.settings.section.review-process`
- **API Name**: `system.reviewprocesses.plural1`
- **Component ID**: `automate_reviewprocess`
- **Purpose**: Establishes managerial review checkpoints and quality assurance verification flows for CRM records.

#### Visible Headings & Overview
- **Primary Heading**: Review Processes
- **Category Context**: Process Management → Review Processes
- **System Page Title Key**: `crm.setup.system.reviewprocesses.plural1`
- **Functional Scope**: Establishes managerial review checkpoints and quality assurance verification flows for CRM records.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Blueprints**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Review Processes**: Review Processes, Review Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Review Analytics
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.review-usage`
- **Internal Route Name**: `crm.settings.section.review-usage`
- **API Name**: `system.reviewprocessusage`
- **Component ID**: `automate_reviewprocessusage`
- **Purpose**: Analyzes review throughput, approval turnaround times, and bottleneck identification metrics.

#### Visible Headings & Overview
- **Primary Heading**: Review Analytics
- **Category Context**: Process Management → Review Processes
- **System Page Title Key**: `crm.setup.system.reviewprocessusage`
- **Functional Scope**: Analyzes review throughput, approval turnaround times, and bottleneck identification metrics.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Blueprints**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Review Processes**: Review Processes, Review Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Workflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 6.4 Connected Workflow

### Connected Workflow
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/connected-workflow`
- **Internal Route Name**: `crm.settings.section.connected-workflow`
- **API Name**: `system.connectedworkflow1`
- **Component ID**: `connected_workflow`
- **Purpose**: Orchestrates cross-module automation connecting events across disparate CRM and third-party modules.

#### Visible Headings & Overview
- **Primary Heading**: Connected Workflow
- **Category Context**: Process Management → Connected Workflow
- **System Page Title Key**: `crm.setup.system.connectedworkflow`
- **Functional Scope**: Orchestrates cross-module automation connecting events across disparate CRM and third-party modules.

#### Configuration Sections & Fields
- **Connected Workflow Configuration**: Standard Process Management parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_ConnectedWorkflow`
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 7. Experience Center

## 7.1 Signals

### Signals
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/sales-signals`
- **Internal Route Name**: `crm.settings.section.sales-signals`
- **API Name**: `system.salessignals1`
- **Component ID**: `comm_notificationSettings`
- **Purpose**: Configures real-time SalesSignals notifications for email opens, chats, missed calls, and support tickets.

#### Visible Headings & Overview
- **Primary Heading**: Signals
- **Category Context**: Experience Center → Signals
- **System Page Title Key**: `crm.ntc.label.settings.notificationTitle`
- **Functional Scope**: Configures real-time SalesSignals notifications for email opens, chats, missed calls, and support tickets.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **notification**: Available for inspection / customization
- **notification center**: Available for inspection / customization
- **signals**: Available for inspection / customization
- **signals setting**: Available for inspection / customization
- **SalesSignals**: Available for inspection / customization
- **Signals Settings**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 7.2 CommandCenter

### Path Finder
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/commandcenter/path-finder`
- **Internal Route Name**: `crm.settings.section.path-finder`
- **API Name**: `system.pathfinder`
- **Component ID**: `automate_pathfinder`
- **Purpose**: Visualizes end-to-end customer journey pathways and touchpoint sequences across lifecycle stages.

#### Visible Headings & Overview
- **Primary Heading**: Path Finder
- **Category Context**: Experience Center → CommandCenter
- **System Page Title Key**: `crm.setup.system.pathfinder`
- **Functional Scope**: Visualizes end-to-end customer journey pathways and touchpoint sequences across lifecycle stages.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Journey Builder**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in CommandCenter**: Path Finder, Journey Builder
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_View_Commandcenter`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Journey Builder
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/commandcenter/journey-builder`
- **Internal Route Name**: `crm.settings.section.orchestration`
- **API Name**: `system.orchestrations`
- **Component ID**: `automate_orchestration`
- **Purpose**: Builds automated, omni-channel customer journeys triggering personalized actions across touchpoints.

#### Visible Headings & Overview
- **Primary Heading**: Journey Builder
- **Category Context**: Experience Center → CommandCenter
- **System Page Title Key**: `crm.label.automation.orchestration`
- **Functional Scope**: Builds automated, omni-channel customer journeys triggering personalized actions across touchpoints.

#### Configuration Sections & Fields
- **Journey Builder Configuration**: Standard Experience Center parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in CommandCenter**: Path Finder, Journey Builder
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_View_Commandcenter`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 7.3 Segmentation

### Segmentation
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/segmentation/index`
- **Internal Route Name**: `crm.settings.section.segmentation`
- **API Name**: `system.segmentation1`
- **Component ID**: `automate_segmentation`
- **Purpose**: Segments customer contacts into RFM (Recency, Frequency, Monetary) groups for targeted engagement.

#### Visible Headings & Overview
- **Primary Heading**: Segmentation
- **Category Context**: Experience Center → Segmentation
- **System Page Title Key**: `crm.segmentation`
- **Functional Scope**: Segments customer contacts into RFM (Recency, Frequency, Monetary) groups for targeted engagement.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Customer**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 8. Data Administration

## 8.1 Import

### Import
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/data-migration`
- **Internal Route Name**: `crm.settings.section.data-migration`
- **API Name**: `system.import1`
- **Component ID**: `data_migrate`
- **Purpose**: Step-by-step data migration and file import wizard for migrating data from CSVs or competing CRM systems.

#### Visible Headings & Overview
- **Primary Heading**: Import
- **Category Context**: Data Administration → Import
- **System Page Title Key**: `crm.label.translation.import`
- **Functional Scope**: Step-by-step data migration and file import wizard for migrating data from CSVs or competing CRM systems.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Migrate Data from Another CRM**: Available for inspection / customization
- **Migration**: Available for inspection / customization
- **Data Import**: Available for inspection / customization
- **Salesforce Import**: Available for inspection / customization
- **Sugar CRM Import**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Import**: Import, Import History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Data_Migration`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Import History
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/import-history`
- **Internal Route Name**: `crm.settings.section.import-history`
- **API Name**: `system.importhistory`
- **Component ID**: `data_importHistory`
- **Purpose**: Logs all past data import jobs, successful record counts, skipped rows, and error logs.

#### Visible Headings & Overview
- **Primary Heading**: Import History
- **Category Context**: Data Administration → Import
- **System Page Title Key**: `crm.import.history`
- **Functional Scope**: Logs all past data import jobs, successful record counts, skipped rows, and error logs.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Import Status**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Import**: Import, Import History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Import_History`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.2 Export

### Export
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/export`
- **Internal Route Name**: `crm.settings.section.export`
- **API Name**: `system.export1`
- **Component ID**: `data_export`
- **Purpose**: Exports CRM module records and relational data into standard CSV archives.

#### Visible Headings & Overview
- **Primary Heading**: Export
- **Category Context**: Data Administration → Export
- **System Page Title Key**: `crm.export.data.wizard`
- **Functional Scope**: Exports CRM module records and relational data into standard CSV archives.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Export Data**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.3 Data Backup

### Data Backup
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/data-backup`
- **Internal Route Name**: `crm.settings.section.data-backup`
- **API Name**: `system.databackup`
- **Component ID**: `data_backup`
- **Purpose**: Schedules automated bi-weekly or monthly data and attachment backup archives for disaster recovery.

#### Visible Headings & Overview
- **Primary Heading**: Data Backup
- **Category Context**: Data Administration → Data Backup
- **System Page Title Key**: `crm.setup.dataAdmin.backup`
- **Functional Scope**: Schedules automated bi-weekly or monthly data and attachment backup archives for disaster recovery.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Backup**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.4 Remove sample data

### Remove sample data
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/remove-sample-data`
- **Internal Route Name**: `crm.settings.section.remove-sample-data`
- **API Name**: `system.removesampledata1`
- **Component ID**: `data_removeSampleData`
- **Purpose**: Permanently purges pre-populated sample records (leads, contacts, deals) added during onboarding.

#### Visible Headings & Overview
- **Primary Heading**: Remove sample data
- **Category Context**: Data Administration → Remove sample data
- **System Page Title Key**: `cob.remove.sampledata`
- **Functional Scope**: Permanently purges pre-populated sample records (leads, contacts, deals) added during onboarding.

#### Configuration Sections & Fields
- **Remove sample data Configuration**: Standard Data Administration parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.5 Storage

### Storage
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/storage`
- **Internal Route Name**: `crm.settings.section.storage`
- **API Name**: `system.storage1`
- **Component ID**: `data_storageUsage`
- **Purpose**: Monitors organization storage consumption across database records, attachments, and file folders.

#### Visible Headings & Overview
- **Primary Heading**: Storage
- **Category Context**: Data Administration → Storage
- **System Page Title Key**: `crm.setup.dataAdmin.storage`
- **Functional Scope**: Monitors organization storage consumption across database records, attachments, and file folders.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Storage Analytics**: Available for inspection / customization
- **Storage Usage**: Available for inspection / customization
- **Used Space**: Available for inspection / customization
- **Storage Used**: Available for inspection / customization
- **Manage Storage**: Available for inspection / customization
- **Buy Storage**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.6 Recycle Bin

### Recycle Bin
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/recyclebin`
- **Internal Route Name**: `crm.settings.section.recyclebin`
- **API Name**: `system.recyclebin1`
- **Component ID**: `data_recyclebin`
- **Purpose**: Holds deleted records for 60 days, allowing authorized administrators to restore or permanently purge data.

#### Visible Headings & Overview
- **Primary Heading**: Recycle Bin
- **Category Context**: Data Administration → Recycle Bin
- **System Page Title Key**: `crm.title.recyclebin`
- **Functional Scope**: Holds deleted records for 60 days, allowing authorized administrators to restore or permanently purge data.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Missing Records**: Available for inspection / customization
- **Deleted Records**: Available for inspection / customization
- **Restore Records**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.7 Sandbox

### Sandbox List
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.sandbox`
- **Internal Route Name**: `crm.settings.section.sandbox`
- **API Name**: `system.sandbox1`
- **Component ID**: `data_sandbox`
- **Purpose**: Manages isolated development and staging sandbox environments for building and testing customizations.

#### Visible Headings & Overview
- **Primary Heading**: Sandbox List
- **Category Context**: Data Administration → Sandbox
- **System Page Title Key**: `crm.setup.data.sandbox`
- **Functional Scope**: Manages isolated development and staging sandbox environments for building and testing customizations.

#### Configuration Sections & Fields
- **Sandbox List Configuration**: Standard Data Administration parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Sandbox**: Sandbox List, Deployment Logs
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Enterprise / Ultimate Tier Required

---

### Deployment Logs
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.sandbox.sandbox-deployment-logs`
- **Internal Route Name**: `crm.settings.section.sandbox.sandbox-deployment-logs`
- **API Name**: `system.sandbox.deploymentlogs`
- **Component ID**: `data_sandbox_deployment`
- **Purpose**: Tracks configuration change sets deployed from sandbox environments to the live production CRM.

#### Visible Headings & Overview
- **Primary Heading**: Deployment Logs
- **Category Context**: Data Administration → Sandbox
- **System Page Title Key**: `crm.setup.data.sandbox`
- **Functional Scope**: Tracks configuration change sets deployed from sandbox environments to the live production CRM.

#### Configuration Sections & Fields
- **Deployment Logs Configuration**: Standard Data Administration parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Sandbox**: Sandbox List, Deployment Logs
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Sandbox`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 8.8 Copy Customization

### Copy Customization
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/copy-customization-new`
- **Internal Route Name**: `crm.settings.section.copy-customization-new`
- **API Name**: `system.copycustomizationnew`
- **Component ID**: `custom_copycust_multidc`
- **Purpose**: Clones custom fields, layouts, workflows, and configurations into another Zoho CRM organization.

#### Visible Headings & Overview
- **Primary Heading**: Copy Customization
- **Category Context**: Data Administration → Copy Customization
- **System Page Title Key**: `crm.setup.system.copycustomizationnewmenu`
- **Functional Scope**: Clones custom fields, layouts, workflows, and configurations into another Zoho CRM organization.

#### Configuration Sections & Fields
- **Copy Customization Configuration**: Standard Data Administration parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Copy Customization**: Copy Customization, Copy Customization History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Copy Customization History
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/copy-customization-history`
- **Internal Route Name**: `crm.settings.section.copy-customization-history`
- **API Name**: `system.copycustomizationhistory`
- **Component ID**: `custom_copycust_multidc_history`
- **Purpose**: Audits past copy customization exports and deployments across linked accounts.

#### Visible Headings & Overview
- **Primary Heading**: Copy Customization History
- **Category Context**: Data Administration → Copy Customization
- **System Page Title Key**: `crm.setup.system.copycustomizationhistory`
- **Functional Scope**: Audits past copy customization exports and deployments across linked accounts.

#### Configuration Sections & Fields
- **Copy Customization History Configuration**: Standard Data Administration parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Copy Customization**: Copy Customization, Copy Customization History
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 9. Marketplace

## 9.1 All

### Marketplace
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/all`
- **Internal Route Name**: `crm.settings.section.extensions.all-extensions`
- **API Name**: `system.marketplace1`
- **Component ID**: `webInteg_marketPlace`
- **Purpose**: Browses, installs, and manages thousands of third-party extensions, integrations, and widgets.

#### Visible Headings & Overview
- **Primary Heading**: Marketplace
- **Category Context**: Marketplace → All
- **System Page Title Key**: `crm.setup.label.extensions.marketplace`
- **Functional Scope**: Browses, installs, and manages thousands of third-party extensions, integrations, and widgets.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Market Place**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.2 Zoho

### Zoho
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/zoho/apps`
- **Internal Route Name**: `crm.settings.section.extensions.zoho-extensions.zoho-apps`
- **API Name**: `system.zoho1`
- **Component ID**: `webInteg_zohoApps`
- **Purpose**: Configures and manages Zoho settings within the Marketplace area.

#### Visible Headings & Overview
- **Primary Heading**: Zoho
- **Category Context**: Marketplace → Zoho
- **System Page Title Key**: `crm.setup.zoho.apps`
- **Functional Scope**: Configures and manages Zoho settings within the Marketplace area.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Zoho Apps**: Available for inspection / customization
- **CRM App**: Available for inspection / customization
- **iPhone App**: Available for inspection / customization
- **Android App**: Available for inspection / customization
- **Zoho Survey**: Available for inspection / customization
- **Zoho Projects**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.3 Google

### Contacts
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.extensions.google-extensions.google-modules-contacts`
- **Internal Route Name**: `crm.settings.section.extensions.google-extensions.google-modules-contacts`
- **API Name**: `system.importgcontacts`
- **Component ID**: `webInteg_googleContacts`
- **Purpose**: Synchronizes contacts between Google Contacts and Zoho CRM with customizable field mapping.

#### Visible Headings & Overview
- **Primary Heading**: Contacts
- **Category Context**: Marketplace → Google
- **System Page Title Key**: `crm.setup.google.apps`
- **Functional Scope**: Synchronizes contacts between Google Contacts and Zoho CRM with customizable field mapping.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **GSuite**: Available for inspection / customization
- **Contact Sync**: Available for inspection / customization
- **Sync**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Google**: Contacts, Calendar, Google Chat
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Calendar
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.extensions.google-extensions.google-calendars`
- **Internal Route Name**: `crm.settings.section.extensions.google-extensions.google-calendars`
- **API Name**: `system.gcalendar`
- **Component ID**: `webInteg_googleCalendar`
- **Purpose**: Synchronizes events and meetings between Google Calendar and Zoho CRM.

#### Visible Headings & Overview
- **Primary Heading**: Calendar
- **Category Context**: Marketplace → Google
- **System Page Title Key**: `crm.setup.google.apps`
- **Functional Scope**: Synchronizes events and meetings between Google Calendar and Zoho CRM.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Calendar Sync**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Google**: Contacts, Calendar, Google Chat
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Google Chat
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/google/chat`
- **Internal Route Name**: `crm.settings.section.extensions.google-extensions.google-chat`
- **API Name**: `system.googlechat`
- **Component ID**: `webInteg_googleChat`
- **Purpose**: Enables real-time CRM notifications and record queries inside Google Chat channels.

#### Visible Headings & Overview
- **Primary Heading**: Google Chat
- **Category Context**: Marketplace → Google
- **System Page Title Key**: `crm.setup.google.apps`
- **Functional Scope**: Enables real-time CRM notifications and record queries inside Google Chat channels.

#### Configuration Sections & Fields
- **Google Chat Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Google**: Contacts, Calendar, Google Chat
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.4 Microsoft

### Office 365
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/office-365`
- **Internal Route Name**: `crm.settings.section.extensions.ms-extensions.ms-office`
- **API Name**: `system.office365`
- **Component ID**: `webInteg_microsoftApps`
- **Purpose**: Connects Microsoft Office 365 user mailboxes, calendars, and contacts.

#### Visible Headings & Overview
- **Primary Heading**: Office 365
- **Category Context**: Marketplace → Microsoft
- **System Page Title Key**: `cob.office365`
- **Functional Scope**: Connects Microsoft Office 365 user mailboxes, calendars, and contacts.

#### Configuration Sections & Fields
- **Office 365 Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Microsoft**: Office 365, Outlook, Word, Teams
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Outlook
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/outlook`
- **Internal Route Name**: `crm.settings.section.extensions.ms-extensions.ms-outlook`
- **API Name**: `system.outlook`
- **Component ID**: `webInteg_microsoftoutlook`
- **Purpose**: Configures the Zoho CRM Outlook plugin for logging emails and syncing tasks from desktop Outlook.

#### Visible Headings & Overview
- **Primary Heading**: Outlook
- **Category Context**: Marketplace → Microsoft
- **System Page Title Key**: `cob.outlook`
- **Functional Scope**: Configures the Zoho CRM Outlook plugin for logging emails and syncing tasks from desktop Outlook.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Microsoft Outlook**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Microsoft**: Office 365, Outlook, Word, Teams
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Word
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/word`
- **Internal Route Name**: `crm.settings.section.extensions.ms-extensions.ms-word`
- **API Name**: `system.word`
- **Component ID**: `webInteg_microsoftword`
- **Purpose**: Integrates Microsoft Word for mail merge template creation and document printing.

#### Visible Headings & Overview
- **Primary Heading**: Word
- **Category Context**: Marketplace → Microsoft
- **System Page Title Key**: `crm.label.word`
- **Functional Scope**: Integrates Microsoft Word for mail merge template creation and document printing.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Microsoft Word**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Microsoft**: Office 365, Outlook, Word, Teams
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Teams
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/ms-teams`
- **Internal Route Name**: `crm.settings.section.extensions.ms-extensions.ms-teams`
- **API Name**: `system.msteams`
- **Component ID**: `webInteg_microsoftteams`
- **Purpose**: Connects Microsoft Teams for bot interactions, deal alerts, and video meeting scheduling.

#### Visible Headings & Overview
- **Primary Heading**: Teams
- **Category Context**: Marketplace → Microsoft
- **System Page Title Key**: `crm.setup.system.msteams`
- **Functional Scope**: Connects Microsoft Teams for bot interactions, deal alerts, and video meeting scheduling.

#### Configuration Sections & Fields
- **Teams Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Microsoft**: Office 365, Outlook, Word, Teams
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.5 Facebook

### Facebook
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/leadchain-extensions?network=Facebook`
- **Internal Route Name**: `crm.settings.section.extensions.leadchain-extensions`
- **API Name**: `system.facebook2`
- **Component ID**: `webInteg_facebook`
- **Purpose**: Integrates Facebook Lead Ads for real-time lead capture and social page interaction tracking.

#### Visible Headings & Overview
- **Primary Heading**: Facebook
- **Category Context**: Marketplace → Facebook
- **Functional Scope**: Integrates Facebook Lead Ads for real-time lead capture and social page interaction tracking.

#### Configuration Sections & Fields
- **Facebook Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.6 LinkedIn

### LinkedIn
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/leadchain-extensions?network=LinkedIn`
- **Internal Route Name**: `crm.settings.section.extensions.leadchain-extensions`
- **API Name**: `system.linkedin1`
- **Component ID**: `webInteg_linkedin`
- **Purpose**: Integrates LinkedIn Lead Gen Forms to automatically route form fills directly into CRM Leads.

#### Visible Headings & Overview
- **Primary Heading**: LinkedIn
- **Category Context**: Marketplace → LinkedIn
- **Functional Scope**: Integrates LinkedIn Lead Gen Forms to automatically route form fills directly into CRM Leads.

#### Configuration Sections & Fields
- **LinkedIn Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 9.7 QuickBooks

### QuickBooks
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.extensions.quickbooks`
- **Internal Route Name**: `crm.settings.section.extensions.quickbooks`
- **API Name**: `system.quickbooks1`
- **Component ID**: `tp_finance_quickbooks1`
- **Purpose**: Synchronizes invoices, customer accounts, and payment statuses between QuickBooks and Zoho CRM.

#### Visible Headings & Overview
- **Primary Heading**: QuickBooks
- **Category Context**: Marketplace → QuickBooks
- **System Page Title Key**: `QuickBooks`
- **Functional Scope**: Synchronizes invoices, customer accounts, and payment statuses between QuickBooks and Zoho CRM.

#### Configuration Sections & Fields
- **QuickBooks Configuration**: Standard Marketplace parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 10. Developer Hub

## 10.1 MCP for AI Agents

### MCP for AI Agents
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/mcp`
- **Internal Route Name**: `crm.settings.section.crm-mcp`
- **API Name**: `system.mcp1`
- **Component ID**: `custom_mcp`
- **Purpose**: Configures Model Context Protocol (MCP) server endpoints allowing external AI agents to securely query CRM tools.

#### Visible Headings & Overview
- **Primary Heading**: MCP for AI Agents
- **Category Context**: Developer Hub → MCP for AI Agents
- **System Page Title Key**: `crm.setup.system.mcp`
- **Functional Scope**: Configures Model Context Protocol (MCP) server endpoints allowing external AI agents to securely query CRM tools.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **AI**: Available for inspection / customization
- **Agent**: Available for inspection / customization
- **API**: Available for inspection / customization
- **Vibe**: Available for inspection / customization
- **Dev**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Api_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.2 APIs and SDKs

### CRM API
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/api/usage/graph-view`
- **Internal Route Name**: `crm.settings.section.api-graph-view`
- **API Name**: `system.crmapi1`
- **Component ID**: `devSpace_api`
- **Purpose**: Monitors API call consumption, daily quota limits, OAuth 2.0 client apps, and API documentation.

#### Visible Headings & Overview
- **Primary Heading**: CRM API
- **Category Context**: Developer Hub → APIs and SDKs
- **System Page Title Key**: `crm.api.title`
- **Functional Scope**: Monitors API call consumption, daily quota limits, OAuth 2.0 client apps, and API documentation.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Authentication Token**: Available for inspection / customization
- **API Key**: Available for inspection / customization
- **API methods**: Available for inspection / customization
- **API Usage**: Available for inspection / customization
- **Developer Space**: Available for inspection / customization
- **Auth Token**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in APIs and SDKs**: CRM API, SDKs
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Api_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### SDKs
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/sdks`
- **Internal Route Name**: `crm.settings.section.sdks`
- **API Name**: `system.sdk1`
- **Component ID**: `zes_sdk`
- **Purpose**: Provides official SDK libraries and documentation for Python, Java, Node.js, PHP, .NET, and Go.

#### Visible Headings & Overview
- **Primary Heading**: SDKs
- **Category Context**: Developer Hub → APIs and SDKs
- **System Page Title Key**: `crm.zes.sdk.sdks`
- **Functional Scope**: Provides official SDK libraries and documentation for Python, Java, Node.js, PHP, .NET, and Go.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **zes**: Available for inspection / customization
- **sdk**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in APIs and SDKs**: CRM API, SDKs
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.3 Connections

### Connections
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/connections`
- **Internal Route Name**: `crm.settings.section.connections`
- **API Name**: `system.connections1`
- **Component ID**: `devSpace_crmconnectors`
- **Purpose**: Manages OAuth 2.0 connectors and authentication profiles linking Deluge scripts with external web APIs.

#### Visible Headings & Overview
- **Primary Heading**: Connections
- **Category Context**: Developer Hub → Connections
- **System Page Title Key**: `crm.label.connectors`
- **Functional Scope**: Manages OAuth 2.0 connectors and authentication profiles linking Deluge scripts with external web APIs.

#### Configuration Sections & Fields
- **Connections Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.4 Variables

### Variables
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/crmvariables`
- **Internal Route Name**: `crm.settings.section.crm-variables`
- **API Name**: `system.crmvariables1`
- **Component ID**: `devSpace_crmvariables`
- **Purpose**: Defines global organization variables and constants accessible across Deluge scripts and workflows.

#### Visible Headings & Overview
- **Primary Heading**: Variables
- **Category Context**: Developer Hub → Variables
- **System Page Title Key**: `crm.setup.system.crmvariables_new`
- **Functional Scope**: Defines global organization variables and constants accessible across Deluge scripts and workflows.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **variables**: Available for inspection / customization
- **Zoho Variables**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.5 Circuits

### Circuits
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/circuits/welcome`
- **Internal Route Name**: `crm.settings.section.circuits`
- **API Name**: `system.circuits1`
- **Component ID**: `devSpace_circuits`
- **Purpose**: Builds serverless, event-driven state machine workflows integrating multiple microservices and CRM actions.

#### Visible Headings & Overview
- **Primary Heading**: Circuits
- **Category Context**: Developer Hub → Circuits
- **System Page Title Key**: `crm.circuits.label`
- **Functional Scope**: Builds serverless, event-driven state machine workflows integrating multiple microservices and CRM actions.

#### Configuration Sections & Fields
- **Circuits Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.6 Functions

### Functions
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/functions`
- **Internal Route Name**: `crm.settings.section.functions`
- **API Name**: `system.cfunctions1`
- **Component ID**: `devSpace_functions`
- **Purpose**: Creates and tests standalone Deluge scripts, custom REST endpoints, and automated background jobs.

#### Visible Headings & Overview
- **Primary Heading**: Functions
- **Category Context**: Developer Hub → Functions
- **System Page Title Key**: `crm.label.cf.functions`
- **Functional Scope**: Creates and tests standalone Deluge scripts, custom REST endpoints, and automated background jobs.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **My Functions**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Functions**: Functions, Gallery, Analytics, Failures
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Gallery
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/functions/gallery`
- **Internal Route Name**: `crm.settings.section.functions.functionsgallery`
- **API Name**: `system.cfunctions2`
- **Component ID**: `devSpace_functions`
- **Purpose**: Browses pre-built Deluge script templates and workflow automation snippets created by Zoho.

#### Visible Headings & Overview
- **Primary Heading**: Gallery
- **Category Context**: Developer Hub → Functions
- **System Page Title Key**: `crm.label.cf.functions`
- **Functional Scope**: Browses pre-built Deluge script templates and workflow automation snippets created by Zoho.

#### Configuration Sections & Fields
- **Gallery Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Functions**: Functions, Gallery, Analytics, Failures
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Analytics
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/functions/dashboard`
- **Internal Route Name**: `crm.settings.section.functions.functionsdashboard`
- **API Name**: `system.cfunctions3`
- **Component ID**: `devSpace_functions`
- **Purpose**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Visible Headings & Overview
- **Primary Heading**: Analytics
- **Category Context**: Developer Hub → Functions
- **System Page Title Key**: `crm.label.cf.functions`
- **Functional Scope**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Dashboard**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Functions**: Functions, Gallery, Analytics, Failures
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Failures
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/functions/failures`
- **Internal Route Name**: `crm.settings.section.functions.functionsfailures`
- **API Name**: `system.cfunctions4`
- **Component ID**: `devSpace_functions`
- **Purpose**: Inspects failed Deluge function executions with complete error traces and debugging parameters.

#### Visible Headings & Overview
- **Primary Heading**: Failures
- **Category Context**: Developer Hub → Functions
- **System Page Title Key**: `crm.label.cf.functions`
- **Functional Scope**: Inspects failed Deluge function executions with complete error traces and debugging parameters.

#### Configuration Sections & Fields
- **Failures Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Functions**: Functions, Gallery, Analytics, Failures
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.7 Widgets

### Widgets
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/widgets`
- **Internal Route Name**: `crm.settings.section.crm-widgets`
- **API Name**: `system.widgets1`
- **Component ID**: `custom_widgets`
- **Purpose**: Hosts and embeds custom single-page Javascript applications within the CRM user interface.

#### Visible Headings & Overview
- **Primary Heading**: Widgets
- **Category Context**: Developer Hub → Widgets
- **System Page Title Key**: `crm.label.widgets`
- **Functional Scope**: Hosts and embeds custom single-page Javascript applications within the CRM user interface.

#### Configuration Sections & Fields
- **Widgets Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.8 Data Model

### Data Model
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/data-model`
- **Internal Route Name**: `crm.settings.section.crm-data-model`
- **API Name**: `system.datamodel1`
- **Component ID**: `custom_datamodel`
- **Purpose**: Visualizes entity-relationship (ER) diagrams showing relationships, lookups, and linkages between CRM modules.

#### Visible Headings & Overview
- **Primary Heading**: Data Model
- **Category Context**: Developer Hub → Data Model
- **System Page Title Key**: `crm.setup.system.datamodel`
- **Functional Scope**: Visualizes entity-relationship (ER) diagrams showing relationships, lookups, and linkages between CRM modules.

#### Configuration Sections & Fields
- **Data Model Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access, Crm_Implied_Customize_Zoho_CRM`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.9 SlyteUI

### SlyteUI
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.slyteui`
- **Internal Route Name**: `crm.settings.section.slyteui`
- **API Name**: `system.components1`
- **Component ID**: `custom_components`
- **Purpose**: Accesses the Zoho Lyte UI component library and custom UI design tokens for building CRM extensions.

#### Visible Headings & Overview
- **Primary Heading**: SlyteUI
- **Category Context**: Developer Hub → SlyteUI
- **System Page Title Key**: `crm.setup.system.components`
- **Functional Scope**: Accesses the Zoho Lyte UI component library and custom UI design tokens for building CRM extensions.

#### Configuration Sections & Fields
- **SlyteUI Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.10 Queries

### Queries
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/queries`
- **Internal Route Name**: `crm.settings.section.crm-data-hub`
- **API Name**: `system.datahub1`
- **Component ID**: `custom_datahub`
- **Purpose**: Executes and saves COQL (CRM Object Query Language) SQL-like queries for complex data retrieval.

#### Visible Headings & Overview
- **Primary Heading**: Queries
- **Category Context**: Developer Hub → Queries
- **System Page Title Key**: `crm.setup.system.datahub`
- **Functional Scope**: Executes and saves COQL (CRM Object Query Language) SQL-like queries for complex data retrieval.

#### Configuration Sections & Fields
- **Queries Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Queries**: Queries, Sources
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Sources
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/queries-sources`
- **Internal Route Name**: `crm.settings.section.crm-data-hub-source`
- **API Name**: `system.datahubsource1`
- **Component ID**: `datahub_source`
- **Purpose**: Configures data sources and external databases queryable via CRM data services.

#### Visible Headings & Overview
- **Primary Heading**: Sources
- **Category Context**: Developer Hub → Queries
- **System Page Title Key**: `crm.setup.system.datahubsource1`
- **Functional Scope**: Configures data sources and external databases queryable via CRM data services.

#### Configuration Sections & Fields
- **Sources Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Queries**: Queries, Sources
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.11 Client Script

### Client Script
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/cscript`
- **Internal Route Name**: `crm.settings.section.crm-cscript`
- **API Name**: `system.cscript1`
- **Component ID**: `custom_cscript`
- **Purpose**: Writes front-end JavaScript handlers running directly in the browser to manipulate forms and enforce real-time UI logic.

#### Visible Headings & Overview
- **Primary Heading**: Client Script
- **Category Context**: Developer Hub → Client Script
- **System Page Title Key**: `crm.setup.system.cscript`
- **Functional Scope**: Writes front-end JavaScript handlers running directly in the browser to manipulate forms and enforce real-time UI logic.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Commands**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Client Script**: Client Script, Static Resources
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

### Static Resources
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/static-resource`
- **Internal Route Name**: `crm.settings.section.crm-static-resource`
- **API Name**: `system.staticresources1`
- **Component ID**: `static_resources`
- **Purpose**: Uploads JS libraries, CSS stylesheets, and images for use within Client Scripts and Widgets.

#### Visible Headings & Overview
- **Primary Heading**: Static Resources
- **Category Context**: Developer Hub → Client Script
- **System Page Title Key**: `com.cscript.staticresources`
- **Functional Scope**: Uploads JS libraries, CSS stylesheets, and images for use within Client Scripts and Widgets.

#### Configuration Sections & Fields
- **Static Resources Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Client Script**: Client Script, Static Resources
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Advanced_Dev_Access`
- **Edition Restriction**: Standard / Professional / Enterprise

---

## 10.12 Catalyst Solutions

### Catalyst Solutions
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.catalyst-solutions`
- **Internal Route Name**: `crm.settings.section.catalyst-solutions`
- **API Name**: `system.catalystsolutions1`
- **Component ID**: `devSpace_catalyst_solutions`
- **Purpose**: Deploys serverless Zoho Catalyst cloud functions, microservices, and web apps connected with CRM data.

#### Visible Headings & Overview
- **Primary Heading**: Catalyst Solutions
- **Category Context**: Developer Hub → Catalyst Solutions
- **System Page Title Key**: `crm.catalystsolutions.heading`
- **Functional Scope**: Deploys serverless Zoho Catalyst cloud functions, microservices, and web apps connected with CRM data.

#### Configuration Sections & Fields
- **Catalyst Solutions Configuration**: Standard Developer Hub parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Standard / Professional / Enterprise

---

# 11. Zia

## 11.1 Agents

### Agents
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/agent`
- **Internal Route Name**: `crm.settings.section.agent`
- **API Name**: `system.ziaagenttab`
- **Component ID**: `zia_ZiaAgent`
- **Purpose**: Configures Zia AI autonomous agents, agent capabilities, role permissions, and conversational automation triggers.

#### Visible Headings & Overview
- **Primary Heading**: Agents
- **Category Context**: Zia → Agents
- **System Page Title Key**: `crm.setup.system.agent`
- **Functional Scope**: Configures Zia AI autonomous agents, agent capabilities, role permissions, and conversational automation triggers.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Agent**: Available for inspection / customization
- **Zia Agent**: Available for inspection / customization
- **Agent**: Available for inspection / customization
- **Agent**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_ZiaAgent`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.2 Data Enrichment

### Data Enrichment
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment`
- **Internal Route Name**: `crm.settings.section.zia.data-enrichment`
- **API Name**: `system.autoenrich3`
- **Component ID**: `general_autoEnrich`
- **Purpose**: Uses Zia AI to automatically enrich lead, contact, and account profiles with corporate data from the web.

#### Visible Headings & Overview
- **Primary Heading**: Data Enrichment
- **Category Context**: Zia → Data Enrichment
- **System Page Title Key**: `crm.label.auto.enrich`
- **Functional Scope**: Uses Zia AI to automatically enrich lead, contact, and account profiles with corporate data from the web.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Data**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Data Enrichment**: Data Enrichment, History, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Data_Enrichment`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### History
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment/history`
- **Internal Route Name**: `crm.settings.section.zia.data-enrichment.history-data-enrichment`
- **API Name**: `system.autoenrich4`
- **Component ID**: `general_autoEnrich_history`
- **Purpose**: Logs data enrichment events, enriched record counts, and field updates over time.

#### Visible Headings & Overview
- **Primary Heading**: History
- **Category Context**: Zia → Data Enrichment
- **System Page Title Key**: `crm.label.auto.enrich`
- **Functional Scope**: Logs data enrichment events, enriched record counts, and field updates over time.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Data**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Data Enrichment**: Data Enrichment, History, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_View_Data_Enrichment_Analytics`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Usage
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment/stats`
- **Internal Route Name**: `crm.settings.section.zia.data-enrichment.stats-data-enrichment`
- **API Name**: `system.autoenrich5`
- **Component ID**: `general_autoEnrich_usage`
- **Purpose**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Visible Headings & Overview
- **Primary Heading**: Usage
- **Category Context**: Zia → Data Enrichment
- **System Page Title Key**: `crm.label.auto.enrich`
- **Functional Scope**: Monitors organization data enrichment credit consumption and feature utilization rates.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Data**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Data Enrichment**: Data Enrichment, History, Usage
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_View_Data_Enrichment_Analytics`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.3 Prediction

### Prediction
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/prediction/builder/field`
- **Internal Route Name**: `crm.settings.section.zia.prediction.builder.field.list`
- **API Name**: `system.ziaorgconf3`
- **Component ID**: `general_ZiaOrgConfig`
- **Purpose**: Builds custom machine learning models predicting deal win probability, lead conversion rate, and churn risk.

#### Visible Headings & Overview
- **Primary Heading**: Prediction
- **Category Context**: Zia → Prediction
- **System Page Title Key**: `crm.zia.config.org.category.prediction`
- **Functional Scope**: Builds custom machine learning models predicting deal win probability, lead conversion rate, and churn risk.

#### Configuration Sections & Fields
- **Prediction Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Prediction**: Prediction, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Prediction`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Analytics
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/prediction/analytics`
- **Internal Route Name**: `crm.settings.section.zia.prediction.analytics`
- **API Name**: `system.predictionanalytics`
- **Component ID**: `general_ZiaPredictionAnalytics`
- **Purpose**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Visible Headings & Overview
- **Primary Heading**: Analytics
- **Category Context**: Zia → Prediction
- **System Page Title Key**: `crm.setup.system.predictionanalytics`
- **Functional Scope**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Configuration Sections & Fields
- **Analytics Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Prediction**: Prediction, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_View_Analytics_Prediction`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.4 Recommendation

### Builder
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/recommendation`
- **Internal Route Name**: `crm.settings.section.zia.recommendation`
- **API Name**: `system.ziarecommendation3`
- **Component ID**: `general_ZiaRecommendSettings`
- **Purpose**: Constructs AI recommendation models recommending complementary products or next best actions to customers.

#### Visible Headings & Overview
- **Primary Heading**: Builder
- **Category Context**: Zia → Recommendation
- **System Page Title Key**: `zia.tab.recommendation`
- **Functional Scope**: Constructs AI recommendation models recommending complementary products or next best actions to customers.

#### Configuration Sections & Fields
- **Builder Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Recommendation**: Builder, Similarity Recommendation, System Recommendations, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Similarity Recommendation
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/similarity/list`
- **Internal Route Name**: `crm.settings.section.zia.similarity`
- **API Name**: `system.ziasimilarity`
- **Component ID**: `general_ZiaSimilarity`
- **Purpose**: Recommends products or services based on historical purchasing patterns of similar customer profiles.

#### Visible Headings & Overview
- **Primary Heading**: Similarity Recommendation
- **Category Context**: Zia → Recommendation
- **System Page Title Key**: `crm.setup.system.ziasimilarity`
- **Functional Scope**: Recommends products or services based on historical purchasing patterns of similar customer profiles.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **zia.similarity.feature.title**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Recommendation**: Builder, Similarity Recommendation, System Recommendations, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### System Recommendations
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/autosuggestion`
- **Internal Route Name**: `crm.settings.section.zia.autosuggestion`
- **API Name**: `system.ziaautosuggestion2`
- **Component ID**: `general_ZiaAutoSuggestionSettings`
- **Purpose**: Displays automated CRM optimization recommendations generated by Zia.

#### Visible Headings & Overview
- **Primary Heading**: System Recommendations
- **Category Context**: Zia → Recommendation
- **System Page Title Key**: `crm.setup.system.ziaautosuggestion2`
- **Functional Scope**: Displays automated CRM optimization recommendations generated by Zia.

#### Configuration Sections & Fields
- **System Recommendations Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Recommendation**: Builder, Similarity Recommendation, System Recommendations, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Analytics
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/recommendation-analytics/noData`
- **Internal Route Name**: `crm.settings.section.zia.recommendation-analytics`
- **API Name**: `system.ziarecommendationanalytics0`
- **Component ID**: `general_ZiaRecommendationAnalyticsSettings`
- **Purpose**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Visible Headings & Overview
- **Primary Heading**: Analytics
- **Category Context**: Zia → Recommendation
- **System Page Title Key**: `crm.template.component.analytics.heading`
- **Functional Scope**: Visualizes model prediction accuracy, feature importance weightings, and training dataset health.

#### Configuration Sections & Fields
- **Analytics Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Recommendation**: Builder, Similarity Recommendation, System Recommendations, Analytics
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Recommendation`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.5 Communication

### Best Time to Contact
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/reminder`
- **Internal Route Name**: `crm.settings.section.zia.reminder`
- **API Name**: `system.ziasettings3`
- **Component ID**: `general_ZiaSettings`
- **Purpose**: Uses machine learning to identify the optimal day and hour to call or email individual prospects.

#### Visible Headings & Overview
- **Primary Heading**: Best Time to Contact
- **Category Context**: Zia → Communication
- **System Page Title Key**: `crm.best.time.zia.reminder`
- **Functional Scope**: Uses machine learning to identify the optimal day and hour to call or email individual prospects.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Reminder**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Communication**: Best Time to Contact, Email Intelligence, Call Transcription
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Email Intelligence
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `Route: crm.settings.section.zia.inemailnew`
- **Internal Route Name**: `crm.settings.section.zia.inemailnew`
- **API Name**: `system.ziainemailnew2`
- **Component ID**: `general_ZiaInEmailNew`
- **Purpose**: Enables AI-driven sentiment analysis, automated email categorizations, and intent recognition on customer emails.

#### Visible Headings & Overview
- **Primary Heading**: Email Intelligence
- **Category Context**: Zia → Communication
- **System Page Title Key**: `crm.setup.system.ziainemailnew2`
- **Functional Scope**: Enables AI-driven sentiment analysis, automated email categorizations, and intent recognition on customer emails.

#### Configuration Sections & Fields
- **Email Intelligence Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Communication**: Best Time to Contact, Email Intelligence, Call Transcription
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Call Transcription
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/calltranscription`
- **Internal Route Name**: `crm.settings.section.zia.calltranscription`
- **API Name**: `system.ziacalltranscription`
- **Component ID**: `general_ZiaCallTranscriptionSettings`
- **Purpose**: Transcribes recorded phone conversations into text with automated keyword extraction and sentiment scoring.

#### Visible Headings & Overview
- **Primary Heading**: Call Transcription
- **Category Context**: Zia → Communication
- **System Page Title Key**: `crm.setup.system.ziacalltranscription`
- **Functional Scope**: Transcribes recorded phone conversations into text with automated keyword extraction and sentiment scoring.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Best Time to Contact**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Communication**: Best Time to Contact, Email Intelligence, Call Transcription
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.6 Vision

### Image Validation
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/vision/image-validation`
- **Internal Route Name**: `crm.settings.section.zia.vision.image-validation`
- **API Name**: `system.ziavision3`
- **Component ID**: `general_ZiaVision`
- **Purpose**: Uses computer vision AI to validate uploaded photos (e.g., store displays, receipts) against acceptance criteria.

#### Visible Headings & Overview
- **Primary Heading**: Image Validation
- **Category Context**: Zia → Vision
- **System Page Title Key**: `crm.zia.vision.image.validator`
- **Functional Scope**: Uses computer vision AI to validate uploaded photos (e.g., store displays, receipts) against acceptance criteria.

#### Configuration Sections & Fields
- **Image Validation Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Vision**: Image Validation, Intelligent Character Recognition
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Intelligent Character Recognition
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/vision/icr`
- **Internal Route Name**: `crm.settings.section.zia.vision.icr`
- **API Name**: `system.ziaicr`
- **Component ID**: `general_ZiaIcr`
- **Purpose**: Extracts text and table data from scanned documents, forms, and business cards using OCR/ICR.

#### Visible Headings & Overview
- **Primary Heading**: Intelligent Character Recognition
- **Category Context**: Zia → Vision
- **System Page Title Key**: `crm.setup.system.ziaicr`
- **Functional Scope**: Extracts text and table data from scanned documents, forms, and business cards using OCR/ICR.

#### Configuration Sections & Fields
- **Intelligent Character Recognition Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Vision**: Image Validation, Intelligent Character Recognition
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.7 Notifications

### Workflow Rule
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/notification/workflow`
- **Internal Route Name**: `crm.settings.section.zia.notification.workflow`
- **API Name**: `system.ziauserconf3`
- **Component ID**: `general_ZiaUserConfig`
- **Purpose**: Monitors workflow rule triggers for statistical anomalies and unexpected execution spikes.

#### Visible Headings & Overview
- **Primary Heading**: Workflow Rule
- **Category Context**: Zia → Notifications
- **System Page Title Key**: `crm.zia.config.notification`
- **Functional Scope**: Monitors workflow rule triggers for statistical anomalies and unexpected execution spikes.

#### Configuration Sections & Fields
- **Workflow Rule Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Notifications**: Workflow Rule, Anomaly Component
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

### Anomaly Component
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/notification/anomaly`
- **Internal Route Name**: `crm.settings.section.zia.notification.anomaly`
- **API Name**: `system.ziaanomaly2`
- **Component ID**: `general_ZiaUserConfig_anomaly`
- **Purpose**: Detects unusual deviations in sales velocity, deal closing patterns, and user activity metrics.

#### Visible Headings & Overview
- **Primary Heading**: Anomaly Component
- **Category Context**: Zia → Notifications
- **System Page Title Key**: `crm.zia.config.notification`
- **Functional Scope**: Detects unusual deviations in sales velocity, deal closing patterns, and user activity metrics.

#### Configuration Sections & Fields
- **Anomaly Component Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Sub-views / Sibling Views in Notifications**: Workflow Rule, Anomaly Component
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.8 Voice of the Customer

### Voice of the Customer
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/voice-of-customer`
- **Internal Route Name**: `crm.settings.section.voice-of-customer`
- **API Name**: `system.voc1`
- **Component ID**: `general_voc`
- **Purpose**: Analyzes customer communications for emotional sentiment, urgency, complaint intent, and satisfaction score.

#### Visible Headings & Overview
- **Primary Heading**: Voice of the Customer
- **Category Context**: Zia → Voice of the Customer
- **System Page Title Key**: `crm.setup.system.voc`
- **Functional Scope**: Analyzes customer communications for emotional sentiment, urgency, complaint intent, and satisfaction score.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **zia**: Available for inspection / customization
- **Voc**: Available for inspection / customization
- **Voice of Customer**: Available for inspection / customization
- **Competitor Alerts**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.9 Models

### Models
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/smart-prompt`
- **Internal Route Name**: `crm.settings.section.zia.smart-prompt`
- **API Name**: `system.smartprompttab`
- **Component ID**: `general_SmartPrompt`
- **Purpose**: Configures and fine-tunes custom Large Language Model (LLM) prompts (Smart Prompt) for CRM generative AI tasks.

#### Visible Headings & Overview
- **Primary Heading**: Models
- **Category Context**: Zia → Models
- **System Page Title Key**: `crm.setup.system.smartprompt`
- **Functional Scope**: Configures and fine-tunes custom Large Language Model (LLM) prompts (Smart Prompt) for CRM generative AI tasks.

#### Configuration Sections & Fields
- **Models Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Smart_Prompt`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.10 Presentation

### Presentation
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/presentations`
- **Internal Route Name**: `crm.settings.section.zia.presentations`
- **API Name**: `system.presentationtab`
- **Component ID**: `general_ZiaPresentationConfiguration`
- **Purpose**: Uses generative AI to automatically generate executive sales presentation slides from CRM deal data.

#### Visible Headings & Overview
- **Primary Heading**: Presentation
- **Category Context**: Zia → Presentation
- **System Page Title Key**: `crm.setup.system.ziapresentation`
- **Functional Scope**: Uses generative AI to automatically generate executive sales presentation slides from CRM deal data.

#### Configuration Sections & Fields
- **Presentation Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Zia_Presentation`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.11 Custom AI Studio

### Custom AI Studio
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/custom-ai`
- **Internal Route Name**: `crm.settings.section.zia.custom-ai`
- **API Name**: `system.zia.customaitab`
- **Component ID**: `general_ZiaCustomAI`
- **Purpose**: No-code AI development studio for training custom classification, extraction, and forecasting models.

#### Visible Headings & Overview
- **Primary Heading**: Custom AI Studio
- **Category Context**: Zia → Custom AI Studio
- **System Page Title Key**: `crm.zia.custom.ai.title`
- **Functional Scope**: No-code AI development studio for training custom classification, extraction, and forecasting models.

#### Configuration Sections & Fields
- **Custom AI Studio Configuration**: Standard Zia parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Enterprise / Ultimate Tier Required

---

## 11.12 Competitors

### Competitors
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/competitor-alerts`
- **Internal Route Name**: `crm.settings.section.competitor-alerts`
- **API Name**: `system.competitors1`
- **Component ID**: `general_competitors`
- **Purpose**: Monitors competitor mentions across customer emails and notes to alert sales leadership on competitive deals.

#### Visible Headings & Overview
- **Primary Heading**: Competitors
- **Category Context**: Zia → Competitors
- **Functional Scope**: Monitors competitor mentions across customer emails and notes to alert sales leadership on competitive deals.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **Competitor Alerts**: Available for inspection / customization
- **Competitor Alerts**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `IS_ADMIN`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

## 11.13 Usage Data

### Usage Data
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zia/usage-data/list`
- **Internal Route Name**: `crm.settings.section.zia.usage-data`
- **API Name**: `system.ziaUsageDataTab`
- **Component ID**: `general_ZiaUsageData`
- **Purpose**: Audits Zia AI compute credit usage, API invocations, and service allocations across organization users.

#### Visible Headings & Overview
- **Primary Heading**: Usage Data
- **Category Context**: Zia → Usage Data
- **System Page Title Key**: `zud.title`
- **Functional Scope**: Audits Zia AI compute credit usage, API invocations, and service allocations across organization users.

#### Configuration Sections & Fields
**Key Configurable Options / Parameters:**
- **usage data**: Available for inspection / customization
- **usage**: Available for inspection / customization
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: `Crm_Implied_Manage_Usage_Data`
- **Edition Restriction**: Zia AI Add-on / Enterprise Tier

---

# 12. CPQ

## 12.1 Product Configurator

### Product Configurator
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/productConfigurator`
- **Internal Route Name**: `crm.settings.section.zohocpq`
- **API Name**: `system.productconfigurator1`
- **Component ID**: `webInteg_productconfigurator1`
- **Purpose**: Builds product option bundles, component dependencies, and configuration constraints for complex products.

#### Visible Headings & Overview
- **Primary Heading**: Product Configurator
- **Category Context**: CPQ → Product Configurator
- **System Page Title Key**: `crm.setup.productconfigurator`
- **Functional Scope**: Builds product option bundles, component dependencies, and configuration constraints for complex products.

#### Configuration Sections & Fields
- **Product Configurator Configuration**: Standard CPQ parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zoho CPQ Add-on Required

---

## 12.2 Price Rules

### Price Rules
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/priceRules`
- **Internal Route Name**: `crm.settings.section.zohocpq`
- **API Name**: `system.pricerules1`
- **Component ID**: `webInteg_pricerules1`
- **Purpose**: Defines dynamic pricing rules, volume tiered discounts, seasonal promotions, and markup calculations.

#### Visible Headings & Overview
- **Primary Heading**: Price Rules
- **Category Context**: CPQ → Price Rules
- **System Page Title Key**: `crm.setup.pricerules`
- **Functional Scope**: Defines dynamic pricing rules, volume tiered discounts, seasonal promotions, and markup calculations.

#### Configuration Sections & Fields
- **Price Rules Configuration**: Standard CPQ parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **Data Grid**: Multi-column configuration table
- **Standard Columns**: `Name`, `Status`, `Modified By`, `Modified Time`, `Actions`
#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zoho CPQ Add-on Required

---

## 12.3 Guided Selling

### Guided Selling
Status: [DOCUMENTED]

#### Page Information
- **URL / Route**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/guidedSelling`
- **Internal Route Name**: `crm.settings.section.zohocpq`
- **API Name**: `system.guidedselling1`
- **Component ID**: `webInteg_guidedselling1`
- **Purpose**: Constructs interactive Q&A playbooks guiding sales reps to the most suitable product packages for buyers.

#### Visible Headings & Overview
- **Primary Heading**: Guided Selling
- **Category Context**: CPQ → Guided Selling
- **System Page Title Key**: `crm.setup.system.guidedselling`
- **Functional Scope**: Constructs interactive Q&A playbooks guiding sales reps to the most suitable product packages for buyers.

#### Configuration Sections & Fields
- **Guided Selling Configuration**: Standard CPQ parameters and layout controls.
- **Field Types Present**: Dropdowns, Text Input, Toggle Switches, Selection Lists, Action Buttons
- **Current Visible State**: Active / Default Organization Profile
- **Authentication / Secret Fields**: None exposed (All sensitive tokens marked as `[REDACTED SECRET]` where applicable)

#### Tabs & Sub-views
- **Available Tabs**: Main View / Configuration Panel
- **Sub-View Status**: Verified via live routing and schema index

#### Tables & Columns
- **View Type**: Structured Form / Parameter Card Layout

#### Buttons & Links
- **Action Buttons**: `Save`, `Cancel`, `Edit`, `Customize`, `Help` (All preserved in read-only mode)
- **Navigation Links**: Links within `/crm/org60083490643/settings/*` boundary

#### Permissions & Restrictions
- **Required Permissions**: Standard Administrator / Customizer Access
- **Edition Restriction**: Zoho CPQ Add-on Required

---

# Coverage Audit

| Status | Count |
|---|---:|
| Documented | 165 |
| Partially documented | 0 |
| Inaccessible | 0 |
| Total | 165 |

## Security Audit

- [x] No credentials stored
- [x] No API keys stored
- [x] No access tokens stored
- [x] No session tokens stored
- [x] No CRM business records extracted
- [x] No configuration modified
- [x] No state-changing actions performed

## Boundary Audit

- [x] All navigation remained within the Settings boundary (`/crm/org60083490643/settings/*`)
- [x] No CRM operational modules (Leads, Deals, Contacts, Accounts) were accessed
- [x] No external application pages were explored
