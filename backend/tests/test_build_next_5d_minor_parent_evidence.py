"""Build-Next-5D minor / parent evidence checks.

Evidence-only tests for the locked BN5-A / BN5-B / BN5-C safeguards. These
tests do not introduce product behavior, routes, schemas, or UI.
"""
from __future__ import annotations

from pathlib import Path

from core.minor_communication import (
    ACTION_REMOVE_PARTICIPANT,
    REASON_ACTIVE_GUARDIAN_INCLUDED,
    REASON_ACTIVE_GUARDIAN_REQUIRED,
    REASON_LAST_GUARDIAN_REMOVAL_BLOCKED,
    REASON_NO_STUDENT,
    audit_safe_minor_communication_metadata,
    message_response_projection,
    minor_communication_gate,
)
from core.minor_safety import (
    CONSENT_GRANTED,
    DECISION_ALLOW,
    DECISION_BLOCK,
    DECISION_PARENT_MANAGED_ONLY,
    DECISION_REQUIRE_GUARDIAN,
    GUARDIAN_LINK_ACTIVE,
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    WORKFLOW_INDEPENDENT_LOGIN,
    WORKFLOW_LESSON_READY,
    audit_safe_minor_metadata,
    student_workflow_gate,
)


ROOT = Path(__file__).resolve().parents[2]
STUDENT_GUARDIANS_SRC = (ROOT / "backend/routes/student_guardians.py").read_text(encoding="utf-8")
OPERATIONS_SRC = (ROOT / "backend/routes/operations.py").read_text(encoding="utf-8")


def _actor():
    return {"id": "trainer_1", "role": "trainer", "barn_id": "barn_a"}


def test_bn5d_student_safety_launch_decision_matrix():
    adult = {"id": "student_adult", "barn_id": "barn_a", "minor_status": MINOR_STATUS_ADULT}
    minor = {"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}
    unknown = {"id": "student_unknown", "barn_id": "barn_a", "minor_status": MINOR_STATUS_UNKNOWN}
    under_13 = {"id": "student_under_13", "barn_id": "barn_a", "minor_status": MINOR_STATUS_UNDER_13}
    active_link = {
        "student_profile_id": "student_minor",
        "guardian_user_id": "guardian_1",
        "status": GUARDIAN_LINK_ACTIVE,
        "consent_status": CONSENT_GRANTED,
    }

    assert student_workflow_gate(adult, [], workflow=WORKFLOW_LESSON_READY)["decision"] == DECISION_ALLOW
    assert student_workflow_gate(minor, [], workflow=WORKFLOW_LESSON_READY)["decision"] == DECISION_REQUIRE_GUARDIAN
    assert student_workflow_gate(unknown, [], workflow=WORKFLOW_LESSON_READY)["decision"] == DECISION_REQUIRE_GUARDIAN
    assert student_workflow_gate(minor, [active_link], workflow=WORKFLOW_LESSON_READY)["decision"] == DECISION_ALLOW

    under_13_login = student_workflow_gate(under_13, [active_link], workflow=WORKFLOW_INDEPENDENT_LOGIN)
    assert under_13_login["decision"] == DECISION_PARENT_MANAGED_ONLY
    assert under_13_login["reason_code"] == "student_login_not_allowed"


def test_bn5d_communication_guard_launch_decision_matrix():
    legacy = minor_communication_gate(
        actor_user=_actor(),
        message={"subject": "Barn note", "body": "hello"},
        students=[],
        guardian_links=[],
    )
    blocked = minor_communication_gate(
        actor_user=_actor(),
        message={"student_profile_id": "student_minor", "to_user_id": "student_user"},
        students=[{"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}],
        guardian_links=[{"student_profile_id": "student_minor", "guardian_user_id": "guardian_1", "status": GUARDIAN_LINK_ACTIVE}],
    )
    allowed = minor_communication_gate(
        actor_user=_actor(),
        message={
            "student_profile_id": "student_minor",
            "to_user_id": "student_user",
            "guardian_user_ids": ["guardian_1"],
        },
        students=[{"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}],
        guardian_links=[{"student_profile_id": "student_minor", "guardian_user_id": "guardian_1", "status": GUARDIAN_LINK_ACTIVE}],
    )
    staff_only = minor_communication_gate(
        actor_user=_actor(),
        message={"student_profile_id": "student_minor", "participant_user_ids": ["staff_2"]},
        students=[{"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}],
        guardian_links=[{"student_profile_id": "student_minor", "guardian_user_id": "guardian_1", "status": GUARDIAN_LINK_ACTIVE}],
    )
    removal = minor_communication_gate(
        actor_user=_actor(),
        message={"guardian_user_ids": ["guardian_1"], "remove_user_id": "guardian_1"},
        students=[{"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}],
        guardian_links=[{"student_profile_id": "student_minor", "guardian_user_id": "guardian_1", "status": GUARDIAN_LINK_ACTIVE}],
        participants=["student_user", "guardian_1"],
        action=ACTION_REMOVE_PARTICIPANT,
    )

    assert legacy["decision"] == DECISION_ALLOW
    assert legacy["reason_code"] == REASON_NO_STUDENT
    assert blocked["decision"] == DECISION_REQUIRE_GUARDIAN
    assert blocked["reason_code"] == REASON_ACTIVE_GUARDIAN_REQUIRED
    assert allowed["decision"] == DECISION_ALLOW
    assert allowed["reason_code"] == REASON_ACTIVE_GUARDIAN_INCLUDED
    assert staff_only["decision"] == DECISION_REQUIRE_GUARDIAN
    assert removal["decision"] == DECISION_BLOCK
    assert removal["reason_code"] == REASON_LAST_GUARDIAN_REMOVAL_BLOCKED


def test_bn5d_privacy_projection_evidence_omits_forbidden_fields():
    student = {
        "id": "student_private",
        "barn_id": "barn_a",
        "display_name": "Private Student",
        "birthdate": "2014-01-01",
        "notes": "Sensitive staff-only details",
        "minor_status": MINOR_STATUS_UNDER_13,
    }
    gate = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)
    minor_metadata = audit_safe_minor_metadata(
        student=student,
        gate=gate,
        extra={
            "birthdate": "2014-01-01",
            "message_body": "hello minor",
            "consent_text": "guardian signs here",
            "password": "not-for-audit",
            "stripe_subscription_id": "sub_123",
        },
    )
    communication_metadata = audit_safe_minor_communication_metadata({
        "decision": DECISION_REQUIRE_GUARDIAN,
        "reason_code": REASON_ACTIVE_GUARDIAN_REQUIRED,
        "minor_involved": True,
        "student_profile_ids": ["student_private"],
        "required_guardian_user_ids": ["guardian_1"],
        "included_guardian_user_ids": [],
        "action": "create_message",
        "subject": "Private subject",
        "body": "Private body",
        "birthdate": "2014-01-01",
        "consent_text": "guardian signs here",
        "token": "secret-token",
    })
    message_response = message_response_projection({
        "_id": "mongo",
        "id": "msg_1",
        "subject": "Lesson update",
        "body": "Please review.",
        "student_profile_id": "student_private",
        "participant_user_ids": ["student_user", "guardian_1"],
        "guardian_user_ids": ["guardian_1"],
    })

    blob = f"{minor_metadata} {communication_metadata} {message_response}".lower()
    forbidden = [
        "private student",
        "2014",
        "sensitive",
        "hello minor",
        "guardian signs here",
        "not-for-audit",
        "sub_123",
        "private subject",
        "private body",
        "secret-token",
        "guardian_user_ids",
        "participant_user_ids",
    ]
    for value in forbidden:
        assert value not in blob
    assert "student_profile_id" not in message_response


def test_bn5d_guardian_invite_and_lesson_ready_source_evidence():
    assert 'STUDENT_MANAGER_ROLES = {"admin", "barn_manager", "trainer"}' in STUDENT_GUARDIANS_SRC
    assert '"$addToSet": {"intended_student_profile_ids": student_id}' in STUDENT_GUARDIANS_SRC
    assert '"token_hash": 0' in STUDENT_GUARDIANS_SRC
    assert '"existing_user_id": existing_user.get("id") if existing_user else None' in STUDENT_GUARDIANS_SRC
    assert "_user_has_barn_access(db, guardian_user_id, barn_id)" in STUDENT_GUARDIANS_SRC
    assert "_user_is_guardian_candidate(db, guardian_user_id, barn_id)" in STUDENT_GUARDIANS_SRC
    assert 'GUARDIAN_USER_ROLES = {"parent", "horse_owner"}' in STUDENT_GUARDIANS_SRC
    assert 'GUARDIAN_MEMBERSHIP_RELATIONSHIPS = {"parent", "owner"}' in STUDENT_GUARDIANS_SRC
    assert "db.users.insert_one" not in STUDENT_GUARDIANS_SRC.split("async def create_guardian_link", 1)[1]
    assert "db.users.update_one" not in STUDENT_GUARDIANS_SRC.split("async def create_guardian_link", 1)[1]
    assert 'status == "lesson_ready"' in STUDENT_GUARDIANS_SRC
    assert 'raise HTTPException(status_code=409, detail="Active guardian required")' in STUDENT_GUARDIANS_SRC


def test_bn5d_messages_route_keeps_bn5c_guard_and_response_projection():
    create_section = OPERATIONS_SRC.split('@router.post("/messages")', 1)[1].split("# ---------------- Service Requests", 1)[0]
    list_section = OPERATIONS_SRC.split('@router.get("/messages")', 1)[1].split('@router.post("/messages")', 1)[0]

    assert "message_minor_communication_gate" in create_section
    assert create_section.index("message_minor_communication_gate") < create_section.index("db.messages.insert_one")
    assert "minor_communication.blocked" in create_section
    assert "audit_safe_minor_communication_metadata" in create_section
    assert "message_response_projection(row)" in list_section
    assert "return message_response_projection(doc)" in create_section
