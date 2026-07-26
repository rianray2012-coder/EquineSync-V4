# Founder Decision Change Log V1.1.0

Predecessor package: `Technical_Audit_Founder_Decision_Packet_2026-07-26`

Successor package: `Technical_Audit_Founder_Decisions_Approved_V1_1_0_2026-07-26`

Directive ID: `ES-FOUNDER-DISPOSITION-TA-FD-001-008-2026-07-26-01`

## Adopted As Recommended

- `ES-TA-FD-001` retained test-failure and pilot-gate policy.
- `ES-TA-FD-002` cross-barn task mutation and authorization model.
- `ES-TA-FD-003` notification delivery and failure policy.
- `ES-TA-FD-004` production storage failure policy.
- `ES-TA-FD-005` background-job leadership and duplicate-execution model.

## Modified Decisions

### ES-TA-FD-006

Predecessor identifier:

`ONLINE_FIRST_LIMITED_ACTOR_BOUND_FIELD_RECOVERY`

V1.1.0 identifier:

`ONLINE_FIRST_LIMITED_ACTOR_BOUND_FIELD_RECOVERY_WITH_CONTROLLED_NATIVE_PILOT_DISTRIBUTION`

Change summary:

- Adds controlled private native pilot distribution channels.
- Preserves online-first product posture.
- Preserves prohibition on full offline support.
- Requires actor/context/barn-bound queued writes and server-side replay reauthorization.
- Requires native pilot distribution prerequisites before native pilot enrollment.

### ES-TA-FD-007

Predecessor recommendation:

DocuSign deferred from initial pilot with sandbox-only internal testing.

V1.1.0 identifier:

`PRODUCTION_READY_DOCUSIGN_REQUIRED_BEFORE_PILOT_WITH_PROVIDER_NEUTRAL_LEGAL_ESIGNATURE_ADAPTER`

Change summary:

- Rejects deferral of production DocuSign as the final Founder disposition.
- Makes production-ready DocuSign a mandatory pilot gate.
- Adds provider-neutral legal e-signature adapter requirement.
- Preserves prohibition on provider activation, envelope sending, signed-document custody, legal-signature claims, and pilot enrollment absent separate readiness and activation approval.

### ES-TA-FD-008

Predecessor identifier:

`WEB_FIRST_OR_WEB_PLUS_PWA_CONTROLLED_PILOT_CHANNEL`

V1.1.0 identifier:

`CONTROLLED_WEB_PWA_AND_PRIVATE_NATIVE_BETA_PILOT_CHANNEL`

Change summary:

- Authorizes controlled pilot preparation for web, PWA, Apple TestFlight, Google Play internal testing, and Google Play closed testing.
- Keeps public iOS App Store and public Google Play production release unauthorized.
- Keeps tester enrollment, push activation, native background sync, pilot enrollment, and public enrollment separately controlled.

## Revised Remediation Sequence Change

`ES-TA-PRF-006` is renamed to `Provider-Neutral Legal ESignature Adapter And DocuSign Production Readiness`.

`ES-TA-PRF-007` is renamed to `Controlled Web PWA And Private Native Beta Pilot Readiness`.

`ES-TA-PRF-008` remains eighth in implementation sequence but should begin as a parallel documentary workstream for node-level classification.

## Non-Authorization Preservation

The V1.1.0 package remains documentary. It does not authorize implementation, provider activation, deployment, release promotion, pilot enrollment, tester enrollment, payment activation, public app-store release, database migration, governance supersession, archival deletion, or M4 work.
