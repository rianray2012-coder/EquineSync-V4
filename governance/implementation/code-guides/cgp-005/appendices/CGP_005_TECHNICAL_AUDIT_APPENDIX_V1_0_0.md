# CGP-005 Technical Audit Appendix V1.0.0

Package ID: `ES-CGP-005-TECHNICAL-AUDIT-APPENDIX-V1.0.0`
Appendix date: `2026-07-27`
Repository: `rianray2012-coder/EquineSync-V4`
Base branch: `integrate-emergent-final-zip`
Reviewed repository head: `4afe3ccd84d9f8be1bc5c79bb27068676d993a70`
Working branch: `codex/cgp005-technical-audit-appendix-v1`

## Final Determination

`CGP005_APPENDIX_REQUIRED`

The CGP-005 source freeze remains valid as originally accepted and verified. The Technical Audit Founder decisions `ES-TA-FD-001` through `ES-TA-FD-008` add binding governance constraints that affect later Code Guide drafting and implementation planning. They do not replace any frozen CGP-005 source, do not change the CGP-005 selected source set, and do not require a CGP-005 amendment on the reviewed evidence.

## Purpose

This appendix records the governing constraints created by the Technical Audit Founder Decision Packet V1.1.0 so that CGP-006 Wave 1 drafting can refresh its inputs without silently promoting PR `#23` into the original CGP-005 source freeze.

This appendix exists to make later drafting traceable. It does not draft Code Guide controls, activate any Code Guide, change runtime behavior, or authorize implementation.

## Relationship To CGP-005

CGP-005 remains the controlling source-freeze package for Wave 1 curated normative source rows. This appendix supplements that freeze with later Founder-approved Technical Audit constraints. It does not replace, supersede, or amend the CGP-005 normative source set.

The original freeze remains accurate because:

- no CGP-005 selected source bytes changed;
- no CGP-005 source-freeze register row was replaced;
- no frozen source hash changed;
- no Code Guide adoption or activation state changed;
- PR `#23` did not modify files under `governance/implementation/code-guides/`;
- the CGP-006 initiation package already treated PR `#23` as non-normative context unless later authorized treatment was performed.

## Relationship To The Technical Audit Founder Decisions

The Technical Audit Founder Decision Packet V1.1.0 records final Founder dispositions for `ES-TA-FD-001` through `ES-TA-FD-008`. These decisions are governance authority with normative effect because they impose acceptance criteria, pilot gates, implementation constraints, provider boundaries, release-channel boundaries, sequencing, or non-authorization controls.

The decision package remains the controlling source for the exact decision language. This appendix is a Code Guide Program treatment of those decisions, not a substitute source.

## Relationship To CGP-006

CGP-006 may use this appendix as the traceable input-refresh basis for affected Wave 1 guide drafting. CGP-006 drafting remains bounded, not adopted, not active, and not implementation authority.

Candidate drafting may resume only after this appendix and the accompanying CGP-006 input refresh matrix are reviewed and accepted through the protected repository path. Implementation remains blocked unless separately authorized and unless the applicable decision constraints are satisfied.

## Source Integrity Statement

This appendix adds governing constraints only. It does not replace any normative source, supersede any controlling artifact, alter any approved hash, regenerate the CGP-005 source freeze, or change the original CGP-005 membership model.

Authority statement: this appendix supplements the existing CGP-005 freeze. It does not replace the CGP-005 normative source set.

## Non-Authorization Boundary

This package does not authorize runtime remediation, backend changes, frontend changes, tests, CI changes, schemas, migrations, infrastructure, provider activation, storage-provider activation, DocuSign activation, Adobe Acrobat Sign activation, alternate signature-provider activation, production envelope creation, signed-document custody, deployment, release promotion, Vercel or Render changes, Stripe configuration, payment activation, money movement, messaging activation, push activation, public app-store release, TestFlight tester enrollment, Google Play tester enrollment, pilot enrollment, public enrollment, remediation implementation, CGP-007, or production behavior.

## Reviewed Evidence

| Evidence | Reviewed result |
| --- | --- |
| Default branch head | `integrate-emergent-final-zip` at `4afe3ccd84d9f8be1bc5c79bb27068676d993a70`. |
| CGP-005 checksum ledger | Verified from `governance/implementation/code-guides`; all listed files OK. |
| CGP-006 initiation checksum ledger | Verified from `governance/implementation/code-guides`; all listed files OK. |
| Technical Audit Founder Decision package ledger | Verified from its package directory; all listed files OK. |
| PR `#23` | Merged at `3eb6825091241709f255b8ccf296987fa9b20724`; added Technical Audit Founder decision files only. |
| PR `#29` | Open draft, clean merge state, successful checks; contains the Document Authority Classification Framework. |
| PR `#30` | Open draft CGP-006 document classification branch observed; not merged into the reviewed default head. |
| Repository state versus classification report | Default head and PR `#29` classification basis remain materially aligned for this appendix. |

## Decision Constraint Records

### ES-TA-FD-001

Decision title: Retained test-failure and pilot-gate policy

Approval reference: `APPROVED_AS_RECOMMENDED` as `ZERO_UNRESOLVED_P0_AND_NODE_LEVEL_RETAINED_BASELINE_CONTROL`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: retained backend failures, known-failure policy, non-regression interpretation, P0/P1 pilot gate, and node-level baseline classification.

Implementation constraint: before pilot enrollment, unresolved P0 findings must be zero; pilot-relevant P1 findings must be repaired or individually accepted by written node-level Founder risk disposition; retained failures, errors, and node IDs must be classified. Tests may not be silently deleted, skipped, xfail-marked, weakened, hidden through broader ignores, or increased in baseline without exact node-level Founder approval.

Affected architecture and domains: backend test baseline, CI interpretation, pilot technical readiness, retained failure burn-down, acceptance evidence.

Affected Code Guides: `ES-CG-10` direct; `ES-CG-13` direct; `ES-CG-00` indirect; `ES-CG-01` indirect.

Drafting implication: CGP-006 must include this pilot-gate constraint in testing, evidence, charter-scope, and precedence drafting.

Implementation implication: no affected pilot-readiness implementation may proceed without satisfying the node-level classification and approval constraints and without separate implementation authority.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-002

Decision title: Cross-barn task mutation and authorization model

Approval reference: `APPROVED_AS_RECOMMENDED` as `FAIL_CLOSED_AUTHORITATIVE_TENANT_BARN_ACTOR_CONTEXT_CAPABILITY_MODEL`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: tenant, barn, actor, context, role, relationship, membership, and capability authorization.

Implementation constraint: every task read and mutation must be evaluated against authenticated actor identity, authoritative tenant, authoritative barn or facility, active role and context, current relationship or membership, and required capability. Every mutation must include authoritative tenant and barn predicates and must be reauthorized server-side at execution time. Cross-barn mutation is denied by default.

Affected architecture and domains: authorization model, multi-facility access, task reads and mutations, stale authority invalidation, denied-response confidentiality, offline replay authorization.

Affected Code Guides: `ES-CG-01` direct; `ES-CG-13` indirect; `ES-CG-10` indirect; `ES-CG-00` indirect.

Drafting implication: CGP-006 must treat fail-closed authority as a precedence and control boundary, with testing and traceability hooks.

Implementation implication: affected access or mutation implementation remains blocked until this model is specified, verified, and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-003

Decision title: Notification delivery and failure policy

Approval reference: `APPROVED_AS_RECOMMENDED` as `DURABLE_NOTIFICATION_DELIVERY_WITH_OBSERVABLE_FAILURES`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: notification creation, provider delivery, delivery states, retries, backoff, idempotency, dead-letter handling, duplicate prevention, opt-out handling, and log hygiene.

Implementation constraint: notification delivery must not use untracked fire-and-forget coroutine calls. Notification creation and provider delivery must be separate states. Delivery must use a durable queue, transactional outbox, or another separately justified durable mechanism, with observable failure and retry states.

Affected architecture and domains: notifications, digest delivery, provider boundary, retry/dead-letter workflow, observability, administrative resend behavior.

Affected Code Guides: `ES-CG-10` direct; `ES-CG-13` direct; `ES-CG-01` indirect; `ES-CG-00` indirect.

Drafting implication: CGP-006 must include durable delivery and observable failure constraints in testing and evidence drafting, and must preserve the no-provider-activation boundary.

Implementation implication: affected notification implementation remains blocked until durable delivery behavior is specified, tested, and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-004

Decision title: Production storage failure policy

Approval reference: `APPROVED_AS_RECOMMENDED` as `PRODUCTION_STORAGE_FAILS_CLOSED_NO_LOCAL_DEV_STUB`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: production storage configuration, upload behavior, document custody, provider initialization failure, health status, and stub isolation.

Implementation constraint: production must never silently use `local_dev_stub`. Missing production storage configuration or provider initialization failure must fail closed through startup failure, unhealthy status, feature disablement, bounded service-unavailable response, or equivalent controls. Production must not return fake or `STUB` upload success.

Affected architecture and domains: file upload, media and agreement storage, signed-document custody, production storage readiness, health and operational status.

Affected Code Guides: `ES-CG-10` direct; `ES-CG-13` direct; `ES-CG-01` indirect; `ES-CG-00` indirect.

Drafting implication: CGP-006 must preserve fail-closed production storage constraints, evidence requirements, and the no-provider-selection/no-migration boundary.

Implementation implication: affected storage and document features remain unavailable for production use until production storage is configured, verified, and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-005

Decision title: Background-job leadership and duplicate-execution model

Approval reference: `APPROVED_AS_RECOMMENDED` as `DEDICATED_WORKER_OR_DATABASE_LEASE_BACKGROUND_JOB_CONTROL`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: recurring jobs, worker ownership, database lease or singleton worker design, duplicate schedule prevention, failover, split-brain handling, rolling deployment, idempotency, and observability.

Implementation constraint: web replicas must not independently execute duplicate recurring schedules. The chosen model must define ownership, acquisition, renewal, duration, expiry, failover, clock assumptions, split-brain handling, graceful shutdown, and rolling-deployment behavior. Pilot-visible scheduled jobs must remain disabled unless leadership and duplicate-execution controls are implemented and verified.

Affected architecture and domains: background jobs, notification reminders, status synchronization, retry processing, scheduler topology, operational visibility.

Affected Code Guides: `ES-CG-10` direct; `ES-CG-13` direct; `ES-CG-01` indirect; `ES-CG-00` indirect.

Drafting implication: CGP-006 must represent job-leadership controls as testable and evidenced constraints.

Implementation implication: affected scheduled job implementation remains blocked until the leadership model is chosen, verified, and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-006

Decision title: Offline product posture and controlled native pilot distribution

Approval reference: `APPROVED_WITH_MODIFICATION` as `ONLINE_FIRST_LIMITED_ACTOR_BOUND_FIELD_RECOVERY_WITH_CONTROLLED_NATIVE_PILOT_DISTRIBUTION`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: online-first product posture, bounded cached reads, narrow queued writes, field recovery, replay reauthorization, sensitive cache expiration, account isolation, and native beta boundary.

Implementation constraint: EquineSync remains online-first for controlled pilot. Initial offline functionality is limited to bounded cached reads, narrow low-risk queued writes, and limited field-recovery behavior. Every queued mutation must be bound to authenticated actor ID, active role or context ID, authoritative barn or facility ID, client operation ID, creation timestamp, authorization version, and affected record identity. Every replay must be reauthorized against current identity, tenant, barn, role, relationship, and capability.

Affected architecture and domains: offline queue, replay authorization, cache isolation, logout/account-switch behavior, native beta distribution, product claims.

Affected Code Guides: `ES-CG-01` direct; `ES-CG-13` direct; `ES-CG-10` direct; `ES-CG-00` indirect.

Drafting implication: CGP-006 must preserve online-first language, limited field recovery, actor/context/barn binding, replay denial/quarantine states, and the prohibition on full offline claims.

Implementation implication: affected offline, sync, replay, and native-beta work remains blocked unless bounded by these constraints and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-007

Decision title: Production-ready legal electronic-signature capability

Approval reference: `APPROVED_WITH_MODIFICATION` as `PRODUCTION_READY_DOCUSIGN_REQUIRED_BEFORE_PILOT_WITH_PROVIDER_NEUTRAL_LEGAL_ESIGNATURE_ADAPTER`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: production-ready DocuSign, provider-neutral legal e-signature adapter, envelope and document identity, signer roles, webhook authenticity, event idempotency, secure custody, retention, support, privacy, legal review, and exact activation approval.

Implementation constraint: a complete production-ready DocuSign capability is required before pilot enrollment. The legal-signature implementation must use a provider-neutral adapter and domain contract. No pilot enrollment, production envelope sending, legal-signature claim, signed-document custody, or provider activation is authorized merely by the documentary decision; a separate readiness package and exact Founder activation approval are required.

Affected architecture and domains: legal e-signature adapter, provider boundary, signed-document custody, webhook handling, production storage dependency, privacy/legal/evidentiary review, pilot gate.

Affected Code Guides: `ES-CG-01` direct; `ES-CG-13` direct; `ES-CG-10` direct; `ES-CG-00` indirect.

Drafting implication: CGP-006 must encode DocuSign readiness as a mandatory pilot gate while preserving provider-neutral architecture and separate activation authority.

Implementation implication: affected legal-signature and pilot-enrollment implementation remains blocked until readiness, custody, storage, evidence, and exact Founder activation requirements are satisfied and separately authorized.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

### ES-TA-FD-008

Decision title: Controlled pilot delivery channel

Approval reference: `APPROVED_WITH_MODIFICATION` as `CONTROLLED_WEB_PWA_AND_PRIVATE_NATIVE_BETA_PILOT_CHANNEL`

Authority effect: `GOVERNANCE_WITH_NORMATIVE_EFFECT`

Governing technical area: controlled web, installable PWA, Apple TestFlight, Google Play internal testing, Google Play closed testing, public-store prohibition, native beta readiness, tester access, support, rollback, device storage, push boundary, and native background-sync boundary.

Implementation constraint: controlled pilot delivery may be prepared through responsive web, installable PWA, Apple TestFlight, Google Play internal testing, or Google Play closed testing. Public iOS App Store release and public Google Play production release are not authorized. Private native beta distribution may proceed only after channel-specific readiness gates. Tester enrollment, pilot enrollment, push activation, native background sync, and public enrollment remain separately blocked.

Affected architecture and domains: delivery channel, release readiness, native beta controls, device-storage review, support and rollback, privacy disclosure, app-store boundary.

Affected Code Guides: `ES-CG-00` direct; `ES-CG-01` direct; `ES-CG-13` direct; `ES-CG-10` indirect.

Drafting implication: CGP-006 must preserve the allowed delivery channels and the explicit non-authorization of public store release, tester enrollment, pilot enrollment, push, and native background sync.

Implementation implication: affected web/PWA/native-channel preparation remains blocked until channel gates and separate authorizations are satisfied.

Repository references: `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md`; `FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md`; `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv`; `DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv`.

## Constraint Mapping To Wave 1 Code Guides

| Decision | `ES-CG-00` | `ES-CG-01` | `ES-CG-10` | `ES-CG-13` | Written justification |
| --- | --- | --- | --- | --- | --- |
| `ES-TA-FD-001` | `INDIRECT` | `INDIRECT` | `DIRECT` | `DIRECT` | The retained-failure pilot gate is primarily testing and evidence work; charter and precedence text must preserve non-authorization and acceptance boundaries. |
| `ES-TA-FD-002` | `INDIRECT` | `DIRECT` | `INDIRECT` | `INDIRECT` | The fail-closed tenant/barn/actor/context/capability model is an authority and precedence constraint with evidence and test implications. |
| `ES-TA-FD-003` | `INDIRECT` | `INDIRECT` | `DIRECT` | `DIRECT` | Durable notification delivery must be testable and evidenced; authority text must preserve provider-activation boundaries. |
| `ES-TA-FD-004` | `INDIRECT` | `INDIRECT` | `DIRECT` | `DIRECT` | Production storage fail-closed behavior requires verification and custody evidence; charter and precedence preserve provider and migration non-authorization. |
| `ES-TA-FD-005` | `INDIRECT` | `INDIRECT` | `DIRECT` | `DIRECT` | Background-job leadership is primarily an assurance and traceability constraint with governance boundary effects. |
| `ES-TA-FD-006` | `INDIRECT` | `DIRECT` | `DIRECT` | `DIRECT` | Online-first, actor-bound field recovery, and replay reauthorization are authority, assurance, and evidence constraints; charter text must prevent full-offline overclaiming. |
| `ES-TA-FD-007` | `INDIRECT` | `DIRECT` | `DIRECT` | `DIRECT` | DocuSign readiness and provider-neutral adapter boundaries are authority constraints with mandatory testing and evidence gates before pilot. |
| `ES-TA-FD-008` | `DIRECT` | `DIRECT` | `INDIRECT` | `DIRECT` | Delivery-channel scope directly affects charter and authority drafting, with evidence requirements and verification implications. |

## CGP-006 Input Refresh Summary

| Code Guide | Refresh required | Drafting status after refresh | Summary |
| --- | --- | --- | --- |
| `ES-CG-00` | `MINOR_REFRESH` | `READY_AFTER_REFRESH` | Add charter and scope treatment for pilot gates, online-first boundaries, channel permissions, and non-authorization. |
| `ES-CG-01` | `MAJOR_REFRESH` | `READY_AFTER_REFRESH` | Add authority, precedence, and implementation-boundary treatment for the eight Founder decisions. |
| `ES-CG-10` | `MAJOR_REFRESH` | `READY_AFTER_REFRESH` | Add test, verification, acceptance, and provider/channel readiness constraints. |
| `ES-CG-13` | `MAJOR_REFRESH` | `READY_AFTER_REFRESH` | Add evidence, traceability, completion, pilot-gate, and readiness-package constraints. |

## Drift Determination

`GOVERNANCE_DRIFT`

The drift from the original CGP-005 baseline to the current execution is governance drift: PR `#23` added Founder-approved Technical Audit constraints after CGP-005; PR `#29` records a classification framework as an open draft; PR `#30` is an open draft CGP-006 classification branch observed during fetch. None of these changed the reviewed default head, the original CGP-005 selected source bytes, or the CGP-005 checksum verification used by this appendix.

## Validation Status

`CGP_005_APPENDIX_VALIDATED_WITH_RETAINED_GAPS`

The appendix is validated for protected review as an additive documentary package. Retained gaps are review and acceptance of this package, CGP-006 input incorporation, and all later implementation, provider, pilot, release, and activation gates.
