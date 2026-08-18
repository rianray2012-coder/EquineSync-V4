"""Phase 15.D — Subscription email dispatcher.

Consumes the `subscriptions.pending_emails` queue that Phase 15.B webhook
handlers populate via `$addToSet`. One pass scans every subscription with a
non-empty queue, sends each pending email through the existing `mailer.send`
layer, and **pulls the event key from the queue only on a successful send**.
Failures stay in the queue and get re-tried on the next pass; after
`MAX_ATTEMPTS` they're recorded as `permanent_failure` and pulled off the
queue so they stop blocking the rest.

Idempotency / audit model
-------------------------
Every send attempt writes a row to the `subscription_email_log` collection
keyed on `(subscription_id, event_key)`. Re-runs UPSERT the same row so a
re-delivery from Stripe (which re-adds the key via `$addToSet`) doesn't
inflate the attempt counter beyond the actual mailer calls. Status values:

    queued     — initial state when first observed
    sent       — mailer returned status=ok or status=dev
    failed     — mailer raised / returned an error; will retry
    permanent_failure — `MAX_ATTEMPTS` reached; key was pulled, no more retries

Strict guardrails
-----------------
* Does NOT mutate `subscriptions` apart from `$pull`ing event keys on
  terminal status (sent / permanent_failure). Stripe subscription state is
  owned by `subscriptions_webhook_handlers.py`.
* Brand name in all subject lines + template copy is **EquineSync**.
* Per-row try/except: one bad subscription cannot halt the loop.
* Never references the legacy `invoices` collection or Phase-9 mailers.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, List, Optional

logger = logging.getLogger("equinesync.subscription_emails")

# mailer.py contract (see backend/mailer.py::send):
#   live success     → {"status": "sent"}
#   no RESEND_API_KEY → {"status": "dev_logged", "dev": True}
#   sandbox-rejected  → {"status": "sandbox", "dev": True}   (treated as success
#                       across the codebase — invites/auth log the send and
#                       surface dev_url to the inviter)
#   live failure      → {"status": "error", "error": "<msg>"}
SUCCESS_MAILER_STATUSES = frozenset({"sent", "dev_logged", "sandbox"})

# Event keys we currently know how to render. 15.B webhook handlers only
# enqueue these three; anything else is treated as an unknown key and
# pulled off so it doesn't block the queue forever.
KNOWN_EVENT_KEYS: List[str] = [
    "trial_will_end",
    "payment_succeeded",
    "payment_failed",
]

MAX_ATTEMPTS = 5

# Subject lines — concierge-warm tone, but still recognizable as billing
# emails (per round-2 user direction).
SUBJECTS: Dict[str, str] = {
    "trial_will_end":     "EquineSync — your trial ends soon",
    "payment_succeeded":  "EquineSync — payment received, you're all set",
    "payment_failed":     "EquineSync — payment issue, please review",
}

TEMPLATES: Dict[str, str] = {
    "trial_will_end":     "subscription_trial_will_end",
    "payment_succeeded":  "subscription_payment_succeeded",
    "payment_failed":     "subscription_payment_failed",
}


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------

async def run_subscription_email_pass(
    db,
    mailer: Dict[str, Callable[..., Awaitable[Any]]],
    *,
    public_base_url: Optional[str] = None,
    now: Optional[datetime] = None,
) -> Dict[str, int]:
    """Process every subscription with a non-empty `pending_emails` queue.

    Args:
        db: motor / async pymongo database handle.
        mailer: ``{"send": send_fn, ...}`` — usually ``{"send": send_email,
            "render": render_email}`` from `mailer.py`. Tests pass an async
            mock here.
        public_base_url: optional override for the {subscription_url} link
            inserted into templates. Falls back to env
            ``PUBLIC_FRONTEND_URL`` then ``http://localhost:3000``.
        now: optional datetime override (tests).

    Returns:
        ``{"scanned": int, "sent": int, "failed": int, "permanent_failures":
        int, "unknown_pulled": int}``
    """
    now = now or datetime.now(timezone.utc)
    base_url = (public_base_url or os.environ.get("PUBLIC_FRONTEND_URL")
                or "http://localhost:3000").rstrip("/")

    cursor = db.subscriptions.find(
        {"pending_emails": {"$exists": True, "$ne": []}},
        {"_id": 0},
    )
    subs = await cursor.to_list(length=10_000)

    stats = {"scanned": 0, "sent": 0, "failed": 0,
             "permanent_failures": 0, "unknown_pulled": 0}

    for sub in subs:
        stats["scanned"] += 1
        try:
            await _process_one_subscription(db, mailer, sub, base_url, now, stats)
        except Exception:
            logger.exception(
                "subscription_emails: subscription %s failed catastrophically; will retry next pass",
                sub.get("stripe_subscription_id") or sub.get("id"),
            )

    return stats


async def _process_one_subscription(
    db, mailer, sub: dict, base_url: str, now: datetime, stats: dict,
) -> None:
    sub_id = sub.get("stripe_subscription_id") or sub.get("id")
    pending = list(dict.fromkeys(sub.get("pending_emails") or []))  # dedupe, preserve order
    if not pending:
        return

    for event_key in pending:
        if event_key not in KNOWN_EVENT_KEYS:
            # Pull unknown keys so they don't block forever; record once.
            await db.subscription_email_log.update_one(
                {"subscription_id": sub_id, "event_key": event_key},
                {"$set": {"status": "permanent_failure",
                          "last_error": "unknown_event_key",
                          "updated_at": now.isoformat()},
                 "$setOnInsert": {"created_at": now.isoformat(), "attempt": 0}},
                upsert=True,
            )
            await db.subscriptions.update_one(
                {"stripe_subscription_id": sub_id},
                {"$pull": {"pending_emails": event_key}},
            )
            stats["unknown_pulled"] += 1
            continue

        await _send_one_event(db, mailer, sub, event_key, base_url, now, stats)


async def _send_one_event(
    db, mailer, sub: dict, event_key: str, base_url: str,
    now: datetime, stats: dict,
) -> None:
    sub_id = sub.get("stripe_subscription_id") or sub.get("id")
    log_filter = {"subscription_id": sub_id, "event_key": event_key}

    # ------------------------------------------------------------------
    # Re-queue safety (round-2 review).
    # The log row is keyed only by (subscription_id, event_key). 15.B uses
    # $addToSet, so a future re-occurrence of the same event (e.g. a later
    # renewal `payment_succeeded`, or a fresh `payment_failed` long after a
    # prior permanent failure) re-puts the same key on the queue. Without
    # this reset, the pre-flight $inc would carry the old terminal counter
    # forward and the next send would be silently pulled. When we see a
    # queued key whose previous log row is already terminal, blank-slate
    # the counter so the new occurrence gets a full retry budget.
    # ------------------------------------------------------------------
    prev = await db.subscription_email_log.find_one(log_filter, {"_id": 0})
    if prev and prev.get("status") in ("sent", "permanent_failure"):
        await db.subscription_email_log.update_one(
            log_filter,
            {"$set": {"attempt": 0, "status": "queued",
                      "last_error": None, "previous_terminal_status": prev["status"],
                      "previous_terminal_at": prev.get("updated_at"),
                      "updated_at": now.isoformat()}},
        )

    # Pre-flight attempt-counter bump (UPSERT). We read the post-update doc
    # to know the current attempt number.
    log_row = await db.subscription_email_log.find_one_and_update(
        log_filter,
        {"$inc": {"attempt": 1},
         "$set": {"status": "queued", "updated_at": now.isoformat()},
         "$setOnInsert": {"created_at": now.isoformat()}},
        upsert=True,
        return_document=True,
    )
    attempt = (log_row or {}).get("attempt", 1)
    if attempt > MAX_ATTEMPTS:
        # Belt-and-braces: if a previous pass already marked permanent and
        # somehow the key is still on the queue, pull it now.
        await db.subscriptions.update_one(
            {"stripe_subscription_id": sub_id},
            {"$pull": {"pending_emails": event_key}},
        )
        return

    recipient = await _resolve_recipient(db, sub)
    if not recipient:
        await _mark_attempt(db, log_filter, "failed",
                            error="no_recipient_email", now=now)
        stats["failed"] += 1
        if attempt >= MAX_ATTEMPTS:
            await _promote_to_permanent(db, log_filter, sub_id, event_key, now)
            stats["permanent_failures"] += 1
        return

    variables = await _build_variables(db, sub, event_key, base_url)
    subject = SUBJECTS[event_key]
    template = TEMPLATES[event_key]

    try:
        result = await mailer["send"](
            to=recipient,
            subject=subject,
            template=template,
            variables=variables,
            base="_base_auth",
        )
        # mailer.send contract documented at top of file. Live success
        # ("sent"), dev-mode ("dev_logged"), and sandbox-rejected ("sandbox")
        # all count as delivered — matches how invites/auth treat them.
        status = (result or {}).get("status") if isinstance(result, dict) else None
        if status in SUCCESS_MAILER_STATUSES:
            await _mark_attempt(db, log_filter, "sent",
                                message_id=(result or {}).get("id"), now=now)
            await db.subscriptions.update_one(
                {"stripe_subscription_id": sub_id},
                {"$pull": {"pending_emails": event_key}},
            )
            stats["sent"] += 1
            return
        # Unknown / error status — count as failure.
        err_msg = (result or {}).get("error") or f"mailer_status={status!r}"
        await _mark_attempt(db, log_filter, "failed",
                            error=str(err_msg)[:500], now=now)
        stats["failed"] += 1
    except Exception as ex:
        logger.exception("subscription_emails: send failed for %s/%s", sub_id, event_key)
        await _mark_attempt(db, log_filter, "failed",
                            error=str(ex)[:500], now=now)
        stats["failed"] += 1

    if attempt >= MAX_ATTEMPTS:
        await _promote_to_permanent(db, log_filter, sub_id, event_key, now)
        stats["permanent_failures"] += 1


async def _mark_attempt(db, log_filter, status, *, error=None,
                        message_id=None, now: datetime) -> None:
    update: Dict[str, Any] = {"status": status, "updated_at": now.isoformat()}
    if status == "sent":
        update["sent_at"] = now.isoformat()
        update["last_error"] = None
        if message_id:
            update["message_id"] = message_id
    elif error is not None:
        update["last_error"] = error
    await db.subscription_email_log.update_one(log_filter, {"$set": update})


async def _promote_to_permanent(db, log_filter, sub_id, event_key,
                                now: datetime) -> None:
    await db.subscription_email_log.update_one(
        log_filter,
        {"$set": {"status": "permanent_failure",
                  "updated_at": now.isoformat()}},
    )
    await db.subscriptions.update_one(
        {"stripe_subscription_id": sub_id},
        {"$pull": {"pending_emails": event_key}},
    )


# ---------------------------------------------------------------------------
# Recipient + variable resolution
# ---------------------------------------------------------------------------

async def _resolve_recipient(db, sub: dict) -> Optional[str]:
    """Return the owner_user_id's email (single recipient, per 15.D plan)."""
    owner_user_id = sub.get("owner_user_id")
    if not owner_user_id:
        return None
    user = await db.users.find_one({"id": owner_user_id}, {"_id": 0, "email": 1})
    email = (user or {}).get("email")
    return email if email else None


def _friendly_date(iso_or_dt: Any) -> str:
    if not iso_or_dt:
        return ""
    if isinstance(iso_or_dt, datetime):
        dt = iso_or_dt
    else:
        try:
            dt = datetime.fromisoformat(str(iso_or_dt).replace("Z", "+00:00"))
        except Exception:
            return str(iso_or_dt)
    return dt.strftime("%B %-d, %Y")


def _money(cents: Optional[int]) -> str:
    if cents is None:
        return ""
    dollars = cents / 100
    has_fraction = round(dollars) != dollars
    return f"${dollars:,.2f}" if has_fraction else f"${int(round(dollars)):,}"


async def _build_variables(db, sub: dict, event_key: str,
                           base_url: str) -> Dict[str, Any]:
    sub_id = sub.get("stripe_subscription_id") or sub.get("id")
    owner_user_id = sub.get("owner_user_id")
    user = (await db.users.find_one({"id": owner_user_id}, {"_id": 0})) if owner_user_id else None
    full_name = (user or {}).get("full_name") or "there"

    plan_tier = sub.get("plan_tier_code") or "your plan"
    plan_name = plan_tier.capitalize() if isinstance(plan_tier, str) else "your plan"
    billing_cycle = sub.get("billing_cycle") or "monthly"

    variables: Dict[str, Any] = {
        "full_name": full_name,
        "plan_name": plan_name,
        "billing_cycle": billing_cycle,
        "subscription_url": f"{base_url}/billing/subscription",
    }

    if event_key == "trial_will_end":
        trial_end = sub.get("trial_end")
        variables["trial_end_friendly"] = _friendly_date(trial_end) or "soon"
        # Days-left is best-effort; if trial_end is missing, fall back to "soon".
        days_left = 3
        try:
            if trial_end:
                te = datetime.fromisoformat(str(trial_end).replace("Z", "+00:00"))
                delta = (te - datetime.now(timezone.utc)).total_seconds() / 86400
                days_left = max(0, int(round(delta)))
        except Exception:
            pass
        variables["days_left"] = days_left
        variables["days_left_plural"] = "" if days_left == 1 else "s"

    elif event_key in ("payment_succeeded", "payment_failed"):
        # Pull the most recent subscription_invoice for this subscription.
        # Schema source of truth: backend/routes/subscriptions_webhook_handlers
        # _upsert_subscription_invoice — `subscription_id` holds the Stripe
        # subscription id, monetary value lives on `amount_cents`, and the
        # paid/failed timestamps live on `paid_at` / `payment_failed_at`.
        invoice = None
        try:
            invoice = await db.subscription_invoices.find_one(
                {"subscription_id": sub_id},
                {"_id": 0},
                sort=[("created_at", -1)],
            )
        except Exception:
            invoice = None
        amt = (invoice or {}).get("amount_cents")
        variables["amount_friendly"] = _money(amt) or "—"
        variables["invoice_ref"] = (invoice or {}).get("stripe_invoice_id") or "—"
        ts_field = "paid_at" if event_key == "payment_succeeded" else "payment_failed_at"
        variables["paid_at_friendly"] = _friendly_date((invoice or {}).get(ts_field))
        variables["next_renewal_friendly"] = _friendly_date(sub.get("current_period_end"))

    return variables
