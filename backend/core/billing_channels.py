"""Billing-channel routing helpers for Phase 15R-G.

This module is read-only. It prepares the web Stripe vs future Apple App Store
contract without creating checkout sessions, validating Apple receipts,
processing webhooks, mutating subscription items, or enforcing usage limits.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from core.entitlements import (
    PAYMENT_PROVIDERS,
    PURCHASE_PLATFORMS,
    normalize_plan_code,
    normalize_subscription_status,
)


BILLING_PROVIDERS = PAYMENT_PROVIDERS
PURCHASE_CHANNELS = PURCHASE_PLATFORMS


def _clean(value: Any) -> str:
    return (str(value or "")).strip().lower()


def _record_ref(row: Mapping[str, Any]) -> str:
    return str(
        row.get("id")
        or row.get("account_id")
        or row.get("barn_id")
        or row.get("stripe_subscription_id")
        or row.get("apple_original_transaction_id")
        or "(unknown)"
    )


def _infer_provider(row: Mapping[str, Any]) -> str:
    if row.get("stripe_subscription_id") or row.get("stripe_customer_id") or row.get("stripe_price_id"):
        return "stripe"
    if row.get("apple_original_transaction_id") or row.get("apple_product_id"):
        return "apple"
    if row.get("comped_by") or _clean(row.get("subscription_status") or row.get("status")) == "comped":
        return "comped"
    return "manual"


def _infer_channel(provider: str) -> str:
    if provider == "stripe":
        return "web"
    if provider == "apple":
        return "ios"
    return "admin"


def normalize_billing_channel(row: Mapping[str, Any]) -> dict[str, Any]:
    """Project one subscription/account row into the future routing contract.

    Unknown provider/channel values are warning-level issues in this helper,
    because 15R-G is a prep-only visibility pass. Existing 15R-B migration
    blocker semantics are intentionally left unchanged.
    """
    issues: list[dict[str, str]] = []
    raw_provider = _clean(row.get("billing_provider"))
    provider = raw_provider or _infer_provider(row)
    provider_source = "explicit" if raw_provider else "inferred"
    if provider not in BILLING_PROVIDERS:
        issues.append({
            "kind": "unknown_billing_provider",
            "message": f"{provider!r} is not in {BILLING_PROVIDERS}.",
        })

    raw_channel = _clean(row.get("purchase_channel") or row.get("purchase_platform"))
    channel = raw_channel or _infer_channel(provider)
    channel_source = "explicit" if raw_channel else "inferred"
    if channel not in PURCHASE_CHANNELS:
        issues.append({
            "kind": "unknown_purchase_channel",
            "message": f"{channel!r} is not in {PURCHASE_CHANNELS}.",
        })

    plan_code = normalize_plan_code(row.get("plan_code") or row.get("plan_tier_code") or "free")
    return {
        "account_id": row.get("account_id") or row.get("barn_id"),
        "subscription_id": row.get("id") or row.get("subscription_id"),
        "plan_code": plan_code,
        "subscription_status": normalize_subscription_status(row.get("subscription_status") or row.get("status")),
        "billing_provider": provider,
        "purchase_channel": channel,
        # Compatibility name for current account_subscriptions rows.
        "purchase_platform": channel,
        "provider_source": provider_source,
        "channel_source": channel_source,
        "platform_access": {
            "web_app": True,
            "ios_app": True,
        },
        "app_access_policy": "subscription_is_cross_platform",
        "issues": issues,
    }


def public_billing_channel_shape(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return a public/app-safe channel shape with payment operational IDs omitted."""
    projected = normalize_billing_channel(row)
    return {
        "account_id": projected["account_id"],
        "plan_code": projected["plan_code"],
        "subscription_status": projected["subscription_status"],
        "billing_provider": projected["billing_provider"],
        "purchase_channel": projected["purchase_channel"],
        "platform_access": projected["platform_access"],
        "app_access_policy": projected["app_access_policy"],
    }


def build_billing_channel_dry_run(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    preview = []
    issues = []
    provider_counts = Counter()
    channel_counts = Counter()

    for row in rows:
        projected = normalize_billing_channel(row)
        preview.append(public_billing_channel_shape(row))
        provider_counts[projected["billing_provider"]] += 1
        channel_counts[projected["purchase_channel"]] += 1
        for issue in projected.get("issues") or []:
            issues.append({
                "severity": "warning",
                "kind": issue["kind"],
                "record": _record_ref(row),
                "message": issue["message"],
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_counts": {"rows": len(preview)},
        "provider_counts": dict(sorted(provider_counts.items())),
        "channel_counts": dict(sorted(channel_counts.items())),
        "issue_counts": dict(sorted(Counter(issue["severity"] for issue in issues).items())),
        "issues": issues,
        "preview_rows": preview,
    }
