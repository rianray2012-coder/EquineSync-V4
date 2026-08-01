"""Document signature and workflow foundation routes.

Build-Next-6A exposed provider readiness only. Build-Next-6C adds a local
template/request foundation. Build-Next-6E adds a sandbox-only DocuSign draft
envelope action behind an explicit env gate while keeping production sending,
signing URLs, provider callbacks, and signed-document storage deferred.
Build-Next-6F adds a live-capable, disabled-by-default DocuSign Connect
webhook receiver for status-only sync; it stores no raw provider payloads or
signed documents.
"""
from __future__ import annotations

import uuid
import os
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from core import audit
from core.db import db as default_db
from core.document_signing import (
    create_docusign_sandbox_envelope,
    document_signature_strategy_snapshot,
    docusign_account_id_matches,
    docusign_connect_configuration_matches,
    docusign_sandbox_ready,
    docusign_webhook_envelope_id,
    docusign_webhook_ready,
    docusign_webhook_status,
    docusign_webhook_status_changed_at,
    verify_docusign_hmac,
)
from core.document_workflows import (
    DOCUMENT_REQUESTS_COLLECTION,
    DOCUMENT_TEMPLATES_COLLECTION,
    LOCAL_DOCUMENT_REQUEST_STATUSES,
    PROVIDER_DOCUSIGN,
    WORKFLOW_PROVIDER_SIGNATURE,
    SIGNER_FACILITY_COUNTERSIGNER,
    SIGNER_GUARDIAN,
    SIGNER_PLATFORM_COUNTERSIGNER,
    SIGNER_SUBJECT,
    audit_safe_document_metadata,
    build_template_contract,
    document_matrix,
    document_type_contract,
    project_document_record,
    provider_status_to_local_status,
    signer_requirements_for_subject,
)
from core.minor_safety import (
    DECISION_ALLOW,
    MINOR_STATUS_UNKNOWN,
    WORKFLOW_DOCUMENT_SIGNATURE,
    WORKFLOW_MEDIA_RELEASE,
    WORKFLOW_WAIVER,
    audit_safe_guardian_minor_metadata,
    guardian_minor_public_error_detail,
    guardian_minor_workflow_gate,
    load_guardian_minor_authority_rows,
    minor_status_for_student,
    normalize_minor_status,
    requires_guardian,
)
from core.permissions import require_permission
from core.tenancy import barn_filter, resolve_barn_id


DOCUMENT_MANAGER_ROLES = {"admin", "barn_manager"}
DOCUMENT_READ_CAPABILITY = "communication" + ":read"
TEMPLATE_STATUSES = {"draft", "active", "archived"}


class DocumentTemplateCreate(BaseModel):
    document_type: str
    provider_template_id: Optional[str] = None
    version: int = Field(default=1, ge=1)
    status: str = "draft"


class DocumentRequestCreate(BaseModel):
    template_id: str
    subject_user_id: Optional[str] = None
    subject_student_profile_id: Optional[str] = None
    minor_status: Optional[str] = None
    guardian_state_token: Optional[str] = None
    guardian_user_ids: List[str] = Field(default_factory=list)
    facility_countersigner_user_id: Optional[str] = None
    platform_countersigner_user_id: Optional[str] = None
    expires_at: Optional[str] = None
    note: Optional[str] = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _require_document_manager(user: Dict[str, Any]) -> None:
    if (user or {}).get("role") not in DOCUMENT_MANAGER_ROLES:
        raise HTTPException(status_code=403, detail="Admin/Manager only")


def _clean_status(status: str) -> str:
    cleaned = (status or "").strip().lower()
    if cleaned not in TEMPLATE_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid template status")
    return cleaned


def _projection(doc: Dict[str, Any]) -> Dict[str, Any]:
    return project_document_record(doc, include_provider_refs=False)


async def _load_template_or_404(database, user: Dict[str, Any], template_id: str) -> Dict[str, Any]:
    template = await database[DOCUMENT_TEMPLATES_COLLECTION].find_one(
        barn_filter(user, {"id": template_id}),
        {"_id": 0},
    )
    if not template:
        raise HTTPException(status_code=404, detail="Document template not found")
    return template


async def _load_request_or_404(database, user: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    doc = await database[DOCUMENT_REQUESTS_COLLECTION].find_one(
        barn_filter(user, {"id": request_id}),
        {"_id": 0},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document request not found")
    return doc


async def _student_minor_status(database, user: Dict[str, Any], student_id: Optional[str]) -> str:
    if not student_id:
        return MINOR_STATUS_UNKNOWN
    student = await database.student_profiles.find_one(
        barn_filter(user, {"id": student_id}),
        {"_id": 0, "minor_status": 1},
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return normalize_minor_status(student.get("minor_status") or MINOR_STATUS_UNKNOWN)


async def _load_student_profile(database, user: Dict[str, Any], student_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not student_id:
        return None
    student = await database.student_profiles.find_one(
        barn_filter(user, {"id": student_id}),
        {"_id": 0},
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


def _document_guard_workflow(document_type: str) -> str:
    normalized = (document_type or "").strip().lower()
    if normalized == "media_photo_release":
        return WORKFLOW_MEDIA_RELEASE
    if "waiver" in normalized:
        return WORKFLOW_WAIVER
    return WORKFLOW_DOCUMENT_SIGNATURE


def _required_signer_ids(
    roles: List[str],
    body: DocumentRequestCreate,
) -> List[str]:
    signer_ids: List[str] = []
    if SIGNER_SUBJECT in roles and body.subject_user_id:
        signer_ids.append(body.subject_user_id)
    if SIGNER_GUARDIAN in roles:
        signer_ids.extend([gid for gid in body.guardian_user_ids if gid])
    if SIGNER_FACILITY_COUNTERSIGNER in roles and body.facility_countersigner_user_id:
        signer_ids.append(body.facility_countersigner_user_id)
    if SIGNER_PLATFORM_COUNTERSIGNER in roles and body.platform_countersigner_user_id:
        signer_ids.append(body.platform_countersigner_user_id)
    # Stable order, no duplicates.
    return list(dict.fromkeys(signer_ids))


def build_router(*, get_current_user, db=None) -> APIRouter:
    database = db if db is not None else default_db
    router = APIRouter(tags=["document-signatures"])

    async def _enforce_document_guard(
        *,
        workflow: str,
        student: Optional[Dict[str, Any]],
        guardian_user_ids: List[str],
        scope_reference: str,
        policy_version: str,
        expected_state_token: Optional[str] = None,
        action: str,
        request: Request,
        user: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        if not student:
            return
        barn_id = resolve_barn_id(user)
        links, consents = await load_guardian_minor_authority_rows(
            database,
            barn_id=barn_id,
            student_profile_ids=[student.get("id")],
            workflow=workflow,
        )
        gate = guardian_minor_workflow_gate(
            workflow=workflow,
            students=[student],
            guardian_links=links,
            workflow_consents=consents,
            barn_id=barn_id,
            participant_user_ids=guardian_user_ids,
            scope_reference=scope_reference,
            policy_version=policy_version,
            expected_state_token=expected_state_token,
            require_guardian_participant=True,
            action=action,
        )
        if gate["decision"] == DECISION_ALLOW:
            return gate
        await audit.record(
            action="document_request.guardian_minor_blocked",
            user=user,
            request=request,
            resource_type="document_request",
            resource_id=scope_reference,
            outcome="denied",
            status_code=403,
            metadata=audit_safe_guardian_minor_metadata(gate),
            _db=database,
        )
        raise HTTPException(status_code=403, detail=guardian_minor_public_error_detail(gate))

    @router.get("/document-signatures/providers")
    async def document_signature_providers(user=Depends(get_current_user)):
        require_permission(user, "integration:read")
        return document_signature_strategy_snapshot()

    @router.get("/document-signatures/document-types")
    async def document_signature_document_types(user=Depends(get_current_user)):
        require_permission(user, DOCUMENT_READ_CAPABILITY)
        return {
            "document_types": document_matrix(),
            "launch_behavior": "soft_warning",
            "live_signing_enabled": False,
        }

    @router.get("/document-signatures/templates")
    async def list_document_templates(user=Depends(get_current_user)):
        _require_document_manager(user)
        rows = await database[DOCUMENT_TEMPLATES_COLLECTION].find(
            barn_filter(user),
            {"_id": 0},
        ).sort("created_at", -1).to_list(500)
        return {"templates": [_projection(row) for row in rows]}

    @router.post("/document-signatures/templates")
    async def create_document_template(
        body: DocumentTemplateCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_document_manager(user)
        try:
            document_type_contract(body.document_type)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        now = _now_iso()
        doc = build_template_contract(
            body.document_type.strip().lower(),
            template_id=_new_id("doc_tmpl"),
            barn_id=resolve_barn_id(user),
            provider_template_id=(body.provider_template_id or None),
            version=body.version,
            status=_clean_status(body.status),
        )
        doc.update({
            "created_by_user_id": user.get("id"),
            "created_at": now,
            "updated_at": now,
        })
        await database[DOCUMENT_TEMPLATES_COLLECTION].insert_one(doc)
        await audit.record(
            action="document_template.created",
            user=user,
            request=request,
            resource_type="document_template",
            resource_id=doc["id"],
            metadata=audit_safe_document_metadata(doc),
            _db=database,
        )
        return _projection(doc)

    @router.get("/document-signatures/requests")
    async def list_document_requests(user=Depends(get_current_user)):
        _require_document_manager(user)
        rows = await database[DOCUMENT_REQUESTS_COLLECTION].find(
            barn_filter(user),
            {"_id": 0},
        ).sort("created_at", -1).to_list(500)
        return {"requests": [_projection(row) for row in rows]}

    @router.post("/document-signatures/requests")
    async def create_document_request(
        body: DocumentRequestCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_document_manager(user)
        if not body.subject_user_id and not body.subject_student_profile_id:
            raise HTTPException(status_code=422, detail="subject_user_id or subject_student_profile_id is required")
        template = await _load_template_or_404(database, user, body.template_id)
        minor_status = normalize_minor_status(body.minor_status or MINOR_STATUS_UNKNOWN)
        student = None
        if body.subject_student_profile_id:
            student = await _load_student_profile(database, user, body.subject_student_profile_id)
            minor_status = minor_status_for_student(student)
        signer_contract = signer_requirements_for_subject(
            template["document_type"],
            minor_status=minor_status,
        )
        signer_roles = list(signer_contract["signer_roles"])
        if SIGNER_GUARDIAN in signer_roles and not [gid for gid in body.guardian_user_ids if gid]:
            raise HTTPException(status_code=422, detail="guardian_user_ids is required for guardian-required document requests")
        guard_workflow = _document_guard_workflow(template["document_type"])
        guard_scope = f"document_template:{template['id']}:v{template.get('version') or 1}"
        guard_policy = f"{template['document_type']}-v{template.get('version') or 1}"
        if requires_guardian(minor_status) and student:
            gate = await _enforce_document_guard(
                workflow=guard_workflow,
                student=student,
                guardian_user_ids=body.guardian_user_ids,
                scope_reference=guard_scope,
                policy_version=guard_policy,
                expected_state_token=body.guardian_state_token,
                action="document_request.create",
                request=request,
                user=user,
            )
        else:
            gate = None
        required_signer_user_ids = _required_signer_ids(signer_roles, body)
        now = _now_iso()
        status = "draft"
        doc = {
            "id": _new_id("doc_req"),
            "barn_id": resolve_barn_id(user),
            "template_id": template["id"],
            "document_type": template["document_type"],
            "display_name": template.get("display_name"),
            "workflow_kind": template.get("workflow_kind"),
            "provider": template.get("provider"),
            "subject_user_id": body.subject_user_id,
            "subject_student_profile_id": body.subject_student_profile_id,
            "minor_status": minor_status,
            "signer_roles": signer_roles,
            "required_signer_user_ids": required_signer_user_ids,
            "required_signer_count": len(required_signer_user_ids),
            "signed_user_ids": [],
            "signed_count": 0,
            "provider_envelope_id": None,
            "status": status,
            "local_status": status,
            "launch_behavior": template.get("launch_behavior") or "soft_warning",
            "requested_by_user_id": user.get("id"),
            "created_at": now,
            "updated_at": now,
            "expires_at": body.expires_at,
            "note_present": bool((body.note or "").strip()),
            "guardian_guard_workflow": guard_workflow,
            "guardian_guard_scope_reference": guard_scope,
            "guardian_guard_policy_version": guard_policy,
            "guardian_guard_state_token": gate.get("state_token") if gate else None,
        }
        await database[DOCUMENT_REQUESTS_COLLECTION].insert_one(doc)
        await audit.record(
            action="document_request.created",
            user=user,
            request=request,
            resource_type="document_request",
            resource_id=doc["id"],
            metadata=audit_safe_document_metadata(doc),
            _db=database,
        )
        return _projection(doc)

    @router.get("/document-signatures/requests/{request_id}")
    async def get_document_request(request_id: str, user=Depends(get_current_user)):
        _require_document_manager(user)
        doc = await _load_request_or_404(database, user, request_id)
        if (doc.get("status") or "") not in LOCAL_DOCUMENT_REQUEST_STATUSES:
            doc["local_status"] = "provider_attention"
        return _projection(doc)

    @router.post("/document-signatures/requests/{request_id}/sandbox-envelope")
    async def create_request_sandbox_envelope(
        request_id: str,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_document_manager(user)
        ready, reason = docusign_sandbox_ready()
        if not ready:
            raise HTTPException(status_code=403, detail=f"DocuSign sandbox envelope creation is not enabled: {reason}")

        doc = await _load_request_or_404(database, user, request_id)
        if doc.get("provider_envelope_id"):
            raise HTTPException(status_code=409, detail="Document request already has a provider envelope")
        if doc.get("workflow_kind") != WORKFLOW_PROVIDER_SIGNATURE or doc.get("provider") != PROVIDER_DOCUSIGN:
            raise HTTPException(status_code=422, detail="Document request is not a DocuSign provider-signature workflow")

        template = await _load_template_or_404(database, user, doc["template_id"])
        student = await _load_student_profile(database, user, doc.get("subject_student_profile_id"))
        if student:
            gate = await _enforce_document_guard(
                workflow=doc.get("guardian_guard_workflow") or WORKFLOW_DOCUMENT_SIGNATURE,
                student=student,
                guardian_user_ids=doc.get("required_signer_user_ids") or [],
                scope_reference=doc.get("guardian_guard_scope_reference") or f"document_request:{doc['id']}",
                policy_version=doc.get("guardian_guard_policy_version") or f"{doc.get('document_type')}-v{template.get('version') or 1}",
                expected_state_token=doc.get("guardian_guard_state_token"),
                action="document_request.sandbox_envelope",
                request=request,
                user=user,
            )
        else:
            gate = None
        provider_template_id = (template.get("provider_template_id") or "").strip()
        if not provider_template_id:
            raise HTTPException(status_code=422, detail="Provider template id is required for sandbox envelope creation")
        recipient_roles = [role for role in doc.get("signer_roles") or [] if role]
        if not recipient_roles:
            raise HTTPException(status_code=422, detail="At least one signer role is required")

        try:
            result = create_docusign_sandbox_envelope(
                account_id=os.environ["DOCUSIGN_ACCOUNT_ID"].strip(),
                provider_template_id=provider_template_id,
                recipient_roles=recipient_roles,
                request_id=doc["id"],
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

        now = _now_iso()
        provider_status = result.get("provider_status") or "created"
        local_status = provider_status_to_local_status(provider_status)
        update = {
            "provider_envelope_id": result["provider_envelope_id"],
            "provider_status": provider_status,
            "status": local_status,
            "local_status": local_status,
            "sandbox_envelope_created_at": now,
            "updated_at": now,
            "guardian_guard_state_token": gate.get("state_token") if gate else doc.get("guardian_guard_state_token"),
        }
        await database[DOCUMENT_REQUESTS_COLLECTION].update_one(
            barn_filter(user, {"id": doc["id"]}),
            {"$set": update},
        )
        doc.update(update)
        await audit.record(
            action="document_request.sandbox_envelope_created",
            user=user,
            request=request,
            resource_type="document_request",
            resource_id=doc["id"],
            metadata=audit_safe_document_metadata(doc),
            _db=database,
        )
        projected = _projection(doc)
        projected["sandbox_envelope_created"] = True
        return projected

    @router.post("/document-signatures/docusign/webhook")
    async def docusign_connect_webhook(request: Request):
        ready, reason = docusign_webhook_ready()
        if not ready:
            raise HTTPException(status_code=403, detail=f"DocuSign webhook processing is not enabled: {reason}")

        body = await request.body()
        if not verify_docusign_hmac(body, request.headers):
            raise HTTPException(status_code=401, detail="Invalid DocuSign webhook signature")
        try:
            payload = json.loads(body.decode("utf-8") or "{}")
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=400, detail="Invalid DocuSign webhook payload") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Invalid DocuSign webhook payload")
        if not docusign_connect_configuration_matches(payload):
            raise HTTPException(status_code=403, detail="Unexpected DocuSign Connect configuration")
        if not docusign_account_id_matches(payload):
            raise HTTPException(status_code=403, detail="Unexpected DocuSign account")

        envelope_id = docusign_webhook_envelope_id(payload)
        if not envelope_id:
            raise HTTPException(status_code=400, detail="Missing DocuSign envelope id")
        match_filter = {
            "provider_envelope_id": envelope_id,
            "provider": PROVIDER_DOCUSIGN,
            "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        }
        doc = await database[DOCUMENT_REQUESTS_COLLECTION].find_one(
            match_filter,
            {"_id": 0},
        )
        if not doc:
            return {"accepted": True, "matched": False}

        provider_status = docusign_webhook_status(payload)
        local_status = provider_status_to_local_status(provider_status)
        now = _now_iso()
        update = {
            "provider_status": provider_status,
            "status": local_status,
            "local_status": local_status,
            "provider_status_changed_at": docusign_webhook_status_changed_at(payload),
            "updated_at": now,
        }
        await database[DOCUMENT_REQUESTS_COLLECTION].update_one(
            {"id": doc["id"], **match_filter},
            {"$set": update},
        )
        doc.update(update)
        await audit.record(
            action="document_request.provider_status_updated",
            actor_email="docusign-connect@system",
            actor_role="provider_webhook",
            barn_id=doc.get("barn_id"),
            request=request,
            resource_type="document_request",
            resource_id=doc["id"],
            metadata=audit_safe_document_metadata(doc),
            _db=database,
        )
        return {
            "accepted": True,
            "matched": True,
            "status": local_status,
        }

    return router
