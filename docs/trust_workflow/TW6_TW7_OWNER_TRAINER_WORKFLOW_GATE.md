# TW-6/TW-7 Owner And Trainer Workflow Gate

Status: TW-6/TW-7 FOUNDER APPROVED
Date: 2026-08-30
Founder approval recorded: 2026-08-30
Authority: Controlled implementation only. This gate does not authorize production launch, provider activation, billing expansion, broad external messaging, document-signature activation, AI live mutation, or multi-facility expansion.

## Purpose

TW-6 and TW-7 deepen the two highest-sensitivity relationship workflows from the deep review:

- TW-6 adds owner, guardian, and rider wellbeing guidance around care confidence, requests, visibility, and first-week expectations.
- TW-7 adds trainer workflow guidance around daily work, governed notes, rider context, and calendar mode.

These changes make the product easier to trust and easier to operate without creating new backend workflow persistence or expanding role authority.

## Implemented Scope

- Added `frontend/src/lib/relationshipWorkflow.js` as the shared source for owner wellbeing and trainer workflow signals.
- Added `frontend/src/components/OwnerWellbeingPanel.jsx` for owner, guardian, and rider trust-map cards.
- Added `frontend/src/components/TrainerWorkflowPanel.jsx` for trainer work-map cards.
- Wired owner wellbeing into `frontend/src/features/dashboards/PersonalDashboard.jsx`.
- Wired trainer workflow into `frontend/src/features/dashboards/TrainerDashboard.jsx`.
- Added `docs/trust_workflow/OWNER_WELLBEING_REGISTRY.csv`.
- Added `docs/trust_workflow/TRAINER_WORKFLOW_REGISTRY.csv`.
- Added `backend/tests/test_trust_workflow_tw6_tw7.py`.

## Owner Wellbeing Contract

Owner-facing wellbeing surfaces must answer:

1. What care confidence signal is visible now?
2. What request path should the owner, guardian, or rider use?
3. What is hidden until facility approval?
4. What should a new owner expect during the first week?

Current owner wellbeing signals:

- `care_status`
- `request_path`
- `visibility_boundary`
- `first_week`

## Trainer Workflow Contract

Trainer workflow surfaces must answer:

1. What trainer work is visible today?
2. What note lifecycle boundaries prevent unsafe sharing?
3. What rider context is useful without exposing unrelated owner data?
4. What scheduling mode remains planned until permission and collision rules are verified?

Current trainer workflow signals:

- `today_command`
- `note_lifecycle`
- `rider_context`
- `calendar_mode`

## Stop Rules

Stop before release if:

- Owner copy exposes internal staff notes, private barn context, or unapproved documents.
- Owner request copy implies a backend state machine that has not been approved.
- Guardian or rider copy expands visibility beyond facility-approved records.
- Trainer note copy implies live owner publishing without review.
- Trainer links add billing, staff-admin, invites, forms/signatures, checkout, subscriptions, students, provider access, or multi-facility actions.
- Trainer calendar copy implies conflict resolution or scheduling authority that has not been verified.

## Out Of Scope

Not implemented in TW-6/TW-7:

- No new backend owner request persistence.
- No new trainer note authoring persistence.
- No owner media upload, photo approval, or video storage expansion.
- No live owner digest delivery.
- No trainer billing packages.
- No trainer multi-facility switching.
- No provider access.
- No payment or document signature provider activation.
- No broad messaging delivery.

## Verification

Required verification for this gate:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw6_tw7.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw0_tw1.py backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_trust_workflow_tw4_tw5.py backend/tests/test_trust_workflow_tw6_tw7.py -q`
- JSX parser check for touched frontend files.
- CSV parse check for all trust-workflow registries.
- Copy scan for unsupported owner, trainer, provider, payment, signature, messaging, AI, and multi-facility claims.

## Next Gate

TW-8 should handle provider access only after a separate founder-approved scope defines invite boundaries, visit packets, revocation, emergency access, document visibility, communication rules, and audit evidence.
