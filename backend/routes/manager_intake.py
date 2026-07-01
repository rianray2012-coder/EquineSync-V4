"""Build-Next-13H barn manager first-login intake shell.

Current-user only, barn_manager-role only. This intentionally does not create
tasks, staff invites, staff permissions, HorseOps records, facility setup
changes, billing changes, DocuSign envelopes, or Admin Portal data.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator


MANAGER_INTAKE_COLLECTION = "manager_intake_profiles"
CONTACT_PREFERENCES = {"email", "sms", "phone", "app", "no_preference"}
OPERATIONS_FOCUS_AREAS = {
    "daily_tasks",
    "horse_care",
    "staff_coordination",
    "facility_maintenance",
    "owner_communication",
    "inventory",
    "scheduling",
    "mixed",
    "other",
    "prefer_not_to_say",
}

MANAGER_INTAKE_FIELDS = {
    "preferred_name",
    "preferred_contact",
    "operations_focus",
    "shift_availability_notes",
    "team_coordination_notes",
    "horse_care_oversight_notes",
    "task_board_goals",
    "facility_connection_notes",
    "emergency_operations_notes",
    "notes",
}
MANAGER_RESPONSE_FIELDS = {
    "id",
    "user_id",
    "email",
    "full_name",
    "preferred_name",
    "preferred_contact",
    "operations_focus",
    "shift_availability_notes",
    "team_coordination_notes",
    "horse_care_oversight_notes",
    "task_board_goals",
    "facility_connection_notes",
    "emergency_operations_notes",
    "notes",
    "created_at",
    "updated_at",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_manager(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "barn_manager":
        raise HTTPException(status_code=403, detail="Manager intake is for barn manager accounts")


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
        "operations_focus",
        "task_board_goals",
        "team_coordination_notes",
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
        "id": f"manager_intake_{uuid.uuid4().hex[:12]}",
        "user_id": user["id"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "preferred_name": None,
        "preferred_contact": None,
        "operations_focus": [],
        "shift_availability_notes": None,
        "team_coordination_notes": None,
        "horse_care_oversight_notes": None,
        "task_board_goals": None,
        "facility_connection_notes": None,
        "emergency_operations_notes": None,
        "notes": None,
        "created_at": now,
        "updated_at": now,
    }


def _project(profile: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: profile.get(k) for k in MANAGER_RESPONSE_FIELDS if k in profile}
    for field in MANAGER_INTAKE_FIELDS:
        out.setdefault(field, [] if field == "operations_focus" else None)
    out["operations_focus"] = out.get("operations_focus") or []
    out["completion"] = _completion(out)
    return out


class ManagerIntakePatch(BaseModel):
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    preferred_contact: Optional[str] = None
    operations_focus: Optional[List[str]] = None
    shift_availability_notes: Optional[str] = Field(default=None, max_length=1000)
    team_coordination_notes: Optional[str] = Field(default=None, max_length=1000)
    horse_care_oversight_notes: Optional[str] = Field(default=None, max_length=1000)
    task_board_goals: Optional[str] = Field(default=None, max_length=1000)
    facility_connection_notes: Optional[str] = Field(default=None, max_length=1000)
    emergency_operations_notes: Optional[str] = Field(default=None, max_length=1000)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator(
        "preferred_name",
        "preferred_contact",
        "shift_availability_notes",
        "team_coordination_notes",
        "horse_care_oversight_notes",
        "task_board_goals",
        "facility_connection_notes",
        "emergency_operations_notes",
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

    @field_validator("operations_focus")
    @classmethod
    def valid_operations_focus(cls, value):  # noqa: N805
        cleaned = _clean_string_list(value, max_items=10, max_len=80, label="Operations focus")
        if cleaned is None:
            return cleaned
        normalized = []
        for item in cleaned:
            text = item.strip().lower()
            if text not in OPERATIONS_FOCUS_AREAS:
                raise ValueError("Invalid operations focus")
            if text not in normalized:
                normalized.append(text)
        return normalized


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/manager-intake", tags=["manager-intake"])

    @router.get("/profile")
    async def get_manager_intake_profile(user=Depends(get_current_user)):
        _require_manager(user)
        existing = await db[MANAGER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(existing or _default_profile(user))

    @router.patch("/profile")
    async def patch_manager_intake_profile(body: ManagerIntakePatch, user=Depends(get_current_user)):
        _require_manager(user)
        existing = await db[MANAGER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        base = existing or _default_profile(user)
        patch = body.model_dump(exclude_unset=True)
        safe_patch = {k: v for k, v in patch.items() if k in MANAGER_INTAKE_FIELDS}
        now = _now_iso()
        safe_patch["updated_at"] = now
        await db[MANAGER_INTAKE_COLLECTION].update_one(
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
        saved = await db[MANAGER_INTAKE_COLLECTION].find_one(
            {"user_id": user["id"]},
            {"_id": 0},
        )
        return _project(saved or {**base, **safe_patch})

    return router
