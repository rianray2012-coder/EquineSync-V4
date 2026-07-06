# Build-Next-15F - Live Today's Pulse Walkthrough

Status: Codex-approved & locked - blocked pending safe role sessions

Date: 2026-07-03

## Purpose

BN15F attempts the fresh live/staging Today's Pulse walkthrough requested after
locked BN15E. It uses the current production-like frontend and backend URLs and
records whether TP-1 through TP-11 can be refreshed with live credentialed
evidence.

This run does not build product behavior and does not mark any row
founder-accepted.

## Verdict For This Run

- Official frontend reachability: PASS.
- Official API health: PASS.
- Production-like database identity: PASS, using the locked BN13O label.
- Credentialed role walkthrough rows: BLOCKED.
- Fresh role screenshots: not captured.
- Founder acceptance: not recorded.

The role rows are blocked because safe UAT role passwords or authenticated
browser sessions were not available to this Codex run. BN15F does not invent
credentials, reset passwords, mutate production data, or mark a role row passing
without a credentialed session.

Lock note: Codex review found no findings. BN15F is locked as a truthful
blocked evidence packet, not as a passing credentialed walkthrough.

## Environment Evidence

Frontend:

- URL: `https://app.equine-sync.com`
- Result: HTTP 200 from Vercel.

API:

- URL: `https://equine-sync-api.onrender.com/api/health`
- Result: `status=ok`, `database=connected`, `environment=production`,
  `mailer_configured=true`.

Database label:

- `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`

Deploy markers:

- Frontend: Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready.
- Backend: Render deploy / 2026-06-30 / commit `5aeea66` / Live.

## Role Rows

BN15F preserves the BN15E TP row mapping:

| TP row | Role evidence row | Role | Status |
| --- | --- | --- | --- |
| TP-1 | UAT-R1 | `platform_admin` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-2 | UAT-R2a / UAT-R2b | `admin` / `barn_owner` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-3 | UAT-R3 | `barn_manager` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-4 | UAT-R4a | `groom` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-5 | BN13M-T1 | `trainer` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-6 | BN13M-W1 | `working_student` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-7 | UAT-R5 | `horse_owner` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-8 | UAT-R6 | `parent` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-9 | UAT-R7 | `rider` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-10 | UAT-R8 | standalone `horse_owner` | BLOCKED_PENDING_CREDENTIAL_SESSION |
| TP-11 | Privacy exclusions | all role rows | BLOCKED_PENDING_CREDENTIAL_SESSION |

## Strict Scope

- Evidence and reporting only.
- No product behavior changes.
- No backend route/schema/auth/permission changes.
- No frontend behavior changes.
- No owner projection changes.
- No HorseOps write behavior.
- No alert/history/service-request behavior changes.
- No billing, checkout, Customer Portal, Stripe, Apple, webhook, entitlement,
  or provider changes.
- No DocuSign changes.
- No Admin Portal capability changes.
- No notification delivery changes.
- No Text/SMS implementation.
- No landing page changes.
- No service worker, push, native mobile, offline sync, AI, scheduler, or
  workflow-engine changes.
- No seeded-demo, UAT-account, production-data, credential, or password
  mutation.
- No public launch, first-client pilot, or founder acceptance approval.

## Verification

Lock verification:

- BN15F focused guard: `7 passed`.
- Broader BN15 evidence regression: `52 passed`.
- Zip integrity passed.
- Package files matched the working tree byte-for-byte.

Focused BN15F evidence guard:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15f_live_today_pulse_walkthrough.py -q
```

Recommended BN15 evidence regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15a_today_pulse_contract.py \
  backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py \
  backend/tests/test_build_next_15c_b_barn_visibility_policy.py \
  backend/tests/test_build_next_15c_c_today_pulse_role_home_evidence.py \
  backend/tests/test_build_next_15d_today_pulse_uat_evidence.py \
  backend/tests/test_build_next_15e_today_pulse_founder_acceptance_ledger.py \
  backend/tests/test_build_next_15f_live_today_pulse_walkthrough.py -q
```

## Package

Expected package:

- `outputs/build_next_15f_live_today_pulse_walkthrough.zip`

Expected files:

- `BUILD_NEXT_15F_LIVE_TODAYS_PULSE_WALKTHROUGH_README.md`
- `backend/tests/test_build_next_15f_live_today_pulse_walkthrough.py`
- `outputs/build_next_15f_live_today_pulse_walkthrough.md`
- `outputs/build_next_15f_screenshots/README.md`
- `memory/PRD.md`

## Required To Clear The Blocker

1. Provide safe role credentials out of band or log into each role manually
   during a supervised browser evidence run.
2. Capture one sanitized screenshot per TP row / role row.
3. Confirm no screenshot exposes staff notes, raw payloads, alert triggers,
   `source_check_id`, audit diffs, auth tokens, passwords, Stripe IDs,
   DocuSign IDs, or private horse records.
4. Re-run BN15F as a credentialed evidence pass.

## Next Gate

Recommended next gate after this blocked BN15F packet:

- BN15F.1 - credentialed live Today's Pulse walkthrough with safe sessions, or
- live Stripe billing evidence if billing remains the higher launch-risk lane.
