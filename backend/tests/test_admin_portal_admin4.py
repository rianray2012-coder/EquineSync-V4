"""tests/test_admin_portal_admin4.py — Admin Portal facility roster.

Covers Admin-4 (read-only cross-facility surface):
  - GET /api/admin/portal/facilities        (paginated, search, filter)
  - GET /api/admin/portal/facilities/{id}   (summary-only health page)

Locked decisions from the founder gate:
  - 1a — READ-ONLY ONLY (no mutations land in Admin-4).
  - 2c — soft-disable deferred entirely (no tenancy-layer enforcement).
  - 3a — future mutable-field whitelist documented in code, NOT shipped.
  - 4a — subscription/usage data is SUMMARY only; no Stripe IDs, no
         drill-down to /subscriptions rows or /billing_events.
  - 5a — cross-facility isolation matrix below.

Critical invariants:
  - Every platform role (5) sees every facility (super_admin /
    platform_admin / support_admin / billing_admin / read_only_auditor).
  - Barn-scoped users (role="admin", role="horse_owner", etc. with NO
    platform_role) get 403 on /facilities and /facilities/{id} — they
    cannot read their OWN barn through the admin surface, let alone
    other barns.
  - No Stripe IDs anywhere in the response (the same Stripe-prefix
    leak guard used in Admin-2).
  - No mutation methods (POST/PUT/PATCH/DELETE) on either path.
  - Generic 404 for missing barn_id.
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
    email = f"adm4_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm4 Test", "role": role},
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


# ---------------------------------------------------------------------
# Access boundary — cross-facility isolation matrix (decision 5a)
# ---------------------------------------------------------------------
@pytest.mark.parametrize("platform_role,expected", [
    ("super_admin",       200),
    ("platform_admin",    200),
    ("support_admin",     200),
    ("billing_admin",     200),
    ("read_only_auditor", 200),
])
def test_facilities_list_visibility_by_platform_role(db, platform_role, expected):
    """Every platform role can list every facility — there's no
    facility-scoping for platform admins (per the Admin-1 founder
    direction: platform_role is a cross-facility trust boundary)."""
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/facilities?limit=5", headers=_bearer(s), timeout=10)
    assert r.status_code == expected


def test_facilities_list_blocks_barn_admin_without_platform_role(db):
    """Founder invariant carried forward: barn-level role="admin" must
    NOT inherit cross-facility admin access. Explicitly set role=admin
    AND NO platform_role to model a barn admin."""
    s = _signup()
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"role": "admin"}})
    r = requests.get(f"{API}/admin/portal/facilities", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_facilities_list_blocks_horse_owner(db):
    s = _signup()
    r = requests.get(f"{API}/admin/portal/facilities", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_facilities_list_unauthenticated_is_401():
    r = requests.get(f"{API}/admin/portal/facilities", timeout=10)
    assert r.status_code == 401


def test_facility_detail_blocks_own_barn_for_non_platform_user(db):
    """A barn-scoped user CANNOT read their OWN barn through the admin
    portal — that's the canonical isolation guarantee for the
    /admin/portal/facilities/{id} surface."""
    s = _signup()
    # Marketplace signups land on PRIMARY_BARN_ID="primary" — make sure
    # the user can't read /admin/portal/facilities/primary even though
    # it's "their" barn.
    own_barn_id = s["user"].get("barn_id") or "primary"
    r = requests.get(
        f"{API}/admin/portal/facilities/{own_barn_id}",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 403


def test_facility_detail_blocks_other_barn_for_non_platform_user(db):
    s = _signup()
    r = requests.get(
        f"{API}/admin/portal/facilities/some-other-barn-id",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 403


def test_facility_detail_404_for_missing_barn_when_platform_admin(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(
        f"{API}/admin/portal/facilities/does-not-exist-{uuid.uuid4().hex[:6]}",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------
# Shape — list endpoint
# ---------------------------------------------------------------------
def test_facilities_list_shape_includes_summary_fields(db):
    s = _admin_session(db, "platform_admin")
    # Plant a barn we can recognise.
    barn_id = f"barn_adm4_{uuid.uuid4().hex[:8]}"
    db.barns.insert_one({
        "id": barn_id, "name": f"Adm4 Test Stables {barn_id[-4:]}",
        "subscription_tier_code": "starter",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    try:
        r = requests.get(
            f"{API}/admin/portal/facilities?q=Adm4 Test Stables&limit=10",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        assert "items" in body and "total" in body and "next_cursor" in body
        ours = [x for x in body["items"] if x.get("id") == barn_id]
        assert ours, "Planted barn missing from search results."
        row = ours[0]
        for k in ("id", "name", "subscription_tier_code", "usage"):
            assert k in row
        assert {"horses_used", "horses_limit", "users_used", "users_limit"} <= set(row["usage"].keys())
    finally:
        db.barns.delete_one({"id": barn_id})


def test_facilities_list_search_q_filters_by_name(db):
    s = _admin_session(db, "platform_admin")
    tag = uuid.uuid4().hex[:8]
    db.barns.insert_one({
        "id": f"barn_q_{tag}", "name": f"UniqueName_{tag}",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    try:
        r = requests.get(
            f"{API}/admin/portal/facilities?q=UniqueName_{tag}",
            headers=_bearer(s), timeout=10,
        )
        body = r.json()
        assert body["total"] >= 1
        assert any(x.get("name", "").startswith(f"UniqueName_{tag}") for x in body["items"])
    finally:
        db.barns.delete_one({"id": f"barn_q_{tag}"})


# ---------------------------------------------------------------------
# Shape — detail endpoint (decision 4a: SUMMARY-only)
# ---------------------------------------------------------------------
def test_facility_detail_shape(db):
    s = _admin_session(db, "platform_admin")
    # Reuse the 'primary' barn which exists from marketplace signups.
    r = requests.get(f"{API}/admin/portal/facilities/primary",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "barn" in body
    assert "subscription_summary" in body
    assert "usage" in body
    assert "counts" in body
    assert "recent_activity" in body
    # Counts mirror the usage tile values.
    assert body["counts"]["users"] == body["usage"]["users_used"]
    assert body["counts"]["horses"] == body["usage"]["horses_used"]


def test_facility_detail_subscription_summary_has_no_stripe_ids(db):
    """Decision 4a: SUMMARY only. No Stripe IDs in the payload —
    Admin-5 owns the drill-down surface."""
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/facilities/primary",
                     headers=_bearer(s), timeout=10)
    body_text = r.text
    for forbidden in ("sub_", "cus_", "evt_", "price_", "pi_", "ch_",
                      "stripe_customer_id", "stripe_subscription_id",
                      "stripe_price_id"):
        assert forbidden not in body_text, (
            f"facility detail leaked Stripe field/prefix '{forbidden}'"
        )


# Codex round-2 (Admin-4) regression: `subscription_id` is needed
# INTERNALLY (the detail endpoint joins through it to fetch the
# subscription summary), but it MUST NOT cross the API boundary.
# `subscription_updated_at` is also stripped on the way out.
def test_facility_list_does_not_leak_internal_subscription_id(db):
    """List rows must NEVER carry `subscription_id` or
    `subscription_updated_at` — both are internal-only join keys."""
    s = _admin_session(db, "platform_admin")
    # Plant a barn with a subscription_id set so we KNOW the row would
    # carry it if the strip were ever removed.
    barn_id = f"barn_strip_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_internal_{uuid.uuid4().hex[:8]}"
    db.barns.insert_one({
        "id": barn_id, "name": f"StripTest_{barn_id[-4:]}",
        "subscription_tier_code": "starter",
        "subscription_id": sub_id,
        "subscription_updated_at": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    try:
        r = requests.get(
            f"{API}/admin/portal/facilities?q=StripTest_{barn_id[-4:]}",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        ours = [x for x in body["items"] if x.get("id") == barn_id]
        assert ours, "Planted barn missing from search results."
        row = ours[0]
        assert "subscription_id" not in row, (
            f"List leaked subscription_id: row={row}"
        )
        assert "subscription_updated_at" not in row, (
            f"List leaked subscription_updated_at: row={row}"
        )
        # And the join key value itself must not appear anywhere in the
        # serialized payload (defense in depth against rename leaks).
        assert sub_id not in r.text, (
            f"List leaked raw subscription_id value '{sub_id}'"
        )
    finally:
        db.barns.delete_one({"id": barn_id})


def test_facility_detail_does_not_leak_internal_subscription_id(db):
    """Detail payload must NEVER carry `subscription_id` or
    `subscription_updated_at` on `barn` — same invariant as the list."""
    s = _admin_session(db, "platform_admin")
    barn_id = f"barn_strip_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_internal_{uuid.uuid4().hex[:8]}"
    db.barns.insert_one({
        "id": barn_id, "name": f"StripDetail_{barn_id[-4:]}",
        "subscription_tier_code": "starter",
        "subscription_id": sub_id,
        "subscription_updated_at": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    try:
        r = requests.get(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        barn = body.get("barn") or {}
        assert "subscription_id" not in barn, (
            f"Detail.barn leaked subscription_id: {barn}"
        )
        assert "subscription_updated_at" not in barn, (
            f"Detail.barn leaked subscription_updated_at: {barn}"
        )
        # Belt-and-braces: full body must not contain the raw id either.
        assert sub_id not in r.text, (
            f"Detail leaked raw subscription_id value '{sub_id}'"
        )
    finally:
        db.barns.delete_one({"id": barn_id})


def test_facility_detail_subscription_summary_keys_are_whitelisted(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/facilities/primary",
                     headers=_bearer(s), timeout=10)
    summary = r.json().get("subscription_summary")
    if summary is None:
        pytest.skip("primary barn has no subscription_summary to inspect")
    # Whitelist — these are the ONLY keys the SUMMARY surface returns.
    allowed = {"plan_tier_code", "status", "billing_cycle",
               "current_period_end", "trial_end", "amount_cents",
               "updated_at"}
    extras = set(summary.keys()) - allowed
    assert not extras, f"Subscription summary leaked extra keys: {extras}"


def test_facility_detail_has_no_drill_down_links_or_billing_events(db):
    """Admin-4 must not include any /subscriptions/* drill-down link or
    billing_events references. Those live in Admin-5."""
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/facilities/primary",
                     headers=_bearer(s), timeout=10)
    body_text = r.text
    for forbidden in ("billing_events", "billing_event", "/admin/portal/subscriptions"):
        assert forbidden not in body_text, (
            f"facility detail leaked drill-down reference '{forbidden}'"
        )


# ---------------------------------------------------------------------
# Surface invariants — Admin-4 read-only ceiling (decision 1a)
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/facilities",
    "/admin/portal/facilities/primary",
])
def test_no_mutations_exposed_on_admin4_endpoints(path):
    """Decision 1a: Admin-4 is read-only. No mutation methods anywhere."""
    for method in ("post", "put", "patch", "delete"):
        r = getattr(requests, method)(
            f"{API}{path}", timeout=10,
            headers={"Content-Type": "application/json"}, json={},
        )
        assert r.status_code in (401, 403, 405), (
            f"{method.upper()} {path} unexpectedly returned {r.status_code}"
        )


def test_admin4_does_not_touch_phase9_invoices_or_recurring_charges(db):
    """Smoke check: the Admin-4 detail payload must NOT include any
    `invoice`, `invoices`, or `recurring_charge` reference. Phase 9
    stays untouched until a separately-gated phase."""
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/facilities/primary",
                     headers=_bearer(s), timeout=10)
    body_text = r.text.lower()
    for forbidden in ("\"invoices\"", "\"invoice\"", "recurring_charge"):
        assert forbidden not in body_text, (
            f"Admin-4 facility detail leaked Phase 9 reference '{forbidden}'"
        )


def test_both_endpoints_emit_audit_log(db):
    s = _admin_session(db, "platform_admin")
    h = _bearer(s)
    before_l = db.audit_log.count_documents({"action": "admin.portal.read.facilities"})
    before_d = db.audit_log.count_documents({"action": "admin.portal.read.facility_detail"})
    requests.get(f"{API}/admin/portal/facilities?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/facilities/primary", headers=h, timeout=10)
    assert db.audit_log.count_documents({"action": "admin.portal.read.facilities"}) == before_l + 1
    assert db.audit_log.count_documents({"action": "admin.portal.read.facility_detail"}) == before_d + 1
