"""routes/admin_portal/reports.py — Phase Admin-7A.2a per-surface
split of the Admin-7B Reports endpoints.

Behaviour is byte-identical to the previous in-`portal.py` block —
this file simply lifts the 4 GET routes (`/reports/usage`,
`/reports/subscriptions`, `/reports/facilities`, `/reports/export.csv`)
into a dedicated module that `portal.py::build_router` calls via
`register(router, ctx)`.

Locked Admin-7B founder decisions (still binding):
  1. Reports readable by all 5 platform roles.
  1. CSV export gated tighter — `support_admin` may read reports but
     may NOT export (REPORTS_CSV_ROLES below excludes them).
  6. Windows: 7d / 30d / 90d only.
  7. CSV: one endpoint, `text/csv`, Stripe-shaped values scrubbed via
     `_scrub_text` before serialization.

Role constants are intentionally at MODULE LEVEL so the source-level
drift guard test (`test_admin_portal_admin7a2.py`) can import them
directly and compare against the frontend mirror in
`permissions.js::ADMIN_REPORTS_CSV_ROLES`.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import Depends, HTTPException, Query, Request
from fastapi.responses import Response

from core import audit
from core.permissions import platform_role, require_platform_role

from ._helpers import _scrub_text


# ----------------------------------------------------------------------
# Module-level constants — promoted from build_router closure scope so
# drift-guard tests can `from .reports import REPORTS_CSV_ROLES`.
# ----------------------------------------------------------------------
REPORTS_READ_ROLES = {
    "super_admin", "platform_admin", "support_admin",
    "billing_admin", "read_only_auditor",
}
# Decision 1: support_admin may read reports but may NOT export CSV.
REPORTS_CSV_ROLES = {
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
}

REPORTS_WINDOWS = {"7d": 7, "30d": 30, "90d": 90}
REPORTS_CSV_TYPES = {"users", "facilities", "subscriptions", "usage"}


def _require_reports_read(u: Dict[str, Any]) -> None:
    if platform_role(u) not in REPORTS_READ_ROLES:
        raise HTTPException(403, "Your platform role cannot view reports.")


def _require_reports_csv(u: Dict[str, Any]) -> None:
    if platform_role(u) not in REPORTS_CSV_ROLES:
        raise HTTPException(
            403, "Your platform role cannot export reports."
        )


def _window_days(window: str) -> int:
    days = REPORTS_WINDOWS.get((window or "").strip().lower())
    if days is None:
        raise HTTPException(
            400,
            f"Invalid window. Allowed: {', '.join(REPORTS_WINDOWS.keys())}",
        )
    return days


def register(router, ctx) -> None:
    """Register all Admin-7B Reports routes onto `router` with the
    shared `ctx` (db, get_current_user, logger)."""
    db = ctx.db
    get_current_user = ctx.get_current_user
    logger = ctx.logger

    async def _safe(coro):
        try:
            return await coro
        except Exception:  # pragma: no cover - defensive
            logger.exception("admin.portal.report metric failed")
            return None

    # --- Reports — usage ---------------------------------------------
    @router.get("/admin/portal/reports/usage")
    async def reports_usage(request: Request,
                            window: str = Query(default="30d"),
                            user=Depends(get_current_user)):
        """Usage aggregates over the selected window. Safe counts only;
        no raw documents, no Stripe IDs."""
        require_platform_role(user)
        _require_reports_read(user)
        days = _window_days(window)
        since_iso = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        results = await asyncio.gather(
            _safe(db.users.count_documents({"created_at": {"$gte": since_iso}})),
            _safe(db.barns.count_documents({"created_at": {"$gte": since_iso}})),
            _safe(db.horses.count_documents({"created_at": {"$gte": since_iso}})),
            _safe(db.audit_log.count_documents({"ts": {"$gte": since_iso}})),
            _safe(db.audit_log.count_documents({"ts": {"$gte": since_iso}, "outcome": "denied"})),
            _safe(db.support_tickets.count_documents({"created_at": {"$gte": since_iso}})),
        )
        partial = any(r is None for r in results)

        def _v(idx: int) -> int:
            return int(results[idx]) if results[idx] is not None else 0

        payload = {
            "window": window,
            "window_days": days,
            "new_users": _v(0),
            "new_facilities": _v(1),
            "new_horses": _v(2),
            "audit_events": _v(3),
            "denied_events": _v(4),
            "new_support_tickets": _v(5),
            "_partial": partial,
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }
        await audit.record(
            action="admin.portal.read.reports.usage",
            user=user, request=request,
            resource_type="admin_portal", resource_id="reports.usage",
            outcome="success", status_code=200,
            metadata={"window": window, "partial": partial},
        )
        return payload

    # --- Reports — subscriptions -------------------------------------
    @router.get("/admin/portal/reports/subscriptions")
    async def reports_subscriptions(request: Request,
                                    window: str = Query(default="30d"),
                                    user=Depends(get_current_user)):
        """Subscription distribution snapshot + new-in-window count.
        Safe aggregates only; no Stripe IDs."""
        require_platform_role(user)
        _require_reports_read(user)
        days = _window_days(window)
        since_iso = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        async def _by_status():
            out: Dict[str, int] = {}
            pipeline = [
                {"$group": {"_id": "$status", "n": {"$sum": 1}}},
            ]
            async for row in db.subscriptions.aggregate(pipeline):
                out[str(row.get("_id") or "unknown")] = int(row.get("n") or 0)
            return out

        async def _by_tier():
            out: Dict[str, int] = {}
            pipeline = [
                {"$group": {"_id": "$tier", "n": {"$sum": 1}}},
            ]
            async for row in db.subscriptions.aggregate(pipeline):
                out[str(row.get("_id") or "unknown")] = int(row.get("n") or 0)
            return out

        by_status = await _safe(_by_status()) or {}
        by_tier = await _safe(_by_tier()) or {}
        new_in_window = await _safe(
            db.subscriptions.count_documents({"created_at": {"$gte": since_iso}})
        )
        total = await _safe(db.subscriptions.count_documents({}))
        partial = (new_in_window is None) or (total is None)

        payload = {
            "window": window,
            "window_days": days,
            "total": int(total or 0),
            "new_in_window": int(new_in_window or 0),
            "by_status": by_status,
            "by_tier": by_tier,
            "_partial": partial,
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }
        await audit.record(
            action="admin.portal.read.reports.subscriptions",
            user=user, request=request,
            resource_type="admin_portal", resource_id="reports.subscriptions",
            outcome="success", status_code=200,
            metadata={"window": window, "partial": partial},
        )
        return payload

    # --- Reports — facilities ----------------------------------------
    @router.get("/admin/portal/reports/facilities")
    async def reports_facilities(request: Request,
                                 window: str = Query(default="30d"),
                                 user=Depends(get_current_user)):
        """Facility & horse aggregates. Safe counts only."""
        require_platform_role(user)
        _require_reports_read(user)
        days = _window_days(window)
        since_iso = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        async def _facilities_by_status():
            out: Dict[str, int] = {}
            pipeline = [
                {"$group": {"_id": "$status", "n": {"$sum": 1}}},
            ]
            async for row in db.barns.aggregate(pipeline):
                out[str(row.get("_id") or "active")] = int(row.get("n") or 0)
            return out

        async def _horses_per_facility_summary():
            pipeline = [
                {"$group": {"_id": "$barn_id", "n": {"$sum": 1}}},
            ]
            counts: List[int] = []
            async for row in db.horses.aggregate(pipeline):
                counts.append(int(row.get("n") or 0))
            if not counts:
                return {"facilities_with_horses": 0, "max_horses_at_facility": 0}
            return {
                "facilities_with_horses": len(counts),
                "max_horses_at_facility": max(counts),
            }

        by_status = await _safe(_facilities_by_status()) or {}
        horses_summary = await _safe(_horses_per_facility_summary()) or {}
        total_facilities = await _safe(db.barns.count_documents({}))
        new_facilities = await _safe(
            db.barns.count_documents({"created_at": {"$gte": since_iso}})
        )
        total_horses = await _safe(db.horses.count_documents({}))
        partial = any(v is None for v in (total_facilities, new_facilities, total_horses))

        payload = {
            "window": window,
            "window_days": days,
            "total_facilities": int(total_facilities or 0),
            "new_facilities_in_window": int(new_facilities or 0),
            "total_horses": int(total_horses or 0),
            "facilities_by_status": by_status,
            "horses_summary": horses_summary,
            "_partial": partial,
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }
        await audit.record(
            action="admin.portal.read.reports.facilities",
            user=user, request=request,
            resource_type="admin_portal", resource_id="reports.facilities",
            outcome="success", status_code=200,
            metadata={"window": window, "partial": partial},
        )
        return payload

    # --- Reports — CSV export ----------------------------------------
    @router.get("/admin/portal/reports/export.csv")
    async def reports_export_csv(request: Request,
                                 type: str = Query(...),
                                 window: str = Query(default="30d"),
                                 user=Depends(get_current_user)):
        """CSV export of safe aggregates. Stripe-shaped values are
        scrubbed before serialization. support_admin is denied
        (decision 1)."""
        require_platform_role(user)
        _require_reports_read(user)   # baseline section gate
        _require_reports_csv(user)    # CSV-specific gate
        t = (type or "").strip().lower()
        if t not in REPORTS_CSV_TYPES:
            raise HTTPException(
                400,
                f"Invalid type. Allowed: {', '.join(sorted(REPORTS_CSV_TYPES))}",
            )
        days = _window_days(window)
        since_iso = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        import csv
        import io as _io

        buf = _io.StringIO()
        writer = csv.writer(buf)

        if t == "users":
            writer.writerow(["metric", "value"])
            total = await _safe(db.users.count_documents({})) or 0
            new_in_window = await _safe(
                db.users.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            pending = await _safe(
                db.users.count_documents({"role_status": "pending_review"})
            ) or 0
            writer.writerow(["total_users", int(total)])
            writer.writerow([f"new_users_{window}", int(new_in_window)])
            writer.writerow(["pending_review_users", int(pending)])
            # By role
            pipeline = [{"$group": {"_id": "$role", "n": {"$sum": 1}}}]
            async for row in db.users.aggregate(pipeline):
                role_label = _scrub_text(str(row.get("_id") or "unknown")) or "unknown"
                writer.writerow([f"role_{role_label}", int(row.get("n") or 0)])

        elif t == "facilities":
            writer.writerow(["metric", "value"])
            total = await _safe(db.barns.count_documents({})) or 0
            new_in_window = await _safe(
                db.barns.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            writer.writerow(["total_facilities", int(total)])
            writer.writerow([f"new_facilities_{window}", int(new_in_window)])
            pipeline = [{"$group": {"_id": "$status", "n": {"$sum": 1}}}]
            async for row in db.barns.aggregate(pipeline):
                status_label = _scrub_text(str(row.get("_id") or "active")) or "active"
                writer.writerow([f"status_{status_label}", int(row.get("n") or 0)])

        elif t == "subscriptions":
            writer.writerow(["metric", "value"])
            total = await _safe(db.subscriptions.count_documents({})) or 0
            new_in_window = await _safe(
                db.subscriptions.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            writer.writerow(["total_subscriptions", int(total)])
            writer.writerow([f"new_subscriptions_{window}", int(new_in_window)])
            pipeline = [{"$group": {"_id": "$status", "n": {"$sum": 1}}}]
            async for row in db.subscriptions.aggregate(pipeline):
                # Stripe-shaped value scrub on any stringified field.
                status_label = _scrub_text(str(row.get("_id") or "unknown")) or "unknown"
                writer.writerow([f"status_{status_label}", int(row.get("n") or 0)])
            pipeline = [{"$group": {"_id": "$tier", "n": {"$sum": 1}}}]
            async for row in db.subscriptions.aggregate(pipeline):
                tier_label = _scrub_text(str(row.get("_id") or "unknown")) or "unknown"
                writer.writerow([f"tier_{tier_label}", int(row.get("n") or 0)])

        else:  # usage
            writer.writerow(["metric", "value"])
            new_users = await _safe(
                db.users.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            new_facilities = await _safe(
                db.barns.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            new_horses = await _safe(
                db.horses.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            audit_events = await _safe(
                db.audit_log.count_documents({"ts": {"$gte": since_iso}})
            ) or 0
            denied_events = await _safe(
                db.audit_log.count_documents({"ts": {"$gte": since_iso}, "outcome": "denied"})
            ) or 0
            new_tickets = await _safe(
                db.support_tickets.count_documents({"created_at": {"$gte": since_iso}})
            ) or 0
            for k, v in (
                (f"new_users_{window}", new_users),
                (f"new_facilities_{window}", new_facilities),
                (f"new_horses_{window}", new_horses),
                (f"audit_events_{window}", audit_events),
                (f"denied_events_{window}", denied_events),
                (f"new_support_tickets_{window}", new_tickets),
            ):
                writer.writerow([k, int(v)])

        csv_text = buf.getvalue()
        # Defense-in-depth: scrub Stripe-shaped values from the final
        # CSV body before it leaves the process.
        csv_text = _scrub_text(csv_text) or ""

        await audit.record(
            action="admin.portal.read.reports.export",
            user=user, request=request,
            resource_type="admin_portal",
            resource_id=f"reports.export.{t}",
            outcome="success", status_code=200,
            metadata={"type": t, "window": window, "bytes": len(csv_text)},
        )
        return Response(
            content=csv_text,
            media_type="text/csv",
            headers={
                "Content-Disposition":
                    f'attachment; filename="equinesync-{t}-{window}.csv"'
            },
        )
