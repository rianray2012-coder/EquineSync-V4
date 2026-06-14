"""core/billing_provisioning.py — Phase 15.A Stripe catalog provisioning.

Plan catalog source-of-truth lives in the local `plans` collection. This module
ensures that collection stays in sync with Stripe Products/Prices.

Two modes:
  - dev/test (APP_ENV != "production"): idempotently find-or-create Products
    + Prices in Stripe via metadata.equinesync_managed=true + metadata.tier_code.
  - production: read STRIPE_PRICE_* env vars, validate each Price exists in
    Stripe, abort startup with a clear error if any are missing/invalid.

Enterprise is NEVER provisioned in Stripe — it's Contact-Sales only.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

import stripe

logger = logging.getLogger(__name__)


# ---------- Static plan catalog (15% annual discount baked in) ----------
# monthly_price_cents → annual_price_cents = round(monthly * 12 * 0.85)
PLAN_CATALOG = [
    {
        "tier_code": "free",
        "name": "Free",
        "description": "For solo riders + owners exploring the network.",
        "monthly_price_cents": 0,
        "annual_price_cents": 0,
        "feature_limits": {
            "horses": 1,
            "users": 1,
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
        "tier_code": "starter",
        "name": "Starter",
        "description": "Up to 50 horses and 5 users. Basic scheduling + reporting.",
        "monthly_price_cents": 4900,    # $49
        "annual_price_cents": 49980,    # $499.80 (49 * 12 * 0.85)
        "feature_limits": {
            "horses": 50,
            "users": 5,
            "storage_gb": 5,
            "advanced_reporting": False,
            "medical_records": False,
            "messaging": False,
            "calendar_integrations": False,
            "api_access": False,
            "dedicated_support": False,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "professional",
        "name": "Professional",
        "description": "Up to 250 horses and 25 users. Advanced reporting, medical records, messaging, calendar integrations.",
        "monthly_price_cents": 14900,    # $149
        "annual_price_cents": 151980,    # $1,519.80 (149 * 12 * 0.85)
        "feature_limits": {
            "horses": 250,
            "users": 25,
            "storage_gb": 50,
            "advanced_reporting": True,
            "medical_records": True,
            "messaging": True,
            "calendar_integrations": True,
            "api_access": False,
            "dedicated_support": False,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
    },
    {
        "tier_code": "enterprise",
        "name": "Enterprise",
        "description": "Unlimited horses + users. API access, advanced integrations, dedicated support.",
        "monthly_price_cents": None,
        "annual_price_cents": None,
        "feature_limits": {
            "horses": None,    # unlimited
            "users": None,
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
]


def _is_production() -> bool:
    return (os.environ.get("APP_ENV") or "development").lower() == "production"


def _stripe_api_key() -> Optional[str]:
    return os.environ.get("STRIPE_API_KEY")


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


async def _provision_dev_catalog(db) -> None:
    """Dev/test only — idempotently create Products + Prices in Stripe and
    upsert local `plans` rows. Stripe failures are non-fatal in dev: we
    always upsert the local row, just without `stripe_*_id` if Stripe is
    unavailable (the /subscriptions/checkout endpoint will then return a
    clear 500 telling the operator the plan needs Stripe Price IDs).
    """
    for tier in PLAN_CATALOG:
        if not tier["stripe_provisioned"]:
            # Free + Enterprise: upsert local row only, no Stripe.
            await _upsert_plan(db, tier, None, None, None)
            continue
        product_id = None
        monthly_id = None
        annual_id = None
        try:
            product = await _find_managed_product(tier["tier_code"])
            if not product:
                product = stripe.Product.create(
                    name=f"Equine Sync — {tier['name']}",
                    description=tier["description"],
                    metadata={
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                    },
                )
                logger.info("stripe.Product created tier=%s id=%s",
                            tier["tier_code"], product["id"])
            product_id = product["id"]
            monthly = await _find_managed_price(product_id, tier["tier_code"], "month")
            if not monthly:
                monthly = stripe.Price.create(
                    product=product_id,
                    unit_amount=tier["monthly_price_cents"],
                    currency="usd",
                    recurring={"interval": "month"},
                    metadata={
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                        "interval": "month",
                    },
                )
                logger.info("stripe.Price created tier=%s interval=month id=%s",
                            tier["tier_code"], monthly["id"])
            monthly_id = monthly["id"]
            annual = await _find_managed_price(product_id, tier["tier_code"], "year")
            if not annual:
                annual = stripe.Price.create(
                    product=product_id,
                    unit_amount=tier["annual_price_cents"],
                    currency="usd",
                    recurring={"interval": "year"},
                    metadata={
                        "equinesync_managed": "true",
                        "tier_code": tier["tier_code"],
                        "interval": "year",
                    },
                )
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


async def _validate_prod_catalog(db) -> None:
    """Production only — env vars must exist, Prices must be valid in Stripe.
    Aborts startup with a clear error otherwise.
    """
    required = [
        "STRIPE_PRICE_STARTER_MONTHLY",
        "STRIPE_PRICE_STARTER_ANNUAL",
        "STRIPE_PRICE_PROFESSIONAL_MONTHLY",
        "STRIPE_PRICE_PROFESSIONAL_ANNUAL",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise RuntimeError(
            f"Production startup: required Stripe Price env vars missing: {missing}"
        )
    for env_var in required:
        price_id = os.environ[env_var]
        try:
            stripe.Price.retrieve(price_id)
        except stripe.error.StripeError as ex:
            raise RuntimeError(
                f"Production startup: STRIPE_PRICE env var '{env_var}'={price_id} "
                f"is not a valid Stripe Price: {ex}"
            ) from ex

    # Upsert local plans with the validated price IDs (no Stripe product creation in prod).
    env_map = {
        "starter": (
            os.environ["STRIPE_PRICE_STARTER_MONTHLY"],
            os.environ["STRIPE_PRICE_STARTER_ANNUAL"],
        ),
        "professional": (
            os.environ["STRIPE_PRICE_PROFESSIONAL_MONTHLY"],
            os.environ["STRIPE_PRICE_PROFESSIONAL_ANNUAL"],
        ),
    }
    for tier in PLAN_CATALOG:
        if not tier["stripe_provisioned"]:
            await _upsert_plan(db, tier, None, None, None)
            continue
        monthly_id, annual_id = env_map[tier["tier_code"]]
        # Resolve product_id from one of the prices for consistency.
        try:
            pr = stripe.Price.retrieve(monthly_id)
            product_id = pr.get("product")
        except Exception:
            product_id = None
        await _upsert_plan(db, tier, product_id, monthly_id, annual_id)


async def _upsert_plan(db, tier, product_id, monthly_price_id, annual_price_id):
    update = {
        "tier_code": tier["tier_code"],
        "name": tier["name"],
        "description": tier["description"],
        "monthly_price_cents": tier["monthly_price_cents"],
        "annual_price_cents": tier["annual_price_cents"],
        "feature_limits": tier["feature_limits"],
        "contact_sales": tier["contact_sales"],
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


async def ensure_stripe_catalog(db) -> None:
    """Entry point — called from lifespan.on_startup.

    Production: STRIPE_API_KEY is required AND env-provided Price IDs are
    validated via stripe.Price.retrieve. Startup aborts on any miss.
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
            "Local `plans` rows still upserted with null Stripe IDs."
        )
        # Codex finding #3: upsert ALL four plans (including Starter +
        # Professional with null Stripe IDs) so /billing/plans returns a
        # consistent catalog in dev when the key is missing.
        for tier in PLAN_CATALOG:
            await _upsert_plan(db, tier, None, None, None)
        return

    stripe.api_key = api_key
    try:
        if _is_production():
            await _validate_prod_catalog(db)
            logger.info("Stripe catalog validated against env Price IDs (production).")
        else:
            await _provision_dev_catalog(db)
            logger.info("Stripe catalog provisioned (dev/test mode).")
    except Exception as ex:
        if _is_production():
            raise
        logger.exception("Stripe catalog provisioning failed (dev) — continuing: %s", ex)
        # Codex finding #3: even on dev failure, make sure all four plan
        # rows exist with null Stripe IDs.
        for tier in PLAN_CATALOG:
            existing = await db.plans.find_one({"tier_code": tier["tier_code"]})
            if not existing:
                await _upsert_plan(db, tier, None, None, None)
