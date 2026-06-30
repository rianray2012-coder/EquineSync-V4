# Build-Next-12A - UAT Account Seed

Status: ready for review.

## Purpose

BN12A creates a safe, repeatable way to seed the eight role accounts needed for
BN12 UAT. It is a CLI-only phase.

It does not approve launch, execute UAT, change product behavior, call Stripe,
call DocuSign, send email, or add a public seed route.

## Script

`backend/scripts/seed_bn12_uat_accounts.py`

## UAT Roster

| UAT ID | Email | Role Context |
| --- | --- | --- |
| UAT-R1 | `uat.platform@equine-sync.com` | Platform admin |
| UAT-R2 | `uat.facility-admin@equine-sync.com` | Facility admin / barn owner |
| UAT-R3 | `uat.manager@equine-sync.com` | Barn manager |
| UAT-R4 | `uat.staff@equine-sync.com` | Staff |
| UAT-R5 | `uat.owner@equine-sync.com` | Horse owner |
| UAT-R6 | `uat.guardian@equine-sync.com` | Guardian / parent |
| UAT-R7 | `uat.participant@equine-sync.com` | Lesson participant |
| UAT-R8 | `uat.individual-owner@equine-sync.com` | Standalone individual owner |

## Safety Rules

- Production writes require `--allow-prod`.
- `--dry-run` never writes and never mints or prints passwords.
- New users receive minted one-time passwords unless a matching env var supplies
  a password.
- Existing users are not re-hashed unless `--reset-passwords` is passed.
- Password values are printed only once and are never written to audit rows,
  logs, docs, or committed files.
- All seeded records are tagged with `uat_seed_key="bn12_uat_accounts"`.

## Run Locally

```bash
cd backend
python -m scripts.seed_bn12_uat_accounts --dry-run
python -m scripts.seed_bn12_uat_accounts
```

## Run In Production Render Shell

```bash
cd /opt/render/project/src/backend
python -m scripts.seed_bn12_uat_accounts --dry-run
python -m scripts.seed_bn12_uat_accounts --allow-prod
```

Copy the printed one-time passwords immediately. They are not shown again.

To intentionally rotate existing UAT passwords:

```bash
python -m scripts.seed_bn12_uat_accounts --allow-prod --reset-passwords
```

## Optional Fixed Password Env Vars

If the operator wants to supply a known private password instead of minting,
set the matching env var before running the script. Do not commit or paste the
values.

```text
SEED_BN12_UAT_PLATFORM_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_FACILITY_ADMIN_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_MANAGER_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_STAFF_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_GUARDIAN_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_PARTICIPANT_EQUINE_SYNC_COM_PASSWORD
SEED_BN12_UAT_INDIVIDUAL_OWNER_EQUINE_SYNC_COM_PASSWORD
```

## After Running

Update `docs/BUILD_NEXT_12_ROLE_READINESS_CHECKLIST.md` from `pending` to
`ready` only after each account has been confirmed to sign in and reach the
intended role/context.

## Current Verdict

`seed tool ready`

BN12 role workflows remain pending until a human/operator completes the actual
UAT walkthroughs and records sanitized evidence.
