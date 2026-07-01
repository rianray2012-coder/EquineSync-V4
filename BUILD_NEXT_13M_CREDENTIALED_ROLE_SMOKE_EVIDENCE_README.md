# Build-Next-13M - Credentialed Role Smoke Evidence

Status: READY FOR CODEX REVIEW

BN13M is the credentialed browser-evidence phase that follows the locked BN13L
execution checklist. This run records the official environment reachability
checks and the current status of each credentialed role row.

## Verdict For This Run

- Official frontend reachability: PASS.
- Official API health: PASS.
- Credentialed role login rows: BLOCKED.
- Screenshots: not captured.
- Founder acceptance: not recorded.

The role rows are blocked because no safe UAT role credentials or authenticated
sessions were available to this run. BN13M does not invent credentials, does not
reset passwords, and does not mark a role row passing without a credentialed
browser session.

## Strict Scope

- Evidence capture and reporting only.
- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation.
- No screenshots were captured in this blocked run.
- No passwords, tokens, secrets, reset links, API keys, Stripe IDs, DocuSign
  IDs, or private client data are included.

## Artifacts

- `outputs/build_next_13m_role_smoke_report.md`
- `backend/tests/test_build_next_13m_role_smoke_evidence.py`
- `outputs/build_next_13m_credentialed_role_smoke_evidence.zip`
- `memory/PRD.md`

## Environment Evidence

Frontend:

- URL: `https://app.equine-sync.com`
- Result: HTTP 200 from Vercel.

API:

- URL: `https://equine-sync-api.onrender.com/api/health`
- Result: `status=ok`, `database=connected`, `environment=production`.

Database label:

- `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`

Deploy markers:

- Frontend: Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready.
- Backend: Render deploy / 2026-06-30 / commit `5aeea66` / Live.

## Required Verification

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_13m_role_smoke_evidence.py -q
```

Recommended source/evidence regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13k_role_flow_smoke.py \
  backend/tests/test_build_next_13l_role_smoke_prep.py \
  backend/tests/test_build_next_13m_role_smoke_evidence.py -q
```

Package integrity:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13m_credentialed_role_smoke_evidence.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Remaining Action

To turn BN13M into a passing credentialed role-smoke phase, rerun the role rows
with safe role credentials or authenticated sessions supplied out of band, then
capture sanitized screenshots for every role row.
