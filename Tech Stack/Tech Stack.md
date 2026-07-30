# Technology Stack Document

## Table of Contents

- [1. Final Technology Stack](#1-final-technology-stack)
- [2. Ground work](#2-ground-work)
  - [2.1 Frontend Framework](#21-frontend-framework)
  - [2.2 UI Framework](#22-ui-framework)
  - [2.3 State Management](#23-state-management)
  - [2.4 Data Tables](#24-data-tables)
  - [2.5 Drag & Drop](#25-drag--drop)
  - [2.6 Forms](#26-forms)
  - [2.7 Charts](#27-charts)
  - [2.8 Backend](#28-backend)
  - [2.9 Database](#29-database)
  - [2.10 ORM](#210-orm)
  - [2.11 Authentication](#211-authentication)
  - [2.12 File Storage](#212-file-storage)
  - [2.13 Cache](#213-cache)
  - [2.14 Background Jobs](#214-background-jobs)
  - [2.15 Frontend Hosting](#215-frontend-hosting)
  - [2.16 Backend Hosting](#216-backend-hosting)
  - [2.17 Database Hosting](#217-database-hosting)
  - [2.18 CI/CD](#218-cicd)

---

## 1. Final Technology Stack

| Layer | Selected Technology | Why use it & what it does |
|--------|---------------------|---------------------------|
| Frontend Framework | **Next.js (App Router) + TypeScript** | React framework serving as the web foundation; provides file-based routing and seamless SSR/API routes. |
| UI Framework | **Tailwind CSS + shadcn/ui** | Styling engine and accessible component primitives; enables rapid custom styling with zero runtime CSS overhead. |
| State Management | **TanStack Query + Redux Toolkit** | Handles server-state caching and global client UI state separately for predictable data flow. |
| Data Tables | **TanStack Table** | Headless utility for advanced list views; offers high performance and 100% UI customizability. |
| Drag & Drop | **dnd-kit** | Modular drag-and-drop toolkit; powers Kanban boards (Deals/Leads) with smooth CSS transform animations. |
| Forms | **React Hook Form + Zod** | Form state manager with schema validation; provides high performance via uncontrolled inputs and strict type safety. |
| Charts | **Recharts** | Composable SVG charting library; used for analytics dashboards, rendering responsive and customizable data visualizations. |
| Backend | **Python + FastAPI** | High-performance async API framework; serves as the backend monolith with native access to AI/ML ecosystems. |
| Database | **PostgreSQL + pgvector** | Primary relational datastore extended for vector embeddings; stores CRM relational data and RAG vector indexes together. |
| ORM | **SQLAlchemy + Alembic** | Python SQL toolkit and migration engine; manages database schemas and executes complex query operations. |
| Authentication | **JWT (python-jose) + Passlib (Argon2)** | Security protocol for stateless API authentication; handles token issuance, validation, and password hashing. |
| File Storage | **AWS S3** | Managed object storage; securely stores user document attachments and CSV exports using pre-signed URLs. |
| Cache | **AWS ElastiCache** | Fully managed Redis in-memory datastore; accelerates dashboard queries and caches session/rate-limiting data. |
| Background Jobs | **AWS SQS** | Serverless message queue; decouples heavy, async tasks (CSV imports, AI scoring) from the main API threads. |
| Frontend Hosting | **Vercel** | Cloud platform optimized for Next.js; automates edge deployments, CI/CD, and global CDN caching. |
| Backend Hosting | **AWS ECS / Fargate** | Serverless container orchestration; automatically scales backend API docker containers without managing EC2 instances. |
| Database Hosting | **Amazon RDS (PostgreSQL)** | Managed relational database service; handles automated backups, multi-AZ failover, and maintenance operations. |
| CI/CD | **GitHub Actions** | Native GitHub automation tool; executes automated tests, linting, and deployment pipelines. |

---

## 2. Ground work

### 2.1 Frontend Framework
**Selected:** Next.js (App Router) + TypeScript
Chosen for its scalable file-based routing, built-in API routes, and strong deployment support on Vercel — giving the project better long-term structure than a plain single-page app.

| Pros | Cons |
|------|------|
| • Built-in routing and file-based structure<br>• Strong ecosystem and developer experience<br>• Better long-term project organization | • Can feel like overkill for simple apps that don't need SEO |

**Alternative Considered:** React (Vite)
A lighter, simpler option considered for its speed, but it needs more manual setup as the project grows.

| Pros | Cons |
|------|------|
| • Very fast local development<br>• No server-rendering complexity<br>• Simple for small apps | • Needs manual routing setup<br>• No built-in API routes<br>• More upfront setup decisions |

### 2.2 UI Framework
**Selected:** Tailwind CSS + shadcn/ui
Chosen for its rapid utility-first styling velocity and accessible unstyled primitives, allowing 100% custom CRM branding without rigid theme locking.

| Pros | Cons |
|------|------|
| • Rapid styling and infinite customizability<br>• Highly accessible primitives (dialogs, dropdowns)<br>• Zero runtime CSS overhead | • Verbose class names in HTML markup<br>• Slight learning curve to set up base design tokens |

**Alternative Considered:** Chakra UI / MUI
Standard component libraries with ready-made UI components. Considered for speed but rejected due to styling rigidity.

| Pros | Cons |
|------|------|
| • Rich pre-styled components ready out of the box<br>• Faster initial prototyping without token setup | • Significant bundle size and runtime performance cost<br>• Harder to heavily customize or theme beyond defaults |

### 2.3 State Management
**Selected:** TanStack Query + Redux Toolkit
Chosen to separate complex asynchronous server-state caching (TanStack Query) from global client UI interactions (Redux Toolkit), avoiding manual cache synchronization bugs.

| Pros | Cons |
|------|------|
| • Powerful caching and remote state handling<br>• Automatic background revalidation and deduplication<br>• Predictable, separated client UI state | • Managing two complementary state libraries<br>• Redux introduces some structural boilerplate |

**Alternative Considered:** Zustand
A minimalist single-store state library considered for its simplicity.

| Pros | Cons |
|------|------|
| • Extremely lightweight footprint<br>• Minimal boilerplate with a simple hook-based API | • Lacks built-in server-state caching and invalidation<br>• Mixing server and client state causes sync complexity |

### 2.4 Data Tables
**Selected:** TanStack Table
Chosen for its headless architecture, providing powerful sorting, filtering, and pagination logic while allowing complete styling freedom for dense CRM list views.

| Pros | Cons |
|------|------|
| • Headless design provides 100% UI styling freedom<br>• Highly flexible and performs great with large data sets<br>• Full TypeScript support | • Requires manual UI implementation for headers and controls<br>• Steep learning curve for advanced features |

**Alternative Considered:** AG Grid
A feature-complete enterprise grid library evaluated for its out-of-the-box spreadsheet capabilities.

| Pros | Cons |
|------|------|
| • Turnkey enterprise features (pivot tables, exports)<br>• Rapid initial setup for complex grid operations | • Heavy bundle size payload<br>• Expensive enterprise license required for advanced features<br>• Harder to seamlessly style with custom CSS |

### 2.5 Drag & Drop
**Selected:** dnd-kit
Chosen to power Kanban boards for Deals and Leads because of its modern, lightweight architecture and excellent CSS transform performance.

| Pros | Cons |
|------|------|
| • Lightweight with superior animation performance<br>• Highly accessible (keyboard and screen-reader support)<br>• Highly customizable collision detection | • Requires explicit manual state handling for list reordering<br>• Less "plug-and-play" than older monolithic libraries |

**Alternative Considered:** react-beautiful-dnd
An established legacy drag-and-drop library considered for its simple setup.

| Pros | Cons |
|------|------|
| • Simple, intuitive API for basic vertical/horizontal lists<br>• Well-known with extensive community tutorials | • Unmaintained project status<br>• Lacks full React 18 strict mode compatibility<br>• Inflexible for complex non-standard grid layouts |

### 2.6 Forms
**Selected:** React Hook Form + Zod
Chosen for its high-performance uncontrolled input model and seamless integration with Zod schemas for shared TypeScript validation.

| Pros | Cons |
|------|------|
| • Excellent render performance on large CRM forms<br>• Strict type safety and automatic schema inference<br>• Easy, seamless validation integration | • Complex generic typing when building dynamic field arrays<br>• Requires understanding uncontrolled component models |

**Alternative Considered:** Formik + Yup
A traditional React form library considered due to its widespread legacy adoption.

| Pros | Cons |
|------|------|
| • Battle-tested with a widely understood API<br>• Simple and straightforward for basic forms | • Controlled inputs cause performance lag on large forms<br>• Yup schema type inference is less robust than Zod |

### 2.7 Charts
**Selected:** Recharts
Chosen for building analytics dashboard widgets because of its composable React syntax and seamless integration with our custom UI cards.

| Pros | Cons |
|------|------|
| • Declarative and composable React component syntax<br>• Easy to customize tooltips, legends, and styling<br>• Responsive container adapters built-in | • SVG rendering can struggle with massive datasets (10k+ points)<br>• Limited to standard chart types (bar, line, pie) |

**Alternative Considered:** Chart.js
An HTML5 Canvas charting library considered for raw rendering speed on high-density datasets.

| Pros | Cons |
|------|------|
| • Canvas-based rendering easily handles massive datasets<br>• Broad plugin ecosystem for specialized chart types | • Imperative configuration object API feels less idiomatic in React<br>• Harder to dynamically style tooltips with Tailwind CSS |

### 2.8 Backend
**Selected:** Python + FastAPI
Chosen specifically to support our V1.5 AI roadmap (Lead Scoring, Email Drafting, RAG), providing native AI/ML library access combined with blazing fast async API performance.

| Pros | Cons |
|------|------|
| • Native access to the rich AI/ML Python ecosystem<br>• Very fast async execution and built-in Pydantic validation<br>• Automatic OpenAPI/Swagger documentation generation | • Smaller ecosystem for traditional enterprise CRM tooling compared to Java or Node.js |

**Alternative Considered:** Node.js + NestJS
An enterprise-grade TypeScript framework considered to keep the entire stack in one language.

| Pros | Cons |
|------|------|
| • Keeps the entire stack in one language (TypeScript)<br>• Excellent enterprise-grade Dependency Injection architecture | • Weaker AI/ML ecosystem for advanced features<br>• Requires external Python microservices for RAG tasks |

### 2.9 Database
**Selected:** PostgreSQL + pgvector
Chosen as the strict relational core necessary for CRM data integrity, with `pgvector` allowing us to store and query AI embeddings in the exact same datastore.

| Pros | Cons |
|------|------|
| • Robust relational model with strict ACID compliance<br>• Native vector search keeps all data in the same DB<br>• Eliminates complex data synchronization bugs | • Vertical scaling limits for traditional RDBMS<br>• Vector search is slower than dedicated vector DBs at massive scale |

**Alternative Considered:** MongoDB
A NoSQL document database evaluated for its flexible, schema-less data structures.

| Pros | Cons |
|------|------|
| • Highly flexible schema allows rapid iteration<br>• Very fast document retrieval and easy horizontal scaling | • Poor fit for highly relational CRM data and complex JOINs<br>• Lacks strict referential integrity (foreign keys) |

### 2.10 ORM
**Selected:** SQLAlchemy + Alembic
Chosen to provide fine-grained, explicit control over complex SQL queries, dynamic role-based scoping filters, and automated schema migrations.

| Pros | Cons |
|------|------|
| • Extremely powerful and mature with fine-grained SQL control<br>• Excellent support for async drivers and complex JOINs<br>• Reliable automated schema migrations via Alembic | • Steep learning curve compared to simpler ORMs<br>• Can be verbose and complex for very simple queries |

**Alternative Considered:** Django ORM / Prisma (Node)
Simpler, highly opinionated ORMs considered for their development velocity.

| Pros | Cons |
|------|------|
| • Intuitive APIs and auto-generated client definitions (Prisma)<br>• Built-in admin dashboard tooling (Django) | • Locks database logic into rigid framework patterns<br>• Less optimal SQL generation for complex multi-join CRM queries |

### 2.11 Authentication
**Selected:** JWT (python-jose) + Passlib (Argon2)
Chosen for providing stateless, secure authentication where custom tenant and role claims (`org_id`, `role`) can be embedded directly into tokens for fast API verification.

| Pros | Cons |
|------|------|
| • Stateless backend verification is scalable and fast<br>• Argon2id provides industry-standard password hashing<br>• Allows embedding custom multi-tenant claims | • Harder to instantly revoke tokens without maintaining a blocklist<br>• Requires manual implementation of password reset flows |

**Alternative Considered:** Firebase Auth
A managed authentication service considered to offload user identity management entirely.

| Pros | Cons |
|------|------|
| • Turnkey social logins and built-in MFA UI<br>• Zero backend auth code required for basic user flows | • Vendor lock-in and monthly active user pricing costs<br>• Difficult to deeply integrate with custom CRM multi-tenant authorization logic |

### 2.12 File Storage
**Selected:** AWS S3
Chosen to securely store user uploads and CSV exports off-server, utilizing pre-signed URLs to offload heavy file transfers directly to the client.

| Pros | Cons |
|------|------|
| • Industry standard with unmatched durability and availability<br>• Secure pre-signed URL architecture saves API bandwidth<br>• Highly cost-effective and scalable | • AWS IAM and permissions policies can be complex to configure initially<br>• Requires careful CORS setup for client-side uploads |

**Alternative Considered:** Cloudflare R2
An S3-compatible object storage provider evaluated for its zero egress fee pricing model.

| Pros | Cons |
|------|------|
| • Zero egress fee pricing structure<br>• Full compatibility with existing S3 SDK tools | • Slightly less mature tooling integration in enterprise AWS deployment pipelines<br>• Operates outside the primary AWS security boundary |

### 2.13 Cache
**Selected:** AWS ElastiCache
Chosen to provide managed, highly available Redis instances to cache expensive dashboard queries, rate-limits, and RAG contexts, reducing primary database load.

| Pros | Cons |
|------|------|
| • Extremely fast, sub-millisecond data retrieval<br>• Fully managed service handles HA, backups, and scaling<br>• Rich Redis data structures (hashes, sets) | • Adds ongoing cloud infrastructure cost<br>• Introduces architectural cache invalidation complexity |

**Alternative Considered:** Self-hosted Redis
Running Redis manually on a dedicated EC2 instance to reduce managed service premiums.

| Pros | Cons |
|------|------|
| • Lower baseline infrastructure costs<br>• Full root control over configuration and tuning | • High engineering maintenance burden for patching and backups<br>• Requires manual setup for High Availability and failover |

### 2.14 Background Jobs
**Selected:** AWS SQS
Chosen to completely decouple asynchronous tasks (CSV imports, AI jobs) from FastAPI web threads using a fully managed, serverless message queue without needing a Redis cluster.

| Pros | Cons |
|------|------|
| • Fully managed, serverless, and highly scalable<br>• Excellent decoupling of heavy tasks from web requests<br>• Built-in Dead Letter Queue (DLQ) support | • At-least-once delivery requires idempotent worker tasks<br>• Message size limit of 256KB requires S3 offloading for large payloads |

**Alternative Considered:** BullMQ + Redis
A popular Node/Python task queue considered for its rich feature set.

| Pros | Cons |
|------|------|
| • Excellent features like delayed jobs and rate-limiting<br>• Rich visual dashboards and seamless ecosystem integration | • Tightly couples the job queue to Redis infrastructure capacity<br>• Requires managing and orchestrating persistent worker processes |

### 2.15 Frontend Hosting
**Selected:** Vercel
Chosen to provide automated, zero-configuration deployments for Next.js, serving our application on a highly optimized global edge network.

| Pros | Cons |
|------|------|
| • Zero-config deployments tailored specifically for Next.js<br>• Excellent CI/CD integration with automated PR previews<br>• High-speed global edge network | • Vendor lock-in to the Vercel platform<br>• Enterprise pricing can get expensive at high scale |

**Alternative Considered:** AWS Amplify
AWS's frontend hosting solution, evaluated to keep all infrastructure on a single AWS bill.

| Pros | Cons |
|------|------|
| • Consolidates cloud billing and IAM governance strictly within AWS<br>• Tight integration with other AWS services | • Slower build iterations compared to Vercel<br>• More complex configuration for Next.js App Router edge features |

### 2.16 Backend Hosting
**Selected:** AWS ECS / Fargate
Chosen for serverless container execution, allowing us to run our Dockerized FastAPI monolith with automatic scaling and no EC2 host maintenance.

| Pros | Cons |
|------|------|
| • Serverless containers eliminate OS maintenance<br>• Highly scalable and reliable with multi-AZ support<br>• Native integration with AWS ALBs and IAM | • Complex initial AWS networking setup (VPCs, Subnets, Security Groups)<br>• Slower cold starts compared to simple PaaS solutions |

**Alternative Considered:** Render / Heroku
Platform-as-a-Service (PaaS) providers evaluated for their extreme deployment simplicity.

| Pros | Cons |
|------|------|
| • Simple git-push deployments<br>• Zero cloud networking knowledge required | • Higher cost per resource at scale<br>• Inflexible private networking options for connecting to AWS databases |

### 2.17 Database Hosting
**Selected:** Amazon RDS (PostgreSQL)
Chosen to offload critical database administration tasks (backups, patching, failover) to AWS while keeping data securely inside our private VPC.

| Pros | Cons |
|------|------|
| • Automated backups and point-in-time recovery<br>• Managed Multi-AZ failover and scaling capabilities<br>• Secure VPC isolation | • Higher baseline recurring cost compared to self-hosting or simple VPS instances |

**Alternative Considered:** Supabase
A Backend-as-a-Service providing managed Postgres, considered for its auto-generated APIs.

| Pros | Cons |
|------|------|
| • Provides auto-generated APIs and real-time subscriptions<br>• Built-in user management and dashboard | • Introduces platform opinions outside our core AWS cloud architecture<br>• Custom backend logic requires working around their BaaS layer |

### 2.18 CI/CD
**Selected:** GitHub Actions
Chosen because our codebase resides on GitHub, providing a friction-free native pipeline for running automated tests, linting, and deployment hooks.

| Pros | Cons |
|------|------|
| • Natively integrated with our Git repository<br>• Highly customizable with a massive marketplace of actions<br>• Parallel execution matrix speeds up builds | • Difficult to debug complex pipeline scripts locally<br>• Secrets management can become fragmented in large orgs |

**Alternative Considered:** GitLab CI
An external CI/CD engine considered for its robust legacy pipeline customization.

| Pros | Cons |
|------|------|
| • Integrated container registry and issue tracking<br>• Excellent UI for complex pipeline visualization | • Requires migrating the codebase or mirroring repos away from GitHub<br>• Steeper learning curve for runner management |
