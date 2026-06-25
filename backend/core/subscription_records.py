"""Account-level subscription projections for Phase 15R-C.

Stripe and Apple are payment providers. The app-facing entitlement rows live in
provider-neutral account collections so checkout/webhook details do not leak
into usage-limit enforcement code later.
"""
from __future__ import annotations

from typing import Any, Mapping

from core.entitlements import (
    empty_extra_quantities,
    normalize_plan_code,
    plan_by_code,
    subscription_to_account_limits_shape,
)


def account_subscription_shape(subscription: Mapping[str, Any]) -> dict[str, Any]:
    account_id = subscription.get("account_id") or subscription.get("barn_id")
    plan_code = normalize_plan_code(subscription.get("plan_code") or subscription.get("plan_tier_code") or "free")
    provider = subscription.get("billing_provider") or (
        "stripe" if subscription.get("stripe_subscription_id") or subscription.get("stripe_customer_id") else "manual"
    )
    platform = subscription.get("purchase_platform") or ("web" if provider == "stripe" else "admin")
    return {
        "account_id": account_id,
        "subscription_id": subscription.get("id") or subscription.get("stripe_subscription_id"),
        "plan_code": plan_code,
        "subscription_status": subscription.get("subscription_status") or subscription.get("status") or "active",
        "billing_provider": provider,
        "purchase_platform": platform,
        "billing_cycle": subscription.get("billing_cycle"),
        "amount_cents": subscription.get("amount_cents"),
        "current_period_start": subscription.get("current_period_start"),
        "current_period_end": subscription.get("current_period_end"),
        "trial_end": subscription.get("trial_end"),
        "cancel_at_period_end": subscription.get("cancel_at_period_end"),
        "stripe_customer_id": subscription.get("stripe_customer_id"),
        "stripe_subscription_id": subscription.get("stripe_subscription_id"),
        "stripe_price_id": subscription.get("stripe_price_id"),
        "apple_original_transaction_id": subscription.get("apple_original_transaction_id"),
        "apple_product_id": subscription.get("apple_product_id"),
        **{
            key: int(subscription.get(key) or 0)
            for key in empty_extra_quantities()
        },
    }


async def sync_account_subscription_records(db, subscription: Mapping[str, Any] | None) -> None:
    if not subscription:
        return
    account_row = account_subscription_shape(subscription)
    account_id = account_row.get("account_id")
    if not account_id:
        return
    plan = plan_by_code(account_row["plan_code"])
    limits_row = subscription_to_account_limits_shape(
        subscription=account_row,
        plan=plan,
        account_id=account_id,
    )
    await db.account_subscriptions.update_one(
        {"account_id": account_id},
        {
            "$set": account_row,
            "$setOnInsert": {"id": account_id},
        },
        upsert=True,
    )
    await db.account_usage_limits.update_one(
        {"account_id": account_id},
        {
            "$set": limits_row,
            "$setOnInsert": {"id": account_id},
        },
        upsert=True,
    )


async def sync_account_subscription_by_id(db, *, subscription_id: str | None = None, stripe_subscription_id: str | None = None) -> None:
    if stripe_subscription_id:
        sub = await db.subscriptions.find_one({"stripe_subscription_id": stripe_subscription_id}, {"_id": 0})
    elif subscription_id:
        sub = await db.subscriptions.find_one({"id": subscription_id}, {"_id": 0})
    else:
        sub = None
    await sync_account_subscription_records(db, sub)
