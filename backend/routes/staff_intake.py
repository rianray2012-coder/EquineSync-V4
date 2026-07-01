"""Build-Next-13I staff first-login intake shell.

Current-user only, groom/working_student-role only. This intentionally does
not create tasks, task completions, HorseOps records, staff permissions,
schedules, facility memberships, payroll records, billing changes, DocuSign
envelopes, or Admin Portal data.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


STAFF_INTAKE_COLLECTION = "staff_intake_profiles"
STAFF_ROLES = {"groom", "working_student"}
CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
EXPERIENCE_LEVELS = {
    "new",
    "beginner",
    "intermediate",
    "experienced",
    "professional",
    "prefer_not_to_say",
}
CARE_AREAS = {
    "feeding",
    "water",
    "hay",
    "hay_nets",
    "stall_bedding",
    "turnout",
    "grooming",
    "blanketing",
    "medication_support",
    "facility_checks",
    "other",
}

STAFF_INTAKE_FIELDS = {
    "preferred_name",
    "preferred_contact",
    "availability_notes",
    "experience_level",
    "care_area_comfort",
    "training_support_needs",
    "emergency_contact_preference",
    "notes",
}
STAFF_RESPONSE_FIELDS = {
    "id",
    "user_id",
    "email",
    "full_name",
    "preferred_name",
    "preferred_contact",
    "availability_notes",
    "experience_level",
    "care_area_comfort",
    "training_support_needs",
    "emergency_contact_preference",
    "notes",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_staff(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() not in STAFF_ROLES:
        raise HTTPException(status_code=403, detail="Staff intake is for staff accounts")


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Input should be a valid string")
    cleaned = value.strip()
    return cleaned or None


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


def _completion(profile: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "preferred_name",
        "preferred_contact",
        "availability_notes",
        "experience_level",
        "care_area_comfort",
        "training_support_needs",
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
        "id": f"staff_intake_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "preferred_contact": None,
        "availability_notes": None,
        "experience_level": None,
        "care_area_comfort": [],
        "training_support_needs": None,
        "emergency_contact_preference": None,
        "notes": None,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in STAFF_RESPONSE_FIELDS if k in profile}
    for field in STAFF_INTAKE_FIELDS:
        out.setdefault(field, [] if field == "care_area_comfort" else None)
    out["care_area_comfort"] = out.get("care_area_comfort") or []
    out["completion"] = _completion(out)
    return out


class StaffIntakePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    preferred_contact: Optional[str] = None
    availability_notes: Optional[str] = Field(default=None, max_length=1000)
    experience_level: Optional[str] = None
    care_area_comfort: Optional[List[str]] = None
    training_support_needs: Optional[str] = Field(default=None, max_length=1000)
    emergency_contact_preference: Optional[str] = Field(default=None, max_length=1000)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "preferred_name",
        "preferred_contact",
        "availability_notes",
        "experience_level",
        "training_support_needs",
        "emergency_contact_preference",
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

    @field_validator("experience_level")
    @classmethod
    def valid_experience_level(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in EXPERIENCE_LEVELS:
            raise ValueError("Invalid experience level")
        return normalized

    @field_validator("care_area_comfort")
    @classmethod
    def valid_care_area_comfort(cls, value):  # noqa: N805
        cleaned = _clean_string_list(value, max_items=12, max_len=80, label="Care area")
        if cleaned is None:
            return cleaned
        normalized = []
        for item in cleaned:
            text = item.strip().lower()
            if text not in CARE_AREAS:
                raise ValueError("Invalid care area")
            if text not in normalized:
                normalized.append(text)
        return normalized


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/staff-intake", tags=["staff-intake"])

    @router.get("/profile")
    async def get_staff_intake_profile(user=Depends(get_current_user)):
        _require_staff(user)
        existing = await db[STAFF_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_staff_intake_profile(body: StaffIntakePatch, user=Depends(get_current_user)):
        _require_staff(user)
        existing = await db[STAFF_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in STAFF_INTAKE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[STAFF_INTAKE_COLLECTION].update_one(
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
        saved = await db[STAFF_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(saved or {**base, **safe_patch})

    return router
