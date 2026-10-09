3p5Z9brl0PMpQNThFRr921ROu4SjrvkeeOhKqO1_uCQ=

# Platform owner and superadmin access

The first owner uses a dedicated internal account. Other internal operators verify
their email and request access; only the owner approves, rejects, resets or revokes
access. Organization administrators do not gain platform access through their CRM
role, security profile or `is_super_admin` flag.

## First-time setup

1. Install the updated backend requirements and frontend dependencies.
2. Configure `SUPERADMIN_MFA_KEY` in the backend's secret configuration. It must be
   a Fernet key, generated once with
   `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.
   Keep it private and backed up. Existing authenticator secrets require the same
   key to decrypt; replacing it is not a normal configuration refresh.
3. Set `SUPERADMIN_FRONTEND_URL` to the exact portal origin, for example
   `http://superadmin.localhost:3000` in native development. Production/staging
   requires its HTTPS origin. This origin controls both activation email URLs and
   permitted browser requests. Do not include a `/superadmin` path.
4. Configure the existing AWS SES transport/sender. Platform emails fail visibly
   when delivery fails; they never log verification codes or activation links.
5. From `crusource-crm-backend`, run:
   ```powershell
   .\.venv\Scripts\python.exe -m alembic upgrade head
   .\.venv\Scripts\python.exe scripts/platform_owner.py bootstrap
   ```
   Enter a dedicated email, owner name and password in the terminal. Passwords
   use hidden input and are not command-line arguments. Existing CRM emails cannot
   be converted. A database constraint prevents a second owner, including races.
6. Restart the backend after changing configuration. Open `/superadmin/login`,
   sign in and enroll an authenticator. Enrollment verification is required before
   accessing any platform data.

The local migration was applied during implementation. No owner account, private
configuration or real approval email was created automatically.

## Operator flow

`Request access → Verify email → Owner approves → Email activation link → Set
password → Enroll authenticator → Sign in with password and authenticator`.

The owner manages verified requests and internal accounts at `/superadmin/access`.
An email code lasts 10 minutes, has five attempts and is purpose-bound to the
request. Approval links last 48 hours and are single-use. Resend invalidates the
previous link. Approval is idempotent, and delivery failure is shown separately
from approval status. A rejected applicant may submit a new verified request.

If enrollment is interrupted, the owner resends activation. For an active operator
who loses their authenticator, **Reset sign-in** requires confirmation, revokes
existing sessions and sends a fresh activation link for password and MFA setup.
**Revoke access** closes all sessions and prevents further sign-in. Revoked accounts
are not automatically reactivated by a reset or resend. The owner cannot be revoked.

Owner recovery is a trusted-server operation:
```powershell
.\.venv\Scripts\python.exe scripts/platform_owner.py recover
```
It resets the owner's password/MFA enrollment and closes every owner session.
There is no public recovery endpoint or hidden bootstrap password. Treat server
access as privileged access. Bootstrap, reviews, sign-ins, resets, recovery and
revocations are recorded in `platform_security_events`; there is no event-browser UI
in this version.

## Session and integration boundaries

- Platform calls use Next's same-origin `/api/v1` proxy. CRM calls retain their
  existing JWT transport, refresh behavior and login-history check-in.
- A separate HttpOnly, host-only, SameSite Strict cookie is scoped to
  `/api/v1/superadmin`. Secure cookies are mandatory in production/staging.
- Database sessions store token hashes. MFA secrets are encrypted. CRM JWTs and
  platform cookies cannot authenticate each other's endpoints.
- Full sessions expire after four hours, with a 30-minute idle limit measured by
  authenticated API activity. Pending login/enrollment challenges last 10 minutes
  and permit five attempts. Account and IP limits also constrain repeated attempts.
- Browser commands require the trusted portal origin and a custom request header;
  authenticated commands additionally require a session-bound CSRF header.
  Cross-origin reads are restricted even when the rest of the application has a
  broader CORS policy.
- Ordinary CRM password reset, OTP resend, Google login, token issuance and
  onboarding reject internal platform identities. Missing platform configuration
  fails platform authentication without failing CRM startup.
- CRM and platform cache/session state remain separate. Platform sign-out removes
  only platform query caches; it leaves CRM tokens untouched.

The access UI lists the latest 200 verified requests/accounts. The database retains
security events and older history. Expired sessions remain unusable; automated
retention/cleanup is a future operational task.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth.py -q
$env:PLATFORM_POSTGRES_TESTS='1'
.\.venv\Scripts\python.exe -m pytest tests/test_platform_auth_postgres.py -q
```

The optional PostgreSQL tests create and remove only uniquely named temporary
schemas. They test concurrent owner bootstrap, approval idempotence and TOTP replay.
Frontend browser verification is `npm run test:platform-auth:browser`. It exercises
real UI/hooks/transport against a simulated API, without provisioning real accounts.
Real SES delivery and production TLS/proxy configuration require deployment smoke
testing with the intended environment.