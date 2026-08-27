"""Stripe client helpers.

Keep Stripe API keys scoped to a client instance instead of mutating the
process-global ``stripe.api_key`` value.
"""
from __future__ import annotations

import os
from typing import Optional

import stripe


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
