# Build Next RF1 Data Fences And Capability Gates

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF1 closes the P0 data-fence findings from locked RF0 before broader refinement work continues. This phase is intentionally narrow: tenant-safe export/report reads, owner-safe portal predicates, stable relationship-based horse access, and backend capability proof.

## Implemented Scope

- Added owner-safe horse inventory endpoints:
  - `GET /owner/horses`
  - `GET /owner-portal/horses`
- Scoped QuickBooks invoice export by `barn_id`.
- Scoped backlog dashboard revenue totals by `barn_id`.
- Replaced owner-portal billing/forms/media/health/emergency/training access predicates that used display/free-text name matching with stable user/owner/horse ID predicates.
- Split owner account predicates from horse-context predicates so billing/payment and form signing cannot be authorized by horse linkage alone.
- Updated owner update reads to recognize `primary_owner_id`, `secondary_owner_ids`, and stable owner-user aliases.
- Added RF1 source/proof tests and a regenerated report.
- Added `backend/scripts/seed_local_demo_test_accounts.py` so local integration tests can bootstrap documented demo accounts without restoring unsafe production seed behavior.

## Explicit Non-Scope

- No RF2 full identity migration.
- No RF7 portal UX completion.
- No RF12 payment/refund/void/export truth overhaul.
- No RF17 feature-shell retirement.
- No provider calls or third-party mutations.
- No founder acceptance auto-marking.

## Verification

```bash
./.venv/bin/python -m pytest backend/tests/test_rf1_data_fences_capability_gates.py -q
./.venv/bin/python -m py_compile backend/routes/backlog.py backend/routes/owner_updates.py backend/routes/horse_ledger.py backend/core/rf1_data_fences_capability_gates_proof.py backend/scripts/build_rf1_data_fences_capability_gates_proof.py
./.venv/bin/python -m backend.scripts.build_rf1_data_fences_capability_gates_proof --output outputs/rf1_data_fences_capability_gates_report.md --fail-on-blockers
```

## Local Runnable Environment

```bash
./.venv/bin/python backend/scripts/seed_local_demo_test_accounts.py
cd backend
ALLOW_AUTO_SEED=true REACT_APP_BACKEND_URL=http://127.0.0.1:8001 ../.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

The script refuses production and defaults to known local test database names.
It creates/updates only the documented local demo users used by backend
integration tests.

## Review Package

- `docs/RF1_DATA_FENCES_CAPABILITY_GATES.md`
- `backend/core/rf1_data_fences_capability_gates_proof.py`
- `backend/scripts/build_rf1_data_fences_capability_gates_proof.py`
- `backend/scripts/seed_local_demo_test_accounts.py`
- `backend/tests/test_rf1_data_fences_capability_gates.py`
- `outputs/rf1_data_fences_capability_gates_report.md`
- `outputs/build_next_rf1_data_fences_capability_gates.zip`

## Lock Note

RF1 is Codex-reviewed and locked. Review finding R1-F01 was fixed by splitting
account-sensitive owner predicates from horse-context predicates. Do not reopen
RF1 except for regression fixes; proceed to RF2 as the next gated phase.

## Founder Review Items

- Accept that RF1 intentionally hides legacy owner-facing records that only match by display/free-text name until RF2 migrates them to stable IDs.
- Decide whether to add seeded cross-barn integration fixtures before locking RF1, or accept the current source-level proof and direct route guards.
