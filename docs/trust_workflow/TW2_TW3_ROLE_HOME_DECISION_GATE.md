# TW-2/TW-3 Role Home And Decision Gate

Status: TW-2/TW-3 FOUNDER APPROVED
Date: 2026-08-30
Founder approval recorded: 2026-08-30
Authority: Controlled implementation only. This gate does not authorize production launch, provider activation, billing expansion, broad external messaging, document-signature activation, AI live mutation, or multi-facility expansion.

## Purpose

TW-2 and TW-3 convert the trust-and-workflow review into visible product structure:

- TW-2 creates role-home North Star panels that tell each role what changed, what needs a decision, what is safe to ignore, and what proof exists.
- TW-3 introduces a shared decision-state vocabulary for requests, notes, review, visibility, and completion.

## Implemented Scope

- Added `frontend/src/lib/trustWorkflow.js` as the shared source for role North Star copy and decision states.
- Added `frontend/src/components/TrustWorkflowPanel.jsx` as the common role-home trust panel.
- Wired the trust panel into trainer, owner, guardian, rider, manager, and service-provider dashboard paths.
- Added decision-state context inside pending service requests in `NotificationsBell.jsx`.
- Added `docs/trust_workflow/DECISION_STATUS_REGISTRY.csv`.
- Added `backend/tests/test_trust_workflow_tw2_tw3.py`.

## Role North Star Contract

Every role-home North Star must answer:

1. What changed since the user last looked?
2. What needs a decision?
3. What is safe to ignore or out of scope?
4. What proof or visibility boundary supports trust?

Current role keys:

- `trainer`
- `owner`
- `guardian`
- `rider`
- `manager`
- `serviceProvider`

## Decision State Contract

Decision states are intentionally plain and cross-product:

- `submitted`
- `seen`
- `assigned`
- `scheduled`
- `needs_review`
- `owner_visible`
- `internal_only`
- `completed`
- `declined_with_note`

These states are not a new backend workflow engine in TW-3. They are the UI vocabulary and guardrail foundation for later workflow expansion.

## Stop Rules

Stop before release if:

- A role North Star promises capability outside the product-status registry.
- Pending requests or review states use one-off labels instead of the shared decision vocabulary.
- Owner-visible, provider-visible, or external-message copy bypasses review/visibility language.
- Service-provider copy treats providers as staff, trainers, owners, or admins.
- Trainer surfaces add billing, staff-admin, invites, forms/signatures, checkout, subscriptions, students, or multi-facility actions without a later approved gate.
- Decision-state UI implies a backend transition that does not exist.

## Out Of Scope

Not implemented in TW-2/TW-3:

- No new backend decision-state persistence.
- No new trainer workflow implementation in TW-3.
- Trainer note authoring lifecycle.
- Owner request state-machine expansion.
- Provider invite, visit packet, revocation, or emergency access.
- Facility launch checklist and readiness score.
- Payment provider activation.
- Document signature activation.
- SMS, push, or email delivery expansion.
- Multi-facility switching.

## Verification

Required verification for this gate:

- `python3 -m pytest backend/tests/test_trust_workflow_tw0_tw1.py backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_build_next_13g_trainer_intake_shell.py -q`
- JSX parser check for touched frontend files when the cloud-backed checkout allows it.
- CSV parse check for `DECISION_STATUS_REGISTRY.csv` and existing TW registries.
- Copy scan for stale "ready" or broad-provider wording in touched surfaces.

## Next Gate

TW-4/TW-5 should add operational proof and facility/admin launch readiness only after TW-2/TW-3 remains clean. Any backend workflow expansion should be separately scoped and tested.
