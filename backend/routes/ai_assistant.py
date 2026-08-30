"""AI intake, extraction, and tightly-gated review workflows.

Default extraction remains draft-only. Official-save behavior is intentionally
limited to Founder-approved lanes and requires an explicit human review action.
It never creates horse-health scores, invoices/payment state, signatures,
messages, schedules, notifications, or access-control records.
"""
from __future__ import annotations

import hashlib
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field, field_validator

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
AI_USAGE_COLLECTION = "ai_usage_daily"
AI_OFFICIAL_SAVE_COLLECTIONS = {
    "inventory_supply": "inventory",
    "work_task_repair": "ai_work_repair_tickets",
}
AI_OFFICIAL_SAVE_SOURCE_TYPES = {
    "inventory_supply": {"invoice", "service_invoice", "photo_inventory", "voice_transcript"},
    "work_task_repair": {"training_note", "voice_transcript"},
}

TERMINAL_REVIEW_STATES = {"approved_no_save", "rejected"}
AI_DRAFT_ALLOWED_ROLES = {
    "admin",
    "barn_owner",
    "barn_manager",
    "trainer",
    "horse_owner",
    "groom",
    "working_student",
}
AI_OFFICIAL_SAVE_ALLOWED_ROLES = {"admin", "barn_owner", "barn_manager", "trainer", "groom", "working_student"}
AI_OFFICIAL_SAVE_LANE_ROLES = {
    "inventory_supply": AI_OFFICIAL_SAVE_ALLOWED_ROLES,
    "work_task_repair": AI_OFFICIAL_SAVE_ALLOWED_ROLES,
}
AI_OFFICIAL_SAVE_MIN_CONFIDENCE = 0.60
AI_DEFAULT_DAILY_JOB_LIMIT = 50
AI_DEFAULT_DAILY_ESTIMATED_TOKEN_LIMIT = 200_000
AI_DEFAULT_DAILY_SOURCE_BYTE_LIMIT = 50 * 1024 * 1024
AI_OUTPUT_TOKEN_BUDGET = 1800


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return int(str(raw).strip())
    except ValueError:
        return default


def _env_bool(name: str, default: bool = True) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return str(raw).strip().lower() not in {"0", "false", "no", "off"}


def _ai_budget_config() -> Dict[str, Any]:
    return {
        "enforcement_enabled": _env_bool("AI_BUDGET_ENFORCEMENT_ENABLED", True),
        "daily_job_limit": max(0, _env_int("AI_DAILY_JOB_LIMIT", AI_DEFAULT_DAILY_JOB_LIMIT)),
        "daily_estimated_token_limit": max(
            0,
            _env_int("AI_DAILY_ESTIMATED_TOKEN_LIMIT", AI_DEFAULT_DAILY_ESTIMATED_TOKEN_LIMIT),
        ),
        "daily_source_byte_limit": max(
            0,
            _env_int("AI_DAILY_SOURCE_BYTE_LIMIT", AI_DEFAULT_DAILY_SOURCE_BYTE_LIMIT),
        ),
        "per_request_output_token_budget": AI_OUTPUT_TOKEN_BUDGET,
    }


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _private_text_metadata(field: str, value: Optional[str]) -> Dict[str, Any]:
    clean = (value or "").strip()
    return {
        f"{field}_present": bool(clean),
        f"{field}_sha256": _hash_text(clean) if clean else None,
        f"{field}_length": len(clean),
    }


def _filename_extension(value: Optional[str], *, mime_type: Optional[str] = None) -> Optional[str]:
    filename = (value or "").strip()
    if "." in filename:
        raw_extension = filename.rsplit(".", 1)[-1].lower()
        safe_extension = "".join(c for c in raw_extension if c.isalnum())[:12]
        if safe_extension:
            return safe_extension
    subtype = (mime_type or "").split("/")[-1].strip().lower()
    if subtype:
        safe_subtype = "".join(c for c in subtype if c.isalnum())[:12]
        return safe_subtype or None
    return None


def _generic_source_filename(original: Optional[str], *, mime_type: Optional[str] = None) -> str:
    extension = _filename_extension(original, mime_type=mime_type)
    return f"source.{extension}" if extension else "source"


def _require_ai_draft_role(user: Dict[str, Any]) -> None:
    if (user or {}).get("role") not in AI_DRAFT_ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail="AI draft review access required")


def _require_ai_official_save_role(user: Dict[str, Any], lane: str) -> None:
    if (user or {}).get("role") not in AI_OFFICIAL_SAVE_LANE_ROLES.get(lane, set()):
        raise HTTPException(status_code=403, detail="AI official-save access required")


def _normalized_text(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _confidence_value(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        return number / 100 if number > 1 else number
    label = _normalized_text(value)
    if label in {"high", "certain"}:
        return 0.9
    if label in {"medium", "moderate"}:
        return 0.7
    if label in {"low", "uncertain"}:
        return 0.4
    try:
        number = float(label.replace("%", ""))
        return number / 100 if number > 1 else number
    except ValueError:
        return None


def _require_save_ready_item(item: Dict[str, Any], *, index: int) -> None:
    review_status = _normalized_text(item.get("review_status"))
    if review_status not in {"reviewed", "corrected", "approved"}:
        raise HTTPException(422, f"Item {index + 1} must be reviewed before official save")
    confidence = _confidence_value(item.get("source_confidence", item.get("confidence")))
    if confidence is not None and confidence < AI_OFFICIAL_SAVE_MIN_CONFIDENCE and review_status != "corrected":
        raise HTTPException(422, f"Item {index + 1} needs correction before official save")


def _source_hash(job: Dict[str, Any]) -> Optional[str]:
    draft = job.get("draft_result") or {}
    return job.get("source_sha256") or draft.get("source_sha256") or draft.get("sha256")


def _estimate_ai_usage(*, source_text: Optional[str], source_doc: Dict[str, Any]) -> Dict[str, int]:
    if source_text is not None:
        source_bytes = len((source_text or "").encode("utf-8"))
    else:
        source_bytes = int(source_doc.get("confirmed_byte_size") or source_doc.get("byte_size") or 0)
    estimated_input_tokens = max(1, (source_bytes + 3) // 4)
    return {
        "source_bytes": source_bytes,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": AI_OUTPUT_TOKEN_BUDGET,
        "estimated_total_tokens": estimated_input_tokens + AI_OUTPUT_TOKEN_BUDGET,
    }


def _empty_usage_doc(*, barn_id: str, date_key: str) -> Dict[str, Any]:
    now = _now_iso()
    return {
        "id": f"ai_usage_{barn_id}_{date_key}",
        "barn_id": barn_id,
        "date": date_key,
        "draft_jobs_created": 0,
        "estimated_tokens_used": 0,
        "source_bytes_processed": 0,
        "by_source_type": {},
        "created_at": now,
        "updated_at": now,
    }


async def _load_ai_usage(db, *, barn_id: str, date_key: str) -> Dict[str, Any]:
    row = await db[AI_USAGE_COLLECTION].find_one(
        {"barn_id": barn_id, "date": date_key},
        {"_id": 0},
    )
    return row or _empty_usage_doc(barn_id=barn_id, date_key=date_key)


def _budget_exceeded_message(limit_name: str) -> str:
    labels = {
        "daily_job_limit": "Daily AI draft job limit reached",
        "daily_estimated_token_limit": "Daily AI estimated token budget reached",
        "daily_source_byte_limit": "Daily AI source processing budget reached",
    }
    return labels.get(limit_name, "Daily AI budget reached")


def _check_ai_budget_capacity(
    *,
    usage: Dict[str, Any],
    estimate: Dict[str, int],
    config: Dict[str, Any],
) -> None:
    if not config["enforcement_enabled"]:
        return
    checks = [
        ("daily_job_limit", int(usage.get("draft_jobs_created") or 0) + 1),
        (
            "daily_estimated_token_limit",
            int(usage.get("estimated_tokens_used") or 0) + estimate["estimated_total_tokens"],
        ),
        (
            "daily_source_byte_limit",
            int(usage.get("source_bytes_processed") or 0) + estimate["source_bytes"],
        ),
    ]
    for key, projected_value in checks:
        limit = int(config.get(key) or 0)
        if limit > 0 and projected_value > limit:
            raise HTTPException(status_code=429, detail=_budget_exceeded_message(key))


async def _record_ai_usage(
    db,
    *,
    barn_id: str,
    user_id: Optional[str],
    source_type: str,
    estimate: Dict[str, int],
) -> Dict[str, Any]:
    date_key = _today_key()
    usage = await _load_ai_usage(db, barn_id=barn_id, date_key=date_key)
    by_source_type = dict(usage.get("by_source_type") or {})
    source_bucket = dict(by_source_type.get(source_type) or {})
    source_bucket["draft_jobs_created"] = int(source_bucket.get("draft_jobs_created") or 0) + 1
    source_bucket["estimated_tokens_used"] = (
        int(source_bucket.get("estimated_tokens_used") or 0) + estimate["estimated_total_tokens"]
    )
    by_source_type[source_type] = source_bucket
    update = {
        "draft_jobs_created": int(usage.get("draft_jobs_created") or 0) + 1,
        "estimated_tokens_used": int(usage.get("estimated_tokens_used") or 0) + estimate["estimated_total_tokens"],
        "source_bytes_processed": int(usage.get("source_bytes_processed") or 0) + estimate["source_bytes"],
        "last_user_id": user_id,
        "by_source_type": by_source_type,
        "updated_at": _now_iso(),
    }
    if await db[AI_USAGE_COLLECTION].find_one({"barn_id": barn_id, "date": date_key}, {"_id": 0}):
        await db[AI_USAGE_COLLECTION].update_one(
            {"barn_id": barn_id, "date": date_key},
            {"$set": update},
        )
        usage.update(update)
    else:
        usage.update(update)
        await db[AI_USAGE_COLLECTION].insert_one(usage)
    return usage


def _usage_projection(usage: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    tokens_used = int(usage.get("estimated_tokens_used") or 0)
    jobs_used = int(usage.get("draft_jobs_created") or 0)
    bytes_used = int(usage.get("source_bytes_processed") or 0)
    return {
        "date": usage.get("date"),
        "enforcement_enabled": bool(config["enforcement_enabled"]),
        "draft_jobs_created": jobs_used,
        "estimated_tokens_used": tokens_used,
        "source_bytes_processed": bytes_used,
        "daily_job_limit": config["daily_job_limit"],
        "daily_estimated_token_limit": config["daily_estimated_token_limit"],
        "daily_source_byte_limit": config["daily_source_byte_limit"],
        "remaining_jobs": max(0, config["daily_job_limit"] - jobs_used) if config["daily_job_limit"] else None,
        "remaining_estimated_tokens": (
            max(0, config["daily_estimated_token_limit"] - tokens_used)
            if config["daily_estimated_token_limit"]
            else None
        ),
        "remaining_source_bytes": (
            max(0, config["daily_source_byte_limit"] - bytes_used)
            if config["daily_source_byte_limit"]
            else None
        ),
        "by_source_type": usage.get("by_source_type") or {},
        "policy": {
            "draft_only_default": True,
            "human_review_required": True,
            "autonomous_mutation_enabled": False,
            "higher_risk_lanes_separately_gated": True,
            "official_save_lanes_enabled": sorted(AI_OFFICIAL_SAVE_COLLECTIONS),
        },
    }


def _source_projection(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": doc["id"],
        "source_type": doc["source_type"],
        "status": doc["status"],
        "filename_present": bool(doc.get("filename_present", doc.get("filename"))),
        "filename_extension": doc.get("filename_extension") or _filename_extension(
            doc.get("filename"),
            mime_type=doc.get("mime_type"),
        ),
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
        "official_save_status": doc.get("official_save_status"),
        "official_records_written": bool(doc.get("official_records_written")),
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


class OfficialSaveItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=180)
    category: Optional[str] = Field(default=None, max_length=80)
    quantity: Optional[float] = None
    unit: Optional[str] = Field(default=None, max_length=40)
    storage_location: Optional[str] = Field(default=None, max_length=160)
    horse_or_barn_assignment: Optional[str] = Field(default=None, max_length=160)
    title: Optional[str] = Field(default=None, max_length=180)
    details: Optional[str] = Field(default=None, max_length=1200)
    priority: Literal["critical", "standard", "informational"] = "standard"
    due_date: Optional[str] = Field(default=None, max_length=40)
    assigned_user_id: Optional[str] = Field(default=None, max_length=80)
    assigned_role: Optional[str] = Field(default=None, max_length=80)
    source_confidence: Optional[Any] = None
    review_status: str = Field(..., max_length=40)
    notes: Optional[List[str] | str] = None

    @field_validator(
        "name",
        "category",
        "unit",
        "storage_location",
        "horse_or_barn_assignment",
        "title",
        "details",
        "due_date",
        "assigned_user_id",
        "assigned_role",
        "review_status",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Input should be a valid string")
        return value.strip() or None

    @field_validator("review_status")
    @classmethod
    def require_review_status(cls, value):  # noqa: N805
        if not value:
            raise ValueError("review_status is required")
        return value


class OfficialSaveIn(BaseModel):
    lane: Literal["inventory_supply", "work_task_repair"]
    items: List[OfficialSaveItemIn] = Field(..., min_length=1, max_length=25)
    reviewer_note: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("reviewer_note", mode="before")
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
        _require_ai_draft_role(user)
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
        generic_filename = _generic_source_filename(body.filename, mime_type=mime_type)
        upload_url = storage_client.presigned_put(key=storage_key, mime_type=mime_type)
        doc = {
            "id": source_id,
            "barn_id": barn_id,
            "user_id": user.get("id"),
            "source_type": body.source_type,
            "filename": generic_filename,
            "filename_present": True,
            "filename_sha256": _hash_text(body.filename),
            "filename_extension": _filename_extension(body.filename, mime_type=mime_type),
            "mime_type": mime_type,
            "byte_size": body.byte_size,
            "storage_key": storage_key,
            "status": "upload_pending",
            **_private_text_metadata("prompt_hint", body.prompt_hint),
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
                "filename_present": True,
                "filename_extension": _filename_extension(body.filename, mime_type=mime_type),
                **_private_text_metadata("prompt_hint", body.prompt_hint),
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
        _require_ai_draft_role(user)
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
        _require_ai_draft_role(user)
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
        inline_source_doc = None
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
            mime_type = source_doc["mime_type"]
            filename = source_doc.get("filename") or _generic_source_filename(None, mime_type=mime_type)
        else:
            source_hash = _hash_text(source_text or "")
            inline_source_doc = {
                "id": f"ai_src_{uuid.uuid4()}",
                "barn_id": barn_id,
                "user_id": user.get("id"),
                "source_type": body.source_type,
                "filename": "inline-source.txt",
                "filename_present": False,
                "filename_extension": "txt",
                "mime_type": "text/plain",
                "byte_size": len((source_text or "").encode("utf-8")),
                "sha256": source_hash,
                "status": "inline_ready",
                "storage_key": None,
                "created_at": now,
                "updated_at": now,
                "uploaded_at": now,
            }
            source_doc = inline_source_doc
        job = {
            "id": job_id,
            "barn_id": barn_id,
            "user_id": user.get("id"),
            "source_id": source_doc["id"],
            "source_type": body.source_type,
            "requested_output": body.requested_output,
            **_private_text_metadata("prompt", body.prompt),
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
        usage_estimate = _estimate_ai_usage(source_text=source_text, source_doc=source_doc)
        budget_config = _ai_budget_config()
        usage = await _load_ai_usage(db, barn_id=barn_id, date_key=_today_key())
        _check_ai_budget_capacity(
            usage=usage,
            estimate=usage_estimate,
            config=budget_config,
        )
        if inline_source_doc is not None:
            await db[AI_SOURCE_COLLECTION].insert_one(inline_source_doc)
        await db[AI_JOB_COLLECTION].insert_one(job)
        try:
            if body.source_id:
                stored = storage_client.read_bytes(
                    key=source_doc["storage_key"],
                    mime_type=source_doc["mime_type"],
                )
                file_bytes = stored.bytes_value
                mime_type = stored.mime_type
            usage_after = await _record_ai_usage(
                db,
                barn_id=barn_id,
                user_id=user.get("id"),
                source_type=body.source_type,
                estimate=usage_estimate,
            )
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
                    "ai_usage_date": usage_after.get("date"),
                    "estimated_total_tokens": usage_estimate["estimated_total_tokens"],
                    "daily_estimated_tokens_used": usage_after.get("estimated_tokens_used"),
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
                metadata={
                    "source_type": body.source_type,
                    "error_type": exc.__class__.__name__,
                    "estimated_total_tokens": usage_estimate["estimated_total_tokens"],
                    "official_records_written": False,
                },
            )
            raise HTTPException(502, "AI draft extraction failed") from exc

    @router.get("/usage-policy")
    async def get_ai_usage_policy(user=Depends(get_current_user)):
        _require_ai_draft_role(user)
        barn_id = resolve_barn_id(user)
        config = _ai_budget_config()
        usage = await _load_ai_usage(db, barn_id=barn_id, date_key=_today_key())
        return {"usage": _usage_projection(usage, config)}

    @router.get("")
    async def list_draft_jobs(
        status: Optional[str] = Query(default=None, max_length=40),
        review_status: Optional[str] = Query(default=None, max_length=40),
        limit: int = Query(default=25, ge=1, le=100),
        user=Depends(get_current_user),
    ):
        _require_ai_draft_role(user)
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
        _require_ai_draft_role(user)
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
        _require_ai_draft_role(user)
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
            **_private_text_metadata("note", body.note),
            "official_records_written": False,
            "created_at": now,
        }
        await db[AI_REVIEW_COLLECTION].insert_one(review)
        review.pop("_id", None)
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
                **_private_text_metadata("note", body.note),
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

    @router.post("/{job_id}/official-save")
    async def official_save_draft_job(
        job_id: str,
        body: OfficialSaveIn,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_ai_draft_role(user)
        _require_ai_official_save_role(user, body.lane)
        barn_id = resolve_barn_id(user)
        job = await db[AI_JOB_COLLECTION].find_one(
            {"id": job_id, "barn_id": barn_id, "user_id": user.get("id")},
            {"_id": 0},
        )
        if not job:
            raise HTTPException(404, "AI draft job not found")
        if job.get("status") != "draft_ready":
            raise HTTPException(409, "AI draft job must be draft_ready before official save")
        if job.get("review_status") in TERMINAL_REVIEW_STATES:
            raise HTTPException(409, "AI draft job has already been terminally reviewed")
        if job.get("source_type") not in AI_OFFICIAL_SAVE_SOURCE_TYPES[body.lane]:
            raise HTTPException(422, "AI draft source type is not approved for this official-save lane")

        now = _now_iso()
        source_hash = _source_hash(job)
        target_collection = AI_OFFICIAL_SAVE_COLLECTIONS[body.lane]
        saved_records = []
        duplicate_records = []

        for index, item_model in enumerate(body.items):
            item = item_model.model_dump()
            _require_save_ready_item(item, index=index)
            duplicate_key = "|".join([
                body.lane,
                _normalized_text(item.get("name") or item.get("title")),
                _normalized_text(item.get("category")),
                _normalized_text(item.get("storage_location") or item.get("due_date")),
            ])
            duplicate = await db[target_collection].find_one(
                {
                    "barn_id": barn_id,
                    "ai_duplicate_key": duplicate_key,
                    "deleted_at": None,
                },
                {"_id": 0, "id": 1, "name": 1, "title": 1},
            )
            if duplicate:
                duplicate_records.append({
                    "index": index,
                    "existing_record_id": duplicate.get("id"),
                    "name": duplicate.get("name") or duplicate.get("title"),
                })
                continue

            base = {
                "id": f"ai_save_{uuid.uuid4()}",
                "barn_id": barn_id,
                "ai_assisted": True,
                "ai_official_save_lane": body.lane,
                "ai_duplicate_key": duplicate_key,
                "source_draft_job_id": job_id,
                "source_id": job.get("source_id"),
                "source_type": job.get("source_type"),
                "source_hash": source_hash,
                "reviewer_user_id": user.get("id"),
                "reviewer_role": user.get("role"),
                **_private_text_metadata("reviewer_note", body.reviewer_note),
                "created_at": now,
                "updated_at": now,
                "deleted_at": None,
            }
            if body.lane == "inventory_supply":
                record = {
                    **base,
                    "name": item.get("name"),
                    "category": item.get("category") or "uncategorized",
                    "quantity": item.get("quantity"),
                    "unit": item.get("unit"),
                    "location": item.get("storage_location"),
                    "storage_location": item.get("storage_location"),
                    "horse_or_barn_assignment": item.get("horse_or_barn_assignment"),
                    "notes": item.get("notes") or [],
                    "review_status": "official_saved",
                }
            else:
                record = {
                    **base,
                    "title": item.get("title") or item.get("name"),
                    "name": item.get("name"),
                    "type": item.get("category") or "repair",
                    "details": item.get("details") or item.get("name"),
                    "priority": item.get("priority") or "standard",
                    "due_date": item.get("due_date"),
                    "assigned_user_id": item.get("assigned_user_id"),
                    "assigned_role": item.get("assigned_role"),
                    "status": "open",
                    "notes": item.get("notes") or [],
                    "review_status": "official_saved",
                }
            if isinstance(record.get("notes"), str):
                record["notes"] = [record["notes"]]
            await db[target_collection].insert_one(record)
            saved_records.append({
                "id": record["id"],
                "collection": target_collection,
                "name": record.get("name") or record.get("title"),
            })

        if not saved_records:
            raise HTTPException(409, "No new official records were saved")

        review = {
            "id": f"ai_review_{uuid.uuid4()}",
            "job_id": job_id,
            "barn_id": barn_id,
            "user_id": user.get("id"),
            "action": "official_save",
            "lane": body.lane,
            "official_records_written": True,
            "saved_record_count": len(saved_records),
            "duplicate_record_count": len(duplicate_records),
            "created_at": now,
        }
        await db[AI_REVIEW_COLLECTION].insert_one(review)
        review.pop("_id", None)
        await db[AI_JOB_COLLECTION].update_one(
            {"id": job_id},
            {"$set": {
                "review_status": "official_saved",
                "official_save_status": body.lane,
                "official_records_written": True,
                "updated_at": now,
            }},
        )
        await audit_record(
            action=f"ai.official_save.{body.lane}",
            user=user,
            request=request,
            resource_type="ai_draft_job",
            resource_id=job_id,
            status_code=200,
            metadata={
                "lane": body.lane,
                "target_collection": target_collection,
                "saved_record_count": len(saved_records),
                "duplicate_record_count": len(duplicate_records),
                "official_records_written": True,
                "autonomous_mutation_enabled": False,
                "human_review_required": True,
            },
        )
        job["review_status"] = "official_saved"
        job["official_save_status"] = body.lane
        job["official_records_written"] = True
        job["updated_at"] = now
        return {
            "job": _job_projection(job),
            "review": review,
            "saved_records": saved_records,
            "duplicates_detected": duplicate_records,
            "official_records_written": True,
            "autonomous_mutation_enabled": False,
        }

    return router
