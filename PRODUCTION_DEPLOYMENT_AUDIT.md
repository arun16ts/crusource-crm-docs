# Crusource CRM Production Deployment Audit

## 1. Executive Summary

| Item | Value |
| :--- | :--- |
| **Audit date/time** | 2026-09-09 |
| **Repository audited** | D:\GitHub\Crusource-CRM |
| **Deployment architecture reviewed** | Docker Compose (PostgreSQL 17, Redis 7, FastAPI/Python 3.12, Next.js 16/React 19, optional ngrok) |
| **Docker configuration reviewed** | `docker-compose.yml`, backend `Dockerfile`, frontend `Dockerfile`, both `.dockerignore` files |
| **Production build configuration reviewed** | Multi-stage Dockerfiles with `dev` and `prod` targets; `BACKEND_TARGET`/`FRONTEND_TARGET` build-target selection |
| **Runtime validation performed** | Docker Compose `config` parse (dev + prod); production `docker build --target prod` for both backend and frontend (both **succeeded**); backend prod container launched and health endpoint probed; frontend prod container launched with bind-mount to reproduce production startup; verified user/permission inside both prod images |

### Overall Production Readiness Assessment: **NOT PRODUCTION READY**

The Docker image *builds* succeed, and the multi-stage `prod` targets are correctly defined and produce minimal non-root images. However, the swarm of confirmed findings below — a production startup failure caused by the Compose bind-mounts, embedded dev/localhost backend URLs in the built frontend, real secrets committed to the repository, over-exposed ports, and unsafe defaults — means the application cannot be safely or reliably started and operated in production using the documented Docker architecture as-is.

Confirmed, reproducible production blockers exist at the *Compose orchestration* and *configuration* layers even though the underlying Dockerfiles build cleanly.

---

## 2. Audit Scope

**Docker / container files inspected:**
- `docker-compose.yml` (root master Compose)
- `crusource-crm-backend/Dockerfile`
- `crusource-crm-frontend/Dockerfile`
- `crusource-crm-backend/.dockerignore`
- `crusource-crm-frontend/.dockerignore`

**Environment files / templates inspected:**
- `.env` (root, committed real credentials)
- `.env.example` (root)
- `crusource-crm-backend/.env` (committed, contains real Gemini key + AWS + Google + ngrok secrets)
- `crusource-crm-backend/.env.example`
- `crusource-crm-frontend/.env.local` (committed, `NEXT_PUBLIC_API_URL=http://localhost:8000`)
- `crusource-crm-frontend/.env.local.example`

**Backend areas inspected (representative + all security/critical paths):**
- `src/main.py` (FastAPI app, CORS, lifespan startup, `create_all`, scheduler)
- `src/shared/database/core.py` (engine, pool, default DATABASE_URL, `create_all`, auto-migration)
- `src/shared/auth/security.py` (SECRET_KEY handling, JWT)
- `src/shared/cache/redis_client.py` (Redis fail-open)
- `src/shared/security/rate_limiter.py` (Redis/in-memory fallback)
- `src/shared/services/queue_service.py` + `src/worker.py` (SQS/sync mode)
- `src/shared/services/health_service.py`, `src/shared/routes/health_routes.py`
- `src/shared/services/s3_storage_service.py`
- `src/modules/auth/routes/auth_routes.py`, `handlers/login_handler.py`, `handlers/token_handler.py`, `handlers/google/google_callback_handler.py`
- `alembic.ini`, `alembic/env.py`, alembic `versions/` collection
- `requirements.txt`

**Frontend areas inspected:**
- `next.config.ts` (rewrites, `INTERNAL_BACKEND_URL`, output standalone, allowedDevOrigins)
- `package.json` (Next 16.2.12, React 19.2.4, scripts/ports)
- `src/lib/auth.utils.ts`, `src/features/auth/googleAuth.ts`, `src/services/teamspace/teamspaceExportService.ts` (`NEXT_PUBLIC_API_URL` consumption)

**CI/CD files inspected:**
- None present. No `.github/workflows`, no CI pipeline, no `.docker-compose.prod.yml`, no `.env.production`.

**Infrastructure / configuration files inspected:**
- `DOCKER_README.md` (documented deployment guide)
- `Docs/designSystem.md` (non-deployment)
- `AI_CODEBASE_AUDIT_REPORT.md` (prior audit)

**Coverage:**
Approximately **5,140 backend + frontend source/configuration files** were enumerated and screened; ~**30** files were read in full for the deployment-relevant trace. **7** Docker/container configuration files (`docker-compose.yml`, 2 Dockerfiles, 2 `.dockerignore`, plus discovered duplicates) were inspected.

---

## 3. Deployment Architecture Observed

### Documented architecture (per `DOCKER_README.md`)
```
Public Internet → ngrok → frontend:3000 → /api/* proxy → backend:8000 → postgres:5432 / redis:6379
```
- Compose master file with Postgres, Redis, Backend (dev/prod targets), Frontend (dev/prod targets), optional ngrok profile.
- Production build via `BACKEND_TARGET=prod FRONTEND_TARGET=prod docker compose up --build`.
- Frontend reaches backend internally over the Docker network; only frontend port 3000 is meant for public exposure.

### Actual implementation
- Compose has **5 services**: `postgres`, `redis`, `backend`, `frontend`, `ngrok` (profile-gated).
- `backend` binds host port **8000**; `frontend` binds host port **3000**; `postgres` binds host port **5432**; `redis` binds host port **6379**; `ngrok` binds host port **4040**.
- Backend and frontend build targets are driven by `${BACKEND_TARGET:-dev}` and `${FRONTEND_TARGET:-dev}` — **default to `dev`**, so `docker compose up` (no env) runs the **development** targets.
- The Compose `volumes:` for backend/frontend are **unconditional** — they apply regardless of the selected build target.

### Important mismatches (documented vs actual)
1. **Production mode with bind-mounts.** Documentation claims `BACKEND_TARGET=prod FRONTEND_TARGET=prod` builds and runs optimized standalone production images. In reality, the unconditional bind-mounts in Compose **overwrite the production image code with host source**, and for the frontend this **breaks startup entirely** (`server.js` not found). Production is not actually achieved via the documented command.
2. **Backend direct exposure.** Documentation presents frontend → internal proxy as the only path. In reality the backend is published on host port 8000, making it directly reachable and bypassable around the intended frontend routing.
3. **No production environment file.** Documentation references only `.env.example`. There is no `.env.production`, no separation of secrets, and the committed `.env`/`.env.local` files use dev values and real secrets.

---

## 4. Production Readiness Scorecard

| Area | Rating |
| :--- | :--- |
| Docker build reliability | GOOD (build succeeds) |
| Container security | GOOD (non-root prod users, but see permissions) |
| Secret management | **CRITICAL — FAIL** |
| Environment configuration | **FAIL — dev config leaks into prod** |
| Networking | **FAIL — over-exposed ports** |
| Database readiness | MEDIUM (persistence OK, migration workflow risky) |
| Redis readiness | MEDIUM (fail-open acceptable, but no auth + exposed) |
| Frontend production readiness | **FAIL — production startup breaks** |
| Backend production readiness | MEDIUM (starts, but degraded/fail-open + volumes) |
| Authentication deployment readiness | MEDIUM (local/HTTP assumptions, tokens in URL) |
| Authorization deployment readiness | MEDIUM (multi-tenant models need scrutiny) |
| Public exposure readiness | **FAIL — direct backend/PSQL/Redis exposure** |
| Ngrok deployment readiness | MEDIUM (dashboard exposure, `latest` tag) |
| AI integration readiness | MEDIUM (secret committed; prompt flow needs review) |
| Operational reliability | MEDIUM (no CI, no health-gated frontend, no resource limits) |

---

## 5. Confirmed Production Blockers

### Issue 1 — Frontend production container fails to start (`server.js` not found)

- **Severity:** CRITICAL
- **Confidence:** CONFIRMED (runtime-validated)
- **Category:** Production deployment blocker
- **Production impact:** Frontend cannot start under the documented production command; the entire application frontend is unavailable.
- **Affected services:** `frontend`
- **File(s):** `docker-compose.yml`, `crusource-crm-frontend/Dockerfile`
- **Location:** `docker-compose.yml` lines 107–111 (unconditional frontend volumes); Dockerfile `prod` stage line 65 (`CMD ["node", "server.js"]`).
- **Evidence:**
  - Dockerfile `prod` command is `node server.js` expecting the standalone bundle at `/app/server.js`.
  - Compose mounts `./crusource-crm-frontend:/app` **unconditionally** (both targets). This bind mount shadows the image's `/app` (which would contain `server.js` from the standalone build) with the host directory, which has **no** `server.js`.
  - Runtime reproduction: `docker build --target prod` (succeeds, contains `/app/server.js`), then running with the Compose bind mount produced `Error: Cannot find module '/app/server.js'` → process exits; `MODULE_NOT_FOUND`.
- **Validation performed:** Production image built successfully; launched with the exact Compose volume and observed the startup failure directly.
- **Why this blocks production:** The documented production command yields a container that immediately crashes on boot.
- **Recommended remediation direction:** Gate dev-only bind-mounts and anonymous volumes behind the dev target (e.g., profile or a separate dev Compose override); never mount host source over a production runner. Do not implement now.

### Issue 2 — Frontend build bakes in `127.0.0.1:8000` backend URL

- **Severity:** CRITICAL
- **Confidence:** CONFIRMED (runtime-validated)
- **Category:** Frontend/backend networking, API routing
- **Production impact:** In the production frontend image, all `/api/*` and `/public/*` rewrites point to `http://127.0.0.1:8000` (inside the frontend container), so the proxy cannot reach the backend and every proxied API call fails (connection refused). The app is non-functional end to end.
- **Affected services:** `frontend` → `backend`
- **File(s):** `crusource-crm-frontend/next.config.ts`, `crusource-crm-frontend/Dockerfile`
- **Location:** `next.config.ts` line 32 (`process.env.INTERNAL_BACKEND_URL || "http://127.0.0.1:8000"`); Dockerfile `builder` stage runs `npm run build` without injecting `INTERNAL_BACKEND_URL`.
- **Evidence:** Read `server.js` inside the built production image. `_originalRewrites.afterFiles` resolves to `http://127.0.0.1:8000/api/:path*` and `http://127.0.0.1:8000/public/:path*`. `INTERNAL_BACKEND_URL` is a **build-time** value in `next.config.ts`; because the Docker builder stage never receives it (only the runtime Compose `environment` sets `INTERNAL_BACKEND_URL: http://backend:8000`, which is too late), the fallback `127.0.0.1:8000` is baked in.
- **Validation performed:** Inspected the baked `server.js` config in the production image; confirmed the hardcoded loopback rewrite destination.
- **Why this blocks production:** Even if the container started, all proxied requests would be misrouted to a loopback that is not the backend.
- **Recommended remediation direction:** Pass `INTERNAL_BACKEND_URL` (or an explicit backend host) as a **build arg** to the production Dockerfile so the rewrite is correct at build time, and/or use a runtime-resolved rewrite. Do not implement now.

### Issue 3 — Real secrets committed to the repository

- **Severity:** CRITICAL
- **Confidence:** CONFIRMED (static)
- **Category:** Secret management, public exposure risk
- **Production impact:** A distributed/leaked repository exposes working credentials.
- **Affected services:** All (backend relies on AWS/Google/ngrok/AI).
- **File(s):** `.env`, `crusource-crm-backend/.env`
- **Location:** `.env` lines 29–53; `crusource-crm-backend/.env` lines 10–35.
- **Evidence:** The committed `.env` and backend `.env` contain real-looking live credentials:
  - a Google OAuth client ID and client secret;
  - an AWS access key ID and secret key (S3), plus separate SES access keys;
  - a Gemini/AI API key;
  - an ngrok authtoken.
  Values are present in plaintext and appear plausibly active. Do not print the values (per operating rules, redacted here).
- **Validation performed:** Direct file reads; keys and structure confirm live-style credentials rather than placeholders.
- **Why this blocks production:** Compromise of any of these secrets is possible; AWS/Google tokens grant external resource access; ngrok token enables tunnels; consistent with exposure of the debug/inspection surface.
- **Recommended remediation direction:** Rotate all credentials, remove them from the repo and `.dockerignore`/`.gitignore` them, and inject via a real secret store at deploy/CI time. Do not implement now.

### Issue 4 — Development volumes and dev code active in "production"

- **Severity:** CRITICAL
- **Confidence:** CONFIRMED (static, validated via compose config)
- **Category:** Development-to-production gap, secret/config leakage
- **Production impact:** Production containers execute host source (not the hardened image), are coupled to the host filesystem, and run the app in an un-hardened, dev-flavoured posture. The frontend additionally crashes (Issue 1). The backend bind mounts `src`/`alembic`/`public`/`storage` unconditionally.
- **Affected services:** `backend`, `frontend`
- **File(s):** `docker-compose.yml` lines 80–85 and 107–111.
- **Evidence:** `docker compose config` with `BACKEND_TARGET=prod FRONTEND_TARGET=prod` still lists all four backend bind-mounts and the three frontend bind-mounts/anonymous volumes. Volumes are not conditional on target.
- **Validation performed:** Parsed both dev and prod Compose renderings; bind-mounts present in both.
- **Why this blocks production:** Production-running images are overwritten with host dev source; reproducibility and isolation are lost; the documented "optimized standalone production images" are not actually used.
- **Recommended remediation direction:** Move dev volumes into a dev-only override/profile; keep production free of source bind-mounts. Do not implement now.

### Issue 5 — Frontend `NEXT_PUBLIC_API_URL` points at `localhost:8000`

- **Severity:** HIGH
- **Confidence:** CONFIRMED (static)
- **Category:** Frontend/backend networking, environment misconfiguration
- **Production impact:** Frontend client code (`API_BASE_URL`, Google login, exports) uses `NEXT_PUBLIC_API_URL`. The committed `frontend/.env.local` sets it to `http://localhost:8000`; when present in the container (bind-mounted), the browser would call the user's own `localhost:8000`, not the backend, breaking auth/Google flows and bypassing the intended proxy.
- **Affected services:** `frontend`
- **File(s):** `crusource-crm-frontend/.env.local`, `crusource-crm-frontend/src/lib/auth.utils.ts`, `src/features/auth/googleAuth.ts`
- **Location:** `.env.local` lines 1–2.
- **Validation performed:** Traced `NEXT_PUBLIC_API_URL` consumption in the three frontend modules above; confirmed fallback to `/api/v1` only when the var is empty, but the dev value is non-empty here.
- **Why this blocks production:** Auth and API calls from the browser target a localhost that does not exist for remote clients; also implies direct backend exposure rather than internal proxy usage.
- **Recommended remediation direction:** Remove `NEXT_PUBLIC_API_URL` from anything shipped to the container, or set it to the public frontend origin so the internal proxy is used. Do not implement now.

### Issue 6 — Backend, PostgreSQL, and Redis published to the host

- **Severity:** HIGH
- **Confidence:** CONFIRMED (static)
- **Category:** Network & public exposure, database/Redis exposure
- **Production impact:** Anyone with host/network access to ports 5432/6379 can reach the database and cache directly; backend on 8000 can be reached around the frontend proxy. No client auth on Redis; Postgres uses default creds.
- **Affected services:** `backend` (8000), `postgres` (5432), `redis` (6379)
- **File(s):** `docker-compose.yml` lines 27–28, 44–45, 64–65.
- **Evidence:** Ports published to host in Compose: `"8000:8000"`, `"${POSTGRES_PORT:-5432}:5432"`, `"${REDIS_PORT:-6379}:6379"`.
- **Validation performed:** `docker compose config` lists all published ports in both dev and prod.
- **Why this blocks production:** The intended architecture (public → frontend only) is not enforced; the database and cache are reachable beyond need and lack auth; backend is directly accessible.
- **Recommended remediation direction:** Do not publish Postgres/Redis to the host in production; restrict backend exposure or route exclusively via frontend proxy. Do not implement now.

---

## 6. Security Findings

### Critical
- **C-1 Committed live credentials** (AWS, Google OAuth, Gemini, ngrok) in `.env` and `crusource-crm-backend/.env`. Evidence: direct file reads. Exposure risk: high — any repo access grants cloud/OAuth/tunnel resources. (Redacted value per rules.)
- **C-2 `SECRET_KEY` default** in Compose is `dev_secret_key_12345` (`docker-compose.yml` line 71), and the committed env uses `dev_secret_key_12345`. If not overridden, JWT signing uses a known, weak key — enabling token forgery / auth bypass. Backend `security.py` rightly refuses to start without `SECRET_KEY`, but Compose always supplies the weak default, so the guard is effectively defeated in production.

### High
- **H-1 Backend directly exposed** on host:8000 bypassing intended frontend routing (see Issue 6).
- **H-2 PostgreSQL and Redis published** to host without auth (see Issue 6).
- **H-3 Redis unauthenticated** (`redis:7-alpine` run with no password; Redis reachable on 6379).
- **H-4 Dev origin allow-list always enabled**: backend CORS always adds `http://localhost:3000`, `127.0.0.1:3000`, 3001, 3005 in production (`main.py` lines 138–140). Combined with wildcard-ish ngrok origin regex, this broadens allowed origins.
- **H-5 `CREATE_ALL`/auto-migration on startup** (`main.py` line 97, `Database/core.py`) can run the schema outside Alembic control, risking schema drift if Alembic is applied separately, and is also a startup path that runs DDL in production.

### Medium
- **M-1 Ngrok inspection dashboard published** on host:4040 (see network section).
- **M-2 ngrok uses `:latest`** image tag — non-reproducible, supply-chain/update risk.
- **M-3 Frontend `allowedDevOrigins`** whitelists all `*.ngrok-*`/`*.trycloudflare.com` subdomains in the production standalone config.
- **M-4 Tokens passed in redirect URL query strings** during Google OAuth (`google_callback_handler.py` lines 236–249) — tokens in URLs are more prone to logging/leakage.
- **M-5 Backend bind-mounted `storage`** may be unwritable by production `appuser` (uid 100) if host ownership differs, causing file upload failures.

### Low
- **L-1** No structured logging/log shipping; secrets could surface in logs.
- **L-2** Errors from DB init are logged as warnings with exception text (potential internal info leakage in health/log output).
- **L-3** No resource limits on any container; a runaway worker can exhaust host.
- **L-4** `/docs`, `/redoc`, `/openapi.json` enabled with no environment gating — debug/docs surface visible in production.

---

## 7. Docker and Container Findings

- **Build issues:** None fatal. Both `--target prod` builds succeeded (validated). Backend prod image is minimal; frontend prod image is the standalone runner (~120MB posture).
- **Target issues:** Correct `dev` and `prod` targets exist and are named correctly. However Compose defaults to `dev` (`${BACKEND_TARGET:-dev}`, `${FRONTEND_TARGET:-dev}`) so a plain `docker compose up` runs dev builds. This is intentional for dev, but documentation's "production mode" command is the only safe prod path — and that path still suffers the bind-mount problem (Issue 4).
- **Image issues:** Non-root `appuser` (backend) and `nextjs` (frontend) are correctly used in prod. Backend `prod` uses `python:3.12-slim` (Debian), frontend `prod` uses `node:20-alpine`; both non-`latest`, reproducible. The frontend `node:20` base vs `package.json` Next 16 / React 19 — node 20 is supported; no mismatch found. Python 3.12 images contain `curl` (used by healthcheck — acceptable).
- **Runtime issues:** Frontend prod image fails under Compose bind-mount (Issue 1). 
- **Permission issues:** Backend prod image correctly `chown`s `/app` to appuser; but bind-mounted `storage`/`public` dirs on host may not match uid 100 (see M-5).
- **Volume issues:** Unconditional dev bind-mounts and anonymous `/app/node_modules` + `/app/.next` volumes in production (Issue 4). Postgres and Redis use named volumes (`crm_postgres_data`, `crm_redis_data`) — persistence is configured (good).
- **Dependency issues:** `requirements.txt` fully pinned (good). Frontend `package-lock.json` is used with `npm ci` in the builder (`COPY package.json package-lock.json*`; `npm ci`) — good, reproducible. Frontend prod runner uses `node server.js` (standalone), correct pattern.

---

## 8. Environment and Secret Findings

- **Unsafe defaults:** `SECRET_KEY` default `dev_secret_key_12345`; Postgres default `admin`/`crusource_password`; bucket `crusource-crm-dev-files`; `QUEUE_MODE=sync`.
- **Missing required production variables:** No `.env.production`, no mandated strong `SECRET_KEY`, no `POSTGRES_PASSWORD` rotation guidance of consequence, no `INTERNAL_BACKEND_URL` build arg, no CORS/`FRONTEND_URL` production origin enforcement.
- **Documentation mismatches:** Docs say only `.env` customization needed; the committed env carries real secrets and dev values. Docs say "only expose port 3000"; Compose exposes 8000/5432/6379/4040.
- **Secret exposure risks:** Live AWS/Google/Gemini/ngrok secrets in repo; `NEXT_PUBLIC_*` values (default exposed to browser) — here `NEXT_PUBLIC_GOOGLE_CLIENT_ID` (public by design) but also the backend `.env` AWS/Gemini/ngrok secrets are passed to the backend container env (and hence into image runtime envs) via `env_file` + `environment`.
- **Build-time vs runtime configuration:** `INTERNAL_BACKEND_URL` is a runtime Compose env but is consumed at build time by `next.config.ts` → baked wrong value (Issue 2). `NEXT_PUBLIC_API_URL` in `.env.local` is a build-time/public value incorrectly set to `http://localhost:8000` (Issue 5).

---

## 9. Network and Public Exposure Findings

- **Exposed ports:** 3000 (frontend), 8000 (backend), 5432 (postgres), 6379 (redis), 4040 (ngrok dashboard).
- **Internal services:** None are confined to the Docker network only; all are published to the host.
- **Direct backend access:** Yes — host:8000 exposes FastAPI directly, bypassing the frontend proxy and exposing `/docs`, `/redoc`, `/openapi.json`, admin/data-admin routers, health endpoints.
- **Database/Redis exposure:** Yes — 5432 and 6379 published to host; no external auth on Redis; Postgres uses default creds (proof of the intended "public → frontend only" architecture is not enforced).
- **Ngrok concerns:** Dashboard on 4040; `ngrok/ngrok:latest`; guest traffic inspection UI exposed.
- **Debug/admin interface exposure:** `/docs`/`/redoc`/`/openapi.json` not gated; `admin_router`, `data_admin_router` included on the same publicly bound service; health endpoints leak component/dependency detail.

---

## 10. Development-to-Production Gaps

1. **Frontend bind-mount breaks prod startup** (dev-only volume always applied) — the single most dangerous gap.
2. **Backend source bind-mounts** mean "production" executes host code and is coupled to the host.
3. **Backend `--reload` only in dev stage** — correct, but irrelevant because production runs via bind-mounted source and Compose default target is dev; if an operator runs `docker compose up` unqualified they get dev reload servers.
4. **Frontend dev start port mismatch:** `package.json` dev/start scripts use port **3005** while Docker uses **3000**; Compose overrides with `npx next dev ... -p 3000` in the Dockerfile so this is internally consistent within Docker, but host-side `npm run dev` listens on 3005 which won't match docs/compose.
5. **Development default env values** (`localhost`, `dev_secret_key_12345`, `sync` queue, development bucket) are not replaced for production.
6. **CORS dev origins** always appended even in prod.
7. **No production-specific Compose/docker-compose.prod.yml**; prod and dev share one file with no env-overridden behavior for mounts/ports.

---

## 11. Runtime Validation Results

### Static analysis only
- All env/secret tracing, CORS, Alembic config, rewrite logic, build-target logic, port mappings, volume mappings.

### Docker build validated
- `docker build --target prod` (backend) — **SUCCESS**; contains non-root appuser, `/health` healthcheck, uvicorn without reload.
- `docker build --target prod` (frontend) — **SUCCESS**; standalone runner, non-root nextjs.
- Verified `/app/server.js` exists in the frontend prod image and contains the baked `127.0.0.1:8000` rewrites (Issue 2).
- Verified user/id inside both prod images (`appuser` uid 100; `nextjs` uid 1001).

### Runtime validated
- Backend prod container launched standalone (no DB/Redis): it **started** and listened on :8000; `/health` returned **503** (DB dependency reachability fail), confirming fail-open/degraded startup and no fail-fast on missing dependencies. Container stopped and removed afterward (no persistent state touched).
- Frontend prod container launched with the exact Compose bind-mount: **crashed with `MODULE_NOT_FOUND: /app/server.js`** — reproduces the production startup blocker (Issue 1).
- No real Compose `up` was run, and no `docker compose down -v` or destructive operations were performed. Existing named volumes (`crm_postgres_data`/`crm_redis_data`) were not created or modified by this audit; only temporary throwaway containers were used and removed. No user data destroyed.

---

## 12. Findings Rejected During Validation

- **Rejected:** "Frontend cannot build for production." — Rejected. `docker build --target prod` **succeeded**; the standalone output was produced. The problem is at the Compose/runtime layer, not the build.
- **Rejected:** "Backend cannot start without Postgres/Redis." — Downgraded/rejected as a start blocker. Backend **did start** and serve (degraded/503). It is a robustness concern (fail-open), not a startup failure; the Compose `depends_on` also gates health for the full stack.
- **Rejected (downgraded):** "Node 20 vs Next 16/React 19 incompatibility in prod." — Downgraded. No build error; supported and consistent within the repo.
- **Rejected:** "Frontend `.env.local` baked into production image." — Partially rejected: the frontend `.dockerignore` excludes `.env*.local`, so it is **not baked** at image build. However it **does leak into the runtime** via the `./crusource-crm-frontend:/app` bind-mount (issue remains valid via a different path).
- **Rejected:** "CORS fails in production with ngrok." — Rejected. The backend CORS explicitly allows ngrok/trycloudflare origins via `allow_origin_regex`, so CORS is permissive enough; the concern is over-permissiveness rather than failure.

---

## 13. Positive Production Readiness Findings

- **Real multi-stage Dockerfiles** with distinct, correctly named `dev` and `prod` targets for both backend and frontend.
- **Non-root production users** in both prod images (`appuser`, `nextjs`).
- **Frontend `output: "standalone"`** and a minimal prod runner using `node server.js` (industry-standard pattern).
- **`npm ci`** with the lock file in the builder — reproducible frontend installs.
- **Fully pinned `requirements.txt`** for reproducible Python installs.
- **Named volumes** for Postgres and Redis — persistence configured.
- **Healthchecks** on Postgres (`pg_isready`), Redis (`redis-cli ping`), backend (`/health`), and compose `depends_on: condition: service_healthy` for backend dependencies.
- **`SECRET_KEY` runtime guard** in `security.py` refuses to start without it (strengthens prod if the weak default were removed).
- **Rate limiting** present on auth/OTP endpoints with Redis + in-memory fallback.
- **Refresh tokens persisted and revocable** (rotated on refresh, revoked on logout), stored hashes via Argon2 for passwords.
- Both base images are versioned (not bare `latest`) for OS layer reproducibility (postgres:17-alpine, redis:7-alpine, python:3.12-slim, node:20-alpine).

---

## 14. Prioritized Production Remediation Plan

*(Recommended direction only — no code changes made.)*

### Priority 0 — Production blockers (must fix before anything can run)
- P0-1 Remove dev-only bind-mounts + anonymous `/app/node_modules` + `/app/.next` volumes from the production path; use a dev-only Compose override/profile so production runners use baked images.
- P0-2 Make `INTERNAL_BACKEND_URL` (or an explicit backend host) a **build arg** so the frontend rewrites point to the internal backend; verify baked rewrite host at runtime (fixes Issue 2).
- P0-3 Rotate and remove all committed secrets (AWS, Google OAuth, Gemini, ngrok); stop shipping secrets in images/env; inject from a secret manager/CI.
- P0-4 Remove the weak default `SECRET_KEY` (`dev_secret_key_12345`) so a missing/weak key fails closed; enforce a strong per-deployment key.

### Priority 1 — Fix before public deployment
- P1-1 Stop publishing Postgres (5432) and Redis (6379) to the host; keep them network-internal-only.
- P1-2 Decide backend exposure: keep backend Docker-network-only and route 100% through the frontend proxy; remove or gate `/docs`,`/redoc`,`/openapi.json` and admin/data-admin exposure; gate the backend 8000 host binding.
- P1-3 Authenticate Redis (require password) and constrain accordingly.
- P1-4 Set production `FRONTEND_URL`/CORS to the real public origin; stop auto-appending localhost origins in production; evaluate the overly-broad ngrok origin regex.
- P1-5 Remove `NEXT_PUBLIC_API_URL=http://localhost:8000` from shipped config so the frontend uses the internal proxy/public origin.
- P1-6 Add a production environment file / deploy-time validation that fails on dev values (`localhost`, dev secret, dev bucket).

### Priority 2 — Fix soon after deployment
- P2-1 Automate Alembic migrations as a controlled deploy step and remove reliance on `create_all`/auto-migration DDL in production startup.
- P2-2 Pin the ngrok image tag and keep the inspection dashboard (4040) off public/host exposure, or disable it in prod.
- P2-3 Move tokens out of URL query strings for OAuth redirects (short-lived referrer-safe storage) given production domain constraints.
- P2-4 Ensure production `storage` volume ownership matches the non-root image user; consider a volume for file persistence rather than host bind mount.
- P2-5 Add health-gated `depends_on` for the frontend (wait for backend healthy) and container restart/readiness checks.

### Priority 3 — Hardening and technical debt
- P3-1 Add structured logging and log shipping; redact secrets/exception internals from logs and health endpoints.
- P3-2 Add CPU/memory limits and reverse-proxy/TLS termination in front, with HSTS/security headers.
- P3-3 Add a CI/CD pipeline (no current CI in the repo) with production build + compose-config validation and secret injection.
- P3-4 Introduce a true production Compose override and document reproducible tagged image releases.
- P3-5 Review multi-tenant authorization enforcement server-side (tenant/org filtering) as part of production hardening, since direct backend exposure raises IDOR/BOLA risk.

---

## 15. Final Production Verdict

### **NO**

This repository **cannot safely proceed to a production deployment** using the current Docker architecture as documented.

**Minimum required conditions before deployment:**
1. Fix the runtime start blocker — Production frontend container must be able to start with the production image (remove dev bind-mounts/volumes so `node server.js` runs from the baked standalone build).
2. Ensure the frontend's internal API proxy/resolves to the real backend over the Docker network at build/runtime time (currently baked as `127.0.0.1:8000`).
3. Remove/rotate all committed live credentials and enforce strong, per-deployment `SECRET_KEY` and database passwords with no development defaults.
4. Stop exposing PostgreSQL and Redis to the host; secure Redis; decide and enforce a single public ingress path (frontend only) with backend internal-only.
5. Provide production environment separation (no `localhost`/dev values, correct public `FRONTEND_URL`/CORS) and an automated migration strategy that doesn't rely on startup `create_all`.

Until the Priority 0 and Priority 1 conditions above are satisfied, deploying this application as-is will result in a non-starting frontend, broken API routing, publicly reachable database/cache, and exposure of live credentials — all of which are unacceptable for production.
