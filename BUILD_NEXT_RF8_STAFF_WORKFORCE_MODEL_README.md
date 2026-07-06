# Build Next RF8 Staff Workforce Model

RF8 packages staff workforce identity hardening for locked review evidence.

Status: CODEX-REVIEWED & LOCKED.

## Scope

- Add a safe same-barn staff directory endpoint.
- Require stable staff IDs on new staff-module creates and normalize those IDs to trusted display names server-side.
- Update staff scheduling, Staff Tasks, handoff, and time-clock create flows to require and submit stable staff user IDs.
- Preserve RF2 stable self-service predicates for My Work, time clock, task status, and payroll export.
- Document deferred Staff Tasks migration, legacy staff-row backfill, and payroll name-filter retirement.

## Out of Scope

- No provider calls.
- No billing/payment truth changes.
- No trainer operating-center rebuild.
- No service-provider multi-barn grants.
- No historical data backfill/mutation.
- No Staff Tasks deletion or Task Engine migration.
- No founder acceptance auto-marking.

## Files

- `backend/routes/backlog.py`
- `frontend/src/lib/staffDirectory.js`
- `frontend/src/pages/StaffScheduling.jsx`
- `frontend/src/pages/StaffTasks.jsx`
- `frontend/src/pages/HandoffReports.jsx`
- `frontend/src/pages/TimeClock.jsx`
- `docs/RF8_STAFF_WORKFORCE_MODEL.md`
- `docs/RF8_STAFF_WORKFORCE_MODEL_PLAN.md`
- `backend/core/rf8_staff_workforce_model.py`
- `backend/scripts/build_rf8_staff_workforce_model.py`
- `backend/tests/test_rf8_staff_workforce_model.py`
- `outputs/rf8_staff_workforce_model_report.md`
- `outputs/build_next_rf8_staff_workforce_model.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf8_staff_workforce_model.py
.venv/bin/python backend/scripts/build_rf8_staff_workforce_model.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf8_staff_workforce_model.zip
git diff --check
```
