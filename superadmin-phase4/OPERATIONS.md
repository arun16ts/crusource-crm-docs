# Phase 4 configuration and recovery

## Configuration

| Setting                                | Implemented behavior                                                                                                                               |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEMO_IP_LIMIT`                        | Default 5 attempts per client IP per 600 seconds                                                                                                   |
| `DEMO_EMAIL_LIMIT`                     | Default 3 accepted new enquiries per normalized-email digest per 3,600 seconds                                                                     |
| `REDIS_URL`                            | Existing shared Redis service; admission fails closed in production/prod/staging/stage if unavailable                                              |
| `DEMO_NOTIFICATION_STAFF_IDS`          | Comma-separated approved platform staff UUIDs; unset queues no notification. Only currently active, MFA-eligible managing staff/owner are accepted |
| `SUPERADMIN_FRONTEND_URL`              | Trusted portal origin for protected notification links; no supplied public return URL is used                                                      |
| Existing SES sender/region/credentials | Existing SES client configuration; restricted verified sender and IAM permissions must be verified operationally                                   |
| `BUSINESS_NOTIFICATION_RETENTION_DAYS` | Default 30, minimum 1; removes sent/superseded outbox rows after retention                                                                         |

ASGI trusted-proxy configuration determines client IP. The intake handler ignores caller-controlled forwarding headers. Confirm that the actual ingress/Next proxy and backend trust configuration resolve useful client identities before publishing; a shared proxy address must not accidentally become every visitor's quota identity. Use Redis Cloud only through the deployed secret, with the provider's actual TLS URL; local/CI Redis remains disposable/local. Never put authenticated connection URLs in evidence.

Contact-purpose consent is recorded as `demo-contact-v1` with a server timestamp. Public copy, eligible recipient setup and a sales-record retention policy need operational ownership before publication. Enquiries, internal notes and activity are retained; no automatic deletion/export workflow was added. Expired intake receipts are removed by the scheduler and lazily on key reuse. Failed notification jobs remain visible for investigation; sent/superseded jobs have the retention above.

## Durable delivery

`business_notifications` is a reusable business outbox, separate from the invitation outbox whose activation-generation and encrypted-token contract remains intact. Demo intent contains only demo ID/reference and configured recipient ID. The scheduler drains up to 25 due jobs every 30 seconds. Claiming acquires a two-minute fenced lease and rechecks current recipient eligibility; ineligible jobs become superseded. No database lock is held during the SES request. This means a message already handed to a provider cannot be recalled if authority changes during that request.

Provider calls use bounded timeouts and one SDK attempt per dispatcher attempt. Retryable failures back off and stop after six completed unsuccessful attempts; permanent failures stop immediately. A worker crash can leave a sending lease to be reclaimed. Provider acceptance followed by a crash before recording it can produce a duplicate email, so delivery is at least once. A `sent` status means provider acceptance, not inbox delivery. Public acknowledgement does not wait for any of this.

The mail contains a minimal reference and protected portal link, without customer email, phone or message. Missing/invalid origin, rejected provider delivery and uncertain delivery produce safe status codes without raw provider exceptions or credentials. Browser detail exposes notification IDs/statuses to managers and polls pending delivery; it does not expose recipient addresses/provider internals.

## Migration and recovery

Migration head is `20261011_platform_sales`, descending from `20261009_merge_exports_platform`. It adds credential grants/revision with a positive revision constraint and five tables: `demo_requests`, `demo_request_activities`, `demo_request_notes`, `demo_intake_receipts`, `business_notifications`. Deterministic stage/order, assignee, follow-up, history, notes, expiry and due-job indexes support bounded access. Search uses escaped literal `ILIKE`; no speculative full-text search or configurable pipeline was added.

Requester/org/assignee/actor foreign keys become null on referenced deletion; deactivation preserves names and eligibility warnings while records exist. Notes/activity reference the aggregate with cascade on an explicit database deletion; the application exposes no aggregate deletion command. Current API maintains append-only activity/notes.

Downgrade refuses populated sales/outbox tables and nonempty staff grants. An empty-schema downgrade/upgrade is tested. Preserve enquiries and restrictive grants during recovery: roll back compatible frontend/backend code, stop the intake route at ingress if needed, and disable the business scheduler job while investigating delivery. Merely unsetting recipient configuration affects future enqueueing and does not cancel already committed jobs. Do not drop populated tables or re-enable legacy public staff applications.

The local PostgreSQL migration tests cover clean full history, upgrade from the previous merged head, invitation/staff preservation, model/schema drift and destructive-downgrade refusal. These are disposable database tests, not an upgrade of the running CRM database.

Before deployment, complete the cross-stack audit in AGENTS.md. Deploy the additive schema, compatible backend, then frontend. The migrator must run with `SKIP_MIGRATIONS=false` and `python scripts/run_migrations.py` before API rollout, and use the same intended database as the API. Verify revision against image heads and migration logs, exact successful CI/image commit, Vercel API origin, proxy/CORS/cookies/CSRF, Redis, scheduler, SES and schema-dependent stage flows. No release action was performed by this package.
