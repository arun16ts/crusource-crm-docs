# Phase 2 review package

9 October 2026. **COMPLETE — local implementation and verification.** Production rollout and live recipient delivery remain release checks.

Super Admin now uses the CRM workspace frame, font, tokens, navigation primitives, tables and buttons. The owner manages Invitations and Staff from Platform Access. Staff use invitation activation, password setup and authenticator enrollment, with a cookie-based enrollment resume flow. Public access applications and developer-login terminology have been removed from these screens.

- [Architecture and state ownership](ARCHITECTURE.md)
- [Verification and reproduction](VERIFICATION.md)
- [Screenshots](SCREENSHOTS.md)
- [Phase 3 handoff](PHASE_3_HANDOFF.md)
- [Approved implementation specification](../SUPERADMIN_PHASE_2_IMPLEMENTATION_PLAN.md)

Visible changes: a 236px collapsible sidebar (64px collapsed), 64px workspace header, CRM inset content frame, mobile navigation, staff sign-in/activation/MFA screens and an Invitations/Staff management area. Owner commands include invite, resend, cancel, reset sign-in and revoke. Lists support server pagination, search and invitation status filters. Route/host helpers preserve short platform-host aliases and full `/superadmin/...` routes.

Existing overview, organization, login-history, trial-extension and feedback content is integrated with the new shell and isolated session/query handling. Its complete page redesign remains Phase 3. Demo intake/board and customer support tickets remain Phases 4 and 5.

## Invitation configuration incident

The user's local invitation request returned 503 because `SUPERADMIN_DELIVERY_KEY` was absent. The Phase 1 migration was present; the failed command rolled back without creating an invitation or delivery job. A fresh dedicated key was generated directly into the ignored local backend `.env`, without displaying or committing it. Existing MFA material was preserved. The development backend reloads changed Python modules.

Configuration rejection now returns the stable `delivery_not_configured` code. The dialog displays that known failure and allows editing/closing. Network, timeout and other server failures still retain the exact action key/body for a safe retry. Missing/invalid keys and invalid activation origins have regression coverage.

Read-only SES checks confirmed the configured sender was verified, account sending was enabled, quota was available and production access was enabled. These checks did not send email. After the user's retry, aggregate read-only database checks showed one delivery with **sent** status and its invitation **enrolling**. This establishes provider acceptance and activation progress, not completed MFA enrollment or mailbox placement guarantees. The durable dispatcher runs every 30 seconds. Preserve the delivery key across restarts; replacing it would make queued encrypted material unreadable.

## Review boundary

No dependency upgrade or new database migration was introduced. The application database was inspected read-only for this incident; all mutating automated workflows used synthetic, isolated databases and fake mail. No real invitation was sent by the implementation agent. The local key configuration is outside Git. No commit, push or deployment was performed.

Source starting revisions: frontend `0276a54d83c08507648dee964cbaaa602d62d5af`; backend `33a6ff4ae16b13c25e04af516a402b38f3d1afd1`; docs `af481069a8a4f9677b6247166825fbe4d370e911`. Phase 1 backend work already existed uncommitted; this phase preserves it and adds a narrow configuration-error fix and tests.
