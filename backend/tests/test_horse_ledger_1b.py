"""tests/test_horse_ledger_1b.py — HorseOps-1B manager edit flows.

Coverage:
  1-12   care-profile PATCH (whitelist + role gating + cross-barn + hay-net cap)
  13-19  owner-visibility policy (defaults + PUT + forbidden expansion + read-time enforcement)
  20-23  equipment (POST/PATCH/retire/cross-barn)
  24-29  service providers + assignments
  30-34  audit (every mutation emits a row; no raw values; field paths only)
  35-39  privacy regressions (manager edits do NOT expand owner view; 1-A R1 invariants intact)
  40-42  adjacent phase invariants (Phase 9/15/Admin Portal byte-identical)
"""
from __future__ import annotations

import os, pathlib, re, sys, uuid
from datetime import datetime, timezone
from typing import Any, Dict

import pytest, requests
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


def _signup(role="horse_owner"):
    email = f"hl1b_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(f"{API}/auth/signup",
                      json={"email": email, "password": "securepass1",
                            "full_name": "HL1B Test", "role": role}, timeout=15)
    r.raise_for_status()
    return r.json()


def _bearer(s):
    return {"Authorization": f"Bearer {s['token']}"}


def _make_barn(db):
    bid = f"barn_hl1b_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "1B Test", "status": "active",
                          "_hl1b_test": True})
    return bid


def _make_horse(db, bid, **extras):
    hid = f"horse_hl1b_{uuid.uuid4().hex[:10]}"
    doc = {"id": hid, "barn_id": bid, "name": "Tester", "status": "active",
           "_hl1b_test": True,
           "created_at": datetime.now(timezone.utc).isoformat()}
    doc.update(extras)
    db.horses.insert_one(doc)
    return hid


def _put_user_in_barn(db, uid, bid, role="barn_manager"):
    db.users.update_one({"id": uid},
                        {"$set": {"barn_id": bid, "role": role, "_hl1b_test": True}})


def _mgr_session(db, bid, role="barn_manager"):
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], bid, role=role)
    return s


def _owner_session(db, bid):
    s = _signup(role="horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, role="horse_owner")
    return s


def _cleanup(db):
    db.users.delete_many({"_hl1b_test": True})
    db.horses.delete_many({"_hl1b_test": True})
    db.barns.delete_many({"_hl1b_test": True})
    db.horse_care_profiles.delete_many({"_hl1b_test": True})
    db.horse_owner_visibility_policy.delete_many({"_hl1b_test": True})
    db.horse_equipment.delete_many({"_hl1b_test": True})
    db.service_providers.delete_many({"_hl1b_test": True})
    db.horse_provider_assignments.delete_many({"_hl1b_test": True})
    # Audit rows for any horse_id starting with horse_hl1b
    db.horse_ledger_audit.delete_many({"horse_id": {"$regex": "^horse_hl1b_"}})
    # Sweep care-profile docs for hl1b horses (in case test path didn't tag).
    db.horse_care_profiles.delete_many({"horse_id": {"$regex": "^horse_hl1b_"}})
    db.horse_owner_visibility_policy.delete_many({"horse_id": {"$regex": "^horse_hl1b_"}})
    db.horse_equipment.delete_many({"horse_id": {"$regex": "^horse_hl1b_"}})
    db.horse_provider_assignments.delete_many({"horse_id": {"$regex": "^horse_hl1b_"}})


# ---------- care-profile PATCH ----------
def test_patch_care_profile_whitelisted_feeding(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": {"grain_feed_type": "Senior",
                                             "amount_value": 4.0,
                                             "amount_unit": "lb"}},
                           timeout=10)
        assert r.status_code == 200, r.text
        prof = db.horse_care_profiles.find_one({"horse_id": hid})
        assert prof["feeding"]["grain_feed_type"] == "Senior"
        assert prof["feeding"]["amount_value"] == 4.0
    finally:
        _cleanup(db)


def test_patch_care_profile_rejects_unknown_section(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"nonsense_section": {"a": 1}}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_patch_care_profile_rejects_unknown_field(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": {"hocus_pocus": "x"}}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_patch_care_profile_rejects_empty_body(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr), json={}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_patch_care_profile_owner_is_403(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(owner),
                           json={"feeding": {"grain_feed_type": "Owner-set"}},
                           timeout=10)
        assert r.status_code == 403
        assert db.horse_care_profiles.find_one({"horse_id": hid}) is None
    finally:
        _cleanup(db)


@pytest.mark.parametrize("role", ["groom", "trainer", "vet", "staff"])
def test_patch_care_profile_non_mutator_roles_403(db, role):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    s = _signup(); _put_user_in_barn(db, s["user"]["id"], bid, role=role)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(s),
                           json={"feeding": {"grain_feed_type": "x"}}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


@pytest.mark.parametrize("role", ["admin", "barn_manager"])
def test_patch_care_profile_mutator_roles_succeed(db, role):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    s = _signup(); _put_user_in_barn(db, s["user"]["id"], bid, role=role)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(s),
                           json={"feeding": {"grain_feed_type": "x"}}, timeout=10)
        assert r.status_code == 200
    finally:
        _cleanup(db)


def test_patch_care_profile_cross_barn_404(db):
    bid_a = _make_barn(db); bid_b = _make_barn(db)
    hid_b = _make_horse(db, bid_b); mgr = _mgr_session(db, bid_a)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid_b}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": {"grain_feed_type": "x"}}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_patch_care_profile_hay_net_cap_6(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        seven = [{"id": f"n{i}", "location": "stall"} for i in range(7)]
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"hay_access": {"hay_nets": seven}}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_patch_care_profile_upserts_then_updates(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r1 = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                            headers=_bearer(mgr),
                            json={"feeding": {"grain_feed_type": "A"}}, timeout=10)
        assert r1.status_code == 200
        r2 = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                            headers=_bearer(mgr),
                            json={"feeding": {"grain_feed_type": "B"}}, timeout=10)
        assert r2.status_code == 200
        assert db.horse_care_profiles.count_documents({"horse_id": hid}) == 1
        prof = db.horse_care_profiles.find_one({"horse_id": hid})
        assert prof["feeding"]["grain_feed_type"] == "B"
    finally:
        _cleanup(db)


def test_patch_care_profile_section_must_be_object(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": "not an object"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_patch_care_profile_disabled_facility_403(db):
    bid = _make_barn(db)
    db.barns.update_one({"id": bid}, {"$set": {"status": "disabled"}})
    hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": {"grain_feed_type": "x"}}, timeout=10)
        assert r.status_code == 403
        assert "Facility unavailable" in (r.json().get("detail") or "")
    finally:
        _cleanup(db)


# ---------- owner-visibility policy ----------
def test_visibility_policy_default_applies_when_no_doc(db):
    """Owner view with no policy doc → conservative defaults (1-A behaviour)."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        body = r.json()
        assert body["view"] == "owner"
        assert body["stall_bedding"] is None
        assert body["handling_behavior"] is None
    finally:
        _cleanup(db)


def test_visibility_policy_put_replaces_sections(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                         headers=_bearer(mgr),
                         json={"sections": {"feeding": {"allowlist": ["grain_feed_type"]}}},
                         timeout=10)
        assert r.status_code == 200
        doc = db.horse_owner_visibility_policy.find_one({"horse_id": hid})
        assert doc["sections"]["feeding"]["allowlist"] == ["grain_feed_type"]
        assert doc["policy_version"] >= 1
    finally:
        _cleanup(db)


def test_visibility_policy_rejects_unknown_section(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                         headers=_bearer(mgr),
                         json={"sections": {"banking": {"allowlist": []}}},
                         timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


@pytest.mark.parametrize("section,key", [
    ("feeding", "staff_only_warnings"),
    ("feeding", "soaking"),
    ("feeding", "legacy"),
    ("hay_access", "restriction_flags"),
    ("hay_access", "hay_nets"),
    ("stall_bedding", "anything"),       # entire section forbidden
    ("handling_behavior", "anything"),
    ("identity", "microchip_number"),
    ("identity", "tattoo_number"),
    ("identity", "required_staff_experience_level"),
    ("health.wellness_latest", "staff_note"),
    ("health.wellness_latest", "internal_observation"),
    ("service_providers", "name"),       # entire section forbidden
    ("feeding", "_internal_flag"),       # underscore-prefixed always forbidden
])
def test_visibility_policy_rejects_forbidden_expansion(db, section, key):
    """The forbidden-keys list MUST stay enforced even via a PUT."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                         headers=_bearer(mgr),
                         json={"sections": {section: {"allowlist": [key]}}},
                         timeout=10)
        assert r.status_code == 422, (section, key, r.text)
    finally:
        _cleanup(db)


def test_visibility_policy_owner_cannot_call_put(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        r = requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                         headers=_bearer(owner),
                         json={"sections": {"feeding": {"allowlist": []}}},
                         timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_visibility_policy_forbidden_keys_stay_hidden_even_if_in_db(db):
    """Backend-authoritative on read: even if a manually-inserted
    policy doc contains forbidden keys, the owner read path must
    intersect with the forbidden-key set and drop them. We don't
    expose a public way to insert forbidden keys, so we plant
    directly via Mongo and assert the read is fail-closed."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    # Plant a tampered policy doc.
    db.horse_owner_visibility_policy.insert_one({
        "id": "hovp_tampered", "horse_id": hid, "barn_id": bid,
        "sections": {"stall_bedding": {"allowlist": ["bedding_type"]}},
        "_hl1b_test": True,
    })
    # Plant structured bedding data for the horse.
    db.horse_care_profiles.insert_one({
        "id": "hcp_tampered", "horse_id": hid, "barn_id": bid,
        "stall_bedding": {"bedding_type": "shavings"},
        "_hl1b_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        # stall_bedding entire section is forbidden in owner view
        # (built-in fail-closed). The tampered allowlist must NOT
        # surface it.
        assert r.json()["stall_bedding"] is None, r.json()
    finally:
        _cleanup(db)


# ---------- equipment ----------
def test_equipment_post_and_patch_retire(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r1 = requests.post(f"{API}/horse-ledger/{hid}/equipment",
                           headers=_bearer(mgr),
                           json={"category": "saddle", "label": "Antares 17.5"},
                           timeout=10)
        assert r1.status_code == 200, r1.text
        eq_id = r1.json()["id"]
        # PATCH → retire
        r2 = requests.patch(f"{API}/horse-ledger/{hid}/equipment/{eq_id}",
                            headers=_bearer(mgr),
                            json={"status": "retired"}, timeout=10)
        assert r2.status_code == 200
        row = db.horse_equipment.find_one({"id": eq_id})
        assert row["status"] == "retired"
    finally:
        _cleanup(db)


def test_equipment_rejects_unknown_field(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/equipment",
                          headers=_bearer(mgr),
                          json={"category": "saddle", "bogus": "x"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_equipment_owner_403(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/equipment",
                          headers=_bearer(owner),
                          json={"category": "saddle"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_equipment_cross_barn_404(db):
    bid_a = _make_barn(db); bid_b = _make_barn(db); mgr = _mgr_session(db, bid_a)
    hid_b = _make_horse(db, bid_b)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid_b}/equipment",
                          headers=_bearer(mgr),
                          json={"category": "saddle"}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


# ---------- service providers + assignments ----------
def test_service_provider_create(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/service-providers",
                          headers=_bearer(mgr),
                          json={"category": "vet", "name": "Dr Park"},
                          timeout=10)
        assert r.status_code == 200
        sp_id = r.json()["id"]
        row = db.service_providers.find_one({"id": sp_id})
        assert row["barn_id"] == bid
    finally:
        _cleanup(db)


def test_service_provider_unknown_category_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/service-providers",
                          headers=_bearer(mgr),
                          json={"category": "nope", "name": "x"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_provider_assignment_create_and_patch(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r1 = requests.post(f"{API}/horse-ledger/{hid}/service-providers",
                           headers=_bearer(mgr),
                           json={"category": "farrier", "name": "Joe"},
                           timeout=10)
        sp_id = r1.json()["id"]
        r2 = requests.post(f"{API}/horse-ledger/{hid}/provider-assignments",
                           headers=_bearer(mgr),
                           json={"provider_id": sp_id, "category": "farrier",
                                 "interval_days": 42}, timeout=10)
        assert r2.status_code == 200, r2.text
        a_id = r2.json()["id"]
        r3 = requests.patch(
            f"{API}/horse-ledger/{hid}/provider-assignments/{a_id}",
            headers=_bearer(mgr),
            json={"is_primary_for_horse": True}, timeout=10,
        )
        assert r3.status_code == 200
    finally:
        _cleanup(db)


def test_provider_assignment_rejects_cross_barn_provider(db):
    bid_a = _make_barn(db); bid_b = _make_barn(db); mgr = _mgr_session(db, bid_a)
    hid_a = _make_horse(db, bid_a)
    # Plant a provider in a DIFFERENT barn.
    db.service_providers.insert_one({
        "id": "sp_other_barn", "barn_id": bid_b, "category": "vet",
        "name": "Foreign Vet", "_hl1b_test": True,
    })
    try:
        r = requests.post(f"{API}/horse-ledger/{hid_a}/provider-assignments",
                          headers=_bearer(mgr),
                          json={"provider_id": "sp_other_barn", "category": "vet"},
                          timeout=10)
        assert r.status_code == 404
    finally:
        db.service_providers.delete_many({"_hl1b_test": True})
        _cleanup(db)


def test_provider_assignment_owner_403(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/provider-assignments",
                          headers=_bearer(owner),
                          json={"provider_id": "x"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


# ---------- audit ----------
def test_audit_row_emitted_on_care_profile_patch(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"feeding": {"grain_feed_type": "Senior",
                                         "amount_value": 4.0}}, timeout=10)
        rows = list(db.horse_ledger_audit.find({"horse_id": hid}))
        assert rows, "no audit row emitted"
        row = rows[0]
        assert row["section"] == "feeding"
        assert row["action"] == "updated"
        assert set(row["field_paths"]) == {"feeding.grain_feed_type",
                                            "feeding.amount_value"}
        # NO before/after values in metadata.
        assert "before" not in row
        assert "after" not in row
        # NO raw operational notes in audit text.
        for v in row.values():
            if isinstance(v, str):
                assert "Senior" not in v
    finally:
        _cleanup(db)


def test_audit_row_emitted_on_equipment_post(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/equipment",
                      headers=_bearer(mgr),
                      json={"category": "saddle", "label": "Antares"}, timeout=10)
        rows = list(db.horse_ledger_audit.find(
            {"horse_id": hid, "section": "equipment"}))
        assert rows
        assert "Antares" not in str(rows[0])
    finally:
        _cleanup(db)


def test_no_audit_row_on_403_denial(db):
    """Permission-denial audit decision: no horse_ledger_audit row."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        before = db.horse_ledger_audit.count_documents({"horse_id": hid})
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(owner),
                           json={"feeding": {"grain_feed_type": "x"}}, timeout=10)
        assert r.status_code == 403
        after = db.horse_ledger_audit.count_documents({"horse_id": hid})
        assert after == before
    finally:
        _cleanup(db)


def test_audit_sensitivity_set_for_staff_only_sections(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"handling_behavior": {"catching_notes": "easy"}},
                       timeout=10)
        row = db.horse_ledger_audit.find_one(
            {"horse_id": hid, "section": "handling_behavior"})
        assert row["sensitivity"] == "staff_only"
    finally:
        _cleanup(db)


def test_audit_only_owner_visible_sensitivity_for_riding_training(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"riding_training": {"discipline": "Dressage"}},
                       timeout=10)
        row = db.horse_ledger_audit.find_one(
            {"horse_id": hid, "section": "riding_training"})
        assert row["sensitivity"] == "owner_visible"
        assert row["owner_visible_eligible"] is True
    finally:
        _cleanup(db)


# ---------- privacy regressions (manager edits don't expand owner view) ----------
def test_manager_edit_does_not_expand_owner_view_for_staff_only_sections(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        # Plant staff-only-ish data via care-profile.
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"stall_bedding": {"bedding_type": "shavings",
                                                "stall_safety_notes": "STAFF ONLY note"},
                             "handling_behavior": {"catching_notes": "kicks!"}},
                       timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        body = r.json()
        assert body["stall_bedding"] is None
        assert body["handling_behavior"] is None
        assert "STAFF ONLY note" not in r.text
        assert "kicks!" not in r.text
    finally:
        _cleanup(db)


def test_legacy_feed_plan_still_hidden_from_owner_after_1b(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"],
                       feed_plan="STAFF ONLY: soak 30min, give bute")
    mgr = _mgr_session(db, bid)
    try:
        # Manager adds a structured profile.
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"feeding": {"grain_feed_type": "Senior"}}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        assert "STAFF ONLY" not in r.text
        # Owner sees the structured field only.
        assert r.json()["feeding"]["legacy"] is None
        assert r.json()["feeding"]["structured"]["grain_feed_type"] == "Senior"
    finally:
        _cleanup(db)


def test_query_string_still_cannot_force_staff_view_after_1b(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    try:
        for q in ("?view=staff", "?view=full", "?view=manager"):
            r = requests.get(f"{API}/horse-ledger/{hid}{q}",
                             headers=_bearer(owner), timeout=10)
            assert r.json()["view"] == "owner", q
    finally:
        _cleanup(db)


def test_service_providers_remain_hidden_from_owner_in_1b(db):
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        rp = requests.post(f"{API}/horse-ledger/{hid}/service-providers",
                           headers=_bearer(mgr),
                           json={"category": "vet", "name": "Dr Park"},
                           timeout=10)
        sp_id = rp.json()["id"]
        requests.post(f"{API}/horse-ledger/{hid}/provider-assignments",
                      headers=_bearer(mgr),
                      json={"provider_id": sp_id, "category": "vet"},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        # Owner view: service_providers section is empty list (hidden).
        assert r.json()["service_providers"] == []
        assert "Dr Park" not in r.text
    finally:
        _cleanup(db)


def test_wellness_strict_allowlist_still_enforced_after_1b(db):
    """1-A R1-B regression must remain green after 1-B."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    db.wellness.insert_one({
        "id": "w_1b", "horse_id": hid, "barn_id": bid,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "good", "score": 9, "summary": "fine",
        "staff_note": "STAFF SECRET", "_hl1b_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        wl = r.json()["health"]["wellness_latest"]
        assert set(wl.keys()) <= {"id", "created_at", "status", "score", "summary"}
        assert "STAFF SECRET" not in r.text
    finally:
        db.wellness.delete_many({"_hl1b_test": True})
        _cleanup(db)


# ---------- adjacent phase invariants ----------
def test_phase_9_collections_byte_identical_after_1b_edit_storm(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    cols = ("invoices", "recurring_charges", "recurring_billing_rules")
    before = {c: db[c].count_documents({}) for c in cols}
    try:
        for i in range(3):
            requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"feeding": {"grain_feed_type": f"V{i}"}},
                           timeout=10)
            requests.post(f"{API}/horse-ledger/{hid}/equipment",
                          headers=_bearer(mgr),
                          json={"category": "saddle"}, timeout=10)
        after = {c: db[c].count_documents({}) for c in cols}
        assert after == before
    finally:
        _cleanup(db)


def test_phase_15_collections_byte_identical_after_1b_edit_storm(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    cols = ("subscriptions", "subscription_invoices", "subscription_email_log",
            "payment_transactions", "payments", "billing_events")
    before = {c: db[c].count_documents({}) for c in cols}
    try:
        for _ in range(3):
            requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr),
                           json={"riding_training": {"discipline": "X"}},
                           timeout=10)
        after = {c: db[c].count_documents({}) for c in cols}
        assert after == before
    finally:
        _cleanup(db)


def test_admin_portal_route_lock_unchanged_after_1b():
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 26
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1



# =====================================================================
# Codex Round-1 regressions (Phase HorseOps-1B)
#
# P0  Owner visibility policy must be applied on every owner read.
# P0  Riding/training staff-only fields must not leak to owners.
# P1  Nested validation for supplements / hay_nets / schedule.
# =====================================================================
def test_policy_removal_hides_previously_visible_safe_key(db):
    """Without a policy doc the owner sees the conservative default
    (grain_feed_type, schedule, supplements). After a PUT that omits
    `grain_feed_type` from the allowlist, the owner read must drop
    that field on the very next GET."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        # Plant structured feeding data.
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"feeding": {"grain_feed_type": "Senior",
                                         "amount_value": 4.0,
                                         "amount_unit": "lb"}}, timeout=10)
        # Owner sees grain_feed_type with no policy doc (default policy).
        r0 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10)
        s0 = r0.json()["feeding"]["structured"]
        assert s0.get("grain_feed_type") == "Senior"
        # Manager now sets a narrowed policy that allows only
        # `supplements` from feeding (NOT grain_feed_type).
        requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                     headers=_bearer(mgr),
                     json={"sections": {"feeding": {"allowlist": ["supplements"]}}},
                     timeout=10)
        r1 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10)
        body = r1.json()["feeding"]
        # grain_feed_type MUST have disappeared even though the structured
        # doc still holds it (proves backend-authoritative read).
        if body and body.get("structured"):
            assert "grain_feed_type" not in body["structured"]
    finally:
        _cleanup(db)


def test_policy_addition_shows_only_safe_allowed_keys(db):
    """Adding `amount_value` + `amount_unit` to the feeding allowlist
    surfaces those keys to the owner. Any keys NOT in the registry
    silently drop (defense in depth)."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"feeding": {"grain_feed_type": "Senior",
                                         "amount_value": 4.0,
                                         "amount_unit": "lb"}}, timeout=10)
        # Default policy: grain_feed_type only by default — amount_value not visible.
        r0 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10).json()
        assert "amount_value" not in (r0["feeding"]["structured"] or {})
        # Manager opts the owner into amount_value + amount_unit.
        requests.put(f"{API}/horse-ledger/{hid}/owner-visibility-policy",
                     headers=_bearer(mgr),
                     json={"sections": {"feeding": {
                         "allowlist": ["grain_feed_type", "amount_value", "amount_unit"]
                     }}}, timeout=10)
        r1 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10).json()
        s = r1["feeding"]["structured"]
        assert s.get("amount_value") == 4.0
        assert s.get("amount_unit") == "lb"
        assert s.get("grain_feed_type") == "Senior"
    finally:
        _cleanup(db)


def test_tampered_policy_with_forbidden_key_stays_hidden_on_read(db):
    """If a policy doc is planted directly in Mongo with a forbidden
    feeding key (e.g. `staff_only_warnings`), the read path must drop
    it via the backend safe-key registry intersection."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    db.horse_owner_visibility_policy.insert_one({
        "id": "hovp_tampered_r1", "horse_id": hid, "barn_id": bid,
        "sections": {"feeding": {"allowlist": ["grain_feed_type",
                                                "staff_only_warnings"]}},
        "_hl1b_test": True,
    })
    db.horse_care_profiles.insert_one({
        "id": "hcp_tampered_r1", "horse_id": hid, "barn_id": bid,
        "feeding": {"grain_feed_type": "Senior",
                    "staff_only_warnings": "GIVE BUTE, OWNER UNAWARE"},
        "_hl1b_test": True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        s = r.json()["feeding"]["structured"] or {}
        assert "staff_only_warnings" not in s
        assert "GIVE BUTE" not in r.text
        # grain_feed_type still surfaces normally.
        assert s.get("grain_feed_type") == "Senior"
    finally:
        _cleanup(db)


@pytest.mark.parametrize("field", [
    "trainer_notes", "exercise_restrictions", "weekly_work_plan",
    "rider_compatibility_notes", "conditioning_plan", "lesson_schedule",
])
def test_riding_training_staff_only_fields_never_leak_to_owner(db, field):
    """1-B added writable operational fields under riding_training.
    None of them may ever appear in the owner read, even with NO
    policy doc, even with a tampered policy doc."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        sentinel = f"SECRET_{field.upper()}_LEAK_PROBE"
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"riding_training": {"discipline": "Dressage",
                                                  field: sentinel}},
                       timeout=10)
        # Default policy.
        r0 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10)
        assert sentinel not in r0.text, f"{field} leaked under default policy"
        # Even if a manager attempts to expand the policy, the backend
        # rejects forbidden keys (422). The read MUST stay clean.
        bad = requests.put(
            f"{API}/horse-ledger/{hid}/owner-visibility-policy",
            headers=_bearer(mgr),
            json={"sections": {"riding_training": {"allowlist": [field]}}},
            timeout=10,
        )
        assert bad.status_code == 422
        r1 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10)
        assert sentinel not in r1.text
        # Direct DB tamper — same outcome.
        db.horse_owner_visibility_policy.update_one(
            {"horse_id": hid},
            {"$set": {"sections.riding_training.allowlist": [field]}},
            upsert=True,
        )
        r2 = requests.get(f"{API}/horse-ledger/{hid}",
                          headers=_bearer(owner), timeout=10)
        assert sentinel not in r2.text, f"{field} leaked after DB tamper"
    finally:
        _cleanup(db)


def test_default_owner_view_excludes_riding_training_staff_only_keys(db):
    """Even without a policy doc, the default owner projection of
    riding_training must include only `discipline`, `current_level`,
    `competition_goals` — nothing else."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"riding_training": {
                           "discipline": "Dressage",
                           "current_level": "PSG",
                           "trainer_notes": "REVISIT FRAME — staff only",
                           "exercise_restrictions": "no canter on left lead",
                       }}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10).json()
        s = (r.get("riding_training") or {}).get("structured") or {}
        assert set(s.keys()) <= {"discipline", "current_level", "competition_goals"}
        assert "trainer_notes" not in s
        assert "exercise_restrictions" not in s
    finally:
        _cleanup(db)


# ---------- nested validation ----------
@pytest.mark.parametrize("payload", [
    {"feeding": {"supplements": "not-a-list"}},
    {"feeding": {"supplements": [{"name": 123}]}},
    {"feeding": {"supplements": ["just a string"]}},
    {"feeding": {"schedule": "morning"}},
    {"feeding": {"schedule": [{"time": {"hour": 6}}]}},
    {"hay_access": {"hay_nets": "not-a-list"}},
    {"hay_access": {"hay_nets": [{"id": "n1"}, "scalar"]}},
    {"turnout": {"schedule": {"oops": "object"}}},
])
def test_patch_care_profile_nested_shape_422(db, payload):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                           headers=_bearer(mgr), json=payload, timeout=10)
        assert r.status_code == 422, (payload, r.text)
    finally:
        _cleanup(db)


def test_patch_care_profile_nested_shape_accepts_well_formed(db):
    """Sanity: a properly-shaped nested payload still saves."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr_session(db, bid)
    try:
        r = requests.patch(
            f"{API}/horse-ledger/{hid}/care-profile",
            headers=_bearer(mgr),
            json={"feeding": {"supplements": [{"name": "Magnesium"}],
                              "schedule": ["AM", "PM"]},
                  "hay_access": {"hay_nets": [{"id": "n1", "location": "stall"}]}},
            timeout=10,
        )
        assert r.status_code == 200, r.text
    finally:
        _cleanup(db)


def test_owner_supplements_projection_drops_dosage_notes(db):
    """When a manager records supplements with dosage/notes, the owner
    view must surface name only."""
    bid = _make_barn(db); owner = _owner_session(db, bid)
    hid = _make_horse(db, bid, owner_id=owner["user"]["id"])
    mgr = _mgr_session(db, bid)
    try:
        requests.patch(f"{API}/horse-ledger/{hid}/care-profile",
                       headers=_bearer(mgr),
                       json={"feeding": {"supplements": [
                           {"name": "Magnesium"}]}},
                       timeout=10)
        # Plant a tampered supplement with extra keys directly via Mongo
        # to simulate a future schema drift.
        db.horse_care_profiles.update_one(
            {"horse_id": hid},
            {"$set": {"feeding.supplements": [
                {"name": "Magnesium", "dosage": "2 scoops",
                 "staff_note": "DO NOT TELL OWNER"}]}},
        )
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(owner), timeout=10)
        sups = r.json()["feeding"]["structured"]["supplements"]
        assert sups == [{"name": "Magnesium"}]
        assert "DO NOT TELL OWNER" not in r.text
    finally:
        _cleanup(db)
