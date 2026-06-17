# Phase HorseOps-1A — Care Ledger (Read-Only Composition)

**Status:** ✅ Codex-approved & locked (Mar 01 2026)
**Date:** Feb 28 2026  (round-1 fixes + lock: Mar 01 2026).
**Scope:** Backend (FastAPI) + Horse Detail frontend tab + tests + indexes only.

## Codex Round-1 fix highlights (Mar 01 2026)

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| R1-A | **P1** | Owner view exposed the full legacy `horses.feed_plan` free-text string, which can carry prep instructions, soaking details, medication notes, or staff-only handling warnings. | `_build_feeding()` in `routes/horse_ledger.py` now drops `legacy` entirely in the owner envelope. If a structured profile exists, the owner sees a strict whitelist (`grain_feed_type`, `schedule`, `supplements[name only]`); if not, the owner sees `feeding: null`. Staff view is unchanged — managers still see the legacy free text via the `{ structured, legacy }` envelope. |
| R1-B | **P1** | Owner view returned `wellness[0]` raw, leaking any staff notes / actor fields / internal observations stored on the wellness row. | `_build_health()` now projects `wellness_latest` to an explicit owner-safe allowlist: `id`, `created_at`, `status`, `score`, `summary`. Every other field from the raw doc is dropped. Staff view continues to receive the full document. |

**New tests (2 added → 29 total):**
- `test_r1_owner_view_does_not_expose_legacy_feed_plan_free_text` — plants `STAFF ONLY: soak / Give bute / WARNING / bites` into the legacy `feed_plan`, asserts owner view contains none of those strings, asserts staff view still contains them.
- `test_r1_owner_view_wellness_projects_to_safe_allowlist_only` — plants 6 staff-only fields (`staff_note`, `internal_observation`, `actor_user_id`, `actor_name`, `_internal_flag`, `raw_vet_dictation`) on a wellness row; asserts the owner-projected `wellness_latest` carries ONLY `{id, created_at, status, score, summary}` and none of the secret strings appear anywhere in the response body. Staff view is unchanged.

## What ships

| File | Purpose |
|------|---------|
| `backend/routes/horse_ledger.py` | **NEW** — Read-only composed-Ledger endpoint `GET /api/horse-ledger/{horse_id}`. Role-driven fail-closed shape. |
| `backend/core/lifespan.py` | Adds 15 indexes for the 8 new HorseOps collections (idempotent `create_index`). |
| `backend/server.py` | Wires the new router with `dependencies=PRODUCT_FACILITY_DEPS` (the Admin-4b enforcement line). |
| `backend/tests/test_horse_ledger_1a.py` | **NEW** — 27 tests covering read shape, barn scoping, Admin-4b enforcement, fail-closed owner semantics, no-Stripe-leak, no-billing-keys, no-writes-in-1A, Phase 9/15/Admin-portal untouched, inventory untouched, index existence, zero-document-writes guard. |
| `frontend/src/pages/CareLedgerTab.jsx` | **NEW** — Read-only "Care Ledger" tab on the existing Horse Detail page. |
| `frontend/src/pages/HorseProfile.jsx` | One-line additive change — adds the new tab. No removal/relocation. |

## Endpoint surface (1-A)

| Method | Path | Roles | Description |
|--------|------|-------|-------------|
| `GET`  | `/api/horse-ledger/{horse_id}` | barn-scoped roles in the SAME barn as the horse | Composed read. Server-side shape is **role-driven, fail-closed**. |

## Role table (1-A)

| Caller | Response |
|--------|----------|
| Barn-scoped non-owner role (`admin`, `barn_manager`, `groom`, `vet`, `trainer`, `staff`) in the same barn | full staff/manager view |
| `horse_owner` whose `id` is in `(primary_owner_id, secondary_owner_ids[])` of the horse | **always** owner-filtered view, regardless of query string |
| `horse_owner` who is NOT an owner of the horse | **404** (non-enumerating) |
| Any caller in a different barn | **404** (non-enumerating) |
| Platform admin (`super_admin`, `platform_admin`, etc.) whose own `barn_id` matches the horse | full staff/manager view (treated as a barn member; no cross-facility privilege from this route) |
| Disabled-facility non-platform caller | **403 "Facility unavailable"** (Admin-4b gate) |
| Disabled-facility platform caller | passes through (Admin-4b R1-C bypass for KNOWN `PLATFORM_ROLES`) |

## Δ1 — Owner access is FAIL-CLOSED

Per founder direction: `?view=owner` is a display hint **only**. The server-side response shape is decided from `user.role` + ownership + barn scoping. **No query string can escalate.**

Verified by:
- `test_horse_owner_in_owner_set_gets_owner_view_regardless_of_query_string` — 6 different `?view=` values all return owner shape.
- `test_horse_owner_without_view_param_still_gets_owner_filtered_view` — no query string at all.
- `test_horse_owner_cannot_force_staff_view` — 8 escalation attempts (`?view=staff`, `?view=full`, `?view=manager`, `?view=admin`, `?view=STAFF`, `?view=`, `?view=staff&view=owner`, `?notreal=1&view=staff`) — every variant returns owner shape.

## Δ2 — Platform-role access (clarified for 1-A)

The product route `/api/horse-ledger/{horse_id}` is **barn-scoped**. The Admin-4b platform-role bypass is for the disabled-facility GATE only — **barn scoping is NOT bypassed**.

A `platform_admin` in barn A requesting a horse in barn B receives 404, same as any other caller. **Cross-facility platform Ledger inspection is explicitly deferred** to a future Admin Portal surface; not in any HorseOps-1A..1-E phase.

Verified by `test_platform_role_cannot_use_product_route_for_cross_barn_horse_in_1a`.

## Owner-visibility defaults (1-A hardcoded, conservative)

| Section | Owner default |
|---------|---------------|
| identity (name, breed, dob, color, markings, photo, primary_owner_id) | visible |
| identity.microchip / tattoo / registry / required_staff_experience | **hidden** |
| identity.secondary_owner_ids / emergency_contact_ids / document_ids | **hidden** |
| feeding (type + schedule + supplement names) | visible |
| feeding.prep / soaking / staff_only_warnings / sensitivities / meds_with_feed | **hidden** |
| hay_access (type + frequency) | visible |
| hay_access.restriction_flags / staff_only_warnings / hay_nets | **hidden** |
| stall_bedding (entire section) | **hidden** |
| turnout.schedule + group | visible |
| turnout.avoid_list / injury_risk_notes / catching_notes | **hidden** |
| handling_behavior (entire section) | **hidden** |
| riding_training | visible |
| equipment | visible (summary) |
| service_providers (entire section) | **hidden in owner view** |
| health.medications | visible (name + dosage + frequency; staff-only warnings stripped) |
| health.injuries / vet_records / wellness | visible (title + date) |
| daily_checks_recent / alerts_open / audit_recent | empty in 1-A by construction |

Verified by tests 10-14.

## Indexes (15)

Created on backend startup via the existing `ensure_indexes` flow in `core/lifespan.py`. **Index creation MAY create empty collections in Mongo as a side-effect; 1-A writes ZERO documents** (verified by `test_no_documents_written_to_horse_ledger_collections_in_1a`).

```
horse_care_profiles            { horse_id: 1 }               unique
horse_care_profiles            { barn_id: 1 }
horse_equipment                { horse_id: 1 }
horse_equipment                { barn_id: 1, category: 1 }
service_providers              { barn_id: 1, category: 1 }
horse_provider_assignments     { horse_id: 1 }
horse_provider_assignments     { barn_id: 1, next_due_date: 1 }
horse_daily_check_logs         { horse_id: 1, check_time: -1 }
horse_daily_check_logs         { barn_id: 1, check_type: 1, check_time: -1 }
horse_ledger_alerts            { horse_id: 1, opened_at: -1 }
horse_ledger_alerts            { barn_id: 1, severity: 1, closed_at: 1 }
horse_owner_visibility_policy  { horse_id: 1 }               unique
horse_ledger_audit             { horse_id: 1, ts: -1 }
horse_ledger_audit             { barn_id: 1, ts: -1 }
horse_ledger_audit             { actor_user_id: 1, ts: -1 }
```

## Admin-4b enforcement wiring (exact line)

`backend/server.py` (locked):

```python
# Phase HorseOps-1A — composed read-only Care Ledger endpoint.
api_router.include_router(
    build_horse_ledger_router(db=db, get_current_user=get_current_user),
    dependencies=PRODUCT_FACILITY_DEPS,        # ← Admin-4b gate
)
```

Removing the `dependencies=PRODUCT_FACILITY_DEPS` line silently disables the gate. `test_get_ledger_disabled_facility_gate_applies` is the regression guard.

This adds the HorseOps router to the **applied-strict** inventory in `PHASE_ADMIN_4B_README.md` — totals become **19 strict + 2 optional-auth + 7 excluded**.

## Composition rule: legacy + structured envelope

When a section may carry both a legacy field (from `horses`) and a structured field (from `horse_care_profiles`):

```json
{
  "feeding": { "structured": null,                 "legacy": "Standard ration AM/PM" },
  "turnout": { "structured": {...},                "legacy": "Group A" },
  "riding_training": { "structured": null,         "legacy": "Second Level" }
}
```

Legacy is **never overwritten, never normalised, never dropped**. Staff can review transition data without losing the original string.

## Tests (29/29 green)

```bash
pytest backend/tests/test_horse_ledger_1a.py        # 29 passed   ⭐ NEW (incl. round-1 R1-A/B)
```

Test coverage map:
- 1-9 — Read shape + barn scoping + Admin-4b enforcement + role table.
- 10-14 — Owner-filtered shape (identity-private hidden, behavior hidden, bedding hidden, cross-owner 404, owner-safe health visible).
- 15-16 — No Stripe-shape leak / no billing-adjacent keys.
- 17-18 — Phase 9 + Phase 15 collections byte-identical before/after.
- 19 — Admin portal route lock unchanged (26 GET + 10 POST + 1 PATCH).
- 20 — Static AST guard: no `insert_*`/`update_*`/`delete_*`/`replace_*`/`bulk_write` calls in `routes/horse_ledger.py`.
- 21 — `horses` doc byte-identical after a Ledger read.
- 22 — All 15 HorseOps indexes exist.
- 23 — `inventory`, `service_requests`, `staff_invites`, `payment_profiles` untouched.
- 24-25 — Δ1 fail-closed: owner shape regardless of query string.
- 26 — Δ2: platform admin cannot cross-barn-inspect via the product route.
- 27 — Index creation writes zero documents into any of the 8 new collections.
- 28 (R1-A) — Owner view does not expose legacy `feed_plan` free text; staff view still does.
- 29 (R1-B) — Owner `wellness_latest` projected to a strict 5-key allowlist (`id`, `created_at`, `status`, `score`, `summary`); planted staff-only fields are not leaked.

## Locked guardrails honoured

- [x] Read-only (AST-verified — no DB writes in 1-A).
- [x] No Phase 9 / Phase 15 logic changes.
- [x] No Admin Portal route / lock-list / capability changes.
- [x] No landing-page changes.
- [x] No `inventory` / `service_requests` / billing collections touched.
- [x] Color palette unchanged.
- [x] Existing horse PATCH still works; legacy fields preserved.

## Codex review checklist

- [ ] `GET /api/horse-ledger/{horse_id}` returns the composed shape for barn members.
- [ ] `horse_owner` ALWAYS gets owner-filtered shape, no query string can escalate.
- [ ] Owners cannot read another owner's horse.
- [ ] Cross-barn caller (any role) gets 404; platform admin not exempt.
- [ ] Disabled facility → 403 "Facility unavailable"; verified at the include_router line.
- [ ] No Stripe-shaped substring surfaces in any response field.
- [ ] No billing-adjacent keys (`balance`, `due_amount`, `subscription_id`, etc.) in the response.
- [ ] Index creation creates the 8 collections empty; 1-A writes zero documents.
- [ ] Legacy `horses` fields still render via the `{ structured, legacy }` envelope.

## What's deferred (locked — not in any HorseOps-1A..1-E phase)

- Inventory depletion.
- Purchasing / vendor ordering / cost accounting / billing tie-ins.
- IoT sensors.
- Native mobile app.
- Foal / breeding pedigree linking.
- Per-barn customisable owner-visibility templates.
- Full-payload audit diff endpoint.
- Weekly recap of Ledger changes.
- **Cross-facility platform Ledger inspection** (future Admin Portal surface).
