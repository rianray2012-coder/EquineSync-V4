"""Build-Next-5C server-side minor communication guard tests."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict

from core.minor_communication import (
    ACTION_REMOVE_PARTICIPANT,
    REASON_ACTIVE_GUARDIAN_INCLUDED,
    REASON_ACTIVE_GUARDIAN_REQUIRED,
    REASON_LAST_GUARDIAN_REMOVAL_BLOCKED,
    REASON_NO_STUDENT,
    audit_safe_minor_communication_metadata,
    message_minor_communication_gate,
    message_response_projection,
    minor_communication_gate,
)
from core.minor_safety import DECISION_ALLOW, DECISION_BLOCK, DECISION_REQUIRE_GUARDIAN


ROOT = Path(__file__).resolve().parents[2]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, _limit):
        return [dict(row) for row in self.rows]


def _match(doc: Dict[str, Any], filt: Dict[str, Any]) -> bool:
    for key, value in filt.items():
        if doc.get(key) != value:
            return False
    return True


def _project(doc: Dict[str, Any], projection):
    out = dict(doc)
    for key, keep in (projection or {}).items():
        if keep == 0:
            out.pop(key, None)
    return out


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])

    async def find_one(self, filt, projection=None):
        for row in self.rows:
            if _match(row, filt):
                return _project(row, projection)
        return None

    def find(self, filt, projection=None):
        return FakeCursor([_project(row, projection) for row in self.rows if _match(row, filt)])


class FakeDb:
    def __init__(self, *, students=None, guardian_links=None):
        self.student_profiles = FakeCollection(students or [])
        self.guardian_links = FakeCollection(guardian_links or [])

    def __getitem__(self, name):
        return getattr(self, name)


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _actor():
    return {"id": "staff_1", "role": "trainer", "barn_id": "barn_a"}


def test_legacy_message_with_no_student_reference_allows():
    gate = asyncio.run(message_minor_communication_gate(
        db=FakeDb(),
        actor_user=_actor(),
        message={"subject": "Barn note", "body": "Hello", "to_user_id": "u_2"},
    ))

    assert gate["decision"] == DECISION_ALLOW
    assert gate["reason_code"] == REASON_NO_STUDENT
    assert gate["minor_involved"] is False


def test_direct_minor_message_without_guardian_is_blocked():
    db = FakeDb(students=[{
        "id": "student_1",
        "barn_id": "barn_a",
        "minor_status": "minor_13_to_17",
    }])

    gate = asyncio.run(message_minor_communication_gate(
        db=db,
        actor_user=_actor(),
        message={"student_profile_id": "student_1", "to_user_id": "student_user_1"},
    ))

    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN
    assert gate["reason_code"] == REASON_ACTIVE_GUARDIAN_REQUIRED
    assert gate["minor_involved"] is True


def test_unknown_age_student_is_guarded_like_minor():
    db = FakeDb(students=[{
        "id": "student_unknown",
        "barn_id": "barn_a",
        "minor_status": "unknown",
    }])

    gate = asyncio.run(message_minor_communication_gate(
        db=db,
        actor_user=_actor(),
        message={"student_profile_id": "student_unknown", "to_user_id": "student_user_1"},
    ))

    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN
    assert gate["reason_code"] == REASON_ACTIVE_GUARDIAN_REQUIRED


def test_minor_message_with_active_guardian_included_allows():
    db = FakeDb(
        students=[{"id": "student_1", "barn_id": "barn_a", "minor_status": "under_13"}],
        guardian_links=[{
            "id": "gl_1",
            "barn_id": "barn_a",
            "student_profile_id": "student_1",
            "guardian_user_id": "guardian_1",
            "status": "active",
        }],
    )

    gate = asyncio.run(message_minor_communication_gate(
        db=db,
        actor_user=_actor(),
        message={
            "student_profile_id": "student_1",
            "to_user_id": "student_user_1",
            "guardian_user_ids": ["guardian_1"],
        },
    ))

    assert gate["decision"] == DECISION_ALLOW
    assert gate["reason_code"] == REASON_ACTIVE_GUARDIAN_INCLUDED
    assert gate["included_guardian_user_ids"] == ["guardian_1"]


def test_staff_only_participant_does_not_satisfy_guardian_requirement():
    db = FakeDb(
        students=[{"id": "student_1", "barn_id": "barn_a", "minor_status": "minor_13_to_17"}],
        guardian_links=[{
            "id": "gl_1",
            "barn_id": "barn_a",
            "student_profile_id": "student_1",
            "guardian_user_id": "guardian_1",
            "status": "active",
        }],
    )

    gate = asyncio.run(message_minor_communication_gate(
        db=db,
        actor_user=_actor(),
        message={
            "student_profile_id": "student_1",
            "to_user_id": "student_user_1",
            "participant_user_ids": ["staff_2"],
        },
    ))

    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN
    assert gate["included_guardian_user_ids"] == []


def test_cross_barn_student_reference_fails_closed():
    db = FakeDb(students=[{"id": "student_1", "barn_id": "barn_b", "minor_status": "adult"}])

    gate = asyncio.run(message_minor_communication_gate(
        db=db,
        actor_user=_actor(),
        message={"student_profile_id": "student_1", "to_user_id": "student_user_1"},
    ))

    assert gate["decision"] == DECISION_BLOCK
    assert gate["reason_code"] == "student_profile_not_found"


def test_removing_last_guardian_from_minor_context_blocks():
    gate = minor_communication_gate(
        actor_user=_actor(),
        message={"guardian_user_ids": ["guardian_1"], "remove_user_id": "guardian_1"},
        students=[{"id": "student_1", "barn_id": "barn_a", "minor_status": "minor_13_to_17"}],
        guardian_links=[{
            "student_profile_id": "student_1",
            "guardian_user_id": "guardian_1",
            "status": "active",
        }],
        participants=["student_user_1", "guardian_1"],
        action=ACTION_REMOVE_PARTICIPANT,
    )

    assert gate["decision"] == DECISION_BLOCK
    assert gate["reason_code"] == REASON_LAST_GUARDIAN_REMOVAL_BLOCKED


def test_audit_metadata_omits_message_and_minor_private_fields():
    gate = {
        "decision": DECISION_REQUIRE_GUARDIAN,
        "reason_code": REASON_ACTIVE_GUARDIAN_REQUIRED,
        "minor_involved": True,
        "student_profile_ids": ["student_1"],
        "required_guardian_user_ids": ["guardian_1"],
        "included_guardian_user_ids": [],
        "action": "create_message",
        "subject": "Secret subject",
        "body": "Secret message",
        "birthdate": "2014-01-01",
        "notes": "private notes",
        "token": "raw-token",
        "consent_text": "signed by parent",
    }

    metadata = audit_safe_minor_communication_metadata(gate)
    blob = str(metadata).lower()

    assert metadata == {
        "decision": DECISION_REQUIRE_GUARDIAN,
        "reason_code": REASON_ACTIVE_GUARDIAN_REQUIRED,
        "minor_involved": True,
        "student_profile_ids": ["student_1"],
        "required_guardian_count": 1,
        "included_guardian_count": 0,
        "action": "create_message",
    }
    assert "secret" not in blob
    assert "2014" not in blob
    assert "private notes" not in blob
    assert "raw-token" not in blob
    assert "signed by parent" not in blob


def test_message_response_omits_minor_guardian_linkage_fields():
    doc = {
        "_id": "mongo-row",
        "id": "msg_1",
        "subject": "Lesson update",
        "body": "Please review.",
        "visibility": "parent_visible",
        "student_profile_id": "student_1",
        "participant_user_ids": ["student_user_1", "guardian_1"],
        "guardian_user_ids": ["guardian_1"],
    }

    projected = message_response_projection(doc)

    assert projected == {
        "id": "msg_1",
        "subject": "Lesson update",
        "body": "Please review.",
        "visibility": "parent_visible",
    }
    assert "student_profile_id" not in projected
    assert "participant_user_ids" not in projected
    assert "guardian_user_ids" not in projected


def test_messages_route_calls_guard_before_insert_and_adds_no_new_message_routes():
    src = _read("backend/routes/operations.py")
    create_section = src.split('@router.post("/messages")', 1)[1].split("# ---------------- Service Requests", 1)[0]
    list_section = src.split('@router.get("/messages")', 1)[1].split('@router.post("/messages")', 1)[0]
    router_lines = [line.strip() for line in src.splitlines() if "@router." in line and "message" in line.lower()]

    assert "message_response_projection(row)" in list_section
    assert "message_minor_communication_gate" in create_section
    assert create_section.index("message_minor_communication_gate") < create_section.index("db.messages.insert_one")
    assert "minor_communication.blocked" in create_section
    assert "audit_safe_minor_communication_metadata" in create_section
    assert "return message_response_projection(doc)" in create_section
    assert router_lines == ['@router.get("/messages")', '@router.post("/messages")']
