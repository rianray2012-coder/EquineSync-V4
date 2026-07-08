"""Phase 15R-A — provider-neutral entitlement schema prep.

These tests intentionally avoid live Stripe, Apple receipt validation,
checkout sessions, webhooks, and database writes. They pin the no-rework
contract that future Stripe/Apple billing adapters will use.
"""
from __future__ import annotations

import pytest

from core.entitlements import (
    CANONICAL_PLAN_CODES,
    LIMIT_FIELDS,
    PAYMENT_PROVIDERS,
    PLAN_CODE_ALIASES,
    PURCHASE_PLATFORMS,
    assert_known_plan_code,
    catalog_subscription_plan_shapes,
    customer_type_for_plan,
    derive_limits_from_plan_and_extras,
    feature_limits_to_entitlement_limits,
    normalize_plan_code,
    plan_by_code,
    plan_to_subscription_plan_shape,
    subscription_to_account_limits_shape,
)


def test_plan_code_aliases_normalize_founder_stripe_lookup_variants():
    assert PLAN_CODE_ALIASES["starter"] == "starter_barn"
    assert PLAN_CODE_ALIASES["professional"] == "advanced_barn"
    assert PLAN_CODE_ALIASES["trainer_no_lessons"] == "trainer_no_lesson"
    assert PLAN_CODE_ALIASES["trainer_lessons_15"] == "trainer_lesson_15"
    assert PLAN_CODE_ALIASES["trainer_lessons_50"] == "trainer_lesson_50"
    assert normalize_plan_code(" Starter ") == "starter_barn"
    assert assert_known_plan_code("professional") == "advanced_barn"
    assert normalize_plan_code(" Trainer_No_Lessons ") == "trainer_no_lesson"
    assert assert_known_plan_code("trainer_lessons_15") == "trainer_lesson_15"


def test_unknown_plan_code_fails_before_any_payment_adapter_work():
    with pytest.raises(ValueError):
        assert_known_plan_code("trainer_lesson_500")


def test_canonical_catalog_contains_founder_plan_set_once():
    expected = {
        "free",
        "individual_owner",
        "private_owner_plus",
        "service_provider_free",
        "service_provider_premium",
        "starter_barn",
        "advanced_barn",
        "elite_barn",
        "trainer_no_lesson",
        "trainer_lesson_15",
        "trainer_lesson_50",
        "enterprise",
        "community_program",
    }
    assert expected <= set(CANONICAL_PLAN_CODES)
    assert len(CANONICAL_PLAN_CODES) == len(set(CANONICAL_PLAN_CODES))


def test_invited_owner_portal_is_free_manual_access_not_paid_stripe_product():
    free = plan_to_subscription_plan_shape(plan_by_code("free"))
    assert free["plan_code"] == "free"
    assert free["display_name"] == "Invited Horse Owner Portal"
    assert free["customer_type"] == "invited_owner_portal"
    assert free["billing_channels"] == ["manual"]
    assert free["stripe_product_id"] is None
    assert free["stripe_monthly_price_id"] is None
    assert free["stripe_annual_price_id"] is None
    assert free["monthly_amount"] == 0
    assert free["annual_amount"] == 0
    assert free["included_horses"] == 0


def test_service_provider_free_is_manual_access_not_owner_portal():
    provider_free = plan_to_subscription_plan_shape(plan_by_code("service_provider_free"))
    assert provider_free["plan_code"] == "service_provider_free"
    assert provider_free["display_name"] == "Service Provider Free"
    assert provider_free["customer_type"] == "service_provider"
    assert provider_free["billing_channels"] == ["manual"]
    assert provider_free["monthly_amount"] == 0
    assert provider_free["annual_amount"] == 0


def test_service_provider_premium_is_paid_provider_plan():
    provider_premium = plan_to_subscription_plan_shape(plan_by_code("service_provider_premium"))
    assert provider_premium["plan_code"] == "service_provider_premium"
    assert provider_premium["customer_type"] == "service_provider"
    assert provider_premium["billing_channels"] == ["stripe", "apple"]
    assert provider_premium["monthly_amount"] == 1500
    assert provider_premium["annual_amount"] == 18000


def test_self_service_paid_plans_are_provider_neutral_for_web_and_ios():
    starter = plan_to_subscription_plan_shape(plan_by_code("starter_barn"))
    assert starter["plan_code"] == "starter_barn"
    assert starter["legacy_tier_code"] == "starter_barn"
    assert starter["customer_type"] == "facility"
    assert starter["billing_channels"] == ["stripe", "apple"]
    assert starter["monthly_amount"] == 6999
    assert starter["annual_amount"] == 69900
    assert starter["included_horses"] == 10
    assert starter["included_staff"] == 3
    assert starter["included_owner_managers"] == 1
    assert starter["included_lesson_participants"] == 0


def test_contact_sales_plans_remain_manual_or_comped_not_self_service_payment():
    enterprise = plan_to_subscription_plan_shape(plan_by_code("enterprise"))
    assert enterprise["plan_code"] == "enterprise"
    assert enterprise["customer_type"] == "enterprise"
    assert enterprise["billing_channels"] == ["manual", "comped"]
    assert enterprise["contact_sales"] is True
    assert enterprise["monthly_amount"] is None
    assert enterprise["annual_amount"] is None
    assert enterprise["included_horses"] is None


def test_limit_vocabulary_translates_existing_feature_limits():
    plan = plan_by_code("trainer_lesson_50")
    limits = feature_limits_to_entitlement_limits(plan["feature_limits"])
    assert tuple(limits.keys()) == LIMIT_FIELDS
    assert limits == {
        "horse_limit": 25,
        "staff_limit": 6,
        "owner_manager_limit": 3,
        "lesson_participant_limit": 50,
    }


def test_add_on_quantities_derive_future_effective_limits():
    plan = plan_by_code("advanced_barn")
    limits = derive_limits_from_plan_and_extras(
        plan,
        {
            "extra_horse_quantity": 2,
            "extra_staff_quantity": 1,
            "extra_owner_manager_quantity": 1,
        },
    )
    assert limits == {
        "horse_limit": 32,
        "staff_limit": 9,
        "owner_manager_limit": 3,
        "lesson_participant_limit": 0,
    }


def test_account_subscription_limits_shape_accepts_legacy_phase15_subscription():
    sub = {
        "barn_id": "barn_123",
        "plan_tier_code": "starter_barn",
        "status": "active",
        "stripe_customer_id": "cus_test_123",
        "stripe_subscription_id": "sub_test_123",
        "extra_horse_quantity": 2,
        "current_period_end": "2026-07-01T00:00:00+00:00",
    }
    shape = subscription_to_account_limits_shape(subscription=sub)
    assert shape["account_id"] == "barn_123"
    assert shape["plan_code"] == "starter_barn"
    assert shape["billing_provider"] == "stripe"
    assert shape["purchase_platform"] == "web"
    assert shape["subscription_status"] == "active"
    assert shape["horse_limit"] == 12
    assert shape["staff_limit"] == 3
    assert shape["owner_manager_limit"] == 1
    assert shape["lesson_participant_limit"] == 0
    assert shape["stripe_customer_id"] == "cus_test_123"
    assert shape["stripe_subscription_id"] == "sub_test_123"
    assert shape["apple_original_transaction_id"] is None
    assert shape["current_period_end"] == "2026-07-01T00:00:00+00:00"


@pytest.mark.parametrize(
    "status",
    ["canceled", "cancelled", "incomplete_expired", "unpaid", "incomplete"],
)
def test_account_subscription_limits_shape_drops_paid_limits_for_inactive_statuses(status):
    """15R-C lock fix: canceled/expired rows must not keep paid entitlements.

    The historical subscription row can still identify the paid Stripe plan in
    account_subscriptions, but the future enforcement mirror
    account_usage_limits must project the effective Free/portal limits.
    """
    sub = {
        "barn_id": "barn_canceled",
        "plan_tier_code": "starter_barn",
        "status": status,
        "stripe_customer_id": "cus_test_123",
        "stripe_subscription_id": "sub_test_123",
        "extra_horse_quantity": 99,
    }
    shape = subscription_to_account_limits_shape(subscription=sub)
    assert shape["account_id"] == "barn_canceled"
    assert shape["plan_code"] == "free"
    assert shape["subscription_status"] == ("canceled" if status == "cancelled" else status)
    assert shape["horse_limit"] == 0
    assert shape["staff_limit"] == 0
    assert shape["owner_manager_limit"] == 0
    assert shape["lesson_participant_limit"] == 0
    assert shape["extra_horse_quantity"] == 0


@pytest.mark.parametrize("status", ["active", "trialing", "past_due"])
def test_account_subscription_limits_shape_keeps_paid_limits_for_active_statuses(status):
    sub = {
        "barn_id": "barn_active",
        "plan_tier_code": "starter_barn",
        "status": status,
        "stripe_customer_id": "cus_test_123",
        "stripe_subscription_id": "sub_test_123",
        "extra_horse_quantity": 2,
    }
    shape = subscription_to_account_limits_shape(subscription=sub)
    assert shape["plan_code"] == "starter_barn"
    assert shape["subscription_status"] == status
    assert shape["horse_limit"] == 12
    assert shape["staff_limit"] == 3


def test_account_subscription_limits_shape_accepts_future_apple_subscription():
    sub = {
        "account_id": "acct_ios_1",
        "plan_code": "private_owner_plus",
        "status": "active",
        "billing_provider": "apple",
        "purchase_platform": "ios",
        "apple_original_transaction_id": "1000000000000001",
        "apple_product_id": "com.equinesync.private_owner_plus.monthly",
    }
    shape = subscription_to_account_limits_shape(subscription=sub)
    assert shape["account_id"] == "acct_ios_1"
    assert shape["plan_code"] == "private_owner_plus"
    assert shape["billing_provider"] == "apple"
    assert shape["purchase_platform"] == "ios"
    assert shape["horse_limit"] == 5
    assert shape["staff_limit"] == 0
    assert shape["owner_manager_limit"] == 1
    assert shape["stripe_customer_id"] is None
    assert shape["stripe_subscription_id"] is None
    assert shape["apple_original_transaction_id"] == "1000000000000001"


def test_catalog_shapes_use_future_subscription_plans_field_names():
    shapes = catalog_subscription_plan_shapes()
    assert len(shapes) == len(CANONICAL_PLAN_CODES)
    required = {
        "plan_code",
        "display_name",
        "stripe_product_id",
        "stripe_monthly_price_id",
        "stripe_annual_price_id",
        "monthly_amount",
        "annual_amount",
        "included_horses",
        "included_staff",
        "included_owner_managers",
        "included_lesson_participants",
        "customer_type",
        "is_active",
    }
    for shape in shapes:
        assert required <= set(shape)


def test_provider_and_platform_vocabulary_is_closed_for_future_adapters():
    assert PAYMENT_PROVIDERS == ("stripe", "apple", "manual", "comped")
    assert PURCHASE_PLATFORMS == ("web", "ios", "admin")


@pytest.mark.parametrize(
    ("plan_code", "customer_type"),
    [
        ("individual_owner", "individual_owner"),
        ("private_owner_plus", "individual_owner"),
        ("service_provider_free", "service_provider"),
        ("service_provider_premium", "service_provider"),
        ("starter_barn", "facility"),
        ("advanced_barn", "facility"),
        ("elite_barn", "facility"),
        ("trainer_no_lesson", "trainer"),
        ("trainer_lesson_15", "trainer"),
        ("trainer_lesson_50", "trainer"),
        ("enterprise", "enterprise"),
        ("community_program", "community"),
    ],
)
def test_customer_type_mapping_is_stable(plan_code, customer_type):
    assert customer_type_for_plan(plan_code) == customer_type
