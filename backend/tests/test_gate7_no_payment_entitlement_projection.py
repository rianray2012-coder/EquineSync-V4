from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUBSCRIPTIONS_ROUTE = ROOT / "backend" / "routes" / "subscriptions.py"
SUBSCRIPTION_UI = ROOT / "frontend" / "src" / "pages" / "SubscriptionBilling.jsx"
SUBSCRIPTION_HELPERS = ROOT / "frontend" / "src" / "lib" / "subscriptionBilling.js"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_free_checkout_backend_remains_local_manual_no_payment():
    route = _read(SUBSCRIPTIONS_ROUTE)

    assert "if tier in LOCAL_FREE_TIERS:" in route
    assert '{"url": None, "session_id": None, "tier": tier}' in route
    assert '"billing_provider": "manual"' in route
    assert '"purchase_platform": "admin"' in route
    assert '"amount_cents": 0' in route
    assert '_require_stripe_session_guard("checkout")' in route

    free_branch = route.split("if tier in LOCAL_FREE_TIERS:", 1)[1].split("# Paid tiers:", 1)[0]
    assert "_stripe_init" not in free_branch
    assert "checkout.sessions.create" not in free_branch
    assert "_require_stripe_session_guard" not in free_branch


def test_subscription_me_projection_strips_raw_stripe_identifiers():
    route = _read(SUBSCRIPTIONS_ROUTE)

    assert '@router.get("/subscriptions/me")' in route
    assert '"stripe_customer_id"' in route
    assert '"stripe_subscription_id"' in route
    assert '"stripe_price_id"' in route
    assert "safe = {k: v for k, v in sub.items() if k not in STRIPE_FIELDS}" in route


def test_subscription_billing_ui_projects_manual_free_access_as_non_stripe():
    ui = _read(SUBSCRIPTION_UI)

    assert 'const LOCAL_FREE_TIERS = new Set(["free", "service_provider_free"]);' in ui
    assert "const manualOrFreeSubscription = Boolean(" in ui
    assert "LOCAL_FREE_TIERS.has(planTier)" in ui
    assert '["manual", "comped"].includes(sub.billing_provider)' in ui
    assert 'sub.purchase_platform === "admin"' in ui
    assert "const canManageStripe = Boolean(sub && !manualOrFreeSubscription);" in ui
    assert 'data-testid="subscription-manual-access-note"' in ui
    assert "Pilot/free access is managed by EquineSync." in ui
    assert "Pilot/free access is founder-managed and does not require Stripe payment setup." in ui
    assert "Paid plan changes use Stripe Checkout when enabled." in ui
    assert "Pilot and invited" in ui
    assert "founder-managed and free during the pilot." in ui


def test_subscription_billing_ui_keeps_stripe_portal_for_paid_subscription_only():
    ui = _read(SUBSCRIPTION_UI)

    assert "canManageStripe ? (" in ui
    assert 'data-testid="subscription-manage-stripe-btn"' in ui
    assert 'title="Manage in Stripe"' in ui
    assert "window.location.assign(data.url)" in ui
    assert 'disabled={!sub || busyAction === "portal"}' not in ui


def test_public_subscription_helpers_keep_free_tiers_non_checkoutable_for_stripe():
    helpers = _read(SUBSCRIPTION_HELPERS)

    assert '"free",' in helpers
    assert '"service_provider_free",' in helpers
    assert '"free"' not in helpers.split("export const SUBSCRIBABLE_TIERS = new Set([", 1)[1].split("]);", 1)[0]
    assert '"service_provider_free"' not in helpers.split("export const SUBSCRIBABLE_TIERS = new Set([", 1)[1].split("]);", 1)[0]
