# Build-Next-15D - Today's Pulse UAT Evidence

Status: Codex-approved & locked

Date: 2026-07-03

## Purpose

BN15D closes the staging/UAT evidence gap for locked Today's Pulse work. It
ties the locked credentialed role screenshots from BN13O to the locked BN15A
through BN15C-C Pulse contract, proving that role-home surfaces have visual
coverage and that Pulse data remains count-only and role-scoped.

## Evidence Model

BN15D does not create new credentials or mutate production data. The visual
evidence is copied from the locked BN13O credentialed role screenshot pass into
a BN15D-specific evidence folder. The Pulse behavior is verified by the locked
BN15 focused tests plus the new BN15D evidence guard.

This is intentionally honest evidence:

- screenshots prove the role shells and route landings;
- BN15A/BN15C-B/BN15C-C tests prove Today Pulse response visibility and privacy;
- BN15D report joins those two proof lines role by role.

## Scope

Included:

- BN15D evidence report:
  `outputs/build_next_15d_today_pulse_uat_evidence_report.md`
- BN15D screenshot evidence folder:
  `outputs/build_next_15d_today_pulse_screenshots/`
- Focused evidence/inventory guard:
  `backend/tests/test_build_next_15d_today_pulse_uat_evidence.py`
- PRD status update.

## Role Evidence Matrix

| Role row | Role | Pulse expectation |
| --- | --- | --- |
| UAT-R1 | `platform_admin` | Platform counts only; no private row payloads. |
| UAT-R2a | `admin` | Manager-safe work, horse-care, owner-request, and plan-usage counts. |
| UAT-R2b | `barn_owner` | Manager-safe work, horse-care, owner-request, and plan-usage counts. |
| UAT-R3 | `barn_manager` | Manager-safe work, horse-care, owner-request, and plan-usage counts. |
| UAT-R4a | `groom` | Work and horse-care counts only; no owner-request or plan-usage counts. |
| BN13M-T1 | `trainer` | Work and horse-care counts only; no owner-request or plan-usage counts. |
| BN13M-W1 | `working_student` | Work and horse-care counts only; no owner-request or plan-usage counts. |
| UAT-R5 | `horse_owner` | Owner-safe horse context; siloed by default. |
| UAT-R6 | `parent` | Owner-safe horse context; siloed by default. |
| UAT-R7 | `rider` | Owner-safe horse context; siloed by default. |
| UAT-R8 | standalone `horse_owner` | Individual-owner horse count only. |

## Privacy Guardrails

BN15D preserves the locked BN15 privacy boundary:

- count-only role-home Pulse evidence;
- no staff notes;
- no raw daily-check payloads;
- no alert triggers;
- no `source_check_id`;
- no audit diffs;
- no Stripe IDs;
- no DocuSign IDs;
- no auth tokens or passwords;
- no private horse records.

## Strictly Excluded

- No backend route/schema/auth/permission changes.
- No owner projection changes.
- No HorseOps write behavior.
- No alert/history/service-request behavior changes.
- No Stripe, Apple, checkout, Customer Portal, webhook, billing, or entitlement changes.
- No DocuSign changes.
- No Admin Portal capability changes.
- No notification delivery changes.
- No Text/SMS implementation.
- No landing page changes.
- No service worker, push, native mobile, offline sync, AI, scheduler, or
  workflow-engine changes.
- No seeded-demo, UAT-account, production-data, or credential mutation.

## Verification

Codex review:

- No findings.
- Focused BN15 evidence suite passed: `35 passed`.
- Zip integrity passed; `ZipFile.testzip()` returned clean.
- Packaged files match the working tree byte-for-byte.
- All 11 screenshot PNGs validate with expected dimensions.
- Scoped whitespace check passed.

Focused BN15 evidence suite:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15a_today_pulse_contract.py \
  backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py \
  backend/tests/test_build_next_15c_b_barn_visibility_policy.py \
  backend/tests/test_build_next_15c_c_today_pulse_role_home_evidence.py \
  backend/tests/test_build_next_15d_today_pulse_uat_evidence.py -q
```

Package integrity:

```bash
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_15d_today_pulse_uat_evidence.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Package

Expected package:

- `outputs/build_next_15d_today_pulse_uat_evidence.zip`

Expected files:

- `BUILD_NEXT_15D_TODAYS_PULSE_UAT_EVIDENCE_README.md`
- `backend/tests/test_build_next_15d_today_pulse_uat_evidence.py`
- `outputs/build_next_15d_today_pulse_uat_evidence_report.md`
- `outputs/build_next_15d_today_pulse_screenshots/`
- `memory/PRD.md`

## Next Gate

Recommended next gate after BN15D locks:

- BN15E - Today's Pulse founder UAT acceptance ledger, or
- continue the billing lane if live Stripe UAT evidence becomes the higher
  launch-risk item.
