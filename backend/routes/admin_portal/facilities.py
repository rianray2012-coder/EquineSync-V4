"""routes/admin_portal/facilities.py — Phase Admin-7A.2b per-surface
split of the locked Admin-1..6 surface.

Behaviour is byte-identical to the previous in-`portal.py` block —
this file lifts the route handler(s) (and surface-specific helpers /
constants) into a dedicated module that `portal.py::build_router`
calls via `register(router, ctx)`.

Locked behaviour (no role / route / audit / response changes). The
route map preservation invariant from `test_admin_portal_admin7a.py`
guarantees the surface keeps registering under the same paths +
methods.
"""
from __future__ import annotations

import asyncio
import logging
import re as _re_module
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from core import audit
from core.permissions import (
    PLATFORM_ROLES,
    platform_role,
    require_platform_role,
)

from ._helpers import (
    SECTION_CAPABILITIES,
    _sections_for,
    _ACTIVITY_PREFIXES,
    _ACTIVITY_EXCLUDE_PREFIXES,
    _METADATA_SCRUB_KEYS,
    _redact_stripe_in_string,
    _scrub_metadata,
    _scrub_metadata_value,
    _scrub_text,
    _admin_ref,
    _resolve_admin_ref,
    _attach_admin_ref,
    _strip_keys,
    _FACILITY_MUTABLE_FIELDS,
    _FACILITY_NEVER_EDITABLE,
    _FACILITY_DISABLE_REASON_CATEGORIES,
    _FACILITY_WRITER_ROLES,
    _FACILITY_FIELD_LIMITS,
    _FACILITY_DISABLE_DETAILS_MAX_LEN,
)


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Facility surface constants — promoted to module scope in Admin-7A.2b
# round-2 so source-level drift guards can import them directly.
#
# Locked invariants (carry from Admin-4):
#   - `subscription_id` is in the INTERNAL projection (needed to join
#     subscription details in the detail endpoint) but is STRIPPED
#     before the response crosses the API boundary via
#     `_BARN_RESPONSE_STRIP_KEYS` + `_strip_barn_response()`.
# ----------------------------------------------------------------------
_BARN_SAFE_FIELDS = {
    "_id": 0,
    "id": 1, "name": 1, "address": 1, "phone": 1, "contact_email": 1,
    "timezone": 1, "notes": 1, "status": 1,
    "subscription_tier_code": 1, "subscription_id": 1,
    "subscription_updated_at": 1, "created_at": 1, "updated_at": 1,
}

# These fields are kept in the INTERNAL projection above but stripped
# from the OUTBOUND response — per locked decision 4a, Admin-4 carries
# NO subscription drill-down identifiers across the API boundary.
_BARN_RESPONSE_STRIP_KEYS = ("subscription_id", "subscription_updated_at")


def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user

    # ------------------------------------------------------------------
    # Admin-4 — facility management (READ-ONLY per founder direction)
    # ------------------------------------------------------------------
    #
    # Strict ceiling for Admin-4:
    #   - NO mutations. Every endpoint registered GET only; the
    #     `test_no_mutations_exposed_on_admin4_endpoints` invariant
    #     asserts 401/403/405 on POST/PUT/PATCH/DELETE.
    #   - NO soft-disable yet. Tenancy-layer enforcement lands in
    #     Admin-4b against a separate gated plan.
    #   - Subscription/usage data is SUMMARY-only. No drill-down to
    #     `subscriptions` rows, no Stripe IDs in responses, no link to
    #     `billing_events`. Admin-5 remains the canonical surface.
    #   - NO Phase 9 reads (`invoices`, `recurring_charges` untouched).
    #
    # Documented future-Admin-4b mutable field whitelist (kept here so
    # the reviewer can see the deferred surface; NOT yet implemented):
    #   editable in Admin-4b:  name, address, phone, contact_email,
    #                          timezone, notes, status (via soft-disable)
    #   NEVER editable:        id, created_at, subscription_id,
    #                          subscription_tier_code,
    #                          subscription_entitlements,
    #                          stripe_customer_id,
    #                          subscription_updated_at, anything in
    #                          invoices/recurring_charges (Phase 9),
    #                          anything in subscriptions (Phase 15).

    # `_BARN_SAFE_FIELDS` and `_BARN_RESPONSE_STRIP_KEYS` live at
    # MODULE scope (above) — the closures here resolve them via LEGB.

    def _strip_barn_response(barn: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not isinstance(barn, dict):
            return barn
        return {k: v for k, v in barn.items() if k not in _BARN_RESPONSE_STRIP_KEYS}

    async def _facility_usage_summary(barn_id: str, entitlements: Dict[str, Any]) -> Dict[str, Any]:
        """Derive `{horses_used, horses_limit, users_used, users_limit}`
        for one facility. Limits come from the entitlements snapshot
        (None → unlimited). Counts come from local collections only."""
        try:
            horses_used = await db.horses.count_documents({"barn_id": barn_id})
        except Exception:
            horses_used = 0
        try:
            users_used = await db.users.count_documents({"barn_id": barn_id})
        except Exception:
            users_used = 0
        return {
            "horses_used": horses_used,
            "horses_limit": (entitlements or {}).get("horses"),
            "users_used": users_used,
            "users_limit": (entitlements or {}).get("users"),
        }

    @router.get("/admin/portal/facilities")
    async def list_facilities(
        request: Request,
        q: Optional[str] = Query(default=None, max_length=200),
        tier: Optional[str] = Query(default=None, max_length=32),
        status: Optional[str] = Query(default=None, max_length=32),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Cross-facility roster.

        Per the Admin-1 founder rule, every platform role can list every
        facility. Barn-scoped (non-platform) users are blocked by
        `require_platform_role(user)` — verified by the Admin-4
        cross-facility isolation matrix.
        """
        require_platform_role(user)
        mongo_q: Dict[str, Any] = {}
        if tier:
            mongo_q["subscription_tier_code"] = tier
        if status:
            mongo_q["status"] = status
        if q:
            import re as _re
            safe = _re.escape(q)
            mongo_q["name"] = {"$regex": safe, "$options": "i"}

        total = await db.barns.count_documents(mongo_q)
        items = await db.barns.find(mongo_q, _BARN_SAFE_FIELDS).sort("created_at", -1).skip(cursor).limit(limit).to_list(length=limit)

        # Attach a tiny summary per row (counts + sub status). Done with
        # asyncio.gather to keep the list snappy for ~25 rows.
        async def _augment(barn: Dict[str, Any]) -> Dict[str, Any]:
            sub = None
            sub_id = barn.get("subscription_id")
            if sub_id:
                sub = await db.subscriptions.find_one(
                    {"id": sub_id},
                    {"_id": 0, "status": 1, "amount_cents": 1, "plan_tier_code": 1,
                     "entitlements_snapshot": 1},
                )
            usage = await _facility_usage_summary(
                barn["id"],
                (sub or {}).get("entitlements_snapshot") or {},
            )
            # Strip internal-only keys (subscription_id, subscription_updated_at)
            # before the row crosses the API boundary — decision 4a.
            return {
                **_strip_barn_response(barn),
                "subscription_status": (sub or {}).get("status"),
                "usage": usage,
            }

        augmented = await asyncio.gather(*[_augment(b) for b in items])
        next_cursor = cursor + len(augmented) if (cursor + len(augmented)) < total else None

        await audit.record(
            action="admin.portal.read.facilities",
            user=user, request=request,
            resource_type="admin_portal", resource_id="facilities",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(augmented)},
        )
        return {"items": augmented, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/facilities/{barn_id}")
    async def get_facility_detail(barn_id: str, request: Request,
                                  user=Depends(get_current_user)):
        """Per-facility health page (read-only).

        Returns: barn safe profile, subscription SUMMARY (no Stripe IDs),
        usage vs limits, count tiles, recent admin activity for this
        barn. No drill-down — Admin-5 owns subscription/billing detail.
        """
        require_platform_role(user)
        barn = await db.barns.find_one({"id": barn_id}, _BARN_SAFE_FIELDS)
        if not barn:
            raise HTTPException(404, "Facility not found.")

        # Subscription SUMMARY — strict whitelist; NO Stripe IDs.
        sub_summary = None
        sub_id = barn.get("subscription_id")
        if sub_id:
            raw_sub = await db.subscriptions.find_one(
                {"id": sub_id},
                {"_id": 0, "plan_tier_code": 1, "status": 1, "billing_cycle": 1,
                 "current_period_end": 1, "trial_end": 1, "amount_cents": 1,
                 "entitlements_snapshot": 1, "updated_at": 1},
            )
            if raw_sub:
                sub_summary = {
                    "plan_tier_code": raw_sub.get("plan_tier_code"),
                    "status": raw_sub.get("status"),
                    "billing_cycle": raw_sub.get("billing_cycle"),
                    "current_period_end": raw_sub.get("current_period_end"),
                    "trial_end": raw_sub.get("trial_end"),
                    "amount_cents": raw_sub.get("amount_cents") or 0,
                    "updated_at": raw_sub.get("updated_at"),
                }

        usage = {"horses_used": 0, "horses_limit": None,
                 "users_used": 0, "users_limit": None}
        # Recompute usage with the raw entitlements snapshot (the summary
        # intentionally doesn't carry it back to the client).
        entitlements_for_usage = {}
        if sub_id:
            row = await db.subscriptions.find_one(
                {"id": sub_id}, {"_id": 0, "entitlements_snapshot": 1},
            )
            entitlements_for_usage = (row or {}).get("entitlements_snapshot") or {}
        usage = await _facility_usage_summary(barn_id, entitlements_for_usage)

        # Recent admin activity for this barn (curated, scrubbed).
        try:
            recent_audit = await db.audit_log.find(
                {"barn_id": barn_id},
                {"_id": 0, "id": 1, "ts": 1, "action": 1, "actor_email": 1,
                 "resource_type": 1, "resource_id": 1, "outcome": 1, "metadata": 1},
            ).sort("ts", -1).limit(10).to_list(length=10)
            for row in recent_audit:
                row["metadata"] = _scrub_metadata(row.get("metadata"))
        except Exception:
            recent_audit = []

        await audit.record(
            action="admin.portal.read.facility_detail",
            user=user, request=request,
            resource_type="facility", resource_id=barn_id,
            outcome="success", status_code=200,
        )
        return {
            "barn": _strip_barn_response(barn),
            "subscription_summary": sub_summary,
            "usage": usage,
            "counts": {
                "users": usage["users_used"],
                "horses": usage["horses_used"],
            },
            "recent_activity": recent_audit,
        }

    # ==================================================================
    # Phase Admin-4b — facility mutations (PATCH / disable / reenable).
    #
    # Strict ceiling:
    #   - Only `super_admin` + `platform_admin` may mutate. Every other
    #     platform_role + every barn-scoped role receives a 403.
    #   - Mutable whitelist is `_FACILITY_MUTABLE_FIELDS` only. Any other
    #     field in the request body → 422.
    #   - Soft-disable only. No hard deletes are introduced.
    #   - Tenancy-layer enforcement (block disabled-facility members from
    #     product routes) is implemented in `core/tenancy.make_require_active_facility`
    #     and wired in `server.py`. See PHASE_ADMIN_4B_README.md inventory.
    #   - Phase 9 (invoices, recurring_charges) and Phase 15
    #     (subscriptions, webhooks) collections are NEVER mutated by
    #     these endpoints — only `barns` is touched.
    # ==================================================================

    def _require_facility_writer(user):
        """Mutation gate: must be `super_admin` or `platform_admin`.
        Falls back to the generic 403 surfaced by `require_platform_role`
        for non-platform users, then layers a tighter writer-role check
        on top — the response detail stays generic to avoid leaking the
        permission matrix to non-writers."""
        require_platform_role(user)
        if platform_role(user) not in _FACILITY_WRITER_ROLES:
            raise HTTPException(403, "Insufficient platform role.")

    def _validate_facility_patch(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalise a PATCH body. Returns the trimmed,
        whitelisted updates dict. Any unknown/disallowed field → 422.
        Length + format rules per `_FACILITY_FIELD_LIMITS`."""
        if not isinstance(payload, dict) or not payload:
            raise HTTPException(422, "Empty request body.")

        unknown = [k for k in payload.keys() if k not in _FACILITY_MUTABLE_FIELDS]
        if unknown:
            # Single, generic message — never reveal whether the
            # unknown key was a Stripe/billing field vs a typo.
            raise HTTPException(
                422,
                f"Field not editable: {sorted(unknown)[0]!r}",
            )

        # Optional timezone strict-IANA validation (fail closed when
        # `zoneinfo` is unavailable — per founder decision 7).
        tz_set: Optional[Set[str]] = None
        try:
            from zoneinfo import available_timezones  # py3.9+
            tz_set = set(available_timezones())
            if not tz_set:
                tz_set = None
        except Exception:
            tz_set = None

        updates: Dict[str, Any] = {}
        for field in _FACILITY_MUTABLE_FIELDS:
            if field not in payload:
                continue
            raw = payload[field]
            if not isinstance(raw, str):
                raise HTTPException(422, f"Field {field!r} must be a string.")
            v = raw.strip()
            lo, hi = _FACILITY_FIELD_LIMITS[field]
            if len(v) < lo:
                raise HTTPException(422, f"Field {field!r} is too short.")
            if len(v) > hi:
                raise HTTPException(422, f"Field {field!r} is too long.")
            if field == "contact_email" and v:
                # Permissive email pattern — defence-in-depth, not
                # marketing-grade. Existing user signup uses the same.
                if not _re_module.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
                    raise HTTPException(422, "Invalid email format.")
            if field == "timezone":
                if tz_set is None:
                    raise HTTPException(
                        422,
                        "Timezone validation is unavailable on this runtime; "
                        "cannot accept timezone updates safely.",
                    )
                if v not in tz_set:
                    raise HTTPException(422, "Unknown IANA timezone.")
            updates[field] = v
        if not updates:
            raise HTTPException(422, "Empty request body.")
        return updates

    @router.patch("/admin/portal/facilities/{barn_id}")
    async def patch_facility(barn_id: str, request: Request,
                             user=Depends(get_current_user)):
        """Apply a whitelisted profile edit to a facility.

        Allowed fields: name, address, phone, contact_email, timezone, notes.
        Any other field → 422. Never touches subscription / Stripe /
        Phase 9 / Phase 15 fields. Per founder decision 9, the audit row
        records only `changed_fields` — never raw before/after values.
        """
        _require_facility_writer(user)

        try:
            payload = await request.json()
        except Exception:
            raise HTTPException(422, "Invalid JSON body.")

        # Hard reject of any never-editable keys before whitelist check —
        # the validator already rejects, but this gives a more precise
        # error for the most dangerous fields (subscription_id, Stripe,
        # Phase 9/15) without exposing them to enumeration.
        bad_priv = [
            k for k in (payload or {}).keys() if k in _FACILITY_NEVER_EDITABLE
        ]
        if bad_priv:
            raise HTTPException(422, f"Field not editable: {bad_priv[0]!r}")

        updates = _validate_facility_patch(payload)

        barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "id": 1})
        if not barn:
            raise HTTPException(404, "Facility not found.")

        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.barns.update_one({"id": barn_id}, {"$set": updates})

        # Audit — record CHANGED FIELDS ONLY (founder decision 9).
        await audit.record(
            action="admin.facility.updated",
            user=user, request=request,
            resource_type="facility", resource_id=barn_id,
            outcome="success", status_code=200,
            metadata={
                "barn_id": barn_id,
                "changed_fields": sorted(k for k in updates if k != "updated_at"),
                "actor_role": platform_role(user),
            },
        )

        # Return the freshly-projected safe view (no Stripe IDs).
        refreshed = await db.barns.find_one(
            {"id": barn_id}, _BARN_SAFE_FIELDS,
        )
        return {"barn": _strip_barn_response(refreshed)}

    @router.post("/admin/portal/facilities/{barn_id}/disable")
    async def disable_facility(barn_id: str, request: Request,
                               user=Depends(get_current_user)):
        """Soft-disable a facility.

        Body: `{"reason_category": "<one of _FACILITY_DISABLE_REASON_CATEGORIES>",
                 "reason_details": "<optional, max 200 chars>"}`.
        Re-running on an already-disabled facility → 409.
        """
        _require_facility_writer(user)

        try:
            payload = await request.json()
        except Exception:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}

        category = (payload.get("reason_category") or "").strip()
        if category not in _FACILITY_DISABLE_REASON_CATEGORIES:
            raise HTTPException(
                422,
                "reason_category must be one of: "
                + ", ".join(sorted(_FACILITY_DISABLE_REASON_CATEGORIES)),
            )
        details_raw = payload.get("reason_details") or ""
        if not isinstance(details_raw, str):
            raise HTTPException(422, "reason_details must be a string.")
        details = details_raw.strip()
        if len(details) > _FACILITY_DISABLE_DETAILS_MAX_LEN:
            raise HTTPException(
                422,
                f"reason_details exceeds {_FACILITY_DISABLE_DETAILS_MAX_LEN} chars.",
            )

        barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "id": 1, "status": 1})
        if not barn:
            raise HTTPException(404, "Facility not found.")
        if (barn.get("status") or "").strip().lower() == "disabled":
            raise HTTPException(409, "Facility already disabled.")

        now_iso = datetime.now(timezone.utc).isoformat()
        update_doc: Dict[str, Any] = {
            "status": "disabled",
            "disabled_at": now_iso,
            "disabled_by": user.get("id"),
            "disabled_reason": category,
            "updated_at": now_iso,
        }
        # Only persist free-text details on the barn doc when supplied —
        # founder decision 4b allows operator context but it must not
        # cross the audit boundary.
        if details:
            update_doc["disabled_reason_details"] = details
        else:
            # Always set the field (cleared on re-enable) for predictability.
            update_doc["disabled_reason_details"] = ""

        await db.barns.update_one({"id": barn_id}, {"$set": update_doc})

        await audit.record(
            action="admin.facility.disabled",
            user=user, request=request,
            resource_type="facility", resource_id=barn_id,
            outcome="success", status_code=200,
            metadata={
                "barn_id": barn_id,
                "reason_category": category,
                "reason_provided": bool(details),
                "actor_role": platform_role(user),
            },
        )
        return {"ok": True, "barn_id": barn_id, "status": "disabled"}

    @router.post("/admin/portal/facilities/{barn_id}/reenable")
    async def reenable_facility(barn_id: str, request: Request,
                                user=Depends(get_current_user)):
        """Re-enable a previously soft-disabled facility.

        Sets `status="active"`, clears `disabled_reason` /
        `disabled_reason_details`, and records `reenabled_at` /
        `reenabled_by`. Historical `disabled_at` / `disabled_by` are
        preserved for audit context. Re-running on an active facility
        → 409.
        """
        _require_facility_writer(user)

        barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "id": 1, "status": 1})
        if not barn:
            raise HTTPException(404, "Facility not found.")
        if (barn.get("status") or "").strip().lower() != "disabled":
            raise HTTPException(409, "Facility is not disabled.")

        now_iso = datetime.now(timezone.utc).isoformat()
        await db.barns.update_one(
            {"id": barn_id},
            {"$set": {
                "status": "active",
                "reenabled_at": now_iso,
                "reenabled_by": user.get("id"),
                "disabled_reason": "",
                "disabled_reason_details": "",
                "updated_at": now_iso,
            }},
        )

        await audit.record(
            action="admin.facility.reenabled",
            user=user, request=request,
            resource_type="facility", resource_id=barn_id,
            outcome="success", status_code=200,
            metadata={
                "barn_id": barn_id,
                "actor_role": platform_role(user),
            },
        )
        return {"ok": True, "barn_id": barn_id, "status": "active"}

