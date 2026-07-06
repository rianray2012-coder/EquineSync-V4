# Build-Next-18C - UAT Role Refresh

Status: LOCKED - UAT role evidence captured.

Date: 2026-07-05

## Purpose

BN18C is the credentialed UAT role-refresh phase after BN17 role journey work
and BN18 production/provider proof. Its hard entry gate is clean production API
health and readiness proof from BN18B.

The production gate now passes. BN18C therefore records the fresh role
screenshot/privacy evidence needed for TP-1 through TP-11 while keeping founder
acceptance as a separate later action.

## Scope

Implemented:

- Added a read-only UAT role-refresh helper:
  `backend/core/uat_role_refresh_proof.py`.
- Added a CLI report generator:
  `backend/scripts/build_next_18c_uat_role_refresh.py`.
- Added focused source/output guards:
  `backend/tests/test_build_next_18c_uat_role_refresh.py`.
- Generated:
  `outputs/bn18c_uat_role_refresh_report.md`.
- Captured fresh evidence under:
  `outputs/build_next_18c_uat_role_refresh_screenshots/`.

## Strict Scope

BN18C in this package is evidence-only and does not:

- Build product behavior.
- Change frontend routes, dashboards, role homes, navigation, copy, CSS, or
  landing pages.
- Change backend routes, schemas, auth, permissions, privacy, owner projection,
  billing, webhooks, document signing, Admin Portal capability, or UAT account
  behavior.
- Reset passwords, seed data, mutate MongoDB, or mark founder acceptance.
- Query or mutate Stripe, Resend, DocuSign, Vercel, Render, Atlas, or provider
  dashboards.

## Current Result

The refreshed generated report is clean:

- Production gate: `pass`.
- Overall status: `ready_for_founder_review`.
- Blockers: `0`.
- Warnings: `0`.
- TP-1 through TP-11 role rows: `evidence_captured`.

The screenshot pass uses current production Vercel frontend and Render API
surfaces after the dashboard/onboarding separation work. These screenshots are
review evidence only and do not record founder acceptance.

## Evidence Files

| TP row | Evidence row | File |
| --- | --- | --- |
| TP-1 | UAT-R1 platform admin | `uat-r1-platform-admin.png` |
| TP-2 | UAT-R2a facility admin | `uat-r2a-facility-admin.png` |
| TP-2 | UAT-R2b barn owner | `uat-r2b-barn-owner.png` |
| TP-3 | UAT-R3 barn manager | `uat-r3-barn-manager.png` |
| TP-4 | UAT-R4a groom/staff | `uat-r4a-groom.png` |
| TP-5 | BN13M-T1 trainer | `bn13m-t1-trainer.png` |
| TP-6 | BN13M-W1 working student | `bn13m-w1-working-student.png` |
| TP-7 | UAT-R5 horse owner | `uat-r5-horse-owner.png` |
| TP-8 | UAT-R6 guardian/parent | `uat-r6-guardian-parent.png` |
| TP-9 | UAT-R7 rider | `uat-r7-rider.png` |
| TP-10 | UAT-R8 standalone owner | `uat-r8-individual-owner.png` |
| TP-11 | Privacy sweep | `privacy-sweep.md` |

Optional supporting setup captures are also present for facility admin and barn
owner review context:

- `uat-r2a-facility-admin-setup.png`
- `uat-r2b-barn-owner-setup.png`

## Visual Review Note

The proof helper validates evidence presence and file signatures, not visual
product judgment. Manual review should inspect the screenshots for expected
role content. During this pass, guardian and rider evidence is live-session
evidence with guardian/rider navigation visible while the main dashboard body
resolves into the shared Stable Command facility surface. That should be
treated as a UX review note for founder judgment, not a hidden pass/fail
mutation in this evidence phase.

## Verification

Completed verification:

- BN18B production gate rerun: `blocker(s)=0`, `warning(s)=0`.
- BN18C role-refresh rerun: `blocker(s)=0`, `warning(s)=0`.
- Focused BN18C tests: `9/9` passed.
- BN18B + BN18C proof regression: `20/20` passed.
- Compile check passed for the helper and CLI.

Focused BN18C tests:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_18c_uat_role_refresh.py -q
```

Compile check:

```bash
./.venv/bin/python -m py_compile \
  backend/core/uat_role_refresh_proof.py \
  backend/scripts/build_next_18c_uat_role_refresh.py
```

Report generation:

```bash
./.venv/bin/python -m backend.scripts.build_next_18c_uat_role_refresh \
  --api-base-url https://api.equine-sync.com \
  --frontend-url https://app.equine-sync.com \
  --screenshot-evidence-dir outputs/build_next_18c_uat_role_refresh_screenshots
```

Package:

`outputs/build_next_18c_uat_role_refresh.zip`

## Lock Boundary

BN18C is locked as the fresh TP-1 through TP-11 role-evidence packet.
Founder review of the screenshot set and privacy sweep remains the next
explicit acceptance step. BN18C does not mark any TP row founder-accepted
automatically.
