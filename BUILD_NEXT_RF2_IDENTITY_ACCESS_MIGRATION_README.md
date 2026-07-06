# Build Next RF2 - Identity-Based Access Migration

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF2 narrows remaining name-based access risk after RF1. It moves the known staff
self-service access predicates in `backend/routes/backlog.py` from display-name
matching to stable user-ID predicates, and records which identity migrations
must stay deferred to later model phases.

## Scope

Included:

- Staff My Work reads for shifts, tasks, handoffs, and time-clock entries.
- Staff task status updates.
- Staff time-clock ownership checks.
- Payroll export stable `staff_user_id` filter support.
- Document signature identity evidence.
- Evidence report, tests, docs, and package.

Excluded:

- Full RF8 staff workforce model or account-membership backfill.
- RF10 provider multi-barn/client access grants.
- RF13 message delivery/recipient identity model.
- RF17 feature-shell UX rewrites.
- Provider calls, billing/provider mutations, app-store/native work, UAT account mutation, or GitHub submission work.

## Artifacts

- `docs/RF2_IDENTITY_BASED_ACCESS_MIGRATION.md`
- `backend/core/rf2_identity_access_migration_proof.py`
- `backend/scripts/build_rf2_identity_access_migration_proof.py`
- `backend/tests/test_rf2_identity_access_migration.py`
- `outputs/rf2_identity_access_migration_report.md`
- `outputs/build_next_rf2_identity_access_migration.zip`

## Founder Decisions

| Decision | Status | Notes |
| --- | --- | --- |
| Accept strict staff self-service matching for stable user-ID records only. | accepted in RF2 lock | Legacy staff records that only contain a free-text staff name will not appear in self-service until RF8 migration/backfill links them to stable IDs. |
| Decide when to retire admin payroll `staff_name` filtering. | deferred by RF2 lock | RF2 keeps the legacy name filter for admin reporting compatibility while adding `staff_user_id` as the preferred stable filter. |
| Keep provider grants, message recipients, and full workforce membership deferred. | accepted deferral in RF2 lock | These require RF8/RF10/RF13 model work and are not safely solved by simple field renames. |

## Lock Note

RF2 is Codex-reviewed and locked. Do not expand RF2 into RF8 workforce
implementation, RF10 provider grants, RF13 messaging delivery, or RF17
feature-shell rewrites. RF3 may proceed next as the onboarding/import/setup
refinement gate.

## Verification

Run:

```bash
./.venv/bin/python -m pytest backend/tests/test_rf2_identity_access_migration.py -q
./.venv/bin/python -m py_compile backend/routes/backlog.py backend/core/rf2_identity_access_migration_proof.py backend/scripts/build_rf2_identity_access_migration_proof.py backend/tests/test_rf2_identity_access_migration.py
./.venv/bin/python -m backend.scripts.build_rf2_identity_access_migration_proof --output outputs/rf2_identity_access_migration_report.md --fail-on-blockers
unzip -t outputs/build_next_rf2_identity_access_migration.zip
```
