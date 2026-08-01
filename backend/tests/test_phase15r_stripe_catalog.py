"""Phase 15R-H — live Stripe catalog reconciliation tests.

These tests are intentionally local-only. They verify founder-provided Stripe
Price IDs and provider-neutral account-limit projections without making Stripe
API calls or requiring secret keys.
"""
from __future__ import annotations

import asyncio
import pathlib

from core.billing_provisioning import (
    ADDON_PRICE_CATALOG,
    LIVE_STRIPE_PRODUCT_IDS,
    LIVE_STRIPE_PRICE_IDS,
    PLAN_CATALOG,
    ensure_stripe_catalog,
    normalize_stripe_plan_code,
)
from core.stripe_catalog_sync import build_stripe_catalog_definition, catalog_counts
from core.stripe_config import StripeConfigurationError, resolve_stripe_secret_key
from core.subscription_records import account_subscription_shape


ROOT = pathlib.Path(__file__).resolve().parents[2]


EXPECTED_PLAN_PRICES = {
    "individual_owner": ("price_1Tk2ljJLyFSImf6Y7m62C3gd", "price_1Tk2mRJLyFSImf6YRlPmlu1l"),
    "private_owner_plus": ("price_1TkB5ZJLyFSImf6YsGv51iHN", "price_1TkB6IJLyFSImf6Y6EUh8Dwc"),
    "starter_barn": ("price_1TkB8uJLyFSImf6YZC8LQzmU", "price_1TkBBUJLyFSImf6Ye3scNRy8"),
    "advanced_barn": ("price_1TkBDiJLyFSImf6YOMe6g8My", "price_1TkBERJLyFSImf6Y8cSX569Z"),
    "elite_barn": ("price_1TkBHjJLyFSImf6YBV9KVZrP", "price_1TkBPlJLyFSImf6YuGXkuvT0"),
    "trainer_no_lesson": ("price_1TkBRMJLyFSImf6YygjgN0Bn", "price_1TkBYEJLyFSImf6YjwI4HP5w"),
    "trainer_lesson_15": ("price_1TkBhzJLyFSImf6YrAGxDoVn", "price_1TkBkFJLyFSImf6Y6ClbJiPO"),
    "trainer_lesson_50": ("price_1TkBnYJLyFSImf6Y1SvF9uLQ", "price_1TkBpaJLyFSImf6YMeu5YlRw"),
}

EXPECTED_PLAN_PRODUCTS = {
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

EXPECTED_ADDONS = {
    "additional_horse_standard": ("prod_UjfDx3cO3OgYG9", "price_1TkBuUJLyFSImf6YtzCNBmTT"),
    "additional_horse_starter": ("prod_UjfG9GupHWHLW7", "price_1TkBx7JLyFSImf6YM4Tb1Rk2"),
    "additional_horse_advanced": ("prod_UjfMUbJIX0dGCn", "price_1TkC2TJLyFSImf6Y9UpftKsE"),
    "additional_staff_seat": ("prod_UjfOyluZB1a5fz", "price_1TkC4zJLyFSImf6YIxPX8p1T"),
    "additional_helper_seat": ("prod_UjmnLwJsDo60A8", "price_1TkVOtJLyFSImf6YeP9sqy24"),
    "additional_owner_manager_seat": ("prod_UjfTFLjeVwqI1e", "price_1TkCANJLyFSImf6Yv05S9zzm"),
    "elite_owner_manager_seat": ("prod_UjfW7Op9Mhdexa", "price_1TkCI2JLyFSImf6YDIdCme7h"),
    "additional_lesson_participant": ("prod_UjfxNgUirIWN2v", "price_1TkChgJLyFSImf6YSdp304bC"),
    "extra_storage": ("prod_UjgHub3Fg5z5vJ", "price_1TkCxGJLyFSImf6YfsgThUvN"),
    "custom_branding": ("prod_UjlUaSBvFXWYaQ", "price_1TkIgOJLyFSImf6Y3LDwBXph"),
    "ai_owner_update_assistant": ("prod_UjmHtMJjtrDFtx", "price_1TkImnJLyFSImf6YRMfk0su5"),
    "quickbooks_integration": ("prod_UjmMqco5cNTifU", "price_1TkIzJJLyFSImf6YOPLPtSon"),
}


def test_live_stripe_plan_price_ids_are_wired_exactly():
    assert set(LIVE_STRIPE_PRICE_IDS) == set(EXPECTED_PLAN_PRICES)
    for plan_code, (monthly, annual) in EXPECTED_PLAN_PRICES.items():
        assert LIVE_STRIPE_PRICE_IDS[plan_code]["monthly"] == monthly
        assert LIVE_STRIPE_PRICE_IDS[plan_code]["annual"] == annual


def test_live_stripe_product_ids_are_wired_exactly_from_pdf_catalog():
    assert LIVE_STRIPE_PRODUCT_IDS == EXPECTED_PLAN_PRODUCTS


def test_contact_sales_and_free_plans_have_no_live_stripe_price_mapping():
    assert "free" not in LIVE_STRIPE_PRICE_IDS
    assert "service_provider_free" not in LIVE_STRIPE_PRICE_IDS
    assert "service_provider_premium" not in LIVE_STRIPE_PRICE_IDS
    assert "enterprise" not in LIVE_STRIPE_PRICE_IDS
    assert "community_program" not in LIVE_STRIPE_PRICE_IDS
    assert "free" not in LIVE_STRIPE_PRODUCT_IDS
    assert "service_provider_free" not in LIVE_STRIPE_PRODUCT_IDS
    assert "service_provider_premium" not in LIVE_STRIPE_PRODUCT_IDS
    assert LIVE_STRIPE_PRODUCT_IDS["enterprise"].startswith("prod_")
    assert LIVE_STRIPE_PRODUCT_IDS["community_program"].startswith("prod_")


def test_founder_trainer_lookup_aliases_normalize_to_canonical_codes():
    assert normalize_stripe_plan_code("trainer_no_lessons") == "trainer_no_lesson"
    assert normalize_stripe_plan_code("trainer_lessons_15") == "trainer_lesson_15"
    assert normalize_stripe_plan_code("trainer_lessons_50") == "trainer_lesson_50"


def test_live_stripe_addon_price_ids_are_wired_exactly():
    assert set(ADDON_PRICE_CATALOG) == set(EXPECTED_ADDONS)
    for addon_code, (product_id, price_id) in EXPECTED_ADDONS.items():
        assert ADDON_PRICE_CATALOG[addon_code]["stripe_product_id"] == product_id
        assert ADDON_PRICE_CATALOG[addon_code]["stripe_price_id"] == price_id
        assert ADDON_PRICE_CATALOG[addon_code]["quantity_field"].startswith((
            "extra_",
            "custom_",
            "ai_",
            "quickbooks_",
        ))


def test_latest_founder_limits_are_in_plan_catalog():
    plans = {p["tier_code"]: p for p in PLAN_CATALOG}
    assert plans["individual_owner"]["feature_limits"]["horses"] == 1
    assert plans["individual_owner"]["feature_limits"]["owner_manager_seats"] == 1
    assert plans["service_provider_free"]["monthly_price_cents"] == 0
    assert plans["service_provider_free"]["stripe_provisioned"] is False
    assert plans["service_provider_free"]["feature_limits"]["basic_horse_info"] is True
    assert plans["service_provider_free"]["feature_limits"]["calendar_visibility"] is True
    assert plans["service_provider_free"]["feature_limits"]["appointment_scheduling"] is True
    assert plans["service_provider_premium"]["monthly_price_cents"] == 1500
    assert plans["service_provider_premium"]["annual_price_cents"] == 18000
    assert plans["service_provider_premium"]["stripe_provisioned"] is True
    assert plans["service_provider_premium"]["feature_limits"]["premium_provider_features"] is True
    assert plans["private_owner_plus"]["feature_limits"]["horses"] == 5
    assert plans["private_owner_plus"]["feature_limits"]["users"] == 2
    assert plans["private_owner_plus"]["feature_limits"]["staff_seats"] == 0
    assert plans["private_owner_plus"]["feature_limits"]["helper_family_seats"] == 1
    assert plans["private_owner_plus"]["feature_limits"]["owner_manager_seats"] == 1
    assert "Includes everything in Individual Horse Owner" in plans["private_owner_plus"]["description"]
    assert plans["starter_barn"]["feature_limits"]["horses"] == 10
    assert plans["starter_barn"]["feature_limits"]["staff_seats"] == 3
    assert plans["advanced_barn"]["feature_limits"]["horses"] == 30
    assert plans["advanced_barn"]["feature_limits"]["owner_manager_seats"] == 2
    assert plans["elite_barn"]["feature_limits"]["horses"] == 50
    assert plans["elite_barn"]["feature_limits"]["owner_manager_seats"] == 4
    assert plans["trainer_no_lesson"]["feature_limits"]["horses"] == 20
    assert plans["trainer_lesson_15"]["feature_limits"]["lesson_participants"] == 15
    assert plans["trainer_lesson_50"]["feature_limits"]["lesson_participants"] == 50
    assert plans["enterprise"]["feature_limits"]["horses"] is None
    assert plans["community_program"]["feature_limits"]["horses"] is None


def test_account_subscription_shape_is_provider_neutral_for_stripe_and_apple():
    stripe_row = account_subscription_shape({
        "barn_id": "barn_web",
        "plan_tier_code": "starter_barn",
        "status": "active",
        "stripe_customer_id": "cus_test_123",
        "stripe_subscription_id": "sub_test_123",
        "stripe_price_id": EXPECTED_PLAN_PRICES["starter_barn"][0],
    })
    assert stripe_row["account_id"] == "barn_web"
    assert stripe_row["plan_code"] == "starter_barn"
    assert stripe_row["billing_provider"] == "stripe"
    assert stripe_row["purchase_platform"] == "web"

    apple_row = account_subscription_shape({
        "account_id": "acct_ios",
        "plan_code": "trainer_lessons_15",
        "billing_provider": "apple",
        "purchase_platform": "ios",
        "apple_original_transaction_id": "1000000000000001",
    })
    assert apple_row["plan_code"] == "trainer_lesson_15"
    assert apple_row["billing_provider"] == "apple"
    assert apple_row["purchase_platform"] == "ios"
    assert apple_row["stripe_subscription_id"] is None


def test_stripe_webhook_handlers_normalize_founder_alias_metadata_before_lookup():
    src = (ROOT / "backend" / "routes" / "subscriptions_webhook_handlers.py").read_text()
    assert "from core.entitlements import normalize_plan_code" in src
    assert 'normalize_plan_code(metadata.get("plan_tier_code"))' in src
    assert 'normalize_plan_code(\n        metadata.get("plan_tier_code")' in src


def test_dev_webhook_route_does_not_require_stripe_api_key_before_dispatch():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert "_stripe_init()\n\n        if secret:" not in src
    assert "configure_stripe_api_key(" in src
    assert "require_present=_is_production()" in src
    assert "STRIPE_API_KEY is required in production" not in src


def test_no_secret_keys_were_committed_for_15r_h():
    paths = [
        ROOT / "backend" / "core" / "billing_provisioning.py",
        ROOT / "backend" / "core" / "subscription_records.py",
        ROOT / "docs" / "PHASE_15R_BILLING_ENTITLEMENTS_REFACTOR.md",
    ]
    combined = "\n".join(p.read_text() for p in paths)
    assert "sk_live_" not in combined
    assert "rk_live_" not in combined


def test_stripe_secret_key_is_canonical_with_api_key_fallback():
    key = "sk_test_same_value"
    resolved = resolve_stripe_secret_key({
        "STRIPE_SECRET_KEY": key,
        "STRIPE_API_KEY": key,
    })
    assert resolved.source == "STRIPE_SECRET_KEY"
    assert resolved.mode == "sandbox"

    fallback = resolve_stripe_secret_key({"STRIPE_API_KEY": "sk_test_fallback"})
    assert fallback.source == "STRIPE_API_KEY"
    assert fallback.mode == "sandbox"


def test_mismatched_stripe_secret_and_api_key_fail_closed():
    try:
        resolve_stripe_secret_key({
            "STRIPE_SECRET_KEY": "sk_test_one",
            "STRIPE_API_KEY": "sk_test_two",
        })
    except StripeConfigurationError as ex:
        assert "differ" in str(ex)
    else:
        raise AssertionError("mismatched Stripe key env values must fail closed")


def test_sandbox_catalog_lookup_keys_are_environment_scoped():
    definition = build_stripe_catalog_definition("sandbox")
    counts = catalog_counts(definition)
    assert counts["plan_products"] == 11
    assert counts["addon_products"] == 12
    assert counts["plan_prices"] == 18
    assert counts["addon_prices"] == 12
    assert counts["blockers"] == 0
    assert "free" in definition.local_only_plan_codes
    assert "service_provider_free" in definition.local_only_plan_codes
    assert set(definition.contact_sales_plan_codes) == {"enterprise", "community_program"}
    lookup_keys = {price.lookup_key for price in definition.prices}
    assert "equinesync.sandbox.plan.starter_barn.monthly" in lookup_keys
    assert "equinesync.sandbox.plan.service_provider_premium.annual" in lookup_keys
    assert "equinesync.sandbox.addon.quickbooks_integration.monthly" in lookup_keys


def test_addons_have_canonical_amount_currency_and_interval_terms():
    for addon_code, config in ADDON_PRICE_CATALOG.items():
        assert isinstance(config.get("unit_amount_cents"), int), addon_code
        assert config["unit_amount_cents"] > 0, addon_code
        assert config.get("currency") == "usd", addon_code
        assert config.get("interval") == "month", addon_code


class _FakeCollection:
    def __init__(self):
        self.rows = {}

    async def find_one(self, query, projection=None):
        key = query.get("tier_code") or query.get("plan_code") or query.get("addon_code")
        return self.rows.get(key)

    async def update_one(self, query, update, upsert=False):
        key = query.get("tier_code") or query.get("plan_code") or query.get("addon_code")
        row = dict(self.rows.get(key) or {})
        if upsert and "$setOnInsert" in update:
            row.update(update["$setOnInsert"])
        row.update(update.get("$set") or {})
        self.rows[key] = row


class _FakeBillingDB:
    def __init__(self):
        self.plans = _FakeCollection()
        self.subscription_plans = _FakeCollection()
        self.subscription_addons = _FakeCollection()


def test_nonproduction_startup_does_not_write_live_ids(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    monkeypatch.delenv("STRIPE_API_KEY", raising=False)
    monkeypatch.setenv("SKIP_STRIPE_CATALOG_PROVISIONING", "true")
    db = _FakeBillingDB()

    asyncio.run(ensure_stripe_catalog(db))

    starter = db.plans.rows["starter_barn"]
    assert starter["stripe_product_id"] is None
    assert starter["stripe_price_id_monthly"] is None
    assert starter["stripe_price_id_annual"] is None
    assert starter["stripe_catalog_environment"] == "sandbox"
    assert starter["stripe_catalog_ready"] is False
    assert "stripe_key_missing" in starter["stripe_catalog_blockers"]

    addon = db.subscription_addons.rows["quickbooks_integration"]
    assert addon["stripe_product_id"] is None
    assert addon["stripe_price_id"] is None
    assert addon["stripe_catalog_environment"] == "sandbox"
