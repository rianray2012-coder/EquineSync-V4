"""Build-Next-5A minor / parent safeguard rule-contract tests."""
from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path

from core.minor_safety import (
    CONSENT_GRANTED,
    DECISION_ALLOW,
    DECISION_BLOCK,
    DECISION_PARENT_MANAGED_ONLY,
    DECISION_REQUIRE_GUARDIAN,
    GUARDIAN_LINK_ACTIVE,
    GUARDIAN_LINK_COLLECTION,
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_EVENT_SIGNUP,
    WORKFLOW_INDEPENDENT_LOGIN,
    WORKFLOW_LESSON_READY,
    audit_safe_minor_metadata,
    can_create_independent_student_account,
    ensure_minor_safety_indexes,
    minor_status_from_birthdate,
    minor_status_for_student,
    requires_guardian,
    student_workflow_gate,
)


ROOT = Path(__file__).resolve().parents[2]


class FakeCollection:
    def __init__(self):
        self.indexes = []

    async def create_index(self, *args, **kwargs):
        self.indexes.append((args, kwargs))


class FakeDb:
    def __init__(self):
        self.student_profiles = FakeCollection()
        self.guardian_links = FakeCollection()

    def __getitem__(self, name):
        if name == STUDENT_PROFILE_COLLECTION:
            return self.student_profiles
        if name == GUARDIAN_LINK_COLLECTION:
            return self.guardian_links
        raise AssertionError(name)


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_birthdate_age_bands_are_deterministic():
    as_of = date(2026, 6, 22)

    assert minor_status_from_birthdate("2010-06-21", as_of=as_of) == MINOR_STATUS_MINOR_13_TO_17
    assert minor_status_from_birthdate("2008-06-22", as_of=as_of) == MINOR_STATUS_ADULT
    assert minor_status_from_birthdate("2014-06-23", as_of=as_of) == MINOR_STATUS_UNDER_13
    assert minor_status_from_birthdate("bad-date", as_of=as_of) == MINOR_STATUS_UNKNOWN
    assert minor_status_from_birthdate("2999-01-01", as_of=as_of) == MINOR_STATUS_UNKNOWN


def test_guardian_requirement_is_conservative_for_unknown_age():
    assert requires_guardian(MINOR_STATUS_ADULT) is False
    assert requires_guardian(MINOR_STATUS_MINOR_13_TO_17) is True
    assert requires_guardian(MINOR_STATUS_UNDER_13) is True
    assert requires_guardian(MINOR_STATUS_UNKNOWN) is True


def test_birthdate_conflict_uses_more_restrictive_minor_status():
    as_of = date(2026, 6, 22)

    adult_label_under_13_birthdate = minor_status_for_student(
        {"minor_status": MINOR_STATUS_ADULT, "birthdate": "2014-01-01"},
        as_of=as_of,
    )
    adult_label_minor_birthdate = minor_status_for_student(
        {"minor_status": MINOR_STATUS_ADULT, "birthdate": "2010-01-01"},
        as_of=as_of,
    )
    minor_label_adult_birthdate = minor_status_for_student(
        {"minor_status": MINOR_STATUS_MINOR_13_TO_17, "birthdate": "1990-01-01"},
        as_of=as_of,
    )

    assert adult_label_under_13_birthdate == MINOR_STATUS_UNDER_13
    assert adult_label_minor_birthdate == MINOR_STATUS_MINOR_13_TO_17
    assert minor_label_adult_birthdate == MINOR_STATUS_MINOR_13_TO_17


def test_under_13_independent_login_is_parent_managed_only():
    student = {"id": "student_under_13", "barn_id": "barn_a", "minor_status": MINOR_STATUS_UNDER_13}

    gate = student_workflow_gate(student, [], workflow=WORKFLOW_INDEPENDENT_LOGIN)

    assert can_create_independent_student_account(MINOR_STATUS_UNDER_13) is False
    assert gate["decision"] == DECISION_PARENT_MANAGED_ONLY
    assert gate["reason_code"] == "student_login_not_allowed"


def test_unknown_age_independent_login_blocks_fail_closed():
    student = {"id": "student_unknown", "barn_id": "barn_a", "minor_status": MINOR_STATUS_UNKNOWN}

    gate = student_workflow_gate(student, [], workflow=WORKFLOW_INDEPENDENT_LOGIN)

    assert can_create_independent_student_account(MINOR_STATUS_UNKNOWN) is False
    assert gate["decision"] == DECISION_BLOCK
    assert gate["reason_code"] == "student_login_not_allowed"


def test_minor_lesson_ready_requires_active_guardian():
    student = {"id": "student_minor", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}

    missing = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)
    active = student_workflow_gate(
        student,
        [{"guardian_user_id": "guardian_1", "status": GUARDIAN_LINK_ACTIVE, "consent_status": CONSENT_GRANTED}],
        workflow=WORKFLOW_LESSON_READY,
    )

    assert missing["decision"] == DECISION_REQUIRE_GUARDIAN
    assert missing["active_guardian_count"] == 0
    assert active["decision"] == DECISION_ALLOW
    assert active["active_guardian_count"] == 1


def test_adult_event_signup_allowed_without_guardian():
    student = {"id": "student_adult", "barn_id": "barn_a", "minor_status": MINOR_STATUS_ADULT}

    gate = student_workflow_gate(student, [], workflow=WORKFLOW_EVENT_SIGNUP)

    assert gate["decision"] == DECISION_ALLOW
    assert gate["guardian_required"] is False


def test_audit_safe_metadata_omits_private_minor_fields():
    student = {
        "id": "student_private",
        "barn_id": "barn_a",
        "display_name": "Private Student",
        "birthdate": "2014-01-01",
        "notes": "Sensitive notes",
    }
    gate = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)

    metadata = audit_safe_minor_metadata(
        student=student,
        gate=gate,
        extra={
            "message_body": "raw message",
            "birthdate": "2014-01-01",
            "consent_text": "signed by parent",
            "active_guardian_count": 0,
        },
    )

    blob = str(metadata).lower()
    assert metadata == {
        "student_profile_id": "student_private",
        "barn_id": "barn_a",
        "minor_status": MINOR_STATUS_UNDER_13,
        "workflow": WORKFLOW_LESSON_READY,
        "decision": DECISION_REQUIRE_GUARDIAN,
        "reason_code": "active_guardian_required",
        "guardian_required": True,
        "active_guardian_count": 0,
        "under_13_policy": "parent_managed_only",
    }
    assert "private student" not in blob
    assert "2014" not in blob
    assert "sensitive" not in blob
    assert "raw message" not in blob
    assert "signed by parent" not in blob


def test_audit_extra_cannot_override_canonical_gate_fields():
    student = {"id": "student_private", "barn_id": "barn_a", "minor_status": MINOR_STATUS_UNDER_13}
    gate = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)

    metadata = audit_safe_minor_metadata(
        student=student,
        gate=gate,
        extra={
            "decision": DECISION_ALLOW,
            "minor_status": MINOR_STATUS_ADULT,
            "reason_code": "caller_override",
            "active_guardian_count": 99,
        },
    )

    assert metadata["decision"] == DECISION_REQUIRE_GUARDIAN
    assert metadata["minor_status"] == MINOR_STATUS_UNDER_13
    assert metadata["reason_code"] == "active_guardian_required"
    assert metadata["active_guardian_count"] == 0


def test_minor_safety_indexes_are_additive_and_named():
    db = FakeDb()

    asyncio.run(ensure_minor_safety_indexes(db))

    student_index_names = {kwargs["name"] for _args, kwargs in db.student_profiles.indexes}
    guardian_index_names = {kwargs["name"] for _args, kwargs in db.guardian_links.indexes}

    assert student_index_names == {
        "sp_id_unique",
        "sp_barn_status",
        "sp_barn_minor_status",
    }
    assert guardian_index_names == {
        "gl_id_unique",
        "gl_student_status",
        "gl_guardian_status",
        "gl_barn_student_status",
    }
    student_id_index = [kwargs for _args, kwargs in db.student_profiles.indexes
                        if kwargs["name"] == "sp_id_unique"][0]
    guardian_id_index = [kwargs for _args, kwargs in db.guardian_links.indexes
                         if kwargs["name"] == "gl_id_unique"][0]
    assert student_id_index["unique"] is True
    assert guardian_id_index["unique"] is True


def test_bn5a_lifespan_wires_index_foundation_only():
    src = _read("backend/core/lifespan.py")

    assert "ensure_minor_safety_indexes" in src
    assert "Build-Next-5A minor safety index foundation failed" in src
    assert "build_student" not in src.lower()
