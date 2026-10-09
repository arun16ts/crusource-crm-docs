# Phase 2 API handoff

9 October 2026. The [OpenAPI snapshot](platform-auth.openapi.json) comes from the registered backend router, without starting the application, scheduler or providers. Source DTOs in `platform_auth/commands`, `queries` and `invitation_schemas.py` are authoritative. Phase 0 demo/support DTOs remain designs.

## Transport and authority

All paths below are relative to `/api/v1/superadmin/auth`. Use the existing same-origin platform HTTP client and HttpOnly `crusource_platform` cookie; do not use CRM bearer/refresh tokens. New provisioning endpoints require the current platform owner. Operators can authenticate and use their existing platform features, but cannot list or manage staff/invitations.

Every browser write supplies `X-Platform-Request: 1`, a trusted `Origin`, and `X-Platform-CSRF` from `/me`. Existing public login/activate/verify use their existing custom-header/origin admission without requiring an authenticated CSRF token. New privileged writes additionally require UUID `Idempotency-Key`; updates require integer `expected_version >= 1`.

| Method/path | Body/query | Success |
|---|---|---|
| POST `/invitations` | `{email, name}` | 202 Invitation |
| GET `/invitations` | `limit, offset, search, status, sort_by, sort_order` | Invitation page |
| POST `/invitations/{id}/resend` | `{expected_version}` | 202 Invitation |
| POST `/invitations/{id}/cancel` | `{expected_version, reason}` | Invitation |
| GET `/staff` | `limit, offset, search, sort_order` | Staff page |
| POST `/staff/{id}/reset-sign-in` | `{expected_version, reason}` | 202 Invitation |
| POST `/staff/{id}/revoke` | `{expected_version, reason}` | Staff |
| GET `/enrollment` | Existing pending cookie; `X-Platform-Request: 1`; trusted Origin if present | `{step:"enroll", uri}` |

Invitation example (synthetic identifiers only):

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "email": "staff@example.com",
  "name": "Staff member",
  "status": "pending",
  "version": 1,
  "generation": 1,
  "expires_at": "2026-10-11T10:00:00Z",
  "created_at": "2026-10-09T10:00:00Z",
  "invited_by": "00000000-0000-0000-0000-000000000002",
  "accepted_user_id": null,
  "delivery_status": "queued"
}
```

Staff has `{id, name, email, is_owner, active, version, capabilities}`. `capabilities` is currently an empty array: capability administration is Phase 4, and the empty value does not remove existing operator access. `active` requires active credential and active platform identity flags. Staff includes owner, active and inactive/revoked credential-bearing platform users; customer/credential-less accounts are excluded.

Pages are `{items, total, limit, offset}`. Defaults: limit 20, offset 0, search empty, descending sort. Limits: 1–100; offset: 0–100000; search: maximum 200 characters. Invitation sort fields: `created_at`, `email`, `expires_at`; status filters: `pending`, `enrolling`, `accepted`, `cancelled`, `expired`. Staff sorts by creation date. UUID breaks ties. Counts use the same server filters; search treats `%` and `_` literally.

Names: trimmed 1–255 characters. Email: EmailStr, at most 255 characters, normalized `strip().lower()`, ASCII mailbox local part; international domains use the same normalized spelling as CRM, with IDNA conversion at mail send. Reasons: trimmed 1–2000 characters. Unknown body fields are rejected, including owner/capability/org fields.

## Commands and UI behavior

Generate a new action UUID when the user starts a new submission; retain it with the exact body through transport retries. Same actor/action/resource/key/body returns the original committed response without repeating state changes or mail. A different body with that key returns `409 idempotency_conflict`. Receipts are retained for approximately 24 hours until scheduled cleanup. Replays reauthorize the current actor and may return a historical response; invalidate/refetch current lists after success.

Send the version from the current row. `409 version_conflict` includes the current version where available: refetch, explain the changed record and require the user to review before a new action. Do not silently retry with a newer version.

Resend only accepts pending, unexpired invitations; it rotates the token/generation and gives a new 48-hour expiry. Cancel accepts live pending/enrolling invitations and invalidates applicable enrollment. Existing staff, including revoked staff, must use explicit reset-sign-in. Reset invalidates sign-in immediately and creates new recovery lineage; the person regains access only after password setup and MFA. Owner reset/revoke through these APIs is prohibited; server recovery remains operational.

Creating an invitation for an existing account conflicts, including customer identities and existing staff. Expired unredeemed invitations can be replaced by a new invitation after expiry is materialized. If activation already created an account, use reset-sign-in rather than another join invitation.

Show invitation state separately from delivery state:

| Delivery | Meaning |
|---|---|
| queued | Committed and awaiting dispatcher |
| sending | Worker holds a lease; provider outcome pending |
| retrying | A bounded retry is scheduled |
| sent | Provider accepted; mailbox receipt unconfirmed |
| failed | Attempt budget/permanent failure; owner may resend while pending/live |
| superseded | Obsolete generation, cancellation or expiry; no further send |

Do not show a success claim that an email arrived for `202`. Legacy failed deliveries remain visible without creating mail jobs during migration. List state is reconciled every 30 seconds; command/token validity checks also enforce actual expiry.

## Authentication and interrupted enrollment

Existing `POST /login {email,password}`, `/activate {token,password}`, `/verify {code}`, `/logout` and `GET /me` retain wire shapes. Pending enrollment does not authorize `/me` or protected platform pages. Password length remains 12–128, enrollment ten minutes/five attempts, full sessions four hours with a 30-minute idle limit. Successful commits precede cookie issuance.

Activation links use a fragment. Consume/remove the fragment using the existing client and never put it in analytics, query strings, errors or logs. On activation-page reload with no token, try `/enrollment` using the pending cookie. A successful response returns the existing setup URI; it does not extend expiry or reset attempts. Keep setup material local to that screen, outside persistent Redux/cache storage, and clear it when leaving/completing setup. An ordinary challenge/full session cannot request enrollment material.

Public `/request-access` and `/verify-email`, old `/requests/{id}/review` and `/operators/{id}/revoke` writes return `410`. Remove their links/forms and developer terminology in Phase 2. Legacy owner reads `/requests` and `/operators` remain temporarily available but are not the new management API.

## Errors and frontend state boundaries

New provisioning APIs return flat errors:

```json
{
  "code": "version_conflict",
  "message": "This record changed. Refresh and try again.",
  "request_id": "opaque-request-reference",
  "current_version": 2,
  "field_errors": {}
}
```

Codes: `validation_error`, `unauthenticated`, `forbidden`, `not_found`, `version_conflict`, `idempotency_conflict`, `invalid_transition`, `rate_limited`, `temporarily_unavailable`. Field keys use locations such as `body.email` and `header.Idempotency-Key`. Database failures return safe `503`; no SQL/parameters are returned. Existing auth HTTP errors retain `detail` strings, so the client must parse both formats. All platform auth responses are no-store.

Extend `platformHttpClient` narrowly to pass the action key and parse flat errors. Put API calls in a service, then expose TanStack Query hooks and keys containing identity and every filter/sort/page parameter. Clear protected queries on logout/identity loss and cancel in-flight queries. Use Redux Toolkit only for shared platform sidebar/drawer preferences. URL state owns page/filter/sort/search; local state owns form drafts/action UUIDs. Keep privileged writes pessimistic and dialogs open on failure.

Reproduce the snapshot from the backend directory:

```powershell
.\.venv\Scripts\python.exe scripts/export_platform_openapi.py ../crusource-crm-docs/superadmin-phase1/platform-auth.openapi.json
```
