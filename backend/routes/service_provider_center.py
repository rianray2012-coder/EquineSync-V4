"""RF10 service-provider operating center.

This route is grant-scoped and provider-role scoped. It reads explicit active
horse-provider assignments and projects only provider-safe horse/care context.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.provider_access import (
    grant_care_filter,
    grant_horse_filter,
    is_provider_user,
    provider_grants,
    require_provider_horse_access,
)


PROVIDER_NOTE_CATEGORIES = {"vet", "farrier", "body_worker", "rehab", "other"}


class ProviderVisitNoteIn(BaseModel):
    horse_id: str
    category: str = "other"
    title: str
    visit_date: Optional[str] = None
    notes: Optional[str] = None
    follow_up_due: Optional[str] = None


def _require_provider(user: Dict[str, Any]) -> None:
    if not is_provider_user(user):
        raise HTTPException(status_code=403, detail="Service provider account required")


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_horse(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "barn_id": row.get("barn_id"),
        "name": row.get("name"),
        "breed": row.get("breed"),
        "age": row.get("age"),
        "sex": row.get("sex"),
        "status": row.get("status"),
        "discipline": row.get("discipline"),
        "allergies": row.get("allergies") or [],
    }


def _safe_vet(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "horse_id": row.get("horse_id"),
        "type": row.get("type"),
        "title": row.get("title"),
        "date": row.get("date"),
        "vet_name": row.get("vet_name"),
        "follow_up_due": row.get("follow_up_due"),
    }


def _safe_farrier(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "horse_id": row.get("horse_id"),
        "date": row.get("date"),
        "farrier_name": row.get("farrier_name"),
        "next_visit_due": row.get("next_visit_due"),
        "shoes_on": row.get("shoes_on") or [],
    }


def _safe_note(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "horse_id": row.get("horse_id"),
        "category": row.get("category"),
        "title": row.get("title"),
        "visit_date": row.get("visit_date"),
        "follow_up_due": row.get("follow_up_due"),
        "created_at": row.get("created_at"),
    }


def _safe_grant(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "horse_id": row.get("horse_id"),
        "barn_id": row.get("barn_id"),
        "provider_id": row.get("provider_id"),
        "category": row.get("category"),
        "status": row.get("status"),
        "last_service_date": row.get("last_service_date"),
        "next_due_date": row.get("next_due_date"),
        "interval_days": row.get("interval_days"),
        "is_primary_for_horse": bool(row.get("is_primary_for_horse")),
    }


def build_router(*, db, get_current_user, new_id) -> APIRouter:
    router = APIRouter(prefix="/service-provider", tags=["service-provider"])

    @router.get("/operating-center")
    async def operating_center(user=Depends(get_current_user)):
        _require_provider(user)
        grants = await provider_grants(db, user)
        horses = await db.horses.find(grant_horse_filter(grants), {"_id": 0}).sort("name", 1).to_list(500)
        vet_records = await db.vet_records.find(grant_care_filter(grants), {"_id": 0}).sort("date", -1).to_list(50)
        farrier = await db.farrier_history.find(grant_care_filter(grants), {"_id": 0}).sort("date", -1).to_list(50)
        notes = await db.provider_visit_notes.find(grant_care_filter(grants), {"_id": 0}).sort("created_at", -1).to_list(50)
        return {
            "provider": {
                "id": user.get("id"),
                "name": user.get("full_name") or user.get("email"),
                "role": user.get("role"),
            },
            "counts": {
                "active_grants": len(grants),
                "shared_horses": len(horses),
                "recent_vet_records": len(vet_records),
                "recent_farrier_records": len(farrier),
                "visit_notes": len(notes),
            },
            "grants": [_safe_grant(row) for row in grants[:100]],
            "shared_horses": [_safe_horse(row) for row in horses],
            "recent_vet_records": [_safe_vet(row) for row in vet_records[:12]],
            "recent_farrier_records": [_safe_farrier(row) for row in farrier[:12]],
            "visit_notes": [_safe_note(row) for row in notes[:12]],
            "deferred": {
                "provider_invoices": "RF12 billing/payment/provider invoice truth",
                "provider_documents": "RF14 legal document/signature/storage truth",
                "provider_messaging": "RF13 delivery/recipient truth",
            },
        }

    @router.post("/visit-notes")
    async def create_visit_note(body: ProviderVisitNoteIn, user=Depends(get_current_user)):
        _require_provider(user)
        if body.category not in PROVIDER_NOTE_CATEGORIES:
            raise HTTPException(422, "category must be a known provider note type")
        horse = await require_provider_horse_access(db, user, body.horse_id)
        doc = body.model_dump()
        doc.update({
            "id": new_id(),
            "provider_user_id": user.get("id"),
            "provider_name": user.get("full_name") or user.get("email"),
            "barn_id": horse.get("barn_id"),
            "horse_name": horse.get("name"),
            "created_at": _iso_now(),
        })
        await db.provider_visit_notes.insert_one(doc)
        return _safe_note(doc)

    return router
