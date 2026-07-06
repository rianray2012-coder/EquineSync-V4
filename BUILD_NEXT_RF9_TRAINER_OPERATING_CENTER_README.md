# Build Next RF9 Trainer Operating Center

RF9 locks trainer operating-center and trainer-fluidity hardening after clean Codex review.

## Scope

- Add a read-only trainer operating-center API.
- Add a same-barn trainer directory for stable trainer selectors.
- Stamp trainer-created lessons and training logs with stable `trainer_id`.
- Scope trainer lesson/training reads to stable trainer IDs.
- Require stable horse/trainer IDs for new Training Plans.
- Replace the generic trainer dashboard with a trainer-specific operating center.
- Preserve trainer intake as review-gated setup intent.
- Document deferred trainer packages, billing truth, haul-ins, school horses, and broad multi-facility grants.

## Out of Scope

- No Stripe or billing mutations.
- No trainer package charging.
- No service-provider multi-barn grants.
- No broad multi-facility membership/grant model.
- No native/offline behavior.
- No provider calls.
- No founder acceptance auto-marking.

## Files

- `backend/routes/operations.py`
- `backend/routes/trainer_operating_center.py`
- `backend/routes/backlog.py`
- `backend/server.py`
- `frontend/src/features/dashboards/TrainerDashboard.jsx`
- `frontend/src/pages/TrainingPlans.jsx`
- `backend/core/rf9_trainer_operating_center.py`
- `backend/scripts/build_rf9_trainer_operating_center.py`
- `backend/tests/test_rf9_trainer_operating_center.py`
- `docs/RF9_TRAINER_OPERATING_CENTER.md`
- `docs/RF9_TRAINER_OPERATING_CENTER_PLAN.md`
- `outputs/rf9_trainer_operating_center_report.md`
- `outputs/build_next_rf9_trainer_operating_center.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf9_trainer_operating_center.py
.venv/bin/python backend/scripts/build_rf9_trainer_operating_center.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf9_trainer_operating_center.zip
git diff --check
```
