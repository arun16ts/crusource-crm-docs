# Super Admin Phase 0 review package

Completed 9 October 2026. Application feature implementation starts in Phase 1.

- [Baseline report: verified checks, source findings and limits](BASELINE_REPORT.md)
- [API/state contracts and architecture rules](CONTRACTS.md)
- [Migration/backfill/collision/rollback checklist](MIGRATION_CHECKLIST.md)
- [Executable typed DTOs](contracts.py), [generated JSON schemas](contracts.schema.json), [contract check results](contract-checks.json)
- [Synthetic legacy inventory](legacy-inventory.json), [reproducible inventory script](inventory-legacy.py)
- [Screenshot metadata and fixture boundaries](ui-captures.json), [capture runner](capture-ui.mjs), [component fixture](ui-fixture.tsx)
- [Phase-wise implementation plan](../SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md)

## Visual references

These are current presentation baselines, not proposed redesigns. Actual components/CSS/font are mounted with synthetic data; the CRM sample body and disabled effects are documented in the baseline report. All addresses shown are synthetic. The screenshots intentionally retain existing UI defects.

| Current screen | Desktop 1440px | Tablet 768px | Mobile 390px |
|---|---|---|---|
| CRM workspace components | [View](screenshots/dashboard-reference-1440.png) | [View](screenshots/dashboard-reference-768.png) | [View](screenshots/dashboard-reference-390.png) |
| Platform overview | [View](screenshots/superadmin-dashboard-1440.png) | [View](screenshots/superadmin-dashboard-768.png) | [View](screenshots/superadmin-dashboard-390.png) |
| Organizations | [View](screenshots/superadmin-organizations-1440.png) | [View](screenshots/superadmin-organizations-768.png) | [View](screenshots/superadmin-organizations-390.png) |
| Platform access | [View](screenshots/superadmin-access-1440.png) | [View](screenshots/superadmin-access-768.png) | [View](screenshots/superadmin-access-390.png) |
| Sign-in | [View](screenshots/superadmin-login-1440.png) | [View](screenshots/superadmin-login-768.png) | [View](screenshots/superadmin-login-390.png) |
| Login history | [View](screenshots/superadmin-login-history-1440.png) | [View](screenshots/superadmin-login-history-768.png) | [View](screenshots/superadmin-login-history-390.png) |
| Feedback | [View](screenshots/superadmin-feedback-1440.png) | [View](screenshots/superadmin-feedback-768.png) | [View](screenshots/superadmin-feedback-390.png) |
| Trial extensions | [View](screenshots/superadmin-trial-extensions-1440.png) | [View](screenshots/superadmin-trial-extensions-768.png) | [View](screenshots/superadmin-trial-extensions-390.png) |

Also inspect [CRM collapsed sidebar, 1440px](screenshots/dashboard-reference-collapsed-1440.png).

## Reproduce locally

PowerShell, from the workspace root. Use the installed backend venv and frontend dependencies. Commands below do not require provider keys or a running application database. Browser capture requires installed Microsoft Edge on Windows (Chromium on other systems) and the cached Instrument Sans font from a successful normal Next build. The capture server binds loopback on an ephemeral port and closes afterward; it blocks external origins and unstubbed application requests.

DTO/schema and legacy-state checks:

```powershell
& '.\crusource-crm-backend\.venv\Scripts\python.exe' '.\crusource-crm-docs\superadmin-phase0\contracts.py'
& '.\crusource-crm-backend\.venv\Scripts\python.exe' '.\crusource-crm-docs\superadmin-phase0\inventory-legacy.py'
```

Frontend checks, executed from `crusource-crm-frontend`:

```powershell
npx.cmd tsc --noEmit
npm.cmd run lint
npm.cmd run test:platform-auth:browser
npm.cmd run test:session-startup:browser
npm.cmd run test:localization
npm.cmd run test:invitations
npm.cmd run test:public:analytics
npm.cmd run build
node ../crusource-crm-docs/superadmin-phase0/capture-ui.mjs
```

Targeted backend baseline, executed from `crusource-crm-backend`. These synthetic environment values prevent app imports from connecting to a configured application database. The tests use in-memory SQLite and fake services. Restore previous environment values afterward or use a fresh shell. Do not enable `PLATFORM_POSTGRES_TESTS` without a verified dedicated test database.

```powershell
$env:ENVIRONMENT='test'
$env:DATABASE_URL='postgresql://phase0:phase0@127.0.0.1:9/phase0?connect_timeout=1'
$env:REDIS_URL='redis://127.0.0.1:9/15'
$env:AWS_EC2_METADATA_DISABLED='true'
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth.py tests/test_superadmin_guard.py tests/test_superadmin_dashboard.py tests/test_superadmin_organizations.py tests/test_superadmin_login_history.py tests/test_superadmin_feedback.py tests/test_startup_pipeline_data_preservation.py tests/test_startup_preserves_pipelines.py -q --tb=short
.\.venv\Scripts\python.exe -m alembic heads
```

Check each exit code; stop on failure. The baseline report records actual results, including existing warnings and the unrun deployment/PostgreSQL checks. Generated schemas/check results/inventory are reproducible; browser/font/build version changes can alter screenshot pixels and metadata.
