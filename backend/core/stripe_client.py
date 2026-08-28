"""Stripe client helpers.

Keep Stripe API keys scoped to a client instance instead of mutating the
process-global ``stripe.api_key`` value.
"""
from __future__ import annotations

import os
from typing import Mapping, Optional, Sequence

import stripe


_TRUE_ENV_VALUES = {"1", "true", "yes", "on", "enabled"}
_LIVE_KEY_MODES = {"restricted_live", "secret_live"}


def stripe_api_key() -> Optional[str]:
    return os.environ.get("STRIPE_API_KEY")


def stripe_client(api_key: Optional[str] = None) -> stripe.StripeClient:
    key = api_key or stripe_api_key()
    if not key:
        raise ValueError("STRIPE_API_KEY is required")
    return stripe.StripeClient(key)


def construct_webhook_event(
    *,
    payload: bytes,
    sig_header: str,
    secret: str,
    api_key: Optional[str] = None,
):
    # Signature verification is local; it should not require an API-capable key
    # in non-production test/dev webhook paths.
    key = api_key or stripe_api_key() or "sk_test_webhook_signature_verification_only"
    return stripe.StripeClient(key).construct_event(payload, sig_header, secret)


def stripe_key_mode(value: Optional[str]) -> str:
    key = (value or "").strip()
    if not key:
        return "missing"
    if key.startswith("rk_test_"):
        return "restricted_test"
    if key.startswith("sk_test_"):
        return "secret_test"
    if key.startswith("rk_live_"):
        return "restricted_live"
    if key.startswith("sk_live_"):
        return "secret_live"
    if key.startswith("pk_test_"):
        return "publishable_test"
    if key.startswith("pk_live_"):
        return "publishable_live"
    return "configured_unknown"


def stripe_env_flag_enabled(
    name: str,
    *,
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    source = os.environ if env is None else env
    return (source.get(name) or "").strip().lower() in _TRUE_ENV_VALUES


def stripe_live_session_enabled(
    session_kind: str,
    *,
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    source = os.environ if env is None else env
    api_mode = stripe_key_mode(source.get("STRIPE_API_KEY"))
    if api_mode not in _LIVE_KEY_MODES:
        return True
    if session_kind == "checkout":
        return stripe_env_flag_enabled("STRIPE_LIVE_CHECKOUT_ENABLED", env=source)
    if session_kind == "portal":
        return stripe_env_flag_enabled("STRIPE_LIVE_PORTAL_ENABLED", env=source)
    return False


def stripe_live_payment_readiness_snapshot(
    *,
    env: Optional[Mapping[str, str]] = None,
) -> dict:
    """Return a redacted live-payment readiness view without calling Stripe."""
    source = os.environ if env is None else env
    api_mode = stripe_key_mode(source.get("STRIPE_API_KEY"))
    publishable_mode = stripe_key_mode(
        source.get("STRIPE_PUBLISHABLE_KEY") or source.get("REACT_APP_STRIPE_PUBLISHABLE_KEY")
    )
    webhook_secret_configured = bool((source.get("STRIPE_WEBHOOK_SECRET") or "").strip())
    live_checkout_enabled = stripe_env_flag_enabled("STRIPE_LIVE_CHECKOUT_ENABLED", env=source)
    live_portal_enabled = stripe_env_flag_enabled("STRIPE_LIVE_PORTAL_ENABLED", env=source)
    return {
        "provider": "stripe",
        "activation_target": "live_payment_readiness",
        "api_key_mode": api_mode,
        "publishable_key_mode": publishable_mode,
        "webhook_secret_configured": webhook_secret_configured,
        "live_key_configured": api_mode in _LIVE_KEY_MODES,
        "live_checkout_enabled": live_checkout_enabled,
        "live_portal_enabled": live_portal_enabled,
        "live_money_enabled": live_checkout_enabled or live_portal_enabled,
    }


def stripe_test_mode_activation_snapshot(
    *,
    env: Optional[Mapping[str, str]] = None,
    allowed_origins: Optional[Sequence[str]] = None,
    catalog_ready: bool = False,
) -> dict:
    """Return a redacted test-mode readiness view for activation proof packets."""
    source = os.environ if env is None else env
    api_mode = stripe_key_mode(source.get("STRIPE_API_KEY"))
    publishable_mode = stripe_key_mode(
        source.get("STRIPE_PUBLISHABLE_KEY") or source.get("REACT_APP_STRIPE_PUBLISHABLE_KEY")
    )
    webhook_secret_configured = bool((source.get("STRIPE_WEBHOOK_SECRET") or "").strip())
    origin_count = len([origin for origin in (allowed_origins or []) if origin])
    test_mode_ready = (
        api_mode in {"restricted_test", "secret_test"}
        and webhook_secret_configured
        and origin_count > 0
        and bool(catalog_ready)
    )
    return {
        "provider": "stripe",
        "activation_target": "test_mode",
        "api_key_mode": api_mode,
        "publishable_key_mode": publishable_mode,
        "webhook_secret_configured": webhook_secret_configured,
        "allowed_origin_count": origin_count,
        "catalog_ready": bool(catalog_ready),
        "test_mode_ready": test_mode_ready,
        "live_money_enabled": False,
        "live_checkout_enabled": False,
        "live_portal_enabled": False,
    }
