"""tests/test_horse_ledger_1a.py — Phase HorseOps-1A verification.

Locked test target: 27 green tests. All are tightly scoped to 1-A
(read-only composition + foundations). Coverage map:

  1-9    Read shape + barn scoping + Admin-4b enforcement.
 10-14   Owner-filtered shape — fail-closed semantics.
 15-16   No Stripe-shape / no billing-word leak.
 17-20   Adjacent phases (9 / 15 / Admin Portal / inventory) untouched.
 21      Legacy `horses` row unchanged after a Ledger read.
 22      All 15 HorseOps-1A indexes exist on startup.
 23      Inventory / service_requests / staff_invites / payment_profiles untouched.
 24-25   Role-driven fail-closed: horse_owner ALWAYS gets owner shape
        regardless of query string.
 26      Platform-role cannot cross-barn-inspect via this product route.
 27      Index creation creates ZERO documents.
"""
from __future__ import annotations

import ast
import os
import pathlib
import re
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

import pytest
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
load_dotenv(ROOT / "backend" / ".env")


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
_BILLING_KEYS = {"balance", "due_amount", "owing", "invoice_id",
                 "subscription_id", "stripe_customer_id"}


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role: str = "horse_owner") -> Dict[str, Any]:
    email = f"hl1a_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "HL Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _bearer(s: Dict[str, Any]) -> Dict[str, str]:
    return {"Authorization": f"Bearer {s['token']}"}


def _promote(db, user_id: str, platform_role: str) -> None:
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _make_barn(db, status: str = "active") -> str:
    barn_id = f"barn_hl1a_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({
        "id": barn_id, "name": "HL-1A Test Stables",
        "status": status, "_hl1a_test": True,
    })
    return barn_id


def _make_horse(db, barn_id: str, **extras) -> str:
    horse_id = f"horse_hl1a_{uuid.uuid4().hex[:10]}"
    doc = {
        "id": horse_id, "barn_id": barn_id,
        "name": "Test Pony", "breed": "Test Breed",
        "age": 8, "color": "bay", "height_hands": 15.2,
        "discipline": "dressage", "status": "active",
        "stall": "A1",
        # Legacy fields populated to exercise the legacy-envelope path.
        "feed_plan": "Standard ration AM/PM",
        "training_goals": "Second Level",
        "behavior_flags": ["cribs"],
        "allergies": ["dust"],
        "_hl1a_test": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    doc.update(extras)
    db.horses.insert_one(doc)
    return horse_id


def _put_user_in_barn(db, user_id: str, barn_id: str,
                      role: str = "barn_manager") -> None:
    db.users.update_one(
        {"id": user_id},
        {"$set": {"barn_id": barn_id, "role": role, "_hl1a_test": True}},
    )


def _cleanup(db):
    db.users.delete_many({"_hl1a_test": True})
    db.horses.delete_many({"_hl1a_test": True})
    db.barns.delete_many({"_hl1a_test": True})


# ---------------------------------------------------------------------
# 1-9  Read shape + barn scoping + Admin-4b enforcement
# ---------------------------------------------------------------------
def test_get_ledger_returns_composed_profile_for_member(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["horse_id"] == horse_id
        assert body["view"] == "staff"
        assert body["identity"]["name"] == "Test Pony"
        # Legacy envelope wraps the legacy feed_plan string.
        assert body["feeding"]["legacy"] == "Standard ration AM/PM"
        # No structured profile yet → structured=None.
        assert body["feeding"]["structured"] is None
        # Empty placeholders for sub-phases not yet built.
        for k in ("daily_checks_recent", "alerts_open", "audit_recent",
                  "service_providers", "equipment"):
            assert body[k] == [], f"{k} should be [] in 1-A, got {body[k]!r}"
    finally:
        _cleanup(db)


def test_get_ledger_returns_legacy_fields_when_no_structured_profile(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        body = r.json()
        # legacy feed_plan / training_goals / behavior_flags / turnout
        # surface through the envelope.
        assert body["feeding"]["legacy"] == "Standard ration AM/PM"
        assert body["riding_training"]["legacy"] == "Second Level"
        assert body["handling_behavior"]["legacy"] == ["cribs"]
        # Health legacy allergies.
        assert body["health"]["allergies_legacy"] == ["dust"]
    finally:
        _cleanup(db)


def test_get_ledger_returns_safe_empty_sections_for_missing_collections(db):
    """Horse with NO legacy + NO structured fields → 200 + null subs."""
    barn_id = _make_barn(db)
    horse_id = _make_horse(
        db, barn_id,
        feed_plan=None, training_goals=None,
        behavior_flags=None, allergies=None,
    )
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        body = r.json()
        for section in ("feeding", "hay_access", "stall_bedding",
                        "turnout", "handling_behavior", "riding_training"):
            assert body[section] is None, (
                f"{section} should be null when no data exists; got {body[section]!r}"
            )
    finally:
        _cleanup(db)


def test_get_ledger_barn_scoping_404_on_cross_barn_horse(db):
    barn_a = _make_barn(db)
    barn_b = _make_barn(db)
    horse_in_b = _make_horse(db, barn_b)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_a, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_in_b}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 404, r.text
    finally:
        _cleanup(db)


def test_get_ledger_disabled_facility_gate_applies(db):
    """Δ2/§7 guard — if `dependencies=PRODUCT_FACILITY_DEPS` is ever
    removed from the include_router call, this test fails."""
    barn_id = _make_barn(db, status="disabled")
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 403, r.text
        assert "Facility unavailable" in (r.json().get("detail") or "")
    finally:
        _cleanup(db)


def test_platform_admin_in_same_barn_gets_staff_view(db):
    """A platform_admin whose own barn_id matches the horse can read
    the Ledger like any other barn member. No special privilege; just
    barn scoping."""
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    _promote(db, s["user"]["id"], "platform_admin")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        assert r.json()["view"] == "staff"
    finally:
        _cleanup(db)


def test_horse_owner_in_owner_set_gets_owner_view_regardless_of_query_string(db):
    """Δ1 fail-closed: an owner of the horse ALWAYS gets owner view.
    Query string never changes the shape."""
    barn_id = _make_barn(db)
    s = _signup(role="horse_owner")
    horse_id = _make_horse(db, barn_id, owner_id=s["user"]["id"])
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="horse_owner")
    try:
        for q in ("", "?view=owner", "?view=staff",
                  "?view=full", "?view=manager", "?view=admin"):
            r = requests.get(f"{API}/horse-ledger/{horse_id}{q}",
                             headers=_bearer(s), timeout=10)
            assert r.status_code == 200, (q, r.text)
            assert r.json()["view"] == "owner", (
                f"query {q!r} produced view={r.json().get('view')!r}"
            )
    finally:
        _cleanup(db)


def test_get_ledger_returns_404_for_unauthenticated():
    """No bearer → 401 (the existing get_current_user behaviour)."""
    r = requests.get(f"{API}/horse-ledger/anything", timeout=10)
    assert r.status_code in (401, 403), r.text


def test_get_ledger_returns_404_for_nonexistent_horse_id(db):
    barn_id = _make_barn(db)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/horse_does_not_exist_zzz",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 10-14  Owner-filtered shape — fail-closed semantics
# ---------------------------------------------------------------------
def test_owner_view_hides_staff_only_and_behavior_section(db):
    barn_id = _make_barn(db)
    s = _signup(role="horse_owner")
    horse_id = _make_horse(
        db, barn_id, owner_id=s["user"]["id"],
        behavior_flags=["kicks", "food_aggression"],
    )
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="horse_owner")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        body = r.json()
        # Handling/behavior section is entirely hidden in owner view.
        assert body["handling_behavior"] is None, body["handling_behavior"]
    finally:
        _cleanup(db)


def test_owner_view_hides_stall_bedding_section(db):
    """Stall bedding is operations-only — always hidden in owner view."""
    barn_id = _make_barn(db)
    s = _signup(role="horse_owner")
    horse_id = _make_horse(db, barn_id, owner_id=s["user"]["id"])
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="horse_owner")
    # Plant a structured stall_bedding profile so the gate is
    # actually exercised (not just relying on "no data → null").
    db.horse_care_profiles.insert_one({
        "id": f"hcp_{uuid.uuid4().hex[:12]}",
        "horse_id": horse_id, "barn_id": barn_id,
        "stall_bedding": {"bedding_type": "shavings", "bedding_depth_preference": "deep"},
        "_hl1a_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        body = r.json()
        assert body["stall_bedding"] is None
    finally:
        db.horse_care_profiles.delete_many({"_hl1a_test": True})
        _cleanup(db)


def test_owner_view_hides_identity_private_fields(db):
    """microchip / tattoo / registry / required_staff_experience hidden
    in owner view; visible in staff view."""
    barn_id = _make_barn(db)
    owner = _signup(role="horse_owner")
    horse_id = _make_horse(
        db, barn_id, owner_id=owner["user"]["id"],
        microchip_number="985112004444",
        tattoo_number="X9-AB-12",
        required_staff_experience_level="advanced",
    )
    _put_user_in_barn(db, owner["user"]["id"], barn_id, role="horse_owner")
    staff = _signup()
    _put_user_in_barn(db, staff["user"]["id"], barn_id, role="barn_manager")
    try:
        # Owner can NOT see microchip / tattoo / required_staff_experience.
        r1 = requests.get(f"{API}/horse-ledger/{horse_id}",
                          headers=_bearer(owner), timeout=10)
        identity = r1.json()["identity"]
        assert "microchip_number" not in identity, identity
        assert "tattoo_number" not in identity, identity
        assert "required_staff_experience_level" not in identity, identity

        # Staff CAN.
        r2 = requests.get(f"{API}/horse-ledger/{horse_id}",
                          headers=_bearer(staff), timeout=10)
        identity = r2.json()["identity"]
        assert identity.get("microchip_number") == "985112004444"
        assert identity.get("tattoo_number") == "X9-AB-12"
        assert identity.get("required_staff_experience_level") == "advanced"
    finally:
        _cleanup(db)


def test_owner_cannot_read_another_owner_horse_ledger(db):
    barn_id = _make_barn(db)
    owner_a = _signup(role="horse_owner")
    owner_b = _signup(role="horse_owner")
    horse_of_b = _make_horse(db, barn_id, owner_id=owner_b["user"]["id"])
    _put_user_in_barn(db, owner_a["user"]["id"], barn_id, role="horse_owner")
    _put_user_in_barn(db, owner_b["user"]["id"], barn_id, role="horse_owner")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_of_b}",
                         headers=_bearer(owner_a), timeout=10)
        assert r.status_code == 404, r.text
    finally:
        _cleanup(db)


def test_owner_view_shows_owner_safe_health_fields(db):
    barn_id = _make_barn(db)
    owner = _signup(role="horse_owner")
    horse_id = _make_horse(db, barn_id, owner_id=owner["user"]["id"])
    _put_user_in_barn(db, owner["user"]["id"], barn_id, role="horse_owner")
    db.medications.insert_one({
        "id": f"med_{uuid.uuid4().hex[:8]}",
        "horse_id": horse_id, "barn_id": barn_id,
        "name": "Pergolide", "dosage": "1 mg", "frequency": "daily",
        "_hl1a_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(owner), timeout=10)
        assert r.status_code == 200
        meds = r.json()["health"]["medications"]
        assert any(m.get("name") == "Pergolide" for m in meds)
    finally:
        db.medications.delete_many({"_hl1a_test": True})
        _cleanup(db)


# ---------------------------------------------------------------------
# Codex round-1 regressions
# ---------------------------------------------------------------------
def test_r1_owner_view_does_not_expose_legacy_feed_plan_free_text(db):
    """Codex round-1 P1: owner view MUST NOT surface the raw
    `horses.feed_plan` legacy string, which is free text and can
    contain prep instructions, soaking details, medication notes,
    or staff-only handling warnings."""
    barn_id = _make_barn(db)
    owner = _signup(role="horse_owner")
    sensitive = (
        "STAFF ONLY: soak 30 min in warm water. "
        "Give bute 1g in feed AM. "
        "WARNING: bites at handling."
    )
    horse_id = _make_horse(
        db, barn_id, owner_id=owner["user"]["id"],
        feed_plan=sensitive,
    )
    _put_user_in_barn(db, owner["user"]["id"], barn_id, role="horse_owner")
    try:
        # Owner view: legacy free text must NOT appear anywhere.
        ro = requests.get(f"{API}/horse-ledger/{horse_id}",
                          headers=_bearer(owner), timeout=10)
        assert ro.status_code == 200
        for needle in ("STAFF ONLY", "soak 30 min", "Give bute",
                       "WARNING", "bites at handling"):
            assert needle not in ro.text, (
                f"R1 P1: owner view leaked legacy feed_plan text "
                f"({needle!r}) -- payload:\n{ro.text[:600]}"
            )
        # And `feeding.legacy` is explicitly None in the owner envelope
        # when no structured profile exists.
        feeding = ro.json()["feeding"]
        if feeding is not None:
            assert feeding.get("legacy") is None, feeding

        # Staff view: the legacy field IS surfaced (manager can see it).
        staff = _signup()
        _put_user_in_barn(db, staff["user"]["id"], barn_id, role="barn_manager")
        rs = requests.get(f"{API}/horse-ledger/{horse_id}",
                          headers=_bearer(staff), timeout=10)
        assert rs.status_code == 200
        # Staff sees the legacy free-text via the envelope.
        assert "STAFF ONLY" in rs.text, (
            "Staff view must continue to surface legacy feed_plan."
        )
    finally:
        _cleanup(db)


def test_r1_owner_view_wellness_projects_to_safe_allowlist_only(db):
    """Codex round-1 P1: owner view MUST project `wellness_latest`
    to an explicit allowlist of safe fields. Staff-only fields
    (notes, actor fields, internal observations) must not surface."""
    barn_id = _make_barn(db)
    owner = _signup(role="horse_owner")
    horse_id = _make_horse(db, barn_id, owner_id=owner["user"]["id"])
    _put_user_in_barn(db, owner["user"]["id"], barn_id, role="horse_owner")

    wellness_id = f"well_{uuid.uuid4().hex[:8]}"
    secret_strings = {
        "staff_note":         "STAFF ONLY: vet recommended sedation",
        "internal_observation": "INTERNAL: cribbing escalating, recommend muzzle",
        "actor_user_id":      "user_internal_xyz",
        "actor_name":         "Dr Internal",
        "_internal_flag":     True,
        "raw_vet_dictation":  "do not share with owner — possible founder lameness",
    }
    db.wellness.insert_one({
        "id": wellness_id,
        "horse_id": horse_id, "barn_id": barn_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        # owner-safe display fields:
        "status": "good", "score": 8, "summary": "Holding steady this week.",
        # staff-only fields that must NOT leak:
        **secret_strings,
        "_hl1a_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(owner), timeout=10)
        assert r.status_code == 200
        body = r.json()
        wl = body["health"]["wellness_latest"]

        # Allowlist of safe keys only — every other key from the raw doc
        # must be ABSENT in the owner projection.
        assert wl is not None
        assert set(wl.keys()) <= {"id", "created_at", "status", "score", "summary"}, (
            f"owner wellness_latest leaked keys outside the safe allowlist: "
            f"{set(wl.keys())}"
        )
        # Safe display fields ARE present.
        assert wl["id"] == wellness_id
        assert wl["status"] == "good"
        assert wl["summary"] == "Holding steady this week."

        # Staff-only string values must not appear anywhere in the wire payload.
        for secret in secret_strings.values():
            if isinstance(secret, str):
                assert secret not in r.text, (
                    f"R1 P1: owner view leaked wellness staff-only value "
                    f"({secret!r})"
                )

        # Staff view: the full wellness doc is still returned (manager
        # gets operational visibility).
        staff = _signup()
        _put_user_in_barn(db, staff["user"]["id"], barn_id, role="barn_manager")
        rs = requests.get(f"{API}/horse-ledger/{horse_id}",
                          headers=_bearer(staff), timeout=10)
        assert rs.status_code == 200
        assert "STAFF ONLY" in rs.text, (
            "staff view should continue to see the full wellness doc"
        )
    finally:
        db.wellness.delete_many({"_hl1a_test": True})
        _cleanup(db)


# ---------------------------------------------------------------------
# 15-16  No Stripe leak / no billing keys
# ---------------------------------------------------------------------
def test_no_stripe_shaped_string_leaks_in_any_response(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(
        db, barn_id,
        feed_plan="Migrated from sub_TESTleakABCDEF12345 last cycle",
        training_goals="Per cus_TESTleakABCDEF12345 program",
        emergency_notes="See pi_TESTleakABCDEF12345 receipts",
    )
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        assert not _STRIPE_LEAK_RE.search(r.text), r.text[:600]
        # Non-Stripe text survives the scrub.
        assert "Migrated from" in r.text
    finally:
        _cleanup(db)


def test_no_billing_words_in_endpoint_response(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        body = r.json()

        def _walk_keys(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    yield k
                    yield from _walk_keys(v)
            elif isinstance(o, list):
                for v in o:
                    yield from _walk_keys(v)
        keys = set(_walk_keys(body))
        bad = keys & _BILLING_KEYS
        assert not bad, f"billing-adjacent keys leaked: {bad}"
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 17-20  Adjacent phases not touched
# ---------------------------------------------------------------------
def test_phase_9_collections_not_touched_by_ledger_read(db):
    """A ledger read must not insert/update/delete any Phase 9 doc."""
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    counts_before = {
        c: db[c].count_documents({}) for c in
        ("invoices", "recurring_charges", "recurring_billing_rules")
    }
    try:
        for _ in range(3):
            r = requests.get(f"{API}/horse-ledger/{horse_id}",
                             headers=_bearer(s), timeout=10)
            assert r.status_code == 200
        counts_after = {
            c: db[c].count_documents({}) for c in counts_before
        }
        assert counts_after == counts_before, (counts_before, counts_after)
    finally:
        _cleanup(db)


def test_phase_15_collections_not_touched_by_ledger_read(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    counts_before = {
        c: db[c].count_documents({}) for c in
        ("subscriptions", "subscription_invoices", "subscription_email_log",
         "payment_transactions", "payments", "billing_events")
    }
    try:
        for _ in range(3):
            requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        counts_after = {
            c: db[c].count_documents({}) for c in counts_before
        }
        assert counts_after == counts_before
    finally:
        _cleanup(db)


def test_admin_portal_routes_unchanged(db):
    """Route-lock regression - Admin-portal surface is locked at 39
    endpoints after HorseOps-1G added the platform inspection reads."""
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 28
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1


def test_no_writes_in_1a_endpoints_only():
    """1-B added writes on the mutation endpoints, but the GET endpoint
    handler (and its composed-read helpers) must remain write-free.
    AST-checks only the GET handler body."""
    src = (ROOT / "backend" / "routes" / "horse_ledger.py").read_text()
    tree = ast.parse(src)
    bad_methods = (
        "insert_one", "insert_many", "update_one", "update_many",
        "delete_one", "delete_many", "replace_one",
        "find_one_and_update", "find_one_and_delete",
        "find_one_and_replace", "bulk_write",
    )
    bad: list[str] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.AsyncFunctionDef)
                and node.name == "get_horse_ledger"):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Attribute) and sub.attr in bad_methods:
                    bad.append(f"{ast.unparse(sub)} @ line {sub.lineno}")
    assert not bad, (
        "GET /horse-ledger/{horse_id} must be read-only:\n  "
        + "\n  ".join(bad)
    )


# ---------------------------------------------------------------------
# 21  horses row unchanged after read
# ---------------------------------------------------------------------
def test_horse_legacy_fields_unchanged_after_read(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    try:
        before = dict(db.horses.find_one({"id": horse_id}))
        for _ in range(3):
            requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        after = dict(db.horses.find_one({"id": horse_id}))
        assert before == after, (before, after)
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 22  All 15 HorseOps-1A indexes exist
# ---------------------------------------------------------------------
def test_horse_ledger_indexes_created_on_startup(db):
    expected = {
        "horse_care_profiles":          {"horse_id_1", "barn_id_1"},
        "horse_equipment":              {"horse_id_1", "barn_id_1_category_1"},
        "service_providers":            {"barn_id_1_category_1"},
        "horse_provider_assignments":   {"horse_id_1", "barn_id_1_next_due_date_1"},
        # Phase 1-C aligned indexes (was `check_time` in the 1-A plan,
        # now `checked_at` to match the live write/query field name).
        "horse_daily_check_logs":       {"hdcl_horse_checked_at",
                                          "hdcl_barn_horse_checked_at",
                                          "hdcl_barn_check_type_checked_at",
                                          "hdcl_task_id"},
        "horse_ledger_alerts":          {"horse_id_1_opened_at_-1",
                                          "barn_id_1_severity_1_closed_at_1"},
        "horse_owner_visibility_policy": {"horse_id_1"},
        "horse_ledger_audit":           {"horse_id_1_ts_-1",
                                          "barn_id_1_ts_-1",
                                          "actor_user_id_1_ts_-1"},
    }
    missing = []
    for coll, names in expected.items():
        idx = set(db[coll].index_information().keys()) - {"_id_"}
        for n in names:
            if n not in idx:
                missing.append(f"{coll}::{n}  (have: {sorted(idx)})")
    assert not missing, "Missing HorseOps-1A indexes:\n  " + "\n  ".join(missing)


# ---------------------------------------------------------------------
# 23  inventory / vendor / payment_profiles untouched
# ---------------------------------------------------------------------
def test_no_inventory_or_vendor_collections_touched(db):
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="barn_manager")
    cols = ("inventory", "service_requests", "staff_invites", "payment_profiles")
    before = {c: db[c].count_documents({}) for c in cols}
    try:
        for _ in range(3):
            requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        after = {c: db[c].count_documents({}) for c in cols}
        assert after == before
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 24-25  Fail-closed: horse_owner without ?view=owner still owner-filtered;
#                     horse_owner cannot force staff view by query string.
# ---------------------------------------------------------------------
def test_horse_owner_without_view_param_still_gets_owner_filtered_view(db):
    barn_id = _make_barn(db)
    s = _signup(role="horse_owner")
    horse_id = _make_horse(
        db, barn_id, owner_id=s["user"]["id"],
        microchip_number="985112004444",
        behavior_flags=["kicks"],
    )
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="horse_owner")
    try:
        # No query string at all.
        r = requests.get(f"{API}/horse-ledger/{horse_id}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        body = r.json()
        assert body["view"] == "owner"
        # Owner-private identity fields still hidden.
        assert "microchip_number" not in body["identity"]
        # Behavior section still hidden.
        assert body["handling_behavior"] is None
    finally:
        _cleanup(db)


def test_horse_owner_cannot_force_staff_view(db):
    """Δ1 fail-closed regression — every documented escalation
    attempt via query string is silently downgraded."""
    barn_id = _make_barn(db)
    s = _signup(role="horse_owner")
    horse_id = _make_horse(db, barn_id, owner_id=s["user"]["id"],
                           microchip_number="985112004444")
    _put_user_in_barn(db, s["user"]["id"], barn_id, role="horse_owner")
    try:
        for q in ("?view=staff", "?view=full", "?view=manager",
                  "?view=admin", "?view=STAFF", "?view=",
                  "?view=staff&view=owner",
                  "?notreal=1&view=staff"):
            r = requests.get(f"{API}/horse-ledger/{horse_id}{q}",
                             headers=_bearer(s), timeout=10)
            assert r.status_code == 200, (q, r.text)
            body = r.json()
            assert body["view"] == "owner", q
            assert "microchip_number" not in body["identity"], q
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 26  Platform-role cannot cross-barn-inspect via this product route
# ---------------------------------------------------------------------
def test_platform_role_cannot_use_product_route_for_cross_barn_horse_in_1a(db):
    """Δ2 — the Admin-4b platform-role bypass is for the disabled-
    facility GATE only. Barn scoping on the product route is NOT
    bypassed by a platform_admin."""
    barn_a = _make_barn(db)
    barn_b = _make_barn(db)
    horse_in_b = _make_horse(db, barn_b)
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], barn_a, role="barn_manager")
    _promote(db, s["user"]["id"], "platform_admin")
    try:
        r = requests.get(f"{API}/horse-ledger/{horse_in_b}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 404, (
            f"platform_admin must not cross-barn-inspect via the "
            f"product route; got {r.status_code} body={r.text}"
        )
    finally:
        _cleanup(db)


# ---------------------------------------------------------------------
# 27  Index creation must not write any documents
# ---------------------------------------------------------------------
def test_no_documents_written_to_horse_ledger_collections_in_1a(db):
    """The 8 new collections may exist (empty) as a Mongo side-effect
    of index creation. 1-A may NOT write any documents into them."""
    eight = (
        "horse_care_profiles", "horse_equipment", "service_providers",
        "horse_provider_assignments", "horse_daily_check_logs",
        "horse_ledger_alerts", "horse_owner_visibility_policy",
        "horse_ledger_audit",
    )
    before = {c: db[c].count_documents({"_hl1a_test": {"$ne": True}})
              for c in eight}
    # Exercise the full 1-A read flow.
    barn_id = _make_barn(db)
    horse_id = _make_horse(db, barn_id)
    owner = _signup(role="horse_owner")
    horse_for_owner = _make_horse(db, barn_id, owner_id=owner["user"]["id"])
    _put_user_in_barn(db, owner["user"]["id"], barn_id, role="horse_owner")
    staff = _signup()
    _put_user_in_barn(db, staff["user"]["id"], barn_id, role="barn_manager")
    try:
        for hid, sess in (
            (horse_id, staff),
            (horse_for_owner, owner),
            ("nonexistent_id_zzz", staff),
        ):
            requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(sess), timeout=10)
        after = {c: db[c].count_documents({"_hl1a_test": {"$ne": True}})
                 for c in eight}
        assert after == before, (
            f"HorseOps-1A wrote into a Ledger collection: {after} vs {before}"
        )
    finally:
        _cleanup(db)
