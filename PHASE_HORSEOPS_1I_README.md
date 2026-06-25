# Phase HorseOps-1I - Mobile Field Verification & Polish

Status: Codex-approved and locked.

## Scope

HorseOps-1I is a frontend-only mobile field-readiness polish pass on top of
locked HorseOps-1H. It does not add backend routes, schemas, billing behavior,
admin roles, auth changes, landing-page changes, service workers, push
notifications, or native mobile work.

## What Changed

- Care Ledger form primitives now keep 44px-friendly mobile tap targets for
  text fields, selects, textareas, toggles, and schedule preset chips.
- Daily Check rows now stack on narrow screens instead of squeezing timestamp,
  status, notes, and the Amend action onto one line.
- Owner recent-request rows now stack on narrow screens and wrap longer
  request copy without horizontal overflow.
- Admin Portal horse drawer now wraps long horse/facility identifiers and uses
  a one-column severity-count layout on phones.

## Privacy And Safety Locks

- No owner projection, alert/history, service-request, audit, or backend route
  behavior changed.
- Owners still do not see alert internals, staff notes, raw daily-check
  payloads, audit rows, trigger/source identifiers, or staff-only fields.
- Admin Horse Directory remains summary-only.
- Local drafts remain field-only; no tokens, passwords, cookies, auth headers,
  or server secrets are stored.

## Browser / Viewport Verification

The Browser plugin was used after the founder restarted the local backend and
frontend. Verification ran against `http://127.0.0.1:3000` with a mobile
viewport (`390x844`).

Rendered evidence included a disposable local trainer signup through the real
public signup flow, a real horse added through the roster sheet, and the
protected horse profile opened through the rendered horse card.

Captured screenshots:

- `outputs/horseops_1i_screenshots/staff-care-ledger-mobile.jpg`
- `outputs/horseops_1i_screenshots/staff-daily-check-drawer-mobile.jpg`

The captured staff Care Ledger and daily-check drawer show the mobile stacking,
tap-target sizing, long-note wrapping, and drawer footer behavior that 1I
polishes.

Remaining screenshot gaps: owner-linked and platform-admin-only screens were
not captured from the disposable trainer session because those require seeded
owner/platform-admin credentials. Their mobile contracts remain covered by the
focused source-level tests listed below.

## Tests

Focused checks:

```bash
python -m pytest backend/tests/test_horse_ledger_1h.py backend/tests/test_horse_ledger_1i.py -q
```

Frontend build:

```bash
npm --prefix frontend run build
```

## Files

- `frontend/src/pages/CareLedgerTab.jsx`
- `frontend/src/pages/OwnerCareLedger.jsx`
- `frontend/src/pages/admin/AdminHorses.jsx`
- `backend/tests/test_horse_ledger_1i.py`
- `PHASE_HORSEOPS_1I_README.md`
- `memory/PRD.md`

## Deferred

- Real-device QA.
- Owner-linked and platform-admin screenshot evidence from seeded privileged
  accounts.
- Service worker / offline sync queue.
- Native mobile app.
- Push notifications.
- Any backend conflict-resolution behavior for drafts.
