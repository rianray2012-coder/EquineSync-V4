"""core/billing_provisioning.py — Phase 15/15R Stripe catalog provisioning.

Plan catalog source-of-truth lives in the local `plans` collection. This module
ensures that collection stays in sync with Stripe Products/Prices.

Two modes:
  - dev/test (APP_ENV != "production"): upsert local catalog rows using the
    founder-approved live Stripe Price IDs below. Stripe API connectivity is
    optional; local catalog rows are still present when no key is configured.
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
from typing import Any, Optional

import stripe

from core.stripe_client import stripe_client

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
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_horse_starter": {
        "stripe_product_id": "prod_UjfG9GupHWHLW7",
        "stripe_price_id": "price_1TkBx7JLyFSImf6YM4Tb1Rk2",
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_horse_advanced": {
        "stripe_product_id": "prod_UjfMUbJIX0dGCn",
        "stripe_price_id": "price_1TkC2TJLyFSImf6Y9UpftKsE",
        "limit_field": "horse_limit",
        "quantity_field": "extra_horse_quantity",
    },
    "additional_staff_seat": {
        "stripe_product_id": "prod_UjfOyluZB1a5fz",
        "stripe_price_id": "price_1TkC4zJLyFSImf6YIxPX8p1T",
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
    },
    "additional_helper_seat": {
        "stripe_product_id": "prod_UjmnLwJsDo60A8",
        "stripe_price_id": "price_1TkVOtJLyFSImf6YeP9sqy24",
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
    },
    "additional_owner_manager_seat": {
        "stripe_product_id": "prod_UjfTFLjeVwqI1e",
        "stripe_price_id": "price_1TkCANJLyFSImf6Yv05S9zzm",
        "limit_field": "owner_manager_limit",
        "quantity_field": "extra_owner_manager_quantity",
    },
    "elite_owner_manager_seat": {
        "stripe_product_id": "prod_UjfW7Op9Mhdexa",
        "stripe_price_id": "price_1TkCI2JLyFSImf6YDIdCme7h",
        "limit_field": "owner_manager_limit",
        "quantity_field": "extra_owner_manager_quantity",
    },
    "additional_lesson_participant": {
        "stripe_product_id": "prod_UjfxNgUirIWN2v",
        "stripe_price_id": "price_1TkChgJLyFSImf6YSdp304bC",
        "limit_field": "lesson_participant_limit",
        "quantity_field": "extra_lesson_participant_quantity",
    },
    "extra_storage": {
        "stripe_product_id": "prod_UjgHub3Fg5z5vJ",
        "stripe_price_id": "price_1TkCxGJLyFSImf6YfsgThUvN",
        "limit_field": "storage_gb",
        "quantity_field": "extra_storage_quantity",
    },
    "custom_branding": {
        "stripe_product_id": "prod_UjlUaSBvFXWYaQ",
        "stripe_price_id": "price_1TkIgOJLyFSImf6Y3LDwBXph",
        "limit_field": "custom_branding",
        "quantity_field": "custom_branding_quantity",
    },
    "ai_owner_update_assistant": {
        "stripe_product_id": "prod_UjmHtMJjtrDFtx",
        "stripe_price_id": "price_1TkImnJLyFSImf6YRMfk0su5",
        "limit_field": "ai_owner_update_assistant",
        "quantity_field": "ai_owner_update_assistant_quantity",
    },
    "quickbooks_integration": {
        "stripe_product_id": "prod_UjmMqco5cNTifU",
        "stripe_price_id": "price_1TkIzJJLyFSImf6YOPLPtSon",
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


def _configured_price_ids(tier_code: str) -> tuple[Optional[str], Optional[str]]:
    """Return monthly/annual Price IDs from env overrides or live catalog map."""
    monthly_env, annual_env = _price_env_vars(tier_code)
    mapped = LIVE_STRIPE_PRICE_IDS.get(tier_code) or {}
    return (
        os.environ.get(monthly_env) or mapped.get("monthly"),
        os.environ.get(annual_env) or mapped.get("annual"),
    )


def _configured_product_id(tier_code: str) -> Optional[str]:
    return os.environ.get(f"STRIPE_PRODUCT_{tier_code.upper()}") or LIVE_STRIPE_PRODUCT_IDS.get(tier_code)


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


def _stripe_api_key() -> Optional[str]:
    return os.environ.get("STRIPE_API_KEY")


async def _find_managed_product(client, tier_code: str):
    """Find a Stripe Product previously created by EquineSync via metadata."""
    # Stripe doesn't search Products by metadata directly — list + filter is fine
    # for the 2 products we manage. Idempotent restart-safe lookup.
    products = client.v1.products.list({"limit": 100, "active": True})
    for p in products.auto_paging_iter():
        meta = p.get("metadata") or {}
        if meta.get("equinesync_managed") == "true" and meta.get("tier_code") == tier_code:
            return p
    return None


async def _find_managed_price(client, product_id: str, tier_code: str, interval: str):
    """Find a managed Price for (tier_code, interval) under a product."""
    prices = client.v1.prices.list({"limit": 100, "active": True, "product": product_id})
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


async def _provision_dev_catalog(db, client) -> None:
    """Dev/test only — upsert local `plans` rows from the live Price map.

    Older Phase 15 dev behavior auto-created Stripe Products/Prices. Now that
    live Price IDs exist, dev/test should not mint parallel Stripe catalog
    objects. If an operator intentionally clears the static map for a future
    test plan, the old find-or-create path below remains available for that
    unmapped plan only.
    """
    for tier in PLAN_CATALOG:
        if not tier["stripe_provisioned"]:
            # Free + custom-contract tiers: upsert local row only, no Stripe.
            await _upsert_plan(db, tier, _configured_product_id(tier["tier_code"]), None, None)
            continue
        configured_monthly, configured_annual = _configured_price_ids(tier["tier_code"])
        if configured_monthly and configured_annual:
            await _upsert_plan(
                db,
                tier,
                _configured_product_id(tier["tier_code"]),
                configured_monthly,
                configured_annual,
            )
            continue
        product_id = None
        monthly_id = None
        annual_id = None
        try:
            product = await _find_managed_product(client, tier["tier_code"])
            if not product:
                product = client.v1.products.create({
                    "name": f"Equine Sync — {tier['name']}",
                    "description": tier["description"],
                    "metadata": {
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                    },
                })
                logger.info("stripe.Product created tier=%s id=%s",
                            tier["tier_code"], product["id"])
            product_id = product["id"]
            monthly = await _find_managed_price(client, product_id, tier["tier_code"], "month")
            if not monthly:
                monthly = client.v1.prices.create({
                    "product": product_id,
                    "unit_amount": tier["monthly_price_cents"],
                    "currency": "usd",
                    "recurring": {"interval": "month"},
                    "metadata": {
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                        "interval": "month",
                    },
                })
                logger.info("stripe.Price created tier=%s interval=month id=%s",
                            tier["tier_code"], monthly["id"])
            monthly_id = monthly["id"]
            annual = await _find_managed_price(client, product_id, tier["tier_code"], "year")
            if not annual:
                annual = client.v1.prices.create({
                    "product": product_id,
                    "unit_amount": tier["annual_price_cents"],
                    "currency": "usd",
                    "recurring": {"interval": "year"},
                    "metadata": {
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                        "interval": "year",
                    },
                })
                logger.info("stripe.Price created tier=%s interval=year id=%s",
                            tier["tier_code"], annual["id"])
            annual_id = annual["id"]
        except Exception as ex:
            logger.warning(
                "Dev Stripe catalog: could not provision tier=%s — "
                "local plan row will lack Stripe IDs until a valid key is "
                "configured. Reason: %s",
                tier["tier_code"], ex,
            )
        await _upsert_plan(db, tier, product_id, monthly_id, annual_id)


async def _validate_prod_catalog(db, client) -> None:
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
        monthly_id, annual_id = _configured_price_ids(tier["tier_code"])
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
            await _upsert_plan(db, tier, _configured_product_id(tier["tier_code"]), None, None)
            continue
        monthly_id, annual_id = configured[tier["tier_code"]]
        for label, price_id in (("monthly", monthly_id), ("annual", annual_id)):
            try:
                client.v1.prices.retrieve(price_id)
            except stripe.error.StripeError as ex:
                raise RuntimeError(
                    f"Production startup: {tier['tier_code']} {label} Price {price_id} "
                    f"is not a valid Stripe Price: {ex}"
                ) from ex
        # Resolve product_id from one of the prices for consistency.
        try:
            pr = client.v1.prices.retrieve(monthly_id)
            product_id = pr.get("product") or _configured_product_id(tier["tier_code"])
        except Exception:
            product_id = _configured_product_id(tier["tier_code"])
        await _upsert_plan(db, tier, product_id, monthly_id, annual_id)


async def _upsert_plan(db, tier, product_id, monthly_price_id, annual_price_id):
    product_id = product_id or _configured_product_id(tier["tier_code"])
    if tier["stripe_provisioned"]:
        fallback_monthly, fallback_annual = _configured_price_ids(tier["tier_code"])
        monthly_price_id = monthly_price_id or fallback_monthly
        annual_price_id = annual_price_id or fallback_annual
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
        "active": True,
    }
    await db.plans.update_one(
        {"tier_code": tier["tier_code"]},
        {"$set": update, "$setOnInsert": {"id": tier["tier_code"]}},
        upsert=True,
    )
    await _upsert_subscription_plan(db, tier, product_id, monthly_price_id, annual_price_id)


async def _upsert_subscription_plan(db, tier, product_id, monthly_price_id, annual_price_id):
    plan_code = tier["tier_code"]
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
        "is_active": True,
    }
    await db.subscription_plans.update_one(
        {"plan_code": plan_code},
        {"$set": update, "$setOnInsert": {"id": plan_code}},
        upsert=True,
    )


async def _upsert_addon_catalog(db):
    for addon_code, config in ADDON_PRICE_CATALOG.items():
        update = {
            "addon_code": addon_code,
            "stripe_product_id": config.get("stripe_product_id"),
            "stripe_price_id": config["stripe_price_id"],
            "billing_provider": "stripe",
            "billing_channel": "web",
            "recurring": True,
            "limit_field": config["limit_field"],
            "quantity_field": config["quantity_field"],
            "is_active": True,
        }
        await db.subscription_addons.update_one(
            {"addon_code": addon_code},
            {"$set": update, "$setOnInsert": {"id": addon_code}},
            upsert=True,
        )


async def ensure_stripe_catalog(db) -> None:
    """Entry point — called from lifespan.on_startup.

    Production: STRIPE_API_KEY is required AND env-provided Price IDs are
    validated via a client-scoped Stripe Price retrieve. Startup aborts on any
    miss.
    Dev: fail-open. Local `plans` rows are ALWAYS upserted (all 4 tiers,
    including Starter/Professional with null Stripe IDs when Stripe is
    unreachable) so /billing/plans is consistent across environments.
    """
    api_key = _stripe_api_key()
    if not api_key:
        if _is_production():
            raise RuntimeError(
                "Production startup: STRIPE_API_KEY missing. Subscriptions cannot operate."
            )
        logger.warning(
            "STRIPE_API_KEY not set — skipping Stripe provisioning. "
            "Local catalog rows still upserted with configured Stripe Price IDs."
        )
        # Codex finding #3: upsert ALL four plans (including Starter +
        # Professional with null Stripe IDs) so /billing/plans returns a
        # consistent catalog in dev when the key is missing.
        for tier in PLAN_CATALOG:
            monthly_id, annual_id = _configured_price_ids(tier["tier_code"])
            await _upsert_plan(db, tier, None, monthly_id, annual_id)
        await _upsert_addon_catalog(db)
        return

    client = stripe_client(api_key)
    try:
        if _is_production():
            await _validate_prod_catalog(db, client)
            logger.info("Stripe catalog validated against env Price IDs (production).")
        else:
            await _provision_dev_catalog(db, client)
            logger.info("Stripe catalog provisioned (dev/test mode).")
        await _upsert_addon_catalog(db)
    except Exception as ex:
        if _is_production():
            raise
        logger.exception("Stripe catalog provisioning failed (dev) — continuing: %s", ex)
        # Codex finding #3: even on dev failure, make sure all catalog plan
        # rows exist with null Stripe IDs.
        for tier in PLAN_CATALOG:
            existing = await db.plans.find_one({"tier_code": tier["tier_code"]})
            if not existing:
                monthly_id, annual_id = _configured_price_ids(tier["tier_code"])
                await _upsert_plan(db, tier, None, monthly_id, annual_id)
        await _upsert_addon_catalog(db)
