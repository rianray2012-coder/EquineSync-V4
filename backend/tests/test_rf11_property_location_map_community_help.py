from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

from routes.backlog import build_router as build_backlog_router


ROOT = Path(__file__).resolve().parents[2]


def _value(doc: Dict[str, Any], key: str) -> Any:
    actual: Any = doc
    for part in key.split("."):
        if not isinstance(actual, dict):
            return None
        actual = actual.get(part)
    return actual


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        actual = _value(doc, key)
        if isinstance(expected, dict) and "$exists" in expected:
            exists = actual is not None
            if exists is not bool(expected["$exists"]):
                return False
        elif isinstance(expected, dict) and "$in" in expected:
            if actual not in expected["$in"]:
                return False
        elif actual != expected:
            return False
    return True


def _project(doc: Dict[str, Any], projection: Dict[str, Any] | None) -> Dict[str, Any]:
    if not projection or projection == {"_id": 0}:
        return {k: v for k, v in doc.items() if k != "_id"}
    included = {k for k, v in projection.items() if v and k != "_id"}
    return {k: doc.get(k) for k in included if k in doc}


class _Cursor:
    def __init__(self, rows: List[Dict[str, Any]], projection=None):
        self.rows = rows
        self.projection = projection

    def sort(self, field, direction=1):
        if isinstance(field, list):
            for name, order in reversed(field):
                self.rows.sort(key=lambda row: str(_value(row, name) or ""), reverse=order < 0)
            return self
        if field:
            self.rows.sort(key=lambda row: str(_value(row, field) or ""), reverse=direction < 0)
        return self

    async def to_list(self, limit):
        return [_project(row, self.projection) for row in self.rows[:limit]]


class _Collection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if _matches(row, query):
                return _project(row, projection)
        return None

    def find(self, query=None, projection=None):
        return _Cursor([row for row in self.rows if _matches(row, query or {})], projection)

    async def insert_one(self, doc):
        self.rows.append(dict(doc))

    async def update_one(self, query, update, upsert=False):
        for row in self.rows:
            if _matches(row, query):
                row.update(update.get("$set", {}))
                return type("Result", (), {"matched_count": 1})()
        if upsert:
            self.rows.append(dict(update.get("$set", {})))
            return type("Result", (), {"matched_count": 1})()
        return type("Result", (), {"matched_count": 0})()


class _FakeDB:
    def __init__(self):
        self.barn_location_share_settings = _Collection([
            {
                "id": "location-share",
                "barn_id": "barn-1",
                "enabled": True,
                "title": "Barn Location Board",
                "note": "Owner-safe barn location view",
                "share_path": "/barn-locations",
                "created_at": "2026-07-06T08:00:00Z",
                "updated_at": "2026-07-06T09:00:00Z",
                "created_by": "manager-1",
                "updated_by": "admin-1",
            }
        ])
        self.arena_schedule_share_settings = _Collection([
            {
                "id": "arena-share",
                "barn_id": "barn-1",
                "enabled": True,
                "title": "Arena Schedule",
                "note": "Shared arena availability",
                "share_path": "/arena-schedule",
                "created_at": "2026-07-06T08:00:00Z",
                "updated_at": "2026-07-06T09:00:00Z",
                "created_by": "manager-1",
                "updated_by": "admin-1",
            }
        ])
        self.stall_assignments = _Collection([
            {
                "id": "stall-1",
                "barn_id": "barn-1",
                "data": {
                    "horse_name": "Juniper",
                    "stall_id": "A1",
                    "barn_area": "Main Barn",
                    "row": "A",
                    "column": "1",
                    "status": "occupied",
                    "notes": "Internal medication watch",
                },
            }
        ])
        self.pasture_schedules = _Collection([
            {
                "id": "pasture-1",
                "barn_id": "barn-1",
                "data": {
                    "pasture": "North Field",
                    "group_name": "Morning turnout",
                    "horse_names": "Juniper, Willow",
                    "start_time": "08:00",
                    "end_time": "10:00",
                    "status": "active",
                    "weather_rule": "Hold if lightning within 10 miles",
                },
            }
        ])
        self.arena_schedule_blocks = _Collection([
            {
                "id": "arena-shared",
                "barn_id": "barn-1",
                "data": {
                    "arena_name": "Indoor",
                    "title": "Owner lesson",
                    "date": "2026-07-06",
                    "start_time": "09:00",
                    "end_time": "10:00",
                    "status": "reserved",
                    "visibility": "shared_with_owners",
                    "horse_name": "Juniper",
                    "owner_name": "Private Owner",
                    "notes": "Internal staff handoff note",
                    "source_request_id": "req-1",
                },
            },
            {
                "id": "arena-internal",
                "barn_id": "barn-1",
                "data": {
                    "arena_name": "Indoor",
                    "title": "Staff training",
                    "date": "2026-07-06",
                    "start_time": "11:00",
                    "end_time": "12:00",
                    "status": "reserved",
                    "visibility": "staff_only",
                    "horse_name": "Willow",
                    "owner_name": "Another Owner",
                    "notes": "Staff-only correction session",
                },
            },
        ])
        self.qr_horse_ids = _Collection([
            {
                "id": "qr-1",
                "barn_id": "barn-1",
                "status": "active",
                "data": {
                    "horse_name": "Juniper",
                    "qr_code": "JUNIPER-A1",
                    "profile_url": "/horses/horse-1",
                    "stall_location": "Main Barn A1",
                },
            }
        ])
        self.backlog_audit_events = _Collection([])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user: Dict[str, Any]):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    def new_id():
        return "new-id"

    app = FastAPI()
    app.include_router(build_backlog_router(db=db, get_current_user=get_current_user, new_id=new_id), prefix="/api")
    return TestClient(app), db


def test_owner_location_share_requires_enabled_publish_state():
    client, db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})
    db.barn_location_share_settings.rows[0]["enabled"] = False

    response = client.get("/api/barn-location-share")

    assert response.status_code == 403


def test_owner_location_share_omits_internal_notes_and_weather_rules():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})

    response = client.get("/api/barn-location-share")
    assert response.status_code == 200
    body = response.json()

    assert body["share_state"] == {
        "enabled": True,
        "state": "published",
        "audience": "owner_parent",
        "source": "barn_admin_share_setting",
    }
    assert body["share"] == {
        "id": "location-share",
        "enabled": True,
        "title": "Barn Location Board",
        "note": "Owner-safe barn location view",
        "share_path": "/barn-locations",
        "updated_at": "2026-07-06T09:00:00Z",
    }
    assert "created_by" not in body["share"]
    assert "updated_by" not in body["share"]
    assert "created_at" not in body["share"]
    assert body["stalls"][0]["horse_name"] == "Juniper"
    assert "notes" not in body["stalls"][0]
    assert "weather_rule" not in body["pastures"][0]
    assert "notes" not in body["horse_locations"][0]


def test_staff_location_share_keeps_operational_fields():
    client, _db = _client({"id": "manager-1", "barn_id": "barn-1", "role": "barn_manager"})

    response = client.get("/api/barn-location-share")
    assert response.status_code == 200
    body = response.json()

    assert body["share_state"]["audience"] == "staff"
    assert body["share"]["created_by"] == "manager-1"
    assert body["share"]["updated_by"] == "admin-1"
    assert body["stalls"][0]["notes"] == "Internal medication watch"
    assert body["pastures"][0]["weather_rule"] == "Hold if lightning within 10 miles"


def test_owner_arena_share_filters_staff_only_and_omits_private_fields():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})

    response = client.get("/api/arena-schedule-share")
    assert response.status_code == 200
    body = response.json()

    assert [block["id"] for block in body["blocks"]] == ["arena-shared"]
    assert body["share_state"]["audience"] == "owner_parent"
    assert body["share"] == {
        "id": "arena-share",
        "enabled": True,
        "title": "Arena Schedule",
        "note": "Shared arena availability",
        "share_path": "/arena-schedule",
        "updated_at": "2026-07-06T09:00:00Z",
    }
    assert "created_by" not in body["share"]
    assert "updated_by" not in body["share"]
    assert "created_at" not in body["share"]
    assert "owner_name" not in body["blocks"][0]
    assert "notes" not in body["blocks"][0]


def test_admin_arena_share_keeps_staff_only_and_private_fields():
    client, _db = _client({"id": "manager-1", "barn_id": "barn-1", "role": "barn_manager"})

    response = client.get("/api/arena-schedule-share")
    assert response.status_code == 200
    body = response.json()

    assert [block["id"] for block in body["blocks"]] == ["arena-shared", "arena-internal"]
    assert body["blocks"][0]["owner_name"] == "Private Owner"
    assert body["blocks"][0]["notes"] == "Internal staff handoff note"


def test_stall_card_claim_remains_local_svg_not_true_qr_encoder():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    response = client.get("/api/integrations/qr-horse-id/qr-1/stall-card")
    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "stall_card_ready"
    assert body["provider"] == "qr_horse_id"
    assert "<svg" in body["svg"]
    assert "true QR encoder" in body["message"]
