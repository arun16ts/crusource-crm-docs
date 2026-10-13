# Workspace and documentation cleanup

**Date:** 13 October 2026  
**Scope:** Documentation organization and local validation artifacts. No application source edits, commits, pushes, migrations, or deployments were performed in this cleanup.

## Documentation

- Moved all 254 original documentation/reference files into the categorized tree. The [index](../INDEX.md) provides navigation and [location map](../DOCUMENT_LOCATIONS.json) records every previous path.
- Preserved 171 non-Markdown files byte-for-byte, including Word/PDF exports, images, test data, reference code, and log exports.
- Preserved the content of 83 Markdown documents, changing only links. Repaired 129 document links and two links to relocated verification evidence. Link validation initially checked 629 local references with none broken; the final check includes these new navigation/report files as well.
- Kept the 11 originally untracked files, including the security and Forecast reports and Superadmin designer handoffs. Their relocation does not commit them.
- Added status/maintenance guidance and clearly separated historical audits/configuration examples. Existing exports were not regenerated and may lag their editable Markdown drafts.
- Updated workspace `AGENTS.md` to point to the docs index and maintained feature inventory.

## Local artifacts

| Area | Result |
| --- | --- |
| `.next-phase2/` | Archived its verification screenshots and route results under `validation/archive/phase2-verification/`; removed the original root folder. |
| Registered Git worktrees | Removed 10 clean frontend worktrees through Git. Their exact commits remain under `refs/archive/workspace-cleanup-20261013/<name>` in the frontend repository. |
| Redundant clones | Removed the clean calendar-export frontend clone after verifying a complete Git bundle. Removed the security frontend validation copy after checking its HEAD, status, and all 23 changed/untracked file contents against the main frontend, with its Git history also bundled. |
| Other worktree artifacts | Archived 17 folders of historical scripts, logs, and validation evidence under `validation/archive/worktree-evidence/`. The Advaith repository copies remain because their backend contains changes. |
| Dependency/build caches | Removed 11 rebuildable dependency, build, advisory-cache, and temporary folders. Application `node_modules`, build output, Python venv, and active services were not cleared. |
| Historical logs | Moved 100 top-level validation logs into `validation/archive/historical-logs/`. Recent security audit logs, advisory results, and SBOM remain in `validation/security-audit/`. |
| `storage/` | Kept database backups, application documents, and the migration-review SQL. Moved UI review screenshots into `validation/archive/ui-reviews/`. |

## Intentionally retained

Changed repository copies in `.worktrees/advaith-adminhub-20261009/`, `validation/forecast-frontend-ci/`, and `validation/phase4/` are preserved. Other restoration/billing/document validation artifacts remain where uniqueness or recovery value has not been established. Thus `.worktrees/` and `validation/` still have useful contents; they were not blanket-deleted.

Windows permissions blocked deletion of these three disposable test directories even after approved access and a scoped ACL-reset attempt:

- `validation/security-audit/full-pytest-temp/`
- `validation/security-audit/full-pytest-final-temp/`
- `validation/security-audit/pytest-storage-green/`

These folders are retained rather than changing broader filesystem permissions. They are separate from application storage and required evidence.

## Recovery and evidence

Cleanup manifests, original document hashes/Markdown, repository status snapshots, verified history bundles, and the pre-relocation graph are retained in `validation/workspace-cleanup/`. Preserve this folder until the reorganization is reviewed. It can contain historical document and Git data; keep it local.

For a removed registered worktree, use its recorded archive ref with `git worktree add` from the owning frontend repository. For the two independent clones, the self-contained `.bundle` files under `validation/workspace-cleanup/git-bundles/` preserve committed history. The removed security copy's uncommitted changes were verified to remain in the main frontend.

Graph source provenance was relocated before refresh, preserving existing knowledge and relationships. New links and folder names do not assert new product features. Graph warnings and validation results are recorded in `validation/workspace-cleanup/`.

Final validation: all 633 local Markdown references resolve, original document integrity checks pass, and no unmerged Git entries or conflict markers were found. Graphify refresh succeeded with 31,186 nodes and 80,245 relationships, retaining all five repository roots and no stale relocated source paths. Its five existing TSX partial-extraction warnings and empty `pyproject.toml` extraction remain recorded; they were not silently treated as complete coverage. Documentation/artifact cleanup did not require rerunning application CI suites.
