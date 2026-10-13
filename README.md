# Crusource documentation

Start with the [complete document index](INDEX.md). [Document locations](DOCUMENT_LOCATIONS.json) maps previous paths to their new locations.

See the [workspace cleanup report](operations/WORKSPACE_CLEANUP_REPORT.md) for what was moved, removed, verified, and retained.

This repository contains product drafts, reference material, implementation reports, and historical evidence. Application source and current CI/deployment configuration live in their owning repositories. A document's existence does not establish that a feature is implemented or deployed.

## Start here

- [CRM modules and features](product/CRUSOURCE_CRM_MODULES_AND_FEATURES.md): source-backed feature inventory. Preserve its status vocabulary: `IMPLEMENTED`, `PARTIALLY IMPLEMENTED`, `BACKEND ONLY`, `INTERNAL`, `PLANNED / DOCUMENTED ONLY`.
- [CRM product requirements](product/CRUSOURCE_CRM_PRD.md) and [stakeholder overview](product/CRUSOURCE_CRM_STAKEHOLDER_OVERVIEW.md): product context; verify implementation claims against source.
- [Unified Superadmin requirements](product/superadmin/SUPERADMIN_PRD.md) and [designer data flows](product/superadmin/SUPERADMIN_DFD.md): drafts for designer review covering CRM and VMS.
- [Security audit baseline](security/CRM_SECURITY_AUDIT.md), [approved repair plan](security/CRM_SECURITY_IMPLEMENTATION_PLAN.md), and [implementation evidence](security/CRM_SECURITY_IMPLEMENTATION_REPORT.md): distinguish original findings from local fixes and actual deployment status.
- [Security rollout instructions](../crusource-crm-backend/docs/security-rollout.md): maintained beside the backend implementation.
- [Forecast plan](features/forecast/FORECAST_IMPLEMENTATION_PLAN.md) and [implementation report](features/forecast/FORECAST_FIX_REPORT.md): feature-specific evidence at the time of writing. Older reported blockers are historical; consult newer validation evidence before treating them as current.

## Organization

| Folder | Purpose |
| --- | --- |
| `product/` | Requirements, stakeholder material, design guidance, and maintained feature inventory. |
| `architecture/` | Architecture and flow diagrams. |
| `features/` | Feature proposals, implementation plans, reports, and Superadmin phase handoffs. A proposal is not a delivered feature. |
| `security/` | Security audit baseline, remediation plan, implementation report, and dependency/environment reviews. |
| `operations/` | Operational guidance. Check commands against the current owning application repository. |
| `reference/` | External-product references, implementation comparisons, and testing data. These are not Crusource implementation truth. |
| `archive/` | Historical specifications, audits, agent notes, log exports, and configuration examples. Retained for provenance; not current operational instructions. |
| `exports/` | Word/PDF handoffs. The paired Markdown draft is the editable source; exports can become stale after Markdown changes. |

## Maintenance

Keep related plans and reports together and link them to source/evidence. Record the date, product/repository scope, draft or implementation status, and deployment status in new reports. Do not silently rewrite old audit findings as if they described a newer release.

Use repository-relative links. Application repositories are siblings of this docs repository; links to source must traverse back to the workspace. Update backlinks and the index when moving files. Keep backups, raw logs, dependency caches, and test checkouts out of the main documentation tree. Existing historical evidence is preserved in the archive; review sensitive exports before sharing them externally.

The archived Compose file and command notes are reference snapshots. Use the [workspace Compose configuration](../docker-compose.yml) and each application's current workflows for execution. No documentation is authorization to reset repositories, delete data, or run deployment commands.
