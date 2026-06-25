"""Phase 15R-G — billing-channel routing prep.

No Stripe checkout, Apple receipt validation, webhooks, Mongo writes, or hard
enforcement are exercised here. These tests pin the provider/channel contract
that future web and iOS billing adapters will share.
"""
from __future__ import annotations

import pathlib

from core.billing_channels import (
    BILLING_PROVIDERS,
    PURCHASE_CHANNELS,
    build_billing_channel_dry_run,
    normalize_billing_channel,
    public_billing_channel_shape,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_vocabulary_matches_existing_15r_provider_channel_contract():
    assert BILLING_PROVIDERS == ("stripe", "apple", "manual", "comped")
    assert PURCHASE_CHANNELS == ("web", "ios", "admin")


def test_stripe_web_subscription_projects_to_cross_platform_access_without_ids():
    row = {
        "id": "sub_local_web",
        "account_id": "acct_web",
        "plan_code": "starter_barn",
        "status": "active",
        "billing_provider": "stripe",
        "purchase_channel": "web",
        "stripe_customer_id": "cus_test_123",
        "stripe_subscription_id": "sub_test_123",
        "stripe_price_id": "price_test_123",
    }

    projected = normalize_billing_channel(row)
    public = public_billing_channel_shape(row)

    assert projected["billing_provider"] == "stripe"
    assert projected["purchase_channel"] == "web"
    assert projected["platform_access"] == {"web_app": True, "ios_app": True}
    assert projected["app_access_policy"] == "subscription_is_cross_platform"
    assert projected["issues"] == []
    assert "stripe_customer_id" not in public
    assert "stripe_subscription_id" not in public
    assert "stripe_price_id" not in public


def test_future_apple_ios_subscription_projects_to_same_cross_platform_access():
    row = {
        "id": "sub_local_ios",
        "account_id": "acct_ios",
        "plan_code": "private_owner_plus",
        "status": "active",
        "billing_provider": "apple",
        "purchase_channel": "ios",
        "apple_original_transaction_id": "1000000000000001",
        "apple_product_id": "com.equinesync.private_owner_plus.monthly",
    }

    projected = normalize_billing_channel(row)
    public = public_billing_channel_shape(row)

    assert projected["billing_provider"] == "apple"
    assert projected["purchase_channel"] == "ios"
    assert projected["platform_access"] == {"web_app": True, "ios_app": True}
    assert projected["issues"] == []
    assert "apple_original_transaction_id" not in public
    assert "apple_product_id" not in public


def test_missing_provider_and_channel_are_inferred_without_blocking():
    stripe = normalize_billing_channel({
        "account_id": "acct_web",
        "plan_code": "starter_barn",
        "stripe_subscription_id": "sub_test_123",
    })
    apple = normalize_billing_channel({
        "account_id": "acct_ios",
        "plan_code": "private_owner_plus",
        "apple_original_transaction_id": "1000000000000001",
    })
    manual = normalize_billing_channel({
        "account_id": "acct_admin",
        "plan_code": "enterprise",
    })

    assert (stripe["billing_provider"], stripe["purchase_channel"]) == ("stripe", "web")
    assert (apple["billing_provider"], apple["purchase_channel"]) == ("apple", "ios")
    assert (manual["billing_provider"], manual["purchase_channel"]) == ("manual", "admin")
    assert stripe["provider_source"] == "inferred"
    assert apple["channel_source"] == "inferred"
    assert manual["issues"] == []


def test_unknown_provider_and_channel_are_warning_only_in_15r_g_dry_run():
    report = build_billing_channel_dry_run([
        {
            "id": "sub_unknown",
            "account_id": "acct_unknown",
            "plan_code": "starter_barn",
            "billing_provider": "cashapp",
            "purchase_channel": "android_store",
        }
    ])

    assert report["issue_counts"] == {"warning": 2}
    assert {issue["kind"] for issue in report["issues"]} == {
        "unknown_billing_provider",
        "unknown_purchase_channel",
    }
    assert not any(issue["severity"] == "blocker" for issue in report["issues"])
    assert report["preview_rows"][0]["platform_access"] == {"web_app": True, "ios_app": True}


def test_15r_g_does_not_touch_checkout_webhooks_or_payment_sdks():
    helper_src = (ROOT / "backend" / "core" / "billing_channels.py").read_text()
    forbidden = [
        "stripe.checkout",
        "Webhook",
        "construct_event",
        "apple receipt",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
    ]
    for token in forbidden:
        assert token not in helper_src
