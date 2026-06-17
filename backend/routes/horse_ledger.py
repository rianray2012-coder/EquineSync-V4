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


def _project_schedule(schedule: Any) -> List[Any]:
    """Owner-safe schedule projection: list of strings/dicts retained
    as-is, but bounded to primitives so nested staff notes can't ride
    along."""
    if not isinstance(schedule, list):
        return []
    out = []
    for item in schedule:
        if isinstance(item, (str, int, float, bool)):
            out.append(item)
        elif isinstance(item, dict):
            # Only carry primitive keys; reject nested dicts.
            out.append({k: v for k, v in item.items()
                        if isinstance(v, (str, int, float, bool))})
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
            out[k] = _project_schedule(v)
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

            # 1-A: these arrive in later sub-phases. Always empty by
            # construction so the frontend can render placeholders.
            "daily_checks_recent": [],
            "alerts_open":         [],
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

    def _schedule_ok(value):
        """Schedule must be a list of primitives (str/number/bool) or
        primitive-only dicts. No deeply nested structures so the
        owner-safe projection cannot carry over a staff note."""
        if not isinstance(value, list):
            return False
        for item in value:
            if isinstance(item, (str, int, float, bool)):
                continue
            if isinstance(item, dict):
                if not all(isinstance(v, (str, int, float, bool))
                           for v in item.values()):
                    return False
                continue
            return False
        return True

    _NESTED_VALIDATORS: Dict[str, Dict[str, Any]] = {
        "feeding": {
            "supplements": _supplements_ok,
            "schedule":    _schedule_ok,
        },
        "hay_access": {
            "hay_nets": _hay_nets_ok,
        },
        "turnout": {
            "schedule": _schedule_ok,
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

    @router.put("/horse-ledger/{horse_id}/owner-visibility-policy")
    async def put_visibility_policy(horse_id: str, body: Dict[str, Any],
                                    user=Depends(get_current_user)):
        horse = await _load_horse_or_404(horse_id, user)
        _require_mutator(user, horse)
        sections = (body or {}).get("sections")
        if not isinstance(sections, dict):
            raise HTTPException(422, "Body must contain `sections` object.")
        for section, spec in sections.items():
            if section not in _POLICY_SECTIONS:
                raise HTTPException(422, f"Unknown policy section: {section!r}")
            if not isinstance(spec, dict) or "allowlist" not in spec:
                raise HTTPException(422, f"Section {section!r} missing allowlist.")
            allowlist = spec["allowlist"]
            if not isinstance(allowlist, list):
                raise HTTPException(422, f"Allowlist for {section!r} must be a list.")
            for key in allowlist:
                if not isinstance(key, str):
                    raise HTTPException(422, f"Allowlist key must be string: {key!r}")
                if _is_forbidden_owner_key(section, key):
                    raise HTTPException(
                        422, f"Key {section}.{key!r} is forbidden for owner allowlist."
                    )
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
            field_paths=sorted(sections.keys()),
            sensitivity="operational",
        )
        return {"ok": True, "horse_id": horse_id,
                "sections": sorted(sections.keys())}

    # ---------------- equipment ----------------
    _EQUIPMENT_WRITABLE = {"category", "label", "brand", "size", "fit_notes",
                           "location", "restrictions", "cleaning_care_notes",
                           "saddle_fit_history", "status"}

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
        if body.get("status") and body["status"] not in {"active", "retired"}:
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
                          "address", "notes", "is_primary_for_barn", "status"}
    _ASSIGNMENT_WRITABLE = {"provider_id", "category", "last_service_date",
                            "next_due_date", "interval_days", "notes",
                            "is_primary_for_horse", "status"}

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
        # Provider must be in same barn.
        prov = await db.service_providers.find_one(
            {"id": body["provider_id"], "barn_id": horse["barn_id"]},
            {"_id": 0, "id": 1},
        )
        if not prov:
            raise HTTPException(404, "Provider not found.")
        import uuid as _uuid
        hpa_id = f"hpa_{_uuid.uuid4().hex[:24]}"
        await db.horse_provider_assignments.insert_one({
            **body, "id": hpa_id, "horse_id": horse_id,
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

    return router
