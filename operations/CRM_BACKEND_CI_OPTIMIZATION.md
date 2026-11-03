# CRM backend CI optimization review

- **Reviewed:** 3 November 2026
- **Scope:** `crusource-crm-backend` CI change detection, required checks, and stage load-test gating.
- **Status:** Local implementation review and focused verification completed. Remote GitHub Actions status was not queried. This report does not claim that CI is green or that deployment occurred.

## Design

The backend workflow uses a change detector to avoid repeating expensive checks for changes that cannot affect them. Pull requests and pushes compare against their actual base; relevant application changes select mapped tests, while shared infrastructure, dependency, unknown, or unclassifiable changes select broader checks. Docs-only changes can skip application tests. Dependency auditing and SBOM generation run when runtime dependencies change, with a weekly scheduled audit to catch newly disclosed vulnerabilities without a dependency edit. The stage pipeline runs Locust for code changes requiring tests; a manual dispatch runs it only when its explicit `run_load_test` input is true.

This can reduce repeated test work, but targeted tests still provision PostgreSQL and Redis, install dependencies, and apply migrations. The workflow therefore does not eliminate that setup cost. No runtime-savings percentage or sub-30-second completion target has been measured here.

## Review and fixes

The earlier review findings were checked against the current CRM backend files and addressed as follows:

1. **Workflow command injection:** detector outputs are passed through step environment variables, not interpolated into the workflow shell script. Ruff receives the selected paths after `--`. The detector now calls Git with an argument vector and `shell=False`, including for event-provided refs.
2. **Git errors skipping checks:** required diff/status failures produce an unknown change set. Unknown changes select full checks; a valid empty diff remains distinguishable. Scheduled runs intentionally select no application tests while still triggering the dependency audit.
3. **Text fixtures mistaken for documentation:** documentation is allowlisted by known paths and filenames; paths under `tests/`, `src/`, scripts, and migrations are treated as executable inputs regardless of extension.
4. **Stage load test behavior:** push/PR docs-only changes skip Locust. Manual dispatch honors `run_load_test` directly, including when the latest diff would otherwise skip application tests.
5. **Additional completeness issues:** Git output is parsed as NUL-delimited paths; malformed paths fail closed. Ruff and Python test/migration configuration changes trigger full lint and broader tests. Changes to the detector select its own regression test.

The CRM implementation uses Python-specific checks and PostgreSQL migration validation. The VMS workflow was used as an architectural reference, not copied as a product-specific implementation.

## Source of truth

- [CRM backend CI workflow](../../crusource-crm-backend/.github/workflows/ci.yml)
- [Stage test and load pipeline](../../crusource-crm-backend/.github/workflows/stage-test-pipeline.yml)
- [Change detector](../../crusource-crm-backend/scripts/ci/detect_changes.py)
- [Detector regression tests](../../crusource-crm-backend/tests/test_ci_change_detection.py)
- [VMS backend CI workflow](../../crusource-vms-backend/.github/workflows/ci.yml) (comparison only)

## Verification evidence and limits

Local verification on the reviewed working tree:

- Detector regression tests: **8 passed**.
- Full backend Ruff check: **passed**.
- Python compile check for `src`, `scripts`, and `alembic`: **passed**.
- YAML parsing of both changed workflows and `git diff --check`: **passed**.
- Full backend pytest: **not clean** — 2,396 passed, 101 skipped, 6 failed, and 30 errors. The errors included pytest temporary-directory access failures. Re-running the affected files with a temporary directory inside the repository removed those setup errors but still produced 12 failures and 101 passes: SES campaign expectations, a migration integrity expectation, and local export/storage filesystem failures. These application/environment failures were not changed as part of this CI review.

The focused checks validate the detector fixes, not every GitHub-hosted behavior or integration service. The full CI suite and remote run remain unverified. Recheck the workflow against the current GitHub Actions configuration and inspect the next remote run before relying on a savings claim or treating the branch as ready to deploy.
