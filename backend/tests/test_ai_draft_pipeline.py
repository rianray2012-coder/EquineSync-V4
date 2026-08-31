from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.ai_assistant import build_router
from services.ai_draft_extractor import (
    OpenAIDraftExtractor,
    AI_SOURCE_TYPES,
    INVENTORY_CANDIDATE_TEMPLATE,
    normalize_source_type,
    output_schema_hint,
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
        doc.setdefault("_id", f"fake_object_id_{uuid.uuid4().hex}")
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
        self.read_count = 0

    def configured(self):
        return True

    def presigned_put(self, *, key, mime_type, ttl_seconds=900):
        self.objects[key] = b"uploaded source bytes"
        return f"https://storage.invalid/{key}?signature=redacted"

    def read_bytes(self, *, key, mime_type):
        self.read_count += 1

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


class ManualReviewExtractor:
    async def extract(self, **kwargs):
        return {
            "draft_only": True,
            "review_required": True,
            "source_category": kwargs["source_type"],
            "extraction_status": "manual_review_required",
            "review_questions": [
                "This PDF could not be read automatically. Please upload a clearer copy or enter the key details manually.",
            ],
            "blocked_actions": ["official_record_save", "automatic_extraction"],
        }


class FailingExtractor:
    async def extract(self, **kwargs):
        raise RuntimeError(
            "provider failure included private source text for Zoe Spoon and invoice INV-123"
        )


class PdfTextFallbackExtractor(OpenAIDraftExtractor):
    def __init__(self):
        super().__init__(api_key="test-key")
        self.text_seen = None

    async def _extract_pdf_file(self, **kwargs):
        raise RuntimeError("simulated direct PDF failure")

    def _extract_pdf_text(self, file_bytes):
        return "Farrier service invoice text with enough readable detail for fallback extraction."

    def _render_pdf_pages_as_data_urls(self, file_bytes):
        raise AssertionError("image fallback should not be used when text fallback succeeds")

    async def _extract_text(self, *, source_type, prompt, text):
        self.text_seen = text
        return {
            "draft_only": True,
            "review_required": True,
            "source_category": source_type,
            "draft_service_history_candidates": [{"service_type": "farrier"}],
            "review_questions": ["Confirm horse and service date."],
            "blocked_actions": [],
        }


class PdfManualFallbackExtractor(OpenAIDraftExtractor):
    def __init__(self):
        super().__init__(api_key="test-key")

    async def _extract_pdf_file(self, **kwargs):
        raise RuntimeError("simulated direct PDF failure")

    def _extract_pdf_text(self, file_bytes):
        return ""

    def _render_pdf_pages_as_data_urls(self, file_bytes):
        return []


def app_for(db, user, storage=None, extractor=None, audit_sink=None):
    app = FastAPI()

    async def get_current_user():
        return user

    async def audit_record(**kwargs):
        if audit_sink is not None:
            audit_sink.append(kwargs)
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


def test_ai_usage_policy_records_safe_daily_budget_metadata():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)

    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft inventory notes for four bags of senior feed.",
            "requested_output": "draft_records",
        })
        assert created.status_code == 201

        policy = client.get("/api/ai/draft-jobs/usage-policy")

    assert policy.status_code == 200
    usage = policy.json()["usage"]
    assert usage["draft_jobs_created"] == 1
    assert usage["estimated_tokens_used"] >= 1801
    assert usage["remaining_jobs"] == usage["daily_job_limit"] - 1
    assert usage["policy"]["draft_only_default"] is True
    assert usage["policy"]["human_review_required"] is True
    assert usage["policy"]["autonomous_mutation_enabled"] is False
    assert usage["policy"]["higher_risk_lanes_separately_gated"] is True
    assert "voice_transcript" in usage["by_source_type"]
    assert "senior feed" not in str(usage)
    assert "founder@example.test" not in str(usage)


def test_ai_daily_budget_blocks_second_job_before_extraction(monkeypatch):
    monkeypatch.setenv("AI_DAILY_JOB_LIMIT", "1")
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)

    with TestClient(app) as client:
        first = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft first note.",
            "requested_output": "draft_records",
        })
        assert first.status_code == 201

        second = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft second note.",
            "requested_output": "draft_records",
        })

    assert second.status_code == 429
    assert "Daily AI draft job limit reached" in second.text
    assert len(db["ai_draft_jobs"].rows) == 1
    assert db["ai_usage_daily"].rows[0]["draft_jobs_created"] == 1


def test_ai_daily_token_budget_blocks_large_source_before_job_insert(monkeypatch):
    monkeypatch.setenv("AI_DAILY_ESTIMATED_TOKEN_LIMIT", "100")
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)

    with TestClient(app) as client:
        blocked = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "x" * 1000,
            "requested_output": "draft_records",
        })

    assert blocked.status_code == 429
    assert "Daily AI estimated token budget reached" in blocked.text
    assert "ai_draft_jobs" not in db
    assert db["ai_usage_daily"].rows == []
    assert "ai_draft_sources" not in db


def test_ai_source_file_budget_blocks_before_private_storage_read(monkeypatch):
    monkeypatch.setenv("AI_DAILY_SOURCE_BYTE_LIMIT", "100")
    db = FakeDb()
    storage = FakeStorage()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user, storage=storage)

    with TestClient(app) as client:
        intent = client.post("/api/ai/draft-jobs/upload-intents", json={
            "source_type": "photo_inventory",
            "filename": "private-tack-room.jpg",
            "mime_type": "image/jpeg",
            "byte_size": 1024,
        })
        source = intent.json()["source"]
        confirm = client.post(f"/api/ai/draft-jobs/upload-intents/{source['id']}/confirm", json={
            "source_id": source["id"],
            "sha256": "c" * 64,
            "byte_size": 1024,
        })
        assert confirm.status_code == 200

        blocked = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_id": source["id"],
            "requested_output": "photo_to_inventory",
        })

    assert blocked.status_code == 429
    assert "Daily AI source processing budget reached" in blocked.text
    assert storage.read_count == 0
    assert "ai_draft_jobs" not in db
    assert db["ai_usage_daily"].rows == []


def test_ai_upload_source_projection_and_storage_metadata_do_not_expose_raw_filename_or_prompt_hint():
    db = FakeDb()
    storage = FakeStorage()
    audit_events = []
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "owner@example.test"}
    app = app_for(db, user, storage=storage, audit_sink=audit_events)
    raw_filename = "Zoe Spoon Farrier Invoice INV-123.pdf"
    raw_prompt_hint = "Extract Zoe Spoon farrier invoice details for Pony Secret."

    with TestClient(app) as client:
        intent = client.post("/api/ai/draft-jobs/upload-intents", json={
            "source_type": "service_invoice",
            "filename": raw_filename,
            "mime_type": "application/pdf",
            "byte_size": 2048,
            "prompt_hint": raw_prompt_hint,
        })

    assert intent.status_code == 201
    source = intent.json()["source"]
    assert "filename" not in source
    assert source["filename_present"] is True
    assert source["filename_extension"] == "pdf"

    stored_source = db["ai_draft_sources"].rows[0]
    assert stored_source["filename"] == "source.pdf"
    assert stored_source["storage_key"].endswith("/source.pdf")
    assert raw_filename not in stored_source["storage_key"]
    assert stored_source["filename_sha256"]
    assert stored_source["prompt_hint_present"] is True
    assert stored_source["prompt_hint_sha256"]
    assert "prompt_hint" not in stored_source
    assert raw_prompt_hint not in str(stored_source)

    audit_metadata = audit_events[-1]["metadata"]
    assert audit_metadata["filename_present"] is True
    assert audit_metadata["filename_extension"] == "pdf"
    assert audit_metadata["prompt_hint_present"] is True
    assert audit_metadata["prompt_hint_sha256"]
    assert raw_filename not in str(audit_metadata)
    assert raw_prompt_hint not in str(audit_metadata)


def test_ai_review_note_metadata_is_hashed_not_stored_raw():
    db = FakeDb()
    audit_events = []
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user, audit_sink=audit_events)
    private_note = "Zoe Spoon's horse note needs a parent check before anything official."

    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft a tack inventory note.",
            "requested_output": "draft_records",
        })
        assert created.status_code == 201
        job = created.json()["job"]
        reviewed = client.post(f"/api/ai/draft-jobs/{job['id']}/review", json={
            "action": "approved_no_save",
            "note": private_note,
        })

    assert reviewed.status_code == 200
    review_row = db["ai_draft_reviews"].rows[0]
    assert "note" not in review_row
    assert review_row["note_present"] is True
    assert review_row["note_sha256"]
    assert private_note not in str(review_row)

    review_audit = [event for event in audit_events if event["action"] == "ai.draft_job.review"][-1]
    assert review_audit["metadata"]["note_present"] is True
    assert review_audit["metadata"]["note_sha256"]
    assert private_note not in str(review_audit["metadata"])


def test_ai_extractor_failure_audit_uses_error_type_not_raw_exception_text():
    db = FakeDb()
    audit_events = []
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user, extractor=FailingExtractor(), audit_sink=audit_events)

    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Private source text for Zoe Spoon and invoice INV-123.",
            "requested_output": "draft_records",
        })

    assert created.status_code == 502
    failure_audit = audit_events[-1]
    assert failure_audit["action"] == "ai.draft_job.extract"
    assert failure_audit["metadata"]["error_type"] == "RuntimeError"
    assert "error" not in failure_audit["metadata"]
    assert "Zoe Spoon" not in str(failure_audit["metadata"])
    assert "INV-123" not in str(failure_audit["metadata"])


def test_official_save_lane_1_creates_inventory_only_after_human_review():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_text": "Four bags senior feed in the feed room.",
            "requested_output": "photo_to_inventory",
        })
        assert created.status_code == 201
        job = created.json()["job"]

        saved = client.post(f"/api/ai/draft-jobs/{job['id']}/official-save", json={
            "lane": "inventory_supply",
            "items": [{
                "name": "Senior feed",
                "category": "feed",
                "quantity": 4,
                "unit": "bag",
                "storage_location": "Feed room",
                "source_confidence": 0.88,
                "review_status": "reviewed",
            }],
            "reviewer_note": "Founder reviewed from source photo.",
        })

    assert saved.status_code == 200
    body = saved.json()
    assert body["official_records_written"] is True
    assert body["autonomous_mutation_enabled"] is False
    assert body["saved_records"][0]["collection"] == "inventory"
    assert db["inventory"].rows[0]["name"] == "Senior feed"
    assert db["inventory"].rows[0]["ai_assisted"] is True
    assert db["inventory"].rows[0]["ai_official_save_lane"] == "inventory_supply"
    assert db["inventory"].rows[0]["reviewer_user_id"] == "u_1"
    assert "reviewer_note" not in db["inventory"].rows[0]
    assert db["inventory"].rows[0]["reviewer_note_present"] is True
    assert db["inventory"].rows[0]["reviewer_note_sha256"]
    assert "invoices" not in db
    assert "horse_health_records" not in db


def test_official_save_lane_2_allows_staff_repair_ticket_creation():
    db = FakeDb()
    user = {"id": "u_groom", "role": "groom", "barn_id": "barn_1", "email": "groom@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Create a repair ticket for the loose latch on stall three.",
            "requested_output": "draft_tasks",
        })
        assert created.status_code == 201
        job = created.json()["job"]

        saved = client.post(f"/api/ai/draft-jobs/{job['id']}/official-save", json={
            "lane": "work_task_repair",
            "items": [{
                "name": "Loose latch on stall three",
                "title": "Repair loose latch on stall three",
                "category": "repair",
                "details": "Latch is loose and needs maintenance review.",
                "priority": "standard",
                "source_confidence": "high",
                "review_status": "reviewed",
            }],
        })

    assert saved.status_code == 200
    assert saved.json()["saved_records"][0]["collection"] == "ai_work_repair_tickets"
    ticket = db["ai_work_repair_tickets"].rows[0]
    assert ticket["status"] == "open"
    assert ticket["ai_assisted"] is True
    assert ticket["reviewer_role"] == "groom"


def test_official_save_blocks_low_confidence_uncorrected_and_duplicate_inventory():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_text": "Maybe senior feed in the feed room.",
            "requested_output": "photo_to_inventory",
        })
        job_id = created.json()["job"]["id"]
        blocked = client.post(f"/api/ai/draft-jobs/{job_id}/official-save", json={
            "lane": "inventory_supply",
            "items": [{
                "name": "Senior feed",
                "category": "feed",
                "storage_location": "Feed room",
                "source_confidence": "low",
                "review_status": "reviewed",
            }],
        })
        assert blocked.status_code == 422

        first = client.post(f"/api/ai/draft-jobs/{job_id}/official-save", json={
            "lane": "inventory_supply",
            "items": [{
                "name": "Senior feed",
                "category": "feed",
                "quantity": 4,
                "unit": "bag",
                "storage_location": "Feed room",
                "source_confidence": "low",
                "review_status": "corrected",
            }],
        })
        assert first.status_code == 200

        second_job = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_text": "Senior feed in the feed room again.",
            "requested_output": "photo_to_inventory",
        }).json()["job"]
        duplicate = client.post(f"/api/ai/draft-jobs/{second_job['id']}/official-save", json={
            "lane": "inventory_supply",
            "items": [{
                "name": "Senior feed",
                "category": "feed",
                "quantity": 4,
                "unit": "bag",
                "storage_location": "Feed room",
                "source_confidence": 0.9,
                "review_status": "reviewed",
            }],
        })

    assert duplicate.status_code == 409
    assert "No new official records were saved" in duplicate.text
    assert len(db["inventory"].rows) == 1


@pytest.mark.parametrize("role", ["rider", "parent", "service_provider", "farrier"])
def test_ai_draft_api_denies_roles_outside_reviewer_allowlist(role):
    db = FakeDb()
    user = {"id": f"u_{role}", "role": role, "barn_id": "barn_1", "email": f"{role}@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_text": "Draft tack room inventory candidates.",
            "requested_output": "draft_records",
        })
        listed = client.get("/api/ai/draft-jobs")
        intent = client.post("/api/ai/draft-jobs/upload-intents", json={
            "source_type": "photo_inventory",
            "filename": "tack-room.jpg",
            "mime_type": "image/jpeg",
            "byte_size": 1024,
        })

    assert created.status_code == 403
    assert listed.status_code == 403
    assert intent.status_code == 403
    assert "AI draft review access required" in created.text
    assert "ai_draft_jobs" not in db
    assert "ai_draft_sources" not in db


@pytest.mark.parametrize("role", ["groom", "working_student"])
def test_ai_draft_api_allows_staff_reviewer_flow(role):
    db = FakeDb()
    user = {"id": f"u_{role}", "role": role, "barn_id": "barn_1", "email": f"{role}@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "voice_transcript",
            "source_text": "Draft feed room supply notes.",
            "requested_output": "draft_records",
        })
        assert created.status_code == 201
        assert created.json()["job"]["draft_only"] is True


def test_ai_draft_api_allows_horse_owner_reviewer_flow():
    db = FakeDb()
    user = {"id": "u_owner", "role": "horse_owner", "barn_id": "barn_1", "email": "owner@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "photo_inventory",
            "source_text": "Draft a personal tack inventory candidate.",
            "requested_output": "draft_records",
        })
        assert created.status_code == 201
        job = created.json()["job"]
        assert job["draft_only"] is True
        assert job["review_required"] is True


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


def test_manual_review_pdf_fallback_returns_reviewable_draft_state():
    db = FakeDb()
    storage = FakeStorage()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "owner@example.test"}
    app = app_for(db, user, storage=storage, extractor=ManualReviewExtractor())
    with TestClient(app) as client:
        intent = client.post("/api/ai/draft-jobs/upload-intents", json={
            "source_type": "service_invoice",
            "filename": "farrier.pdf",
            "mime_type": "application/pdf",
            "byte_size": 1024,
        })
        source = intent.json()["source"]
        confirm = client.post(f"/api/ai/draft-jobs/upload-intents/{source['id']}/confirm", json={
            "source_id": source["id"],
            "sha256": "b" * 64,
            "byte_size": 1024,
        })
        assert confirm.status_code == 200

        job = client.post("/api/ai/draft-jobs", json={
            "source_type": "service_invoice",
            "source_id": source["id"],
            "requested_output": "draft_service_history",
        })
        assert job.status_code == 201
        body = job.json()["job"]
        assert body["status"] == "draft_needs_manual_review"
        assert body["draft_result"]["extraction_status"] == "manual_review_required"

        reviewed = client.post(f"/api/ai/draft-jobs/{body['id']}/review", json={
            "action": "rejected",
            "note": "Manual review fallback needs a clearer source.",
        })
        assert reviewed.status_code == 200
        assert reviewed.json()["review"]["official_records_written"] is False


def test_pdf_text_fallback_used_when_direct_pdf_extraction_fails():
    extractor = PdfTextFallbackExtractor()
    result = asyncio.run(extractor._extract_pdf(
        source_type="service_invoice",
        prompt="Draft service-history candidates.",
        file_bytes=b"%PDF simulated bytes",
        filename="farrier.pdf",
    ))
    assert result["draft_only"] is True
    assert result["review_required"] is True
    assert result["extraction_status"] == "draft_ready"
    assert result["fallback_used"] == "pdf_text"
    assert result["attempted_methods"] == ["openai_file", "pdf_text"]
    assert extractor.text_seen


@pytest.mark.parametrize(
    ("source_type", "expected_key", "expected_blocked_action"),
    [
        ("ride_data", "draft_ride_summary", "health_diagnosis"),
        ("lesson_schedule", "draft_schedule_candidates", "participant_notification"),
        ("training_note", "draft_training_note", "medical_or_safety_decision"),
        ("voice_transcript", "draft_tasks", "payment_status_change"),
        ("health_observation", "draft_health_score_candidate", "diagnosis"),
        ("photo_inventory", "draft_inventory_candidates", "official_record_save"),
        ("service_invoice", "draft_invoice_candidates", "official_record_save"),
    ],
)
def test_output_schema_hint_expands_domain_specific_draft_shapes(source_type, expected_key, expected_blocked_action):
    schema = output_schema_hint(source_type)

    assert f'"source_category": "{source_type}"' in schema
    assert f'"{expected_key}"' in schema
    assert '"draft_only": true' in schema
    assert '"review_required": true' in schema
    assert '"review_summary": null' in schema
    assert '"confidence": null' in schema
    assert '"missing_information": []' in schema
    assert f'"{expected_blocked_action}"' in schema


@pytest.mark.parametrize("source_type", sorted(AI_SOURCE_TYPES))
def test_output_schema_hint_includes_common_structured_review_fields(source_type):
    schema = output_schema_hint(source_type)

    assert '"review_summary": null' in schema
    assert '"confidence": null' in schema
    assert '"missing_information": []' in schema
    assert '"blocked_actions": [' in schema


@pytest.mark.parametrize("source_type", ["invoice", "service_invoice", "photo_inventory"])
def test_inventory_source_schema_includes_reviewable_candidate_shape(source_type):
    schema = json.loads(output_schema_hint(source_type))
    candidate = schema["draft_inventory_candidates"][0]

    for field in INVENTORY_CANDIDATE_TEMPLATE:
        assert field in candidate
    assert candidate["review_status"] == "needs_review"
    assert "inventory_record_create" in schema["blocked_actions"]
    assert "ai_autonomous_mutation" in schema["blocked_actions"]


def test_parse_output_normalizes_ai_response_to_no_save_review_required_payload():
    extractor = OpenAIDraftExtractor(api_key="test-key")
    parsed = extractor._parse_output(
        {
            "output_text": (
                '{"draft_only": false, "review_required": false, '
                '"source_category": "invoice", "draft_records": []}'
            )
        },
        source_type="health_observation",
    )

    assert parsed["draft_only"] is True
    assert parsed["review_required"] is True
    assert parsed["source_category"] == "health_observation"
    assert parsed["review_questions"] == []
    assert parsed["missing_information"] == []
    assert parsed["review_summary"] is None
    assert parsed["confidence"] is None
    assert "official_record_save" in parsed["blocked_actions"]
    assert "ai_autonomous_mutation" in parsed["blocked_actions"]
    assert "diagnosis" in parsed["blocked_actions"]
    assert "treatment_decision" in parsed["blocked_actions"]
    assert "treatment_recommendation" in parsed["blocked_actions"]
    assert "medication_change" in parsed["blocked_actions"]
    assert "emergency_triage" in parsed["blocked_actions"]
    assert "participant_notification" in parsed["blocked_actions"]
    assert "provider_message_send" in parsed["blocked_actions"]
    assert parsed["not_diagnosis"] is True
    assert parsed["draft_health_score_candidate"]["requires_human_confirmation"] is True


def test_health_observation_schema_is_draft_score_only_and_blocks_clinical_actions():
    schema = json.loads(output_schema_hint("health_observation"))

    assert schema["draft_only"] is True
    assert schema["review_required"] is True
    assert schema["source_category"] == "health_observation"
    assert schema["not_diagnosis"] is True
    assert schema["draft_health_score_candidate"]["requires_human_confirmation"] is True
    assert schema["draft_health_score_candidate"]["official_health_score_save_allowed"] is False
    assert schema["reviewer_boundary"]["candidate_only"] is True
    assert schema["reviewer_boundary"]["vet_or_manager_escalation_decided_by_human"] is True
    assert schema["reviewer_boundary"]["do_not_notify_or_save"] is True
    for field in [
        "appetite",
        "water_intake",
        "manure_or_urine_notes",
        "behavior_or_attitude",
        "gait_or_movement",
        "vitals_if_provided",
        "injury_or_lameness_flags",
        "pain_or_comfort_observations",
    ]:
        assert field in schema["draft_health_observation"]
    for blocked_action in [
        "official_record_save",
        "ai_autonomous_mutation",
        "diagnosis",
        "treatment_recommendation",
        "treatment_decision",
        "medication_change",
        "emergency_triage",
        "participant_notification",
        "provider_message_send",
    ]:
        assert blocked_action in schema["blocked_actions"]


def test_pilot_extraction_schemas_cover_busy_barn_draft_lanes_without_new_authority():
    photo_schema = json.loads(output_schema_hint("photo_inventory"))
    assert photo_schema["room_or_area"] is None
    assert photo_schema["visible_storage_state"] is None
    assert photo_schema["visible_count_estimates"] == []
    assert photo_schema["not_counted_or_uncertain"] == []
    assert "inventory_record_create" in photo_schema["blocked_actions"]

    invoice_schema = json.loads(output_schema_hint("service_invoice"))
    assert invoice_schema["draft_service_history_candidates"][0]["payment_status_candidate"] == "review_required"
    assert invoice_schema["draft_invoice_candidates"][0]["payment_status_candidate"] == "review_required"
    assert invoice_schema["draft_payment_status_candidate"]["official_payment_status_change_allowed"] is False
    assert "payment_status_change" in invoice_schema["blocked_actions"]
    assert "invoice_finalization" in invoice_schema["blocked_actions"]

    voice_schema = json.loads(output_schema_hint("voice_transcript"))
    assert voice_schema["voice_capture_context"]["hands_free"] is True
    assert voice_schema["draft_work_ticket_candidates"][0]["review_status"] == "needs_review"
    assert voice_schema["draft_inventory_candidates"][0]["review_status"] == "needs_review"
    assert voice_schema["draft_invoice_candidates"][0]["payment_status_candidate"] == "review_required"
    assert "participant_notification" in voice_schema["blocked_actions"]
    assert "payment_status_change" in voice_schema["blocked_actions"]


def test_parse_output_normalizes_invoice_payment_status_to_review_only():
    extractor = OpenAIDraftExtractor(api_key="test-key")
    parsed = extractor._parse_output(
        {
            "output_text": json.dumps({
                "draft_only": False,
                "review_required": False,
                "source_category": "service_invoice",
                "draft_payment_status_candidate": {
                    "status": "paid",
                    "basis": ["vendor receipt says paid"],
                    "official_payment_status_change_allowed": True,
                },
                "blocked_actions": [],
            })
        },
        source_type="service_invoice",
    )

    assert parsed["draft_only"] is True
    assert parsed["review_required"] is True
    assert parsed["draft_payment_status_candidate"]["official_payment_status_change_allowed"] is False
    assert "payment_status_change" in parsed["blocked_actions"]
    assert "invoice_finalization" in parsed["blocked_actions"]
    assert "inventory_record_create" in parsed["blocked_actions"]


def test_health_observation_cannot_request_official_health_score_save_lane():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "health_observation",
            "source_text": "Horse ate breakfast but was quieter than usual and took a few short steps.",
            "requested_output": "draft_health_score",
        })
        assert created.status_code == 201
        job = created.json()["job"]

        saved = client.post(f"/api/ai/draft-jobs/{job['id']}/official-save", json={
            "lane": "health_score",
            "items": [{
                "name": "Draft health score",
                "category": "health",
                "details": "Review-only health score candidate.",
                "source_confidence": "medium",
                "review_status": "reviewed",
            }],
        })

    assert saved.status_code == 422
    assert "horse_health_records" not in db


def test_health_observation_cannot_use_other_official_save_lanes_directly():
    db = FakeDb()
    user = {"id": "u_1", "role": "barn_manager", "barn_id": "barn_1", "email": "founder@example.test"}
    app = app_for(db, user)
    with TestClient(app) as client:
        created = client.post("/api/ai/draft-jobs", json={
            "source_type": "health_observation",
            "source_text": "Horse appears slightly stiff after turnout and needs human review.",
            "requested_output": "draft_health_score",
        })
        assert created.status_code == 201
        job = created.json()["job"]

        saved = client.post(f"/api/ai/draft-jobs/{job['id']}/official-save", json={
            "lane": "inventory_supply",
            "items": [{
                "name": "Do not save from health source",
                "category": "health",
                "details": "Direct API attempt must stay blocked.",
                "source_confidence": "high",
                "review_status": "reviewed",
            }],
        })

    assert saved.status_code == 422
    assert "not approved for this official-save lane" in saved.text
    assert "inventory" not in db
    assert "ai_work_repair_tickets" not in db
    assert "horse_health_records" not in db


def test_parse_output_normalizes_inventory_candidates_to_reviewable_shape():
    extractor = OpenAIDraftExtractor(api_key="test-key")
    parsed = extractor._parse_output(
        {
            "output_text": json.dumps({
                "draft_only": False,
                "review_required": False,
                "source_category": "invoice",
                "draft_inventory_candidates": [
                    {
                        "item_name": "Senior feed",
                        "category": "feed",
                        "quantity": 4,
                        "notes": "Check storage bin before reorder.",
                        "review_status": "ready_to_save",
                    }
                ],
                "blocked_actions": [],
            })
        },
        source_type="invoice",
    )

    candidate = parsed["draft_inventory_candidates"][0]
    assert candidate["item_name"] == "Senior feed"
    assert candidate["category"] == "feed"
    assert candidate["quantity"] == 4
    assert candidate["unit"] is None
    assert candidate["storage_location"] is None
    assert candidate["review_status"] == "needs_review"
    assert candidate["notes"] == ["Check storage bin before reorder."]
    assert "official_record_save" in parsed["blocked_actions"]
    assert "ai_autonomous_mutation" in parsed["blocked_actions"]
    assert "inventory_record_create" in parsed["blocked_actions"]


def test_invoice_schema_exposes_payment_review_boundary_without_money_mutation():
    schema = json.loads(output_schema_hint("service_invoice"))

    assert schema["draft_payment_review"]["candidate_status"] == "review_required"
    assert schema["draft_payment_review"]["requires_human_confirmation"] is True
    assert schema["draft_payment_review"]["official_payment_status_change_allowed"] is False
    assert schema["draft_payment_review"]["invoice_finalization_allowed"] is False
    assert schema["draft_payment_review"]["subscription_entitlement_change_allowed"] is False
    assert schema["draft_reconciliation_questions"] == []
    for blocked_action in [
        "payment_status_change",
        "invoice_finalization",
        "charge_money",
        "refund_or_credit",
        "subscription_entitlement_change",
    ]:
        assert blocked_action in schema["blocked_actions"]


def test_invoice_payment_review_normalization_overrides_unsafe_model_flags():
    extractor = OpenAIDraftExtractor(api_key="test-key")
    parsed = extractor._parse_output(
        {
            "output_text": json.dumps({
                "draft_only": False,
                "review_required": False,
                "source_category": "invoice",
                "draft_payment_status_candidate": {
                    "status": "paid",
                    "basis": "invoice says paid",
                    "official_payment_status_change_allowed": True,
                },
                "draft_payment_review": {
                    "candidate_status": "paid",
                    "basis": "invoice stamp",
                    "official_payment_status_change_allowed": True,
                    "invoice_finalization_allowed": True,
                    "subscription_entitlement_change_allowed": True,
                },
                "draft_reconciliation_questions": "Was this already matched to Stripe?",
                "blocked_actions": [],
            })
        },
        source_type="invoice",
    )

    assert parsed["draft_only"] is True
    assert parsed["review_required"] is True
    assert parsed["draft_payment_status_candidate"]["official_payment_status_change_allowed"] is False
    payment_review = parsed["draft_payment_review"]
    assert payment_review["candidate_status"] == "paid"
    assert payment_review["basis"] == ["invoice stamp"]
    assert payment_review["requires_human_confirmation"] is True
    assert payment_review["official_payment_status_change_allowed"] is False
    assert payment_review["invoice_finalization_allowed"] is False
    assert payment_review["subscription_entitlement_change_allowed"] is False
    assert parsed["draft_reconciliation_questions"] == []
    for blocked_action in [
        "payment_status_change",
        "invoice_finalization",
        "charge_money",
        "refund_or_credit",
        "subscription_entitlement_change",
    ]:
        assert blocked_action in parsed["blocked_actions"]


def test_pdf_manual_review_payload_when_all_pdf_fallbacks_fail():
    extractor = PdfManualFallbackExtractor()
    result = asyncio.run(extractor._extract_pdf(
        source_type="service_invoice",
        prompt="Draft service-history candidates.",
        file_bytes=b"%PDF simulated bytes",
        filename="farrier.pdf",
    ))
    assert result["draft_only"] is True
    assert result["review_required"] is True
    assert result["extraction_status"] == "manual_review_required"
    assert result["attempted_methods"] == ["openai_file", "pdf_text", "pdf_page_images"]
    assert "ai_autonomous_mutation" in result["blocked_actions"]
    assert "automatic_extraction" in result["blocked_actions"]


def test_ai_source_validation_and_private_key_boundaries():
    assert normalize_source_type("Invoice") == "invoice"
    assert validate_ai_source(source_type="invoice", mime_type="application/pdf", byte_size=10) == "application/pdf"
    with pytest.raises(ValueError):
        validate_ai_source(source_type="photo_inventory", mime_type="application/pdf", byte_size=10)
    key = private_ai_storage_key(barn_id="barn_1", source_id="ai_src_1", filename="../Bad File.PDF")
    assert key == "barn_1/ai-draft-sources/ai_src_1/source.pdf"
