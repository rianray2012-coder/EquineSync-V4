"""routes/horses.py — core horse-profile CRUD.

Extracted from routes/care.py (Phase 3C). Horse-profile create/read/update/list
only. Behavior is identical to the previous care.py handlers (pure lift-and-shift;
no new validation or permission logic).

Intentional exception: ``GET /api/horses/{horse_id}/timeline`` remains in
``task_engine.py`` because it is a task-event projection/aggregation, not
horse-profile CRUD.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.account_route_context import account_barn_filter
from core.permissions import require
from core.provider_access import grant_horse_filter, is_provider_user, provider_grants
from core.tenancy import barn_filter, stamp_barn


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


class HorseIn(BaseModel):
    name: str
    barn_name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    color: Optional[str] = None
    height_hands: Optional[float] = None
    discipline: Optional[str] = None
    owner_id: Optional[str] = None
    rider_id: Optional[str] = None
    trainer_id: Optional[str] = None
    stall: Optional[str] = None
    photo_url: Optional[str] = None
    allergies: Optional[List[str]] = []
    emergency_notes: Optional[str] = None
    insurance: Optional[str] = None
    wellness_score: Optional[int] = 85
    status: Optional[str] = "active"
    training_goals: Optional[str] = None
    feed_plan: Optional[str] = None
    turnout_group: Optional[str] = None
    behavior_flags: Optional[List[str]] = []


class HorsePassportIn(BaseModel):
    passport_number: Optional[str] = None
    registry_name: Optional[str] = None
    microchip_number: Optional[str] = None
    issued_by: Optional[str] = None
    document_url: Optional[str] = None
    notes: Optional[str] = None


class HorseCorrectionIn(BaseModel):
    reason: str
    updates: Dict[str, Any] = Field(default_factory=dict)
    evidence_url: Optional[str] = None


class HorseMergeIn(BaseModel):
    source_horse_id: str
    reason: str


class HorseTransferIn(BaseModel):
    to_owner_id: str
    reason: str
    effective_date: Optional[str] = None
    transfer_status: Optional[str] = "pending"


def build_router(*, db, get_current_user, list_collection, clean, new_id, require_active_facility=None) -> APIRouter:
    router = APIRouter(tags=["horses"])
    enforce_active_facility = require_active_facility or get_current_user

    async def _managed_horse(horse_id: str, user: Dict[str, Any]) -> Dict[str, Any]:
        require(user, "barn:manage")
        horse = await db.horses.find_one(barn_filter(user, {"id": horse_id}), {"_id": 0})
        if not horse:
            raise HTTPException(404, "Horse not found")
        return horse

    async def _record_lifecycle_event(user: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        event.update({
            "id": new_id(),
            "barn_id": user.get("barn_id") or "primary",
            "actor_user_id": user.get("id"),
            "created_at": _iso(_now_utc()),
        })
        await db.horse_lifecycle_events.insert_one(event)
        return event

    @router.get("/horses")
    async def list_horses(account_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            grants = await provider_grants(db, user)
            return await list_collection("horses", grant_horse_filter(grants))
        # BN3C pilot: read scope can use selected account context; writes remain legacy-scoped.
        return await list_collection("horses", await account_barn_filter(db, user, account_id=account_id))

    @router.post("/horses")
    async def create_horse(body: HorseIn, user=Depends(get_current_user), _active=Depends(enforce_active_facility)):
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        # Phase 4B-1: stamp the caller's barn at write time.
        stamp_barn(user, doc)
        await db.horses.insert_one(doc)
        return clean(doc)

    @router.get("/horses/{horse_id}")
    async def get_horse(horse_id: str, account_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            grants = await provider_grants(db, user)
            h = await db.horses.find_one(grant_horse_filter(grants, horse_id), {"_id": 0})
            if not h:
                raise HTTPException(404, "Horse not found")
            return h
        # BN3C pilot: scope read by id + selected facility account; cross-account ids 404.
        h = await db.horses.find_one(await account_barn_filter(db, user, account_id=account_id, extra={"id": horse_id}), {"_id": 0})
        if not h:
            raise HTTPException(404, "Horse not found")
        return h

    @router.patch("/horses/{horse_id}")
    async def update_horse(horse_id: str, body: Dict[str, Any], user=Depends(get_current_user), _active=Depends(enforce_active_facility)):
        scope = barn_filter(user, {"id": horse_id})
        existing = await db.horses.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Horse not found")
        # Phase 4B-1: never allow a client to move a horse between barns
        # (or rewrite its id) via the free-form PATCH body.
        updates = {k: v for k, v in body.items() if k not in ("barn_id", "id")}
        if updates:
            await db.horses.update_one(scope, {"$set": updates})
        return await db.horses.find_one(scope, {"_id": 0})

    @router.post("/horses/{horse_id}/passport")
    async def upsert_horse_passport(
        horse_id: str,
        body: HorsePassportIn,
        user=Depends(get_current_user),
        _active=Depends(enforce_active_facility),
    ):
        await _managed_horse(horse_id, user)
        now = _iso(_now_utc())
        passport = {
            **body.model_dump(),
            "horse_id": horse_id,
            "barn_id": user.get("barn_id") or "primary",
            "updated_at": now,
            "updated_by_user_id": user.get("id"),
            "lifecycle_state": "passport_recorded",
        }
        await db.horse_passports.update_one(
            barn_filter(user, {"horse_id": horse_id}),
            {"$set": passport, "$setOnInsert": {"id": new_id(), "created_at": now}},
            upsert=True,
        )
        await _record_lifecycle_event(user, {
            "horse_id": horse_id,
            "event_type": "horse.passport_recorded",
            "payload": passport,
        })
        return await db.horse_passports.find_one(barn_filter(user, {"horse_id": horse_id}), {"_id": 0})

    @router.post("/horses/{horse_id}/corrections")
    async def create_horse_correction(
        horse_id: str,
        body: HorseCorrectionIn,
        user=Depends(get_current_user),
        _active=Depends(enforce_active_facility),
    ):
        await _managed_horse(horse_id, user)
        blocked = {"id", "barn_id", "_id"}
        updates = {key: value for key, value in (body.updates or {}).items() if key not in blocked}
        correction = {
            "id": new_id(),
            "horse_id": horse_id,
            "barn_id": user.get("barn_id") or "primary",
            "reason": body.reason,
            "updates": updates,
            "evidence_url": body.evidence_url,
            "status": "applied" if updates else "recorded",
            "created_at": _iso(_now_utc()),
            "created_by_user_id": user.get("id"),
        }
        await db.horse_corrections.insert_one(correction)
        if updates:
            await db.horses.update_one(barn_filter(user, {"id": horse_id}), {"$set": {**updates, "updated_at": correction["created_at"]}})
        await _record_lifecycle_event(user, {
            "horse_id": horse_id,
            "event_type": "horse.correction_applied" if updates else "horse.correction_recorded",
            "payload": correction,
        })
        return clean(correction)

    @router.post("/horses/{horse_id}/merge")
    async def merge_horse(
        horse_id: str,
        body: HorseMergeIn,
        user=Depends(get_current_user),
        _active=Depends(enforce_active_facility),
    ):
        target = await _managed_horse(horse_id, user)
        if body.source_horse_id == horse_id:
            raise HTTPException(422, "Source and target horses must be different")
        source = await db.horses.find_one(barn_filter(user, {"id": body.source_horse_id}), {"_id": 0})
        if not source:
            raise HTTPException(404, "Source horse not found")
        now = _iso(_now_utc())
        merge = {
            "id": new_id(),
            "barn_id": user.get("barn_id") or "primary",
            "target_horse_id": target["id"],
            "source_horse_id": source["id"],
            "reason": body.reason,
            "status": "applied",
            "created_at": now,
            "created_by_user_id": user.get("id"),
        }
        await db.horse_merges.insert_one(merge)
        await db.horses.update_one(
            barn_filter(user, {"id": source["id"]}),
            {"$set": {"lifecycle_state": "merged", "merged_into_horse_id": target["id"], "updated_at": now}},
        )
        await _record_lifecycle_event(user, {
            "horse_id": target["id"],
            "event_type": "horse.merge_applied",
            "payload": merge,
        })
        return clean(merge)

    @router.post("/horses/{horse_id}/transfer")
    async def create_horse_transfer(
        horse_id: str,
        body: HorseTransferIn,
        user=Depends(get_current_user),
        _active=Depends(enforce_active_facility),
    ):
        await _managed_horse(horse_id, user)
        status = (body.transfer_status or "pending").strip().lower()
        if status not in {"pending", "approved", "completed"}:
            raise HTTPException(422, "Unsupported transfer status")
        now = _iso(_now_utc())
        transfer = {
            "id": new_id(),
            "horse_id": horse_id,
            "barn_id": user.get("barn_id") or "primary",
            "from_owner_id": (await db.horses.find_one(barn_filter(user, {"id": horse_id}), {"_id": 0, "owner_id": 1}) or {}).get("owner_id"),
            "to_owner_id": body.to_owner_id,
            "reason": body.reason,
            "effective_date": body.effective_date,
            "status": status,
            "created_at": now,
            "created_by_user_id": user.get("id"),
        }
        await db.horse_transfers.insert_one(transfer)
        horse_updates = {"transfer_state": status, "pending_owner_id": body.to_owner_id, "updated_at": now}
        if status == "completed":
            horse_updates.update({"owner_id": body.to_owner_id, "pending_owner_id": None})
        await db.horses.update_one(barn_filter(user, {"id": horse_id}), {"$set": horse_updates})
        await _record_lifecycle_event(user, {
            "horse_id": horse_id,
            "event_type": f"horse.transfer_{status}",
            "payload": transfer,
        })
        return clean(transfer)

    return router
