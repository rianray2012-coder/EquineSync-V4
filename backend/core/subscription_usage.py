"""Soft usage and add-on prompt helpers for Phase 15R-D.

These helpers are read-only projections. They do not enforce limits, mutate
Stripe subscription items, validate Apple receipts, or write database rows.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


USAGE_WARNING_THRESHOLD = 0.8
USAGE_LIMIT_KEYS = (
    "horses",
    "users",
    "staff",
    "owner_managers",
    "lesson_participants",
    "storage_gb",
)

HORSE_ADDON_BY_PLAN = {
    "starter_barn": "additional_horse_starter",
    "advanced_barn": "additional_horse_advanced",
    "elite_barn": "additional_horse_advanced",
}

ADDON_BY_LIMIT = {
    "users": "additional_staff_seat",
    "staff": "additional_staff_seat",
    "owner_managers": "additional_owner_manager_seat",
    "lesson_participants": "additional_lesson_participant",
    "storage_gb": "extra_storage",
}


def _finite_limit(value: Any) -> int | None:
    if value is None:
        return None
    try:
        limit = int(value)
    except (TypeError, ValueError):
        return None
    return limit


def _int_count(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def suggested_addon_code(limit_key: str, plan_code: str | None = None) -> str | None:
    key = (limit_key or "").strip().lower()
    plan = (plan_code or "").strip().lower()
    if key == "horses":
        return HORSE_ADDON_BY_PLAN.get(plan, "additional_horse_standard")
    if key == "owner_managers" and plan == "elite_barn":
        return "elite_owner_manager_seat"
    return ADDON_BY_LIMIT.get(key)


def usage_pressure(used: Any, limit: Any) -> str:
    used_i = _int_count(used)
    limit_i = _finite_limit(limit)
    if limit_i is None:
        return "unlimited"
    if limit_i <= 0:
        return "over" if used_i > 0 else "ok"
    if used_i >= limit_i:
        return "over"
    if used_i / limit_i >= USAGE_WARNING_THRESHOLD:
        return "approaching"
    return "ok"


def build_usage_entry(
    *,
    key: str,
    used: Any,
    limit: Any,
    plan_code: str | None = None,
) -> dict[str, Any]:
    used_i = _int_count(used)
    limit_i = _finite_limit(limit)
    pressure = usage_pressure(used_i, limit_i)
    finite = limit_i is not None
    entry = {
        "used": used_i,
        "limit": limit_i,
        "remaining": None if not finite else max(0, int(limit_i or 0) - used_i),
        "pressure": pressure,
        "soft_only": True,
        "upgrade_prompt": pressure in {"approaching", "over"},
    }
    addon_code = suggested_addon_code(key, plan_code)
    if entry["upgrade_prompt"] and addon_code:
        entry["suggested_addon_code"] = addon_code
    return entry


def build_addon_suggestions(usage: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    for key in USAGE_LIMIT_KEYS:
        entry = usage.get(key) or {}
        addon_code = entry.get("suggested_addon_code")
        if not entry.get("upgrade_prompt") or not addon_code:
            continue
        suggestions.append({
            "usage_key": key,
            "pressure": entry.get("pressure"),
            "addon_code": addon_code,
            "soft_only": True,
        })
    return suggestions


def scrub_addon_catalog_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return an app-safe add-on catalog row without operational Price IDs."""
    return {
        "addon_code": row.get("addon_code") or row.get("id"),
        "billing_provider": row.get("billing_provider"),
        "billing_channel": row.get("billing_channel"),
        "recurring": bool(row.get("recurring", True)),
        "limit_field": row.get("limit_field"),
        "quantity_field": row.get("quantity_field"),
        "is_active": bool(row.get("is_active", True)),
    }


def scrub_addon_catalog(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [scrub_addon_catalog_row(row) for row in rows]
