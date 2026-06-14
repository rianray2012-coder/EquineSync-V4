"""routes/membership.py — Equine Sync marketplace membership + Stripe Checkout.

Public marketplace tier selection + Stripe Checkout integration via the
emergentintegrations Stripe playbook. Server-authoritative pricing (no
client-controlled amounts), payment_transactions audit collection, and a
polling-based status endpoint to update the user's `subscription_status`.

Tiers (USD/month):
  - free            → $0      (no checkout, immediate "free" status)
  - owner_rider     → $15     (horse owners + riders)
  - trainer_provider→ $49     (trainers + service providers)  ★ most popular
  - barn_facility   → $149    (barns / facilities)
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from emergentintegrations.payments.stripe.checkout import (
    StripeCheckout,
    CheckoutSessionRequest,
)

logger = logging.getLogger(__name__)


# ---------- Server-authoritative tier catalog ----------
# Amounts are FLOATS in USD per the playbook (Stripe rejects ints).
TIERS = {
    "free": {
        "amount": 0.0,
        "label": "Free",
        "blurb": "Create your profile and explore the network.",
    },
    "owner_rider": {
        "amount": 15.0,
        "label": "Horse Owner / Rider",
        "blurb": "For independent owners and riders.",
    },
    "trainer_provider": {
        "amount": 49.0,
        "label": "Trainer / Service Provider",
        "blurb": "For trainers, vets, farriers and equine pros.",
    },
    "barn_facility": {
        "amount": 149.0,
        "label": "Barn / Facility",
        "blurb": "For full barn operations and lesson programs.",
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class CheckoutRequestBody(BaseModel):
    tier: str
    origin_url: str  # frontend window.location.origin for success/cancel URLs


def _stripe_client(request: Request) -> StripeCheckout:
    api_key = os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise HTTPException(500, "Stripe is not configured on this server.")
    host_url = str(request.base_url)
    webhook_url = f"{host_url.rstrip('/')}/api/webhook/stripe"
    # If a signing secret is configured, hand it to the playbook helper so
    # webhook signature verification is enforced (MVP billing lifecycle).
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    kwargs = {"api_key": api_key, "webhook_url": webhook_url}
    if secret:
        kwargs["webhook_secret"] = secret
    try:
        return StripeCheckout(**kwargs)
    except TypeError:
        # Older playbook signatures don't accept webhook_secret — fall back.
        return StripeCheckout(api_key=api_key, webhook_url=webhook_url)


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(tags=["membership"])

    @router.get("/membership/tiers")
    async def get_tiers():
        """Public catalog — used by the landing page + signup wizard."""
        return [
            {"id": k, "amount": v["amount"], "label": v["label"], "blurb": v["blurb"]}
            for k, v in TIERS.items()
        ]

    @router.post("/membership/checkout")
    async def create_checkout_gone(body: CheckoutRequestBody, request: Request,
                                   user=Depends(get_current_user)):
        """Phase 15.G — Legacy membership checkout is sunset.

        The marketplace-tier `/membership/checkout` flow has been superseded
        by the Phase 15 facility-tier subscription billing system. Calls now
        return HTTP 410 Gone with a clear, non-sensitive pointer to the new
        endpoint. The rest of the marketplace membership lifecycle
        (start-trial, cancel, polling status, webhook) is retained for
        rolling sessions and the legacy Stripe one-time-checkout webhook
        path until Phase 16 reconciliation.
        """
        raise HTTPException(
            status_code=410,
            detail={
                "code": "membership_checkout_sunset",
                "message": (
                    "/api/membership/checkout is no longer available. "
                    "Use POST /api/subscriptions/checkout with "
                    "{plan_tier_code, billing_cycle, origin_url}."
                ),
                "successor": "/api/subscriptions/checkout",
            },
        )

    @router.get("/membership/checkout/status/{session_id}")
    async def checkout_status_gone(session_id: str, request: Request,
                                   user=Depends(get_current_user)):
        """Phase 15.G — Legacy status polling is sunset alongside the
        legacy create endpoint. Returns HTTP 410 with the same structured
        sunset payload as `/membership/checkout`. New paid flows return
        the user to `/billing/success`, where the Phase 15 webhook
        pipeline finalizes the subscription idempotently — no client
        polling required.
        """
        raise HTTPException(
            status_code=410,
            detail={
                "code": "membership_checkout_status_sunset",
                "message": (
                    "/api/membership/checkout/status/{session_id} is no longer "
                    "available. Paid subscription state is finalized via the "
                    "Phase 15 webhook (POST /api/webhook/stripe-subscriptions) "
                    "and exposed by GET /api/subscriptions/me."
                ),
                "successor": "/api/subscriptions/me",
            },
        )

    @router.post("/membership/cancel")
    async def cancel_membership(user=Depends(get_current_user)):
        """MVP billing lifecycle — local cancellation only.

        Because the current Stripe integration uses one-time Checkout (NOT
        true recurring Subscriptions), there is no subscription object to
        cancel in Stripe. Calling this endpoint flips the local
        `subscription_status` to `cancelled` and drops the user back to the
        free experience. The user keeps whatever access they already paid for
        until their next billing cycle (we just don't auto re-charge in this
        MVP). True recurring subscriptions + Stripe-side cancellation are
        deferred to a future phase.
        """
        await db.users.update_one(
            {"id": user["id"]},
            {"$set": {
                "subscription_status": "cancelled",
                "membership_tier": "free",
                "subscription_updated_at": _now_iso(),
                "subscription_cancelled_at": _now_iso(),
            }},
        )
        u = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
        return {"ok": True, "user": u}

    @router.post("/membership/start-trial")
    async def start_trial(body: CheckoutRequestBody, user=Depends(get_current_user)):
        """Start the one-time 7-day trial on a paid tier — no card needed.

        Only available if the user has not already used their trial. Skips
        Stripe entirely; sets `subscription_status='trialing'` and
        `trial_expires_at=now+7d`. After expiry the frontend nudges the user
        into Checkout via /membership/checkout.
        """
        tier_key = (body.tier or "").strip().lower()
        if tier_key not in TIERS or tier_key == "free":
            raise HTTPException(400, "Trial requires a paid tier.")
        if user.get("trial_used"):
            raise HTTPException(409, "Free trial already used on this account.")
        from datetime import datetime as _dt, timedelta as _td, timezone as _tz
        expires = (_dt.now(_tz.utc) + _td(days=7)).isoformat()
        await db.users.update_one(
            {"id": user["id"]},
            {"$set": {
                "membership_tier": tier_key,
                "subscription_status": "trialing",
                "trial_expires_at": expires,
                "trial_used": True,
                "subscription_updated_at": _now_iso(),
            }},
        )
        u = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
        return {"ok": True, "user": u, "trial_expires_at": expires}

    @router.post("/webhook/stripe")
    async def stripe_webhook(request: Request):
        """Stripe webhook receiver — verifies signature via emergentintegrations
        and finalizes payment_transactions + user.subscription_status.

        MVP billing lifecycle (NOT true subscriptions): handles
        checkout.session.completed (→ paid) and checkout.session.expired
        (→ session timed out before payment). Recurring subscription events
        like customer.subscription.updated/deleted are deferred to a future
        phase that would require migrating off one-time Checkout.
        """
        body = await request.body()
        sig = request.headers.get("Stripe-Signature")
        client = _stripe_client(request)
        try:
            evt = await client.handle_webhook(body, sig)
        except Exception as ex:
            logger.exception("stripe webhook handler failed")
            raise HTTPException(400, f"Invalid webhook: {ex}")
        session_id = evt.session_id
        if not session_id:
            return {"received": True}
        tx = await db.payment_transactions.find_one({"session_id": session_id})
        if not tx:
            return {"received": True}

        payment_status = getattr(evt, "payment_status", None)
        evt_type = (getattr(evt, "event_type", "") or "").lower()
        # checkout.session.expired — close the local row without touching user.
        if "expired" in evt_type or getattr(evt, "status", None) == "expired":
            if tx.get("status") != "expired":
                await db.payment_transactions.update_one(
                    {"session_id": session_id},
                    {"$set": {
                        "status": "expired",
                        "payment_status": payment_status or "expired",
                        "updated_at": _now_iso(),
                    }},
                )
            return {"received": True}

        # checkout.session.completed → mark paid + flip user (idempotent).
        if payment_status == "paid" and tx.get("payment_status") != "paid":
            await db.users.update_one(
                {"id": tx["user_id"]},
                {"$set": {
                    "membership_tier": tx.get("tier"),
                    "subscription_status": "active",
                    "subscription_updated_at": _now_iso(),
                    "trial_expires_at": None,  # paid → trial is irrelevant
                }},
            )
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "paid",
                    "status": "complete",
                    "updated_at": _now_iso(),
                }},
            )
        return {"received": True}

    return router
