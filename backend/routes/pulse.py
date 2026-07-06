"""Build-Next-15A - Today Pulse read-only data contract.

This route gives role-home pages a stable, privacy-safe set of counts and
visibility flags. It intentionally does not return task rows, care payloads,
alert triggers, audit diffs, Stripe IDs, or staff notes.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.account_context import (
    is_facility_context,
    is_individual_owner_context,
    resolve_active_context,
)
from core.permissions import PLATFORM_ROLES


SCHEMA_VERSION = "bn15a.today_pulse.v1"
VISIBILITY_POLICY_SCHEMA_VERSION = "bn15c_b.barn_visibility_policy.v1"
VISIBILITY_POLICY_COLLECTION = "barn_visibility_policies"
VISIBILITY_POLICY_MODES = {"siloed", "community", "custom"}
DEFAULT_OWNER_SAFE_SUMMARY_COUNTS = {"total_horses": False}
COMPLETED_TASK_STATUSES = {"completed", "skipped", "cancelled"}
MANAGER_ROLES = {"admin", "barn_admin", "barn_owner", "barn_manager"}
STAFF_ROLES = {"groom", "working_student", "trainer"}
OWNER_SAFE_ROLES = {"horse_owner", "parent", "rider"}


class BarnVisibilityPolicyIn(BaseModel):
    mode: str = Field(default="siloed")
    owner_safe_summary_counts: Dict[str, bool] = Field(default_factory=dict)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _clean(value: Any) -> str:
    return str(value or "").strip().lower()


def _today_bounds(now: Optional[datetime] = None) -> tuple[str, str]:
    current = now or _now_utc()
    start = current.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start.isoformat(), end.isoformat()


async def _count(collection, query: Dict[str, Any]) -> int:
    return int(await collection.count_documents(query))


async def _find_one(collection, query: Dict[str, Any], projection: Optional[Dict[str, Any]] = None):
    if projection is None:
        return await collection.find_one(query)
    return await collection.find_one(query, projection)


def _empty_card(visible: bool = False, tone: str = "neutral") -> Dict[str, Any]:
    return {"visible": visible, "count": 0, "tone": tone}


def _privacy_contract() -> Dict[str, bool]:
    return {
        "counts_only": True,
        "raw_payloads_included": False,
        "staff_notes_included": False,
        "alert_triggers_included": False,
        "source_check_ids_included": False,
        "audit_diffs_included": False,
        "auth_tokens_included": False,
        "passwords_included": False,
        "stripe_ids_included": False,
    }


def _deferred_items() -> list[str]:
    return [
        "cross-role_screenshot_evidence",
        "barn_visibility_policy_cross_role_screenshot_evidence",
        "notification_delivery_changes",
        "billing_enforcement_changes",
    ]


def normalize_barn_visibility_policy(doc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Return the safe barn visibility policy shape used by Today Pulse.

    Unknown modes fail closed to siloed. Unknown toggle keys are ignored so a
    planted or stale policy cannot expose future counts before code supports
    them deliberately.
    """
    raw_mode = _clean((doc or {}).get("mode"))
    mode = raw_mode if raw_mode in VISIBILITY_POLICY_MODES else "siloed"
    raw_counts = (doc or {}).get("owner_safe_summary_counts") or {}
    counts = {
        key: bool(raw_counts.get(key, default))
        for key, default in DEFAULT_OWNER_SAFE_SUMMARY_COUNTS.items()
    }
    if mode == "siloed":
        counts["total_horses"] = False
    elif mode == "community":
        counts["total_horses"] = True
    return {
        "schema_version": VISIBILITY_POLICY_SCHEMA_VERSION,
        "mode": mode,
        "owner_safe_summary_counts": counts,
    }


async def _barn_visibility_policy(db, barn_id: str) -> Dict[str, Any]:
    doc = await _find_one(
        db[VISIBILITY_POLICY_COLLECTION],
        {"barn_id": barn_id},
        {"_id": 0, "mode": 1, "owner_safe_summary_counts": 1},
    )
    return normalize_barn_visibility_policy(doc)


def _owner_safe_total_horses_enabled(policy: Dict[str, Any]) -> bool:
    counts = policy.get("owner_safe_summary_counts") or {}
    return bool(counts.get("total_horses"))


def _policy_response(policy: Dict[str, Any], barn_id: str) -> Dict[str, Any]:
    return {
        "barn_id": barn_id,
        "schema_version": policy["schema_version"],
        "mode": policy["mode"],
        "owner_safe_summary_counts": policy["owner_safe_summary_counts"],
        "deferred": [
            "owner_safe_open_alert_count_visibility",
            "owner_safe_urgent_alert_count_visibility",
        ],
    }


def _require_visibility_policy_manager(context: Dict[str, Any]) -> None:
    if _clean(context.get("role")) not in MANAGER_ROLES:
        raise HTTPException(403, "Barn visibility policy requires manager access.")
    if _clean(context.get("membership_status")) != "active":
        raise HTTPException(403, "Barn visibility policy requires active facility membership.")


async def _resolve_visibility_policy_barn(db, user: Dict[str, Any], account_id: Optional[str] = None) -> str:
    context = await resolve_active_context(db, user, requested_account_id=account_id)
    active = context.get("active_context")
    if not is_facility_context(active):
        raise HTTPException(404, "Facility context not found.")
    _require_visibility_policy_manager(active)
    barn_id = active.get("barn_id") or active.get("account_id")
    if await _facility_disabled(db, barn_id):
        raise HTTPException(403, "Facility unavailable.")
    return barn_id


async def _facility_disabled(db, barn_id: str) -> bool:
    barn = await _find_one(db.barns, {"id": barn_id}, {"_id": 0, "status": 1})
    return bool(barn and barn.get("status") == "disabled")


async def _build_platform_cards(db) -> Dict[str, Dict[str, Any]]:
    return {
        "todays_work": _empty_card(False),
        "horse_care": _empty_card(False),
        "owner_requests": _empty_card(False),
        "setup": _empty_card(False),
        "plan_usage": _empty_card(False),
        "platform": {
            "visible": True,
            "users": await _count(db.users, {}),
            "facilities": await _count(db.barns, {}),
            "open_owner_requests": await _count(
                db.service_requests,
                {"source": "owner_care_ledger", "status": {"$in": ["new", "in_progress"]}},
            ),
            "open_alerts": await _count(
                db.horse_ledger_alerts,
                {"status": {"$in": ["open", "acknowledged"]}},
            ),
            "tone": "neutral",
        },
    }


async def _build_facility_cards(
    db,
    *,
    barn_id: str,
    user: Dict[str, Any],
    tenant_id: str,
    effective_role: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    today_start, today_end = _today_bounds()
    role = _clean(effective_role or user.get("role"))
    manager_visible = role in MANAGER_ROLES
    staff_visible = manager_visible or role in STAFF_ROLES
    owner_safe_visible = role in OWNER_SAFE_ROLES
    visibility_policy = await _barn_visibility_policy(db, barn_id)
    owner_safe_total_horses = owner_safe_visible and _owner_safe_total_horses_enabled(visibility_policy)

    task_base = {
        "tenant_id": tenant_id,
        "barn_id": barn_id,
        "scheduled_at": {"$gte": today_start, "$lt": today_end},
    }
    pending_tasks = await _count(db.tasks, {**task_base, "status": {"$nin": list(COMPLETED_TASK_STATUSES)}})
    completed_tasks = await _count(db.tasks, {**task_base, "status": {"$in": list(COMPLETED_TASK_STATUSES)}})
    horse_count = await _count(db.horses, {"barn_id": barn_id})
    open_alerts = await _count(
        db.horse_ledger_alerts,
        {"barn_id": barn_id, "status": {"$in": ["open", "acknowledged"]}},
    )
    urgent_alerts = await _count(
        db.horse_ledger_alerts,
        {"barn_id": barn_id, "status": {"$in": ["open", "acknowledged"]}, "severity": "urgent"},
    )
    owner_requests = await _count(
        db.service_requests,
        {"barn_id": barn_id, "source": "owner_care_ledger", "status": {"$in": ["new", "in_progress"]}},
    )
    progress = await _find_one(db.onboarding_progress, {"user_id": user.get("id")}, {"_id": 0, "completed": 1, "steps": 1})
    usage = await _find_one(db.account_usage_limits, {"account_id": barn_id}, {"_id": 0})
    horse_limit = None if not usage else usage.get("horse_limit")
    over_horse_limit = bool(isinstance(horse_limit, int) and horse_count > horse_limit)

    return {
        "todays_work": {
            "visible": staff_visible,
            "pending": pending_tasks if staff_visible else 0,
            "completed": completed_tasks if staff_visible else 0,
            "count": (pending_tasks + completed_tasks) if staff_visible else 0,
            "tone": "attention" if staff_visible and pending_tasks else "neutral",
        },
        "horse_care": {
            "visible": staff_visible or owner_safe_visible,
            "horses": horse_count if (staff_visible or owner_safe_total_horses) else 0,
            "open_alerts": open_alerts if staff_visible else 0,
            "urgent_alerts": urgent_alerts if staff_visible else 0,
            "visibility_policy": visibility_policy["mode"],
            "tone": "urgent" if staff_visible and urgent_alerts else ("attention" if staff_visible and open_alerts else "neutral"),
        },
        "owner_requests": {
            "visible": manager_visible,
            "pending": owner_requests if manager_visible else 0,
            "count": owner_requests if manager_visible else 0,
            "tone": "attention" if manager_visible and owner_requests else "neutral",
        },
        "setup": {
            "visible": True,
            "completed": bool(progress and progress.get("completed")),
            "completion_percent": _completion_percent(progress),
            "tone": "neutral",
        },
        "plan_usage": {
            "visible": manager_visible,
            "active_horses": horse_count if manager_visible else 0,
            "horse_limit": horse_limit if manager_visible else None,
            "over_limit": over_horse_limit if manager_visible else False,
            "tone": "attention" if manager_visible and over_horse_limit else "neutral",
        },
        "platform": _empty_card(False),
    }


def _completion_percent(progress: Optional[Dict[str, Any]]) -> Optional[int]:
    if not progress:
        return None
    steps = progress.get("steps") or {}
    if not isinstance(steps, dict) or not steps:
        return 100 if progress.get("completed") else 0
    completed = sum(1 for status in steps.values() if status == "complete")
    return round(100 * completed / max(1, len(steps)))


async def _build_individual_owner_cards(db, *, user: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    progress = await _find_one(db.onboarding_progress, {"user_id": user.get("id")}, {"_id": 0, "completed": 1, "steps": 1})
    user_id = user.get("id")
    horse_q = {"$or": [{"primary_owner_id": user_id}, {"owner_id": user_id}]} if user_id else {"id": "__none__"}
    horse_count = await _count(db.horses, horse_q)

    return {
        "todays_work": _empty_card(False),
        "horse_care": {
            "visible": True,
            "horses": horse_count,
            "open_alerts": 0,
            "urgent_alerts": 0,
            "tone": "neutral",
        },
        "owner_requests": _empty_card(False),
        "setup": {
            "visible": True,
            "completed": bool(progress and progress.get("completed")),
            "completion_percent": _completion_percent(progress),
            "tone": "neutral",
        },
        "plan_usage": _empty_card(False),
        "platform": _empty_card(False),
    }


def _none_cards() -> Dict[str, Dict[str, Any]]:
    return {
        "todays_work": _empty_card(False),
        "horse_care": _empty_card(False),
        "owner_requests": _empty_card(False),
        "setup": _empty_card(False),
        "plan_usage": _empty_card(False),
        "platform": _empty_card(False),
    }


async def build_today_pulse(
    db,
    user: Dict[str, Any],
    *,
    account_id: Optional[str] = None,
    tenant_id: str = "default",
) -> Dict[str, Any]:
    """Build a privacy-safe role-home pulse response.

    This is kept separate from the FastAPI route so focused tests can exercise
    the contract without needing a live server.
    """
    context = await resolve_active_context(db, user, requested_account_id=account_id)
    active = context.get("active_context")
    platform_role = context.get("platform_role")
    role = _clean(user.get("role"))

    scope: Dict[str, Any] = {
        "kind": "none",
        "account_id": None,
        "barn_id": None,
        "role": role or None,
        "platform_role": platform_role,
        "requested_account_id": account_id,
        "requested_context_found": context.get("requested_context_found"),
    }

    if platform_role in PLATFORM_ROLES:
        scope.update({"kind": "platform"})
        cards = await _build_platform_cards(db)
    elif is_facility_context(active):
        barn_id = active.get("barn_id") or active.get("account_id")
        if await _facility_disabled(db, barn_id):
            raise HTTPException(403, "Facility unavailable.")
        effective_role = _clean(active.get("role"))
        scope.update({
            "kind": "facility",
            "account_id": active.get("account_id"),
            "barn_id": barn_id,
            "role": effective_role or None,
        })
        cards = await _build_facility_cards(
            db,
            barn_id=barn_id,
            user=user,
            tenant_id=tenant_id,
            effective_role=effective_role,
        )
    elif is_individual_owner_context(active):
        scope.update({
            "kind": "individual_owner",
            "account_id": active.get("account_id"),
            "barn_id": None,
        })
        cards = await _build_individual_owner_cards(db, user=user)
    else:
        cards = _none_cards()

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now_utc().isoformat(),
        "scope": scope,
        "cards": cards,
        "privacy": _privacy_contract(),
        "deferred": _deferred_items(),
    }


def build_router(db, get_current_user, tenant_id: str) -> APIRouter:
    router = APIRouter(prefix="/pulse", tags=["pulse"])

    @router.get("/today")
    async def today_pulse(account_id: Optional[str] = None, user=Depends(get_current_user)):
        return await build_today_pulse(db, user, account_id=account_id, tenant_id=tenant_id)

    @router.get("/visibility-policy")
    async def get_visibility_policy(account_id: Optional[str] = None, user=Depends(get_current_user)):
        barn_id = await _resolve_visibility_policy_barn(db, user, account_id=account_id)
        return _policy_response(await _barn_visibility_policy(db, barn_id), barn_id)

    @router.put("/visibility-policy")
    async def put_visibility_policy(
        body: BarnVisibilityPolicyIn,
        account_id: Optional[str] = None,
        user=Depends(get_current_user),
    ):
        barn_id = await _resolve_visibility_policy_barn(db, user, account_id=account_id)
        policy = normalize_barn_visibility_policy(body.model_dump())
        now = _now_utc().isoformat()
        await db[VISIBILITY_POLICY_COLLECTION].update_one(
            {"barn_id": barn_id},
            {
                "$set": {
                    "barn_id": barn_id,
                    "schema_version": VISIBILITY_POLICY_SCHEMA_VERSION,
                    "mode": policy["mode"],
                    "owner_safe_summary_counts": policy["owner_safe_summary_counts"],
                    "updated_at": now,
                    "updated_by": user.get("id"),
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
        return _policy_response(policy, barn_id)

    return router
