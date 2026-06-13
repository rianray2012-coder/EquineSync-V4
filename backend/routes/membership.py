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
    async def create_checkout(body: CheckoutRequestBody, request: Request,
                              user=Depends(get_current_user)):
        """Create a Stripe Checkout session for the chosen tier.

        Free tier short-circuits — no Stripe call, user is flipped to
        subscription_status='free' immediately and the response includes
        url=None so the frontend can route to the success page directly.
        """
        tier_key = (body.tier or "").strip().lower()
        if tier_key not in TIERS:
            raise HTTPException(400, f"Invalid tier. Choose one of {sorted(TIERS)}.")
        tier = TIERS[tier_key]

        # Free tier: no Stripe checkout needed.
        if tier["amount"] <= 0:
            await db.users.update_one(
                {"id": user["id"]},
                {"$set": {
                    "membership_tier": "free",
                    "subscription_status": "free",
                    "subscription_updated_at": _now_iso(),
                }},
            )
            return {"url": None, "session_id": None, "tier": tier_key, "status": "free"}

        origin = (body.origin_url or "").rstrip("/")
        if not origin.startswith(("http://", "https://")):
            raise HTTPException(400, "origin_url must be an absolute http(s) URL.")

        success_url = f"{origin}/signup/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{origin}/signup?cancelled=1"

        client = _stripe_client(request)
        req = CheckoutSessionRequest(
            amount=float(tier["amount"]),
            currency="usd",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": user["id"],
                "user_email": user.get("email", ""),
                "tier": tier_key,
                "source": "marketplace_signup",
            },
        )
        try:
            session = await client.create_checkout_session(req)
        except Exception as ex:
            logger.exception("stripe checkout session create failed")
            raise HTTPException(502, f"Could not start checkout: {ex}")

        # MANDATORY: payment_transactions audit row (status=initiated).
        await db.payment_transactions.insert_one({
            "id": str(uuid.uuid4()),
            "session_id": session.session_id,
            "user_id": user["id"],
            "user_email": user.get("email"),
            "tier": tier_key,
            "amount": float(tier["amount"]),
            "currency": "usd",
            "metadata": req.metadata,
            "payment_status": "initiated",
            "status": "open",
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
        })
        return {
            "url": session.url,
            "session_id": session.session_id,
            "tier": tier_key,
            "amount": float(tier["amount"]),
        }

    @router.get("/membership/checkout/status/{session_id}")
    async def checkout_status(session_id: str, request: Request,
                              user=Depends(get_current_user)):
        """Poll Stripe for the session status.

        Idempotency: we only flip the user's subscription_status ONCE per
        session_id. Repeat calls return the cached row from
        payment_transactions.
        """
        tx = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
        if not tx:
            raise HTTPException(404, "Unknown checkout session.")
        if tx.get("user_id") != user["id"]:
            raise HTTPException(403, "Not your checkout session.")

        # If we've already finalized, just return what we have.
        if tx.get("payment_status") in ("paid", "expired", "failed"):
            return {
                "session_id": session_id,
                "payment_status": tx["payment_status"],
                "status": tx.get("status"),
                "tier": tx.get("tier"),
            }

        client = _stripe_client(request)
        try:
            st = await client.get_checkout_status(session_id)
        except Exception as ex:
            logger.exception("stripe get_checkout_status failed")
            raise HTTPException(502, f"Could not check status: {ex}")

        payment_status = st.payment_status
        status = st.status
        update = {
            "payment_status": payment_status,
            "status": status,
            "updated_at": _now_iso(),
        }
        # Idempotent user flip — only on the first observed "paid".
        if payment_status == "paid" and tx.get("payment_status") != "paid":
            await db.users.update_one(
                {"id": user["id"]},
                {"$set": {
                    "membership_tier": tx.get("tier"),
                    "subscription_status": "active",
                    "subscription_updated_at": _now_iso(),
                }},
            )
        await db.payment_transactions.update_one(
            {"session_id": session_id}, {"$set": update}
        )
        return {
            "session_id": session_id,
            "payment_status": payment_status,
            "status": status,
            "tier": tx.get("tier"),
        }

    @router.post("/webhook/stripe")
    async def stripe_webhook(request: Request):
        """Stripe webhook receiver — verifies signature via emergentintegrations
        and finalizes payment_transactions + user.subscription_status.
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
        if tx and evt.payment_status == "paid" and tx.get("payment_status") != "paid":
            await db.users.update_one(
                {"id": tx["user_id"]},
                {"$set": {
                    "membership_tier": tx.get("tier"),
                    "subscription_status": "active",
                    "subscription_updated_at": _now_iso(),
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
