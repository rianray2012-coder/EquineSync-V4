"""CGP-006 IWP-0002 Guardian/Minor safeguarding V1.1 regression matrix."""
from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict

from core.minor_communication import (
    ACTION_REMOVE_PARTICIPANT,
    REASON_LAST_GUARDIAN_REMOVAL_BLOCKED,
    message_guardian_minor_safeguarding_gate,
    minor_communication_gate,
)
from core.minor_safety import (
    AUTHORITY_SCOPE_BILLING_PAYMENT,
    AUTHORITY_SCOPE_COMMUNICATION,
    AUTHORITY_SCOPE_DOCUMENT_SIGNATURE,
    AUTHORITY_SCOPE_EVENT_SIGNUP,
    AUTHORITY_SCOPE_LESSON_PARTICIPATION,
    AUTHORITY_SCOPE_MEDIA_RELEASE,
    AUTHORITY_SCOPE_WAIVER,
    CONSENT_GRANTED,
    DECISION_ALLOW,
    DECISION_BLOCK,
    DECISION_PARENT_MANAGED_ONLY,
    DECISION_REQUIRE_GUARDIAN,
    GUARDIAN_LINK_ACTIVE,
    GUARDIAN_LINK_COLLECTION,
    GUARDIAN_WORKFLOW_CONSENT_COLLECTION,
    INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED,
    INTERNAL_GUARDIAN_AUTHORITY_RESTRICTED,
    INTERNAL_GUARDIAN_AUTHORITY_SCOPE_MISSING,
    INTERNAL_GUARDIAN_CROSS_BARN,
    INTERNAL_GUARDIAN_LINK_DISPUTED,
    INTERNAL_GUARDIAN_LINK_EXPIRED,
    INTERNAL_GUARDIAN_LINK_PENDING,
    INTERNAL_GUARDIAN_LINK_REVOKED,
    INTERNAL_GUARDIAN_LINK_SUSPENDED,
    INTERNAL_GUARDIAN_REQUIRED,
    INTERNAL_MINOR_STATUS_UNKNOWN,
    INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE,
    INTERNAL_WORKFLOW_CONSENT_REQUIRED,
    INTERNAL_WORKFLOW_CONSENT_REVOKED,
    INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH,
    INTERNAL_WORKFLOW_POLICY_VERSION_STALE,
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_DOCUMENT_SIGNATURE,
    WORKFLOW_EVENT_SIGNUP,
    WORKFLOW_INDEPENDENT_LOGIN,
    WORKFLOW_LESSON_READY,
    WORKFLOW_MEDIA_RELEASE,
    WORKFLOW_MESSAGING,
    WORKFLOW_PAYMENT,
    WORKFLOW_WAIVER,
    audit_safe_guardian_minor_metadata,
    guardian_minor_public_error_detail,
    guardian_minor_workflow_gate,
    minor_status_from_birthdate,
    minor_status_for_student,
    student_workflow_gate,
)


ROOT = Path(__file__).resolve().parents[2]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, _limit):
        return [dict(row) for row in self.rows]


def _matches(row: Dict[str, Any], filt: Dict[str, Any]) -> bool:
    for key, value in (filt or {}).items():
        if isinstance(value, dict) and "$in" in value:
            if row.get(key) not in value["$in"]:
                return False
        elif row.get(key) != value:
            return False
    return True


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])

    async def find_one(self, filt, projection=None):
        for row in self.rows:
            if _matches(row, filt):
                return dict(row)
        return None

    def find(self, filt, projection=None):
        return FakeCursor([row for row in self.rows if _matches(row, filt)])


class FakeDb:
    def __init__(self, *, students=None, links=None, consents=None):
        self.student_profiles = FakeCollection(students or [])
        self.guardian_links = FakeCollection(links or [])
        self.guardian_workflow_consents = FakeCollection(consents or [])

    def __getitem__(self, name):
        if name == STUDENT_PROFILE_COLLECTION:
            return self.student_profiles
        if name == GUARDIAN_LINK_COLLECTION:
            return self.guardian_links
        if name == GUARDIAN_WORKFLOW_CONSENT_COLLECTION:
            return self.guardian_workflow_consents
        raise AssertionError(name)


def _student(student_id="student_1", *, status=MINOR_STATUS_MINOR_13_TO_17, barn="barn_a", **extra):
    row = {"id": student_id, "barn_id": barn, "minor_status": status}
    row.update(extra)
    return row


def _link(
    student_id="student_1",
    guardian_id="guardian_1",
    *,
    status=GUARDIAN_LINK_ACTIVE,
    scopes=None,
    barn="barn_a",
    **extra,
):
    row = {
        "id": f"link_{student_id}_{guardian_id}",
        "barn_id": barn,
        "student_profile_id": student_id,
        "guardian_user_id": guardian_id,
        "status": status,
        "authority_scopes": scopes or [AUTHORITY_SCOPE_LESSON_PARTICIPATION],
        "version": 1,
    }
    row.update(extra)
    return row


def _consent(
    workflow=WORKFLOW_LESSON_READY,
    student_id="student_1",
    guardian_id="guardian_1",
    *,
    scope="scope:ok",
    policy="policy-v1",
    status=CONSENT_GRANTED,
    barn="barn_a",
    **extra,
):
    row = {
        "id": f"consent_{workflow}_{student_id}_{guardian_id}",
        "barn_id": barn,
        "student_profile_id": student_id,
        "guardian_user_id": guardian_id,
        "workflow": workflow,
        "scope_reference": scope,
        "policy_version": policy,
        "status": status,
        "version": 1,
    }
    row.update(extra)
    return row


def _gate(workflow, students, links, consents=None, **kwargs):
    return guardian_minor_workflow_gate(
        workflow=workflow,
        students=students,
        guardian_links=links,
        workflow_consents=consents or [],
        barn_id=kwargs.pop("barn_id", "barn_a"),
        scope_reference=kwargs.pop("scope", "scope:ok"),
        policy_version=kwargs.pop("policy", "policy-v1"),
        **kwargs,
    )


def _valid_guard(workflow, scope, student_id="student_1", guardian_id="guardian_1"):
    scope_by_workflow = {
        WORKFLOW_LESSON_READY: AUTHORITY_SCOPE_LESSON_PARTICIPATION,
        WORKFLOW_WAIVER: AUTHORITY_SCOPE_WAIVER,
        WORKFLOW_DOCUMENT_SIGNATURE: AUTHORITY_SCOPE_DOCUMENT_SIGNATURE,
        WORKFLOW_MEDIA_RELEASE: AUTHORITY_SCOPE_MEDIA_RELEASE,
        WORKFLOW_PAYMENT: AUTHORITY_SCOPE_BILLING_PAYMENT,
        WORKFLOW_EVENT_SIGNUP: AUTHORITY_SCOPE_EVENT_SIGNUP,
        WORKFLOW_MESSAGING: AUTHORITY_SCOPE_COMMUNICATION,
    }
    return (
        [_student(student_id)],
        [_link(student_id, guardian_id, scopes=[scope_by_workflow[workflow]])],
        [] if workflow == WORKFLOW_MESSAGING else [_consent(workflow, student_id, guardian_id, scope=scope)],
    )


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_gms_t_001_unknown_age_fails_closed_for_guarded_action():
    gate = _gate(WORKFLOW_LESSON_READY, [_student(status=MINOR_STATUS_UNKNOWN)], [], [])
    assert gate["decision"] == DECISION_BLOCK
    assert gate["internal_reason_code"] == INTERNAL_MINOR_STATUS_UNKNOWN


def test_gms_t_002_contradictory_age_uses_restrictive_minor_classification():
    status = minor_status_for_student({"minor_status": MINOR_STATUS_ADULT, "birthdate": "2014-01-01"}, as_of=date(2026, 7, 31))
    gate = _gate(WORKFLOW_LESSON_READY, [_student(status=status)], [], [])
    assert status == MINOR_STATUS_UNDER_13
    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN


def test_gms_t_003_birthday_transition_to_13_is_deterministic():
    assert minor_status_from_birthdate("2013-08-01", as_of=date(2026, 7, 31)) == MINOR_STATUS_UNDER_13
    assert minor_status_from_birthdate("2013-08-01", as_of=date(2026, 8, 1)) == MINOR_STATUS_MINOR_13_TO_17


def test_gms_t_004_birthday_transition_to_18_is_deterministic():
    assert minor_status_from_birthdate("2008-08-01", as_of=date(2026, 7, 31)) == MINOR_STATUS_MINOR_13_TO_17
    assert minor_status_from_birthdate("2008-08-01", as_of=date(2026, 8, 1)) == MINOR_STATUS_ADULT


def test_gms_t_005_minor_lesson_without_guardian_denies():
    gate = _gate(WORKFLOW_LESSON_READY, [_student()], [], [])
    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_REQUIRED


def test_gms_t_006_pending_guardian_link_denies():
    gate = _gate(WORKFLOW_LESSON_READY, [_student()], [_link(status="pending")], [])
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_LINK_PENDING


def test_gms_t_007_revoked_expired_disputed_suspended_guardians_deny():
    expired = datetime.now(timezone.utc) - timedelta(days=1)
    cases = [
        (_link(status="revoked"), INTERNAL_GUARDIAN_LINK_REVOKED),
        (_link(status="expired"), INTERNAL_GUARDIAN_LINK_EXPIRED),
        (_link(disputed=True), INTERNAL_GUARDIAN_LINK_DISPUTED),
        (_link(status="suspended"), INTERNAL_GUARDIAN_LINK_SUSPENDED),
        (_link(expires_at=expired.isoformat()), INTERNAL_GUARDIAN_LINK_EXPIRED),
    ]
    for link, reason in cases:
        assert _gate(WORKFLOW_LESSON_READY, [_student()], [link], [])["internal_reason_code"] == reason


def test_gms_t_008_cross_barn_guardian_denies_without_leaking():
    gate = _gate(WORKFLOW_LESSON_READY, [_student()], [_link(barn="barn_b")], [])
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_CROSS_BARN
    assert "CROSS_BARN" not in guardian_minor_public_error_detail(gate)["message"]


def test_gms_t_009_relationship_without_workflow_authority_denies():
    gate = _gate(WORKFLOW_PAYMENT, [_student()], [_link(scopes=[AUTHORITY_SCOPE_COMMUNICATION])], [])
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_AUTHORITY_SCOPE_MISSING


def test_gms_t_010_restricted_authority_denies():
    gate = _gate(
        WORKFLOW_PAYMENT,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_BILLING_PAYMENT], restricted_scopes=[AUTHORITY_SCOPE_BILLING_PAYMENT])],
        [],
    )
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_AUTHORITY_RESTRICTED


def test_gms_t_011_under_13_independent_access_parent_managed_only():
    gate = student_workflow_gate(_student(status=MINOR_STATUS_UNDER_13), [], workflow=WORKFLOW_INDEPENDENT_LOGIN)
    assert gate["decision"] == DECISION_PARENT_MANAGED_ONLY


def test_gms_t_012_lesson_requires_workflow_consent_not_just_guardian():
    gate = _gate(WORKFLOW_LESSON_READY, [_student()], [_link(scopes=[AUTHORITY_SCOPE_LESSON_PARTICIPATION])], [])
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REQUIRED


def test_gms_t_013_lesson_valid_guardian_authority_and_consent_allows():
    students, links, consents = _valid_guard(WORKFLOW_LESSON_READY, "scope:ok")
    assert _gate(WORKFLOW_LESSON_READY, students, links, consents)["decision"] == DECISION_ALLOW


def test_gms_t_014_message_omitted_student_id_derives_minor_from_recipient():
    db = FakeDb(
        students=[_student(user_id="minor_user")],
        links=[_link(scopes=[AUTHORITY_SCOPE_COMMUNICATION])],
    )
    gate = asyncio.run(message_guardian_minor_safeguarding_gate(
        db=db,
        actor_user={"id": "adult_user", "barn_id": "barn_a"},
        message={"to_user_id": "minor_user", "body": "hi"},
    ))
    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN
    assert gate["internal_reason_code"] == INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE


def test_gms_t_015_multi_minor_requires_coverage_for_each_minor():
    students = [_student("student_1"), _student("student_2")]
    links = [
        _link("student_1", "guardian_1", scopes=[AUTHORITY_SCOPE_COMMUNICATION]),
        _link("student_2", "guardian_2", scopes=[AUTHORITY_SCOPE_COMMUNICATION]),
    ]
    gate = _gate(
        WORKFLOW_MESSAGING,
        students,
        links,
        [],
        participant_user_ids=["guardian_1", "student_user_1", "student_user_2"],
        consent_required=False,
        require_guardian_participant=True,
    )
    assert gate["internal_reason_code"] == INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE


def test_gms_t_016_multi_minor_with_each_guardian_participant_allows():
    students = [_student("student_1"), _student("student_2")]
    links = [
        _link("student_1", "guardian_1", scopes=[AUTHORITY_SCOPE_COMMUNICATION]),
        _link("student_2", "guardian_2", scopes=[AUTHORITY_SCOPE_COMMUNICATION]),
    ]
    gate = _gate(
        WORKFLOW_MESSAGING,
        students,
        links,
        [],
        participant_user_ids=["guardian_1", "guardian_2", "student_user_1", "student_user_2"],
        consent_required=False,
        require_guardian_participant=True,
    )
    assert gate["decision"] == DECISION_ALLOW


def test_gms_t_017_guardian_not_in_thread_does_not_count_for_messaging():
    students, links, _consents = _valid_guard(WORKFLOW_MESSAGING, "thread:1")
    gate = _gate(
        WORKFLOW_MESSAGING,
        students,
        links,
        [],
        participant_user_ids=["adult_user", "minor_user"],
        consent_required=False,
        require_guardian_participant=True,
    )
    assert gate["decision"] == DECISION_REQUIRE_GUARDIAN


def test_gms_t_018_last_guardian_participant_removal_blocks():
    gate = minor_communication_gate(
        actor_user={"id": "staff_1"},
        message={"guardian_user_ids": ["guardian_1"], "remove_user_id": "guardian_1"},
        students=[_student()],
        guardian_links=[_link(scopes=[AUTHORITY_SCOPE_COMMUNICATION])],
        participants=["minor_user", "guardian_1"],
        action=ACTION_REMOVE_PARTICIPANT,
    )
    assert gate["decision"] == DECISION_BLOCK
    assert gate["reason_code"] == REASON_LAST_GUARDIAN_REMOVAL_BLOCKED


def test_gms_t_019_relationship_revocation_succeeds_then_future_workflows_block():
    active = _gate(WORKFLOW_MESSAGING, [_student()], [_link(scopes=[AUTHORITY_SCOPE_COMMUNICATION])], [], consent_required=False)
    revoked = _gate(WORKFLOW_MESSAGING, [_student()], [_link(status="revoked", scopes=[AUTHORITY_SCOPE_COMMUNICATION])], [], consent_required=False)
    route_src = _read("backend/routes/student_guardians.py")
    assert active["decision"] == DECISION_ALLOW
    assert revoked["internal_reason_code"] == INTERNAL_GUARDIAN_LINK_REVOKED
    assert '@router.post("/{student_id}/guardian-links/{link_id}/revoke")' in route_src


def test_gms_t_020_atomic_replacement_preserves_minor_message_coverage():
    students = [_student()]
    links = [_link(guardian_id="guardian_2", scopes=[AUTHORITY_SCOPE_COMMUNICATION])]
    gate = _gate(
        WORKFLOW_MESSAGING,
        students,
        links,
        [],
        participant_user_ids=["minor_user", "guardian_2"],
        consent_required=False,
        require_guardian_participant=True,
        action="participant.replace_guardian",
    )
    assert gate["decision"] == DECISION_ALLOW


def test_gms_t_021_revoked_guardian_blocks_existing_thread_send():
    gate = _gate(
        WORKFLOW_MESSAGING,
        [_student()],
        [_link(status="revoked", scopes=[AUTHORITY_SCOPE_COMMUNICATION])],
        [],
        participant_user_ids=["minor_user", "guardian_1"],
        consent_required=False,
        require_guardian_participant=True,
    )
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_LINK_REVOKED


def test_gms_t_022_waiver_requires_separate_workflow_consent():
    gate = _gate(WORKFLOW_WAIVER, [_student()], [_link(scopes=[AUTHORITY_SCOPE_WAIVER])], [])
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REQUIRED


def test_gms_t_023_stale_waiver_policy_version_denies():
    gate = _gate(
        WORKFLOW_WAIVER,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_WAIVER])],
        [_consent(WORKFLOW_WAIVER, scope="scope:ok", policy="old-v1")],
        policy="new-v2",
    )
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_POLICY_VERSION_STALE


def test_gms_t_024_waiver_wrong_scope_denies():
    gate = _gate(
        WORKFLOW_WAIVER,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_WAIVER])],
        [_consent(WORKFLOW_WAIVER, scope="lesson:other")],
        scope="lesson:target",
    )
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH


def test_gms_t_025_current_scoped_waiver_consent_allows():
    students, links, consents = _valid_guard(WORKFLOW_WAIVER, "waiver:lesson:1")
    assert _gate(WORKFLOW_WAIVER, students, links, consents, scope="waiver:lesson:1")["decision"] == DECISION_ALLOW


def test_gms_t_026_document_signature_without_specific_consent_denies():
    gate = _gate(WORKFLOW_DOCUMENT_SIGNATURE, [_student()], [_link(scopes=[AUTHORITY_SCOPE_DOCUMENT_SIGNATURE])], [])
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REQUIRED


def test_gms_t_027_current_document_signature_consent_allows_without_provider_call():
    students, links, consents = _valid_guard(WORKFLOW_DOCUMENT_SIGNATURE, "document_template:tmpl:v2")
    route_src = _read("backend/routes/document_signatures.py")
    sandbox_section = route_src.split("async def create_request_sandbox_envelope", 1)[1].split(
        '@router.post("/document-signatures/docusign/webhook")',
        1,
    )[0]
    gate = _gate(WORKFLOW_DOCUMENT_SIGNATURE, students, links, consents, scope="document_template:tmpl:v2")
    assert gate["decision"] == DECISION_ALLOW
    assert sandbox_section.index("_enforce_document_guard") < sandbox_section.index("create_docusign_sandbox_envelope")


def test_gms_t_028_replay_or_stale_state_token_denies_retry_required():
    students, links, consents = _valid_guard(WORKFLOW_DOCUMENT_SIGNATURE, "document_request:req_1")
    gate = _gate(
        WORKFLOW_DOCUMENT_SIGNATURE,
        students,
        links,
        consents,
        scope="document_request:req_1",
        expected_state_token="stale-token",
    )
    assert gate["internal_reason_code"] == INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED


def test_gms_t_029_media_revoked_or_wrong_purpose_denies():
    revoked = _gate(
        WORKFLOW_MEDIA_RELEASE,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_MEDIA_RELEASE])],
        [_consent(WORKFLOW_MEDIA_RELEASE, scope="media:purpose:1", status="revoked")],
        scope="media:purpose:1",
    )
    mismatch = _gate(
        WORKFLOW_MEDIA_RELEASE,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_MEDIA_RELEASE])],
        [_consent(WORKFLOW_MEDIA_RELEASE, scope="media:private")],
        scope="media:marketing",
    )
    assert revoked["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REVOKED
    assert mismatch["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH


def test_gms_t_030_minor_payment_defaults_to_denied_without_billing_consent():
    gate = _gate(WORKFLOW_PAYMENT, [_student()], [_link(scopes=[AUTHORITY_SCOPE_BILLING_PAYMENT])], [])
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REQUIRED


def test_gms_t_031_payment_outside_approved_scope_denies():
    gate = _gate(
        WORKFLOW_PAYMENT,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_BILLING_PAYMENT])],
        [_consent(WORKFLOW_PAYMENT, scope="invoice:small")],
        scope="invoice:large",
    )
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH


def test_gms_t_032_event_signup_missing_event_consent_denies():
    gate = _gate(WORKFLOW_EVENT_SIGNUP, [_student()], [_link(scopes=[AUTHORITY_SCOPE_EVENT_SIGNUP])], [])
    assert gate["internal_reason_code"] == INTERNAL_WORKFLOW_CONSENT_REQUIRED


def test_gms_t_033_legacy_guardian_link_without_authority_or_consent_denies():
    legacy_link = _link(scopes=[])
    gate = _gate(WORKFLOW_PAYMENT, [_student()], [legacy_link], [])
    assert gate["internal_reason_code"] == INTERNAL_GUARDIAN_AUTHORITY_SCOPE_MISSING


def test_gms_t_034_concurrent_revocation_detected_by_version_token():
    students, active_links, consents = _valid_guard(WORKFLOW_LESSON_READY, "scope:ok")
    token = _gate(WORKFLOW_LESSON_READY, students, active_links, consents)["state_token"]
    revoked = [_link(status="revoked", scopes=[AUTHORITY_SCOPE_LESSON_PARTICIPATION])]
    gate = _gate(WORKFLOW_LESSON_READY, students, revoked, consents, expected_state_token=token)
    assert gate["internal_reason_code"] == INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED


def test_gms_t_035_message_send_cannot_race_after_last_guardian_removed():
    gate = _gate(
        WORKFLOW_MESSAGING,
        [_student()],
        [_link(scopes=[AUTHORITY_SCOPE_COMMUNICATION])],
        [],
        participant_user_ids=["minor_user"],
        consent_required=False,
        require_guardian_participant=True,
        action="message.create_after_removal",
    )
    assert gate["internal_reason_code"] == INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE


def test_gms_t_036_stale_cache_token_after_revocation_denies():
    students, links, consents = _valid_guard(WORKFLOW_MESSAGING, "thread:1")
    token = _gate(WORKFLOW_MESSAGING, students, links, consents, consent_required=False)["state_token"]
    revoked = [_link(status="revoked", scopes=[AUTHORITY_SCOPE_COMMUNICATION])]
    gate = _gate(WORKFLOW_MESSAGING, students, revoked, consents, consent_required=False, expected_state_token=token)
    assert gate["internal_reason_code"] == INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED


def test_gms_t_037_public_error_minimizes_relationship_state_detail():
    gate = _gate(WORKFLOW_LESSON_READY, [_student()], [_link(status="disputed")], [])
    public = guardian_minor_public_error_detail(gate)
    assert public["code"] == "STUDENT_WORKFLOW_BLOCKED"
    assert "disputed" not in str(public).lower()
    assert "custody" not in str(public).lower()


def test_gms_t_038_audit_metadata_excludes_private_minor_content():
    students, links, consents = _valid_guard(WORKFLOW_PAYMENT, "invoice:1")
    gate = _gate(WORKFLOW_PAYMENT, students, links, consents, scope="invoice:1")
    gate.update({
        "birthdate": "2014-01-01",
        "body": "private message",
        "consent_text": "legal text",
        "payment_detail": "card",
    })
    metadata = audit_safe_guardian_minor_metadata(gate)
    blob = str(metadata).lower()
    for forbidden in ("2014", "private message", "legal text", "card"):
        assert forbidden not in blob


def test_gms_t_039_alternate_sinks_call_central_guard_before_write():
    operations = _read("backend/routes/operations.py")
    billing = _read("backend/routes/billing.py")
    recurring = _read("backend/routes/recurring_charges.py")
    documents = _read("backend/routes/document_signatures.py")
    assert operations.index("_enforce_guarded_students") < operations.index("db.lessons.insert_one")
    assert operations.index("message_guardian_minor_safeguarding_gate") < operations.index("db.messages.insert_one")
    assert billing.index("_enforce_payment_guard") < billing.index("db.invoices.insert_one")
    assert recurring.index("_payment_gate") < recurring.index("db.recurring_charges.insert_one")
    assert recurring.index('action="recurring_charge.update"') < recurring.index("db.recurring_charges.update_one(scope")
    assert recurring.index('action="recurring_charge.materialize"') < recurring.index("db.invoices.insert_one(doc)")
    assert documents.index("_enforce_document_guard") < documents.index("database[DOCUMENT_REQUESTS_COLLECTION].insert_one")


def test_gms_t_040_no_implicit_emergency_override_exists():
    gate = _gate(WORKFLOW_EVENT_SIGNUP, [_student()], [_link(scopes=[AUTHORITY_SCOPE_EVENT_SIGNUP])], [], action="emergency_override")
    src = _read("backend/core/minor_safety.py").lower()
    assert gate["decision"] == DECISION_BLOCK
    assert "emergency_override_allow" not in src


def test_gms_t_041_adult_supported_workflow_remains_allowed():
    gate = _gate(WORKFLOW_PAYMENT, [_student(status=MINOR_STATUS_ADULT)], [], [])
    assert gate["decision"] == DECISION_ALLOW
    assert gate["minor_involved"] is False


def test_gms_t_042_ui_is_disclosure_safe_and_server_remains_controlling():
    forms = _read("frontend/src/pages/FormsSignatures.jsx")
    student_guardians = _read("backend/routes/student_guardians.py")
    assert "custody" not in forms.lower()
    assert "dispute" not in forms.lower()
    assert "guardian_minor_public_error_detail" in student_guardians


def test_gms_t_043_unrelated_adult_to_adult_message_remains_allowed():
    gate = asyncio.run(message_guardian_minor_safeguarding_gate(
        db=FakeDb(),
        actor_user={"id": "adult_1", "barn_id": "barn_a"},
        message={"to_user_id": "adult_2", "body": "barn update"},
    ))
    assert gate["decision"] == DECISION_ALLOW
    assert gate["minor_involved"] is False
