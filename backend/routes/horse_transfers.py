"""Horse Passport ownership transfer workflow.

This first slice intentionally transfers only owner-safe Passport categories.
It does not copy messages, invoices, documents, staff notes, raw daily checks,
alerts, provider contacts, or audit diffs. See
docs/HORSE_PASSPORT_TRANSFER_POLICY.md for the governing policy.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core import audit
from core.tenancy import barn_filter, resolve_barn_id
from routes.admin_portal._helpers import _redact_stripe_in_string
from routes.horse_ledger import build_owner_safe_transfer_care_summary


TRANSFER_POLICY_VERSION = "horse-passport-transfer-v1"
TRANSFER_REQUEST_COLLECTION = "horse_transfer_requests"
TRANSFER_ARCHIVE_COLLECTION = "horse_transfer_archives"

TRANSFER_STATUSES = {
    "owner_approved",
    "barn_approved",
    "pending_acceptance",
    "accepted",
    "canceled",
}
ACTIVE_TRANSFER_STATUSES = {"owner_approved", "barn_approved", "pending_acceptance"}
SAFE_TRANSFER_CATEGORIES = frozenset({
    "identity_public",
    "ownership_record",
    "care_summary",
})
BLOCKED_TRANSFER_CATEGORIES = frozenset({
    "raw_daily_checks",
    "alerts",
    "staff_notes",
    "audit_diffs",
    "health_documents",
    "vet_photos",
    "messages",
    "invoices",
    "billing_records",
    "provider_contacts",
    "provider_grants",
})
TRANSFER_ADMIN_ROLES = {"admin", "barn_manager"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _role(user: Dict[str, Any]) -> str:
    return (user.get("role") or "").strip().lower()


def _is_adminish(user: Dict[str, Any]) -> bool:
    return _role(user) in TRANSFER_ADMIN_ROLES


def _is_owner(user: Dict[str, Any], horse: Dict[str, Any]) -> bool:
    uid = user.get("id")
    if not uid:
        return False
    if horse.get("owner_id") == uid or horse.get("primary_owner_id") == uid:
        return True
    secondary = horse.get("secondary_owner_ids") or []
    return isinstance(secondary, list) and uid in secondary


def _requires_barn_approval(source_barn_id: Optional[str], destination_barn_id: Optional[str]) -> bool:
    return bool(destination_barn_id and destination_barn_id != source_barn_id)


def _require_safe_categories(categories: List[str]) -> List[str]:
    seen: Set[str] = set()
    cleaned: List[str] = []
    for raw in categories:
        if raw in seen:
            continue
        seen.add(raw)
        if raw in BLOCKED_TRANSFER_CATEGORIES:
            raise HTTPException(
                422,
                f"{raw} is blocked pending Product/Legal transfer policy.",
            )
        if raw not in SAFE_TRANSFER_CATEGORIES:
            raise HTTPException(422, f"{raw} is not a supported transfer category.")
        cleaned.append(raw)
    if not cleaned:
        raise HTTPException(422, "At least one transfer category is required.")
    return cleaned


def _clean_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _identity_public(horse: Dict[str, Any]) -> Dict[str, Any]:
    data = horse.get("data") if isinstance(horse.get("data"), dict) else {}
    return _scrub_strings({
        "id": horse.get("id"),
        "name": horse.get("name") or data.get("name"),
        "breed": horse.get("breed") or data.get("breed"),
        "color": horse.get("color") or data.get("color"),
        "discipline": horse.get("discipline") or data.get("discipline"),
        "photo_url": horse.get("photo_url") or data.get("photo_url"),
        "status": horse.get("status"),
    })


def _scrub_strings(value: Any) -> Any:
    if isinstance(value, str):
        return _redact_stripe_in_string(value)
    if isinstance(value, list):
        return [_scrub_strings(v) for v in value]
    if isinstance(value, dict):
        return {k: _scrub_strings(v) for k, v in value.items()}
    return value


class TransferCreate(BaseModel):
    horse_id: str
    new_owner_user_id: str
    destination_barn_id: Optional[str] = None
    categories: List[str] = Field(default_factory=lambda: [
        "identity_public",
        "ownership_record",
        "care_summary",
    ])


class TransferStatusPatch(BaseModel):
    reason: Optional[str] = None


def build_router(*, db, get_current_user, new_id) -> APIRouter:
    router = APIRouter(prefix="/horse-transfers", tags=["horse-transfers"])

    async def _load_transfer(transfer_id: str) -> Dict[str, Any]:
        transfer = await db[TRANSFER_REQUEST_COLLECTION].find_one(
            {"id": transfer_id}, {"_id": 0}
        )
        if not transfer:
            raise HTTPException(404, "Transfer request not found.")
        return transfer

    def _can_view_transfer(user: Dict[str, Any], transfer: Dict[str, Any]) -> bool:
        if user.get("id") in {
            transfer.get("from_owner_user_id"),
            transfer.get("to_owner_user_id"),
            transfer.get("created_by_user_id"),
        }:
            return True
        return _is_adminish(user) and resolve_barn_id(user) in {
            transfer.get("source_barn_id"),
            transfer.get("destination_barn_id"),
        }

    def _transfer_projection(transfer: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": transfer.get("id"),
            "horse_id": transfer.get("horse_id"),
            "status": transfer.get("status"),
            "categories": transfer.get("categories") or [],
            "policy_version": transfer.get("policy_version"),
            "from_owner_user_id": transfer.get("from_owner_user_id"),
            "to_owner_user_id": transfer.get("to_owner_user_id"),
            "source_barn_id": transfer.get("source_barn_id"),
            "destination_barn_id": transfer.get("destination_barn_id"),
            "created_at": transfer.get("created_at"),
            "updated_at": transfer.get("updated_at"),
            "accepted_at": transfer.get("accepted_at"),
            "canceled_at": transfer.get("canceled_at"),
            "owner_approved_at": transfer.get("owner_approved_at"),
            "barn_approved_at": transfer.get("barn_approved_at"),
            "requires_barn_approval": transfer.get("requires_barn_approval", False),
            "archive_id": transfer.get("archive_id"),
        }

    async def _build_export_snapshot(
        transfer: Dict[str, Any],
        horse: Dict[str, Any],
    ) -> Dict[str, Any]:
        categories = transfer.get("categories") or []
        snapshot: Dict[str, Any] = {
            "policy_version": TRANSFER_POLICY_VERSION,
            "transfer_id": transfer.get("id"),
            "horse_id": transfer.get("horse_id"),
            "categories": categories,
        }
        if "identity_public" in categories:
            snapshot["identity_public"] = _identity_public(horse)
        if "ownership_record" in categories:
            snapshot["ownership_record"] = {
                "from_owner_user_id": transfer.get("from_owner_user_id"),
                "to_owner_user_id": transfer.get("to_owner_user_id"),
                "source_barn_id": transfer.get("source_barn_id"),
                "destination_barn_id": transfer.get("destination_barn_id"),
            }
        if "care_summary" in categories:
            snapshot["care_summary"] = await build_owner_safe_transfer_care_summary(db, horse)
        return _scrub_strings(snapshot)

    @router.post("")
    async def create_transfer(body: TransferCreate, user=Depends(get_current_user)):
        categories = _require_safe_categories(body.categories)
        horse = await db.horses.find_one(
            barn_filter(user, {"id": body.horse_id}), {"_id": 0}
        )
        if not horse:
            raise HTTPException(404, "Horse not found.")
        if not _is_owner(user, horse):
            raise HTTPException(403, "Only the current owner can start a transfer.")

        new_owner = await db.users.find_one(
            {"id": body.new_owner_user_id, "role": "horse_owner"}, {"_id": 0}
        )
        if not new_owner:
            raise HTTPException(404, "New owner not found.")
        if body.destination_barn_id and new_owner.get("barn_id") and body.destination_barn_id != new_owner.get("barn_id"):
            raise HTTPException(422, "Destination barn must match the new owner's barn.")
        source_barn_id = horse.get("barn_id") or resolve_barn_id(user)
        requires_barn_approval = _requires_barn_approval(source_barn_id, body.destination_barn_id)
        existing = await db[TRANSFER_REQUEST_COLLECTION].find_one(
            {"horse_id": body.horse_id, "status": {"$in": sorted(ACTIVE_TRANSFER_STATUSES)}},
            {"_id": 0, "id": 1},
        )
        if existing:
            raise HTTPException(409, "A pending transfer already exists for this horse.")

        now = _now_iso()
        tid = f"htr_{uuid.uuid4().hex[:24]}"
        doc = {
            "id": tid,
            "horse_id": body.horse_id,
            "status": "owner_approved" if requires_barn_approval else "pending_acceptance",
            "categories": categories,
            "policy_version": TRANSFER_POLICY_VERSION,
            "from_owner_user_id": horse.get("primary_owner_id") or horse.get("owner_id") or user.get("id"),
            "to_owner_user_id": body.new_owner_user_id,
            "source_barn_id": source_barn_id,
            "destination_barn_id": body.destination_barn_id,
            "requires_barn_approval": requires_barn_approval,
            "created_by_user_id": user.get("id"),
            "created_by_role": user.get("role"),
            "created_at": now,
            "updated_at": now,
            "owner_approved_at": now,
            "owner_approved_by_user_id": user.get("id"),
            "barn_approved_at": None,
            "barn_approved_by_user_id": None,
            "accepted_at": None,
            "canceled_at": None,
        }
        await db[TRANSFER_REQUEST_COLLECTION].insert_one(doc)
        await audit.record(
            action="horse_transfer.created",
            user=user,
            barn_id=doc["source_barn_id"],
            resource_type="horse_transfer",
            resource_id=tid,
            metadata={
                "horse_id": body.horse_id,
                "categories": categories,
                "policy_version": TRANSFER_POLICY_VERSION,
                "requires_barn_approval": requires_barn_approval,
            },
            _db=db,
        )
        return _transfer_projection(doc)

    @router.get("/pending")
    async def pending_transfers(user=Depends(get_current_user)):
        uid = user.get("id")
        role = _role(user)
        clauses: List[Dict[str, Any]] = [
            {"to_owner_user_id": uid},
            {"from_owner_user_id": uid},
            {"created_by_user_id": uid},
        ]
        if role in TRANSFER_ADMIN_ROLES:
            bid = resolve_barn_id(user)
            clauses.extend([
                {"source_barn_id": bid},
                {"destination_barn_id": bid},
            ])
        rows = await db[TRANSFER_REQUEST_COLLECTION].find(
            {"status": {"$in": sorted(ACTIVE_TRANSFER_STATUSES)}, "$or": clauses},
            {"_id": 0},
        ).sort("created_at", -1).to_list(100)
        return {"items": [_transfer_projection(r) for r in rows]}

    @router.get("/{transfer_id}")
    async def get_transfer(transfer_id: str, user=Depends(get_current_user)):
        transfer = await _load_transfer(transfer_id)
        if not _can_view_transfer(user, transfer):
            raise HTTPException(404, "Transfer request not found.")
        return _transfer_projection(transfer)

    @router.get("/{transfer_id}/export-preview")
    async def export_preview(transfer_id: str, user=Depends(get_current_user)):
        transfer = await _load_transfer(transfer_id)
        horse = await db.horses.find_one({"id": transfer["horse_id"]}, {"_id": 0})
        if not horse:
            raise HTTPException(404, "Horse not found.")
        allowed = (
            _is_adminish(user) and resolve_barn_id(user) == transfer.get("source_barn_id")
        ) or user.get("id") in {
            transfer.get("from_owner_user_id"),
            transfer.get("to_owner_user_id"),
            transfer.get("created_by_user_id"),
        }
        if not allowed:
            raise HTTPException(404, "Transfer request not found.")
        return await _build_export_snapshot(transfer, horse)

    @router.post("/{transfer_id}/cancel")
    async def cancel_transfer(
        transfer_id: str,
        body: TransferStatusPatch,
        user=Depends(get_current_user),
    ):
        transfer = await _load_transfer(transfer_id)
        if transfer.get("status") not in ACTIVE_TRANSFER_STATUSES:
            raise HTTPException(409, "Only active transfers can be canceled.")
        allowed = (
            user.get("id") == transfer.get("created_by_user_id")
            or user.get("id") == transfer.get("from_owner_user_id")
            or (_is_adminish(user) and resolve_barn_id(user) == transfer.get("source_barn_id"))
        )
        if not allowed:
            raise HTTPException(404, "Transfer request not found.")
        updates = {"status": "canceled", "canceled_at": _now_iso(), "updated_at": _now_iso()}
        await db[TRANSFER_REQUEST_COLLECTION].update_one({"id": transfer_id}, {"$set": updates})
        await audit.record(
            action="horse_transfer.canceled",
            user=user,
            barn_id=transfer.get("source_barn_id"),
            resource_type="horse_transfer",
            resource_id=transfer_id,
            metadata={"reason_provided": bool(body.reason)},
            _db=db,
        )
        updated = await db[TRANSFER_REQUEST_COLLECTION].find_one({"id": transfer_id}, {"_id": 0})
        return _transfer_projection(updated)

    @router.post("/{transfer_id}/barn-approve")
    async def barn_approve_transfer(
        transfer_id: str,
        body: TransferStatusPatch,
        user=Depends(get_current_user),
    ):
        transfer = await _load_transfer(transfer_id)
        if transfer.get("status") != "owner_approved":
            raise HTTPException(409, "Only owner-approved transfers can receive barn approval.")
        if not transfer.get("requires_barn_approval"):
            raise HTTPException(409, "Barn approval is not required for this transfer.")
        if not (_is_adminish(user) and resolve_barn_id(user) == transfer.get("source_barn_id")):
            raise HTTPException(404, "Transfer request not found.")
        now = _now_iso()
        updates = {
            "status": "barn_approved",
            "barn_approved_at": now,
            "barn_approved_by_user_id": user.get("id"),
            "barn_approval_reason_provided": bool(body.reason),
            "updated_at": now,
        }
        await db[TRANSFER_REQUEST_COLLECTION].update_one({"id": transfer_id}, {"$set": updates})
        await audit.record(
            action="horse_transfer.barn_approved",
            user=user,
            barn_id=transfer.get("source_barn_id"),
            resource_type="horse_transfer",
            resource_id=transfer_id,
            metadata={
                "horse_id": transfer.get("horse_id"),
                "policy_version": TRANSFER_POLICY_VERSION,
                "reason_provided": bool(body.reason),
            },
            _db=db,
        )
        updated = await db[TRANSFER_REQUEST_COLLECTION].find_one({"id": transfer_id}, {"_id": 0})
        return _transfer_projection(updated)

    @router.post("/{transfer_id}/accept")
    async def accept_transfer(
        transfer_id: str,
        body: TransferStatusPatch,
        user=Depends(get_current_user),
    ):
        transfer = await _load_transfer(transfer_id)
        if transfer.get("requires_barn_approval") and transfer.get("status") != "barn_approved":
            raise HTTPException(409, "Barn approval is required before new-owner acceptance.")
        if transfer.get("status") not in {"pending_acceptance", "barn_approved"}:
            raise HTTPException(409, "Transfer must be ready for new-owner acceptance.")
        if user.get("id") != transfer.get("to_owner_user_id"):
            raise HTTPException(404, "Transfer request not found.")
        horse = await db.horses.find_one({"id": transfer["horse_id"]}, {"_id": 0})
        if not horse:
            raise HTTPException(404, "Horse not found.")

        snapshot = await _build_export_snapshot(transfer, horse)
        now = _now_iso()
        secondary = [
            uid for uid in _clean_list(horse.get("secondary_owner_ids"))
            if uid not in {transfer.get("from_owner_user_id"), transfer.get("to_owner_user_id")}
        ]
        horse_updates = {
            "owner_id": transfer.get("to_owner_user_id"),
            "primary_owner_id": transfer.get("to_owner_user_id"),
            "secondary_owner_ids": secondary,
            "ownership_transfer_last_id": transfer_id,
            "ownership_transfer_last_at": now,
        }
        if transfer.get("destination_barn_id"):
            horse_updates["barn_id"] = transfer["destination_barn_id"]

        archive = {
            "id": f"hta_{uuid.uuid4().hex[:24]}",
            "transfer_id": transfer_id,
            "horse_id": transfer["horse_id"],
            "policy_version": TRANSFER_POLICY_VERSION,
            "created_at": now,
            "snapshot": snapshot,
        }
        await db[TRANSFER_ARCHIVE_COLLECTION].insert_one(archive)
        await db.horses.update_one({"id": transfer["horse_id"]}, {"$set": horse_updates})
        await db[TRANSFER_REQUEST_COLLECTION].update_one(
            {"id": transfer_id},
            {"$set": {
                "status": "accepted",
                "accepted_at": now,
                "updated_at": now,
                "acceptance_reason_provided": bool(body.reason),
                "archive_id": archive["id"],
            }},
        )
        await audit.record(
            action="horse_transfer.accepted",
            user=user,
            barn_id=transfer.get("destination_barn_id") or transfer.get("source_barn_id"),
            resource_type="horse_transfer",
            resource_id=transfer_id,
            metadata={
                "horse_id": transfer["horse_id"],
                "categories": transfer.get("categories") or [],
                "policy_version": TRANSFER_POLICY_VERSION,
                "archive_id": archive["id"],
            },
            _db=db,
        )
        updated = await db[TRANSFER_REQUEST_COLLECTION].find_one({"id": transfer_id}, {"_id": 0})
        return _transfer_projection(updated)

    return router
