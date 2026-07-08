from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

import notifications as notification_dispatcher  # noqa: E402
from routes.backlog import build_router as build_backlog_router  # noqa: E402


def _value(doc: Dict[str, Any], key: str) -> Any:
    actual: Any = doc
    for part in key.split("."):
        if not isinstance(actual, dict):
            return None
        actual = actual.get(part)
    return actual


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        if key == "$or":
            if not any(_matches(doc, clause) for clause in expected):
                return False
            continue
        actual = _value(doc, key)
        if isinstance(expected, dict) and "$exists" in expected:
            exists = actual is not None
            if exists is not bool(expected["$exists"]):
                return False
        elif isinstance(expected, dict) and "$in" in expected:
            if isinstance(actual, list):
                if not any(item in expected["$in"] for item in actual):
                    return False
            elif actual not in expected["$in"]:
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
        self._limit = None

    def sort(self, field, direction=1):
        if isinstance(field, list):
            for name, order in reversed(field):
                self.rows.sort(key=lambda row: str(_value(row, name) or ""), reverse=order < 0)
            return self
        if field:
            self.rows.sort(key=lambda row: str(_value(row, field) or ""), reverse=direction < 0)
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    async def to_list(self, limit):
        effective = self._limit or limit
        return [_project(row, self.projection) for row in self.rows[:effective]]


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
                row.update((update or {}).get("$set", {}))
                return type("UpdateResult", (), {"matched_count": 1})()
        if upsert:
            doc = dict(query)
            doc.update((update or {}).get("$set", {}))
            self.rows.append(doc)
        return type("UpdateResult", (), {"matched_count": 0})()

    async def count_documents(self, query):
        return len([row for row in self.rows if _matches(row, query or {})])


class _FakeDB:
    def __init__(self):
        self.group_messages = _Collection([
            {
                "id": "owners-all",
                "barn_id": "barn-1",
                "created_at": "2026-07-06T09:00:00Z",
                "updated_at": "2026-07-06T09:00:00Z",
                "data": {
                    "subject": "Barnwide owner note",
                    "body": "Owner audience only.",
                    "audience": "owners",
                    "channel": "in_app",
                    "status": "sent",
                },
            },
            {
                "id": "owner-targeted",
                "barn_id": "barn-1",
                "created_at": "2026-07-06T09:01:00Z",
                "updated_at": "2026-07-06T09:01:00Z",
                "data": {
                    "subject": "Owner targeted",
                    "body": "For owner one.",
                    "audience": "custom",
                    "channel": "in_app",
                    "status": "sent",
                    "recipient_user_ids": ["owner-1"],
                },
            },
            {
                "id": "guardian-targeted",
                "barn_id": "barn-1",
                "created_at": "2026-07-06T09:02:00Z",
                "updated_at": "2026-07-06T09:02:00Z",
                "data": {
                    "subject": "Guardian targeted",
                    "body": "For guardian one.",
                    "audience": "custom",
                    "channel": "in_app",
                    "status": "sent",
                    "recipient_user_ids": ["parent-1"],
                },
            },
            {
                "id": "other-targeted",
                "barn_id": "barn-1",
                "created_at": "2026-07-06T09:03:00Z",
                "updated_at": "2026-07-06T09:03:00Z",
                "data": {
                    "subject": "Other targeted",
                    "body": "For someone else.",
                    "audience": "custom",
                    "channel": "in_app",
                    "status": "sent",
                    "recipient_user_ids": ["owner-2"],
                },
            },
            {
                "id": "other-barn",
                "barn_id": "barn-2",
                "created_at": "2026-07-06T09:04:00Z",
                "updated_at": "2026-07-06T09:04:00Z",
                "data": {
                    "subject": "Other barn",
                    "body": "Wrong barn.",
                    "audience": "owners",
                    "channel": "in_app",
                    "status": "sent",
                },
            },
        ])
        self.owner_media_updates = _Collection([])
        self.integration_connections = _Collection([])
        self.backlog_audit_events = _Collection([])
        self.users = _Collection([
            {"id": "admin-1", "barn_id": "barn-1", "role": "admin"},
            {"id": "manager-1", "barn_id": "barn-1", "role": "barn_manager"},
            {"id": "admin-2", "barn_id": "barn-2", "role": "admin"},
            {"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"},
            {"id": "owner-2", "barn_id": "barn-2", "role": "horse_owner"},
        ])
        self.horses = _Collection([
            {"id": "horse-1", "barn_id": "barn-1", "owner_id": "owner-1"},
            {"id": "horse-2", "barn_id": "barn-2", "owner_id": "owner-2"},
        ])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user: Dict[str, Any]):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    def new_id():
        return f"new-{len(db.group_messages.rows) + len(db.backlog_audit_events.rows) + 1}"

    app = FastAPI()
    app.include_router(build_backlog_router(db=db, get_current_user=get_current_user, new_id=new_id), prefix="/api")
    return TestClient(app), db


def test_group_message_custom_recipients_are_normalized_and_push_preview_only():
    client, db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    created = client.post("/api/feature-modules/group-messaging/records", json={
        "data": {
            "subject": "Targeted update",
            "body": "Please review.",
            "audience": "custom",
            "channel": "push_ready",
            "status": "queued",
            "recipient_user_ids": "owner-1, parent-1, owner-1",
        },
    })
    assert created.status_code == 200
    assert created.json()["data"]["recipient_user_ids"] == ["owner-1", "parent-1"]

    preview = client.post("/api/integrations/push-notifications/preview", json={
        "include_group_messages": True,
        "include_owner_updates": False,
    })
    assert preview.status_code == 200
    body = preview.json()
    payload = next(row for row in body["payloads"] if row["record_id"] == created.json()["id"])
    assert body["status"] == "push_preview_ready"
    assert payload["delivery_status"] == "preview_only"
    assert payload["metadata"]["delivery_claim"] == "preview_only_no_external_delivery"
    assert payload["metadata"]["recipient_user_ids"] == ["owner-1", "parent-1"]
    assert payload["metadata"]["recipient_count"] == 2
    assert not any(row["record_id"] == "other-barn" for row in body["payloads"])
    assert db.backlog_audit_events.rows[-1]["metadata"]["provider"] == "push_notifications"


def test_owner_and_guardian_announcements_are_relationship_scoped():
    owner_client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})
    owner_response = owner_client.get("/api/owner-portal/announcements")
    assert owner_response.status_code == 200
    owner_ids = {row["id"] for row in owner_response.json()}
    assert owner_ids == {"owners-all", "owner-targeted"}

    guardian_client, _db = _client({"id": "parent-1", "barn_id": "barn-1", "role": "parent"})
    guardian_response = guardian_client.get("/api/owner-portal/announcements")
    assert guardian_response.status_code == 200
    guardian_ids = {row["id"] for row in guardian_response.json()}
    assert guardian_ids == {"guardian-targeted"}


def test_task_notification_candidates_stay_in_event_barn():
    async def run():
        db = _FakeDB()
        recipients = await notification_dispatcher._candidate_recipients(db, {
            "id": "event-1",
            "tenant_id": "barn-1",
            "actor_user_id": "admin-1",
            "event_type": "task.completed",
            "category": "medication",
            "subject_horse_ids": ["horse-1", "horse-2"],
        })
        assert set(recipients) == {"manager-1", "owner-1"}
        assert "admin-2" not in recipients
        assert "owner-2" not in recipients

    asyncio.run(run())
