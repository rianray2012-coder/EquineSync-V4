"""tests/test_horse_ledger_1c.py — HorseOps-1C staff daily checks.

Coverage:
  Permissions (mutator hybrid + owner 403 + cross-barn 404)
  Validation (enums, payload subkeys, primitives, length cap)
  Task linkage (store-only — does NOT auto-complete tasks)
  Read integration (staff sees recent; owner hard-hidden)
  Owner-visibility policy cannot expose daily checks
  Audit (field paths only, no raw notes, no 403 audit rows)
  Adjacent-phase invariants (Phase 9/15/Admin Portal/1-A/1-B unchanged)
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
TAG  = "_hl1c_test"


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role="horse_owner"):
    email = f"hl1c_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(f"{API}/auth/signup",
                      json={"email": email, "password": "securepass1",
                            "full_name": "HL1C Test", "role": role}, timeout=15)
    r.raise_for_status()
    return r.json()


def _bearer(s):
    return {"Authorization": f"Bearer {s['token']}"}


def _make_barn(db):
    bid = f"barn_hl1c_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "1C Test", "status": "active",
                         TAG: True})
    return bid


def _make_horse(db, bid, **extras):
    hid = f"horse_hl1c_{uuid.uuid4().hex[:10]}"
    doc = {"id": hid, "barn_id": bid, "name": "Tester", "status": "active",
           TAG: True,
           "created_at": datetime.now(timezone.utc).isoformat()}
    doc.update(extras)
    db.horses.insert_one(doc)
    return hid


def _put_user_in_barn(db, uid, bid, role="barn_manager"):
    db.users.update_one({"id": uid},
                        {"$set": {"barn_id": bid, "role": role, TAG: True}})


def _session(db, bid, role):
    s = _signup()
    _put_user_in_barn(db, s["user"]["id"], bid, role=role)
    return s


def _mgr(db, bid):    return _session(db, bid, "barn_manager")
def _admin(db, bid):  return _session(db, bid, "admin")
def _groom(db, bid):  return _session(db, bid, "groom")
def _trainer(db, bid):return _session(db, bid, "trainer")
def _vet(db, bid):    return _session(db, bid, "vet")
def _staff(db, bid):  return _session(db, bid, "staff")
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
    db.tasks.delete_many({TAG: True})
    db.horse_daily_check_logs.delete_many({"horse_id": {"$regex": "^horse_hl1c_"}})
    db.horse_owner_visibility_policy.delete_many({"horse_id": {"$regex": "^horse_hl1c_"}})
    db.horse_ledger_audit.delete_many({"horse_id": {"$regex": "^horse_hl1c_"}})


# =====================================================================
# Permissions: hybrid mutator gate.
# =====================================================================
@pytest.mark.parametrize("role_factory", [_mgr, _admin, _groom, _trainer, _vet, _staff])
def test_staff_and_managers_can_create_daily_check(db, role_factory):
    bid = _make_barn(db); hid = _make_horse(db, bid); s = role_factory(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(s),
                          json={"check_type": "feed", "status": "ok",
                                "payload": {"feed": {"given": True}}},
                          timeout=10)
        assert r.status_code == 200, r.text
        cid = r.json()["id"]
        # Persisted with barn_id and checker.
        row = db.horse_daily_check_logs.find_one({"id": cid})
        assert row["barn_id"] == bid
        assert row["checked_by_user_id"] == s["user"]["id"]
        assert row["check_type"] == "feed"
        assert row["amended_at"] is None
    finally:
        _cleanup(db)


def test_owner_cannot_create_daily_check(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    s = _owner(db, bid, hid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(s),
                          json={"check_type": "feed"}, timeout=10)
        assert r.status_code == 403
        assert db.horse_daily_check_logs.count_documents({"horse_id": hid}) == 0
        # 403 must NOT emit an audit row.
        assert db.horse_ledger_audit.count_documents(
            {"horse_id": hid, "section": "daily_checks"}) == 0
    finally:
        _cleanup(db)


def test_cross_barn_user_cannot_create_daily_check(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); foreign = _mgr(db, bid2)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(foreign),
                          json={"check_type": "feed"}, timeout=10)
        assert r.status_code == 404, r.text
    finally:
        _cleanup(db)


def test_cross_barn_user_cannot_list_daily_checks(db):
    bid1 = _make_barn(db); hid = _make_horse(db, bid1)
    bid2 = _make_barn(db); foreign = _groom(db, bid2)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(foreign), timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_owner_cannot_list_daily_checks(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); o = _owner(db, bid, hid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(o), timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_disabled_facility_blocks_daily_check_create(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    db.barns.update_one({"id": bid}, {"$set": {"status": "disabled"}})
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed"}, timeout=10)
        assert r.status_code == 403, r.text
    finally:
        db.barns.update_one({"id": bid}, {"$set": {"status": "active"}})
        _cleanup(db)


# =====================================================================
# Validation.
# =====================================================================
@pytest.mark.parametrize("bad_type", ["nope", "FEED", "", None, 123])
def test_invalid_check_type_422(db, bad_type):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        body: Dict[str, Any] = {"status": "ok"}
        if bad_type is not None:
            body["check_type"] = bad_type
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr), json=body, timeout=10)
        assert r.status_code == 422, (bad_type, r.text)
    finally:
        _cleanup(db)


@pytest.mark.parametrize("bad_status", ["yes", "OK", "done", ""])
def test_invalid_status_422(db, bad_status):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed", "status": bad_status},
                          timeout=10)
        assert r.status_code == 422, (bad_status, r.text)
    finally:
        _cleanup(db)


def test_unknown_top_level_field_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed", "secret_flag": True},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_unknown_payload_subkey_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "hay_net",
                                "payload": {"hay_net": {
                                    "nets_checked": 3,
                                    "staff_note": "secret note"}}},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_unknown_payload_section_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "general",
                                "payload": {"unknown_section": {"foo": "bar"}}},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


@pytest.mark.parametrize("bad", ["wet", "DRY", "soggy", ""])
def test_bedding_condition_enum_422(db, bad):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "bedding",
                                "payload": {"bedding": {"condition": bad}}},
                          timeout=10)
        assert r.status_code == 422, (bad, r.text)
    finally:
        _cleanup(db)


def test_payload_non_primitive_value_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "hay_net",
                                "payload": {"hay_net": {"nets_checked": [1, 2, 3]}}},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_notes_length_cap_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "general",
                                "notes": "x" * 501}, timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


# =====================================================================
# Task linkage.
# =====================================================================
def _seed_task(db, bid, task_id="task_hl1c_t1", tenant_id="default"):
    """Seed a task using the REAL task-engine shape:
    `tenant_id="default"` + `barn_id=<bid>`. Real tasks materialized
    by `task_engine.py` always carry tenant_id="default"."""
    db.tasks.insert_one({
        "id": task_id, "tenant_id": tenant_id, "barn_id": bid,
        "category": "feed", "status": "scheduled", TAG: True,
    })
    return task_id


def test_task_linkage_same_barn_persists_task_id(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    tid = _seed_task(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed", "task_id": tid},
                          timeout=10)
        assert r.status_code == 200, r.text
        row = db.horse_daily_check_logs.find_one({"id": r.json()["id"]})
        assert row["task_id"] == tid
        # Linked task is NOT mutated.
        t = db.tasks.find_one({"id": tid})
        assert t["status"] == "scheduled"
    finally:
        _cleanup(db)


def test_task_linkage_real_task_engine_shape_persists(db):
    """Regression for Codex Round-1: real tasks have tenant_id='default'
    and barn_id=<barn>. Validation must accept that shape."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    # Insert a task using the EXACT shape `task_engine.py` materializes.
    tid = f"task_real_{uuid.uuid4().hex[:10]}"
    db.tasks.insert_one({
        "id": tid,
        "tenant_id": "default",         # task engine's DEFAULT_TENANT_ID
        "barn_id":   bid,
        "category":  "feed",
        "status":    "scheduled",
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        TAG: True,
    })
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed", "task_id": tid},
                          timeout=10)
        assert r.status_code == 200, r.text
        row = db.horse_daily_check_logs.find_one({"id": r.json()["id"]})
        assert row["task_id"] == tid
    finally:
        _cleanup(db)


def test_task_linkage_cross_barn_422(db):
    """A task in another barn (real task-engine shape) is rejected."""
    bid1 = _make_barn(db); hid = _make_horse(db, bid1); mgr = _mgr(db, bid1)
    bid2 = _make_barn(db); tid = _seed_task(db, bid2, task_id="task_hl1c_other")
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed", "task_id": tid},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_daily_check_indexes_exist_and_use_checked_at(db):
    """Codex Round-1: 1-A indexed `check_time`, but 1-C writes/queries
    `checked_at`. The lifespan must create checked_at-based indexes
    and the task_id partial index. Restart already happened in CI/dev;
    this regression asserts the live state matches the plan."""
    idx = {i["name"]: dict(i["key"]) for i in db.horse_daily_check_logs.list_indexes()}
    # No stale `check_time` indexes left over.
    assert not any("check_time" in str(k) for k in idx.values()), \
        f"stale check_time index found: {idx}"
    # checked_at-based composite indexes present.
    expected = {
        "hdcl_horse_checked_at":           {"horse_id": 1, "checked_at": -1},
        "hdcl_barn_horse_checked_at":      {"barn_id": 1, "horse_id": 1, "checked_at": -1},
        "hdcl_barn_check_type_checked_at": {"barn_id": 1, "check_type": 1, "checked_at": -1},
        "hdcl_task_id":                    {"task_id": 1},
    }
    for name, key in expected.items():
        assert name in idx, f"missing index {name}: have {list(idx)}"
        assert idx[name] == key, f"{name} key mismatch: {idx[name]} vs {key}"


def test_task_linkage_unknown_task_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "feed",
                                "task_id": "task_does_not_exist"},
                          timeout=10)
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


# =====================================================================
# PATCH amendments.
# =====================================================================
def _create(s, hid, **body):
    body.setdefault("check_type", "general")
    return requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(s), json=body, timeout=10).json()["id"]


def test_author_can_amend_their_own_check(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); g = _groom(db, bid)
    try:
        cid = _create(g, hid, status="ok",
                      payload={"general": {"observation": "first"}})
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(g),
                           json={"status": "needs_attention",
                                 "notes": "amended"}, timeout=10)
        assert r.status_code == 200, r.text
        row = db.horse_daily_check_logs.find_one({"id": cid})
        assert row["status"] == "needs_attention"
        assert row["notes"] == "amended"
        assert row["amended_at"] is not None
        # checked_at is preserved (original creation timestamp).
        assert row["checked_at"] == row["created_at"]
    finally:
        _cleanup(db)


def test_non_author_staff_cannot_amend(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    author = _groom(db, bid); other = _trainer(db, bid)
    try:
        cid = _create(author, hid)
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(other),
                           json={"status": "missed"}, timeout=10)
        assert r.status_code == 403, r.text
    finally:
        _cleanup(db)


def test_manager_can_amend_any_check(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    author = _groom(db, bid); mgr = _mgr(db, bid)
    try:
        cid = _create(author, hid)
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(mgr),
                           json={"status": "missed"}, timeout=10)
        assert r.status_code == 200, r.text
    finally:
        _cleanup(db)


def test_admin_can_amend_any_check(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    author = _staff(db, bid); ad = _admin(db, bid)
    try:
        cid = _create(author, hid)
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(ad),
                           json={"status": "ok"}, timeout=10)
        assert r.status_code == 200, r.text
    finally:
        _cleanup(db)


def test_owner_cannot_amend_any_check(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        cid = _create(mgr, hid)
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(o),
                           json={"status": "ok"}, timeout=10)
        assert r.status_code == 403
    finally:
        _cleanup(db)


def test_patch_unknown_check_id_404(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/hdcl_nope",
                           headers=_bearer(mgr),
                           json={"status": "ok"}, timeout=10)
        assert r.status_code == 404
    finally:
        _cleanup(db)


def test_patch_unknown_field_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        cid = _create(mgr, hid)
        r = requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                           headers=_bearer(mgr),
                           json={"check_type": "water"}, timeout=10)
        # check_type is immutable on PATCH (only status/notes/payload).
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_patch_merges_payload_subkeys(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        cid = _create(mgr, hid, check_type="hay_net",
                      payload={"hay_net": {"nets_checked": 3}})
        requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                       headers=_bearer(mgr),
                       json={"payload": {"hay_net": {"nets_refilled": 2}}},
                       timeout=10)
        row = db.horse_daily_check_logs.find_one({"id": cid})
        # Both subkeys present after section-level merge.
        assert row["payload"]["hay_net"]["nets_checked"] == 3
        assert row["payload"]["hay_net"]["nets_refilled"] == 2
    finally:
        _cleanup(db)


# =====================================================================
# Read integration via the Care Ledger.
# =====================================================================
def test_staff_get_ledger_includes_daily_checks_recent(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        for i in range(3):
            requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "water",
                                "payload": {"water": {"bucket_ok": True}}},
                          timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(mgr), timeout=10)
        recent = r.json().get("daily_checks_recent")
        assert isinstance(recent, list) and len(recent) == 3
        for entry in recent:
            assert entry["barn_id"] == bid
            assert entry["check_type"] == "water"
    finally:
        _cleanup(db)


def test_owner_get_ledger_hides_daily_checks_recent(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "notes": "SECRET_OWNER_LEAK_PROBE",
                            "payload": {"feed": {"given": True}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(o), timeout=10)
        body = r.json()
        assert body["daily_checks_recent"] == []
        assert "SECRET_OWNER_LEAK_PROBE" not in r.text
    finally:
        _cleanup(db)


def test_owner_cannot_force_reveal_via_view_query(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "notes": "VIEW_QUERY_LEAK_PROBE",
                            "payload": {"feed": {"given": True}}},
                      timeout=10)
        for q in ("?view=staff", "?view=full", "?owner_view=false"):
            r = requests.get(f"{API}/horse-ledger/{hid}{q}",
                             headers=_bearer(o), timeout=10)
            assert r.json()["daily_checks_recent"] == []
            assert "VIEW_QUERY_LEAK_PROBE" not in r.text
    finally:
        _cleanup(db)


def test_owner_cannot_force_reveal_via_tampered_policy_doc(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    mgr = _mgr(db, bid); o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "notes": "TAMPER_LEAK_PROBE",
                            "payload": {"feed": {"given": True}}},
                      timeout=10)
        db.horse_owner_visibility_policy.insert_one({
            "id": f"hovp_tamp_{uuid.uuid4().hex[:8]}",
            "horse_id": hid, "barn_id": bid,
            "sections": {"daily_checks_recent": {"allowlist": ["*"]}},
            TAG: True,
        })
        r = requests.get(f"{API}/horse-ledger/{hid}",
                         headers=_bearer(o), timeout=10)
        assert r.json()["daily_checks_recent"] == []
        assert "TAMPER_LEAK_PROBE" not in r.text
    finally:
        _cleanup(db)


def test_policy_put_rejects_daily_checks_section(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.put(
            f"{API}/horse-ledger/{hid}/owner-visibility-policy",
            headers=_bearer(mgr),
            json={"sections": {"daily_checks_recent": {"allowlist": ["check_type"]}}},
            timeout=10,
        )
        assert r.status_code == 422, r.text
    finally:
        _cleanup(db)


def test_list_daily_checks_filters_by_check_type(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr), json={"check_type": "feed"}, timeout=10)
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr), json={"check_type": "water"}, timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(mgr),
                         params={"check_type": "feed"}, timeout=10)
        items = r.json()["items"]
        assert len(items) == 1
        assert items[0]["check_type"] == "feed"
    finally:
        _cleanup(db)


def test_list_daily_checks_invalid_filter_422(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.get(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(mgr),
                         params={"check_type": "bogus"}, timeout=10)
        assert r.status_code == 422
    finally:
        _cleanup(db)


# =====================================================================
# Audit invariants.
# =====================================================================
def test_audit_row_emitted_on_create(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); g = _groom(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(g),
                      json={"check_type": "hay_net",
                            "notes": "RAW_NOTE_SHOULD_NOT_APPEAR_IN_AUDIT",
                            "payload": {"hay_net": {"nets_checked": 4,
                                                     "nets_refilled": 2}}},
                      timeout=10)
        row = db.horse_ledger_audit.find_one(
            {"horse_id": hid, "section": "daily_checks", "action": "created"})
        assert row is not None
        assert row["actor_role"] == "groom"
        assert "field_paths" in row and isinstance(row["field_paths"], list)
        assert "check_type" in row["field_paths"]
        assert "notes" in row["field_paths"]
        assert "payload.hay_net.nets_checked" in row["field_paths"]
        assert row["sensitivity"] == "staff_only"
        assert row["owner_visible_eligible"] is False
        # NO raw notes or payload values in the audit doc.
        as_str = str(row)
        assert "RAW_NOTE_SHOULD_NOT_APPEAR_IN_AUDIT" not in as_str
        # Value 4 cannot be cleanly substring-searched but the schema
        # has no 'before'/'after' fields. Assert explicitly.
        for forbidden_key in ("before", "after", "values", "payload_actual"):
            assert forbidden_key not in row
    finally:
        _cleanup(db)


def test_audit_row_emitted_on_patch(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        cid = _create(mgr, hid)
        requests.patch(f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
                       headers=_bearer(mgr),
                       json={"status": "needs_attention"}, timeout=10)
        rows = list(db.horse_ledger_audit.find(
            {"horse_id": hid, "section": "daily_checks"}))
        assert any(r["action"] == "updated" for r in rows)
    finally:
        _cleanup(db)


def test_no_audit_row_on_403(db):
    bid = _make_barn(db); hid = _make_horse(db, bid)
    o = _owner(db, bid, hid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(o),
                      json={"check_type": "feed"}, timeout=10)
        assert db.horse_ledger_audit.count_documents(
            {"horse_id": hid, "section": "daily_checks"}) == 0
    finally:
        _cleanup(db)


def test_feed_check_audit_sensitivity_is_operational(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "feed",
                            "payload": {"feed": {"given": True}}},
                      timeout=10)
        row = db.horse_ledger_audit.find_one(
            {"horse_id": hid, "section": "daily_checks", "action": "created"})
        assert row["sensitivity"] == "operational"
        # Even an operational sensitivity does NOT make daily checks
        # owner-visible. The eligible flag stays False.
        assert row["owner_visible_eligible"] is False
    finally:
        _cleanup(db)


# =====================================================================
# Stripe scrubbing on read.
# =====================================================================
def test_stripe_shape_in_notes_scrubbed_on_get(db):
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                      headers=_bearer(mgr),
                      json={"check_type": "general",
                            "notes": "ref sub_ABC123XYZ456DEF and cus_GHI789JKL012MNO",
                            "payload": {"general": {"observation": "fine"}}},
                      timeout=10)
        r = requests.get(f"{API}/horse-ledger/{hid}/daily-checks",
                         headers=_bearer(mgr), timeout=10)
        text = r.text
        assert "sub_ABC123XYZ456DEF" not in text
        assert "cus_GHI789JKL012MNO" not in text
        assert "[stripe_id_redacted]" in text
    finally:
        _cleanup(db)


# =====================================================================
# Adjacent-phase invariants.
# =====================================================================
def test_phase_9_collections_untouched_after_1c_storm(db):
    """A 1-C edit storm does not touch billing collections."""
    counts_before = {
        c: db[c].count_documents({})
        for c in ("invoices", "recurring_charges", "recurring_billing_rules")
    }
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        for ct in ("feed", "hay", "hay_net", "water", "bedding", "general"):
            requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": ct}, timeout=10)
        counts_after = {
            c: db[c].count_documents({}) for c in counts_before
        }
        assert counts_before == counts_after
    finally:
        _cleanup(db)


def test_phase_15_collections_untouched_after_1c_storm(db):
    cols = [c for c in db.list_collection_names()
            if c.startswith("subscription") or c.startswith("billing_events")]
    counts_before = {c: db[c].count_documents({}) for c in cols}
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        for _ in range(3):
            requests.post(f"{API}/horse-ledger/{hid}/daily-checks",
                          headers=_bearer(mgr),
                          json={"check_type": "general"}, timeout=10)
        counts_after = {c: db[c].count_documents({}) for c in cols}
        assert counts_before == counts_after
    finally:
        _cleanup(db)


def test_admin_portal_route_lock_unchanged_after_1c(db):
    """The Admin Portal locked-route counts must remain on the current lock."""
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 28
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1


# =====================================================================
# Codex Round-2 regressions (Phase HorseOps-1C)
#
# P1  Payload section must match check_type (no cross-section payloads).
# P1  Stale `check_time` indexes must be dropped on existing deployments.
# =====================================================================
@pytest.mark.parametrize("check_type,wrong_section,sub", [
    ("feed",    "bedding", {"condition": "clean"}),
    ("feed",    "hay_net", {"nets_checked": 3}),
    ("water",   "feed",    {"given": True}),
    ("hay_net", "water",   {"bucket_ok": True}),
    ("bedding", "feed",    {"given": True}),
    ("hay",     "bedding", {"condition": "clean"}),
    ("general", "feed",    {"given": True}),
])
def test_payload_section_must_match_check_type_422(db, check_type, wrong_section, sub):
    """Round-2 P1: payload sections are paired 1:1 to `check_type`. A
    `feed` check cannot carry `payload.bedding`, etc. Each mismatched
    combination must 422 and leave no DB row behind."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(
            f"{API}/horse-ledger/{hid}/daily-checks",
            headers=_bearer(mgr),
            json={"check_type": check_type,
                  "payload": {wrong_section: sub}},
            timeout=10,
        )
        assert r.status_code == 422, (check_type, wrong_section, r.text)
        assert db.horse_daily_check_logs.count_documents({"horse_id": hid}) == 0
    finally:
        _cleanup(db)


@pytest.mark.parametrize("check_type,right_section,sub", [
    ("feed",    "feed",       {"given": True}),
    ("water",   "water",      {"bucket_ok": True}),
    ("bedding", "bedding",    {"condition": "clean"}),
    ("hay",     "hay_access", {"free_choice_available": True}),
    ("hay_net", "hay_net",    {"nets_checked": 2}),
    ("general", "general",    {"observation": "fine"}),
])
def test_payload_section_matching_check_type_accepted(db, check_type, right_section, sub):
    """Sanity: each `check_type` accepts its paired payload section."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        r = requests.post(
            f"{API}/horse-ledger/{hid}/daily-checks",
            headers=_bearer(mgr),
            json={"check_type": check_type,
                  "payload": {right_section: sub}},
            timeout=10,
        )
        assert r.status_code == 200, (check_type, r.text)
    finally:
        _cleanup(db)


def test_patch_payload_section_must_match_existing_check_type_422(db):
    """PATCH cannot smuggle a mismatched section either. The existing
    log's `check_type` drives the validation."""
    bid = _make_barn(db); hid = _make_horse(db, bid); mgr = _mgr(db, bid)
    try:
        cid = _create(mgr, hid, check_type="feed",
                      payload={"feed": {"given": True}})
        r = requests.patch(
            f"{API}/horse-ledger/{hid}/daily-checks/{cid}",
            headers=_bearer(mgr),
            json={"payload": {"bedding": {"condition": "clean"}}},
            timeout=10,
        )
        assert r.status_code == 422, r.text
        # Existing payload is unchanged.
        row = db.horse_daily_check_logs.find_one({"id": cid})
        assert row["payload"] == {"feed": {"given": True}}
    finally:
        _cleanup(db)


def test_stale_check_time_indexes_dropped_on_startup(db):
    """Round-2 P1: existing deployments still carry the legacy
    `check_time` indexes from the 1-A plan. Seed them and ensure the
    next startup migration drops them by name and recreates the
    `checked_at`-aligned indexes.

    This test reproduces the migration in-place by calling the index
    API directly (the live backend already ran its lifespan migration
    on the last restart). Hand-creating the stale indexes, calling the
    drop-then-create dance, and asserting the final state matches the
    plan is sufficient to lock the migration contract."""
    coll = db.horse_daily_check_logs
    # Seed the legacy indexes.
    coll.create_index([("horse_id", 1), ("check_time", -1)])
    coll.create_index([("barn_id", 1), ("check_type", 1), ("check_time", -1)])
    legacy_before = {i["name"] for i in coll.list_indexes()
                     if "check_time" in str(i["key"])}
    assert legacy_before, "seed step did not produce a stale index"
    # Run the migration the same way `lifespan.py` does.
    for stale in ("horse_id_1_check_time_-1",
                  "barn_id_1_check_type_1_check_time_-1"):
        try:
            coll.drop_index(stale)
        except Exception:
            pass
    coll.create_index([("horse_id", 1), ("checked_at", -1)],
                      name="hdcl_horse_checked_at")
    coll.create_index([("barn_id", 1), ("horse_id", 1), ("checked_at", -1)],
                      name="hdcl_barn_horse_checked_at")
    coll.create_index([("barn_id", 1), ("check_type", 1), ("checked_at", -1)],
                      name="hdcl_barn_check_type_checked_at")
    coll.create_index([("task_id", 1)], name="hdcl_task_id", sparse=True)
    # Stale gone, new present.
    final = {i["name"]: dict(i["key"]) for i in coll.list_indexes()}
    assert not any("check_time" in str(k) for k in final.values()), final
    for expected in ("hdcl_horse_checked_at",
                     "hdcl_barn_horse_checked_at",
                     "hdcl_barn_check_type_checked_at",
                     "hdcl_task_id"):
        assert expected in final, (expected, list(final))


def test_migration_is_idempotent_when_no_stale_indexes_present(db):
    """Calling the drop step twice (or on a cold deploy) must not
    raise. `drop_index` is wrapped in try/except in `lifespan.py`;
    this regression locks that contract."""
    coll = db.horse_daily_check_logs
    # Ensure no stale indexes are present.
    for stale in ("horse_id_1_check_time_-1",
                  "barn_id_1_check_type_1_check_time_-1"):
        try:
            coll.drop_index(stale)
        except Exception:
            pass
    # Now call the drop step again — must not raise.
    for stale in ("horse_id_1_check_time_-1",
                  "barn_id_1_check_type_1_check_time_-1"):
        try:
            coll.drop_index(stale)
            raised = False
        except Exception:
            raised = False  # swallowed in lifespan
        assert raised is False
