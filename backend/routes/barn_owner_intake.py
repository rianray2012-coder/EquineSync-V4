"""Build-Next-13F barn owner first-login intake shell.

Current-user only, barn_owner-role only. This intentionally does not create
facility records, account memberships, onboarding progress, staff invites,
billing changes, Stripe/Apple activity, or Admin Portal data.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


BARN_OWNER_INTAKE_COLLECTION = "barn_owner_intake_profiles"
CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
FACILITY_TYPES = {
    "boarding",
    "training",
    "lesson_program",
    "private_barn",
    "rescue",
    "mixed",
    "other",
    "prefer_not_to_say",
}
HORSE_COUNT_RANGES = {"none_yet", "1_10", "11_30", "31_75", "76_plus", "unknown"}
STAFF_COUNT_RANGES = {"solo", "1_3", "4_10", "11_plus", "unknown"}
SETUP_TIMELINES = {"now", "30_days", "90_days", "later", "exploring"}

BARN_OWNER_INTAKE_FIELDS = {
    "preferred_name",
    "preferred_contact",
    "facility_name",
    "facility_city_state",
    "facility_type",
    "horse_count_range",
    "staff_count_range",
    "services_offered",
    "setup_goals",
    "timeline",
    "notes",
}
BARN_OWNER_RESPONSE_FIELDS = {
    "id",
    "user_id",
    "email",
    "full_name",
    "preferred_name",
    "preferred_contact",
    "facility_name",
    "facility_city_state",
    "facility_type",
    "horse_count_range",
    "staff_count_range",
    "services_offered",
    "setup_goals",
    "timeline",
    "notes",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_barn_owner(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "barn_owner":
        raise HTTPException(status_code=403, detail="Barn owner intake is for barn owner accounts")


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
        "facility_name",
        "facility_type",
        "horse_count_range",
        "timeline",
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
        "id": f"barn_owner_intake_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "preferred_contact": None,
        "facility_name": None,
        "facility_city_state": None,
        "facility_type": None,
        "horse_count_range": None,
        "staff_count_range": None,
        "services_offered": [],
        "setup_goals": None,
        "timeline": None,
        "notes": None,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in BARN_OWNER_RESPONSE_FIELDS if k in profile}
    for field in BARN_OWNER_INTAKE_FIELDS:
        out.setdefault(field, [] if field == "services_offered" else None)
    out["services_offered"] = out.get("services_offered") or []
    out["completion"] = _completion(out)
    return out


class BarnOwnerIntakePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    preferred_contact: Optional[str] = None
    facility_name: Optional[str] = Field(default=None, max_length=160)
    facility_city_state: Optional[str] = Field(default=None, max_length=160)
    facility_type: Optional[str] = None
    horse_count_range: Optional[str] = None
    staff_count_range: Optional[str] = None
    services_offered: Optional[List[str]] = None
    setup_goals: Optional[str] = Field(default=None, max_length=1000)
    timeline: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "preferred_name",
        "preferred_contact",
        "facility_name",
        "facility_city_state",
        "facility_type",
        "horse_count_range",
        "staff_count_range",
        "setup_goals",
        "timeline",
        "notes",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805 - pydantic validator signature
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

    @field_validator("facility_type")
    @classmethod
    def valid_facility_type(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in FACILITY_TYPES:
            raise ValueError("Invalid facility type")
        return normalized

    @field_validator("horse_count_range")
    @classmethod
    def valid_horse_count_range(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in HORSE_COUNT_RANGES:
            raise ValueError("Invalid horse count range")
        return normalized

    @field_validator("staff_count_range")
    @classmethod
    def valid_staff_count_range(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in STAFF_COUNT_RANGES:
            raise ValueError("Invalid staff count range")
        return normalized

    @field_validator("timeline")
    @classmethod
    def valid_timeline(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in SETUP_TIMELINES:
            raise ValueError("Invalid setup timeline")
        return normalized

    @field_validator("services_offered")
    @classmethod
    def valid_services_offered(cls, value):  # noqa: N805
        if value is None:
            return value
        cleaned = []
        for raw in value:
            text = str(raw or "").strip()
            if not text:
                continue
            if len(text) > 80:
                raise ValueError("Service label is too long")
            if text not in cleaned:
                cleaned.append(text)
        if len(cleaned) > 12:
            raise ValueError("Too many services")
        return cleaned


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/barn-owner-intake", tags=["barn-owner-intake"])

    @router.get("/profile")
    async def get_barn_owner_intake_profile(user=Depends(get_current_user)):
        _require_barn_owner(user)
        existing = await db[BARN_OWNER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_barn_owner_intake_profile(body: BarnOwnerIntakePatch, user=Depends(get_current_user)):
        _require_barn_owner(user)
        existing = await db[BARN_OWNER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in BARN_OWNER_INTAKE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[BARN_OWNER_INTAKE_COLLECTION].update_one(
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
