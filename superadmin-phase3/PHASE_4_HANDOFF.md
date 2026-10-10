# Phase 4 handoff — demo requests and platform sales pipeline

Phase 3 supplies the existing protected screens, shared CRM frame, platform session/transport boundaries, URL view state, bounded server reads and guarded command/retry patterns. See [the review package](README.md) and [trial/Feedback contracts](TRIALS_FEEDBACK.md). Local verification does not replace operational release checks.

The next authorized development package should follow Phase 4 of [the phase-wise roadmap](../SUPERADMIN_PHASE_WISE_IMPLEMENTATION_PLAN.md): public demo-request intake and a staff board/list. It is not implemented by Phase 3.

- Trace current public landing, billing sales modal, locale routing and navigation before choosing intake links and English/Dutch paths.
- Keep demo enquiries as platform sales records, separate from tenant CRM Leads and Organizations. Anonymous intake must not expose list/detail reads or disclose previous enquiries.
- Use a focused backend module with typed commands/queries, repository persistence, manually registered routes and additive migrations. Queue durable delivery after commit; do not wait for email to acknowledge intake.
- Carry bounded idempotency, input/body limits and shared abuse controls into public intake. Staff commands retain cookie/MFA/origin/custom-header/CSRF and gain the roadmap's explicit capability decisions; do not make all future actions owner-only by accident.
- Board loading must be bounded per column with server counts; list pagination alone cannot represent a complete board. Moves need stable stages, expected-version checks, conflict handling and immutable history.
- Keep shared server state in TanStack Query and shareable filters in the URL. Add navigation/permission decisions intentionally. Do not introduce tenant impersonation or treat Converted as paid revenue or automatic account provisioning.
- Run complete frontend/backend/migration checks and actual-route/browser tests before calling the next package ready. Separately verify real deployed origins/cookies, provider delivery, Vercel/ECS commits and customer/staff flows before release.

No Phase 4 implementation, push or deployment is included in this handoff.
