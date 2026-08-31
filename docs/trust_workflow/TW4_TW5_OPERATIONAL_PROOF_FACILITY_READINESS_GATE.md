# TW-4/TW-5 Operational Proof And Facility Readiness Gate

Status: TW-4/TW-5 FOUNDER APPROVED
Date: 2026-08-30
Founder approval recorded: 2026-08-30
Authority: Controlled implementation only. This gate does not authorize production launch, provider activation, billing expansion, broad external messaging, document-signature activation, AI live mutation, or multi-facility expansion.

## Purpose

TW-4 and TW-5 convert the deeper trust-and-workflow review into visible proof and readiness surfaces:

- TW-4 adds operational proof signals so users can see freshness, review state, audit path, and exception context before acting.
- TW-5 adds facility/admin readiness signals so setup, provider dependencies, permissions, support diagnostics, and launch boundaries are legible.

These changes are a source-level trust layer. They do not create new backend authority, payment processing, document signing, provider access, external delivery, AI mutation, or multi-facility operations.

## Implemented Scope

- Added `frontend/src/lib/operationalProof.js` as the shared source for operational proof and facility readiness signals.
- Added `frontend/src/components/OperationalProofPanel.jsx` for proof cards used across facility, handoff, support, and admin surfaces.
- Added `frontend/src/components/FacilityReadinessPanel.jsx` for launch-readiness areas tied to existing setup progress when available.
- Wired facility proof and readiness into `frontend/src/pages/Dashboard.jsx`.
- Wired handoff proof into `frontend/src/pages/HandoffReports.jsx`.
- Wired support proof into `frontend/src/pages/admin/AdminSupport.jsx`.
- Wired admin proof into `frontend/src/pages/admin/AdminDashboard.jsx`.
- Corrected one admin-dashboard brand string from `Equine·Sync` to `EquineSync`.
- Added `docs/trust_workflow/OPERATIONAL_PROOF_REGISTRY.csv`.
- Added `docs/trust_workflow/FACILITY_READINESS_REGISTRY.csv`.
- Added `backend/tests/test_trust_workflow_tw4_tw5.py`.

## Operational Proof Contract

Every TW-4 proof surface must answer:

1. What is the latest verified signal?
2. What decision, handoff, support, or admin state is visible?
3. What audit or review path supports trust?
4. What boundary prevents unsupported activation claims?

Current proof keys:

- `facility`
- `handoff`
- `support`
- `admin`

## Facility Readiness Contract

Facility readiness must show status without implying release authority. Current readiness areas:

- `horses`
- `staff`
- `owners`
- `schedules`
- `billing`
- `documents`
- `emergency_contacts`
- `permissions`

Readiness statuses are intentionally constrained to `complete`, `in_progress`, `pending`, `provider_required`, `gated`, and `planned`.

## Stop Rules

Stop before release if:

- A proof panel claims provider, payment, document-signature, messaging, AI, or multi-facility activation.
- Facility readiness treats provider-required billing or documents as live without provider proof.
- Support diagnostics create impersonation, hidden privilege, or unsafe access paths.
- Admin proof adds mutation controls to the read-only admin dashboard.
- Handoff proof hides draft, submitted, reviewed, open item, priority, or timestamp context.
- Setup readiness creates lockout behavior or hard launch requirements not present in the existing onboarding model.

## Out Of Scope

Not implemented in TW-4/TW-5:

- No new backend workflow persistence.
- No new provider invite, visit packet, revocation, emergency access, or scoped document access.
- No payment provider activation or subscription billing expansion.
- No document signature provider activation.
- No SMS, push, email, or broad external messaging delivery expansion.
- No AI live mutation.
- No multi-facility switching.
- No production launch authority.

## Verification

Required verification for this gate:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_trust_workflow_tw4_tw5.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw0_tw1.py backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_trust_workflow_tw4_tw5.py -q`
- JSX parser check for touched frontend files.
- CSV parse check for all trust-workflow registries.
- Copy scan for unsupported activation claims in TW4/TW5 source and docs.

## Next Gate

TW-6/TW-7 may deepen owner wellbeing, trainer workflow, and support experience only after TW-4/TW-5 remains clean. Backend workflow expansion, provider access, payments, signatures, messaging, AI mutation, and multi-facility work must remain separately scoped and founder-approved.
