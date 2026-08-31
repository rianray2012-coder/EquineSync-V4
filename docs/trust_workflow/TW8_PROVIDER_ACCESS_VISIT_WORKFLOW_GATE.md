# TW-8 Provider Access And Visit Workflow Gate

Status: TW-8 FOUNDER APPROVED
Date: 2026-08-30
Founder approval recorded: 2026-08-30
Authority: Controlled implementation only. This gate does not authorize production launch, payment activation, billing expansion, broad external messaging, document-signature activation, AI live mutation, or multi-facility expansion.

## Purpose

TW-8 turns the service-provider review recommendations into a visible access model:

- Provider access must be explicit, grant-scoped, review-aware, revocable, and auditable.
- Visit context must be limited to approved horse, appointment, care, and document details.
- Provider notes, documents, messages, billing handoff, and emergency access must stay inside their readiness boundaries until separately approved.

These changes clarify the provider workflow without creating new invite, revoke, document, messaging, payment, emergency, or backend lifecycle authority.

## Implemented Scope

- Added `frontend/src/lib/providerAccessWorkflow.js` as the shared source for provider access signals, statuses, and stop rules.
- Added `frontend/src/components/ProviderAccessPanel.jsx` for service-provider access-map cards.
- Wired the provider access map into `frontend/src/features/dashboards/ServiceProviderDashboard.jsx`.
- Added `docs/trust_workflow/PROVIDER_ACCESS_REGISTRY.csv`.
- Added `backend/tests/test_trust_workflow_tw8.py`.

## Provider Access Contract

Every TW-8 provider surface must answer:

1. What access is explicitly granted?
2. What visit packet context is visible?
3. What can be revoked or expired?
4. What provider notes require review before broader visibility?
5. What document, communication, billing, and emergency functions remain gated?
6. What audit evidence would be required before live expansion?

Current provider access signals:

- `invite_scope`
- `visit_packet`
- `revocation`
- `reviewed_notes`
- `document_boundary`
- `communication_boundary`
- `billing_handoff`
- `emergency_mode`

## Stop Rules

Stop before release if:

- Provider users are treated as staff, trainers, owners, or admins.
- Provider copy implies live invite creation, live revoke controls, live emergency grants, live document uploads, live signatures, live payments, external message delivery, AI mutation, or multi-facility access.
- Visit packets expose internal staff notes, unrelated owner data, unapproved documents, or facility-private operations.
- Provider notes can become owner-visible or staff-visible without review state.
- Billing handoff implies payment processing or invoice collection before TW-9.
- Emergency mode omits reason capture, narrow scope, expiration, or audit evidence.

## Out Of Scope

Not implemented in TW-8:

- No new backend provider grant lifecycle persistence.
- No live provider invite creation.
- No live provider revocation controls.
- No live emergency provider access.
- No provider document upload or document-signature activation.
- No external SMS, push, email, or broad messaging delivery.
- No provider payment processing or invoice collection.
- No AI live mutation.
- No multi-facility switching.
- No production launch authority.

## Verification

Required verification for this gate:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw8.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw0_tw1.py backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_trust_workflow_tw4_tw5.py backend/tests/test_trust_workflow_tw6_tw7.py backend/tests/test_trust_workflow_tw8.py -q`
- JSX parser check for touched frontend files.
- CSV parse check for all trust-workflow registries.
- Copy scan for unsupported provider, payment, signature, messaging, AI, emergency, and multi-facility claims.

## Next Gate

TW-9 should handle business, pricing, billing clarity, analytics, portability, public proof, and launch-safe marketing only after a separate founder-approved scope. Payment-provider activation and data export must remain independently verified before any live claims.
