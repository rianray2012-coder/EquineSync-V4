"""Build-Next-1 — billing launch verification and Apple contract prep.

These tests are local-only. They pin the read-only launch-readiness contract
without calling Stripe, validating Apple receipts, creating checkout sessions,
processing webhooks, mutating subscription items, enforcing limits, or writing
MongoDB rows.
"""
from __future__ import annotations

import pathlib

from core.billing_launch_readiness import (
    APPLE_PRODUCT_ID_CONTRACT,
    CONTACT_SALES_PLAN_CODES,
    FREE_MANUAL_PLAN_CODES,
    SELF_SERVICE_PLAN_CODES,
    build_billing_launch_readiness_report,
    render_billing_launch_readiness_markdown,
)
from core.billing_provisioning import ADDON_PRICE_CATALOG, PLAN_CATALOG


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_build_next_1_catalog_report_has_no_blockers_from_locked_constants():
    report = build_billing_launch_readiness_report()
    assert report["source_counts"]["catalog_plans"] == len(PLAN_CATALOG)
    assert report["source_counts"]["self_service_plans"] == 9
    assert report["source_counts"]["contact_sales_plans"] == 2
    assert report["source_counts"]["addons"] == len(ADDON_PRICE_CATALOG) == 12
    assert not any(issue["severity"] == "blocker" for issue in report["issues"])


def test_free_and_contact_sales_contracts_match_founder_locks():
    report = build_billing_launch_readiness_report()
    preview = {row["plan_code"]: row for row in report["plan_preview"]}

    assert FREE_MANUAL_PLAN_CODES == ("free", "service_provider_free")
    assert preview["free"] == {
        "plan_code": "free",
        "customer_type": "free_manual",
        "stripe_product_configured": False,
        "stripe_monthly_configured": False,
        "stripe_annual_configured": False,
        "stripe_env_required": False,
        "apple_contract_status": "not_applicable",
    }
    assert preview["service_provider_free"]["customer_type"] == "free_manual"
    assert preview["service_provider_free"]["stripe_product_configured"] is False
    assert preview["service_provider_free"]["stripe_monthly_configured"] is False
    assert preview["service_provider_free"]["stripe_annual_configured"] is False
    assert preview["service_provider_free"]["stripe_env_required"] is False

    assert set(CONTACT_SALES_PLAN_CODES) == {"enterprise", "community_program"}
    for plan_code in CONTACT_SALES_PLAN_CODES:
        assert preview[plan_code]["customer_type"] == "contact_sales"
        assert preview[plan_code]["stripe_product_configured"] is True
        assert preview[plan_code]["stripe_monthly_configured"] is False
        assert preview[plan_code]["stripe_annual_configured"] is False
        assert preview[plan_code]["stripe_env_required"] is False
        assert preview[plan_code]["apple_contract_status"] == "not_applicable"


def test_apple_product_contract_covers_only_self_service_plans_as_placeholders():
    assert tuple(APPLE_PRODUCT_ID_CONTRACT) == SELF_SERVICE_PLAN_CODES
    assert "free" not in APPLE_PRODUCT_ID_CONTRACT
    assert "service_provider_free" not in APPLE_PRODUCT_ID_CONTRACT
    assert "enterprise" not in APPLE_PRODUCT_ID_CONTRACT
    assert "community_program" not in APPLE_PRODUCT_ID_CONTRACT
    for plan_code, row in APPLE_PRODUCT_ID_CONTRACT.items():
        assert row["monthly"] == f"com.equinesync.{plan_code}.monthly"
        assert row["annual"] == f"com.equinesync.{plan_code}.annual"
        assert row["status"] == "placeholder_not_configured"


def test_supplied_local_rows_missing_are_warning_only_not_blockers():
    report = build_billing_launch_readiness_report(plans=[], subscription_plans=[], addons=[])
    assert not any(issue["severity"] == "blocker" for issue in report["issues"])
    kinds = {issue["kind"] for issue in report["issues"]}
    assert "plans_row_missing" in kinds
    assert "subscription_plans_row_missing" in kinds
    assert "subscription_addons_row_missing" in kinds


def test_supplied_plans_rows_with_stale_stripe_ids_are_blockers():
    report = build_billing_launch_readiness_report(plans=[{
        "tier_code": "starter_barn",
        "stripe_product_id": "prod_stale",
        "stripe_price_id_monthly": "price_stale_monthly",
        "stripe_price_id_annual": "price_stale_annual",
    }])
    blockers = {issue["kind"] for issue in report["issues"] if issue["severity"] == "blocker"}
    assert "plans_stripe_product_id_mismatch" in blockers
    assert "plans_stripe_price_id_monthly_mismatch" in blockers
    assert "plans_stripe_price_id_annual_mismatch" in blockers


def test_supplied_subscription_plan_rows_with_stale_stripe_ids_are_blockers():
    report = build_billing_launch_readiness_report(subscription_plans=[{
        "plan_code": "advanced_barn",
        "stripe_product_id": "prod_stale",
        "stripe_monthly_price_id": "price_stale_monthly",
        "stripe_annual_price_id": "price_stale_annual",
    }])
    blockers = {issue["kind"] for issue in report["issues"] if issue["severity"] == "blocker"}
    assert "subscription_plans_stripe_product_id_mismatch" in blockers
    assert "subscription_plans_stripe_monthly_price_id_mismatch" in blockers
    assert "subscription_plans_stripe_annual_price_id_mismatch" in blockers


def test_free_and_contact_sales_rows_reject_public_price_ids():
    report = build_billing_launch_readiness_report(
        plans=[
            {
                "tier_code": "free",
                "stripe_product_id": "prod_should_not_exist",
                "stripe_price_id_monthly": "price_should_not_exist",
                "stripe_price_id_annual": "price_should_not_exist",
            },
            {
                "tier_code": "enterprise",
                "stripe_product_id": "prod_UjfCInFonGujyh",
                "stripe_price_id_monthly": "price_should_not_exist",
                "stripe_price_id_annual": "price_should_not_exist",
            },
        ],
    )
    blockers = {issue["kind"] for issue in report["issues"] if issue["severity"] == "blocker"}
    assert "plans_stripe_product_id_mismatch" in blockers
    assert "plans_stripe_price_id_monthly_mismatch" in blockers
    assert "plans_stripe_price_id_annual_mismatch" in blockers


def test_supplied_addon_rows_with_stale_stripe_ids_are_blockers():
    report = build_billing_launch_readiness_report(addons=[{
        "addon_code": "additional_horse_standard",
        "stripe_product_id": "prod_stale",
        "stripe_price_id": "price_stale",
    }])
    blockers = {issue["kind"] for issue in report["issues"] if issue["severity"] == "blocker"}
    assert "subscription_addons_stripe_product_id_mismatch" in blockers
    assert "subscription_addons_stripe_price_id_mismatch" in blockers


def test_subscription_plan_apple_product_ids_are_warning_only_until_configured():
    report = build_billing_launch_readiness_report(subscription_plans=[{
        "plan_code": "trainer_lesson_15",
        "stripe_product_id": "prod_Ujes2frtPqSVU5",
        "stripe_monthly_price_id": "price_1TkBhzJLyFSImf6YrAGxDoVn",
        "stripe_annual_price_id": "price_1TkBkFJLyFSImf6Y6ClbJiPO",
        "apple_monthly_product_id": "com.equinesync.trainer_lesson_15.monthly",
        "apple_annual_product_id": "com.equinesync.trainer_lesson_15.annual",
    }])
    blockers = [issue for issue in report["issues"] if issue["severity"] == "blocker"]
    warnings = {issue["kind"] for issue in report["issues"] if issue["severity"] == "warning"}
    assert not blockers
    assert "subscription_plans_apple_monthly_product_id_mismatch" in warnings
    assert "subscription_plans_apple_annual_product_id_mismatch" in warnings


def test_build_next_1_pins_public_plans_scrubber_source_guard():
    route_src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert '@router.get("/billing/plans-public")' in route_src
    public_section = route_src.split('@router.get("/billing/plans-public")', 1)[1]
    public_section = public_section.split('@router.get("/billing/addons")', 1)[0]
    for token in (
        '"stripe_price_id_monthly"',
        '"stripe_price_id_annual"',
        '"stripe_product_id"',
        '"has_monthly"',
        '"has_annual"',
    ):
        assert token in public_section
    assert "pub.pop(k, None)" in public_section
    assert "Cache-Control" in public_section


def test_rendered_markdown_contains_apple_contract_and_deferred_boundaries():
    report = build_billing_launch_readiness_report()
    markdown = render_billing_launch_readiness_markdown(report)
    assert "# Build-Next-1 Billing Launch Readiness Report" in markdown
    assert "com.equinesync.starter_barn.monthly" in markdown
    assert "Apple receipt validation" in markdown
    assert "Stripe Checkout changes" in markdown
    assert "No issues found." in markdown


def test_build_next_1_helper_has_no_payment_or_write_behavior():
    helper = (ROOT / "backend" / "core" / "billing_launch_readiness.py").read_text()
    forbidden = [
        "stripe.checkout",
        "Webhook",
        "construct_event",
        "verify_receipt",
        "apple receipt",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
    ]
    for token in forbidden:
        assert token not in helper


def test_build_next_1_script_is_read_only_against_mongo():
    script = (ROOT / "backend" / "scripts" / "build_next_1_billing_launch_readiness.py").read_text()
    assert "--constants-only" in script
    assert ".find(" in script
    for token in ("insert_one", "update_one", "delete_one", "bulk_write"):
        assert token not in script
