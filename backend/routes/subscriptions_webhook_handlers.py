"""routes/subscriptions_webhook_handlers.py — Phase 15.B lifecycle handlers.

Status-gated, fail-safe, idempotent processing of the 10 handler groups / 11
Stripe event types listed in the Phase 15.B plan.

Dispatch contract (called by routes/subscriptions.py):
    await process_event(db, event_dict) -> (http_status, body_dict)

The caller is responsible for: signature verification (already done by 15.A
infra), translating the returned (status, body) tuple into a FastAPI
response, and propagating any HTTPException raised inside a handler.

All handlers MUST be idempotent (Stripe-ID-keyed upserts). All payload
strings written to billing_events.summary are capped at 500 chars. Raw
Stripe payload bodies are NEVER stored. Only the deliberately-listed
fields below land in our collections.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

import stripe
from fastapi import HTTPException

from core.entitlements import normalize_plan_code, plan_by_code
from core.subscription_records import sync_account_subscription_by_id, sync_account_subscription_records

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Constants / status enum (closed set — Phase 15.B lock J)
# ----------------------------------------------------------------------
STATUS_PROCESSING = "processing"
STATUS_OK = "ok"
STATUS_RETRY_502 = "retry_502"
STATUS_METADATA_MISSING_RETRYABLE = "metadata_missing_retryable"
STATUS_METADATA_MISSING_PERMANENT = "metadata_missing_permanent"
STATUS_UNKNOWN_EVENT = "unknown_event"

SHORT_CIRCUIT_STATUSES = {
    STATUS_OK,
    STATUS_UNKNOWN_EVENT,
    STATUS_METADATA_MISSING_PERMANENT,
}
REPLAY_STATUSES = {
    STATUS_RETRY_502,
    STATUS_METADATA_MISSING_RETRYABLE,
}

DEFAULT_STALE_LOCK_SECONDS = 60
SUMMARY_MAX_CHARS = 500

# 10 handler groups / 11 event types.
HANDLED_EVENTS = {
    "checkout.session.completed",
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
    "customer.subscription.trial_will_end",
    "invoice.created",
    "invoice.finalized",
    "invoice.paid",
    "invoice.payment_failed",
    "payment_intent.succeeded",
    "payment_intent.payment_failed",
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now().isoformat()


def _ts_to_iso(ts: Optional[int]) -> Optional[str]:
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _summary(*parts: Any) -> str:
    """Build a billing_events.summary string from a small list of safe parts.
    Caps at SUMMARY_MAX_CHARS. Never accepts a raw payload dict.
    """
    text = " · ".join(str(p) for p in parts if p is not None)
    return text[:SUMMARY_MAX_CHARS]


def _stale_lock_seconds() -> int:
    try:
        return int(os.environ.get("BILLING_EVENTS_STALE_LOCK_SECONDS") or DEFAULT_STALE_LOCK_SECONDS)
    except (TypeError, ValueError):
        return DEFAULT_STALE_LOCK_SECONDS


class _TransientStripeError(RuntimeError):
    """Marker raised by handlers to signal 'mark retry_502 and 502 the response'."""


class _MetadataMissing(RuntimeError):
    def __init__(self, retryable: bool, reason: str):
        self.retryable = retryable
        self.reason = reason
        super().__init__(reason)


# ----------------------------------------------------------------------
# Pipeline entry point — called from routes/subscriptions.py
# ----------------------------------------------------------------------
async def process_event(db, event: dict) -> tuple[int, dict]:
    event_id = event.get("id")
    event_type = (event.get("type") or "").strip()
    if not event_id:
        return 400, {"received": True, "handled": False, "reason": "missing event id"}

    # ---------- 1. Status-gated lookup ----------
    existing = await db.billing_events.find_one({"stripe_event_id": event_id})
    if existing:
        st = existing.get("processing_status")
        if st in SHORT_CIRCUIT_STATUSES:
            return 200, {
                "received": True,
                "handled": True,
                "idempotent": True,
                "status": st,
            }
        if st == STATUS_PROCESSING:
            ts_iso = existing.get("processed_at")
            stale = False
            ts = None
            if ts_iso:
                try:
                    ts = datetime.fromisoformat(ts_iso)
                    if (_now() - ts).total_seconds() > _stale_lock_seconds():
                        stale = True
                except (ValueError, TypeError):
                    # Codex round-3 #3: invalid ISO → treat as stale rather
                    # than crash. `ts` stays None for the log line below.
                    stale = True
                    ts = None
            else:
                stale = True
            if not stale:
                # Active lock: ask Stripe to redeliver. 409 per 15.B lock.
                return 409, {
                    "received": True,
                    "handled": False,
                    "in_flight": True,
                    "reason": "another worker is processing this event",
                }
            # Stale lock — reclaim.
            age_label = (
                f"{(_now() - ts).total_seconds():.1f}s" if ts is not None else "unknown"
            )
            logger.warning(
                "billing_events stale 'processing' lock reclaimed event_id=%s age=%s",
                event_id, age_label,
            )
            await db.billing_events.update_one(
                {"stripe_event_id": event_id},
                {"$set": {
                    "processing_status": STATUS_PROCESSING,
                    "processed_at": _now_iso(),
                    "updated_at": _now_iso(),
                }},
            )
        elif st in REPLAY_STATUSES:
            # Legitimate replay path — bump retry_count, claim, fall through.
            await db.billing_events.update_one(
                {"stripe_event_id": event_id},
                {
                    "$set": {
                        "processing_status": STATUS_PROCESSING,
                        "processed_at": _now_iso(),
                        "updated_at": _now_iso(),
                    },
                    "$inc": {"retry_count": 1},
                },
            )
        else:
            # Unknown status value — treat as replay (defensive).
            logger.warning(
                "billing_events row had unexpected processing_status=%s — replaying", st,
            )
    else:
        # 2. Fresh delivery — insert claim row.
        from pymongo.errors import DuplicateKeyError
        try:
            await db.billing_events.insert_one({
                "id": event_id,
                "stripe_event_id": event_id,
                "event_type": event_type,
                "event_created_at": _ts_to_iso(event.get("created")),
                "object_id": _safe_object_id(event),
                "barn_id": None,
                "summary": "",
                "processing_status": STATUS_PROCESSING,
                "processed_at": _now_iso(),
                "retry_count": 0,
                "last_error_class": None,
                "created_at": _now_iso(),
                "updated_at": _now_iso(),
            })
        except DuplicateKeyError as ex:
            # Codex round-3 #2: ONLY recurse on duplicate-key races.
            logger.info("billing_events claim race event_id=%s: %s", event_id, ex)
            return await process_event(db, event)
        except Exception as ex:
            # Codex round-3 #2: any other DB error → 502, NO recursion.
            logger.exception("billing_events insert failed event_id=%s: %s", event_id, ex)
            raise HTTPException(
                status_code=502,
                detail="Webhook claim insert failed; retry expected.",
            )

    # ---------- 3. Unknown event types ----------
    if event_type not in HANDLED_EVENTS:
        await _finalize(db, event_id, STATUS_UNKNOWN_EVENT, summary=_summary(event_type), barn_id=None)
        return 200, {"received": True, "handled": False, "type": event_type, "status": STATUS_UNKNOWN_EVENT}

    # ---------- 4. Dispatch ----------
    handler = _HANDLERS[event_type]
    try:
        barn_id, summary_parts = await handler(db, event)
    except _MetadataMissing as ex:
        if ex.retryable:
            # Codex round-3 #1: retryable metadata miss MUST return non-2xx
            # so Stripe replays the event. 503 is the natural pick (service
            # is temporarily unable to reconcile — try again later).
            await _finalize(db, event_id, STATUS_METADATA_MISSING_RETRYABLE,
                            summary=_summary(event_type, ex.reason), barn_id=None)
            raise HTTPException(
                status_code=503,
                detail=f"Metadata not yet resolvable; retry expected ({ex.reason}).",
            )
        # Permanent miss → 200 short-circuit (no future replay will help).
        await _finalize(db, event_id, STATUS_METADATA_MISSING_PERMANENT,
                        summary=_summary(event_type, ex.reason), barn_id=None)
        return 200, {"received": True, "handled": False, "type": event_type,
                     "status": STATUS_METADATA_MISSING_PERMANENT}
    except _TransientStripeError as ex:
        await _finalize(db, event_id, STATUS_RETRY_502,
                        summary=_summary(event_type, "transient_stripe"),
                        barn_id=None, last_error_class=type(ex).__name__)
        raise HTTPException(status_code=502, detail="Stripe API transient failure; retry expected.")
    except HTTPException:
        # Already a typed HTTP error — let it bubble (subscription router caller raises).
        raise
    except Exception as ex:
        logger.exception("billing_events handler crashed event_id=%s type=%s", event_id, event_type)
        await _finalize(db, event_id, STATUS_RETRY_502,
                        summary=_summary(event_type, "handler_exception"),
                        barn_id=None, last_error_class=type(ex).__name__)
        raise HTTPException(status_code=502, detail="Webhook handler transient failure; retry expected.")

    # ---------- 5. Success ----------
    await _finalize(db, event_id, STATUS_OK, summary=_summary(event_type, *summary_parts), barn_id=barn_id)
    return 200, {"received": True, "handled": True, "type": event_type, "idempotent": False}


async def _finalize(db, event_id: str, status: str, *, summary: str,
                    barn_id: Optional[str], last_error_class: Optional[str] = None):
    await db.billing_events.update_one(
        {"stripe_event_id": event_id},
        {"$set": {
            "processing_status": status,
            "processed_at": _now_iso(),
            "updated_at": _now_iso(),
            "summary": summary[:SUMMARY_MAX_CHARS],
            "barn_id": barn_id,
            "last_error_class": last_error_class,
        }},
    )


def _safe_object_id(event: dict) -> Optional[str]:
    obj = (event.get("data") or {}).get("object") or {}
    return obj.get("id")


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
async def _resolve_subscription_local(db, stripe_subscription_id: str) -> Optional[dict]:
    if not stripe_subscription_id:
        return None
    return await db.subscriptions.find_one(
        {"stripe_subscription_id": stripe_subscription_id}, {"_id": 0},
    )


async def _resolve_subscription_invoice_local(db, stripe_invoice_id: str) -> Optional[dict]:
    if not stripe_invoice_id:
        return None
    return await db.subscription_invoices.find_one(
        {"stripe_invoice_id": stripe_invoice_id}, {"_id": 0},
    )


async def _refresh_entitlements(db, sub_doc: dict, plan_tier_code: Optional[str]) -> dict:
    """Refresh entitlements_snapshot from plans + mirror onto the barn."""
    if not plan_tier_code:
        return sub_doc.get("entitlements_snapshot") or {}
    plan = await _resolve_plan_for_snapshot(db, plan_tier_code)
    snapshot = (plan or {}).get("feature_limits") or {}
    await db.subscriptions.update_one(
        {"stripe_subscription_id": sub_doc["stripe_subscription_id"]},
        {"$set": {"entitlements_snapshot": snapshot, "updated_at": _now_iso()}},
    )
    if sub_doc.get("barn_id"):
        await db.barns.update_one(
            {"id": sub_doc["barn_id"]},
            {
                "$set": {"subscription_entitlements": snapshot},
                "$setOnInsert": {"id": sub_doc["barn_id"], "created_at": _now_iso()},
            },
            upsert=True,
        )
    return snapshot


async def _resolve_plan_for_snapshot(db, plan_tier_code: Optional[str]) -> dict:
    """Resolve a non-empty entitlement source for webhook subscription mirrors."""
    if not plan_tier_code:
        raise _MetadataMissing(retryable=True, reason="plan_tier_code not resolvable")
    plan = await db.plans.find_one({"tier_code": plan_tier_code}, {"_id": 0})
    if plan:
        return plan
    try:
        return plan_by_code(plan_tier_code)
    except ValueError as ex:
        raise _MetadataMissing(
            retryable=True,
            reason=f"plan_tier_code not resolvable: {plan_tier_code}",
        ) from ex


async def _mirror_inactive_subscription_to_barn(db, *, barn_id: Optional[str], stripe_subscription_id: str) -> None:
    if not barn_id:
        return
    free_plan = await _resolve_plan_for_snapshot(db, "free")
    await db.barns.update_one(
        {"id": barn_id},
        {"$set": {
            "subscription_id": None,
            "subscription_entitlements": free_plan.get("feature_limits") or {},
            "subscription_updated_at": _now_iso(),
            "last_inactive_subscription_id": stripe_subscription_id,
        }},
    )


def _safe_stripe_retrieve(retriever_fn):
    """Wrap a Stripe SDK call so transient failures become _TransientStripeError."""
    try:
        return retriever_fn()
    except stripe.error.StripeError as ex:
        logger.warning("stripe transient failure: %s", ex)
        raise _TransientStripeError(str(ex))


# ----------------------------------------------------------------------
# Per-event handlers — each returns (barn_id, summary_parts_tuple)
# ----------------------------------------------------------------------

async def _h_checkout_session_completed(db, event):
    session = (event.get("data") or {}).get("object") or {}
    metadata = session.get("metadata") or {}
    barn_id = metadata.get("barn_id")
    stripe_subscription_id = session.get("subscription")
    plan_tier_code = normalize_plan_code(metadata.get("plan_tier_code"))
    billing_cycle = metadata.get("billing_cycle")
    if not (barn_id and stripe_subscription_id and plan_tier_code):
        # 15.A contract: this metadata is always present on OUR sessions.
        raise _MetadataMissing(retryable=False, reason="missing required metadata")

    # Idempotent path — if a subscription row already exists, ensure barn
    # pointer is repaired (same contract as the 15.A handler).
    existing = await db.subscriptions.find_one(
        {"stripe_subscription_id": stripe_subscription_id}
    )
    if existing:
        await db.barns.update_one(
            {"id": barn_id},
            {
                "$set": {
                    "subscription_id": stripe_subscription_id,
                    "subscription_updated_at": _now_iso(),
                },
                "$setOnInsert": {"id": barn_id, "created_at": _now_iso()},
            },
            upsert=True,
        )
        await sync_account_subscription_by_id(db, stripe_subscription_id=stripe_subscription_id)
        return barn_id, ("checkout_replay", stripe_subscription_id)

    stripe_sub = _safe_stripe_retrieve(
        lambda: stripe.Subscription.retrieve(stripe_subscription_id)
    )
    plan = await _resolve_plan_for_snapshot(db, plan_tier_code)
    snapshot = (plan or {}).get("feature_limits") or {}
    items = (stripe_sub.get("items") or {}).get("data") or [{}]
    price_id = (items[0].get("price") or {}).get("id")

    sub_doc = {
        "id": stripe_subscription_id,
        "barn_id": barn_id,
        "owner_user_id": metadata.get("owner_user_id"),
        "plan_id": (plan or {}).get("id") or plan_tier_code,
        "plan_tier_code": plan_tier_code,
        "stripe_customer_id": session.get("customer"),
        "stripe_subscription_id": stripe_subscription_id,
        "stripe_price_id": price_id,
        "status": stripe_sub.get("status"),
        "billing_cycle": billing_cycle,
        "current_period_start": _ts_to_iso(stripe_sub.get("current_period_start")),
        "current_period_end": _ts_to_iso(stripe_sub.get("current_period_end")),
        "cancel_at_period_end": bool(stripe_sub.get("cancel_at_period_end")),
        "trial_end": _ts_to_iso(stripe_sub.get("trial_end")),
        "entitlements_snapshot": snapshot,
        "pending_emails": [],
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "last_event_at": _now_iso(),
    }
    await db.subscriptions.insert_one(sub_doc)
    await db.barns.update_one(
        {"id": barn_id},
        {
            "$set": {
                "subscription_id": stripe_subscription_id,
                "subscription_entitlements": snapshot,
                "subscription_updated_at": _now_iso(),
            },
            "$setOnInsert": {"id": barn_id, "created_at": _now_iso()},
        },
        upsert=True,
    )
    await sync_account_subscription_records(db, sub_doc)
    return barn_id, ("checkout_created", stripe_subscription_id)


async def _h_subscription_created(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    stripe_subscription_id = obj.get("id")
    if not stripe_subscription_id:
        raise _MetadataMissing(retryable=False, reason="missing subscription id")
    metadata = obj.get("metadata") or {}
    barn_id = metadata.get("barn_id")
    if not barn_id:
        existing = await _resolve_subscription_local(db, stripe_subscription_id)
        barn_id = (existing or {}).get("barn_id")
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="barn_id not resolvable yet")
    # Same upsert contract as checkout — idempotent.
    plan_tier_code = normalize_plan_code(
        metadata.get("plan_tier_code")
        or (await _resolve_subscription_local(db, stripe_subscription_id) or {}).get("plan_tier_code")
    )
    plan = await _resolve_plan_for_snapshot(db, plan_tier_code)
    snapshot = (plan or {}).get("feature_limits") or {}
    items = (obj.get("items") or {}).get("data") or [{}]
    price_id = (items[0].get("price") or {}).get("id")
    # Phase 15.G — persist amount_cents (Stripe `unit_amount`) so the
    # admin billing dashboard MRR fallback + invoice ledger never needs a
    # round-trip to the Stripe API to find the line-item amount.
    # Round-2 (Codex should-fix): only set when the field is present so
    # an event without unit_amount cannot overwrite a known nonzero value.
    raw_amount = (items[0].get("price") or {}).get("unit_amount")
    set_doc = {
        "barn_id": barn_id,
        "stripe_subscription_id": stripe_subscription_id,
        "stripe_customer_id": obj.get("customer"),
        "stripe_price_id": price_id,
        "plan_tier_code": plan_tier_code,
        "status": obj.get("status"),
        "current_period_start": _ts_to_iso(obj.get("current_period_start")),
        "current_period_end": _ts_to_iso(obj.get("current_period_end")),
        "cancel_at_period_end": bool(obj.get("cancel_at_period_end")),
        "trial_end": _ts_to_iso(obj.get("trial_end")),
        "entitlements_snapshot": snapshot,
        "updated_at": _now_iso(),
        "last_event_at": _now_iso(),
    }
    if raw_amount is not None:
        set_doc["amount_cents"] = raw_amount
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": set_doc,
            "$setOnInsert": {
                "id": stripe_subscription_id,
                "owner_user_id": metadata.get("owner_user_id"),
                "billing_cycle": metadata.get("billing_cycle"),
                "pending_emails": [],
                "created_at": _now_iso(),
            },
        },
        upsert=True,
    )
    # Codex round-3 #4: also stamp barn pointer + entitlements snapshot so an
    # out-of-order `customer.subscription.created` (arrived before our
    # checkout.session.completed) still produces a consistent barn record.
    await db.barns.update_one(
        {"id": barn_id},
        {
            "$set": {
                "subscription_id": stripe_subscription_id,
                "subscription_entitlements": snapshot,
                "subscription_updated_at": _now_iso(),
            },
            "$setOnInsert": {"id": barn_id, "created_at": _now_iso()},
        },
        upsert=True,
    )
    await sync_account_subscription_by_id(db, stripe_subscription_id=stripe_subscription_id)
    return barn_id, ("subscription_created", stripe_subscription_id)


async def _h_subscription_updated(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    stripe_subscription_id = obj.get("id")
    local = await _resolve_subscription_local(db, stripe_subscription_id)
    metadata = obj.get("metadata") or {}
    barn_id = (local or {}).get("barn_id") or metadata.get("barn_id")
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="barn_id not resolvable yet")
    items = (obj.get("items") or {}).get("data") or [{}]
    new_price_id = (items[0].get("price") or {}).get("id")

    # Codex round-3 #4 / round-4 blocker: when there's no local row, we must
    # produce a FULL record (plan_tier_code + entitlements_snapshot + barn
    # mirror) — not a partial one that we'd then mark `ok` and never repair.
    # If metadata doesn't have enough to fully reconstruct, retry until a
    # fuller event arrives.
    if not local:
        plan_tier_code = normalize_plan_code(metadata.get("plan_tier_code"))
        if not plan_tier_code:
            # Try resolving via the price id against our local plan catalog.
            if new_price_id:
                plan_by_price = await db.plans.find_one(
                    {"$or": [
                        {"stripe_price_id_monthly": new_price_id},
                        {"stripe_price_id_annual": new_price_id},
                    ]},
                    {"_id": 0},
                )
                if plan_by_price:
                    plan_tier_code = plan_by_price.get("tier_code")
        if not plan_tier_code:
            raise _MetadataMissing(
                retryable=True,
                reason="no local row and plan_tier_code not resolvable from metadata or price",
            )
        plan = await _resolve_plan_for_snapshot(db, plan_tier_code)
        snapshot = (plan or {}).get("feature_limits") or {}
        raw_amount = (items[0].get("price") or {}).get("unit_amount")
        set_doc = {
            "barn_id": barn_id,
            "stripe_subscription_id": stripe_subscription_id,
            "stripe_customer_id": obj.get("customer"),
            "stripe_price_id": new_price_id,
            "plan_id": (plan or {}).get("id") or plan_tier_code,
            "plan_tier_code": plan_tier_code,
            "status": obj.get("status"),
            "current_period_start": _ts_to_iso(obj.get("current_period_start")),
            "current_period_end": _ts_to_iso(obj.get("current_period_end")),
            "cancel_at_period_end": bool(obj.get("cancel_at_period_end")),
            "trial_end": _ts_to_iso(obj.get("trial_end")),
            "entitlements_snapshot": snapshot,
            "updated_at": _now_iso(),
            "last_event_at": _now_iso(),
        }
        if raw_amount is not None:
            set_doc["amount_cents"] = raw_amount
        await db.subscriptions.update_one(
            {"stripe_subscription_id": stripe_subscription_id},
            {
                "$set": set_doc,
                "$setOnInsert": {
                    "id": stripe_subscription_id,
                    "owner_user_id": metadata.get("owner_user_id"),
                    "billing_cycle": metadata.get("billing_cycle"),
                    "pending_emails": [],
                    "created_at": _now_iso(),
                },
            },
            upsert=True,
        )
        await db.barns.update_one(
            {"id": barn_id},
            {
                "$set": {
                    "subscription_id": stripe_subscription_id,
                    "subscription_entitlements": snapshot,
                    "subscription_updated_at": _now_iso(),
                },
                "$setOnInsert": {"id": barn_id, "created_at": _now_iso()},
            },
            upsert=True,
        )
        await sync_account_subscription_by_id(db, stripe_subscription_id=stripe_subscription_id)
        return barn_id, ("subscription_updated_bootstrapped", stripe_subscription_id, plan_tier_code)

    # ---------- Existing local row: standard update path ----------
    new_raw_amount = (items[0].get("price") or {}).get("unit_amount")
    set_doc = {
        "barn_id": barn_id,
        "stripe_subscription_id": stripe_subscription_id,
        "stripe_customer_id": obj.get("customer"),
        "status": obj.get("status"),
        "current_period_start": _ts_to_iso(obj.get("current_period_start")),
        "current_period_end": _ts_to_iso(obj.get("current_period_end")),
        "cancel_at_period_end": bool(obj.get("cancel_at_period_end")),
        "trial_end": _ts_to_iso(obj.get("trial_end")),
        "stripe_price_id": new_price_id,
        "updated_at": _now_iso(),
        "last_event_at": _now_iso(),
    }
    if new_raw_amount is not None:
        set_doc["amount_cents"] = new_raw_amount
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id}, {"$set": set_doc},
    )
    summary_parts = ["subscription_updated", stripe_subscription_id]
    # Entitlements refresh on price change.
    if local and new_price_id and new_price_id != local.get("stripe_price_id"):
        # Resolve the new tier code from the plan whose monthly OR annual price matches.
        new_plan = await db.plans.find_one(
            {"$or": [
                {"stripe_price_id_monthly": new_price_id},
                {"stripe_price_id_annual": new_price_id},
            ]},
            {"_id": 0},
        )
        new_tier_code = (new_plan or {}).get("tier_code")
        if new_tier_code:
            updated_sub = await _resolve_subscription_local(db, stripe_subscription_id)
            await db.subscriptions.update_one(
                {"stripe_subscription_id": stripe_subscription_id},
                {"$set": {"plan_tier_code": new_tier_code, "plan_id": (new_plan or {}).get("id") or new_tier_code}},
            )
            updated_sub["plan_tier_code"] = new_tier_code
            await _refresh_entitlements(db, updated_sub, new_tier_code)
            summary_parts.append(f"price_changed:{new_tier_code}")
    await sync_account_subscription_by_id(db, stripe_subscription_id=stripe_subscription_id)
    if (obj.get("status") or "").strip().lower() in {"canceled", "cancelled", "unpaid", "incomplete_expired"}:
        await _mirror_inactive_subscription_to_barn(
            db,
            barn_id=barn_id,
            stripe_subscription_id=stripe_subscription_id,
        )
    return barn_id, tuple(summary_parts)


async def _h_subscription_deleted(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    stripe_subscription_id = obj.get("id")
    local = await _resolve_subscription_local(db, stripe_subscription_id)
    if not local:
        raise _MetadataMissing(retryable=False, reason="no local subscription to cancel")
    barn_id = local.get("barn_id")
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {"$set": {
            "status": "canceled",
            "canceled_at": _now_iso(),
            "updated_at": _now_iso(),
            "last_event_at": _now_iso(),
        }},
    )
    if barn_id:
        await _mirror_inactive_subscription_to_barn(
            db,
            barn_id=barn_id,
            stripe_subscription_id=stripe_subscription_id,
        )
    await sync_account_subscription_by_id(db, stripe_subscription_id=stripe_subscription_id)
    return barn_id, ("subscription_deleted", stripe_subscription_id)


async def _h_subscription_trial_will_end(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    stripe_subscription_id = obj.get("id")
    local = await _resolve_subscription_local(db, stripe_subscription_id)
    barn_id = (local or {}).get("barn_id") or ((obj.get("metadata") or {}).get("barn_id"))
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="barn_id not resolvable yet")
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": {
                "trial_will_end_at": _ts_to_iso(obj.get("trial_end")),
                "updated_at": _now_iso(),
                "last_event_at": _now_iso(),
            },
            "$addToSet": {"pending_emails": "trial_will_end"},
        },
    )
    return barn_id, ("trial_will_end", stripe_subscription_id)


async def _resolve_invoice_barn(db, invoice_obj: dict) -> Optional[str]:
    sub_id = invoice_obj.get("subscription")
    if sub_id:
        sub = await _resolve_subscription_local(db, sub_id)
        if sub:
            return sub.get("barn_id")
    cust = invoice_obj.get("customer")
    if cust:
        sub = await db.subscriptions.find_one({"stripe_customer_id": cust}, {"_id": 0})
        if sub:
            return sub.get("barn_id")
    return None


async def _upsert_subscription_invoice(db, invoice_obj: dict, barn_id: str, *, extra_set: Optional[dict] = None) -> str:
    stripe_invoice_id = invoice_obj.get("id")
    sub_id = invoice_obj.get("subscription")
    set_doc = {
        "barn_id": barn_id,
        "subscription_id": sub_id,
        "stripe_invoice_id": stripe_invoice_id,
        "stripe_customer_id": invoice_obj.get("customer"),
        "amount_cents": invoice_obj.get("amount_due") or invoice_obj.get("amount_paid") or 0,
        "currency": invoice_obj.get("currency"),
        "status": invoice_obj.get("status"),
        "hosted_invoice_url": invoice_obj.get("hosted_invoice_url"),
        "invoice_pdf_url": invoice_obj.get("invoice_pdf"),
        "period_start": _ts_to_iso(invoice_obj.get("period_start")),
        "period_end": _ts_to_iso(invoice_obj.get("period_end")),
        "due_date": _ts_to_iso(invoice_obj.get("due_date")),
        "updated_at": _now_iso(),
    }
    if extra_set:
        set_doc.update(extra_set)
    await db.subscription_invoices.update_one(
        {"stripe_invoice_id": stripe_invoice_id},
        {
            "$set": set_doc,
            "$setOnInsert": {
                "id": stripe_invoice_id,
                "payment_failure_count": 0,
                "created_at": _now_iso(),
            },
        },
        upsert=True,
    )
    return stripe_invoice_id


async def _h_invoice_created(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    barn_id = await _resolve_invoice_barn(db, obj)
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="subscription not synced for invoice")
    iid = await _upsert_subscription_invoice(db, obj, barn_id)
    return barn_id, ("invoice_created", iid)


async def _h_invoice_finalized(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    barn_id = await _resolve_invoice_barn(db, obj)
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="subscription not synced for invoice")
    iid = await _upsert_subscription_invoice(db, obj, barn_id)
    return barn_id, ("invoice_finalized", iid)


async def _h_invoice_paid(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    barn_id = await _resolve_invoice_barn(db, obj)
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="subscription not synced for invoice")
    iid = await _upsert_subscription_invoice(
        db, obj, barn_id,
        extra_set={"paid_at": _ts_to_iso(obj.get("status_transitions", {}).get("paid_at")) or _now_iso()},
    )
    # Insert/update payments row via the payment_intent
    pi_id = obj.get("payment_intent")
    if pi_id:
        await db.payments.update_one(
            {"stripe_payment_intent_id": pi_id},
            {
                "$set": {
                    "barn_id": barn_id,
                    "subscription_id": obj.get("subscription"),
                    "stripe_invoice_id": iid,
                    "amount_cents": obj.get("amount_paid") or 0,
                    "currency": obj.get("currency"),
                    "status": "succeeded",
                    "processed_at": _now_iso(),
                    "updated_at": _now_iso(),
                },
                "$setOnInsert": {
                    "id": pi_id,
                    "stripe_payment_intent_id": pi_id,
                    "created_at": _now_iso(),
                },
            },
            upsert=True,
        )
    # Pending-email flag (additive).
    sub_id = obj.get("subscription")
    if sub_id:
        await db.subscriptions.update_one(
            {"stripe_subscription_id": sub_id},
            {"$addToSet": {"pending_emails": "payment_succeeded"},
             "$set": {"last_event_at": _now_iso()}},
        )
    return barn_id, ("invoice_paid", iid)


async def _h_invoice_payment_failed(db, event):
    obj = (event.get("data") or {}).get("object") or {}
    barn_id = await _resolve_invoice_barn(db, obj)
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="subscription not synced for invoice")
    iid = obj.get("id")
    # Mirror Stripe's actual status — do NOT force uncollectible.
    set_doc = {
        "barn_id": barn_id,
        "subscription_id": obj.get("subscription"),
        "stripe_invoice_id": iid,
        "stripe_customer_id": obj.get("customer"),
        "amount_cents": obj.get("amount_due") or 0,
        "currency": obj.get("currency"),
        "status": obj.get("status"),  # whatever Stripe says (often "open").
        "hosted_invoice_url": obj.get("hosted_invoice_url"),
        "invoice_pdf_url": obj.get("invoice_pdf"),
        "payment_failed_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    await db.subscription_invoices.update_one(
        {"stripe_invoice_id": iid},
        {
            "$set": set_doc,
            "$setOnInsert": {
                "id": iid,
                "created_at": _now_iso(),
            },
            "$inc": {"payment_failure_count": 1},
        },
        upsert=True,
    )
    await db.barns.update_one(
        {"id": barn_id},
        {
            "$set": {"last_payment_failed_at": _now_iso()},
            "$setOnInsert": {"id": barn_id, "created_at": _now_iso()},
        },
        upsert=True,
    )
    sub_id = obj.get("subscription")
    if sub_id:
        await db.subscriptions.update_one(
            {"stripe_subscription_id": sub_id},
            {"$addToSet": {"pending_emails": "payment_failed"},
             "$set": {"last_event_at": _now_iso()}},
        )
    return barn_id, ("invoice_payment_failed", iid, obj.get("status"))


async def _h_payment_intent(db, event):
    """Single handler for both payment_intent.succeeded and .payment_failed."""
    obj = (event.get("data") or {}).get("object") or {}
    pi_id = obj.get("id")
    invoice_id = obj.get("invoice")
    barn_id = None
    sub_id = None
    if invoice_id:
        inv = await _resolve_subscription_invoice_local(db, invoice_id)
        if inv:
            barn_id = inv.get("barn_id")
            sub_id = inv.get("subscription_id")
    if not barn_id:
        cust = obj.get("customer")
        if cust:
            sub = await db.subscriptions.find_one({"stripe_customer_id": cust}, {"_id": 0})
            if sub:
                barn_id = sub.get("barn_id")
                sub_id = sub.get("stripe_subscription_id")
    if not barn_id:
        raise _MetadataMissing(retryable=True, reason="invoice/subscription not synced for payment_intent")
    event_type = (event.get("type") or "")
    status = "succeeded" if event_type.endswith(".succeeded") else "failed"
    charges = (obj.get("charges") or {}).get("data") or [{}]
    payment_method = (charges[0].get("payment_method_details") or {}).get("card") or {}
    set_doc = {
        "barn_id": barn_id,
        "subscription_id": sub_id,
        "stripe_payment_intent_id": pi_id,
        "stripe_invoice_id": invoice_id,
        "amount_cents": obj.get("amount") or 0,
        "currency": obj.get("currency"),
        "status": status,
        "payment_method_brand": payment_method.get("brand"),
        "payment_method_last4": payment_method.get("last4"),
        "failure_message": obj.get("last_payment_error", {}).get("message"),
        "processed_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    await db.payments.update_one(
        {"stripe_payment_intent_id": pi_id},
        {
            "$set": set_doc,
            "$setOnInsert": {
                "id": pi_id,
                "created_at": _now_iso(),
            },
        },
        upsert=True,
    )
    return barn_id, ("payment_intent", status, pi_id)


_HANDLERS = {
    "checkout.session.completed": _h_checkout_session_completed,
    "customer.subscription.created": _h_subscription_created,
    "customer.subscription.updated": _h_subscription_updated,
    "customer.subscription.deleted": _h_subscription_deleted,
    "customer.subscription.trial_will_end": _h_subscription_trial_will_end,
    "invoice.created": _h_invoice_created,
    "invoice.finalized": _h_invoice_finalized,
    "invoice.paid": _h_invoice_paid,
    "invoice.payment_failed": _h_invoice_payment_failed,
    "payment_intent.succeeded": _h_payment_intent,
    "payment_intent.payment_failed": _h_payment_intent,
}
