"""routes/operations.py — operational records: lessons, training,
messages, service requests, incidents.

Phase-F final extraction (Feb 20 2026). Trivial CRUD over MongoDB
collections, sharing list_collection/clean/new_id helpers. The
service-request approve/decline flows carry their own role gating
(admin/barn_manager/trainer) plus a pending-state guard so re-mutation
returns 409.

Note: invoice/billing routes were extracted to `routes/billing.py` in Phase 3F.
"""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from core.minor_communication import (
    audit_safe_minor_communication_metadata,
    message_minor_communication_gate,
    message_response_projection,
)
from core.permissions import require
from core.tenancy import barn_filter, stamp_barn
from core import audit


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _is_trainer(user: Dict[str, Any]) -> bool:
    return (user.get("role") or "").strip().lower() == "trainer"


def _trainer_owned_filter(user: Dict[str, Any]) -> Dict[str, Any]:
    return barn_filter(user, {"$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}]})


async def _require_same_barn_trainer(db, user: Dict[str, Any], trainer_id: str) -> Dict[str, Any]:
    trainer = await db.users.find_one(
        barn_filter(user, {"id": trainer_id, "role": "trainer"}),
        {"_id": 0, "id": 1, "full_name": 1, "email": 1},
    )
    if not trainer:
        raise HTTPException(422, "Unknown trainer")
    return trainer


async def _stamp_trainer_identity(db, user: Dict[str, Any], doc: Dict[str, Any]) -> Dict[str, Any]:
    trainer_id = doc.get("trainer_id")
    if _is_trainer(user):
        if trainer_id and trainer_id != user.get("id"):
            raise HTTPException(403, "Trainer can only assign their own trainer id")
        doc["trainer_id"] = user.get("id")
        doc["trainer_name"] = user.get("full_name") or user.get("email") or user.get("id")
        return doc
    if trainer_id:
        trainer = await _require_same_barn_trainer(db, user, trainer_id)
        doc["trainer_id"] = trainer["id"]
        doc["trainer_name"] = trainer.get("full_name") or trainer.get("email") or trainer["id"]
        return doc
    doc["trainer_name"] = user.get("full_name")
    return doc


# ---------------- Models ----------------

class LessonIn(BaseModel):
    rider_id: str
    horse_id: Optional[str] = None
    trainer_id: Optional[str] = None
    start_time: str
    duration_min: int = 60
    focus: Optional[str] = None
    notes: Optional[str] = None
    completed: bool = False


class TrainingSessionIn(BaseModel):
    horse_id: str
    trainer_id: Optional[str] = None
    date: str
    discipline: Optional[str] = None
    exercises: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[int] = None
    homework: Optional[str] = None


class MessageIn(BaseModel):
    to_role: Optional[str] = None
    to_user_id: Optional[str] = None
    subject: str
    body: str
    visibility: str = "staff_only"
    student_profile_id: Optional[str] = None
    participant_user_ids: Optional[list[str]] = None
    guardian_user_ids: Optional[list[str]] = None


class ServiceRequestIn(BaseModel):
    horse_id: str
    type: str
    details: Optional[str] = None
    requested_date: Optional[str] = None
    requested_time: Optional[str] = None
    rental_duration: Optional[str] = None
    arena_name: Optional[str] = None


class DeclineSRBody(BaseModel):
    reason: Optional[str] = None


class IncidentIn(BaseModel):
    horse_id: Optional[str] = None
    type: str
    title: str
    description: str
    severity: str = "moderate"
    occurred_at: str
    follow_up: Optional[str] = None


def build_router(*, db, get_current_user, list_collection, clean, new_id) -> APIRouter:
    router = APIRouter(tags=["operations"])

    # ---------------- Lessons ----------------

    @router.get("/lessons")
    async def list_lessons(user=Depends(get_current_user)):
        q = _trainer_owned_filter(user) if _is_trainer(user) else barn_filter(user)
        return await list_collection("lessons", q, sort_field="start_time")

    @router.post("/lessons")
    async def create_lesson(body: LessonIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        # Best-effort name resolution so list views render without an extra
        # lookup hop. Missing references are tolerated (operationally a
        # rider record may be added later, after the lesson is sketched in).
        # Phase 4B-3: all enrichment lookups are barn-scoped so a cross-barn id
        # resolves to None (no cross-barn name leak); RF9 now requires stable
        # same-barn references for lesson creates.
        rider = await db.riders.find_one(barn_filter(user, {"id": body.rider_id}), {"_id": 0, "full_name": 1})
        if not rider:
            raise HTTPException(404, "Rider not found")
        doc["rider_name"] = rider["full_name"] if rider else None
        if body.horse_id:
            horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0, "name": 1})
            if not horse:
                raise HTTPException(404, "Horse not found")
            doc["horse_name"] = horse["name"] if horse else None
        await _stamp_trainer_identity(db, user, doc)
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        await db.lessons.insert_one(doc)
        return clean(doc)

    # ---------------- Training ----------------

    @router.get("/training")
    async def list_training(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        extra = {"horse_id": horse_id} if horse_id else {}
        if _is_trainer(user):
            extra = {**extra, "$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}]}
        return await list_collection("training", barn_filter(user, extra), sort_field="date")

    @router.post("/training")
    async def create_training(body: TrainingSessionIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0, "name": 1})
        if not horse:
            raise HTTPException(404, "Horse not found")
        doc["horse_name"] = horse["name"] if horse else None
        await _stamp_trainer_identity(db, user, doc)
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        await db.training.insert_one(doc)
        return clean(doc)

    # ---------------- Messages ----------------

    @router.get("/messages")
    async def list_messages(user=Depends(get_current_user)):
        rows = await list_collection("messages", barn_filter(user), sort_field="created_at")
        return [message_response_projection(row) for row in rows]

    @router.post("/messages")
    async def create_message(body: MessageIn, request: Request, user=Depends(get_current_user)):
        doc = body.model_dump()
        gate = await message_minor_communication_gate(db=db, actor_user=user, message=doc)
        if gate["decision"] != "allow":
            await audit.record(
                action="minor_communication.blocked", user=user, request=request,
                resource_type="student_profile",
                resource_id=(doc.get("student_profile_id") or None),
                outcome="denied",
                status_code=403,
                metadata=audit_safe_minor_communication_metadata(gate),
            )
            raise HTTPException(status_code=403, detail="Guardian must be included")
        doc.update({
            "id": new_id(),
            "from_user_id": user["id"],
            "from_name": user["full_name"],
            "created_at": _iso(_now_utc()),
            "read": False,
        })
        stamp_barn(user, doc)
        await db.messages.insert_one(doc)
        return message_response_projection(doc)

    # ---------------- Service Requests ----------------

    def _arena_end_time(start: Optional[str], rental_duration: Optional[str]) -> str:
        duration_map = {
            "30_min": timedelta(minutes=30),
            "1_hour": timedelta(hours=1),
            "half_day": timedelta(hours=4),
            "full_day": timedelta(hours=8),
        }
        if not start:
            return ""
        try:
            base = datetime.combine(datetime.now(timezone.utc).date(), time.fromisoformat(start))
        except ValueError:
            return ""
        return (base + duration_map.get(rental_duration or "", timedelta(hours=1))).time().strftime("%H:%M")

    def _validate_service_request(body: ServiceRequestIn) -> None:
        if body.type != "arena_use":
            return
        allowed = {"30_min", "1_hour", "half_day", "full_day"}
        if body.rental_duration not in allowed:
            raise HTTPException(422, "Arena bookings must use 30 minutes, 1 hour, half day, or full day")
        if not body.requested_date:
            raise HTTPException(422, "Requested date is required for arena bookings")
        if body.rental_duration in {"30_min", "1_hour"} and not body.requested_time:
            raise HTTPException(422, "Start time is required for 30 minute and 1 hour arena bookings")

    @router.get("/service-requests")
    async def list_sr(user=Depends(get_current_user)):
        extra = {"requested_by": user.get("id")} if user.get("role") in ("horse_owner", "parent") else {}
        return await list_collection("service_requests", barn_filter(user, extra), sort_field="created_at")

    @router.post("/service-requests")
    async def create_sr(body: ServiceRequestIn, user=Depends(get_current_user)):
        _validate_service_request(body)
        doc = body.model_dump()
        horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0, "name": 1})
        if not horse:
            raise HTTPException(404, "Horse not found")
        doc["horse_name"] = horse["name"] if horse else None
        doc.update({
            "id": new_id(),
            "requested_by": user["id"],
            "requester_name": user["full_name"],
            "status": "pending",
            "created_at": _iso(_now_utc()),
        })
        stamp_barn(user, doc)
        await db.service_requests.insert_one(doc)
        return clean(doc)

    @router.post("/service-requests/{sr_id}/approve")
    async def approve_sr(sr_id: str, request: Request, user=Depends(get_current_user)):
        require(user, "service_request:approve")
        scope = barn_filter(user, {"id": sr_id})
        existing = await db.service_requests.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Service request not found")
        if existing.get("status") != "pending":
            raise HTTPException(409, f"Request is already {existing.get('status')}")
        now = _iso(_now_utc())
        await db.service_requests.update_one(
            scope,
            {"$set": {"status": "approved",
                      "approved_at": now,
                      "approved_by_user_id": user["id"]}},
        )
        if existing.get("type") == "arena_use":
            arena_data = {
                "arena_name": existing.get("arena_name") or "Arena",
                "title": f"Arena rental · {existing.get('requester_name') or 'Owner'}",
                "date": existing.get("requested_date") or "",
                "start_time": existing.get("requested_time") or "",
                "end_time": _arena_end_time(existing.get("requested_time"), existing.get("rental_duration")),
                "rental_duration": existing.get("rental_duration") or "",
                "status": "reserved",
                "visibility": "shared_with_owners",
                "horse_name": existing.get("horse_name") or "",
                "owner_name": existing.get("requester_name") or "",
                "notes": existing.get("details") or "",
                "source_request_id": sr_id,
            }
            await db.arena_schedule_blocks.insert_one({
                "id": new_id(),
                "barn_id": existing.get("barn_id") or user.get("barn_id") or "primary",
                "data": arena_data,
                "created_at": now,
                "updated_at": now,
                "created_by": user["id"],
                "updated_by": user["id"],
            })
        await audit.record(
            action="service_request.approved", user=user, request=request,
            resource_type="service_request", resource_id=sr_id,
            metadata={"type": existing.get("type")},
        )
        return await db.service_requests.find_one(scope, {"_id": 0})

    @router.post("/service-requests/{sr_id}/decline")
    async def decline_sr(sr_id: str, request: Request, body: Optional[DeclineSRBody] = None,
                          user=Depends(get_current_user)):
        require(user, "service_request:decline")
        scope = barn_filter(user, {"id": sr_id})
        existing = await db.service_requests.find_one(scope, {"_id": 0, "status": 1})
        if not existing:
            raise HTTPException(404, "Service request not found")
        if existing.get("status") != "pending":
            raise HTTPException(409, f"Request is already {existing.get('status')}")
        reason = (body.reason if body else None) or "Request declined."
        await db.service_requests.update_one(
            scope,
            {"$set": {
                "status": "declined",
                "declined_at": _iso(_now_utc()),
                "declined_by_user_id": user["id"],
                "decline_reason": reason[:500],
            }},
        )
        await audit.record(
            action="service_request.declined", user=user, request=request,
            resource_type="service_request", resource_id=sr_id,
            metadata={"reason_provided": bool(body and body.reason)},
        )
        return await db.service_requests.find_one(scope, {"_id": 0})

    # ---------------- Incidents ----------------

    @router.get("/incidents")
    async def list_incidents(user=Depends(get_current_user)):
        return await list_collection("incidents", barn_filter(user), sort_field="occurred_at")

    @router.post("/incidents")
    async def create_incident(body: IncidentIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        if body.horse_id:
            horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0, "name": 1})
            doc["horse_name"] = horse["name"] if horse else None
        else:
            doc["horse_name"] = None
        doc.update({"id": new_id(),
                    "status": "open",
                    "reported_by": user["full_name"],
                    "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        await db.incidents.insert_one(doc)
        return clean(doc)

    return router
