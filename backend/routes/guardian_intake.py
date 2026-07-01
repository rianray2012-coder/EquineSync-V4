"""Build-Next-13D guardian + minor rider intake shell.

Current-guardian only, parent-role only. This intentionally does not create
lesson enrollment, DocuSign envelopes, billing records, staff visibility, or
formal consent gates.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


GUARDIAN_MINOR_PROFILE_COLLECTION = "guardian_minor_rider_profiles"
GUARDIAN_CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
MINOR_AGE_RANGES = {"under_8", "8_12", "13_15", "16_17", "prefer_not_to_say"}
MINOR_EXPERIENCE_LEVELS = {
    "new",
    "beginner",
    "intermediate",
    "advanced",
    "prefer_not_to_say",
}
FORMAL_CONSENT_STATUS = "pending_formal_consent"

GUARDIAN_MINOR_PROFILE_FIELDS = {
    "guardian_preferred_contact",
    "minor_display_name",
    "minor_age_range",
    "minor_birthdate",
    "riding_interests",
    "experience_level",
    "goals",
    "availability_notes",
    "emergency_contact_name",
    "emergency_contact_phone",
    "medical_allergy_notes",
}
GUARDIAN_MINOR_RESPONSE_FIELDS = {
    "id",
    "guardian_user_id",
    "guardian_email",
    "guardian_full_name",
    "guardian_preferred_contact",
    "minor_display_name",
    "minor_age_range",
    "minor_birthdate",
    "riding_interests",
    "experience_level",
    "goals",
    "availability_notes",
    "emergency_contact_name",
    "emergency_contact_phone",
    "medical_allergy_notes",
    "consent_status",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_parent(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "parent":
        raise HTTPException(status_code=403, detail="Guardian intake is for parent accounts")


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Input should be a valid string")
    cleaned = value.strip()
    return cleaned or None


def _completion(profile: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "guardian_preferred_contact",
        "minor_display_name",
        "minor_age_range",
        "experience_level",
        "goals",
        "emergency_contact_name",
        "emergency_contact_phone",
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
        "id": f"guardian_minor_profile_{uuid.uuid4().hex[:12]}",
        "guardian_user_id": user["id"],
        "guardian_email": user.get("email"),
        "guardian_full_name": user.get("full_name"),
        "guardian_preferred_contact": None,
        "minor_display_name": None,
        "minor_age_range": None,
        "minor_birthdate": None,
        "riding_interests": [],
        "experience_level": None,
        "goals": None,
        "availability_notes": None,
        "emergency_contact_name": None,
        "emergency_contact_phone": None,
        "medical_allergy_notes": None,
        "consent_status": FORMAL_CONSENT_STATUS,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in GUARDIAN_MINOR_RESPONSE_FIELDS if k in profile}
    for field in GUARDIAN_MINOR_PROFILE_FIELDS:
        out.setdefault(field, [] if field == "riding_interests" else None)
    out["riding_interests"] = out.get("riding_interests") or []
    out["consent_status"] = FORMAL_CONSENT_STATUS
    out["completion"] = _completion(out)
    return out


class GuardianMinorProfilePatch(BaseModel):
    guardian_preferred_contact: Optional[str] = None
    minor_display_name: Optional[str] = Field(default=None, max_length=120)
    minor_age_range: Optional[str] = None
    minor_birthdate: Optional[str] = Field(default=None, max_length=20)
    riding_interests: Optional[List[str]] = None
    experience_level: Optional[str] = None
    goals: Optional[str] = Field(default=None, max_length=1000)
    availability_notes: Optional[str] = Field(default=None, max_length=1000)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=120)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=60)
    medical_allergy_notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "guardian_preferred_contact",
        "minor_display_name",
        "minor_age_range",
        "minor_birthdate",
        "experience_level",
        "goals",
        "availability_notes",
        "emergency_contact_name",
        "emergency_contact_phone",
        "medical_allergy_notes",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805 - pydantic validator signature
        return _clean_text(value)

    @field_validator("guardian_preferred_contact")
    @classmethod
    def valid_contact_preference(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in GUARDIAN_CONTACT_PREFERENCES:
            raise ValueError("Invalid contact preference")
        return normalized

    @field_validator("minor_age_range")
    @classmethod
    def valid_age_range(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in MINOR_AGE_RANGES:
            raise ValueError("Invalid minor age range")
        return normalized

    @field_validator("experience_level")
    @classmethod
    def valid_experience(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in MINOR_EXPERIENCE_LEVELS:
            raise ValueError("Invalid experience level")
        return normalized

    @field_validator("riding_interests")
    @classmethod
    def valid_interests(cls, value):  # noqa: N805
        if value is None:
            return value
        cleaned = []
        for raw in value:
            text = str(raw or "").strip()
            if not text:
                continue
            if len(text) > 60:
                raise ValueError("Riding interest is too long")
            if text not in cleaned:
                cleaned.append(text)
        if len(cleaned) > 12:
            raise ValueError("Too many riding interests")
        return cleaned


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/guardian", tags=["guardian-intake"])

    @router.get("/minor-rider-profile")
    async def get_minor_rider_profile(user=Depends(get_current_user)):
        _require_parent(user)
        existing = await db[GUARDIAN_MINOR_PROFILE_COLLECTION].find_one(
            {"guardian_user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/minor-rider-profile")
    async def patch_minor_rider_profile(body: GuardianMinorProfilePatch, user=Depends(get_current_user)):
        _require_parent(user)
        existing = await db[GUARDIAN_MINOR_PROFILE_COLLECTION].find_one(
            {"guardian_user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in GUARDIAN_MINOR_PROFILE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        safe_patch["consent_status"] = FORMAL_CONSENT_STATUS
        await db[GUARDIAN_MINOR_PROFILE_COLLECTION].update_one(
            {"guardian_user_id": user["id"]},
            {
                "$set": safe_patch,
                "$setOnInsert": {
                    "id": base["id"],
                    "guardian_user_id": user["id"],
                    "guardian_email": user.get("email"),
                    "guardian_full_name": user.get("full_name"),
                    "created_at": base["created_at"],
                },
            },
            upsert=True,
        )
        updated = {**base, **safe_patch}
        return _project(updated)

    return router
