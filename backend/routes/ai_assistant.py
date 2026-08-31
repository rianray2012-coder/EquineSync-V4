"""Draft-only AI intake and extraction pipeline.

The route owns staging AI jobs only. It never creates official inventory,
horse-health, schedule, invoice, payment, message, or access-control records.
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field, field_validator

from core.permissions import require
from core.tenancy import resolve_barn_id
from services.ai_draft_extractor import (
    AIStorageClient,
    OpenAIDraftExtractor,
    normalize_source_type,
    private_ai_storage_key,
    validate_ai_source,
)


AI_SOURCE_COLLECTION = "ai_draft_sources"
AI_JOB_COLLECTION = "ai_draft_jobs"
AI_REVIEW_COLLECTION = "ai_draft_reviews"

TERMINAL_REVIEW_STATES = {"approved_no_save", "rejected"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _source_projection(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": doc["id"],
        "source_type": doc["source_type"],
        "status": doc["status"],
        "filename": doc.get("filename"),
        "mime_type": doc.get("mime_type"),
        "byte_size": doc.get("byte_size"),
        "sha256": doc.get("sha256"),
        "created_at": doc.get("created_at"),
        "uploaded_at": doc.get("uploaded_at"),
    }


def _job_projection(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": doc["id"],
        "source_id": doc.get("source_id"),
        "source_type": doc["source_type"],
        "status": doc["status"],
        "draft_only": True,
        "review_required": True,
        "requested_output": doc.get("requested_output"),
        "draft_result": doc.get("draft_result"),
        "review_status": doc.get("review_status"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
        "completed_at": doc.get("completed_at"),
        "error_code": doc.get("error_code"),
    }


async def _default_audit_record(**kwargs) -> None:
    from core import audit

    await audit.record(**kwargs)


class UploadIntentIn(BaseModel):
    source_type: str = Field(..., max_length=64)
    filename: str = Field(..., min_length=1, max_length=180)
    mime_type: str = Field(..., max_length=120)
    byte_size: int = Field(..., gt=0)
    prompt_hint: Optional[str] = Field(default=None, max_length=500)

    @field_validator("source_type")
    @classmethod
    def valid_source_type(cls, value):  # noqa: N805
        return normalize_source_type(value)

    @field_validator("filename", "mime_type", "prompt_hint", mode="before")
    @classmethod
    def trim_text(cls, value):  # noqa: N805
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Input should be a valid string")
        return value.strip()


class UploadConfirmIn(BaseModel):
    source_id: str = Field(..., min_length=8, max_length=80)
    sha256: Optional[str] = Field(default=None, max_length=64)
    byte_size: Optional[int] = Field(default=None, gt=0)


class DraftJobCreateIn(BaseModel):
    source_type: str = Field(..., max_length=64)
    requested_output: str = Field(default="draft_extraction", max_length=80)
    prompt: Optional[str] = Field(default=None, max_length=1200)
    source_id: Optional[str] = Field(default=None, max_length=80)
    source_text: Optional[str] = Field(default=None, max_length=16000)

    @field_validator("source_type")
    @classmethod
    def valid_source_type(cls, value):  # noqa: N805
        return normalize_source_type(value)

    @field_validator("requested_output", "prompt", "source_id", "source_text", mode="before")
    @classmethod
    def trim_text(cls, value):  # noqa: N805
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Input should be a valid string")
        return value.strip()


class DraftReviewIn(BaseModel):
    action: str = Field(..., max_length=32)
    note: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("action")
    @classmethod
    def valid_action(cls, value):  # noqa: N805
        normalized = (value or "").strip().lower()
        if normalized not in TERMINAL_REVIEW_STATES:
            raise ValueError("Review action must be approved_no_save or rejected")
        return normalized

    @field_validator("note", mode="before")
    @classmethod
    def trim_note(cls, value):  # noqa: N805
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Input should be a valid string")
        return value.strip() or None


def build_router(*, db, get_current_user, extractor=None, storage_client=None, audit_record=None) -> APIRouter:
    router = APIRouter(prefix="/ai/draft-jobs", tags=["ai-draft-jobs"])
    extractor = extractor if extractor is not None else OpenAIDraftExtractor()
    storage_client = storage_client if storage_client is not None else AIStorageClient()
    audit_record = audit_record if audit_record is not None else _default_audit_record

    @router.post("/upload-intents", status_code=201)
    async def create_upload_intent(
        body: UploadIntentIn,
        request: Request,
        user=Depends(get_current_user),
    ):
        require(user, "ai_draft:review")
        try:
            mime_type = validate_ai_source(
                source_type=body.source_type,
                mime_type=body.mime_type,
                byte_size=body.byte_size,
            )
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        if not storage_client.configured():
            raise HTTPException(503, "Private AI storage is not configured")
        source_id = f"ai_src_{uuid.uuid4()}"
        now = _now_iso()
        barn_id = resolve_barn_id(user)
        storage_key = private_ai_storage_key(
            barn_id=barn_id,
            source_id=source_id,
            filename=body.filename,
        )
        upload_url = storage_client.presigned_put(key=storage_key, mime_type=mime_type)
        doc = {
            "id": source_id,
            "barn_id": barn_id,
            "user_id": user.get("id"),
            "source_type": body.source_type,
            "filename": body.filename,
            "mime_type": mime_type,
            "byte_size": body.byte_size,
            "storage_key": storage_key,
            "status": "upload_pending",
            "prompt_hint": body.prompt_hint,
            "created_at": now,
            "updated_at": now,
            "uploaded_at": None,
        }
        await db[AI_SOURCE_COLLECTION].insert_one(doc)
        await audit_record(
            action="ai.source.upload_intent.create",
            user=user,
            request=request,
            resource_type="ai_draft_source",
            resource_id=source_id,
            status_code=201,
            metadata={
                "source_type": body.source_type,
                "mime_type": mime_type,
                "byte_size": body.byte_size,
                "storage_key_present": True,
            },
        )
        return {
            "source": _source_projection(doc),
            "upload": {
                "method": "PUT",
                "url": upload_url,
                "headers": {"Content-Type": mime_type},
                "expires_in_seconds": 900,
            },
        }

    @router.post("/upload-intents/{source_id}/confirm")
    async def confirm_upload(
        source_id: str,
        body: UploadConfirmIn,
        request: Request,
        user=Depends(get_current_user),
    ):
        require(user, "ai_draft:review")
        if source_id != body.source_id:
            raise HTTPException(400, "source_id mismatch")
        source = await db[AI_SOURCE_COLLECTION].find_one(
            {"id": source_id, "barn_id": resolve_barn_id(user), "user_id": user.get("id")},
            {"_id": 0},
        )
        if not source:
            raise HTTPException(404, "AI source not found")
        now = _now_iso()
        update = {
            "status": "uploaded",
            "updated_at": now,
            "uploaded_at": now,
        }
        if body.sha256:
            update["sha256"] = body.sha256.lower()
        if body.byte_size:
            update["confirmed_byte_size"] = body.byte_size
        await db[AI_SOURCE_COLLECTION].update_one({"id": source_id}, {"$set": update})
        source.update(update)
        await audit_record(
            action="ai.source.upload.confirm",
            user=user,
            request=request,
            resource_type="ai_draft_source",
            resource_id=source_id,
            status_code=200,
            metadata={"sha256_present": bool(body.sha256), "byte_size_present": bool(body.byte_size)},
        )
        return {"source": _source_projection(source)}

    @router.post("", status_code=201)
    async def create_draft_job(
        body: DraftJobCreateIn,
        request: Request,
        user=Depends(get_current_user),
    ):
        require(user, "ai_draft:review")
        if bool(body.source_id) == bool(body.source_text):
            raise HTTPException(400, "Provide exactly one of source_id or source_text")
        barn_id = resolve_barn_id(user)
        now = _now_iso()
        job_id = f"ai_job_{uuid.uuid4()}"
        source_doc = None
        source_text = body.source_text
        file_bytes = None
        mime_type = "text/plain"
        filename = "source.txt"
        if body.source_id:
            source_doc = await db[AI_SOURCE_COLLECTION].find_one(
                {"id": body.source_id, "barn_id": barn_id, "user_id": user.get("id")},
                {"_id": 0},
            )
            if not source_doc:
                raise HTTPException(404, "AI source not found")
            if source_doc.get("status") != "uploaded":
                raise HTTPException(409, "AI source upload is not confirmed")
            if source_doc.get("source_type") != body.source_type:
                raise HTTPException(400, "source_type mismatch")
            stored = storage_client.read_bytes(
                key=source_doc["storage_key"],
                mime_type=source_doc["mime_type"],
            )
            file_bytes = stored.bytes_value
            mime_type = stored.mime_type
            filename = source_doc.get("filename") or filename
        else:
            source_hash = _hash_text(source_text or "")
            source_doc = {
                "id": f"ai_src_{uuid.uuid4()}",
                "barn_id": barn_id,
                "user_id": user.get("id"),
                "source_type": body.source_type,
                "filename": "inline-source.txt",
                "mime_type": "text/plain",
                "byte_size": len((source_text or "").encode("utf-8")),
                "sha256": source_hash,
                "status": "inline_ready",
                "storage_key": None,
                "created_at": now,
                "updated_at": now,
                "uploaded_at": now,
            }
            await db[AI_SOURCE_COLLECTION].insert_one(source_doc)
        job = {
            "id": job_id,
            "barn_id": barn_id,
            "user_id": user.get("id"),
            "source_id": source_doc["id"],
            "source_type": body.source_type,
            "requested_output": body.requested_output,
            "prompt": body.prompt,
            "status": "running",
            "draft_only": True,
            "review_required": True,
            "review_status": "pending_review",
            "draft_result": None,
            "error_code": None,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
        }
        await db[AI_JOB_COLLECTION].insert_one(job)
        try:
            draft = await extractor.extract(
                source_type=body.source_type,
                prompt=body.prompt or body.requested_output,
                text=source_text,
                file_bytes=file_bytes,
                mime_type=mime_type,
                filename=filename,
            )
            draft["draft_only"] = True
            draft["review_required"] = True
            completed = _now_iso()
            job_status = (
                "draft_needs_manual_review"
                if draft.get("extraction_status") == "manual_review_required"
                else "draft_ready"
            )
            update = {
                "status": job_status,
                "draft_result": draft,
                "updated_at": completed,
                "completed_at": completed,
            }
            await db[AI_JOB_COLLECTION].update_one({"id": job_id}, {"$set": update})
            job.update(update)
            await audit_record(
                action="ai.draft_job.extract",
                user=user,
                request=request,
                resource_type="ai_draft_job",
                resource_id=job_id,
                status_code=201,
                metadata={
                    "source_type": body.source_type,
                    "source_id": source_doc["id"],
                    "draft_ready": job_status == "draft_ready",
                    "manual_review_required": job_status == "draft_needs_manual_review",
                    "official_records_written": False,
                },
            )
            return {"job": _job_projection(job)}
        except Exception as exc:  # noqa: BLE001 - error is converted to job state
            failed = _now_iso()
            update = {
                "status": "extraction_failed",
                "error_code": "extractor_failed",
                "updated_at": failed,
                "completed_at": failed,
            }
            await db[AI_JOB_COLLECTION].update_one({"id": job_id}, {"$set": update})
            job.update(update)
            await audit_record(
                action="ai.draft_job.extract",
                user=user,
                request=request,
                resource_type="ai_draft_job",
                resource_id=job_id,
                outcome="failure",
                status_code=502,
                metadata={"source_type": body.source_type, "error": str(exc), "official_records_written": False},
            )
            raise HTTPException(502, "AI draft extraction failed") from exc

    @router.get("")
    async def list_draft_jobs(
        status: Optional[str] = Query(default=None, max_length=40),
        review_status: Optional[str] = Query(default=None, max_length=40),
        limit: int = Query(default=25, ge=1, le=100),
        user=Depends(get_current_user),
    ):
        require(user, "ai_draft:review")
        query = {"barn_id": resolve_barn_id(user), "user_id": user.get("id")}
        if status:
            query["status"] = status.strip()
        if review_status:
            query["review_status"] = review_status.strip()
        cursor = db[AI_JOB_COLLECTION].find(query, {"_id": 0, "prompt": 0}).sort("created_at", -1).limit(limit)
        jobs = await cursor.to_list(length=limit)
        return {"jobs": [_job_projection(job) for job in jobs]}

    @router.get("/{job_id}")
    async def get_draft_job(job_id: str, user=Depends(get_current_user)):
        require(user, "ai_draft:review")
        job = await db[AI_JOB_COLLECTION].find_one(
            {"id": job_id, "barn_id": resolve_barn_id(user), "user_id": user.get("id")},
            {"_id": 0, "prompt": 0},
        )
        if not job:
            raise HTTPException(404, "AI draft job not found")
        return {"job": _job_projection(job)}

    @router.post("/{job_id}/review")
    async def review_draft_job(
        job_id: str,
        body: DraftReviewIn,
        request: Request,
        user=Depends(get_current_user),
    ):
        require(user, "ai_draft:review")
        job = await db[AI_JOB_COLLECTION].find_one(
            {"id": job_id, "barn_id": resolve_barn_id(user), "user_id": user.get("id")},
            {"_id": 0},
        )
        if not job:
            raise HTTPException(404, "AI draft job not found")
        if job.get("status") not in {"draft_ready", "draft_needs_manual_review"}:
            raise HTTPException(409, "AI draft job is not ready for review")
        now = _now_iso()
        review = {
            "id": f"ai_review_{uuid.uuid4()}",
            "job_id": job_id,
            "barn_id": resolve_barn_id(user),
            "user_id": user.get("id"),
            "action": body.action,
            "note": body.note,
            "official_records_written": False,
            "created_at": now,
        }
        await db[AI_REVIEW_COLLECTION].insert_one(review)
        await db[AI_JOB_COLLECTION].update_one(
            {"id": job_id},
            {"$set": {"review_status": body.action, "updated_at": now}},
        )
        await audit_record(
            action="ai.draft_job.review",
            user=user,
            request=request,
            resource_type="ai_draft_job",
            resource_id=job_id,
            status_code=200,
            metadata={
                "review_action": body.action,
                "official_records_written": False,
                "save_workflow": "not_implemented_in_this_slice",
            },
        )
        job["review_status"] = body.action
        job["updated_at"] = now
        return {
            "job": _job_projection(job),
            "review": {
                "id": review["id"],
                "action": body.action,
                "official_records_written": False,
            },
        }

    return router
