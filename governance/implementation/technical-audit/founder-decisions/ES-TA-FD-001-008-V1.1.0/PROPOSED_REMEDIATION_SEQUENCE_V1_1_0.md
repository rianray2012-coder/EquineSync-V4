# Proposed Remediation Sequence V1.1.0

Status: Founder-approved documentary sequencing. This file does not create or authorize implementation branches.

## Sequence

1. `ES-TA-PRF-001` Cross-Barn Authorization And Isolation
2. `ES-TA-PRF-002` Production Storage Fail-Closed Behavior
3. `ES-TA-PRF-003` Notification Coroutine And Delivery Reliability
4. `ES-TA-PRF-004` Background-Job Leadership And Duplicate-Execution Controls
5. `ES-TA-PRF-005` Offline Actor Context Barn Binding
6. `ES-TA-PRF-006` Provider-Neutral Legal ESignature Adapter And DocuSign Production Readiness
7. `ES-TA-PRF-007` Controlled Web PWA And Private Native Beta Pilot Readiness
8. `ES-TA-PRF-008` Retained Test-Baseline Classification And Burn-Down

`ES-TA-PRF-008` should also begin as a parallel documentary workstream because the complete 161-node register is required before pilot-gate execution.

## ES-TA-PRF-001 Cross-Barn Authorization And Isolation

Related decision: `ES-TA-FD-002`

Invariant: every task read/mutation and every document/agreement/native/offline request must be reauthorized against current actor, tenant, barn/facility, role/context, relationship, and capability.

Scope: task read and mutation authorization; denial behavior; relationship/role/barn invalidation; audit events; regression matrix.

Required tests: cross-barn read/mutation denial, relationship removal, role change, barn removal, trainer multi-facility context, platform-admin denial/default, offline replay denial.

Stop conditions: schema migration, platform-admin privilege expansion, or runtime implementation beyond exact authorization.

Production impact: separate production-release decision required.

## ES-TA-PRF-002 Production Storage Fail-Closed Behavior

Related decision: `ES-TA-FD-004`

Invariant: production never silently uses `local_dev_stub` and never returns fake `STUB` upload success.

Scope: storage provider initialization, production failure mode, health status, bounded upload/document unavailability, explicit dev/test stub mode.

Required tests: missing production storage config, provider init failure, upload `503`, no secret leakage, explicit dev/test stub.

Stop conditions: provider activation, file migration, retention policy work, signed-document custody.

Production impact: separate production-release decision required.

## ES-TA-PRF-003 Notification Coroutine And Delivery Reliability

Related decision: `ES-TA-FD-003`

Invariant: notification creation and provider delivery are separate durable states; no untracked fire-and-forget coroutine calls.

Scope: task notifications, owner digests, weekly recaps, signature notifications/reminders, retry/dead-letter/duplicate prevention, opt-outs, admin resend.

Required tests: provider success/failure, retry/backoff, duplicate prevention, invalid email, opt-out, dead-letter, partial digest failure, privacy-safe logs.

Stop conditions: live messaging activation, provider credential changes, schema migration without authorization.

Production impact: separate production-release and provider-activation decisions required.

## ES-TA-PRF-004 Background-Job Leadership And Duplicate-Execution Controls

Related decision: `ES-TA-FD-005`

Invariant: web replicas do not independently execute duplicate recurring schedules.

Scope: dedicated singleton worker, database-backed lease, or equivalent; job ownership; lease lifecycle; failover; rolling deployment; idempotency.

Required tests: leader acquisition, competing workers, renewal, expiry, failover, rolling deploy, poison job, duplicate prevention.

Stop conditions: provider topology change, worker deployment, database migration without authorization.

Production impact: separate production-release decision required.

## ES-TA-PRF-005 Offline Actor Context Barn Binding

Related decisions: `ES-TA-FD-006`, `ES-TA-FD-002`

Invariant: every queued mutation is bound to actor, role/context, barn/facility, client operation, creation time, authorization version, and affected record; every replay is reauthorized server-side.

Scope: queue metadata, replay reauthorization, logout/account switch/role removal/barn removal behavior, queue visibility, quarantine/cancel policy.

Required tests: replay success, stale permission denial, role removal, relationship removal, barn removal, credential expiry, logout, account switch, duplicate operation ID, conflict, poison quarantine.

Stop conditions: full offline operation, native background sync, unrestricted offline mutation, sensitive cache policy gap.

Production impact: separate production-release and pilot-scope decisions required.

## ES-TA-PRF-006 Provider-Neutral Legal ESignature Adapter And DocuSign Production Readiness

Related decisions: `ES-TA-FD-007`, `ES-TA-FD-004`, `ES-TA-FD-002`, `ES-TA-FD-003`, `ES-TA-FD-005`

Invariant: production-ready DocuSign capability is mandatory before pilot; implementation must use a provider-neutral legal e-signature adapter and domain contract.

Scope: provider-neutral contract, DocuSign production account/application ownership, credential custody, envelope creation, template/version control, signer identity, guardian/minor treatment, signing workflow, callback/webhook verification, idempotency, status reconciliation, signed-document and certificate retrieval, secure custody, access control, retention/deletion, cancellation/resend/decline/expiration/retry/provider outage, audit trail, privacy/legal review, observability, support/recovery.

Required tests: behavioral signing flows, negative authorization tests, webhook authenticity, replay and duplicate events, provider outage, status reconciliation, signed-document custody blocked without storage readiness.

Stop conditions: provider activation, production envelope sending, signed-document custody, legal claim, or pilot enrollment without separate exact Founder activation approval.

Production impact: separate production-release, provider-readiness, legal/privacy, and exact activation decisions required.

## ES-TA-PRF-007 Controlled Web PWA And Private Native Beta Pilot Readiness

Related decisions: `ES-TA-FD-006`, `ES-TA-FD-008`

Invariant: controlled private native beta distribution may be prepared, but it does not authorize full offline support, public app-store release, tester enrollment, or pilot enrollment.

Scope: responsive web/PWA readiness, TestFlight and Google Play internal/closed testing readiness, build verification, signing/account custody, privacy disclosures, tester access controls, crash reporting, support, release/rollback, authentication, device storage, channel compliance.

Required tests: responsive web/PWA smoke, build/signing verification, auth, device-storage review, no unsupported native/offline/push/background-sync claims.

Stop conditions: public app-store release, TestFlight tester enrollment, Google Play tester enrollment, push activation, native background sync, pilot enrollment.

Production impact: separate pilot-channel, tester-enrollment, and release decisions required.

## ES-TA-PRF-008 Retained Test-Baseline Classification And Burn-Down

Related decision: `ES-TA-FD-001`

Invariant: retained failures/errors are controlled technical debt, not blanket acceptance.

Scope: classify all 161 retained node IDs by node ID, product area, severity, root cause, test quality, pilot relevance, remediation owner, intended disposition, and closure evidence.

Required tests: per repaired/reclassified node; no skip/xfail/delete/weaken/broaden-ignore treatment.

Stop conditions: baseline increase without exact Founder approval, unowned P0/P1 residuals, test deletion/weakening.

Production impact: no production release by itself; required before pilot-gate execution.
