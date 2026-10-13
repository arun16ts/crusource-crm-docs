# Phase 1 review package

9 October 2026. **COMPLETE — local backend implementation and verification.** 139 targeted backend tests passed, including real PostgreSQL migrations/races; both existing browser suites passed. Production cutover is deferred until the compatible Phase 2 UI and Phase 6 release checks.

The backend now provides owner-only staff invitations, resend/cancel, staff listing, explicit sign-in reset and revocation. Activation consumes a single-use link and requires MFA before granting access. Enrollment resumes through its existing cookie without extending expiry or resetting attempts. Durable encrypted email jobs commit with invitations and dispatch afterward.

- [Architecture and transaction decisions](ARCHITECTURE.md)
- [Phase 2 API handoff](API_HANDOFF.md)
- [Generated router OpenAPI](platform-auth.openapi.json)
- [Migration, configuration and rollback runbook](RELEASE_RUNBOOK.md)
- [Verification evidence](VERIFICATION.md)

This is backend work. CRM-aligned staff screens, developer terminology removal and frontend invitation management belong to Phase 2. Demo intake, pipeline boards and support tickets retain their later phases. TanStack Query owns API state and Redux owns shared UI preferences when those screens are implemented; Phase 1 introduces no frontend state stores.

The compatible frontend is now implemented locally: [Phase 2 review package](../superadmin-phase2/README.md). It delivers the shared CRM workspace and staff-facing invitation/authentication workflows, with real Next.js/API fixture verification. Production cutover retains the release checks below.

The existing public access/review/revoke writers return `410`; their historical read endpoints remain owner-only. Do not deploy this backend independently of the replacement owner workflow. No live email was sent and no application database was migrated during local verification.
