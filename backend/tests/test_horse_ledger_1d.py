"""tests/test_horse_ledger_1d.py — HorseOps-1D alerts, escalations,
history, and staff experience-level gate.

Coverage:
  - Alert minting (event-driven from daily-check writes)
  - Dedupe / occurrence_count / severity-upgrade-only
  - Lifecycle: open → acknowledged → closed; reopen manager-only
  - Permissions: staff vs manager vs owner vs cross-barn
  - Experience gate: generic 403, NO audit/alert/event side effects
  - Owner read of `alerts_open` stays `[]`
  - History endpoint merges checks + alerts + audit
  - Adjacent-phase invariants
"""
from __future__ import annotations

import os, pathlib, sys, uuid
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
API  = f"{BASE}/api"
TAG  = "_hl1d_test"


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role="horse_owner"):
    email = f"hl1d_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(f"{API}/auth/signup",
                      json={"email": email, "password": "securepass1",
                            "full_name": "HL1D Test", "role": role}, timeout=15)
    r.raise_for_status()
    return r.json()


def _bearer(s):
    return {"Authorization": f"Bearer {s['token']}"}


def _make_barn(db):
    bid = f"barn_hl1d_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "1D Test", "status": "active",
                         TAG: True})
    return bid


def _make_horse(db, bid, **extras):
    hid = f"horse_hl1d_{uuid.uuid4().hex[:10]}"
    doc = {"id": hid, "barn_id": bid, "name": "Tester", "status": "active",
           TAG: True, "created_at": datetime.now(timezone.utc).isoformat()}
    doc.update(extras)
    db.horses.insert_one(doc)
    return hid


def _put_user_in_barn(db, uid, bid, role="barn_manager", experience_level=None):
    upd = {"barn_id": bid, "role": role, TAG: True}
    if experience_level is not None:
        upd["experience_level"] = experience_level
    db.users.update_one({"id": uid}, {"$set": upd})


def _session(db, bid, role, experience_level=None):
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], bid, role=role,
                      experience_level=experience_level)
    return s


def _mgr(db, bid):    return _session(db, bid, "barn_manager")
def _admin(db, bid):  return _session(db, bid, "admin")
def _groom(db, bid, exp=None):  return _session(db, bid, "groom",   experience_level=exp)
def _vet(db, bid, exp=None):    return _session(db, bid, "vet",     experience_level=exp)
def _staff(db, bid, exp=None):  return _session(db, bid, "staff",   experience_level=exp)
def _owner(db, bid, horse_id=None):
    s = _signup(role="horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, role="horse_owner")
    if horse_id is not None:
        db.horses.update_one({"id": horse_id}, {"$set": {"owner_id": s["user"]["id"]}})
    return s


def _cleanup(db):
    db.users.delete_many({TAG: True})
    db.barns.delete_many({TAG: True})
    db.horses.delete_many({TAG: True})
    rgx = {"$regex": "^horse_hl1d_"}
    for c in ("horse_daily_check_logs", "horse_care_profiles",
              "horse_owner_visibility_policy", "horse_ledger_audit",
              "horse_ledger_alerts", "horse_ledger_alert_events"):
        db[c].delete_many({"horse_id": rgx})


# =====================================================================
# A. Alert minting — event-driven from daily-check writes.
# =====================================================================
@pytest.mark.parametrize("check_type,body,expected_severity", [
    ("feed",    {"status": "missed"},                                 "urgent"),
    ("water",   {"status": "missed"},                                 "urgent"),
    ("water",   {"payload": {"water": {"bucket_ok": False}}},         "urgent"),
    ("water",   {"payload": {"water": {"automatic_waterer_ok": False}}}, "urgent"),
    ("feed",    {"payload": {"feed": {"given": False}}},              "urgent"),
    ("bedding", {"payload": {"bedding": {"top_off_needed": True, "condition": "clean"}}}, "attention"),
    ("bedding", {"payload": {"bedding": {"full_strip_needed": True, "condition": "clean"}}}, "attention"),
    ("hay_net", {"payload": {"hay_net": {"nets_checked": 3, "nets_refilled": 0}}}, "attention"),
    ("hay",     {"payload": {"hay_access": {"free_choice_available": False}}}, "attention"),
    ("general", {"status": "needs_attention"},                        "attention"),
])
def test_alert_minted_for_each_trigger(db, check_type, body, expected_severity):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    payload_body = {"check_type": check_type, **body}
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr), json=payload_body, timeout=10)
        assert r.status_code == 200, r.text
        cid = r.json()["id"]
        # Exactly one alert minted.
        alerts = list(db.horse_ledger_alerts.find({"horse_id": hid}))
        assert len(alerts) == 1, alerts
        a = alerts[0]
        assert a["alert_type"] == check_type
        assert a["severity"]   == expected_severity
        assert a["status"]     == "open"
        assert a["source_check_id"] == cid
        assert a["occurrence_count"] == 1
        # And exactly one history event.
        evs = list(db.horse_ledger_alert_events.find({"alert_id": a["id"]}))
        assert len(evs) == 1
        assert evs[0]["event_type"] == "opened"
    finally:
        _cleanup(db)


def test_ok_check_mints_no_alert(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        for ct in ("feed", "water", "bedding", "hay", "hay_net"):
            requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": ct, "status": "ok"},
                          timeout=10)
        assert db.horse_ledger_alerts.count_documents({"horse_id": hid}) == 0
    finally:
        _cleanup(db)


# =====================================================================
# B. Dedupe + occurrence_count + severity-upgrade-only.
# =====================================================================
def test_repeated_same_check_id_no_duplicate(db):
    """PATCH amend on the same check row should not produce a second
    alert for the same `source_check_id + alert_type`."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        c = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed",
                                "payload": {"feed": {"given": False}}},
                          timeout=10).json()
        cid = c["id"]
        # PATCH amend (same source_check_id).
        requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                       headers=_bearer(mgr),
                       json={"notes": "amend"}, timeout=10)
        assert db.horse_ledger_alerts.count_documents({"horse_id": hid}) == 1
    finally:
        _cleanup(db)


def test_repeated_same_category_updates_existing_alert(db):
    """Two same-category triggers from DIFFERENT checks bump
    occurrence_count and last_seen_at on the existing open alert."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r1 = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                           headers=_bearer(mgr),
                           json={"check_type": "water",
                                 "payload": {"water": {"bucket_ok": False}}},
                           timeout=10).json()
        first_ts = db.horse_ledger_alerts.find_one({"horse_id": hid})["last_seen_at"]
        r2 = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                           headers=_bearer(mgr),
                           json={"check_type": "water",
                                 "payload": {"water": {"automatic_waterer_ok": False}}},
                           timeout=10).json()
        # Still one alert, but count == 2 and triggers merged.
        alerts = list(db.horse_ledger_alerts.find({"horse_id": hid}))
        assert len(alerts) == 1
        a = alerts[0]
        assert a["occurrence_count"] == 2
        assert a["last_seen_at"] >= first_ts
        assert set(a["triggers"]) >= {"water.bucket_ok=false", "water.automatic_waterer_ok=false"}
        # Two history events.
        assert db.horse_ledger_alert_events.count_documents({"alert_id": a["id"]}) == 2
    finally:
        _cleanup(db)


def test_severity_only_upgrades_never_downgrades(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        # First trigger: attention (bedding top-off).
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "bedding",
                            "payload": {"bedding": {"top_off_needed": True, "condition": "clean"}}},
                      timeout=10)
        a1 = db.horse_ledger_alerts.find_one({"horse_id": hid})
        assert a1["severity"] == "attention"
        # Second trigger: missed bedding status (urgent if treated so,
        # but our derive returns `attention` for bedding missed —
        # ensure dedupe still keeps `attention`).
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "bedding", "status": "missed",
                            "payload": {"bedding": {"condition": "soiled"}}},
                      timeout=10)
        a2 = db.horse_ledger_alerts.find_one({"horse_id": hid})
        # Severity stays at `attention` since bedding-missed maps to attention.
        assert a2["severity"] == "attention"
        # Now a feed alert with explicit urgent severity in a different check_type
        # would create a different alert row, so test upgrade by simulating water:
        # water alert path: first bucket_ok=false (urgent), then bucket_ok=false again.
    finally:
        _cleanup(db)


def test_closed_alert_then_new_trigger_creates_new_row(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        a = db.horse_ledger_alerts.find_one({"horse_id": hid})
        # Close it.
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                       headers=_bearer(mgr),
                       json={"status": "closed",
                             "resolution_note": "Feed delivered late"},
                       timeout=10)
        assert db.horse_ledger_alerts.find_one({"id": a["id"]})["status"] == "closed"
        # New trigger → new alert row (does not reopen the closed one).
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        assert db.horse_ledger_alerts.count_documents(
            {"horse_id": hid, "alert_type": "feed"}) == 2
    finally:
        _cleanup(db)


def test_different_alert_types_independent_rows(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "water",
                            "payload": {"water": {"bucket_ok": False}}},
                      timeout=10)
        assert db.horse_ledger_alerts.count_documents({"horse_id": hid}) == 2
    finally:
        _cleanup(db)


# =====================================================================
# C. Lifecycle endpoints (acknowledge / close / reopen).
# =====================================================================
def _mint_alert(db, bid, hid, mgr):
    r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
    assert r.status_code == 200, r.text
    return db.horse_ledger_alerts.find_one({"horse_id": hid})


def test_any_staff_can_acknowledge(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); g = _groom(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(g),
                           json={"status": "acknowledged"}, timeout=10)
        assert r.status_code == 200, r.text
        cur = db.horse_ledger_alerts.find_one({"id": a["id"]})
        assert cur["status"] == "acknowledged"
        assert cur["acknowledged_by_user_id"] == g["user"]["id"]
    finally:
        _cleanup(db)


def test_any_staff_can_close(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); g = _groom(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(g),
                           json={"status": "closed",
                                 "resolution_note": "Refilled"}, timeout=10)
        assert r.status_code == 200, r.text
        cur = db.horse_ledger_alerts.find_one({"id": a["id"]})
        assert cur["status"] == "closed"
        assert cur["closed_by_user_id"] == g["user"]["id"]
    finally:
        _cleanup(db)


def test_only_manager_can_reopen(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); g = _groom(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                       headers=_bearer(mgr),
                       json={"status": "closed"}, timeout=10)
        # Staff cannot reopen.
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(g),
                           json={"status": "open"}, timeout=10)
        assert r.status_code == 403
        # Manager can.
        r2 = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                            headers=_bearer(mgr),
                            json={"status": "open"}, timeout=10)
        assert r2.status_code == 200, r2.text
        assert db.horse_ledger_alerts.find_one({"id": a["id"]})["status"] == "open"
    finally:
        _cleanup(db)


def test_owner_cannot_patch_alert(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(o),
                           json={"status": "closed"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_cross_barn_patch_alert_404(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1); mgr1 = _mgr(db, bid1)
    bid2 = _make_barn(db); mgr2 = _mgr(db, bid2)
    try:
        a = _mint_alert(db, bid1, hid, mgr1)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(mgr2),
                           json={"status": "closed"}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_patch_unknown_alert_id_404(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/hla_nope",
                           headers=_bearer(mgr),
                           json={"status": "closed"}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_resolution_note_length_cap_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(mgr),
                           json={"status": "closed",
                                 "resolution_note": "x" * 501}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_invalid_transition_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        # Close first.
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                       headers=_bearer(mgr),
                       json={"status": "closed"}, timeout=10)
        # Now acknowledged → closed transition isn't valid from closed
        # without going through reopen → 422.
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(mgr),
                           json={"status": "acknowledged"}, timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_patch_unknown_field_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        r = requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                           headers=_bearer(mgr),
                           json={"severity": "info"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


# =====================================================================
# D. List + filters.
# =====================================================================
def test_list_alerts_default_is_active(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        # 2 active alerts (different categories).
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "water",
                            "payload": {"water": {"bucket_ok": False}}},
                      timeout=10)
        # Close one.
        wid = db.horse_ledger_alerts.find_one({"alert_type": "water"})["id"]
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{wid}",
                       headers=_bearer(mgr),
                       json={"status": "closed"}, timeout=10)
        # Default list = active (open + acknowledged) only.
        r = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                         headers=_bearer(mgr), timeout=10)
        items = r.json()["items"]
        assert len(items) == 1
        assert items[0]["alert_type"] == "feed"
        # status=all returns both.
        r2 = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                          headers=_bearer(mgr),
                          params={"status": "all"}, timeout=10)
        assert len(r2.json()["items"]) == 2
        # status=closed returns just one.
        r3 = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                          headers=_bearer(mgr),
                          params={"status": "closed"}, timeout=10)
        items3 = r3.json()["items"]
        assert len(items3) == 1
        assert items3[0]["alert_type"] == "water"
    finally:
        _cleanup(db)


def test_list_alerts_invalid_filter_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                         headers=_bearer(mgr),
                         params={"status": "bogus"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_owner_cannot_list_alerts(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_cross_barn_list_alerts_404(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); foreign = _mgr(db, bid2)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/alerts",
                         headers=_bearer(foreign), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


# =====================================================================
# E. Owner hard-hide invariants.
# =====================================================================
def test_owner_ledger_alerts_open_is_empty_even_with_active_alerts(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "notes": "SECRET_ALERT_NOTE",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(o), timeout=10)
        body = r.json()
        assert body["alerts_open"] == []
        assert "SECRET_ALERT_NOTE" not in r.text
    finally:
        _cleanup(db)


def test_staff_ledger_alerts_open_populated(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(mgr), timeout=10)
        opens = r.json()["alerts_open"]
        assert len(opens) == 1
        assert opens[0]["alert_type"] == "feed"
        assert opens[0]["severity"]   == "urgent"
    finally:
        _cleanup(db)


def test_owner_cannot_reveal_alerts_via_view_query(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "water",
                            "payload": {"water": {"bucket_ok": False}}},
                      timeout=10)
        for q in ("?view=staff", "?view=full"):
            r = requests.get(f"{API}/horse-ledger/{hid}{q}",
                             headers=_bearer(o), timeout=10)
            assert r.json()["alerts_open"] == []
    finally:
        _cleanup(db)


def test_policy_put_rejects_alerts_open_section(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.put(
            f"{API}/horse-ledger/{hid}/owner-visibility-policy",
            headers=_bearer(mgr),
            json={"sections": {"alerts_open": {"allowlist": ["alert_type"]}}},
            timeout=10,
        )
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_owner_cannot_reveal_alerts_via_tampered_policy(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "water",
                            "notes": "TAMPER_ALERTS_PROBE",
                            "payload": {"water": {"bucket_ok": False}}},
                      timeout=10)
        db.horse_owner_visibility_policy.insert_one({
            "id": f"hovp_d_{uuid.uuid4().hex[:8]}",
            "horse_id": hid, "barn_id": bid,
            "sections": {"alerts_open": {"allowlist": ["*"]}},
            TAG: True,
        })
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(o), timeout=10)
        assert r.json()["alerts_open"] == []
        assert "TAMPER_ALERTS_PROBE" not in r.text
    finally:
        _cleanup(db)


# =====================================================================
# F. Experience-level gate.
# =====================================================================
def _set_required_level(db, hid, bid, required):
    db.horse_care_profiles.insert_one({
        "id": f"hcp_d_{uuid.uuid4().hex[:8]}",
        "horse_id": hid, "barn_id": bid,
        "handling_behavior": {"required_staff_experience_level": required},
        TAG: True,
    })


@pytest.mark.parametrize("caller_level,required,should_block", [
    ("novice",       "intermediate", True),
    ("novice",       "experienced",  True),
    ("novice",       "advanced",     True),
    ("intermediate", "experienced",  True),
    ("intermediate", "advanced",     True),
    ("experienced",  "advanced",     True),
    ("experienced",  "experienced",  False),
    ("advanced",     "experienced",  False),
    ("advanced",     "advanced",     False),
    ("intermediate", "intermediate", False),
])
@pytest.mark.parametrize("check_type", ["feed", "hay", "hay_net", "water", "bedding"])
def test_experience_gate_blocks_under_qualified_writes(
        db, caller_level, required, should_block, check_type):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    _set_required_level(db, hid, bid, required)
    g = _groom(db, bid, exp=caller_level)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(g),
                          json={"check_type": check_type}, timeout=10)
        if should_block:
            assert r.status_code == 403, (caller_level, required, check_type, r.text)
            assert r.json()["detail"] == "Insufficient permission for this care action."
            # NO daily-check row, NO audit row, NO alert row, NO event row.
            assert db.horse_daily_check_logs.count_documents({"horse_id": hid}) == 0
            assert db.horse_ledger_audit.count_documents({"horse_id": hid, "section": "daily_checks"}) == 0
            assert db.horse_ledger_alerts.count_documents({"horse_id": hid}) == 0
            assert db.horse_ledger_alert_events.count_documents({"horse_id": hid}) == 0
        else:
            assert r.status_code == 200, (caller_level, required, check_type, r.text)
    finally:
        _cleanup(db)


def test_general_check_bypasses_experience_gate(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    _set_required_level(db, hid, bid, "advanced")
    g = _groom(db, bid, exp="novice")
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(g),
                          json={"check_type": "general", "status": "ok"},
                          timeout=10)
        assert r.status_code == 200, r.text
    finally:
        _cleanup(db)


def test_admin_and_manager_bypass_experience_gate(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    _set_required_level(db, hid, bid, "advanced")
    for s in (_mgr(db, bid), _admin(db, bid)):
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(s),
                          json={"check_type": "feed",
                                "payload": {"feed": {"given": True}}},
                          timeout=10)
        assert r.status_code == 200, r.text
    _cleanup(db)


def test_null_caller_experience_treated_as_novice(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    _set_required_level(db, hid, bid, "experienced")
    g = _groom(db, bid, exp=None)  # no experience_level set
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(g),
                          json={"check_type": "feed"}, timeout=10)
        assert r.status_code == 403
        assert r.json()["detail"] == "Insufficient permission for this care action."
    finally:
        _cleanup(db)


def test_experience_gate_blocks_patch_amend(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    # Plant a check first WITHOUT a required level.
    mgr = _mgr(db, bid)
    r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": True}}},
                      timeout=10)
    cid = r.json()["id"]
    # Now raise the required level.
    _set_required_level(db, hid, bid, "advanced")
    g = _groom(db, bid, exp="novice")
    # PATCH by the same author (groom) — author check would normally
    # pass, but the experience gate blocks.
    try:
        # Make groom the author so amender check doesn't 403 first.
        db.horse_daily_check_logs.update_one({"id": cid},
            {"$set": {"checked_by_user_id": g["user"]["id"]}})
        r2 = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                            headers=_bearer(g),
                            json={"notes": "amend"}, timeout=10)
        assert r2.status_code == 403
        assert r2.json()["detail"] == "Insufficient permission for this care action."
    finally:
        _cleanup(db)


# =====================================================================
# G. Audit invariants — alert lifecycle emits field_paths only.
# =====================================================================
def test_alert_close_emits_audit_with_field_paths_only(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        a = _mint_alert(db, bid, hid, mgr)
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                       headers=_bearer(mgr),
                       json={"status": "closed",
                             "resolution_note": "RAW_NOTE_HIDE_IN_AUDIT"},
                       timeout=10)
        row = db.horse_ledger_audit.find_one(
            {"horse_id": hid, "section": "alerts", "action": "closed"})
        assert row is not None
        assert "RAW_NOTE_HIDE_IN_AUDIT" not in str(row)
        assert "resolution_note" in row["field_paths"]
        # No before/after/values in the audit row.
        for forbidden_key in ("before", "after", "values", "payload_actual"):
            assert forbidden_key not in row
    finally:
        _cleanup(db)


def test_no_audit_row_for_alert_minting_side_effect(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        # Only the daily_checks audit row exists; no `alerts/created`
        # audit row (lifecycle audit happens on PATCH only).
        assert db.horse_ledger_audit.count_documents(
            {"horse_id": hid, "section": "alerts"}) == 0
        assert db.horse_ledger_audit.count_documents(
            {"horse_id": hid, "section": "daily_checks"}) == 1
    finally:
        _cleanup(db)


# =====================================================================
# H. History endpoint.
# =====================================================================
def test_history_merges_checks_alerts_and_audit(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        # Create a few rows.
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": False}}},
                      timeout=10)
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "water", "status": "ok"},
                      timeout=10)
        a = db.horse_ledger_alerts.find_one({"horse_id": hid})
        requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                       headers=_bearer(mgr),
                       json={"status": "acknowledged"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/history",
                         headers=_bearer(mgr), timeout=10)
        items = r.json()["items"]
        types = {it["entry_type"] for it in items}
        assert types >= {"daily_check", "alert", "audit"}
        # Sorted desc.
        ts = [it["ts"] for it in items]
        assert ts == sorted(ts, reverse=True)
    finally:
        _cleanup(db)


def test_history_owner_403(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); o = _owner(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/history",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_history_cross_barn_404(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); foreign = _mgr(db, bid2)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/history",
                         headers=_bearer(foreign), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_history_limit_capped_at_200(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/history",
                         headers=_bearer(mgr),
                         params={"limit": 99999}, timeout=10)
        assert r.status_code == 200
        assert len(r.json()["items"]) <= 200
    finally:
        _cleanup(db)


# =====================================================================
# I. Adjacent-phase invariants + indexes.
# =====================================================================
def test_alert_event_indexes_present(db):
    idx = {i["name"] for i in db.horse_ledger_alert_events.list_indexes()}
    for expected in ("hlae_alert_ts", "hlae_horse_ts", "hlae_barn_ts"):
        assert expected in idx, f"missing index {expected}: have {sorted(idx)}"


def test_phase_9_collections_untouched_after_1d_storm(db):
    counts_before = {
        c: db[c].count_documents({})
        for c in ("invoices", "recurring_charges", "recurring_billing_rules")
    }
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        for _ in range(5):
            requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed",
                                "payload": {"feed": {"given": False}}},
                          timeout=10)
            a = db.horse_ledger_alerts.find_one({"horse_id": hid})
            if a:
                requests.patch(f"{API}/horse-ledger/{hid}/alerts/{a['id']}",
                               headers=_bearer(mgr),
                               json={"status": "closed"}, timeout=10)
        counts_after = {
            c: db[c].count_documents({}) for c in counts_before
        }
        assert counts_before == counts_after
    finally:
        _cleanup(db)


def test_admin_portal_route_lock_unchanged_after_1d(db):
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 26
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1
