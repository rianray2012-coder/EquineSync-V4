"""Build-Next-5C minor communication guard.

Pure policy helpers plus one tiny DB-backed evaluator for the existing
`POST /api/messages` write path. This does not create a new messaging system,
thread model, notification channel, or frontend surface.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from core.minor_safety import (
    DECISION_ALLOW,
    DECISION_BLOCK,
    DECISION_REQUIRE_GUARDIAN,
    GUARDIAN_LINK_ACTIVE,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_MESSAGING,
    guardian_minor_workflow_gate,
    load_guardian_minor_authority_rows,
    minor_status_for_student,
    requires_guardian,
)


ACTION_CREATE_MESSAGE = "create_message"
ACTION_REMOVE_PARTICIPANT = "remove_participant"
COMMUNICATION_ACTIONS = {ACTION_CREATE_MESSAGE, ACTION_REMOVE_PARTICIPANT}

REASON_NO_STUDENT = "no_student_reference"
REASON_NO_MINOR = "no_minor_involved"
REASON_ACTIVE_GUARDIAN_INCLUDED = "active_guardian_included"
REASON_ACTIVE_GUARDIAN_REQUIRED = "active_guardian_required"
REASON_LAST_GUARDIAN_REMOVAL_BLOCKED = "last_guardian_removal_blocked"

_SAFE_METADATA_KEYS = {
    "decision",
    "reason_code",
    "minor_involved",
    "student_profile_ids",
    "required_guardian_count",
    "included_guardian_count",
    "action",
}

_MESSAGE_RESPONSE_PRIVATE_FIELDS = {
    "student_profile_id",
    "participant_user_ids",
    "guardian_user_ids",
}


def message_response_projection(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Project message rows to the legacy public shape.

    BN5-C stores minor/guardian context so the server can enforce guardian
    inclusion, but the existing inbox API should not expose that linkage data.
    """
    out = dict(doc or {})
    out.pop("_id", None)
    for key in _MESSAGE_RESPONSE_PRIVATE_FIELDS:
        out.pop(key, None)
    return out


def _clean_ids(values: Optional[Iterable[Any]]) -> List[str]:
    out: List[str] = []
    for value in values or []:
        if value is None:
            continue
        text = str(value).strip()
        if text and text not in out:
            out.append(text)
    return out


def _active_guardian_ids(guardian_links: Iterable[Dict[str, Any]]) -> List[str]:
    ids: List[str] = []
    for link in guardian_links or []:
        if (link.get("status") or "").strip().lower() != GUARDIAN_LINK_ACTIVE:
            continue
        guardian_user_id = link.get("guardian_user_id")
        if guardian_user_id and guardian_user_id not in ids:
            ids.append(guardian_user_id)
    return ids


def _message_ids(message: Dict[str, Any], key: str) -> List[str]:
    raw = message.get(key)
    if isinstance(raw, str):
        return _clean_ids([raw])
    return _clean_ids(raw)


def minor_communication_gate(
    *,
    actor_user: Dict[str, Any],
    message: Dict[str, Any],
    students: Iterable[Dict[str, Any]],
    guardian_links: Iterable[Dict[str, Any]],
    participants: Optional[Iterable[str]] = None,
    action: str = ACTION_CREATE_MESSAGE,
) -> Dict[str, Any]:
    """Return the BN5-C communication decision.

    The guard activates only when a student profile is referenced. Unknown-age
    and minor students require an active guardian. Adult students do not.
    """
    student_rows = list(students or [])
    student_ids = _clean_ids([student.get("id") for student in student_rows])
    if not student_rows:
        return {
            "decision": DECISION_ALLOW,
            "reason_code": REASON_NO_STUDENT,
            "minor_involved": False,
            "student_profile_ids": [],
            "required_guardian_user_ids": [],
            "included_guardian_user_ids": [],
            "action": action,
        }

    guarded_students = [
        student for student in student_rows
        if requires_guardian(minor_status_for_student(student))
    ]
    if not guarded_students:
        return {
            "decision": DECISION_ALLOW,
            "reason_code": REASON_NO_MINOR,
            "minor_involved": False,
            "student_profile_ids": student_ids,
            "required_guardian_user_ids": [],
            "included_guardian_user_ids": [],
            "action": action,
        }

    guarded_ids = set(_clean_ids([student.get("id") for student in guarded_students]))
    relevant_links = [
        link for link in (guardian_links or [])
        if link.get("student_profile_id") in guarded_ids
    ]
    required_guardian_ids = _active_guardian_ids(relevant_links)
    included_ids = set(_message_ids(message, "guardian_user_ids"))
    participant_ids = set(_clean_ids(participants)) | set(_message_ids(message, "participant_user_ids"))
    if message.get("to_user_id"):
        participant_ids.add(str(message["to_user_id"]))
    included_guardians = sorted(set(required_guardian_ids) & (included_ids | participant_ids))

    if action == ACTION_REMOVE_PARTICIPANT:
        removing = str(message.get("remove_user_id") or "").strip()
        remaining_guardians = [gid for gid in included_guardians if gid != removing]
        if removing in required_guardian_ids and not remaining_guardians:
            return {
                "decision": DECISION_BLOCK,
                "reason_code": REASON_LAST_GUARDIAN_REMOVAL_BLOCKED,
                "minor_involved": True,
                "student_profile_ids": student_ids,
                "required_guardian_user_ids": required_guardian_ids,
                "included_guardian_user_ids": included_guardians,
                "action": action,
            }

    if not included_guardians:
        return {
            "decision": DECISION_REQUIRE_GUARDIAN,
            "reason_code": REASON_ACTIVE_GUARDIAN_REQUIRED,
            "minor_involved": True,
            "student_profile_ids": student_ids,
            "required_guardian_user_ids": required_guardian_ids,
            "included_guardian_user_ids": [],
            "action": action,
        }

    return {
        "decision": DECISION_ALLOW,
        "reason_code": REASON_ACTIVE_GUARDIAN_INCLUDED,
        "minor_involved": True,
        "student_profile_ids": student_ids,
        "required_guardian_user_ids": required_guardian_ids,
        "included_guardian_user_ids": included_guardians,
        "action": action,
    }


def audit_safe_minor_communication_metadata(gate: Dict[str, Any]) -> Dict[str, Any]:
    """Project safe communication-guard metadata for audit rows."""
    out = {
        "decision": gate.get("decision"),
        "reason_code": gate.get("reason_code"),
        "minor_involved": bool(gate.get("minor_involved")),
        "student_profile_ids": _clean_ids(gate.get("student_profile_ids")),
        "required_guardian_count": len(_clean_ids(gate.get("required_guardian_user_ids"))),
        "included_guardian_count": len(_clean_ids(gate.get("included_guardian_user_ids"))),
        "action": gate.get("action"),
    }
    return {key: value for key, value in out.items() if key in _SAFE_METADATA_KEYS and value is not None}


async def message_minor_communication_gate(
    *,
    db,
    actor_user: Dict[str, Any],
    message: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate the existing `/messages` create payload against BN5-C rules."""
    student_profile_id = message.get("student_profile_id")
    if not student_profile_id:
        return minor_communication_gate(
            actor_user=actor_user,
            message=message,
            students=[],
            guardian_links=[],
            participants=[],
            action=ACTION_CREATE_MESSAGE,
        )

    barn_id = actor_user.get("barn_id") or "primary"
    student = await db[STUDENT_PROFILE_COLLECTION].find_one(
        {"id": student_profile_id, "barn_id": barn_id},
        {"_id": 0},
    )
    if not student:
        return {
            "decision": DECISION_BLOCK,
            "reason_code": "student_profile_not_found",
            "minor_involved": True,
            "student_profile_ids": [student_profile_id],
            "required_guardian_user_ids": [],
            "included_guardian_user_ids": [],
            "action": ACTION_CREATE_MESSAGE,
        }

    links = await db.guardian_links.find(
        {
            "barn_id": barn_id,
            "student_profile_id": student_profile_id,
            "status": GUARDIAN_LINK_ACTIVE,
        },
        {"_id": 0},
    ).to_list(100)
    return minor_communication_gate(
        actor_user=actor_user,
        message=message,
        students=[student],
        guardian_links=links,
        participants=message.get("participant_user_ids") or [],
        action=ACTION_CREATE_MESSAGE,
    )


async def message_guardian_minor_safeguarding_gate(
    *,
    db,
    actor_user: Dict[str, Any],
    message: Dict[str, Any],
    action: str = ACTION_CREATE_MESSAGE,
) -> Dict[str, Any]:
    """Run the V1.1 guard against actual message participants.

    The older BN5 helper accepted an optional `student_profile_id`. This
    evaluator closes the omission path by also resolving student rows from
    same-barn participant user ids when the caller omits student metadata.
    """
    barn_id = actor_user.get("barn_id") or "primary"
    explicit_student_ids = _clean_ids([message.get("student_profile_id")])
    explicit_student_ids.extend(_clean_ids(message.get("student_profile_ids")))
    participant_ids = set(_clean_ids(message.get("participant_user_ids")))
    participant_ids |= set(_clean_ids(message.get("guardian_user_ids")))
    if message.get("to_user_id"):
        participant_ids.add(str(message["to_user_id"]))
    if actor_user.get("id"):
        participant_ids.add(str(actor_user["id"]))

    students: list[Dict[str, Any]] = []
    seen: set[str] = set()
    for student_id in explicit_student_ids:
        student = await db[STUDENT_PROFILE_COLLECTION].find_one(
            {"id": student_id, "barn_id": barn_id},
            {"_id": 0},
        )
        if student and student.get("id") not in seen:
            students.append(student)
            seen.add(student["id"])
    for participant_id in sorted(participant_ids):
        for field in ("user_id", "rider_user_id", "minor_user_id", "student_user_id"):
            student = await db[STUDENT_PROFILE_COLLECTION].find_one(
                {"barn_id": barn_id, field: participant_id},
                {"_id": 0},
            )
            if student and student.get("id") not in seen:
                students.append(student)
                seen.add(student["id"])

    links, consents = await load_guardian_minor_authority_rows(
        db,
        barn_id=barn_id,
        student_profile_ids=[student.get("id") for student in students],
        workflow=WORKFLOW_MESSAGING,
    )
    return guardian_minor_workflow_gate(
        workflow=WORKFLOW_MESSAGING,
        students=students,
        guardian_links=links,
        workflow_consents=consents,
        barn_id=barn_id,
        participant_user_ids=participant_ids,
        scope_reference=str(message.get("thread_id") or message.get("id") or "direct_message"),
        policy_version="messaging-v1",
        consent_required=False,
        require_guardian_participant=True,
        action=action,
    )
