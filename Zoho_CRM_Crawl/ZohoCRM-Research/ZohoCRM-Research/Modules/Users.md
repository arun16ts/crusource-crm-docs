# Module — Users

## US.1 General Information

- **Users** are individual Zoho CRM logins assigned a Role and Profile and (optionally) a Territory.
- **Source**: https://help.zoho.com/portal/en/kb/crm/security-control/data-security-types/articles/get-started-manage-users

## US.2 User Attributes (admin-editable)

| Attribute | Type | Notes |
|---|---|---|
| Name | text | — |
| Email Address | email | login + contact |
| Role | Lookup (Roles) | drives hierarchy-based access |
| Profile | Lookup (Profiles) | drives fine-grained permissions |
| Territory | Lookup (Territories — Enterprise+) | sales buckets |
| Status | Picklist | Active / Inactive |
| Time Zone | Picklist | — |
| Locale / Language | Picklist | — |
| Reporting To | Lookup (User) | managerial hierarchy |

## US.3 Lifecycle

- Invitation email sent when Admin clicks "Add User".
- User can be Deactivated (soft delete) — historical ownership retained.
- Reassignment to another user supported on deactivation.

## US.4 Self-Service

- Change own profile picture / password.
- Configure personal email signature, notification preferences.

## US.5 Cross References

- `../Modules/Permissions.md`.
- `../05_Business_Rules.md` §5.4.
