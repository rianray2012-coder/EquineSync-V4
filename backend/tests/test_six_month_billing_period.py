"""D-14 (14 Sep 2026) — six-month billing period.

Apple's default auto-renewable subscription ceiling is $1,000.00, so the
$1,499 / $1,799 annual prices for advanced_barn and trainer_lesson_50 cannot
be entered in App Store Connect. The founder directed a six-month term for
those tiers in the stores, with an identical web/Stripe price so
FD-2026-09-11-03 parity holds. These tests pin that period end to end without
calling Stripe, Mongo, or the network.
"""
from __future__ import annotations

import asyncio
import pathlib

import pytest

from core import billing_provisioning as bp
from core.billing_launch_readiness import (
    APPLE_PRODUCT_ID_CONTRACT,
    STORE_SELLABLE_PERIODS,
    build_billing_launch_readiness_report,
    store_sellable_periods,
)
from core.entitlements import plan_to_subscription_plan_shape
from routes.admin_billing import _monthly_equivalent_cents


ROOT = pathlib.Path(__file__).resolve().parents[2]
SIX_MONTH_TIERS = ("advanced_barn", "trainer_lesson_50")


def _tier(code: str) -> dict:
    return next(t for t in bp.PLAN_CATALOG if t["tier_code"] == code)


# ---------------------------------------------------------------------------
# Catalog + period model
# ---------------------------------------------------------------------------

def test_billing_periods_model_is_monthly_six_month_annual():
    assert bp.BILLING_PERIOD_CODES == ("monthly", "six_month", "annual")
    assert bp.BILLING_PERIODS["six_month"]["stripe_interval"] == "month"
    assert bp.BILLING_PERIODS["six_month"]["stripe_interval_count"] == 6
    assert bp.BILLING_PERIODS["six_month"]["months"] == 6
    assert bp.stripe_recurring_for_period("six_month") == {"interval": "month", "interval_count": 6}
    assert bp.stripe_recurring_for_period("monthly") == {"interval": "month"}
    assert bp.stripe_recurring_for_period("annual") == {"interval": "year"}


def test_six_month_prices_follow_rule_a_and_apple_ceiling():
    """Rule A: 5 x monthly rounded UP to an Apple .99 point; never > $1,000."""
    assert bp.SIX_MONTH_PRICE_CENTS == {"advanced_barn": 74999, "trainer_lesson_50": 89999}
    for code, cents in bp.SIX_MONTH_PRICE_CENTS.items():
        tier = _tier(code)
        assert tier["six_month_price_cents"] == cents
        assert cents <= 100_000, "Apple default subscription ceiling is $1,000.00"
        assert cents >= 5 * tier["monthly_price_cents"], "store must never undercut web"
        assert cents - 5 * tier["monthly_price_cents"] < 100, "rounded to the nearest point only"
        assert cents % 100 == 99, "Apple points above $100 end in .99"
        # Same per-month rate as the existing annual (10 x monthly) logic,
        # give or take the round-up to an Apple point (< $1 a month).
        assert abs(cents / 6 - tier["annual_price_cents"] / 12) < 100


def test_only_the_two_d14_tiers_sell_six_month():
    for tier in bp.PLAN_CATALOG:
        periods = bp.tier_billing_periods(tier)
        if tier["tier_code"] in SIX_MONTH_TIERS:
            assert periods == ("monthly", "six_month", "annual")
        elif tier.get("contact_sales"):
            assert periods == ()
        else:
            assert periods == ("monthly", "annual")
    # elite_barn: 5 x $299.99 = $1,499.95 exceeds the cap; monthly-only in-app (E1).
    assert bp.tier_price_cents(_tier("elite_barn"), "six_month") is None


def test_six_month_env_var_names_follow_the_stripe_price_pattern(monkeypatch):
    assert bp.price_env_var("advanced_barn", "six_month") == "STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH"
    assert bp.price_env_var("trainer_lesson_50", "six_month") == "STRIPE_PRICE_TRAINER_LESSON_50_SIX_MONTH"
    assert bp.price_env_var("starter_barn", "annual") == "STRIPE_PRICE_STARTER_BARN_ANNUAL"

    # Not recorded in the live map until Cowork creates the Stripe Prices.
    monkeypatch.delenv("STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH", raising=False)
    assert bp.configured_price_ids_by_period(_tier("advanced_barn"))["six_month"] is None
    # Env override wins, exactly like the monthly/annual overrides.
    monkeypatch.setenv("STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH", "price_six_month_override")
    by_period = bp.configured_price_ids_by_period(_tier("advanced_barn"))
    assert by_period["six_month"] == "price_six_month_override"
    assert by_period["monthly"] == bp.LIVE_STRIPE_PRICE_IDS["advanced_barn"]["monthly"]
    assert by_period["annual"] == bp.LIVE_STRIPE_PRICE_IDS["advanced_barn"]["annual"]
    # Tiers without the term never ask for it.
    assert "six_month" not in bp.configured_price_ids_by_period(_tier("starter_barn"))


# ---------------------------------------------------------------------------
# Startup: plan rows + production validation
# ---------------------------------------------------------------------------

class _Collection:
    def __init__(self):
        self.rows: dict[str, dict] = {}

    async def update_one(self, flt, update, upsert=False):
        key = next(iter(flt.values()))
        row = self.rows.setdefault(key, {})
        row.update(update.get("$set") or {})
        for k, v in (update.get("$setOnInsert") or {}).items():
            row.setdefault(k, v)

    async def find_one(self, *a, **k):
        return None


class _DB:
    def __init__(self):
        self.plans = _Collection()
        self.subscription_plans = _Collection()
        self.subscription_addons = _Collection()


def test_upsert_plan_writes_six_month_fields_only_for_tiers_that_sell_it(monkeypatch):
    monkeypatch.setenv("STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH", "price_adv_6m")
    monkeypatch.delenv("STRIPE_PRICE_STARTER_BARN_SIX_MONTH", raising=False)
    db = _DB()
    asyncio.run(bp._upsert_plan(db, _tier("advanced_barn"), None, None, None))
    asyncio.run(bp._upsert_plan(db, _tier("starter_barn"), None, None, None, six_month_price_id="price_should_be_dropped"))

    adv = db.plans.rows["advanced_barn"]
    assert adv["six_month_price_cents"] == 74999
    assert adv["stripe_price_id_six_month"] == "price_adv_6m"
    assert adv["billing_periods"] == ["monthly", "six_month", "annual"]
    adv_sub = db.subscription_plans.rows["advanced_barn"]
    assert adv_sub["stripe_six_month_price_id"] == "price_adv_6m"
    assert adv_sub["six_month_amount"] == 74999
    assert adv_sub["apple_six_month_product_id"] is None

    starter = db.plans.rows["starter_barn"]
    assert starter["six_month_price_cents"] is None
    assert starter["stripe_price_id_six_month"] is None
    assert starter["billing_periods"] == ["monthly", "annual"]
    assert db.subscription_plans.rows["starter_barn"]["stripe_six_month_price_id"] is None


class _Prices:
    def __init__(self):
        self.retrieved: list[str] = []

    def retrieve(self, price_id):
        self.retrieved.append(price_id)
        return {"id": price_id, "product": "prod_test"}


class _Client:
    def __init__(self):
        self.v1 = type("V1", (), {})()
        self.v1.prices = _Prices()


def _clear_six_month_env(monkeypatch):
    for code in SIX_MONTH_TIERS:
        monkeypatch.delenv(bp.price_env_var(code, "six_month"), raising=False)
    # service_provider_premium is stripe_provisioned but env-configured only
    # (not in LIVE_STRIPE_PRICE_IDS); give it IDs so only six-month is at stake.
    monkeypatch.setenv("STRIPE_PRICE_SERVICE_PROVIDER_PREMIUM_MONTHLY", "price_spp_monthly")
    monkeypatch.setenv("STRIPE_PRICE_SERVICE_PROVIDER_PREMIUM_ANNUAL", "price_spp_annual")


def test_prod_validation_requires_six_month_price_ids_for_declared_tiers(monkeypatch):
    """The boot check is the parity guard: a catalog that sells six-month
    cannot start production without a six-month Stripe Price for each tier."""
    _clear_six_month_env(monkeypatch)
    monkeypatch.setattr(bp, "LIVE_STRIPE_PRICE_IDS", {
        code: dict(prices) for code, prices in bp.LIVE_STRIPE_PRICE_IDS.items()
    })
    with pytest.raises(RuntimeError) as ex:
        asyncio.run(bp._validate_prod_catalog(_DB(), _Client()))
    message = str(ex.value)
    assert "STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH" in message
    assert "STRIPE_PRICE_TRAINER_LESSON_50_SIX_MONTH" in message
    assert "LIVE_STRIPE_PRICE_IDS[advanced_barn].six_month" in message
    # Monthly/annual are all mapped, so nothing else is reported missing.
    assert "ANNUAL" not in message and "MONTHLY" not in message


def test_prod_validation_passes_and_retrieves_six_month_prices_when_configured(monkeypatch):
    _clear_six_month_env(monkeypatch)
    monkeypatch.setenv("STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH", "price_adv_6m_live")
    monkeypatch.setenv("STRIPE_PRICE_TRAINER_LESSON_50_SIX_MONTH", "price_t50_6m_live")
    db, client = _DB(), _Client()
    asyncio.run(bp._validate_prod_catalog(db, client))
    assert "price_adv_6m_live" in client.v1.prices.retrieved
    assert "price_t50_6m_live" in client.v1.prices.retrieved
    assert db.plans.rows["advanced_barn"]["stripe_price_id_six_month"] == "price_adv_6m_live"
    assert db.plans.rows["trainer_lesson_50"]["stripe_price_id_six_month"] == "price_t50_6m_live"
    assert db.plans.rows["elite_barn"]["stripe_price_id_six_month"] is None
    # 9 self-service tiers x 2 + 2 six-month prices, each retrieved once for
    # validation, plus one monthly re-read per tier for the product id.
    assert len(client.v1.prices.retrieved) == 9 * 2 + 2 + 9


# ---------------------------------------------------------------------------
# API shapes + checkout + webhook + MRR
# ---------------------------------------------------------------------------

def test_plan_to_public_exposes_six_month_amount_and_readiness_flag():
    from routes.subscriptions import CYCLE_PRICE_FIELDS, _plan_to_public

    assert CYCLE_PRICE_FIELDS == {
        "monthly": "stripe_price_id_monthly",
        "six_month": "stripe_price_id_six_month",
        "annual": "stripe_price_id_annual",
    }
    pub = _plan_to_public({
        "tier_code": "advanced_barn", "name": "Advanced Barn", "description": "x",
        "monthly_price_cents": 14999, "six_month_price_cents": 74999, "annual_price_cents": 149900,
        "stripe_price_id_monthly": "price_m", "stripe_price_id_six_month": "price_6", "stripe_price_id_annual": "price_a",
    })
    assert pub["six_month_price_cents"] == 74999
    assert pub["has_six_month"] is True
    starter = _plan_to_public({
        "tier_code": "starter_barn", "name": "Starter Barn", "description": "x",
        "monthly_price_cents": 6999, "annual_price_cents": 69900,
        "stripe_price_id_monthly": "price_m", "stripe_price_id_annual": "price_a",
    })
    assert starter["six_month_price_cents"] is None
    assert starter["has_six_month"] is False


def test_checkout_public_scrub_and_webhook_lookup_cover_six_month_source_guard():
    route_src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert "billing_cycle must be 'monthly', 'six_month', or 'annual'." in route_src
    assert "if cycle not in BILLING_PERIOD_CODES:" in route_src
    assert "does not offer a six-month term" in route_src
    assert "price_id = plan.get(CYCLE_PRICE_FIELDS[cycle])" in route_src
    public_section = route_src.split('@router.get("/billing/plans-public")', 1)[1]
    public_section = public_section.split('@router.get("/billing/addons")', 1)[0]
    assert '"stripe_price_id_six_month"' in public_section
    assert '"has_six_month"' in public_section

    webhook_src = (ROOT / "backend" / "routes" / "subscriptions_webhook_handlers.py").read_text()
    assert webhook_src.count('{"stripe_price_id_six_month": new_price_id}') == 2


def test_monthly_equivalent_divides_six_month_amount_by_six():
    plans = {"advanced_barn": {"monthly_price_cents": 14999, "six_month_price_cents": 74999, "annual_price_cents": 149900}}
    assert _monthly_equivalent_cents({"plan_tier_code": "advanced_barn", "billing_cycle": "six_month"}, plans) == 12500
    assert _monthly_equivalent_cents({"billing_cycle": "six_month", "amount_cents": 89999}) == 15000
    assert _monthly_equivalent_cents({"plan_tier_code": "advanced_barn", "billing_cycle": "annual"}, plans) == 12492


def test_subscription_plan_shape_carries_six_month_fields():
    shape = plan_to_subscription_plan_shape({
        "tier_code": "trainer_lesson_50",
        "six_month_price_cents": 89999,
        "stripe_price_id_six_month": "price_6",
        "feature_limits": {},
    })
    assert shape["six_month_amount"] == 89999
    assert shape["stripe_six_month_price_id"] == "price_6"
    assert shape["apple_six_month_product_id"] is None


# ---------------------------------------------------------------------------
# Store product-id contract + readiness report
# ---------------------------------------------------------------------------

def test_store_product_ids_and_in_app_periods_match_d14():
    for code in SIX_MONTH_TIERS:
        row = APPLE_PRODUCT_ID_CONTRACT[code]
        assert row["six_month"] == f"com.equinesync.app.{code}.six_month"
        assert row["store_periods"] == ["monthly", "six_month"]
    assert "six_month" not in APPLE_PRODUCT_ID_CONTRACT["elite_barn"]
    assert APPLE_PRODUCT_ID_CONTRACT["elite_barn"]["store_periods"] == ["monthly"]
    assert APPLE_PRODUCT_ID_CONTRACT["starter_barn"]["store_periods"] == ["monthly", "annual"]
    assert "six_month" not in APPLE_PRODUCT_ID_CONTRACT["starter_barn"]
    assert set(STORE_SELLABLE_PERIODS) == {"advanced_barn", "trainer_lesson_50", "elite_barn"}
    assert store_sellable_periods("individual_owner") == ("monthly", "annual")


def test_readiness_report_flags_missing_six_month_price_as_warning_not_blocker():
    report = build_billing_launch_readiness_report()
    kinds = {(i["kind"], i["record"], i["severity"]) for i in report["issues"]}
    for code in SIX_MONTH_TIERS:
        assert ("self_service_missing_six_month_price_id", code, "warning") in kinds
    assert not any(i["severity"] == "blocker" for i in report["issues"])
    preview = {row["plan_code"]: row for row in report["plan_preview"]}
    assert preview["advanced_barn"]["sells_six_month"] is True
    assert preview["advanced_barn"]["stripe_six_month_configured"] is False
    assert preview["elite_barn"]["sells_six_month"] is False


def test_docs_and_env_examples_mention_the_six_month_variables():
    env_doc = (ROOT / "docs" / "PHASE_15A_ENV_PLACEHOLDERS.md").read_text()
    env_example = (ROOT / "backend" / ".env.example").read_text()
    pricing = (ROOT / "docs" / "PRICING_PLAN_ADDENDUM.md").read_text()
    for name in ("STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH", "STRIPE_PRICE_TRAINER_LESSON_50_SIX_MONTH"):
        assert name in env_doc
        assert name in env_example
    assert "$749.99" in pricing and "$899.99" in pricing
    combined = env_doc + env_example + (ROOT / "backend" / "core" / "billing_provisioning.py").read_text()
    assert "sk_live_" not in combined and "rk_live_" not in combined
