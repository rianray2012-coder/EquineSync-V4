# Build-Next-15F.1 - Credentialed Live Today's Pulse Walkthrough

Status: Ready for Codex review - credentialed screenshots complete; founder acceptance not recorded

Date: 2026-07-03

## Purpose

BN15F.1 is the follow-up evidence gate after locked BN15F. Its job is to clear
the credential blocker by capturing fresh, credentialed, production-like
Today’s Pulse walkthrough evidence for the BN15E TP-1 through TP-11 rows.

This phase is evidence-only. It does not build product behavior and does not
mark any row founder-accepted.

## Verdict For This Run

- Official frontend reachability: PASS.
- Official API health: PASS.
- Production-like database identity: PASS, using the locked BN13O label.
- Credentialed role walkthrough rows: PASS.
- Fresh role screenshots: TP-1 through TP-10 captured; TP-11 privacy sweep complete.
- Founder acceptance: not recorded.

The environment is ready for the walkthrough. TP-1 was captured from a safe
Platform Admin browser session, and TP-2 was captured from safe Facility
Admin and Barn Owner browser sessions. TP-3 was captured from a safe Barn
Manager browser session. TP-4 was captured from a safe Staff/Groom browser
session. TP-5 was captured from a safe Trainer browser session. TP-7 was
captured from a safe Horse Owner browser session. TP-8 was captured from a safe
Guardian/Parent browser session. TP-6 was captured from a safe Working Student
browser session. TP-9 was captured from a safe Lesson Participant browser
session. TP-10 was captured from a safe Individual Owner browser session.
TP-11 is complete as a screenshot-only privacy sweep across the captured role
evidence. BN15F.1 does not invent
credentials, reset passwords, run seed scripts, mutate production data, or mark
a role row passing without a credentialed session.

Facility Admin, Barn Owner, and Barn Manager dashboard evidence are each
included in two supporting screenshot parts because the live dashboard needed a
reduced viewport to show the relevant sections.

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

BN15F.1 preserves the BN15E TP row mapping:

| TP row | Role evidence row | Role | Status |
| --- | --- | --- | --- |
| TP-1 | UAT-R1 | `platform_admin` | PASS |
| TP-2 | UAT-R2a / UAT-R2b | `admin` / `barn_owner` | PASS |
| TP-3 | UAT-R3 | `barn_manager` | PASS |
| TP-4 | UAT-R4a | `groom` | PASS |
| TP-5 | BN13M-T1 | `trainer` | PASS |
| TP-6 | BN13M-W1 | `working_student` | PASS |
| TP-7 | UAT-R5 | `horse_owner` | PASS |
| TP-8 | UAT-R6 | `parent` | PASS |
| TP-9 | UAT-R7 | `rider` | PASS |
| TP-10 | UAT-R8 | standalone `horse_owner` | PASS |
| TP-11 | Privacy exclusions | all role rows | PASS |

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

## Evidence Boundary

The credential blocker is cleared for screenshot evidence. TP-1 through TP-10
were captured from safe role sessions, and TP-11 is marked PASS for the
screenshot-only privacy sweep. BN15F.1 does not claim credentialed API response
payload capture and does not mark any row founder-accepted.

## Verification

Verification completed for this package:

- BN15F.1 focused guard: `8 passed`.
- Broader BN15 evidence regression: `61 passed`.

Focused BN15F.1 evidence guard:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15f1_live_today_pulse_walkthrough.py -q
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
  backend/tests/test_build_next_15f_live_today_pulse_walkthrough.py \
  backend/tests/test_build_next_15f1_live_today_pulse_walkthrough.py -q
```

## Package

Expected package:

- `outputs/build_next_15f1_live_today_pulse_walkthrough.zip`

Expected files:

- `BUILD_NEXT_15F1_CREDENTIALED_LIVE_TODAYS_PULSE_WALKTHROUGH_README.md`
- `backend/tests/test_build_next_15f1_live_today_pulse_walkthrough.py`
- `outputs/build_next_15f1_live_today_pulse_walkthrough.md`
- `outputs/build_next_15f1_screenshots/README.md`
- `outputs/build_next_15f1_screenshots/uat-r1-platform-admin.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r4a-groom.png`
- `outputs/build_next_15f1_screenshots/bn13m-t1-trainer.png`
- `outputs/build_next_15f1_screenshots/bn13m-w1-working-student.png`
- `outputs/build_next_15f1_screenshots/uat-r5-horse-owner.png`
- `outputs/build_next_15f1_screenshots/uat-r6-guardian-parent.png`
- `outputs/build_next_15f1_screenshots/uat-r7-rider.png`
- `outputs/build_next_15f1_screenshots/uat-r8-individual-owner.png`
- `memory/PRD.md`

## Next Gate

BN15F.1 can be reviewed as a completed credentialed screenshot evidence pass.
Do not advance rows to founder acceptance until Rian explicitly marks them
accepted.
