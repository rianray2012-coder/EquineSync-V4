"""Build-Next-5B guardian-first student onboarding foundation.

This router intentionally stays narrow: it creates operational student
profiles, creates/reuses guardian invites, links accepted guardian users, and
enforces the BN5-A lesson-ready gate. It does not implement messaging,
waivers, payments, document signing, or parent-portal workflows.
"""
from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from core import audit
from core.minor_safety import (
    AUTHORITY_SCOPE_RELATIONSHIP_ADMINISTRATION,
    CONSENT_GRANTED,
    CONSENT_REQUIRED,
    GUARDIAN_AUTHORITY_SCOPES,
    GUARDIAN_LINK_ACTIVE,
    GUARDIAN_LINK_PENDING,
    GUARDIAN_WORKFLOW_CONSENT_COLLECTION,
    MINOR_STATUS_UNKNOWN,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_AUTHORITY_SCOPES,
    WORKFLOW_CONSENT_REQUIRED,
    WORKFLOW_LESSON_READY,
    audit_safe_guardian_minor_metadata,
    audit_safe_minor_metadata,
    guardian_minor_public_error_detail,
    guardian_minor_workflow_gate,
    load_guardian_minor_authority_rows,
    minor_status_for_student,
    normalize_minor_status,
    requires_guardian,
    student_workflow_gate,
)
from core.tenancy import barn_filter, resolve_barn_id


STUDENT_MANAGER_ROLES = {"admin", "barn_manager", "trainer"}
STUDENT_PROFILE_STATUSES = {"draft", "guardian_pending", "lesson_ready", "archived"}
GUARDIAN_USER_ROLES = {"parent", "horse_owner"}
GUARDIAN_MEMBERSHIP_RELATIONSHIPS = {"parent", "owner"}
GUARDIAN_RELATIONSHIPS = {
    "parent",
    "guardian",
    "grandparent",
    "step_parent",
    "legal_guardian",
    "other",
}
GUARDIAN_INVITE_ROLE = "parent"


class StudentProfileCreate(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=120)
    birthdate: Optional[str] = Field(default=None, max_length=20)
    minor_status: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=1000)


class StudentStatusPatch(BaseModel):
    status: str


class GuardianInviteCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(default=None, max_length=120)
    relationship: str = "parent"


class GuardianLinkCreate(BaseModel):
    guardian_user_id: Optional[str] = None
    invite_id: Optional[str] = None
    relationship: str = "parent"
    is_primary: bool = True
    authority_scopes: Optional[list[str]] = None


class GuardianWorkflowConsentCreate(BaseModel):
    guardian_user_id: str
    workflow: str
    scope_reference: str = Field(..., min_length=1, max_length=200)
    policy_version: str = Field(default="v1", min_length=1, max_length=80)
    expires_at: Optional[str] = Field(default=None, max_length=80)
    evidence_reference: Optional[str] = Field(default=None, max_length=200)


class GuardianLinkRevoke(BaseModel):
    reason: Optional[str] = Field(default=None, max_length=200)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _new_token_pair() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, _hash_token(raw)


def _require_student_manager(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() not in STUDENT_MANAGER_ROLES:
        raise HTTPException(status_code=403, detail="Permission denied")


def _normalize_relationship(value: str) -> str:
    rel = (value or "parent").strip().lower()
    if rel not in GUARDIAN_RELATIONSHIPS:
        raise HTTPException(status_code=422, detail="Invalid guardian relationship")
    return rel


def _project_student(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in doc.items() if k != "_id"}


async def _load_student_or_404(db, user: Dict[str, Any], student_id: str) -> Dict[str, Any]:
    student = await db[STUDENT_PROFILE_COLLECTION].find_one(
        barn_filter(user, {"id": student_id}),
        {"_id": 0},
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


async def _active_guardian_links(db, barn_id: str, student_id: str) -> list[Dict[str, Any]]:
    return await db.guardian_links.find(
        {
            "barn_id": barn_id,
            "student_profile_id": student_id,
            "status": GUARDIAN_LINK_ACTIVE,
        },
        {"_id": 0},
    ).to_list(100)


def _default_authority_scopes() -> list[str]:
    return sorted(GUARDIAN_AUTHORITY_SCOPES)


def _normalize_authority_scopes(values: Optional[list[str]]) -> list[str]:
    if values is None:
        return _default_authority_scopes()
    scopes = []
    for raw in values:
        scope = str(raw or "").strip().upper()
        if scope not in GUARDIAN_AUTHORITY_SCOPES:
            raise HTTPException(status_code=422, detail="Invalid guardian authority scope")
        if scope not in scopes:
            scopes.append(scope)
    if not scopes:
        raise HTTPException(status_code=422, detail="authority_scopes cannot be empty")
    return sorted(scopes)


async def _touch_guardian_safeguarding_version(db, barn_id: str, student_id: str) -> None:
    await db[STUDENT_PROFILE_COLLECTION].update_one(
        {"id": student_id, "barn_id": barn_id},
        {"$inc": {"guardian_safeguarding_version": 1}, "$set": {"updated_at": _iso(_now_utc())}},
    )


async def _guard_student_workflow(
    *,
    db,
    student: Dict[str, Any],
    workflow: str,
    scope_reference: str,
    policy_version: str,
    action: str,
    consent_required: Optional[bool] = None,
) -> Dict[str, Any]:
    barn_id = student.get("barn_id") or "primary"
    links, consents = await load_guardian_minor_authority_rows(
        db,
        barn_id=barn_id,
        student_profile_ids=[student.get("id")],
        workflow=workflow,
    )
    return guardian_minor_workflow_gate(
        workflow=workflow,
        students=[student],
        guardian_links=links,
        workflow_consents=consents,
        barn_id=barn_id,
        scope_reference=scope_reference,
        policy_version=policy_version,
        consent_required=consent_required,
        action=action,
    )


async def _user_has_barn_access(db, user_id: str, barn_id: str) -> bool:
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "barn_id": 1})
    if not user:
        return False
    if (user.get("barn_id") or "primary") == barn_id:
        return True
    membership = await db.account_memberships.find_one(
        {
            "user_id": user_id,
            "barn_id": barn_id,
            "membership_status": "active",
        },
        {"_id": 0, "id": 1},
    )
    return bool(membership)


async def _user_is_guardian_candidate(db, user_id: str, barn_id: str) -> bool:
    """Return whether a user can be linked as a guardian for this barn.

    BN5-B accepts a launch user mirror role of parent/horse_owner, or a future
    account_memberships role/relationship that explicitly represents
    parent/owner access in this barn. Staff/trainers with mere barn access must
    not satisfy the minor guardian gate.
    """
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "barn_id": 1, "role": 1})
    if not user:
        return False
    user_role = (user.get("role") or "").strip().lower()
    if (user.get("barn_id") or "primary") == barn_id and user_role in GUARDIAN_USER_ROLES:
        return True
    membership = await db.account_memberships.find_one(
        {
            "user_id": user_id,
            "barn_id": barn_id,
            "membership_status": "active",
            "$or": [
                {"role": {"$in": sorted(GUARDIAN_USER_ROLES)}},
                {"relationship_type": {"$in": sorted(GUARDIAN_MEMBERSHIP_RELATIONSHIPS)}},
            ],
        },
        {"_id": 0, "id": 1},
    )
    return bool(membership)


async def _audit_minor_event(
    *,
    db,
    action: str,
    user: Dict[str, Any],
    request: Request,
    student: Dict[str, Any],
    workflow: str,
    guardian_links: list[Dict[str, Any]],
    resource_type: str = "student_profile",
    resource_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
    outcome: str = "success",
    status_code: Optional[int] = None,
) -> None:
    gate = student_workflow_gate(student, guardian_links, workflow=workflow)
    await audit.record(
        action=action,
        user=user,
        request=request,
        resource_type=resource_type,
        resource_id=resource_id or student.get("id"),
        outcome=outcome,
        status_code=status_code,
        metadata=audit_safe_minor_metadata(student=student, gate=gate, extra=extra),
        _db=db,
    )


def build_router(
    *,
    db,
    get_current_user,
    mailer_send,
    base_url_from_request,
    new_id,
) -> APIRouter:
    router = APIRouter(prefix="/student-profiles", tags=["student-guardians"])

    @router.post("")
    async def create_student_profile(
        body: StudentProfileCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        barn_id = resolve_barn_id(user)
        doc = {
            "id": new_id(),
            "barn_id": barn_id,
            "display_name": body.display_name.strip(),
            "birthdate": body.birthdate,
            "minor_status": normalize_minor_status(body.minor_status or MINOR_STATUS_UNKNOWN),
            "notes": body.notes,
            "status": "draft",
            "created_by_user_id": user["id"],
            "created_at": _iso(_now_utc()),
            "updated_at": _iso(_now_utc()),
        }
        doc["minor_status"] = minor_status_for_student(doc)
        await db[STUDENT_PROFILE_COLLECTION].insert_one(doc)
        await _audit_minor_event(
            db=db,
            action="student_profile.created",
            user=user,
            request=request,
            student=doc,
            workflow=WORKFLOW_LESSON_READY,
            guardian_links=[],
        )
        return _project_student(doc)

    @router.get("")
    async def list_student_profiles(user=Depends(get_current_user)):
        _require_student_manager(user)
        rows = await db[STUDENT_PROFILE_COLLECTION].find(
            barn_filter(user),
            {"_id": 0},
        ).sort("created_at", -1).to_list(500)
        return rows

    @router.get("/{student_id}")
    async def get_student_profile(student_id: str, user=Depends(get_current_user)):
        _require_student_manager(user)
        return await _load_student_or_404(db, user, student_id)

    @router.post("/{student_id}/guardian-invites")
    async def create_guardian_invite(
        student_id: str,
        body: GuardianInviteCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        student = await _load_student_or_404(db, user, student_id)
        barn_id = resolve_barn_id(user)
        relationship = _normalize_relationship(body.relationship)
        email_l = body.email.lower()

        existing = await db.invites.find_one({
            "barn_id": barn_id,
            "email": email_l,
            "role": GUARDIAN_INVITE_ROLE,
            "status": "pending",
        })
        if existing:
            await db.invites.update_one(
                {"id": existing["id"]},
                {
                    "$addToSet": {"intended_student_profile_ids": student_id},
                    "$set": {
                        "guardian_relationship": relationship,
                        "updated_at": _iso(_now_utc()),
                    },
                },
            )
            if student.get("status") == "draft":
                await db[STUDENT_PROFILE_COLLECTION].update_one(
                    {"id": student_id, "barn_id": barn_id},
                    {"$set": {"status": "guardian_pending", "updated_at": _iso(_now_utc())}},
                )
            invite = await db.invites.find_one({"id": existing["id"]}, {"_id": 0, "token_hash": 0})
            await _audit_minor_event(
                db=db,
                action="student_guardian.invite_reused",
                user=user,
                request=request,
                student=student,
                workflow=WORKFLOW_LESSON_READY,
                guardian_links=await _active_guardian_links(db, barn_id, student_id),
                resource_type="invite",
                resource_id=existing["id"],
            )
            return invite

        existing_user = await db.users.find_one({"email": email_l}, {"_id": 0, "id": 1})
        raw_token, token_hash = _new_token_pair()
        ttl_days = int(os.environ.get("INVITE_TTL_DAYS", "7"))
        expires_at = _now_utc() + timedelta(days=ttl_days)
        invite = {
            "id": new_id(),
            "email": email_l,
            "full_name": body.full_name,
            "role": GUARDIAN_INVITE_ROLE,
            "barn_id": barn_id,
            "token_hash": token_hash,
            "status": "pending",
            "message": None,
            "invited_by_id": user["id"],
            "invited_by_name": user.get("full_name"),
            "existing_user_id": existing_user.get("id") if existing_user else None,
            "intended_student_profile_ids": [student_id],
            "guardian_relationship": relationship,
            "expires_at": _iso(expires_at),
            "created_at": _iso(_now_utc()),
            "sends": [],
        }
        await db.invites.insert_one(invite)
        if student.get("status") == "draft":
            await db[STUDENT_PROFILE_COLLECTION].update_one(
                {"id": student_id, "barn_id": barn_id},
                {"$set": {"status": "guardian_pending", "updated_at": _iso(_now_utc())}},
            )

        accept_url = f"{base_url_from_request(request)}/accept-invite?token={raw_token}"
        mail = await mailer_send(
            to=email_l,
            subject="You're invited to join EquineSync as a guardian",
            template="onboarding_invite",
            variables={
                "barn_name": "EquineSync",
                "invitee_name": (body.full_name or email_l.split("@")[0]).strip() or "guardian",
                "inviter_name": user.get("full_name") or "EquineSync",
                "role_label": "Parent / Guardian",
                "accept_url": accept_url,
                "ttl_days": ttl_days,
            },
        )
        await db.invites.update_one(
            {"id": invite["id"]},
            {"$push": {"sends": {"at": _iso(_now_utc()), "status": mail.get("status"), "id": mail.get("id")}}},
        )
        await _audit_minor_event(
            db=db,
            action="student_guardian.invite_created",
            user=user,
            request=request,
            student=student,
            workflow=WORKFLOW_LESSON_READY,
            guardian_links=await _active_guardian_links(db, barn_id, student_id),
            resource_type="invite",
            resource_id=invite["id"],
        )
        out = await db.invites.find_one({"id": invite["id"]}, {"_id": 0, "token_hash": 0})
        out["existing_user"] = bool(existing_user)
        if mail.get("dev"):
            out["dev_accept_url"] = accept_url
        return out

    @router.post("/{student_id}/guardian-links")
    async def create_guardian_link(
        student_id: str,
        body: GuardianLinkCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        student = await _load_student_or_404(db, user, student_id)
        barn_id = resolve_barn_id(user)
        relationship = _normalize_relationship(body.relationship)

        guardian_user_id = body.guardian_user_id
        invite_id = body.invite_id
        if invite_id:
            inv = await db.invites.find_one({"id": invite_id, "barn_id": barn_id}, {"_id": 0})
            if not inv:
                raise HTTPException(status_code=404, detail="Invite not found")
            if inv.get("role") != GUARDIAN_INVITE_ROLE:
                raise HTTPException(status_code=409, detail="Guardian invite is not accepted")
            if inv.get("status") != "accepted" or not inv.get("accepted_user_id"):
                raise HTTPException(status_code=409, detail="Guardian invite is not accepted")
            if student_id not in (inv.get("intended_student_profile_ids") or []):
                raise HTTPException(status_code=403, detail="Invite is not linked to this student")
            guardian_user_id = inv["accepted_user_id"]

        if not guardian_user_id:
            raise HTTPException(status_code=422, detail="guardian_user_id or invite_id is required")
        if not await _user_has_barn_access(db, guardian_user_id, barn_id):
            raise HTTPException(status_code=404, detail="Guardian user not found")
        if not await _user_is_guardian_candidate(db, guardian_user_id, barn_id):
            raise HTTPException(status_code=403, detail="Guardian user is not eligible")

        existing = await db.guardian_links.find_one(
            {
                "barn_id": barn_id,
                "student_profile_id": student_id,
                "guardian_user_id": guardian_user_id,
                "status": {"$ne": "revoked"},
            },
            {"_id": 0},
        )
        if existing:
            return existing

        link = {
            "id": new_id(),
            "barn_id": barn_id,
            "student_profile_id": student_id,
            "guardian_user_id": guardian_user_id,
            "relationship": relationship,
            "is_primary": bool(body.is_primary),
            "status": GUARDIAN_LINK_ACTIVE,
            "consent_status": CONSENT_GRANTED if requires_guardian(student.get("minor_status")) else "not_required",
            "authority_scopes": _normalize_authority_scopes(body.authority_scopes),
            "restricted_scopes": [],
            "restricted_workflows": [],
            "disputed": False,
            "version": 1,
            "invite_id": invite_id,
            "created_at": _iso(_now_utc()),
            "updated_at": _iso(_now_utc()),
        }
        await db.guardian_links.insert_one(link)
        await _touch_guardian_safeguarding_version(db, barn_id, student_id)
        await _audit_minor_event(
            db=db,
            action="student_guardian.link_created",
            user=user,
            request=request,
            student=student,
            workflow=WORKFLOW_LESSON_READY,
            guardian_links=[link],
            resource_type="guardian_link",
            resource_id=link["id"],
        )
        return link

    @router.post("/{student_id}/guardian-consents")
    async def create_guardian_workflow_consent(
        student_id: str,
        body: GuardianWorkflowConsentCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        student = await _load_student_or_404(db, user, student_id)
        barn_id = resolve_barn_id(user)
        workflow = (body.workflow or "").strip().lower()
        if workflow not in WORKFLOW_CONSENT_REQUIRED:
            raise HTTPException(status_code=422, detail="Workflow consent is not required for this workflow")
        required_scope = WORKFLOW_AUTHORITY_SCOPES[workflow]
        guardian_link = await db.guardian_links.find_one(
            {
                "barn_id": barn_id,
                "student_profile_id": student_id,
                "guardian_user_id": body.guardian_user_id,
                "status": GUARDIAN_LINK_ACTIVE,
            },
            {"_id": 0},
        )
        if not guardian_link:
            raise HTTPException(status_code=404, detail="Guardian relationship not found")
        if required_scope not in {str(scope).strip().upper() for scope in guardian_link.get("authority_scopes") or []}:
            raise HTTPException(status_code=409, detail="Guardian authority is incomplete")
        now = _iso(_now_utc())
        consent = {
            "id": new_id(),
            "barn_id": barn_id,
            "student_profile_id": student_id,
            "guardian_user_id": body.guardian_user_id,
            "workflow": workflow,
            "scope_reference": body.scope_reference.strip(),
            "policy_version": body.policy_version.strip(),
            "status": CONSENT_GRANTED,
            "evidence_reference": (body.evidence_reference or "").strip() or None,
            "granted_by_user_id": user.get("id"),
            "grantor_authority_scope": required_scope,
            "effective_at": now,
            "expires_at": body.expires_at,
            "revoked_at": None,
            "version": 1,
            "created_at": now,
            "updated_at": now,
        }
        await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].insert_one(consent)
        await _touch_guardian_safeguarding_version(db, barn_id, student_id)
        gate = await _guard_student_workflow(
            db=db,
            student=student,
            workflow=workflow,
            scope_reference=body.scope_reference,
            policy_version=body.policy_version,
            action="consent_granted",
        )
        await audit.record(
            action="student_guardian.workflow_consent_granted",
            user=user,
            request=request,
            resource_type="guardian_workflow_consent",
            resource_id=consent["id"],
            metadata=audit_safe_guardian_minor_metadata(gate),
            _db=db,
        )
        return consent

    @router.post("/{student_id}/guardian-links/{link_id}/revoke")
    async def revoke_guardian_link(
        student_id: str,
        link_id: str,
        request: Request,
        body: Optional[GuardianLinkRevoke] = None,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        student = await _load_student_or_404(db, user, student_id)
        barn_id = resolve_barn_id(user)
        existing = await db.guardian_links.find_one(
            {"id": link_id, "barn_id": barn_id, "student_profile_id": student_id},
            {"_id": 0},
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Guardian relationship not found")
        now = _iso(_now_utc())
        await db.guardian_links.update_one(
            {"id": link_id, "barn_id": barn_id, "student_profile_id": student_id},
            {
                "$set": {
                    "status": "revoked",
                    "revoked_at": now,
                    "revoked_by_user_id": user.get("id"),
                    "revocation_reason_present": bool(body and body.reason),
                    "updated_at": now,
                },
                "$inc": {"version": 1},
            },
        )
        await db[GUARDIAN_WORKFLOW_CONSENT_COLLECTION].update_many(
            {
                "barn_id": barn_id,
                "student_profile_id": student_id,
                "guardian_user_id": existing.get("guardian_user_id"),
                "status": CONSENT_GRANTED,
            },
            {
                "$set": {"status": "revoked", "revoked_at": now, "updated_at": now},
                "$inc": {"version": 1},
            },
        )
        await _touch_guardian_safeguarding_version(db, barn_id, student_id)
        gate = guardian_minor_workflow_gate(
            workflow=WORKFLOW_LESSON_READY,
            students=[student],
            guardian_links=[],
            workflow_consents=[],
            barn_id=barn_id,
            scope_reference=f"student_profile:{student_id}:lesson_ready",
            policy_version="lesson-ready-v1",
            action="relationship_revoked",
        )
        await audit.record(
            action="student_guardian.link_revoked",
            user=user,
            request=request,
            resource_type="guardian_link",
            resource_id=link_id,
            outcome="success",
            metadata=audit_safe_guardian_minor_metadata(gate),
            _db=db,
        )
        return {"ok": True, "status": "revoked"}

    @router.patch("/{student_id}/status")
    async def patch_student_status(
        student_id: str,
        body: StudentStatusPatch,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_student_manager(user)
        status = (body.status or "").strip().lower()
        if status not in STUDENT_PROFILE_STATUSES:
            raise HTTPException(status_code=422, detail="Invalid student profile status")
        student = await _load_student_or_404(db, user, student_id)
        barn_id = resolve_barn_id(user)
        links = await _active_guardian_links(db, barn_id, student_id)
        if status == "lesson_ready":
            gate = student_workflow_gate(student, links, workflow=WORKFLOW_LESSON_READY)
            if gate["decision"] != "allow":
                await _audit_minor_event(
                    db=db,
                    action="student_profile.status_blocked",
                    user=user,
                    request=request,
                    student=student,
                    workflow=WORKFLOW_LESSON_READY,
                    guardian_links=links,
                    outcome="denied",
                    status_code=409,
                )
                raise HTTPException(status_code=409, detail="Active guardian required")
            v11_gate = await _guard_student_workflow(
                db=db,
                student=student,
                workflow=WORKFLOW_LESSON_READY,
                scope_reference=f"student_profile:{student_id}:lesson_ready",
                policy_version="lesson-ready-v1",
                action="student_profile.status_lesson_ready",
            )
            if v11_gate["decision"] != "allow":
                await audit.record(
                    action="student_profile.status_blocked",
                    user=user,
                    request=request,
                    resource_type="student_profile",
                    resource_id=student_id,
                    outcome="denied",
                    status_code=409,
                    metadata=audit_safe_guardian_minor_metadata(v11_gate),
                    _db=db,
                )
                raise HTTPException(status_code=409, detail=guardian_minor_public_error_detail(v11_gate))

        await db[STUDENT_PROFILE_COLLECTION].update_one(
            {"id": student_id, "barn_id": barn_id},
            {"$set": {"status": status, "updated_at": _iso(_now_utc())}},
        )
        updated = await _load_student_or_404(db, user, student_id)
        await _audit_minor_event(
            db=db,
            action="student_profile.status_changed",
            user=user,
            request=request,
            student=updated,
            workflow=WORKFLOW_LESSON_READY,
            guardian_links=links,
        )
        return updated

    return router
