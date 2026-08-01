"""Build-Next-5A minor / parent safeguard rule contract.

Pure helpers only. This module does not create routes, mutate product records,
send messages, issue invites, or make legal claims. Later BN5 phases can call
these helpers from guardian/student onboarding and messaging surfaces.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import json
from typing import Any, Dict, Iterable, Optional


STUDENT_PROFILE_COLLECTION = "student_profiles"
GUARDIAN_LINK_COLLECTION = "guardian_links"
GUARDIAN_WORKFLOW_CONSENT_COLLECTION = "guardian_workflow_consents"

MINOR_STATUS_ADULT = "adult"
MINOR_STATUS_MINOR_13_TO_17 = "minor_13_to_17"
MINOR_STATUS_UNDER_13 = "under_13"
MINOR_STATUS_UNKNOWN = "unknown"
MINOR_STATUSES = {
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
}

GUARDIAN_LINK_ACTIVE = "active"
GUARDIAN_LINK_PENDING = "pending"
GUARDIAN_LINK_REVOKED = "revoked"
GUARDIAN_LINK_STATUSES = {
    GUARDIAN_LINK_ACTIVE,
    GUARDIAN_LINK_PENDING,
    GUARDIAN_LINK_REVOKED,
}

CONSENT_NOT_REQUIRED = "not_required"
CONSENT_REQUIRED = "required"
CONSENT_GRANTED = "granted"
CONSENT_REVOKED = "revoked"
CONSENT_STATUSES = {
    CONSENT_NOT_REQUIRED,
    CONSENT_REQUIRED,
    CONSENT_GRANTED,
    CONSENT_REVOKED,
}

DECISION_ALLOW = "allow"
DECISION_BLOCK = "block"
DECISION_REQUIRE_GUARDIAN = "require_guardian"
DECISION_PARENT_MANAGED_ONLY = "parent_managed_only"
WORKFLOW_DECISIONS = {
    DECISION_ALLOW,
    DECISION_BLOCK,
    DECISION_REQUIRE_GUARDIAN,
    DECISION_PARENT_MANAGED_ONLY,
}

UNDER_13_POLICY_PARENT_MANAGED_ONLY = "parent_managed_only"

WORKFLOW_INDEPENDENT_LOGIN = "independent_login"
WORKFLOW_LESSON_READY = "lesson_ready"
WORKFLOW_MESSAGING = "messaging"
WORKFLOW_WAIVER = "waiver"
WORKFLOW_MEDIA_RELEASE = "media_release"
WORKFLOW_PAYMENT = "payment"
WORKFLOW_EVENT_SIGNUP = "event_signup"
WORKFLOW_STUDENT_PROFILE = "student_profile"
WORKFLOW_DOCUMENT_SIGNATURE = "document_signature"
WORKFLOW_GUARDIAN_LIFECYCLE = "guardian_lifecycle_and_participant_removal"
GUARDIAN_REQUIRED_WORKFLOWS = {
    WORKFLOW_LESSON_READY,
    WORKFLOW_MESSAGING,
    WORKFLOW_WAIVER,
    WORKFLOW_MEDIA_RELEASE,
    WORKFLOW_PAYMENT,
    WORKFLOW_EVENT_SIGNUP,
}

AUTHORITY_SCOPE_COMMUNICATION = "COMMUNICATION"
AUTHORITY_SCOPE_LESSON_PARTICIPATION = "LESSON_PARTICIPATION"
AUTHORITY_SCOPE_WAIVER = "WAIVER"
AUTHORITY_SCOPE_DOCUMENT_SIGNATURE = "DOCUMENT_SIGNATURE"
AUTHORITY_SCOPE_MEDIA_RELEASE = "MEDIA_RELEASE"
AUTHORITY_SCOPE_BILLING_PAYMENT = "BILLING_PAYMENT"
AUTHORITY_SCOPE_EVENT_SIGNUP = "EVENT_SIGNUP"
AUTHORITY_SCOPE_RELATIONSHIP_ADMINISTRATION = "RELATIONSHIP_ADMINISTRATION"
GUARDIAN_AUTHORITY_SCOPES = {
    AUTHORITY_SCOPE_COMMUNICATION,
    AUTHORITY_SCOPE_LESSON_PARTICIPATION,
    AUTHORITY_SCOPE_WAIVER,
    AUTHORITY_SCOPE_DOCUMENT_SIGNATURE,
    AUTHORITY_SCOPE_MEDIA_RELEASE,
    AUTHORITY_SCOPE_BILLING_PAYMENT,
    AUTHORITY_SCOPE_EVENT_SIGNUP,
    AUTHORITY_SCOPE_RELATIONSHIP_ADMINISTRATION,
}
WORKFLOW_AUTHORITY_SCOPES = {
    WORKFLOW_MESSAGING: AUTHORITY_SCOPE_COMMUNICATION,
    WORKFLOW_LESSON_READY: AUTHORITY_SCOPE_LESSON_PARTICIPATION,
    WORKFLOW_WAIVER: AUTHORITY_SCOPE_WAIVER,
    WORKFLOW_DOCUMENT_SIGNATURE: AUTHORITY_SCOPE_DOCUMENT_SIGNATURE,
    WORKFLOW_MEDIA_RELEASE: AUTHORITY_SCOPE_MEDIA_RELEASE,
    WORKFLOW_PAYMENT: AUTHORITY_SCOPE_BILLING_PAYMENT,
    WORKFLOW_EVENT_SIGNUP: AUTHORITY_SCOPE_EVENT_SIGNUP,
    WORKFLOW_GUARDIAN_LIFECYCLE: AUTHORITY_SCOPE_RELATIONSHIP_ADMINISTRATION,
}
WORKFLOW_CONSENT_REQUIRED = {
    WORKFLOW_LESSON_READY,
    WORKFLOW_WAIVER,
    WORKFLOW_DOCUMENT_SIGNATURE,
    WORKFLOW_MEDIA_RELEASE,
    WORKFLOW_PAYMENT,
    WORKFLOW_EVENT_SIGNUP,
}

PUBLIC_CODE_STUDENT_WORKFLOW_BLOCKED = "STUDENT_WORKFLOW_BLOCKED"
PUBLIC_CODE_COMMUNICATION_BLOCKED = "COMMUNICATION_BLOCKED"
PUBLIC_CODE_DOCUMENT_ACTION_BLOCKED = "DOCUMENT_ACTION_BLOCKED"
PUBLIC_CODE_PAYMENT_ACTION_BLOCKED = "PAYMENT_ACTION_BLOCKED"
PUBLIC_CODE_AUTHORIZATION_CHANGED_RETRY = "AUTHORIZATION_CHANGED_RETRY"

INTERNAL_MINOR_STATUS_UNKNOWN = "MINOR_STATUS_UNKNOWN"
INTERNAL_GUARDIAN_REQUIRED = "GUARDIAN_REQUIRED"
INTERNAL_GUARDIAN_LINK_PENDING = "GUARDIAN_LINK_PENDING"
INTERNAL_GUARDIAN_LINK_REVOKED = "GUARDIAN_LINK_REVOKED"
INTERNAL_GUARDIAN_LINK_EXPIRED = "GUARDIAN_LINK_EXPIRED"
INTERNAL_GUARDIAN_LINK_DISPUTED = "GUARDIAN_LINK_DISPUTED"
INTERNAL_GUARDIAN_LINK_SUSPENDED = "GUARDIAN_LINK_SUSPENDED"
INTERNAL_GUARDIAN_CROSS_BARN = "GUARDIAN_CROSS_BARN"
INTERNAL_GUARDIAN_AUTHORITY_SCOPE_MISSING = "GUARDIAN_AUTHORITY_SCOPE_MISSING"
INTERNAL_GUARDIAN_AUTHORITY_RESTRICTED = "GUARDIAN_AUTHORITY_RESTRICTED"
INTERNAL_WORKFLOW_CONSENT_REQUIRED = "WORKFLOW_CONSENT_REQUIRED"
INTERNAL_WORKFLOW_CONSENT_REVOKED = "WORKFLOW_CONSENT_REVOKED"
INTERNAL_WORKFLOW_CONSENT_EXPIRED = "WORKFLOW_CONSENT_EXPIRED"
INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH = "WORKFLOW_CONSENT_SCOPE_MISMATCH"
INTERNAL_WORKFLOW_POLICY_VERSION_STALE = "WORKFLOW_POLICY_VERSION_STALE"
INTERNAL_PRIVATE_ADULT_MINOR_COMMUNICATION_PROHIBITED = "PRIVATE_ADULT_MINOR_COMMUNICATION_PROHIBITED"
INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE = "PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE"
INTERNAL_LAST_GUARDIAN_REMOVAL_PROHIBITED = "LAST_GUARDIAN_REMOVAL_PROHIBITED"
INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED = "AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED"

_GUARDIAN_INVALID_STATUS_REASON = {
    "pending": INTERNAL_GUARDIAN_LINK_PENDING,
    "revoked": INTERNAL_GUARDIAN_LINK_REVOKED,
    "expired": INTERNAL_GUARDIAN_LINK_EXPIRED,
    "disputed": INTERNAL_GUARDIAN_LINK_DISPUTED,
    "suspended": INTERNAL_GUARDIAN_LINK_SUSPENDED,
}
_CONSENT_INVALID_STATUS_REASON = {
    "revoked": INTERNAL_WORKFLOW_CONSENT_REVOKED,
    "expired": INTERNAL_WORKFLOW_CONSENT_EXPIRED,
    "declined": INTERNAL_WORKFLOW_CONSENT_REQUIRED,
    "superseded": INTERNAL_WORKFLOW_POLICY_VERSION_STALE,
}
_GUARDIAN_MINOR_AUDIT_KEYS = {
    "workflow",
    "decision",
    "public_code",
    "internal_reason_code",
    "minor_involved",
    "student_profile_ids",
    "guardian_required_count",
    "qualifying_guardian_count",
    "consent_count",
    "state_token",
    "action",
}

_AUDIT_SAFE_FIELDS = {
    "student_profile_id",
    "barn_id",
    "minor_status",
    "workflow",
    "decision",
    "reason_code",
    "guardian_required",
    "active_guardian_count",
    "under_13_policy",
}
_MINOR_STATUS_RANK = {
    MINOR_STATUS_ADULT: 0,
    MINOR_STATUS_MINOR_13_TO_17: 1,
    MINOR_STATUS_UNDER_13: 2,
    MINOR_STATUS_UNKNOWN: 3,
}
_CANONICAL_AUDIT_FIELDS = {
    "student_profile_id",
    "barn_id",
    "minor_status",
    "workflow",
    "decision",
    "reason_code",
    "guardian_required",
    "active_guardian_count",
    "under_13_policy",
}


def _today_utc() -> date:
    return datetime.now(timezone.utc).date()


def _parse_birthdate(value: Any) -> Optional[date]:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def minor_status_from_birthdate(birthdate: Any, *, as_of: Optional[date] = None) -> str:
    """Classify a birthdate into the locked BN5-A age bands.

    Invalid or future dates are treated as `unknown`, which is intentionally
    conservative: unknown age requires a guardian for guarded workflows.
    """
    born = _parse_birthdate(birthdate)
    as_of = as_of or _today_utc()
    if not born or born > as_of:
        return MINOR_STATUS_UNKNOWN

    age = as_of.year - born.year - ((as_of.month, as_of.day) < (born.month, born.day))
    if age < 13:
        return MINOR_STATUS_UNDER_13
    if age < 18:
        return MINOR_STATUS_MINOR_13_TO_17
    return MINOR_STATUS_ADULT


def normalize_minor_status(value: Any) -> str:
    status = (value or "").strip().lower()
    return status if status in MINOR_STATUSES else MINOR_STATUS_UNKNOWN


def minor_status_for_student(student: Dict[str, Any], *, as_of: Optional[date] = None) -> str:
    explicit = normalize_minor_status(student.get("minor_status"))
    if student.get("birthdate"):
        from_birthdate = minor_status_from_birthdate(student.get("birthdate"), as_of=as_of)
        if explicit == MINOR_STATUS_UNKNOWN:
            return from_birthdate
        # Fail closed on conflicts: use the more restrictive classification so
        # a stale/manual `minor_status="adult"` cannot bypass a minor birthdate.
        return max(
            (explicit, from_birthdate),
            key=lambda status: _MINOR_STATUS_RANK.get(status, _MINOR_STATUS_RANK[MINOR_STATUS_UNKNOWN]),
        )
    if explicit != MINOR_STATUS_UNKNOWN:
        return explicit
    return MINOR_STATUS_UNKNOWN


def requires_guardian(minor_status: str) -> bool:
    """Return whether launch rules require a guardian for this status."""
    return normalize_minor_status(minor_status) in {
        MINOR_STATUS_MINOR_13_TO_17,
        MINOR_STATUS_UNDER_13,
        MINOR_STATUS_UNKNOWN,
    }


def can_create_independent_student_account(
    minor_status: str,
    *,
    under_13_policy: str = UNDER_13_POLICY_PARENT_MANAGED_ONLY,
) -> bool:
    """Return whether a direct student login is allowed by age policy alone.

    Guardian workflow requirements are enforced separately by
    `student_workflow_gate`. At launch, under-13 and unknown-age students cannot
    create independent accounts.
    """
    status = normalize_minor_status(minor_status)
    if status == MINOR_STATUS_UNDER_13 and under_13_policy == UNDER_13_POLICY_PARENT_MANAGED_ONLY:
        return False
    if status == MINOR_STATUS_UNKNOWN:
        return False
    return status in {MINOR_STATUS_ADULT, MINOR_STATUS_MINOR_13_TO_17}


def active_guardian_links(guardian_links: Iterable[Dict[str, Any]]) -> list[Dict[str, Any]]:
    return [
        link for link in guardian_links
        if (link.get("status") or "").strip().lower() == GUARDIAN_LINK_ACTIVE
    ]


def student_workflow_gate(
    student: Dict[str, Any],
    guardian_links: Iterable[Dict[str, Any]],
    *,
    workflow: str,
    as_of: Optional[date] = None,
    under_13_policy: str = UNDER_13_POLICY_PARENT_MANAGED_ONLY,
) -> Dict[str, Any]:
    """Return the locked BN5-A decision for a student workflow.

    This is intentionally data-only so future routes can enforce the same rule
    without duplicating policy branches in UI code.
    """
    status = minor_status_for_student(student, as_of=as_of)
    active_guardians = active_guardian_links(guardian_links)
    guardian_required = requires_guardian(status)

    if workflow == WORKFLOW_INDEPENDENT_LOGIN and not can_create_independent_student_account(
        status,
        under_13_policy=under_13_policy,
    ):
        decision = DECISION_PARENT_MANAGED_ONLY if status == MINOR_STATUS_UNDER_13 else DECISION_BLOCK
        reason = "student_login_not_allowed"
    elif workflow in GUARDIAN_REQUIRED_WORKFLOWS and guardian_required and not active_guardians:
        decision = DECISION_REQUIRE_GUARDIAN
        reason = "active_guardian_required"
    else:
        decision = DECISION_ALLOW
        reason = "ok"

    return {
        "decision": decision,
        "reason_code": reason,
        "minor_status": status,
        "workflow": workflow,
        "guardian_required": guardian_required,
        "active_guardian_count": len(active_guardians),
        "under_13_policy": under_13_policy,
        "student_profile_id": student.get("id"),
        "barn_id": student.get("barn_id"),
    }


def audit_safe_minor_metadata(
    *,
    student: Dict[str, Any],
    gate: Dict[str, Any],
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Project minor-safety metadata for audit rows.

    Only opaque ids, booleans, counts, status codes, and reason codes are
    allowed. Birthdates, names, notes, message bodies, consent text, and raw
    documents never cross this boundary.
    """
    out = {
        "student_profile_id": student.get("id") or gate.get("student_profile_id"),
        "barn_id": student.get("barn_id") or gate.get("barn_id"),
        "minor_status": normalize_minor_status(gate.get("minor_status")),
        "workflow": gate.get("workflow"),
        "decision": gate.get("decision"),
        "reason_code": gate.get("reason_code"),
        "guardian_required": bool(gate.get("guardian_required")),
        "active_guardian_count": int(gate.get("active_guardian_count") or 0),
        "under_13_policy": gate.get("under_13_policy") or UNDER_13_POLICY_PARENT_MANAGED_ONLY,
    }
    if extra:
        for key, value in extra.items():
            if key in _AUDIT_SAFE_FIELDS and key not in _CANONICAL_AUDIT_FIELDS:
                out[key] = value
    return {k: v for k, v in out.items() if v is not None}


def _clean_id_list(values: Optional[Iterable[Any]]) -> list[str]:
    out: list[str] = []
    for value in values or []:
        if value is None:
            continue
        text = str(value).strip()
        if text and text not in out:
            out.append(text)
    return out


def _clean_scope_set(values: Any) -> set[str]:
    if values is None:
        return set()
    if isinstance(values, str):
        values = [part.strip() for part in values.replace(",", " ").split()]
    return {str(value).strip().upper() for value in values or [] if str(value).strip()}


def _parse_instant(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc)
    if isinstance(value, str) and value.strip():
        raw = value.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError:
            try:
                d = date.fromisoformat(raw[:10])
            except ValueError:
                return None
            return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def _is_expired(value: Any, as_of: datetime) -> bool:
    instant = _parse_instant(value)
    return bool(instant and instant < as_of)


def _is_future(value: Any, as_of: datetime) -> bool:
    instant = _parse_instant(value)
    return bool(instant and instant > as_of)


def _workflow_scope(workflow: str) -> str:
    return WORKFLOW_AUTHORITY_SCOPES.get((workflow or "").strip().lower(), "")


def student_workflow_scope(student_profile_id: Any, workflow: str) -> str:
    student_id = str(student_profile_id or "").strip()
    workflow_key = (workflow or "").strip().lower()
    return f"student:{student_id}:workflow:{workflow_key}" if student_id and workflow_key else ""


def workflow_scope(workflow: str) -> str:
    workflow_key = (workflow or "").strip().lower()
    return f"workflow:{workflow_key}" if workflow_key else ""


def _consent_scope_matches(
    *,
    consent: Dict[str, Any],
    student_id: Any,
    workflow: str,
    scope_reference: Optional[str],
) -> bool:
    expected_scope = str(scope_reference or "").strip()
    actual_scope = str(consent.get("scope_reference") or "").strip()
    if not actual_scope:
        return False
    if expected_scope and actual_scope == expected_scope:
        return True
    student_scope = student_workflow_scope(student_id, workflow)
    if actual_scope == student_scope:
        return True
    if (consent.get("scope_level") or "").strip().lower() == "workflow" and actual_scope == workflow_scope(workflow):
        return True
    return False


def _legacy_link_barn_proven(link: Dict[str, Any], *, student: Dict[str, Any], barn_id: str) -> bool:
    student_barn = str(student.get("barn_id") or "").strip()
    active_barn = str(barn_id or "").strip()
    if not active_barn or student_barn != active_barn:
        return False
    if link.get("barn_id"):
        return str(link.get("barn_id")).strip() == active_barn
    if str(link.get("migration_verified_barn_id") or "").strip() == active_barn:
        return True
    if str(link.get("legacy_barn_id") or "").strip() == active_barn:
        return True
    return bool(link.get("barn_scope_verified") or link.get("legacy_barn_scope_verified"))


def _public_code_for_workflow(workflow: str, internal_reason: str) -> str:
    if internal_reason == INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED:
        return PUBLIC_CODE_AUTHORIZATION_CHANGED_RETRY
    if workflow == WORKFLOW_MESSAGING:
        return PUBLIC_CODE_COMMUNICATION_BLOCKED
    if workflow in {WORKFLOW_DOCUMENT_SIGNATURE, WORKFLOW_WAIVER, WORKFLOW_MEDIA_RELEASE}:
        return PUBLIC_CODE_DOCUMENT_ACTION_BLOCKED
    if workflow == WORKFLOW_PAYMENT:
        return PUBLIC_CODE_PAYMENT_ACTION_BLOCKED
    return PUBLIC_CODE_STUDENT_WORKFLOW_BLOCKED


def _state_token(
    *,
    students: list[Dict[str, Any]],
    guardian_links: list[Dict[str, Any]],
    workflow_consents: list[Dict[str, Any]],
    workflow: str,
    scope_reference: Optional[str],
    policy_version: Optional[str],
) -> str:
    rows = {
        "workflow": workflow,
        "scope_reference": scope_reference,
        "policy_version": policy_version,
        "students": [
            {
                "id": row.get("id"),
                "barn_id": row.get("barn_id"),
                "minor_status": minor_status_for_student(row),
                "birthdate": row.get("birthdate"),
                "updated_at": row.get("updated_at"),
                "guardian_safeguarding_version": row.get("guardian_safeguarding_version"),
            }
            for row in sorted(students, key=lambda item: str(item.get("id") or ""))
        ],
        "guardian_links": [
            {
                "id": row.get("id"),
                "barn_id": row.get("barn_id"),
                "student_profile_id": row.get("student_profile_id"),
                "guardian_user_id": row.get("guardian_user_id"),
                "status": row.get("status"),
                "authority_scopes": sorted(_clean_scope_set(row.get("authority_scopes"))),
                "restricted_scopes": sorted(_clean_scope_set(row.get("restricted_scopes"))),
                "restricted_workflows": sorted(_clean_id_list(row.get("restricted_workflows"))),
                "expires_at": row.get("expires_at"),
                "suspended_at": row.get("suspended_at"),
                "disputed": bool(row.get("disputed")),
                "updated_at": row.get("updated_at"),
                "version": row.get("version"),
            }
            for row in sorted(
                guardian_links,
                key=lambda item: (str(item.get("student_profile_id") or ""), str(item.get("guardian_user_id") or "")),
            )
        ],
        "workflow_consents": [
            {
                "id": row.get("id"),
                "barn_id": row.get("barn_id"),
                "student_profile_id": row.get("student_profile_id"),
                "guardian_user_id": row.get("guardian_user_id"),
                "workflow": row.get("workflow"),
                "status": row.get("status"),
                "scope_reference": row.get("scope_reference"),
                "policy_version": row.get("policy_version"),
                "effective_at": row.get("effective_at"),
                "expires_at": row.get("expires_at"),
                "revoked_at": row.get("revoked_at"),
                "updated_at": row.get("updated_at"),
                "version": row.get("version"),
            }
            for row in sorted(
                workflow_consents,
                key=lambda item: (
                    str(item.get("student_profile_id") or ""),
                    str(item.get("guardian_user_id") or ""),
                    str(item.get("workflow") or ""),
                    str(item.get("scope_reference") or ""),
                ),
            )
        ],
    }
    blob = json.dumps(rows, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _block_decision(
    *,
    workflow: str,
    reason: str,
    students: list[Dict[str, Any]],
    guardian_links: list[Dict[str, Any]],
    workflow_consents: list[Dict[str, Any]],
    scope_reference: Optional[str],
    policy_version: Optional[str],
    action: str,
) -> Dict[str, Any]:
    state_token = _state_token(
        students=students,
        guardian_links=guardian_links,
        workflow_consents=workflow_consents,
        workflow=workflow,
        scope_reference=scope_reference,
        policy_version=policy_version,
    )
    decision = DECISION_REQUIRE_GUARDIAN if reason in {
        INTERNAL_GUARDIAN_REQUIRED,
        INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE,
    } else DECISION_BLOCK
    return {
        "decision": decision,
        "workflow": workflow,
        "public_code": _public_code_for_workflow(workflow, reason),
        "internal_reason_code": reason,
        "minor_involved": True,
        "student_profile_ids": _clean_id_list([student.get("id") for student in students]),
        "guardian_required_count": len([student for student in students if requires_guardian(minor_status_for_student(student))]),
        "qualifying_guardian_user_ids": [],
        "consent_ids": [],
        "state_token": state_token,
        "action": action,
    }


def _allow_decision(
    *,
    workflow: str,
    students: list[Dict[str, Any]],
    guardian_links: list[Dict[str, Any]],
    workflow_consents: list[Dict[str, Any]],
    qualifying_guardian_user_ids: Iterable[Any],
    consent_ids: Iterable[Any],
    scope_reference: Optional[str],
    policy_version: Optional[str],
    action: str,
) -> Dict[str, Any]:
    student_ids = _clean_id_list([student.get("id") for student in students])
    guardian_required_count = len([student for student in students if requires_guardian(minor_status_for_student(student))])
    qualifying = _clean_id_list(qualifying_guardian_user_ids)
    consents = _clean_id_list(consent_ids)
    return {
        "decision": DECISION_ALLOW,
        "workflow": workflow,
        "public_code": "OK",
        "internal_reason_code": "OK",
        "minor_involved": guardian_required_count > 0,
        "student_profile_ids": student_ids,
        "guardian_required_count": guardian_required_count,
        "qualifying_guardian_user_ids": qualifying,
        "consent_ids": consents,
        "state_token": _state_token(
            students=students,
            guardian_links=guardian_links,
            workflow_consents=workflow_consents,
            workflow=workflow,
            scope_reference=scope_reference,
            policy_version=policy_version,
        ),
        "action": action,
    }


def _link_failure_reason(
    link: Dict[str, Any],
    *,
    student: Dict[str, Any],
    barn_id: str,
    workflow: str,
    required_scope: str,
    as_of: datetime,
) -> Optional[str]:
    if not _legacy_link_barn_proven(link, student=student, barn_id=barn_id):
        return INTERNAL_GUARDIAN_CROSS_BARN
    status = (link.get("status") or "").strip().lower()
    if status != GUARDIAN_LINK_ACTIVE:
        return _GUARDIAN_INVALID_STATUS_REASON.get(status, INTERNAL_GUARDIAN_REQUIRED)
    if _is_expired(link.get("expires_at"), as_of):
        return INTERNAL_GUARDIAN_LINK_EXPIRED
    if link.get("suspended_at") or bool(link.get("suspended")):
        return INTERNAL_GUARDIAN_LINK_SUSPENDED
    if bool(link.get("disputed")):
        return INTERNAL_GUARDIAN_LINK_DISPUTED
    restricted_scopes = _clean_scope_set(link.get("restricted_scopes"))
    restricted_workflows = {item.lower() for item in _clean_id_list(link.get("restricted_workflows"))}
    if required_scope in restricted_scopes or workflow in restricted_workflows:
        return INTERNAL_GUARDIAN_AUTHORITY_RESTRICTED
    scopes = _clean_scope_set(link.get("authority_scopes"))
    if required_scope and required_scope not in scopes:
        return INTERNAL_GUARDIAN_AUTHORITY_SCOPE_MISSING
    if not link.get("guardian_user_id"):
        return INTERNAL_GUARDIAN_REQUIRED
    return None


def _consent_failure_reason(
    consent: Dict[str, Any],
    *,
    student_id: Any,
    barn_id: str,
    workflow: str,
    scope_reference: Optional[str],
    policy_version: Optional[str],
    as_of: datetime,
) -> Optional[str]:
    if (consent.get("barn_id") or barn_id) != barn_id:
        return INTERNAL_GUARDIAN_CROSS_BARN
    if (consent.get("workflow") or "").strip().lower() != workflow:
        return INTERNAL_WORKFLOW_CONSENT_REQUIRED
    status = (consent.get("status") or "").strip().lower()
    if status != CONSENT_GRANTED:
        return _CONSENT_INVALID_STATUS_REASON.get(status, INTERNAL_WORKFLOW_CONSENT_REQUIRED)
    if consent.get("revoked_at"):
        return INTERNAL_WORKFLOW_CONSENT_REVOKED
    if _is_future(consent.get("effective_at"), as_of):
        return INTERNAL_WORKFLOW_CONSENT_REQUIRED
    if _is_expired(consent.get("expires_at"), as_of):
        return INTERNAL_WORKFLOW_CONSENT_EXPIRED
    if not _consent_scope_matches(
        consent=consent,
        student_id=student_id,
        workflow=workflow,
        scope_reference=scope_reference,
    ):
        return INTERNAL_WORKFLOW_CONSENT_SCOPE_MISMATCH
    expected_version = str(policy_version or "").strip()
    actual_version = str(consent.get("policy_version") or "").strip()
    if expected_version and actual_version != expected_version:
        return INTERNAL_WORKFLOW_POLICY_VERSION_STALE
    return None


def guardian_minor_workflow_gate(
    *,
    workflow: str,
    students: Iterable[Dict[str, Any]],
    guardian_links: Iterable[Dict[str, Any]],
    workflow_consents: Optional[Iterable[Dict[str, Any]]] = None,
    barn_id: Optional[str] = None,
    guardian_user_ids: Optional[Iterable[Any]] = None,
    participant_user_ids: Optional[Iterable[Any]] = None,
    scope_reference: Optional[str] = None,
    policy_version: Optional[str] = None,
    consent_required: Optional[bool] = None,
    require_guardian_participant: bool = False,
    action: str = "write",
    expected_state_token: Optional[str] = None,
    as_of: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Evaluate a guarded Guardian/Minor workflow from authoritative rows.

    This is the V1.1 server-side boundary used by routes. It deliberately
    separates relationship, authority scope, and workflow consent, fails closed
    on unknown/minor ambiguity, and returns only disclosure-safe public codes.
    """
    workflow_key = (workflow or "").strip().lower()
    required_scope = _workflow_scope(workflow_key)
    as_of = as_of or datetime.now(timezone.utc)
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=timezone.utc)
    student_rows = [dict(student) for student in students or []]
    link_rows = [dict(link) for link in guardian_links or []]
    consent_rows = [dict(consent) for consent in workflow_consents or []]
    scope_reference = str(scope_reference or "").strip() or None
    policy_version = str(policy_version or "").strip() or None
    active_barn_id = barn_id or next((student.get("barn_id") for student in student_rows if student.get("barn_id")), None)
    current_token = _state_token(
        students=student_rows,
        guardian_links=link_rows,
        workflow_consents=consent_rows,
        workflow=workflow_key,
        scope_reference=scope_reference,
        policy_version=policy_version,
    )
    if expected_state_token and expected_state_token != current_token:
        return _block_decision(
            workflow=workflow_key,
            reason=INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED,
            students=student_rows,
            guardian_links=link_rows,
            workflow_consents=consent_rows,
            scope_reference=scope_reference,
            policy_version=policy_version,
            action=action,
        )
    if not student_rows:
        return {
            "decision": DECISION_ALLOW,
            "workflow": workflow_key,
            "public_code": "OK",
            "internal_reason_code": "NO_MINOR_INVOLVED",
            "minor_involved": False,
            "student_profile_ids": [],
            "guardian_required_count": 0,
            "qualifying_guardian_user_ids": [],
            "consent_ids": [],
            "state_token": current_token,
            "action": action,
        }

    participant_ids = set(_clean_id_list(participant_user_ids))
    participant_ids |= set(_clean_id_list(guardian_user_ids))
    all_qualified: list[str] = []
    all_consents: list[str] = []
    consent_needed = workflow_key in WORKFLOW_CONSENT_REQUIRED if consent_required is None else bool(consent_required)

    for student in student_rows:
        if active_barn_id and student.get("barn_id") and student.get("barn_id") != active_barn_id:
            return _block_decision(
                workflow=workflow_key,
                reason=INTERNAL_GUARDIAN_CROSS_BARN,
                students=student_rows,
                guardian_links=link_rows,
                workflow_consents=consent_rows,
                scope_reference=scope_reference,
                policy_version=policy_version,
                action=action,
            )
        status = minor_status_for_student(student, as_of=as_of.date())
        if status == MINOR_STATUS_ADULT:
            continue
        if status == MINOR_STATUS_UNKNOWN:
            return _block_decision(
                workflow=workflow_key,
                reason=INTERNAL_MINOR_STATUS_UNKNOWN,
                students=student_rows,
                guardian_links=link_rows,
                workflow_consents=consent_rows,
                scope_reference=scope_reference,
                policy_version=policy_version,
                action=action,
            )

        student_id = student.get("id")
        student_links = [link for link in link_rows if link.get("student_profile_id") == student_id]
        if not student_links:
            return _block_decision(
                workflow=workflow_key,
                reason=INTERNAL_GUARDIAN_REQUIRED,
                students=student_rows,
                guardian_links=link_rows,
                workflow_consents=consent_rows,
                scope_reference=scope_reference,
                policy_version=policy_version,
                action=action,
            )
        qualified_links: list[Dict[str, Any]] = []
        first_failure = INTERNAL_GUARDIAN_REQUIRED
        for link in student_links:
            failure = _link_failure_reason(
                link,
                student=student,
                barn_id=active_barn_id or "",
                workflow=workflow_key,
                required_scope=required_scope,
                as_of=as_of,
            )
            if failure:
                first_failure = failure
                continue
            qualified_links.append(link)
        if not qualified_links:
            return _block_decision(
                workflow=workflow_key,
                reason=first_failure,
                students=student_rows,
                guardian_links=link_rows,
                workflow_consents=consent_rows,
                scope_reference=scope_reference,
                policy_version=policy_version,
                action=action,
            )
        if require_guardian_participant:
            qualified_links = [
                link for link in qualified_links
                if str(link.get("guardian_user_id") or "").strip() in participant_ids
            ]
            if not qualified_links:
                return _block_decision(
                    workflow=workflow_key,
                    reason=INTERNAL_PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE,
                    students=student_rows,
                    guardian_links=link_rows,
                    workflow_consents=consent_rows,
                    scope_reference=scope_reference,
                    policy_version=policy_version,
                    action=action,
                )

        qualified_ids = _clean_id_list([link.get("guardian_user_id") for link in qualified_links])
        all_qualified.extend(qualified_ids)
        if not consent_needed:
            continue

        matching_consent_ids: list[str] = []
        consent_failure = INTERNAL_WORKFLOW_CONSENT_REQUIRED
        for consent in consent_rows:
            if consent.get("student_profile_id") != student_id:
                continue
            if str(consent.get("guardian_user_id") or "").strip() not in qualified_ids:
                continue
            failure = _consent_failure_reason(
                consent,
                student_id=student_id,
                barn_id=active_barn_id or "",
                workflow=workflow_key,
                scope_reference=scope_reference,
                policy_version=policy_version,
                as_of=as_of,
            )
            if failure:
                consent_failure = failure
                continue
            matching_consent_ids.append(str(consent.get("id") or ""))
        if not matching_consent_ids:
            return _block_decision(
                workflow=workflow_key,
                reason=consent_failure,
                students=student_rows,
                guardian_links=link_rows,
                workflow_consents=consent_rows,
                scope_reference=scope_reference,
                policy_version=policy_version,
                action=action,
            )
        all_consents.extend(matching_consent_ids)

    return _allow_decision(
        workflow=workflow_key,
        students=student_rows,
        guardian_links=link_rows,
        workflow_consents=consent_rows,
        qualifying_guardian_user_ids=all_qualified,
        consent_ids=all_consents,
        scope_reference=scope_reference,
        policy_version=policy_version,
        action=action,
    )


def audit_safe_guardian_minor_metadata(gate: Dict[str, Any]) -> Dict[str, Any]:
    """Project the V1.1 guard result without names, birthdates, bodies, or legal text."""
    out = {
        "workflow": gate.get("workflow"),
        "decision": gate.get("decision"),
        "public_code": gate.get("public_code"),
        "internal_reason_code": gate.get("internal_reason_code"),
        "minor_involved": bool(gate.get("minor_involved")),
        "student_profile_ids": _clean_id_list(gate.get("student_profile_ids")),
        "guardian_required_count": int(gate.get("guardian_required_count") or 0),
        "qualifying_guardian_count": len(_clean_id_list(gate.get("qualifying_guardian_user_ids"))),
        "consent_count": len(_clean_id_list(gate.get("consent_ids"))),
        "state_token": gate.get("state_token"),
        "action": gate.get("action"),
    }
    return {key: value for key, value in out.items() if key in _GUARDIAN_MINOR_AUDIT_KEYS and value is not None}


def guardian_minor_public_error_detail(gate: Dict[str, Any]) -> Dict[str, str]:
    """Return a stable, disclosure-safe API detail for a blocked guarded action."""
    code = gate.get("public_code") or PUBLIC_CODE_STUDENT_WORKFLOW_BLOCKED
    message = "Guardian or consent setup is required before this action can be completed."
    if code == PUBLIC_CODE_AUTHORIZATION_CHANGED_RETRY:
        message = "Authorization changed. Refresh and try again."
    return {"code": code, "message": message}


async def load_guardian_minor_authority_rows(
    db,
    *,
    barn_id: str,
    student_profile_ids: Iterable[Any],
    workflow: str,
) -> tuple[list[Dict[str, Any]], list[Dict[str, Any]]]:
    """Load relationship/consent rows for the central guard without caching."""
    links: list[Dict[str, Any]] = []
    consents: list[Dict[str, Any]] = []
    workflow_key = (workflow or "").strip().lower()
    for student_id in _clean_id_list(student_profile_ids):
        found_links = await db[GUARDIAN_LINK_COLLECTION].find(
            {
                "student_profile_id": student_id,
                "$or": [
                    {"barn_id": barn_id},
                    {"barn_id": None},
                    {"barn_id": {"$exists": False}},
                ],
            },
            {"_id": 0},
        ).to_list(100)
        links.extend(found_links)
        found_consents = await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].find(
            {"barn_id": barn_id, "student_profile_id": student_id, "workflow": workflow_key},
            {"_id": 0},
        ).to_list(100)
        consents.extend(found_consents)
    return links, consents


async def ensure_minor_safety_indexes(db) -> None:
    """Create additive indexes for future BN5 student/guardian collections."""
    await db[STUDENT_PROFILE_COLLECTION].create_index("id", unique=True, name="sp_id_unique")
    await db[STUDENT_PROFILE_COLLECTION].create_index(
        [("barn_id", 1), ("status", 1)],
        name="sp_barn_status",
    )
    await db[STUDENT_PROFILE_COLLECTION].create_index(
        [("barn_id", 1), ("minor_status", 1), ("status", 1)],
        name="sp_barn_minor_status",
    )
    await db[GUARDIAN_LINK_COLLECTION].create_index("id", unique=True, name="gl_id_unique")
    await db[GUARDIAN_LINK_COLLECTION].create_index(
        [("student_profile_id", 1), ("status", 1)],
        name="gl_student_status",
    )
    await db[GUARDIAN_LINK_COLLECTION].create_index(
        [("guardian_user_id", 1), ("status", 1)],
        name="gl_guardian_status",
    )
    await db[GUARDIAN_LINK_COLLECTION].create_index(
        [("barn_id", 1), ("student_profile_id", 1), ("status", 1)],
        name="gl_barn_student_status",
    )


async def ensure_guardian_minor_safeguarding_indexes(db) -> None:
    """Create additive V1.1 Guardian/Minor authority and consent indexes."""
    await db[GUARDIAN_LINK_COLLECTION].create_index(
        [("barn_id", 1), ("student_profile_id", 1), ("guardian_user_id", 1), ("status", 1)],
        name="gl_v11_barn_student_guardian_status",
    )
    await db[GUARDIAN_LINK_COLLECTION].create_index(
        [("barn_id", 1), ("guardian_user_id", 1), ("status", 1)],
        name="gl_v11_barn_guardian_status",
    )
    await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].create_index("id", unique=True, name="gwc_id_unique")
    await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].create_index(
        [("barn_id", 1), ("student_profile_id", 1), ("workflow", 1), ("status", 1)],
        name="gwc_barn_student_workflow_status",
    )
    await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].create_index(
        [("barn_id", 1), ("guardian_user_id", 1), ("workflow", 1), ("status", 1)],
        name="gwc_barn_guardian_workflow_status",
    )
