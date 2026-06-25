"""Phase 15R-B migration dry-run gap report tests.

No Mongo, Stripe, Apple, checkout, or webhook calls are required. The dry-run
functions operate on plain dictionaries and the CLI is source-checked to remain
read-only against MongoDB.
"""
from __future__ import annotations

import pathlib

from core.entitlements_migration import (
    analyze_plans,
    analyze_subscriptions,
    build_migration_dry_run,
    render_migration_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _plan(code="starter_barn", **overrides):
    base = {
        "id": code,
        "tier_code": code,
        "name": code.replace("_", " ").title(),
        "description": "test",
        "monthly_price_cents": 6999,
        "annual_price_cents": 69900,
        "feature_limits": {
            "horses": 10,
            "staff_seats": 3,
            "owner_manager_seats": 1,
            "lesson_participants": 0,
        },
        "contact_sales": False,
        "stripe_provisioned": True,
        "active": True,
    }
    base.update(overrides)
    return base


def _subscription(code="starter_barn", **overrides):
    base = {
        "id": "sub_local_1",
        "barn_id": "barn_1",
        "plan_tier_code": code,
        "status": "active",
    }
    base.update(overrides)
    return base


def _issue_kinds(issues):
    return {issue["kind"] for issue in issues}


def test_clean_dry_run_projects_future_shapes_without_issues():
    plans = [_plan()]
    subscriptions = [_subscription(stripe_customer_id="cus_123456", stripe_subscription_id="sub_123456")]

    report = build_migration_dry_run(
        plans=plans,
        subscriptions=subscriptions,
        generated_at="2026-06-19T00:00:00+00:00",
    )

    assert report["source_counts"] == {"plans": 1, "subscriptions": 1}
    assert report["projection_counts"] == {
        "subscription_plans": 1,
        "account_subscription_limits": 1,
    }
    assert report["severity_counts"] == {}
    plan_preview = report["subscription_plans_preview"][0]
    assert plan_preview["plan_code"] == "starter_barn"
    assert plan_preview["included_horses"] == 10
    limits_preview = report["account_subscription_limits_preview"][0]
    assert limits_preview["plan_code"] == "starter_barn"
    assert limits_preview["billing_provider"] == "stripe"
    assert limits_preview["purchase_platform"] == "web"
    assert limits_preview["horse_limit"] == 10


def test_alias_plan_codes_are_reported_but_still_projected():
    projections, issues = analyze_subscriptions([
        _subscription("trainer_lessons_15", id="sub_alias"),
    ])

    assert projections[0]["plan_code"] == "trainer_lesson_15"
    assert "aliased_plan_code" in _issue_kinds(issues)
    assert not any(issue["severity"] == "blocker" for issue in issues)


def test_legacy_plan_codes_are_warnings_and_project_to_canonical_plans():
    plan_projections, plan_issues = analyze_plans([
        _plan("starter", monthly_price_cents=4900, annual_price_cents=49000),
        _plan("professional", monthly_price_cents=14900, annual_price_cents=149000),
    ])
    sub_projections, sub_issues = analyze_subscriptions([
        _subscription("starter", id="sub_legacy_starter"),
        _subscription("professional", id="sub_legacy_professional"),
    ])

    assert [p["plan_code"] for p in plan_projections] == ["starter_barn", "advanced_barn"]
    assert [p["legacy_tier_code"] for p in plan_projections] == ["starter", "professional"]
    assert [s["plan_code"] for s in sub_projections] == ["starter_barn", "advanced_barn"]
    all_issues = plan_issues + sub_issues
    assert "legacy_plan_code" in _issue_kinds(all_issues)
    assert not any(issue["kind"] == "unknown_plan_code" for issue in all_issues)
    assert not any(issue["severity"] == "blocker" for issue in all_issues)


def test_unknown_plan_code_is_blocker_for_plan_and_subscription_rows():
    _, plan_issues = analyze_plans([_plan("platinum")])
    _, sub_issues = analyze_subscriptions([_subscription("platinum")])

    assert "unknown_plan_code" in _issue_kinds(plan_issues)
    assert "unknown_plan_code" in _issue_kinds(sub_issues)
    assert all(issue["severity"] == "blocker" for issue in plan_issues + sub_issues)


def test_free_plan_with_stripe_ids_is_blocker():
    _, issues = analyze_plans([
        _plan(
            "free",
            monthly_price_cents=0,
            annual_price_cents=0,
            feature_limits={"horses": 0, "staff_seats": 0, "owner_manager_seats": 0},
            stripe_provisioned=False,
            stripe_product_id="prod_123456789",
        )
    ])

    assert "free_plan_has_stripe_ids" in _issue_kinds(issues)
    assert any(issue["severity"] == "blocker" for issue in issues)


def test_free_subscription_with_stripe_ids_is_blocker():
    _, issues = analyze_subscriptions([
        _subscription(
            "free",
            id="free_barn_1",
            stripe_customer_id="cus_123456789",
            stripe_subscription_id="sub_123456789",
        )
    ])

    assert "free_subscription_treated_as_paid" in _issue_kinds(issues)
    assert any(issue["severity"] == "blocker" for issue in issues)


def test_missing_provider_is_warning_and_inferred_manual():
    projections, issues = analyze_subscriptions([
        _subscription("private_owner_plus", id="sub_manual", stripe_customer_id=None),
    ])

    assert "billing_provider_inferred" in _issue_kinds(issues)
    assert projections[0]["billing_provider"] == "manual"
    assert projections[0]["purchase_platform"] == "admin"


def test_unknown_provider_and_platform_are_blockers():
    _, issues = analyze_subscriptions([
        _subscription(
            "starter_barn",
            id="bad_provider",
            billing_provider="cashapp",
            purchase_platform="android_store",
        )
    ])

    kinds = _issue_kinds(issues)
    assert "unknown_billing_provider" in kinds
    assert "unknown_purchase_platform" in kinds
    assert sum(1 for issue in issues if issue["severity"] == "blocker") == 2


def test_apple_subscription_projects_without_stripe_ids():
    projections, issues = analyze_subscriptions([
        _subscription(
            "private_owner_plus",
            id="ios_sub",
            account_id="acct_ios",
            billing_provider="apple",
            purchase_platform="ios",
            apple_original_transaction_id="1000000000000001",
            apple_product_id="com.equinesync.private_owner_plus.monthly",
        )
    ])

    assert not issues
    row = projections[0]
    assert row["account_id"] == "acct_ios"
    assert row["billing_provider"] == "apple"
    assert row["purchase_platform"] == "ios"
    assert row["stripe_customer_id"] is None
    assert row["stripe_subscription_id"] is None
    assert row["apple_original_transaction_id"] == "1000000000000001"


def test_markdown_report_contains_counts_issues_and_deferred_guardrails():
    report = build_migration_dry_run(
        plans=[_plan()],
        subscriptions=[_subscription("free", stripe_subscription_id="sub_123456789")],
        generated_at="2026-06-19T00:00:00+00:00",
    )
    markdown = render_migration_markdown(report)

    assert "# Phase 15R-B Migration Dry-Run Gap Report" in markdown
    assert "subscription_plans preview" in markdown
    assert "account_subscription_limits preview" in markdown
    assert "free_subscription_treated_as_paid" in markdown
    assert "No checkout/webhook/usage-enforcement behavior changes." in markdown


def test_cli_script_is_read_only_against_mongo():
    src = (ROOT / "backend" / "scripts" / "phase15r_migration_dry_run.py").read_text()
    forbidden = [
        ".insert_one(",
        ".insert_many(",
        ".update_one(",
        ".update_many(",
        ".replace_one(",
        ".delete_one(",
        ".delete_many(",
        ".bulk_write(",
        "upsert=True",
    ]
    for token in forbidden:
        assert token not in src, f"dry-run script must not contain Mongo write token {token}"


def test_cli_default_output_path_is_under_outputs():
    src = (ROOT / "backend" / "scripts" / "phase15r_migration_dry_run.py").read_text()
    assert '"outputs"' in src
    assert "phase15r_b_migration_dry_run_report.md" in src
