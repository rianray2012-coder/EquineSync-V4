from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

from core.rf9_trainer_operating_center import build_rf9_trainer_operating_center, render_rf9_report
from routes.backlog import _normalize_training_plan_identity_data
from routes.operations import build_router as build_operations_router
from routes.trainer_operating_center import build_router as build_trainer_operating_center_router


ROOT = Path(__file__).resolve().parents[2]


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        if key == "$or":
            if not any(_matches(doc, clause) for clause in expected):
                return False
            continue
        actual = doc
        for part in key.split("."):
            if not isinstance(actual, dict):
                actual = None
                break
            actual = actual.get(part)
        if isinstance(expected, dict) and "$in" in expected:
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
        if field:
            self.rows.sort(key=lambda row: str(row.get(field) or ""), reverse=direction < 0)
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


class _FakeDB:
    def __init__(self):
        self.users = _Collection([
            {"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer", "email": "avery@example.test"},
            {"id": "trainer-2", "barn_id": "barn-1", "role": "trainer", "full_name": "Blake Trainer", "email": "blake@example.test"},
        ])
        self.riders = _Collection([
            {"id": "rider-1", "barn_id": "barn-1", "full_name": "Riley Rider", "skill_level": "intermediate", "minor_status": "adult"},
        ])
        self.horses = _Collection([
            {"id": "horse-1", "barn_id": "barn-1", "name": "Juniper", "trainer_id": "trainer-1", "status": "active"},
            {"id": "horse-2", "barn_id": "barn-1", "name": "Cedar", "trainer_id": "trainer-2", "status": "active"},
        ])
        self.lessons = _Collection([
            {"id": "lesson-own", "barn_id": "barn-1", "trainer_id": "trainer-1", "rider_id": "rider-1", "rider_name": "Riley Rider", "horse_id": "horse-1", "horse_name": "Juniper", "start_time": "2026-07-06T15:00:00"},
            {"id": "lesson-complete", "barn_id": "barn-1", "trainer_id": "trainer-1", "rider_id": "rider-1", "rider_name": "Riley Rider", "horse_id": "horse-1", "horse_name": "Juniper", "start_time": "2026-07-06T14:00:00", "completed": True},
            {"id": "lesson-other", "barn_id": "barn-1", "trainer_id": "trainer-2", "rider_id": "rider-1", "rider_name": "Riley Rider", "horse_id": "horse-2", "horse_name": "Cedar", "start_time": "2026-07-06T16:00:00"},
            {"id": "lesson-legacy", "barn_id": "barn-1", "trainer_name": "Avery Trainer", "rider_id": "rider-1", "start_time": "2026-07-06T17:00:00"},
        ])
        self.training = _Collection([
            {"id": "training-own", "barn_id": "barn-1", "trainer_id": "trainer-1", "horse_id": "horse-1", "horse_name": "Juniper", "date": "2026-07-06", "discipline": "flatwork"},
            {"id": "training-other", "barn_id": "barn-1", "trainer_id": "trainer-2", "horse_id": "horse-2", "horse_name": "Cedar", "date": "2026-07-06"},
        ])
        self.training_plans = _Collection([
            {"id": "plan-own", "barn_id": "barn-1", "updated_at": "2026-07-06T12:00:00", "data": {"trainer_user_id": "trainer-1", "horse_id": "horse-1", "horse_name": "Juniper", "goal": "Quiet changes", "status": "active"}},
            {"id": "plan-other", "barn_id": "barn-1", "updated_at": "2026-07-06T12:00:00", "data": {"trainer_user_id": "trainer-2", "horse_id": "horse-2", "horse_name": "Cedar", "goal": "Straightness", "status": "active"}},
        ])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    def new_id():
        return "new-id"

    def clean(doc):
        return {k: v for k, v in doc.items() if k != "_id"}

    async def list_collection(coll, query=None, sort_field=None, limit=500):
        return await db[coll].find(query or {}, {"_id": 0}).sort(sort_field, -1).to_list(limit)

    app = FastAPI()
    app.include_router(
        build_operations_router(
            db=db,
            get_current_user=get_current_user,
            list_collection=list_collection,
            clean=clean,
            new_id=new_id,
        ),
        prefix="/api",
    )
    app.include_router(build_trainer_operating_center_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_rf9_report_ready_with_deferred_business_rows():
    report = build_rf9_trainer_operating_center(ROOT)
    rendered = render_rf9_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert report["status_counts"].get("deferred", 0) >= 2
    assert "RF9 Trainer Operating Center Report" in rendered
    assert "Founder Decision Rows" in rendered


def test_trainer_lesson_list_is_stable_id_scoped():
    client, _db = _client({"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"})

    response = client.get("/api/lessons")
    assert response.status_code == 200
    ids = [row["id"] for row in response.json()]
    assert "lesson-own" in ids
    assert "lesson-other" not in ids
    assert "lesson-legacy" not in ids


def test_trainer_create_lesson_stamps_current_trainer_id_and_rejects_other_trainer():
    client, db = _client({"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"})

    created = client.post("/api/lessons", json={
        "rider_id": "rider-1",
        "horse_id": "horse-1",
        "start_time": "2026-07-07T10:00:00",
        "focus": "Canter transitions",
    })
    assert created.status_code == 200
    assert db.lessons.rows[-1]["trainer_id"] == "trainer-1"
    assert db.lessons.rows[-1]["trainer_name"] == "Avery Trainer"

    denied = client.post("/api/lessons", json={
        "rider_id": "rider-1",
        "horse_id": "horse-1",
        "trainer_id": "trainer-2",
        "start_time": "2026-07-07T11:00:00",
    })
    assert denied.status_code == 403


@pytest.mark.anyio
async def test_training_plan_create_requires_and_stamps_stable_ids():
    db = _FakeDB()
    user = {"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"}

    data = await _normalize_training_plan_identity_data(
        db,
        user,
        "training-plans",
        {"horse_id": "horse-1", "trainer_user_id": "trainer-1", "goal": "Quiet changes"},
        creating=True,
    )

    assert data["horse_name"] == "Juniper"
    assert data["trainer_name"] == "Avery Trainer"


@pytest.mark.anyio
async def test_training_plan_create_rejects_missing_stable_ids():
    db = _FakeDB()
    user = {"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"}

    try:
        await _normalize_training_plan_identity_data(
            db,
            user,
            "training-plans",
            {"horse_name": "Juniper", "trainer_name": "Avery Trainer", "goal": "Quiet changes"},
            creating=True,
        )
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 422
    else:
        raise AssertionError("Expected missing stable training plan ids to fail")


def test_training_create_requires_same_barn_horse_and_stamps_trainer_id():
    client, db = _client({"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"})

    created = client.post("/api/training", json={
        "horse_id": "horse-1",
        "date": "2026-07-07",
        "discipline": "flatwork",
    })
    assert created.status_code == 200
    assert db.training.rows[-1]["trainer_id"] == "trainer-1"

    missing = client.post("/api/training", json={
        "horse_id": "missing-horse",
        "date": "2026-07-07",
    })
    assert missing.status_code == 404


def test_trainer_operating_center_projects_only_trainer_owned_context():
    client, _db = _client({"id": "trainer-1", "barn_id": "barn-1", "role": "trainer", "full_name": "Avery Trainer"})

    response = client.get("/api/trainer/operating-center")
    assert response.status_code == 200
    body = response.json()

    assert body["trainer"]["id"] == "trainer-1"
    assert [row["id"] for row in body["upcoming_lessons"]] == ["lesson-own"]
    assert body["counts"]["upcoming_lessons"] == 1
    assert [row["id"] for row in body["recent_training"]] == ["training-own"]
    assert [row["id"] for row in body["active_plans"]] == ["plan-own"]
    assert [row["id"] for row in body["assigned_horses"]] == ["horse-1"]
    assert body["deferred"]["lesson_packages"] == "RF12 billing/package truth"


def test_trainer_operating_center_rejects_non_trainer_role():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin", "full_name": "Admin"})

    response = client.get("/api/trainer/operating-center")
    assert response.status_code == 403
