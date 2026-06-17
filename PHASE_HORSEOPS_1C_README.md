# Phase HorseOps-1C — Staff Daily Checks via Existing Tasks Engine

Scope summary, integration story, review checklist.

---

## Codex Round-2 fixes (Feb 2026) — applied

| Finding | Fix |
|---|---|
| Stale `check_time` indexes were not actually dropped by code | `core/lifespan.py` now runs an idempotent migration *before* creating the new `checked_at`-aligned indexes. The known legacy names (`horse_id_1_check_time_-1`, `barn_id_1_check_type_1_check_time_-1`) are passed to `drop_index` inside a try/except, so cold deploys (no stale indexes) and warm deploys (legacy indexes present) both end at the same final state. Two new regressions: `test_stale_check_time_indexes_dropped_on_startup` (asserts the seed→drop→create dance ends with `checked_at`-only indexes), and `test_migration_is_idempotent_when_no_stale_indexes_present` (asserts repeated drops do not raise). |
| Payload section was not tied to `check_type` | New `_CHECK_TYPE_PAYLOAD_SECTION` mapping (`feed→feed`, `hay→hay_access`, `hay_net→hay_net`, `water→water`, `bedding→bedding`, `general→general`) enforced inside `_validate_check_payload(payload, check_type=...)`. POST passes the body's `check_type`; PATCH passes the existing log's `check_type` (it's immutable on PATCH so the mapping is stable). New parametrized regressions: `test_payload_section_must_match_check_type_422` (7 cross-section combinations all 422), `test_payload_section_matching_check_type_accepted` (6 paired-section happy paths all 200), and `test_patch_payload_section_must_match_existing_check_type_422` (asserts PATCH cannot smuggle a mismatched section even after creation). |

Both fixes are non-breaking — owner hard-hide, hybrid permissions, PATCH author-or-manager scope, and audit-row schema are byte-identical to round-1.

---

## Codex Round-1 fixes (Feb 2026) — applied

| Finding | Fix |
|---|---|
| `task_id` validation used wrong scope | Real tasks materialized by `task_engine.py` carry `tenant_id="default"` + `barn_id=<barn_id>`. The 1-C lookup was filtering by `tenant_id == horse["barn_id"]`, which rejects every real same-barn task. Now queries by `barn_id` only. Added `test_task_linkage_real_task_engine_shape_persists` regression that seeds a task with the exact engine shape. |
| Daily-check indexes referenced the wrong field | 1-A indexed `check_time`, but 1-C writes/queries `checked_at`. `core/lifespan.py` now creates four named, `checked_at`-aligned indexes — `hdcl_horse_checked_at`, `hdcl_barn_horse_checked_at`, `hdcl_barn_check_type_checked_at`, `hdcl_task_id` (sparse). Stale `check_time` indexes are dropped on existing deployments by listing + dropping legacy names. Regression `test_daily_check_indexes_exist_and_use_checked_at` pins the live state. |

Both fixes are non-breaking — owner hard-hide, hybrid permissions, PATCH author-or-manager scope, and audit-row schema are byte-identical to the round-0 package.

---

## Scope (locked plan)

Three endpoints under the Care Ledger surface — **no new scheduler, no new alert worker, no parallel task system**:

| Endpoint | Purpose |
|---|---|
| `POST /api/horse-ledger/{horse_id}/daily-checks` | Create one observation log |
| `GET /api/horse-ledger/{horse_id}/daily-checks` | List recent (staff/manager only) |
| `PATCH /api/horse-ledger/{horse_id}/daily-checks/{check_id}` | Append amendment by author or manager |

All three live in `routes/horse_ledger.py` and inherit:
- `PRODUCT_FACILITY_DEPS` (Admin-4b disabled-facility gate)
- `_load_horse_or_404` (barn-scoped, no platform bypass)
- `_scrub_strings` on all outbound payloads (Stripe-shape redaction)

---

## Task-engine integration story

The existing `task_engine.py` retains recurring scheduling for `feed`, `stall_clean`, `turnout_*`, `medication`, etc.

Daily checks are an **immutable observation log layered on top**:
- `horse_daily_check_logs` rows may carry an optional `task_id` (FK back into `tasks`) for trail linkage.
- Linking a check to a task does **NOT** auto-complete the task. The task lifecycle is unchanged. No `payload_actual` writes. No scheduler changes.
- An ad-hoc mid-day water check or opportunistic hay-net refill simply omits `task_id`.

This deliberately keeps the task engine the recurring scheduler and the check log the observation surface.

---

## Schema — `horse_daily_check_logs`

```
{
  id:                "hdcl_<uuid>",
  horse_id:          str,
  barn_id:           str,                      // copied from horse
  task_id:           str | null,               // optional FK
  check_type:        "feed"|"hay"|"hay_net"|"water"|"bedding"|"general",
  status:            "ok"|"needs_attention"|"missed"|"not_applicable",
  notes:             str | null,               // staff-only, 500 char cap, NEVER owner-visible
  payload: {
    hay_net?:    {nets_checked, nets_refilled, hay_net_id},
    hay_access?: {free_choice_available, exception},
    water?:      {bucket_ok, automatic_waterer_ok, refilled},
    feed?:       {given, missed_reason, amount_value, amount_unit},
    bedding?:    {condition: "clean|damp|soiled", top_off_needed, full_strip_needed},
    general?:    {observation},
  },
  created_at:        iso8601,
  checked_at:        iso8601,
  checked_by_user_id:str,
  amended_at:        iso8601 | null,           // PATCH only sets this
}
```

Payload subkeys are strictly whitelisted in `_CHECK_PAYLOAD_SUBKEYS`. Values must be primitives. `bedding.condition` is enum-constrained.

---

## Permissions (hybrid mutator gate)

| Role | Create | List | PATCH |
|---|---|---|---|
| `admin`, `barn_manager` | ✅ | ✅ | ✅ any in-barn log |
| `groom`, `trainer`, `vet`, `staff` | ✅ | ✅ | ✅ only their own logs |
| `horse_owner` | ❌ 403 | ❌ 403 | ❌ 403 |
| Cross-barn (any role) | 404 | 404 | 404 |

PATCH amender check: `role ∈ {admin, barn_manager} || existing.checked_by_user_id == user.id`.

---

## Privacy model — hard-hidden from owners

- `GET /api/horse-ledger/{horse_id}` for an owner returns `daily_checks_recent: []` always.
- `?view=staff`, `?view=full`, etc. cannot escalate an owner — the same fail-closed branching as 1-A.
- `_FORBIDDEN_OWNER_KEYS["daily_checks_recent"] = {"*"}` — `PUT /owner-visibility-policy` 422s any attempt to expose the section, even with a manager token.
- A tampered policy doc planted directly in Mongo with `daily_checks_recent.allowlist` still produces an empty list for owners (the read path doesn't consult the policy for this section).
- `_scrub_strings` on the GET response redacts any Stripe-shaped substring (`sub_…`, `cus_…`, `evt_…`) in `notes`.

---

## Audit (`horse_ledger_audit`)

Every successful create + update emits one row:
- `section: "daily_checks"`
- `action: "created" | "updated"`
- `field_paths`: keys only, including nested `payload.<section>.<subkey>` paths
- `sensitivity: "operational"` for `feed` checks, `"staff_only"` for everything else
- `owner_visible_eligible: false` always (daily checks are never owner-visible in 1-C, even for `feed`)
- **No raw `notes`, no payload values, no before/after, no 403 audit rows.**

---

## Test coverage

`/app/backend/tests/test_horse_ledger_1c.py` — **73 cases** (55 round-0 + 2 round-1 + 16 round-2 regressions). Full Care-Ledger suite **203 passing** (29 1-A + 101 1-B + 73 1-C). Backend + JSX lint clean.

### Permissions (8)
- `test_staff_and_managers_can_create_daily_check` × 6 (parametrized over admin/barn_manager/groom/trainer/vet/staff)
- `test_owner_cannot_create_daily_check`
- `test_cross_barn_user_cannot_create_daily_check`
- `test_cross_barn_user_cannot_list_daily_checks`
- `test_owner_cannot_list_daily_checks`
- `test_disabled_facility_blocks_daily_check_create`

### Validation (~15)
- `test_invalid_check_type_422` × 5
- `test_invalid_status_422` × 4
- `test_unknown_top_level_field_422`
- `test_unknown_payload_subkey_422`
- `test_unknown_payload_section_422`
- `test_bedding_condition_enum_422` × 4
- `test_payload_non_primitive_value_422`
- `test_notes_length_cap_422`

### Task linkage (4)
- `test_task_linkage_same_barn_persists_task_id` (also asserts task lifecycle untouched)
- `test_task_linkage_real_task_engine_shape_persists` *(Round-1 regression: real tasks carry `tenant_id="default"` + `barn_id=<bid>` — validation queries by `barn_id` only)*
- `test_task_linkage_cross_barn_422`
- `test_task_linkage_unknown_task_422`

### PATCH amendments (8)
- `test_author_can_amend_their_own_check` (asserts `checked_at` preserved, `amended_at` set)
- `test_non_author_staff_cannot_amend`
- `test_manager_can_amend_any_check`
- `test_admin_can_amend_any_check`
- `test_owner_cannot_amend_any_check`
- `test_patch_unknown_check_id_404`
- `test_patch_unknown_field_422` (check_type immutable on PATCH)
- `test_patch_merges_payload_subkeys`

### Read integration (7)
- `test_staff_get_ledger_includes_daily_checks_recent`
- `test_owner_get_ledger_hides_daily_checks_recent`
- `test_owner_cannot_force_reveal_via_view_query`
- `test_owner_cannot_force_reveal_via_tampered_policy_doc`
- `test_policy_put_rejects_daily_checks_section`
- `test_list_daily_checks_filters_by_check_type`
- `test_list_daily_checks_invalid_filter_422`

### Audit (4)
- `test_audit_row_emitted_on_create` (raw notes + values NOT in audit; no `before`/`after`/`values`/`payload_actual` keys)
- `test_audit_row_emitted_on_patch`
- `test_no_audit_row_on_403`
- `test_feed_check_audit_sensitivity_is_operational` (still `owner_visible_eligible: false`)

### Stripe scrubbing (1)
- `test_stripe_shape_in_notes_scrubbed_on_get`

### Adjacent-phase invariants (4)
- `test_phase_9_collections_untouched_after_1c_storm`
- `test_phase_15_collections_untouched_after_1c_storm`
- `test_admin_portal_route_lock_unchanged_after_1c`
- `test_daily_check_indexes_exist_and_use_checked_at` *(Round-1 regression: 1-A's planned `check_time` indexes were renamed/aligned to the live `checked_at` field; this test pins the four current indexes — `hdcl_horse_checked_at`, `hdcl_barn_horse_checked_at`, `hdcl_barn_check_type_checked_at`, `hdcl_task_id` — and asserts no stale `check_time` indexes remain)*

### Cross-suite
- Full 1-A regression suite (29) green after 1-C ships.
- Full 1-B regression suite (101) green after 1-C ships.

---

## Frontend

`/app/frontend/src/pages/CareLedgerTab.jsx`:
- New `DailyChecksSection` component, rendered only for `STAFF_ROLES = {admin, barn_manager, groom, trainer, vet, staff}` AND non-owner view.
- 5 quick-action chips (Feed given · Hay checked · Hay net refilled · Water checked · Bedding checked) + a "+ Note" general chip.
- Recent list (timestamp · checker · `check_type` badge · `status` badge using the equine palette: `brass` for OK, `silver` for needs_attention, `platinum` for missed, muted for N/A — **no red/orange/amber/yellow**).
- Per-row "Amend" affordance shown only when role is manager OR the row's `checked_by_user_id` matches the current user.
- `DailyCheckDrawer` (new + amend) reuses the existing `Drawer` primitive. Conditional sub-payload fields by `check_type`. Notes textarea labeled "Notes (staff-only — never shown to owners)".
- Owner UI: completely unchanged. No Daily Checks section, no edit affordances.

All interactive elements carry stable `data-testid` attributes (`daily-check-quick-<type>`, `daily-check-row-<id>`, `daily-check-amend-<id>`, `daily-check-drawer-status`, `daily-check-payload-<section>-<key>`, `daily-check-status-<status>`).

---

## Deferred / out of scope

- **Alerts / escalations / history** — HorseOps-1D.
- **Owner-facing filtered view** — HorseOps-1E.
- **Barn-wide owner-visibility template** — HorseOps-1B.1 (approved as future scope).
- **Curated schedule-shape picker** for the manager drawer — UX polish item alongside the template.
- Native mobile, breeding/pedigree, inventory depletion, purchasing, vendor ordering, cost accounting, Phase 16 — all unchanged.

---

## Files in this delta package (`/app/phase_horseops_1c_changes.zip`)

- `backend/routes/horse_ledger.py` — 3 new endpoints + helpers + audit hook + `daily_checks_recent` populated for staff
- `backend/tests/test_horse_ledger_1c.py` — 55 new tests
- `frontend/src/pages/CareLedgerTab.jsx` — `DailyChecksSection` + `DailyCheckDrawer`
- `memory/PRD.md` — running phase ledger
- `PHASE_HORSEOPS_1C_README.md` — this file

---

## Review checklist (Codex)

- [x] Daily checks store-only — no task lifecycle coupling.
- [x] No new scheduler, no new alert worker.
- [x] Hybrid mutator gate (staff create, author+manager amend).
- [x] Owners 403 on every mutation, `daily_checks_recent: []` on every read.
- [x] Owner-visibility policy PUT 422s `daily_checks_recent` section.
- [x] Tampered policy doc cannot force owner reveal.
- [x] Validation rejects unknown top-level fields, unknown payload sections, unknown payload subkeys, non-primitive values, bad enums, oversize notes.
- [x] Task linkage requires same-barn task; cross-barn → 422; unknown task → 422.
- [x] Audit row schema unchanged from 1-B (`field_paths` only, no raw values, no 403 rows).
- [x] `_scrub_strings` runs on the daily-check list response.
- [x] Phase 9 / Phase 15 / Admin Portal collections byte-identical after a 1-C edit storm.
- [x] 1-A and 1-B regressions still green (185/185 across the Care-Ledger suite).
- [x] Frontend palette is equine-tokens only — no red/orange/amber/yellow.
