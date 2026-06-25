"""Build-Next-5A minor / parent safeguard rule contract.

Pure helpers only. This module does not create routes, mutate product records,
send messages, issue invites, or make legal claims. Later BN5 phases can call
these helpers from guardian/student onboarding and messaging surfaces.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Dict, Iterable, Optional


STUDENT_PROFILE_COLLECTION = "student_profiles"
GUARDIAN_LINK_COLLECTION = "guardian_links"

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
GUARDIAN_REQUIRED_WORKFLOWS = {
    WORKFLOW_LESSON_READY,
    WORKFLOW_MESSAGING,
    WORKFLOW_WAIVER,
    WORKFLOW_MEDIA_RELEASE,
    WORKFLOW_PAYMENT,
    WORKFLOW_EVENT_SIGNUP,
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
