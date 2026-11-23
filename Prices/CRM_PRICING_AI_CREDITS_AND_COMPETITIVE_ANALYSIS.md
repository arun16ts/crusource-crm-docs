# Crusource CRM — AI Credit Usage, Infrastructure Costs, Competitive Analysis & Pricing Strategy

> **Date:** 2026-11-23  
> **Scope:** `crusource-crm-backend`, `crusource-crm-frontend`, AWS Production Infrastructure (`ap-south-1`), and Competitor Benchmarks (Zoho CRM, HubSpot, Salesforce)  
> **Companion Workbook:** `Crusource_CRM_Pricing_And_Cost_Analysis.xlsx` (4-sheet styled Excel model with formulas)

---

## 1. Executive Summary

Crusource CRM already implements enterprise-grade capabilities—**Role Hierarchy & Field-Level Security (FLS)**, **Approval Rules**, **Teamspace Shared Pools**, **Deal Teams & Quota Splits**, **Sales Forecasting**, **Custom Reports & Anomaly Detection**, **Outbound Email Campaigns**, **Zoho CRM Migration Sync**, and **6 Gemini-powered AI features**—which competitors typically gate behind **₹2,400/user/mo** (Zoho Enterprise) or **$100/user/mo** (Salesforce Pro Suite).

With a **2-plan model (14-Day Free Trial + All-Access Pro + AI Credit Top-Ups)**:
* **Recommended Pro Price (Annual):** **$19 / user / month** (Global USD) · **₹1,199 / user / month** (India INR)
* **Recommended Pro Price (Monthly):** **$24 / user / month** (Global USD) · **₹1,499 / user / month** (India INR)
* **Org Monthly AI Credit Pool:** `500 base credits + 400 credits per active paid seat` (1 AI Credit = **$0.001** of Gemini API cost)
* **Fixed Production Infra Baseline (AWS + Vercel + Redis):** **~$94.93 / month** (~₹8,069/mo at ₹85/$)
* **Break-Even Point:** **1 organization with 6 seats** on USD pricing ($114 MRR) or **8 seats** on INR pricing (₹9,592 MRR)
* **Projected Gross Margin at Scale (25–100 orgs):** **86% – 92% gross margin** after AWS, Vercel, Redis, Gemini AI, and payment gateway fees.

---

## 2. AI Models & Unit Cost Audit (Codebase Truth)

### 2.1 Configured Models & API Rates
All LLM and embedding calls in `crusource-crm-backend` use `google-genai`:
* **Primary LLM (`gemini-2.5-flash`):** Configured in `src/modules/ai_chat/services/providers/gemini_provider.py`, `OrgSettings.loop_ai_model`, `DEFAULT_SCORING_MODEL`, and `PUBLIC_AI_MODEL`.
  * **Input tokens:** **$0.30 / 1M tokens**
  * **Output tokens:** **$2.50 / 1M tokens** *(output costs 8.33× more than input)*
* **Embeddings (`gemini-embedding-001`):** Configured via `GeminiProvider._cached_embed_model`.
  * **Input tokens:** **$0.15 / 1M tokens** ($0.00 output)

### 2.2 Per-Feature Token Usage, Dollar Cost & Current Controls

| AI Feature | Code Location | Model & Config | Typical Tokens / Call | Est. Cost / Action (USD) | Suggested Credits | Current Tracking & Limits |
| --- | --- | --- | --- | --- | --- | --- |
| **Loop AI Conversational Copilot** (`POST /api/v1/ai/chat/stream`) | `stream_chat_handler.py`, `gemini_provider.py`, `hybrid_retriever.py`, `vector_retriever.py` | `gemini-2.5-flash` (`max_output_tokens=2048`) + 1 query embedding | **Typical:** ~2,500–4,000 in / 250–600 out<br>**Heavy ("list all" 150 records + 6-turn history):** up to ~14,000 in / 2,048 out | **$0.0014 – $0.0027** avg<br>(up to ~$0.009+ heavy) | **2–3 credits** (or dynamic `ceil(usd × 1000)`) | Concurrency lease only (`acquire_chat`: max 4/org, 1/user). **Not logged to `AITokenUsage`; no monthly cap.** |
| **AI Email Draft & Refinement** (`POST /api/v1/ai/draft-email`) | `draft_email_handler.py`, `email_context_assembler.py`, `email_draft_prompt_builder.py` | `gemini-2.5-flash` (`thinking_budget=0`, `max_output_tokens=4096`) | **Draft:** ~1,100–1,700 in / 300–500 out<br>**Refine:** ~600–800 in / 300–450 out | **$0.0011 – $0.0020** | **2 credits** | Rate-limited at `30/hour/user` (`guards.py`). **`generate_structured()` discards usage metadata; no org cap.** |
| **Natural Language Report Builder** (`POST /api/v1/ai/reports/draft`) | `ai_routes.py` (`draft_report`), `report_nlp_service.py` (fallback) | `gemini-2.5-flash` (`thinking_budget=0`, `max_output_tokens=4096`) | **~2,500–4,000 in** (serializes full 8-entity `field_registry` every call) / 150–400 out | **$0.0012 – $0.0022** | **2 credits** | Shares `30/hour/user` `_draft_limiter`. **Discards usage metadata; no org cap.** |
| **AI Lead Prioritization & Scoring** (single, batch ≤50, & NLP chat) | `lead_scoring_service.py`, `lead_scoring_nlp_service.py`, `lead_scoring_models.py` | `gemini-2.5-flash` (`thinking_budget=0`, non-PII JSON + SHA-256 input-hash cache) | ~380–420 in / 80–150 out *(0 tokens on cache hit)* | **$0.00042 / lead** (~$0.42 per 1,000 leads) | **1 credit** *(0 cached)* | **Only metered feature:** logs to `ai_token_usage_ledger` (`AITokenUsage`), capped by `OrgSettings.ai_scoring_monthly_token_limit` (default `500,000` tokens/mo ≈ ~$0.45/mo). |
| **AI Import Column Mapping** | `ai_column_mapping_service.py`, `ai_mapping_routes.py` | `gemini-2.5-flash` (`max_output_tokens=1024`) | ~800–2,000 in / 150–400 out | **$0.0006 – $0.0016** *(0 on deterministic fallback)* | **1–2 credits** | Profile permission `ai_column_mapping` only. **No token logging or cap.** |
| **Vector Embedding Sync** (`POST /api/v1/ai/sync-embeddings`) | `embedding_service.py`, `record_serializers.py` | `gemini-embedding-001` (batches of 50; `sync_single_record` is DB text-only, $0) | ~70–150 tokens / record | **$0.000015 / record** (~$0.015 per 1,000 records) | **1 credit per 65–100 records** | `embedding_sync_slot` concurrency guard only. **No monthly sync cap.** |
| **Public Website AI Chat** (`POST /api/v1/ai/public-chat`) | `public_chat_handler.py`, `public_usage.py`, `public_knowledge.json` (9.2 KB) | `gemini-2.5-flash` (`max_output_tokens=800`) | ~1,200–1,500 in / 200–400 out *(FAQs & greetings cost $0)* | **$0.0010 – $0.0015** | Free to visitor | Well-capped: 10/day/visitor, 15/10min/IP, `PUBLIC_AI_GLOBAL_DAILY_LIMIT=1000` (**max ~$1.50/day** global). |
| **Campaign AI Executive Summary** | `get_campaign_ai_summary_handler.py` | Calls `provider.generate_text(prompt)` — **method missing on `GeminiProvider`** | **0 tokens currently** (falls back to `_generate_heuristic_summary`) | **$0.00 currently** (~$0.00026 if fixed) | **1 credit** (once fixed) | Silent fallback to deterministic heuristic summary. |

### 2.3 Estimated Monthly Gemini Cost per Organization
* **Small Team (3–5 seats):** ~300 chats, 150 email drafts, 20 report drafts, 500 lead scores, 2k record embeds → **~$1.00 – $1.60 / mo**
* **Mid-Market Team (15 seats):** ~2,000 chats, 1,000 email drafts, 80 report drafts, 3,000 lead scores, 15k record embeds → **~$6.00 – $10.50 / mo**
* **Heavy Team (50 seats):** ~8,000 chats, 4,000 email drafts, 250 report drafts, 12,000 lead scores, 50k record embeds → **~$24.00 – $42.00 / mo**
* **Uncapped Abuse Risk (1 org without limits):** Continuous `30 drafts/hr` + 32k-char RAG chat + repeated embedding syncs → **~$60 – $150+ / org / mo**

---

## 3. Monthly Application Operating Costs (AWS, Vercel, Redis & Third-Party)

Grounded in `crusource-crm-backend/terraform/environments/prod/main.tf` and `variables.tf` (`ap-south-1`, Mumbai):

| Cost Category | Service / Component | Configured Spec | Billing Model | Monthly USD | Monthly INR (@ ₹85) | Notes & Scaling Trigger |
| --- | --- | --- | --- | ---: | ---: | --- |
| AWS Compute | AWS ECS Fargate (CRM API) | 0.5 vCPU (`512`) / 1 GB RAM (`1024`), 1 task 24/7 | Hourly (`$0.04256`/vCPU + `$0.004655`/GB) | $18.93 | ₹1,609 | Add 2nd task (~$38) at >150 concurrent users |
| AWS Database | AWS RDS PostgreSQL | `db.t3.micro` Single-AZ, 20 GB SSD + backups | Hourly (~`$0.026`/hr) + storage | $21.50 | ₹1,828 | Upgrade to `db.t3.small` (~$40) at ~25–40 orgs |
| AWS Networking | Shared ALB (`crusource-prod-alb`) | Shared with Crusource Core + SNI ACM SSL | Fixed `$16.43`/mo + LCU split (50% share) | $12.00 | ₹1,020 | Total shared ALB ~$20–$30/mo |
| AWS Networking | Public IPv4 + Egress | 1 Public IPv4 on ECS task (`$0.005`/hr) + traffic | Hourly IP + data out | $5.00 | ₹425 | Optional savings later via VPC endpoints |
| AWS Storage/Secrets | S3 + Secrets Manager + ECR | `crusource-crm-prod-files` + RDS secret + images | Per GB + `$0.40`/secret | $3.50 | ₹298 | 10 GB S3 ≈ `$0.23`/mo |
| AWS Monitoring | CloudWatch Logs | `/ecs/crusource-prod-crm` (`$0.50`/GB ingest) | Pay-per-GB | $3.00 | ₹255 | Keep retention 14–30 days |
| AWS Email | AWS SES Outbound | `$0.10` per 1,000 emails (~20k/mo baseline) | Pay-per-email | $2.00 | ₹170 | Scales linearly with campaign volume |
| Frontend Hosting | Vercel Pro | Next.js App Router + 1 TB Fast Data Transfer | `$20` / deploying dev seat / mo | $20.00 | ₹1,700 | Covers frontend hosting up to 1 TB transfer |
| Cache & Leases | Redis Cloud Essentials | 250 MB – 1 GB tier (rate limits, SSE, leases) | Fixed tier (`$5`–`$15`/mo) | $7.00 | ₹595 | Free 30 MB tier is dev-only |
| Domain & CI | Domain + GitHub Actions | `crusource.com` share + CI runners | Amortized | $2.00 | ₹170 | ACM SSL certs are free |
| **PROD BASELINE** | **Total Production Infra (Excl. AI & Stage)** | — | **Fixed / Semi-Fixed** | **$94.93** | **₹8,069** | Multi-tenant: adding orgs adds ~$0 compute until DB/ECS scale |
| *Optional Staging* | *AWS Stage ECS + RDS (`crm-stage`)* | *0.5 vCPU/1 GB + `db.t3.micro` (if 24/7)* | *Hourly* | *$40.00* | *₹3,400* | *Scale ECS to 0 off-hours to cut ~50%* |

---

## 4. Competitive Feature & Pricing Analysis (vs. Zoho CRM, HubSpot, Salesforce)

### 4.1 Feature Comparison Summary

| Category | Feature | Crusource CRM (Pro) | Zoho CRM (India) | HubSpot (India) | Salesforce (USD) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **Core CRM** | Leads, Contacts, Accounts, Deals, Pipelines, Tasks/Calls/Meetings | Included | Free / Standard (₹800/u) | Free / Starter (₹585/u) | Starter ($25/u) | Parity |
| **Core CRM** | Duplicate Detection & Merging | Included | Standard / Pro | Pro (₹66,697/mo) | Starter / Pro | **Win vs HubSpot** |
| **Governance** | Role Hierarchy Tree & Granular RBAC | Included | **Enterprise (₹2,400/u)** | **Enterprise (₹3L/mo)** | **Pro Suite ($100/u)** | **Big Win** |
| **Governance** | Field-Level Security (Hide / Read-Only) | Included | **Enterprise (₹2,400/u)** | **Enterprise (₹3L/mo)** | **Pro Suite ($100/u)** | **Big Win** |
| **Governance** | Approval Rules & Governed Bulk Actions | Included | **Enterprise (₹2,400/u)** | **Enterprise (₹3L/mo)** | **Pro Suite ($100/u)** | **Big Win** |
| **Governance** | Immutable Audit Logs & Login History | Included | Standard / Enterprise | Enterprise (₹3L/mo) | Pro Suite ($100/u) | **Win vs HubSpot** |
| **Collaboration** | Teamspace Shared Pools & Access Requests | Included | **Enterprise (₹2,400/u)** | **Enterprise (₹3L/mo)** | **Pro Suite ($100/u)** | **Big Win** |
| **Collaboration** | Deal Teams & Revenue Quota Splits | Included | **Enterprise (₹2,400/u)** | **Enterprise (₹3L/mo)** | **Pro Suite ($100/u)** | **Big Win** |
| **Collaboration** | Account Hierarchy (Parent / Child) | Included | Enterprise (₹2,400/u) | Pro / Enterprise | Starter / Pro | **Win vs Zoho** |
| **Analytics** | Forecasting & Quota Attainment | Included | Standard (₹800/u) | Pro (₹66,697/mo) | Pro Suite ($100/u) | **Big Win vs HS/SF** |
| **Analytics** | Custom Reports (Tabular/Summary/Matrix) + Anomaly Check | Included | Unlimited in Pro (₹1,400/u) | Pro (₹66,697/mo) | Pro Suite ($100/u) | **Win vs HS/SF** |
| **Email** | Outbound Campaigns + Template Studio w/ Approvals | Included | Approvals in Enterprise | Approvals in Enterprise | Pro Suite ($100/u) | **Big Win vs All 3** |
| **AI Suite** | Loop AI Copilot (Hybrid Vector+Lexical+KB RAG) | Included | Ask Zia in Pro (₹1,400/u) | Breeze (Credits req.) | Agentforce ($25+) | **Win** |
| **AI Suite** | AI Lead Scoring + 1:1 Draft + Campaign Draft + NL Reports | Included | Pro / Enterprise | Starter–Enterprise | Starter–Pro / Add-on | **Win vs HubSpot** |
| **AI Suite** | AI Import Column Mapping (PII-Anonymized) | Included | Not Native | Not Native | Not Native | **Unique Advantage** |
| **Migration** | One-Click Zoho CRM Sync Engine | Included | Native | 3rd-party / CSV | 3rd-party / CSV | **Switching Wedge** |
| **Known Gaps** | 3rd-Party App Marketplace (800–1,500+ apps) | Gap (Roadmap) | Standard+ | Starter+ | Pro Suite ($100/u) | Competitor Advantage |
| **Known Gaps** | Built-in VoIP Telephony / Dialer | Gap (Call logs only) | Standard+ | Starter / Pro | CTI Add-on | Competitor Advantage |
| **Known Gaps** | CPQ / Quoting / Invoicing / QuickBooks | Gap (Deal stages only) | Pro / Enterprise | Pro / Enterprise | Pro Suite ($100/u) | Competitor Advantage |

### 4.2 Positioning Takeaway
* Crusource gives **Zoho Enterprise / Salesforce Pro** governance and **6 AI tools** without HubSpot's ₹2.5L–₹5.84L mandatory onboarding fees or complex 4-tier paywalls.
* Because Crusource does not yet have a 3rd-party app marketplace, native VoIP dialer, or CPQ/invoicing, pricing **below Zoho Professional (₹1,400) and Salesforce Starter ($25)** creates an immediate value-for-money advantage while keeping software gross margins at **85%+**.

---

## 5. Recommended 2-Plan Pricing Model & AI Credit System

### 5.1 Plan Structure (Free Trial + All-Access Pro)

| Plan | Global Price (USD) | India Price (INR) | CRM Quotas | AI Features & Org Credit Pool |
| --- | --- | --- | --- | --- |
| **Free Trial (14 Days)** | **$0** *(No card required)* | **₹0** *(No card required)* | Max **5 seats**, **500 contacts**, **1 GB** storage, **100 emails/day** | All Pro AI features unlocked · **200 AI Credits** one-time trial cap (max Gemini COGS ≤ $0.20) |
| **Crusource Pro (All-Access)** | **$19 / user / mo** *(annual)*<br>**$24 / user / mo** *(monthly)* | **₹1,199 / user / mo** *(annual)*<br>**₹1,499 / user / mo** *(monthly)* | Unlimited contacts (50k fair-use), **10 GB + 1 GB/seat** storage, full RBAC, FLS, Approvals, Teamspace, Forecast, Reports, Campaigns, Zoho Sync | All 6 AI features · **Pooled Org AI Credits = `500 base + (400 × active seats)` / month** |

#### Monthly AI Pool Examples & Worst-Case COGS Cap
* **1 Seat:** `900 credits/mo` → max Gemini COGS **$0.90** vs $19 / ₹1,199 revenue (**4.7% max COGS**)
* **5 Seats:** `2,500 credits/mo` → max Gemini COGS **$2.50** vs $95 / ₹5,995 revenue (**2.6% max COGS**)
* **15 Seats:** `6,500 credits/mo` → max Gemini COGS **$6.50** vs $285 / ₹17,985 revenue (**2.3% max COGS**)
* **50 Seats:** `20,500 credits/mo` → max Gemini COGS **$20.50** vs $950 / ₹59,950 revenue (**2.2% max COGS**)

### 5.2 AI Credit Definition & Top-Up Packs
Define **1 AI Credit = $0.001 of Gemini API cost** (`ceil(actual_usd_cost × 1000)` logged in `ai_token_usage_ledger`). This protects your margin automatically if an org runs large 32k-char RAG queries or switches `loop_ai_model` to a Pro model.

| Top-Up Pack | Credits Included | Global Price (USD) | India Price (INR) | Max Gemini COGS | Gross Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Boost Pack** | 2,500 | $10.00 | ₹799 | ≤ $2.50 | **75.0%** |
| **Growth Pack** | 7,500 | $25.00 | ₹1,999 | ≤ $7.50 | **70.0%** |
| **Scale Pack** | 25,000 | $75.00 | ₹5,999 | ≤ $25.00 | **66.7%** |

*Recommended UX:* Monthly plan credits reset on the billing cycle; **purchased top-up credits roll over** for 90 days (or until used). When an org hits 100%, return HTTP `429` for paid LLM calls with an in-app Top-Up prompt while keeping free deterministic fallbacks (rule-based CSV column mapping, cached lead scores, FAQs) active.

### 5.3 Competitor Price Comparison (15-Seat Team, Annual Billing)

| CRM Product & Tier | Price / User / Mo | 15-Seat Monthly Cost | Mandatory Onboarding | Crusource Savings |
| --- | --- | ---: | ---: | --- |
| **Crusource Pro (India)** | **₹1,199** | **₹17,985** | ₹0 | **Baseline (INR)** |
| Zoho CRM Professional (India) | ₹1,400 | ₹21,000 | ₹0 | **14.4% cheaper** (plus Approvals/Teamspace) |
| Zoho CRM Enterprise (India) | ₹2,400 | ₹36,000 | ₹0 | **50.0% cheaper** (parity governance + AI) |
| HubSpot Professional (India) | ₹66,697 (3u) + ₹3,755/u | ₹1,11,757 | ₹2,50,000 | **83.9% cheaper** |
| HubSpot Enterprise (India) | ₹3,00,000 (5u) + ₹6,250/u | ₹3,62,500 | ₹5,84,000 | **95.0% cheaper** |
| **Crusource Pro (Global)** | **$19** | **$285** | $0 | **Baseline (USD)** |
| Salesforce Starter Suite | $25 | $375 | $0 | **24.0% cheaper** (much deeper governance) |
| Salesforce Pro Suite | $100 | $1,500 | $0 | **81.0% cheaper** |

---

## 6. Profitability & Break-Even Forecast (After AWS, Vercel, Redis & AI)

*Assumptions: Average org burns 45% of its included monthly AI credit pool; gateway fee = 2.9%; top-up attach adds ~$4–$10/org/mo.*

### 6.1 Global USD Model ($19/user/mo)

| Growth Stage | Orgs | Seats | Sub MRR | Top-Up MRR | Total Rev | Infra (AWS+Vercel+Redis) | Gemini AI | Gateway (2.9%) | **Net Gross Profit** | **Margin** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Break-Even** | 1 | 6 | $114.00 | $0.00 | $114.00 | $94.93 | $1.31 | $3.31 | **$14.46** | **12.7%** |
| **Early Launch** | 10 | 50 | $950.00 | $60.00 | $1,010.00 | $110.00 | $29.25 | $29.29 | **$841.46** | **83.3%** |
| **Traction** | 25 | 150 | $2,850.00 | $200.00 | $3,050.00 | $145.00 | $92.63 | $88.45 | **$2,723.93** | **89.3%** |
| **Scale** | 50 | 350 | $6,650.00 | $450.00 | $7,100.00 | $220.00 | $209.25 | $205.90 | **$6,464.85** | **91.1%** |
| **Mature** | 100 | 800 | $15,200.00 | $1,000.00 | $16,200.00 | $340.00 | $466.50 | $469.80 | **$14,923.70** | **92.1%** |

### 6.2 India INR Model (₹1,199/user/mo)

| Growth Stage | Orgs | Seats | Sub MRR | Top-Up MRR | Total Rev | Infra (₹85/$) | Gemini AI | Gateway (2.9%) | **Net Gross Profit** | **Margin** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Break-Even** | 1 | 8 | ₹9,592 | ₹0 | ₹9,592 | ₹8,069 | ₹141 | ₹278 | **₹1,104** | **11.5%** |
| **Early Launch** | 10 | 50 | ₹59,950 | ₹4,800 | ₹64,750 | ₹9,350 | ₹2,486 | ₹1,878 | **₹51,036** | **78.8%** |
| **Traction** | 25 | 150 | ₹1,79,850 | ₹16,000 | ₹1,95,850 | ₹12,325 | ₹7,873 | ₹5,680 | **₹1,69,972** | **86.8%** |
| **Scale** | 50 | 350 | ₹4,19,650 | ₹36,000 | ₹4,55,650 | ₹18,700 | ₹17,786 | ₹13,214 | **₹4,05,950** | **89.1%** |
| **Mature** | 100 | 800 | ₹9,59,200 | ₹80,000 | ₹10,39,200 | ₹28,900 | ₹39,653 | ₹30,137 | **₹9,40,510** | **90.5%** |

---

## 7. Engineering Pre-Requisites Before Enabling Paid Billing & AI Limits

1. **Log all 6 AI features into `ai_token_usage_ledger`:** Extend `AITokenUsage` tracking from `lead_scoring` to Loop AI chat (`stream_chat_response`), email drafting (`DraftEmailHandler`), report drafting (`draft_report`), column mapping (`map_columns_with_ai`), and embedding sync (`EmbeddingService`), storing computed `credits_used` and `estimated_cost_usd`.
2. **Enforce atomic org-level credit checks & deduction:** Add `monthly_ai_credits_base`, `monthly_ai_credits_per_seat`, and `ai_credit_topup_balance` (or ledger balance) at the org level; check balance before every paid Gemini call and emit SSE warnings at 80% / 95% and HTTP `429` at 100%.
3. **Eliminate hidden thinking-token leaks:** Set `thinking_config=types.ThinkingConfig(thinking_budget=0)` in `stream_chat_response` and `ai_column_mapping_service.py` (matching `generate_structured_with_usage`), and restrict or multiplier-weight `OrgSettings.loop_ai_model` if non-Flash models are enabled.
4. **Fix broken Campaign AI Summary call:** `GetCampaignAiSummaryHandler` calls `provider.generate_text(prompt)`, which does not exist on `GeminiProvider`. Implement `generate_text` (with usage tracking) or intentionally keep the deterministic summary.
5. **Align billing code & UI to the 2-plan model:** Update `crusource-crm-backend` plan seeds (`a1b2c3d4e5f7` / `seed_crm_admin_data.py` currently seed 3 tiers: `starter`, `professional`, `enterprise`), `PricingSection.tsx` (currently 3 tiers), and replace `BillingBetaNotice` on `/dashboard/billing` with the Pro subscription, org AI credit meter, and top-up checkout flow.
