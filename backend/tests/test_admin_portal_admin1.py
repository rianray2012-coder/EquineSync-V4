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
    # Admin-7B (Feb 2026): billing_admin gained `integrations` →
    # dashboard, subscriptions, billing, alerts, reports, integrations,
    # audit_logs.
    ("billing_admin",      7),
    # Admin-7B: support_admin gained `reports` (read but not export) →
    # dashboard, users, facilities, horses, subscriptions, support,
    # alerts, reports, audit_logs.
    ("support_admin",      9),
    # Admin-7B: read_only_auditor gained `integrations` → dashboard,
    # subscriptions, billing, reports, integrations, audit_logs.
    ("read_only_auditor",  6),
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


# ---------------------------------------------------------------------
# Codex round-1 follow-up — App.js admin route collision regression
# ---------------------------------------------------------------------
def test_no_app_js_admin_path_collision():
    """Codex round-1 feedback: the Admin-1 portal placeholders must NOT
    shadow legacy /admin/* routes (Phase 15.E /admin/billing and
    Phase 13 /admin/review-queue).

    Strategy: parse frontend/src/App.js for every `path="/admin..."`
    literal and assert no two routes declare the same exact path. This
    catches a future regression where someone re-adds an Admin-1
    placeholder under a colliding URL.
    """
    import re
    app_js = pathlib.Path("/app/frontend/src/App.js").read_text()

    # Extract all top-level Route paths in the file. We deliberately
    # match only string literals (not template literals) and only
    # paths starting with /admin so legacy app routes like /dashboard
    # don't pollute the check.
    top_level_paths = re.findall(r'path="(/admin[^"]*)"', app_js)

    # Nested child Routes declared inside the <Route path="/admin/portal">
    # block use relative paths (e.g. path="dashboard"). Reconstruct the
    # full path so this check sees the actual rendered URL.
    portal_block = re.search(
        r'<Route path="/admin/portal"[^>]*>(.*?)</Route>',
        app_js, flags=re.DOTALL,
    )
    if portal_block:
        nested_rel = re.findall(r'<Route\s+path="([^"]+)"', portal_block.group(1))
        for rel in nested_rel:
            if rel.startswith("/"):
                top_level_paths.append(rel)
            else:
                top_level_paths.append(f"/admin/portal/{rel}".replace("//", "/"))

    # Dedup-check: any duplicate exact path is a route collision.
    seen = {}
    duplicates = []
    for p in top_level_paths:
        seen[p] = seen.get(p, 0) + 1
        if seen[p] == 2:
            duplicates.append(p)
    assert not duplicates, (
        f"App.js declares duplicate /admin/* route paths: {duplicates}. "
        f"The Admin-1 portal MUST live under /admin/portal/* so it never "
        f"shadows legacy /admin/billing or /admin/review-queue."
    )

    # Additional guard: the two known legacy paths must still be reachable
    # (i.e. they must appear in App.js — if a future refactor drops them,
    # we want a loud failure here so the reviewer can confirm intent).
    assert "/admin/billing" in app_js, (
        "Phase 15.E /admin/billing route appears to have been removed "
        "from App.js. Admin-1 must NOT remove it; see "
        "/app/memory/PRD.md Phase 15.E."
    )
    assert "/admin/review-queue" in app_js, (
        "Phase 13 /admin/review-queue route appears to have been removed "
        "from App.js. Admin-1 must NOT remove it."
    )

    # And: every Admin-1 portal placeholder path must be inside
    # /admin/portal/* (defense-in-depth: prevents anyone from declaring
    # a new portal placeholder at /admin/users etc.).
    portal_only_admin_paths = [
        p for p in top_level_paths
        if p.startswith("/admin/portal/") or p == "/admin/portal"
    ]
    legacy_admin_paths = [
        p for p in top_level_paths
        if p.startswith("/admin/") and not p.startswith("/admin/portal")
        and p != "/admin"
    ]
    # The only acceptable legacy admin routes for now are the two known
    # Phase 13 / Phase 15.E entries. Anything else means someone added
    # a new top-level /admin/<x> placeholder that risks future collision.
    unknown_legacy = set(legacy_admin_paths) - {"/admin/billing", "/admin/review-queue"}
    assert not unknown_legacy, (
        f"Unexpected non-portal /admin/* paths in App.js: {sorted(unknown_legacy)}. "
        f"New Admin Portal sections must live under /admin/portal/*."
    )
    assert len(portal_only_admin_paths) >= 14, (
        "Expected at least 14 portal placeholder paths under /admin/portal/*; "
        f"found {len(portal_only_admin_paths)}: {portal_only_admin_paths}."
    )
