"""Authenticated support intake for pilot testers.

This is intentionally not an anonymous public helpdesk endpoint. Signed-in
users can file a support ticket that lands in the existing Admin Portal
support inbox, while audit metadata records only non-sensitive routing facts.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from core import audit
from core.tenancy import resolve_barn_id


SUPPORT_CATEGORIES = {
    "bug",
    "access",
    "billing",
    "data",
    "workflow",
    "feedback",
    "other",
}
SUPPORT_SEVERITIES = {"low", "medium", "high", "urgent"}
DEFAULT_STATUS = "new"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Input should be a valid string")
    cleaned = value.strip()
    return cleaned or None


class SupportTicketCreate(BaseModel):
    category: str = Field(default="bug", max_length=32)
    severity: str = Field(default="medium", max_length=32)
    subject: str = Field(..., min_length=3, max_length=140)
    message: str = Field(..., min_length=10, max_length=4000)
    page_url: Optional[str] = Field(default=None, max_length=500)
    device_context: Optional[str] = Field(default=None, max_length=500)
    preferred_contact: Optional[str] = Field(default="app", max_length=40)

    @field_validator(
        "category",
        "severity",
        "subject",
        "message",
        "page_url",
        "device_context",
        "preferred_contact",
        mode="before",
    )
    @classmethod
    def trim_text(cls, value):  # noqa: N805
        return _clean_text(value)

    @field_validator("category")
    @classmethod
    def valid_category(cls, value):  # noqa: N805
        normalized = (value or "bug").strip().lower()
        if normalized not in SUPPORT_CATEGORIES:
            raise ValueError("Invalid support category")
        return normalized

    @field_validator("severity")
    @classmethod
    def valid_severity(cls, value):  # noqa: N805
        normalized = (value or "medium").strip().lower()
        if normalized not in SUPPORT_SEVERITIES:
            raise ValueError("Invalid support severity")
        return normalized


def _safe_user_context(user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "role": user.get("role"),
        "platform_role": user.get("platform_role"),
        "barn_id": resolve_barn_id(user),
        "barn_name": user.get("barn_name"),
        "account_type": user.get("account_type"),
        "customer_type": user.get("customer_type"),
        "membership_status": user.get("membership_status"),
    }


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/support", tags=["support"])

    @router.post("/tickets", status_code=201)
    async def create_support_ticket(
        body: SupportTicketCreate,
        request: Request,
        user=Depends(get_current_user),
    ):
        ticket_id = f"ticket_{uuid.uuid4()}"
        now = _now_iso()
        barn_id = resolve_barn_id(user)
        ticket = {
            "id": ticket_id,
            "barn_id": barn_id,
            "subject": body.subject,
            "description": body.message,
            "channel": "in_app_pilot",
            "source": "pilot_support_form",
            "category": body.category,
            "severity": body.severity,
            "page_url": body.page_url,
            "device_context": body.device_context,
            "preferred_contact": body.preferred_contact,
            "submitter_user_id": user.get("id"),
            "submitter_email": user.get("email"),
            "submitter_name": user.get("full_name"),
            "submitter_context": _safe_user_context(user),
            "status": DEFAULT_STATUS,
            "assignee_user_id": None,
            "assignee_email": None,
            "internal_notes": [],
            "created_at": now,
            "updated_at": now,
            "resolved_at": None,
        }
        result = await db.support_tickets.insert_one(ticket)
        admin_ref = f"st_{result.inserted_id}"
        await audit.record(
            action="support.ticket.create",
            user=user,
            request=request,
            resource_type="support_ticket",
            resource_id=ticket_id,
            outcome="success",
            status_code=201,
            metadata={
                "category": body.category,
                "severity": body.severity,
                "channel": ticket["channel"],
                "message_present": True,
                "page_url_present": bool(body.page_url),
                "device_context_present": bool(body.device_context),
            },
        )
        return {
            "ok": True,
            "ticket": {
                "id": ticket_id,
                "admin_ref": admin_ref,
                "status": DEFAULT_STATUS,
                "category": body.category,
                "severity": body.severity,
                "created_at": now,
            },
        }

    @router.get("/tickets/{ticket_id}")
    async def get_own_support_ticket(ticket_id: str, user=Depends(get_current_user)):
        if not ticket_id.startswith("ticket_"):
            raise HTTPException(404, "Ticket not found.")
        ticket = await db.support_tickets.find_one(
            {"id": ticket_id, "submitter_user_id": user.get("id")},
            {
                "_id": 0,
                "id": 1,
                "subject": 1,
                "status": 1,
                "category": 1,
                "severity": 1,
                "created_at": 1,
                "updated_at": 1,
                "resolved_at": 1,
            },
        )
        if not ticket:
            raise HTTPException(404, "Ticket not found.")
        return {"ticket": ticket}

    return router
