"""tests/test_admin_portal_admin4b.py — Admin Portal facility mutations
and soft-disable tenancy enforcement (Phase Admin-4b).

Covers founder-locked invariants:
  1. Mutable whitelist (`name, address, phone, contact_email, timezone,
     notes`) — every other field returns 422.
  2. Never-editable list is enforced even when a field appears valid
     (e.g. attempting `subscription_id` or `stripe_customer_id`).
  3. `--force-role-change` (wait — that's Admin-8). Here: only
     `super_admin` + `platform_admin` can mutate; `support_admin`,
     `billing_admin`, `read_only_auditor`, and barn-scoped roles are
     blocked.
  4. Soft-disable + reenable emit the locked audit actions with
     non-sensitive metadata only (NO raw before/after values for
     profile fields, NO free-text reason details).
  5. Disable idempotency → 409. Reenable idempotency → 409.
  6. Tenancy enforcement: a disabled-facility member is blocked from
     representative tenant-scoped product routes with a generic 403
     `"Facility unavailable"`. Platform admins continue to operate.
  7. `/auth/me` exposes `facility_status` so the frontend can render
     a banner; `/auth/refresh` still works for disabled-barn users
     (login flow is not blocked).
  8. Disable / reenable do NOT mutate any Phase 9 invoice /
     recurring_charge document OR any Phase 15 subscription /
     payment / webhook document (apart from the ordinary audit row).
  9. No Stripe-shaped or `subscription_id` value leaks into the
     facility list / detail / PATCH / disable / reenable response.
"""
from __future__ import annotations

import os
import pathlib
import re
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

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

_STRIPE_LEAK_RE = re.compile(r"\b(?:sub|cus|pi|ch|evt|in|price)_[A-Za-z0-9]{14,}\b")


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


# ---------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------
def _signup(role: str = "horse_owner") -> Dict[str, Any]:
    email = f"adm4b_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm4b Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str) -> None:
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _admin_session(db, plat_role: str = "platform_admin") -> Dict[str, Any]:
    s = _signup()
    _promote(db, s["user"]["id"], plat_role)
    return s


def _bearer(s: Dict[str, Any]) -> Dict[str, str]:
    return {"Authorization": f"Bearer {s['token']}"}


def _make_test_barn(db) -> str:
    barn_id = f"barn_adm4b_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({
        "id": barn_id,
        "name": "Admin-4b Test Stables",
        "address": "1 Test Lane",
        "phone": "+1-555-0000",
        "contact_email": "test@example.com",
        "timezone": "America/New_York",
        "notes": "",
        "status": "active",
        "subscription_tier_code": "starter",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "_admin4b_test": True,
    })
    return barn_id


def _barn_member_session(db, barn_id: str) -> Dict[str, Any]:
    """Sign up a fresh barn-scoped user, then move them into the test
    barn so we can disable that barn without affecting other tests'
    primary-barn users."""
    s = _signup()
    db.users.update_one(
        {"id": s["user"]["id"]},
        {"$set": {"barn_id": barn_id, "_admin4b_test": True}},
    )
    return s


def _cleanup(db, barn_id: Optional[str] = None):
    db.users.delete_many({"_admin4b_test": True})
    if barn_id:
        db.barns.delete_many({"id": barn_id})
        db.audit_log.delete_many({"resource_id": barn_id, "resource_type": "facility"})


# ---------------------------------------------------------------------
# 1 + 2 — PATCH whitelist + disallowed-field rejection
# ---------------------------------------------------------------------
def test_patch_facility_allows_whitelisted_fields(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"name": "Renamed Stables", "phone": "+1-555-9999"},
            timeout=10,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["barn"]["name"] == "Renamed Stables"
        assert body["barn"]["phone"] == "+1-555-9999"

        # Audit row carries CHANGED FIELDS only — never raw before/after.
        rows = list(db.audit_log.find(
            {"resource_id": barn_id, "action": "admin.facility.updated"},
        ))
        assert rows, "expected admin.facility.updated audit row"
        meta = rows[-1].get("metadata", {})
        assert set(meta.get("changed_fields", [])) >= {"name", "phone"}
        # Defensive: no raw value leaks.
        as_text = str(meta)
        assert "Renamed Stables" not in as_text, "audit must not store raw values"
        assert "+1-555-9999" not in as_text
    finally:
        _cleanup(db, barn_id)


@pytest.mark.parametrize("bad_field,bad_value", [
    ("subscription_id",          "sub_locally_irrelevant"),
    ("stripe_customer_id",       "cus_irrelevant"),
    ("subscription_tier_code",   "premium"),
    ("subscription_entitlements", {"horses": 50}),
    ("created_at",               "2020-01-01T00:00:00+00:00"),
    ("barn_id",                  "barn_other"),
    ("status",                   "disabled"),
    ("demo_seed_key",            "x"),
])
def test_patch_facility_rejects_never_editable_fields(db, bad_field, bad_value):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={bad_field: bad_value},
            timeout=10,
        )
        assert r.status_code == 422, (
            f"expected 422 for {bad_field!r}, got {r.status_code}: {r.text}"
        )
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_rejects_unknown_fields(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"name": "ok", "color_scheme": "purple"},
            timeout=10,
        )
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_validates_email_format(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"contact_email": "not-an-email"},
            timeout=10,
        )
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_validates_iana_timezone(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        # garbage tz string
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"timezone": "Mars/Olympus"},
            timeout=10,
        )
        assert r.status_code == 422, r.text
        # valid tz passes
        r2 = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"timezone": "Europe/London"},
            timeout=10,
        )
        assert r2.status_code == 200, r2.text
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_rejects_empty_body(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={},
            timeout=10,
        )
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_returns_404_for_missing_barn(db):
    s = _admin_session(db, "platform_admin")
    r = requests.patch(
        f"{API}/admin/portal/facilities/does-not-exist-{uuid.uuid4().hex[:6]}",
        headers=_bearer(s),
        json={"name": "x"},
        timeout=10,
    )
    assert r.status_code == 404, r.text


# ---------------------------------------------------------------------
# 3 — permission matrix
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role,expected", [
    ("super_admin",       200),
    ("platform_admin",    200),
    ("support_admin",     403),
    ("billing_admin",     403),
    ("read_only_auditor", 403),
])
def test_patch_facility_permission_matrix(db, role, expected):
    s = _admin_session(db, role)
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"name": "Allowed?"},
            timeout=10,
        )
        assert r.status_code == expected, (
            f"role={role} expected={expected} got={r.status_code} body={r.text}"
        )
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_blocks_barn_scoped_admin(db):
    """Barn-scoped role="admin" with NO platform_role cannot mutate."""
    s = _signup()
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"role": "admin"}})
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"name": "Sneaky"},
            timeout=10,
        )
        assert r.status_code == 403, r.text
    finally:
        _cleanup(db, barn_id)


def test_patch_facility_blocks_barn_manager(db):
    s = _signup()
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"role": "barn_manager"}})
    barn_id = _make_test_barn(db)
    try:
        r = requests.patch(
            f"{API}/admin/portal/facilities/{barn_id}",
            headers=_bearer(s),
            json={"name": "Sneaky"},
            timeout=10,
        )
        assert r.status_code == 403, r.text
    finally:
        _cleanup(db, barn_id)


# ---------------------------------------------------------------------
# 4 + 5 — disable / reenable happy path + idempotency
# ---------------------------------------------------------------------
def test_disable_facility_happy_path(db):
    s = _admin_session(db, "super_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "billing_dispute",
                  "reason_details": "Operator-only context"},
            timeout=10,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["status"] == "disabled"

        barn = db.barns.find_one({"id": barn_id})
        assert barn["status"] == "disabled"
        assert barn["disabled_at"]
        assert barn["disabled_by"] == s["user"]["id"]
        assert barn["disabled_reason"] == "billing_dispute"
        # Operator-only context IS stored on the barn for context…
        assert barn.get("disabled_reason_details") == "Operator-only context"

        # …but NEVER in audit metadata (founder decision 4b).
        rows = list(db.audit_log.find(
            {"resource_id": barn_id, "action": "admin.facility.disabled"},
        ))
        assert rows, "expected admin.facility.disabled audit row"
        meta = rows[-1].get("metadata", {})
        assert meta.get("reason_category") == "billing_dispute"
        assert meta.get("reason_provided") is True
        assert "Operator-only context" not in str(meta), (
            "free-text reason details must NEVER appear in audit metadata"
        )
    finally:
        _cleanup(db, barn_id)


def test_disable_rejects_unknown_reason_category(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "vibes_off"},
            timeout=10,
        )
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db, barn_id)


def test_disable_twice_returns_409(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r1 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s), json={"reason_category": "abuse"}, timeout=10,
        )
        assert r1.status_code == 200, r1.text
        r2 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s), json={"reason_category": "abuse"}, timeout=10,
        )
        assert r2.status_code == 409, r2.text
    finally:
        _cleanup(db, barn_id)


def test_reenable_happy_path(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        # Disable first.
        r1 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "customer_request"},
            timeout=10,
        )
        assert r1.status_code == 200
        # Reenable.
        r2 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/reenable",
            headers=_bearer(s), timeout=10,
        )
        assert r2.status_code == 200, r2.text
        barn = db.barns.find_one({"id": barn_id})
        assert barn["status"] == "active"
        assert barn["reenabled_at"]
        assert barn["reenabled_by"] == s["user"]["id"]
        assert barn.get("disabled_reason") == ""
        # Historical disable info preserved.
        assert barn.get("disabled_at")
        assert barn.get("disabled_by")

        rows = list(db.audit_log.find(
            {"resource_id": barn_id, "action": "admin.facility.reenabled"},
        ))
        assert rows
    finally:
        _cleanup(db, barn_id)


def test_reenable_active_returns_409(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    try:
        r = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/reenable",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 409, r.text
    finally:
        _cleanup(db, barn_id)


@pytest.mark.parametrize("role", ["support_admin", "billing_admin", "read_only_auditor"])
def test_disable_permission_matrix_non_writers_blocked(db, role):
    s = _admin_session(db, role)
    barn_id = _make_test_barn(db)
    try:
        r = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "abuse"},
            timeout=10,
        )
        assert r.status_code == 403, r.text
    finally:
        _cleanup(db, barn_id)


# ---------------------------------------------------------------------
# 6 — tenancy enforcement: disabled barn member gets 403 on product
# routes; platform admin still works.
# ---------------------------------------------------------------------
def test_disabled_facility_member_blocked_on_product_routes(db):
    admin = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    member = _barn_member_session(db, barn_id)
    try:
        # Sanity: while active, the member can call a product route.
        r_active = requests.get(f"{API}/horses",
                                headers=_bearer(member), timeout=10)
        # 200 (no horses) or 200/empty list; must NOT be 403 yet.
        assert r_active.status_code != 403, (
            f"active barn member should not be blocked; got {r_active.status_code}"
        )

        # Disable the barn.
        rd = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(admin),
            json={"reason_category": "security"},
            timeout=10,
        )
        assert rd.status_code == 200, rd.text

        # Now the same member is blocked on representative product routes.
        # Coverage: horses (Phase 4 CRUD), owner-updates (Phase 7A
        # Owner Trust Layer), invoices (Phase 9 billing read path).
        for path in ("/horses", "/owner-updates", "/invoices"):
            rr = requests.get(f"{API}{path}",
                              headers=_bearer(member), timeout=10)
            assert rr.status_code == 403, (
                f"expected 403 on {path} after disable, got {rr.status_code}: {rr.text}"
            )
            assert "Facility unavailable" in (rr.json().get("detail") or ""), (
                f"wrong detail text on {path}: {rr.text}"
            )

        # Platform admin can STILL view the disabled facility via portal.
        rp = requests.get(f"{API}/admin/portal/facilities/{barn_id}",
                          headers=_bearer(admin), timeout=10)
        assert rp.status_code == 200, rp.text
    finally:
        _cleanup(db, barn_id)


def test_disabled_facility_member_still_has_auth_me(db):
    """/auth/me must still return for a disabled-barn user so the
    frontend can render a 'Facility unavailable' banner. The shape
    is additively extended with `facility_status`."""
    admin = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    member = _barn_member_session(db, barn_id)
    try:
        # Disable the barn first.
        rd = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(admin),
            json={"reason_category": "abuse"},
            timeout=10,
        )
        assert rd.status_code == 200

        rm = requests.get(f"{API}/auth/me",
                          headers=_bearer(member), timeout=10)
        assert rm.status_code == 200, rm.text
        body = rm.json()
        assert body.get("facility_status") == "disabled", body

        # Confirm an active barn (admin's own barn = primary) reports "active".
        ra = requests.get(f"{API}/auth/me",
                          headers=_bearer(admin), timeout=10)
        assert ra.status_code == 200
        assert ra.json().get("facility_status") == "active"
    finally:
        _cleanup(db, barn_id)


def test_disabled_facility_member_can_refresh(db):
    """/auth/refresh must continue to work for a disabled barn member —
    they need to be able to keep their session alive to see the banner."""
    admin = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    member = _barn_member_session(db, barn_id)
    try:
        rd = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(admin),
            json={"reason_category": "abuse"},
            timeout=10,
        )
        assert rd.status_code == 200
        # We don't care about refresh succeeding semantically — only
        # that it's not blocked by the new tenancy gate.
        rr = requests.post(f"{API}/auth/refresh",
                           headers=_bearer(member),
                           timeout=10)
        # Either 200/401 are acceptable; 403 "Facility unavailable" is NOT.
        if rr.status_code == 403:
            assert "Facility unavailable" not in (rr.json().get("detail") or ""), (
                "refresh must not be tenancy-gated"
            )
    finally:
        _cleanup(db, barn_id)


# ---------------------------------------------------------------------
# 8 — Phase 9 / Phase 15 untouched by disable / reenable.
# ---------------------------------------------------------------------
def test_disable_does_not_mutate_phase9_or_phase15_docs(db):
    """Plant a Phase 9 invoice + Phase 15 subscription tied to the
    test barn, then disable/reenable. The non-audit document fields
    must be byte-identical afterwards."""
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    inv_id = f"inv_adm4b_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_local_adm4b_{uuid.uuid4().hex[:8]}"
    rc_id = f"rc_adm4b_{uuid.uuid4().hex[:8]}"
    db.invoices.insert_one({
        "id": inv_id, "barn_id": barn_id, "amount_cents": 12000,
        "status": "open", "_admin4b_test": True,
        "created_at": "2026-01-01T00:00:00+00:00",
    })
    db.subscriptions.insert_one({
        "id": sub_id, "barn_id": barn_id, "status": "active",
        "tier": "starter", "_admin4b_test": True,
    })
    db.recurring_charges.insert_one({
        "id": rc_id, "barn_id": barn_id, "amount_cents": 5000,
        "status": "active", "_admin4b_test": True,
    })
    try:
        before_inv = dict(db.invoices.find_one({"id": inv_id}))
        before_sub = dict(db.subscriptions.find_one({"id": sub_id}))
        before_rc = dict(db.recurring_charges.find_one({"id": rc_id}))

        r1 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "billing_dispute"},
            timeout=10,
        )
        assert r1.status_code == 200
        r2 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/reenable",
            headers=_bearer(s), timeout=10,
        )
        assert r2.status_code == 200

        after_inv = dict(db.invoices.find_one({"id": inv_id}))
        after_sub = dict(db.subscriptions.find_one({"id": sub_id}))
        after_rc = dict(db.recurring_charges.find_one({"id": rc_id}))
        assert after_inv == before_inv, "Phase 9 invoice was mutated"
        assert after_sub == before_sub, "Phase 15 subscription was mutated"
        assert after_rc == before_rc, "Phase 9 recurring_charge was mutated"
    finally:
        db.invoices.delete_many({"_admin4b_test": True})
        db.subscriptions.delete_many({"_admin4b_test": True})
        db.recurring_charges.delete_many({"_admin4b_test": True})
        _cleanup(db, barn_id)


# ---------------------------------------------------------------------
# 9 — No Stripe-shaped ID / `subscription_id` leak in any
# facility list / detail / PATCH / disable / reenable response.
# ---------------------------------------------------------------------
def test_no_stripe_id_leak_in_facility_responses(db):
    s = _admin_session(db, "platform_admin")
    barn_id = _make_test_barn(db)
    # Plant a Stripe-shaped subscription_id directly on the barn so
    # the safety net is actually exercised.
    db.barns.update_one(
        {"id": barn_id},
        {"$set": {"subscription_id": "sub_TESTleak1234567890",
                  "stripe_customer_id": "cus_TESTleak1234567890"}},
    )
    try:
        # list
        r1 = requests.get(f"{API}/admin/portal/facilities?limit=50",
                          headers=_bearer(s), timeout=10)
        assert r1.status_code == 200
        assert "subscription_id" not in r1.text
        assert not _STRIPE_LEAK_RE.search(r1.text), r1.text[:400]

        # detail
        r2 = requests.get(f"{API}/admin/portal/facilities/{barn_id}",
                          headers=_bearer(s), timeout=10)
        assert r2.status_code == 200
        assert "subscription_id" not in r2.text
        assert not _STRIPE_LEAK_RE.search(r2.text), r2.text[:400]

        # PATCH
        r3 = requests.patch(f"{API}/admin/portal/facilities/{barn_id}",
                            headers=_bearer(s),
                            json={"name": "Renamed"}, timeout=10)
        assert r3.status_code == 200
        assert "subscription_id" not in r3.text
        assert not _STRIPE_LEAK_RE.search(r3.text), r3.text[:400]

        # disable
        r4 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/disable",
            headers=_bearer(s),
            json={"reason_category": "abuse"}, timeout=10,
        )
        assert r4.status_code == 200
        assert "subscription_id" not in r4.text
        assert not _STRIPE_LEAK_RE.search(r4.text), r4.text[:400]

        # reenable
        r5 = requests.post(
            f"{API}/admin/portal/facilities/{barn_id}/reenable",
            headers=_bearer(s), timeout=10,
        )
        assert r5.status_code == 200
        assert "subscription_id" not in r5.text
        assert not _STRIPE_LEAK_RE.search(r5.text), r5.text[:400]
    finally:
        _cleanup(db, barn_id)


# ---------------------------------------------------------------------
# 10 — /admin/portal/me carries the new `capabilities.facilities_write`.
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role,expected", [
    ("super_admin",       True),
    ("platform_admin",    True),
    ("support_admin",     False),
    ("billing_admin",     False),
    ("read_only_auditor", False),
])
def test_admin_portal_me_exposes_facilities_write_capability(db, role, expected):
    s = _admin_session(db, role)
    r = requests.get(f"{API}/admin/portal/me",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200, r.text
    caps = r.json().get("capabilities", {})
    assert caps.get("facilities_write") is expected, (
        f"role={role} expected facilities_write={expected}; got {caps}"
    )
