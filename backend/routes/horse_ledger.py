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

from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from core.provider_access import service_provider_user_exists
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


# ---------------------------------------------------------------------
# Owner-safe key registry (Phase 1-B Round-1 fix).
#
# The READ path is backend-authoritative. The effective owner allowlist
# per section is computed as:
#     (policy_allowlist ∩ _OWNER_SAFE_KEYS[section]) ∪ _DEFAULT_OWNER_POLICY[section]
#         minus  any FORBIDDEN owner key (incl. underscore-prefixed)
#
# `_OWNER_SAFE_KEYS` is the *universe* of keys a manager could ever
# expose to an owner for a given section. Anything not in this set is
# treated as staff-only on read, regardless of what the policy doc
# says. This is defense-in-depth: even a stale or tampered policy doc
# cannot surface keys the registry doesn't bless.
#
# `_DEFAULT_OWNER_POLICY` is the conservative fail-closed default
# applied when no policy doc exists for the horse.
# ---------------------------------------------------------------------
_OWNER_SAFE_KEYS: Dict[str, frozenset] = {
    "feeding": frozenset({
        "grain_feed_type", "schedule", "supplements",
        "amount_value", "amount_unit",
    }),
    "hay_access": frozenset({
        "access_type", "hay_type", "quantity_per_feeding",
        "quantity_value", "quantity_unit",
    }),
    "turnout": frozenset({
        "schedule", "pasture_paddock_assignment", "turnout_group",
        "buddies", "required_apparel",
    }),
    "riding_training": frozenset({
        "discipline", "current_level", "competition_goals",
        "goals_short_term", "goals_long_term",
    }),
    "equipment": frozenset({"category", "label"}),
    # Sections explicitly NOT exposable to owners under any policy:
    #   stall_bedding, handling_behavior, service_providers
}

_DEFAULT_OWNER_POLICY: Dict[str, frozenset] = {
    "feeding":         frozenset({"grain_feed_type", "schedule", "supplements"}),
    "hay_access":      frozenset({"access_type", "hay_type", "quantity_per_feeding"}),
    "turnout":         frozenset({"schedule", "pasture_paddock_assignment", "turnout_group"}),
    "riding_training": frozenset({"discipline", "current_level", "competition_goals"}),
    "equipment":       frozenset({"category", "label"}),
}


def _effective_owner_keys(section: str,
                          policy_doc: Optional[Dict[str, Any]]) -> set:
    """Return the effective owner-visible key set for a section.

    Intersects the policy's allowlist with the backend safe-key
    registry. If the policy doc is missing OR has no entry for this
    section, the conservative default is used (fail-closed)."""
    safe = _OWNER_SAFE_KEYS.get(section, frozenset())
    if not safe:
        return set()
    default = _DEFAULT_OWNER_POLICY.get(section, frozenset())
    if policy_doc is None:
        return set(default)
    sections = (policy_doc or {}).get("sections") or {}
    spec = sections.get(section)
    if not isinstance(spec, dict):
        return set(default)
    allow_raw = spec.get("allowlist")
    if not isinstance(allow_raw, list):
        return set(default)
    # Filter to safe keys AND drop underscore-prefixed / non-strings.
    cleaned = {k for k in allow_raw if isinstance(k, str) and not k.startswith("_")}
    return cleaned & safe


def _project_supplements(supplements: Any) -> List[Dict[str, Any]]:
    """Owner-safe supplement projection: name-only, no dosage/notes."""
    if not isinstance(supplements, list):
        return []
    out = []
    for s in supplements:
        if isinstance(s, dict) and s.get("name"):
            out.append({"name": s["name"]})
        elif isinstance(s, str):
            out.append({"name": s})
    return out


# Round-2 P0: schedule subkeys are restricted to a tiny, owner-safe
# registry per section. Both the read projection AND the PATCH
# validator use this registry — at write time we 422 on unknown subkeys
# so a staff note keyed `staff_note` (or anything else) never even
# lands in the DB. The read projection then strips any unknown subkey
# as defense-in-depth in case a doc was hand-planted.
_SCHEDULE_SUBKEYS: Dict[str, frozenset] = {
    "feeding": frozenset({"time", "label", "amount"}),
    "turnout": frozenset({"time", "label", "duration", "paddock"}),
}


def _project_schedule(section: str, schedule: Any) -> List[Any]:
    """Owner-safe schedule projection. Lists of primitives pass
    through; dict entries are restricted to the section's
    `_SCHEDULE_SUBKEYS` allowlist. Anything else is dropped so a
    free-form `staff_note` (or any other unsanctioned key) can never
    surface to an owner."""
    if not isinstance(schedule, list):
        return []
    allowed = _SCHEDULE_SUBKEYS.get(section, frozenset())
    out: List[Any] = []
    for item in schedule:
        if isinstance(item, (str, int, float, bool)):
            out.append(item)
        elif isinstance(item, dict):
            cleaned = {k: v for k, v in item.items()
                       if k in allowed and isinstance(v, (str, int, float, bool))}
            if cleaned:
                out.append(cleaned)
    return out


def _project_owner_safe(section: str,
                        structured: Optional[Dict[str, Any]],
                        policy_keys: Optional[set]) -> Optional[Dict[str, Any]]:
    """Project a structured payload to the owner-safe view for a
    section using the effective key set."""
    if not structured:
        return None
    keys = policy_keys if policy_keys is not None else set(_DEFAULT_OWNER_POLICY.get(section, set()))
    if not keys:
        return None
    out: Dict[str, Any] = {}
    for k in keys:
        if k not in structured:
            continue
        v = structured[k]
        if k == "supplements":
            out[k] = _project_supplements(v)
        elif k == "schedule":
            out[k] = _project_schedule(section, v)
        else:
            out[k] = v
    return out or None


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
                   owner_view: bool,
                   policy_keys: Optional[set] = None) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("feeding")
    legacy_str = horse.get("feed_plan")
    envelope = _legacy_envelope(structured, legacy_str)
    if envelope is None:
        return None
    if not owner_view:
        return envelope
    # Owner-filtered feeding.
    #
    # The legacy `horses.feed_plan` field is FREE TEXT and may contain
    # prep instructions, soaking details, medication notes, or staff-
    # only handling warnings. It is NEVER surfaced raw to owners. The
    # owner view exposes ONLY the keys in the effective policy
    # intersection (policy_keys ∩ _OWNER_SAFE_KEYS["feeding"]).
    safe_struct = _project_owner_safe("feeding", structured, policy_keys)
    if safe_struct is None:
        return None
    # legacy is intentionally DROPPED in the owner envelope.
    return {"structured": safe_struct, "legacy": None}


def _build_hay_access(profile: Optional[Dict[str, Any]],
                      owner_view: bool,
                      policy_keys: Optional[set] = None) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("hay_access")
    if not structured:
        return None
    if not owner_view:
        return {"structured": structured, "legacy": None}
    # Owner-filtered: only keys in the effective allowlist surface.
    # `restriction_flags`, `staff_only_warnings`, and all hay-net
    # operational state are excluded by the FORBIDDEN registry and by
    # not being in `_OWNER_SAFE_KEYS["hay_access"]`.
    safe = _project_owner_safe("hay_access", structured, policy_keys)
    if safe is None:
        return None
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
                   owner_view: bool,
                   policy_keys: Optional[set] = None) -> Optional[Dict[str, Any]]:
    structured = (profile or {}).get("turnout")
    legacy_group = horse.get("turnout_group")
    envelope = _legacy_envelope(structured, legacy_group)
    if envelope is None:
        return None
    if not owner_view:
        return envelope
    # Owner-filtered. Avoid list / injury risk notes / catching notes
    # are forbidden via the FORBIDDEN registry and dropped automatically
    # by `_project_owner_safe`.
    safe_struct = _project_owner_safe("turnout", structured, policy_keys) if structured else None
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
                           owner_view: bool,
                           policy_keys: Optional[set] = None) -> Optional[Dict[str, Any]]:
    """Riding & Training. Phase 1-B introduced manager-writable
    operational fields (`trainer_notes`, `exercise_restrictions`,
    `weekly_work_plan`, `rider_compatibility_notes`,
    `conditioning_plan`, `lesson_schedule`) that MUST NOT leak to
    owners. Staff view returns the full structured envelope; owner view
    is projected to the intersection of `policy_keys` and the section's
    `_OWNER_SAFE_KEYS` set, with the staff-only fields excluded.

    Legacy `horses.training_goals` is intentionally dropped in the
    owner view to avoid surfacing free-text staff annotations.
    """
    structured = (profile or {}).get("riding_training")
    legacy_goals = horse.get("training_goals")
    if not owner_view:
        return _legacy_envelope(structured, legacy_goals)
    safe_struct = _project_owner_safe(
        "riding_training", structured, policy_keys,
    ) if structured else None
    if not safe_struct:
        return None
    return {"structured": safe_struct, "legacy": None}


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


async def build_owner_safe_transfer_care_summary(db, horse: Dict[str, Any]) -> Dict[str, Any]:
    """Care-summary projection shared by owner ledger and passport transfer.

    Passport transfer must not grow its own definition of owner-safe care data;
    it should inherit the same section allowlists, schedule key filtering, and
    Stripe-string scrubbing used by the owner Ledger projection.
    """
    horse_id = horse.get("id")
    owner_view = True
    profile = await db.horse_care_profiles.find_one(
        {"horse_id": horse_id}, {"_id": 0},
    )
    policy_doc = await db.horse_owner_visibility_policy.find_one(
        {"horse_id": horse_id}, {"_id": 0},
    )
    eff = lambda s: _effective_owner_keys(s, policy_doc)  # noqa: E731
    equipment_keys = eff("equipment")
    equipment = [
        {k: r.get(k) for k in sorted(equipment_keys)}
        for r in (await db.horse_equipment.find(
            {"horse_id": horse_id, "barn_id": horse.get("barn_id"),
             "status": {"$ne": "retired"}},
            {"_id": 0, "category": 1, "label": 1},
        ).to_list(20))
    ] if equipment_keys else []
    return _scrub_strings({
        "feeding": _build_feeding(horse, profile, owner_view, eff("feeding")),
        "hay_access": _build_hay_access(profile, owner_view, eff("hay_access")),
        "turnout": _build_turnout(horse, profile, owner_view, eff("turnout")),
        "riding_training": _build_riding_training(
            horse, profile, owner_view, eff("riding_training"),
        ),
        "equipment": equipment,
    })


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
        # Owner-visibility policy doc is loaded ONCE on every read so
        # the response always reflects the current policy state. Used
        # only to compute owner-visible key sets — staff reads bypass.
        policy_doc = None
        if owner_view:
            policy_doc = await db.horse_owner_visibility_policy.find_one(
                {"horse_id": horse_id}, {"_id": 0},
            )
        # Pre-compute effective owner key sets per section.
        eff = (lambda s: _effective_owner_keys(s, policy_doc)) if owner_view else (lambda s: None)
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
            "feeding":          _build_feeding(horse, profile, owner_view, eff("feeding")),
            "hay_access":       _build_hay_access(profile, owner_view, eff("hay_access")),
            "stall_bedding":    _build_stall_bedding(profile, owner_view),
            "turnout":          _build_turnout(horse, profile, owner_view, eff("turnout")),
            "handling_behavior": _build_handling_behavior(horse, profile, owner_view),
            "riding_training":  _build_riding_training(horse, profile, owner_view, eff("riding_training")),

            "equipment":        _build_equipment_summary(equipment_rows, owner_view),
            "service_providers": [] if owner_view else list(provider_rows),

            "health":           _build_health(
                                    meds, med_logs, vet_records,
                                    injuries, wellness,
                                    horse.get("allergies"),
                                    owner_view,
                                ),

            # Staff/manager view loads the 20 most recent daily check
            # logs in descending `checked_at` order. Owners ALWAYS get
            # an empty array — daily checks are hard-hidden in 1-C.
            "daily_checks_recent": [] if owner_view else (
                await db.horse_daily_check_logs.find(
                    {"horse_id": horse_id, "barn_id": horse["barn_id"]},
                    {"_id": 0},
                ).sort("checked_at", -1).to_list(20)
            ),
            # Phase 1-D: staff/manager view loads top 20 active (open +
            # acknowledged) alerts, severity desc then last_seen desc.
            # Owners ALWAYS get [] — alerts are hard-hidden in 1-D.
            "alerts_open": [] if owner_view else (
                await db.horse_ledger_alerts.find(
                    {"horse_id": horse_id, "barn_id": horse["barn_id"],
                     "status": {"$in": ["open", "acknowledged"]}},
                    {"_id": 0},
                ).sort([("severity_rank", -1), ("last_seen_at", -1)]).to_list(20)
            ),
            "audit_recent":        [],
        }

        # Final defense-in-depth scrub for Stripe-shaped substrings
        # (R1-B parity) on every string in the response.
        return _scrub_strings(response)

    # =================================================================
    # Phase HorseOps-1B — manager edit flows + first writes.
    # =================================================================
    # 5 operational first-write collections + audit rows in
    # `horse_ledger_audit`. Owner-visibility policy is backend-
    # authoritative on every read; manager writes never expand owner
    # view beyond the allowlist intersected with the forbidden set.
    # =================================================================

    def _require_mutator(user, horse):
        """Mutator gate: only `admin` or `barn_manager` in the horse's
        barn may mutate. Owners (even primary) are read-only. Cross-
        barn or wrong role → 403."""
        role = (user.get("role") or "").strip().lower()
        if role not in {"admin", "barn_manager"}:
            raise HTTPException(403, "Insufficient role for Care Ledger edit.")
        # barn_filter already enforced via the horse fetch.

    async def _emit_audit(horse_id, barn_id, user, *, section, action,
                          field_paths, sensitivity):
        """Append a privacy-first audit row. NO before/after, NO notes,
        NO hay-net instructions, NO behavior warnings — field-path
        only + section + sensitivity enum."""
        import uuid as _uuid
        await db.horse_ledger_audit.insert_one({
            "id": f"hla_{_uuid.uuid4().hex[:24]}",
            "horse_id": horse_id, "barn_id": barn_id,
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor_user_id": user.get("id"),
            "actor_role":    user.get("role"),
            "section":   section,
            "action":    action,
            "field_paths": sorted(field_paths),
            "sensitivity": sensitivity,
            "owner_visible_eligible": sensitivity == "owner_visible",
        })

    # Per-section writable whitelists (every other field → 422).
    _SECTION_WRITABLE: Dict[str, set] = {
        "feeding": {
            "grain_feed_type", "amount", "amount_value", "amount_unit",
            "schedule", "prep_instructions", "soaking", "supplements",
            "meds_with_feed", "water_source", "water_check_required",
            "special_handling_notes", "horse_preferences", "sensitivities",
            "staff_only_warnings",
        },
        "hay_access": {
            "access_type", "hay_type", "quantity_per_feeding",
            "quantity_value", "quantity_unit", "target_level",
            "source_location", "allergy_restriction_notes",
            "slow_feeder_used", "restriction_flags", "hay_nets",
            "exception_notes",
        },
        "stall_bedding": {
            "stall_number", "barn_aisle_section", "stall_type",
            "bedding_type", "bedding_type_other",
            "bedding_depth_preference", "banked_bedding_required",
            "dust_sensitivity", "respiratory_restriction_notes",
            "bedding_allergy_notes", "spot_clean_frequency",
            "muck_schedule", "full_strip_schedule", "add_bedding_threshold",
            "stall_safety_notes", "water_bucket_check_required",
            "automatic_waterer_present",
        },
        "turnout": {
            "schedule", "pasture_paddock_assignment", "turnout_group",
            "buddies", "avoid", "grass_restrictions", "mud_restrictions",
            "weather_rules", "required_apparel", "injury_risk_notes",
            "catching_notes",
        },
        "handling_behavior": {
            "catching_notes", "grooming_sensitivities", "tacking_preferences",
            "trailer_loading_notes", "clipping_notes", "injection_behavior",
            "farrier_behavior", "vet_behavior", "known_risks",
            "required_staff_experience_level",
        },
        "riding_training": {
            "discipline", "current_level", "goals_short_term",
            "goals_long_term", "weekly_work_plan", "ride_schedule",
            "lesson_schedule", "trainer_notes", "exercise_restrictions",
            "conditioning_plan", "competition_goals",
            "rider_compatibility_notes",
        },
    }

    # Sensitivity classifier per section (default fail-closed staff_only).
    _SECTION_SENSITIVITY: Dict[str, str] = {
        "feeding":           "operational",
        "hay_access":        "operational",
        "stall_bedding":     "staff_only",
        "turnout":           "operational",
        "handling_behavior": "staff_only",
        "riding_training":   "owner_visible",
        "equipment":         "operational",
        "service":           "operational",
        "visibility_policy": "operational",
    }

    # Forbidden owner-allowlist keys — even a manager cannot add these.
    _FORBIDDEN_OWNER_KEYS = {
        "feeding": {"legacy", "soaking", "soaking.*", "prep_instructions",
                    "staff_only_warnings", "sensitivities", "meds_with_feed",
                    "meds_with_feed.*", "horse_preferences",
                    "special_handling_notes", "water_check_required",
                    "water_source"},
        "hay_access": {"restriction_flags", "staff_only_warnings",
                       "hay_nets", "hay_nets.*", "allergy_restriction_notes",
                       "exception_notes", "slow_feeder_used",
                       "source_location", "target_level"},
        "stall_bedding": {"*"},
        "handling_behavior": {"*"},
        "turnout": {"avoid", "injury_risk_notes", "catching_notes",
                    "grass_restrictions", "mud_restrictions",
                    "weather_rules"},
        # Round-1 P0 fix: riding_training gained writable operational
        # fields in 1-B. These MUST NOT leak to owners — neither
        # through a policy expansion nor through a direct projection.
        "riding_training": {"trainer_notes", "exercise_restrictions",
                            "weekly_work_plan", "rider_compatibility_notes",
                            "conditioning_plan", "lesson_schedule",
                            "ride_schedule"},
        "identity": {"microchip_number", "tattoo_number", "registry_numbers",
                     "required_staff_experience_level",
                     "emergency_contact_ids", "document_ids",
                     "secondary_owner_ids"},
        "health.medication_logs_30d": {"*"},
        "health.injuries": {"notes"},
        "health.vet_records": {"notes"},
        "health.wellness_latest": {"staff_note", "internal_observation",
                                   "actor_user_id", "actor_name",
                                   "raw_vet_dictation"},
        "service_providers": {"*"},
        # Phase 1-C: daily checks are hard-hidden from owners. Any
        # attempt to expose `daily_checks_recent` via the owner-
        # visibility policy must 422.
        "daily_checks_recent": {"*"},
        # Phase 1-D: alerts are hard-hidden from owners. Owner-
        # visibility policy PUT 422s on this section.
        "alerts_open": {"*"},
    }

    def _is_forbidden_owner_key(section: str, key: str) -> bool:
        forb = _FORBIDDEN_OWNER_KEYS.get(section, set())
        if "*" in forb:
            return True
        if key.startswith("_"):
            return True
        if key in forb:
            return True
        # Wildcard prefix match (e.g., "hay_nets.*" forbids "hay_nets.foo")
        for f in forb:
            if f.endswith(".*") and key.startswith(f[:-1]):
                return True
        return False

    def _hay_nets_ok(value):
        """Hay-nets must be a list of dicts (≤6). Each item must be an
        object so we don't accept random scalars masquerading as nets."""
        if not isinstance(value, list) or len(value) > 6:
            return False
        return all(isinstance(item, dict) for item in value)

    def _supplements_ok(value):
        """Supplements must be a list of objects, each with a string
        `name`. Free-text strings, nested arrays, or non-dict items
        are rejected so owner projection can never accidentally pull
        a staff note into the supplement payload."""
        if not isinstance(value, list):
            return False
        for item in value:
            if not isinstance(item, dict):
                return False
            if "name" in item and not isinstance(item["name"], str):
                return False
        return True

    def _schedule_ok(section: str, value):
        """Schedule must be a list of primitives (str/number/bool) or
        dicts whose keys are in the section's `_SCHEDULE_SUBKEYS`
        allowlist with primitive values. This is what stops a payload
        like `[{"time": "AM", "staff_note": "..."}]` from ever landing
        in the DB."""
        if not isinstance(value, list):
            return False
        allowed = _SCHEDULE_SUBKEYS.get(section, frozenset())
        for item in value:
            if isinstance(item, (str, int, float, bool)):
                continue
            if isinstance(item, dict):
                if not item:
                    return False
                for k, v in item.items():
                    if k not in allowed:
                        return False
                    if not isinstance(v, (str, int, float, bool)):
                        return False
                continue
            return False
        return True

    _NESTED_VALIDATORS: Dict[str, Dict[str, Any]] = {
        "feeding": {
            "supplements": lambda v: _supplements_ok(v),
            "schedule":    lambda v: _schedule_ok("feeding", v),
        },
        "hay_access": {
            "hay_nets": lambda v: _hay_nets_ok(v),
        },
        "turnout": {
            "schedule": lambda v: _schedule_ok("turnout", v),
        },
    }

    async def _load_horse_or_404(horse_id, user):
        horse = await db.horses.find_one(
            barn_filter(user, {"id": horse_id}), {"_id": 0},
        )
        if not horse:
            raise HTTPException(404, "Horse not found")
        return horse

    # ---------------- PATCH care-profile (section-scoped) ----------------
    @router.patch("/horse-ledger/{horse_id}/care-profile")
    async def patch_care_profile(horse_id: str, body: Dict[str, Any],
                                 user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        if not isinstance(body, dict) or not body:
            raise HTTPException(422, "Empty body.")
        unknown_sections = [s for s in body if s not in _SECTION_WRITABLE]
        if unknown_sections:
            raise HTTPException(422, f"Unknown section: {unknown_sections[0]!r}")

        updates = {}
        changed_paths = []
        for section, section_body in body.items():
            if not isinstance(section_body, dict):
                raise HTTPException(422, f"Section {section!r} must be an object.")
            allowed = _SECTION_WRITABLE[section]
            for k in section_body:
                if k not in allowed:
                    raise HTTPException(422, f"Field {section}.{k!r} not editable.")
            if section == "hay_access" and "hay_nets" in section_body:
                if not _hay_nets_ok(section_body["hay_nets"]):
                    raise HTTPException(422, "Max 6 hay nets per horse.")
            # Nested validation pass — reject obvious shape violations
            # so the read path can safely project structured fields.
            for nested_key, validator in _NESTED_VALIDATORS.get(section, {}).items():
                if nested_key in section_body and not validator(section_body[nested_key]):
                    raise HTTPException(
                        422,
                        f"Invalid shape for {section}.{nested_key}.",
                    )
            updates[section] = section_body
            for k in section_body:
                changed_paths.append(f"{section}.{k}")

        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid as _uuid
        await db.horse_care_profiles.update_one(
            {"horse_id": horse_id},
            {"$set": {**updates, "updated_at": now_iso,
                      "updated_by": user.get("id"),
                      "barn_id": horse["barn_id"]},
             "$setOnInsert": {"id": f"hcp_{_uuid.uuid4().hex[:24]}",
                              "horse_id": horse_id, "created_at": now_iso}},
            upsert=True,
        )
        # Emit one audit row per touched section.
        for section in updates:
            sens = _SECTION_SENSITIVITY.get(section, "staff_only")
            await _emit_audit(
                horse_id, horse["barn_id"], user,
                section=section, action="updated",
                field_paths=[p for p in changed_paths if p.startswith(section + ".")],
                sensitivity=sens,
            )
        return {"ok": True, "horse_id": horse_id,
                "sections_updated": sorted(updates.keys())}

    # ---------------- PUT owner-visibility-policy ----------------
    _POLICY_SECTIONS = frozenset({
        "identity", "feeding", "hay_access", "stall_bedding", "turnout",
        "handling_behavior", "riding_training", "equipment",
        "service_providers", "health.medications", "health.vet_records",
        "health.injuries", "health.wellness_latest",
    })

    def _require_barn_template_manager(user) -> str:
        role = (user.get("role") or "").strip().lower()
        if role not in {"admin", "barn_manager"}:
            raise HTTPException(403, "Insufficient role for Care Ledger edit.")
        return resolve_barn_id(user)

    def _validate_policy_sections(sections: Any) -> Dict[str, Any]:
        if not isinstance(sections, dict):
            raise HTTPException(422, "Body must contain `sections` object.")
        cleaned: Dict[str, Any] = {}
        for section, spec in sections.items():
            if section not in _POLICY_SECTIONS:
                raise HTTPException(422, f"Unknown policy section: {section!r}")
            if not isinstance(spec, dict) or "allowlist" not in spec:
                raise HTTPException(422, f"Section {section!r} missing allowlist.")
            allowlist = spec["allowlist"]
            if not isinstance(allowlist, list):
                raise HTTPException(422, f"Allowlist for {section!r} must be a list.")
            out_keys: List[str] = []
            for key in allowlist:
                if not isinstance(key, str):
                    raise HTTPException(422, f"Allowlist key must be string: {key!r}")
                if _is_forbidden_owner_key(section, key):
                    raise HTTPException(
                        422, f"Key {section}.{key!r} is forbidden for owner allowlist."
                    )
                # Round-2 P1: unknown allowlist keys (outside the safe
                # registry) must be rejected up-front so a manager
                # cannot save ineffective policy values that the UI
                # then implies were accepted.
                safe = _OWNER_SAFE_KEYS.get(section)
                if safe is not None and key not in safe:
                    raise HTTPException(
                        422,
                        f"Key {section}.{key!r} is not an owner-safe key.",
                    )
                if safe is None:
                    # Section has no owner-exposable keys (e.g.
                    # stall_bedding, handling_behavior, service_providers).
                    raise HTTPException(
                        422,
                        f"Section {section!r} cannot be exposed to owners.",
                    )
                if key not in out_keys:
                    out_keys.append(key)
            cleaned[section] = {"allowlist": out_keys}
        return cleaned

    def _policy_field_paths(sections: Dict[str, Any]) -> List[str]:
        paths: List[str] = []
        for section, spec in sections.items():
            for key in spec.get("allowlist") or []:
                paths.append(f"{section}.{key}")
        return sorted(paths or sections.keys())

    @router.put("/horse-ledger/{horse_id}/owner-visibility-policy")
    async def put_visibility_policy(horse_id: str, body: Dict[str, Any],
                                    user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        sections = _validate_policy_sections((body or {}).get("sections"))
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid as _uuid
        await db.horse_owner_visibility_policy.update_one(
            {"horse_id": horse_id},
            {"$set": {"sections": sections, "updated_at": now_iso,
                      "updated_by": user.get("id"),
                      "barn_id": horse["barn_id"]},
             "$inc":  {"policy_version": 1},
             "$setOnInsert": {"id": f"hovp_{_uuid.uuid4().hex[:24]}",
                              "horse_id": horse_id}},
            upsert=True,
        )
        await _emit_audit(
            horse_id, horse["barn_id"], user,
            section="visibility_policy", action="updated",
            field_paths=_policy_field_paths(sections),
            sensitivity="operational",
        )
        return {"ok": True, "horse_id": horse_id,
                "sections": sorted(sections.keys())}

    # ---------------- Phase 1-F: barn-wide owner visibility template ----------------
    @router.get("/horse-ledger/templates/owner-visibility")
    async def get_owner_visibility_template(user=Depends(get_current_user)):
        barn_id = _require_barn_template_manager(user)
        row = await db.horse_owner_visibility_templates.find_one(
            {"barn_id": barn_id}, {"_id": 0},
        )
        if not row:
            return {"barn_id": barn_id, "sections": {}, "template_version": 0}
        return _scrub_strings({
            "barn_id": barn_id,
            "sections": row.get("sections") or {},
            "template_version": row.get("template_version") or 0,
            "updated_at": row.get("updated_at"),
        })

    @router.put("/horse-ledger/templates/owner-visibility")
    async def put_owner_visibility_template(body: Dict[str, Any],
                                            user=Depends(get_current_user)):
        barn_id = _require_barn_template_manager(user)
        sections = _validate_policy_sections((body or {}).get("sections"))
        if not sections:
            raise HTTPException(422, "Template must contain at least one section.")
        now_iso = datetime.now(timezone.utc).isoformat()
        await db.horse_owner_visibility_templates.update_one(
            {"barn_id": barn_id},
            {"$set": {"sections": sections, "updated_at": now_iso,
                      "updated_by": user.get("id")},
             "$inc": {"template_version": 1},
             "$setOnInsert": {"id": f"hovt_{uuid.uuid4().hex[:24]}",
                              "barn_id": barn_id, "created_at": now_iso}},
            upsert=True,
        )
        await db.horse_ledger_audit.insert_one({
            "id": f"hla_{uuid.uuid4().hex[:24]}",
            "horse_id": None, "barn_id": barn_id,
            "ts": now_iso,
            "actor_user_id": user.get("id"),
            "actor_role": user.get("role"),
            "section": "visibility_template",
            "action": "updated",
            "field_paths": _policy_field_paths(sections),
            "sensitivity": "operational",
            "owner_visible_eligible": False,
        })
        return {"ok": True, "barn_id": barn_id,
                "sections": sorted(sections.keys())}

    @router.post("/horse-ledger/templates/owner-visibility/apply")
    async def apply_owner_visibility_template(body: Dict[str, Any],
                                              user=Depends(get_current_user)):
        barn_id = _require_barn_template_manager(user)
        body = body or {}
        horse_ids = body.get("horse_ids")
        if horse_ids is not None:
            if not isinstance(horse_ids, list) or not all(isinstance(h, str) for h in horse_ids):
                raise HTTPException(422, "horse_ids must be a list of strings.")
            if not horse_ids:
                raise HTTPException(422, "horse_ids cannot be empty.")
            horse_filter = {"barn_id": barn_id, "id": {"$in": sorted(set(horse_ids))}}
        else:
            horse_filter = {"barn_id": barn_id, "status": {"$ne": "archived"}}
        template = await db.horse_owner_visibility_templates.find_one(
            {"barn_id": barn_id}, {"_id": 0},
        )
        if not template:
            raise HTTPException(404, "No owner visibility template configured.")
        sections = _validate_policy_sections(template.get("sections"))
        if not sections:
            raise HTTPException(422, "Owner visibility template is empty.")
        horses = await db.horses.find(horse_filter, {"_id": 0, "id": 1}).to_list(500)
        found_ids = [h["id"] for h in horses if h.get("id")]
        if horse_ids is not None and len(found_ids) != len(set(horse_ids)):
            raise HTTPException(404, "One or more horses were not found.")
        now_iso = datetime.now(timezone.utc).isoformat()
        for horse_id in found_ids:
            await db.horse_owner_visibility_policy.update_one(
                {"horse_id": horse_id},
                {"$set": {"sections": sections, "updated_at": now_iso,
                          "updated_by": user.get("id"),
                          "barn_id": barn_id,
                          "source": "barn_visibility_template"},
                 "$inc": {"policy_version": 1},
                 "$setOnInsert": {"id": f"hovp_{uuid.uuid4().hex[:24]}",
                                  "horse_id": horse_id}},
                upsert=True,
            )
            await _emit_audit(
                horse_id, barn_id, user,
                section="visibility_policy", action="template_applied",
                field_paths=_policy_field_paths(sections),
                sensitivity="operational",
            )
        return {"ok": True, "barn_id": barn_id,
                "applied_count": len(found_ids),
                "horse_ids": found_ids}

    # ---------------- Phase 1-F: manager pulse ----------------
    @router.get("/horse-ledger/pulse/manager")
    async def manager_pulse(user=Depends(get_current_user)):
        barn_id = _require_barn_template_manager(user)
        rows = await db.horse_ledger_alerts.find(
            {"barn_id": barn_id, "status": {"$in": ["open", "acknowledged"]}},
            {"_id": 0, "horse_id": 1, "severity": 1, "severity_rank": 1,
             "last_seen_at": 1},
        ).sort([("severity_rank", -1), ("last_seen_at", -1)]).to_list(500)
        horse_ids = sorted({r.get("horse_id") for r in rows if r.get("horse_id")})
        names = {}
        if horse_ids:
            horses = await db.horses.find(
                {"barn_id": barn_id, "id": {"$in": horse_ids}},
                {"_id": 0, "id": 1, "name": 1},
            ).to_list(len(horse_ids))
            names = {h.get("id"): h.get("name") for h in horses}
        grouped: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            hid = row.get("horse_id")
            if not hid:
                continue
            entry = grouped.setdefault(hid, {
                "horse_id": hid,
                "horse_name": names.get(hid) or "Horse",
                "open_count": 0,
                "urgent_count": 0,
                "attention_count": 0,
                "top_severity": "info",
                "top_severity_rank": 0,
                "last_seen_at": None,
            })
            entry["open_count"] += 1
            sev = row.get("severity") or "info"
            if sev == "urgent":
                entry["urgent_count"] += 1
            elif sev == "attention":
                entry["attention_count"] += 1
            rank = int(row.get("severity_rank") or 0)
            if rank > entry["top_severity_rank"]:
                entry["top_severity_rank"] = rank
                entry["top_severity"] = sev
            ts = row.get("last_seen_at")
            if ts and (entry["last_seen_at"] is None or ts > entry["last_seen_at"]):
                entry["last_seen_at"] = ts
        items = sorted(
            grouped.values(),
            key=lambda x: (x["top_severity_rank"], x.get("last_seen_at") or ""),
            reverse=True,
        )
        return _scrub_strings({"barn_id": barn_id, "items": items[:20]})

    # ---------------- equipment ----------------
    _EQUIPMENT_WRITABLE = {"category", "label", "brand", "size", "fit_notes",
                           "location", "restrictions", "cleaning_care_notes",
                           "saddle_fit_history", "status"}
    _EQUIPMENT_STATUS = {"active", "retired"}

    @router.post("/horse-ledger/{horse_id}/equipment")
    async def add_equipment(horse_id: str, body: Dict[str, Any],
                            user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        if not isinstance(body, dict) or not body.get("category"):
            raise HTTPException(422, "category is required.")
        bad = [k for k in body if k not in _EQUIPMENT_WRITABLE]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        if body.get("status") and body["status"] not in _EQUIPMENT_STATUS:
            raise HTTPException(422, "status must be active|retired.")
        import uuid as _uuid
        eq_id = f"eq_{_uuid.uuid4().hex[:24]}"
        doc = {**body, "id": eq_id, "horse_id": horse_id,
               "barn_id": horse["barn_id"],
               "status": body.get("status") or "active",
               "created_at": datetime.now(timezone.utc).isoformat()}
        await db.horse_equipment.insert_one(doc)
        await _emit_audit(horse_id, horse["barn_id"], user,
                          section="equipment", action="created",
                          field_paths=sorted(body.keys()),
                          sensitivity="operational")
        return {"ok": True, "id": eq_id}

    @router.patch("/horse-ledger/{horse_id}/equipment/{equipment_id}")
    async def patch_equipment(horse_id: str, equipment_id: str,
                              body: Dict[str, Any],
                              user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        bad = [k for k in (body or {}) if k not in _EQUIPMENT_WRITABLE]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        if body.get("status") and body["status"] not in _EQUIPMENT_STATUS:
            raise HTTPException(422, "status must be active|retired.")
        r = await db.horse_equipment.update_one(
            {"id": equipment_id, "horse_id": horse_id,
             "barn_id": horse["barn_id"]},
            {"$set": {**body, "updated_at": datetime.now(timezone.utc).isoformat()}},
        )
        if r.matched_count == 0:
            raise HTTPException(404, "Equipment not found.")
        action = "archived" if body.get("status") == "retired" else "updated"
        await _emit_audit(horse_id, horse["barn_id"], user,
                          section="equipment", action=action,
                          field_paths=sorted(body.keys()),
                          sensitivity="operational")
        return {"ok": True}

    # ---------------- service providers + assignments ----------------
    _PROVIDER_CATS = {"vet", "farrier", "body_worker", "chiropractor",
                      "massage", "acupuncturist", "saddle_fitter",
                      "nutritionist", "dentist", "trainer", "other"}
    _PROVIDER_WRITABLE = {"category", "name", "company", "phone", "email",
                          "address", "notes", "is_primary_for_barn", "status",
                          "provider_user_id"}
    _PROVIDER_STATUS = {"active", "archived"}
    _ASSIGNMENT_WRITABLE = {"provider_id", "provider_user_id", "category", "last_service_date",
                            "next_due_date", "interval_days", "notes",
                            "is_primary_for_horse", "status"}
    _ASSIGNMENT_STATUS = {"active", "archived"}

    @router.post("/horse-ledger/{horse_id}/service-providers")
    async def add_provider(horse_id: str, body: Dict[str, Any],
                           user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        if (body or {}).get("category") not in _PROVIDER_CATS:
            raise HTTPException(422, "category must be a known provider type.")
        if not body.get("name"):
            raise HTTPException(422, "name is required.")
        bad = [k for k in body if k not in _PROVIDER_WRITABLE]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        if body.get("status") and body["status"] not in _PROVIDER_STATUS:
            raise HTTPException(422, "status must be active|archived.")
        if not await service_provider_user_exists(db, user, body.get("provider_user_id")):
            raise HTTPException(422, "provider_user_id must reference a same-barn provider user.")
        import uuid as _uuid
        sp_id = f"sp_{_uuid.uuid4().hex[:24]}"
        await db.service_providers.insert_one({
            **body, "id": sp_id, "barn_id": horse["barn_id"],
            "status": body.get("status") or "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        await _emit_audit(horse_id, horse["barn_id"], user,
                          section="service", action="created",
                          field_paths=sorted(body.keys()),
                          sensitivity="operational")
        return {"ok": True, "id": sp_id}

    @router.post("/horse-ledger/{horse_id}/provider-assignments")
    async def add_assignment(horse_id: str, body: Dict[str, Any],
                             user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        if not (body or {}).get("provider_id"):
            raise HTTPException(422, "provider_id is required.")
        if body.get("category") and body["category"] not in _PROVIDER_CATS:
            raise HTTPException(422, "category must be a known provider type.")
        bad = [k for k in body if k not in _ASSIGNMENT_WRITABLE]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        if body.get("status") and body["status"] not in _ASSIGNMENT_STATUS:
            raise HTTPException(422, "status must be active|archived.")
        # Provider must be in same barn.
        prov = await db.service_providers.find_one(
            {"id": body["provider_id"], "barn_id": horse["barn_id"]},
            {"_id": 0, "id": 1, "provider_user_id": 1},
        )
        if not prov:
            raise HTTPException(404, "Provider not found.")
        if body.get("provider_user_id") and prov.get("provider_user_id") and body["provider_user_id"] != prov["provider_user_id"]:
            raise HTTPException(422, "provider_user_id must match the linked provider.")
        if not await service_provider_user_exists(db, user, body.get("provider_user_id") or prov.get("provider_user_id")):
            raise HTTPException(422, "provider_user_id must reference a same-barn provider user.")
        import uuid as _uuid
        hpa_id = f"hpa_{_uuid.uuid4().hex[:24]}"
        await db.horse_provider_assignments.insert_one({
            **body, "id": hpa_id, "horse_id": horse_id,
            "provider_user_id": body.get("provider_user_id") or prov.get("provider_user_id"),
            "barn_id": horse["barn_id"],
            "status": body.get("status") or "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        await _emit_audit(horse_id, horse["barn_id"], user,
                          section="service", action="created",
                          field_paths=sorted(body.keys()),
                          sensitivity="operational")
        return {"ok": True, "id": hpa_id}

    @router.patch("/horse-ledger/{horse_id}/provider-assignments/{assignment_id}")
    async def patch_assignment(horse_id: str, assignment_id: str,
                               body: Dict[str, Any],
                               user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        bad = [k for k in (body or {}) if k not in _ASSIGNMENT_WRITABLE]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        if body.get("category") and body["category"] not in _PROVIDER_CATS:
            raise HTTPException(422, "category must be a known provider type.")
        if body.get("status") and body["status"] not in _ASSIGNMENT_STATUS:
            raise HTTPException(422, "status must be active|archived.")
        if not await service_provider_user_exists(db, user, body.get("provider_user_id")):
            raise HTTPException(422, "provider_user_id must reference a same-barn provider user.")
        r = await db.horse_provider_assignments.update_one(
            {"id": assignment_id, "horse_id": horse_id,
             "barn_id": horse["barn_id"]},
            {"$set": {**body, "updated_at": datetime.now(timezone.utc).isoformat()}},
        )
        if r.matched_count == 0:
            raise HTTPException(404, "Assignment not found.")
        await _emit_audit(horse_id, horse["barn_id"], user,
                          section="service", action="updated",
                          field_paths=sorted(body.keys()),
                          sensitivity="operational")
        return {"ok": True}

    # =================================================================
    # Phase HorseOps-1C — staff daily checks.
    # =================================================================
    # Immutable observation log layered on top of the existing task
    # engine. Daily checks live in `horse_daily_check_logs`. A check
    # may optionally reference a `task_id` for trail linkage, but
    # creating a check does NOT auto-complete the task and does NOT
    # touch the task engine in any way. No new scheduler. No alerts
    # worker (1-D). Owner visibility is HARD-HIDDEN — `daily_checks_
    # recent` is never projected to owners and the visibility-policy
    # PUT 422s on any attempt to expose it.
    # =================================================================
    _CHECK_TYPES  = {"feed", "hay", "hay_net", "water", "bedding", "general"}
    _CHECK_STATUS = {"ok", "needs_attention", "missed", "not_applicable"}
    _CHECK_TOP_WRITABLE = {"check_type", "status", "notes", "payload",
                           "task_id", "checked_at"}
    _CHECK_PATCH_WRITABLE = {"status", "notes", "payload"}

    # Per-check_type payload subkey whitelists. Anything outside →
    # 422. Defense-in-depth on read also drops unknown keys via
    # `_project_check_payload`.
    _CHECK_PAYLOAD_SUBKEYS = {
        "hay_net":   {"nets_checked", "nets_refilled", "hay_net_id"},
        "hay_access":{"free_choice_available", "exception"},
        "water":     {"bucket_ok", "automatic_waterer_ok", "refilled"},
        "feed":      {"given", "missed_reason", "amount_value", "amount_unit"},
        "bedding":   {"condition", "top_off_needed", "full_strip_needed"},
        "general":   {"observation"},
    }
    _BEDDING_CONDITIONS = {"clean", "damp", "soiled"}

    # Staff roles that may CREATE a daily check (hybrid gate). PATCH is
    # restricted further to the original author or admin/barn_manager.
    _STAFF_CREATE_ROLES = {"admin", "barn_manager", "groom", "trainer",
                           "vet", "staff"}

    def _require_check_creator(user, horse):
        role = (user.get("role") or "").strip().lower()
        if role not in _STAFF_CREATE_ROLES:
            raise HTTPException(403, "Insufficient role for daily checks.")

    def _require_check_amender(user, horse, existing_log):
        role = (user.get("role") or "").strip().lower()
        if role in {"admin", "barn_manager"}:
            return
        if existing_log.get("checked_by_user_id") == user.get("id"):
            return
        raise HTTPException(403, "Only the author or a manager may amend.")

    # =================================================================
    # Phase HorseOps-1D — staff experience gate.
    # =================================================================
    # `users.experience_level` is the new field (default null → treated
    # as `novice`). Admin / barn_manager always bypass. `general` check
    # type bypasses. 403 message is INTENTIONALLY GENERIC — it must NOT
    # reveal that this horse has elevated handling risk.
    _EXP_RANK = {"novice": 0, "intermediate": 1, "experienced": 2, "advanced": 3}
    _EXP_GATED_CHECK_TYPES = {"feed", "hay", "hay_net", "water", "bedding"}
    _EXP_GATE_403 = "Insufficient permission for this care action."

    async def _enforce_experience_gate(user, horse, check_type):
        role = (user.get("role") or "").strip().lower()
        if role in {"admin", "barn_manager"}:
            return
        if check_type not in _EXP_GATED_CHECK_TYPES:
            return
        prof = await db.horse_care_profiles.find_one(
            {"horse_id": horse["id"]}, {"_id": 0, "handling_behavior": 1},
        )
        required = ((prof or {}).get("handling_behavior") or {}).get(
            "required_staff_experience_level")
        if not required:
            return
        required_rank = _EXP_RANK.get(required)
        if required_rank is None:
            return  # Unknown level → fail open (data drift).
        caller_level = (user.get("experience_level") or "novice")
        caller_rank = _EXP_RANK.get(caller_level, 0)
        if caller_rank < required_rank:
            # NO alert, NO audit row, NO history event on denial
            # (locked HorseOps convention — denied attempts leave no
            # operational artifact).
            raise HTTPException(403, _EXP_GATE_403)

    # =================================================================
    # Phase HorseOps-1D — alert minting (event-driven from daily checks).
    # =================================================================
    _ALERT_TYPES = {"feed", "hay", "hay_net", "water", "bedding", "general"}
    _ALERT_STATUSES = {"open", "acknowledged", "closed"}
    # Severity ladder: info < attention < urgent. Repeats may upgrade
    # but never downgrade.
    _SEVERITY_RANK = {"info": 0, "attention": 1, "urgent": 2}

    def _derive_alert_triggers(check_type, status, payload):
        """Return (severity, triggers[]) for a daily-check row, or
        (None, []) if no alert should mint. Per the founder spec, only
        the listed triggers create alerts; pure `ok` checks do not."""
        triggers = []
        severity = None
        if status == "missed":
            triggers.append("status.missed")
            severity = "urgent" if check_type in {"feed", "water"} else "attention"
        elif status == "needs_attention":
            triggers.append("status.needs_attention")
            severity = "attention"
        p = payload or {}
        water = p.get("water") or {}
        if water.get("bucket_ok") is False:
            triggers.append("water.bucket_ok=false")
            severity = "urgent"
        if water.get("automatic_waterer_ok") is False:
            triggers.append("water.automatic_waterer_ok=false")
            severity = "urgent"
        feed = p.get("feed") or {}
        if feed.get("given") is False:
            triggers.append("feed.given=false")
            severity = "urgent"
        bedding = p.get("bedding") or {}
        if bedding.get("full_strip_needed") is True:
            triggers.append("bedding.full_strip_needed=true")
            severity = severity or "attention"
        if bedding.get("top_off_needed") is True:
            triggers.append("bedding.top_off_needed=true")
            severity = severity or "attention"
        hay_net = p.get("hay_net") or {}
        if hay_net.get("nets_checked", 0) and not hay_net.get("nets_refilled"):
            triggers.append("hay_net.nets_refilled=0")
            severity = severity or "attention"
        hay_access = p.get("hay_access") or {}
        if hay_access.get("free_choice_available") is False:
            triggers.append("hay_access.free_choice_available=false")
            severity = severity or "attention"
        return (severity, triggers)

    async def _mint_alert_for_check(horse, check_doc):
        """Idempotent alert minting from a daily-check row. Dedupe key
        is `(horse_id, alert_type, status != "closed")`. Repeats bump
        `occurrence_count` and `last_seen_at`; severity may upgrade.
        `source_check_id + alert_type` never produces a duplicate
        ROW, but it MAY upgrade the existing alert's severity and
        merge new triggers (Round-1 fix — a PATCH amend that flips
        `feed.given` from true to false must escalate the alert)."""
        severity, triggers = _derive_alert_triggers(
            check_doc["check_type"], check_doc["status"], check_doc.get("payload"),
        )
        if not severity:
            return  # No alert needed.
        alert_type = check_doc["check_type"]
        horse_id = horse["id"]
        barn_id  = horse["barn_id"]
        source_check_id = check_doc["id"]
        now_iso = datetime.now(timezone.utc).isoformat()
        # 1. Exact (source_check_id, alert_type) — same check row.
        #    Do NOT bump occurrence_count (it's the same source), but
        #    DO upgrade severity and merge triggers so a PATCH amend
        #    that worsens the condition is reflected on the alert.
        existing_exact = await db.horse_ledger_alerts.find_one(
            {"horse_id": horse_id, "alert_type": alert_type,
             "source_check_id": source_check_id},
            {"_id": 0},
        )
        if existing_exact:
            cur_rank = _SEVERITY_RANK.get(existing_exact.get("severity"), -1)
            new_rank = _SEVERITY_RANK.get(severity, 0)
            sev_to_set = severity if new_rank > cur_rank else existing_exact["severity"]
            sev_rank   = _SEVERITY_RANK[sev_to_set]
            merged = sorted(set((existing_exact.get("triggers") or []) + triggers))
            updates = {
                "last_seen_at": now_iso,
                "severity": sev_to_set,
                "severity_rank": sev_rank,
                "triggers": merged,
            }
            if updates["severity"] != existing_exact.get("severity") or \
               merged != (existing_exact.get("triggers") or []):
                await db.horse_ledger_alerts.update_one(
                    {"id": existing_exact["id"]}, {"$set": updates},
                )
                await db.horse_ledger_alert_events.insert_one({
                    "id": f"hlae_{uuid.uuid4().hex[:24]}",
                    "alert_id": existing_exact["id"],
                    "horse_id": horse_id, "barn_id": barn_id, "ts": now_iso,
                    "event_type": "amended",
                    "actor_user_id": check_doc.get("checked_by_user_id"),
                    "actor_role":    None,
                    "source_check_id": source_check_id,
                    "notes_present": bool(check_doc.get("notes")),
                })
            return
        # 2. Open/acknowledged alert exists for this (horse, type) →
        #    update last_seen + occurrence_count + merge triggers.
        existing_open = await db.horse_ledger_alerts.find_one(
            {"horse_id": horse_id, "alert_type": alert_type,
             "status": {"$in": ["open", "acknowledged"]}},
            {"_id": 0},
        )
        if existing_open:
            # Severity upgrade only.
            cur_rank = _SEVERITY_RANK.get(existing_open.get("severity"), -1)
            new_rank = _SEVERITY_RANK.get(severity, 0)
            sev_to_set = severity if new_rank > cur_rank else existing_open["severity"]
            sev_rank   = _SEVERITY_RANK[sev_to_set]
            merged = sorted(set((existing_open.get("triggers") or []) + triggers))
            await db.horse_ledger_alerts.update_one(
                {"id": existing_open["id"]},
                {"$set": {
                    "last_seen_at": now_iso,
                    "severity": sev_to_set,
                    "severity_rank": sev_rank,
                    "triggers": merged,
                    "last_source_check_id": source_check_id,
                },
                 "$inc": {"occurrence_count": 1}},
            )
            await db.horse_ledger_alert_events.insert_one({
                "id": f"hlae_{uuid.uuid4().hex[:24]}",
                "alert_id": existing_open["id"],
                "horse_id": horse_id, "barn_id": barn_id, "ts": now_iso,
                "event_type": "reoccurred",
                "actor_user_id": check_doc.get("checked_by_user_id"),
                "actor_role":    None,
                "source_check_id": source_check_id,
                "notes_present": bool(check_doc.get("notes")),
            })
            return
        # 3. Otherwise create a new alert.
        alert_id = f"hla_{uuid.uuid4().hex[:24]}"
        await db.horse_ledger_alerts.insert_one({
            "id": alert_id,
            "horse_id": horse_id, "barn_id": barn_id,
            "alert_type": alert_type,
            "severity":     severity,
            "severity_rank": _SEVERITY_RANK[severity],
            "status":     "open",
            "source_check_id": source_check_id,
            "last_source_check_id": source_check_id,
            "first_seen_at": now_iso,
            "last_seen_at":  now_iso,
            "occurrence_count": 1,
            "triggers": sorted(set(triggers)),
            "acknowledged_at": None, "acknowledged_by_user_id": None,
            "closed_at": None, "closed_by_user_id": None,
            "resolution_note": None,
            "next_escalation_at": None,  # informational only, populated by manual escalate
        })
        await db.horse_ledger_alert_events.insert_one({
            "id": f"hlae_{uuid.uuid4().hex[:24]}",
            "alert_id": alert_id,
            "horse_id": horse_id, "barn_id": barn_id, "ts": now_iso,
            "event_type": "opened",
            "actor_user_id": check_doc.get("checked_by_user_id"),
            "actor_role":    None,
            "source_check_id": source_check_id,
            "notes_present": bool(check_doc.get("notes")),
        })

    def _validate_check_body(body, *, is_patch):
        """Raises HTTPException(422) on any shape violation. Used for
        both POST (full body) and PATCH (subset)."""
        if not isinstance(body, dict) or not body:
            raise HTTPException(422, "Empty body.")
        allowed = _CHECK_PATCH_WRITABLE if is_patch else _CHECK_TOP_WRITABLE
        bad = [k for k in body if k not in allowed]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        # check_type only on POST
        if not is_patch:
            ct = body.get("check_type")
            if ct not in _CHECK_TYPES:
                raise HTTPException(422, "check_type invalid.")
        # status on either path
        if "status" in body and body["status"] not in _CHECK_STATUS:
            raise HTTPException(422, "status invalid.")
        # notes length cap, staff-only free text
        if "notes" in body and body["notes"] is not None:
            if not isinstance(body["notes"], str):
                raise HTTPException(422, "notes must be a string.")
            if len(body["notes"]) > 500:
                raise HTTPException(422, "notes too long (max 500).")
        # task_id shape (full validation incl. barn match happens later)
        if "task_id" in body and body["task_id"] is not None:
            if not isinstance(body["task_id"], str) or not body["task_id"]:
                raise HTTPException(422, "task_id must be a non-empty string.")
        # checked_at: ISO string only
        if "checked_at" in body and body["checked_at"] is not None:
            if not isinstance(body["checked_at"], str):
                raise HTTPException(422, "checked_at must be ISO string.")

    # Phase 1-C Round-2: each check_type owns exactly one payload
    # section. The validator rejects any mismatched section so a
    # `feed` check cannot carry `payload.bedding`, etc. The mapping
    # is also enforced on PATCH using the existing log's check_type
    # (the field is immutable on PATCH, so the mapping is stable).
    _CHECK_TYPE_PAYLOAD_SECTION = {
        "feed":    "feed",
        "hay":     "hay_access",
        "hay_net": "hay_net",
        "water":   "water",
        "bedding": "bedding",
        "general": "general",
    }

    def _validate_check_payload(payload, *, check_type):
        """Validate nested payload sections against the subkey
        whitelist + value enums. Each `check_type` may only carry
        its own paired payload section — feed→feed, water→water,
        bedding→bedding, hay→hay_access, hay_net→hay_net,
        general→general. payload may be None/empty."""
        if payload is None:
            return
        if not isinstance(payload, dict):
            raise HTTPException(422, "payload must be an object.")
        expected_section = _CHECK_TYPE_PAYLOAD_SECTION.get(check_type)
        for section, section_body in payload.items():
            allowed = _CHECK_PAYLOAD_SUBKEYS.get(section)
            if allowed is None:
                raise HTTPException(422, f"Unknown payload section: {section!r}")
            if expected_section is not None and section != expected_section:
                raise HTTPException(
                    422,
                    f"payload.{section} not allowed for check_type {check_type!r} "
                    f"(expected payload.{expected_section}).",
                )
            if not isinstance(section_body, dict):
                raise HTTPException(422, f"payload.{section} must be an object.")
            bad = [k for k in section_body if k not in allowed]
            if bad:
                raise HTTPException(
                    422, f"Field not editable: payload.{section}.{bad[0]}")
            # bedding.condition enum check
            if section == "bedding" and "condition" in section_body:
                if section_body["condition"] not in _BEDDING_CONDITIONS:
                    raise HTTPException(422, "bedding.condition invalid.")
            # primitive-only values
            for k, v in section_body.items():
                if v is None:
                    continue
                if not isinstance(v, (str, int, float, bool)):
                    raise HTTPException(
                        422, f"payload.{section}.{k} must be primitive.")

    def _check_field_paths(body):
        """Build the audit field_paths list — keys only, no values."""
        paths = []
        for k in body:
            if k == "payload" and isinstance(body[k], dict):
                for section, sub in body[k].items():
                    if isinstance(sub, dict):
                        for nk in sub:
                            paths.append(f"payload.{section}.{nk}")
                    else:
                        paths.append(f"payload.{section}")
            else:
                paths.append(k)
        return sorted(paths)

    @router.post("/horse-ledger/{horse_id}/daily-checks")
    async def create_daily_check(horse_id: str, body: Dict[str, Any],
                                 user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_check_creator(user, horse)
        _validate_check_body(body, is_patch=False)
        _validate_check_payload(body.get("payload"), check_type=body["check_type"])
        # Phase 1-D: experience gate runs AFTER role+shape checks so a
        # malformed body still 422s instead of leaking gate behavior.
        await _enforce_experience_gate(user, horse, body["check_type"])
        # Optional task linkage — must be a task in the same barn.
        # Real tasks (materialized by `task_engine.py`) carry
        # `tenant_id="default"` and `barn_id=<barn_id>`. We match on
        # `barn_id` so the existing task-engine shape is accepted.
        task_id = body.get("task_id")
        if task_id:
            task = await db.tasks.find_one(
                {"id": task_id, "barn_id": horse["barn_id"]},
                {"_id": 0, "id": 1, "barn_id": 1},
            )
            if not task:
                # The 1-C founder spec calls for 422 (a *known* invalid
                # body), not 404 (the parent resource). Cross-barn task
                # ids are treated as malformed input.
                raise HTTPException(422, "task_id not in this barn.")
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid as _uuid
        check_id = f"hdcl_{_uuid.uuid4().hex[:24]}"
        doc = {
            "id": check_id,
            "horse_id": horse_id,
            "barn_id":  horse["barn_id"],
            "task_id":  task_id or None,
            "check_type": body["check_type"],
            "status":     body.get("status") or "ok",
            "notes":      body.get("notes"),
            "payload":    body.get("payload") or {},
            "created_at": now_iso,
            "checked_at": body.get("checked_at") or now_iso,
            "checked_by_user_id": user.get("id"),
            "amended_at": None,
        }
        await db.horse_daily_check_logs.insert_one(doc)
        sensitivity = "operational" if body["check_type"] == "feed" else "staff_only"
        await _emit_audit(
            horse_id, horse["barn_id"], user,
            section="daily_checks", action="created",
            field_paths=_check_field_paths(body),
            sensitivity=sensitivity,
        )
        # Phase 1-D: mint/update alert side-effect AFTER the daily-check
        # row + audit row are persisted, so the alert is always linked
        # to a real source_check_id.
        await _mint_alert_for_check(horse, doc)
        return {"ok": True, "id": check_id}

    @router.get("/horse-ledger/{horse_id}/daily-checks")
    async def list_daily_checks(horse_id: str,
                                limit: int = 20,
                                check_type: Optional[str] = None,
                                user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        # Hard-hidden from owners.
        role = (user.get("role") or "").strip().lower()
        if role == "horse_owner":
            raise HTTPException(403, "Daily checks are staff-only.")
        _require_check_creator(user, horse)  # any in-barn staff role
        q: Dict[str, Any] = {"horse_id": horse_id, "barn_id": horse["barn_id"]}
        if check_type is not None:
            if check_type not in _CHECK_TYPES:
                raise HTTPException(422, "check_type invalid.")
            q["check_type"] = check_type
        limit = max(1, min(int(limit or 20), 100))
        rows = await db.horse_daily_check_logs.find(q, {"_id": 0}) \
            .sort("checked_at", -1).to_list(limit)
        return _scrub_strings({"items": rows})

    @router.patch("/horse-ledger/{horse_id}/daily-checks/{check_id}")
    async def patch_daily_check(horse_id: str, check_id: str,
                                body: Dict[str, Any],
                                user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        existing = await db.horse_daily_check_logs.find_one(
            {"id": check_id, "horse_id": horse_id,
             "barn_id": horse["barn_id"]}, {"_id": 0},
        )
        if not existing:
            raise HTTPException(404, "Daily check not found.")
        _require_check_amender(user, horse, existing)
        _validate_check_body(body, is_patch=True)
        # PATCH cannot change check_type, so the existing row's type
        # determines which payload section is allowed.
        _validate_check_payload(body.get("payload"),
                                check_type=existing.get("check_type"))
        # Experience gate also applies to PATCH amend.
        await _enforce_experience_gate(user, horse, existing["check_type"])
        updates: Dict[str, Any] = {}
        for k in ("status", "notes"):
            if k in body:
                updates[k] = body[k]
        if "payload" in body and isinstance(body["payload"], dict):
            # Merge payload section-by-section so a partial PATCH does
            # not blow away prior subkeys. (Section-level replace,
            # subkey-level merge.)
            merged = dict(existing.get("payload") or {})
            for section, sub in body["payload"].items():
                cur = dict(merged.get(section) or {})
                cur.update(sub)
                merged[section] = cur
            updates["payload"] = merged
        if not updates:
            raise HTTPException(422, "No editable fields supplied.")
        updates["amended_at"] = datetime.now(timezone.utc).isoformat()
        await db.horse_daily_check_logs.update_one(
            {"id": check_id}, {"$set": updates},
        )
        sensitivity = "operational" if existing.get("check_type") == "feed" else "staff_only"
        await _emit_audit(
            horse_id, horse["barn_id"], user,
            section="daily_checks", action="updated",
            field_paths=_check_field_paths(body),
            sensitivity=sensitivity,
        )
        # Mint/update alert from the merged view of the doc.
        merged_doc = {**existing, **updates, "id": check_id}
        # Status defaults to existing if PATCH didn't change it.
        if "status" not in updates:
            merged_doc["status"] = existing.get("status") or "ok"
        # Re-derive triggers off the merged doc; reuses the dedupe
        # logic, so a `feed.given=false` PATCH on an `ok` row will
        # mint a new alert.
        await _mint_alert_for_check(horse, merged_doc)
        return {"ok": True}

    # =================================================================
    # Phase HorseOps-1D — alert lifecycle endpoints.
    # =================================================================
    # status filter values:
    #   active        → open + acknowledged (default for list view)
    #   open          → only open
    #   acknowledged  → only acknowledged
    #   closed        → only closed
    #   all           → all three
    _ALERT_STATUS_FILTERS = {"open", "acknowledged", "closed", "active", "all"}
    # ≤500 char resolution note cap, staff-only free text.
    _MAX_RES_NOTE = 500

    def _alert_status_q(status_filter: Optional[str]) -> Dict[str, Any]:
        if status_filter in (None, "", "active"):
            return {"status": {"$in": ["open", "acknowledged"]}}
        if status_filter == "all":
            return {}
        return {"status": status_filter}

    @router.get("/horse-ledger/{horse_id}/alerts")
    async def list_alerts(horse_id: str, status: Optional[str] = None,
                          limit: int = 20,
                          user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        role = (user.get("role") or "").strip().lower()
        if role == "horse_owner":
            raise HTTPException(403, "Alerts are staff-only.")
        _require_check_creator(user, horse)  # any in-barn staff role
        if status is not None and status not in _ALERT_STATUS_FILTERS:
            raise HTTPException(422, "status filter invalid.")
        q = {"horse_id": horse_id, "barn_id": horse["barn_id"], **_alert_status_q(status)}
        limit = max(1, min(int(limit or 20), 100))
        rows = await db.horse_ledger_alerts.find(q, {"_id": 0}) \
            .sort([("severity_rank", -1), ("last_seen_at", -1)]).to_list(limit)
        return _scrub_strings({"items": rows})

    @router.patch("/horse-ledger/{horse_id}/alerts/{alert_id}")
    async def patch_alert(horse_id: str, alert_id: str,
                          body: Dict[str, Any],
                          user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        role = (user.get("role") or "").strip().lower()
        if role == "horse_owner":
            raise HTTPException(403, "Alerts are staff-only.")
        _require_check_creator(user, horse)
        existing = await db.horse_ledger_alerts.find_one(
            {"id": alert_id, "horse_id": horse_id, "barn_id": horse["barn_id"]},
            {"_id": 0},
        )
        if not existing:
            raise HTTPException(404, "Alert not found.")
        if not isinstance(body, dict) or not body:
            raise HTTPException(422, "Empty body.")
        allowed = {"status", "resolution_note", "next_escalation_at"}
        bad = [k for k in body if k not in allowed]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        new_status = body.get("status")
        if new_status is not None and new_status not in _ALERT_STATUSES:
            raise HTTPException(422, "status invalid.")
        if "resolution_note" in body and body["resolution_note"] is not None:
            if not isinstance(body["resolution_note"], str):
                raise HTTPException(422, "resolution_note must be a string.")
            if len(body["resolution_note"]) > _MAX_RES_NOTE:
                raise HTTPException(
                    422, f"resolution_note too long (max {_MAX_RES_NOTE}).")
        # Determine the transition.
        cur = existing.get("status")
        now_iso = datetime.now(timezone.utc).isoformat()
        updates: Dict[str, Any] = {}
        event_type = None
        if new_status == "acknowledged" and cur == "open":
            updates["status"] = "acknowledged"
            updates["acknowledged_at"] = now_iso
            updates["acknowledged_by_user_id"] = user.get("id")
            event_type = "acknowledged"
        elif new_status == "closed" and cur in {"open", "acknowledged"}:
            updates["status"] = "closed"
            updates["closed_at"] = now_iso
            updates["closed_by_user_id"] = user.get("id")
            if "resolution_note" in body:
                updates["resolution_note"] = body["resolution_note"]
            event_type = "closed"
        elif new_status == "open" and cur == "closed":
            # Reopen — only managers may do this.
            if role not in {"admin", "barn_manager"}:
                raise HTTPException(403, "Only a manager may reopen an alert.")
            updates["status"] = "open"
            updates["closed_at"] = None
            updates["closed_by_user_id"] = None
            event_type = "reopened"
        elif new_status is not None:
            raise HTTPException(
                422, f"Invalid transition {cur!r} → {new_status!r}.")
        # Phase 1-D Round-1: `next_escalation_at` is informational only,
        # but it is NOT a silent field. Only admin/barn_manager may set
        # it, and setting it always emits an alert_event + audit row so
        # the change is visible on the alert's history.
        if "next_escalation_at" in body:
            if role not in {"admin", "barn_manager"}:
                raise HTTPException(
                    403, "Only a manager may set next_escalation_at.")
            v = body["next_escalation_at"]
            if v is not None and not isinstance(v, str):
                raise HTTPException(422, "next_escalation_at must be ISO string.")
            updates["next_escalation_at"] = v
            # If no status transition happened, mint an `escalation_scheduled`
            # event so the change is auditable.
            if event_type is None:
                event_type = "escalation_scheduled"
        if not updates:
            raise HTTPException(422, "No editable changes.")
        await db.horse_ledger_alerts.update_one(
            {"id": alert_id}, {"$set": updates},
        )
        if event_type:
            await db.horse_ledger_alert_events.insert_one({
                "id": f"hlae_{uuid.uuid4().hex[:24]}",
                "alert_id": alert_id,
                "horse_id": horse_id, "barn_id": horse["barn_id"],
                "ts": now_iso,
                "event_type": event_type,
                "actor_user_id": user.get("id"),
                "actor_role":    role,
                "source_check_id": None,
                "notes_present": bool(updates.get("resolution_note")),
            })
            # Audit row for the lifecycle transition (field_paths only).
            sensitivity = "operational" if existing.get("alert_type") in {"feed", "water"} else "staff_only"
            await _emit_audit(
                horse_id, horse["barn_id"], user,
                section="alerts", action=event_type,
                field_paths=sorted([k for k in updates.keys()]),
                sensitivity=sensitivity,
            )
        return {"ok": True}

    @router.get("/horse-ledger/{horse_id}/history")
    async def get_history(horse_id: str, limit: int = 50,
                          before: Optional[str] = None,
                          user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        role = (user.get("role") or "").strip().lower()
        if role == "horse_owner":
            raise HTTPException(403, "History is staff-only.")
        _require_check_creator(user, horse)
        limit = max(1, min(int(limit or 50), 200))
        cap = limit * 3  # over-fetch each source so the merged window covers `limit`.
        barn_id = horse["barn_id"]
        # Build the ts filter once.
        ts_q: Dict[str, Any] = {}
        if before:
            ts_q = {"$lt": before}
        # 1. recent daily checks
        check_q: Dict[str, Any] = {"horse_id": horse_id, "barn_id": barn_id}
        if ts_q:
            check_q["checked_at"] = ts_q
        checks = await db.horse_daily_check_logs.find(check_q, {"_id": 0}) \
            .sort("checked_at", -1).to_list(cap)
        # 2. recent alerts (by last_seen_at)
        alert_q: Dict[str, Any] = {"horse_id": horse_id, "barn_id": barn_id}
        if ts_q:
            alert_q["last_seen_at"] = ts_q
        alerts = await db.horse_ledger_alerts.find(alert_q, {"_id": 0}) \
            .sort("last_seen_at", -1).to_list(cap)
        # 3. recent audit (field_paths only — already that shape)
        audit_q: Dict[str, Any] = {"horse_id": horse_id, "barn_id": barn_id}
        if ts_q:
            audit_q["ts"] = ts_q
        audits = await db.horse_ledger_audit.find(audit_q, {"_id": 0}) \
            .sort("ts", -1).to_list(cap)
        # Merge + sort desc by ts (per-entry timestamp field varies).
        def _ts(entry, key):
            return entry.get(key) or ""
        merged = []
        for c in checks:
            merged.append({"entry_type": "daily_check", "ts": _ts(c, "checked_at"),
                           "id": c["id"], "check_type": c.get("check_type"),
                           "status": c.get("status"),
                           "checked_by_user_id": c.get("checked_by_user_id")})
        for a in alerts:
            merged.append({"entry_type": "alert", "ts": _ts(a, "last_seen_at"),
                           "id": a["id"], "alert_type": a.get("alert_type"),
                           "severity": a.get("severity"),
                           "status": a.get("status"),
                           "occurrence_count": a.get("occurrence_count")})
        for au in audits:
            merged.append({"entry_type": "audit", "ts": _ts(au, "ts"),
                           "section": au.get("section"),
                           "action": au.get("action"),
                           "field_paths": au.get("field_paths") or [],
                           "actor_user_id": au.get("actor_user_id")})
        merged.sort(key=lambda e: e["ts"], reverse=True)
        items = merged[:limit]
        # Stripe-scrub the merged response.
        return _scrub_strings({"items": items})

    # =================================================================
    # Phase HorseOps-1E — owner-facing filtered care ledger +
    # service-request flow.
    # =================================================================
    # Reuses the existing `service_requests` collection with
    # `source="owner_care_ledger"` as the discriminator so the existing
    # operational `/service-requests` routes (routes/operations.py) stay
    # byte-identical.
    _OWNER_REQUEST_TYPES = {"question", "care_follow_up",
                            "appointment_request", "other"}
    _OWNER_CONTACT       = {"app", "email", "phone"}
    _OWNER_MSG_MAX       = 1000
    _STAFF_NOTE_MAX      = 500
    _OWNER_RATE_WINDOW_S = 3600
    _OWNER_RATE_CAP      = 5
    _OWNER_STATUS        = {"new", "in_progress", "resolved"}
    _OWNER_VALID_TRANS = {
        ("new", "in_progress"), ("new", "resolved"),
        ("in_progress", "resolved"), ("in_progress", "new"),
        ("resolved", "in_progress"),  # reopen
    }

    def _is_horse_owner_for(user, horse) -> bool:
        """Owner if `user.id` matches `horses.primary_owner_id` (the
        locked Care Ledger field name from 1-A), `horses.owner_id`
        (legacy alias still in use across older docs), or appears in
        `horses.secondary_owner_ids`. Round-1 fix: 1-E originally
        only checked `owner_id` which caused 404s for every horse
        whose owner is recorded under `primary_owner_id`."""
        uid = user.get("id")
        if not uid:
            return False
        if horse.get("primary_owner_id") == uid:
            return True
        if horse.get("owner_id") == uid:
            return True
        sec = horse.get("secondary_owner_ids") or []
        return isinstance(sec, list) and uid in sec

    def _is_horse_guardian_for(user, horse) -> bool:
        uid = user.get("id")
        if not uid:
            return False
        if horse.get("guardian_user_id") == uid:
            return True
        guardians = horse.get("guardian_user_ids") or []
        return isinstance(guardians, list) and uid in guardians

    def _can_use_owner_request_contract(user, horse) -> bool:
        role = (user.get("role") or "").strip().lower()
        if role == "horse_owner":
            return _is_horse_owner_for(user, horse)
        if role == "parent":
            return _is_horse_guardian_for(user, horse)
        return False

    def _owner_safe_horse_projection(horse: Dict[str, Any]) -> Dict[str, Any]:
        data = horse.get("data") if isinstance(horse.get("data"), dict) else {}
        return _scrub_strings({
            "id": horse.get("id"),
            "name": horse.get("name") or data.get("name"),
            "barn_id": horse.get("barn_id"),
            "stall_location": horse.get("stall_location") or data.get("stall_location"),
            "breed": horse.get("breed") or data.get("breed"),
            "color": horse.get("color") or data.get("color"),
            "discipline": horse.get("discipline") or data.get("discipline"),
        })

    def _owner_safe_horse_clauses(user: Dict[str, Any]) -> List[Dict[str, Any]]:
        uid = user.get("id")
        if not uid:
            return []
        return [
            {"owner_id": uid},
            {"primary_owner_id": uid},
            {"secondary_owner_ids": uid},
            {"owner_user_id": uid},
            {"owner_user_ids": uid},
            {"guardian_user_id": uid},
            {"guardian_user_ids": uid},
            {"rider_user_id": uid},
            {"rider_user_ids": uid},
        ]

    async def _list_owner_safe_horses(user) -> Dict[str, Any]:
        role = (user.get("role") or "").strip().lower()
        if role not in {"horse_owner", "parent", "rider"}:
            raise HTTPException(403, "Owner-safe horse list is owner/guardian/rider only.")
        clauses = _owner_safe_horse_clauses(user)
        if not clauses:
            return {"items": []}
        rows = await db.horses.find(
            {
                "barn_id": resolve_barn_id(user),
                "$or": clauses,
            },
            {"_id": 0},
        ).sort("name", 1).to_list(200)
        return {"items": [_owner_safe_horse_projection(row) for row in rows]}

    async def _load_horse_for_owner_or_404(horse_id, user):
        """Owner endpoints leak NO existence — non-owners and cross-
        barn calls always 404."""
        horse = await db.horses.find_one({"id": horse_id}, {"_id": 0})
        if not horse:
            raise HTTPException(404, "Not found.")
        role = (user.get("role") or "").strip().lower()
        if role in {"horse_owner", "parent"}:
            if horse.get("barn_id") != user.get("barn_id"):
                raise HTTPException(404, "Not found.")
            if not _can_use_owner_request_contract(user, horse):
                raise HTTPException(404, "Not found.")
            return horse
        # Staff preview: must be in the same barn AND be admin/manager.
        if role in {"admin", "barn_manager"}:
            if horse.get("barn_id") != user.get("barn_id"):
                raise HTTPException(404, "Not found.")
            return horse
        # Other staff roles cannot preview the owner surface in 1-E.
        raise HTTPException(404, "Not found.")

    @router.get("/owner/horses")
    async def owner_horses(user=Depends(get_current_user)):
        return await _list_owner_safe_horses(user)

    @router.get("/owner-portal/horses")
    async def owner_portal_horses(user=Depends(get_current_user)):
        return await _list_owner_safe_horses(user)

    def _strip_staff_note(row: Dict[str, Any]) -> Dict[str, Any]:
        """Owner-safe projection of a service_requests row — drops the
        manager-only staff_note field unconditionally."""
        cleaned = {k: v for k, v in (row or {}).items() if k != "staff_note"}
        return cleaned

    def _owner_visible_work_filter(horse: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "barn_id": horse["barn_id"],
            **extra,
            "$or": [
                {"owner_visible": True},
                {"visibility": {"$in": ["owner_visible", "shared_with_owner"]}},
            ],
        }

    def _safe_lesson_summary(row: Dict[str, Any], horse: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": row.get("id"),
            "horse_id": row.get("horse_id"),
            "horse_name": row.get("horse_name") or horse.get("name"),
            "trainer_id": row.get("trainer_id") or row.get("trainer_user_id"),
            "trainer_name": row.get("trainer_name"),
            "start_time": row.get("start_time"),
            "duration_min": row.get("duration_min"),
            "focus": row.get("focus"),
            "completed": bool(row.get("completed")),
        }

    def _safe_training_summary(row: Dict[str, Any], horse: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": row.get("id"),
            "horse_id": row.get("horse_id"),
            "horse_name": row.get("horse_name") or horse.get("name"),
            "trainer_id": row.get("trainer_id") or row.get("trainer_user_id"),
            "trainer_name": row.get("trainer_name"),
            "date": row.get("date"),
            "discipline": row.get("discipline"),
            "exercises": row.get("exercises"),
            "rating": row.get("rating"),
            "homework": row.get("homework"),
        }

    def _safe_plan_summary(row: Dict[str, Any], horse: Dict[str, Any]) -> Dict[str, Any]:
        data = row.get("data") or {}
        return {
            "id": row.get("id"),
            "horse_id": data.get("horse_id"),
            "horse_name": data.get("horse_name") or horse.get("name"),
            "trainer_id": data.get("trainer_user_id") or data.get("trainer_id"),
            "trainer_name": data.get("trainer_name"),
            "goal": data.get("goal"),
            "status": data.get("status") or "planned",
            "updated_at": row.get("updated_at"),
        }

    @router.get("/horse-ledger/{horse_id}/owner-summary")
    async def owner_summary(horse_id: str, user=Depends(get_current_user)):
        horse = await _load_horse_for_owner_or_404(horse_id, user)
        care_sections = await build_owner_safe_transfer_care_summary(db, horse)
        visible_sections = {
            "identity": _build_identity(horse, True),
            **care_sections,
            # Owner-safe health placeholder. The full owner health
            # projection lives in the main GET ledger; for the summary
            # endpoint we surface a single non-leaking signal.
            "health":          {"status": "up_to_date"},
        }
        # Compute owner-safe care_status (strict precedence: alerts > requests > all_clear).
        # The active-alert lookup returns only "is there any?" — zero
        # detail crosses the boundary.
        role = (user.get("role") or "").strip().lower()
        owner_uid = (user.get("id") if role in {"horse_owner", "parent"}
                     else (horse.get("primary_owner_id") or horse.get("owner_id") or ""))
        care_status = "all_clear"
        active_alert = await db.horse_ledger_alerts.find_one(
            {"horse_id": horse_id, "barn_id": horse["barn_id"],
             "status": {"$in": ["open", "acknowledged"]}},
            {"_id": 0, "id": 1},
        )
        if active_alert:
            care_status = "barn_reviewing"
        elif owner_uid:
            open_req = await db.service_requests.find_one(
                {"horse_id": horse_id, "barn_id": horse["barn_id"],
                 "source": "owner_care_ledger",
                 "owner_user_id": owner_uid,
                 "status": {"$in": ["new", "in_progress"]}},
                {"_id": 0, "id": 1},
            )
            if open_req:
                care_status = "follow_up_available"
        # Calm summary cards — server-side derived labels only.
        def _card(key, label, struct):
            if struct is None:
                return {"key": key, "label": label, "status": "hidden",
                        "message": "Operational — staff only."}
            return {"key": key, "label": label, "status": "up_to_date",
                    "message": "Up to date."}
        cards = [
            _card("identity",        "Identity",         visible_sections["identity"]),
            _card("feeding",         "Feeding",          visible_sections["feeding"]),
            _card("hay_access",      "Hay & access",     visible_sections["hay_access"]),
            _card("turnout",         "Turnout",          visible_sections["turnout"]),
            _card("riding_training", "Riding & training", visible_sections["riding_training"]),
            _card("equipment",       "Equipment",        visible_sections["equipment"]),
            _card("health",          "Health",           visible_sections["health"]),
        ]
        # Owner's recent requests (own only — even when called by staff preview).
        recent_requests: List[Dict[str, Any]] = []
        if owner_uid:
            rows = await db.service_requests.find(
                {"horse_id": horse_id, "barn_id": horse["barn_id"],
                 "source": "owner_care_ledger", "owner_user_id": owner_uid},
                {"_id": 0},
            ).sort("created_at", -1).to_list(10)
            recent_requests = [_strip_staff_note(r) for r in rows]
        owner_lessons = await db.lessons.find(
            _owner_visible_work_filter(horse, {"horse_id": horse_id}),
            {"_id": 0},
        ).sort("start_time", 1).to_list(6)
        owner_training = await db.training.find(
            _owner_visible_work_filter(horse, {"horse_id": horse_id}),
            {"_id": 0},
        ).sort("date", -1).to_list(6)
        owner_plans = await db.training_plans.find(
            _owner_visible_work_filter(horse, {"data.horse_id": horse_id}),
            {"_id": 0},
        ).sort("updated_at", -1).to_list(6)
        payload = {
            "horse_id":             horse_id,
            "generated_at":         datetime.now(timezone.utc).isoformat(),
            "care_status":          care_status,
            "summary_cards":        cards,
            "visible_sections":     visible_sections,
            "recent_owner_updates": [],  # reserved for a future phase
            "training_summary": {
                "upcoming_lessons": [_safe_lesson_summary(r, horse) for r in owner_lessons if not r.get("completed")],
                "recent_training":  [_safe_training_summary(r, horse) for r in owner_training],
                "active_plans":     [_safe_plan_summary(r, horse) for r in owner_plans],
            },
            "recent_owner_requests":recent_requests,
            "request_options": {
                "request_type":      sorted(_OWNER_REQUEST_TYPES),
                "preferred_contact": sorted(_OWNER_CONTACT),
                "message_max":       _OWNER_MSG_MAX,
            },
        }
        # _scrub_strings handles Stripe-shape redaction on every string.
        return _scrub_strings(payload)

    @router.post("/horse-ledger/{horse_id}/owner-service-requests")
    async def create_owner_request(horse_id: str, body: Dict[str, Any],
                                   user=Depends(get_current_user)):
        # Owner/guardian create. Staff/admin previewing the owner page
        # does NOT get write access here.
        role = (user.get("role") or "").strip().lower()
        if role not in {"horse_owner", "parent"}:
            raise HTTPException(403, "Owner/guardian-only.")
        horse = await _load_horse_for_owner_or_404(horse_id, user)
        if not isinstance(body, dict):
            raise HTTPException(422, "Body must be an object.")
        allowed = {"request_type", "message", "preferred_contact"}
        bad = [k for k in body if k not in allowed]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        rt = body.get("request_type")
        if rt not in _OWNER_REQUEST_TYPES:
            raise HTTPException(422, "request_type invalid.")
        pc = body.get("preferred_contact")
        if pc is not None and pc not in _OWNER_CONTACT:
            raise HTTPException(422, "preferred_contact invalid.")
        msg = body.get("message")
        if not isinstance(msg, str) or not msg.strip():
            raise HTTPException(422, "message is required.")
        if len(msg) > _OWNER_MSG_MAX:
            raise HTTPException(422, f"message too long (max {_OWNER_MSG_MAX}).")
        # Rate-limit: 5 per (owner, horse) per rolling 1h.
        cutoff = datetime.now(timezone.utc).timestamp() - _OWNER_RATE_WINDOW_S
        cutoff_iso = datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat()
        recent = await db.service_requests.count_documents({
            "source": "owner_care_ledger",
            "owner_user_id": user["id"], "horse_id": horse_id,
            "created_at": {"$gte": cutoff_iso},
        })
        if recent >= _OWNER_RATE_CAP:
            raise HTTPException(429, "Too many requests. Please try again later.")
        now_iso = datetime.now(timezone.utc).isoformat()
        rid = f"osr_{uuid.uuid4().hex[:24]}"
        doc = {
            "id": rid,
            "source": "owner_care_ledger",
            "horse_id": horse_id, "barn_id": horse["barn_id"],
            "owner_user_id": user["id"],
            "request_type": rt,
            "message": msg,
            "preferred_contact": pc or "app",
            "status": "new",
            "created_at": now_iso, "updated_at": now_iso,
            "resolved_at": None, "resolved_by_user_id": None,
            "staff_note": None,
        }
        await db.service_requests.insert_one(doc)
        return {"ok": True, "id": rid}

    @router.get("/horse-ledger/{horse_id}/owner-service-requests")
    async def list_owner_requests(horse_id: str, user=Depends(get_current_user)):
        # Owner/guardian sees own; manager/admin sees all owner-care
        # requests on the horse. Other staff → 404 (founder lock #6 —
        # no assigned-staff visibility in 1-E).
        horse = await db.horses.find_one({"id": horse_id}, {"_id": 0})
        if not horse:
            raise HTTPException(404, "Not found.")
        role = (user.get("role") or "").strip().lower()
        if horse.get("barn_id") != user.get("barn_id"):
            raise HTTPException(404, "Not found.")
        q: Dict[str, Any] = {
            "horse_id": horse_id, "barn_id": horse["barn_id"],
            "source": "owner_care_ledger",
        }
        owner_response = False
        if role in {"horse_owner", "parent"}:
            if not _can_use_owner_request_contract(user, horse):
                raise HTTPException(404, "Not found.")
            q["owner_user_id"] = user["id"]
            owner_response = True
        elif role in {"admin", "barn_manager"}:
            pass  # full barn-scoped view
        else:
            raise HTTPException(404, "Not found.")
        rows = await db.service_requests.find(q, {"_id": 0}) \
            .sort("created_at", -1).to_list(50)
        if owner_response:
            rows = [_strip_staff_note(r) for r in rows]
        return _scrub_strings({"items": rows})

    @router.patch("/horse-ledger/{horse_id}/owner-service-requests/{rid}")
    async def patch_owner_request(horse_id: str, rid: str,
                                  body: Dict[str, Any],
                                  user=Depends(get_current_user)):
        role = (user.get("role") or "").strip().lower()
        if role not in {"admin", "barn_manager"}:
            raise HTTPException(403, "Manager-only.")
        horse = await db.horses.find_one({"id": horse_id}, {"_id": 0})
        if not horse or horse.get("barn_id") != user.get("barn_id"):
            raise HTTPException(404, "Not found.")
        existing = await db.service_requests.find_one(
            {"id": rid, "horse_id": horse_id, "barn_id": horse["barn_id"],
             "source": "owner_care_ledger"}, {"_id": 0},
        )
        if not existing:
            raise HTTPException(404, "Not found.")
        if not isinstance(body, dict) or not body:
            raise HTTPException(422, "Empty body.")
        allowed = {"status", "staff_note"}
        bad = [k for k in body if k not in allowed]
        if bad:
            raise HTTPException(422, f"Field not editable: {bad[0]!r}")
        new_status = body.get("status")
        if new_status is not None and new_status not in _OWNER_STATUS:
            raise HTTPException(422, "status invalid.")
        if "staff_note" in body and body["staff_note"] is not None:
            sn = body["staff_note"]
            if not isinstance(sn, str):
                raise HTTPException(422, "staff_note must be string.")
            if len(sn) > _STAFF_NOTE_MAX:
                raise HTTPException(422, f"staff_note too long (max {_STAFF_NOTE_MAX}).")
        updates: Dict[str, Any] = {}
        if new_status is not None and new_status != existing.get("status"):
            if (existing.get("status"), new_status) not in _OWNER_VALID_TRANS:
                raise HTTPException(
                    422,
                    f"Invalid transition {existing.get('status')!r} → {new_status!r}.",
                )
            updates["status"] = new_status
            if new_status == "resolved":
                updates["resolved_at"] = datetime.now(timezone.utc).isoformat()
                updates["resolved_by_user_id"] = user.get("id")
            elif existing.get("status") == "resolved":
                # Reopening clears resolved bookkeeping.
                updates["resolved_at"] = None
                updates["resolved_by_user_id"] = None
        if "staff_note" in body:
            updates["staff_note"] = body["staff_note"]
        if not updates:
            raise HTTPException(422, "No editable changes.")
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.service_requests.update_one({"id": rid}, {"$set": updates})
        return {"ok": True}

    return router
