"""Build-Next-16B - backend setup readiness contract.

BN16B makes onboarding completion backend-authoritative without changing the
frontend journey. Required setup evidence blocks completion with a 409, optional
and deferred steps remain non-blocking, and barn managers can inspect readiness
without finalizing launch.
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=3000")
os.environ.setdefault("DB_NAME", "test_database")

from routes.onboarding import (
    BN16B_COMPLETION_ROLES,
    BN16B_DEFERRED_STEP_IDS,
    BN16B_OPTIONAL_STEP_IDS,
    BN16B_REQUIRED_STEP_IDS,
    BN16B_SETUP_ACCESS_ROLES,
    build_router,
)


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, length=100):
        return [dict(row) for row in self.rows[:length]]


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = [dict(row) for row in (rows or [])]

    async def find_one(self, filt, projection=None):
        for row in self.rows:
            if _matches(row, filt):
                return _project(row, projection)
        return None

    def find(self, filt, projection=None):
        return FakeCursor([_project(row, projection) for row in self.rows if _matches(row, filt)])

    async def count_documents(self, filt):
        return sum(1 for row in self.rows if _matches(row, filt))

    async def insert_one(self, doc):
        self.rows.append(dict(doc))
        return None

    async def update_one(self, filt, update, upsert=False):
        for row in self.rows:
            if _matches(row, filt):
                _apply_update(row, update)
                return None
        if upsert:
            doc = dict(filt)
            _apply_update(doc, update)
            self.rows.append(doc)
        return None

    async def delete_one(self, filt):
        self.rows = [row for row in self.rows if not _matches(row, filt)]
        return None


class FakeDb:
    def __init__(self):
        for name in [
            "barn",
            "feed_templates",
            "horses",
            "inventory",
            "locations",
            "onboarding_progress",
            "owners",
            "riders",
            "staff_invites",
        ]:
            setattr(self, name, FakeCollection())

    def __getitem__(self, name):
        return getattr(self, name)


def _project(row, projection):
    if not projection:
        return dict(row)
    if projection.get("_id") == 0 and len(projection) == 1:
        return {k: v for k, v in row.items() if k != "_id"}
    selected = {k: row.get(k) for k, include in projection.items() if include and k in row}
    if projection.get("_id") == 0:
        selected.pop("_id", None)
    return selected


def _matches(row, filt):
    for key, expected in (filt or {}).items():
        actual = row.get(key)
        if isinstance(expected, dict):
            if "$in" in expected and actual not in expected["$in"]:
                return False
            if "$ne" in expected and actual == expected["$ne"]:
                return False
        elif actual != expected:
            return False
    return True


def _apply_update(row, update):
    for key, value in (update or {}).get("$set", {}).items():
        target = row
        parts = key.split(".")
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value


def _app(db: FakeDb, user: dict) -> TestClient:
    async def get_current_user():
        return dict(user)

    def require_setup_role(current_user):
        if current_user.get("role") not in {"admin", "barn_manager"}:
            raise AssertionError("require_setup_role should not be used by BN16B readiness")

    async def list_collection(name, filt):
        return await getattr(db, name).find(filt, {"_id": 0}).to_list(1000)

    app = FastAPI()
    app.include_router(build_router(
        db=db,
        get_current_user=get_current_user,
        require_setup_role=require_setup_role,
        roles=["admin", "barn_manager", "barn_owner"],
        list_collection=list_collection,
        clean=lambda doc: dict(doc),
        new_id=lambda: "new_id",
    ))
    return TestClient(app)


def _user(role="admin"):
    return {"id": f"u_{role}", "role": role, "barn_id": "barn_a", "full_name": "UAT User"}


def _seed_ready_setup(db: FakeDb, *, user_id="u_admin"):
    db.barn.rows.append({"id": "barn_a", "name": "Stable Command"})
    db.locations.rows.append({"id": "loc_1", "barn_id": "barn_a", "name": "Main Barn"})
    db.owners.rows.append({"id": "owner_1", "barn_id": "barn_a", "full_name": "Owner One"})
    db.horses.rows.append({"id": "horse_1", "barn_id": "barn_a", "name": "Demo Horse"})
    db.feed_templates.rows.append({"id": "feed_1", "barn_id": "barn_a", "meal": "AM"})
    db.onboarding_progress.rows.append({
        "user_id": user_id,
        "barn_id": "barn_a",
        "steps": {"review": "complete"},
        "completed": False,
    })


def test_readiness_reports_required_blockers_and_deferred_schedules():
    db = FakeDb()
    client = _app(db, _user("admin"))

    response = client.get("/onboarding/readiness")

    assert response.status_code == 200
    data = response.json()
    assert data["phase"] == "BN16B"
    assert data["completion_scope"] == "barn"
    assert data["can_finalize"] is True
    assert data["can_complete"] is False
    assert [step["id"] for step in data["required_steps"]] == list(BN16B_REQUIRED_STEP_IDS)
    assert {item["step_id"] for item in data["blockers"]} == set(BN16B_REQUIRED_STEP_IDS)
    assert data["progress"] == {"required_completed": 0, "required_total": 6, "required_percent": 0}
    assert data["deferred_steps"] == [{
        "id": "schedules",
        "label": "Recurring Schedules",
        "status": "deferred",
        "required": False,
        "deferred": True,
        "reason": "Deferred until recurring schedule materialization is ready.",
    }]


def test_complete_refuses_required_blockers_with_409():
    db = FakeDb()
    client = _app(db, _user("admin"))

    response = client.post("/onboarding/complete")

    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["message"] == "Setup is not ready to complete."
    assert {item["step_id"] for item in detail["blockers"]} == set(BN16B_REQUIRED_STEP_IDS)
    assert not (db.onboarding_progress.rows[0]).get("completed")


def test_complete_succeeds_when_required_evidence_and_review_are_complete():
    db = FakeDb()
    _seed_ready_setup(db, user_id="u_admin")
    client = _app(db, _user("admin"))

    response = client.post("/onboarding/complete")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ok"] is True
    assert data["readiness"]["can_complete"] is True
    progress = db.onboarding_progress.rows[0]
    assert progress["completed"] is True
    assert progress["completed_at"]


def test_optional_and_deferred_steps_do_not_block_completion():
    db = FakeDb()
    _seed_ready_setup(db, user_id="u_barn_owner")
    client = _app(db, _user("barn_owner"))

    readiness = client.get("/onboarding/readiness").json()
    response = client.post("/onboarding/complete")

    assert response.status_code == 200, response.text
    assert [step["id"] for step in readiness["optional_steps"]] == list(BN16B_OPTIONAL_STEP_IDS)
    assert [step["status"] for step in readiness["optional_steps"]] == ["pending"] * 4
    assert [step["id"] for step in readiness["deferred_steps"]] == list(BN16B_DEFERRED_STEP_IDS)
    assert readiness["blockers"] == []


def test_barn_manager_can_read_readiness_but_cannot_complete():
    db = FakeDb()
    _seed_ready_setup(db, user_id="u_barn_manager")
    client = _app(db, _user("barn_manager"))

    readiness = client.get("/onboarding/readiness")
    complete = client.post("/onboarding/complete")

    assert readiness.status_code == 200
    assert readiness.json()["can_view"] is True
    assert readiness.json()["can_finalize"] is False
    assert readiness.json()["can_complete"] is False
    assert complete.status_code == 403
    assert "facility admin or barn owner" in complete.json()["detail"]


def test_non_setup_role_cannot_read_readiness_or_create_progress():
    db = FakeDb()
    client = _app(db, _user("horse_owner"))

    readiness = client.get("/onboarding/readiness")

    assert readiness.status_code == 403
    assert "facility setup role" in readiness.json()["detail"]
    assert db.onboarding_progress.rows == []


def test_non_finalizer_complete_denied_before_progress_side_effects():
    db = FakeDb()
    client = _app(db, _user("barn_manager"))

    complete = client.post("/onboarding/complete")

    assert complete.status_code == 403
    assert "facility admin or barn owner" in complete.json()["detail"]
    assert db.onboarding_progress.rows == []


def test_bn16b_source_constants_are_locked_to_plan_shape():
    assert BN16B_COMPLETION_ROLES == {"admin", "barn_owner"}
    assert BN16B_SETUP_ACCESS_ROLES == {"admin", "barn_owner", "barn_manager"}
    assert BN16B_REQUIRED_STEP_IDS == (
        "barn",
        "locations",
        "owners",
        "horses",
        "feed_templates",
        "review",
    )
    assert BN16B_OPTIONAL_STEP_IDS == ("riders", "inventory", "operations_setup", "staff")
    assert BN16B_DEFERRED_STEP_IDS == ("schedules",)
