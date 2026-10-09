"""Executable design contracts for Phases 1, 4 and 5; not registered API code.

Run with the backend venv. Emits schemas and checks boundary examples offline.
Business authorization, transitions and transactions are specified in CONTRACTS.md.
"""
from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal
from uuid import UUID

from pydantic import (
    AwareDatetime, BaseModel, ConfigDict, EmailStr, Field, StringConstraints,
    ValidationError, create_model, field_validator,
)

Identifier = UUID
Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
Reason = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
Body = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=10000)]
Search = Annotated[str, StringConstraints(strip_whitespace=True, max_length=200)]
Version = Annotated[int, Field(strict=True, ge=1)]


class DTO(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Capability(StrEnum):
    DEMO_READ = "demo.read"
    DEMO_MANAGE = "demo.manage"
    SUPPORT_READ = "support.read"
    SUPPORT_MANAGE = "support.manage"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ENROLLING = "enrolling"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class DeliveryStatus(StrEnum):
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    RETRYING = "retrying"
    FAILED = "failed"
    SUPERSEDED = "superseded"


class DemoStage(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    DEMO_SCHEDULED = "demo_scheduled"
    DEMO_COMPLETED = "demo_completed"
    FOLLOW_UP = "follow_up"
    CONVERTED = "converted"
    NOT_PROCEEDING = "not_proceeding"


class TicketStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class PageQuery(DTO):
    limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 20
    offset: Annotated[int, Field(strict=True, ge=0, le=100000)] = 0
    search: Search = ""
    sort_order: Literal["asc", "desc"] = "desc"


class VersionedCommand(DTO):
    expected_version: Version


class InviteStaff(DTO):
    email: Annotated[EmailStr, Field(max_length=255)]
    name: Name

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower() if isinstance(value, str) else value


class ResendInvitation(VersionedCommand):
    pass


class CancelInvitation(VersionedCommand):
    reason: Reason


class ResetStaffSignIn(VersionedCommand):
    reason: Reason


class RevokeStaff(VersionedCommand):
    reason: Reason


class Invitation(DTO):
    id: Identifier
    email: Annotated[EmailStr, Field(max_length=255)]
    name: Name
    status: InvitationStatus
    version: Version
    generation: Annotated[int, Field(strict=True, ge=1)]
    expires_at: AwareDatetime
    created_at: AwareDatetime
    invited_by: Identifier | None  # null only for explicit legacy lineage
    accepted_user_id: Identifier | None
    delivery_status: DeliveryStatus


class Staff(DTO):
    id: Identifier
    name: Name
    email: EmailStr
    is_owner: bool
    active: bool
    version: Version
    capabilities: list[Capability]


class InvitationQuery(PageQuery):
    status: InvitationStatus | None = None
    sort_by: Literal["created_at", "email", "expires_at"] = "created_at"


class SubmitDemo(DTO):
    name: Name
    email: Annotated[EmailStr, Field(max_length=255)]
    company: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
    phone: Annotated[str, StringConstraints(strip_whitespace=True, max_length=32)] | None = None
    message: Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)] = ""
    locale: Literal["en", "nl"] = "en"
    consent: Literal[True]
    website: Literal[""] = ""  # honeypot; never persists as lead data


class DemoReceipt(DTO):
    receipt_id: Identifier
    message: Literal["Your demo request has been received."]


class DemoRequest(DTO):
    id: Identifier
    name: Name
    email: EmailStr
    company: Name
    phone: str | None
    message: str
    locale: Literal["en", "nl"]
    stage: DemoStage
    disposition: Literal["normal", "spam"]
    assignee_id: Identifier | None
    follow_up_at: AwareDatetime | None
    scheduled_demo_at: AwareDatetime | None
    version: Version
    created_at: AwareDatetime
    updated_at: AwareDatetime


class MoveDemo(VersionedCommand):
    stage: DemoStage
    reason: Reason | None = None
    scheduled_demo_at: AwareDatetime | None = None


class AssignRecord(VersionedCommand):
    assignee_id: Identifier | None  # explicit null unassigns


class SetDemoFollowUp(VersionedCommand):
    follow_up_at: AwareDatetime | None


class SetDemoDisposition(VersionedCommand):
    disposition: Literal["normal", "spam"]
    reason: Reason


class AddDemoNote(VersionedCommand):
    body: Body


class DemoNote(DTO):
    id: Identifier
    body: Body
    author_id: Identifier | None
    created_at: AwareDatetime


class DemoStageCount(DTO):
    stage: DemoStage
    total: Annotated[int, Field(strict=True, ge=0)]


class DemoCounts(DTO):
    items: list[DemoStageCount]


class DemoQuery(PageQuery):
    stage: DemoStage | None = None
    disposition: Literal["normal", "spam"] = "normal"
    assignee_id: Identifier | None = None
    unassigned: bool = False
    sort_by: Literal["created_at", "updated_at", "follow_up_at"] = "created_at"


class CreateTicket(DTO):
    subject: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    body: Body
    category: Literal["general", "account", "billing", "bug", "feature_request"] = "general"


class ReplyToTicket(VersionedCommand):
    body: Body


class AddInternalNote(VersionedCommand):
    body: Body


class ChangeTicketStatus(VersionedCommand):
    status: TicketStatus
    reason: Reason | None = None


class ReopenTicket(VersionedCommand):
    reason: Reason


class CustomerTicket(DTO):
    id: Identifier
    subject: str
    category: Literal["general", "account", "billing", "bug", "feature_request"]
    status: TicketStatus
    version: Version
    created_at: AwareDatetime
    updated_at: AwareDatetime


class PlatformTicket(CustomerTicket):
    org_id: Identifier
    requester_id: Identifier
    assignee_id: Identifier | None


class CustomerMessage(DTO):
    id: Identifier
    ticket_id: Identifier
    author_kind: Literal["customer", "staff"]
    author_name: Name
    body: Body
    created_at: AwareDatetime


class PlatformMessage(CustomerMessage):
    visibility: Literal["public", "internal"]
    author_id: Identifier | None


class CustomerTicketQuery(PageQuery):
    status: TicketStatus | None = None
    sort_by: Literal["created_at", "updated_at"] = "updated_at"


class PlatformTicketQuery(CustomerTicketQuery):
    org_id: Identifier | None = None
    assignee_id: Identifier | None = None
    unassigned: bool = False


class MessageQuery(DTO):
    limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 30
    before_id: Identifier | None = None


class HistoryEntry(DTO):
    id: Identifier
    action: Annotated[str, StringConstraints(max_length=80)]
    actor_id: Identifier | None
    reason: Reason | None
    created_at: AwareDatetime
    from_state: str | None
    to_state: str | None


class ApiError(DTO):
    code: Literal["validation_error", "unauthenticated", "forbidden", "not_found",
                  "version_conflict", "idempotency_conflict", "invalid_transition",
                  "rate_limited", "temporarily_unavailable"]
    message: str
    request_id: str
    current_version: Version | None = None
    field_errors: dict[str, list[str]] = Field(default_factory=dict)


# Concrete envelopes allow backend/frontend generation without untyped entity bags.
for item in (Invitation, Staff, DemoRequest, DemoNote, CustomerTicket, PlatformTicket, HistoryEntry):
    page_name = item.__name__ + "Page"
    globals()[page_name] = create_model(page_name, __base__=DTO,
        items=(list[item], ...), total=(Annotated[int, Field(ge=0)], ...),
        limit=(Annotated[int, Field(ge=1, le=100)], ...), offset=(Annotated[int, Field(ge=0)], ...))
for item in (CustomerMessage, PlatformMessage):
    page_name = item.__name__ + "Page"
    globals()[page_name] = create_model(page_name, __base__=DTO,
        items=(list[item], ...), next_before_id=(Identifier | None, ...),
        has_more=(bool, ...))


def verify_and_export():
    checks = 0

    def rejected(model, payload):
        nonlocal checks
        try:
            model.model_validate(payload)
        except ValidationError:
            checks += 1
            return
        raise AssertionError(f"{model.__name__} unexpectedly accepted invalid data")

    assert InviteStaff(email=" PERSON@example.com ", name=" Person ").email == "person@example.com"
    checks += 1
    rejected(InviteStaff, {"email": "not-an-email", "name": "Person"})
    rejected(InviteStaff, {"email": "person@example.com", "name": " "})
    rejected(InviteStaff, {"email": "person@example.com", "name": "Person", "is_owner": True})
    rejected(CreateTicket, {"subject": "Help", "body": "x", "org_id": "injected"})
    rejected(CreateTicket, {"subject": "x" * 201, "body": "Help"})
    rejected(ReplyToTicket, {"body": "x" * 10001, "expected_version": 1})
    rejected(ReplyToTicket, {"body": "Help", "expected_version": 0})
    rejected(ReplyToTicket, {"body": "Help", "expected_version": True})
    rejected(CustomerTicketQuery, {"limit": 101})
    rejected(CustomerTicketQuery, {"org_id": "injected"})
    rejected(PlatformTicketQuery, {"sort_by": "unsafe_sql"})
    rejected(SetDemoFollowUp, {"expected_version": 1, "follow_up_at": "2026-10-09T09:00:00"})
    demo = {"name": "Person", "email": "person@example.com", "company": "Example", "consent": True}
    SubmitDemo.model_validate(demo)
    checks += 1
    rejected(SubmitDemo, {**demo, "consent": False})
    rejected(SubmitDemo, {**demo, "assignee_id": "injected"})
    rejected(CustomerMessage, {"id": "00000000-0000-0000-0000-000000000001", "ticket_id": "00000000-0000-0000-0000-000000000002", "author_kind": "staff", "author_name": "Staff", "body": "Private", "created_at": "2026-10-09T09:00:00Z", "visibility": "internal"})
    models = {name: value for name, value in globals().items()
              if isinstance(value, type) and issubclass(value, DTO) and value is not DTO}
    schemas = {name: value.model_json_schema() for name, value in models.items()}
    output = Path(__file__).with_name("contracts.schema.json")
    output.write_text(json.dumps({"status": "DESIGN_CONTRACT_NOT_LIVE_API", "models": schemas}, indent=2) + "\n", encoding="utf-8")
    result = {"scope": "offline DTO examples only", "checks_passed": checks, "models_exported": len(schemas)}
    Path(__file__).with_name("contract-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    verify_and_export()
