# Crusource CRM — Low-Level Design (LLD)

**Version:** 1.0 | **Date:** July 2026 | **Audience:** Engineering Team

> This document translates the High-Level Design into implementation-level detail — class structures, method signatures, SQL queries, component trees, service contracts, and algorithm pseudocode — so a developer can open this document and start coding.

---

## Table of Contents

1. [Backend Module Architecture](#1-backend-module-architecture)
2. [Directory Structure](#2-directory-structure)
3. [SQLAlchemy ORM Models](#3-sqlalchemy-orm-models)
4. [Pydantic Request / Response Schemas](#4-pydantic-request--response-schemas)
5. [Service Layer — Business Logic](#5-service-layer--business-logic)
6. [API Router Definitions](#6-api-router-definitions)
7. [Authentication & Authorization Implementation](#7-authentication--authorization-implementation)
8. [Row-Level Scope Filter Implementation](#8-row-level-scope-filter-implementation)
9. [Lead Conversion — Atomic Transaction](#9-lead-conversion--atomic-transaction)
10. [Deal Pipeline — Stage Transition Logic](#10-deal-pipeline--stage-transition-logic)
11. [Activity Timeline — Unified Query](#11-activity-timeline--unified-query)
12. [Document Upload / Download — Pre-Signed URL Flow](#12-document-upload--download--pre-signed-url-flow)
13. [CSV Import — Bulk Processing](#13-csv-import--bulk-processing)
14. [AI Subsystem — Detailed Implementation](#14-ai-subsystem--detailed-implementation)
15. [Caching — Implementation Details](#15-caching--implementation-details)
16. [Background Workers — SQS Consumer](#16-background-workers--sqs-consumer)
17. [Global Search — Implementation](#17-global-search--implementation)
18. [Notification System](#18-notification-system)
19. [Dashboard & Reporting — Query Specifications](#19-dashboard--reporting--query-specifications)
20. [Frontend Architecture — Component Tree](#20-frontend-architecture--component-tree)
21. [Frontend State Management](#21-frontend-state-management)
22. [Frontend Routing — Next.js App Router](#22-frontend-routing--nextjs-app-router)
23. [Database Migration Strategy](#23-database-migration-strategy)
24. [Error Handling — Centralized Pattern](#24-error-handling--centralized-pattern)
25. [Rate Limiting Implementation](#25-rate-limiting-implementation)
26. [CI/CD Pipeline Specification](#26-cicd-pipeline-specification)
27. [Environment Configuration](#27-environment-configuration)

---

## 1. Backend Module Architecture

The backend follows a **layered architecture** within a modular monolith. Each business domain is a self-contained module with its own models, schemas, services, and routers.

```
┌─────────────────────────────────────────────────┐
│                  API Layer (Routers)             │
│  auth │ leads │ contacts │ accounts │ deals │ …  │
├─────────────────────────────────────────────────┤
│               Service Layer (Business Logic)     │
│  auth │ lead  │ contact  │ account  │ deal  │ …  │
├─────────────────────────────────────────────────┤
│              Repository Layer (Data Access)       │
│         Scope Filter ← applied at this layer     │
├─────────────────────────────────────────────────┤
│               ORM Layer (SQLAlchemy Models)       │
├─────────────────────────────────────────────────┤
│               PostgreSQL 16 + pgvector           │
└─────────────────────────────────────────────────┘
```

**Key principle:** Routers handle HTTP concerns only (request parsing, response formatting). Services contain all business rules. Repositories encapsulate database queries with scope filtering.

---

## 2. Directory Structure

```
backend/
├── app/
│   ├── main.py                          # FastAPI app factory, middleware, lifespan
│   ├── config.py                        # Settings from env / Secrets Manager
│   ├── database.py                      # Async engine, session factory
│   ├── dependencies.py                  # Shared DI (get_db, get_current_user)
│   │
│   ├── auth/
│   │   ├── router.py                    # POST /auth/login, /auth/refresh
│   │   ├── service.py                   # login(), refresh_token()
│   │   ├── schemas.py                   # LoginRequest, TokenResponse
│   │   └── jwt.py                       # encode_jwt(), decode_jwt()
│   │
│   ├── users/
│   │   ├── router.py                    # /users CRUD endpoints
│   │   ├── service.py                   # create_user(), deactivate(), transfer()
│   │   ├── schemas.py                   # UserCreate, UserUpdate, UserResponse
│   │   └── models.py                    # User SQLAlchemy model
│   │
│   ├── leads/
│   │   ├── router.py                    # /leads CRUD + /convert + /kanban
│   │   ├── service.py                   # create_lead(), convert_lead(), etc.
│   │   ├── schemas.py                   # LeadCreate, LeadResponse, ConvertRequest
│   │   └── models.py                    # Lead, LeadScore SQLAlchemy models
│   │
│   ├── contacts/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── accounts/
│   │   ├── router.py
│   │   ├── service.py                   # Includes duplicate detection logic
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── deals/
│   │   ├── router.py
│   │   ├── service.py                   # Stage transition + side effects
│   │   ├── schemas.py
│   │   └── models.py                    # Deal, PipelineStage, DealRiskAlert
│   │
│   ├── activities/
│   │   ├── router.py                    # /activities + /timeline
│   │   ├── service.py                   # Timeline query, activity creation
│   │   ├── schemas.py                   # ActivityCreate (discriminated union)
│   │   └── models.py                    # Activity (STI base)
│   │
│   ├── documents/
│   │   ├── router.py
│   │   ├── service.py                   # S3 pre-signed URL generation
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── dashboard/
│   │   ├── router.py                    # /dashboard/home, /dashboard/analytics
│   │   ├── service.py                   # Aggregation queries + caching
│   │   └── schemas.py
│   │
│   ├── reports/
│   │   ├── router.py
│   │   ├── service.py                   # Pre-built report executors
│   │   ├── schemas.py
│   │   └── report_definitions.py        # Report SQL/config registry
│   │
│   ├── ai/
│   │   ├── router.py                    # /ai/email-draft, /ai/chat, etc.
│   │   ├── service.py                   # Orchestrates SQS dispatch
│   │   ├── scoring.py                   # Lead scoring algorithm
│   │   ├── risk_alerts.py               # Deal risk detection algorithm
│   │   ├── prompt_builder.py            # Prompt templates for Claude
│   │   ├── embedding.py                 # Chunking + embedding pipeline
│   │   └── schemas.py
│   │
│   ├── search/
│   │   ├── router.py                    # /search?q=
│   │   └── service.py                   # UNION ALL query builder
│   │
│   ├── notifications/
│   │   ├── router.py
│   │   ├── service.py
│   │   └── models.py
│   │
│   ├── settings/
│   │   ├── router.py                    # /settings/pipeline-stages, /scoring-weights
│   │   └── service.py
│   │
│   ├── common/
│   │   ├── scope.py                     # ScopeFilter class
│   │   ├── pagination.py                # CursorPaginator
│   │   ├── exceptions.py                # Custom exception hierarchy
│   │   ├── middleware.py                # RequestID, CORS, timing
│   │   └── cache.py                     # Redis cache helper (get/set/invalidate)
│   │
│   └── workers/
│       ├── consumer.py                  # SQS long-poll consumer loop
│       ├── handlers/
│       │   ├── email_draft.py           # Process email draft jobs
│       │   ├── summarize.py             # Process summarization jobs
│       │   ├── embedding.py             # Process embedding jobs
│       │   └── notification.py          # Process notification delivery
│       └── main.py                      # Worker entrypoint
│
├── alembic/                             # Migration scripts
│   ├── env.py
│   └── versions/
│
├── tests/
│   ├── conftest.py                      # Fixtures (test DB, test client)
│   ├── test_auth/
│   ├── test_leads/
│   ├── test_deals/
│   └── ...
│
├── Dockerfile
├── docker-compose.yml                   # Local dev (Postgres + Redis + LocalStack)
├── pyproject.toml
└── alembic.ini
```

```
frontend/
├── app/                                 # Next.js App Router
│   ├── layout.tsx                       # Root layout (sidebar, topbar)
│   ├── page.tsx                         # Home dashboard
│   ├── login/page.tsx
│   ├── leads/
│   │   ├── page.tsx                     # List + Kanban views
│   │   └── [id]/page.tsx               # Lead detail
│   ├── contacts/
│   ├── accounts/
│   ├── deals/
│   ├── activities/
│   ├── documents/
│   ├── reports/
│   ├── settings/
│   └── search/
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── TopBar.tsx
│   │   ├── QuickCreate.tsx
│   │   └── NotificationBell.tsx
│   ├── ui/                              # shadcn/ui primitives
│   ├── data-table/                      # TanStack Table wrapper
│   ├── kanban/                          # dnd-kit Kanban board
│   ├── forms/                           # React Hook Form field components
│   ├── charts/                          # Recharts dashboard widgets
│   ├── timeline/                        # Activity timeline renderer
│   └── ai/                              # AI chat panel, score badge, risk alert
│
├── lib/
│   ├── api.ts                           # Axios/fetch wrapper with JWT interceptor
│   ├── auth.ts                          # Token storage, refresh logic
│   ├── hooks/                           # Custom TanStack Query hooks per module
│   └── utils.ts
│
├── store/
│   └── slices/                          # Redux Toolkit slices
│       ├── uiSlice.ts                   # Sidebar state, modals
│       └── chatSlice.ts                 # AI chat panel state
│
├── styles/
│   └── globals.css                      # Tailwind CSS base + custom tokens
│
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 3. SQLAlchemy ORM Models

### 3.1 Base Model

```python
# app/common/base.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class TenantMixin:
    """Every tenant-scoped table includes org_id for isolation."""
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
```

### 3.2 Organization Model

```python
# app/users/models.py
class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trial_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    subscription_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="trial"
    )  # trial | active | expired | cancelled

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="organization")
    pipeline_stages: Mapped[list["PipelineStage"]] = relationship(back_populates="organization")
    scoring_weights: Mapped[list["ScoringWeight"]] = relationship(back_populates="organization")
```

### 3.3 User Model

```python
class User(Base, TimestampMixin, TenantMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("org_id", "email", name="uq_users_org_email"),
        Index("ix_users_org_role", "org_id", "role"),
        Index("ix_users_reports_to", "reports_to"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # admin | sales_manager | sales_rep
    reports_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="users")
    manager: Mapped["User | None"] = relationship(remote_side=[id])
    direct_reports: Mapped[list["User"]] = relationship(
        back_populates="manager", foreign_keys=[reports_to]
    )
```

### 3.4 Lead Model

```python
# app/leads/models.py
class Lead(Base, TimestampMixin, TenantMixin):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_org_owner", "org_id", "owner_id"),
        Index("ix_leads_org_status", "org_id", "status"),
        Index("ix_leads_org_created", "org_id", "created_at", postgresql_using="btree"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str | None] = mapped_column(String(50))    # cold_email | referral | website | trade_show
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="new")  # new | qualified | converted | junk
    converted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    converted_contact_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"))
    converted_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    converted_deal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("deals.id"))

    # Relationships
    owner: Mapped["User"] = relationship()
    score: Mapped["LeadScore | None"] = relationship(back_populates="lead", uselist=False)


class LeadScore(Base):
    __tablename__ = "lead_scores"
    __table_args__ = (UniqueConstraint("lead_id", name="uq_lead_scores_lead"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)       # 0–100
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    scored_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="score")
```

### 3.5 Account, Contact, Deal Models

```python
# app/accounts/models.py
class Account(Base, TimestampMixin, TenantMixin):
    __tablename__ = "accounts"
    __table_args__ = (
        Index("ix_accounts_org_owner", "org_id", "owner_id"),
        Index("ix_accounts_org_name", "org_id", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    website: Mapped[str | None] = mapped_column(String(255))

    contacts: Mapped[list["Contact"]] = relationship(back_populates="account")
    deals: Mapped[list["Deal"]] = relationship(back_populates="account")


# app/contacts/models.py
class Contact(Base, TimestampMixin, TenantMixin):
    __tablename__ = "contacts"
    __table_args__ = (
        Index("ix_contacts_org_owner", "org_id", "owner_id"),
        Index("ix_contacts_account", "account_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))

    account: Mapped["Account"] = relationship(back_populates="contacts")


# app/deals/models.py
class PipelineStage(Base, TenantMixin):
    __tablename__ = "pipeline_stages"
    __table_args__ = (UniqueConstraint("org_id", "display_order", name="uq_stages_org_order"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    win_probability: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_won: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Deal(Base, TimestampMixin, TenantMixin):
    __tablename__ = "deals"
    __table_args__ = (
        Index("ix_deals_org_owner", "org_id", "owner_id"),
        Index("ix_deals_org_stage", "org_id", "stage_id"),
        Index("ix_deals_org_close", "org_id", "expected_close_date"),
        Index("ix_deals_account", "account_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    contact_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stage_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pipeline_stages.id"), nullable=False)
    expected_close_date: Mapped[date | None] = mapped_column(Date)
    next_followup_date: Mapped[date | None] = mapped_column(Date)
    last_interaction_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    account: Mapped["Account"] = relationship(back_populates="deals")
    stage: Mapped["PipelineStage"] = relationship()
    risk_alerts: Mapped[list["DealRiskAlert"]] = relationship(back_populates="deal")


class DealRiskAlert(Base, TenantMixin):
    __tablename__ = "deal_risk_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False)
    risk_type: Mapped[str] = mapped_column(String(50), nullable=False)   # stale_activity | close_date_near
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    is_dismissed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dismissed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    deal: Mapped["Deal"] = relationship(back_populates="risk_alerts")
```

### 3.6 Activity Model (Single-Table Inheritance)

```python
# app/activities/models.py
class Activity(Base, TimestampMixin, TenantMixin):
    __tablename__ = "activities"
    __table_args__ = (
        Index("ix_activities_org_owner", "org_id", "owner_id"),
        Index("ix_activities_related", "org_id", "related_to_type", "related_to_id"),
        Index("ix_activities_due_date", "due_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # task | meeting | call | note

    # Polymorphic link to any CRM record
    related_to_type: Mapped[str] = mapped_column(String(20), nullable=False)  # lead | contact | account | deal
    related_to_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    # Task-specific
    subject: Mapped[str | None] = mapped_column(String(255))
    due_date: Mapped[date | None] = mapped_column(Date)
    task_status: Mapped[str | None] = mapped_column(String(20))   # not_started | in_progress | completed
    priority: Mapped[str | None] = mapped_column(String(20))      # low | normal | high | highest

    # Meeting-specific
    title: Mapped[str | None] = mapped_column(String(255))
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    host_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Call-specific
    direction: Mapped[str | None] = mapped_column(String(10))     # inbound | outbound
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    # Note-specific
    body: Mapped[str | None] = mapped_column(Text)

    # Shared — for AI summarization
    transcript: Mapped[str | None] = mapped_column(Text)

    # Relationships
    ai_summary: Mapped["AISummary | None"] = relationship(back_populates="activity", uselist=False)
```

### 3.7 AI & Support Models

```python
# app/ai/models.py
class AISummary(Base):
    __tablename__ = "ai_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("activities.id"), unique=True, nullable=False
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_next_step: Mapped[str | None] = mapped_column(Text)
    follow_up_task_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("activities.id"))
    model_id: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    activity: Mapped["Activity"] = relationship(back_populates="ai_summary", foreign_keys=[activity_id])


class AIEmailDraft(Base):
    __tablename__ = "ai_email_drafts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    related_to_type: Mapped[str] = mapped_column(String(20), nullable=False)
    related_to_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    model_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending | completed | failed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user | assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_record_ids: Mapped[list | None] = mapped_column(ARRAY(UUID(as_uuid=True)))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    __table_args__ = (
        Index(
            "ix_embeddings_vector",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=False)  # pgvector VECTOR type
```

---

## 4. Pydantic Request / Response Schemas

### 4.1 Lead Schemas (Representative Example)

```python
# app/leads/schemas.py
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum


class LeadSource(str, Enum):
    COLD_EMAIL = "cold_email"
    REFERRAL = "referral"
    WEBSITE = "website"
    TRADE_SHOW = "trade_show"
    OTHER = "other"


class LeadStatus(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    JUNK = "junk"


class LeadCreate(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    company: str | None = Field(None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    source: LeadSource | None = None


class LeadUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    company: str | None = Field(None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    source: LeadSource | None = None
    status: LeadStatus | None = None


class LeadScoreResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)
    reason: str
    scored_at: datetime


class LeadResponse(BaseModel):
    id: UUID
    owner_id: UUID
    first_name: str
    last_name: str
    company: str | None
    email: str | None
    phone: str | None
    source: str | None
    status: LeadStatus
    score: LeadScoreResponse | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConvertLeadRequest(BaseModel):
    deal_name: str = Field(..., max_length=255)
    deal_amount: float = Field(default=0, ge=0)
    stage_id: UUID
    expected_close_date: str | None = None       # ISO date
    existing_account_id: UUID | None = None      # Provide to link instead of create


class ConvertLeadResponse(BaseModel):
    account_id: UUID
    contact_id: UUID
    deal_id: UUID


class LeadKanbanColumn(BaseModel):
    status: LeadStatus
    count: int
    leads: list[LeadResponse]
```

### 4.2 Cursor-Based Pagination Schema

```python
# app/common/pagination.py
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Generic, TypeVar

T = TypeVar("T")

class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: UUID | None = None
    has_more: bool
    total_count: int | None = None   # Optional, expensive on large tables

class PaginationParams(BaseModel):
    cursor: UUID | None = None
    limit: int = Field(default=50, ge=1, le=100)
    sort_by: str = "created_at"
    sort_order: str = "desc"         # asc | desc
```

---

## 5. Service Layer — Business Logic

### 5.1 Lead Service (Representative)

```python
# app/leads/service.py
class LeadService:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.user = current_user
        self.scope = ScopeFilter(current_user)

    async def list_leads(
        self, params: PaginationParams, filters: LeadFilterParams
    ) -> CursorPage[LeadResponse]:
        query = (
            select(Lead)
            .options(selectinload(Lead.score))
            .where(self.scope.apply(Lead))
        )

        # Apply filters
        if filters.status:
            query = query.where(Lead.status == filters.status)
        if filters.source:
            query = query.where(Lead.source == filters.source)
        if filters.owner_id:
            query = query.where(Lead.owner_id == filters.owner_id)

        # Cursor pagination
        query = CursorPaginator.apply(query, Lead, params)

        result = await self.db.execute(query)
        leads = result.scalars().all()

        return CursorPaginator.build_page(leads, params, LeadResponse)

    async def create_lead(self, data: LeadCreate) -> LeadResponse:
        lead = Lead(
            org_id=self.user.org_id,
            owner_id=self.user.id,
            **data.model_dump(),
        )
        self.db.add(lead)
        await self.db.flush()

        # Trigger initial scoring
        await self._score_lead(lead)

        await self.db.commit()
        await self.db.refresh(lead)
        return LeadResponse.model_validate(lead)

    async def convert_lead(self, lead_id: UUID, data: ConvertLeadRequest) -> ConvertLeadResponse:
        """Atomic: Lead → Account + Contact + Deal (see Section 9)."""
        # Full implementation in Section 9
        ...

    async def _score_lead(self, lead: Lead) -> None:
        """Synchronous rule-based scoring (see Section 14.1)."""
        score, reason = LeadScoringEngine(self.db, lead.org_id).score(lead)
        lead_score = LeadScore(
            lead_id=lead.id,
            score=score,
            reason=reason,
            scored_at=datetime.now(timezone.utc),
        )
        self.db.add(lead_score)
```

---

## 6. API Router Definitions

### 6.1 Lead Router (Representative)

```python
# app/leads/router.py
from fastapi import APIRouter, Depends, Query, status
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/v1/leads", tags=["Leads"])


@router.get("", response_model=CursorPage[LeadResponse])
async def list_leads(
    cursor: UUID | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    status: LeadStatus | None = Query(None),
    source: LeadSource | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.list_leads(
        PaginationParams(cursor=cursor, limit=limit, sort_by=sort_by, sort_order=sort_order),
        LeadFilterParams(status=status, source=source),
    )


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.create_lead(data)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.get_lead(lead_id)


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: UUID,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.update_lead(lead_id, data)


@router.post("/{lead_id}/convert", response_model=ConvertLeadResponse, status_code=status.HTTP_201_CREATED)
async def convert_lead(
    lead_id: UUID,
    data: ConvertLeadRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.convert_lead(lead_id, data)


@router.post("/import", status_code=status.HTTP_202_ACCEPTED)
async def import_leads(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.import_csv(file)


@router.get("/kanban", response_model=list[LeadKanbanColumn])
async def kanban_view(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = LeadService(db, user)
    return await service.get_kanban()
```

### 6.2 Main App — Router Registration

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.common.middleware import RequestIDMiddleware, TimingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: warm up DB pool, cache connection
    yield
    # Shutdown: dispose engine
    await engine.dispose()

app = FastAPI(
    title="Crusource CRM API",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.leads.router import router as leads_router
from app.contacts.router import router as contacts_router
from app.accounts.router import router as accounts_router
from app.deals.router import router as deals_router
from app.activities.router import router as activities_router
from app.documents.router import router as documents_router
from app.dashboard.router import router as dashboard_router
from app.reports.router import router as reports_router
from app.ai.router import router as ai_router
from app.search.router import router as search_router
from app.notifications.router import router as notifications_router
from app.settings.router import router as settings_router

for r in [
    auth_router, users_router, leads_router, contacts_router,
    accounts_router, deals_router, activities_router, documents_router,
    dashboard_router, reports_router, ai_router, search_router,
    notifications_router, settings_router,
]:
    app.include_router(r)
```

---

## 7. Authentication & Authorization Implementation

### 7.1 JWT Encoding / Decoding

```python
# app/auth/jwt.py
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def encode_jwt(user_id: str, org_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "org_id": org_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError as e:
        raise AuthenticationError("Invalid or expired token") from e
```

### 7.2 Login Service

```python
# app/auth/service.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, email: str, password: str) -> TokenResponse:
        # 1. Find active user
        result = await self.db.execute(
            select(User).where(User.email == email, User.is_active == True)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise AuthenticationError("Invalid credentials")

        # 2. Verify password
        if not pwd_context.verify(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        # 3. Check org subscription
        org = await self.db.get(Organization, user.org_id)
        if org.subscription_status == "expired":
            raise ForbiddenError("Organization subscription has expired")

        # 4. Generate JWT
        token = encode_jwt(str(user.id), str(user.org_id), user.role)
        return TokenResponse(access_token=token, expires_in=ACCESS_TOKEN_EXPIRE_HOURS * 3600)
```

### 7.3 Dependency — `get_current_user`

```python
# app/dependencies.py
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_jwt(credentials.credentials)

    user = await db.get(User, uuid.UUID(payload["sub"]))
    if not user or not user.is_active:
        raise AuthenticationError("User not found or deactivated")
    if str(user.org_id) != payload["org_id"]:
        raise AuthenticationError("Token org mismatch")

    return user


def require_role(*roles: str):
    """Dependency factory for endpoint role guards."""
    async def guard(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise ForbiddenError(f"Requires role: {', '.join(roles)}")
        return user
    return guard
```

---

## 8. Row-Level Scope Filter Implementation

```python
# app/common/scope.py
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload


class ScopeFilter:
    """Applies row-level visibility based on the user's role.

    - admin:         org_id = user.org_id  (sees everything in org)
    - sales_manager: owner_id IN (self + direct_reports)
    - sales_rep:     owner_id = self
    """

    def __init__(self, user: "User"):
        self.user = user
        self._direct_report_ids: list[uuid.UUID] | None = None

    async def load_direct_reports(self, db: AsyncSession) -> None:
        """Pre-load direct report IDs for sales_manager (cached per request)."""
        if self.user.role == "sales_manager" and self._direct_report_ids is None:
            result = await db.execute(
                select(User.id).where(User.reports_to == self.user.id)
            )
            self._direct_report_ids = list(result.scalars().all())

    def apply(self, model_class) -> list:
        """Returns a list of WHERE conditions to chain onto a query.

        Usage:
            query = select(Lead).where(*self.scope.apply(Lead))
        """
        conditions = [model_class.org_id == self.user.org_id]

        if self.user.role == "admin":
            pass  # No further filter
        elif self.user.role == "sales_manager":
            visible_ids = [self.user.id] + (self._direct_report_ids or [])
            conditions.append(model_class.owner_id.in_(visible_ids))
        elif self.user.role == "sales_rep":
            conditions.append(model_class.owner_id == self.user.id)

        return conditions
```

**Usage in every service method:**

```python
query = select(Deal).where(*self.scope.apply(Deal))
```

---

## 9. Lead Conversion — Atomic Transaction

```python
# app/leads/service.py (convert_lead method)
async def convert_lead(self, lead_id: UUID, data: ConvertLeadRequest) -> ConvertLeadResponse:
    """
    Atomic transaction: Lead → Account + Contact + Deal.
    If an existing account is provided, link to it; otherwise create a new one.
    """
    async with self.db.begin_nested():  # Savepoint for rollback on conflict
        # 1. Fetch and validate lead
        lead = await self._get_owned_lead(lead_id)
        if lead.status == "converted":
            raise ConflictError("Lead is already converted")
        if lead.status == "junk":
            raise ValidationError("Cannot convert a junk lead")

        # 2. Resolve or create Account
        if data.existing_account_id:
            account = await self.db.get(Account, data.existing_account_id)
            if not account or account.org_id != self.user.org_id:
                raise NotFoundError("Account not found")
        else:
            # Check for duplicates
            existing = await self.db.execute(
                select(Account).where(
                    Account.org_id == self.user.org_id,
                    func.lower(Account.name) == func.lower(lead.company or ""),
                )
            )
            duplicate = existing.scalar_one_or_none()
            if duplicate:
                raise ConflictError(
                    f"Duplicate account detected",
                    details={"existing_account_id": str(duplicate.id)},
                )

            account = Account(
                org_id=self.user.org_id,
                owner_id=self.user.id,
                name=lead.company or f"{lead.first_name} {lead.last_name}",
            )
            self.db.add(account)
            await self.db.flush()  # Get account.id

        # 3. Create Contact
        contact = Contact(
            org_id=self.user.org_id,
            owner_id=self.user.id,
            account_id=account.id,
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
        )
        self.db.add(contact)
        await self.db.flush()

        # 4. Create Deal
        deal = Deal(
            org_id=self.user.org_id,
            owner_id=self.user.id,
            account_id=account.id,
            contact_id=contact.id,
            name=data.deal_name,
            amount=data.deal_amount,
            stage_id=data.stage_id,
            expected_close_date=data.expected_close_date,
        )
        self.db.add(deal)
        await self.db.flush()

        # 5. Update lead to converted
        lead.status = "converted"
        lead.converted_at = datetime.now(timezone.utc)
        lead.converted_account_id = account.id
        lead.converted_contact_id = contact.id
        lead.converted_deal_id = deal.id

    await self.db.commit()

    # 6. Invalidate caches
    await cache.delete_pattern(f"dash:home:{self.user.org_id}:*")
    await cache.delete_pattern(f"kanban:leads:{self.user.org_id}:*")

    return ConvertLeadResponse(
        account_id=account.id,
        contact_id=contact.id,
        deal_id=deal.id,
    )
```

---

## 10. Deal Pipeline — Stage Transition Logic

```python
# app/deals/service.py
class DealService:
    async def update_deal(self, deal_id: UUID, data: DealUpdate) -> DealResponse:
        deal = await self._get_owned_deal(deal_id)
        old_stage_id = deal.stage_id

        # Apply updates
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(deal, field, value)

        # Side effects on stage change
        if data.stage_id and data.stage_id != old_stage_id:
            await self._on_stage_change(deal, old_stage_id, data.stage_id)

        deal.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        return DealResponse.model_validate(deal)

    async def _on_stage_change(
        self, deal: Deal, old_stage_id: UUID, new_stage_id: UUID
    ) -> None:
        """Side effects triggered by a deal stage change."""
        # 1. Update last_interaction_at
        deal.last_interaction_at = datetime.now(timezone.utc)

        # 2. Clear active risk alerts (activity happened)
        await self.db.execute(
            update(DealRiskAlert)
            .where(
                DealRiskAlert.deal_id == deal.id,
                DealRiskAlert.is_dismissed == False,
            )
            .values(is_dismissed=True, dismissed_by=self.user.id)
        )

        # 3. If closed, clear next_followup_date
        new_stage = await self.db.get(PipelineStage, new_stage_id)
        if new_stage.is_closed:
            deal.next_followup_date = None

        # 4. Invalidate caches
        await cache.delete(f"dash:home:{deal.org_id}:{deal.owner_id}")
        await cache.delete(f"dash:analytics:{deal.org_id}")
        await cache.delete_pattern(f"kanban:deals:{deal.org_id}:*")

    async def get_kanban(self) -> list[DealKanbanColumn]:
        """Single query: GROUP BY stage with column totals."""
        query = (
            select(
                PipelineStage.id,
                PipelineStage.name,
                PipelineStage.display_order,
                PipelineStage.win_probability,
                func.count(Deal.id).label("count"),
                func.coalesce(func.sum(Deal.amount), 0).label("total_amount"),
            )
            .outerjoin(Deal, and_(
                Deal.stage_id == PipelineStage.id,
                *self.scope.apply(Deal),
            ))
            .where(PipelineStage.org_id == self.user.org_id)
            .group_by(PipelineStage.id)
            .order_by(PipelineStage.display_order)
        )

        result = await self.db.execute(query)
        columns = result.all()

        # Fetch deals per column (separate query for pagination)
        kanban = []
        for col in columns:
            deals_query = (
                select(Deal)
                .where(Deal.stage_id == col.id, *self.scope.apply(Deal))
                .order_by(Deal.updated_at.desc())
                .limit(50)
            )
            deals = (await self.db.execute(deals_query)).scalars().all()

            kanban.append(DealKanbanColumn(
                stage_id=col.id,
                stage_name=col.name,
                display_order=col.display_order,
                win_probability=col.win_probability,
                deal_count=col.count,
                total_amount=col.total_amount,
                deals=[DealCardResponse.model_validate(d) for d in deals],
            ))

        return kanban
```

---

## 11. Activity Timeline — Unified Query

```python
# app/activities/service.py
class ActivityService:
    async def get_timeline(
        self, entity_type: str, entity_id: UUID, params: PaginationParams
    ) -> CursorPage[TimelineEntry]:
        """
        Single query on activities table (STI) with LEFT JOIN ai_summaries.
        Returns tasks, meetings, calls, notes with inline AI summaries.
        """
        query = (
            select(Activity)
            .options(selectinload(Activity.ai_summary))
            .where(
                Activity.related_to_type == entity_type,
                Activity.related_to_id == entity_id,
                *self.scope.apply(Activity),
            )
            .order_by(Activity.created_at.desc())
        )

        query = CursorPaginator.apply(query, Activity, params)
        result = await self.db.execute(query)
        activities = result.scalars().all()

        entries = []
        for act in activities:
            entry = TimelineEntry(
                id=act.id,
                activity_type=act.activity_type,
                created_at=act.created_at,
                owner_id=act.owner_id,
            )

            # Type-specific fields
            if act.activity_type == "task":
                entry.task_data = TaskData(
                    subject=act.subject,
                    due_date=act.due_date,
                    status=act.task_status,
                    priority=act.priority,
                )
            elif act.activity_type == "meeting":
                entry.meeting_data = MeetingData(
                    title=act.title,
                    start_time=act.start_time,
                    end_time=act.end_time,
                )
            elif act.activity_type == "call":
                entry.call_data = CallData(
                    direction=act.direction,
                    duration_seconds=act.duration_seconds,
                    start_time=act.start_time,
                )
            elif act.activity_type == "note":
                entry.note_data = NoteData(body=act.body)

            # AI summary (shown by default on timeline, full notes one click away)
            if act.ai_summary:
                entry.ai_summary = AISummaryData(
                    summary_text=act.ai_summary.summary_text,
                    suggested_next_step=act.ai_summary.suggested_next_step,
                    has_follow_up_task=act.ai_summary.follow_up_task_id is not None,
                )

            entries.append(entry)

        return CursorPaginator.build_page(entries, params)
```

---

## 12. Document Upload / Download — Pre-Signed URL Flow

```python
# app/documents/service.py
import boto3
from app.config import settings


class DocumentService:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.user = current_user
        self.s3 = boto3.client("s3", region_name=settings.AWS_REGION)
        self.scope = ScopeFilter(current_user)

    async def generate_upload_url(self, data: UploadURLRequest) -> UploadURLResponse:
        """Generate pre-signed PUT URL for direct browser → S3 upload."""
        s3_key = (
            f"{self.user.org_id}/{data.related_to_type}/{data.related_to_id}"
            f"/{uuid.uuid4()}/{data.file_name}"
        )

        url = self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.S3_BUCKET,
                "Key": s3_key,
                "ContentType": data.content_type,
            },
            ExpiresIn=900,  # 15 minutes
        )

        return UploadURLResponse(upload_url=url, s3_key=s3_key)

    async def register_document(self, data: DocumentRegister) -> DocumentResponse:
        """After successful S3 upload, register metadata in DB."""
        doc = Document(
            org_id=self.user.org_id,
            owner_id=self.user.id,
            file_name=data.file_name,
            file_size_bytes=data.file_size_bytes,
            content_type=data.content_type,
            s3_key=data.s3_key,
            related_to_type=data.related_to_type,
            related_to_id=data.related_to_id,
            uploaded_at=datetime.now(timezone.utc),
        )
        self.db.add(doc)
        await self.db.commit()

        # Enqueue embedding job for RAG
        await sqs.send_message(
            queue_url=settings.SQS_EMBEDDINGS_QUEUE,
            message_body=json.dumps({
                "job_type": "embed_document",
                "org_id": str(self.user.org_id),
                "source_type": "document",
                "source_id": str(doc.id),
                "s3_key": data.s3_key,
            }),
        )

        return DocumentResponse.model_validate(doc)

    async def generate_download_url(self, doc_id: UUID) -> DownloadURLResponse:
        """Generate pre-signed GET URL for direct S3 → browser download."""
        doc = await self._get_scoped_document(doc_id)

        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET, "Key": doc.s3_key},
            ExpiresIn=900,
        )

        return DownloadURLResponse(download_url=url, file_name=doc.file_name)

    async def delete_document(self, doc_id: UUID) -> None:
        """Delete document metadata from DB and object from S3."""
        doc = await self._get_scoped_document(doc_id)

        # Delete from S3
        self.s3.delete_object(Bucket=settings.S3_BUCKET, Key=doc.s3_key)

        # Delete embeddings
        await self.db.execute(
            delete(DocumentEmbedding).where(
                DocumentEmbedding.source_type == "document",
                DocumentEmbedding.source_id == doc.id,
            )
        )

        # Delete metadata
        await self.db.delete(doc)
        await self.db.commit()
```

---

## 13. CSV Import — Bulk Processing

```python
# app/common/csv_import.py
import csv
import io
from fastapi import UploadFile


class CSVImporter:
    """Generic CSV import processor for any CRM module."""

    MAX_ROWS = 5000
    CHUNK_SIZE = 100

    def __init__(self, db: AsyncSession, user: User, model_class, schema_class):
        self.db = db
        self.user = user
        self.model_class = model_class
        self.schema_class = schema_class

    async def process(self, file: UploadFile) -> ImportResult:
        content = await file.read()
        reader = csv.DictReader(io.StringIO(content.decode("utf-8")))

        created = 0
        errors = []

        rows = list(reader)
        if len(rows) > self.MAX_ROWS:
            raise ValidationError(f"CSV exceeds max {self.MAX_ROWS} rows")

        # Process in chunks for batch INSERT efficiency
        for chunk_start in range(0, len(rows), self.CHUNK_SIZE):
            chunk = rows[chunk_start : chunk_start + self.CHUNK_SIZE]
            records = []

            for i, row in enumerate(chunk, start=chunk_start + 1):
                try:
                    validated = self.schema_class(**row)
                    record = self.model_class(
                        org_id=self.user.org_id,
                        owner_id=self.user.id,
                        **validated.model_dump(),
                    )
                    records.append(record)
                except Exception as e:
                    errors.append({"row": i, "error": str(e)})

            self.db.add_all(records)
            created += len(records)

        await self.db.commit()

        return ImportResult(
            total_rows=len(rows),
            created=created,
            error_count=len(errors),
            errors=errors[:50],  # Cap error details
        )
```

---

## 14. AI Subsystem — Detailed Implementation

### 14.1 Lead Scoring Algorithm (Rule-Based, No LLM)

```python
# app/ai/scoring.py
class LeadScoringEngine:
    """
    Weighted signal evaluation → 0–100 score + plain-language reason.
    Runs synchronously (no LLM).
    Triggers: overnight cron + instantly on status/activity change.
    """

    DEFAULT_WEIGHTS = {
        "source_referral": 25,
        "source_website": 15,
        "source_cold_email": 5,
        "source_trade_show": 20,
        "response_time_1h": 20,
        "response_time_24h": 10,
        "response_time_slow": 0,
        "status_qualified": 15,
        "status_new": 5,
        "has_email": 5,
        "has_phone": 5,
        "has_company": 5,
    }

    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
        self.weights: dict[str, float] = {}

    async def load_weights(self) -> None:
        """Load org-specific weights or fall back to defaults."""
        result = await self.db.execute(
            select(ScoringWeight).where(ScoringWeight.org_id == self.org_id)
        )
        custom = {w.signal_name: float(w.weight) for w in result.scalars().all()}
        self.weights = {**self.DEFAULT_WEIGHTS, **custom}

    async def score(self, lead: "Lead") -> tuple[int, str]:
        await self.load_weights()

        points = 0
        reasons = []

        # Signal: Lead source
        source_key = f"source_{lead.source}" if lead.source else None
        if source_key and source_key in self.weights:
            pts = self.weights[source_key]
            points += pts
            if pts > 0:
                reasons.append(f"{lead.source.replace('_', ' ').title()} source (+{pts})")

        # Signal: Response time (time between creation and first activity)
        first_activity = await self.db.execute(
            select(func.min(Activity.created_at)).where(
                Activity.related_to_type == "lead",
                Activity.related_to_id == lead.id,
            )
        )
        first_at = first_activity.scalar_one_or_none()
        if first_at:
            delta = (first_at - lead.created_at).total_seconds()
            if delta <= 3600:
                pts = self.weights["response_time_1h"]
                points += pts
                reasons.append(f"Contacted within 1 hour (+{pts})")
            elif delta <= 86400:
                pts = self.weights["response_time_24h"]
                points += pts
                reasons.append(f"Contacted within 24 hours (+{pts})")

        # Signal: Lead status
        status_key = f"status_{lead.status}"
        if status_key in self.weights:
            pts = self.weights[status_key]
            points += pts
            if pts > 0:
                reasons.append(f"Status: {lead.status.title()} (+{pts})")

        # Signal: Completeness
        if lead.email:
            points += self.weights["has_email"]
        if lead.phone:
            points += self.weights["has_phone"]
        if lead.company:
            points += self.weights["has_company"]

        # Clamp to 0–100
        score = max(0, min(100, points))
        reason_text = "; ".join(reasons) if reasons else "No strong signals detected"

        return score, reason_text
```

### 14.2 Deal Risk Alert Scanner (Rule-Based, No LLM)

```python
# app/ai/risk_alerts.py
class DealRiskScanner:
    """
    Daily cron: scans open deals for risk conditions.
    Conditions:
      - No activity logged in ≥ 7 days
      - Expected close date ≤ 7 days from now without recent activity
    """

    STALE_DAYS = 7
    CLOSE_WARNING_DAYS = 7

    async def scan_org(self, db: AsyncSession, org_id: UUID) -> int:
        now = datetime.now(timezone.utc)
        today = now.date()
        alerts_created = 0

        # Get all open deals (non-closed stages)
        open_deals = await db.execute(
            select(Deal)
            .join(PipelineStage)
            .where(
                Deal.org_id == org_id,
                PipelineStage.is_closed == False,
            )
        )

        for deal in open_deals.scalars().all():
            risks = []

            # Check stale activity
            days_since = None
            if deal.last_interaction_at:
                days_since = (now - deal.last_interaction_at).days
                if days_since >= self.STALE_DAYS:
                    risks.append(("stale_activity", f"No activity in {days_since} days"))
            else:
                days_since_created = (now - deal.created_at).days
                if days_since_created >= self.STALE_DAYS:
                    risks.append(("stale_activity", f"No activity since creation ({days_since_created} days)"))

            # Check close date proximity
            if deal.expected_close_date:
                days_to_close = (deal.expected_close_date - today).days
                if 0 <= days_to_close <= self.CLOSE_WARNING_DAYS:
                    reason = f"Closing date in {days_to_close} days"
                    if days_since and days_since >= 3:
                        reason += f", last activity {days_since} days ago"
                    risks.append(("close_date_near", reason))

            # Create alerts (skip if active un-dismissed alert already exists)
            for risk_type, reason in risks:
                existing = await db.execute(
                    select(DealRiskAlert).where(
                        DealRiskAlert.deal_id == deal.id,
                        DealRiskAlert.risk_type == risk_type,
                        DealRiskAlert.is_dismissed == False,
                    )
                )
                if not existing.scalar_one_or_none():
                    alert = DealRiskAlert(
                        org_id=org_id,
                        deal_id=deal.id,
                        risk_type=risk_type,
                        reason=reason,
                        created_at=now,
                    )
                    db.add(alert)
                    alerts_created += 1

        await db.commit()
        return alerts_created
```

### 14.3 Email Drafting — Async SQS Flow

```python
# app/ai/service.py
class AIService:
    async def request_email_draft(
        self, related_to_type: str, related_to_id: UUID
    ) -> AIJobAccepted:
        """Enqueue email draft generation → returns 202."""
        draft = AIEmailDraft(
            org_id=self.user.org_id,
            user_id=self.user.id,
            related_to_type=related_to_type,
            related_to_id=related_to_id,
            subject="",
            body="",
            model_id="claude-sonnet-4-20250514",
            status="pending",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(draft)
        await self.db.commit()

        await sqs.send_message(
            queue_url=settings.SQS_AI_JOBS_QUEUE,
            message_body=json.dumps({
                "job_type": "email_draft",
                "job_id": str(draft.id),
                "org_id": str(self.user.org_id),
                "user_id": str(self.user.id),
                "payload": {
                    "record_type": related_to_type,
                    "record_id": str(related_to_id),
                },
            }),
        )

        return AIJobAccepted(job_id=draft.id, status="pending")
```

```python
# app/workers/handlers/email_draft.py
class EmailDraftHandler:
    async def handle(self, message: dict) -> None:
        """Worker-side: fetch context → build prompt → call Claude → persist result."""
        async with get_db_session() as db:
            draft = await db.get(AIEmailDraft, uuid.UUID(message["job_id"]))

            # 1. Fetch record + recent activities for context
            record = await self._fetch_record(
                db, message["payload"]["record_type"], message["payload"]["record_id"]
            )
            activities = await self._fetch_recent_activities(
                db, message["payload"]["record_type"], message["payload"]["record_id"],
                limit=10,
            )

            # 2. Build prompt
            prompt = PromptBuilder.email_draft(record, activities)

            # 3. Call Claude API
            response = await claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # 4. Parse and persist
            content = response.content[0].text
            subject, body = self._parse_email(content)

            draft.subject = subject
            draft.body = body
            draft.status = "completed"
            await db.commit()
```

### 14.4 RAG Chatbot — Query Pipeline

```python
# app/ai/rag.py
class RAGChatService:
    async def chat(self, message: str, session_id: UUID) -> ChatResponse:
        """
        1. Embed the user query
        2. ANN search in document_embeddings (scoped)
        3. Build context-augmented prompt
        4. Call Claude
        5. Return answer with source_record_ids
        """
        # 1. Embed query
        query_embedding = await self._embed_text(message)

        # 2. Scoped ANN search
        visible_ids = await self._get_visible_record_ids()
        top_chunks = await self.db.execute(
            select(DocumentEmbedding)
            .where(
                DocumentEmbedding.org_id == self.user.org_id,
                DocumentEmbedding.source_id.in_(visible_ids),
            )
            .order_by(DocumentEmbedding.embedding.cosine_distance(query_embedding))
            .limit(10)
        )
        chunks = top_chunks.scalars().all()

        # 3. Build prompt with context
        context = "\n\n".join([c.content_text for c in chunks])
        source_ids = list(set(c.source_id for c in chunks))

        prompt = PromptBuilder.rag_chat(
            user_message=message,
            context=context,
            chat_history=await self._get_session_history(session_id),
        )

        # 4. Call Claude
        response = await claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.content[0].text

        # 5. Persist messages
        await self._save_message(session_id, "user", message)
        await self._save_message(session_id, "assistant", answer, source_ids)

        return ChatResponse(content=answer, source_record_ids=source_ids)
```

### 14.5 Embedding Pipeline

```python
# app/workers/handlers/embedding.py
class EmbeddingHandler:
    CHUNK_SIZE = 512  # tokens

    async def handle(self, message: dict) -> None:
        async with get_db_session() as db:
            # 1. Fetch source text (record fields or document from S3)
            text = await self._fetch_text(db, message)

            # 2. Chunk text
            chunks = self._chunk_text(text, self.CHUNK_SIZE)

            # 3. Delete existing embeddings for this source
            await db.execute(
                delete(DocumentEmbedding).where(
                    DocumentEmbedding.source_type == message["source_type"],
                    DocumentEmbedding.source_id == uuid.UUID(message["source_id"]),
                )
            )

            # 4. Embed and insert
            for i, chunk in enumerate(chunks):
                embedding = await self._embed_text(chunk)
                db.add(DocumentEmbedding(
                    org_id=uuid.UUID(message["org_id"]),
                    source_type=message["source_type"],
                    source_id=uuid.UUID(message["source_id"]),
                    chunk_index=i,
                    content_text=chunk,
                    embedding=embedding,
                ))

            await db.commit()

    def _chunk_text(self, text: str, max_tokens: int) -> list[str]:
        """Split text into overlapping chunks by token count."""
        words = text.split()
        chunks = []
        stride = max_tokens - 50  # 50-token overlap

        for start in range(0, len(words), stride):
            chunk = " ".join(words[start : start + max_tokens])
            chunks.append(chunk)
            if start + max_tokens >= len(words):
                break

        return chunks
```

---

## 15. Caching — Implementation Details

```python
# app/common/cache.py
import json
import redis.asyncio as redis
from app.config import settings

pool = redis.ConnectionPool.from_url(settings.REDIS_URL)


class CacheService:
    def __init__(self):
        self.client = redis.Redis(connection_pool=pool)

    async def get(self, key: str) -> dict | None:
        data = await self.client.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl_seconds: int) -> None:
        await self.client.setex(key, ttl_seconds, json.dumps(value, default=str))

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        """Delete all keys matching a glob pattern. Use sparingly."""
        async for key in self.client.scan_iter(match=pattern, count=100):
            await self.client.delete(key)

    # Rate limiting
    async def check_rate_limit(self, user_id: str, endpoint: str, limit: int, window: int) -> bool:
        """Sliding window rate limiter. Returns True if allowed."""
        key = f"ratelimit:{user_id}:{endpoint}"
        current = await self.client.incr(key)
        if current == 1:
            await self.client.expire(key, window)
        return current <= limit


cache = CacheService()
```

**Cache key patterns and TTLs (from HLD):**

| Target | Key | TTL | Invalidation Event |
|---|---|---|---|
| Home Dashboard | `dash:home:{org_id}:{user_id}` | 5 min | Activity/deal/lead write |
| Analytics Dashboard | `dash:analytics:{org_id}` | 10 min | Deal/lead write |
| Kanban views | `kanban:{type}:{org_id}:{user_id}` | 2 min | Status/stage change |
| Pre-built Reports | `report:{slug}:{org_id}:{user_id}` | 15 min | Underlying data change |
| User's direct reports | `reports:{user_id}` | 30 min | Admin "Reports To" change |

---

## 16. Background Workers — SQS Consumer

```python
# app/workers/consumer.py
import asyncio
import json
import boto3
from app.config import settings
from app.workers.handlers import HANDLER_REGISTRY

sqs = boto3.client("sqs", region_name=settings.AWS_REGION)


async def consume_queue(queue_url: str) -> None:
    """Long-poll SQS consumer loop."""
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,              # Long-poll
            VisibilityTimeout=300,           # 5 min buffer for LLM calls
        )

        messages = response.get("Messages", [])
        for msg in messages:
            try:
                body = json.loads(msg["Body"])
                handler = HANDLER_REGISTRY[body["job_type"]]
                await handler.handle(body)

                # Delete on success
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg["ReceiptHandle"],
                )
            except Exception as e:
                logger.error(f"Worker error: {e}", extra={"message_id": msg["MessageId"]})
                # Message returns to queue after visibility timeout
                # After 3 failures → DLQ


HANDLER_REGISTRY = {
    "email_draft": EmailDraftHandler(),
    "summarize": SummarizeHandler(),
    "embed_document": EmbeddingHandler(),
    "notification": NotificationHandler(),
}


# app/workers/main.py
async def main():
    """Worker entrypoint — runs parallel consumers for all queues."""
    await asyncio.gather(
        consume_queue(settings.SQS_AI_JOBS_QUEUE),
        consume_queue(settings.SQS_EMBEDDINGS_QUEUE),
        consume_queue(settings.SQS_NOTIFICATIONS_QUEUE),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 17. Global Search — Implementation

```python
# app/search/service.py
class SearchService:
    async def search(self, query: str) -> list[SearchResult]:
        """
        UNION ALL across leads, contacts, accounts, deals.
        Uses ILIKE on name/email/company fields.
        Scoped by org_id + user visibility. Limited to top 20.
        """
        pattern = f"%{query}%"

        queries = []

        # Leads
        leads_q = (
            select(
                literal("lead").label("type"),
                Lead.id,
                func.concat(Lead.first_name, " ", Lead.last_name).label("name"),
                Lead.email.label("detail"),
            )
            .where(
                *self.scope.apply(Lead),
                or_(
                    func.concat(Lead.first_name, " ", Lead.last_name).ilike(pattern),
                    Lead.email.ilike(pattern),
                    Lead.company.ilike(pattern),
                ),
            )
        )
        queries.append(leads_q)

        # Contacts
        contacts_q = (
            select(
                literal("contact").label("type"),
                Contact.id,
                func.concat(Contact.first_name, " ", Contact.last_name).label("name"),
                Contact.email.label("detail"),
            )
            .where(
                *self.scope.apply(Contact),
                or_(
                    func.concat(Contact.first_name, " ", Contact.last_name).ilike(pattern),
                    Contact.email.ilike(pattern),
                ),
            )
        )
        queries.append(contacts_q)

        # Accounts
        accounts_q = (
            select(
                literal("account").label("type"),
                Account.id,
                Account.name,
                Account.website.label("detail"),
            )
            .where(
                *self.scope.apply(Account),
                Account.name.ilike(pattern),
            )
        )
        queries.append(accounts_q)

        # Deals
        deals_q = (
            select(
                literal("deal").label("type"),
                Deal.id,
                Deal.name,
                cast(Deal.amount, String).label("detail"),
            )
            .where(
                *self.scope.apply(Deal),
                Deal.name.ilike(pattern),
            )
        )
        queries.append(deals_q)

        # UNION ALL + LIMIT 20
        union = union_all(*queries).limit(20)
        result = await self.db.execute(union)

        return [
            SearchResult(type=row.type, id=row.id, name=row.name, detail=row.detail)
            for row in result.all()
        ]
```

---

## 18. Notification System

```python
# app/notifications/service.py
class NotificationService:
    """
    V1: HTTP polling (GET /notifications every 30s).
    Post-V1 upgrade path: WebSocket push.
    """

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        user_id: UUID,
        org_id: UUID,
        notification_type: str,
        title: str,
        related_to_type: str | None = None,
        related_to_id: UUID | None = None,
    ) -> None:
        notification = Notification(
            user_id=user_id,
            org_id=org_id,
            type=notification_type,
            title=title,
            related_to_type=related_to_type,
            related_to_id=related_to_id,
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )
        db.add(notification)

    async def list_notifications(
        self, unread_only: bool = False
    ) -> list[NotificationResponse]:
        query = (
            select(Notification)
            .where(Notification.user_id == self.user.id)
            .order_by(Notification.created_at.desc())
            .limit(50)
        )
        if unread_only:
            query = query.where(Notification.is_read == False)

        result = await self.db.execute(query)
        return [NotificationResponse.model_validate(n) for n in result.scalars().all()]

    async def mark_read(self, notification_id: UUID) -> None:
        notif = await self.db.get(Notification, notification_id)
        if notif and notif.user_id == self.user.id:
            notif.is_read = True
            await self.db.commit()
```

**Notification trigger events:**

| Event | Type | Recipient | Triggered By |
|---|---|---|---|
| Task assigned to user | `assignment` | Assigned user | Activity creation with different `owner_id` |
| Task due date reached | `task_due` | Task owner | Daily cron job |
| Deal risk alert created | `deal_risk` | Deal owner | Risk scanner cron |

---

## 19. Dashboard & Reporting — Query Specifications

### 19.1 Home Dashboard Queries

```python
# app/dashboard/service.py
class DashboardService:
    async def get_home_dashboard(self) -> HomeDashboard:
        cache_key = f"dash:home:{self.user.org_id}:{self.user.id}"
        cached = await cache.get(cache_key)
        if cached:
            return HomeDashboard(**cached)

        scope = self.scope.apply

        # KPI 1: Open deals count
        open_deals = await self.db.execute(
            select(func.count(Deal.id))
            .join(PipelineStage)
            .where(*scope(Deal), PipelineStage.is_closed == False)
        )

        # KPI 2: Untouched deals (no activity in 7+ days)
        untouched_deals = await self.db.execute(
            select(func.count(Deal.id))
            .join(PipelineStage)
            .where(
                *scope(Deal),
                PipelineStage.is_closed == False,
                or_(
                    Deal.last_interaction_at < func.now() - text("INTERVAL '7 days'"),
                    Deal.last_interaction_at.is_(None),
                ),
            )
        )

        # KPI 3: My leads count
        my_leads = await self.db.execute(
            select(func.count(Lead.id)).where(*scope(Lead), Lead.status != "converted")
        )

        # KPI 4: My calls today
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
        my_calls = await self.db.execute(
            select(func.count(Activity.id)).where(
                *scope(Activity),
                Activity.activity_type == "call",
                Activity.created_at >= today_start,
            )
        )

        # Widget: My Open Tasks (top 10)
        open_tasks = await self.db.execute(
            select(Activity)
            .where(
                *scope(Activity),
                Activity.activity_type == "task",
                Activity.task_status != "completed",
            )
            .order_by(Activity.due_date.asc().nullslast())
            .limit(10)
        )

        # Widget: My Meetings (next 5)
        upcoming_meetings = await self.db.execute(
            select(Activity)
            .where(
                *scope(Activity),
                Activity.activity_type == "meeting",
                Activity.start_time >= func.now(),
            )
            .order_by(Activity.start_time.asc())
            .limit(5)
        )

        # Widget: Today's Leads
        todays_leads = await self.db.execute(
            select(Lead)
            .where(*scope(Lead), Lead.created_at >= today_start)
            .order_by(Lead.created_at.desc())
            .limit(10)
        )

        # Widget: Deals Closing This Month
        month_end = today_start.replace(month=today_start.month + 1, day=1) - timedelta(days=1)
        closing_deals = await self.db.execute(
            select(Deal)
            .join(PipelineStage)
            .where(
                *scope(Deal),
                PipelineStage.is_closed == False,
                Deal.expected_close_date <= month_end.date(),
                Deal.expected_close_date >= today_start.date(),
            )
            .order_by(Deal.expected_close_date.asc())
            .limit(10)
        )

        dashboard = HomeDashboard(
            kpis=DashboardKPIs(
                open_deals=open_deals.scalar(),
                untouched_deals=untouched_deals.scalar(),
                my_leads=my_leads.scalar(),
                my_calls_today=my_calls.scalar(),
            ),
            open_tasks=[...],
            upcoming_meetings=[...],
            todays_leads=[...],
            closing_deals=[...],
        )

        await cache.set(cache_key, dashboard.model_dump(), ttl_seconds=300)
        return dashboard
```

### 19.2 Pre-Built Report Definitions

```python
# app/reports/report_definitions.py
REPORTS = {
    "leads-by-source": {
        "name": "Leads by Source",
        "folder": "Lead Reports",
        "query": lambda scope: (
            select(
                Lead.source,
                func.count(Lead.id).label("count"),
            )
            .where(*scope(Lead))
            .group_by(Lead.source)
        ),
    },
    "leads-by-status": {
        "name": "Leads by Status",
        "folder": "Lead Reports",
        "query": lambda scope: (
            select(
                Lead.status,
                func.count(Lead.id).label("count"),
            )
            .where(*scope(Lead))
            .group_by(Lead.status)
        ),
    },
    "pipeline-by-stage": {
        "name": "Pipeline by Stage",
        "folder": "Deal Reports",
        "query": lambda scope: (
            select(
                PipelineStage.name,
                func.count(Deal.id).label("deal_count"),
                func.sum(Deal.amount).label("total_value"),
            )
            .join(PipelineStage, Deal.stage_id == PipelineStage.id)
            .where(*scope(Deal))
            .group_by(PipelineStage.name, PipelineStage.display_order)
            .order_by(PipelineStage.display_order)
        ),
    },
    "deal-win-loss": {
        "name": "Win/Loss Rate",
        "folder": "Deal Reports",
        "query": lambda scope: (
            select(
                PipelineStage.name,
                func.count(Deal.id).label("count"),
            )
            .join(PipelineStage)
            .where(*scope(Deal), PipelineStage.is_closed == True)
            .group_by(PipelineStage.name, PipelineStage.is_won)
        ),
    },
    "overdue-tasks": {
        "name": "Overdue Tasks",
        "folder": "Activity Reports",
        "query": lambda scope: (
            select(Activity)
            .where(
                *scope(Activity),
                Activity.activity_type == "task",
                Activity.task_status != "completed",
                Activity.due_date < func.current_date(),
            )
            .order_by(Activity.due_date.asc())
        ),
    },
    "rep-performance": {
        "name": "Sales Rep Performance",
        "folder": "Sales Rep Performance Reports",
        "allowed_roles": ["admin", "sales_manager"],
        "query": lambda scope: (
            select(
                User.first_name,
                User.last_name,
                func.count(Deal.id).filter(PipelineStage.is_won == True).label("deals_won"),
                func.count(Deal.id).filter(PipelineStage.is_closed == True).label("deals_closed"),
                func.sum(Deal.amount).filter(PipelineStage.is_won == True).label("revenue_won"),
            )
            .join(Deal, Deal.owner_id == User.id)
            .join(PipelineStage, Deal.stage_id == PipelineStage.id)
            .where(User.org_id == scope.user.org_id)
            .group_by(User.id)
        ),
    },
}
```

---

## 20. Frontend Architecture — Component Tree

```
<RootLayout>                                          ← app/layout.tsx
├── <AuthProvider>                                    ← JWT context
│   ├── <ReduxProvider>                              ← Redux store
│   │   ├── <QueryClientProvider>                   ← TanStack Query
│   │   │   ├── <Sidebar>                           ← Left navigation
│   │   │   │   ├── <SidebarLink to="/"> Home
│   │   │   │   ├── <SidebarLink to="/workqueues">
│   │   │   │   ├── <SidebarLink to="/reports">
│   │   │   │   ├── <SidebarSection label="Sales">
│   │   │   │   │   ├── Leads │ Contacts │ Accounts │ Deals │ Documents
│   │   │   │   ├── <SidebarSection label="Activities">
│   │   │   │   │   ├── Tasks │ Meetings │ Calls
│   │   │   │   └── <SidebarLink to="/settings"> (Admin only)
│   │   │   │
│   │   │   ├── <TopBar>
│   │   │   │   ├── <GlobalSearch>                  ← /search?q=
│   │   │   │   ├── <QuickCreateButton>             ← (+) modal
│   │   │   │   ├── <NotificationBell>              ← polling /notifications
│   │   │   │   ├── <CalendarIcon>
│   │   │   │   └── <ProfileMenu>
│   │   │   │
│   │   │   ├── <AIChatPanel>                       ← Floating panel, always available
│   │   │   │
│   │   │   └── <main> {children}                   ← Page content
```

### Key Page Components

```
/leads (page.tsx)
├── <ViewToggle>                         ← List | Kanban
├── <FilterBar>                          ← Status, source, owner filters
├── <DataTable>                          ← TanStack Table (list view)
│   ├── Columns: Name | Company | Email | Source | Status | Score | Created
│   └── Row actions: View | Edit | Convert | Delete
└── <KanbanBoard>                        ← dnd-kit (kanban view)
    ├── <KanbanColumn status="new">
    │   └── <LeadCard> (draggable)
    │       ├── Name, Company
    │       └── <ScoreBadge score={85}>
    ├── <KanbanColumn status="qualified">
    └── <KanbanColumn status="converted">

/deals/{id} (page.tsx)
├── <DealHeader>                         ← Name, amount, stage, owner
│   └── <RiskAlertBanner>               ← If active alert
├── <StageProgressBar>                   ← Visual pipeline progress
├── <DealDetails>                        ← Contact, account, dates
├── <ActivityTimeline>                   ← Unified timeline component
│   └── <TimelineEntry>
│       ├── Icon by type (task/meeting/call/note)
│       ├── <AISummaryCard> (shown by default)
│       └── "View full notes" expand
├── <DocumentsList>                      ← Attached files
└── <ActionBar>
    ├── <DraftEmailButton>              ← "Draft with AI"
    ├── <LogActivity>                   ← Quick task/meeting/call/note
    └── <UploadDocument>
```

---

## 21. Frontend State Management

### 21.1 TanStack Query — Server State (per module)

```typescript
// lib/hooks/useLeads.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useLeads(params: LeadListParams) {
  return useQuery({
    queryKey: ["leads", params],
    queryFn: () => api.get("/v1/leads", { params }),
    staleTime: 30_000,           // 30s before refetch
    refetchOnWindowFocus: true,
  });
}

export function useCreateLead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: LeadCreate) => api.post("/v1/leads", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leads"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useConvertLead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ConvertRequest }) =>
      api.post(`/v1/leads/${id}/convert`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leads"] });
      queryClient.invalidateQueries({ queryKey: ["deals"] });
      queryClient.invalidateQueries({ queryKey: ["accounts"] });
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
    },
  });
}
```

### 21.2 Redux Toolkit — Client UI State

```typescript
// store/slices/uiSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UIState {
  sidebarCollapsed: boolean;
  activeModal: string | null;
  quickCreateType: string | null;
  aiChatOpen: boolean;
}

const uiSlice = createSlice({
  name: "ui",
  initialState: {
    sidebarCollapsed: false,
    activeModal: null,
    quickCreateType: null,
    aiChatOpen: false,
  } as UIState,
  reducers: {
    toggleSidebar: (state) => { state.sidebarCollapsed = !state.sidebarCollapsed; },
    openModal: (state, action: PayloadAction<string>) => { state.activeModal = action.payload; },
    closeModal: (state) => { state.activeModal = null; },
    openQuickCreate: (state, action: PayloadAction<string>) => {
      state.quickCreateType = action.payload;
      state.activeModal = "quick-create";
    },
    toggleAIChat: (state) => { state.aiChatOpen = !state.aiChatOpen; },
  },
});
```

---

## 22. Frontend Routing — Next.js App Router

```
app/
├── layout.tsx              → RootLayout (auth guard, sidebar, topbar)
├── page.tsx                → /                    (Home Dashboard)
├── login/
│   └── page.tsx            → /login               (Public, no layout)
├── leads/
│   ├── page.tsx            → /leads               (List + Kanban)
│   └── [id]/
│       └── page.tsx        → /leads/:id           (Lead Detail)
├── contacts/
│   ├── page.tsx            → /contacts
│   └── [id]/page.tsx       → /contacts/:id
├── accounts/
│   ├── page.tsx            → /accounts
│   └── [id]/page.tsx       → /accounts/:id        (Tabbed: Contacts | Deals | Activities)
├── deals/
│   ├── page.tsx            → /deals               (List + Kanban)
│   └── [id]/page.tsx       → /deals/:id           (Detail + Timeline)
├── activities/
│   ├── tasks/page.tsx      → /activities/tasks
│   ├── meetings/page.tsx   → /activities/meetings
│   └── calls/page.tsx      → /activities/calls
├── documents/
│   └── page.tsx            → /documents
├── reports/
│   ├── page.tsx            → /reports              (Report list)
│   └── [slug]/page.tsx     → /reports/:slug        (Report view)
├── search/
│   └── page.tsx            → /search?q=
├── settings/
│   ├── page.tsx            → /settings             (Admin only)
│   ├── users/page.tsx      → /settings/users
│   ├── pipeline/page.tsx   → /settings/pipeline
│   └── scoring/page.tsx    → /settings/scoring
└── workqueues/
    └── page.tsx            → /workqueues
```

**Auth Guard (middleware):**

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const isLoginPage = request.nextUrl.pathname === "/login";

  if (!token && !isLoginPage) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  if (token && isLoginPage) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

---

## 23. Database Migration Strategy

```
alembic/
├── env.py                    # Async engine config
├── alembic.ini
└── versions/
    ├── 001_create_organizations.py
    ├── 002_create_users.py
    ├── 003_create_leads.py
    ├── 004_create_accounts.py
    ├── 005_create_contacts.py
    ├── 006_create_pipeline_stages.py
    ├── 007_create_deals.py
    ├── 008_create_activities.py
    ├── 009_create_documents.py
    ├── 010_create_ai_tables.py
    ├── 011_create_notifications.py
    ├── 012_seed_default_pipeline_stages.py
    └── 013_enable_pgvector.py
```

**Seed migration for default pipeline stages:**

```python
# alembic/versions/012_seed_default_pipeline_stages.py
def upgrade():
    """Insert default pipeline stages for the initial organization."""
    stages = [
        ("Qualification",  1, 10.00, False, False),
        ("Discovery",      2, 25.00, False, False),
        ("Proposal",       3, 50.00, False, False),
        ("Negotiation",    4, 75.00, False, False),
        ("Closed Won",     5, 100.00, True,  True),
        ("Closed Lost",    6, 0.00,   True,  False),
    ]
    # Stages are created per-org at organization creation time via service layer
```

---

## 24. Error Handling — Centralized Pattern

```python
# app/common/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, code: str, message: str, status: int = 400, details: dict | None = None):
        self.code = code
        self.message = message
        self.status = status
        self.details = details


class ValidationError(AppError):
    def __init__(self, message: str, details=None):
        super().__init__("VALIDATION_ERROR", message, 422, details)

class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__("AUTHENTICATION_REQUIRED", message, 401)

class ForbiddenError(AppError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__("FORBIDDEN", message, 403)

class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__("NOT_FOUND", message, 404)

class ConflictError(AppError):
    def __init__(self, message: str, details=None):
        super().__init__("DUPLICATE_RESOURCE", message, 409, details)

class RateLimitError(AppError):
    def __init__(self):
        super().__init__("RATE_LIMITED", "Too many requests", 429)

class AIGenerationError(AppError):
    def __init__(self, message: str = "AI generation failed"):
        super().__init__("AI_GENERATION_FAILED", message, 502)


# Global exception handler
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": request.state.request_id,
            }
        },
    )

# Register in main.py:
# app.add_exception_handler(AppError, app_error_handler)
```

---

## 25. Rate Limiting Implementation

```python
# app/common/middleware.py
from app.common.cache import cache

RATE_LIMITS = {
    "/v1/auth/login": (10, 60),       # 10 per minute
    "/v1/ai/email-draft": (20, 300),   # 20 per 5 min
    "/v1/ai/chat": (30, 300),          # 30 per 5 min
    "/v1/ai/summarize": (20, 300),     # 20 per 5 min
    "default": (100, 60),              # 100 per minute
}


class RateLimitMiddleware:
    async def __call__(self, request, call_next):
        user_id = getattr(request.state, "user_id", "anonymous")
        path = request.url.path

        # Find matching limit
        limit, window = RATE_LIMITS.get(path, RATE_LIMITS["default"])

        allowed = await cache.check_rate_limit(user_id, path, limit, window)
        if not allowed:
            raise RateLimitError()

        return await call_next(request)
```

---

## 26. CI/CD Pipeline Specification

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # ─── Backend ───────────────────────────────
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      redis:
        image: redis:7
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[test]"
      - run: alembic upgrade head
      - run: pytest --cov=app --cov-report=xml
      - run: ruff check app/
      - run: mypy app/

  backend-deploy:
    needs: backend-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
      - uses: aws-actions/amazon-ecr-login@v2
      - run: |
          docker build -t $ECR_REPO:$GITHUB_SHA .
          docker push $ECR_REPO:$GITHUB_SHA
      - run: |
          aws ecs update-service \
            --cluster crusource-api \
            --service api \
            --force-new-deployment

  # ─── Frontend ──────────────────────────────
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test

  # Frontend deploys automatically via Vercel Git integration
```

---

## 27. Environment Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str                          # postgresql+asyncpg://...
    DB_POOL_SIZE: int = 30
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str                             # redis://elasticache-endpoint:6379

    # AWS
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str
    SQS_AI_JOBS_QUEUE: str
    SQS_EMBEDDINGS_QUEUE: str
    SQS_NOTIFICATIONS_QUEUE: str

    # Auth
    JWT_SECRET: str                            # From AWS Secrets Manager
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    # Claude API
    ANTHROPIC_API_KEY: str                     # From AWS Secrets Manager

    # App
    FRONTEND_URL: str                          # https://app.crusource.com
    ENVIRONMENT: str = "production"            # development | staging | production
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
```

**Local development overrides (`.env`):**

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/crusource_dev
REDIS_URL=redis://localhost:6379
AWS_REGION=us-east-1
S3_BUCKET=crusource-dev-documents
SQS_AI_JOBS_QUEUE=http://localhost:4566/000000000000/ai-jobs
SQS_EMBEDDINGS_QUEUE=http://localhost:4566/000000000000/embeddings
SQS_NOTIFICATIONS_QUEUE=http://localhost:4566/000000000000/notifications
JWT_SECRET=dev-secret-change-in-production
ANTHROPIC_API_KEY=sk-ant-...
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

---

> **Document Status:** Draft — July 2026
