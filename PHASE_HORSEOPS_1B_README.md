# Phase HorseOps-1B — Care Ledger Manager Edit Flows + First Writes

Scope summary, review checklist, and round notes for Codex review.

---

## Scope (locked plan reminder)

5 first-write collections + audit:

| Endpoint | Collection written |
|---|---|
| `PATCH /api/horse-ledger/{horse_id}/care-profile` | `horse_care_profiles` |
| `PUT /api/horse-ledger/{horse_id}/owner-visibility-policy` | `horse_owner_visibility_policy` |
| `POST/PATCH /api/horse-ledger/{horse_id}/equipment[/{eq_id}]` | `horse_equipment` |
| `POST /api/horse-ledger/{horse_id}/service-providers` | `service_providers` |
| `POST/PATCH /api/horse-ledger/{horse_id}/provider-assignments[/{a_id}]` | `horse_provider_assignments` |

Every mutation also emits one row to `horse_ledger_audit` — `field_paths` only, no raw values, no notes, no 403 audit rows.

### Mutator gate
- `admin` and `barn_manager` only.
- Owners → **403**. Other staff roles (groom/trainer/vet/staff) → **403**.
- Cross-barn → **404**.

### Privacy model (backend-authoritative on every read)
- Owner GET reads the current `horse_owner_visibility_policy` doc.
- Per-section effective allowlist = `(policy.allowlist ∩ _OWNER_SAFE_KEYS[section]) ∪ _DEFAULT_OWNER_POLICY[section] \ FORBIDDEN`.
- Sections with no owner-exposable keys (`stall_bedding`, `handling_behavior`, `service_providers`) **never** surface to owners regardless of policy doc.
- Free-text legacy fields (`horses.feed_plan`, `horses.training_goals`, `horses.behavior_flags`) are dropped in the owner envelope.

---

## Round-1 fixes (Feb 2026) — applied

| Finding | Fix |
|---|---|
| P0 Owner-visibility policy stored but not applied on reads | `GET /horse-ledger/{id}` loads `horse_owner_visibility_policy` for owner view and projects each section via `_effective_owner_keys`. Policy edits/removal take effect on the very next GET. |
| P0 Newly writable riding/training fields could leak | `_build_riding_training` projects through `_project_owner_safe`; default safe keys = `discipline`, `current_level`, `competition_goals` only. `_FORBIDDEN_OWNER_KEYS["riding_training"]` adds `trainer_notes`, `exercise_restrictions`, `weekly_work_plan`, `rider_compatibility_notes`, `conditioning_plan`, `lesson_schedule`, `ride_schedule`. |
| P1 Validation only top-level | `_NESTED_VALIDATORS` enforces shape on `feeding.supplements`, `feeding.schedule`, `turnout.schedule`, `hay_access.hay_nets`. |
| P2 Unapproved color tokens (`rose-*`, `bg-black/60`) | Replaced with `text-equine-platinum/85`, `border-equine-silver/30`, `bg-equine-silver/5`, `bg-equine-black/70`. No red/orange/amber/yellow tokens remain in `CareLedgerTab.jsx`. |

---

## Round-2 fixes (Feb 2026) — applied

| Finding | Fix |
|---|---|
| P0 `feeding.schedule` / `turnout.schedule` could leak staff notes via primitive-keyed `staff_note` | New `_SCHEDULE_SUBKEYS` registry (`feeding`: `{time,label,amount}`; `turnout`: `{time,label,duration,paddock}`). `_schedule_ok(section, value)` 422s any subkey outside the registry at write time; `_project_schedule(section, schedule)` strips unknown subkeys at owner read time as defense-in-depth. |
| P1 Policy PUT accepted unknown allowlist keys | PUT `/owner-visibility-policy` now 422s on any key not in `_OWNER_SAFE_KEYS[section]`. Sections with no owner-exposable keys (`stall_bedding`, `handling_behavior`, `service_providers`) 422 outright. |
| P1 Loose status validation on equipment / provider / assignment | New enums: `_EQUIPMENT_STATUS = {active, retired}`, `_PROVIDER_STATUS = {active, archived}`, `_ASSIGNMENT_STATUS = {active, archived}`. Enforced on POST + PATCH for all three collections. |
| P2 Missing phase README | This file. |

---

## Test coverage

`/app/backend/tests/test_horse_ledger_1b.py` — **101 cases** (57 original + 20 Round-1 + 24 Round-2). Full Care-Ledger suite **130 passing** (29 in `test_horse_ledger_1a.py` + 101 in `test_horse_ledger_1b.py`).

### Round-1 regressions (20)
- `test_policy_removal_hides_previously_visible_safe_key`
- `test_policy_addition_shows_only_safe_allowed_keys`
- `test_tampered_policy_with_forbidden_key_stays_hidden_on_read`
- `test_riding_training_staff_only_fields_never_leak_to_owner` × 6 (parametrized)
- `test_default_owner_view_excludes_riding_training_staff_only_keys`
- `test_patch_care_profile_nested_shape_422` × 8 (parametrized)
- `test_patch_care_profile_nested_shape_accepts_well_formed`
- `test_owner_supplements_projection_drops_dosage_notes`

### Round-2 regressions (24)
- `test_schedule_dict_with_unknown_subkey_rejected_at_write` × 2 (feeding, turnout)
- `test_schedule_staff_note_stripped_on_owner_read_if_db_tampered` × 2 (feeding, turnout)
- `test_policy_put_rejects_unknown_allowlist_key`
- `test_policy_put_rejects_section_with_no_owner_exposable_keys` × 3 (stall_bedding, handling_behavior, service_providers)
- `test_policy_put_accepts_known_safe_keys`
- `test_equipment_post_rejects_bad_status` × 5
- `test_provider_post_rejects_bad_status` × 4
- `test_assignment_post_rejects_bad_status` × 4
- `test_assignment_patch_rejects_bad_status`
- `test_status_enum_happy_paths`

### Adjacent-phase invariants (still in the suite)
- `test_phase_9_collections_byte_identical_after_1b_edit_storm`
- `test_phase_15_collections_byte_identical_after_1b_edit_storm`
- `test_admin_portal_route_lock_unchanged_after_1b`

---

## Deferred / out of scope (do not include in 1-B)

- **Barn-wide owner-visibility template.** "Apply this owner-visibility policy to every horse in the barn" UI/endpoint. Approved as a future gated phase (likely `HorseOps-1B.1`) but explicitly excluded from this Round-2 package.
- **HorseOps-1C** — staff daily checks for hay nets, bedding, water, feed via the existing `tasks` engine.
- **HorseOps-1D** — alerts/escalations/history + staff experience-level blocks.
- **HorseOps-1E** — owner-facing filtered view (full UI + service-request flow).

---

## Files in this delta package (`/app/phase_horseops_1b_changes.zip`)

- `backend/routes/horse_ledger.py` — read + 1-B mutation logic.
- `backend/tests/test_horse_ledger_1b.py` — 101 tests.
- `frontend/src/pages/CareLedgerTab.jsx` — read view + manager-only drawers (admin/barn_manager).
- `memory/PRD.md` — running phase ledger.
- `PHASE_HORSEOPS_1B_README.md` — this file.

---

## Review checklist (Codex)

- [x] Mutators restricted to `admin` / `barn_manager`. Owners 403. Cross-barn 404.
- [x] Owner read loads the policy doc and re-projects every time.
- [x] No raw before/after in audit rows. No audit rows on 403/denial.
- [x] Schedule subkeys restricted to known-safe registry at write **and** read.
- [x] Policy PUT 422s on unknown / forbidden / non-exposable keys.
- [x] Equipment / provider / assignment status enums constrained.
- [x] Supplements projected to `{name}` only on owner read.
- [x] `_redact_stripe_in_string` runs on every outbound string (`_scrub_strings`).
- [x] Frontend palette is equine-tokens only.
- [x] Phase 9 / Phase 15 / Admin Portal collections byte-identical after a 1-B edit storm.
