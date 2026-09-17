# Crusource CRM - Master Docker & Ngrok Deployment Guide

This guide details how to clone, configure, build, and run the entire Crusource CRM platform on any system using a single master Docker Compose file, with full support for development hot-reloading, production builds, and public internet tunneling via **ngrok**.

---

## 🏗 System Architecture

```
                       ┌───────────────────────────────────────────────┐
                       │               Public Internet                 │
                       │     (e.g., https://your-domain.ngrok-free.app)│
                       └───────────────────────┬───────────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────┴──────────────────────────────────────────────────────┐
│  Crusource CRM Docker Network                                                                      │
│                                                                                                     │
│   ┌───────────────────────────┐                     ┌───────────────────────────┐                   │
│   │    ngrok (Optional)       │                     │    crusource-frontend     │                   │
│   │    Image: ngrok/ngrok     ├────────────────────►│    Next.js 16 (Webpack)   │                   │
│   │    Dashboard: :4040       │                     │    Port: 3000             │                   │
│   └───────────────────────────┘                     └─────────────┬─────────────┘                   │
│                                                                   │ /api/* proxy                    │
│                                                                   ▼                                 │
│   ┌───────────────────────────┐                     ┌───────────────────────────┐                   │
│   │    crusource-postgres     │◄────────────────────┤    crusource-backend      │                   │
│   │    PostgreSQL 17          │                     │    FastAPI (Python 3.12)  │                   │
│   │    Port: 5432             │                     │    Port: 8000             │                   │
│   └───────────────────────────┘                     └─────────────┬─────────────┘                   │
│                                                                   │                                 │
│   ┌───────────────────────────┐                                   │                                 │
│   │    crusource-redis        │◄──────────────────────────────────┘                                 │
│   │    Redis 7 Alpine         │                                                                     │
│   │    Port: 6379             │                                                                     │
│   └───────────────────────────┘                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start on Any Machine

### Step 1: Clone Repository
```bash
git clone <your-repository-url> Crusource-CRM
cd Crusource-CRM
```

### Step 2: Initialize Environment Variables
Copy the template `.env.example` into `.env` at the root directory:
```bash
# Windows (PowerShell)
cp .env.example .env

# Linux / macOS
cp .env.example .env
```
*(The default `.env` is pre-configured for local testing. Customize `SECRET_KEY`, OAuth, AWS, or Ngrok keys as required).*

---

## 📦 Running the Application

### 1. Standard Development Mode
Starts PostgreSQL, Redis, Backend with live code reload, and Frontend with fast refresh:

```bash
docker compose up --build
```
> **Detached / Background mode**:
> ```bash
> docker compose up --build -d
> ```

- **Frontend Application**: [http://localhost:3000](http://localhost:3000)
- **Backend Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### 2. Tunneling to the Internet via Ngrok

#### Method A: Dockerized Ngrok Profile (Zero Host Installation)
1. Add your token and domain in `.env`:
   ```env
   NGROK_AUTHTOKEN=your_ngrok_token_here
   NGROK_DOMAIN=your-static-domain.ngrok-free.app # Optional: static free domain
   ```
2. Start the stack with the `ngrok` profile:
   ```bash
   docker compose --profile ngrok up --build -d
   ```
3. Open [http://localhost:4040](http://localhost:4040) in your browser to inspect all live HTTP requests, WebSocket connections, and latency metrics.

#### Method B: Host-Installed Ngrok CLI
```bash
# In terminal 1: start CRM
docker compose up -d

# In terminal 2: tunnel port 3000 with host header rewrite
ngrok http --host-header=rewrite 3000
```
*(Next.js automatically proxies all `/api/*` requests internally to FastAPI over the Docker network, so you only need to expose port 3000).*

---

### 3. Production Build Mode (Recommended for Client Presentations)
In production mode, all pages, routes, and bundles are pre-compiled during image creation. This eliminates cold-compilation delays, uses minimal memory (~120MB), and ensures instant sub-50ms page loads:

```bash
# Build & run production bundle
FRONTEND_TARGET=prod docker compose up -d --build --force-recreate frontend

# Or run entire stack in production target
BACKEND_TARGET=prod FRONTEND_TARGET=prod docker compose up --build -d
```

---

## 🗄 Database Migrations

Apply Alembic database migrations inside the running backend container:

```bash
docker compose exec backend alembic upgrade head
```

Create a new migration script:
```bash
docker compose exec backend alembic revision --autogenerate -m "add_new_feature"
```

---

## 🛠 Management & Troubleshooting Commands

| Action | Command |
| :--- | :--- |
| **Stream all logs** | `docker compose logs -f` |
| **Backend logs only** | `docker compose logs -f backend` |
| **Frontend logs only** | `docker compose logs -f frontend` |
| **Ngrok logs only** | `docker compose logs -f ngrok` |
| **Recreate frontend after code changes** | `docker compose up -d --build --force-recreate frontend` |
| **Recreate backend after code changes** | `docker compose up -d --build --force-recreate backend` |
| **Restart backend service** | `docker compose restart backend` |
| **Restart frontend service** | `docker compose restart frontend` |
| **Stop all containers** | `docker compose down` |
| **Stop & wipe database volumes (clean reset)** | `docker compose down -v` |
| **Force full rebuild without cache** | `docker compose build --no-cache` |

---

## 🔍 Common Issues & Solutions

### 1. Ngrok Returns `502 Bad Gateway` / `Could not connect to upstream`
* **Cause**: Node.js dev server memory exhausted or cold-compiling.
* **Fix**:
  * Set `NODE_OPTIONS="--max-old-space-size=4096"` in `docker-compose.yml`.
  * Ensure ngrok has `--host-header=rewrite` configured.
  * For live presentations, use `FRONTEND_TARGET=prod`.

### 2. Cross-Origin / Invalid Host Header on Ngrok
* **Cause**: Next.js blocks unrecognized host headers by default.
* **Fix**: Ensure your ngrok domain is in `allowedDevOrigins` inside `next.config.ts` (`*.ngrok-free.app`, `*.ngrok-free.dev`, `*.ngrok.app`).
