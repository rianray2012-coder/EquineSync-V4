"""Build-Next-13E owner first-login intake shell.

Current-owner only, horse_owner-role only. This intentionally does not create
facility memberships, horse records, billing changes, Stripe/Apple activity, or
HorseOps owner projections.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


OWNER_INTAKE_COLLECTION = "owner_intake_profiles"
OWNER_CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
OWNER_TYPES = {
    "facility_linked",
    "individual_owner",
    "exploring_facility",
    "prefer_not_to_say",
}
HORSE_COUNT_INTENTS = {"one", "two_to_five", "six_plus", "unknown"}

OWNER_INTAKE_FIELDS = {
    "preferred_name",
    "preferred_contact",
    "owner_type",
    "primary_horse_name",
    "horse_count_intent",
    "riding_or_care_goals",
    "facility_search_name",
    "facility_city_state",
    "notes",
}
OWNER_INTAKE_RESPONSE_FIELDS = {
    "id",
    "user_id",
    "email",
    "full_name",
    "preferred_name",
    "preferred_contact",
    "owner_type",
    "primary_horse_name",
    "horse_count_intent",
    "riding_or_care_goals",
    "facility_search_name",
    "facility_city_state",
    "notes",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_horse_owner(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "horse_owner":
        raise HTTPException(status_code=403, detail="Owner intake is for horse owner accounts")


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
        "owner_type",
        "primary_horse_name",
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
        "id": f"owner_intake_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "preferred_contact": None,
        "owner_type": None,
        "primary_horse_name": None,
        "horse_count_intent": None,
        "riding_or_care_goals": None,
        "facility_search_name": None,
        "facility_city_state": None,
        "notes": None,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in OWNER_INTAKE_RESPONSE_FIELDS if k in profile}
    for field in OWNER_INTAKE_FIELDS:
        out.setdefault(field, None)
    out["completion"] = _completion(out)
    return out


class OwnerIntakePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    preferred_contact: Optional[str] = None
    owner_type: Optional[str] = None
    primary_horse_name: Optional[str] = Field(default=None, max_length=120)
    horse_count_intent: Optional[str] = None
    riding_or_care_goals: Optional[str] = Field(default=None, max_length=1000)
    facility_search_name: Optional[str] = Field(default=None, max_length=160)
    facility_city_state: Optional[str] = Field(default=None, max_length=160)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "preferred_name",
        "preferred_contact",
        "owner_type",
        "primary_horse_name",
        "horse_count_intent",
        "riding_or_care_goals",
        "facility_search_name",
        "facility_city_state",
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
        if normalized not in OWNER_CONTACT_PREFERENCES:
            raise ValueError("Invalid contact preference")
        return normalized

    @field_validator("owner_type")
    @classmethod
    def valid_owner_type(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in OWNER_TYPES:
            raise ValueError("Invalid owner type")
        return normalized

    @field_validator("horse_count_intent")
    @classmethod
    def valid_horse_count_intent(cls, value):  # noqa: N805
        if value is None:
            return value
        normalized = value.strip().lower()
        if normalized not in HORSE_COUNT_INTENTS:
            raise ValueError("Invalid horse count intent")
        return normalized


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/owner-intake", tags=["owner-intake"])

    @router.get("/profile")
    async def get_owner_intake_profile(user=Depends(get_current_user)):
        _require_horse_owner(user)
        existing = await db[OWNER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_owner_intake_profile(body: OwnerIntakePatch, user=Depends(get_current_user)):
        _require_horse_owner(user)
        existing = await db[OWNER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in OWNER_INTAKE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[OWNER_INTAKE_COLLECTION].update_one(
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
