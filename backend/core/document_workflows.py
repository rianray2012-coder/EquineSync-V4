"""Document workflow contract helpers for Build-Next-6B.

This module is intentionally pure: no database writes, no provider calls, no
DocuSign SDK usage, no signed-document storage, and no participation gates.
It defines the launch contract that a later implementation phase can wire into
routes after founder/legal approval.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

from core.document_signing import PROVIDER_DOCUSIGN
from core.minor_safety import (
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    normalize_minor_status,
    requires_guardian,
)


DOCUMENT_TEMPLATES_COLLECTION = "document_templates"
DOCUMENT_REQUESTS_COLLECTION = "document_requests"
DOCUMENT_SIGNATURES_COLLECTION = "document_signatures"
DOCUMENT_ACKNOWLEDGEMENTS_COLLECTION = "document_acknowledgements"

WORKFLOW_PROVIDER_SIGNATURE = "provider_signature"
WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT = "in_house_acknowledgement"
WORKFLOW_KINDS = {
    WORKFLOW_PROVIDER_SIGNATURE,
    WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
}

PROVIDER_NONE = "none"
PROVIDER_STATUS_TO_LOCAL_STATUS = {
    "created": "draft",
    "sent": "sent",
    "delivered": "viewed",
    "completed": "completed",
    "declined": "declined",
    "voided": "voided",
    "expired": "expired",
}
LOCAL_DOCUMENT_REQUEST_STATUSES = {
    "draft",
    "sent",
    "viewed",
    "completed",
    "declined",
    "voided",
    "expired",
    "provider_attention",
}

LAUNCH_BEHAVIOR_SOFT_WARNING = "soft_warning"
LAUNCH_BEHAVIOR_DEFERRED = "deferred"
LAUNCH_BEHAVIORS = {
    LAUNCH_BEHAVIOR_SOFT_WARNING,
    LAUNCH_BEHAVIOR_DEFERRED,
}

SIGNER_SUBJECT = "subject"
SIGNER_GUARDIAN = "guardian"
SIGNER_FACILITY_COUNTERSIGNER = "facility_countersigner"
SIGNER_PLATFORM_COUNTERSIGNER = "platform_countersigner"
SIGNER_ROLES = {
    SIGNER_SUBJECT,
    SIGNER_GUARDIAN,
    SIGNER_FACILITY_COUNTERSIGNER,
    SIGNER_PLATFORM_COUNTERSIGNER,
}

LEGAL_DOCUMENT_TYPES = (
    "general_liability_waiver",
    "minor_participant_liability_waiver",
    "media_photo_release",
    "emergency_vet_authorization",
    "lesson_program_agreement",
    "boarding_facility_services_agreement",
    "trainer_service_provider_agreement",
)

ACKNOWLEDGEMENT_DOCUMENT_TYPES = (
    "arena_facility_rules_acknowledgement",
    "community_program_acknowledgement",
    "onboarding_policy_acknowledgement",
)

DOCUMENT_TYPE_MATRIX: Dict[str, Dict[str, Any]] = {
    "general_liability_waiver": {
        "display_name": "General liability waiver",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility", "trainer", "individual_owner"],
        "required_for_roles": ["horse_owner", "parent", "rider", "trainer"],
        "required_for_workflows": ["lesson_ready", "event_signup", "arena_use"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "minor_participant_liability_waiver": {
        "display_name": "Minor participant liability waiver",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility", "trainer", "community_program"],
        "required_for_roles": ["parent"],
        "required_for_workflows": ["lesson_ready", "event_signup"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "media_photo_release": {
        "display_name": "Media / photo release",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility", "trainer", "community_program"],
        "required_for_roles": ["horse_owner", "parent", "rider"],
        "required_for_workflows": ["owner_updates", "marketing_media"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "emergency_vet_authorization": {
        "display_name": "Emergency veterinary care authorization",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility", "individual_owner"],
        "required_for_roles": ["horse_owner", "parent"],
        "required_for_workflows": ["horse_care", "emergency_workflow"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "lesson_program_agreement": {
        "display_name": "Lesson program agreement",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["trainer", "facility"],
        "required_for_roles": ["parent", "rider"],
        "required_for_workflows": ["lesson_ready"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": True,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "boarding_facility_services_agreement": {
        "display_name": "Boarding / facility services agreement",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility"],
        "required_for_roles": ["horse_owner", "parent"],
        "required_for_workflows": ["boarding_onboarding"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": True,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "trainer_service_provider_agreement": {
        "display_name": "Trainer / service-provider agreement",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "required_for_customer_types": ["facility", "trainer"],
        "required_for_roles": ["trainer", "service_provider"],
        "required_for_workflows": ["provider_assignment"],
        "requires_guardian_signature": False,
        "requires_facility_countersignature": True,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "arena_facility_rules_acknowledgement": {
        "display_name": "Arena / facility rules acknowledgement",
        "workflow_kind": WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
        "provider": PROVIDER_NONE,
        "required_for_customer_types": ["facility", "trainer", "individual_owner"],
        "required_for_roles": ["horse_owner", "parent", "rider", "trainer"],
        "required_for_workflows": ["arena_use"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "community_program_acknowledgement": {
        "display_name": "Community program acknowledgement",
        "workflow_kind": WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
        "provider": PROVIDER_NONE,
        "required_for_customer_types": ["community_program"],
        "required_for_roles": ["parent", "rider"],
        "required_for_workflows": ["community_program_signup"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
    "onboarding_policy_acknowledgement": {
        "display_name": "Onboarding policy acknowledgement",
        "workflow_kind": WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
        "provider": PROVIDER_NONE,
        "required_for_customer_types": ["facility", "trainer", "individual_owner"],
        "required_for_roles": ["horse_owner", "parent", "rider", "trainer", "staff"],
        "required_for_workflows": ["onboarding"],
        "requires_guardian_signature": True,
        "requires_facility_countersignature": False,
        "requires_platform_countersignature": False,
        "expires_after_days": 365,
        "launch_behavior": LAUNCH_BEHAVIOR_SOFT_WARNING,
        "exportable_evidence": True,
    },
}

TEMPLATE_REQUIRED_FIELDS = (
    "id",
    "barn_id",
    "document_type",
    "display_name",
    "workflow_kind",
    "provider",
    "provider_template_id",
    "version",
    "status",
    "required_for_customer_types",
    "required_for_roles",
    "required_for_workflows",
    "requires_guardian_signature",
    "requires_facility_countersignature",
    "requires_platform_countersignature",
    "expires_after_days",
)
REQUEST_REQUIRED_FIELDS = (
    "id",
    "barn_id",
    "template_id",
    "subject_user_id",
    "subject_student_profile_id",
    "required_signer_user_ids",
    "provider_envelope_id",
    "status",
    "requested_by_user_id",
    "created_at",
    "expires_at",
)
SIGNATURE_REQUIRED_FIELDS = (
    "id",
    "barn_id",
    "request_id",
    "template_id",
    "signer_user_id",
    "relationship_to_subject",
    "provider_signature_id",
    "status",
    "signed_at",
    "provider_certificate_ref",
)
ACKNOWLEDGEMENT_REQUIRED_FIELDS = (
    "id",
    "barn_id",
    "policy_key",
    "user_id",
    "version",
    "status",
    "acknowledged_at",
    "audit_metadata",
)

PRIVATE_DOCUMENT_FIELDS = {
    "_id",
    "legal_text",
    "signed_document_body",
    "signed_document_url",
    "raw_provider_payload",
    "provider_access_token",
    "provider_refresh_token",
    "provider_private_key",
    "webhook_secret",
    "guardian_consent_text",
    "birthdate",
    "private_notes",
    "staff_notes",
    "audit_diff",
    "required_signer_user_ids",
    "signed_user_ids",
}
PROVIDER_REF_FIELDS = {
    "provider_envelope_id",
    "provider_signature_id",
    "provider_certificate_ref",
}
AUDIT_SAFE_KEYS = {
    "document_type",
    "workflow_kind",
    "provider",
    "status",
    "local_status",
    "launch_behavior",
    "required_signer_count",
    "signed_count",
    "requires_guardian_signature",
    "requires_facility_countersignature",
    "requires_platform_countersignature",
}


def document_matrix() -> Dict[str, Dict[str, Any]]:
    """Return a copy of the BN6B document type matrix."""
    return {key: dict(value) for key, value in DOCUMENT_TYPE_MATRIX.items()}


def document_type_contract(document_type: str) -> Dict[str, Any]:
    key = (document_type or "").strip().lower()
    if key not in DOCUMENT_TYPE_MATRIX:
        raise ValueError(f"Unknown document type: {document_type}")
    return dict(DOCUMENT_TYPE_MATRIX[key])


def provider_status_to_local_status(provider_status: Optional[str]) -> str:
    status = (provider_status or "").strip().lower()
    return PROVIDER_STATUS_TO_LOCAL_STATUS.get(status, "provider_attention")


def signer_requirements_for_subject(
    document_type: str,
    *,
    minor_status: str,
    requires_facility_countersignature: Optional[bool] = None,
    requires_platform_countersignature: Optional[bool] = None,
) -> Dict[str, Any]:
    """Return required signer roles for the subject/minor context.

    Under-13 subjects are guardian-only for legal/acknowledgement signature
    participation; 13-17 and unknown-age subjects require a guardian and may
    also have the subject signer role for the later UX phase.
    """
    contract = document_type_contract(document_type)
    status = normalize_minor_status(minor_status)
    signer_roles: list[str] = []

    if status == MINOR_STATUS_ADULT:
        signer_roles.append(SIGNER_SUBJECT)
    elif requires_guardian(status) and contract.get("requires_guardian_signature"):
        signer_roles.append(SIGNER_GUARDIAN)
        if status in {MINOR_STATUS_MINOR_13_TO_17, MINOR_STATUS_UNKNOWN}:
            signer_roles.append(SIGNER_SUBJECT)
    else:
        signer_roles.append(SIGNER_SUBJECT)

    facility_counter = (
        contract.get("requires_facility_countersignature")
        if requires_facility_countersignature is None
        else bool(requires_facility_countersignature)
    )
    platform_counter = (
        contract.get("requires_platform_countersignature")
        if requires_platform_countersignature is None
        else bool(requires_platform_countersignature)
    )
    if facility_counter:
        signer_roles.append(SIGNER_FACILITY_COUNTERSIGNER)
    if platform_counter:
        signer_roles.append(SIGNER_PLATFORM_COUNTERSIGNER)

    return {
        "document_type": document_type,
        "minor_status": status,
        "signer_roles": signer_roles,
        "guardian_required": SIGNER_GUARDIAN in signer_roles,
        "subject_may_sign": SIGNER_SUBJECT in signer_roles,
        "under_13_policy": "parent_managed_only" if status == MINOR_STATUS_UNDER_13 else None,
    }


def build_template_contract(
    document_type: str,
    *,
    template_id: str,
    barn_id: Optional[str] = None,
    provider_template_id: Optional[str] = None,
    version: int = 1,
    status: str = "draft",
) -> Dict[str, Any]:
    """Build the future template shape without writing it."""
    contract = document_type_contract(document_type)
    return {
        "id": template_id,
        "barn_id": barn_id,
        "platform_template": barn_id is None,
        "document_type": document_type,
        "display_name": contract["display_name"],
        "workflow_kind": contract["workflow_kind"],
        "provider": contract["provider"],
        "provider_template_id": provider_template_id,
        "version": int(version),
        "status": status,
        "required_for_customer_types": list(contract["required_for_customer_types"]),
        "required_for_roles": list(contract["required_for_roles"]),
        "required_for_workflows": list(contract["required_for_workflows"]),
        "requires_guardian_signature": bool(contract["requires_guardian_signature"]),
        "requires_facility_countersignature": bool(contract["requires_facility_countersignature"]),
        "requires_platform_countersignature": bool(contract["requires_platform_countersignature"]),
        "expires_after_days": contract["expires_after_days"],
        "launch_behavior": contract["launch_behavior"],
        "exportable_evidence": bool(contract["exportable_evidence"]),
    }


def provider_envelope_contract_preview(
    *,
    request: Mapping[str, Any],
    template: Mapping[str, Any],
    signer_roles: Iterable[str],
) -> Dict[str, Any]:
    """Return a safe local-to-provider mapping preview.

    This is deliberately not a DocuSign API payload. It contains only local refs
    and role labels needed for review of the future mapping contract.
    """
    return {
        "provider": template.get("provider") or PROVIDER_NONE,
        "workflow_kind": template.get("workflow_kind"),
        "template_id": template.get("id"),
        "document_type": template.get("document_type"),
        "request_id": request.get("id"),
        "barn_id": request.get("barn_id"),
        "recipient_roles": [role for role in signer_roles if role in SIGNER_ROLES],
        "status_mapping": dict(PROVIDER_STATUS_TO_LOCAL_STATUS),
        "creates_live_envelope": False,
    }


def project_document_record(
    doc: Mapping[str, Any],
    *,
    include_provider_refs: bool = False,
) -> Dict[str, Any]:
    """Project document rows for API responses without private payloads."""
    out: Dict[str, Any] = {}
    for key, value in (doc or {}).items():
        if key in PRIVATE_DOCUMENT_FIELDS:
            continue
        if key in PROVIDER_REF_FIELDS and not include_provider_refs:
            continue
        out[key] = value
    return out


def audit_safe_document_metadata(metadata: Mapping[str, Any]) -> Dict[str, Any]:
    """Keep document audit metadata small and non-sensitive."""
    clean: Dict[str, Any] = {}
    for key in AUDIT_SAFE_KEYS:
        value = (metadata or {}).get(key)
        if value is not None:
            clean[key] = value
    if "required_signer_user_ids" in (metadata or {}):
        clean["required_signer_count"] = len(list(metadata.get("required_signer_user_ids") or []))
    if "signed_user_ids" in (metadata or {}):
        clean["signed_count"] = len(list(metadata.get("signed_user_ids") or []))
    return clean
