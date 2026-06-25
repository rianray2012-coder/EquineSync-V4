# Phase HorseOps-1J - Evidence Closure Only

Status: Codex-approved and locked.

## Purpose

HorseOps-1J closes the remaining screenshot and evidence gap from locked
HorseOps-1I. This is an evidence-only phase. It adds no product behavior and
does not change backend routes, schemas, permissions, privacy projections,
Admin Portal capabilities, billing, landing pages, service workers, push
notifications, native mobile behavior, or workflow engines.

## Evidence Captured

All screenshots were captured at mobile viewport 390x844 and are included in
`outputs/horseops_1j_screenshots/`.

| Evidence | Path |
|---|---|
| Staff / manager Care Ledger mobile view | `outputs/horseops_1j_screenshots/staff-care-ledger-mobile.jpg` |
| Staff daily-check drawer mobile view | `outputs/horseops_1j_screenshots/staff-daily-check-drawer-mobile.jpg` |
| Owner Care Ledger mobile view for an owner-linked horse | `outputs/horseops_1j_screenshots/owner-care-ledger-mobile.jpg` |
| Owner request drawer mobile view | `outputs/horseops_1j_screenshots/owner-request-drawer-mobile.jpg` |
| Platform Admin Horses directory mobile view | `outputs/horseops_1j_screenshots/admin-horses-mobile.jpg` |
| Platform Admin horse summary drawer mobile view | `outputs/horseops_1j_screenshots/admin-horse-drawer-mobile.jpg` |

## Privacy Evidence

Visual and DOM evidence was checked for the approved privacy boundaries:

- Owner screenshots show only owner-safe summary cards and the "Ask the barn"
  request drawer.
- Owner screenshots do not show staff notes, raw daily-check payload internals,
  alert triggers, `source_check_id`, audit diffs, passwords, auth tokens,
  Stripe IDs, or private admin/staff-only fields.
- Platform Admin horse screenshots show the approved summary-only directory and
  summary drawer. They show counts and identity fields, not raw daily-check
  payloads, alert triggers, `source_check_id`, staff notes, owner request
  messages, audit diffs, or Stripe IDs.
- Staff screenshots show the existing staff Care Ledger and daily-check drawer
  from the locked 1H/1I mobile flow.

## Seed / Test Data

Evidence used local disposable seeded data only:

- Existing local staff/manager-style HorseOps QA session for the staff
  screenshots.
- Phase Admin-8 seeded demo client account for owner screenshots.
- Phase Admin-8 seeded platform-admin account for Admin Portal screenshots.
- A local-only owner linkage was applied in the test database so the demo owner
  could access the owner route for an existing seeded horse. This did not change
  code or seeded-demo behavior.

No real passwords, tokens, Stripe IDs, or secrets are committed in this package.

## Verification

Focused verification:

```bash
python -m pytest backend/tests/test_horse_ledger_1j.py -q
```

The test pins:

- all six required screenshot paths exist,
- file extensions are `.jpg`,
- file signatures are JPEG,
- dimensions are exactly 390x844,
- no stale pricing-foundation language remains in this README.

## Package

Package path:

```text
outputs/phase_horseops_1j_changes.zip
```

Expected files:

- `PHASE_HORSEOPS_1J_README.md`
- `memory/PRD.md`
- `backend/tests/test_horse_ledger_1j.py`
- six screenshots under `outputs/horseops_1j_screenshots/`

## Lock Notes

HorseOps-1J was reviewed and locked as an evidence-closure package. The zip
contains only evidence/docs/tests/screenshots and does not introduce product
behavior.

## Deferred

No next feature starts in this phase. HorseOps-1J stops for Codex review after
packaging.
