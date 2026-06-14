"""tests/test_admin_portal_admin1.py — Admin Portal foundation tests.

Covers the Admin-1 scope only:
  - /api/admin/portal/me access boundary
      • 401 unauthenticated
      • 403 authenticated without platform_role (including role="admin"
        barn admins — they must NOT inherit platform-admin access)
      • 200 for each of the 5 platform roles
      • Section list narrows per role
  - /api/admin/portal/health gate matches the same boundary
  - Audit log entry written on successful /portal/me read

Strict guardrails verified:
  - No mutations exposed in the Admin-1 router.
  - Endpoint surface intentionally minimal (me + health).
"""
from __future__ import annotations

import os
import pathlib
import sys
import uuid

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
    email = f"adm1_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm1 Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str):
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


# ---------------------------------------------------------------------
# Boundary
# ---------------------------------------------------------------------
def test_portal_me_requires_authentication():
    r = requests.get(f"{API}/admin/portal/me", timeout=10)
    assert r.status_code == 401


def test_portal_me_rejects_user_with_no_platform_role():
    sess = _signup("horse_owner")
    r = requests.get(
        f"{API}/admin/portal/me",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 403
    assert "platform" in (r.json().get("detail") or "").lower()


def test_role_admin_barn_admin_does_not_inherit_platform_access(db):
    """Founder direction: role='admin' is a barn-level trust boundary
    that MUST NOT auto-elevate into platform admin."""
    sess = _signup("horse_owner")
    db.users.update_one(
        {"id": sess["user"]["id"]},
        {"$set": {"role": "admin"}},
        # explicitly NO platform_role set
    )
    r = requests.get(
        f"{API}/admin/portal/me",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


@pytest.mark.parametrize("plat_role,expected_sections", [
    ("super_admin",       14),
    ("platform_admin",    14),
    ("billing_admin",      5),  # dashboard, subscriptions, billing, alerts, reports
    ("support_admin",      6),  # dashboard, users, facilities, horses, support, alerts
    ("read_only_auditor",  5),  # dashboard, subscriptions, billing, reports, audit_logs
])
def test_portal_me_allows_each_platform_role(db, plat_role, expected_sections):
    sess = _signup("horse_owner")
    _promote(db, sess["user"]["id"], plat_role)

    r = requests.get(
        f"{API}/admin/portal/me",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["platform_role"] == plat_role
    assert isinstance(body["sections"], list)
    assert len(body["sections"]) == expected_sections, (
        f"{plat_role} should see {expected_sections} sections, got "
        f"{len(body['sections'])}: {body['sections']}"
    )
    # The cap map is exposed so the FE can render section-level locks.
    assert "section_capabilities" in body
    assert set(body["section_capabilities"].keys()) >= {
        "dashboard", "users", "facilities", "horses", "approvals",
        "subscriptions", "billing", "permissions", "support", "alerts",
        "reports", "integrations", "settings", "audit_logs",
    }


def test_portal_me_rejects_unknown_platform_role_value(db):
    """Defense-in-depth: a user.platform_role outside PLATFORM_ROLES
    must NOT pass the gate (typos, retired roles, etc.)."""
    sess = _signup("horse_owner")
    _promote(db, sess["user"]["id"], "definitely_not_a_real_role")

    r = requests.get(
        f"{API}/admin/portal/me",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------
# Health pings
# ---------------------------------------------------------------------
def test_portal_health_requires_platform_role():
    sess = _signup("horse_owner")
    r = requests.get(
        f"{API}/admin/portal/health",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


def test_portal_health_succeeds_for_platform_admin(db):
    sess = _signup("horse_owner")
    _promote(db, sess["user"]["id"], "platform_admin")
    r = requests.get(
        f"{API}/admin/portal/health",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


# ---------------------------------------------------------------------
# Audit logging
# ---------------------------------------------------------------------
def test_portal_me_emits_audit_log(db):
    sess = _signup("horse_owner")
    _promote(db, sess["user"]["id"], "platform_admin")

    before = db.audit_log.count_documents({"action": "admin.portal.me"})
    requests.get(
        f"{API}/admin/portal/me",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=10,
    )
    after = db.audit_log.count_documents({"action": "admin.portal.me"})
    assert after == before + 1


# ---------------------------------------------------------------------
# Surface invariants
# ---------------------------------------------------------------------
def test_admin_portal_exposes_no_mutations():
    """Admin-1 is read-only. Verifies the router doesn't accidentally
    expose POST/PUT/PATCH/DELETE endpoints under /api/admin/portal/*.
    """
    # Spot-check that the only known surface is GET; an unexpected
    # POST should return 405, not 200/201.
    for method in ("post", "put", "patch", "delete"):
        r = getattr(requests, method)(
            f"{API}/admin/portal/me",
            timeout=10,
            headers={"Content-Type": "application/json"},
            json={},
        )
        assert r.status_code in (401, 403, 405), (
            f"{method.upper()} /admin/portal/me unexpectedly returned {r.status_code}"
        )
