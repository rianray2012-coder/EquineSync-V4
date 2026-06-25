"""tests/test_horse_ledger_1g.py - HorseOps-1G platform inspection.

1G adds the deferred Admin Portal horse directory / Care Ledger summary.
It is platform-only and read-only. The detail endpoint is intentionally
summary-only: no raw daily-check payloads, alert triggers, source IDs,
staff notes, owner request messages, or audit diffs cross the boundary.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = pathlib.Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

sys.path.insert(0, str(BACKEND))
load_dotenv(BACKEND / ".env")


def _base_url() -> str:
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v.rstrip("/")
    env = FRONTEND / ".env"
    if env.is_file():
        for line in env.read_text().splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip().rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not configured")


BASE = _base_url()
API = f"{BASE}/api"
TAG = "_hl1g_test"


@pytest.fixture
def db():
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        raise RuntimeError("MONGO_URL not configured; export it or add backend/.env")
    c = MongoClient(mongo_url)
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role: str = "horse_owner") -> dict:
    email = f"hl1g_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "HL1G Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


def _platform_session(db, platform_role: str = "platform_admin") -> dict:
    s = _signup()
    db.users.update_one(
        {"id": s["user"]["id"]},
        {"$set": {"platform_role": platform_role, TAG: True}},
    )
    return s


def _barn_user_session(db, barn_id: str, role: str = "admin") -> dict:
    # Public signup may reject privileged barn roles. Create a normal user,
    # then shape the barn-scoped test account directly in Mongo.
    s = _signup(role="horse_owner")
    db.users.update_one(
        {"id": s["user"]["id"]},
        {"$set": {"barn_id": barn_id, "role": role, TAG: True}},
    )
    return s


def _make_barn(db, name: str) -> str:
    bid = f"barn_hl1g_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({
        "id": bid, "name": name, "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(), TAG: True,
    })
    return bid


def _make_horse(db, barn_id: str, name: str = "1G Horse") -> str:
    hid = f"horse_hl1g_{uuid.uuid4().hex[:10]}"
    db.horses.insert_one({
        "id": hid, "barn_id": barn_id, "name": name, "status": "active",
        "breed": "Appendix", "age": 9,
        "primary_owner_id": "owner_should_not_cross",
        "microchip_number": "chip_should_not_cross",
        "private_note": "staff_only_horse_note_should_not_cross",
        "created_at": datetime.now(timezone.utc).isoformat(),
        TAG: True,
    })
    return hid


def _cleanup(db):
    rgx = {"$regex": "^horse_hl1g_"}
    db.users.delete_many({TAG: True})
    db.barns.delete_many({TAG: True})
    db.horses.delete_many({"id": rgx})
    db.horse_equipment.delete_many({"horse_id": rgx})
    db.horse_daily_check_logs.delete_many({"horse_id": rgx})
    db.horse_ledger_alerts.delete_many({"horse_id": rgx})
    db.service_requests.delete_many({"horse_id": rgx})
    db.horse_owner_visibility_policy.delete_many({"horse_id": rgx})
    db.audit_log.delete_many({"resource_id": {"$in": ["horses"]}})


def test_platform_horse_list_is_cross_facility_and_scrubbed(db):
    b1 = _make_barn(db, "One")
    b2 = _make_barn(db, "Two")
    h1 = _make_horse(db, b1, "Ledger One sub_12345678901234")
    h2 = _make_horse(db, b2, "Ledger Two")
    plat = _platform_session(db, "support_admin")
    try:
        r = requests.get(
            f"{API}/admin/portal/horses?q=Ledger&limit=10",
            headers=_bearer(plat), timeout=10,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        ids = {x["id"] for x in body["items"]}
        assert {h1, h2}.issubset(ids)

        payload = json.dumps(body)
        assert "owner_should_not_cross" not in payload
        assert "chip_should_not_cross" not in payload
        assert "staff_only_horse_note_should_not_cross" not in payload
        assert "sub_12345678901234" not in payload
        assert "[stripe_id_redacted]" in payload
    finally:
        _cleanup(db)


def test_horse_admin_surface_blocks_non_platform_and_wrong_platform_role(db):
    bid = _make_barn(db, "Blocked")
    _make_horse(db, bid)
    barn_admin = _barn_user_session(db, bid, "admin")
    billing = _platform_session(db, "billing_admin")
    try:
        r1 = requests.get(f"{API}/admin/portal/horses", headers=_bearer(barn_admin), timeout=10)
        r2 = requests.get(f"{API}/admin/portal/horses", headers=_bearer(billing), timeout=10)
        assert r1.status_code == 403
        assert r2.status_code == 403
    finally:
        _cleanup(db)


def test_horse_ledger_summary_is_counts_only_no_sensitive_payloads(db):
    bid = _make_barn(db, "Summary")
    hid = _make_horse(db, bid)
    now = datetime.now(timezone.utc)
    db.horse_equipment.insert_one({
        "id": f"eq_{uuid.uuid4().hex}", "horse_id": hid, "barn_id": bid,
        "category": "hay_net", "label": "Net A", "status": "active", TAG: True,
    })
    db.horse_daily_check_logs.insert_one({
        "id": f"check_{uuid.uuid4().hex}", "horse_id": hid, "barn_id": bid,
        "check_type": "hay_net", "checked_at": now.isoformat(),
        "payload": {"hay_net": {"nets_refilled": 0}, "staff_note": "daily_secret_note"},
        TAG: True,
    })
    db.horse_ledger_alerts.insert_one({
        "id": f"alert_{uuid.uuid4().hex}", "horse_id": hid, "barn_id": bid,
        "alert_type": "hay_net", "severity": "urgent", "severity_rank": 2,
        "status": "open", "source_check_id": "source_check_secret",
        "last_seen_at": now.isoformat(), "triggers": ["hay_net.nets_refilled=0"],
        TAG: True,
    })
    db.service_requests.insert_one({
        "id": f"osr_{uuid.uuid4().hex}", "source": "owner_care_ledger",
        "horse_id": hid, "barn_id": bid, "owner_user_id": "owner_x",
        "status": "new", "request_type": "care_status",
        "message": "owner message should not cross",
        "created_at": now.isoformat(), TAG: True,
    })
    db.horse_owner_visibility_policy.insert_one({
        "horse_id": hid, "barn_id": bid, "policy_version": 3,
        "sections": {"feeding": {"allowlist": ["schedule"]}},
        "updated_at": (now - timedelta(minutes=5)).isoformat(), TAG: True,
    })
    plat = _platform_session(db, "platform_admin")
    try:
        r = requests.get(
            f"{API}/admin/portal/horses/{hid}/ledger-summary",
            headers=_bearer(plat), timeout=10,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        summary = body["ledger_summary"]
        assert summary["equipment_active"] == 1
        assert summary["daily_checks_24h"] == 1
        assert summary["active_alerts"] == 1
        assert summary["active_alerts_by_severity"]["urgent"] == 1
        assert summary["owner_requests_open"] == 1
        assert summary["visibility_policy"]["configured"] is True
        assert summary["visibility_policy"]["sections"] == ["feeding"]

        payload = json.dumps(body)
        for forbidden in (
            "daily_secret_note",
            "hay_net.nets_refilled=0",
            "source_check_secret",
            "owner message should not cross",
            "triggers",
            "source_check_id",
            "payload",
            "message",
        ):
            assert forbidden not in payload
    finally:
        _cleanup(db)


def test_horse_admin_reads_emit_audit_and_self_reads_are_excluded(db):
    from routes.admin_portal._helpers import _ACTIVITY_EXCLUDE_PREFIXES

    bid = _make_barn(db, "Audit")
    hid = _make_horse(db, bid)
    plat = _platform_session(db, "super_admin")
    try:
        before_list = db.audit_log.count_documents({"action": "admin.portal.read.horses"})
        before_detail = db.audit_log.count_documents({"action": "admin.portal.read.horse_ledger_summary"})
        assert requests.get(f"{API}/admin/portal/horses", headers=_bearer(plat), timeout=10).status_code == 200
        assert requests.get(
            f"{API}/admin/portal/horses/{hid}/ledger-summary",
            headers=_bearer(plat), timeout=10,
        ).status_code == 200
        assert db.audit_log.count_documents({"action": "admin.portal.read.horses"}) == before_list + 1
        assert db.audit_log.count_documents({"action": "admin.portal.read.horse_ledger_summary"}) == before_detail + 1
        assert "admin.portal.read.horses" in _ACTIVITY_EXCLUDE_PREFIXES
        assert "admin.portal.read.horse_ledger_summary" in _ACTIVITY_EXCLUDE_PREFIXES
    finally:
        _cleanup(db)


def test_admin_portal_route_lock_includes_1g_horse_routes():
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES, LOCKED_PATCH_ROUTES,
    )
    assert len(LOCKED_GET_ROUTES) == 28
    assert len(LOCKED_POST_ROUTES) == 10
    assert len(LOCKED_PATCH_ROUTES) == 1
    assert "/api/admin/portal/horses" in LOCKED_GET_ROUTES
    assert "/api/admin/portal/horses/{horse_id}/ledger-summary" in LOCKED_GET_ROUTES


def test_admin_horses_frontend_replaces_placeholder():
    app_js = (FRONTEND / "src" / "App.js").read_text()
    page_js = (FRONTEND / "src" / "pages" / "admin" / "AdminHorses.jsx").read_text()
    assert 'import AdminHorses from "./pages/admin/AdminHorses";' in app_js
    assert 'path="horses" element={<AdminHorses />}' in app_js
    assert 'AdminPlaceholder section="Horses"' not in app_js
    for forbidden in ("daily-check payloads", "alert triggers", "source_check_id", "owner request messages"):
        assert forbidden in page_js
