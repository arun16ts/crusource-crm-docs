# Public pages and chatbot implementation

Date: 4 October 2026. Implemented locally; no production deployment or external analytics account setup was performed.

## Delivered

- Shared public navigation and shell; landing resources section; corrected footer destinations and CRM Sign In label. Unsupported latency, hallucination, encryption/certification and uptime claims were removed from active public copy. The illustrative landing workstation is labeled as sample data; reduced-motion preferences disable its automatic tour and smooth scrolling.
- Public routes bypass the existing Redux persistence gate, so published content renders on the server without waiting for browser storage/auth rehydration. Private routes retain their existing gate. Navigation stays within desktop and mobile viewports.
- Nine EN/NL task guides at `/docs/[slug]`, with prerequisites, steps, troubleshooting, breadcrumbs, contents and adjacent-guide links. Search uses URL parameters. Published slugs are explicit; unknown slugs return 404.
- FAQ search/category URL state, native keyboard-accessible accordions and question permalinks. The FAQ page and widget use the same published EN/NL answers.
- Integration catalogue filters and detail pages. Google is Limited/Beta with scope/configuration limitations. All Buddy is Planned because no wired Crusource connection was found. Automatic synchronization and duplicate-protection promises were removed.
- `/security` overview and honest informational `/privacy`, `/terms`, `/contact` destinations. Formal policies, support contact and contact submission delivery are pending the user's later details. No form reports a fabricated success.
- Public chatbot FAQs remain free at zero allowance and during Redis/provider outages. Typed matching is deterministic and locale-aware; unrelated questions are no longer answered by a loose keyword match.
- Shared Redis allowance: five dispatched AI requests per signed anonymous visitor per UTC day. Reset is midnight UTC (05:30 Asia/Calcutta), shown in the visitor's timezone. Resetting the conversation does not reset usage. Legacy browser lifetime counts are discarded.
- Atomic Lua checks cover request replay/fingerprint, per-visitor active streams, global concurrency and a daily global dispatch ceiling. One public model attempt, SDK retries disabled, input/output bounds and a 60-second stream timeout. Post-dispatch failures/cancellations remain counted. Static answers and pre-dispatch provider unavailability are free.
- Same-origin public API cookie transport, `/api/v1/ai/public-usage`, named SSE source/usage/error events and network-chunk-safe parsing/stream cleanup. Markdown links reject unsafe protocols. Error payloads exclude provider exception details; structured logs record request ID, dispatch window/count and outcome/latency without question text.

## Content maintenance

Edit frontend `src/data/publicFaqs.json`, then run `npm run sync:public-knowledge` from the frontend. It generates the backend published knowledge file and legacy FAQ translation keys. `npm run test:public` checks streaming/matching and that both repositories contain the same published answers. Release the frontend and backend together when changing this contract.

Guide content lives in `src/data/publicGuides.json`. Keep supported-step and availability claims tied to actual UI/API behavior. The maintained feature inventory was updated only for this scope.

## Verification

- Backend: 29 targeted checks passed, including real Lua execution against the existing local Redis in a unique temporary key namespace. Covers concurrency, replay, lease/global caps, UTC boundary, outages, signed cookie transport, input validation, safe errors and cancellation. CRM data was not modified; no paid AI calls were made.
- Public streaming test passed for byte-split events, Unicode, metadata, safe error events, stream cancellation and exact matching.
- Browser fixture passed using actual components/hooks and fake APIs: free FAQ at zero, server reset timer, dispatch usage, conversation reset separation, legacy migration, outage FAQ access, anchors, URL reload, availability filters, mobile navigation and EN/NL rendering.
- Live Next.js route checks passed for 11 pages, page-specific canonical links and unknown guide/integration slugs.
- Live browser smoke tests passed against the running frontend on `localhost`: actual rendering, desktop EN/NL and mobile navigation bounds, hydrated search URL changes and Dutch preference continuity. The `127.0.0.1` browser origin encountered development HMR WebSocket resets; the live browser script defaults to the dev server's `localhost` origin.
- TypeScript and localization verification passed. Focused ESLint found no errors; the shared SSE client's pre-existing citation `any[]` warning remains.
- Review screenshots are under `storage/public-pages-review/`. The existing translation browser expectation was updated for the reviewed FAQ wording; its authenticated mutation flow was not executed against live CRM records.
- Graphify code graph was refreshed. Existing graph extraction warnings concern an unrelated forecast component, an unsupported SQL parser dependency and an empty TOML extraction.
- Follow-up public analytics checks passed with offline SDK doubles: opt-in/decline/revocation, GPC, regional configuration, property/URL redaction, protected-route exclusion and provider failure isolation. Existing public browser tests and TypeScript passed again. Focused ESLint has no errors; the root layout's existing custom-font warning remains.

## Runtime and deployment

The Redis client already pinned in backend requirements (`redis==5.0.3`) was missing from the local venv and has been installed. No database schema or Alembic migration was needed.

Backend settings:

| Setting | Behavior/default |
|---|---|
| `REDIS_URL` | Shared Redis required for public provider dispatch; static FAQ stays available without it |
| `ENVIRONMENT` | Use production/staging in hosted deployments so visitor cookies are Secure |
| `PUBLIC_AI_ENABLED` | `true`; set `false` to stop provider dispatch while keeping public content |
| `PUBLIC_AI_MODEL` | Existing public default `gemini-2.5-flash`; confirm provider availability in your account |
| `PUBLIC_AI_MAX_CONCURRENT` | `20` global active streams |
| `PUBLIC_AI_GLOBAL_DAILY_LIMIT` | `1000` global daily dispatches; this is an operation cap, not a currency budget |

Keep provider credentials server-side. Configure trusted Vercel/AWS proxy address resolution at the ASGI/deployment layer; the app does not trust arbitrary forwarded-IP headers. The shared request guard applies 15 requests per observed client address per ten minutes independently of the AI allowance. The Redis endpoint must support the multi-key Lua operations used here.

The debit commits immediately before provider invocation, after provider readiness/config preparation. There is no long-lived reservation stage (`reserved` is zero). A crash between that conservative debit and external invocation may retain a debit; external exactly-once execution is not promised. Visitor cookies are not proof of a unique person, so aggregate limits also apply.

## Remaining work

- Publish the user's approved company policies and support contact/delivery flow when supplied.
- Vercel/Mixpanel public engagement collection is now wired with production-only opt-in, sanitized published routes and curated FAQ/AI-answer events. It stays disabled until provider accounts and policies are configured. See `public_analytics_setup.md` for settings and checks. Backend dispatch/outcome logs remain authoritative for AI usage. Super Admin provider reports, Error Center/settings/usage views and ticket creation remain separate work.
- Establish production performance baselines and carry out staging/provider-account checks and deployment. No performance numbers or compliance certificates were invented.
- A separately authenticated customer portal, new screenshots from authorized real workspaces and broader editorial content remain future scope.
