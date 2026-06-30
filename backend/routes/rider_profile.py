"""Build-Next-13C rider self-profile intake shell.

Current-user only, rider-role only. This is deliberately separate from the
lesson engine and guardian/minor workflows so rider first-login setup can land
without expanding scheduling, billing, DocuSign, or facility permissions.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


RIDER_PROFILE_COLLECTION = "rider_profiles"
RIDER_EXPERIENCE_LEVELS = {
    "new",
    "beginner",
    "intermediate",
    "advanced",
    "professional",
    "prefer_not_to_say",
}
RIDER_PROFILE_FIELDS = {
    "preferred_name",
    "disciplines",
    "experience_level",
    "goals",
    "availability_notes",
    "emergency_contact_name",
    "emergency_contact_phone",
    "consent_acknowledged",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_rider(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "rider":
        raise HTTPException(status_code=403, detail="Rider profile is for rider accounts")


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _completion(profile: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "preferred_name",
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
        "id": f"rider_profile_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "disciplines": [],
        "experience_level": None,
        "goals": None,
        "availability_notes": None,
        "emergency_contact_name": None,
        "emergency_contact_phone": None,
        "consent_acknowledged": False,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: v for k, v in profile.items() if k != "_id"}
    for field in RIDER_PROFILE_FIELDS:
        out.setdefault(field, [] if field == "disciplines" else None)
    out["disciplines"] = out.get("disciplines") or []
    out["consent_acknowledged"] = bool(out.get("consent_acknowledged"))
    out["completion"] = _completion(out)
    return out


class RiderProfilePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=80)
    disciplines: Optional[List[str]] = None
    experience_level: Optional[str] = None
    goals: Optional[str] = Field(default=None, max_length=1000)
    availability_notes: Optional[str] = Field(default=None, max_length=1000)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=120)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=60)
    consent_acknowledged: Optional[bool] = None

    @field_validator(
        "preferred_name",
        "experience_level",
        "goals",
        "availability_notes",
        "emergency_contact_name",
        "emergency_contact_phone",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805 - pydantic validator signature
        return _clean_text(value)

    @field_validator("experience_level")
    @classmethod
    def valid_experience(cls, value):  # noqa: N805 - pydantic validator signature
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in RIDER_EXPERIENCE_LEVELS:
            raise ValueError("Invalid experience level")
        return normalized

    @field_validator("disciplines")
    @classmethod
    def valid_disciplines(cls, value):  # noqa: N805 - pydantic validator signature
        if value is None:
            return value
        cleaned = []
        for raw in value:
            text = str(raw or "").strip()
            if not text:
                continue
            if len(text) > 60:
                raise ValueError("Discipline is too long")
            if text not in cleaned:
                cleaned.append(text)
        if len(cleaned) > 12:
            raise ValueError("Too many disciplines")
        return cleaned


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/rider", tags=["rider-profile"])

    @router.get("/profile")
    async def get_rider_profile(user=Depends(get_current_user)):
        _require_rider(user)
        existing = await db[RIDER_PROFILE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_rider_profile(body: RiderProfilePatch, user=Depends(get_current_user)):
        _require_rider(user)
        existing = await db[RIDER_PROFILE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in RIDER_PROFILE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[RIDER_PROFILE_COLLECTION].update_one(
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
