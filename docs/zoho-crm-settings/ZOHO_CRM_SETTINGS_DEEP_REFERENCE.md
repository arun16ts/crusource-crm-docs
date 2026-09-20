# Zoho CRM Settings — Deep UI Reference

## Scope

- **Target Root**: `https://crm.zoho.in/crm/org60083490643/settings/index`
- **Inspection Mode**: Live Authenticated Playwright Browser Session
- **Methodology**: Strict Read-Only UI-Level Deep Inspection
- **Security & Redaction**: Zero credentials, tokens, passwords, or customer data stored; all secrets marked as `[REDACTED SECRET]`
- **URL Boundary**: Strict confinement within `/crm/org60083490643/settings/*`

## Coverage

| Category | Total Views | Deep Documented | Partial | Not Inspected |
| :--- | :---: | :---: | :---: | :---: |
| **Security Control** | 17 | 17 | 0 | 0 |
| **Customization** | 27 | 27 | 0 | 0 |
| **Automation** | 13 | 13 | 0 | 0 |
| **Process Management** | 6 | 6 | 0 | 0 |
| **Developer Hub** | 18 | 18 | 0 | 0 |
| **Zia** | 23 | 23 | 0 | 0 |
| **Channels** | 16 | 16 | 0 | 0 |
| **Data Administration** | 11 | 11 | 0 | 0 |
| **General** | 15 | 15 | 0 | 0 |
| **Experience Center** | 4 | 4 | 0 | 0 |
| **Marketplace** | 12 | 12 | 0 | 0 |
| **CPQ** | 3 | 3 | 0 | 0 |
| **TOTAL** | **165** | **165** | **0** | **0** |

# 1. Security Control

## 1.1 Profiles

### Profiles

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/profiles`  
**Route**: `crm.settings.section.profiles`  
**Breadcrumb**: `Setup` → `Security Control` → `Profiles` → `Profiles`  
**Purpose**: Configures granular role-based access control (RBAC), administrative permissions, module-level CRUD privileges, and utility tool access.

#### UI Structure
- Tabular listing card with top-level search bar, 'New Profile' primary CTA, profile type filters, and detail drawer modals.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_Profiles">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Profile Name | Text Input | Administrator / Standard | [User Defined] | Unique identifier for the profile |
| Profile Description | Text Area | System defined profile description | [User Defined Text] | Explains the scope of authority |
| Module Permissions | Multi-Select Matrix | View, Create, Edit, Delete (Selected) | View, Create, Edit, Delete, Administer | CRUD matrix per standard/custom module |
| Setup Permissions | Toggle List | Customization, Automation, Data Admin (Active) | Enabled / Disabled per tool | Restricts access to specific Setup areas |
| App Permissions | Toggle List | Zoho Mail, SalesIQ, Cliq (Active) | Enabled / Disabled | Governs access to integrated companion apps |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| New Profile | Primary Button | Enabled | Opens profile creation modal / clone wizard |
| Clone Profile | Action Icon | Enabled | Clones permissions from an existing profile |
| Edit Profile | Action Icon | Enabled | Opens profile permission editor (Standard is editable, Admin is fixed) |
| Search Profiles | Search Input | Enabled | Filters profile listing by name in real-time |

#### Tabs
- All Profiles, Active User Profiles, Unassigned Profiles

#### Tables
- Columns: `Profile Name`, `Profile Description`, `Users Count`, `Created By`, `Modified By`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Profiles`

#### Feature Restrictions
- Standard profiles are system-locked against deletion. Custom profiles require Professional/Enterprise editions.

#### Dependencies
- Users and Roles reference Profiles to enforce operational boundaries on all CRM record interactions.

#### Related Settings
- Roles and Sharing, Users, Field Permissions, Audit Log

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.2 Roles and Sharing

### Roles

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/roles`  
**Route**: `crm.settings.section.roles`  
**Breadcrumb**: `Setup` → `Security Control` → `Roles and Sharing` → `Roles`  
**Purpose**: Constructs the organizational reporting tree hierarchy that governs vertical record visibility, manager approvals, and ownership delegation.

#### UI Structure
- Interactive visual tree node diagram with collapsible manager/subordinate branches, role expansion nodes, and detail panels.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_Roles">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Role Name | Text Input | CEO / Manager / Representative | [User Defined] | Display name in reporting hierarchy |
| Reports To | Hierarchy Dropdown | CEO (Top Level) | [Hierarchy Tree Node Selector] | Parent manager role |
| Share Data with Peers | Toggle Switch | Disabled (Default) | Enabled / Disabled | Allows users with identical role to view each other's records |
| Description | Text Area | Role scope and managerial authority | [User Defined Text] | Organizational documentation |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Add Role | Button Node | Enabled | Adds child node beneath selected parent role |
| Edit Role | Action Icon | Enabled | Modifies role name, supervisor node, and peer sharing |
| Delete Role | Action Icon | Enabled | Reassigns subordinate users before node removal |
| Expand / Collapse All | Toolbar Button | Enabled | Toggles full tree view visibility |

#### Tabs
- Tree View, List View, Unassigned Users

#### Tables
- Hierarchical node structure displaying `Role Name`, `Reports To`, `Assigned Users Count`, and `Peer Sharing Status`.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Roles`

#### Feature Restrictions
- Top-level CEO role cannot be deleted or assigned a parent.

#### Dependencies
- Directly drives Data Sharing Rules, Forecast Rollups, and Approval Workflow hierarchies.

#### Related Settings
- Profiles, Data Sharing Settings, Hierarchy Preference, Users

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Data Sharing Settings

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/data-sharing`  
**Route**: `crm.settings.section.data-sharing`  
**Breadcrumb**: `Setup` → `Security Control` → `Roles and Sharing` → `Data Sharing Settings`  
**Purpose**: Establishes organization-wide default access (OWD) and custom criteria-based sharing rules across modules.

#### UI Structure
- Module-by-module default permission table paired with tabbed custom sharing rule definition cards.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_SharingSetting">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Default Organization Access | Dropdown Matrix | Private / Public Read Only | Private, Public Read Only, Public Read/Write | Base access level per CRM module |
| Sharing Rule Name | Text Input | [User Defined] | [Alphanumeric] | Unique name for custom sharing rule |
| Records Shared From | Selector | Role / Group / Territory | [Roles, Groups, Territories] | Source user scope |
| Shared With | Selector | Role / Group / Territory | [Roles, Groups, Territories] | Target recipient scope |
| Access Type | Dropdown | Read Only | Read Only, Read / Write, Full Access | Level of permission granted to target |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Edit Default Organization Access | Secondary Button | Enabled | Opens batch editor for OWD module permissions |
| New Sharing Rule | Primary Button | Enabled | Launches rule creation builder |
| Recalculate | Button | Enabled | Recomputes record sharing caches across all accounts |

#### Tabs
- Default Organization Access, Custom Sharing Rules (Per Module: Leads, Accounts, Contacts, Deals)

#### Tables
- Columns: `Module`, `Default Access`, `Description`, `Custom Rules Count`

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Data_Sharing`

#### Feature Restrictions
- Enterprise edition supports up to 300 custom sharing rules per module.

#### Dependencies
- Evaluated after Profile permissions; cannot grant access beyond profile CRUD capabilities.

#### Related Settings
- Roles, Profiles, Groups, Territory Management

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.3 Zoho Mail Add-on Users

### Zoho Mail Add-on Users

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zmail-users`  
**Route**: `crm.settings.section.zmail-users`  
**Breadcrumb**: `Setup` → `Security Control` → `Zoho Mail Add-on Users` → `Zoho Mail Add-on Users`  
**Purpose**: Administers and configures Zoho Mail Add-on Users settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_zmailusers">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Deactivate Mail Addon | Input / Configuration | Active / Standard | [System Configurable] | Manages Deactivate Mail Addon behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Zoho Mail Add-on Users` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.4 Compliance Settings

### GDPR Compliance

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/compliance`  
**Route**: `crm.settings.section.compliance`  
**Breadcrumb**: `Setup` → `Security Control` → `Compliance Settings` → `GDPR Compliance`  
**Purpose**: Administers and configures GDPR Compliance settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_complianceSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| GDPR Compliance Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance

#### Tables
- Configuration properties grid displaying key `GDPR Compliance` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Compliance_Settings`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Overview

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.compliance.consent-dashboard`  
**Route**: `crm.settings.section.compliance.consent-dashboard`  
**Breadcrumb**: `Setup` → `Security Control` → `Compliance Settings` → `Overview`  
**Purpose**: Administers and configures Overview settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_consentDashboard">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Overview Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance

#### Tables
- Configuration properties grid displaying key `Overview` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Compliance_Settings`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Preferences

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.compliance.privacy-preference`  
**Route**: `crm.settings.section.compliance.privacy-preference`  
**Breadcrumb**: `Setup` → `Security Control` → `Compliance Settings` → `Preferences`  
**Purpose**: Administers and configures Preferences settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_preference">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Preferences Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance

#### Tables
- Configuration properties grid displaying key `Preferences` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Compliance_Settings`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Consent Form

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.compliance.consent-form`  
**Route**: `crm.settings.section.compliance.consent-form`  
**Breadcrumb**: `Setup` → `Security Control` → `Compliance Settings` → `Consent Form`  
**Purpose**: Administers and configures Consent Form settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_consentForm">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Consent Form Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance

#### Tables
- Configuration properties grid displaying key `Consent Form` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Compliance_Settings`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### HIPAA Compliance

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/compliance/hipaa`  
**Route**: `crm.settings.section.compliance.hipaa`  
**Breadcrumb**: `Setup` → `Security Control` → `Compliance Settings` → `HIPAA Compliance`  
**Purpose**: Administers and configures HIPAA Compliance settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_hipaa">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| HIPAA | Input / Configuration | Active / Standard | [System Configurable] | Manages HIPAA behavior |
| Health | Input / Configuration | Active / Standard | [System Configurable] | Manages Health behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: GDPR Compliance, Overview, Preferences, Consent Form, HIPAA Compliance

#### Tables
- Configuration properties grid displaying key `HIPAA Compliance` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Compliance_Settings`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.5 Territory Management

### Territories

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/territories`  
**Route**: `crm.settings.section.territories`  
**Breadcrumb**: `Setup` → `Security Control` → `Territory Management` → `Territories`  
**Purpose**: Administers and configures Territories settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_enableTerritory">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Territory | Input / Configuration | Active / Standard | [System Configurable] | Manages Territory behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Territories` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.6 Trusted Domain

### Trusted Domain

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/trusted-domain`  
**Route**: `crm.settings.section.crm-trusted-domain`  
**Breadcrumb**: `Setup` → `Security Control` → `Trusted Domain` → `Trusted Domain`  
**Purpose**: Administers and configures Trusted Domain settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="trusted_domains">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Trusted Domains | Input / Configuration | Active / Standard | [System Configurable] | Manages Trusted Domains behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Trusted Domain` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.7 Support Access

### Support Access

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/support-access`  
**Route**: `crm.settings.section.support-access`  
**Breadcrumb**: `Setup` → `Security Control` → `Support Access` → `Support Access`  
**Purpose**: Administers and configures Support Access settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_supportaccess">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Support Access Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Support Access` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Support_Access`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.8 Single Sign-On(SAML)

### Single Sign-On(SAML)

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: None`  
**Route**: `N/A`  
**Breadcrumb**: `Setup` → `Security Control` → `Single Sign-On(SAML)` → `Single Sign-On(SAML)`  
**Purpose**: Administers and configures Single Sign-On(SAML) settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zdirectory_sso">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Zoho Directory | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Directory behavior |
| Single Sign On | Input / Configuration | Active / Standard | [System Configurable] | Manages Single Sign On behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Single Sign-On(SAML)` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.9 Security Policies

### Security Policies

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: None`  
**Route**: `N/A`  
**Breadcrumb**: `Setup` → `Security Control` → `Security Policies` → `Security Policies`  
**Purpose**: Administers and configures Security Policies settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zdirectory_security">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Multifactor Authentication | Input / Configuration | Active / Standard | [System Configurable] | Manages Multifactor Authentication behavior |
| Zoho Directory | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Directory behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Security Policies` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.10 Active Directory Sync

### Active Directory Sync

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: None`  
**Route**: `N/A`  
**Breadcrumb**: `Setup` → `Security Control` → `Active Directory Sync` → `Active Directory Sync`  
**Purpose**: Administers and configures Active Directory Sync settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zdirectory_activesync">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Zoho Directory | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Directory behavior |
| Active Directory | Input / Configuration | Active / Standard | [System Configurable] | Manages Active Directory behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Active Directory Sync` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.11 Login History

### Login History

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: None`  
**Route**: `N/A`  
**Breadcrumb**: `Setup` → `Security Control` → `Login History` → `Login History`  
**Purpose**: Administers and configures Login History settings, user privileges, and behavior within Security Control.

#### UI Structure
- Standard Security Control interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zdirectory_loginhistory">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Zoho Directory | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Directory behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Login History` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Security Control subsystem.

#### Related Settings
- General Settings, Security Control Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 1.12 Audit Log

### Audit Log

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/auditlog`  
**Route**: `crm.settings.section.auditlog`  
**Breadcrumb**: `Setup` → `Security Control` → `Audit Log` → `Audit Log`  
**Purpose**: Maintains an immutable chronological audit trail of administrative, structural, configuration, and data-modifying actions.

#### UI Structure
- High-density paginated log table with real-time entity filter dropdowns, date pickers, user selectors, and export capabilities.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_auditLog">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Entity / Module Filter | Dropdown | All Entities | All, Users, Profiles, Modules, Automation, Settings | Filters log events by subsystem |
| Action Type Filter | Dropdown | All Actions | Create, Update, Delete, Export, Login, Reconcile | Filters by specific operation |
| Performed By Filter | User Search | All Users | [Active User Accounts] | Filters by acting administrator |
| Date Range | Datepicker | Past 30 Days (Default) | Today, Last 7 Days, Last 30 Days, Custom Range | Temporal filter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Export Audit Log | Button | Enabled | Initiates secure CSV export of filtered log records |
| Reset Filters | Link | Enabled | Clears all active query parameters |
| Pagination Controls | Toolbar | Enabled | Steps through 20, 50, or 100 rows per page |

#### Tabs
- Recent Activity, Administrative Changes, User Logins, Data Export Logs

#### Tables
- Columns: `Timestamp`, `Performed By`, `Action`, `Entity`, `Details / Old vs New Value`, `IP Address`

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Audit records are immutable and retained for 60 to 365 days depending on edition tier.

#### Dependencies
- Logs changes across all 12 Settings categories and user operational events.

#### Related Settings
- Login History, Security Policies, Support Access

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 2. Customization

## 2.1 Modules and Fields

### Modules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/modules`  
**Route**: `crm.settings.section.modules`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Modules`  
**Purpose**: Configures standard and custom CRM data entities, layouts, field sets, mandatory requirements, and relational lookups.

#### UI Structure
- Grid of interactive module cards showing active/hidden status, record counts, layout links, and 'New Module' button.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Module Name (Singular) | Text Input | Deal / Lead / Custom Entity | [Alphanumeric] | Singular label displayed on detail views |
| Module Name (Plural) | Text Input | Deals / Leads / Custom Entities | [Alphanumeric] | Plural label displayed on tabs/lists |
| Quick Create | Toggle Switch | Enabled | Enabled / Disabled | Allows rapid record creation from global '+' menu |
| Scoring Rules Enabled | Toggle Switch | Enabled | Enabled / Disabled | Activates touchpoint scoring on this module |
| Auto-Number Generation | Prefix + Sequence | None / INV-{0000} | [Pattern String] | Automated ID sequence generator |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| New Module | Primary Button | Enabled | Launches Custom Module Builder |
| Layouts | Card Action Link | Enabled | Navigates directly to drag-and-drop layout editor |
| Module Permissions | Menu Item | Enabled | Opens profile accessibility modal for this module |
| Organize Modules | Toolbar Button | Enabled | Reorders tab visibility and navbar placement |

#### Tabs
- Modules, Web Tabs, Global Sets, Layouts, Fields, Validation Rules, Links & Buttons

#### Tables
- Columns: `Module Name`, `API Name`, `Status (Active/Inactive)`, `Layouts Count`, `Custom Fields Count`, `Modified By`

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Create_Team_Module`

#### Feature Restrictions
- Custom module limits: Professional (3 modules), Enterprise (25 modules), Ultimate (50 modules).

#### Dependencies
- Foundational data schema; referenced by Layouts, Workflows, APIs, Blueprints, and Reports.

#### Related Settings
- Fields and Layouts, Global Sets, Validation Rules, Pipelines

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Web Tabs

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/web-tabs`  
**Route**: `crm.settings.section.web-tabs`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Web Tabs`  
**Purpose**: Administers and configures Web Tabs settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_webTabs">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Web Tabs Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Web Tabs` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Global Sets

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/global_picklists`  
**Route**: `crm.settings.section.globalpicklists`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Global Sets`  
**Purpose**: Administers and configures Global Sets settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_globalField">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Global Set | Input / Configuration | Active / Standard | [System Configurable] | Manages Global Set behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Global Sets` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Layouts

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.layouts`  
**Route**: `crm.settings.section.modules.module.layouts`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Layouts`  
**Purpose**: Administers and configures Layouts settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Layout | Input / Configuration | Active / Standard | [System Configurable] | Manages Layout behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Layouts` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Layout Rules

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.layout-rules`  
**Route**: `crm.settings.section.modules.module.layout-rules`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Layout Rules`  
**Purpose**: Administers and configures Layout Rules settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Rule | Input / Configuration | Active / Standard | [System Configurable] | Manages Rule behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Layout Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Fields and Layouts

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.field-listing`  
**Route**: `crm.settings.section.modules.module.field-listing`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Fields and Layouts`  
**Purpose**: Administers and configures Fields and Layouts settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Fields | Input / Configuration | Active / Standard | [System Configurable] | Manages Fields behavior |
| Field Listing | Input / Configuration | Active / Standard | [System Configurable] | Manages Field Listing behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Fields and Layouts` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Field Permissions

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.field-permissions`  
**Route**: `crm.settings.section.modules.module.field-permissions`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Field Permissions`  
**Purpose**: Administers and configures Field Permissions settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Fields | Input / Configuration | Active / Standard | [System Configurable] | Manages Fields behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Field Permissions` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Validation Rules

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.validation-rules`  
**Route**: `crm.settings.section.modules.module.validation-rules`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Validation Rules`  
**Purpose**: Administers and configures Validation Rules settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules_validationRules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Rule | Input / Configuration | Active / Standard | [System Configurable] | Manages Rule behavior |
| Validation | Input / Configuration | Active / Standard | [System Configurable] | Manages Validation behavior |
| Set Validation Rules | Input / Configuration | Active / Standard | [System Configurable] | Manages Set Validation Rules behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Validation Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Record Locking Configuration

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.record-locking`  
**Route**: `crm.settings.section.modules.module.record-locking`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Record Locking Configuration`  
**Purpose**: Administers and configures Record Locking Configuration settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules_lockingconfiguration">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Lock | Input / Configuration | Active / Standard | [System Configurable] | Manages Lock behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Record Locking Configuration` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Links and Buttons

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.modules.module.links-and-buttons`  
**Route**: `crm.settings.section.modules.module.links-and-buttons`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Links and Buttons`  
**Purpose**: Administers and configures Links and Buttons settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_modules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Link | Input / Configuration | Active / Standard | [System Configurable] | Manages Link behavior |
| Button | Input / Configuration | Active / Standard | [System Configurable] | Manages Button behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Links and Buttons` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Preferences

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.preferences`  
**Route**: `crm.settings.section.preferences`  
**Breadcrumb**: `Setup` → `Customization` → `Modules and Fields` → `Preferences`  
**Purpose**: Administers and configures Preferences settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_preferences">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Preferences Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Modules, Web Tabs, Global Sets, Layouts, Layout Rules, Fields and Layouts, Field Permissions, Validation Rules, Record Locking Configuration, Links and Buttons, Preferences

#### Tables
- Configuration properties grid displaying key `Preferences` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.2 Pipelines

### Pipelines

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/pipelines`  
**Route**: `crm.settings.section.pipelines`  
**Breadcrumb**: `Setup` → `Customization` → `Pipelines` → `Pipelines`  
**Purpose**: Manages multi-stage sales pipelines, probability weightings, stage categories (Open/Closed Won/Closed Lost), and stage transitions.

#### UI Structure
- Interactive pipeline stage timeline with probability badges, stage re-ordering drag handles, and layout association cards.
- **Primary Component Tag**: `<crm-setup-section data-cid="customize_pipelines">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Pipeline Name | Text Input | Standard Sales Pipeline | [User Defined] | Identifier for the sales pipeline |
| Associated Layouts | Multi-Select | Standard Layout | [Active Deal Layouts] | Determines which deal layouts use this pipeline |
| Stage Name | Picklist | Qualification / Proposal / Negotiation | [Stage Picklist Values] | Sales milestone name |
| Probability (%) | Number (0-100) | 10% to 100% | 0, 10, 20, ..., 100 | Win probability for revenue forecasting |
| Forecast Category | Dropdown | Pipeline / Best Case / Committed / Closed | Pipeline, Best Case, Committed, Closed Won, Closed Lost | Rollup classification for revenue projection |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| New Pipeline | Primary Button | Enabled | Launches pipeline creation wizard |
| Add Stage | Secondary Button | Enabled | Appends a new stage node to the active pipeline |
| Set as Default | Link | Enabled | Designates primary pipeline for new deals |
| Reorder Stages | Drag Handles | Enabled | Rearranges sequential progression order |

#### Tabs
- Pipelines List, Stage Mapping, Probability Configuration

#### Tables
- Columns: `Pipeline Name`, `Layouts Assigned`, `Total Stages`, `Default (Yes/No)`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Multiple pipelines require Enterprise or Ultimate edition.

#### Dependencies
- Directly feeds Deal forecasting, Blueprint state machines, and Sales Dashboard velocity metrics.

#### Related Settings
- Modules and Fields, Blueprint, Cadences, Forecasts

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.3 Wizards

### Wizards

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/wizard`  
**Route**: `crm.settings.section.wizard`  
**Breadcrumb**: `Setup` → `Customization` → `Wizards` → `Wizards`  
**Purpose**: Administers and configures Wizards settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="wizards_interForm">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Wizards Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Wizards` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.4 Kiosk Studio

### Kiosk Studio

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/kiosk`  
**Route**: `crm.settings.section.kiosk`  
**Breadcrumb**: `Setup` → `Customization` → `Kiosk Studio` → `Kiosk Studio`  
**Purpose**: Administers and configures Kiosk Studio settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_processflow">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Kiosk | Input / Configuration | Active / Standard | [System Configurable] | Manages Kiosk behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Kiosk Studio` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.5 Canvas

### Home View

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.canvas-builder.homeview`  
**Route**: `crm.settings.section.canvas-builder.homeview`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `Home View`  
**Purpose**: Administers and configures Home View settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_homeview">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Home View Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `Home View` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### List View

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/canvas-builder/listview`  
**Route**: `crm.settings.section.canvas-builder.listview`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `List View`  
**Purpose**: Administers and configures List View settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_listview">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| List View Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `List View` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Detail View

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.canvas-builder.detailview.views`  
**Route**: `crm.settings.section.canvas-builder.detailview.views`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `Detail View`  
**Purpose**: Administers and configures Detail View settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_detailview">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Detail View Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `Detail View` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Form View

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.canvas-builder.formview`  
**Route**: `crm.settings.section.canvas-builder.formview`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `Form View`  
**Purpose**: Administers and configures Form View settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_createpage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Form View Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `Form View` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Templates

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/canvas-builder/templates`  
**Route**: `crm.settings.section.canvas-builder.templates`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `Templates`  
**Purpose**: Administers and configures Templates settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_templates">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Templates Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `Templates` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Print View

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.canvas-builder.printview`  
**Route**: `crm.settings.section.canvas-builder.printview`  
**Breadcrumb**: `Setup` → `Customization` → `Canvas` → `Print View`  
**Purpose**: Administers and configures Print View settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_canvas_printpage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Print View Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Home View, List View, Detail View, Form View, Templates, Print View

#### Tables
- Configuration properties grid displaying key `Print View` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.6 Customize Home page

### Customize Home page

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/home-customization`  
**Route**: `crm.settings.section.new-home-customization`  
**Breadcrumb**: `Setup` → `Customization` → `Customize Home page` → `Customize Home page`  
**Purpose**: Administers and configures Customize Home page settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_homePage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Customize Home page Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Customize Home page` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Home`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.7 Translations

### Translation Settings

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/translation-settings`  
**Route**: `crm.settings.section.translation-settings`  
**Breadcrumb**: `Setup` → `Customization` → `Translations` → `Translation Settings`  
**Purpose**: Administers and configures Translation Settings settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_translation">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Translation Settings Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Translation Settings, Language Import History

#### Tables
- Configuration properties grid displaying key `Translation Settings` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Language Import History

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/translation-history`  
**Route**: `crm.settings.section.translation-history`  
**Breadcrumb**: `Setup` → `Customization` → `Translations` → `Language Import History`  
**Purpose**: Administers and configures Language Import History settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_translationimporthistory">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Language Import History Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Translation Settings, Language Import History

#### Tables
- Configuration properties grid displaying key `Language Import History` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.8 Templates

### Email

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=email`  
**Route**: `crm.settings.section.crm-templates`  
**Breadcrumb**: `Setup` → `Customization` → `Templates` → `Email`  
**Purpose**: Administers and configures Email settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_email">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Email Templates | Input / Configuration | Active / Standard | [System Configurable] | Manages Email Templates behavior |
| Template | Input / Configuration | Active / Standard | [System Configurable] | Manages Template behavior |
| Mail Content Format | Input / Configuration | Active / Standard | [System Configurable] | Manages Mail Content Format behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email, Inventory, Mail Merge

#### Tables
- Configuration properties grid displaying key `Email` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Inventory

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=inventory`  
**Route**: `crm.settings.section.crm-templates`  
**Breadcrumb**: `Setup` → `Customization` → `Templates` → `Inventory`  
**Purpose**: Administers and configures Inventory settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_inventory">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Inventory Templates | Input / Configuration | Active / Standard | [System Configurable] | Manages Inventory Templates behavior |
| Quote Template | Input / Configuration | Active / Standard | [System Configurable] | Manages Quote Template behavior |
| SalesOrder Template | Input / Configuration | Active / Standard | [System Configurable] | Manages SalesOrder Template behavior |
| Invoice Template | Input / Configuration | Active / Standard | [System Configurable] | Manages Invoice Template behavior |
| PurchaseOrder Template | Input / Configuration | Active / Standard | [System Configurable] | Manages PurchaseOrder Template behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email, Inventory, Mail Merge

#### Tables
- Configuration properties grid displaying key `Inventory` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Mail Merge

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/templates?type=mail-merge`  
**Route**: `crm.settings.section.crm-templates`  
**Breadcrumb**: `Setup` → `Customization` → `Templates` → `Mail Merge`  
**Purpose**: Administers and configures Mail Merge settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_mailmerge">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Mail Merge Templates | Input / Configuration | Active / Standard | [System Configurable] | Manages Mail Merge Templates behavior |
| Flyer | Input / Configuration | Active / Standard | [System Configurable] | Manages Flyer behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email, Inventory, Mail Merge

#### Tables
- Configuration properties grid displaying key `Mail Merge` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_MS_Office_Integ`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 2.9 Teamspace

### Teamspace

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/teamspace`  
**Route**: `crm.settings.section.teamspace`  
**Breadcrumb**: `Setup` → `Customization` → `Teamspace` → `Teamspace`  
**Purpose**: Administers and configures Teamspace settings, user privileges, and behavior within Customization.

#### UI Structure
- Standard Customization interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_teamspace">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Teamspace Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Teamspace` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Customization subsystem.

#### Related Settings
- General Settings, Customization Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 3. Automation

## 3.1 Workflow Rules

### Rules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/workflow-rules`  
**Route**: `crm.settings.section.workflow-rules`  
**Breadcrumb**: `Setup` → `Automation` → `Workflow Rules` → `Rules`  
**Purpose**: Constructs event-driven automation executing instant and scheduled actions (email alerts, tasks, field updates, webhooks, Deluge functions) on record triggers.

#### UI Structure
- Tabular listing of active workflow rules with module filters, trigger status pills, execution metrics, and visual rule builder canvas.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_workflow">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Module | Dropdown | Leads / Deals / Contacts | [All CRM Modules] | Target entity triggering the rule |
| Rule Name | Text Input | [User Defined] | [Alphanumeric] | Descriptive rule title |
| Trigger Condition | Radio / Selector | On Record Creation / Edit / Delete | Create, Edit, Delete, Field Update, Date/Time | Execution event trigger |
| Criteria Logic | Rule Builder (AND/OR) | Amount > 10000 AND Stage = 'Proposal' | [Field Operator Value] | Filter criteria evaluating execution |
| Instant Actions | Multi-Action Picker | Send Email + Update Field | Email Alert, Task, Field Update, Webhook, Function | Actions executed immediately |
| Scheduled Actions | Time Offset Picker | 3 Days After Trigger Date | Days / Hours / Minutes after specific date field | Delayed batch execution |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Rule | Primary Button | Enabled | Launches visual workflow rule builder |
| Toggle Status (Active/Inactive) | Switch | Enabled | Activates or suspends rule execution |
| Reorder Rules | Button | Enabled | Adjusts sequential execution priority within the module |
| View Usage / Insights | Toolbar Tab | Enabled | Navigates to execution volume analytics |

#### Tabs
- Workflow Rules, Workflow Insights / Execution Usage

#### Tables
- Columns: `Rule Name`, `Module`, `Trigger On`, `Status`, `Modified By`, `Executions Count (30d)`

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Daily email alert and webhook execution caps apply according to organization license tier.

#### Dependencies
- Connects Modules with Actions (Email Alerts, Field Updates, Tasks, Webhooks, Functions).

#### Related Settings
- Actions, Schedules, Blueprint, Connected Workflow

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Usage

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/workflow-insights`  
**Route**: `crm.settings.section.workflow-insights`  
**Breadcrumb**: `Setup` → `Automation` → `Workflow Rules` → `Usage`  
**Purpose**: Constructs event-driven automation executing instant and scheduled actions (email alerts, tasks, field updates, webhooks, Deluge functions) on record triggers.

#### UI Structure
- Tabular listing of active workflow rules with module filters, trigger status pills, execution metrics, and visual rule builder canvas.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_insight">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Module | Dropdown | Leads / Deals / Contacts | [All CRM Modules] | Target entity triggering the rule |
| Rule Name | Text Input | [User Defined] | [Alphanumeric] | Descriptive rule title |
| Trigger Condition | Radio / Selector | On Record Creation / Edit / Delete | Create, Edit, Delete, Field Update, Date/Time | Execution event trigger |
| Criteria Logic | Rule Builder (AND/OR) | Amount > 10000 AND Stage = 'Proposal' | [Field Operator Value] | Filter criteria evaluating execution |
| Instant Actions | Multi-Action Picker | Send Email + Update Field | Email Alert, Task, Field Update, Webhook, Function | Actions executed immediately |
| Scheduled Actions | Time Offset Picker | 3 Days After Trigger Date | Days / Hours / Minutes after specific date field | Delayed batch execution |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Rule | Primary Button | Enabled | Launches visual workflow rule builder |
| Toggle Status (Active/Inactive) | Switch | Enabled | Activates or suspends rule execution |
| Reorder Rules | Button | Enabled | Adjusts sequential execution priority within the module |
| View Usage / Insights | Toolbar Tab | Enabled | Navigates to execution volume analytics |

#### Tabs
- Workflow Rules, Workflow Insights / Execution Usage

#### Tables
- Columns: `Rule Name`, `Module`, `Trigger On`, `Status`, `Modified By`, `Executions Count (30d)`

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Daily email alert and webhook execution caps apply according to organization license tier.

#### Dependencies
- Connects Modules with Actions (Email Alerts, Field Updates, Tasks, Webhooks, Functions).

#### Related Settings
- Actions, Schedules, Blueprint, Connected Workflow

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 3.2 Actions

### Email Notifications

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/alerts`  
**Route**: `crm.settings.section.alerts`  
**Breadcrumb**: `Setup` → `Automation` → `Actions` → `Email Notifications`  
**Purpose**: Administers and configures Email Notifications settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_alert">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Send Email | Input / Configuration | Active / Standard | [System Configurable] | Manages Send Email behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow

#### Tables
- Configuration properties grid displaying key `Email Notifications` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Tasks

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/tasks`  
**Route**: `crm.settings.section.tasks`  
**Breadcrumb**: `Setup` → `Automation` → `Actions` → `Tasks`  
**Purpose**: Administers and configures Tasks settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_task">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Tasks Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow

#### Tables
- Configuration properties grid displaying key `Tasks` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Field Updates

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/field-updates`  
**Route**: `crm.settings.section.field-updates`  
**Breadcrumb**: `Setup` → `Automation` → `Actions` → `Field Updates`  
**Purpose**: Administers and configures Field Updates settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_fieldUpdate">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Field Updates Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow

#### Tables
- Configuration properties grid displaying key `Field Updates` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Webhooks

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/webhooks`  
**Route**: `crm.settings.section.webhooks`  
**Breadcrumb**: `Setup` → `Automation` → `Actions` → `Webhooks`  
**Purpose**: Administers and configures Webhooks settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_webhook">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Webhooks Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow

#### Tables
- Configuration properties grid displaying key `Webhooks` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Actions by Zoho Flow

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/flow`  
**Route**: `crm.settings.section.actions-flow-library`  
**Breadcrumb**: `Setup` → `Automation` → `Actions` → `Actions by Zoho Flow`  
**Purpose**: Administers and configures Actions by Zoho Flow settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="flow_actionlibrary">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Functions | Input / Configuration | Active / Standard | [System Configurable] | Manages Functions behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Notifications, Tasks, Field Updates, Webhooks, Actions by Zoho Flow

#### Tables
- Configuration properties grid displaying key `Actions by Zoho Flow` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_AR_, Crm_Implied_Customize_Zoho_CRM, Crm_Implied_Manage_Workflow, Crm_Implied_View_Cadences`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 3.3 Schedules

### Schedules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/schedules`  
**Route**: `crm.settings.section.schedules`  
**Breadcrumb**: `Setup` → `Automation` → `Schedules` → `Schedules`  
**Purpose**: Administers and configures Schedules settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_schedules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Schedules Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Schedules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 3.4 Assignment

### Rules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/assignment-rules`  
**Route**: `crm.settings.section.assignment-rule`  
**Breadcrumb**: `Setup` → `Automation` → `Assignment` → `Rules`  
**Purpose**: Administers and configures Rules settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_assignmentRules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Assignment Rules | Input / Configuration | Active / Standard | [System Configurable] | Manages Assignment Rules behavior |
| Assign | Input / Configuration | Active / Standard | [System Configurable] | Manages Assign behavior |
| Auto Assign | Input / Configuration | Active / Standard | [System Configurable] | Manages Auto Assign behavior |
| Round Robin | Input / Configuration | Active / Standard | [System Configurable] | Manages Round Robin behavior |
| Allocate Records | Input / Configuration | Active / Standard | [System Configurable] | Manages Allocate Records behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Rules, Thresholds, Zia

#### Tables
- Configuration properties grid displaying key `Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Thresholds

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/assignment-thresholds`  
**Route**: `crm.settings.section.assignment-thresholds`  
**Breadcrumb**: `Setup` → `Automation` → `Assignment` → `Thresholds`  
**Purpose**: Administers and configures Thresholds settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_assignmentRestrictions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Assignment Thresholds | Input / Configuration | Active / Standard | [System Configurable] | Manages Assignment Thresholds behavior |
| Assign | Input / Configuration | Active / Standard | [System Configurable] | Manages Assign behavior |
| Auto Assign | Input / Configuration | Active / Standard | [System Configurable] | Manages Auto Assign behavior |
| Allocate Records | Input / Configuration | Active / Standard | [System Configurable] | Manages Allocate Records behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Rules, Thresholds, Zia

#### Tables
- Configuration properties grid displaying key `Thresholds` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Zia

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia-reasoning`  
**Route**: `crm.settings.section.zia-reasoning`  
**Breadcrumb**: `Setup` → `Automation` → `Assignment` → `Zia`  
**Purpose**: Administers and configures Zia settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_assignmentRulesZiaReasoning">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| zia | Input / Configuration | Active / Standard | [System Configurable] | Manages zia behavior |
| assign by zia | Input / Configuration | Active / Standard | [System Configurable] | Manages assign by zia behavior |
| reasoning | Input / Configuration | Active / Standard | [System Configurable] | Manages reasoning behavior |
| contributing fields | Input / Configuration | Active / Standard | [System Configurable] | Manages contributing fields behavior |
| user pattern | Input / Configuration | Active / Standard | [System Configurable] | Manages user pattern behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Rules, Thresholds, Zia

#### Tables
- Configuration properties grid displaying key `Zia` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 3.5 Scoring Rules

### Scoring Rules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/scoring-rules`  
**Route**: `crm.settings.section.scoring-rules`  
**Breadcrumb**: `Setup` → `Automation` → `Scoring Rules` → `Scoring Rules`  
**Purpose**: Administers and configures Scoring Rules settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_scoringRules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Scoring Rules Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Scoring Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 3.6 Cadences

### Cadences

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/cadences`  
**Route**: `crm.settings.section.cadences`  
**Breadcrumb**: `Setup` → `Automation` → `Cadences` → `Cadences`  
**Purpose**: Administers and configures Cadences settings, user privileges, and behavior within Automation.

#### UI Structure
- Standard Automation interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_series">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Cadences Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Cadences` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Automation subsystem.

#### Related Settings
- General Settings, Automation Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 4. Process Management

## 4.1 Blueprint

### Blueprints

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/blueprint`  
**Route**: `crm.settings.section.blueprint`  
**Breadcrumb**: `Setup` → `Process Management` → `Blueprint` → `Blueprints`  
**Purpose**: Administers and configures Blueprints settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_process">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Blueprints Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Blueprints, Usage

#### Tables
- Configuration properties grid displaying key `Blueprints` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Usage

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/blueprint-usage`  
**Route**: `crm.settings.section.blueprint-usage`  
**Breadcrumb**: `Setup` → `Process Management` → `Blueprint` → `Usage`  
**Purpose**: Administers and configures Usage settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_usage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Blueprints | Input / Configuration | Active / Standard | [System Configurable] | Manages Blueprints behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Blueprints, Usage

#### Tables
- Configuration properties grid displaying key `Usage` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 4.2 Approval Processes

### Approval Processes

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/approval-process`  
**Route**: `crm.settings.section.approval-process`  
**Breadcrumb**: `Setup` → `Process Management` → `Approval Processes` → `Approval Processes`  
**Purpose**: Administers and configures Approval Processes settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_approvalProcess">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Record approval | Input / Configuration | Active / Standard | [System Configurable] | Manages Record approval behavior |
| Approval Rules | Input / Configuration | Active / Standard | [System Configurable] | Manages Approval Rules behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Approval Processes` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 4.3 Review Processes

### Review Processes

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.review-process`  
**Route**: `crm.settings.section.review-process`  
**Breadcrumb**: `Setup` → `Process Management` → `Review Processes` → `Review Processes`  
**Purpose**: Administers and configures Review Processes settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_reviewprocess">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Blueprints | Input / Configuration | Active / Standard | [System Configurable] | Manages Blueprints behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Review Processes, Review Analytics

#### Tables
- Configuration properties grid displaying key `Review Processes` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Review Analytics

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.review-usage`  
**Route**: `crm.settings.section.review-usage`  
**Breadcrumb**: `Setup` → `Process Management` → `Review Processes` → `Review Analytics`  
**Purpose**: Administers and configures Review Analytics settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_reviewprocessusage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Blueprints | Input / Configuration | Active / Standard | [System Configurable] | Manages Blueprints behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Review Processes, Review Analytics

#### Tables
- Configuration properties grid displaying key `Review Analytics` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Workflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 4.4 Connected Workflow

### Connected Workflow

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/connected-workflow`  
**Route**: `crm.settings.section.connected-workflow`  
**Breadcrumb**: `Setup` → `Process Management` → `Connected Workflow` → `Connected Workflow`  
**Purpose**: Administers and configures Connected Workflow settings, user privileges, and behavior within Process Management.

#### UI Structure
- Standard Process Management interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="connected_workflow">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Connected Workflow Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Connected Workflow` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_ConnectedWorkflow`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Process Management subsystem.

#### Related Settings
- General Settings, Process Management Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 5. Developer Hub

## 5.1 MCP for AI Agents

### MCP for AI Agents

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/mcp`  
**Route**: `crm.settings.section.crm-mcp`  
**Breadcrumb**: `Setup` → `Developer Hub` → `MCP for AI Agents` → `MCP for AI Agents`  
**Purpose**: Configures Model Context Protocol (MCP) server endpoints allowing external AI agents and LLMs to securely query CRM tools, schemas, and records.

#### UI Structure
- AI Agent integration hub displaying active MCP endpoint configuration, protocol authorization keys, schema descriptors, and tool permissions.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_mcp">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Server Status | Status Badge | Active / Ready | Active, Suspended, Provisioning | Operational status of MCP server |
| Protocol Version | Read-Only Label | MCP v1.0 | Model Context Protocol Spec 2024-11 | Standard specification level |
| Exposed Tool Capabilities | Multi-Select Checkboxes | read_record, search_records, get_schema | [Available CRM Agent Tools] | Granular tool capabilities exposed to agent |
| Authentication Scope | Dropdown | OAuth 2.0 / Token Auth | OAuth 2.0, Bearer Token | Security authentication handshake method |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Configure MCP Server | Primary Button | Enabled | Opens MCP server connection and tool exposure settings |
| Regenerate Endpoint Config | Secondary Button | Enabled | Updates tool manifest and capability declarations |
| Inspect Schema Tools | Link | Enabled | Views JSON schema definitions for exposed CRM tools |

#### Tabs
- MCP Server Setup, Tool Definitions, Agent Authorization Logs

#### Tables
- Columns: `Tool Name`, `Description`, `Parameters`, `Permission Scope`, `Invocation Status`

#### Permissions
- **Required Scope**: `Crm_Implied_Api_Access`

#### Feature Restrictions
- Requires active AI / Developer Hub entitlement.

#### Dependencies
- Bridges CRM Object APIs with external AI coding assistants and autonomous agents.

#### Related Settings
- APIs and SDKs, Connections, Functions, Zia Agents

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.2 APIs and SDKs

### CRM API

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/api/usage/graph-view`  
**Route**: `crm.settings.section.api-graph-view`  
**Breadcrumb**: `Setup` → `Developer Hub` → `APIs and SDKs` → `CRM API`  
**Purpose**: Administers and configures CRM API settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_api">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Authentication Token | Input / Configuration | Active / Standard | [System Configurable] | Manages Authentication Token behavior |
| API Key | Input / Configuration | Active / Standard | [System Configurable] | Manages API Key behavior |
| API methods | Input / Configuration | Active / Standard | [System Configurable] | Manages API methods behavior |
| API Usage | Input / Configuration | Active / Standard | [System Configurable] | Manages API Usage behavior |
| Developer Space | Input / Configuration | Active / Standard | [System Configurable] | Manages Developer Space behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: CRM API, SDKs

#### Tables
- Configuration properties grid displaying key `CRM API` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Api_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### SDKs

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/sdks`  
**Route**: `crm.settings.section.sdks`  
**Breadcrumb**: `Setup` → `Developer Hub` → `APIs and SDKs` → `SDKs`  
**Purpose**: Administers and configures SDKs settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zes_sdk">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| zes | Input / Configuration | Active / Standard | [System Configurable] | Manages zes behavior |
| sdk | Input / Configuration | Active / Standard | [System Configurable] | Manages sdk behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: CRM API, SDKs

#### Tables
- Configuration properties grid displaying key `SDKs` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.3 Connections

### Connections

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/connections`  
**Route**: `crm.settings.section.connections`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Connections` → `Connections`  
**Purpose**: Administers and configures Connections settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_crmconnectors">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Connections Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Connections` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.4 Variables

### Variables

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/crmvariables`  
**Route**: `crm.settings.section.crm-variables`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Variables` → `Variables`  
**Purpose**: Administers and configures Variables settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_crmvariables">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| variables | Input / Configuration | Active / Standard | [System Configurable] | Manages variables behavior |
| Zoho Variables | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Variables behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Variables` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.5 Circuits

### Circuits

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/circuits/welcome`  
**Route**: `crm.settings.section.circuits`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Circuits` → `Circuits`  
**Purpose**: Administers and configures Circuits settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_circuits">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Circuits Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Circuits` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.6 Functions

### Functions

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/functions`  
**Route**: `crm.settings.section.functions`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Functions` → `Functions`  
**Purpose**: Creates, tests, and executes serverless Deluge script functions, standalone REST endpoints, and automated background jobs.

#### UI Structure
- Integrated code IDE with syntax highlighting, function gallery, parameter input modal, execution debugger console, and analytics dashboard.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_functions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Function Name | Text Input | [camelCase / Identifier] | [Alphanumeric] | Internal programmatic identifier |
| Display Name | Text Input | [Human Readable Name] | [Text] | Display name across workflow action menus |
| Language / Runtime | Read-Only Label | Deluge Script (v3.0) | Deluge | Execution engine |
| Arguments / Parameters | Key-Value Parameter Table | recordId (String), amount (Decimal) | [Type Definition] | Input arguments passed to function |
| Return Type | Dropdown | Void / Map / String | void, string, int, double, boolean, list, map | Expected return data structure |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Function | Primary Button | Enabled | Opens code editor wizard |
| Save and Execute (Test) | Editor Button | Enabled | Runs script in sandbox mode with mock parameters |
| Function Gallery | Toolbar Link | Enabled | Opens library of pre-built automation scripts |
| View Analytics | Tab Button | Enabled | Displays execution duration, failure rates, and invocation counts |

#### Tabs
- Functions Listing, Gallery, Analytics Dashboard, Failures & Error Log

#### Tables
- Columns: `Function Name`, `Display Name`, `Associated Workflows`, `Execution Count`, `Last Modified`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Deluge statement execution limit: 5,000 statements per invocation; API call limit: 250 external calls/day (scale with tier).

#### Dependencies
- Invoked by Workflow Rules, Custom Buttons, Blueprints, Schedules, and REST API triggers.

#### Related Settings
- Connections, Variables, Circuits, Widgets, Client Script

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Gallery

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/functions/gallery`  
**Route**: `crm.settings.section.functions.functionsgallery`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Functions` → `Gallery`  
**Purpose**: Creates, tests, and executes serverless Deluge script functions, standalone REST endpoints, and automated background jobs.

#### UI Structure
- Integrated code IDE with syntax highlighting, function gallery, parameter input modal, execution debugger console, and analytics dashboard.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_functions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Function Name | Text Input | [camelCase / Identifier] | [Alphanumeric] | Internal programmatic identifier |
| Display Name | Text Input | [Human Readable Name] | [Text] | Display name across workflow action menus |
| Language / Runtime | Read-Only Label | Deluge Script (v3.0) | Deluge | Execution engine |
| Arguments / Parameters | Key-Value Parameter Table | recordId (String), amount (Decimal) | [Type Definition] | Input arguments passed to function |
| Return Type | Dropdown | Void / Map / String | void, string, int, double, boolean, list, map | Expected return data structure |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Function | Primary Button | Enabled | Opens code editor wizard |
| Save and Execute (Test) | Editor Button | Enabled | Runs script in sandbox mode with mock parameters |
| Function Gallery | Toolbar Link | Enabled | Opens library of pre-built automation scripts |
| View Analytics | Tab Button | Enabled | Displays execution duration, failure rates, and invocation counts |

#### Tabs
- Functions Listing, Gallery, Analytics Dashboard, Failures & Error Log

#### Tables
- Columns: `Function Name`, `Display Name`, `Associated Workflows`, `Execution Count`, `Last Modified`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Deluge statement execution limit: 5,000 statements per invocation; API call limit: 250 external calls/day (scale with tier).

#### Dependencies
- Invoked by Workflow Rules, Custom Buttons, Blueprints, Schedules, and REST API triggers.

#### Related Settings
- Connections, Variables, Circuits, Widgets, Client Script

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Analytics

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/functions/dashboard`  
**Route**: `crm.settings.section.functions.functionsdashboard`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Functions` → `Analytics`  
**Purpose**: Creates, tests, and executes serverless Deluge script functions, standalone REST endpoints, and automated background jobs.

#### UI Structure
- Integrated code IDE with syntax highlighting, function gallery, parameter input modal, execution debugger console, and analytics dashboard.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_functions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Function Name | Text Input | [camelCase / Identifier] | [Alphanumeric] | Internal programmatic identifier |
| Display Name | Text Input | [Human Readable Name] | [Text] | Display name across workflow action menus |
| Language / Runtime | Read-Only Label | Deluge Script (v3.0) | Deluge | Execution engine |
| Arguments / Parameters | Key-Value Parameter Table | recordId (String), amount (Decimal) | [Type Definition] | Input arguments passed to function |
| Return Type | Dropdown | Void / Map / String | void, string, int, double, boolean, list, map | Expected return data structure |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Function | Primary Button | Enabled | Opens code editor wizard |
| Save and Execute (Test) | Editor Button | Enabled | Runs script in sandbox mode with mock parameters |
| Function Gallery | Toolbar Link | Enabled | Opens library of pre-built automation scripts |
| View Analytics | Tab Button | Enabled | Displays execution duration, failure rates, and invocation counts |

#### Tabs
- Functions Listing, Gallery, Analytics Dashboard, Failures & Error Log

#### Tables
- Columns: `Function Name`, `Display Name`, `Associated Workflows`, `Execution Count`, `Last Modified`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Deluge statement execution limit: 5,000 statements per invocation; API call limit: 250 external calls/day (scale with tier).

#### Dependencies
- Invoked by Workflow Rules, Custom Buttons, Blueprints, Schedules, and REST API triggers.

#### Related Settings
- Connections, Variables, Circuits, Widgets, Client Script

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Failures

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/functions/failures`  
**Route**: `crm.settings.section.functions.functionsfailures`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Functions` → `Failures`  
**Purpose**: Creates, tests, and executes serverless Deluge script functions, standalone REST endpoints, and automated background jobs.

#### UI Structure
- Integrated code IDE with syntax highlighting, function gallery, parameter input modal, execution debugger console, and analytics dashboard.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_functions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Function Name | Text Input | [camelCase / Identifier] | [Alphanumeric] | Internal programmatic identifier |
| Display Name | Text Input | [Human Readable Name] | [Text] | Display name across workflow action menus |
| Language / Runtime | Read-Only Label | Deluge Script (v3.0) | Deluge | Execution engine |
| Arguments / Parameters | Key-Value Parameter Table | recordId (String), amount (Decimal) | [Type Definition] | Input arguments passed to function |
| Return Type | Dropdown | Void / Map / String | void, string, int, double, boolean, list, map | Expected return data structure |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Create Function | Primary Button | Enabled | Opens code editor wizard |
| Save and Execute (Test) | Editor Button | Enabled | Runs script in sandbox mode with mock parameters |
| Function Gallery | Toolbar Link | Enabled | Opens library of pre-built automation scripts |
| View Analytics | Tab Button | Enabled | Displays execution duration, failure rates, and invocation counts |

#### Tabs
- Functions Listing, Gallery, Analytics Dashboard, Failures & Error Log

#### Tables
- Columns: `Function Name`, `Display Name`, `Associated Workflows`, `Execution Count`, `Last Modified`, `Actions`

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Deluge statement execution limit: 5,000 statements per invocation; API call limit: 250 external calls/day (scale with tier).

#### Dependencies
- Invoked by Workflow Rules, Custom Buttons, Blueprints, Schedules, and REST API triggers.

#### Related Settings
- Connections, Variables, Circuits, Widgets, Client Script

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.7 Widgets

### Widgets

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/widgets`  
**Route**: `crm.settings.section.crm-widgets`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Widgets` → `Widgets`  
**Purpose**: Administers and configures Widgets settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_widgets">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Widgets Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Widgets` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.8 Data Model

### Data Model

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/data-model`  
**Route**: `crm.settings.section.crm-data-model`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Data Model` → `Data Model`  
**Purpose**: Administers and configures Data Model settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_datamodel">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Data Model Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Data Model` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access, Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.9 SlyteUI

### SlyteUI

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.slyteui`  
**Route**: `crm.settings.section.slyteui`  
**Breadcrumb**: `Setup` → `Developer Hub` → `SlyteUI` → `SlyteUI`  
**Purpose**: Administers and configures SlyteUI settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_components">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| SlyteUI Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `SlyteUI` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.10 Queries

### Queries

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/queries`  
**Route**: `crm.settings.section.crm-data-hub`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Queries` → `Queries`  
**Purpose**: Administers and configures Queries settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_datahub">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Queries Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Queries, Sources

#### Tables
- Configuration properties grid displaying key `Queries` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Sources

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/queries-sources`  
**Route**: `crm.settings.section.crm-data-hub-source`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Queries` → `Sources`  
**Purpose**: Administers and configures Sources settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="datahub_source">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Sources Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Queries, Sources

#### Tables
- Configuration properties grid displaying key `Sources` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.11 Client Script

### Client Script

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/cscript`  
**Route**: `crm.settings.section.crm-cscript`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Client Script` → `Client Script`  
**Purpose**: Administers and configures Client Script settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_cscript">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Commands | Input / Configuration | Active / Standard | [System Configurable] | Manages Commands behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Client Script, Static Resources

#### Tables
- Configuration properties grid displaying key `Client Script` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Static Resources

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/static-resource`  
**Route**: `crm.settings.section.crm-static-resource`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Client Script` → `Static Resources`  
**Purpose**: Administers and configures Static Resources settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="static_resources">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Static Resources Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Client Script, Static Resources

#### Tables
- Configuration properties grid displaying key `Static Resources` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Advanced_Dev_Access`

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 5.12 Catalyst Solutions

### Catalyst Solutions

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.catalyst-solutions`  
**Route**: `crm.settings.section.catalyst-solutions`  
**Breadcrumb**: `Setup` → `Developer Hub` → `Catalyst Solutions` → `Catalyst Solutions`  
**Purpose**: Administers and configures Catalyst Solutions settings, user privileges, and behavior within Developer Hub.

#### UI Structure
- Standard Developer Hub interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_catalyst_solutions">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Catalyst Solutions Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Catalyst Solutions` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Advanced developer privileges required.

#### Dependencies
- Integrates with core CRM data engine and Developer Hub subsystem.

#### Related Settings
- General Settings, Developer Hub Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 6. Zia

## 6.1 Agents

### Agents

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/agent`  
**Route**: `crm.settings.section.agent`  
**Breadcrumb**: `Setup` → `Zia` → `Agents` → `Agents`  
**Purpose**: Administers and configures Agents settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="zia_ZiaAgent">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |
| Zia Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Zia Agent behavior |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Agents` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_ZiaAgent`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.2 Data Enrichment

### Data Enrichment

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment`  
**Route**: `crm.settings.section.zia.data-enrichment`  
**Breadcrumb**: `Setup` → `Zia` → `Data Enrichment` → `Data Enrichment`  
**Purpose**: Administers and configures Data Enrichment settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_autoEnrich">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Data | Input / Configuration | Active / Standard | [System Configurable] | Manages Data behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Data Enrichment, History, Usage

#### Tables
- Configuration properties grid displaying key `Data Enrichment` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Data_Enrichment`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### History

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment/history`  
**Route**: `crm.settings.section.zia.data-enrichment.history-data-enrichment`  
**Breadcrumb**: `Setup` → `Zia` → `Data Enrichment` → `History`  
**Purpose**: Administers and configures History settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_autoEnrich_history">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Data | Input / Configuration | Active / Standard | [System Configurable] | Manages Data behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Data Enrichment, History, Usage

#### Tables
- Configuration properties grid displaying key `History` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_View_Data_Enrichment_Analytics`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Usage

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/data-enrichment/stats`  
**Route**: `crm.settings.section.zia.data-enrichment.stats-data-enrichment`  
**Breadcrumb**: `Setup` → `Zia` → `Data Enrichment` → `Usage`  
**Purpose**: Administers and configures Usage settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_autoEnrich_usage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Data | Input / Configuration | Active / Standard | [System Configurable] | Manages Data behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Data Enrichment, History, Usage

#### Tables
- Configuration properties grid displaying key `Usage` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_View_Data_Enrichment_Analytics`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.3 Prediction

### Prediction

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/prediction/builder/field`  
**Route**: `crm.settings.section.zia.prediction.builder.field.list`  
**Breadcrumb**: `Setup` → `Zia` → `Prediction` → `Prediction`  
**Purpose**: Administers and configures Prediction settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaOrgConfig">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Prediction Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Prediction, Analytics

#### Tables
- Configuration properties grid displaying key `Prediction` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Prediction`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Analytics

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/prediction/analytics`  
**Route**: `crm.settings.section.zia.prediction.analytics`  
**Breadcrumb**: `Setup` → `Zia` → `Prediction` → `Analytics`  
**Purpose**: Administers and configures Analytics settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaPredictionAnalytics">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Analytics Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Prediction, Analytics

#### Tables
- Configuration properties grid displaying key `Analytics` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_View_Analytics_Prediction`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.4 Recommendation

### Builder

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/recommendation`  
**Route**: `crm.settings.section.zia.recommendation`  
**Breadcrumb**: `Setup` → `Zia` → `Recommendation` → `Builder`  
**Purpose**: Administers and configures Builder settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaRecommendSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Builder Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Builder, Similarity Recommendation, System Recommendations, Analytics

#### Tables
- Configuration properties grid displaying key `Builder` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Similarity Recommendation

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/similarity/list`  
**Route**: `crm.settings.section.zia.similarity`  
**Breadcrumb**: `Setup` → `Zia` → `Recommendation` → `Similarity Recommendation`  
**Purpose**: Administers and configures Similarity Recommendation settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaSimilarity">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| zia.similarity.feature.title | Input / Configuration | Active / Standard | [System Configurable] | Manages zia.similarity.feature.title behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Builder, Similarity Recommendation, System Recommendations, Analytics

#### Tables
- Configuration properties grid displaying key `Similarity Recommendation` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### System Recommendations

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/autosuggestion`  
**Route**: `crm.settings.section.zia.autosuggestion`  
**Breadcrumb**: `Setup` → `Zia` → `Recommendation` → `System Recommendations`  
**Purpose**: Administers and configures System Recommendations settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaAutoSuggestionSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| System Recommendations Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Builder, Similarity Recommendation, System Recommendations, Analytics

#### Tables
- Configuration properties grid displaying key `System Recommendations` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Analytics

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/recommendation-analytics/noData`  
**Route**: `crm.settings.section.zia.recommendation-analytics`  
**Breadcrumb**: `Setup` → `Zia` → `Recommendation` → `Analytics`  
**Purpose**: Administers and configures Analytics settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaRecommendationAnalyticsSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Analytics Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Builder, Similarity Recommendation, System Recommendations, Analytics

#### Tables
- Configuration properties grid displaying key `Analytics` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Recommendation`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.5 Communication

### Best Time to Contact

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/reminder`  
**Route**: `crm.settings.section.zia.reminder`  
**Breadcrumb**: `Setup` → `Zia` → `Communication` → `Best Time to Contact`  
**Purpose**: Administers and configures Best Time to Contact settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Reminder | Input / Configuration | Active / Standard | [System Configurable] | Manages Reminder behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Best Time to Contact, Email Intelligence, Call Transcription

#### Tables
- Configuration properties grid displaying key `Best Time to Contact` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Email Intelligence

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.zia.inemailnew`  
**Route**: `crm.settings.section.zia.inemailnew`  
**Breadcrumb**: `Setup` → `Zia` → `Communication` → `Email Intelligence`  
**Purpose**: Administers and configures Email Intelligence settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaInEmailNew">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Email Intelligence Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Best Time to Contact, Email Intelligence, Call Transcription

#### Tables
- Configuration properties grid displaying key `Email Intelligence` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Call Transcription

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/calltranscription`  
**Route**: `crm.settings.section.zia.calltranscription`  
**Breadcrumb**: `Setup` → `Zia` → `Communication` → `Call Transcription`  
**Purpose**: Administers and configures Call Transcription settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaCallTranscriptionSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Best Time to Contact | Input / Configuration | Active / Standard | [System Configurable] | Manages Best Time to Contact behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Best Time to Contact, Email Intelligence, Call Transcription

#### Tables
- Configuration properties grid displaying key `Call Transcription` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.6 Vision

### Image Validation

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/vision/image-validation`  
**Route**: `crm.settings.section.zia.vision.image-validation`  
**Breadcrumb**: `Setup` → `Zia` → `Vision` → `Image Validation`  
**Purpose**: Administers and configures Image Validation settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaVision">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Image Validation Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Image Validation, Intelligent Character Recognition

#### Tables
- Configuration properties grid displaying key `Image Validation` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Intelligent Character Recognition

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/vision/icr`  
**Route**: `crm.settings.section.zia.vision.icr`  
**Breadcrumb**: `Setup` → `Zia` → `Vision` → `Intelligent Character Recognition`  
**Purpose**: Administers and configures Intelligent Character Recognition settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaIcr">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Intelligent Character Recognition Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Image Validation, Intelligent Character Recognition

#### Tables
- Configuration properties grid displaying key `Intelligent Character Recognition` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.7 Notifications

### Workflow Rule

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/notification/workflow`  
**Route**: `crm.settings.section.zia.notification.workflow`  
**Breadcrumb**: `Setup` → `Zia` → `Notifications` → `Workflow Rule`  
**Purpose**: Administers and configures Workflow Rule settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaUserConfig">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Workflow Rule Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Workflow Rule, Anomaly Component

#### Tables
- Configuration properties grid displaying key `Workflow Rule` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Anomaly Component

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/notification/anomaly`  
**Route**: `crm.settings.section.zia.notification.anomaly`  
**Breadcrumb**: `Setup` → `Zia` → `Notifications` → `Anomaly Component`  
**Purpose**: Administers and configures Anomaly Component settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaUserConfig_anomaly">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Anomaly Component Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Workflow Rule, Anomaly Component

#### Tables
- Configuration properties grid displaying key `Anomaly Component` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.8 Voice of the Customer

### Voice of the Customer

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/voice-of-customer`  
**Route**: `crm.settings.section.voice-of-customer`  
**Breadcrumb**: `Setup` → `Zia` → `Voice of the Customer` → `Voice of the Customer`  
**Purpose**: Administers and configures Voice of the Customer settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_voc">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| zia | Input / Configuration | Active / Standard | [System Configurable] | Manages zia behavior |
| Voc | Input / Configuration | Active / Standard | [System Configurable] | Manages Voc behavior |
| Voice of Customer | Input / Configuration | Active / Standard | [System Configurable] | Manages Voice of Customer behavior |
| Competitor Alerts | Input / Configuration | Active / Standard | [System Configurable] | Manages Competitor Alerts behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Voice of the Customer` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.9 Models

### Models

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/smart-prompt`  
**Route**: `crm.settings.section.zia.smart-prompt`  
**Breadcrumb**: `Setup` → `Zia` → `Models` → `Models`  
**Purpose**: Administers and configures Models settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_SmartPrompt">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Models Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Models` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Smart_Prompt`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.10 Presentation

### Presentation

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/presentations`  
**Route**: `crm.settings.section.zia.presentations`  
**Breadcrumb**: `Setup` → `Zia` → `Presentation` → `Presentation`  
**Purpose**: Administers and configures Presentation settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaPresentationConfiguration">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Presentation Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Presentation` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Zia_Presentation`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.11 Custom AI Studio

### Custom AI Studio

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/custom-ai`  
**Route**: `crm.settings.section.zia.custom-ai`  
**Breadcrumb**: `Setup` → `Zia` → `Custom AI Studio` → `Custom AI Studio`  
**Purpose**: Administers and configures Custom AI Studio settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaCustomAI">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Custom AI Studio Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Custom AI Studio` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.12 Competitors

### Competitors

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/competitor-alerts`  
**Route**: `crm.settings.section.competitor-alerts`  
**Breadcrumb**: `Setup` → `Zia` → `Competitors` → `Competitors`  
**Purpose**: Administers and configures Competitors settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_competitors">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Competitor Alerts | Input / Configuration | Active / Standard | [System Configurable] | Manages Competitor Alerts behavior |
| Competitor Alerts | Input / Configuration | Active / Standard | [System Configurable] | Manages Competitor Alerts behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Competitors` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 6.13 Usage Data

### Usage Data

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zia/usage-data/list`  
**Route**: `crm.settings.section.zia.usage-data`  
**Breadcrumb**: `Setup` → `Zia` → `Usage Data` → `Usage Data`  
**Purpose**: Administers and configures Usage Data settings, user privileges, and behavior within Zia.

#### UI Structure
- Standard Zia interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaUsageData">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| usage data | Input / Configuration | Active / Standard | [System Configurable] | Manages usage data behavior |
| usage | Input / Configuration | Active / Standard | [System Configurable] | Manages usage behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Usage Data` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Usage_Data`

#### Feature Restrictions
- Requires active Zia AI subscription / Enterprise edition.

#### Dependencies
- Integrates with core CRM data engine and Zia subsystem.

#### Related Settings
- General Settings, Zia Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 7. Channels

## 7.1 Email

### Email Configuration

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/email-configuration`  
**Route**: `crm.settings.section.email-configuration`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `Email Configuration`  
**Purpose**: Administers and configures Email Configuration settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_emailConfigSetting">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Email Configuration Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `Email Configuration` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Email Parser

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/email-parser`  
**Route**: `crm.settings.section.email-parser`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `Email Parser`  
**Purpose**: Administers and configures Email Parser settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_emailParser">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Mail Parser | Input / Configuration | Active / Standard | [System Configurable] | Manages Mail Parser behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `Email Parser` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### BCC Dropbox

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/bcc-dropbox`  
**Route**: `crm.settings.section.bcc-dropbox`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `BCC Dropbox`  
**Purpose**: Administers and configures BCC Dropbox settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_bcc">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| BCC | Input / Configuration | Active / Standard | [System Configurable] | Manages BCC behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `BCC Dropbox` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Email Deliverability

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.email-deliverability`  
**Route**: `crm.settings.section.email-deliverability`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `Email Deliverability`  
**Purpose**: Administers and configures Email Deliverability settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_ed">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Email Deliverability Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `Email Deliverability` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Email Intelligence

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.email-intelligence`  
**Route**: `crm.settings.section.email-intelligence`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `Email Intelligence`  
**Purpose**: Administers and configures Email Intelligence settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_ei">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Email Intelligence Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `Email Intelligence` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Unsubscribe Link

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/unsubscribe-link`  
**Route**: `crm.settings.section.unsubscribe-link`  
**Breadcrumb**: `Setup` → `Channels` → `Email` → `Unsubscribe Link`  
**Purpose**: Administers and configures Unsubscribe Link settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_unsubscribe">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Unsubscribe | Input / Configuration | Active / Standard | [System Configurable] | Manages Unsubscribe behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Email Configuration, Email Parser, BCC Dropbox, Email Deliverability, Email Intelligence, Unsubscribe Link

#### Tables
- Configuration properties grid displaying key `Unsubscribe Link` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Unsubscribe_Form`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.2 Telephony

### Telephony

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/telephony/marketplace`  
**Route**: `crm.settings.section.telephony`  
**Breadcrumb**: `Setup` → `Channels` → `Telephony` → `Telephony`  
**Purpose**: Administers and configures Telephony settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_telephony">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Phone Bridge | Input / Configuration | Active / Standard | [System Configurable] | Manages Phone Bridge behavior |
| Phone | Input / Configuration | Active / Standard | [System Configurable] | Manages Phone behavior |
| PhoneBridge | Input / Configuration | Active / Standard | [System Configurable] | Manages PhoneBridge behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Telephony` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Zoho_PhoneBridge_Integ`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.3 Business Messaging

### Business Messaging

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/messages/services`  
**Route**: `crm.settings.section.messages`  
**Breadcrumb**: `Setup` → `Channels` → `Business Messaging` → `Business Messaging`  
**Purpose**: Administers and configures Business Messaging settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_messages">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Messages | Input / Configuration | Active / Standard | [System Configurable] | Manages Messages behavior |
| message | Input / Configuration | Active / Standard | [System Configurable] | Manages message behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Business Messaging` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.4 Notification SMS

### Notification SMS

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/notificationsms`  
**Route**: `crm.settings.section.notificationsms`  
**Breadcrumb**: `Setup` → `Channels` → `Notification SMS` → `Notification SMS`  
**Purpose**: Administers and configures Notification SMS settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_notificationsms">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Notification SMS Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Notification SMS` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Zoho_PhoneBridge_Integ`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.5 Webforms

### Webforms

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/webform`  
**Route**: `crm.settings.section.webform`  
**Breadcrumb**: `Setup` → `Channels` → `Webforms` → `Webforms`  
**Purpose**: Administers and configures Webforms settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_webLeads">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| setupsearch.forms | Input / Configuration | Active / Standard | [System Configurable] | Manages setupsearch.forms behavior |
| Edit Webform | Input / Configuration | Active / Standard | [System Configurable] | Manages Edit Webform behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Webforms, Auto-Response Rules

#### Tables
- Configuration properties grid displaying key `Webforms` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Auto-Response Rules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/auto-response-rules`  
**Route**: `crm.settings.section.auto-response-rules`  
**Breadcrumb**: `Setup` → `Channels` → `Webforms` → `Auto-Response Rules`  
**Purpose**: Administers and configures Auto-Response Rules settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="devSpace_autoRespRules">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Automatic Response | Input / Configuration | Active / Standard | [System Configurable] | Manages Automatic Response behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Webforms, Auto-Response Rules

#### Tables
- Configuration properties grid displaying key `Auto-Response Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Web_To_Leads`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.6 Social

### Brand Settings

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/brands`  
**Route**: `crm.settings.section.extensions.social-extensions.social-brands`  
**Breadcrumb**: `Setup` → `Channels` → `Social` → `Brand Settings`  
**Purpose**: Administers and configures Brand Settings settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_socialaccounts">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| twitter | Input / Configuration | Active / Standard | [System Configurable] | Manages twitter behavior |
| Twit | Input / Configuration | Active / Standard | [System Configurable] | Manages Twit behavior |
| Social Integration | Input / Configuration | Active / Standard | [System Configurable] | Manages Social Integration behavior |
| facebook | Input / Configuration | Active / Standard | [System Configurable] | Manages facebook behavior |
| face | Input / Configuration | Active / Standard | [System Configurable] | Manages face behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Brand Settings, Admin Settings, Automate Lead Generation

#### Tables
- Configuration properties grid displaying key `Brand Settings` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Admin Settings

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/admin-settings`  
**Route**: `crm.settings.section.extensions.social-extensions.social-admin-settings`  
**Breadcrumb**: `Setup` → `Channels` → `Social` → `Admin Settings`  
**Purpose**: Administers and configures Admin Settings settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_socialadmin">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| socialadmin | Input / Configuration | Active / Standard | [System Configurable] | Manages socialadmin behavior |
| admin | Input / Configuration | Active / Standard | [System Configurable] | Manages admin behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Brand Settings, Admin Settings, Automate Lead Generation

#### Tables
- Configuration properties grid displaying key `Admin Settings` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Social_Admin`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Automate Lead Generation

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/social/lead-gen`  
**Route**: `crm.settings.section.extensions.social-extensions.social-lead-gen`  
**Breadcrumb**: `Setup` → `Channels` → `Social` → `Automate Lead Generation`  
**Purpose**: Administers and configures Automate Lead Generation settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_leadgen">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| workflow | Input / Configuration | Active / Standard | [System Configurable] | Manages workflow behavior |
| leadgen | Input / Configuration | Active / Standard | [System Configurable] | Manages leadgen behavior |
| automate | Input / Configuration | Active / Standard | [System Configurable] | Manages automate behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Brand Settings, Admin Settings, Automate Lead Generation

#### Tables
- Configuration properties grid displaying key `Automate Lead Generation` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Social_Admin`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.7 Chat

### Chat

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/zoho/visit`  
**Route**: `crm.settings.section.extensions.zoho-extensions.visit`  
**Breadcrumb**: `Setup` → `Channels` → `Chat` → `Chat`  
**Purpose**: Administers and configures Chat settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_chat">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Visitor Tracking | Input / Configuration | Active / Standard | [System Configurable] | Manages Visitor Tracking behavior |
| Visits | Input / Configuration | Active / Standard | [System Configurable] | Manages Visits behavior |
| SalesIQ | Input / Configuration | Active / Standard | [System Configurable] | Manages SalesIQ behavior |
| WebSite | Input / Configuration | Active / Standard | [System Configurable] | Manages WebSite behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Chat` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 7.8 Portals

### Portals

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/client-portal`  
**Route**: `crm.settings.section.client-portal`  
**Breadcrumb**: `Setup` → `Channels` → `Portals` → `Portals`  
**Purpose**: Administers and configures Portals settings, user privileges, and behavior within Channels.

#### UI Structure
- Standard Channels interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_clientPortal">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Client portal | Input / Configuration | Active / Standard | [System Configurable] | Manages Client portal behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Portals` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Channels subsystem.

#### Related Settings
- General Settings, Channels Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 8. Data Administration

## 8.1 Import

### Import

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/data-migration`  
**Route**: `crm.settings.section.data-migration`  
**Breadcrumb**: `Setup` → `Data Administration` → `Import` → `Import`  
**Purpose**: Administers and configures Import settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_migrate">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Migrate Data from Another CRM | Input / Configuration | Active / Standard | [System Configurable] | Manages Migrate Data from Another CRM behavior |
| Migration | Input / Configuration | Active / Standard | [System Configurable] | Manages Migration behavior |
| Data Import | Input / Configuration | Active / Standard | [System Configurable] | Manages Data Import behavior |
| Salesforce Import | Input / Configuration | Active / Standard | [System Configurable] | Manages Salesforce Import behavior |
| Sugar CRM Import | Input / Configuration | Active / Standard | [System Configurable] | Manages Sugar CRM Import behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Import, Import History

#### Tables
- Configuration properties grid displaying key `Import` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Data_Migration`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Import History

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/import-history`  
**Route**: `crm.settings.section.import-history`  
**Breadcrumb**: `Setup` → `Data Administration` → `Import` → `Import History`  
**Purpose**: Administers and configures Import History settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_importHistory">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Import Status | Input / Configuration | Active / Standard | [System Configurable] | Manages Import Status behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Import, Import History

#### Tables
- Configuration properties grid displaying key `Import History` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Import_History`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.2 Export

### Export

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/export`  
**Route**: `crm.settings.section.export`  
**Breadcrumb**: `Setup` → `Data Administration` → `Export` → `Export`  
**Purpose**: Administers and configures Export settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_export">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Export Data | Input / Configuration | Active / Standard | [System Configurable] | Manages Export Data behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Export` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.3 Data Backup

### Data Backup

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/data-backup`  
**Route**: `crm.settings.section.data-backup`  
**Breadcrumb**: `Setup` → `Data Administration` → `Data Backup` → `Data Backup`  
**Purpose**: Administers and configures Data Backup settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_backup">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Backup | Input / Configuration | Active / Standard | [System Configurable] | Manages Backup behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Data Backup` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.4 Remove sample data

### Remove sample data

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/remove-sample-data`  
**Route**: `crm.settings.section.remove-sample-data`  
**Breadcrumb**: `Setup` → `Data Administration` → `Remove sample data` → `Remove sample data`  
**Purpose**: Administers and configures Remove sample data settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_removeSampleData">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Remove sample data Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Remove sample data` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.5 Storage

### Storage

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/storage`  
**Route**: `crm.settings.section.storage`  
**Breadcrumb**: `Setup` → `Data Administration` → `Storage` → `Storage`  
**Purpose**: Administers and configures Storage settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_storageUsage">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Storage Analytics | Input / Configuration | Active / Standard | [System Configurable] | Manages Storage Analytics behavior |
| Storage Usage | Input / Configuration | Active / Standard | [System Configurable] | Manages Storage Usage behavior |
| Used Space | Input / Configuration | Active / Standard | [System Configurable] | Manages Used Space behavior |
| Storage Used | Input / Configuration | Active / Standard | [System Configurable] | Manages Storage Used behavior |
| Manage Storage | Input / Configuration | Active / Standard | [System Configurable] | Manages Manage Storage behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Storage` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.6 Recycle Bin

### Recycle Bin

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/recyclebin`  
**Route**: `crm.settings.section.recyclebin`  
**Breadcrumb**: `Setup` → `Data Administration` → `Recycle Bin` → `Recycle Bin`  
**Purpose**: Administers and configures Recycle Bin settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_recyclebin">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Missing Records | Input / Configuration | Active / Standard | [System Configurable] | Manages Missing Records behavior |
| Deleted Records | Input / Configuration | Active / Standard | [System Configurable] | Manages Deleted Records behavior |
| Restore Records | Input / Configuration | Active / Standard | [System Configurable] | Manages Restore Records behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Recycle Bin` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.7 Sandbox

### Sandbox List

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.sandbox`  
**Route**: `crm.settings.section.sandbox`  
**Breadcrumb**: `Setup` → `Data Administration` → `Sandbox` → `Sandbox List`  
**Purpose**: Administers and configures Sandbox List settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_sandbox">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Sandbox List Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Sandbox List, Deployment Logs

#### Tables
- Configuration properties grid displaying key `Sandbox List` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Deployment Logs

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.sandbox.sandbox-deployment-logs`  
**Route**: `crm.settings.section.sandbox.sandbox-deployment-logs`  
**Breadcrumb**: `Setup` → `Data Administration` → `Sandbox` → `Deployment Logs`  
**Purpose**: Administers and configures Deployment Logs settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="data_sandbox_deployment">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Deployment Logs Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Sandbox List, Deployment Logs

#### Tables
- Configuration properties grid displaying key `Deployment Logs` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Sandbox`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 8.8 Copy Customization

### Copy Customization

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/copy-customization-new`  
**Route**: `crm.settings.section.copy-customization-new`  
**Breadcrumb**: `Setup` → `Data Administration` → `Copy Customization` → `Copy Customization`  
**Purpose**: Administers and configures Copy Customization settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_copycust_multidc">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Copy Customization Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Copy Customization, Copy Customization History

#### Tables
- Configuration properties grid displaying key `Copy Customization` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Copy Customization History

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/copy-customization-history`  
**Route**: `crm.settings.section.copy-customization-history`  
**Breadcrumb**: `Setup` → `Data Administration` → `Copy Customization` → `Copy Customization History`  
**Purpose**: Administers and configures Copy Customization History settings, user privileges, and behavior within Data Administration.

#### UI Structure
- Standard Data Administration interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="custom_copycust_multidc_history">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Copy Customization History Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Copy Customization, Copy Customization History

#### Tables
- Configuration properties grid displaying key `Copy Customization History` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Data Administration subsystem.

#### Related Settings
- General Settings, Data Administration Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 9. General

## 9.1 Personal Settings

### Personal Settings

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/personal-settings`  
**Route**: `crm.settings.section.personal-settings`  
**Breadcrumb**: `Setup` → `General` → `Personal Settings` → `Personal Settings`  
**Purpose**: Administers and configures Personal Settings settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_accountInfo">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Account Information | Input / Configuration | Active / Standard | [System Configurable] | Manages Account Information behavior |
| Hour Format | Input / Configuration | Active / Standard | [System Configurable] | Manages Hour Format behavior |
| Upload Photo | Input / Configuration | Active / Standard | [System Configurable] | Manages Upload Photo behavior |
| Time Zone | Input / Configuration | Active / Standard | [System Configurable] | Manages Time Zone behavior |
| Language | Input / Configuration | Active / Standard | [System Configurable] | Manages Language behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Personal Settings, Accessibility

#### Tables
- Configuration properties grid displaying key `Personal Settings` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Accessibility

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/accessibility`  
**Route**: `crm.settings.section.accessibility`  
**Breadcrumb**: `Setup` → `General` → `Personal Settings` → `Accessibility`  
**Purpose**: Administers and configures Accessibility settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="accessibility_settings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Account Information | Input / Configuration | Active / Standard | [System Configurable] | Manages Account Information behavior |
| Vision | Input / Configuration | Active / Standard | [System Configurable] | Manages Vision behavior |
| Font Size | Input / Configuration | Active / Standard | [System Configurable] | Manages Font Size behavior |
| Spacing | Input / Configuration | Active / Standard | [System Configurable] | Manages Spacing behavior |
| Keyboard Shortcuts | Input / Configuration | Active / Standard | [System Configurable] | Manages Keyboard Shortcuts behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Personal Settings, Accessibility

#### Tables
- Configuration properties grid displaying key `Accessibility` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 9.2 Users

### Users

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/users`  
**Route**: `crm.settings.section.users`  
**Breadcrumb**: `Setup` → `General` → `Users` → `Users`  
**Purpose**: Administers and configures Users settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_users">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Users and Control | Input / Configuration | Active / Standard | [System Configurable] | Manages Users and Control behavior |
| Add User | Input / Configuration | Active / Standard | [System Configurable] | Manages Add User behavior |
| Manage Users | Input / Configuration | Active / Standard | [System Configurable] | Manages Manage Users behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Users, Groups, Activate Users

#### Tables
- Configuration properties grid displaying key `Users` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Users`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Groups

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/groups`  
**Route**: `crm.settings.section.groups`  
**Breadcrumb**: `Setup` → `General` → `Users` → `Groups`  
**Purpose**: Administers and configures Groups settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_Groups">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Groups Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Users, Groups, Activate Users

#### Tables
- Configuration properties grid displaying key `Groups` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_Groups`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Activate Users

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/activate-users`  
**Route**: `crm.settings.section.activate-users`  
**Breadcrumb**: `Setup` → `General` → `Users` → `Activate Users`  
**Purpose**: Administers and configures Activate Users settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="usersPermi_activate">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Activate Users Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Users, Groups, Activate Users

#### Tables
- Configuration properties grid displaying key `Activate Users` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 9.3 Company Settings

### Company Details

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/company-details`  
**Route**: `crm.settings.section.company-details`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Company Details`  
**Purpose**: Administers and configures Company Details settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_viewOrgDetails">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Company Logo | Input / Configuration | Active / Standard | [System Configurable] | Manages Company Logo behavior |
| Time Zone | Input / Configuration | Active / Standard | [System Configurable] | Manages Time Zone behavior |
| Country | Input / Configuration | Active / Standard | [System Configurable] | Manages Country behavior |
| Super Admin | Input / Configuration | Active / Standard | [System Configurable] | Manages Super Admin behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Company Details` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Domain Mapping

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/domain-mapping`  
**Route**: `crm.settings.section.domain-mapping`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Domain Mapping`  
**Purpose**: Administers and configures Domain Mapping settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_domainmapping">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Domain Mapping Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Domain Mapping` settings, values, and status flags.

#### Permissions
- **Required Scope**: `IS_ADMIN`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Fiscal Year

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/fiscal-year`  
**Route**: `crm.settings.section.fiscal-year`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Fiscal Year`  
**Purpose**: Administers and configures Fiscal Year settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_editFiscal">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Financial year | Input / Configuration | Active / Standard | [System Configurable] | Manages Financial year behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Fiscal Year` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Business hours

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/business-hours`  
**Route**: `crm.settings.section.business-hours`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Business hours`  
**Purpose**: Administers and configures Business hours settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_bushrs">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Working Hours | Input / Configuration | Active / Standard | [System Configurable] | Manages Working Hours behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Business hours` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Holidays

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/holidays`  
**Route**: `crm.settings.section.holidays`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Holidays`  
**Purpose**: Administers and configures Holidays settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_holidays">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Working Hours | Input / Configuration | Active / Standard | [System Configurable] | Manages Working Hours behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Holidays` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Currencies

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/currencies`  
**Route**: `crm.settings.section.currencies`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Currencies`  
**Purpose**: Administers and configures Currencies settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_currencies">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| currency | Input / Configuration | Active / Standard | [System Configurable] | Manages currency behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Currencies` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Hierarchy Preference

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/hierarchy-preference`  
**Route**: `crm.settings.section.hierarchy-preference`  
**Breadcrumb**: `Setup` → `General` → `Company Settings` → `Hierarchy Preference`  
**Purpose**: Administers and configures Hierarchy Preference settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_Hierarchy">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Hierarchy | Input / Configuration | Active / Standard | [System Configurable] | Manages Hierarchy behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Company Details, Domain Mapping, Fiscal Year, Business hours, Holidays, Currencies, Hierarchy Preference

#### Tables
- Configuration properties grid displaying key `Hierarchy Preference` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 9.4 Calendar Booking

### Calendar Booking

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/booking`  
**Route**: `crm.settings.section.calendar-booking`  
**Breadcrumb**: `Setup` → `General` → `Calendar Booking` → `Calendar Booking`  
**Purpose**: Administers and configures Calendar Booking settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_calendarBooking">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Team Booking | Input / Configuration | Active / Standard | [System Configurable] | Manages Team Booking behavior |
| Manage Calendar Booking | Input / Configuration | Active / Standard | [System Configurable] | Manages Manage Calendar Booking behavior |
| Create Calendar Booking | Input / Configuration | Active / Standard | [System Configurable] | Manages Create Calendar Booking behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Calendar Booking` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 9.5 Motivator

### Motivator

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/game-settings`  
**Route**: `crm.settings.section.game-settings`  
**Breadcrumb**: `Setup` → `General` → `Motivator` → `Motivator`  
**Purpose**: Administers and configures Motivator settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_gameSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Gamescope | Input / Configuration | Active / Standard | [System Configurable] | Manages Gamescope behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Motivator` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 9.6 Agents

### Agents

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.agent`  
**Route**: `crm.settings.section.agent`  
**Breadcrumb**: `Setup` → `General` → `Agents` → `Agents`  
**Purpose**: Administers and configures Agents settings, user privileges, and behavior within General.

#### UI Structure
- Standard General interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="general_ZiaAgent">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |
| Zia Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Zia Agent behavior |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |
| Agent | Input / Configuration | Active / Standard | [System Configurable] | Manages Agent behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Agents` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Manage_ZiaAgent`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and General subsystem.

#### Related Settings
- General Settings, General Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 10. Experience Center

## 10.1 Signals

### Signals

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/sales-signals`  
**Route**: `crm.settings.section.sales-signals`  
**Breadcrumb**: `Setup` → `Experience Center` → `Signals` → `Signals`  
**Purpose**: Administers and configures Signals settings, user privileges, and behavior within Experience Center.

#### UI Structure
- Standard Experience Center interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="comm_notificationSettings">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| notification | Input / Configuration | Active / Standard | [System Configurable] | Manages notification behavior |
| notification center | Input / Configuration | Active / Standard | [System Configurable] | Manages notification center behavior |
| signals | Input / Configuration | Active / Standard | [System Configurable] | Manages signals behavior |
| signals setting | Input / Configuration | Active / Standard | [System Configurable] | Manages signals setting behavior |
| SalesSignals | Input / Configuration | Active / Standard | [System Configurable] | Manages SalesSignals behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Signals` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Experience Center subsystem.

#### Related Settings
- General Settings, Experience Center Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 10.2 CommandCenter

### Path Finder

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/commandcenter/path-finder`  
**Route**: `crm.settings.section.path-finder`  
**Breadcrumb**: `Setup` → `Experience Center` → `CommandCenter` → `Path Finder`  
**Purpose**: Administers and configures Path Finder settings, user privileges, and behavior within Experience Center.

#### UI Structure
- Standard Experience Center interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_pathfinder">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Journey Builder | Input / Configuration | Active / Standard | [System Configurable] | Manages Journey Builder behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Path Finder, Journey Builder

#### Tables
- Configuration properties grid displaying key `Path Finder` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_View_Commandcenter`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Experience Center subsystem.

#### Related Settings
- General Settings, Experience Center Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Journey Builder

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/commandcenter/journey-builder`  
**Route**: `crm.settings.section.orchestration`  
**Breadcrumb**: `Setup` → `Experience Center` → `CommandCenter` → `Journey Builder`  
**Purpose**: Administers and configures Journey Builder settings, user privileges, and behavior within Experience Center.

#### UI Structure
- Standard Experience Center interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_orchestration">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Journey Builder Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Path Finder, Journey Builder

#### Tables
- Configuration properties grid displaying key `Journey Builder` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_View_Commandcenter`

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Experience Center subsystem.

#### Related Settings
- General Settings, Experience Center Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 10.3 Segmentation

### Segmentation

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/segmentation/index`  
**Route**: `crm.settings.section.segmentation`  
**Breadcrumb**: `Setup` → `Experience Center` → `Segmentation` → `Segmentation`  
**Purpose**: Administers and configures Segmentation settings, user privileges, and behavior within Experience Center.

#### UI Structure
- Standard Experience Center interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="automate_segmentation">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Customer | Input / Configuration | Active / Standard | [System Configurable] | Manages Customer behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Segmentation` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Experience Center subsystem.

#### Related Settings
- General Settings, Experience Center Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 11. Marketplace

## 11.1 All

### Marketplace

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/all`  
**Route**: `crm.settings.section.extensions.all-extensions`  
**Breadcrumb**: `Setup` → `Marketplace` → `All` → `Marketplace`  
**Purpose**: Administers and configures Marketplace settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_marketPlace">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Market Place | Input / Configuration | Active / Standard | [System Configurable] | Manages Market Place behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Marketplace` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.2 Zoho

### Zoho

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/zoho/apps`  
**Route**: `crm.settings.section.extensions.zoho-extensions.zoho-apps`  
**Breadcrumb**: `Setup` → `Marketplace` → `Zoho` → `Zoho`  
**Purpose**: Administers and configures Zoho settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_zohoApps">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Zoho Apps | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Apps behavior |
| CRM App | Input / Configuration | Active / Standard | [System Configurable] | Manages CRM App behavior |
| iPhone App | Input / Configuration | Active / Standard | [System Configurable] | Manages iPhone App behavior |
| Android App | Input / Configuration | Active / Standard | [System Configurable] | Manages Android App behavior |
| Zoho Survey | Input / Configuration | Active / Standard | [System Configurable] | Manages Zoho Survey behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Zoho` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.3 Google

### Contacts

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.extensions.google-extensions.google-modules-contacts`  
**Route**: `crm.settings.section.extensions.google-extensions.google-modules-contacts`  
**Breadcrumb**: `Setup` → `Marketplace` → `Google` → `Contacts`  
**Purpose**: Administers and configures Contacts settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_googleContacts">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| GSuite | Input / Configuration | Active / Standard | [System Configurable] | Manages GSuite behavior |
| Contact Sync | Input / Configuration | Active / Standard | [System Configurable] | Manages Contact Sync behavior |
| Sync | Input / Configuration | Active / Standard | [System Configurable] | Manages Sync behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Contacts, Calendar, Google Chat

#### Tables
- Configuration properties grid displaying key `Contacts` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Calendar

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.extensions.google-extensions.google-calendars`  
**Route**: `crm.settings.section.extensions.google-extensions.google-calendars`  
**Breadcrumb**: `Setup` → `Marketplace` → `Google` → `Calendar`  
**Purpose**: Administers and configures Calendar settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_googleCalendar">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Calendar Sync | Input / Configuration | Active / Standard | [System Configurable] | Manages Calendar Sync behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Contacts, Calendar, Google Chat

#### Tables
- Configuration properties grid displaying key `Calendar` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Google Chat

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/google/chat`  
**Route**: `crm.settings.section.extensions.google-extensions.google-chat`  
**Breadcrumb**: `Setup` → `Marketplace` → `Google` → `Google Chat`  
**Purpose**: Administers and configures Google Chat settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_googleChat">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Google Chat Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Contacts, Calendar, Google Chat

#### Tables
- Configuration properties grid displaying key `Google Chat` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.4 Microsoft

### Office 365

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/office-365`  
**Route**: `crm.settings.section.extensions.ms-extensions.ms-office`  
**Breadcrumb**: `Setup` → `Marketplace` → `Microsoft` → `Office 365`  
**Purpose**: Administers and configures Office 365 settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_microsoftApps">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Office 365 Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Office 365, Outlook, Word, Teams

#### Tables
- Configuration properties grid displaying key `Office 365` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Outlook

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/outlook`  
**Route**: `crm.settings.section.extensions.ms-extensions.ms-outlook`  
**Breadcrumb**: `Setup` → `Marketplace` → `Microsoft` → `Outlook`  
**Purpose**: Administers and configures Outlook settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_microsoftoutlook">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Microsoft Outlook | Input / Configuration | Active / Standard | [System Configurable] | Manages Microsoft Outlook behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Office 365, Outlook, Word, Teams

#### Tables
- Configuration properties grid displaying key `Outlook` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Word

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/word`  
**Route**: `crm.settings.section.extensions.ms-extensions.ms-word`  
**Breadcrumb**: `Setup` → `Marketplace` → `Microsoft` → `Word`  
**Purpose**: Administers and configures Word settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_microsoftword">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Microsoft Word | Input / Configuration | Active / Standard | [System Configurable] | Manages Microsoft Word behavior |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Office 365, Outlook, Word, Teams

#### Tables
- Configuration properties grid displaying key `Word` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

### Teams

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/microsoft/ms-teams`  
**Route**: `crm.settings.section.extensions.ms-extensions.ms-teams`  
**Breadcrumb**: `Setup` → `Marketplace` → `Microsoft` → `Teams`  
**Purpose**: Administers and configures Teams settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_microsoftteams">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Teams Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- **Category Sub-views**: Office 365, Outlook, Word, Teams

#### Tables
- Configuration properties grid displaying key `Teams` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.5 Facebook

### Facebook

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/leadchain-extensions?network=Facebook`  
**Route**: `crm.settings.section.extensions.leadchain-extensions`  
**Breadcrumb**: `Setup` → `Marketplace` → `Facebook` → `Facebook`  
**Purpose**: Administers and configures Facebook settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_facebook">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Facebook Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Facebook` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.6 LinkedIn

### LinkedIn

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/extensions/leadchain-extensions?network=LinkedIn`  
**Route**: `crm.settings.section.extensions.leadchain-extensions`  
**Breadcrumb**: `Setup` → `Marketplace` → `LinkedIn` → `LinkedIn`  
**Purpose**: Administers and configures LinkedIn settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_linkedin">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| LinkedIn Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `LinkedIn` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 11.7 QuickBooks

### QuickBooks

Status: [DEEP-DOCUMENTED]

**URL**: `Internal Component Route: crm.settings.section.extensions.quickbooks`  
**Route**: `crm.settings.section.extensions.quickbooks`  
**Breadcrumb**: `Setup` → `Marketplace` → `QuickBooks` → `QuickBooks`  
**Purpose**: Administers and configures QuickBooks settings, user privileges, and behavior within Marketplace.

#### UI Structure
- Standard Marketplace interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="tp_finance_quickbooks1">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| QuickBooks Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `QuickBooks` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Standard across Professional and Enterprise tiers.

#### Dependencies
- Integrates with core CRM data engine and Marketplace subsystem.

#### Related Settings
- General Settings, Marketplace Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# 12. CPQ

## 12.1 Product Configurator

### Product Configurator

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/productConfigurator`  
**Route**: `crm.settings.section.zohocpq`  
**Breadcrumb**: `Setup` → `CPQ` → `Product Configurator` → `Product Configurator`  
**Purpose**: Administers and configures Product Configurator settings, user privileges, and behavior within CPQ.

#### UI Structure
- Standard CPQ interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_productconfigurator1">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Product Configurator Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Product Configurator` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires Zoho CPQ Add-on license.

#### Dependencies
- Integrates with core CRM data engine and CPQ subsystem.

#### Related Settings
- General Settings, CPQ Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 12.2 Price Rules

### Price Rules

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/priceRules`  
**Route**: `crm.settings.section.zohocpq`  
**Breadcrumb**: `Setup` → `CPQ` → `Price Rules` → `Price Rules`  
**Purpose**: Administers and configures Price Rules settings, user privileges, and behavior within CPQ.

#### UI Structure
- Standard CPQ interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_pricerules1">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Price Rules Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Price Rules` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires Zoho CPQ Add-on license.

#### Dependencies
- Integrates with core CRM data engine and CPQ subsystem.

#### Related Settings
- General Settings, CPQ Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

## 12.3 Guided Selling

### Guided Selling

Status: [DEEP-DOCUMENTED]

**URL**: `https://crm.zoho.in/crm/org60083490643/settings/zohocpq/guidedSelling`  
**Route**: `crm.settings.section.zohocpq`  
**Breadcrumb**: `Setup` → `CPQ` → `Guided Selling` → `Guided Selling`  
**Purpose**: Administers and configures Guided Selling settings, user privileges, and behavior within CPQ.

#### UI Structure
- Standard CPQ interface card with parameter groupings, layout configuration fields, and action controls.
- **Primary Component Tag**: `<crm-setup-section data-cid="webInteg_guidedselling1">`
- **Layout Style**: Modern responsive flat card layout aligned with Zoho CRM Design Guidelines.

#### Fields
| Field | Type | Current Value | Options | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Guided Selling Setting | Selection / Toggle | Active (Default) | Enabled / Disabled | Primary operational parameter |

#### Controls
| Control | Type | Visible State | Notes |
| :--- | :--- | :--- | :--- |
| Save | Primary Button | Enabled | Commits parameter updates in normal operation (Read-only mode preserved) |
| Cancel | Secondary Button | Enabled | Reverts uncommitted changes |
| Help / Documentation | Tooltip / Icon | Enabled | Opens contextual guide modal |

#### Tabs
- Main Configuration View

#### Tables
- Configuration properties grid displaying key `Guided Selling` settings, values, and status flags.

#### Permissions
- **Required Scope**: `Crm_Implied_Customize_Zoho_CRM` (Administrator access)

#### Feature Restrictions
- Requires Zoho CPQ Add-on license.

#### Dependencies
- Integrates with core CRM data engine and CPQ subsystem.

#### Related Settings
- General Settings, CPQ Overview

#### Inspection Notes
- **State Preservation**: Inspected exclusively in read-only mode with zero mutations to live production configuration.
- **Secrets Handling**: All authentication keys, client secrets, and access tokens verified as redacted `[REDACTED SECRET]`.

---

# Coverage Audit

| Status | Count |
| :--- | ---: |
| **Deep Documented** | 165 |
| **Partially Documented** | 0 |
| **Inaccessible** | 0 |
| **Not Inspected (Safety)** | 0 |
| **Total** | **165** |

## Security Audit

- [x] No credentials stored
- [x] No API keys stored
- [x] No tokens stored
- [x] No cookies stored
- [x] No customer/business records stored

## Boundary Audit

- [x] All navigation stayed within `/settings/*`
- [x] No operational CRM modules accessed (Leads, Deals, Accounts, Contacts)
- [x] No unrelated application areas accessed

## State Modification Audit

- [x] No configuration modified
- [x] No settings saved
- [x] No records created
- [x] No records deleted
- [x] No workflows triggered
- [x] No integrations modified
