"""tests/test_admin_portal_admin6.py — Audit Logs + Support + Alerts.

Locked founder decisions:
  1a — Implement the 3 support mutations (status, assign, notes).
  2a — Admin-side only; NO public ingestion endpoint.
  3a — Metadata scrub = key list + Stripe-VALUE regex + length truncation.
  4a — billing_admin audit scope = 4 specific prefixes.
  5a — denied_admin_access_pattern severity = "warning".
  6a — Three separate sidebar nav items.
  7a — Fold Admin-5a carry-forwards into Admin-6 polish.

Codex-locked guardrail (CRITICAL):
  Support note bodies may live in support_tickets.internal_notes, but
  MUST NEVER appear in audit metadata. Tests plant `STRIPELEAK`,
  `sub_…`, `token`, `password` payloads and assert the audit row only
  contains `note_present: true`.
"""
from __future__ import annotations

import os
import pathlib
import re
import sys
import uuid
from datetime import datetime, timezone, timedelta

import pytest
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

sys.path.insert(0, "/app/backend")
load_dotenv("/app/backend/.env")


def _base_url() -> str:
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v.rstrip("/")
    env = pathlib.Path(__file__).resolve().parents[2] / "frontend" / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("REACT_APP_BACKEND_URL="):
            return line.split("=", 1)[1].strip().rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not configured")


BASE = _base_url()
API = f"{BASE}/api"

STRIPE_VALUE_RE = re.compile(r'"(sub|evt|in|cus|price)_[A-Za-z0-9_]{4,}"')


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role: str = "horse_owner") -> dict:
    email = f"adm6_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm6 Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str):
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _admin_session(db, plat_role: str = "platform_admin") -> dict:
    s = _signup()
    _promote(db, s["user"]["id"], plat_role)
    return s


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


def _plant_support_ticket(db, *, subject="Login flaky",
                          status="new", assignee=None) -> str:
    tid = f"ticket_{uuid.uuid4()}"
    now = datetime.now(timezone.utc).isoformat()
    db.support_tickets.insert_one({
        "id": tid,
        "barn_id": None,
        "subject": subject,
        "description": "Repro: clicks twice, sees 502.",
        "channel": "in_app",
        "submitter_user_id": "u_test",
        "submitter_email": "user@example.com",
        "status": status,
        "assignee_user_id": assignee,
        "assignee_email": None,
        "internal_notes": [],
        "created_at": now, "updated_at": now, "resolved_at": None,
    })
    return tid


def _ticket_ref(db, ticket_id: str) -> str:
    row = db.support_tickets.find_one({"id": ticket_id}, {"_id": 1})
    return f"st_{row['_id']}"


def _plant_audit_row(db, *, action: str, actor_email: str = "ops@example.com",
                     outcome: str = "success",
                     resource_type: str = "admin_portal",
                     resource_id: str = "test",
                     metadata: dict | None = None) -> str:
    aid = f"audit_{uuid.uuid4()}"
    db.audit_log.insert_one({
        "id": aid,
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action, "actor_email": actor_email,
        "actor_user_id": "u_test",
        "resource_type": resource_type, "resource_id": resource_id,
        "outcome": outcome, "status_code": 200,
        "metadata": metadata or {},
        "ip_address": "127.0.0.1",
    })
    return aid


# ---------------------------------------------------------------------
# Access boundary
# ---------------------------------------------------------------------
ALL_PLATFORM_ROLES = (
    "super_admin", "platform_admin", "support_admin",
    "billing_admin", "read_only_auditor",
)


@pytest.mark.parametrize("platform_role", ALL_PLATFORM_ROLES)
def test_audit_logs_visible_to_every_platform_role(db, platform_role):
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/audit-logs?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200, (
        f"{platform_role} got {r.status_code}: {r.text}"
    )


@pytest.mark.parametrize("platform_role", ["super_admin", "platform_admin", "support_admin"])
def test_support_visible_to_support_roles(db, platform_role):
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/support?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200


@pytest.mark.parametrize("platform_role", ["billing_admin", "read_only_auditor"])
def test_support_blocked_for_non_support_roles(db, platform_role):
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/support?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 403


@pytest.mark.parametrize("platform_role",
                         ["super_admin", "platform_admin", "support_admin", "billing_admin"])
def test_alerts_visible_to_alert_roles(db, platform_role):
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/alerts",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200


def test_alerts_blocked_for_read_only_auditor(db):
    s = _admin_session(db, "read_only_auditor")
    r = requests.get(f"{API}/admin/portal/alerts",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 403


@pytest.mark.parametrize("path", [
    "/admin/portal/audit-logs",
    "/admin/portal/support",
    "/admin/portal/alerts",
])
def test_unauthenticated_is_401(path):
    r = requests.get(f"{API}{path}", timeout=10)
    assert r.status_code == 401


@pytest.mark.parametrize("path", [
    "/admin/portal/audit-logs",
    "/admin/portal/support",
    "/admin/portal/alerts",
])
def test_horse_owner_is_403(db, path):
    s = _signup()
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


# ---------------------------------------------------------------------
# billing_admin audit scope (decision 4a)
# ---------------------------------------------------------------------
def test_billing_admin_audit_scope_restricts_results(db):
    """billing_admin must only see audits matching the 4 locked prefixes.
    Planted non-billing rows MUST NOT appear in their list."""
    # Plant rows: one in-scope, one out-of-scope (clearly outside).
    in_scope = _plant_audit_row(
        db, action="admin.portal.read.payments",
        actor_email="ops@example.com",
    )
    out_of_scope = _plant_audit_row(
        db, action="admin.portal.users.suspend",
        actor_email="ops@example.com",
    )
    try:
        s = _admin_session(db, "billing_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?limit=100&actor_email=ops@example.com",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        actions = [row.get("action") for row in r.json()["items"]]
        assert "admin.portal.read.payments" in actions
        assert "admin.portal.users.suspend" not in actions, (
            "billing_admin saw an out-of-scope audit row"
        )
    finally:
        db.audit_log.delete_many({"id": {"$in": [in_scope, out_of_scope]}})


def test_billing_admin_audit_detail_404_for_out_of_scope(db):
    """Direct detail access to an out-of-scope row must 404 (NOT 200)."""
    out_of_scope = _plant_audit_row(
        db, action="admin.portal.users.suspend",
        actor_email="ops@example.com",
    )
    try:
        # Resolve the planted row's admin_ref via super_admin first.
        s_super = _admin_session(db, "super_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?actor_email=ops@example.com&limit=20",
            headers=_bearer(s_super), timeout=10,
        )
        rows = r.json()["items"]
        target = next(x for x in rows if x.get("action") == "admin.portal.users.suspend")
        ref = target["admin_ref"]
        # Now billing_admin must NOT be able to read it.
        s_bill = _admin_session(db, "billing_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs/{ref}",
            headers=_bearer(s_bill), timeout=10,
        )
        assert r.status_code == 404
    finally:
        db.audit_log.delete_one({"id": out_of_scope})


# ---------------------------------------------------------------------
# Audit log shape + leak guards
# ---------------------------------------------------------------------
def test_audit_log_row_shape_and_no_raw_resource_id(db):
    """Audit list rows must surface `admin_ref` and the opaque
    `resource` ref; raw `resource_id` MUST be stripped."""
    aid = _plant_audit_row(db, action="admin.portal.users.suspend",
                           resource_type="user", resource_id="u_unique_value")
    try:
        s = _admin_session(db, "platform_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?actor_email=ops@example.com&limit=20",
            headers=_bearer(s), timeout=10,
        )
        rows = r.json()["items"]
        target = next(x for x in rows if x.get("action") == "admin.portal.users.suspend")
        assert target["admin_ref"].startswith("al_")
        assert "id" not in target, "audit row leaked raw `id`"
        assert "resource_id" not in target, (
            "audit row leaked raw `resource_id` (should be replaced with opaque `resource` ref)"
        )
        # For a known type (user), the resource block surfaces the id.
        assert target.get("resource", {}).get("kind") == "user"
    finally:
        db.audit_log.delete_one({"id": aid})


def test_audit_log_metadata_scrubs_sensitive_keys(db):
    """Planted metadata containing password / token / secret keys MUST
    be filtered out by `_scrub_metadata` (decision 3a)."""
    aid = _plant_audit_row(
        db, action="admin.portal.users.create_test",
        actor_email="ops@example.com",
        metadata={
            "password": "supersecret",
            "api_key": "should_never_appear",
            "stripe_webhook_secret": "whsec_xxx",
            "safe_field": "ok_value",
        },
    )
    try:
        s = _admin_session(db, "platform_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?actor_email=ops@example.com&limit=20",
            headers=_bearer(s), timeout=10,
        )
        target = next(x for x in r.json()["items"]
                      if x.get("action") == "admin.portal.users.create_test")
        meta = target.get("metadata") or {}
        for forbidden in ("password", "api_key", "stripe_webhook_secret"):
            assert forbidden not in meta, f"metadata leaked '{forbidden}'"
        assert meta.get("safe_field") == "ok_value"
        # Also assert the forbidden VALUES never appear in the raw body.
        assert "supersecret" not in r.text
        assert "whsec_xxx" not in r.text
    finally:
        db.audit_log.delete_one({"id": aid})


def test_audit_log_metadata_redacts_stripe_shaped_values(db):
    """Decision 3a — Stripe-VALUE regex must redact stray Stripe IDs
    that ended up nested in metadata strings."""
    aid = _plant_audit_row(
        db, action="admin.portal.test_stripe_value",
        actor_email="ops@example.com",
        metadata={"reference": "cus_LEAKED_ID_xxxxxxxx",
                  "ok_text": "just words"},
    )
    try:
        s = _admin_session(db, "platform_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?actor_email=ops@example.com&limit=20",
            headers=_bearer(s), timeout=10,
        )
        target = next(x for x in r.json()["items"]
                      if x.get("action") == "admin.portal.test_stripe_value")
        meta = target.get("metadata") or {}
        assert meta.get("reference") == "[stripe_id_redacted]"
        assert meta.get("ok_text") == "just words"
        # And the raw planted ID must not appear anywhere in the body.
        assert "cus_LEAKED_ID_xxxxxxxx" not in r.text
        assert not STRIPE_VALUE_RE.search(r.text), (
            "audit list leaked a Stripe-shaped value somewhere"
        )
    finally:
        db.audit_log.delete_one({"id": aid})


def test_audit_log_metadata_truncates_long_strings(db):
    """Decision 3a — value strings > 256 chars are truncated."""
    long_val = "A" * 400
    aid = _plant_audit_row(
        db, action="admin.portal.test_long_value",
        actor_email="ops@example.com",
        metadata={"note": long_val},
    )
    try:
        s = _admin_session(db, "platform_admin")
        r = requests.get(
            f"{API}/admin/portal/audit-logs?actor_email=ops@example.com&limit=20",
            headers=_bearer(s), timeout=10,
        )
        target = next(x for x in r.json()["items"]
                      if x.get("action") == "admin.portal.test_long_value")
        v = target.get("metadata", {}).get("note", "")
        assert v.endswith("…(truncated)"), v[:50]
        assert len(v) <= 280  # 256 + suffix
    finally:
        db.audit_log.delete_one({"id": aid})


# ---------------------------------------------------------------------
# Support mutations (decisions 1a + Codex note-body guardrail)
# ---------------------------------------------------------------------
def test_support_status_change_audits_before_and_after(db):
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db, status="new")
    ref = _ticket_ref(db, tid)
    try:
        r = requests.post(
            f"{API}/admin/portal/support/{ref}/status",
            headers=_bearer(s), json={"status": "in_progress"}, timeout=10,
        )
        assert r.status_code == 200
        # Audit row carries before/after
        audit = db.audit_log.find_one(
            {"action": "admin.portal.support.status_change",
             "resource_id": tid},
        )
        assert audit is not None
        meta = audit.get("metadata") or {}
        assert meta.get("before") == "new"
        assert meta.get("after") == "in_progress"
        # DB updated
        tk = db.support_tickets.find_one({"id": tid})
        assert tk["status"] == "in_progress"
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


def test_support_assign_audits_before_and_after_user_id(db):
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    # Plant a platform-admin user to assign to.
    assignee_email = f"assign_{uuid.uuid4().hex[:6]}@example.com"
    rs = requests.post(f"{API}/auth/signup", json={
        "email": assignee_email, "password": "securepass1",
        "full_name": "Assignee", "role": "horse_owner",
    }, timeout=15)
    assignee = rs.json()["user"]
    db.users.update_one({"id": assignee["id"]},
                        {"$set": {"platform_role": "support_admin"}})
    try:
        r = requests.post(
            f"{API}/admin/portal/support/{ref}/assign",
            headers=_bearer(s), json={"assignee_user_id": assignee["id"]},
            timeout=10,
        )
        assert r.status_code == 200
        audit = db.audit_log.find_one(
            {"action": "admin.portal.support.assign",
             "resource_id": tid},
        )
        assert audit is not None
        meta = audit.get("metadata") or {}
        assert meta.get("before_user_id") is None
        assert meta.get("after_user_id") == assignee["id"]
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


def test_support_assign_rejects_non_platform_user(db):
    """An assignee without a platform_role must be rejected (400)."""
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    # Plant a regular (non-platform) user.
    rs = requests.post(f"{API}/auth/signup", json={
        "email": f"reg_{uuid.uuid4().hex[:6]}@example.com",
        "password": "securepass1",
        "full_name": "Regular", "role": "horse_owner",
    }, timeout=15)
    regular = rs.json()["user"]
    try:
        r = requests.post(
            f"{API}/admin/portal/support/{ref}/assign",
            headers=_bearer(s), json={"assignee_user_id": regular["id"]},
            timeout=10,
        )
        assert r.status_code == 400
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


def test_support_note_body_never_appears_in_audit_metadata(db):
    """🛡 Codex-locked guardrail — note body MUST stay in
    support_tickets.internal_notes. Audit metadata MUST only contain
    `{"note_present": true}` no matter what payload was sent."""
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    LEAK_BODY = (
        "STRIPELEAK_marker password=hunter2 token=secret_abc "
        "stripe_id=sub_LEAKED_ABCDEFGH api_key=evilkey"
    )
    try:
        r = requests.post(
            f"{API}/admin/portal/support/{ref}/notes",
            headers=_bearer(s), json={"body": LEAK_BODY}, timeout=10,
        )
        assert r.status_code == 200

        # 1) The audit row exists.
        audit = db.audit_log.find_one(
            {"action": "admin.portal.support.add_note",
             "resource_id": tid},
        )
        assert audit is not None

        # 2) Audit metadata is EXACTLY `{"note_present": true}` (or a
        #    superset of safe keys), and contains NONE of the leak
        #    tokens.
        meta = audit.get("metadata") or {}
        assert meta.get("note_present") is True
        # Strongest check: the full audit row, serialized, MUST NOT
        # contain any of the leak fragments anywhere.
        full_audit_text = str(audit)
        for tok in ("STRIPELEAK_marker", "hunter2", "secret_abc",
                    "sub_LEAKED_ABCDEFGH", "evilkey", "password", "token",
                    "api_key"):
            assert tok not in full_audit_text, (
                f"Audit row leaked '{tok}' (full row: {full_audit_text})"
            )

        # 3) The note body IS stored in the ticket.
        ticket = db.support_tickets.find_one({"id": tid})
        notes = ticket.get("internal_notes") or []
        assert len(notes) == 1
        assert notes[0]["body"] == LEAK_BODY
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


def test_support_mutations_blocked_for_billing_admin(db):
    """Mutations require support-tab access. billing_admin → 403 on
    all 3 mutation endpoints (the read endpoint also 403s)."""
    s = _admin_session(db, "billing_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    try:
        r = requests.post(f"{API}/admin/portal/support/{ref}/status",
                          headers=_bearer(s), json={"status": "in_progress"},
                          timeout=10)
        assert r.status_code == 403
        r = requests.post(f"{API}/admin/portal/support/{ref}/assign",
                          headers=_bearer(s), json={"assignee_user_id": None},
                          timeout=10)
        assert r.status_code == 403
        r = requests.post(f"{API}/admin/portal/support/{ref}/notes",
                          headers=_bearer(s), json={"body": "hi"},
                          timeout=10)
        assert r.status_code == 403
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


def test_support_status_change_rejects_invalid_status(db):
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    try:
        r = requests.post(f"{API}/admin/portal/support/{ref}/status",
                          headers=_bearer(s), json={"status": "bogus"},
                          timeout=10)
        assert r.status_code == 400
    finally:
        db.support_tickets.delete_one({"id": tid})


def test_support_detail_recent_activity_is_audit_log_only(db):
    """Detail recent_activity should ONLY contain audit_log rows
    (action present; never event_type)."""
    s = _admin_session(db, "platform_admin")
    tid = _plant_support_ticket(db)
    ref = _ticket_ref(db, tid)
    # Generate one audit row by changing status.
    requests.post(f"{API}/admin/portal/support/{ref}/status",
                  headers=_bearer(s), json={"status": "in_progress"},
                  timeout=10)
    try:
        r = requests.get(f"{API}/admin/portal/support/{ref}",
                         headers=_bearer(s), timeout=10)
        body = r.json()
        activity = body.get("recent_activity") or []
        assert activity, "expected at least one audit row from status change"
        for row in activity:
            assert "action" in row
            assert "event_type" not in row
    finally:
        db.support_tickets.delete_one({"id": tid})
        db.audit_log.delete_many({"resource_id": tid})


# ---------------------------------------------------------------------
# No mutation surfaces on read endpoints
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/audit-logs",
    "/admin/portal/audit-logs/al_doesnotexist",
    "/admin/portal/alerts",
])
def test_no_mutations_exposed_on_audit_or_alerts(path):
    for method in ("post", "put", "patch", "delete"):
        r = getattr(requests, method)(
            f"{API}{path}", timeout=10,
            headers={"Content-Type": "application/json"}, json={},
        )
        assert r.status_code in (401, 403, 405), (
            f"{method.upper()} {path} unexpectedly returned {r.status_code}"
        )


# ---------------------------------------------------------------------
# Alerts derivation (decision 5a — denied severity = warning)
# ---------------------------------------------------------------------
def test_alerts_billing_webhook_retry_appears(db):
    """Plant a billing_event with `processing_status=retry_502` and
    confirm a `billing_webhook_retry` alert appears."""
    s = _admin_session(db, "platform_admin")
    eid = f"evt_alerttest_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    db.billing_events.insert_one({
        "id": eid, "barn_id": None,
        "event_type": "customer.subscription.updated",
        "processing_status": "retry_502",
        "event_created_at": now_iso,
        "created_at": now_iso, "updated_at": now_iso,
    })
    try:
        r = requests.get(f"{API}/admin/portal/alerts",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        keys = [a.get("key") for a in r.json()["items"]]
        assert "billing_webhook_retry" in keys
    finally:
        db.billing_events.delete_one({"id": eid})


def test_alerts_payment_failure_appears(db):
    s = _admin_session(db, "platform_admin")
    iid = f"in_alerttest_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    db.subscription_invoices.insert_one({
        "id": iid, "barn_id": None,
        "subscription_id": "sub_test",
        "amount_cents": 4900, "status": "open",
        "payment_failure_count": 3,
        "created_at": now_iso, "updated_at": now_iso,
    })
    try:
        r = requests.get(f"{API}/admin/portal/alerts",
                         headers=_bearer(s), timeout=10)
        keys = [a.get("key") for a in r.json()["items"]]
        assert "payment_failure" in keys
    finally:
        db.subscription_invoices.delete_one({"id": iid})


def test_alerts_denied_access_pattern_severity_warning(db):
    """Decision 5a — denied admin access pattern severity = warning."""
    s = _admin_session(db, "platform_admin")
    # Plant 3 denied admin.portal.* audit rows for the same actor.
    actor = f"shady_{uuid.uuid4().hex[:6]}@example.com"
    planted = []
    for _ in range(3):
        planted.append(_plant_audit_row(
            db, action="admin.portal.users.suspend",
            actor_email=actor, outcome="denied",
        ))
    try:
        r = requests.get(f"{API}/admin/portal/alerts",
                         headers=_bearer(s), timeout=10)
        items = r.json()["items"]
        match = next((a for a in items
                      if a.get("key") == "denied_admin_access_pattern"
                      and a.get("actor_email") == actor), None)
        assert match is not None
        assert match["severity"] == "warning", match
        assert match["count"] >= 3
    finally:
        db.audit_log.delete_many({"id": {"$in": planted}})


def test_alerts_scope_for_billing_admin(db):
    """billing_admin can only see billing-related alert keys."""
    s = _admin_session(db, "billing_admin")
    # Plant a payment_failure (in-scope) and a pending_user_approval
    # (out-of-scope).
    iid = f"in_alertscope_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    db.subscription_invoices.insert_one({
        "id": iid, "barn_id": None, "subscription_id": "sub_x",
        "status": "open", "payment_failure_count": 1,
        "amount_cents": 100,
        "created_at": now_iso, "updated_at": now_iso,
    })
    # Out-of-scope: user pending_review > 48h ago
    uid = f"u_alertscope_{uuid.uuid4().hex[:6]}"
    old_iso = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()
    db.users.insert_one({
        "id": uid, "email": f"{uid}@example.com",
        "role": "horse_owner", "role_status": "pending_review",
        "created_at": old_iso,
    })
    try:
        r = requests.get(f"{API}/admin/portal/alerts",
                         headers=_bearer(s), timeout=10)
        keys = [a.get("key") for a in r.json()["items"]]
        assert "payment_failure" in keys
        # The user-approval-stale key must be hidden from billing_admin.
        assert "pending_user_approval_stale" not in keys
    finally:
        db.subscription_invoices.delete_one({"id": iid})
        db.users.delete_one({"id": uid})


# ---------------------------------------------------------------------
# Self-flood guard (decision 8a continues)
# ---------------------------------------------------------------------
def test_admin6_reads_excluded_from_activity_feed(db):
    s = _admin_session(db, "platform_admin")
    h = _bearer(s)
    # Trigger one read per Admin-6 endpoint.
    requests.get(f"{API}/admin/portal/audit-logs?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/support?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/alerts", headers=h, timeout=10)
    r = requests.get(f"{API}/admin/portal/activity?limit=100",
                     headers=h, timeout=10)
    assert r.status_code == 200
    actions = [x.get("action") for x in r.json()["items"]]
    for f in ("admin.portal.read.audit_logs",
              "admin.portal.read.audit_log_detail",
              "admin.portal.read.support",
              "admin.portal.read.support_detail",
              "admin.portal.read.alerts"):
        assert f not in actions, f"Activity feed leaked Admin-6 read '{f}'"


# ---------------------------------------------------------------------
# Phase 9 isolation continues (no `recurring_charges` in any Admin-6
# surface; no Phase 9 `invoices` references).
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/audit-logs?limit=5",
    "/admin/portal/support?limit=5",
    "/admin/portal/alerts",
])
def test_admin6_does_not_reference_phase9(db, path):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert "recurring_charges" not in r.text
