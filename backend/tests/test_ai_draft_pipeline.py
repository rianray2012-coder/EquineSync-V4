from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.ai_assistant import build_router
from services.ai_draft_extractor import (
    normalize_source_type,
    private_ai_storage_key,
    validate_ai_source,
)


class InsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class FakeCollection:
    def __init__(self):
        self.rows = []

    async def insert_one(self, doc):
        self.rows.append(dict(doc))
        return InsertResult(len(self.rows))

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if all(row.get(k) == v for k, v in query.items()):
                out = dict(row)
                if projection:
                    for key, include in projection.items():
                        if include == 0:
                            out.pop(key, None)
                return out
        return None

    async def update_one(self, query, update):
        for row in self.rows:
            if all(row.get(k) == v for k, v in query.items()):
                row.update(update.get("$set", {}))
                return

    def find(self, query, projection=None):
        matches = []
        for row in self.rows:
            if all(row.get(k) == v for k, v in query.items()):
                out = dict(row)
                if projection:
                    for key, include in projection.items():
                        if include == 0:
                            out.pop(key, None)
                matches.append(out)
        return FakeCursor(matches)


class FakeCursor:
    def __init__(self, rows):
        self.rows = rows

    def sort(self, key, direction):
        reverse = direction < 0
        self.rows = sorted(self.rows, key=lambda row: str(row.get(key) or ""), reverse=reverse)
        return self

    def limit(self, limit):
        self.rows = self.rows[:limit]
        return self

    async def to_list(self, length):
        return self.rows[:length]


class FakeDb(dict):
    def __getitem__(self, name):
        if name not in self:
            self[name] = FakeCollection()
        return dict.__getitem__(self, name)


class FakeStorage:
    def __init__(self):
        self.objects: Dict[str, bytes] = {}

    def configured(self):
        return True

    def presigned_put(self, *, key, mime_type, ttl_seconds=900):
        self.objects[key] = b"uploaded source bytes"
        return f"https://storage.invalid/{key}?signature=redacted"

    def read_bytes(self, *, key, mime_type):
        class Stored:
            bytes_value = b"stored private source"

            def __init__(self, mt):
                self.mime_type = mt

        return Stored(mime_type)


class FakeExtractor:
    async def extract(self, **kwargs):
        return {
            "draft_only": True,
            "review_required": True,
            "source_category": kwargs["source_type"],
            "draft_records": [{
                "record_type": "inventory_candidate",
                "title": "Draft only",
                "summary": "Human review required",
                "suggested_fields": {"source": "fake"},
                "confidence": "medium",
            }],
            "review_questions": ["Confirm before saving."],
            "blocked_actions": ["official_record_save"],
        }


def app_for(db, user, storage=None, extractor=None):
    app = FastAPI()

    async def get_current_user():
        return user

    async def audit_record(**kwargs):
        return None

    app.include_router(build_router(
        db=db,
        get_current_user=get_current_user,
        storage_client=storage or FakeStorage(),
        extractor=extractor or FakeExtractor(),
        audit_record=audit_record,
    ), prefix="/api")
    return app


def test_inline_text_job_is_draft_only_and_review_does_not_save_records():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Add a draft inventory note for two bags of senior feed.",
            "requested_output": "draft_records",
        })
        assert created.status_code == 201
        job = created.json()["job"]
        assert job["status"] == "draft_ready"
        assert job["draft_only"] is True
        assert job["review_required"] is True
        assert job["draft_result"]["draft_only"] is True
        assert job["draft_result"]["review_required"] is True

        reviewed = client.post(f"/api/ai/draft-jobs/{job['id']}/review", json={
            "action": "approved_no_save",
            "note": "Looks useful, but do not save yet.",
        })
        assert reviewed.status_code == 200
        assert reviewed.json()["review"]["official_records_written"] is False
        assert "inventory_items" not in db
        assert "invoices" not in db
        assert "horse_health_records" not in db


def test_list_draft_jobs_returns_only_own_draft_queue():
    db = FakeDb()
    owner = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "owner@example.test"}
    app = app_for(db, owner)
    with TestClient(app) as client:
        first = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft a training note for a quiet flat lesson.",
            "requested_output": "draft_records",
        })
        second = client.post("/api/ai/draft-jobs", json={
            "source_type": "lesson_schedule",
            "source_text": "Tuesday 5pm beginner lesson with Zoe.",
            "requested_output": "schedule_candidates",
        })
        assert first.status_code == 201
        assert second.status_code == 201

        reviewed_id = first.json()["job"]["id"]
        reviewed = client.post(f"/api/ai/draft-jobs/{reviewed_id}/review", json={
            "action": "rejected",
            "note": "Needs better source detail.",
        })
        assert reviewed.status_code == 200

        pending = client.get("/api/ai/draft-jobs?review_status=pending_review")
        assert pending.status_code == 200
        pending_jobs = pending.json()["jobs"]
        assert [job["id"] for job in pending_jobs] == [second.json()["job"]["id"]]

    other = {"id": "u_2", "role": "barn_manager", "barn_id": "barn_1", "email": "other@example.test"}
    other_app = app_for(db, other)
    with TestClient(other_app) as client:
        visible = client.get("/api/ai/draft-jobs")
        assert visible.status_code == 200
        assert visible.json()["jobs"] == []


def test_private_upload_source_pipeline_reads_only_own_barn_source():
    db = FakeDb()
    storage = FakeStorage()
    owner = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "owner@example.test"}
    app = app_for(db, owner, storage=storage)
    with TestClient(app) as client:
        intent = client.post("/api/ai/draft-jobs/upload-intents", json={
            "source_type": "photo_inventory",
            "filename": "feed-room.jpg",
            "mime_type": "image/jpeg",
            "byte_size": 1024,
        })
        assert intent.status_code == 201
        source = intent.json()["source"]
        assert source["status"] == "upload_pending"
        assert "url" in intent.json()["upload"]

        confirm = client.post(f"/api/ai/draft-jobs/upload-intents/{source['id']}/confirm", json={
            "source_id": source["id"],
            "sha256": "a" * 64,
            "byte_size": 1024,
        })
        assert confirm.status_code == 200
        assert confirm.json()["source"]["status"] == "uploaded"

        job = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_id": source["id"],
            "requested_output": "photo_to_inventory",
        })
        assert job.status_code == 201
        assert job.json()["job"]["status"] == "draft_ready"

    other = {"id": "u_2", "role": "barn_manager", "barn_id": "barn_2", "email": "other@example.test"}
    other_app = app_for(db, other, storage=storage)
    with TestClient(other_app) as client:
        denied = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_id": source["id"],
            "requested_output": "photo_to_inventory",
        })
        assert denied.status_code == 404


def test_ai_source_validation_and_private_key_boundaries():
    assert normalize_source_type("Invoice") == "invoice"
    assert validate_ai_source(source_type="invoice", mime_type="application/pdf", byte_size=10) == "application/pdf"
    with pytest.raises(ValueError):
        validate_ai_source(source_type="photo_inventory", mime_type="application/pdf", byte_size=10)
    key = private_ai_storage_key(barn_id="barn_1", source_id="ai_src_1", filename="../Bad File.PDF")
    assert key.startswith("barn_1/ai-draft-sources/ai_src_1/")
    assert "/" not in key.rsplit("/", 1)[-1]
