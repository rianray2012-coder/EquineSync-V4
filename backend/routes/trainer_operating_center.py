"""Trainer operating-center read model for RF9.

Read-only and trainer-role scoped. This route collects only stable-ID-linked
trainer work from existing lessons, training logs, training plans, and assigned
horses. It does not create packages, billing records, provider grants, or
multi-facility memberships.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from fastapi import APIRouter, Depends, HTTPException

from core.tenancy import barn_filter


TRAINER_PLAN_STATUSES = {"planned", "active"}


def _require_trainer(user: Dict[str, Any]) -> None:
    if (user.get("role") or "").strip().lower() != "trainer":
        raise HTTPException(status_code=403, detail="Trainer operating center is for trainer accounts")


def _trainer_work_filter(user: Dict[str, Any]) -> Dict[str, Any]:
    return barn_filter(user, {"$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}]})


def _trainer_plan_filter(user: Dict[str, Any]) -> Dict[str, Any]:
    return barn_filter(user, {"$or": [{"data.trainer_user_id": user.get("id")}, {"data.trainer_id": user.get("id")}]})


def _uniq(values: Iterable[str | None]) -> List[str]:
    out: List[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


async def _find_many(collection, query: Dict[str, Any], *, sort_field: str, sort_dir: int, limit: int) -> List[Dict[str, Any]]:
    return await collection.find(query, {"_id": 0}).sort(sort_field, sort_dir).to_list(limit)


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/trainer", tags=["trainer-operating-center"])

    @router.get("/directory")
    async def trainer_directory(user=Depends(get_current_user)):
        if (user.get("role") or "").strip().lower() not in {"admin", "barn_manager", "trainer"}:
            raise HTTPException(status_code=403, detail="Trainer directory access required")
        rows = await db.users.find(
            barn_filter(user, {"role": "trainer"}),
            {"_id": 0, "id": 1, "full_name": 1, "email": 1, "role": 1},
        ).sort("full_name", 1).to_list(200)
        return {"items": rows}

    @router.get("/operating-center")
    async def trainer_operating_center(user=Depends(get_current_user)):
        _require_trainer(user)
        lessons = await _find_many(db.lessons, _trainer_work_filter(user), sort_field="start_time", sort_dir=1, limit=100)
        training = await _find_many(db.training, _trainer_work_filter(user), sort_field="date", sort_dir=-1, limit=100)
        plans = await _find_many(db.training_plans, _trainer_plan_filter(user), sort_field="updated_at", sort_dir=-1, limit=100)

        horse_ids = _uniq(
            [row.get("horse_id") for row in lessons]
            + [row.get("horse_id") for row in training]
            + [(row.get("data") or {}).get("horse_id") for row in plans]
        )
        assigned_horses = await db.horses.find(
            barn_filter(user, {"$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}, {"id": {"$in": horse_ids}}]}),
            {"_id": 0, "id": 1, "name": 1, "status": 1, "discipline": 1, "training_goals": 1},
        ).sort("name", 1).to_list(100)

        rider_ids = _uniq([row.get("rider_id") for row in lessons])
        riders = []
        if rider_ids:
            riders = await db.riders.find(
                barn_filter(user, {"id": {"$in": rider_ids}}),
                {"_id": 0, "id": 1, "full_name": 1, "skill_level": 1, "goals": 1},
            ).sort("full_name", 1).to_list(100)

        active_plans = [
            plan for plan in plans
            if ((plan.get("data") or {}).get("status") or "planned") in TRAINER_PLAN_STATUSES
        ]
        upcoming_lessons = [row for row in lessons if not row.get("completed")]

        return {
            "trainer": {
                "id": user.get("id"),
                "name": user.get("full_name") or user.get("email"),
            },
            "counts": {
                "assigned_horses": len(assigned_horses),
                "riders": len(riders),
                "upcoming_lessons": len(upcoming_lessons),
                "recent_training": len(training),
                "active_plans": len(active_plans),
            },
            "assigned_horses": assigned_horses,
            "riders": riders,
            "upcoming_lessons": upcoming_lessons[:12],
            "recent_training": training[:12],
            "active_plans": active_plans[:12],
            "deferred": {
                "lesson_packages": "RF12 billing/package truth",
                "haul_ins": "RF9 founder priority decision or RF18 UAT depth",
                "multi_facility": "future account-membership/grant work; not RF9 broad provider grants",
            },
        }

    return router
