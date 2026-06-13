"""routes/admin_review.py — Admin review queue for marketplace signups.

Trainers / barn owners / service providers self-register via /auth/signup with
role_status="pending_review". This module surfaces the queue and the
approve/reject actions to admins (capability: barn:manage).

Reject = soft (role_status="rejected"); the account stays for audit/support
history per the user's explicit choice (no hard delete).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.permissions import require


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RejectBody(BaseModel):
    reason: Optional[str] = None  # admin note, surfaced back to the user


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/admin", tags=["admin-review"])

    @router.get("/review-queue")
    async def list_pending(user=Depends(get_current_user)):
        """List all marketplace users awaiting verification."""
        require(user, "barn:manage")
        cursor = db.users.find(
            {"role_status": "pending_review"},
            {"_id": 0, "password_hash": 0},
        ).sort("created_at", -1).limit(200)
        items = await cursor.to_list(length=200)
        return {"items": items, "count": len(items)}

    @router.get("/review-queue/history")
    async def list_history(user=Depends(get_current_user)):
        """Approved + rejected users (for audit / support context)."""
        require(user, "barn:manage")
        cursor = db.users.find(
            {"role_status": {"$in": ["approved", "rejected"]},
             "signup_source": "marketplace"},
            {"_id": 0, "password_hash": 0},
        ).sort("review_decided_at", -1).limit(200)
        items = await cursor.to_list(length=200)
        return {"items": items, "count": len(items)}

    @router.post("/review-queue/{user_id}/approve")
    async def approve(user_id: str, user=Depends(get_current_user)):
        require(user, "barn:manage")
        target = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
        if not target:
            raise HTTPException(404, "User not found.")
        if target.get("role_status") != "pending_review":
            raise HTTPException(409, f"User is not pending review (current: {target.get('role_status')}).")
        update = {
            "role_status": "approved",
            "review_decided_at": _now_iso(),
            "review_decided_by": user["id"],
        }
        await db.users.update_one({"id": user_id}, {"$set": update})
        # Audit trail row.
        await db.review_decisions.insert_one({
            "user_id": user_id,
            "decision": "approved",
            "decided_by": user["id"],
            "decided_at": update["review_decided_at"],
            "role": target.get("role"),
        })
        target.update(update)
        return target

    @router.post("/review-queue/{user_id}/reject")
    async def reject(user_id: str, body: RejectBody, user=Depends(get_current_user)):
        require(user, "barn:manage")
        target = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
        if not target:
            raise HTTPException(404, "User not found.")
        if target.get("role_status") != "pending_review":
            raise HTTPException(409, f"User is not pending review (current: {target.get('role_status')}).")
        update = {
            "role_status": "rejected",
            "review_decided_at": _now_iso(),
            "review_decided_by": user["id"],
            "review_rejection_reason": (body.reason or "").strip() or None,
        }
        await db.users.update_one({"id": user_id}, {"$set": update})
        await db.review_decisions.insert_one({
            "user_id": user_id,
            "decision": "rejected",
            "decided_by": user["id"],
            "decided_at": update["review_decided_at"],
            "role": target.get("role"),
            "reason": update["review_rejection_reason"],
        })
        target.update(update)
        return target

    return router
