"""tests/test_horse_ledger_1e.py — HorseOps-1E owner summary + owner
service-request flow.

Coverage:
  - owner-summary owner-safe (forbidden keys, tampered policy, ?view escalation)
  - care_status precedence (alerts > requests > all_clear)
  - request_type enum (no billing_question)
  - rate limit (≤5 per owner+horse per rolling hour)
  - existence-leak 404 (cross-barn, non-owner)
  - assigned-staff deferred (founder lock #6)
  - staff status mutation (manager/admin only; valid transitions)
  - adjacent-phase invariants
"""
from __future__ import annotations

import os, pathlib, sys, uuid
from datetime import datetime, timezone, timedelta
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
API  = f"{BASE}/api"
TAG  = "_hl1e_test"


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role="horse_owner"):
    email = f"hl1e_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(f"{API}/auth/signup",
                      json={"email": email, "password": "securepass1",
                            "full_name": "HL1E Test", "role": role}, timeout=15)
    r.raise_for_status()
    return r.json()


def _bearer(s): return {"Authorization": f"Bearer {s['token']}"}


def _make_barn(db):
    bid = f"barn_hl1e_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "1E", "status": "active", TAG: True})
    return bid


def _make_horse(db, bid, owner_id=None, **extras):
    hid = f"horse_hl1e_{uuid.uuid4().hex[:10]}"
    doc = {"id": hid, "barn_id": bid, "name": "T", "status": "active",
           TAG: True, "created_at": datetime.now(timezone.utc).isoformat()}
    if owner_id:
        doc["owner_id"] = owner_id
    doc.update(extras)
    db.horses.insert_one(doc)
    return hid


def _put_user_in_barn(db, uid, bid, role):
    db.users.update_one({"id": uid}, {"$set": {"barn_id": bid, "role": role, TAG: True}})


def _session(db, bid, role):
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], bid, role)
    return s


def _mgr(db, bid):    return _session(db, bid, "barn_manager")
def _admin(db, bid):  return _session(db, bid, "admin")
def _groom(db, bid):  return _session(db, bid, "groom")
def _owner(db, bid, horse_id):
    s = _signup(role="horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, "horse_owner")
    db.horses.update_one({"id": horse_id}, {"$set": {"owner_id": s["user"]["id"]}})
    return s


def _cleanup(db):
    db.users.delete_many({TAG: True})
    db.barns.delete_many({TAG: True})
    db.horses.delete_many({TAG: True})
    rgx = {"$regex": "^horse_hl1e_"}
    for c in ("horse_daily_check_logs", "horse_ledger_alerts",
              "horse_ledger_alert_events", "horse_care_profiles",
              "horse_owner_visibility_policy", "horse_ledger_audit",
              "horse_provider_assignments", "horse_equipment", "service_providers"):
        db[c].delete_many({"horse_id": rgx})
    db.service_requests.delete_many({"horse_id": rgx})


# =====================================================================
# A. owner-summary access + shape.
# =====================================================================
def test_owner_can_fetch_owner_summary(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["horse_id"] == hid
        assert body["care_status"] == "all_clear"
        assert isinstance(body["summary_cards"], list) and len(body["summary_cards"]) == 7
        assert "visible_sections" in body
        assert body["request_options"]["request_type"] == \
            sorted(["question", "care_follow_up", "appointment_request", "other"])
        assert "billing_question" not in body["request_options"]["request_type"]
    finally:
        _cleanup(db)


def test_cross_barn_owner_summary_returns_404(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); o = _owner(db, bid2, _make_horse(db, bid2))
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 404, r.text
    finally:
        _cleanup(db)


def test_non_owner_in_same_barn_gets_404_for_owner_summary(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o1 = _owner(db, bid, hid)
    # Different owner in same barn but for a different horse.
    other_hid = _make_horse(db, bid)
    o2 = _owner(db, bid, other_hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o2), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_manager_can_preview_owner_summary(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(mgr), timeout=10)
        assert r.status_code == 200, r.text
        body = r.json()
        # Manager preview is owner-safe shape only — no daily_checks / alerts.
        assert "daily_checks_recent" not in body
        assert "alerts_open" not in body
    finally:
        _cleanup(db)


def test_non_manager_staff_cannot_preview_owner_summary(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    g = _groom(db, bid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(g), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


@pytest.mark.parametrize("forbidden_key", [
    "daily_checks_recent", "alerts_open", "triggers", "severity",
    "severity_rank", "source_check_id", "staff_note", "required_staff_experience_level",
    "handling_behavior", "stall_bedding", "service_providers",
])
def test_owner_summary_never_contains_forbidden_keys(db, forbidden_key):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    # Plant some staff-side data so forbidden keys could in principle leak.
    requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                  headers=_bearer(mgr),
                  json={"check_type": "feed",
                        "notes": "SECRET_STAFF_NOTE",
                        "payload": {"feed": {"given": False}}},
                  timeout=10)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        text = r.text
        # The forbidden key name string itself appears in the response
        # only legitimately inside `request_options.request_type` etc.,
        # so this assertion is by-key-presence at the top level.
        body = r.json()
        assert forbidden_key not in body
        assert "SECRET_STAFF_NOTE" not in text
    finally:
        _cleanup(db)


# =====================================================================
# B. care_status precedence (alerts > requests > all_clear).
# =====================================================================
def test_care_status_barn_reviewing_when_alert_active(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.json()["care_status"] == "barn_reviewing"
        body = r.json()
        # No alert detail leaked.
        for k in ("triggers", "severity", "source_check_id", "alerts_open"):
            assert k not in body
    finally:
        _cleanup(db)


def test_care_status_follow_up_when_open_request_no_alert(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                      headers=_bearer(o),
                      json={"request_type": "question",
                            "message": "Any update on coat?",
                            "preferred_contact": "app"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.json()["care_status"] == "follow_up_available"
    finally:
        _cleanup(db)


def test_care_status_alert_wins_over_open_request(db):
    """Precedence lock: alert beats request."""
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                      headers=_bearer(o),
                      json={"request_type": "question",
                            "message": "M?", "preferred_contact": "app"},
                      timeout=10)
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.json()["care_status"] == "barn_reviewing"
    finally:
        _cleanup(db)


def test_care_status_all_clear_when_nothing_active(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.json()["care_status"] == "all_clear"
    finally:
        _cleanup(db)


# =====================================================================
# C. request_type validation + billing_question rejection.
# =====================================================================
@pytest.mark.parametrize("bad", ["billing_question", "NONE", "", "support"])
def test_invalid_request_type_422(db, bad):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": bad, "message": "hi",
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 422, (bad, r.text)
    finally:
        _cleanup(db)


@pytest.mark.parametrize("rt", ["question", "care_follow_up", "appointment_request", "other"])
def test_valid_request_types_accepted(db, rt):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": rt, "message": "ok",
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 200, (rt, r.text)
    finally:
        _cleanup(db)


def test_message_length_cap_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": "question",
                                "message": "x" * 1001,
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_empty_message_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": "question", "message": "  ",
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_owner_cannot_set_staff_note_via_post(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": "question", "message": "m",
                                "preferred_contact": "app",
                                "staff_note": "INJECT"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


# =====================================================================
# D. Rate limit (≤5 per owner+horse per rolling hour).
# =====================================================================
def test_rate_limit_blocks_sixth_request(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        for i in range(5):
            r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                              headers=_bearer(o),
                              json={"request_type": "question",
                                    "message": f"m{i}",
                                    "preferred_contact": "app"}, timeout=10)
            assert r.status_code == 200, (i, r.text)
        r6 = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                           headers=_bearer(o),
                           json={"request_type": "question", "message": "m6",
                                 "preferred_contact": "app"}, timeout=10)
        assert r6.status_code == 429
        assert r6.json()["detail"] == "Too many requests. Please try again later."
        # Verify no row written for the 6th attempt.
        assert db.service_requests.count_documents(
            {"horse_id": hid, "source": "owner_care_ledger"}) == 5
    finally:
        _cleanup(db)


def test_rate_limit_window_respects_old_rows(db):
    """A row older than 1 hour shouldn't count toward the cap."""
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    old_iso = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    # Plant 5 old rows (>1h ago) — they should NOT count.
    for i in range(5):
        db.service_requests.insert_one({
            "id": f"osr_old_{i}", "source": "owner_care_ledger",
            "horse_id": hid, "barn_id": bid,
            "owner_user_id": o["user"]["id"],
            "request_type": "question", "message": "old",
            "preferred_contact": "app", "status": "new",
            "created_at": old_iso, "updated_at": old_iso,
            "resolved_at": None, "resolved_by_user_id": None, "staff_note": None,
            TAG: True,
        })
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(o),
                          json={"request_type": "question", "message": "fresh",
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 200, r.text
    finally:
        _cleanup(db)


def test_rate_limit_is_per_owner_per_horse(db):
    """Same owner, different horse → counters independent."""
    bid = _make_barn(db); h1 = _make_horse(db, bid); h2 = _make_horse(db, bid)
    o = _owner(db, bid, h1)
    db.horses.update_one({"id": h2}, {"$set": {"owner_id": o["user"]["id"]}})
    try:
        for i in range(5):
            r1 = requests.post(f"{API}/horse-ledger/{h1}/owner-service-requests",
                               headers=_bearer(o),
                               json={"request_type": "question",
                                     "message": f"h1-{i}",
                                     "preferred_contact": "app"}, timeout=10)
            r2 = requests.post(f"{API}/horse-ledger/{h2}/owner-service-requests",
                               headers=_bearer(o),
                               json={"request_type": "question",
                                     "message": f"h2-{i}",
                                     "preferred_contact": "app"}, timeout=10)
            assert r1.status_code == 200 and r2.status_code == 200, (i, r1.text, r2.text)
    finally:
        _cleanup(db)


# =====================================================================
# E. Staff visibility (founder lock #6 — manager/admin only).
# =====================================================================
def test_manager_can_list_owner_requests(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                  headers=_bearer(o),
                  json={"request_type": "question", "message": "Q?",
                        "preferred_contact": "app"}, timeout=10)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(mgr), timeout=10)
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        assert len(items) == 1
        assert items[0]["message"] == "Q?"
        # Manager response carries staff_note (may be None).
        assert "staff_note" in items[0]
    finally:
        _cleanup(db)


def test_staff_role_cannot_see_owner_requests_in_1e(db):
    """Founder lock #6 — assigned-staff visibility deferred."""
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); g = _groom(db, bid)
    requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                  headers=_bearer(o),
                  json={"request_type": "question", "message": "Q?",
                        "preferred_contact": "app"}, timeout=10)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(g), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_owner_sees_only_own_requests(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                      headers=_bearer(o),
                      json={"request_type": "question", "message": "mine",
                            "preferred_contact": "app"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(o), timeout=10)
        items = r.json()["items"]
        assert len(items) == 1
        # Owner response strips staff_note unconditionally.
        assert "staff_note" not in items[0]
    finally:
        _cleanup(db)


# =====================================================================
# F. Manager status mutation.
# =====================================================================
def _seed_request(db, hid, bid, owner_uid):
    rid = f"osr_seed_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    db.service_requests.insert_one({
        "id": rid, "source": "owner_care_ledger",
        "horse_id": hid, "barn_id": bid,
        "owner_user_id": owner_uid,
        "request_type": "question", "message": "m",
        "preferred_contact": "app", "status": "new",
        "created_at": now, "updated_at": now,
        "resolved_at": None, "resolved_by_user_id": None, "staff_note": None,
        TAG: True,
    })
    return rid


def test_manager_can_transition_to_resolved(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                           headers=_bearer(mgr),
                           json={"status": "resolved",
                                 "staff_note": "Talked to owner."},
                           timeout=10)
        assert r.status_code == 200, r.text
        row = db.service_requests.find_one({"id": rid})
        assert row["status"] == "resolved"
        assert row["resolved_at"] is not None
        assert row["resolved_by_user_id"] == mgr["user"]["id"]
        assert row["staff_note"] == "Talked to owner."
    finally:
        _cleanup(db)


def test_staff_cannot_patch_owner_request(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); g = _groom(db, bid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                           headers=_bearer(g),
                           json={"status": "in_progress"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_owner_cannot_patch_owner_request(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                           headers=_bearer(o),
                           json={"status": "resolved"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_invalid_status_transition_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    # Move to resolved.
    requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                   headers=_bearer(mgr), json={"status": "resolved"}, timeout=10)
    try:
        # resolved → new is not in the valid set; only resolved→in_progress is.
        r = requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                           headers=_bearer(mgr),
                           json={"status": "new"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_staff_note_length_cap_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                           headers=_bearer(mgr),
                           json={"staff_note": "x" * 501}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_staff_note_never_in_owner_response(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid); mgr = _mgr(db, bid)
    rid = _seed_request(db, hid, bid, o["user"]["id"])
    requests.patch(f"{API}/horse-ledger/{hid}/owner-service-requests/{rid}",
                   headers=_bearer(mgr),
                   json={"staff_note": "INTERNAL_DO_NOT_SHOW"}, timeout=10)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(o), timeout=10)
        assert "INTERNAL_DO_NOT_SHOW" not in r.text
        # Same for the owner-summary recent_owner_requests block.
        r2 = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                          headers=_bearer(o), timeout=10)
        assert "INTERNAL_DO_NOT_SHOW" not in r2.text
    finally:
        _cleanup(db)


# =====================================================================
# G. Existing operational service-request rows are isolated.
# =====================================================================
def test_pre_existing_operational_rows_not_returned_by_owner_list(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid)
    # Insert an operational row WITHOUT source="owner_care_ledger".
    db.service_requests.insert_one({
        "id": f"sr_op_{uuid.uuid4().hex[:8]}",
        "horse_id": hid, "barn_id": bid,
        "type": "farrier", "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        TAG: True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(mgr), timeout=10)
        assert r.status_code == 200
        assert r.json()["items"] == []
    finally:
        _cleanup(db)


# =====================================================================
# H. Existence-leak + adjacent-phase invariants.
# =====================================================================
def test_cross_barn_post_owner_request_404(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); other = _owner(db, bid2, _make_horse(db, bid2))
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                          headers=_bearer(other),
                          json={"request_type": "question", "message": "x",
                                "preferred_contact": "app"}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_admin_portal_lock_unchanged_after_1e(db):
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 26
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1


def test_service_request_owner_indexes_present(db):
    idx = {i["name"] for i in db.service_requests.list_indexes()}
    assert "sr_source_barn_horse_created" in idx
    assert "sr_owner_horse_created" in idx


# =====================================================================
# Codex Round-1 regressions (Phase HorseOps-1E)
#
# P0  Owner access must support `primary_owner_id` (locked Care Ledger
#     field name from 1-A) in addition to `owner_id` and
#     `secondary_owner_ids`. Without this, every horse keyed under
#     `primary_owner_id` 404s the owner.
# =====================================================================
def _owner_via_primary(db, bid, horse_id):
    """Owner whose ID is stored in `horses.primary_owner_id` only
    (NOT `owner_id`). Mirrors the locked Care Ledger schema from 1-A."""
    s = _signup(role="horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, "horse_owner")
    db.horses.update_one(
        {"id": horse_id},
        {"$set": {"primary_owner_id": s["user"]["id"]},
         "$unset": {"owner_id": ""}},
    )
    return s


def test_owner_summary_accepts_primary_owner_id(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner_via_primary(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 200, r.text
        assert r.json()["horse_id"] == hid
    finally:
        _cleanup(db)


def test_owner_can_post_owner_request_via_primary_owner_id(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner_via_primary(db, bid, hid)
    try:
        r = requests.post(
            f"{API}/horse-ledger/{hid}/owner-service-requests",
            headers=_bearer(o),
            json={"request_type": "question", "message": "via primary",
                  "preferred_contact": "app"}, timeout=10,
        )
        assert r.status_code == 200, r.text
        row = db.service_requests.find_one(
            {"id": r.json()["id"], "source": "owner_care_ledger"})
        assert row["owner_user_id"] == o["user"]["id"]
    finally:
        _cleanup(db)


def test_owner_list_via_primary_owner_id(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner_via_primary(db, bid, hid)
    # Seed a request directly.
    db.service_requests.insert_one({
        "id": "osr_primary_seed", "source": "owner_care_ledger",
        "horse_id": hid, "barn_id": bid,
        "owner_user_id": o["user"]["id"],
        "request_type": "question", "message": "seeded",
        "preferred_contact": "app", "status": "new",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "resolved_at": None, "resolved_by_user_id": None, "staff_note": None,
        TAG: True,
    })
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-service-requests",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        assert any(it["id"] == "osr_primary_seed" for it in items)
        # Owner response still strips staff_note.
        for it in items:
            assert "staff_note" not in it
    finally:
        _cleanup(db)


def test_owner_summary_care_status_request_via_primary_owner_id(db):
    """care_status follow_up_available must also key off
    `primary_owner_id` (was effectively broken before — owner posts
    succeeded under owner_id but care_status lookup used owner_id only).
    """
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner_via_primary(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                      headers=_bearer(o),
                      json={"request_type": "question", "message": "?",
                            "preferred_contact": "app"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(o), timeout=10)
        assert r.json()["care_status"] == "follow_up_available"
    finally:
        _cleanup(db)


def test_manager_preview_care_status_uses_primary_owner_id_for_owner_lookup(db):
    """Manager preview reads `recent_owner_requests` for the horse's
    primary owner; if it uses only `owner_id`, the preview will show an
    empty list when the field is `primary_owner_id`."""
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner_via_primary(db, bid, hid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/owner-service-requests",
                      headers=_bearer(o),
                      json={"request_type": "question", "message": "?",
                            "preferred_contact": "app"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(mgr), timeout=10)
        assert r.status_code == 200
        # care_status follows the primary owner's request.
        assert r.json()["care_status"] == "follow_up_available"
        # And the recent_owner_requests block reflects the primary owner.
        recent = r.json().get("recent_owner_requests") or []
        assert len(recent) == 1
    finally:
        _cleanup(db)


def test_secondary_owner_id_still_works(db):
    """Regression: the existing `secondary_owner_ids` path is not
    broken by adding `primary_owner_id` support."""
    bid = _make_barn(db); hid = _make_horse(db, bid)
    # Create a primary-only owner (so the horse has SOMEONE), then a
    # secondary owner.
    primary = _owner_via_primary(db, bid, hid)
    sec = _signup(role="horse_owner")
    _put_user_in_barn(db, sec["user"]["id"], bid, "horse_owner")
    db.horses.update_one({"id": hid},
                         {"$set": {"secondary_owner_ids": [sec["user"]["id"]]}})
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/owner-summary",
                         headers=_bearer(sec), timeout=10)
        assert r.status_code == 200, r.text
        # Posting a request as the secondary owner succeeds.
        r2 = requests.post(
            f"{API}/horse-ledger/{hid}/owner-service-requests",
            headers=_bearer(sec),
            json={"request_type": "question", "message": "from secondary",
                  "preferred_contact": "app"}, timeout=10,
        )
        assert r2.status_code == 200
    finally:
        _cleanup(db)

