# Phase HorseOps-1H - Mobile Field Readiness

Status: ready for Codex review.

## Scope

HorseOps-1H is a frontend-first mobile readiness pass for the locked Care
Ledger surfaces. It does not add backend routes, schemas, billing behavior,
admin roles, or landing-page changes.

## What Changed

- Added `frontend/src/lib/horseOpsDrafts.js`, a small local-only draft helper
  for HorseOps field forms.
- Staff daily-check drawers now restore unsent draft fields on the same device
  and clear the draft after a successful save.
- Owner "Ask the barn" requests now restore unsent draft fields on the same
  device and clear the draft after a successful send.
- Care Ledger drawers now use mobile-safe height, safe-area footer padding,
  sticky actions, and larger tap targets.
- Daily-check quick actions and amend controls now meet the 44px tap target
  target for field use.
- Admin Portal horse directory keeps its desktop table and adds mobile summary
  cards that open the same scrubbed, summary-only drawer.

## Privacy And Safety Locks

- Draft storage is local device convenience only; it stores form fields, never
  auth tokens, passwords, cookies, headers, or server secrets.
- Backend privacy remains authoritative. 1H does not change owner projections,
  alert/history APIs, service-request rules, or platform horse summary APIs.
- Owner-facing UI continues to avoid raw alert/history internals, staff notes,
  raw daily-check payloads, audit rows, and trigger/source identifiers.
- Admin horse mobile cards are summary-only and open the existing scrubbed
  drawer.

## Files

- `frontend/src/lib/horseOpsDrafts.js`
- `frontend/src/pages/CareLedgerTab.jsx`
- `frontend/src/pages/OwnerCareLedger.jsx`
- `frontend/src/pages/admin/AdminHorses.jsx`
- `backend/tests/test_horse_ledger_1h.py`
- `memory/PRD.md`
- `PHASE_HORSEOPS_1H_README.md`

## Tests

Focused source-level tests:

```bash
python -m pytest backend/tests/test_horse_ledger_1h.py -q
```

Current verification:

- `backend/tests/test_horse_ledger_1h.py` — 7/7 passed.
- Changed frontend files parse cleanly with `@babel/parser`.
- Full frontend build passes: `npm --prefix frontend run build` → compiled
  successfully.

Recommended adjacent regression before lock:

```bash
python -m pytest \
  backend/tests/test_horse_ledger_1e.py \
  backend/tests/test_horse_ledger_1g.py \
  backend/tests/test_horse_ledger_1h.py -q
```

## Deferred

- Service worker / offline sync queue.
- Native mobile app.
- Push notifications.
- Backend conflict-resolution for multi-device drafts.
- New HorseOps API behavior.
