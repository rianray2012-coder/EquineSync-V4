"""routes/admin_portal/integrations.py — Phase Admin-7A.2a per-surface
split of the Admin-7B Integrations endpoints.

Behaviour is byte-identical to the previous in-`portal.py` block.

Locked Admin-7B founder decisions (still binding):
  2. Integrations excludes `support_admin`.
  5. Static slugs only — `stripe`, `resend`, `webhooks`, `jobs` —
     never opaque Mongo refs.
  Stripe env contract: `STRIPE_SECRET_KEY` first, `STRIPE_API_KEY`
  compatibility fallback. See `core/stripe_config.py`
  for the Phase 15 source of truth.

Role + slug constants live at MODULE LEVEL so the source-level drift
guard test (`test_admin_portal_admin7a2.py`) can import them directly
and compare against the frontend section-caps mirror.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

from fastapi import Depends, HTTPException, Request

from core import audit
from core.permissions import platform_role, require_platform_role
from core.stripe_config import StripeConfigurationError, resolve_stripe_secret_key


# ----------------------------------------------------------------------
# Module-level constants — promoted from build_router closure scope so
# drift-guard tests can `from .integrations import INTEGRATIONS_READ_ROLES`.
# ----------------------------------------------------------------------
INTEGRATIONS_READ_ROLES = {
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
}
# Static integration slugs (decision 5 — never opaque Mongo refs).
INTEGRATION_SLUGS = ("stripe", "resend", "webhooks", "jobs")


def _require_integrations_read(u: Dict[str, Any]) -> None:
    if platform_role(u) not in INTEGRATIONS_READ_ROLES:
        raise HTTPException(403, "Your platform role cannot view integrations.")


def stripe_configured() -> bool:
    """Mirror the Phase 15 Stripe contract.

    ``STRIPE_SECRET_KEY`` is canonical. ``STRIPE_API_KEY`` is retained as a
    compatibility fallback, but conflicting values are unsafe and are reported
    as not configured.
    """
    try:
        return resolve_stripe_secret_key(require_present=False) is not None
    except StripeConfigurationError:
        return False


def register(router, ctx) -> None:
    db = ctx.db
    get_current_user = ctx.get_current_user
    logger = ctx.logger

    async def _integration_status(slug: str) -> Dict[str, Any]:
        """Compute safe derived status for a static integration slug.
        Never returns secrets, raw env values, webhook URLs, or
        Stripe-shaped IDs."""
        if slug == "stripe":
            configured = stripe_configured()
            # Last successful billing event (timestamp only; no raw IDs).
            last_ok = None
            stale_count = 0
            recent_summaries: List[Dict[str, Any]] = []
            try:
                row = await db.billing_events.find_one(
                    {"processing_status": "processed"},
                    sort=[("event_created_at", -1)],
                    projection={"_id": 0, "event_created_at": 1},
                )
                if row:
                    last_ok = row.get("event_created_at")
                stale_count = await db.billing_events.count_documents({
                    "processing_status": {"$in": [
                        "retry_502", "metadata_missing_retryable",
                    ]},
                })
                # Recent sanitized summaries — count + status only.
                pipeline = [
                    {"$sort": {"event_created_at": -1}},
                    {"$limit": 50},
                    {"$group": {"_id": "$processing_status",
                                 "n": {"$sum": 1}}},
                ]
                async for r in db.billing_events.aggregate(pipeline):
                    recent_summaries.append({
                        "processing_status": str(r.get("_id") or "unknown"),
                        "count": int(r.get("n") or 0),
                    })
            except Exception:
                logger.exception("admin.portal.integration.stripe stats failed")
            return {
                "slug": "stripe",
                "label": "Stripe (Payments)",
                "configured": configured,
                "status_label": "healthy" if (configured and stale_count == 0)
                                 else ("attention" if configured else "not_configured"),
                "last_successful_event_at": last_ok,
                "stale_count": int(stale_count),
                "retry_count": int(stale_count),
                "recent_summaries": recent_summaries,
            }

        if slug == "resend":
            configured = bool(os.environ.get("RESEND_API_KEY"))
            pending_count = 0
            try:
                pending_count = await db.subscriptions.count_documents(
                    {"pending_emails": {"$exists": True, "$ne": []}}
                )
            except Exception:
                logger.exception("admin.portal.integration.resend stats failed")
            return {
                "slug": "resend",
                "label": "Resend (Transactional Email)",
                "configured": configured,
                "status_label": "healthy" if configured else "not_configured",
                "pending_email_count": int(pending_count),
            }

        if slug == "webhooks":
            stale_count = 0
            last_ok = None
            try:
                stale_count = await db.billing_events.count_documents({
                    "processing_status": {"$in": [
                        "retry_502", "metadata_missing_retryable",
                    ]},
                })
                row = await db.billing_events.find_one(
                    {"processing_status": "processed"},
                    sort=[("event_created_at", -1)],
                    projection={"_id": 0, "event_created_at": 1},
                )
                if row:
                    last_ok = row.get("event_created_at")
            except Exception:
                logger.exception("admin.portal.integration.webhooks stats failed")
            return {
                "slug": "webhooks",
                "label": "Inbound Webhooks",
                "configured": True,
                "status_label": "healthy" if stale_count == 0 else "attention",
                "stale_count": int(stale_count),
                "last_successful_event_at": last_ok,
            }

        if slug == "jobs":
            scheduler_enabled = (
                os.environ.get("SCHEDULER_ENABLED") or "true"
            ).strip().lower() in ("1", "true", "yes", "on")
            return {
                "slug": "jobs",
                "label": "Background Jobs",
                "configured": scheduler_enabled,
                "status_label": "healthy" if scheduler_enabled else "disabled",
                "scheduler_enabled": scheduler_enabled,
            }

        raise HTTPException(404, "Unknown integration slug.")

    @router.get("/admin/portal/integrations")
    async def list_integrations(request: Request,
                                user=Depends(get_current_user)):
        require_platform_role(user)
        _require_integrations_read(user)
        items = []
        for slug in INTEGRATION_SLUGS:
            try:
                items.append(await _integration_status(slug))
            except Exception:
                logger.exception("admin.portal.integrations summary failed for %s", slug)
        await audit.record(
            action="admin.portal.read.integrations",
            user=user, request=request,
            resource_type="admin_portal", resource_id="integrations",
            outcome="success", status_code=200,
            metadata={"count": len(items)},
        )
        return {"items": items, "total": len(items)}

    @router.get("/admin/portal/integrations/{slug}")
    async def get_integration_detail(slug: str, request: Request,
                                     user=Depends(get_current_user)):
        require_platform_role(user)
        _require_integrations_read(user)
        s = (slug or "").strip().lower()
        if s not in INTEGRATION_SLUGS:
            raise HTTPException(404, "Unknown integration slug.")
        detail = await _integration_status(s)
        await audit.record(
            action="admin.portal.read.integration_detail",
            user=user, request=request,
            resource_type="admin_portal", resource_id=f"integration:{s}",
            outcome="success", status_code=200,
            metadata={"slug": s},
        )
        return detail
