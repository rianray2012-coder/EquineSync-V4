# Technical-Audit Founder Decision Packet V1.1.0

Package ID: `ES-TA-FD-001-008-V1.1.0`

Directive ID: `ES-FOUNDER-DISPOSITION-TA-FD-001-008-2026-07-26-01`

Repository: `rianray2012-coder/EquineSync-V4`

Protected integration branch: `integrate-emergent-final-zip`

Protected production branch: `release/production`

Controlling technical-audit determination: `TECHNICAL_AUDIT_COMPLETED_WITH_PRODUCT_DECISIONS_REQUIRED`

Predecessor decision-packet determination: `FOUNDER_DECISION_PACKET_READY_FOR_REVIEW`

Deployment-control status: `AUTOMATIC_PRODUCTION_PROMOTION_CLOSED_WITH_PROTECTED_RELEASE_BRANCH`

Package status: `FOUNDER_APPROVED_DOCUMENTARY_PRODUCT_POLICY_DISPOSITIONS`

## Source Treatment

This V1.1.0 package adopts and records final Founder dispositions for `ES-TA-FD-001` through `ES-TA-FD-008`. It preserves the predecessor packet as historical source evidence and does not overwrite it.

The predecessor package was verified by `PRODUCT_DECISION_PACKET_SHA256SUMS.txt` before drafting. The expected source hashes matched.

Current remote integration head at package preparation: `636b104a8766f08eb1e4b57d1bc840ef217187e9`.

Source packet context head: `991d9ea816e5f1309431e7bb66640a3aa8805445`.

Drift from the source context to the current integration head was confined to governance/code-guide documentary files under `governance/implementation/code-guides/`. Drift from the original technical-audit base additionally includes the already-accepted six-file deployment-control documentary closure under `governance/implementation/deployment-control/`. No backend, frontend, CI, provider configuration, deployment configuration, environment, schema, migration, Stripe, payment, or test-baseline runtime drift was observed in the drift check used for this packet.

## Global Non-Authorization Boundary

This package does not authorize runtime remediation, backend changes, frontend changes, test changes, CI changes, implementation branches, remediation pull requests, database migration, storage-provider activation, DocuSign activation, Adobe Acrobat Sign activation, alternate signature-provider activation, production envelope creation, signed-document custody, production deployment, release promotion, Vercel or Render changes, Stripe configuration, payment activation, money movement, messaging activation, push activation, public app-store release, TestFlight tester enrollment, Google Play tester enrollment, pilot enrollment, public enrollment, governance supersession, archival deletion, or M4 work.

## Final Disposition Table

| Decision | Title | Founder Disposition | Controlling Disposition Identifier | Related Remediation Family |
| --- | --- | --- | --- | --- |
| `ES-TA-FD-001` | Retained test-failure and pilot-gate policy | `APPROVED_AS_RECOMMENDED` | `ZERO_UNRESOLVED_P0_AND_NODE_LEVEL_RETAINED_BASELINE_CONTROL` | `ES-TA-PRF-008` |
| `ES-TA-FD-002` | Cross-barn task mutation and authorization model | `APPROVED_AS_RECOMMENDED` | `FAIL_CLOSED_AUTHORITATIVE_TENANT_BARN_ACTOR_CONTEXT_CAPABILITY_MODEL` | `ES-TA-PRF-001` |
| `ES-TA-FD-003` | Notification delivery and failure policy | `APPROVED_AS_RECOMMENDED` | `DURABLE_NOTIFICATION_DELIVERY_WITH_OBSERVABLE_FAILURES` | `ES-TA-PRF-003` |
| `ES-TA-FD-004` | Production storage failure policy | `APPROVED_AS_RECOMMENDED` | `PRODUCTION_STORAGE_FAILS_CLOSED_NO_LOCAL_DEV_STUB` | `ES-TA-PRF-002` |
| `ES-TA-FD-005` | Background-job leadership and duplicate-execution model | `APPROVED_AS_RECOMMENDED` | `DEDICATED_WORKER_OR_DATABASE_LEASE_BACKGROUND_JOB_CONTROL` | `ES-TA-PRF-004` |
| `ES-TA-FD-006` | Offline product posture and controlled native pilot distribution | `APPROVED_WITH_MODIFICATION` | `ONLINE_FIRST_LIMITED_ACTOR_BOUND_FIELD_RECOVERY_WITH_CONTROLLED_NATIVE_PILOT_DISTRIBUTION` | `ES-TA-PRF-005`, `ES-TA-PRF-007` |
| `ES-TA-FD-007` | Production-ready legal electronic-signature capability | `APPROVED_WITH_MODIFICATION` | `PRODUCTION_READY_DOCUSIGN_REQUIRED_BEFORE_PILOT_WITH_PROVIDER_NEUTRAL_LEGAL_ESIGNATURE_ADAPTER` | `ES-TA-PRF-006` |
| `ES-TA-FD-008` | Controlled pilot delivery channel | `APPROVED_WITH_MODIFICATION` | `CONTROLLED_WEB_PWA_AND_PRIVATE_NATIVE_BETA_PILOT_CHANNEL` | `ES-TA-PRF-007` |

## ES-TA-FD-001 Final Disposition

Founder approves `ES-TA-FD-001` as `ZERO_UNRESOLVED_P0_AND_NODE_LEVEL_RETAINED_BASELINE_CONTROL`.

No retained failure or error is accepted by blanket waiver. Before pilot enrollment there must be zero unresolved P0 findings, every pilot-relevant P1 finding must be repaired or individually accepted by written node-level Founder risk disposition, and the 158 retained failures, 3 retained errors, and 161 retained node IDs must be classified by node ID, product area, severity, root cause, test quality, pilot relevance, remediation owner, intended disposition, and closure evidence.

No test may be silently deleted, skipped, xfail-marked, weakened, excluded, or hidden through broadened ignore rules. No known-failure baseline increase is permitted without exact node-level Founder approval. Baseline reductions may occur only through passing behavioral evidence or a documented determination that the underlying requirement was formally superseded. A passing non-regression ratchet must not be represented as proof that the full backend suite is healthy. Raw pytest success before public launch remains a later release-gate determination unless adopted earlier through a separate Founder decision.

## ES-TA-FD-002 Final Disposition

Founder approves `ES-TA-FD-002` as `FAIL_CLOSED_AUTHORITATIVE_TENANT_BARN_ACTOR_CONTEXT_CAPABILITY_MODEL`.

Active context alone is insufficient for access or mutation. Every task read and mutation must be evaluated against authenticated actor identity, authoritative tenant, authoritative barn or facility, active role and context, current relationship or membership, and required capability. Every mutation must contain authoritative tenant and barn predicates and must be reauthorized server-side at execution time. Cross-barn mutation is denied by default.

Trainer multi-facility access must use explicit context and current relationship-based capability. Platform-level administrative access, if later permitted, must be exceptional, separately authorized, least-privileged, time-bounded where practical, and auditable. Denied responses must not reveal another barn's records. Relationship removal, role change, barn removal, and permission change must invalidate stale authority. The retained cross-barn isolation errors must be resolved or affected workflows excluded from pilot scope.

## ES-TA-FD-003 Final Disposition

Founder approves `ES-TA-FD-003` as `DURABLE_NOTIFICATION_DELIVERY_WITH_OBSERVABLE_FAILURES`.

Notification delivery must not use untracked fire-and-forget coroutine calls. Notification creation and provider delivery must be separate states. Delivery must use a durable queue, transactional outbox, or another separately justified durable mechanism. Originating care, task, or business transactions may complete while an unavailable email provider remains a retryable delivery failure.

Delivery states must include pending, queued, sending, sent, retrying, failed, dead-lettered, and suppressed where applicable. Retry, backoff, duplicate prevention, idempotency, dead-letter handling, and administrative resend behavior must be defined and tested. Invalid addresses, opt-outs, provider failure, partial digest failure, and duplicate dispatch must be bounded. Logs must not expose secrets, raw provider payloads, or unnecessary message content. Live provider activation remains separately controlled.

## ES-TA-FD-004 Final Disposition

Founder approves `ES-TA-FD-004` as `PRODUCTION_STORAGE_FAILS_CLOSED_NO_LOCAL_DEV_STUB`.

Production must never silently use `local_dev_stub`. Stub storage may be used only in explicitly configured development or isolated test environments. Missing production storage configuration or provider initialization failure must fail closed through startup failure, unhealthy service status, feature disablement, bounded service-unavailable response, or a combination of those controls.

Production must not return fake or `STUB` upload success. Sensitive files, media, agreements, or signed documents must not be written to uncontrolled local storage. Health and operational status must expose provider availability without exposing credentials or secrets. Upload and document features must remain unavailable until production storage is configured and verified. This decision does not select a storage provider or authorize file migration.

## ES-TA-FD-005 Final Disposition

Founder approves `ES-TA-FD-005` as `DEDICATED_WORKER_OR_DATABASE_LEASE_BACKGROUND_JOB_CONTROL`.

Web replicas must not independently execute duplicate recurring schedules. The initial implementation may use a dedicated singleton worker, a database-backed distributed lease, or a separately justified equivalent mechanism. The chosen model must define ownership, acquisition, renewal, duration, expiry, failover, clock assumptions, split-brain handling, graceful shutdown, and rolling-deployment behavior.

Downstream job idempotency remains mandatory. Job ownership, lease state, last-run status, retry state, and failures must be observable. Pilot-visible scheduled jobs must remain disabled unless leadership and duplicate-execution controls are implemented and verified. Provider topology or worker deployment changes require separate authorization.

## ES-TA-FD-006 Final Disposition

Founder approves `ES-TA-FD-006` as `ONLINE_FIRST_LIMITED_ACTOR_BOUND_FIELD_RECOVERY_WITH_CONTROLLED_NATIVE_PILOT_DISTRIBUTION`.

EquineSync remains online-first for the controlled pilot. The controlled pilot may be distributed through responsive web, installable PWA, Apple TestFlight, Google Play internal testing, or Google Play closed testing. Native beta distribution does not authorize or imply full offline support.

Initial offline functionality may include bounded cached reads, a narrow allowlist of low-risk queued writes, and limited field-recovery behavior. Every queued mutation must be bound to authenticated actor ID, active role or context ID, authoritative barn or facility ID, client operation ID, creation timestamp, authorization version, and affected record identity. The server must reauthorize every replay against current identity, tenant, barn, role, relationship, and capability.

Logout, account switching, role removal, relationship removal, barn removal, or credential expiration must prevent silent replay. Invalid queued items must be denied, quarantined, cancelled, or presented for user review according to a documented policy. Queue states must be visible where relevant, including pending, retrying, synchronized, failed, denied, quarantined, and cancelled.

Sensitive cached data must have defined expiration and account-isolation controls. Product and pilot language must not claim full offline operation. Broad offline task or care operations, native background synchronization, and unrestricted offline mutation remain unauthorized. Public App Store and public Google Play release remain separately controlled. Build distribution, privacy disclosures, crash reporting, tester access, support procedures, and device-security requirements must be verified before native pilot enrollment.

## ES-TA-FD-007 Final Disposition

Founder approves `ES-TA-FD-007` as `PRODUCTION_READY_DOCUSIGN_REQUIRED_BEFORE_PILOT_WITH_PROVIDER_NEUTRAL_LEGAL_ESIGNATURE_ADAPTER`.

A complete, production-ready DocuSign capability is required before pilot enrollment. This replaces the predecessor recommendation to defer production DocuSign from the initial pilot.

DocuSign readiness must include production account and application ownership, controlled production credentials and secret custody, authenticated envelope creation, document-template and document-version control, recipient and signer identity handling, guardian and minor-signature treatment where applicable, embedded or remote signing workflow, signing-session and callback handling, authenticated webhook verification, replay-safe webhook processing, event idempotency and duplicate prevention, status reconciliation, signed-document retrieval, completion-certificate retrieval, secure document custody, production storage readiness under `ES-TA-FD-004`, signed-document access control, retention and deletion treatment, cancellation, resend, decline, expiration, retry and provider-outage handling, audit-trail preservation, privacy review, legal and evidentiary review, observability and reconciliation procedures, support and recovery procedures, behavioral tests, negative tests, webhook security tests, failure-recovery tests, production-readiness evidence, and separate exact Founder activation approval.

The legal-signature implementation must use a provider-neutral adapter and domain contract. DocuSign-specific concepts must not be embedded throughout general EquineSync product, agreement, user, horse, facility, or workflow logic. The adapter must support later qualification of another legally and technically acceptable electronic-signature provider, including Adobe Acrobat Sign, another Founder-approved provider, or a future provider satisfying the same legal, security, custody, privacy, evidentiary, operational, and reliability requirements.

The provider-neutral contract must account for provider identity, envelope or agreement identity, document identity and version, recipient and signer roles, provider-neutral status states, provider event normalization, webhook authenticity, provider event idempotency, signing URL or signing-session creation, completed-document retrieval, completion-certificate retrieval, cancellation and expiration, error mapping, retryability, audit metadata, custody metadata, retention metadata, and provider readiness state.

DocuSign remains the initially required production-ready provider. A future alternate provider may not replace the initial DocuSign readiness gate unless the Founder separately amends this decision. No pilot enrollment, production envelope sending, legal-signature claim, signed-document custody, or provider activation is authorized merely by this documentary decision. A separate readiness package and exact Founder activation approval are required.

## ES-TA-FD-008 Final Disposition

Founder approves `ES-TA-FD-008` as `CONTROLLED_WEB_PWA_AND_PRIVATE_NATIVE_BETA_PILOT_CHANNEL`.

The controlled pilot may be delivered through responsive web, installable PWA, Apple TestFlight, Google Play internal testing, or Google Play closed testing.

Public iOS App Store release is not authorized. Public Google Play production release is not authorized. Private native beta distribution may proceed only after build verification, signing and account custody verification, privacy disclosure review, tester-access controls, crash-reporting readiness, support procedures, release and rollback procedures, authentication testing, device-storage review, and channel-specific compliance review.

Native distribution does not imply full offline support, native background synchronization, push-notification readiness, production app-store readiness, or public enrollment. Push-notification activation requires separate approval. Native background-sync capability requires separate approval. App Store and Play Store public-listing materials remain deferred. Pilot enrollment remains blocked until all controlling pilot gates, including `ES-TA-FD-001` and `ES-TA-FD-007`, are satisfied and separately approved.

## Cross-Decision Consistency

- `ES-TA-FD-001` remains the overall technical pilot gate.
- `ES-TA-FD-006` and `ES-TA-FD-008` jointly authorize preparation for controlled private native beta distribution, but they do not authorize full offline support, public app-store release, tester enrollment, or pilot enrollment.
- `ES-TA-FD-007` creates a mandatory pilot gate: no pilot enrollment until production DocuSign readiness is completed and separately activated by exact Founder approval.
- `ES-TA-FD-004` is a dependency for signed-document custody.
- `ES-TA-FD-002` applies to documents, agreements, queued offline writes, and native-client requests.
- `ES-TA-FD-003` and `ES-TA-FD-005` apply to signature notifications, reminders, status synchronization, retry processing, and background scheduling.
- Private native beta distribution may be technically prepared before all pilot gates close, but real user enrollment remains separately blocked.
- No decision authorizes production release, provider activation, pilot enrollment, public app-store release, database migration, live messaging, payment activation, or money movement.

## Revised Remediation Sequence

1. `ES-TA-PRF-001` Cross-Barn Authorization And Isolation
2. `ES-TA-PRF-002` Production Storage Fail-Closed Behavior
3. `ES-TA-PRF-003` Notification Coroutine And Delivery Reliability
4. `ES-TA-PRF-004` Background-Job Leadership And Duplicate-Execution Controls
5. `ES-TA-PRF-005` Offline Actor Context Barn Binding
6. `ES-TA-PRF-006` Provider-Neutral Legal ESignature Adapter And DocuSign Production Readiness
7. `ES-TA-PRF-007` Controlled Web PWA And Private Native Beta Pilot Readiness
8. `ES-TA-PRF-008` Retained Test-Baseline Classification And Burn-Down

`ES-TA-PRF-008` node classification should begin as a parallel documentary workstream because the complete 161-node register is required before pilot-gate execution.

## Final Package Determination

`FOUNDER_DECISIONS_ES_TA_FD_001_008_APPROVED_FOR_DOCUMENTARY_RECORDING`
