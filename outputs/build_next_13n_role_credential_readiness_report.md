# Build-Next-13N Role Credential Readiness Report

Status: READY FOR CODEX REVIEW

Generated: 2026-07-01

## Summary

BN13N adds a dedicated, production-safe operator script for preparing the
credentialed role-smoke account set needed by BN13M.

This package does not run the script against production, does not write to
MongoDB, and does not record any password values.

## Readiness Matrix

| Row | Role | Email | Expected marker | Account source | BN13N status |
| --- | --- | --- | --- | --- | --- |
| UAT-R1 | platform admin | `uat.platform@equine-sync.com` | role=`admin`, platform_role=`platform_admin` | BN12A existing row | ready to seed/confirm |
| UAT-R2a | facility admin | `uat.facility-admin@equine-sync.com` | role=`admin` | BN12A existing row | ready to seed/confirm |
| UAT-R2b | barn owner | `uat.barn-owner@equine-sync.com` | role=`barn_owner` | BN13N dedicated row | ready to create |
| BN13M-T1 | trainer | `uat.trainer@equine-sync.com` | role=`trainer` | BN13N dedicated row | ready to create |
| UAT-R3 | barn manager | `uat.manager@equine-sync.com` | role=`barn_manager` | BN12A existing row | ready to seed/confirm |
| UAT-R4a | groom | `uat.staff@equine-sync.com` | role=`groom` | BN12A existing row | ready to seed/confirm |
| BN13M-W1 | working student | `uat.working-student@equine-sync.com` | role=`working_student` | BN13N dedicated row | ready to create |
| UAT-R5 | horse owner | `uat.owner@equine-sync.com` | role=`horse_owner` | BN12A existing row | ready to seed/confirm |
| UAT-R6 | guardian / parent | `uat.guardian@equine-sync.com` | role=`parent` | BN12A existing row | ready to seed/confirm |
| UAT-R7 | rider | `uat.participant@equine-sync.com` | role=`rider` | BN12A existing row | ready to seed/confirm |
| UAT-R8 | standalone individual owner | `uat.individual-owner@equine-sync.com` | role=`horse_owner`, no barn_id | BN12A existing row | ready to seed/confirm |

## Script Behavior

`backend/scripts/seed_bn13_role_smoke_accounts.py`:

- reuses the BN12 UAT facility id `bn12_uat_facility`,
- prepares 11 role-smoke rows,
- creates or updates only UAT-tagged role-smoke users,
- upserts account membership mirrors,
- sets `email_verified=true` and active account status,
- requires `--allow-prod` for production writes,
- supports `--dry-run` with no writes and no password minting,
- supports `--reset-passwords` for intentional rotation,
- emits audit rows without raw password values.

## Production Operator Commands

Dry-run first:

```bash
APP_ENV=production python -m scripts.seed_bn13_role_smoke_accounts --dry-run
```

Apply after reviewing dry-run output:

```bash
APP_ENV=production python -m scripts.seed_bn13_role_smoke_accounts --allow-prod
```

Rotate passwords only when intentionally needed:

```bash
APP_ENV=production python -m scripts.seed_bn13_role_smoke_accounts --allow-prod --reset-passwords
```

## Password Handling

Optional env-var password inputs:

- `SEED_BN13_UAT_PLATFORM_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_FACILITY_ADMIN_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_BARN_OWNER_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_TRAINER_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_MANAGER_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_STAFF_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_WORKING_STUDENT_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_GUARDIAN_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_PARTICIPANT_EQUINE_SYNC_COM_PASSWORD`
- `SEED_BN13_UAT_INDIVIDUAL_OWNER_EQUINE_SYNC_COM_PASSWORD`

No password value is included in this report.

## Remaining Blockers Before BN13M-R2

1. Run the dry-run in the production Render shell.
2. Apply the script only after dry-run output is reviewed.
3. Copy any one-time passwords out of band.
4. Store no passwords in repo files.
5. Rerun BN13M with credentialed browser sessions and screenshots.

## Strictly Unchanged

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No screenshots.
