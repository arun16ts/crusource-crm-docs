"""Reproducible legacy-state rehearsal using actual models and an in-memory DB.

Never reads application data; emits aggregate synthetic counts only. Does not run
backfill or prove PostgreSQL behavior. Environment overrides precede app imports.
"""
import hashlib
import json
import os
import runpy
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent.parent / "crusource-crm-backend"
os.environ.update(ENVIRONMENT="test", DATABASE_URL="postgresql://phase0:phase0@127.0.0.1:9/phase0?connect_timeout=1",
                  REDIS_URL="redis://127.0.0.1:9/15", AWS_EC2_METADATA_DISABLED="true")
sys.path.insert(0, str(BACKEND))
fixture = runpy.run_path(str(BACKEND / "tests/conftest.py"))
Base, engine = fixture["Base"], fixture["engine"]
from src.modules.platform_auth.repositories.models import PlatformAccessRequest, PlatformCredential, PlatformSession
from src.modules.user.repositories.models import User

assert engine.url.get_backend_name() == "sqlite" and engine.url.database == ":memory:"
NOW = datetime(2026, 10, 9, 9, tzinfo=timezone.utc)
uid = lambda label: uuid5(NAMESPACE_URL, "phase0-synthetic/" + label)
digest = lambda label: hashlib.sha256(("phase0-synthetic/" + label).encode()).hexdigest()
Base.metadata.create_all(bind=engine)
try:
    with fixture["TestingSessionLocal"]() as db:
        for label, active, owner, credential in [
            ("owner", True, True, True), ("operator", True, False, True),
            ("revoked", False, False, True), ("enrolling", True, False, True),
            ("Case", True, False, False), ("case", True, False, False),
        ]:
            db.add(User(id=uid(label), name="Synthetic account", email=label+"@example.test",
                        org_id=None, is_super_admin=True, is_active=active, auth_provider="platform"))
            db.flush()
            if credential:
                db.add(PlatformCredential(user_id=uid(label), is_owner=owner, active=active and label != "enrolling",
                                          secret=None, last_totp_step=-1))
        states = [("unverified", "unverified", None), ("pending", "pending", None),
                  ("approved-valid", "approved", 48), ("approved-expired", "approved", -1),
                  ("approved-mail-failed", "approved", 48), ("enrolling", "enrolling", None),
                  ("operator", "activated", None), ("rejected", "rejected", None),
                  ("Case", "pending", None), ("case", "pending", None)]
        for label, status, expiry in states:
            db.add(PlatformAccessRequest(id=uid("request/"+label), email=label+"@example.test",
                   name="Synthetic request", reason="Offline migration rehearsal", status=status,
                   created_at=NOW, reviewer_id=uid("owner") if status in {"approved", "enrolling", "activated"} else None,
                   activation_hash=digest(label) if expiry else None,
                   activation_expires_at=NOW+timedelta(hours=expiry) if expiry else None,
                   delivery_status="failed" if "mail-failed" in label else "sent" if expiry else "not_sent"))
        for label, user, purpose, expired, revoked in [
            ("owner-session", "owner", "authenticated", False, False),
            ("operator-session", "operator", "authenticated", False, False),
            ("enrollment", "enrolling", "enroll", False, False),
            ("revoked-session", "revoked", "authenticated", False, True),
            ("expired-session", "operator", "authenticated", True, False),
        ]:
            db.add(PlatformSession(id=uid(label), token_hash=digest(label), user_id=uid(user), purpose=purpose,
                   created_at=NOW, last_seen_at=NOW, expires_at=NOW+timedelta(minutes=-1 if expired else 10), revoked=revoked))
        db.commit()
        requests = db.query(PlatformAccessRequest).all()
        users = db.query(User).all()
        credentials = db.query(PlatformCredential).all()
        sessions = db.query(PlatformSession).all()
        duplicates = lambda rows: sum(count > 1 for count in Counter(row.email.strip().lower() for row in rows).values())
        report = {
            "dataset": "SYNTHETIC_IN_MEMORY_ONLY", "as_of": NOW.isoformat(),
            "legacy_request_status_counts": dict(sorted(Counter(row.status for row in requests).items())),
            "users": len(users), "owner_credentials": sum(row.is_owner for row in credentials),
            "active_operator_credentials": sum(row.active and not row.is_owner for row in credentials),
            "inactive_credentials": sum(not row.active for row in credentials),
            "superadmin_flags_without_credentials": sum(row.id not in {c.user_id for c in credentials} for row in users),
            "normalized_collision_groups": {"users": duplicates(users), "access_requests": duplicates(requests)},
            "live_approved_activation_links": sum(row.status == "approved" and row.activation_expires_at > NOW.replace(tzinfo=None) for row in requests),
            "session_counts": {"total": len(sessions), "revoked": sum(row.revoked for row in sessions),
                               "expired": sum(row.expires_at < NOW.replace(tzinfo=None) for row in sessions),
                               "live_enrollment": sum(row.purpose == "enroll" and not row.revoked and row.expires_at > NOW.replace(tzinfo=None) for row in sessions)},
            "migration_executed": False,
            "limitations": ["No deployed database inspected", "SQLite does not establish PostgreSQL locking/index safety", "No passwords, encrypted secrets or tokens copied from real accounts"],
        }
        assert report["owner_credentials"] == 1
        assert report["normalized_collision_groups"] == {"users": 1, "access_requests": 1}
        assert report["live_approved_activation_links"] == 2
        assert report["session_counts"]["live_enrollment"] == 1
        (HERE / "legacy-inventory.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(report))
finally:
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
