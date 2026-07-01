# Build-Next-13L - Credentialed Role Smoke Prep

Status: CODEX-APPROVED & LOCKED

BN13L is a prep-only phase. It takes BN13K's blocked live role-smoke rows and
turns them into a safe execution packet for the later credentialed browser
evidence phase.

## Purpose

Prepare a role-by-role staging walkthrough that an operator can execute without
committing credentials, secrets, tokens, screenshots, or live session data to
the repository.

BN13L does not execute the browser walkthrough. That belongs to BN13M after the
official environment and safe role credentials are available.

## Strict Scope

- Evidence planning and checklist only.
- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation.
- No screenshots.
- No founder acceptance recorded.

## Artifacts

- `outputs/build_next_13l_role_smoke_execution_checklist.md`
- `outputs/build_next_13l_role_smoke_result_template.md`
- `backend/tests/test_build_next_13l_role_smoke_prep.py`
- `outputs/build_next_13l_credentialed_role_smoke_prep.zip`
- `memory/PRD.md`

## Execution Model For BN13M

BN13L prepares two documents:

1. **Execution checklist**: exact rows, expected first landing route, expected
   surface, sidebar expectations, forbidden-link checks, and screenshot naming.
2. **Result template**: blank pass/blocker table that can be filled during
   BN13M without storing any secret values.

## Credential Safety

- Credentials are supplied out of band or entered manually in the browser.
- Credentials are never written into docs, tests, logs, screenshots, or zip
  files.
- Result rows record only role, email, status, screenshot path, and sanitized
  notes.
- A missing credential is a `BLOCKED` result, not a test failure and not a
  reason to invent data.

## Required Verification

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_13l_role_smoke_prep.py -q
```

Recommended source regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13j_role_first_login_matrix.py \
  backend/tests/test_build_next_13k_role_flow_smoke.py \
  backend/tests/test_build_next_13l_role_smoke_prep.py -q
```

Package integrity:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13l_credentialed_role_smoke_prep.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Lock Notes

BN13L should be approved only as a prep packet. It intentionally leaves the live
credentialed role-flow evidence blocked for BN13M.

Codex review found no blocking findings. BN13L is locked as the credentialed
role-smoke prep packet only; browser execution, screenshots, and founder
acceptance remain deferred to BN13M.
