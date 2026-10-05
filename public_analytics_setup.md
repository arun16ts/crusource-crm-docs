# Public-page analytics setup

Current status: **PLANNED / DOCUMENTED ONLY**, checked against the source on 5 October 2026. The earlier implementation claim is stale: the current frontend has neither `@vercel/analytics` nor `mixpanel-browser` in `package.json`, no source references to those SDKs, no `.env.public-analytics.example`, and no `test:public:analytics` script or matching analytics test. Provider collection is not wired in the current application. The reason for removal has not been established from Git history.

The following configuration and collection contract describe proposed restoration or reimplementation, not existing behavior. Provider accounts and production delivery have not been verified. Super Admin analytics reports, Error Center, centralized log search and authoritative AI-usage dashboards remain separate work; see [the revised upgrade plan](superadmin_upgrade_plan.md).

## Proposed configuration

Proposed implementation: add the official `@vercel/analytics` and `mixpanel-browser` SDKs and create a credential-free `crusource-crm-frontend/.env.public-analytics.example` with configuration names and disabled defaults. The example file does not currently exist. After implementation, configure values in Vercel's deployment settings, then rebuild. `NEXT_PUBLIC_*` values are browser-visible build-time configuration.

1. Complete the approved public privacy disclosures and choose the analytics data region before enabling collection. The new implementation must disable optional tracking by default.
2. Enable Web Analytics in the Vercel project, following the [Vercel setup guide](https://vercel.com/docs/analytics/quickstart). Set `NEXT_PUBLIC_VERCEL_ANALYTICS_ENABLED=true` when ready.
3. Create the Mixpanel project in the chosen region. Set its **public browser ingestion token** as `NEXT_PUBLIC_MIXPANEL_PUBLIC_TOKEN` and its region as `NEXT_PUBLIC_MIXPANEL_REGION` (`us`, `eu`, or `in`). Regional endpoints follow the [Mixpanel JavaScript SDK guidance](https://docs.mixpanel.com/docs/tracking-methods/sdks/javascript). Reporting/service-account secrets belong on the backend, never in these browser settings.
4. Set `NEXT_PUBLIC_PUBLIC_ANALYTICS_ENABLED=true` for the production deployment only. `NEXT_PUBLIC_VERCEL_ENV` must be `production`; development/preview builds remain excluded. Vercel normally supplies the deployment environment. Public visitors must additionally choose Allow before either SDK collects events.
5. Verify one synthetic public visit and FAQ interaction in the provider dashboards. Check that search parameters, fragments and questions are absent. Check Decline, revocation, private routes and browser blocking. Provider delivery is best-effort; account connectivity has not been verified locally.

## Proposed collection contract

Vercel should receive page views for explicitly published public routes. The integration must strip query parameters and fragments, drop protected routes and unknown slugs, and check the current route and consent at send time, including after client navigation. Verify the selected SDK's supported send hook during implementation. Start without Vercel custom events.

Mixpanel should receive three curated event types:

| Event | Meaning | Properties |
|---|---|---|
| `public_page_viewed` | Published public route visited | Published path, EN/NL locale, environment |
| `faq_answered` | Published FAQ opened on the FAQ page or answered locally in chat | Same plus approved FAQ ID, page/chat surface, content revision |
| `public_ai_answer_viewed` | AI-sourced answer displayed when the browser stream finishes without cancellation | Published path, locale, environment |

The proposed `public_ai_answer_viewed` event measures browser engagement. It must not debit allowance or serve as proof of a billable dispatch/completed provider request. The current source also has no `public_ai_dispatched` or `public_ai_finished` log events, contrary to the earlier version of this document. Any authoritative dispatch/outcome reporting must be implemented and verified on the backend, including failures and cancellations. Browser blockers or disconnects can omit engagement events. Static FAQs must not emit an AI usage event.

The implementation must exclude search text, questions, transcripts, CRM records, authenticated identities, URLs with queries, referrers and arbitrary event properties. Keep Mixpanel autocapture, automatic page views, replay, heatmaps, IP-based geolocation and persistent visitor identity storage disabled, verifying supported settings against the selected SDK. The send hook must remove implicit SDK URL/referrer properties and accept only curated events/properties. Anonymous in-memory IDs may exist during the page session; a visitor can receive a new ID after reload, so cross-session funnel attribution is intentionally limited.

The proposed EN/NL consent control must support Allow/Decline, changing the preference and changes from other tabs. Do Not Track and Global Privacy Control must override Allow. Use a versioned local-storage key; inaccessible storage must leave collection disabled. Revocation must block future sends and reset anonymous SDK identity; already dispatched requests cannot be withdrawn. Initialize no SDK before consent, and isolate analytics initialization failures from product interactions.

## Verification

Required implementation checks: add `test:public:analytics` using real provider/service code with offline SDK doubles. Verify no initialization before consent, decline/re-enable/revoke, exact property redaction, regional SDK configuration, public/protected navigation, one initialization, GPC override and failed-provider isolation. Use no provider accounts or paid AI calls. Add or verify the public browser test script before invoking it; neither script is evidence of current implementation. Run TypeScript and localization checks alongside the new tests.

After restoration or implementation, release this collection layer with the public-page changes. Keep it disabled until the provider/project setup and approved public policy are ready. Do not claim that collection completes the separate Super Admin upgrade.
