"""Horse Passport transfer workflow tests.

The first transfer slice is intentionally owner-safe: it creates/accepts/cancels
TransferRequest rows, updates ownership on acceptance, and archives only the
selected safe categories.
"""
from __future__ import annotations

import os
import pathlib
import sys
import uuid
from datetime import datetime, timezone

import pytest
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

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
TAG = "_htransfer_test"


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role="horse_owner"):
    email = f"htransfer_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={
            "email": email,
            "password": "securepass1",
            "full_name": "Horse Transfer Test",
            "role": role,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _bearer(session):
    return {"Authorization": f"Bearer {session['token']}"}


def _make_barn(db, prefix="barn_htransfer"):
    bid = f"{prefix}_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": bid, "name": "Transfer Barn", "status": "active", TAG: True})
    return bid


def _put_user_in_barn(db, uid, bid, role):
    db.users.update_one({"id": uid}, {"$set": {"barn_id": bid, "role": role, TAG: True}})


def _owner(db, bid):
    s = _signup("horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, "horse_owner")
    return s


def _manager(db, bid):
    s = _signup("horse_owner")
    _put_user_in_barn(db, s["user"]["id"], bid, "barn_manager")
    return s


def _make_horse(db, bid, owner_id):
    hid = f"horse_htransfer_{uuid.uuid4().hex[:10]}"
    db.horses.insert_one({
        "id": hid,
        "barn_id": bid,
        "name": "Transfer Horse",
        "breed": "Appendix",
        "color": "Bay",
        "discipline": "Hunter",
        "status": "active",
        "owner_id": owner_id,
        "primary_owner_id": owner_id,
        "secondary_owner_ids": [owner_id],
        "created_at": datetime.now(timezone.utc).isoformat(),
        TAG: True,
    })
    return hid


def _seed_sensitive_ledger_rows(db, bid, hid):
    db.horse_care_profiles.insert_one({
        "id": f"hcp_{uuid.uuid4().hex[:10]}",
        "horse_id": hid,
        "barn_id": bid,
        "feeding": {
            "grain_feed_type": "Balancer",
            "schedule": [{"time": "07:00", "label": "AM", "staff_note": "DO NOT TRANSFER"}],
            "supplements": [{"name": "Vitamin E", "dosage": "STAFF ONLY"}],
            "staff_only_warnings": "bites at feed door",
        },
        "turnout": {
            "schedule": [{"time": "09:00", "label": "north", "injury_risk_notes": "private"}],
            "turnout_group": "quiet",
        },
        "handling_behavior": {"notes": "private handling warning"},
        TAG: True,
    })
    db.horse_daily_check_logs.insert_one({
        "horse_id": hid,
        "barn_id": bid,
        "notes": "raw daily check must not transfer",
        TAG: True,
    })
    db.horse_ledger_alerts.insert_one({
        "horse_id": hid,
        "barn_id": bid,
        "trigger": "private alert trigger",
        "severity": "urgent",
        TAG: True,
    })
    db.horse_equipment.insert_one({
        "id": f"eq_{uuid.uuid4().hex[:10]}",
        "horse_id": hid,
        "barn_id": bid,
        "category": "saddle",
        "label": "Private saddle note",
        "status": "active",
        TAG: True,
    })
    db.horse_owner_visibility_policy.insert_one({
        "horse_id": hid,
        "barn_id": bid,
        "sections": {
            "feeding": {"allowlist": ["grain_feed_type"]},
            "turnout": {"allowlist": []},
            "equipment": {"allowlist": []},
        },
        TAG: True,
    })


def _cleanup(db):
    db.users.delete_many({TAG: True})
    db.barns.delete_many({TAG: True})
    db.horses.delete_many({TAG: True})
    for coll in (
        "horse_transfer_requests",
        "horse_transfer_archives",
        "horse_care_profiles",
        "horse_daily_check_logs",
        "horse_ledger_alerts",
        "horse_ledger_audit",
        "horse_owner_visibility_policy",
        "audit_log",
    ):
        db[coll].delete_many({TAG: True})
    db.horse_transfer_requests.delete_many({"horse_id": {"$regex": "^horse_htransfer_"}})
    db.horse_transfer_archives.delete_many({"horse_id": {"$regex": "^horse_htransfer_"}})
    db.audit_log.delete_many({
        "action": {"$regex": "^horse_transfer\\."},
        "metadata.horse_id": {"$regex": "^horse_htransfer_"},
    })


def _create_transfer(hid, new_owner, headers, **overrides):
    payload = {
        "horse_id": hid,
        "new_owner_user_id": new_owner["user"]["id"],
        "categories": ["identity_public", "ownership_record", "care_summary"],
    }
    payload.update(overrides)
    return requests.post(f"{API}/horse-transfers", headers=headers, json=payload, timeout=20)


def test_create_transfer_and_export_preview_are_owner_safe(db):
    bid = _make_barn(db)
    old_owner = _owner(db, bid)
    new_owner = _owner(db, bid)
    hid = _make_horse(db, bid, old_owner["user"]["id"])
    _seed_sensitive_ledger_rows(db, bid, hid)
    try:
        created = _create_transfer(hid, new_owner, _bearer(old_owner))
        assert created.status_code == 200, created.text
        assert created.json()["status"] == "pending_acceptance"
        tid = created.json()["id"]

        preview = requests.get(
            f"{API}/horse-transfers/{tid}/export-preview",
            headers=_bearer(old_owner),
            timeout=20,
        )
        assert preview.status_code == 200, preview.text
        body = preview.json()
        assert body["policy_version"] == "horse-passport-transfer-v1"
        assert body["identity_public"]["name"] == "Transfer Horse"
        care = body["care_summary"]
        assert care["feeding"]["structured"] == {"grain_feed_type": "Balancer"}
        assert care["turnout"] is None
        assert care["equipment"] == []
        text = str(body)
        assert "DO NOT TRANSFER" not in text
        assert "STAFF ONLY" not in text
        assert "bites at feed door" not in text
        assert "private alert trigger" not in text
        assert "raw daily check must not transfer" not in text
        assert "staff_note" not in text
        assert "injury_risk_notes" not in text
        assert "Private saddle note" not in text
    finally:
        _cleanup(db)


def test_barn_manager_cannot_start_transfer_without_owner_approval(db):
    bid = _make_barn(db)
    old_owner = _owner(db, bid)
    new_owner = _owner(db, bid)
    manager = _manager(db, bid)
    hid = _make_horse(db, bid, old_owner["user"]["id"])
    try:
        r = _create_transfer(hid, new_owner, _bearer(manager))
        assert r.status_code == 403
        assert "current owner" in r.text
    finally:
        _cleanup(db)


def test_blocked_transfer_categories_are_rejected(db):
    bid = _make_barn(db)
    old_owner = _owner(db, bid)
    new_owner = _owner(db, bid)
    hid = _make_horse(db, bid, old_owner["user"]["id"])
    try:
        r = _create_transfer(
            hid,
            new_owner,
            _bearer(old_owner),
            categories=["identity_public", "messages"],
        )
        assert r.status_code == 422
        assert "blocked pending Product/Legal" in r.text
    finally:
        _cleanup(db)


def test_cancel_prevents_later_acceptance(db):
    bid = _make_barn(db)
    old_owner = _owner(db, bid)
    new_owner = _owner(db, bid)
    hid = _make_horse(db, bid, old_owner["user"]["id"])
    try:
        created = _create_transfer(hid, new_owner, _bearer(old_owner))
        assert created.status_code == 200, created.text
        tid = created.json()["id"]
        canceled = requests.post(
            f"{API}/horse-transfers/{tid}/cancel",
            headers=_bearer(old_owner),
            json={"reason": "sale changed"},
            timeout=20,
        )
        assert canceled.status_code == 200, canceled.text
        assert canceled.json()["status"] == "canceled"

        accepted = requests.post(
            f"{API}/horse-transfers/{tid}/accept",
            headers=_bearer(new_owner),
            json={},
            timeout=20,
        )
        assert accepted.status_code == 409
    finally:
        _cleanup(db)


def test_accept_updates_owner_and_cuts_off_prior_owner_summary_access(db):
    source_bid = _make_barn(db, "source_barn_htransfer")
    destination_bid = _make_barn(db, "dest_barn_htransfer")
    old_owner = _owner(db, source_bid)
    new_owner = _owner(db, destination_bid)
    hid = _make_horse(db, source_bid, old_owner["user"]["id"])
    manager = _manager(db, source_bid)
    try:
        created = _create_transfer(
            hid,
            new_owner,
            _bearer(old_owner),
            destination_barn_id=destination_bid,
        )
        assert created.status_code == 200, created.text
        assert created.json()["status"] == "owner_approved"
        assert created.json()["requires_barn_approval"] is True
        tid = created.json()["id"]

        blocked_accept = requests.post(
            f"{API}/horse-transfers/{tid}/accept",
            headers=_bearer(new_owner),
            json={},
            timeout=20,
        )
        assert blocked_accept.status_code == 409
        assert "Barn approval is required" in blocked_accept.text

        barn_approved = requests.post(
            f"{API}/horse-transfers/{tid}/barn-approve",
            headers=_bearer(manager),
            json={"reason": "custody release approved"},
            timeout=20,
        )
        assert barn_approved.status_code == 200, barn_approved.text
        assert barn_approved.json()["status"] == "barn_approved"

        accepted = requests.post(
            f"{API}/horse-transfers/{tid}/accept",
            headers=_bearer(new_owner),
            json={},
            timeout=20,
        )
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["status"] == "accepted"

        horse = db.horses.find_one({"id": hid})
        assert horse["owner_id"] == new_owner["user"]["id"]
        assert horse["primary_owner_id"] == new_owner["user"]["id"]
        assert old_owner["user"]["id"] not in horse.get("secondary_owner_ids", [])
        assert horse["barn_id"] == destination_bid

        old_read = requests.get(
            f"{API}/horse-ledger/{hid}/owner-summary",
            headers=_bearer(old_owner),
            timeout=20,
        )
        assert old_read.status_code == 404

        new_read = requests.get(
            f"{API}/horse-ledger/{hid}/owner-summary",
            headers=_bearer(new_owner),
            timeout=20,
        )
        assert new_read.status_code == 200, new_read.text

        archive = db.horse_transfer_archives.find_one({"transfer_id": tid})
        assert archive is not None
        assert archive["snapshot"]["policy_version"] == "horse-passport-transfer-v1"
    finally:
        _cleanup(db)
