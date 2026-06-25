# Phase 15R-B - Migration Dry-Run + Gap Report

Status: locked.

## Scope

Phase 15R-B adds a read-only migration dry-run for the deferred Phase 15R
billing entitlement refactor. It projects current `plans` and `subscriptions`
rows into the future `subscription_plans` and `account_subscription_limits`
shapes prepared in 15R-A.

## Delivered

- New read-only analyzer:
  `backend/core/entitlements_migration.py`.
- New CLI:
  `backend/scripts/phase15r_migration_dry_run.py`.
- New focused tests:
  `backend/tests/test_phase15r_migration_dry_run.py`.
- New report artifact:
  `outputs/phase15r_b_migration_dry_run_report.md`.

## What The Dry-Run Flags

- Unknown plan codes.
- Legacy Phase 15 plan codes that need canonical normalization
  (`starter` -> `starter_barn`, `professional` -> `advanced_barn`).
- Founder-provided alias plan codes that need canonical normalization
  (`trainer_no_lessons`, `trainer_lessons_15`, `trainer_lessons_50`).
- Missing plan-limit fields that will default during projection.
- Free invited-owner access carrying Stripe IDs.
- Free subscriptions treated as paid Stripe subscriptions.
- Unknown billing providers or purchase platforms.
- Apple/manual/comped rows carrying Stripe IDs.
- Projected account-limit rows missing required limit fields.

## How To Run The Live Report

From the repository root:

```bash
MONGO_URL="mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=3000" \
DB_NAME="test_database" \
./.venv/bin/python -m backend.scripts.phase15r_migration_dry_run
```

The report is written to:

```text
outputs/phase15r_b_migration_dry_run_report.md
```

The script returns exit code `0` when no blockers are found and exit code `2`
when blocker-level migration issues are found.

## Codex Sandbox Note

Codex's restricted sandbox could not connect to local MongoDB at
`127.0.0.1:27017`, so the packaged report was generated from the static
`PLAN_CATALOG` fallback and clearly labels that limitation. The CLI itself is
ready for local/live dry-run execution when `MONGO_URL` and `DB_NAME` are
available.

## Round-1 Patch

The first live local run found two blocker-level unknown plan rows:
`starter` and `professional`. These are old Phase 15 plan codes, not true
unknown products. Round-1 now treats them as `legacy_plan_code` warnings and
projects them as:

- `starter` -> `starter_barn`
- `professional` -> `advanced_barn`

True unknown codes such as `platinum` remain blocker-level
`unknown_plan_code` issues.

## Lock Result

Founder-run live Mongo dry-run passed with:

```text
4 plan rows, 2 subscription rows, 0 blocker(s), 13 warning(s)
```

The old Phase 15 `starter` and `professional` rows now appear as
warning-level `legacy_plan_code` issues and project to `starter_barn` and
`advanced_barn`. Remaining warnings are deferred data cleanup/provider-field
normalization, not runtime blockers.

## Guardrails

- No Mongo writes.
- No `subscription_plans` collection created.
- No `account_subscription_limits` collection created.
- No Stripe API calls.
- No Apple receipt validation or App Store server-notification code.
- No checkout changes.
- No webhook changes.
- No frontend or public pricing display changes.
- No hard enforcement.
- No Phase 9 billing changes.

## Verification

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_phase15r_entitlements.py \
  backend/tests/test_phase15r_migration_dry_run.py -q
```

Result:

```text
34 passed
```
