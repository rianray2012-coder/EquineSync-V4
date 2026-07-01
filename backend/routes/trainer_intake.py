"""Build-Next-13G trainer first-login intake shell.

Current-user only, trainer-role only. This intentionally does not create
lessons, rider enrollments, horse assignments, staff permissions, billing
changes, DocuSign envelopes, or HorseOps data.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


TRAINER_INTAKE_COLLECTION = "trainer_intake_profiles"
CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
RIDER_LEVELS = {
    "new",
    "beginner",
    "intermediate",
    "advanced",
    "professional",
    "mixed",
    "prefer_not_to_say",
}
PROGRAM_FOCUS_AREAS = {
    "lessons",
    "training",
    "show_program",
    "young_horses",
    "rehab",
    "sales",
    "mixed",
    "other",
    "prefer_not_to_say",
}

TRAINER_INTAKE_FIELDS = {
    "preferred_name",
    "preferred_contact",
    "disciplines",
    "program_focus",
    "rider_levels_supported",
    "availability_notes",
    "certification_insurance_notes",
    "facility_connection_notes",
    "goals",
    "notes",
}
TRAINER_RESPONSE_FIELDS = {
    "id",
    "user_id",
    "email",
    "full_name",
    "preferred_name",
    "preferred_contact",
    "disciplines",
    "program_focus",
    "rider_levels_supported",
    "availability_notes",
    "certification_insurance_notes",
    "facility_connection_notes",
    "goals",
    "notes",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_trainer(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "trainer":
        raise HTTPException(status_code=403, detail="Trainer intake is for trainer accounts")


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Input should be a valid string")
    cleaned = value.strip()
    return cleaned or None


def _completion(profile: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "preferred_name",
        "preferred_contact",
        "disciplines",
        "program_focus",
        "rider_levels_supported",
        "goals",
    ]
    completed = [field for field in required if profile.get(field)]
    return {
        "required_fields": required,
        "completed_fields": completed,
        "missing_fields": [field for field in required if field not in completed],
        "percent": int(round((len(completed) / len(required)) * 100)),
    }


def _default_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    now = _now_iso()
    return {
        "id": f"trainer_intake_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "preferred_contact": None,
        "disciplines": [],
        "program_focus": None,
        "rider_levels_supported": [],
        "availability_notes": None,
        "certification_insurance_notes": None,
        "facility_connection_notes": None,
        "goals": None,
        "notes": None,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in TRAINER_RESPONSE_FIELDS if k in profile}
    for field in TRAINER_INTAKE_FIELDS:
        out.setdefault(field, [] if field in {"disciplines", "rider_levels_supported"} else None)
    out["disciplines"] = out.get("disciplines") or []
    out["rider_levels_supported"] = out.get("rider_levels_supported") or []
    out["completion"] = _completion(out)
    return out


def _clean_string_list(value, *, max_items: int, max_len: int, label: str):
    if value is None:
        return value
    cleaned = []
    for raw in value:
        text = str(raw or "").strip()
        if not text:
            continue
        if len(text) > max_len:
            raise ValueError(f"{label} is too long")
        if text not in cleaned:
            cleaned.append(text)
    if len(cleaned) > max_items:
        raise ValueError(f"Too many {label.lower()} values")
    return cleaned


class TrainerIntakePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    preferred_contact: Optional[str] = None
    disciplines: Optional[List[str]] = None
    program_focus: Optional[str] = None
    rider_levels_supported: Optional[List[str]] = None
    availability_notes: Optional[str] = Field(default=None, max_length=1000)
    certification_insurance_notes: Optional[str] = Field(default=None, max_length=1000)
    facility_connection_notes: Optional[str] = Field(default=None, max_length=1000)
    goals: Optional[str] = Field(default=None, max_length=1000)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "preferred_name",
        "preferred_contact",
        "program_focus",
        "availability_notes",
        "certification_insurance_notes",
        "facility_connection_notes",
        "goals",
        "notes",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805
        return _clean_text(value)

    @field_validator("preferred_contact")
    @classmethod
    def valid_contact_preference(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in CONTACT_PREFERENCES:
            raise ValueError("Invalid contact preference")
        return normalized

    @field_validator("program_focus")
    @classmethod
    def valid_program_focus(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in PROGRAM_FOCUS_AREAS:
            raise ValueError("Invalid program focus")
        return normalized

    @field_validator("disciplines")
    @classmethod
    def valid_disciplines(cls, value):  # noqa: N805
        return _clean_string_list(value, max_items=12, max_len=80, label="Discipline")

    @field_validator("rider_levels_supported")
    @classmethod
    def valid_rider_levels_supported(cls, value):  # noqa: N805
        cleaned = _clean_string_list(value, max_items=8, max_len=40, label="Rider level")
        if cleaned is None:
            return cleaned
        normalized = []
        for level in cleaned:
            text = level.strip().lower()
            if text not in RIDER_LEVELS:
                raise ValueError("Invalid rider level")
            if text not in normalized:
                normalized.append(text)
        return normalized


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/trainer-intake", tags=["trainer-intake"])

    @router.get("/profile")
    async def get_trainer_intake_profile(user=Depends(get_current_user)):
        _require_trainer(user)
        existing = await db[TRAINER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_trainer_intake_profile(body: TrainerIntakePatch, user=Depends(get_current_user)):
        _require_trainer(user)
        existing = await db[TRAINER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in TRAINER_INTAKE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[TRAINER_INTAKE_COLLECTION].update_one(
            {"user_id": user["id"]},
            {
                "$set": safe_patch,
                "$setOnInsert": {
                    "id": base["id"],
                    "user_id": user["id"],
                    "email": user.get("email"),
                    "full_name": user.get("full_name"),
                    "created_at": base["created_at"],
                },
            },
            upsert=True,
        )
        updated = {**base, **safe_patch}
        return _project(updated)

    return router
