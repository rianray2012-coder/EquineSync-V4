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
    message_guardian_minor_safeguarding_gate,
    message_minor_communication_gate,
    message_response_projection,
)
from core.minor_safety import (
    DECISION_ALLOW,
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_EVENT_SIGNUP,
    WORKFLOW_LESSON_READY,
    audit_safe_guardian_minor_metadata,
    guardian_minor_public_error_detail,
    guardian_minor_workflow_gate,
    load_guardian_minor_authority_rows,
    minor_status_for_student,
    normalize_minor_status,
    student_workflow_scope,
)
from core.permissions import require
from core.tenancy import barn_filter, stamp_barn
from core import audit
from routes.backlog import _classify_arena_conflicts


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
    student_profile_id: Optional[str] = None
    guardian_guard_scope_reference: Optional[str] = None
    guardian_state_token: Optional[str] = None
    horse_id: Optional[str] = None
    trainer_id: Optional[str] = None
    start_time: str
    duration_min: int = 60
    focus: Optional[str] = None
    notes: Optional[str] = None
    completed: bool = False
    safety_stop: Optional[bool] = False
    suitability_status: Optional[str] = None


class TrainingSessionIn(BaseModel):
    horse_id: str
    student_profile_id: Optional[str] = None
    guardian_guard_scope_reference: Optional[str] = None
    guardian_state_token: Optional[str] = None
    trainer_id: Optional[str] = None
    date: str
    discipline: Optional[str] = None
    exercises: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[int] = None
    homework: Optional[str] = None
    safety_stop: Optional[bool] = False
    suitability_status: Optional[str] = None


class LessonCancelIn(BaseModel):
    reason: str
    cancelled_at: Optional[str] = None


class LessonSubstitutionIn(BaseModel):
    substitute_trainer_id: Optional[str] = None
    substitute_horse_id: Optional[str] = None
    substitute_rider_id: Optional[str] = None
    reason: str


class TrainingCancelIn(BaseModel):
    reason: str
    cancelled_at: Optional[str] = None


class TrainingSubstitutionIn(BaseModel):
    substitute_trainer_id: Optional[str] = None
    substitute_horse_id: Optional[str] = None
    reason: str


class MessageIn(BaseModel):
    to_role: Optional[str] = None
    to_user_id: Optional[str] = None
    subject: str
    body: str
    visibility: str = "staff_only"
    student_profile_id: Optional[str] = None
    student_profile_ids: Optional[list[str]] = None
    participant_user_ids: Optional[list[str]] = None
    guardian_user_ids: Optional[list[str]] = None


class ServiceRequestIn(BaseModel):
    horse_id: str
    type: str
    student_profile_id: Optional[str] = None
    guardian_guard_scope_reference: Optional[str] = None
    guardian_state_token: Optional[str] = None
    event_id: Optional[str] = None
    event_policy_version: Optional[str] = None
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

    def _minor_status_from_age(age: Any) -> str:
        try:
            years = int(age)
        except (TypeError, ValueError):
            return MINOR_STATUS_UNKNOWN
        if years < 13:
            return MINOR_STATUS_UNDER_13
        if years < 18:
            return MINOR_STATUS_MINOR_13_TO_17
        return MINOR_STATUS_ADULT

    async def _student_from_profile_id(user: Dict[str, Any], student_profile_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not student_profile_id:
            return None
        return await db[STUDENT_PROFILE_COLLECTION].find_one(
            barn_filter(user, {"id": student_profile_id}),
            {"_id": 0},
        )

    async def _student_from_rider(user: Dict[str, Any], rider: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not rider:
            return None
        linked_student_id = rider.get("student_profile_id")
        if linked_student_id:
            linked = await _student_from_profile_id(user, linked_student_id)
            if linked:
                return linked
            return {
                "id": linked_student_id,
                "barn_id": rider.get("barn_id") or user.get("barn_id") or "primary",
                "minor_status": MINOR_STATUS_UNKNOWN,
            }
        minor_status = normalize_minor_status(rider.get("minor_status") or MINOR_STATUS_UNKNOWN)
        if minor_status == MINOR_STATUS_UNKNOWN and rider.get("age") is not None:
            minor_status = _minor_status_from_age(rider.get("age"))
        student = {
            "id": f"rider:{rider.get('id')}",
            "barn_id": rider.get("barn_id") or user.get("barn_id") or "primary",
            "birthdate": rider.get("birthdate"),
            "minor_status": minor_status,
        }
        student["minor_status"] = minor_status_for_student(student)
        return student

    async def _students_for_subjects(
        *,
        user: Dict[str, Any],
        student_profile_id: Optional[str] = None,
        rider: Optional[Dict[str, Any]] = None,
        horse: Optional[Dict[str, Any]] = None,
    ) -> list[Dict[str, Any]]:
        students: list[Dict[str, Any]] = []
        explicit_student = await _student_from_profile_id(user, student_profile_id)
        if student_profile_id and not explicit_student:
            students.append({
                "id": student_profile_id,
                "barn_id": user.get("barn_id") or "primary",
                "minor_status": MINOR_STATUS_UNKNOWN,
            })
        elif explicit_student:
            students.append(explicit_student)
        rider_row = rider
        if not rider_row and horse and horse.get("rider_id"):
            rider_row = await db.riders.find_one(
                barn_filter(user, {"id": horse["rider_id"]}),
                {"_id": 0},
            )
        from_rider = await _student_from_rider(user, rider_row)
        if from_rider and explicit_student:
            linked_id = rider_row.get("student_profile_id") if rider_row else None
            if linked_id and linked_id != explicit_student.get("id"):
                students.append(from_rider)
        elif from_rider and from_rider.get("id") not in {student.get("id") for student in students}:
            students.append(from_rider)
        return students

    def _guarded_scope_reference(workflow: str, students: list[Dict[str, Any]], explicit_scope: Optional[str], fallback: str) -> str:
        if explicit_scope and explicit_scope.strip():
            return explicit_scope.strip()
        guarded = [
            student for student in students
            if minor_status_for_student(student) != MINOR_STATUS_ADULT
        ]
        if len(guarded) == 1:
            scoped = student_workflow_scope(guarded[0].get("id"), workflow)
            if scoped:
                return scoped
        return fallback

    async def _enforce_guarded_students(
        *,
        students: list[Dict[str, Any]],
        workflow: str,
        scope_reference: str,
        policy_version: str,
        expected_state_token: Optional[str] = None,
        action: str,
        request: Request,
        user: Dict[str, Any],
        status_code: int = 409,
    ) -> Dict[str, Any]:
        barn_id = user.get("barn_id") or "primary"
        if students and all(minor_status_for_student(student) == MINOR_STATUS_ADULT for student in students):
            links, consents = [], []
        else:
            links, consents = await load_guardian_minor_authority_rows(
                db,
                barn_id=barn_id,
                student_profile_ids=[student.get("id") for student in students],
                workflow=workflow,
            )
        gate = guardian_minor_workflow_gate(
            workflow=workflow,
            students=students,
            guardian_links=links,
            workflow_consents=consents,
            barn_id=barn_id,
            scope_reference=scope_reference,
            policy_version=policy_version,
            expected_state_token=expected_state_token,
            action=action,
        )
        if gate["decision"] == DECISION_ALLOW:
            return gate
        await audit.record(
            action="guardian_minor.workflow_blocked",
            user=user,
            request=request,
            resource_type="guardian_minor_guard",
            resource_id=scope_reference,
            outcome="denied",
            status_code=status_code,
            metadata=audit_safe_guardian_minor_metadata(gate),
            _db=db,
        )
        raise HTTPException(status_code=status_code, detail=guardian_minor_public_error_detail(gate))

    async def _enforce_safety_stop(
        *,
        user: Dict[str, Any],
        horse: Optional[Dict[str, Any]] = None,
        rider: Optional[Dict[str, Any]] = None,
        requested_safety_stop: Optional[bool] = False,
        requested_suitability_status: Optional[str] = None,
    ) -> None:
        suitability = (requested_suitability_status or "").strip().lower()
        if requested_safety_stop or suitability in {"blocked", "not_suitable", "safety_stop"}:
            raise HTTPException(409, "Safety Stop blocks lesson/training participation")

        subject_ids = [
            value for value in [
                horse.get("id") if horse else None,
                rider.get("id") if rider else None,
            ] if value
        ]
        safety_stops = getattr(db, "safety_stops", None)
        if subject_ids and safety_stops is not None:
            active_stop = await safety_stops.find_one(
                barn_filter(user, {
                    "subject_id": {"$in": subject_ids},
                    "status": {"$in": ["active", "hard_stop"]},
                }),
                {"_id": 0, "id": 1, "subject_id": 1, "reason": 1},
            )
            if active_stop:
                raise HTTPException(409, "Safety Stop blocks lesson/training participation")

        for source in (horse or {}, rider or {}):
            if source.get("safety_stop_active") is True:
                raise HTTPException(409, "Safety Stop blocks lesson/training participation")
            source_suitability = (source.get("suitability_status") or "").strip().lower()
            if source_suitability in {"blocked", "not_suitable", "safety_stop"}:
                raise HTTPException(409, "Safety Stop blocks lesson/training participation")

    async def _record_lesson_training_event(
        collection_name: str,
        record_id: str,
        event_type: str,
        user: Dict[str, Any],
        metadata: Dict[str, Any],
    ) -> None:
        await db.lesson_training_events.insert_one({
            "id": new_id(),
            "barn_id": user.get("barn_id") or "primary",
            "collection": collection_name,
            "record_id": record_id,
            "event_type": event_type,
            "metadata": metadata,
            "created_at": _iso(_now_utc()),
            "created_by_user_id": user["id"],
        })

    async def _require_same_barn_horse(user: Dict[str, Any], horse_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not horse_id:
            return None
        horse = await db.horses.find_one(
            barn_filter(user, {"id": horse_id}),
            {"_id": 0, "id": 1, "name": 1, "safety_stop_active": 1, "suitability_status": 1},
        )
        if not horse:
            raise HTTPException(404, "Horse not found")
        return horse

    async def _require_same_barn_rider(user: Dict[str, Any], rider_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not rider_id:
            return None
        rider = await db.riders.find_one(barn_filter(user, {"id": rider_id}), {"_id": 0})
        if not rider:
            raise HTTPException(404, "Rider not found")
        return rider

    # ---------------- Lessons ----------------

    @router.get("/lessons")
    async def list_lessons(user=Depends(get_current_user)):
        q = _trainer_owned_filter(user) if _is_trainer(user) else barn_filter(user)
        return await list_collection("lessons", q, sort_field="start_time")

    @router.post("/lessons")
    async def create_lesson(body: LessonIn, request: Request, user=Depends(get_current_user)):
        doc = body.model_dump()
        # Best-effort name resolution so list views render without an extra
        # lookup hop. Missing references are tolerated (operationally a
        # rider record may be added later, after the lesson is sketched in).
        # Phase 4B-3: all enrichment lookups are barn-scoped so a cross-barn id
        # resolves to None (no cross-barn name leak); RF9 now requires stable
        # same-barn references for lesson creates.
        rider = await db.riders.find_one(barn_filter(user, {"id": body.rider_id}), {"_id": 0})
        if not rider:
            raise HTTPException(404, "Rider not found")
        doc["rider_name"] = rider["full_name"] if rider else None
        if body.horse_id:
            horse = await db.horses.find_one(
                barn_filter(user, {"id": body.horse_id}),
                {"_id": 0, "id": 1, "name": 1, "safety_stop_active": 1, "suitability_status": 1},
            )
            if not horse:
                raise HTTPException(404, "Horse not found")
            doc["horse_name"] = horse["name"] if horse else None
        else:
            horse = None
        await _enforce_safety_stop(
            user=user,
            horse=horse,
            rider=rider,
            requested_safety_stop=body.safety_stop,
            requested_suitability_status=body.suitability_status,
        )
        await _stamp_trainer_identity(db, user, doc)
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        students = await _students_for_subjects(
            user=user,
            student_profile_id=body.student_profile_id,
            rider=rider,
        )
        guard_scope = _guarded_scope_reference(
            WORKFLOW_LESSON_READY,
            students,
            body.guardian_guard_scope_reference,
            f"lesson:{doc['id']}",
        )
        gate = await _enforce_guarded_students(
            students=students,
            workflow=WORKFLOW_LESSON_READY,
            scope_reference=guard_scope,
            policy_version="lesson-ready-v1",
            expected_state_token=body.guardian_state_token,
            action="lesson.create",
            request=request,
            user=user,
        )
        doc["guardian_guard_scope_reference"] = guard_scope
        doc["guardian_guard_policy_version"] = "lesson-ready-v1"
        doc["guardian_guard_state_token"] = gate.get("state_token")
        await db.lessons.insert_one(doc)
        return clean(doc)

    @router.post("/lessons/{lesson_id}/cancel")
    async def cancel_lesson(lesson_id: str, body: LessonCancelIn, user=Depends(get_current_user)):
        scope = barn_filter(user, {"id": lesson_id})
        existing = await db.lessons.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Lesson not found")
        if existing.get("cancelled") or existing.get("status") == "cancelled":
            raise HTTPException(409, "Lesson is already cancelled")
        now = _iso(_now_utc())
        cancelled_at = body.cancelled_at or now
        updates = {
            "status": "cancelled",
            "cancelled": True,
            "cancelled_at": cancelled_at,
            "cancelled_by_user_id": user["id"],
            "cancel_reason": body.reason[:500],
            "updated_at": now,
        }
        await db.lessons.update_one(scope, {"$set": updates})
        await _record_lesson_training_event(
            "lessons",
            lesson_id,
            "lesson.cancelled",
            user,
            {"reason": body.reason[:500], "cancelled_at": cancelled_at},
        )
        return clean(await db.lessons.find_one(scope, {"_id": 0}))

    @router.post("/lessons/{lesson_id}/substitute")
    async def substitute_lesson(lesson_id: str, body: LessonSubstitutionIn, user=Depends(get_current_user)):
        scope = barn_filter(user, {"id": lesson_id})
        existing = await db.lessons.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Lesson not found")
        if existing.get("cancelled") or existing.get("status") == "cancelled":
            raise HTTPException(409, "Cancelled lessons cannot be substituted")
        substitute_horse = await _require_same_barn_horse(user, body.substitute_horse_id)
        substitute_rider = await _require_same_barn_rider(user, body.substitute_rider_id)
        substitute_trainer = (
            await _require_same_barn_trainer(db, user, body.substitute_trainer_id)
            if body.substitute_trainer_id else None
        )
        await _enforce_safety_stop(user=user, horse=substitute_horse, rider=substitute_rider)
        now = _iso(_now_utc())
        updates = {
            "substitution_state": "substituted",
            "substitution_reason": body.reason[:500],
            "substituted_at": now,
            "substituted_by_user_id": user["id"],
            "updated_at": now,
        }
        if substitute_trainer:
            updates["substitute_trainer_id"] = substitute_trainer["id"]
            updates["substitute_trainer_name"] = substitute_trainer.get("full_name") or substitute_trainer.get("email")
        if substitute_horse:
            updates["substitute_horse_id"] = substitute_horse["id"]
            updates["substitute_horse_name"] = substitute_horse.get("name")
        if substitute_rider:
            updates["substitute_rider_id"] = substitute_rider["id"]
            updates["substitute_rider_name"] = substitute_rider.get("full_name")
        await db.lessons.update_one(scope, {"$set": updates})
        await _record_lesson_training_event(
            "lessons",
            lesson_id,
            "lesson.substituted",
            user,
            {
                "reason": body.reason[:500],
                "substitute_trainer_id": body.substitute_trainer_id,
                "substitute_horse_id": body.substitute_horse_id,
                "substitute_rider_id": body.substitute_rider_id,
            },
        )
        return clean(await db.lessons.find_one(scope, {"_id": 0}))

    # ---------------- Training ----------------

    @router.get("/training")
    async def list_training(horse_id: Optional[str] = None, user=Depends(get_current_user)):
        extra = {"horse_id": horse_id} if horse_id else {}
        if _is_trainer(user):
            extra = {**extra, "$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}]}
        return await list_collection("training", barn_filter(user, extra), sort_field="date")

    @router.post("/training")
    async def create_training(body: TrainingSessionIn, request: Request, user=Depends(get_current_user)):
        doc = body.model_dump()
        horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0})
        if not horse:
            raise HTTPException(404, "Horse not found")
        doc["horse_name"] = horse["name"] if horse else None
        await _enforce_safety_stop(
            user=user,
            horse=horse,
            requested_safety_stop=body.safety_stop,
            requested_suitability_status=body.suitability_status,
        )
        await _stamp_trainer_identity(db, user, doc)
        doc.update({"id": new_id(), "created_at": _iso(_now_utc())})
        stamp_barn(user, doc)
        students = await _students_for_subjects(
            user=user,
            student_profile_id=body.student_profile_id,
            horse=horse,
        )
        guard_scope = _guarded_scope_reference(
            WORKFLOW_LESSON_READY,
            students,
            body.guardian_guard_scope_reference,
            f"training:{doc['id']}",
        )
        gate = await _enforce_guarded_students(
            students=students,
            workflow=WORKFLOW_LESSON_READY,
            scope_reference=guard_scope,
            policy_version="lesson-ready-v1",
            expected_state_token=body.guardian_state_token,
            action="training.create",
            request=request,
            user=user,
        )
        doc["guardian_guard_scope_reference"] = guard_scope
        doc["guardian_guard_policy_version"] = "lesson-ready-v1"
        doc["guardian_guard_state_token"] = gate.get("state_token")
        await db.training.insert_one(doc)
        return clean(doc)

    @router.post("/training/{training_id}/cancel")
    async def cancel_training(training_id: str, body: TrainingCancelIn, user=Depends(get_current_user)):
        scope = barn_filter(user, {"id": training_id})
        existing = await db.training.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Training session not found")
        if existing.get("cancelled") or existing.get("status") == "cancelled":
            raise HTTPException(409, "Training session is already cancelled")
        now = _iso(_now_utc())
        cancelled_at = body.cancelled_at or now
        updates = {
            "status": "cancelled",
            "cancelled": True,
            "cancelled_at": cancelled_at,
            "cancelled_by_user_id": user["id"],
            "cancel_reason": body.reason[:500],
            "updated_at": now,
        }
        await db.training.update_one(scope, {"$set": updates})
        await _record_lesson_training_event(
            "training",
            training_id,
            "training.cancelled",
            user,
            {"reason": body.reason[:500], "cancelled_at": cancelled_at},
        )
        return clean(await db.training.find_one(scope, {"_id": 0}))

    @router.post("/training/{training_id}/substitute")
    async def substitute_training(training_id: str, body: TrainingSubstitutionIn, user=Depends(get_current_user)):
        scope = barn_filter(user, {"id": training_id})
        existing = await db.training.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Training session not found")
        if existing.get("cancelled") or existing.get("status") == "cancelled":
            raise HTTPException(409, "Cancelled training sessions cannot be substituted")
        substitute_horse = await _require_same_barn_horse(user, body.substitute_horse_id)
        substitute_trainer = (
            await _require_same_barn_trainer(db, user, body.substitute_trainer_id)
            if body.substitute_trainer_id else None
        )
        await _enforce_safety_stop(user=user, horse=substitute_horse)
        now = _iso(_now_utc())
        updates = {
            "substitution_state": "substituted",
            "substitution_reason": body.reason[:500],
            "substituted_at": now,
            "substituted_by_user_id": user["id"],
            "updated_at": now,
        }
        if substitute_trainer:
            updates["substitute_trainer_id"] = substitute_trainer["id"]
            updates["substitute_trainer_name"] = substitute_trainer.get("full_name") or substitute_trainer.get("email")
        if substitute_horse:
            updates["substitute_horse_id"] = substitute_horse["id"]
            updates["substitute_horse_name"] = substitute_horse.get("name")
        await db.training.update_one(scope, {"$set": updates})
        await _record_lesson_training_event(
            "training",
            training_id,
            "training.substituted",
            user,
            {
                "reason": body.reason[:500],
                "substitute_trainer_id": body.substitute_trainer_id,
                "substitute_horse_id": body.substitute_horse_id,
            },
        )
        return clean(await db.training.find_one(scope, {"_id": 0}))

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
        v11_gate = await message_guardian_minor_safeguarding_gate(db=db, actor_user=user, message=doc)
        if v11_gate["decision"] != "allow":
            await audit.record(
                action="minor_communication.blocked", user=user, request=request,
                resource_type="student_profile",
                resource_id=(doc.get("student_profile_id") or None),
                outcome="denied",
                status_code=403,
                metadata=audit_safe_guardian_minor_metadata(v11_gate),
                _db=db,
            )
            raise HTTPException(status_code=403, detail=guardian_minor_public_error_detail(v11_gate))
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
    async def create_sr(body: ServiceRequestIn, request: Request, user=Depends(get_current_user)):
        _validate_service_request(body)
        doc = body.model_dump()
        horse = await db.horses.find_one(barn_filter(user, {"id": body.horse_id}), {"_id": 0})
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
        if (body.type or "").strip().lower() in {"event_signup", "community_program_signup"}:
            students = await _students_for_subjects(
                user=user,
                student_profile_id=body.student_profile_id,
                horse=horse,
            )
            guard_scope = _guarded_scope_reference(
                WORKFLOW_EVENT_SIGNUP,
                students,
                body.guardian_guard_scope_reference or (f"event:{body.event_id}" if body.event_id else None),
                f"service_request:{doc['id']}",
            )
            gate = await _enforce_guarded_students(
                students=students,
                workflow=WORKFLOW_EVENT_SIGNUP,
                scope_reference=guard_scope,
                policy_version=body.event_policy_version or "event-signup-v1",
                expected_state_token=body.guardian_state_token,
                action="service_request.event_signup.create",
                request=request,
                user=user,
            )
            doc["guardian_guard_scope_reference"] = guard_scope
            doc["guardian_guard_policy_version"] = body.event_policy_version or "event-signup-v1"
            doc["guardian_guard_state_token"] = gate.get("state_token")
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
        arena_data = None
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
            barn_id = existing.get("barn_id") or user.get("barn_id") or "primary"
            existing_blocks = await db.arena_schedule_blocks.find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).to_list(500)
            conflict = _classify_arena_conflicts(arena_data, existing_blocks)
            if conflict["requires_review"]:
                raise HTTPException(409, {"code": "calendar_conflict_review_required", **conflict})
            arena_data = {**arena_data, "conflict_state": conflict["state"], "conflict_details": conflict}
        if (existing.get("type") or "").strip().lower() in {"event_signup", "community_program_signup"}:
            horse = None
            if existing.get("horse_id"):
                horse = await db.horses.find_one(barn_filter(user, {"id": existing["horse_id"]}), {"_id": 0})
            students = await _students_for_subjects(
                user=user,
                student_profile_id=existing.get("student_profile_id"),
                horse=horse,
            )
            gate = await _enforce_guarded_students(
                students=students,
                workflow=WORKFLOW_EVENT_SIGNUP,
                scope_reference=existing.get("guardian_guard_scope_reference")
                or (f"event:{existing.get('event_id')}" if existing.get("event_id") else f"service_request:{sr_id}"),
                policy_version=existing.get("guardian_guard_policy_version") or existing.get("event_policy_version") or "event-signup-v1",
                expected_state_token=existing.get("guardian_guard_state_token"),
                action="service_request.event_signup.approve",
                request=request,
                user=user,
            )
            await db.service_requests.update_one(
                scope,
                {"$set": {"guardian_guard_state_token": gate.get("state_token")}},
            )
        await db.service_requests.update_one(
            scope,
            {"$set": {"status": "approved",
                      "approved_at": now,
                      "approved_by_user_id": user["id"]}},
        )
        if arena_data:
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
