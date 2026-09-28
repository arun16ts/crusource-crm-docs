# Crusource CRM — Environment Configuration, Security & Architecture Upgrade

This document details the architectural and security changes made to the environment configuration system, why the previous setup was vulnerable, and how the new design resolves those issues.

---

## 1. Executive Summary

| Area | Previous State (Vulnerable / Unstructured) | Upgraded State (Secure & 12-Factor Compliant) |
| :--- | :--- | :--- |
| **Secrets Management** | Real secrets and weak defaults mixed into local files with no templates in Git. | Clean `.env.example` templates tracked in Git; active `.env` files strictly ignored and isolated. |
| **JWT `SECRET_KEY` Validation** | Permissive fallback allowed `"dev_secret_key_12345"` to run in any environment. | Fail-fast validator halts startup (`RuntimeError`) in `production`/`staging` if the key is weak or default. |
| **Google OAuth Token Flow** | Full JWT access/refresh tokens were transmitted in cleartext URL query parameters during 302 redirects. | Replaced with a **60-second single-use authorization code exchange pattern** via `POST /api/v1/auth/google/exchange`. |
| **Host Header / Redirect Security** | Redirect URLs reflected untrusted client request headers (`Origin`, `Referer`, `Host`). | Strict whitelist enforcement against configured `FRONTEND_URL` and `ALLOWED_ORIGINS`. |
| **Monorepo Environment Hygiene** | Redundant database and cache port variables were duplicated across backend and compose. | Clear separation: Root `.env` (Docker infrastructure), Backend `.env` (FastAPI), Frontend `.env.local` (Next.js). |

---

## 2. Deep Dive: Previous Problems & Technical Solutions

### Problem 1: The `SECRET_KEY` Production Trap (Critical Security Flaw)
- **Vulnerability**:
  In `src/shared/auth/security.py`, the code previously checked:
  ```python
  SECRET_KEY = os.getenv("SECRET_KEY")
  if not SECRET_KEY:
      raise RuntimeError("SECRET_KEY environment variable is missing.")
  ```
  Because the `.env` file provided `SECRET_KEY="dev_secret_key_12345"`, this check always passed. If deployed to a staging or production server with this config, an external attacker could forge arbitrary JWT tokens with admin privileges, taking over any organization or user account.
- **Solution Implemented**:
  Added `validate_secret_key_or_fail()` to `security.py`:
  ```python
  INSECURE_DEFAULT_KEYS = {
      "dev_secret_key_12345", "secret", "changeme", "password", "admin", "12345678"
  }

  def validate_secret_key_or_fail():
      if not SECRET_KEY:
          raise RuntimeError("FATAL: SECRET_KEY environment variable is missing.")
      if SECRET_KEY in INSECURE_DEFAULT_KEYS or len(SECRET_KEY.strip()) < 32:
          if ENVIRONMENT in ("production", "prod", "staging"):
              raise RuntimeError(
                  f"FATAL: SECRET_KEY is too weak for environment='{ENVIRONMENT}'. "
                  f"It must be at least 32 characters and cannot match default templates."
              )
  ```

---

### Problem 2: Cleartext Tokens in OAuth 302 Redirects (AUTH-001)
- **Vulnerability**:
  In `google_callback_handler.py`, the backend previously redirected the user to the frontend via:
  ```python
  redirect_url = f"{frontend_url}/auth/callback?access_token={backend_tokens.access_token}&refresh_token={backend_tokens.refresh_token}"
  return RedirectResponse(redirect_url)
  ```
  **Attack Vector**:
  1. The tokens appear in plain text in browser history and the URL address bar.
  2. The tokens are leaked in third-party HTTP `Referer` headers when external assets or links load.
  3. The tokens are permanently stored in intermediate proxy, CDN, and web server access logs.
- **Solution Implemented**:
  1. **One-Time Code Generation**: The backend generates a cryptographically signed, short-lived (60-second) single-use authorization code (`create_oauth_exchange_code`).
  2. **Clean Redirect**: User is redirected to `${frontend_url}/auth/callback?code=${exchange_code}&return_to=${return_to}` (no JWT tokens in the URL).
  3. **Secure POST Exchange**: The frontend calls `POST /api/v1/auth/google/exchange` with `{ "code": exchange_code }`. The backend validates the code and returns the tokens in the HTTP response body.

---

### Problem 3: Host Header Poisoning via Dynamic Redirect Construction (AUTH-002)
- **Vulnerability**:
  In `google_oauth_state.py`, the code previously inspected incoming client request headers (`Origin`, `Referer`, `X-Forwarded-Host`) without validating them against a whitelist. A malicious client could send an arbitrary `Host: evil-site.com` or `Origin: https://evil-site.com` header, causing the backend to construct OAuth redirects targeting the attacker's server.
- **Solution Implemented**:
  Refactored `_get_frontend_url()` and `_get_redirect_uri()` to validate incoming origins strictly against an allowed whitelist parsed from `FRONTEND_URL` and `ALLOWED_ORIGINS` in `.env`.

---

### Problem 4: Redundant & Conflicting Environment Variables
- **Problem**:
  The backend `.env` previously contained `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, and `REDIS_PORT`. FastAPI never read those individual variables (it only reads `DATABASE_URL` and `REDIS_URL`). This created confusion when rotating database credentials, as changing `POSTGRES_PASSWORD` in the backend `.env` did nothing unless `DATABASE_URL` was also changed.
- **Solution Implemented**:
  Consolidated the environment architecture into 3 clear scopes:

```
Crusource CRM Monorepo
│
├── .env                       <-- [Infrastructure] Docker Compose (PostgreSQL, Redis)
│   ├── POSTGRES_USER
│   ├── POSTGRES_PASSWORD
│   ├── POSTGRES_DB
│   └── REDIS_PORT
│
├── crusource-crm-backend/.env <-- [Application API] FastAPI Python Backend
│   ├── ENVIRONMENT
│   ├── BACKEND_URL / FRONTEND_URL / ALLOWED_ORIGINS
│   ├── SECRET_KEY / ALGORITHM / TOKEN_EXPIRATIONS
│   ├── DATABASE_URL / REDIS_URL
│   ├── GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REDIRECT_URI
│   ├── AWS_SES (Access Key, Secret Key, Region, From Email)
│   ├── AWS_S3 (Access Key, Secret Key, Bucket)
│   ├── GEMINI_API_KEY
│   └── QUEUE_MODE
│
└── crusource-crm-frontend/.env.local <-- [Client App] Next.js 16 / React 19
    ├── NEXT_PUBLIC_API_URL
    ├── NEXT_PUBLIC_GOOGLE_CLIENT_ID
    └── INTERNAL_BACKEND_URL (Used for Docker SSR & Server-Side Proxy)
```

---

## 3. Verification & Validation Summary

| Test / Check | Command Executed | Outcome | Status |
| :--- | :--- | :--- | :--- |
| **Production Fail-Fast Guard** | `python -c "import os, dotenv; os.environ['ENVIRONMENT'] = 'production'; from src.shared.auth import security"` | Crashes immediately on weak/default key with descriptive `RuntimeError`. | **PASS** |
| **Development Warning Mode** | `python -c "import dotenv; dotenv.load_dotenv(); from src.shared.auth.security import validate_secret_key_or_fail"` | Emits explicit `[SECURITY WARNING]` to `sys.stderr` and continues local execution. | **PASS** |
| **OAuth 60s Code Exchange** | `python -c "from src.modules.auth.handlers.google.google_oauth_state import create_oauth_exchange_code, decode_oauth_exchange_code; ..."` | Encodes and verifies 60s temporary code; rejects invalid/expired codes. | **PASS** |
| **Frontend TypeScript Build** | `npx tsc --noEmit` in `crusource-crm-frontend` | Clean compilation with **0 errors**. | **PASS** |
