# Build-Next-13K - Role Flow Smoke Evidence

Status: READY FOR CODEX REVIEW

Build-Next-13K is an evidence-only phase. It converts the BN13 role routing
matrix into a practical staging smoke checklist without changing product
behavior.

## Scope

BN13K verifies, at source level, that each supported role still has the expected
first landing path, role-home shell, and navigation boundary. It also records
the live staging rows that must be completed with credentialed browser evidence
before any launch/UAT row can be marked founder-accepted.

Covered roles:

- Platform admin
- Facility admin
- Barn owner
- Trainer
- Barn manager
- Staff/groom
- Working student
- Horse owner
- Guardian/parent
- Rider

## Evidence Rules

- Source-level checks can pass from repository evidence.
- Live smoke rows require a successful login in the official staging or
  production-like environment.
- Missing credentials, unclear role marker, or unconfirmed official environment
  must be recorded as a blocker row, not a pass.
- Localhost evidence is reference-only.
- No password, token, or secret is written to the report.

## Strictly Unchanged

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No intake-field changes.
- No seeded account behavior changes.

## Artifacts

- `outputs/build_next_13k_role_flow_smoke_report.md`
- `backend/tests/test_build_next_13k_role_flow_smoke.py`
- `outputs/build_next_13k_role_flow_smoke.zip`
- `memory/PRD.md`

Screenshots are intentionally not included in this packet because credentialed
official-environment browser access was not available inside this phase. The
report lists the exact screenshot rows still required to close live smoke.

## Verification

Focused source regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13a_role_routing.py \
  backend/tests/test_build_next_13b_role_navigation.py \
  backend/tests/test_build_next_13c_rider_intake_shell.py \
  backend/tests/test_build_next_13d_guardian_minor_intake.py \
  backend/tests/test_build_next_13e_owner_intake_shell.py \
  backend/tests/test_build_next_13f_barn_owner_intake_shell.py \
  backend/tests/test_build_next_13g_trainer_intake_shell.py \
  backend/tests/test_build_next_13h_manager_intake_shell.py \
  backend/tests/test_build_next_13i_staff_intake_shell.py \
  backend/tests/test_build_next_13j_role_first_login_matrix.py \
  backend/tests/test_build_next_13k_role_flow_smoke.py -q
```

Frontend compile:

```bash
cd frontend && npm run build
```

Package integrity:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13k_role_flow_smoke.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Review Notes

BN13K does not close official UAT. It makes the remaining live role smoke work
explicit and keeps the launch gate from silently treating source evidence as
credentialed staging evidence.
