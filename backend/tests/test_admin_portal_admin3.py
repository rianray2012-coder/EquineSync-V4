"""tests/test_admin_portal_admin3.py — Admin Portal user management.

Covers Admin-3 (first mutation surface):
  - GET /api/admin/portal/users        (paginated, filters, search)
  - GET /api/admin/portal/users/{id}   (detail + barn + horses + audit)
  - GET /api/admin/portal/approvals    (pending review queue)
  - POST .../users/{id}/{approve,reject,request-info,suspend,reactivate}

Critical invariants:
  - Non-platform users get 403
  - role="admin" without platform_role STILL blocked
  - read_only_auditor / billing_admin → read-only (cannot mutate)
  - support_admin → request-info only
  - platform_admin → cannot touch a super_admin target
  - No admin can mutate their own account
  - All mutations audit-log with before/after status + note_present
  - Idempotent re-approve / re-reject / re-suspend → no audit double-entry
  - User responses never expose password / password_hash / tokens
  - Filters/search/pagination work
  - Generic 404 for missing targets
"""
from __future__ import annotations

import os
import pathlib
import sys
import uuid
from datetime import datetime, timezone

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


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role: str = "horse_owner") -> dict:
    email = f"adm3_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm3 Test", "role": role},
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


def _pending_target(role: str = "trainer") -> dict:
    """Create a marketplace user that will land in pending_review."""
    return _signup(role)


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


# ---------------------------------------------------------------------
# Access boundary
# ---------------------------------------------------------------------
def test_users_list_requires_platform_role():
    s = _signup()
    r = requests.get(f"{API}/admin/portal/users", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_users_list_unauthenticated_is_401():
    r = requests.get(f"{API}/admin/portal/users", timeout=10)
    assert r.status_code == 401


def test_role_admin_barn_admin_does_not_inherit_admin3_access(db):
    """Founder invariant carried forward from Admin-1: barn-level
    role='admin' must NOT grant admin-portal access, period."""
    s = _signup()
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"role": "admin"}})
    r = requests.get(f"{API}/admin/portal/users", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_approvals_requires_platform_role():
    s = _signup()
    r = requests.get(f"{API}/admin/portal/approvals", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_user_detail_requires_platform_role(db):
    s = _signup()
    target = _pending_target()
    r = requests.get(
        f"{API}/admin/portal/users/{target['user']['id']}",
        headers=_bearer(s),
        timeout=10,
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------
# Read endpoints — shape + safety
# ---------------------------------------------------------------------
def test_users_list_strips_sensitive_fields(db):
    s = _admin_session(db)
    r = requests.get(f"{API}/admin/portal/users?limit=5", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "items" in body and "total" in body
    for u in body["items"]:
        # Hard-deny on any of these in the safe user shape.
        for forbidden in ("password", "password_hash", "token", "access_token",
                          "refresh_token", "jwt"):
            assert forbidden not in u, f"User leaked '{forbidden}'"


def test_users_list_search_q_finds_email_substring(db):
    s = _admin_session(db)
    # Plant a uniquely-named user we can search for.
    tag = uuid.uuid4().hex[:10]
    t = _pending_target()
    db.users.update_one({"id": t["user"]["id"]}, {"$set": {"full_name": f"Findme_{tag}"}})
    r = requests.get(
        f"{API}/admin/portal/users?q=Findme_{tag}&limit=5",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 1
    assert any(u.get("full_name", "").startswith("Findme_") for u in body["items"])


def test_users_list_pagination_cursor(db):
    s = _admin_session(db)
    r = requests.get(f"{API}/admin/portal/users?limit=2&cursor=0",
                     headers=_bearer(s), timeout=10)
    body = r.json()
    assert len(body["items"]) <= 2
    assert body["cursor"] == 0
    assert "next_cursor" in body


def test_user_detail_returns_barn_and_horses_summary(db):
    s = _admin_session(db)
    t = _pending_target()
    r = requests.get(
        f"{API}/admin/portal/users/{t['user']['id']}",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert "user" in body
    assert "barn" in body
    assert "horses" in body and "count" in body["horses"]
    assert "recent_audit" in body
    # No sensitive keys in detail either.
    for k in ("password", "password_hash", "token"):
        assert k not in body["user"]


def test_user_detail_returns_generic_404():
    s = _signup()
    _promote_via_fixture = None  # silencer for IDE
    db = MongoClient(os.environ["MONGO_URL"])[os.environ.get("DB_NAME") or "test_database"]
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"platform_role": "platform_admin"}})
    r = requests.get(
        f"{API}/admin/portal/users/does-not-exist-{uuid.uuid4().hex[:6]}",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 404


def test_approvals_returns_pending_users(db):
    s = _admin_session(db)
    t = _pending_target()
    r = requests.get(f"{API}/admin/portal/approvals", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    ids = [u["id"] for u in body["items"]]
    assert t["user"]["id"] in ids


# ---------------------------------------------------------------------
# Role matrix — mutation permissions
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role,can_approve,can_request_info", [
    ("super_admin",       True,  True),
    ("platform_admin",    True,  True),
    ("support_admin",     False, True),
    ("billing_admin",     False, False),
    ("read_only_auditor", False, False),
])
def test_role_matrix_for_mutations(db, role, can_approve, can_request_info):
    actor = _admin_session(db, role)
    target = _pending_target()
    h = _bearer(actor)

    r_app = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/approve",
        headers=h, json={}, timeout=10,
    )
    if can_approve:
        assert r_app.status_code == 200, f"{role} should approve: got {r_app.status_code}"
    else:
        assert r_app.status_code == 403, f"{role} should be denied approve: got {r_app.status_code}"

    # Fresh target for request-info (the approve above may have flipped status).
    t2 = _pending_target()
    r_info = requests.post(
        f"{API}/admin/portal/users/{t2['user']['id']}/request-info",
        headers=h, json={"review_note": "Please verify trainer cert."},
        timeout=10,
    )
    if can_request_info:
        assert r_info.status_code == 200, f"{role} should request-info: got {r_info.status_code}"
    else:
        assert r_info.status_code == 403, f"{role} should be denied request-info: got {r_info.status_code}"


# ---------------------------------------------------------------------
# Mutation business rules
# ---------------------------------------------------------------------
def test_cannot_act_on_own_account(db):
    actor = _admin_session(db, "platform_admin")
    h = _bearer(actor)
    for action in ("approve", "reject", "suspend", "reactivate", "request-info"):
        body = {"review_note": "test"} if action in ("reject", "request-info") else {}
        r = requests.post(
            f"{API}/admin/portal/users/{actor['user']['id']}/{action}",
            headers=h, json=body, timeout=10,
        )
        assert r.status_code == 403, f"Self-action {action} should be 403"


def test_platform_admin_cannot_mutate_super_admin_target(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    _promote(db, target["user"]["id"], "super_admin")

    for action in ("approve", "reject", "suspend"):
        body = {"review_note": "test"} if action == "reject" else {}
        r = requests.post(
            f"{API}/admin/portal/users/{target['user']['id']}/{action}",
            headers=_bearer(actor), json=body, timeout=10,
        )
        assert r.status_code == 403, f"platform_admin should not {action} super_admin"


def test_super_admin_can_mutate_super_admin_target(db):
    actor = _admin_session(db, "super_admin")
    target = _pending_target()
    _promote(db, target["user"]["id"], "super_admin")
    r = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/suspend",
        headers=_bearer(actor), json={}, timeout=10,
    )
    # super_admin acting on another super_admin is allowed.
    assert r.status_code == 200


def test_approve_idempotent(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    h = _bearer(actor)
    r1 = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/approve",
        headers=h, json={}, timeout=10,
    )
    assert r1.status_code == 200
    assert r1.json().get("role_status") == "active"
    # Second approve should no-op.
    r2 = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/approve",
        headers=h, json={}, timeout=10,
    )
    assert r2.status_code == 200
    assert r2.json().get("_noop") is True


def test_reject_idempotent_and_stores_note(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    h = _bearer(actor)
    note = "Application missing trainer certification."
    r1 = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/reject",
        headers=h, json={"review_note": note}, timeout=10,
    )
    assert r1.status_code == 200
    body = r1.json()
    assert body.get("role_status") == "rejected"
    assert body.get("review_note") == note
    # Second reject is a no-op.
    r2 = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/reject",
        headers=h, json={"review_note": note}, timeout=10,
    )
    assert r2.json().get("_noop") is True


def test_suspend_then_reactivate(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    h = _bearer(actor)
    s = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/suspend",
        headers=h, json={}, timeout=10,
    )
    assert s.status_code == 200
    assert s.json().get("account_status") == "suspended"
    r = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/reactivate",
        headers=h, json={}, timeout=10,
    )
    assert r.status_code == 200
    assert r.json().get("account_status") == "active"


def test_approve_with_barn_id_validates(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    r = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/approve",
        headers=_bearer(actor),
        json={"barn_id": "definitely-not-a-real-barn"},
        timeout=10,
    )
    assert r.status_code == 404


def test_request_info_does_not_change_role_status(db):
    actor = _admin_session(db, "support_admin")
    target = _pending_target()
    r = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/request-info",
        headers=_bearer(actor),
        json={"review_note": "Need additional documents."},
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    # Status remains pending_review — only info_requested_at is stamped.
    assert body.get("role_status") == "pending_review"
    assert body.get("info_requested_at")


def test_review_note_is_capped_at_500_chars(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    long_note = "x" * 1000
    r = requests.post(
        f"{API}/admin/portal/users/{target['user']['id']}/reject",
        headers=_bearer(actor), json={"review_note": long_note}, timeout=10,
    )
    # Pydantic max_length rejects with 422; either 422 OR truncation
    # (we use Field max_length so 422 is the contract).
    assert r.status_code in (200, 422)
    if r.status_code == 200:
        assert len(r.json().get("review_note") or "") <= 500


# ---------------------------------------------------------------------
# Audit logging
# ---------------------------------------------------------------------
def test_each_mutation_writes_audit_log_with_before_after(db):
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    target_id = target["user"]["id"]
    h = _bearer(actor)

    before_count = db.audit_log.count_documents({"action": "admin.user.approve"})
    requests.post(f"{API}/admin/portal/users/{target_id}/approve",
                  headers=h, json={}, timeout=10)
    after_count = db.audit_log.count_documents({"action": "admin.user.approve"})
    assert after_count == before_count + 1

    entry = db.audit_log.find_one({"action": "admin.user.approve", "resource_id": target_id},
                                  sort=[("ts", -1)])
    assert entry is not None
    meta = entry.get("metadata") or {}
    assert "before" in meta and "after" in meta
    assert meta["after"].get("role_status") == "active"
    assert meta["before"].get("role_status") == "pending_review"
    # Note-present boolean only — no raw note in audit metadata.
    assert "note_present" in meta
    # No PII beyond the masked email tail.
    assert "@" not in str(meta.get("target_email_masked") or "")


def test_idempotent_mutation_does_NOT_double_audit(db):
    """A no-op re-approve must not create a second audit entry."""
    actor = _admin_session(db, "platform_admin")
    target = _pending_target()
    target_id = target["user"]["id"]
    h = _bearer(actor)
    requests.post(f"{API}/admin/portal/users/{target_id}/approve",
                  headers=h, json={}, timeout=10)
    before = db.audit_log.count_documents({"action": "admin.user.approve",
                                            "resource_id": target_id})
    requests.post(f"{API}/admin/portal/users/{target_id}/approve",
                  headers=h, json={}, timeout=10)
    after = db.audit_log.count_documents({"action": "admin.user.approve",
                                           "resource_id": target_id})
    assert after == before, "Idempotent no-op must not double-audit."
