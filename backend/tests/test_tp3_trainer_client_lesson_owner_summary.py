from __future__ import annotations

import os
import sys
import types
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

admin_portal_pkg = types.ModuleType("routes.admin_portal")
admin_portal_pkg.__path__ = []
admin_helpers = types.ModuleType("routes.admin_portal._helpers")
admin_helpers._redact_stripe_in_string = lambda value: value
sys.modules.setdefault("routes.admin_portal", admin_portal_pkg)
sys.modules.setdefault("routes.admin_portal._helpers", admin_helpers)

from routes.horse_ledger import build_router as build_horse_ledger_router


def _value_for(doc: Dict[str, Any], key: str) -> Any:
    value: Any = doc
    for part in key.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        if key == "$or":
            if not any(_matches(doc, clause) for clause in expected):
                return False
            continue
        actual = _value_for(doc, key)
        if isinstance(expected, dict):
            if "$in" in expected and actual not in expected["$in"]:
                return False
            if "$ne" in expected and actual == expected["$ne"]:
                return False
        elif actual != expected:
            return False
    return True


def _project(doc: Dict[str, Any], projection: Dict[str, Any] | None) -> Dict[str, Any]:
    if not projection or projection == {"_id": 0}:
        return {k: v for k, v in doc.items() if k != "_id"}
    included = {k for k, v in projection.items() if v and k != "_id"}
    return {k: _value_for(doc, k) for k in included if _value_for(doc, k) is not None}


class _Cursor:
    def __init__(self, rows: List[Dict[str, Any]], projection=None):
        self.rows = rows
        self.projection = projection
        self._index = 0

    def sort(self, field, direction=1):
        if isinstance(field, list):
            for sort_field, sort_direction in reversed(field):
                self.rows.sort(key=lambda row: str(_value_for(row, sort_field) or ""), reverse=sort_direction < 0)
        elif field:
            self.rows.sort(key=lambda row: str(_value_for(row, field) or ""), reverse=direction < 0)
        return self

    def limit(self, limit):
        self.rows = self.rows[:limit]
        return self

    async def to_list(self, limit):
        return [_project(row, self.projection) for row in self.rows[:limit]]

    def __aiter__(self):
        self._index = 0
        return self

    async def __anext__(self):
        if self._index >= len(self.rows):
            raise StopAsyncIteration
        row = self.rows[self._index]
        self._index += 1
        return _project(row, self.projection)


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


class _FakeDB:
    def __init__(self):
        self.horses = _Collection([
            {"id": "horse-owned", "barn_id": "barn-1", "name": "Valencia", "owner_id": "owner-1", "status": "active"},
            {"id": "horse-other", "barn_id": "barn-1", "name": "Other", "owner_id": "owner-2", "status": "active"},
        ])
        self.horse_care_profiles = _Collection([])
        self.horse_owner_visibility_policy = _Collection([])
        self.horse_equipment = _Collection([])
        self.horse_provider_assignments = _Collection([])
        self.medications = _Collection([])
        self.medication_logs = _Collection([])
        self.vet_records = _Collection([])
        self.injuries = _Collection([])
        self.wellness = _Collection([])
        self.horse_ledger_alerts = _Collection([])
        self.service_requests = _Collection([])
        self.lessons = _Collection([
            {
                "id": "lesson-owner-visible",
                "barn_id": "barn-1",
                "horse_id": "horse-owned",
                "horse_name": "Valencia",
                "trainer_id": "trainer-1",
                "trainer_name": "Avery Trainer",
                "rider_id": "rider-private",
                "rider_name": "Rider Name Must Not Leak",
                "start_time": "2026-09-01T14:00:00Z",
                "duration_min": 45,
                "focus": "Balance in transitions",
                "notes": "Private trainer note must not leak",
                "owner_visible": True,
            },
            {
                "id": "lesson-private",
                "barn_id": "barn-1",
                "horse_id": "horse-owned",
                "trainer_id": "trainer-1",
                "trainer_name": "Avery Trainer",
                "start_time": "2026-09-01T15:00:00Z",
                "notes": "Private lesson must not leak",
                "owner_visible": False,
            },
            {
                "id": "lesson-other-horse",
                "barn_id": "barn-1",
                "horse_id": "horse-other",
                "trainer_id": "trainer-1",
                "trainer_name": "Avery Trainer",
                "start_time": "2026-09-01T16:00:00Z",
                "owner_visible": True,
            },
        ])
        self.training = _Collection([
            {
                "id": "training-owner-visible",
                "barn_id": "barn-1",
                "horse_id": "horse-owned",
                "horse_name": "Valencia",
                "trainer_id": "trainer-1",
                "trainer_name": "Avery Trainer",
                "date": "2026-08-31",
                "discipline": "flatwork",
                "exercises": "Transitions",
                "homework": "Walk-halt practice",
                "rating": 8,
                "notes": "Staff-only critique must not leak",
                "visibility": "owner_visible",
            },
            {
                "id": "training-private",
                "barn_id": "barn-1",
                "horse_id": "horse-owned",
                "trainer_id": "trainer-1",
                "date": "2026-08-30",
                "notes": "Private training must not leak",
            },
        ])
        self.training_plans = _Collection([
            {
                "id": "plan-owner-visible",
                "barn_id": "barn-1",
                "updated_at": "2026-08-30T12:00:00Z",
                "owner_visible": True,
                "data": {
                    "horse_id": "horse-owned",
                    "horse_name": "Valencia",
                    "trainer_user_id": "trainer-1",
                    "trainer_name": "Avery Trainer",
                    "goal": "Softer transitions",
                    "status": "active",
                    "staff_note": "Plan note must not leak",
                },
            },
            {
                "id": "plan-private",
                "barn_id": "barn-1",
                "updated_at": "2026-08-29T12:00:00Z",
                "data": {
                    "horse_id": "horse-owned",
                    "trainer_user_id": "trainer-1",
                    "goal": "Private plan must not leak",
                    "status": "active",
                },
            },
        ])


def _client(user):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_horse_ledger_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_tp3_owner_summary_includes_only_explicit_owner_visible_trainer_work():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})

    response = client.get("/api/horse-ledger/horse-owned/owner-summary")
    assert response.status_code == 200
    body = response.json()
    text = response.text

    assert body["training_summary"]["upcoming_lessons"] == [{
        "id": "lesson-owner-visible",
        "horse_id": "horse-owned",
        "horse_name": "Valencia",
        "trainer_id": "trainer-1",
        "trainer_name": "Avery Trainer",
        "start_time": "2026-09-01T14:00:00Z",
        "duration_min": 45,
        "focus": "Balance in transitions",
        "completed": False,
    }]
    assert body["training_summary"]["recent_training"][0]["id"] == "training-owner-visible"
    assert body["training_summary"]["active_plans"][0]["id"] == "plan-owner-visible"

    for forbidden in [
        "lesson-private",
        "lesson-other-horse",
        "training-private",
        "plan-private",
        "Rider Name Must Not Leak",
        "Private trainer note must not leak",
        "Staff-only critique must not leak",
        "Plan note must not leak",
    ]:
        assert forbidden not in text


def test_tp3_owner_summary_rejects_unowned_horse_before_training_projection():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})

    response = client.get("/api/horse-ledger/horse-other/owner-summary")
    assert response.status_code == 404
