# Module — Permissions (Profiles + Roles + Sharing)

## PM.1 Profiles

Source: https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/manage-profile-permissions (could not be crawled during this session, page references confirmed in `10_References.md` — field structure reconstructed from snippets).

A Profile defines what a user can *do*. Categories of permission include:

- **Module Permissions** — per module: View / Create / Edit / Delete / Export / Import / Approve.
- **Field-level Permissions** — View / Edit / Hide, per field.
- **Record-level Permissions** — by module (co-ordinated with Roles).
- **Administrative Permissions**: Manage Users, Manage Roles, Manage Workflows, Manage Blueprints, Manage Approvals, Customization, Data Administration, Import/Export, Manage Extensions.
- **Special Permissions**: Mail Merge, Mass Email, Mass Update, Mass Delete, Re-assign, Share, Public Links, View Forecasts.

Default *Standard* profile and *Administrator* profile are pre-supplied.

## PM.2 Roles (verbatim principles — https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction)

> "Users at a higher hierarchy can always access all the records of at a lower hierarchy."
> "By default, users of the same role cannot access each others data."
> "Using the Share Data with Peers option you can enable sharing of data among users of the same role."
> "By default, users at the top of the hierarchy cannot view the data shared to their subordinate users through custom sharing rules. However, you can enable access rights to the managers by using the Superiors Allowed option while creating data sharing rule."
> "A user with an Administrator profile will have access to all the data irrespective of the role assigned to the user."

## PM.3 Sharing Rules

- Sharing Rules ↔ Roles mechanism to grant access to specific roles/users.

## PM.4 Field-level Permissions

- Each field can be marked Hide / Read / Edit per profile.

## PM.5 Cross References

- `../05_Business_Rules.md` §5.4, §5.5.
- `../Modules/Users.md`.
