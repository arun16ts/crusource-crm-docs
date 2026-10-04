# Public-page analytics setup

Implemented locally on 4 October 2026. Provider accounts have not been connected and no production deployment was performed. This change covers public-page collection; Super Admin analytics reports, Error Center, centralized log search and authoritative AI-usage dashboards remain separate work.

## Configuration

The frontend includes the official `@vercel/analytics` and `mixpanel-browser` SDKs. Configuration names and disabled defaults are in `crusource-crm-frontend/.env.public-analytics.example`; it contains no credentials. Configure values in Vercel's deployment settings, then rebuild. `NEXT_PUBLIC_*` values are browser-visible build-time configuration.

1. Complete the approved public privacy disclosures and choose the analytics data region before enabling collection. No optional tracking runs with the checked-in defaults.
2. Enable Web Analytics in the Vercel project, following the [Vercel setup guide](https://vercel.com/docs/analytics/quickstart). Set `NEXT_PUBLIC_VERCEL_ANALYTICS_ENABLED=true` when ready.
3. Create the Mixpanel project in the chosen region. Set its **public browser ingestion token** as `NEXT_PUBLIC_MIXPANEL_PUBLIC_TOKEN` and its region as `NEXT_PUBLIC_MIXPANEL_REGION` (`us`, `eu`, or `in`). Regional endpoints follow the [Mixpanel JavaScript SDK guidance](https://docs.mixpanel.com/docs/tracking-methods/sdks/javascript). Reporting/service-account secrets belong on the backend, never in these browser settings.
4. Set `NEXT_PUBLIC_PUBLIC_ANALYTICS_ENABLED=true` for the production deployment only. `NEXT_PUBLIC_VERCEL_ENV` must be `production`; development/preview builds remain excluded. Vercel normally supplies the deployment environment. Public visitors must additionally choose Allow before either SDK collects events.
5. Verify one synthetic public visit and FAQ interaction in the provider dashboards. Check that search parameters, fragments and questions are absent. Check Decline, revocation, private routes and browser blocking. Provider delivery is best-effort; account connectivity has not been verified locally.

## Collection contract

Vercel receives page views for explicitly published public routes. Its `beforeSend` hook strips query parameters and fragments, and drops protected routes and unknown slugs. It also checks the current route and consent at send time, including after client navigation. No Vercel custom events are enabled by this change.

Mixpanel receives three curated event types:

| Event | Meaning | Properties |
|---|---|---|
| `public_page_viewed` | Published public route visited | Published path, EN/NL locale, environment |
| `faq_answered` | Published FAQ opened on the FAQ page or answered locally in chat | Same plus approved FAQ ID, page/chat surface, content revision |
| `public_ai_answer_viewed` | AI-sourced answer displayed when the browser stream finishes without cancellation | Published path, locale, environment |

`public_ai_answer_viewed` measures browser engagement. It does **not** debit allowance or prove a billable dispatch/completed provider request. The existing backend `public_ai_dispatched` and `public_ai_finished` logs remain the authoritative dispatch/outcome records, including failures and cancellations. Browser blockers or disconnects can omit engagement events. Static FAQs never emit an AI usage event.

Search text, questions, transcripts, CRM records, authenticated identities, URLs with queries, referrers and arbitrary event properties are excluded. Mixpanel autocapture, automatic page views, replay, heatmaps, IP-based geolocation and persistent visitor identity storage are disabled. A send hook removes implicit SDK URL/referrer properties and accepts only curated events/properties. Anonymous in-memory IDs can exist during the page session; a visitor can receive a new ID after reload, so cross-session funnel attribution is intentionally limited.

The optional EN/NL consent control supports Allow/Decline, changing the preference and changes from other tabs. Do Not Track and Global Privacy Control override Allow. Preferences use a versioned local-storage key; inaccessible storage leaves collection disabled. Revocation blocks future sends and resets the anonymous SDK identity; already dispatched requests cannot be withdrawn. No SDK is initialized before consent, and analytics initialization failures do not interrupt product interactions.

## Verification

`npm run test:public:analytics` uses real provider/service code with offline SDK doubles. It checks no initialization before consent, decline/re-enable/revoke, exact property redaction, regional SDK configuration, public/protected navigation, one initialization, GPC override and failed-provider isolation. No provider accounts or paid AI calls are used. Run `npm run test:public:browser`, TypeScript and localization checks alongside it.

Release this collection layer with the public-page changes. Keep it disabled until the provider/project setup and approved public policy are ready. Do not claim that collection completes the separate Super Admin upgrade.
