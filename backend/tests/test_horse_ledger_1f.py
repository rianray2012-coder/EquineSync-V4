"""tests/test_horse_ledger_1f.py — HorseOps-1F manager polish.

Coverage:
  - barn-wide owner-visibility template save/apply
  - policy validation reuses the locked 1-B safe-key registry
  - manager pulse is staff-only and summary-only
"""
from __future__ import annotations

import os, pathlib, sys, uuid
from datetime import datetime, timezone

import pytest, requests
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
    if env.is_file():
        for line in env.read_text().splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip().rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not configured")


BASE = _base_url()
API = f"{BASE}/api"
TAG = "_hl1f_test"


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role="horse_owner"):
    email = f"hl1f_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "HL1F Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _bearer(s):
    return {"Authorization": f"Bearer {s['token']}"}


def _make_barn(db):
    bid = f"barn_hl1f_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "1F", "status": "active", TAG: True})
    return bid


def _put_user_in_barn(db, uid, bid, role):
    db.users.update_one({"id": uid}, {"$set": {"barn_id": bid, "role": role, TAG: True}})


def _session(db, bid, role):
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], bid, role)
    return s


def _make_horse(db, bid, name="T"):
    hid = f"horse_hl1f_{uuid.uuid4().hex[:10]}"
    db.horses.insert_one({
        "id": hid, "barn_id": bid, "name": name, "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(), TAG: True,
    })
    return hid


def _cleanup(db):
    db.users.delete_many({TAG: True})
    db.barns.delete_many({TAG: True})
    db.horses.delete_many({TAG: True})
    rgx = {"$regex": "^horse_hl1f_"}
    db.horse_owner_visibility_policy.delete_many({"horse_id": rgx})
    db.horse_owner_visibility_templates.delete_many({TAG: True})
    db.horse_ledger_audit.delete_many({"$or": [{"horse_id": rgx}, {TAG: True}]})
    db.horse_ledger_alerts.delete_many({"horse_id": rgx})


SAFE_TEMPLATE = {
    "sections": {
        "feeding": {"allowlist": ["grain_feed_type", "schedule"]},
        "turnout": {"allowlist": ["schedule", "pasture_paddock_assignment"]},
        "equipment": {"allowlist": ["category", "label"]},
    }
}


def test_manager_can_save_and_read_barn_visibility_template(db):
    bid = _make_barn(db)
    mgr = _session(db, bid, "barn_manager")
    try:
        r = requests.put(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), json=SAFE_TEMPLATE, timeout=10,
        )
        assert r.status_code == 200, r.text
        row = db.horse_owner_visibility_templates.find_one({"barn_id": bid})
        # Tag test-owned template for cleanup without changing product behavior.
        db.horse_owner_visibility_templates.update_one({"barn_id": bid}, {"$set": {TAG: True}})
        assert row["sections"]["feeding"]["allowlist"] == ["grain_feed_type", "schedule"]

        got = requests.get(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), timeout=10,
        )
        assert got.status_code == 200
        assert got.json()["sections"]["turnout"]["allowlist"] == ["schedule", "pasture_paddock_assignment"]
    finally:
        _cleanup(db)


def test_template_requires_at_least_one_section(db):
    bid = _make_barn(db)
    mgr = _session(db, bid, "barn_manager")
    try:
        r = requests.put(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), json={"sections": {}}, timeout=10,
        )
        assert r.status_code == 422
    finally:
        _cleanup(db)


@pytest.mark.parametrize("bad_sections", [
    {"stall_bedding": {"allowlist": ["stall_number"]}},
    {"feeding": {"allowlist": ["staff_only_warnings"]}},
    {"feeding": {"allowlist": ["unknown_safeish"]}},
])
def test_template_reuses_owner_safe_policy_validation(db, bad_sections):
    bid = _make_barn(db)
    mgr = _session(db, bid, "admin")
    try:
        r = requests.put(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), json={"sections": bad_sections}, timeout=10,
        )
        assert r.status_code == 422
    finally:
        _cleanup(db)


def test_apply_template_writes_per_horse_policy_rows_and_audit(db):
    bid = _make_barn(db)
    h1 = _make_horse(db, bid, "One")
    h2 = _make_horse(db, bid, "Two")
    mgr = _session(db, bid, "barn_manager")
    try:
        r = requests.put(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), json=SAFE_TEMPLATE, timeout=10,
        )
        assert r.status_code == 200
        db.horse_owner_visibility_templates.update_one({"barn_id": bid}, {"$set": {TAG: True}})
        apply = requests.post(
            f"{API}/horse-ledger/templates/owner-visibility/apply",
            headers=_bearer(mgr), json={}, timeout=10,
        )
        assert apply.status_code == 200, apply.text
        assert apply.json()["applied_count"] == 2
        rows = list(db.horse_owner_visibility_policy.find({"horse_id": {"$in": [h1, h2]}}))
        assert len(rows) == 2
        assert {r["source"] for r in rows} == {"barn_visibility_template"}
        audits = list(db.horse_ledger_audit.find({"horse_id": {"$in": [h1, h2]},
                                                  "action": "template_applied"}))
        assert len(audits) == 2
        for a in audits:
            assert "sections" not in a
            assert "raw" not in a
            assert all("." in p for p in a["field_paths"])
    finally:
        _cleanup(db)


def test_apply_template_explicit_horse_ids_are_barn_scoped(db):
    bid = _make_barn(db)
    h1 = _make_horse(db, bid, "One")
    other_bid = _make_barn(db)
    other_horse = _make_horse(db, other_bid, "Other")
    mgr = _session(db, bid, "admin")
    try:
        assert requests.put(
            f"{API}/horse-ledger/templates/owner-visibility",
            headers=_bearer(mgr), json=SAFE_TEMPLATE, timeout=10,
        ).status_code == 200
        db.horse_owner_visibility_templates.update_one({"barn_id": bid}, {"$set": {TAG: True}})
        r = requests.post(
            f"{API}/horse-ledger/templates/owner-visibility/apply",
            headers=_bearer(mgr),
            json={"horse_ids": [h1, other_horse]},
            timeout=10,
        )
        assert r.status_code == 404
        assert db.horse_owner_visibility_policy.count_documents({"horse_id": other_horse}) == 0
    finally:
        _cleanup(db)


def test_non_manager_cannot_manage_template_or_pulse(db):
    bid = _make_barn(db)
    groom = _session(db, bid, "groom")
    try:
        for method, path, payload in [
            ("put", "/horse-ledger/templates/owner-visibility", SAFE_TEMPLATE),
            ("post", "/horse-ledger/templates/owner-visibility/apply", {}),
            ("get", "/horse-ledger/pulse/manager", None),
        ]:
            fn = getattr(requests, method)
            r = fn(f"{API}{path}", headers=_bearer(groom), json=payload, timeout=10) if payload is not None else fn(f"{API}{path}", headers=_bearer(groom), timeout=10)
            assert r.status_code == 403
    finally:
        _cleanup(db)


def test_manager_pulse_groups_active_alerts_without_raw_alert_detail(db):
    bid = _make_barn(db)
    h1 = _make_horse(db, bid, "Pulse One")
    h2 = _make_horse(db, bid, "Pulse Two")
    mgr = _session(db, bid, "barn_manager")
    now = datetime.now(timezone.utc).isoformat()
    db.horse_ledger_alerts.insert_many([
        {"id": "hla_hl1f_1", "horse_id": h1, "barn_id": bid,
         "alert_type": "feed", "status": "open", "severity": "attention",
         "severity_rank": 1, "last_seen_at": now, "triggers": ["private"], TAG: True},
        {"id": "hla_hl1f_2", "horse_id": h2, "barn_id": bid,
         "alert_type": "water", "status": "open", "severity": "urgent",
         "severity_rank": 2, "last_seen_at": now, "source_check_id": "secret", TAG: True},
    ])
    try:
        r = requests.get(f"{API}/horse-ledger/pulse/manager", headers=_bearer(mgr), timeout=10)
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        assert items[0]["horse_id"] == h2
        assert items[0]["urgent_count"] == 1
        assert "source_check_id" not in r.text
        assert "triggers" not in r.text
        assert "secret" not in r.text
    finally:
        _cleanup(db)


def test_visibility_template_index_exists(db):
    idx = {i["name"] for i in db.horse_owner_visibility_templates.list_indexes()}
    assert "hovt_barn_unique" in idx
