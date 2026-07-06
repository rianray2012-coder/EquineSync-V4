"""routes/care.py — care records: owners, riders, medications,
vet, farrier, injuries, wellness, feed-tasks.

Phase-F final sweep extraction (Feb 20 2026). All handlers are trivial
CRUD over MongoDB collections; they share the `list_collection`, `clean`
and `new_id` helpers from server.py. Models live here too because they
are not shared with any other route module.

Note: horse-profile CRUD was extracted to `routes/horses.py` in Phase 3C.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from core.provider_access import (
    grant_care_filter,
    is_provider_user,
    provider_grants,
    require_provider_horse_access,
)
from core.tenancy import barn_filter, stamp_barn


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


# ---------------- Models ----------------

class OwnerIn(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    horses: Optional[List[str]] = []
    photo_url: Optional[str] = None


class RiderIn(BaseModel):
    full_name: str
    age: Optional[int] = None
    skill_level: str = "beginner"
    goals: Optional[str] = None
    trainer_id: Optional[str] = None
    emergency_contact: Optional[str] = None
    photo_url: Optional[str] = None


class MedicationIn(BaseModel):
    horse_id: str
    name: str
    dosage: str
    route: Optional[str] = "oral"
    frequency: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    prescribing_vet: Optional[str] = None
    notes: Optional[str] = None
    times: Optional[List[str]] = []


class MedLogIn(BaseModel):
    medication_id: str
    scheduled_time: str
    status: str
    notes: Optional[str] = None
    # Phase 6B: optional client-supplied idempotency key. When provided, repeat
    # posts with the same (barn, client_log_id) return the same log instead of
    # inserting a duplicate. Omitting it preserves the original insert behavior.
    client_log_id: Optional[str] = None


class VetRecordIn(BaseModel):
    horse_id: str
    type: str
    title: str
    date: str
    vet_name: Optional[str] = None
    notes: Optional[str] = None
    document_url: Optional[str] = None
    cost: Optional[float] = 0


class InjuryIn(BaseModel):
    horse_id: str
    title: str
    description: Optional[str] = None
    status: str = "active"
    severity: str = "mild"
    start_date: Optional[str] = None
    rehab_plan: Optional[str] = None


class WellnessIn(BaseModel):
    horse_id: str
    appetite: int = 5
    water_intake: int = 5
    energy: int = 5
    body_condition: float = 5.0
    coat_quality: int = 5
    notes: Optional[str] = None
    status: str = "normal"


class FeedTaskIn(BaseModel):
    horse_id: str
    meal: str
    ration: str
    instructions: Optional[str] = None
    completed: bool = False
    completed_by: Optional[str] = None


def build_router(*, db, get_current_user, list_collection, clean, new_id) -> APIRouter:
    router = APIRouter(tags=["care"])

    # ---------------- Phase 6A: care input integrity helpers ----------------
    # Validate that a referenced id belongs to the caller's barn BEFORE writing
    # a care record. Cross-barn and absent ids return the same generic 404 so
    # there is no existence leak (consistent with the 4E isolation contract).

    async def _provider_care_scope(user, horse_id: Optional[str] = None) -> Dict:
        grants = await provider_grants(db, user)
        if horse_id and not any(row.get("horse_id") == horse_id for row in grants):
            raise HTTPException(404, "Horse not found")
        return grant_care_filter(grants, horse_id)

    async def _care_scope(user, horse_id: Optional[str] = None) -> Dict:
        if is_provider_user(user):
            return await _provider_care_scope(user, horse_id)
        return barn_filter(user, {"horse_id": horse_id} if horse_id else None)

    async def _require_horse(user, horse_id: str) -> Dict:
        if is_provider_user(user):
            return await require_provider_horse_access(db, user, horse_id)
        horse = await db.horses.find_one(barn_filter(user, {"id": horse_id}), {"_id": 0, "id": 1, "barn_id": 1, "name": 1})
        if not horse:
            raise HTTPException(404, "Horse not found")
        return horse

    def _reject_provider_care_write(user) -> None:
        if is_provider_user(user):
            raise HTTPException(403, "Service providers must use provider visit notes for RF10 care entries")

    async def _require_medication(user, medication_id: str) -> Dict:
        if is_provider_user(user):
            grants = await provider_grants(db, user)
            med = await db.medications.find_one(
                {"id": medication_id, **grant_care_filter(grants)},
                {"_id": 0, "id": 1, "horse_id": 1, "barn_id": 1},
            )
            if not med:
                raise HTTPException(404, "Medication not found")
            return med
        med = await db.medications.find_one(barn_filter(user, {"id": medication_id}), {"_id": 0, "id": 1, "barn_id": 1})
        if not med:
            raise HTTPException(404, "Medication not found")
        return med

    def _provider_medication_log_filter(meds: List[Dict]) -> Dict:
        clauses = [
            {"medication_id": row["id"], "barn_id": row["barn_id"]}
            for row in meds
            if row.get("id") and row.get("barn_id")
        ]
        if not clauses:
            return {"medication_id": "__no_provider_medications__"}
        return clauses[0] if len(clauses) == 1 else {"$or": clauses}

    # ---------------- Owners ----------------

    @router.get("/owners")
    async def list_owners(user=Depends(get_current_user)):
        if is_provider_user(user):
            return []
        # Phase 6C: deterministic newest-first ordering (created_at desc).
        return await list_collection("owners", barn_filter(user), sort_field="created_at")

    @router.post("/owners")
    async def create_owner(body: OwnerIn, user=Depends(get_current_user)):
        if is_provider_user(user):
            raise HTTPException(403, "Service providers cannot manage owner records")
        # Phase 6A: every referenced horse must belong to the caller's barn.
        for horse_id in (body.horses or []):
            await _require_horse(user, horse_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        await db.owners.insert_one(doc)
        return clean(doc)

    # ---------------- Riders ----------------

    @router.get("/riders")
    async def list_riders(user=Depends(get_current_user)):
        if is_provider_user(user):
            return []
        # Phase 6C: deterministic newest-first ordering (created_at desc).
        return await list_collection("riders", barn_filter(user), sort_field="created_at")

    @router.post("/riders")
    async def create_rider(body: RiderIn, user=Depends(get_current_user)):
        if is_provider_user(user):
            raise HTTPException(403, "Service providers cannot manage rider records")
        # Phase 6A backlog (deferred): rider.trainer_id references a user/staff
        # record (cross-domain into `users`), outside the care-records boundary.
        # Validating trainer barn membership is tracked for a later phase.
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        await db.riders.insert_one(doc)
        return clean(doc)

    # ---------------- Medications ----------------

    @router.get("/medications")
    async def list_meds(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return await list_collection("medications", await _care_scope(user, horse_id), sort_field="created_at")
        extra = {"horse_id": horse_id} if horse_id else {}
        # Phase 6C: deterministic newest-first ordering (created_at desc).
        return await list_collection("medications", barn_filter(user, extra), sort_field="created_at")

    @router.post("/medications")
    async def create_med(body: MedicationIn, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        horse = await _require_horse(user, body.horse_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        doc["barn_id"] = horse.get("barn_id") if is_provider_user(user) else stamp_barn(user, doc)["barn_id"]
        await db.medications.insert_one(doc)
        return clean(doc)

    @router.get("/medication-logs")
    async def list_med_logs(medication_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            if medication_id:
                med = await _require_medication(user, medication_id)
                return await list_collection("medication_logs", {"medication_id": medication_id, "barn_id": med.get("barn_id")}, sort_field="scheduled_time")
            meds = await db.medications.find(await _care_scope(user), {"_id": 0, "id": 1, "barn_id": 1}).to_list(1000)
            if not meds:
                return []
            return await list_collection("medication_logs", _provider_medication_log_filter(meds), sort_field="scheduled_time")
        # Phase 6C: optional barn-scoped medication_id filter (parity with the
        # horse_id filter on the other care lists). A foreign/unknown id simply
        # returns an empty array (barn_filter scopes it) — no 404, no leak.
        extra = {"medication_id": medication_id} if medication_id else {}
        return await list_collection(
            "medication_logs", barn_filter(user, extra), sort_field="scheduled_time"
        )

    @router.post("/medication-logs")
    async def create_med_log(body: MedLogIn, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        await _require_medication(user, body.medication_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "completed_by": user["id"], "completed_at": _iso(_now_utc())})
        if not is_provider_user(user):
            stamp_barn(user, doc)
        # Phase 6B: opt-in idempotency. With a client_log_id, atomically upsert
        # keyed by (barn_id, client_log_id) so repeat submits return the first
        # log and never duplicate. Without it, behave exactly as before.
        if body.client_log_id:
            key = barn_filter(user, {"client_log_id": body.client_log_id})
            await db.medication_logs.update_one(key, {"$setOnInsert": doc}, upsert=True)
            return clean(await db.medication_logs.find_one(key, {"_id": 0}))
        # No key: preserve the original shape — don't persist/return client_log_id: null.
        doc.pop("client_log_id", None)
        await db.medication_logs.insert_one(doc)
        return clean(doc)

    # ---------------- Feed Tasks (legacy collection — kept for back-compat) ----------------

    @router.get("/feed-tasks")
    async def list_feed(date_str: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return []
        extra = {"date": date_str} if date_str else {}
        # Phase 6C: deterministic newest-first ordering (created_at desc).
        return await list_collection("feed_tasks", barn_filter(user, extra), sort_field="created_at")

    @router.post("/feed-tasks/{task_id}/complete")
    async def complete_feed(task_id: str, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        scope = barn_filter(user, {"id": task_id})
        if not await db.feed_tasks.find_one(scope, {"_id": 0}):
            raise HTTPException(404, "Feed task not found")
        # Phase 6B: idempotent completion — only set fields when not already
        # completed, so a re-complete preserves the original completer/timestamp.
        # Response shape is unchanged (still the feed-task doc).
        await db.feed_tasks.update_one(
            barn_filter(user, {"id": task_id, "completed": {"$ne": True}}),
            {"$set": {"completed": True, "completed_by": user["full_name"], "completed_at": _iso(_now_utc())}},
        )
        return await db.feed_tasks.find_one(scope, {"_id": 0})

    # ---------------- Vet records ----------------

    @router.get("/vet-records")
    async def list_vet(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return await list_collection("vet_records", await _care_scope(user, horse_id), sort_field="date")
        # Phase 4B-7: read now barn-scoped — the task_engine completion hooks
        # stamp barn_id on engine-written vet_records (and the startup backfill
        # covers legacy rows), so barn_filter no longer hides engine-projected rows.
        extra = {"horse_id": horse_id} if horse_id else None
        return await list_collection("vet_records", barn_filter(user, extra), sort_field="date")

    @router.post("/vet-records")
    async def create_vet(body: VetRecordIn, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        horse = await _require_horse(user, body.horse_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        doc["barn_id"] = horse.get("barn_id") if is_provider_user(user) else stamp_barn(user, doc)["barn_id"]
        await db.vet_records.insert_one(doc)
        return clean(doc)

    # ---------------- Farrier history (engine-projected) ----------------

    @router.get("/farrier-history")
    async def list_farrier(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return await list_collection("farrier_history", await _care_scope(user, horse_id), sort_field="date")
        # Phase 4B-7: read now barn-scoped — engine-written farrier_history rows
        # stamp barn_id (+ startup backfill for legacy rows). See vet-records note.
        # Phase 6C: harmonized to route through list_collection (date desc) — same
        # behavior as the bespoke .find().sort().to_list(500) it replaced.
        extra = {"horse_id": horse_id} if horse_id else None
        return await list_collection("farrier_history", barn_filter(user, extra), sort_field="date")

    # ---------------- Injuries ----------------

    @router.get("/injuries")
    async def list_injuries(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return await list_collection("injuries", await _care_scope(user, horse_id), sort_field="created_at")
        extra = {"horse_id": horse_id} if horse_id else {}
        # Phase 6C: deterministic newest-first ordering (created_at desc).
        return await list_collection("injuries", barn_filter(user, extra), sort_field="created_at")

    @router.post("/injuries")
    async def create_injury(body: InjuryIn, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        horse = await _require_horse(user, body.horse_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        doc["barn_id"] = horse.get("barn_id") if is_provider_user(user) else stamp_barn(user, doc)["barn_id"]
        await db.injuries.insert_one(doc)
        return clean(doc)

    # ---------------- Wellness ----------------

    @router.get("/wellness")
    async def list_wellness(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        if is_provider_user(user):
            return await list_collection("wellness", await _care_scope(user, horse_id), sort_field="created_at")
        extra = {"horse_id": horse_id} if horse_id else {}
        return await list_collection("wellness", barn_filter(user, extra), sort_field="created_at")

    @router.post("/wellness")
    async def create_wellness(body: WellnessIn, user=Depends(get_current_user)):
        _reject_provider_care_write(user)
        # Phase 6A: reject a foreign/absent horse_id up front (no record written).
        horse = await _require_horse(user, body.horse_id)
        doc = body.model_dump()
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        doc["barn_id"] = horse.get("barn_id") if is_provider_user(user) else stamp_barn(user, doc)["barn_id"]
        await db.wellness.insert_one(doc)
        # Bump horse wellness_score using the same heuristic as before.
        # Phase 4B-2: scope the horse update by barn so a cross-barn horse_id
        # can never trigger a side effect on another barn's horse.
        avg = (body.appetite + body.water_intake + body.energy + body.coat_quality) * 5
        horse_scope = {"id": body.horse_id, "barn_id": horse.get("barn_id")} if is_provider_user(user) else barn_filter(user, {"id": body.horse_id})
        await db.horses.update_one(horse_scope, {"$set": {"wellness_score": min(100, avg)}})
        return clean(doc)

    return router
