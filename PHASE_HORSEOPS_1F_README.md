# Phase HorseOps-1F — Manager Polish: Templates, Schedule Presets, Pulse

Scope, endpoint map, privacy model, tests, and Codex review checklist.

---

## Scope

HorseOps-1F is an additive manager-polish layer on top of the locked
Care Ledger phases:

- Barn-wide owner-visibility template.
- One-click apply of the saved template to all active horses, writing the
  existing per-horse `horse_owner_visibility_policy` rows.
- Curated schedule-shape picker in the Feeding and Turnout manager drawers.
- Staff-only Manager Pulse rollup of active care items by horse.

No owner-alert details, notifications, AI replies, billing changes, Admin
Portal changes, Stripe changes, or Phase 9/15 changes are included.

---

## Backend

New endpoints in `backend/routes/horse_ledger.py`:

| Method | Path | Roles | Notes |
|---|---|---|---|
| GET | `/api/horse-ledger/templates/owner-visibility` | `admin`, `barn_manager` | Reads the current barn template or returns an empty version. |
| PUT | `/api/horse-ledger/templates/owner-visibility` | `admin`, `barn_manager` | Saves one template per barn. Reuses the locked 1-B safe-key validation. |
| POST | `/api/horse-ledger/templates/owner-visibility/apply` | `admin`, `barn_manager` | Applies the saved template to all active horses, or explicit same-barn `horse_ids`. |
| GET | `/api/horse-ledger/pulse/manager` | `admin`, `barn_manager` | Summary-only active alert rollup by horse. No triggers, notes, source ids, or raw alert rows. |

New collection:

- `horse_owner_visibility_templates`
  - one row per barn
  - index: `hovt_barn_unique` on `barn_id`

Important implementation detail: applying a template does **not** create a new
owner-read path. Owner reads remain backend-authoritative and continue to load
the existing per-horse `horse_owner_visibility_policy` row. The template simply
bulk-writes those already-locked policy rows.

---

## Privacy / Safety Invariants

- Template save/apply reuses `_validate_policy_sections()`, the same safe-key
  validation used by per-horse policy PUT.
- Forbidden sections such as `stall_bedding`, `handling_behavior`, and
  `service_providers` still 422.
- Forbidden keys such as `feeding.staff_only_warnings` still 422.
- Unknown allowlist keys still 422.
- Apply is barn-scoped; an explicit `horse_ids` payload containing a cross-barn
  horse returns 404 and does not write that horse policy.
- Template apply audit rows carry `field_paths` only; no raw policy payload or
  before/after values are stored in audit metadata.
- Manager Pulse returns counts and severity labels only; raw alert internals
  (`triggers`, `source_check_id`, notes) do not cross the API boundary.

---

## Frontend

`frontend/src/pages/CareLedgerTab.jsx`:

- Adds a `Barn template` button next to `Owner visibility` for managers.
- Adds `VisibilityTemplateDrawer`:
  - safe-key checkboxes from the existing `POLICY_KEYS` UI list
  - `Save template`
  - `Apply saved template to all horses`
  - applied-count confirmation stays visible in the drawer
- Adds `SchedulePresetPicker` for Feeding and Turnout:
  - Feeding presets emit only `{time, label, amount}`
  - Turnout presets emit only `{time, label, duration, paddock}`
  - These match the locked backend `_SCHEDULE_SUBKEYS` registry.
- Adds `ManagerPulse`, visible only in staff/manager view.

Owner UI is unchanged.

---

## Tests

`backend/tests/test_horse_ledger_1f.py` — 8 focused tests:

- `test_manager_can_save_and_read_barn_visibility_template`
- `test_template_requires_at_least_one_section`
- `test_template_reuses_owner_safe_policy_validation`
- `test_apply_template_writes_per_horse_policy_rows_and_audit`
- `test_apply_template_explicit_horse_ids_are_barn_scoped`
- `test_non_manager_cannot_manage_template_or_pulse`
- `test_manager_pulse_groups_active_alerts_without_raw_alert_detail`
- `test_visibility_template_index_exists`

Local Codex desktop limitation: this environment does not have `pytest`
installed, so focused pytest execution must be run in the backend environment
that has the app dependencies.

---

## Files In Package

- `backend/routes/horse_ledger.py`
- `backend/core/lifespan.py`
- `backend/tests/test_horse_ledger_1f.py`
- `frontend/src/pages/CareLedgerTab.jsx`
- `memory/PRD.md`
- `PHASE_HORSEOPS_1F_README.md`

---

## Codex Review Checklist

- [ ] Template endpoints are manager-only.
- [ ] Template validation cannot expand owner visibility beyond 1-B safe keys.
- [ ] Template apply writes only same-barn horse policies.
- [ ] Template apply emits audit rows with field paths only.
- [ ] Manager Pulse is manager-only and summary-only.
- [ ] Owner route and owner summary behavior from 1-E remain unchanged.
- [ ] No billing, Stripe, Admin Portal, notification, AI, or Phase 9/15 drift.
