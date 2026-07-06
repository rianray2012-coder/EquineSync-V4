from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

from routes.care import build_router as build_care_router
from routes.horses import build_router as build_horses_router
from routes.service_provider_center import build_router as build_service_provider_center_router


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
        elif isinstance(expected, dict) and "$ne" in expected:
            if actual == expected["$ne"]:
                return False
        elif isinstance(actual, list):
            if expected not in actual:
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
                self.rows.sort(key=lambda row: str(row.get(name) or ""), reverse=order < 0)
            return self
        if field:
            self.rows.sort(key=lambda row: str(row.get(field) or ""), reverse=direction < 0)
        return self

    def limit(self, limit):
        self.rows = self.rows[:limit]
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
        self.barns = _Collection([
            {"id": "barn-1", "status": "active"},
            {"id": "barn-2", "status": "active"},
            {"id": "barn-disabled", "status": "disabled"},
        ])
        self.users = _Collection([
            {"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier", "email": "fran@example.test"},
            {"id": "vet-1", "barn_id": "barn-1", "role": "veterinarian", "full_name": "Val Vet", "email": "val@example.test"},
        ])
        self.service_providers = _Collection([
            {"id": "sp-farrier", "barn_id": "barn-1", "category": "farrier", "name": "Fran Farrier", "provider_user_id": "farrier-1", "status": "active"},
            {"id": "sp-vet", "barn_id": "barn-1", "category": "vet", "name": "Val Vet", "provider_user_id": "vet-1", "status": "active"},
        ])
        self.horse_provider_assignments = _Collection([
            {"id": "grant-active", "barn_id": "barn-1", "horse_id": "horse-1", "provider_id": "sp-farrier", "provider_user_id": "farrier-1", "category": "farrier", "status": "active", "notes": "Internal barn scheduling note"},
            {"id": "grant-revoked", "barn_id": "barn-1", "horse_id": "horse-2", "provider_id": "sp-farrier", "provider_user_id": "farrier-1", "category": "farrier", "status": "archived"},
            {"id": "grant-other-role", "barn_id": "barn-1", "horse_id": "horse-3", "provider_id": "sp-vet", "provider_user_id": "vet-1", "category": "vet", "status": "active"},
            {"id": "grant-disabled", "barn_id": "barn-disabled", "horse_id": "horse-disabled", "provider_id": "sp-farrier", "provider_user_id": "farrier-1", "category": "farrier", "status": "active"},
        ])
        self.horses = _Collection([
            {"id": "horse-1", "barn_id": "barn-1", "name": "Juniper", "breed": "Warmblood", "allergies": ["penicillin"]},
            {"id": "horse-2", "barn_id": "barn-1", "name": "Cedar"},
            {"id": "horse-3", "barn_id": "barn-1", "name": "Maple"},
            {"id": "horse-disabled", "barn_id": "barn-disabled", "name": "Hidden"},
        ])
        self.vet_records = _Collection([
            {"id": "vet-own", "barn_id": "barn-1", "horse_id": "horse-1", "title": "Lameness recheck", "date": "2026-07-06", "vet_name": "Dr. Lane"},
            {"id": "vet-other", "barn_id": "barn-1", "horse_id": "horse-2", "title": "Dental", "date": "2026-07-06"},
        ])
        self.farrier_history = _Collection([
            {"id": "farrier-own", "barn_id": "barn-1", "horse_id": "horse-1", "date": "2026-07-06", "farrier_name": "Fran Farrier"},
            {"id": "farrier-other", "barn_id": "barn-1", "horse_id": "horse-2", "date": "2026-07-06", "farrier_name": "Fran Farrier"},
        ])
        self.provider_visit_notes = _Collection([])
        self.medications = _Collection([
            {"id": "med-collide", "barn_id": "barn-1", "horse_id": "horse-1", "name": "Phenylbutazone"},
            {"id": "med-collide", "barn_id": "barn-2", "horse_id": "horse-external", "name": "Phenylbutazone"},
        ])
        self.medication_logs = _Collection([
            {"id": "log-own", "barn_id": "barn-1", "medication_id": "med-collide", "scheduled_time": "2026-07-06T08:00:00Z"},
            {"id": "log-foreign", "barn_id": "barn-2", "medication_id": "med-collide", "scheduled_time": "2026-07-06T09:00:00Z"},
        ])
        self.owners = _Collection([{"id": "owner-1", "barn_id": "barn-1", "full_name": "Owner"}])
        self.riders = _Collection([{"id": "rider-1", "barn_id": "barn-1", "full_name": "Rider"}])
        self.feed_tasks = _Collection([])
        self.injuries = _Collection([])
        self.wellness = _Collection([])

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
        build_service_provider_center_router(db=db, get_current_user=get_current_user, new_id=new_id),
        prefix="/api",
    )
    app.include_router(
        build_horses_router(
            db=db,
            get_current_user=get_current_user,
            list_collection=list_collection,
            clean=clean,
            new_id=new_id,
        ),
        prefix="/api",
    )
    app.include_router(
        build_care_router(
            db=db,
            get_current_user=get_current_user,
            list_collection=list_collection,
            clean=clean,
            new_id=new_id,
        ),
        prefix="/api",
    )
    return TestClient(app), db


def test_provider_operating_center_is_explicit_grant_scoped():
    client, _db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    response = client.get("/api/service-provider/operating-center")
    assert response.status_code == 200
    body = response.json()

    assert [row["horse_id"] for row in body["grants"]] == ["horse-1"]
    assert "notes" not in body["grants"][0]
    assert [row["id"] for row in body["shared_horses"]] == ["horse-1"]
    assert [row["id"] for row in body["recent_farrier_records"]] == ["farrier-own"]
    assert body["deferred"]["provider_invoices"] == "RF12 billing/payment/provider invoice truth"


def test_provider_direct_horse_and_care_reads_are_grant_scoped():
    client, _db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    horses = client.get("/api/horses")
    assert horses.status_code == 200
    assert [row["id"] for row in horses.json()] == ["horse-1"]

    denied = client.get("/api/horses/horse-2")
    assert denied.status_code == 404

    vet = client.get("/api/vet-records")
    assert vet.status_code == 200
    assert [row["id"] for row in vet.json()] == ["vet-own"]


def test_provider_medication_logs_are_scoped_by_medication_and_barn():
    client, _db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    all_logs = client.get("/api/medication-logs")
    assert all_logs.status_code == 200
    assert [row["id"] for row in all_logs.json()] == ["log-own"]

    by_medication = client.get("/api/medication-logs", params={"medication_id": "med-collide"})
    assert by_medication.status_code == 200
    assert [row["id"] for row in by_medication.json()] == ["log-own"]


def test_provider_visit_note_requires_granted_horse_and_stamps_provider():
    client, db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    denied = client.post("/api/service-provider/visit-notes", json={
        "horse_id": "horse-2",
        "category": "farrier",
        "title": "Trim notes",
    })
    assert denied.status_code == 404

    created = client.post("/api/service-provider/visit-notes", json={
        "horse_id": "horse-1",
        "category": "farrier",
        "title": "Trim notes",
        "visit_date": "2026-07-06",
    })
    assert created.status_code == 200
    row = db.provider_visit_notes.rows[-1]
    assert row["provider_user_id"] == "farrier-1"
    assert row["barn_id"] == "barn-1"
    assert row["horse_name"] == "Juniper"


def test_provider_center_rejects_non_provider_role():
    client, _db = _client({"id": "manager-1", "barn_id": "barn-1", "role": "barn_manager", "full_name": "Manager"})

    response = client.get("/api/service-provider/operating-center")
    assert response.status_code == 403


def test_provider_owner_and_rider_lists_do_not_expose_barn_directory():
    client, _db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    assert client.get("/api/owners").json() == []
    assert client.get("/api/riders").json() == []


def test_provider_canonical_care_writes_are_rejected():
    client, _db = _client({"id": "farrier-1", "barn_id": "barn-1", "role": "farrier", "full_name": "Fran Farrier"})

    vet = client.post("/api/vet-records", json={
        "horse_id": "horse-1",
        "type": "exam",
        "title": "Exam",
        "date": "2026-07-06",
    })
    assert vet.status_code == 403

    medication = client.post("/api/medications", json={
        "horse_id": "horse-1",
        "name": "Phenylbutazone",
        "dosage": "1 g",
        "frequency": "daily",
    })
    assert medication.status_code == 403

    wellness = client.post("/api/wellness", json={
        "horse_id": "horse-1",
        "appetite": 5,
        "water_intake": 5,
        "energy": 5,
        "body_condition": 5,
        "coat_quality": 5,
    })
    assert wellness.status_code == 403
