"""Build-Next-5B guardian/student invite foundation source guards."""
from __future__ import annotations

from pathlib import Path

from core.minor_safety import (
    CONSENT_GRANTED,
    DECISION_ALLOW,
    DECISION_REQUIRE_GUARDIAN,
    GUARDIAN_LINK_ACTIVE,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    WORKFLOW_LESSON_READY,
    audit_safe_minor_metadata,
    student_workflow_gate,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


ROUTE_SRC = _read("backend/routes/student_guardians.py")
SERVER_SRC = _read("backend/server.py")


def _function_section(name: str) -> str:
    marker = f"async def {name}"
    assert marker in ROUTE_SRC
    tail = ROUTE_SRC.split(marker, 1)[1]
    next_def = tail.find("\n    @router.")
    return tail if next_def < 0 else tail[:next_def]


def test_bn5b_router_is_wired_under_active_facility_gate():
    assert "from routes.student_guardians import build_router as build_student_guardians_router" in SERVER_SRC
    assert "build_student_guardians_router(" in SERVER_SRC
    include_section = SERVER_SRC.split("Build-Next-5B", 1)[1].split("# Horses", 1)[0]
    assert "dependencies=PRODUCT_FACILITY_DEPS" in include_section


def test_student_profile_create_uses_bn5a_minor_status_and_safe_audit():
    section = _function_section("create_student_profile")

    assert "minor_status_for_student(doc)" in section
    assert "student_profile.created" in section
    assert "WORKFLOW_LESSON_READY" in section
    assert "audit_safe_minor_metadata" in ROUTE_SRC
    assert "display_name" in section
    assert "notes" in section
    assert "metadata={\"display_name\"" not in section
    assert "metadata={\"notes\"" not in section


def test_student_manager_roles_are_narrow_and_include_trainer():
    assert 'STUDENT_MANAGER_ROLES = {"admin", "barn_manager", "trainer"}' in ROUTE_SRC
    assert "def _require_student_manager" in ROUTE_SRC
    assert 'raise HTTPException(status_code=403, detail="Permission denied")' in ROUTE_SRC
    assert "_require_student_manager(user)" in _function_section("create_student_profile")
    assert "_require_student_manager(user)" in _function_section("create_guardian_invite")
    assert "_require_student_manager(user)" in _function_section("create_guardian_link")
    assert "_require_student_manager(user)" in _function_section("patch_student_status")


def test_guardian_invite_reuses_pending_invites_and_does_not_return_token_hash():
    section = _function_section("create_guardian_invite")

    assert '"status": "pending"' in section
    assert '"role": GUARDIAN_INVITE_ROLE' in section
    assert '"$addToSet": {"intended_student_profile_ids": student_id}' in section
    assert '"token_hash": 0' in section
    assert 'out["dev_accept_url"]' in section
    assert '"existing_user_id": existing_user.get("id") if existing_user else None' in section


def test_existing_guardian_link_path_checks_membership_without_duplicate_user_creation():
    helper = ROUTE_SRC.split("async def _user_has_barn_access", 1)[1].split("async def _audit_minor_event", 1)[0]
    section = _function_section("create_guardian_link")

    assert "db.users.find_one" in helper
    assert "db.account_memberships.find_one" in helper
    assert "membership_status" in helper
    assert "_user_has_barn_access(db, guardian_user_id, barn_id)" in section
    assert "db.users.insert_one" not in section
    assert "db.users.update_one" not in section
    assert '"status": GUARDIAN_LINK_ACTIVE' in section
    assert '"consent_status": CONSENT_GRANTED' in section


def test_guardian_link_requires_guardian_safe_role_or_membership():
    helper = ROUTE_SRC.split("async def _user_is_guardian_candidate", 1)[1].split("async def _audit_minor_event", 1)[0]
    section = _function_section("create_guardian_link")

    assert 'GUARDIAN_USER_ROLES = {"parent", "horse_owner"}' in ROUTE_SRC
    assert 'GUARDIAN_MEMBERSHIP_RELATIONSHIPS = {"parent", "owner"}' in ROUTE_SRC
    assert "user_role in GUARDIAN_USER_ROLES" in helper
    assert '"relationship_type": {"$in": sorted(GUARDIAN_MEMBERSHIP_RELATIONSHIPS)}' in helper
    assert "_user_is_guardian_candidate(db, guardian_user_id, barn_id)" in section
    assert 'raise HTTPException(status_code=403, detail="Guardian user is not eligible")' in section


def test_revoked_or_unaccepted_invites_cannot_activate_guardian_link():
    section = _function_section("create_guardian_link")

    assert 'inv.get("role") != GUARDIAN_INVITE_ROLE' in section
    assert 'inv.get("status") != "accepted"' in section
    assert 'raise HTTPException(status_code=409, detail="Guardian invite is not accepted")' in section
    assert 'student_id not in (inv.get("intended_student_profile_ids") or [])' in section


def test_guardian_invite_marks_pending_but_active_link_does_not():
    invite_section = _function_section("create_guardian_invite")
    link_section = _function_section("create_guardian_link")

    assert '"status": "guardian_pending"' in invite_section
    assert '"status": "guardian_pending"' not in link_section


def test_lesson_ready_status_is_backend_gated_by_active_guardian():
    section = _function_section("patch_student_status")

    assert 'status == "lesson_ready"' in section
    assert "student_workflow_gate(student, links, workflow=WORKFLOW_LESSON_READY)" in section
    assert 'gate["decision"] != "allow"' in section
    assert 'raise HTTPException(status_code=409, detail="Active guardian required")' in section
    assert "student_profile.status_blocked" in section
    assert "student_profile.status_changed" in section


def test_bn5a_gate_contract_allows_lesson_ready_only_after_active_guardian():
    student = {"id": "student_1", "barn_id": "barn_a", "minor_status": MINOR_STATUS_MINOR_13_TO_17}
    blocked = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)
    allowed = student_workflow_gate(
        student,
        [{"status": GUARDIAN_LINK_ACTIVE, "consent_status": CONSENT_GRANTED, "guardian_user_id": "guardian_1"}],
        workflow=WORKFLOW_LESSON_READY,
    )

    assert blocked["decision"] == DECISION_REQUIRE_GUARDIAN
    assert allowed["decision"] == DECISION_ALLOW


def test_audit_metadata_contract_omits_private_minor_fields():
    student = {
        "id": "student_private",
        "barn_id": "barn_a",
        "display_name": "Private Student",
        "birthdate": "2014-01-01",
        "notes": "Sensitive staff-only details",
        "minor_status": MINOR_STATUS_UNDER_13,
    }
    gate = student_workflow_gate(student, [], workflow=WORKFLOW_LESSON_READY)
    metadata = audit_safe_minor_metadata(
        student=student,
        gate=gate,
        extra={
            "birthdate": "2014-01-01",
            "notes": "Sensitive staff-only details",
            "message_body": "hello minor",
            "consent_text": "guardian signs here",
        },
    )
    blob = str(metadata).lower()

    assert "private student" not in blob
    assert "2014" not in blob
    assert "sensitive" not in blob
    assert "hello minor" not in blob
    assert "guardian signs here" not in blob


def test_bn5b_does_not_add_forbidden_workflow_routes():
    lowered = ROUTE_SRC.lower()
    router_lines = "\n".join(line.strip().lower() for line in ROUTE_SRC.splitlines() if "@router." in line)

    for forbidden in ("/messages", "/waivers", "/payments", "/documents"):
        assert forbidden not in router_lines
    for forbidden in ("stripe", "apple", "phase 16", "service worker", "push notification"):
        assert forbidden not in lowered
