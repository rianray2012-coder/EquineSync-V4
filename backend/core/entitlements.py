"""Provider-neutral entitlement helpers for Phase 15R-A.

This module intentionally does not create checkout sessions, validate Apple
receipts, process Stripe webhooks, or write database rows. It defines the
canonical plan-code and limit vocabulary that future Stripe/Apple billing
adapters can plug into without changing app-facing entitlement shapes.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from core.billing_provisioning import PLAN_CATALOG, PLAN_ORDER


CANONICAL_PLAN_CODES = tuple(tier["tier_code"] for tier in PLAN_CATALOG)

PLAN_CODE_ALIASES = {
    "starter": "starter_barn",
    "professional": "advanced_barn",
    "trainer_no_lessons": "trainer_no_lesson",
    "trainer_lessons_15": "trainer_lesson_15",
    "trainer_lessons_50": "trainer_lesson_50",
}

LEGACY_PLAN_CODE_ALIASES = {
    "starter",
    "professional",
}

LIMIT_FIELDS = (
    "horse_limit",
    "staff_limit",
    "owner_manager_limit",
    "lesson_participant_limit",
)

USAGE_COUNTERS = (
    "active_horses",
    "staff_seats",
    "owner_manager_seats",
    "lesson_participants",
)

PAYMENT_PROVIDERS = ("stripe", "apple", "manual", "comped")
PURCHASE_PLATFORMS = ("web", "ios", "admin")

INVITED_OWNER_PLAN_CODE = "free"
DEFAULT_BILLING_PROVIDER = "manual"
DEFAULT_PURCHASE_PLATFORM = "admin"
ENTITLEMENT_ACTIVE_STATUSES = ("active", "trialing", "past_due")
INACTIVE_ENTITLEMENT_FALLBACK_PLAN_CODE = INVITED_OWNER_PLAN_CODE


def normalize_subscription_status(value: str | None) -> str:
    """Normalize subscription status spellings used across Stripe/legacy rows."""
    raw = (value or "active").strip().lower()
    if raw == "cancelled":
        return "canceled"
    return raw


def is_entitlement_active_status(value: str | None) -> bool:
    """Whether a subscription status should grant paid-plan limits."""
    return normalize_subscription_status(value) in ENTITLEMENT_ACTIVE_STATUSES


def normalize_plan_code(value: str | None) -> str:
    """Return the canonical plan_code for a legacy tier/lookup code."""
    raw = (value or "").strip().lower()
    return PLAN_CODE_ALIASES.get(raw, raw)


def assert_known_plan_code(value: str | None) -> str:
    """Normalize a plan code and fail fast when it is not in the catalog."""
    code = normalize_plan_code(value)
    if code not in CANONICAL_PLAN_CODES:
        raise ValueError(f"Unknown plan_code: {value!r}")
    return code


def plan_by_code(plan_code: str | None) -> dict[str, Any]:
    code = assert_known_plan_code(plan_code)
    for plan in PLAN_CATALOG:
        if plan["tier_code"] == code:
            return deepcopy(plan)
    raise ValueError(f"Unknown plan_code: {plan_code!r}")


def _limit_value(feature_limits: Mapping[str, Any], key: str, default: Any = 0) -> Any:
    value = feature_limits.get(key, default)
    return value


def feature_limits_to_entitlement_limits(feature_limits: Mapping[str, Any] | None) -> dict[str, Any]:
    """Translate legacy Phase 15 feature_limits into Phase 15R limit names."""
    limits = feature_limits or {}
    return {
        "horse_limit": _limit_value(limits, "horses"),
        "staff_limit": _limit_value(limits, "staff_seats"),
        "owner_manager_limit": _limit_value(limits, "owner_manager_seats"),
        "lesson_participant_limit": _limit_value(limits, "lesson_participants"),
    }


def included_limits_for_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    limits = feature_limits_to_entitlement_limits(plan.get("feature_limits") or {})
    return {
        "included_horses": limits["horse_limit"],
        "included_staff": limits["staff_limit"],
        "included_owner_managers": limits["owner_manager_limit"],
        "included_lesson_participants": limits["lesson_participant_limit"],
    }


def customer_type_for_plan(plan_code: str | None) -> str:
    code = assert_known_plan_code(plan_code)
    if code == "free":
        return "invited_owner_portal"
    if code in {"individual_owner", "private_owner_plus"}:
        return "individual_owner"
    if code in {"starter_barn", "advanced_barn", "elite_barn"}:
        return "facility"
    if code in {"trainer_no_lesson", "trainer_lesson_15", "trainer_lesson_50"}:
        return "trainer"
    if code == "enterprise":
        return "enterprise"
    if code == "community_program":
        return "community"
    return "unknown"


def billing_channels_for_plan(plan: Mapping[str, Any]) -> list[str]:
    code = assert_known_plan_code(plan.get("tier_code") or plan.get("plan_code"))
    if code == INVITED_OWNER_PLAN_CODE:
        return ["manual"]
    if plan.get("contact_sales"):
        return ["manual", "comped"]
    if plan.get("stripe_provisioned"):
        # Stripe handles web purchases. Apple product IDs land later but the
        # entitlement shape is ready for iOS-originated subscriptions.
        return ["stripe", "apple"]
    return ["manual"]


def plan_to_subscription_plan_shape(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Future `subscription_plans` row shape, derived from today's catalog.

    The legacy `tier_code` is kept as `legacy_tier_code` so Phase 15 callers can
    migrate gradually. Amounts remain cents, matching the current codebase.
    """
    code = assert_known_plan_code(plan.get("tier_code") or plan.get("plan_code"))
    included = included_limits_for_plan(plan)
    return {
        "plan_code": code,
        "legacy_tier_code": plan.get("tier_code") or code,
        "display_name": plan.get("name"),
        "customer_type": customer_type_for_plan(code),
        "billing_channels": billing_channels_for_plan(plan),
        "stripe_product_id": plan.get("stripe_product_id"),
        "stripe_monthly_price_id": plan.get("stripe_price_id_monthly"),
        "stripe_annual_price_id": plan.get("stripe_price_id_annual"),
        "apple_monthly_product_id": plan.get("apple_monthly_product_id"),
        "apple_annual_product_id": plan.get("apple_annual_product_id"),
        "monthly_amount": plan.get("monthly_price_cents"),
        "annual_amount": plan.get("annual_price_cents"),
        **included,
        "is_active": bool(plan.get("active", True)),
        "contact_sales": bool(plan.get("contact_sales")),
        "display_order": plan.get("display_order", PLAN_ORDER.get(code, 999)),
    }


def catalog_subscription_plan_shapes() -> list[dict[str, Any]]:
    return [plan_to_subscription_plan_shape(plan) for plan in PLAN_CATALOG]


def empty_extra_quantities() -> dict[str, int]:
    return {
        "extra_horse_quantity": 0,
        "extra_staff_quantity": 0,
        "extra_owner_manager_quantity": 0,
        "extra_lesson_participant_quantity": 0,
    }


def derive_limits_from_plan_and_extras(
    plan: Mapping[str, Any],
    extras: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    limits = feature_limits_to_entitlement_limits(plan.get("feature_limits") or {})
    extra = {**empty_extra_quantities(), **(extras or {})}

    def add(limit_key: str, extra_key: str) -> Any:
        base = limits.get(limit_key)
        if base is None:
            return None
        return int(base or 0) + int(extra.get(extra_key) or 0)

    return {
        "horse_limit": add("horse_limit", "extra_horse_quantity"),
        "staff_limit": add("staff_limit", "extra_staff_quantity"),
        "owner_manager_limit": add("owner_manager_limit", "extra_owner_manager_quantity"),
        "lesson_participant_limit": add("lesson_participant_limit", "extra_lesson_participant_quantity"),
    }


def subscription_to_account_limits_shape(
    *,
    subscription: Mapping[str, Any] | None,
    plan: Mapping[str, Any] | None = None,
    account_id: str | None = None,
) -> dict[str, Any]:
    """Return the future account_subscription_limits response shape.

    This is a pure projection. It accepts today's Phase 15 subscription rows
    (`plan_tier_code`) and emits the future provider-neutral fields.
    """
    sub = subscription or {}
    original_code = normalize_plan_code(sub.get("plan_code") or sub.get("plan_tier_code") or "free")
    status = normalize_subscription_status(sub.get("subscription_status") or sub.get("status"))
    effective_code = (
        original_code
        if is_entitlement_active_status(status)
        else INACTIVE_ENTITLEMENT_FALLBACK_PLAN_CODE
    )
    if plan is not None and normalize_plan_code(plan.get("tier_code") or plan.get("plan_code")) == effective_code:
        resolved_plan = deepcopy(plan)
    else:
        resolved_plan = plan_by_code(effective_code)
    extras = (
        {key: sub.get(key, 0) for key in empty_extra_quantities()}
        if is_entitlement_active_status(status)
        else empty_extra_quantities()
    )
    limits = derive_limits_from_plan_and_extras(resolved_plan, extras)
    provider = sub.get("billing_provider") or (
        "stripe" if sub.get("stripe_subscription_id") or sub.get("stripe_customer_id") else DEFAULT_BILLING_PROVIDER
    )
    platform = sub.get("purchase_platform") or (
        "web" if provider == "stripe" else DEFAULT_PURCHASE_PLATFORM
    )
    return {
        "account_id": account_id or sub.get("account_id") or sub.get("barn_id"),
        "plan_code": effective_code,
        **limits,
        **extras,
        "subscription_status": status,
        "billing_provider": provider,
        "purchase_platform": platform,
        "stripe_customer_id": sub.get("stripe_customer_id"),
        "stripe_subscription_id": sub.get("stripe_subscription_id"),
        "apple_original_transaction_id": sub.get("apple_original_transaction_id"),
        "apple_product_id": sub.get("apple_product_id"),
        "current_period_end": sub.get("current_period_end"),
        "last_verified_at": sub.get("last_verified_at"),
    }
