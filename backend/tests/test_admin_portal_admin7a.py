"""tests/test_admin_portal_admin7a.py — Admin-7A.1 layered-split
regression.

Goals:
  - Prove every Admin-1..6 endpoint still exists under the same path
    after the layered split (route-map preservation).
  - Sanity-check the response shape of one representative endpoint
    per locked surface (response-shape preservation).
  - Confirm the new helper boundary in `routes/admin_portal/_helpers.py`
    exposes the locked public surface.
  - No behavior change: this whole suite must pass against the new
    package layout (`routes/admin_portal/portal.py` +
    `routes/admin_portal/_helpers.py` + `routes/admin_portal/__init__.py`)
    AND would have passed against the pre-split flat module.
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


def _admin_session(db, plat_role: str = "platform_admin") -> dict:
    email = f"adm7a_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(f"{API}/auth/signup", json={
        "email": email, "password": "securepass1",
        "full_name": "A7A Test", "role": "horse_owner",
    }, timeout=15)
    r.raise_for_status()
    s = r.json()
    db.users.update_one({"id": s["user"]["id"]},
                        {"$set": {"platform_role": plat_role}})
    return s


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


# ---------------------------------------------------------------------
# Helper boundary — confirm the new `_helpers.py` exposes the locked
# public surface and that it points at the same callables that
# `portal.py` registered (Admin-7A.1 invariant).
# ---------------------------------------------------------------------
def test_helpers_module_exposes_locked_surface():
    """The Admin-7A.1 helper boundary must expose every name in the
    locked `__all__` list. Per-surface modules in 7A.2 import from
    here, so a missing name now means a 7A.2 import error later."""
    from routes.admin_portal import _helpers
    locked = {
        "SECTION_CAPABILITIES", "_sections_for",
        "_METADATA_SCRUB_KEYS", "_STRIPE_VALUE_PATTERNS",
        "_STRIPE_EMBEDDED_RE", "_STRIPE_VALUE_RE", "_METADATA_VALUE_MAX_LEN",
        "_ACTIVITY_EXCLUDE_PREFIXES",
        "_redact_stripe_in_string", "_scrub_metadata", "_scrub_metadata_value",
        "_scrub_text",
        "_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
        "_strip_keys",
    }
    for name in locked:
        assert hasattr(_helpers, name), f"_helpers missing {name}"
        assert name in (_helpers.__all__ or ()), f"{name} not in __all__"


def test_helpers_are_identical_to_portal_definitions():
    """Re-export shim: `_helpers.X is portal.X` for every locked
    helper. Once 7A.2 physically moves them, the `is` test becomes
    `portal.X is _helpers.X` (one canonical place)."""
    from routes.admin_portal import _helpers
    from routes.admin_portal import portal as portal_module
    for name in ("_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
                 "_scrub_metadata", "_scrub_text", "_strip_keys",
                 "_sections_for", "SECTION_CAPABILITIES"):
        assert getattr(_helpers, name) is getattr(portal_module, name), (
            f"_helpers.{name} is not the same object as portal.{name}"
        )


def test_build_router_importable_from_package():
    """External import path must resolve to the same callable as the
    package's `portal.build_router`."""
    from routes.admin_portal import build_router as pkg_br
    from routes.admin_portal.portal import build_router as inner_br
    assert pkg_br is inner_br


# ---------------------------------------------------------------------
# Route-map preservation — every locked Admin-1..6 endpoint must still
# be registered under the same path + same allowed HTTP methods.
# ---------------------------------------------------------------------
LOCKED_GET_ROUTES = [
    # Admin-1
    "/api/admin/portal/me",
    "/api/admin/portal/health",
    # Admin-2 (the dashboard is composed from these three endpoints)
    "/api/admin/portal/kpis",
    "/api/admin/portal/subscription-health",
    "/api/admin/portal/activity",
    # Admin-3
    "/api/admin/portal/users",
    "/api/admin/portal/users/{user_id}",
    "/api/admin/portal/approvals",
    # Admin-4
    "/api/admin/portal/facilities",
    "/api/admin/portal/facilities/{barn_id}",
    # Admin-5
    "/api/admin/portal/subscriptions",
    "/api/admin/portal/subscriptions/{admin_ref}",
    "/api/admin/portal/billing-events",
    "/api/admin/portal/payments",
    # Admin-6
    "/api/admin/portal/audit-logs",
    "/api/admin/portal/audit-logs/{audit_ref}",
    "/api/admin/portal/support",
    "/api/admin/portal/support/{ticket_ref}",
    "/api/admin/portal/alerts",
]
LOCKED_POST_ROUTES = [
    # Admin-3
    "/api/admin/portal/users/{user_id}/approve",
    "/api/admin/portal/users/{user_id}/reject",
    "/api/admin/portal/users/{user_id}/suspend",
    "/api/admin/portal/users/{user_id}/reactivate",
    # Admin-6
    "/api/admin/portal/support/{ticket_ref}/status",
    "/api/admin/portal/support/{ticket_ref}/assign",
    "/api/admin/portal/support/{ticket_ref}/notes",
]


def _all_routes():
    """Pull every registered path + method-set off the live FastAPI app."""
    sys.path.insert(0, "/app/backend")
    from server import app
    out = {}
    for r in app.routes:
        path = getattr(r, "path", None)
        if not path:
            continue
        methods = set(getattr(r, "methods", ()) or ())
        out.setdefault(path, set()).update(methods)
    return out


def test_all_locked_admin_portal_routes_present():
    routes = _all_routes()
    missing = [p for p in LOCKED_GET_ROUTES + LOCKED_POST_ROUTES
               if p not in routes]
    assert not missing, (
        f"Admin-7A.1 split lost {len(missing)} locked route(s): {missing}"
    )


@pytest.mark.parametrize("path", LOCKED_GET_ROUTES)
def test_locked_get_routes_accept_get(path):
    routes = _all_routes()
    assert "GET" in routes[path], f"{path} no longer accepts GET"


@pytest.mark.parametrize("path", LOCKED_POST_ROUTES)
def test_locked_post_routes_accept_post(path):
    routes = _all_routes()
    assert "POST" in routes[path], f"{path} no longer accepts POST"


# ---------------------------------------------------------------------
# Response-shape regressions — one canonical shape probe per surface.
# Confirms the split didn't drop a field / rename a key by accident.
# ---------------------------------------------------------------------
def test_shape_admin1_me(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/me", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("platform_role", "sections"):
        assert k in body, f"/me missing key {k}"
    assert isinstance(body["sections"], list)


def test_shape_admin2_kpis(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/kpis", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    # KPIs surface keys may evolve; just confirm we receive a dict.
    assert isinstance(r.json(), dict)


def test_shape_admin2_activity(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/activity?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "items" in body


def test_shape_admin3_users(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/users?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total", "limit", "cursor"):
        assert k in body, f"/users missing key {k}"


def test_shape_admin4_facilities(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/facilities?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total"):
        assert k in body


def test_shape_admin5_subscriptions(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/subscriptions?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total", "next_cursor"):
        assert k in body


def test_shape_admin5_billing_events(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/billing-events?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    assert "items" in r.json()


def test_shape_admin6_audit_logs(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/audit-logs?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total", "next_cursor"):
        assert k in body


def test_shape_admin6_support(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/support?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total"):
        assert k in body


def test_shape_admin6_alerts(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/alerts", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("items", "total"):
        assert k in body
