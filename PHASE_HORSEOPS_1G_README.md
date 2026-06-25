# Phase HorseOps-1G - Platform Care Ledger Inspection

Status: ✅ Codex-approved & locked (Jun 18 2026)

Scope, endpoint map, privacy model, tests, and Codex review checklist.

---

## Scope

HorseOps-1G ships the previously deferred cross-facility platform Care
Ledger inspection surface inside the Admin Portal.

This phase is read-only and summary-only:

- Adds the Admin Portal horse directory.
- Adds a per-horse Care Ledger summary drawer.
- Keeps the product `/api/horse-ledger/{horse_id}` endpoint barn-scoped
  and unchanged.
- Does not add mutations, notifications, billing changes, Phase 9/15
  changes, owner-route changes, or new collections.

---

## Backend

New Admin Portal surface module:

- `backend/routes/admin_portal/horses.py`

New endpoints:

| Method | Path | Roles | Notes |
|---|---|---|---|
| GET | `/api/admin/portal/horses` | `super_admin`, `platform_admin`, `support_admin` | Cross-facility horse roster with search/status/facility filters. |
| GET | `/api/admin/portal/horses/{horse_id}/ledger-summary` | `super_admin`, `platform_admin`, `support_admin` | Summary-only Care Ledger counts. |

Route lock updated:

- Admin Portal surface is now **39 endpoints**:
  - 28 GET
  - 10 POST
  - 1 PATCH
- The two new 1G GETs are listed in `LOCKED_GET_ROUTES`.
- `test_admin_portal_route_lock_guard.py` now expects 39 decorators.

Activity feed self-flood guard:

- `_ACTIVITY_EXCLUDE_PREFIXES` now includes:
  - `admin.portal.read.horses`
  - `admin.portal.read.horse_ledger_summary`

---

## Privacy / Safety Invariants

The new Admin Portal surface is intentionally not a platform-role bypass
for the product ledger route. Product Care Ledger access still flows
through the existing barn-scoped `/api/horse-ledger/{horse_id}` routes.

List response exposes only:

- `id`
- `name`
- `barn_id`
- `barn_name`
- `status`
- `breed`
- `age`
- `created_at`

Ledger summary response exposes only:

- horse identity projection
- active equipment count
- daily check count in the last 24 hours
- active alert count and severity counts
- open owner request count
- visibility policy configured/version/section names

Explicitly excluded from 1G responses:

- raw daily-check payloads
- alert triggers
- `source_check_id`
- staff notes
- owner request messages
- audit diffs
- owner IDs
- microchip/private horse fields
- Stripe-shaped strings

The frontend repeats this boundary in copy and renders only the summary
fields returned by the backend.

---

## Frontend

New page:

- `frontend/src/pages/admin/AdminHorses.jsx`

Route wiring:

- `/admin/portal/horses` now renders `AdminHorses`.
- The previous Horses placeholder route is removed.

UI:

- Search by horse name.
- Status filter.
- Read-only table.
- Read-only summary drawer.
- Approved Admin Portal palette only.
- No mutation buttons.

---

## Tests

New test file:

- `backend/tests/test_horse_ledger_1g.py`

Coverage:

- platform roles can inspect horses cross-facility
- barn-scoped users cannot use the Admin Portal horse surface
- `billing_admin` is blocked because `horses` is not in its section caps
- list response strips private horse fields and redacts Stripe-shaped strings
- summary response is counts-only and excludes raw payloads/triggers/source IDs/messages
- both reads emit audit rows
- both read audit actions are excluded from the dashboard activity feed
- route lock includes both 1G GET paths
- frontend replaces the old Horses placeholder with `AdminHorses`

Local Codex desktop note: focused pytest could not be used for the final
local pass because pytest import hung before test collection on this machine.
The same contract was verified with a direct runner against the local backend
and Mongo.

Verification completed:

- backend Python syntax checks passed
- admin route decorator scan reports 39 routes: 28 GET, 10 POST, 1 PATCH
- new AdminHorses page uses no forbidden admin color tokens
- new files are ASCII-only
- direct functional check passed: health, cross-facility horse list,
  barn-scoped/billing_admin denial, summary-only privacy scrub, audit rows,
  self-read exclusions, and frontend route/privacy copy
- zip integrity passed; `memory/PRD.md` included at full size

---

## Files In Package

- `backend/routes/admin_portal/horses.py`
- `backend/routes/admin_portal/portal.py`
- `backend/routes/admin_portal/__init__.py`
- `backend/routes/admin_portal/_helpers.py`
- `backend/tests/test_admin_portal_admin7a.py`
- `backend/tests/test_admin_portal_route_lock_guard.py`
- `backend/tests/test_horse_ledger_1a.py`
- `backend/tests/test_horse_ledger_1b.py`
- `backend/tests/test_horse_ledger_1c.py`
- `backend/tests/test_horse_ledger_1d.py`
- `backend/tests/test_horse_ledger_1e.py`
- `backend/tests/test_horse_ledger_1g.py`
- `frontend/src/App.js`
- `frontend/src/pages/admin/AdminHorses.jsx`
- `memory/PRD.md`
- `PHASE_HORSEOPS_1G_README.md`

---

## Codex Review Checklist

- [x] Product Care Ledger route remains barn-scoped and unchanged.
- [x] Admin horse surface is platform-role gated to `horses` section roles.
- [x] `billing_admin` and barn-scoped users cannot read it.
- [x] Responses are summary-only and never include raw checks, triggers,
      source IDs, staff notes, owner request messages, owner IDs, or
      private horse fields.
- [x] Stripe-shaped substrings are redacted.
- [x] Route lock is exactly 39 endpoints.
- [x] No mutations, no new collections, no billing/Phase 9/Phase 15 drift.
