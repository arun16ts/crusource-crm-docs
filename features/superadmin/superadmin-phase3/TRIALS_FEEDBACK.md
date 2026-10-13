# Phase 3D / 3E — trial review and Feedback

Date: 10 October 2026. Status: **COMPLETE — local implementation and verification.**

This package continues the committed Overview, Organizations and Login History work. Starting revisions: frontend `a4864f87`, backend `4e3d075`. Current application changes remain local and uncommitted. No push, deployment or application-database migration was performed.

## Trial reviews

The pre-3D committed approval handler was reproduced in disposable native PostgreSQL with two concurrent reviewers. Both returned approved for the same request, two SubscriptionHistory rows committed, and only seven extension days remained. That was a real lost-update/integrity defect, independent of browser request counts.

The guarded review handler now acquires the existing platform security-writer transaction lock, reloads current credential/session/user authority, checks the command receipt, and delegates one business action. Request, organization and subscription rows are locked; organization locking also protects creation of a missing subscription and different requests for the same organization. The business handler flushes under this boundary. Request, organization, subscription, history and receipt commit together. No external network work runs under these locks. Ordinary reads do not acquire a new business advisory lock.

`Idempotency-Key` is an optional UUID header for compatibility; the new UI always sends it. Matching actor/action/resource/key and body return the committed result. Different input under that key conflicts. Revalidation precedes replay, so revocation blocks both new writes and receipt replay. Receipts use the existing 24-hour retention/cleanup mechanism. A new key against an already reviewed request returns `409`, never another extension.

Approve/reject bodies add optional `expected_updated_at`. The UI uses the authoritative detail response; UTC-normalized mismatch and non-pending state return `409`. Notes and day bounds remain intact. Approval still extends from a future expiration, or from now when expired. The existing rule resetting the subscription/organization to trialing is preserved; this phase introduces no paid/canceled eligibility policy change.

The list uses URL-owned status/search/page/limit/created-order, stable creation-time/UUID ordering and bounded server pagination. Global pending count is labelled separately from the matching table total. Dialogs store a selected ID and local drafts, resolve the current row through a guarded detail query, and handle conflict/refresh or uncertain retry explicitly. An uncertain retry retains the exact body and key. The copied server entity and obsolete trial UI Redux slice/components were removed after tracing callers.

Invalidation remains within the current staff/session key namespace: trial lists/details; on approval, organization lists and the affected organization's summaries/details, plus Overview. It does not invalidate unrelated Feedback, login history or CRM queries.

## Feedback and protected screenshots

Screenshots were actually stored as data URLs in `UserFeedback.client_metadata.images`, not private storage-object references. The old admin list returned those bodies and rendered arbitrary stored strings as image URLs.

The new UI asks for `include_images=false`. The repository defers the full JSON metadata on the paginated ORM read, then projects metadata with `images` removed and an array count in one bounded SQL query for visible IDs. There is no per-record image query. The response adds attachment indices; image bodies stay out of list responses. The default legacy response remains compatible for existing callers.

`GET /api/v1/superadmin/feedback/{id}/images/{index}` uses the platform cookie/origin/custom-header guard and returns a bounded raster response with `private, no-store`, `nosniff` and an explicit media type. Server-side validation shares the customer UI's two-image, 5 MB per-image PNG/JPEG/WEBP/GIF limits and verifies MIME/signature/base64. SVG, remote URLs, malformed metadata and unavailable historical images do not become public or external fetches. No permanent public media route or new storage system was introduced.

The viewer fetches the selected image through the platform transport, renders an ephemeral blob URL and releases URLs/cache entries on navigation/close. The shared dialog supplies focus trapping and Escape dismissal. Stable table column definitions prevent action buttons remounting when viewer/dialog state changes; a browser regression reproduced the missing focus return and verifies the correction. Screenshot navigation uses buttons and arrow keys; narrow/mobile layouts and focus return are verified in browser tests.

The focused Feedback screen uses URL search/category/minimum rating/organization/date/page/limit and the shared server table/pagination. UTC date presets/custom windows use an additive exclusive `date_before`; legacy inclusive `date_to` stays available. Invalid date ranges suppress the list query. Statistics remain independent, explicitly labelled platform-wide or organization-wide. Loading, authoritative empty results, initial errors, stale refresh errors and retries are separate states. Comments/tags render as text. Customer feedback ownership, collection and trigger flows remain unchanged.

## Evidence and verification

Recorded evidence: [baseline browser reads](trials-feedback/baseline/routes.json), [final real-route matrix](trials-feedback/after/routes.json), [native trial defect before](trials-feedback/trial-concurrency-before.json), [native review outcomes after](trials-feedback/trial-concurrency-after.json), [Feedback scale comparison](trials-feedback/feedback-scale.json), [frontend checks](trials-feedback/frontend-checks.json), [backend checks](trials-feedback/backend-checks.json), and source fingerprints for [frontend](trials-feedback/frontend-source-proof.json) / [backend](trials-feedback/backend-source-proof.json). Browser tests use actual Next.js routes/proxy, FastAPI handlers and real platform guards with synthetic identities in an isolated in-memory database; native transaction/migration tests use disposable PostgreSQL and Redis. The main localhost:3000 application was not listening when checked through Chrome DevTools MCP. Fixtures are local integration evidence, not authenticated staging or real-mail evidence.

The 1,000-record native PostgreSQL Feedback fixture contained two valid raster screenshots per record. Both reads returned 25 rows at offset 500 and total 1,000. Legacy response: 4,384,670 bytes, about 70 ms query plus serialization. Slim response: 11,020 bytes, about 42 ms. These are local observations, not production latency guarantees. Slim reads used three set-based statements (count, bounded page, metadata projection), without image-body transfer or N+1 queries. Counts still require database work, and projecting legacy JSON still requires PostgreSQL to read/decompress the visible records' metadata.

The audit retains the shared CRM frame comparison, full application CI regressions, clean migrations/drift, authorization and staff provisioning regressions. Development StrictMode can start then cancel a read before its successful replacement; successful responses are recorded separately from request attempts. No new polling was added.

## Final acceptance and screenshots

Frontend: clean lockfile install; complete changed-file formatting (23 current modified/new supported files); full lint (0 errors, 1,482 repository warnings); all current CI unit/localization/spreadsheet/Loop/public contracts; types; every required browser command; safe-config production build; dependency audit. Additional Phase 1/2/3 platform auth, actual-route, provisioning, CRM session startup and review tests passed. Modified/new frontend files match the final validation checkout byte for byte, and superseded files are absent. No new repository/worktree was created.

Backend: Ruff, compile, committed migrations, full suite **1,976 passed / 60 skipped**; required Redis **33**, webhook/production PostgreSQL **59**, recovery/startup/import PostgreSQL **10**, separate empty-database migration drift **1**, Alembic check and native platform PostgreSQL **35** passed. The last group includes ten new trial/projection/scale checks. Required opt-in groups were run explicitly rather than treated as covered by SQLite. No model/schema change or migration was introduced; the single head remains `20261009_merge_exports_platform`.

Final actual-route tests cover 61 synthetic requests/reviews, 25-row pagination, approval, rejection, competing-review conflict, exact body/key retry after committing then dropping a response, detail refresh, readonly details, CRM bearer rejection, missing CSRF, URL reload/back/forward, filtered/global labels, initial/refresh errors, authoritative empty results, invalid date-query suppression, valid raster decoding, screenshot keyboard navigation/focus return and ten seconds of idle Feedback without a list/image poll. Portable tests additionally prove blob URLs are released on navigation/close. Earlier packages' actual Overview/Organizations/Login History routes and regressions were rerun.

Screenshots: final [trial desktop](trials-feedback/after/trial-extensions-1440.png), [trial mobile](trials-feedback/after/trial-extensions-390.png), [desktop review dialog](trials-feedback/after/trial-dialog-1440.png), [mobile review dialog](trials-feedback/after/trial-dialog-390.png), [Feedback desktop](trials-feedback/after/feedback-1440.png), [Feedback mobile](trials-feedback/after/feedback-390.png), [viewer](trials-feedback/after/image-dialog.png), [mobile viewer](trials-feedback/after/mobile-image.png), and [200% CSS scaling](trials-feedback/after/feedback-css-200percent.png). The folder also contains 1024/768px captures and numbered filtered/empty views. Instrument Sans was registered and loaded at each reference width; heading/content bounds and dialog keyboard behavior passed. CSS scaling is not a claim of testing every browser zoom setting. Images and identities are synthetic fixtures.

The extra deterministic CRM-frame comparison passed identical screenshots against the pre-merge frame at expanded/collapsed 1440, 1024, 768 and 390px. It blocks only a locally injected Kaspersky host; the historical unmodified extra test's antivirus failure was not reclassified as an application success. Application and antivirus settings were unchanged. Earlier supplemental route failures came from Node's inability to resolve `superadmin.localhost`; test-only helpers now use browser requests for authenticated checks and explicit loopback for intercepted/anonymous requests. All final route suites passed.

Final Graphify update exited 0. Existing parser/dependency and inaccessible old validation-directory warnings remain. Generated graphs are supporting context, not implementation evidence. Local browser runs use Windows Edge; Linux/Chromium remote CI has not been run or claimed. Main localhost, stage/provider credentials and deployment checks remain distinct from fixture verification.

## Release and separate policy limits

The disposable PostgreSQL and Redis test containers were removed after verification. The original local `crusource-postgres` and `crusource-redis` containers remain running on ports 5432 and 6379.

Backend deployment must precede the frontend's new detail/image reads; retain existing staff MFA, cookie, CSRF and origin configuration. There is no new schema migration in this package. Stage/Vercel/ECS identity, live staff/customer accounts and actual provider delivery remain Phase 6 release verification. Local success does not prove them.

The pre-existing trial eligibility rule for already paid/canceled subscriptions, customer submission concurrency, and very large synchronous login-history export duration/disk budgets are separate policy/scale decisions. This package makes review transactions safe without silently changing those rules or adding unrelated exports, billing administration or capability features.
