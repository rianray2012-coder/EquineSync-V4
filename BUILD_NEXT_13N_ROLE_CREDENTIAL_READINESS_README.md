# Build-Next-13N - Role Credential Readiness

Status: CODEX-APPROVED & LOCKED

BN13N prepares the account-readiness step needed before BN13M can be rerun with
real credentialed browser screenshots.

## Purpose

BN13M proved that the production frontend and API are reachable, but every role
row remained blocked because safe role credentials or authenticated sessions
were not available. BN13N closes the planning gap by adding a dedicated,
production-safe operator script for the BN13 role-smoke account set.

## Strict Scope

- Account readiness tooling and evidence only.
- No product behavior changes.
- No role-routing changes.
- No intake-field changes.
- No billing, Stripe, Apple, DocuSign, HorseOps, Admin Portal, task, facility
  setup, email, notification, landing page, launch, or UAT approval changes.
- No screenshots.
- No password values committed.
- No live database writes are performed by this package.

## Artifacts

- `backend/scripts/seed_bn13_role_smoke_accounts.py`
- `outputs/build_next_13n_role_credential_readiness_report.md`
- `backend/tests/test_build_next_13n_role_credential_readiness.py`
- `outputs/build_next_13n_role_credential_readiness.zip`
- `memory/PRD.md`

## Operator Script

The new script prepares all rows needed for BN13M:

```bash
python -m scripts.seed_bn13_role_smoke_accounts --dry-run
python -m scripts.seed_bn13_role_smoke_accounts --allow-prod
```

For production writes, the script requires `--allow-prod`.

To rotate existing UAT role-smoke passwords intentionally:

```bash
python -m scripts.seed_bn13_role_smoke_accounts --allow-prod --reset-passwords
```

To rotate one role-smoke password without touching the other accounts:

```bash
python -m scripts.seed_bn13_role_smoke_accounts --allow-prod --reset-passwords --email uat.barn-owner@equine-sync.com
```

## Credential Safety

- `--dry-run` reads only, writes nothing, and mints/prints no passwords.
- New users receive one-time passwords only when the script is actually applied.
- Existing users are not re-hashed unless `--reset-passwords` is passed.
- Operators may supply private passwords through env vars such as
  `SEED_BN13_UAT_TRAINER_EQUINE_SYNC_COM_PASSWORD`.
- Passwords are never written to Mongo audit metadata, docs, tests, or zip files.

## BN13M Rows Covered

- UAT-R1 platform admin
- UAT-R2a facility admin
- UAT-R2b dedicated barn owner
- BN13M-T1 dedicated trainer
- UAT-R3 barn manager
- UAT-R4a groom
- BN13M-W1 dedicated working student
- UAT-R5 horse owner
- UAT-R6 guardian / parent
- UAT-R7 rider
- UAT-R8 standalone individual owner

## Verification

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_13n_role_credential_readiness.py -q
```

Package integrity:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13n_role_credential_readiness.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Remaining Action

An operator still needs to run the script in the correct environment, copy any
one-time passwords out of band, and then rerun BN13M for actual browser
screenshots.

## Lock Notes

Codex review found no blocking findings after the dry-run reset safety patch.
BN13N is locked as the role credential-readiness package. It does not prove that
the accounts were seeded or that screenshots were captured; those remain BN13O.
