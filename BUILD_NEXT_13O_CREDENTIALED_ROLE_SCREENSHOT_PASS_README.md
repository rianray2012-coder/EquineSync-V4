# Build-Next-13O - Credentialed Role Screenshot Pass

Status: READY FOR CODEX REVIEW - BLOCKED EVIDENCE RUN

BN13O is the follow-up evidence pass after locked BN13N. Its job is to run the
BN13N role-smoke account script in the official environment, then capture
credentialed browser screenshots for every role row.

## Verdict For This Run

- Official frontend reachability: PASS.
- Official API health: PASS.
- BN13N script execution in production: BLOCKED.
- Credentialed role login rows: BLOCKED.
- Screenshots: not captured.
- Founder acceptance: not recorded.

The production app and API are reachable, but this Codex run does not have a
safe Render shell session, role passwords, or authenticated browser sessions.
BN13O therefore records a blocked screenshot-pass attempt instead of marking any
role row complete.

## Strict Scope

- Evidence capture and reporting only.
- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation.
- No BN13N script execution was performed by this package.
- No screenshots were captured in this blocked run.
- No passwords, tokens, reset links, API keys, Stripe IDs, DocuSign IDs, private
  keys, or authenticated session data are included.

## Artifacts

- `outputs/build_next_13o_role_smoke_report.md`
- `backend/tests/test_build_next_13o_role_screenshot_pass.py`
- `outputs/build_next_13o_credentialed_role_screenshot_pass.zip`
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
./.venv/bin/python -m pytest backend/tests/test_build_next_13o_role_screenshot_pass.py -q
```

Recommended evidence regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13m_role_smoke_evidence.py \
  backend/tests/test_build_next_13n_role_credential_readiness.py \
  backend/tests/test_build_next_13o_role_screenshot_pass.py -q
```

Package integrity:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13o_credentialed_role_screenshot_pass.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Remaining Action

To clear BN13O, an operator must:

1. Run the BN13N script in the production Render shell:
   - dry-run first,
   - then apply with `--allow-prod` only after the preview is reviewed.
   - use `--email <role-email>` with `--reset-passwords` when only one
     password needs to be rotated.
2. Copy any one-time passwords out of band.
3. Log into each role through the production frontend with a clean session.
4. Capture sanitized screenshots for every role row.
5. Repackage BN13O with each row marked PASS, BLOCKED, or FAIL and a screenshot
   for every PASS row.

## Review Notes

This package is intentionally blocked. It proves the official app surfaces are
reachable, but it does not prove role-session behavior. Founder acceptance and
launch readiness remain pending until credentialed screenshots are captured.
