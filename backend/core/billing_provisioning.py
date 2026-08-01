"""core/billing_provisioning.py - Phase 15/15R Stripe catalog provisioning.

Plan catalog source-of-truth lives in the local `plans` collection. This module
ensures that collection stays in sync with Stripe Products/Prices.

Two modes:
  - dev/test (APP_ENV != "production"): upsert safe local catalog rows. Startup
    never writes founder-approved live Stripe object IDs into sandbox/dev rows.
    Sandbox object creation and verification is handled by
    scripts/sync_stripe_catalog.py.
  - production: use explicit STRIPE_PRICE_* env vars when present, otherwise
    use the founder-approved live Price IDs below. Validate each Price exists
    in Stripe and abort startup if any configured Price is invalid.

Enterprise and community programs have live Stripe Products for catalog
traceability, but no public recurring Prices — they're Contact-Sales /
custom-contract only.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

import stripe

from core import runtime_state
from core.stripe_config import StripeConfigurationError, configure_stripe_api_key

logger = logging.getLogger(__name__)


# Phase 15R-H — live Stripe Product/Price IDs reconciled against the founder's
# exported Stripe catalog PDF. These are object identifiers, not secret API
# keys. Env vars with the legacy
# STRIPE_PRICE_<PLAN>_<MONTHLY|ANNUAL> names still override this map for staged
# rollouts, but the source catalog no longer depends on hand-entering every
# Price ID into .env.
LIVE_STRIPE_PRODUCT_IDS = {
    "individual_owner": "prod_UjVm4KzSjDgEYG",
    "private_owner_plus": "prod_UjVoQZFGN8I0dF",
    "starter_barn": "prod_UjeQPuCZ05lhma",
    "advanced_barn": "prod_UjeVYa8dU20kwm",
    "elite_barn": "prod_UjeZyVxTTjyhFu",
    "trainer_no_lesson": "prod_UjeklCXZdjUYv6",
    "trainer_lesson_15": "prod_Ujes2frtPqSVU5",
    "trainer_lesson_50": "prod_Ujf5N0uBEa2llZ",
    "enterprise": "prod_UjfCInFonGujyh",
    "community_program": "prod_UjzRc2zZyQqBzP",
}

LIVE_STRIPE_PRICE_IDS = {
    "individual_owner": {
        "monthly": "price_1Tk2ljJLyFSImf6Y7m62C3gd",
        "annual": "price_1Tk2mRJLyFSImf6YRlPmlu1l",
    },
    "private_owner_plus": {
        "monthly": "price_1TkB5ZJLyFSImf6YsGv51iHN",
        "annual": "price_1TkB6IJLyFSImf6Y6EUh8Dwc",
    },
    "starter_barn": {
        "monthly": "price_1TkB8uJLyFSImf6YZC8LQzmU",
        "annual": "price_1TkBBUJLyFSImf6Ye3scNRy8",
    },
    "advanced_barn": {
        "monthly": "price_1TkBDiJLyFSImf6YOMe6g8My",
        "annual": "price_1TkBERJLyFSImf6Y8cSX569Z",
    },
    "elite_barn": {
        "monthly": "price_1TkBHjJLyFSImf6YBV9KVZrP",
        "annual": "price_1TkBPlJLyFSImf6YuGXkuvT0",
    },
    "trainer_no_lesson": {
        "monthly": "price_1TkBRMJLyFSImf6YygjgN0Bn",
        "annual": "price_1TkBYEJLyFSImf6YjwI4HP5w",
    },
    "trainer_lesson_15": {
        "monthly": "price_1TkBhzJLyFSImf6YrAGxDoVn",
        "annual": "price_1TkBkFJLyFSImf6Y6ClbJiPO",
    },
    "trainer_lesson_50": {
        "monthly": "price_1TkBnYJLyFSImf6Y1SvF9uLQ",
        "annual": "price_1TkBpaJLyFSImf6YMeu5YlRw",
    },
}

FOUNDER_STRIPE_PLAN_CODE_ALIASES = {
    "trainer_no_lessons": "trainer_no_lesson",
    "trainer_lessons_15": "trainer_lesson_15",
    "trainer_lessons_50": "trainer_lesson_50",
}

ADDON_PRICE_CATALOG = {
    "additional_horse_standard": {
        "stripe_product_id": "prod_UjfDx3cO3OgYG9",
        "stripe_price_id": "price_1TkBuUJLyFSImf6YtzCNBmTT",
        "unit_amount_cents": 500,
        "currency": "usd",
        "interval": "month",
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_horse_starter": {
        "stripe_product_id": "prod_UjfG9GupHWHLW7",
        "stripe_price_id": "price_1TkBx7JLyFSImf6YM4Tb1Rk2",
        "unit_amount_cents": 700,
        "currency": "usd",
        "interval": "month",
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_horse_advanced": {
        "stripe_product_id": "prod_UjfMUbJIX0dGCn",
        "stripe_price_id": "price_1TkC2TJLyFSImf6Y9UpftKsE",
        "unit_amount_cents": 600,
        "currency": "usd",
        "interval": "month",
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_staff_seat": {
        "stripe_product_id": "prod_UjfOyluZB1a5fz",
        "stripe_price_id": "price_1TkC4zJLyFSImf6YIxPX8p1T",
        "unit_amount_cents": 800,
        "currency": "usd",
        "interval": "month",
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
    },
    "additional_helper_seat": {
        "stripe_product_id": "prod_UjmnLwJsDo60A8",
        "stripe_price_id": "price_1TkVOtJLyFSImf6YeP9sqy24",
        "unit_amount_cents": 600,
        "currency": "usd",
        "interval": "month",
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
    },
    "additional_owner_manager_seat": {
        "stripe_product_id": "prod_UjfTFLjeVwqI1e",
        "stripe_price_id": "price_1TkCANJLyFSImf6Yv05S9zzm",
        "unit_amount_cents": 1500,
        "currency": "usd",
        "interval": "month",
        "limit_field": "owner_manager_limit",
        "quantity_field": "extra_owner_manager_quantity",
    },
    "elite_owner_manager_seat": {
        "stripe_product_id": "prod_UjfW7Op9Mhdexa",
        "stripe_price_id": "price_1TkCI2JLyFSImf6YDIdCme7h",
        "unit_amount_cents": 2000,
        "currency": "usd",
        "interval": "month",
        "limit_field": "owner_manager_limit",
        "quantity_field": "extra_owner_manager_quantity",
    },
    "additional_lesson_participant": {
        "stripe_product_id": "prod_UjfxNgUirIWN2v",
        "stripe_price_id": "price_1TkChgJLyFSImf6YSdp304bC",
        "unit_amount_cents": 300,
        "currency": "usd",
        "interval": "month",
        "limit_field": "lesson_participant_limit",
        "quantity_field": "extra_lesson_participant_quantity",
    },
    "extra_storage": {
        "stripe_product_id": "prod_UjgHub3Fg5z5vJ",
        "stripe_price_id": "price_1TkCxGJLyFSImf6YfsgThUvN",
        "unit_amount_cents": 1000,
        "currency": "usd",
        "interval": "month",
        "limit_field": "storage_gb",
        "quantity_field": "extra_storage_quantity",
    },
    "custom_branding": {
        "stripe_product_id": "prod_UjlUaSBvFXWYaQ",
        "stripe_price_id": "price_1TkIgOJLyFSImf6Y3LDwBXph",
        "unit_amount_cents": 9900,
        "currency": "usd",
        "interval": "month",
        "limit_field": "custom_branding",
        "quantity_field": "custom_branding_quantity",
    },
    "ai_owner_update_assistant": {
        "stripe_product_id": "prod_UjmHtMJjtrDFtx",
        "stripe_price_id": "price_1TkImnJLyFSImf6YRMfk0su5",
        "unit_amount_cents": 2900,
        "currency": "usd",
        "interval": "month",
        "limit_field": "ai_owner_update_assistant",
        "quantity_field": "ai_owner_update_assistant_quantity",
    },
    "quickbooks_integration": {
        "stripe_product_id": "prod_UjmMqco5cNTifU",
        "stripe_price_id": "price_1TkIzJJLyFSImf6YOPLPtSon",
        "unit_amount_cents": 1900,
        "currency": "usd",
        "interval": "month",
        "limit_field": "quickbooks_integration",
        "quantity_field": "quickbooks_integration_quantity",
    },
}


# ---------- Static plan catalog ----------
# Prices mirror docs/PRICING_PLAN_ADDENDUM.md. Annual prices are explicit
# founder-approved values, not computed discounts.
PLAN_CATALOG = [
    {
        "tier_code": "free",
        "name": "Invited Horse Owner Portal",
        "description": "Free portal access for horse owners invited by a subscribed barn, trainer, or facility.",
        "monthly_price_cents": 0,
        "annual_price_cents": 0,
        "feature_limits": {
            "horses": 0,
            "users": 1,
            "staff_seats": 0,
            "owner_manager_seats": 0,
            "owner_portal_accounts_included": True,
            "storage_gb": 1,
            "advanced_reporting": False,
            "medical_records": False,
            "messaging": False,
            "calendar_integrations": False,
            "api_access": False,
            "dedicated_support": False,
        },
        "contact_sales": False,
        "stripe_provisioned": False,
    },
    {
        "tier_code": "individual_owner",
        "name": "Individual Horse Owner",
        "description": "For owners managing one horse outside an affiliated barn.",
        "monthly_price_cents": 1499,
        "annual_price_cents": 14900,
        "feature_limits": {
            "horses": 1,
            "users": 1,
            "emergency_contacts": 1,
            "staff_seats": 0,
            "owner_manager_seats": 1,
            "storage_gb": 5,
            "advanced_reporting": False,
            "medical_records": True,
            "messaging": False,
            "calendar_integrations": False,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {"additional_horse_cents": 500},
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "service_provider_free",
        "name": "Service Provider Free",
        "description": "Free service-provider access for basic horse information, calendar visibility, and appointment scheduling.",
        "monthly_price_cents": 0,
        "annual_price_cents": 0,
        "feature_limits": {
            "users": 1,
            "staff_seats": 0,
            "owner_manager_seats": 0,
            "service_provider_profile": True,
            "basic_horse_info": True,
            "calendar_visibility": True,
            "appointment_scheduling": True,
            "client_notes": False,
            "document_uploads": False,
            "premium_provider_features": False,
            "advanced_reporting": False,
            "medical_records": False,
            "messaging": False,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "contact_sales": False,
        "stripe_provisioned": False,
    },
    {
        "tier_code": "service_provider_premium",
        "name": "Service Provider Premium",
        "description": "For independent service providers who need premium scheduling, client notes, documents, and provider visibility.",
        "monthly_price_cents": 1500,
        "annual_price_cents": 18000,
        "feature_limits": {
            "users": 1,
            "staff_seats": 0,
            "owner_manager_seats": 0,
            "service_provider_profile": True,
            "basic_horse_info": True,
            "calendar_visibility": True,
            "appointment_scheduling": True,
            "client_notes": True,
            "document_uploads": True,
            "premium_provider_features": True,
            "advanced_reporting": True,
            "medical_records": False,
            "messaging": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "private_owner_plus",
        "name": "Private Owner Plus",
        "description": "Includes everything in Individual Horse Owner, plus one additional profile and private-owner tools for multi-horse setups.",
        "monthly_price_cents": 2999,
        "annual_price_cents": 29900,
        "feature_limits": {
            "horses": 5,
            "users": 2,
            "staff_seats": 0,
            "helper_family_seats": 1,
            "owner_manager_seats": 1,
            "storage_gb": 10,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": False,
            "inventory": "basic",
            "qr_stall_cards": True,
            "emergency_mode": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {"additional_horse_cents": 500, "additional_helper_seat_cents": 600},
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "starter_barn",
        "name": "Starter Barn",
        "description": "For small boarding barns, boutique private facilities, and small training barns.",
        "monthly_price_cents": 6999,
        "annual_price_cents": 69900,
        "feature_limits": {
            "horses": 10,
            "users": 4,
            "staff_seats": 3,
            "owner_manager_seats": 1,
            "owner_portal_accounts_included": True,
            "storage_gb": 15,
            "advanced_reporting": False,
            "medical_records": True,
            "messaging": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {
            "additional_horse_cents": 700,
            "additional_staff_seat_cents": 800,
            "additional_owner_manager_seat_cents": 1500,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "advanced_barn",
        "name": "Advanced Barn",
        "description": "For professional boarding barns, training barns, and mid-size operations.",
        "monthly_price_cents": 14999,
        "annual_price_cents": 149900,
        "feature_limits": {
            "horses": 30,
            "users": 10,
            "staff_seats": 8,
            "owner_manager_seats": 2,
            "owner_portal_accounts_included": True,
            "storage_gb": 50,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "inventory": "advanced",
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {
            "additional_horse_cents": 600,
            "additional_staff_seat_cents": 800,
            "additional_owner_manager_seat_cents": 1500,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "elite_barn",
        "name": "Elite Barn",
        "description": "For larger premium, high-service barns and show facilities.",
        "monthly_price_cents": 29999,
        "annual_price_cents": 299900,
        "feature_limits": {
            "horses": 50,
            "users": 16,
            "staff_seats": 12,
            "owner_manager_seats": 4,
            "owner_portal_accounts_included": True,
            "storage_gb": 100,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "advanced_permissions": True,
            "digital_signatures": True,
            "custom_branding": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": True,
        },
        "overage": {
            "additional_horse_cents": 500,
            "additional_staff_seat_cents": 800,
            "additional_owner_manager_seat_cents": 2000,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "trainer_no_lesson",
        "name": "Trainer - No Lesson Program",
        "description": "For independent trainers managing training horses without a lesson program.",
        "monthly_price_cents": 5999,
        "annual_price_cents": 59900,
        "feature_limits": {
            "horses": 20,
            "users": 3,
            "staff_seats": 2,
            "owner_manager_seats": 1,
            "owner_portal_accounts_included": True,
            "storage_gb": 20,
            "advanced_reporting": False,
            "medical_records": True,
            "messaging": True,
            "training_plans": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {"additional_horse_cents": 500, "additional_staff_seat_cents": 800},
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "trainer_lesson_15",
        "name": "Trainer + Lesson Program - 15 Participants",
        "description": "For trainers with a small lesson program.",
        "monthly_price_cents": 9999,
        "annual_price_cents": 99900,
        "feature_limits": {
            "horses": 15,
            "users": 4,
            "staff_seats": 3,
            "owner_manager_seats": 1,
            "lesson_participants": 15,
            "owner_portal_accounts_included": True,
            "storage_gb": 25,
            "advanced_reporting": False,
            "medical_records": True,
            "messaging": True,
            "lesson_scheduling": True,
            "lesson_packages": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {"participant_overage_allowed": False},
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "trainer_lesson_50",
        "name": "Trainer + Lesson Program - 50 Participants",
        "description": "For established lesson programs, riding schools, and larger student bases.",
        "monthly_price_cents": 17999,
        "annual_price_cents": 179900,
        "feature_limits": {
            "horses": 25,
            "users": 9,
            "staff_seats": 6,
            "owner_manager_seats": 3,
            "lesson_participants": 50,
            "owner_portal_accounts_included": True,
            "storage_gb": 50,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "lesson_scheduling": True,
            "lesson_packages": True,
            "attendance_tracking": True,
            "digital_waivers": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "overage": {
            "additional_participant_cents": 300,
            "additional_horse_cents": 500,
            "additional_staff_seat_cents": 800,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "enterprise",
        "name": "Enterprise",
        "description": "For multi-location centers, universities, therapeutic riding centers, and large riding schools.",
        "monthly_price_cents": None,
        "annual_price_cents": None,
        "feature_limits": {
            "horses": None,
            "users": None,
            "staff_seats": None,
            "owner_manager_seats": None,
            "lesson_participants": None,
            "storage_gb": None,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "calendar_integrations": True,
            "api_access": True,
            "dedicated_support": True,
        },
        "contact_sales": True,
        "stripe_provisioned": False,
    },
    {
        "tier_code": "community_program",
        "name": "Community Program",
        "description": "Discounted nonprofit, education, rescue, 4-H, FFA, and therapeutic riding pricing.",
        "monthly_price_cents": None,
        "annual_price_cents": None,
        "feature_limits": {
            "horses": None,
            "users": None,
            "staff_seats": None,
            "owner_manager_seats": None,
            "lesson_participants": None,
            "storage_gb": None,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
            "discount_range": "30-50%",
        },
        "contact_sales": True,
        "stripe_provisioned": False,
    },
]

PLAN_ORDER = {tier["tier_code"]: idx for idx, tier in enumerate(PLAN_CATALOG)}


def _price_env_prefix(tier_code: str) -> str:
    return f"STRIPE_PRICE_{tier_code.upper()}"


def _price_env_vars(tier_code: str) -> tuple[str, str]:
    prefix = _price_env_prefix(tier_code)
    return f"{prefix}_MONTHLY", f"{prefix}_ANNUAL"


def normalize_stripe_plan_code(value: str | None) -> str:
    raw = (value or "").strip().lower()
    return FOUNDER_STRIPE_PLAN_CODE_ALIASES.get(raw, raw)


def _configured_price_ids(
    tier_code: str,
    *,
    allow_live_fallback: bool | None = None,
) -> tuple[Optional[str], Optional[str]]:
    """Return monthly/annual Price IDs for the active production posture.

    Live founder-approved IDs are a production fallback only. Non-production
    callers must pass explicit verified sandbox IDs instead of inheriting live
    catalog constants.
    """
    if allow_live_fallback is None:
        allow_live_fallback = _is_production()
    monthly_env, annual_env = _price_env_vars(tier_code)
    mapped = (LIVE_STRIPE_PRICE_IDS.get(tier_code) or {}) if allow_live_fallback else {}
    return (
        os.environ.get(monthly_env) or mapped.get("monthly"),
        os.environ.get(annual_env) or mapped.get("annual"),
    )


def _configured_product_id(
    tier_code: str,
    *,
    allow_live_fallback: bool | None = None,
) -> Optional[str]:
    if allow_live_fallback is None:
        allow_live_fallback = _is_production()
    mapped = LIVE_STRIPE_PRODUCT_IDS.get(tier_code) if allow_live_fallback else None
    return os.environ.get(f"STRIPE_PRODUCT_{tier_code.upper()}") or mapped


def _customer_type_for_tier(tier_code: str) -> str:
    if tier_code == "free":
        return "invited_owner_portal"
    if tier_code in {"service_provider_free", "service_provider_premium"}:
        return "service_provider"
    if tier_code in {"individual_owner", "private_owner_plus"}:
        return "individual_owner"
    if tier_code in {"starter_barn", "advanced_barn", "elite_barn"}:
        return "facility"
    if tier_code in {"trainer_no_lesson", "trainer_lesson_15", "trainer_lesson_50"}:
        return "trainer"
    if tier_code == "enterprise":
        return "enterprise"
    if tier_code == "community_program":
        return "community"
    return "unknown"


def _billing_channels_for_tier(tier: dict[str, Any]) -> list[str]:
    if tier["tier_code"] == "free":
        return ["manual"]
    if tier.get("contact_sales"):
        return ["manual", "comped"]
    if tier.get("stripe_provisioned"):
        return ["stripe", "apple"]
    return ["manual"]


def _included_limits(tier: dict[str, Any]) -> dict[str, Any]:
    limits = tier.get("feature_limits") or {}
    return {
        "included_horses": limits.get("horses"),
        "included_staff": limits.get("staff_seats", 0),
        "included_owner_managers": limits.get("owner_manager_seats", 0),
        "included_lesson_participants": limits.get("lesson_participants", 0),
    }


def _is_production() -> bool:
    return (os.environ.get("APP_ENV") or "development").lower() == "production"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stripe_environment() -> str:
    return "live" if _is_production() else "sandbox"


def _skip_startup_stripe_provisioning() -> bool:
    return (os.environ.get("SKIP_STRIPE_CATALOG_PROVISIONING") or "true").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _startup_autoprovision_enabled() -> bool:
    return (os.environ.get("STRIPE_CATALOG_AUTOPROVISION_ON_STARTUP") or "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


async def _find_managed_product(tier_code: str):
    """Find a Stripe Product previously created by EquineSync via metadata."""
    # Stripe doesn't search Products by metadata directly — list + filter is fine
    # for the 2 products we manage. Idempotent restart-safe lookup.
    products = stripe.Product.list(limit=100, active=True)
    for p in products.auto_paging_iter():
        meta = p.get("metadata") or {}
        if meta.get("equinesync_managed") == "true" and meta.get("tier_code") == tier_code:
            return p
    return None


async def _find_managed_price(product_id: str, tier_code: str, interval: str):
    """Find a managed Price for (tier_code, interval) under a product."""
    prices = stripe.Price.list(limit=100, active=True, product=product_id)
    for pr in prices.auto_paging_iter():
        meta = pr.get("metadata") or {}
        if (
            meta.get("equinesync_managed") == "true"
            and meta.get("tier_code") == tier_code
            and pr["recurring"]
            and pr["recurring"]["interval"] == interval
        ):
            return pr
    return None


async def _provision_dev_catalog(db, *, blockers: Optional[list[str]] = None) -> None:
    """Dev/test only - upsert local rows without creating Stripe objects.

    Stripe sandbox catalog creation is intentionally moved to
    scripts/sync_stripe_catalog.py, where operators can dry-run, apply,
    re-apply, verify, and capture a sanitized receipt. Startup may preserve
    already-verified sandbox IDs, but it must not copy live IDs into sandbox
    rows or silently create new provider objects.
    """
    for tier in PLAN_CATALOG:
        await _upsert_plan(
            db,
            tier,
            None,
            None,
            None,
            stripe_catalog_environment="sandbox",
            stripe_catalog_ready=False,
            stripe_catalog_blockers=blockers or ["stripe_catalog_sync_required"],
            preserve_existing_stripe_ids=True,
        )
    await _upsert_addon_catalog(
        db,
        stripe_catalog_environment="sandbox",
        stripe_catalog_ready=False,
        stripe_catalog_blockers=blockers or ["stripe_catalog_sync_required"],
        preserve_existing_stripe_ids=True,
    )


async def _validate_prod_catalog(db) -> None:
    """Production only — Price IDs must exist and be valid in Stripe.

    Env vars override the founder-approved static map. Startup aborts with a
    clear error if a self-service tier has no monthly/annual Price ID or if
    Stripe cannot retrieve a configured Price.
    """
    missing = []
    configured: dict[str, tuple[str, str]] = {}
    for tier in PLAN_CATALOG:
        if not tier["stripe_provisioned"]:
            continue
        monthly_id, annual_id = _configured_price_ids(tier["tier_code"], allow_live_fallback=True)
        if not monthly_id:
            missing.append(f"{_price_env_vars(tier['tier_code'])[0]} or LIVE_STRIPE_PRICE_IDS[{tier['tier_code']}].monthly")
        if not annual_id:
            missing.append(f"{_price_env_vars(tier['tier_code'])[1]} or LIVE_STRIPE_PRICE_IDS[{tier['tier_code']}].annual")
        if monthly_id and annual_id:
            configured[tier["tier_code"]] = (monthly_id, annual_id)
    if missing:
        raise RuntimeError(
            f"Production startup: required Stripe Price IDs missing: {missing}"
        )

    # Upsert local plans with the validated price IDs (no Stripe product creation in prod).
    for tier in PLAN_CATALOG:
        if not tier["stripe_provisioned"]:
            await _upsert_plan(
                db,
                tier,
                _configured_product_id(tier["tier_code"], allow_live_fallback=True),
                None,
                None,
                stripe_catalog_environment="live",
                stripe_catalog_ready=True,
                stripe_catalog_verified_at=_now_iso(),
                stripe_catalog_blockers=[],
            )
            continue
        monthly_id, annual_id = configured[tier["tier_code"]]
        for label, price_id in (("monthly", monthly_id), ("annual", annual_id)):
            try:
                stripe.Price.retrieve(price_id)
            except stripe.error.StripeError as ex:
                raise RuntimeError(
                    f"Production startup: {tier['tier_code']} {label} Price {price_id} "
                    f"is not a valid Stripe Price: {ex}"
                ) from ex
        # Resolve product_id from one of the prices for consistency.
        try:
            pr = stripe.Price.retrieve(monthly_id)
            product_id = pr.get("product") or _configured_product_id(tier["tier_code"], allow_live_fallback=True)
        except Exception:
            product_id = _configured_product_id(tier["tier_code"], allow_live_fallback=True)
        await _upsert_plan(
            db,
            tier,
            product_id,
            monthly_id,
            annual_id,
            stripe_catalog_environment="live",
            stripe_catalog_ready=True,
            stripe_catalog_verified_at=_now_iso(),
            stripe_catalog_blockers=[],
        )


async def _upsert_plan(
    db,
    tier,
    product_id,
    monthly_price_id,
    annual_price_id,
    *,
    stripe_catalog_environment: Optional[str] = None,
    stripe_catalog_ready: bool = False,
    stripe_catalog_verified_at: Optional[str] = None,
    stripe_catalog_blockers: Optional[list[str]] = None,
    preserve_existing_stripe_ids: bool = False,
):
    if preserve_existing_stripe_ids:
        existing = await db.plans.find_one(
            {"tier_code": tier["tier_code"]},
            {
                "_id": 0,
                "stripe_product_id": 1,
                "stripe_price_id_monthly": 1,
                "stripe_price_id_annual": 1,
            },
        )
        existing = existing or {}
        product_id = product_id or existing.get("stripe_product_id")
        monthly_price_id = monthly_price_id or existing.get("stripe_price_id_monthly")
        annual_price_id = annual_price_id or existing.get("stripe_price_id_annual")

    if _is_production():
        product_id = product_id or _configured_product_id(tier["tier_code"], allow_live_fallback=True)
        if tier["stripe_provisioned"]:
            fallback_monthly, fallback_annual = _configured_price_ids(
                tier["tier_code"],
                allow_live_fallback=True,
            )
            monthly_price_id = monthly_price_id or fallback_monthly
            annual_price_id = annual_price_id or fallback_annual

    blockers = list(stripe_catalog_blockers or [])
    update = {
        "tier_code": tier["tier_code"],
        "plan_code": tier["tier_code"],
        "name": tier["name"],
        "description": tier["description"],
        "monthly_price_cents": tier["monthly_price_cents"],
        "annual_price_cents": tier["annual_price_cents"],
        "feature_limits": tier["feature_limits"],
        "overage": tier.get("overage") or {},
        "contact_sales": tier["contact_sales"],
        "display_order": PLAN_ORDER.get(tier["tier_code"], 999),
        "stripe_product_id": product_id,
        "stripe_price_id_monthly": monthly_price_id,
        "stripe_price_id_annual": annual_price_id,
        "stripe_catalog_environment": stripe_catalog_environment or _stripe_environment(),
        "stripe_catalog_ready": bool(stripe_catalog_ready),
        "stripe_catalog_verified_at": stripe_catalog_verified_at,
        "stripe_catalog_blockers": blockers,
        "active": True,
    }
    await db.plans.update_one(
        {"tier_code": tier["tier_code"]},
        {"$set": update, "$setOnInsert": {"id": tier["tier_code"]}},
        upsert=True,
    )
    await _upsert_subscription_plan(
        db,
        tier,
        product_id,
        monthly_price_id,
        annual_price_id,
        stripe_catalog_environment=stripe_catalog_environment,
        stripe_catalog_ready=stripe_catalog_ready,
        stripe_catalog_verified_at=stripe_catalog_verified_at,
        stripe_catalog_blockers=blockers,
        preserve_existing_stripe_ids=preserve_existing_stripe_ids,
    )


async def _upsert_subscription_plan(
    db,
    tier,
    product_id,
    monthly_price_id,
    annual_price_id,
    *,
    stripe_catalog_environment: Optional[str] = None,
    stripe_catalog_ready: bool = False,
    stripe_catalog_verified_at: Optional[str] = None,
    stripe_catalog_blockers: Optional[list[str]] = None,
    preserve_existing_stripe_ids: bool = False,
):
    plan_code = tier["tier_code"]
    if preserve_existing_stripe_ids:
        existing = await db.subscription_plans.find_one(
            {"plan_code": plan_code},
            {
                "_id": 0,
                "stripe_product_id": 1,
                "stripe_monthly_price_id": 1,
                "stripe_annual_price_id": 1,
            },
        )
        existing = existing or {}
        product_id = product_id or existing.get("stripe_product_id")
        monthly_price_id = monthly_price_id or existing.get("stripe_monthly_price_id")
        annual_price_id = annual_price_id or existing.get("stripe_annual_price_id")

    update = {
        "plan_code": plan_code,
        "legacy_tier_code": plan_code,
        "display_name": tier["name"],
        "description": tier["description"],
        "customer_type": _customer_type_for_tier(plan_code),
        "billing_channels": _billing_channels_for_tier(tier),
        "stripe_product_id": product_id,
        "stripe_monthly_price_id": monthly_price_id,
        "stripe_annual_price_id": annual_price_id,
        "apple_monthly_product_id": None,
        "apple_annual_product_id": None,
        "monthly_amount": tier["monthly_price_cents"],
        "annual_amount": tier["annual_price_cents"],
        **_included_limits(tier),
        "contact_sales": bool(tier.get("contact_sales")),
        "display_order": PLAN_ORDER.get(plan_code, 999),
        "stripe_catalog_environment": stripe_catalog_environment or _stripe_environment(),
        "stripe_catalog_ready": bool(stripe_catalog_ready),
        "stripe_catalog_verified_at": stripe_catalog_verified_at,
        "stripe_catalog_blockers": list(stripe_catalog_blockers or []),
        "is_active": True,
    }
    await db.subscription_plans.update_one(
        {"plan_code": plan_code},
        {"$set": update, "$setOnInsert": {"id": plan_code}},
        upsert=True,
    )


async def _upsert_addon_catalog(
    db,
    *,
    stripe_ids_by_addon: Optional[dict[str, dict[str, Optional[str]]]] = None,
    stripe_catalog_environment: Optional[str] = None,
    stripe_catalog_ready: bool = False,
    stripe_catalog_verified_at: Optional[str] = None,
    stripe_catalog_blockers: Optional[list[str]] = None,
    preserve_existing_stripe_ids: bool = False,
):
    stripe_ids_by_addon = stripe_ids_by_addon or {}
    blockers = list(stripe_catalog_blockers or [])
    for addon_code, config in ADDON_PRICE_CATALOG.items():
        ids = stripe_ids_by_addon.get(addon_code) or {}
        product_id = ids.get("product_id")
        price_id = ids.get("price_id")
        if preserve_existing_stripe_ids:
            existing = await db.subscription_addons.find_one(
                {"addon_code": addon_code},
                {"_id": 0, "stripe_product_id": 1, "stripe_price_id": 1},
            )
            existing = existing or {}
            product_id = product_id or existing.get("stripe_product_id")
            price_id = price_id or existing.get("stripe_price_id")
        if _is_production():
            product_id = product_id or config.get("stripe_product_id")
            price_id = price_id or config.get("stripe_price_id")
        update = {
            "addon_code": addon_code,
            "stripe_product_id": product_id,
            "stripe_price_id": price_id,
            "billing_provider": "stripe",
            "billing_channel": "web",
            "recurring": True,
            "unit_amount_cents": config.get("unit_amount_cents"),
            "currency": config.get("currency", "usd"),
            "interval": config.get("interval", "month"),
            "limit_field": config["limit_field"],
            "quantity_field": config["quantity_field"],
            "stripe_catalog_environment": stripe_catalog_environment or _stripe_environment(),
            "stripe_catalog_ready": bool(stripe_catalog_ready),
            "stripe_catalog_verified_at": stripe_catalog_verified_at,
            "stripe_catalog_blockers": blockers,
            "is_active": True,
        }
        await db.subscription_addons.update_one(
            {"addon_code": addon_code},
            {"$set": update, "$setOnInsert": {"id": addon_code}},
            upsert=True,
        )


async def upsert_environment_catalog_rows(
    db,
    *,
    environment: str,
    plan_ids: dict[str, dict[str, Optional[str]]],
    addon_ids: dict[str, dict[str, Optional[str]]],
    ready: bool,
    verified_at: Optional[str] = None,
    blockers: Optional[list[str]] = None,
) -> None:
    """Upsert catalog rows using caller-verified environment-specific IDs."""

    for tier in PLAN_CATALOG:
        ids = plan_ids.get(tier["tier_code"]) or {}
        await _upsert_plan(
            db,
            tier,
            ids.get("product_id"),
            ids.get("monthly_price_id"),
            ids.get("annual_price_id"),
            stripe_catalog_environment=environment,
            stripe_catalog_ready=ready,
            stripe_catalog_verified_at=verified_at,
            stripe_catalog_blockers=blockers or [],
        )
    await _upsert_addon_catalog(
        db,
        stripe_ids_by_addon=addon_ids,
        stripe_catalog_environment=environment,
        stripe_catalog_ready=ready,
        stripe_catalog_verified_at=verified_at,
        stripe_catalog_blockers=blockers or [],
    )


async def _existing_environment_catalog_ready(db, environment: str):
    blockers: list[str] = []
    verified_at_values: list[str] = []
    for tier in PLAN_CATALOG:
        code = tier["tier_code"]
        row = await db.plans.find_one({"tier_code": code}, {"_id": 0})
        sub_row = await db.subscription_plans.find_one({"plan_code": code}, {"_id": 0})
        if not row:
            blockers.append(f"plans_row_missing:{code}")
            continue
        if not sub_row:
            blockers.append(f"subscription_plans_row_missing:{code}")
        if row.get("stripe_catalog_environment") != environment:
            blockers.append(f"plans_environment_mismatch:{code}")
        if row.get("stripe_catalog_ready") is not True:
            blockers.append(f"plans_not_ready:{code}")
        if row.get("stripe_catalog_verified_at"):
            verified_at_values.append(row["stripe_catalog_verified_at"])
        if tier.get("stripe_provisioned"):
            if not row.get("stripe_product_id"):
                blockers.append(f"plans_product_missing:{code}")
            if not row.get("stripe_price_id_monthly"):
                blockers.append(f"plans_monthly_missing:{code}")
            if not row.get("stripe_price_id_annual"):
                blockers.append(f"plans_annual_missing:{code}")
        elif tier.get("contact_sales"):
            if not row.get("stripe_product_id"):
                blockers.append(f"plans_contact_sales_product_missing:{code}")

    for addon_code in ADDON_PRICE_CATALOG:
        row = await db.subscription_addons.find_one(
            {"addon_code": addon_code},
            {"_id": 0},
        )
        if not row:
            blockers.append(f"addon_row_missing:{addon_code}")
            continue
        if row.get("stripe_catalog_environment") != environment:
            blockers.append(f"addon_environment_mismatch:{addon_code}")
        if row.get("stripe_catalog_ready") is not True:
            blockers.append(f"addon_not_ready:{addon_code}")
        if not row.get("stripe_product_id"):
            blockers.append(f"addon_product_missing:{addon_code}")
        if not row.get("stripe_price_id"):
            blockers.append(f"addon_price_missing:{addon_code}")
        if row.get("stripe_catalog_verified_at"):
            verified_at_values.append(row["stripe_catalog_verified_at"])

    return (not blockers), (max(verified_at_values) if verified_at_values else None), blockers


async def ensure_stripe_catalog(db) -> None:
    """Entry point — called from lifespan.on_startup.

    Production: a live Stripe backend key is required AND Price IDs are
    validated via stripe.Price.retrieve. Startup aborts on any miss.
    Dev/test: fail-open for non-financial surfaces, but never write live Stripe
    IDs into sandbox/local rows. Use scripts/sync_stripe_catalog.py to create
    and verify environment-specific sandbox catalog objects.
    """
    environment = _stripe_environment()
    expected_mode = "live" if _is_production() else "sandbox"
    try:
        resolved_key = configure_stripe_api_key(
            require_present=_is_production(),
            expected_mode=expected_mode if _is_production() else None,
        )
    except StripeConfigurationError as ex:
        blockers = ["stripe_key_invalid"]
        runtime_state.mark_stripe_catalog(
            ready=False,
            environment=environment,
            verified_at=None,
            blockers=blockers,
        )
        if _is_production():
            raise RuntimeError(f"Production startup: {ex}") from ex
        logger.warning("Stripe catalog startup skipped: %s", ex)
        await _provision_dev_catalog(db, blockers=blockers)
        return

    if not resolved_key:
        blockers = ["stripe_key_missing"]
        if _is_production():
            runtime_state.mark_stripe_catalog(
                ready=False,
                environment=environment,
                verified_at=None,
                blockers=blockers,
            )
            raise RuntimeError(
                "Production startup: Stripe server secret key missing. Subscriptions cannot operate."
            )
        logger.warning(
            "Stripe server secret key not set - local catalog rows will be upserted "
            "without Stripe object IDs."
        )
        await _provision_dev_catalog(db, blockers=blockers)
        runtime_state.mark_stripe_catalog(
            ready=False,
            environment=environment,
            verified_at=None,
            blockers=blockers,
        )
        return

    if not _is_production() and resolved_key.mode != "sandbox":
        blockers = ["stripe_key_wrong_environment"]
        logger.warning("Stripe catalog startup skipped: non-production requires a sandbox key.")
        await _provision_dev_catalog(db, blockers=blockers)
        runtime_state.mark_stripe_catalog(
            ready=False,
            environment=environment,
            verified_at=None,
            blockers=blockers,
        )
        return

    try:
        if _is_production():
            await _validate_prod_catalog(db)
            await _upsert_addon_catalog(
                db,
                stripe_catalog_environment="live",
                stripe_catalog_ready=True,
                stripe_catalog_verified_at=_now_iso(),
                stripe_catalog_blockers=[],
            )
            runtime_state.mark_stripe_catalog(
                ready=True,
                environment="live",
                verified_at=_now_iso(),
                blockers=[],
            )
            logger.info("Stripe catalog validated against configured Price IDs (production).")
        else:
            ready, verified_at, readiness_blockers = await _existing_environment_catalog_ready(
                db,
                "sandbox",
            )
            if ready:
                runtime_state.mark_stripe_catalog(
                    ready=True,
                    environment="sandbox",
                    verified_at=verified_at,
                    blockers=[],
                )
                logger.info("Stripe sandbox catalog readiness loaded from verified Mongo rows.")
                return
            blockers = (
                ["stripe_catalog_startup_provisioning_skipped"]
                if _skip_startup_stripe_provisioning() or not _startup_autoprovision_enabled()
                else ["stripe_catalog_sync_required"]
            )
            blockers.extend(readiness_blockers[:20])
            await _provision_dev_catalog(db, blockers=blockers)
            runtime_state.mark_stripe_catalog(
                ready=False,
                environment="sandbox",
                verified_at=None,
                blockers=blockers,
            )
            logger.info(
                "Stripe catalog startup checked (sandbox); use scripts/sync_stripe_catalog.py "
                "for controlled provisioning and verification."
            )
    except Exception as ex:
        if _is_production():
            runtime_state.mark_stripe_catalog(
                ready=False,
                environment=environment,
                verified_at=None,
                blockers=["stripe_catalog_validation_failed"],
            )
            raise
        logger.exception("Stripe catalog provisioning failed (dev) — continuing: %s", ex)
        blockers = ["stripe_catalog_startup_error"]
        await _provision_dev_catalog(db, blockers=blockers)
        runtime_state.mark_stripe_catalog(
            ready=False,
            environment=environment,
            verified_at=None,
            blockers=blockers,
        )
