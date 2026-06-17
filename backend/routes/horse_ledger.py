"""routes/horse_ledger.py — Phase HorseOps-1A.

The Horse Ledger (compact UI label: "Care Ledger") — a composed read-only
view of a horse's operational profile. This module is the FIRST surface
of the HorseOps phase tree.

1-A SCOPE (LOCKED):
  * 1 endpoint only: GET /api/horse-ledger/{horse_id}
  * READ ONLY — no writes to any collection.
  * Composes from existing `horses` + care/health collections.
  * 8 new collections (`horse_care_profiles`, `horse_equipment`,
    `service_providers`, `horse_provider_assignments`,
    `horse_daily_check_logs`, `horse_ledger_alerts`,
    `horse_owner_visibility_policy`, `horse_ledger_audit`) are read
    from when present; absent rows yield safe-empty sub-sections.
  * Role-driven response shape (fail-closed):
      - user.role == "horse_owner"  → ALWAYS owner-filtered shape,
        no query string can escalate.
      - Other barn-scoped roles in the same barn → full staff/manager shape.
      - Cross-barn caller (any role, incl. platform admins) → 404.
  * Disabled-facility enforcement comes from `PRODUCT_FACILITY_DEPS` at
    the `include_router(...)` site in `server.py`. Platform admins
    bypass per Admin-4b R1-C semantics; barn scoping is NOT bypassed
    by this product route.
  * No Stripe-shaped substring may leak in any string value. The
    `_redact_stripe_in_string` helper from Admin-4b R1-B runs on every
    outbound string.

OUT OF SCOPE for 1-A (lands in 1-B..1-E):
  * Edits, drawer UIs, mutation endpoints.
  * Daily-check writes, hay-net refills, bedding logs.
  * Alerts worker, escalations.
  * Owner request-more-visibility flow.
  * Cross-facility platform Ledger inspection (deferred to a future
    Admin Portal surface; NOT this product route).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from core.tenancy import barn_filter, resolve_barn_id
from routes.admin_portal._helpers import _redact_stripe_in_string


# ---------------------------------------------------------------------
# Owner-visibility defaults (hardcoded for 1-A; per-barn templates land
# in a later phase). Per founder direction: fail-closed / conservative.
# ---------------------------------------------------------------------
_OWNER_VISIBLE_SECTIONS = frozenset({
    # Visible — public-facing or owner-relevant.
    "identity_public",
    "feeding_summary",
    "supplements_names_only",
    "hay_summary",
    "turnout_summary",
    "riding_training",
    "equipment",
    "service_providers",
    "health_owner_safe",
    # Hidden by default in 1-A:
    #   identity_private (microchip / tattoo / registry / required_staff_experience)
    #   feeding_full / hay_full / handling_behavior / stall_bedding
    #   daily_checks_recent / alerts_open / audit_recent
})


def _scrub_strings(obj: Any) -> Any:
    """Recursively run `_redact_stripe_in_string` on every string in
    nested dicts/lists. Reuses the Admin-4b R1-B primitive so a
    Stripe-shaped substring pasted into a free-text horse field can
    never leak through this read endpoint."""
    if isinstance(obj, str):
        return _redact_stripe_in_string(obj)
    if isinstance(obj, dict):
        return {k: _scrub_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub_strings(v) for v in obj]
    return obj


def _legacy_envelope(structured: Any, legacy: Any) -> Optional[Dict[str, Any]]:
    """Compose the locked envelope shape when a section MAY carry both
    a structured value (from `horse_care_profiles`) and a legacy value
    (from the original `horses` doc). One side may be `None`."""
    has_struct = structured not in (None, {}, [])
    has_legacy = legacy not in (None, "", [])
    if not has_struct and not has_legacy:
        return None
    return {"structured": structured if has_struct else None,
            "legacy":     legacy     if has_legacy else None}


# ---------------------------------------------------------------------
# Section builders. Pure functions — no DB writes, no mutation of args.
# ---------------------------------------------------------------------
def _build_identity(horse: Dict[str, Any], owner_view: bool) -> Dict[str, Any]:
    """Identity section. Microchip/tattoo/registry numbers and the
    required-staff-experience field are operator-private and hidden
    in the owner view (founder decision §3.8)."""
    public = {
        "id":              horse.get("id"),
        "barn_id":         horse.get("barn_id"),
        "name":            horse.get("name"),
        "barn_name":       horse.get("barn_name"),
        "breed":           horse.get("breed"),
        "age":             horse.get("age"),
        "dob":             horse.get("dob"),
        "color":           horse.get("color"),
        "height_hands":    horse.get("height_hands"),
        "discipline":      horse.get("discipline"),
        "sex":             horse.get("sex"),
        "markings":        horse.get("markings"),
        "photo_url":       horse.get("photo_url"),
        "registered_name": horse.get("registered_name"),
        "show_name":       horse.get("show_name"),
        "stall":           horse.get("stall"),
        "status":          horse.get("status"),
        "ownership_structure": horse.get("ownership_structure"),
        "primary_owner_id":    horse.get("primary_owner_id") or horse.get("owner_id"),
    }
    if owner_view:
        return public
    return {
        **public,
        "microchip_number":  horse.get("microchip_number"),
        "tattoo_number":     horse.get("tattoo_number"),
        "registry_numbers":  horse.get("registry_numbers") or [],
        "secondary_owner_ids": horse.get("secondary_owner_ids") or [],
        "emergency_contact_ids": horse.get("emergency_contact_ids") or [],
        "document_ids":      horse.get("document_ids") or [],
        "required_staff_experience_level": horse.get("required_staff_experience_level"),
        "ledger_initialized_at": horse.get("ledger_initialized_at"),
    }


def _build_feeding(horse: Dict[str, Any], profile: Optional[Dict[str, Any]],
                   owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("feeding")
    legacy_str = horse.get("feed_plan")
    envelope = _legacy_envelope(structured, legacy_str)
    if envelope is None:
        return None
    if not owner_view:
        return envelope
    # Owner-filtered feeding.
    #
    # Codex round-1 P1: the legacy `horses.feed_plan` field is FREE TEXT
    # and may contain prep instructions, soaking details, medication
    # notes, or staff-only handling warnings. It must NOT be surfaced
    # raw to owners. The owner view exposes ONLY a conservative
    # structured projection: feed type + schedule + supplement names.
    # If no structured profile exists yet, the owner sees `feeding: null`
    # — they will see real feeding info once a manager populates the
    # structured profile in 1-B.
    if not structured:
        return None
    safe_struct = {
        "grain_feed_type": structured.get("grain_feed_type"),
        "schedule":        structured.get("schedule") or [],
        "supplements":     [
            {"name": s.get("name")} for s in (structured.get("supplements") or [])
            if isinstance(s, dict)
        ],
    }
    # legacy is intentionally DROPPED in the owner envelope to avoid
    # surfacing free-text staff notes.
    return {"structured": safe_struct, "legacy": None}


def _build_hay_access(profile: Optional[Dict[str, Any]],
                      owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("hay_access")
    if not structured:
        return None
    if not owner_view:
        return {"structured": structured, "legacy": None}
    # Owner-filtered: type + frequency surface; restriction flags,
    # staff-only warnings, and all hay-net operational state hidden.
    safe = {
        "access_type":           structured.get("access_type"),
        "hay_type":              structured.get("hay_type"),
        "quantity_per_feeding":  structured.get("quantity_per_feeding"),
    }
    return {"structured": safe, "legacy": None}


def _build_stall_bedding(profile: Optional[Dict[str, Any]],
                         owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("stall_bedding")
    if not structured:
        return None
    if owner_view:
        # Entire bedding section is operations-only (founder decision).
        return None
    return {"structured": structured, "legacy": None}


def _build_turnout(horse: Dict[str, Any], profile: Optional[Dict[str, Any]],
                   owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("turnout")
    legacy_group = horse.get("turnout_group")
    envelope = _legacy_envelope(structured, legacy_group)
    if envelope is None:
        return None
    if not owner_view:
        return envelope
    # Owner-filtered: schedule + group only; avoid list / injury risk
    # notes / catching notes hidden.
    safe_struct: Optional[Dict[str, Any]] = None
    if structured:
        safe_struct = {
            "schedule":                  structured.get("schedule") or [],
            "pasture_paddock_assignment": structured.get("pasture_paddock_assignment"),
            "turnout_group":             structured.get("turnout_group"),
        }
    return _legacy_envelope(safe_struct, legacy_group)


def _build_handling_behavior(horse: Dict[str, Any],
                             profile: Optional[Dict[str, Any]],
                             owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("handling_behavior")
    legacy_flags = horse.get("behavior_flags") or []
    if owner_view:
        # ENTIRE section is staff-only — never surface to owners.
        return None
    return _legacy_envelope(structured, legacy_flags)


def _build_riding_training(horse: Dict[str, Any],
                           profile: Optional[Dict[str, Any]],
                           owner_view: bool) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("riding_training")
    legacy_goals = horse.get("training_goals")
    return _legacy_envelope(structured, legacy_goals)


def _build_equipment_summary(equipment_rows: List[Dict[str, Any]],
                             owner_view: bool) -> List[Dict[str, Any]]:
    """Equipment list. In 1-A this is always empty because
    `horse_equipment` is not written until 1-B; the index exists, the
    collection is queryable, but no rows are present yet."""
    if owner_view:
        return [
            {"category": r.get("category"), "label": r.get("label")}
            for r in equipment_rows if r.get("status") != "retired"
        ]
    return list(equipment_rows)


def _build_health(meds: List[Dict[str, Any]],
                  med_logs: List[Dict[str, Any]],
                  vet_records: List[Dict[str, Any]],
                  injuries: List[Dict[str, Any]],
                  wellness: List[Dict[str, Any]],
                  legacy_allergies: Optional[List[str]],
                  owner_view: bool) -> Dict[str, Any]:
    if owner_view:
        # Owner-safe projection. Each sub-field is an EXPLICIT allowlist
        # — never a whole document. Codex round-1 P1: previously
        # `wellness[0]` was returned raw, which can leak staff notes,
        # actor fields, internal observations. We now project to a
        # fixed set of safe display fields.
        wellness_safe: Optional[Dict[str, Any]] = None
        if wellness:
            w = wellness[0] or {}
            wellness_safe = {
                "id":         w.get("id"),
                "created_at": w.get("created_at"),
                "status":     w.get("status"),
                "score":      w.get("score"),
                "summary":    w.get("summary"),     # owner-safe display string if present
            }
        return {
            "medications": [
                {"id": m.get("id"), "name": m.get("name"),
                 "dosage": m.get("dosage"), "frequency": m.get("frequency")}
                for m in meds
            ],
            "vet_records_recent": [
                {"id": v.get("id"), "title": v.get("title"),
                 "date": v.get("date")}
                for v in vet_records
            ],
            "injuries_active": [
                {"id": i.get("id"), "title": i.get("title"),
                 "status": i.get("status")}
                for i in injuries
            ],
            "wellness_latest": wellness_safe,
            "allergies_legacy": legacy_allergies or [],
        }
    return {
        "medications":         list(meds),
        "medication_logs_30d": list(med_logs),
        "vet_records_recent":  list(vet_records),
        "injuries_active":     list(injuries),
        "wellness_latest":     wellness[0] if wellness else None,
        "allergies_legacy":    legacy_allergies or [],
    }


# ---------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------
def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(tags=["horse_ledger"])

    @router.get("/horse-ledger/{horse_id}")
    async def get_horse_ledger(
        horse_id: str,
        user=Depends(get_current_user),
    ) -> Dict[str, Any]:
        """Composed read-only Ledger view.

        Response shape is decided server-side by `user.role` +
        ownership + barn scoping. The `?view=` query string is
        intentionally NOT read here — it would be a display hint at
        most. See Δ1 / Δ4 of the locked HorseOps-1A plan.
        """
        # ---- Barn scoping (NO platform-role bypass on this route) ----
        # Use barn_filter() so a cross-barn id returns 404 rather than
        # leaking existence. This is the same primitive horses.py uses
        # and is intentionally identical to keep the surface boring.
        horse = await db.horses.find_one(
            barn_filter(user, {"id": horse_id}), {"_id": 0},
        )
        if not horse:
            raise HTTPException(404, "Horse not found")

        # ---- Role branch (fail-closed) ----
        # If user.role == "horse_owner", the response MUST be the
        # owner-filtered shape regardless of any query string the
        # client may have sent. A horse_owner who is not in the
        # ownership set 404s — never a 403 (which would leak existence).
        owner_view = False
        if (user.get("role") or "").strip().lower() == "horse_owner":
            primary = horse.get("primary_owner_id") or horse.get("owner_id")
            secondary = horse.get("secondary_owner_ids") or []
            uid = user.get("id")
            if uid != primary and uid not in secondary:
                raise HTTPException(404, "Horse not found")
            owner_view = True

        # ---- Read side composition (NO writes) ----
        profile = await db.horse_care_profiles.find_one(
            {"horse_id": horse_id}, {"_id": 0},
        )
        # In 1-A, horse_equipment, service_providers, daily_check_logs,
        # alerts, and audit are queryable but empty by definition (no
        # 1-A writer exists). We still issue the reads so the response
        # shape is identical from day-one.
        equipment_rows = [
            r async for r in db.horse_equipment.find(
                {"horse_id": horse_id, "status": {"$ne": "retired"}},
                {"_id": 0},
            )
        ]
        provider_rows = [
            r async for r in db.horse_provider_assignments.find(
                {"horse_id": horse_id}, {"_id": 0},
            ).sort("next_due_date", 1)
        ]

        # Existing care/health collections.
        meds = [
            m async for m in db.medications.find(
                {"horse_id": horse_id}, {"_id": 0},
            )
        ]
        med_logs = [
            m async for m in db.medication_logs.find(
                {"horse_id": horse_id}, {"_id": 0},
            ).sort("created_at", -1).limit(50)
        ]
        vet_records = [
            v async for v in db.vet_records.find(
                {"horse_id": horse_id}, {"_id": 0},
            ).sort("date", -1).limit(20)
        ]
        injuries = [
            i async for i in db.injuries.find(
                {"horse_id": horse_id, "status": {"$ne": "resolved"}},
                {"_id": 0},
            )
        ]
        wellness = [
            w async for w in db.wellness.find(
                {"horse_id": horse_id}, {"_id": 0},
            ).sort("created_at", -1).limit(10)
        ]

        response: Dict[str, Any] = {
            "horse_id":     horse_id,
            "view":         "owner" if owner_view else "staff",
            "section_capabilities_version": "1a",

            "identity":         _build_identity(horse, owner_view),
            "feeding":          _build_feeding(horse, profile, owner_view),
            "hay_access":       _build_hay_access(profile, owner_view),
            "stall_bedding":    _build_stall_bedding(profile, owner_view),
            "turnout":          _build_turnout(horse, profile, owner_view),
            "handling_behavior": _build_handling_behavior(horse, profile, owner_view),
            "riding_training":  _build_riding_training(horse, profile, owner_view),

            "equipment":        _build_equipment_summary(equipment_rows, owner_view),
            "service_providers": [] if owner_view else list(provider_rows),

            "health":           _build_health(
                                    meds, med_logs, vet_records,
                                    injuries, wellness,
                                    horse.get("allergies"),
                                    owner_view,
                                ),

            # 1-A: these arrive in later sub-phases. Always empty by
            # construction so the frontend can render placeholders.
            "daily_checks_recent": [],
            "alerts_open":         [],
            "audit_recent":        [],
        }

        # Final defense-in-depth scrub for Stripe-shaped substrings
        # (R1-B parity) on every string in the response.
        return _scrub_strings(response)

    return router
