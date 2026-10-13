# Landing Page and Public Pages Upgrade Plan

Date: 4 October 2026
Status: public-page/chatbot core and opt-in public analytics wiring implemented and locally verified. Approved company policies/contact details, production rollout, analytics account activation and the separate Super Admin integration remain pending. See `landing_public_pages_implementation_report.md` and `public_analytics_setup.md` for delivered scope, checks and activation settings.
Hosting context: frontend on Vercel, backend on AWS. Coordinate analytics and error reporting with `superadmin_upgrade_plan.md` rather than creating competing systems.

## Goals

Upgrade the landing page, Docs, FAQ, Integrations and Client Portal entry into one coherent public experience. Correct the public chatbot so static FAQ answers are free, AI usage is measured on the server only when a provider request is actually dispatched, and usage resets on a defined schedule.

Applied defaults after approval to proceed: five provider dispatches per anonymous visitor per UTC day; FAQ access remains unlimited. Client Portal is relabeled CRM Sign In and uses the existing login. A separate customer portal requires its own authorization design. The user confirmed that approved policy documents and support contact details will be provided later.

## Verified pre-upgrade baseline

| Area | Finding |
|---|---|
| Landing | Localized `[locale]/page.tsx` with Hero, WhySection, AIWorkflowsShowcase, FinalCTA and a public chatbot; separate Navbar and MarketingNavbar implementations |
| Docs | A client page with a local topic selection/search over `PUBLIC_DOCS_SECTIONS`; topic/search state does not have shareable routes |
| FAQ | A client page using `PUBLIC_FAQS`; category/search/expanded state is local |
| Integrations | Local catalogue in `publicKnowledgeBase.ts`, with All Buddy and Google Workspace descriptions; no explicit implementation/readiness field |
| Client Portal | Footer label links to `/login`; no dedicated customer portal implementation was found in the reviewed frontend/backend sources |
| Other public links | Privacy, Terms, Security and Contact currently also link to `/login` |
| Chatbot browser quota | `MAX_PUBLIC_QUESTIONS = 5`; counts both FAQ and AI paths; persists a plain lifetime count in localStorage without a reset timestamp |
| Chatbot blocking | Quota check runs before FAQ lookup; FAQ buttons are disabled at zero; the composer is replaced when allowance is exhausted |
| Backend limiter | In-memory per-process limiter of 15 requests per IP over 600 seconds; not the same policy as the frontend quota |
| Provider | Public handler calls the Gemini provider, which can attempt several models and then return a canned fallback; there is no usage/source metadata contract |
| Public knowledge | FAQ page content, translated chatbot answers and provider instructions/fallback can diverge; matcher uses simple keyword scoring |

Source evidence: frontend `src/app/[locale]/page.tsx`, `src/app/docs/page.tsx`, `src/app/faq/page.tsx`, `src/app/integrations/page.tsx`, `src/components/landing/{Navbar,MarketingNavbar,Footer,PublicLoopAIChat}.tsx`, `src/hooks/ai/{usePublicAIChat,useLandingFaqs}.ts`, `src/data/{landingFaqData,publicKnowledgeBase}.ts`, `src/services/aiChatService.ts`; backend `src/modules/ai_chat/routes/ai_routes.py`, `handlers/ai_chat_query_handler.py`, `services/providers/gemini_provider.py`.

## Shared public-site foundation

Preserve the Crusource orange identity, but reduce visual competition between animated showcases and the primary product explanation. Use one responsive public layout, consistent typography/spacing, accessible navigation, footer, search patterns, breadcrumbs and CTA components. Consolidate Navbar/MarketingNavbar around shared navigation data while retaining intentional landing-page styling.

Recommended navigation: Product, Integrations, Docs, FAQ, Pricing if its published offer is accurate, Sign In and Get Started. Show Resources on mobile with the same destinations as desktop. Keep the chatbot available on relevant public pages without overlapping cookie controls, navigation or mobile form inputs.

Keep content in versioned, typed registries or MDX initially. Do not add a CMS until there is an editorial need. Public routes should be server-rendered/static where feasible; search, filters, accordions, animation and chat are focused client boundaries. Use URL state for shareable searches, selected topics and filters. Add page-specific metadata, canonicals and social images through Next.js metadata conventions. [Next.js metadata guidance](https://nextjs.org/docs/app/getting-started/metadata-and-og-images).

## Page-by-page plan

| Page | Proposed upgrade | Completion evidence |
|---|---|---|
| Landing | Clear audience/problem statement, primary Get Started CTA, secondary product walkthrough, concise module benefits, authentic screenshots, governance/security explanation and resources links | Visitor can understand the product and find signup/docs quickly on desktop and mobile |
| Docs | Getting Started, CRM Modules, Teamspace/Governance, Imports/Exports, Loop AI, Integrations and Troubleshooting; stable `/docs/[slug]` pages, table of contents, breadcrumbs, next/previous links and updated dates | Direct links and reload/back work; search finds instructions by task; actual UI/API steps match docs |
| FAQ | Categories, searchable questions, stable question anchors, related docs links, keyboard-accessible accordions and locale consistency | FAQ answers match chatbot content and remain usable without an AI provider |
| Integrations | Search/filter catalogue, detail pages, supported capabilities, prerequisites, permission scopes, setup guides, limitations and explicit availability | Every Available claim has a working UI/API integration; unsupported claims marked accurately |
| Client Portal entry | Clarify audience, correct label/destination and authenticated routing | Existing CRM sign-in is not presented as a separate customer product |
| Privacy/Terms/Security/Contact | Correct routes and approved content/contact flow | No legal/contact link unexpectedly redirects to login |

Landing structure: Hero -> product walkthrough -> core workflows -> governance and trust -> integrations -> onboarding/pricing summary -> FAQ preview -> final CTA. Use genuine product evidence; do not invent customer testimonials, performance numbers or compliance certification. Review existing claims such as sub-50ms navigation, zero hallucination, encryption and SOC 2 wording against evidence before publishing them. Show sample data as sample data.

Docs should lead with user tasks rather than internal implementation details. Each article includes purpose, prerequisites/permissions, numbered steps, screenshots when useful, common errors and related links. Public docs must exclude secrets, operational admin endpoints and customer information. Contact forms need a real delivery/storage path, spam protection and honest success/error states; do not report success if a submission was not accepted.

For integration cards, use explicit public availability vocabulary such as Available, Limited/Beta, Planned and Unavailable. Keep the maintained feature inventory's existing IMPLEMENTED/PARTIALLY IMPLEMENTED/etc. vocabulary unchanged. Verify each public description against its wired product flow; a service file alone is insufficient proof.

## Client Portal scope decision

Option A: existing CRM sign-in. Relabel the footer as CRM Sign In or Workspace Login, use the existing authentication/recovery flows, and route authenticated users to their authorized workspace. No new customer portal API is necessary.

Option B: a separate customer portal. Plan it as a distinct product phase with customer identity/invitations, tenant and contact/account membership, explicit shared-resource grants, session revocation and its own guarded APIs. Initial scope could be shared documents, submitted requests and visible request status. Never expose internal leads, deals, activities or organization-wide documents through ordinary CRM login or possession of a customer email. Test two customers in the same organization as well as cross-organization isolation. Existing shared-document token routes may inform the design but are not proof of customer-portal authorization. Additional features such as payments, messaging or project tracking require explicit scope.

## Chatbot usage rules

| Interaction/result | AI quota effect |
|---|---|
| FAQ button or exact static FAQ answer | Zero; no provider API call |
| Search or open Docs/FAQ/Integrations content | Zero |
| Ambiguous question with suggested FAQ options | Zero until a provider is actually used |
| Cached answer with no provider invocation | Zero |
| Provider unavailable/configuration missing before dispatch | Zero |
| Request blocked by validation/quota/abuse guard before dispatch | Zero |
| Actual provider request dispatched | One public AI usage unit under the proposed single-dispatch policy |
| Timeout/cancel after dispatch | Remains counted because API usage may already have occurred |
| Reset conversation | Clears conversation only; does not reset quota |

The allowance counts dispatched AI requests, not successful messages or every chat interaction. Provider cost/attempt telemetry is separate. Disable uncontrolled public model fallback/automatic retries initially so one public AI operation cannot silently issue four provider calls. If retries are later introduced, document their visitor-credit policy and record every provider attempt for cost control. A static fallback after a real provider attempt must not be described as a zero-usage FAQ interaction.

## FAQ-first routing and truthful answer labels

1. FAQ buttons pass a stable FAQ ID to a dedicated local-answer action. Do not infer known FAQ selection through fuzzy text or send it to the AI endpoint.
2. Typed questions first use deterministic, locale-aware matching against approved public content. Exact/high-confidence matches return static content; ambiguous matches show candidate articles or an Ask AI option. Avoid a loose keyword match falsely answering an unrelated question.
3. Only unmatched questions selected for AI pass through the server AI budget check and provider dispatch.
4. Public AI uses approved public product knowledge, with links to source pages where supported; it must never query tenant CRM data.
5. Return explicit answer source: `faq`, `ai`, `cache` or `fallback`. Label a canned response as fallback rather than AI-generated.
6. Keep FAQ suggestions and FAQ access available at quota zero. Keep the input usable for FAQ lookup; unavailable AI requests show reset information and helpful docs links.

Use one canonical public content source, with stable IDs, localized text, revision and published state, to generate the FAQ page, chatbot local answers and provider knowledge. Sharing public content does not mean shipping internal developer docs into the browser. Keep rendering and external links sanitized.

## Server-controlled quota and reset window

Recommended initial policy: five AI requests per anonymous visitor per UTC calendar day; automatic reset at 00:00 UTC, displayed in the visitor's local timezone. In Asia/Calcutta that is 05:30. This is a proposal pending the chosen limit/window. A per-hour option uses explicit UTC hour buckets; do not mix rolling and calendar-window semantics.

Implement a focused public usage service backed by shared Redis rather than browser counters or process memory. Use a server-issued opaque visitor identifier in a secure cookie through a same-origin public-chat proxy; browser code must not invent authoritative identities. The quota endpoint and stream must use the same identity transport. On AWS, configure Redis for production shared state and test expiration/restart behavior.

Make reservation/check/expiry atomic, and reject concurrent requests that would exceed the allowance. Bind idempotency records to visitor + client request ID + request fingerprint; reuse must not dispatch again or increment twice. Preserve a bounded completed-response result or return a defined duplicate/in-progress outcome. Atomic counter/expiry needs a transaction or script; a separated INCR/EXPIRE sequence can create race conditions. [Redis counter/rate-limiter guidance](https://redis.io/docs/latest/commands/incr/).

Usage state should include window start/end, used, reserved and remaining. Reserve before dispatch, validate provider readiness, record dispatch exactly once, and release only reservations that never dispatched. Maintain a durable/bounded dispatch ledger as needed to recover abandoned reservations; an uncertain post-dispatch failure must not automatically refund a real API call. Do not promise exactly-once external provider execution across process crashes without provider-supported idempotency; use conservative recovery and surface reconciliation cases.

Return server metadata: `limit`, `used`, `remaining`, `reserved`, `reset_at`, `server_time`, `window_type` and `policy_version`. A proposed `GET /api/v1/ai/public-usage` obtains authoritative state; extend `/ai/public-chat` with a request ID and explicit SSE metadata/source/usage/error/done events. Define transport errors before streaming as HTTP errors; mid-stream failures use typed error events with a safe support reference, not raw exception strings as assistant text. Update the shared SSE service to consume these events correctly.

Migrate away from `crusource_landing_ai_queries_count`; discard its legacy lifetime value because it includes free FAQs and is not trusted usage. Client persistence can cache display state with expiry/policy version, but cannot authorize provider calls. Refresh server usage on open/focus, after dispatch, when the reset time arrives and across tabs. Use server time for eligibility; local clock changes must not reset allowance. Requests dispatched just before a boundary belong to their original window even if streaming completes afterward.

Separate abuse protection from AI entitlement: a shared IP/request-rate guard, bounded input/output, one active stream per visitor and global provider-spend/concurrency controls. Existing 15-per-10-minute behavior can be retained as an initial abuse limit after confirming proxy identity and traffic patterns; FAQ reads have no AI debit. Trust forwarded IPs only from configured Vercel/AWS proxies. A cookie is not a guaranteed unique person; clearing cookies, private browsing and shared networks need aggregate abuse controls. If Redis is unavailable, temporarily disable provider dispatch while preserving static content.

## Analytics, errors and Super Admin controls

Reuse the planned Vercel/Mixpanel integration. Separate `faq_answered` from `public_ai_dispatched` and `public_ai_completed`; FAQ activity is engagement, not paid AI usage. Emit authoritative provider-dispatch usage on the backend and avoid counting the same event twice. Do not send free-text questions, customer information or conversation transcripts to analytics by default.

Log request ID, answer source, content revision, quota decision, reset window, model/attempt count, latency and outcome as sanitized metadata. Feed unexpected public AI failures into the proposed Super Admin Error Center. Track quota-limit responses as expected outcomes unless failure rates indicate a defect.

Provide guarded Super Admin settings for public AI enablement, allowance/window, model/retry policy, provider readiness, spend ceiling and source-separated usage metrics. Changing policy must define the effective window; audit changes and avoid silently granting or revoking visitor allowance midway through a window. Provider secrets remain server-side.

## Delivery phases

| Phase | Deliverables | Acceptance |
|---|---|---|
| 1. Content/navigation audit | Shared navigation/footer, real link destinations, integration/claim evidence, portal scope and canonical content source | No misleading links/claims; approved route map and content outline |
| 2. Chatbot correction | Free FAQ routing, source labels, authoritative quota/reservation, reset metadata and streaming errors | FAQ never dispatches provider/debits quota; AI counts only dispatch; expiry and concurrent/idempotent requests behave correctly |
| 3. Public-page upgrade | Landing composition, shareable Docs/FAQ/Integration routes, locale parity, metadata and accessibility | Mobile/keyboard flows work; direct links/reload/back preserve context; public content renders without AI |
| 4. Portal path | Existing sign-in cleanup or separately approved customer-portal MVP | Chosen audience and authorization are correct; no cross-customer exposure |
| 5. Measurement/rollout | Analytics, error/log integration, performance baseline, quotas/spend alerts and staged rollout | Static vs AI usage is visibly separated; provider failure does not break the site |

Fix the chatbot accounting independently of the visual redesign; that correction should not wait for every public page to be rebuilt.

## Verification

Backend: provider-spy tests for zero FAQ calls, actual dispatch debits, missing-provider/preflight failures, timeout/cancel after dispatch, concurrent reservations, request replay, UTC reset/boundary, Redis unavailability, trusted proxy identity, safe SSE failures and absence of tenant-data access. No paid AI calls in automated tests.

Frontend: FAQ at zero allowance, dedicated FAQ-ID actions, localized matching, server usage updates, stale/local-clock/multiple-tab state, conversation reset without quota reset, message source labels, stream abort/retry and legacy storage migration. Browser fixtures should cover both FAQ and real-provider-test-double paths.

Public pages: link checks, topic anchors/deep links, search/filter URL state, EN/NL content/labels, accessible navigation and accordions, reduced-motion support, mobile chatbot viewport/focus, page metadata and bundle/performance regressions. Establish measured performance baselines before adopting numerical targets. Run relevant backend tests, TypeScript, focused ESLint, localization checks and meaningful browser tests. Customer-portal isolation tests are mandatory if Option B is selected.

Roll out the chat correction in development/staging first, then production using separate switches for AI dispatch and redesigned pages. Keep free content accessible if provider/Redis/telemetry is down. Do not introduce database migrations unless the selected policy/ledger/portal models need them; any new migration must preserve a single Alembic head.
