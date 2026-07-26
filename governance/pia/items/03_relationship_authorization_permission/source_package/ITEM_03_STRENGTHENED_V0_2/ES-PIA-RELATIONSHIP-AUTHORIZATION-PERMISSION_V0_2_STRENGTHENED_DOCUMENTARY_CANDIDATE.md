# Relationship, Authorization, and Permission PIA

**PIA ID:** `ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION`
**Version:** `0.2`
**Status:** `ITEM_03_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`
**Classification:** `FOUNDATIONAL_DOCUMENTARY_SUCCESSOR_CANDIDATE`
**Components:** `A_RELATIONSHIP; B_AUTHORIZATION; C_PERMISSION`
**Predecessor:** `ITEM_03_INITIAL_DRAFT_V0_1`
**Founder decision incorporated:** `ES-PIA-GFD-003`
**Implementation Authority:** `FALSE`
**Migration Authority:** `FALSE`
**Deployment Authority:** `FALSE`
**Enrollment Authority:** `FALSE`
**Independent review completed:** `FALSE`

This separate V0.2 candidate strengthens the preserved integrated A/B/C V0.1 review object. It incorporates the Founder-approved documentary allocation in `ES-PIA-GFD-003` and does not ratify the current Component A successor, candidate ADRs, or any implementation. Documentary completeness is not independent review.

## 1. Document Control and Status

The Founder is the sole approval authority. This package is a documentary successor candidate dated 2026-07-22. V0.1 remains immutable and is not overwritten. Formal review is `NOT_STARTED`; adoption, ratification, constitutional lock, implementation, migration, deployment, activation, production use, and enrollment are all `FALSE`.

Exact disposition: `ITEM_03_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`.

## 2. Executive Summary

Item 03 defines an authority chain without collapsing identity, account, actor, principal, relationship, representation, delegation, authorization, permission, restriction, claim, agreement, provider relationship, facility context, payment status, or portal participation. Component A owns relationship, representation, and delegation truth. Component B assembles typed, current, purpose-bound authorization inputs and records attributable decisions. Component C evaluates and enforces minimum permission projections.

No identity, role label, payment, possession, contact information, shared address, facility association, organization association, provider status, schedule assignment, portal access, onboarding sequence, profile, API credential, appointment, or integration independently creates relationship or permission.

Provider connection, profile status, API access, appointment participation, payment, or portal visibility never independently creates authority. No runtime is provisioned or launched under this directive.

## 3. Purpose, Outcomes, and Success Measures

The purpose is to give every protected workflow a traceable contract for who may request, represent, approve, perform, view, correct, delegate, revoke, restrict, or dispute an action. Documentary success requires complete registers, source and decision traceability, deny-by-default logic, restriction precedence, revocation handling, bounded offline behavior, objective acceptance/test definitions, and explicit unresolved authority.

Success here means the candidate is sufficiently specified for a compliant fresh review. It does not mean engineering, operations, release, or enrollment readiness.

## 4. Authoritative Sources and Inheritance

`SOURCE_REGISTER.csv` identifies the controlling and state-qualified sources. Adopted Master PIA Standard V1.1 and locked Relationship, Permission, Agreement, Claims, Privacy, Safeguarding, Audit, and Records canons control their respective domains. The underlying Relationship design remains Founder-approved. The current Component A successor, candidate ADRs, and authorization interface remain predecessor-qualified and pending fresh review.

The 2026-07-22 Founder approval record controls the GFD-003 scope allocation only. It cannot approve a successor, launch a review runtime, authorize implementation, or cure unresolved predecessor authority.

## 5. Scope, Boundaries, and Ownership

Included scope: relationship claims and types; representation bases; delegation lifecycle; authorization inputs and decisions; permission projections; restrictions; revocations; disputes; provider authority boundaries; source freshness; offline proposals; correction; and evidence.

Excluded scope: identity authentication truth; Facility/Tenant/Organization topology; horse truth; care, scheduling, participation, financial, portal, or reporting workflow truth; jurisdiction-specific legal conclusions; schemas; migrations; application architecture; code; provider activation; deployment; and production operations.

Under GFD-003, Item 03 owns provider relationship, representation, delegation, and authority. Item 07 owns provider care coordination, Item 10 owns provider participation and portal surfaces, and Item 09 owns provider fees, obligations, payments, and payouts.

## 6. Definitions and Controlled Vocabulary

- **Identity:** canonical fact about who or what an entity is; it does not grant authority.
- **Account:** authentication and access container associated with a principal; it does not itself establish an actor capacity.
- **Actor:** attributable human or system participant in an action.
- **Principal:** person or organization for whom an actor acts.
- **Relationship:** versioned, sourced link between canonical parties under a defined type, capacity, scope, time, and status.
- **Representation:** evidence-backed basis for an actor to act for a principal.
- **Delegation:** bounded, accepted when required, time-limited transfer of an existing authority that cannot exceed its source.
- **Authorization:** evaluation of current inputs and policy for one requested action.
- **Permission:** enforceable minimum projection produced by authorization evaluation.
- **Restriction:** explicit narrowing or denial with precedence over inferred allow.
- **Claim:** attributable assertion subject to verification, dispute, correction, and supersession.
- **Agreement:** versioned commitment or consent record; not self-executing permission.
- **Provider relationship:** canonical relationship and authority evidence for a provider, distinct from profile, portal, API, appointment, care, and payment states.

## 7. Actors, Roles, Relationships, and Authorities

Every consequential action identifies the authenticated actor, acting actor, represented principal, approving actor, executing actor, affected subject, tenant/context, and accountable human where a system actor participates. Role is descriptive input, relationship is source truth, representation identifies the acting basis, delegation narrows source authority, authorization evaluates the request, and permission enforces the outcome.

Guardian and minor-related authority requires a current, purpose-scoped representation basis, applicable agreement/consent, protective restrictions, and safeguarding checks. A claimed family label, shared address, payment, account association, or emergency assertion is not sufficient.

## 8. Capability Map and Release Classification

Documented capabilities are relationship lifecycle, representation, delegation, authorization request/decision, permission projection, restriction/revocation, dispute/correction, provider boundary, evidence, and offline proposal reconciliation. High-risk families include guardian/minor, provider, care, financial, export, support, emergency, cross-tenant, and authority-changing actions.

Release classification is `DEFERRED_TO_IMPLEMENTATION_ATLAS`. No capability is implementation-authorized.

## 9. User and Operational Workflows

Required documentary workflows are: assert and verify a relationship; propose and accept representation; create, narrow, reject, expire, revoke, or dispute a delegation; assemble authorization inputs; evaluate permission; enforce a minimum projection; explain denial safely; apply restriction; propagate revocation; correct source truth without destructive history; reconcile an offline proposal; and reconstruct a decision.

Provider onboarding, profile creation, API connection, appointment participation, portal visibility, or payment must remain separate workflows that cannot self-create Item 03 authority.

## 10. Business Rules and Decision Logic

1. Deny by default.
2. Require canonical principal and accountable actor attribution.
3. Treat context and role as inputs, never authority.
4. Require current source, relationship, representation, delegation, agreement, restriction, and policy versions as applicable.
5. A delegation cannot exceed, outlive, or survive invalidation of its source authority.
6. Explicit restriction, revocation, expiry, dispute, incompatibility, or protective narrowing overrides inferred allow.
7. Return the minimum action, object, field, purpose, time, tenant, and state projection.
8. Preserve exact evaluated versions, outcome, reason codes, correlation, and correction lineage.
9. Never infer provider authority from connection, profile, API, appointment, payment, or portal state.

## 11. Data Entities, Relationships, and Provenance

Documentary entities include `RelationshipClaim`, `RelationshipTypeVersion`, `PartyCapacity`, `RepresentationBasis`, `DelegationGrant`, `VerificationAssessment`, `SourceAuthorityReference`, `AuthorizationRequest`, `AuthorizationDecision`, `PermissionProjection`, `Restriction`, `RevocationWatermark`, `DisputeReference`, `DecisionExplanation`, and `CorrectionSupersessionLink`.

Each material record carries stable ID, version, tenant, source owner, accountable actor, provenance, effective and recorded times, purpose, scope, status, restrictions, sensitivity, correlation, and supersession links as applicable. Derived decisions list every material source version.

## 12. Record Ownership, Stewardship, Correction, and Retention

Component A owns relationship, representation, and delegation records. Component B owns authorization request/decision evidence. Component C owns permission-policy references and enforcement outcomes. Identity, facility, horse, care, scheduling, participation, financial, portal, agreement, claims, and reporting domains retain their own truth.

Correction creates an attributable successor and preserves prior bytes, identifiers, evaluated decisions, and supersession lineage. Revoking access does not erase valid history. Retention and export remain governed by Records, Privacy, Claims, Agreement, legal-hold, and owning-domain authority; no duration is invented here.

## 13. State and Transition Models

`STATE_TRANSITION_MATRIX.csv` defines allowed triggers, actors, guards, evidence, and prohibited automatic transitions. Relationship claims may move through asserted, provisional, active, disputed, suspended, ended, and superseded states. Delegations may move through proposed, pending acceptance, active, expired, revoked, ineligible, disputed, and superseded states.

Only explicit expiry or fail-closed invalidation may occur automatically. Relationship activation, delegation renewal, dispute resolution, authority expansion, provider activation, and protective-restriction override require separately authorized evidence and may not be inferred.

## 14. Authorization and Permission Matrix

`AUTHORIZATION_INPUT_REGISTER.csv`, `PERMISSION_MATRIX.csv`, and `PERMISSION_EVALUATION_CONTRACT.md` define the evaluation contract. Inputs include actor/principal chain, tenant/context, action, resource, fields, purpose, identity assurance, current relationship and representation, delegation, agreement, restriction, dispute, safeguarding, source versions, policy version, watermark, time, and device/sync state.

Outcome is `ALLOW_BOUNDED`, `DENY`, or `STEP_UP_REQUIRED`; no implicit allow exists. Enforcement occurs in a trusted boundary. UI visibility, cached data, schedule assignment, payment, or portal access is never proof of permission.

## 15. User Interface and Experience Requirements

Before a consequential action, the user must see the acting capacity, represented principal, tenant/context, action scope, affected subject, expiry, restrictions, and consequence. Denials expose safe reason categories without revealing protected facts. Delegation, revocation, restriction, dispute, correction, support, and provider access require accessible review surfaces.

Interfaces must not display identity, roles, relationship badges, provider profiles, payment, facility association, schedules, onboarding completion, or portal presence as equivalent to permission.

## 16. API, Event, Job, and Integration Contracts

`API_EVENT_JOB_CONTRACTS.md` defines typed, versioned, purpose-bound, tenant-scoped documentary contracts. Requests carry the principal chain, action/resource/fields, purpose, source and policy versions, context, freshness, watermark, correlation, and idempotency. Responses carry outcome, bounded projection, safe reasons, step-up, evaluated versions, generation, expiry, and watermark.

Events cover restriction, revocation, expiry, dispute, supersession, and correction. Jobs and integrations reauthorize at execution and cannot promote external claims, provider profiles, API credentials, appointments, payments, or portal states into canonical authority.

## 17. Notifications and Communications

Notices may be required for relationship assertion, representation request, delegation proposal/acceptance/rejection, restriction, revocation, dispute, correction, support access, provider authority change, and denied high-risk action. Item 10 owns communication surfaces and delivery behavior; Item 03 supplies the permission-filtered event and minimum content contract.

Delivery, read state, acknowledgment, click, or reply does not independently prove consent, relationship, representation, or authority.

## 18. Files, Media, and Document Handling

Identity proofs, guardian documents, agreements, provider credentials, court documents, and authority evidence are evidence objects, not self-executing authority. Their exact version, hash, source, presentation context, access projection, retention basis, malware controls, correction, and supersession must be preserved.

Possession, upload, signature-provider status, or successful verification of a file does not create capacity or permission beyond the approved evaluation contract.

## 19. Search, Reporting, and Analytics

Search and reporting consume permission-filtered projections and prevent cross-tenant or protected-record enumeration. Under GFD-004, each domain PIA owns canonical truth and metric definitions; Item 05 owns shared presentation, discovery, filtering, and administrative surfaces without becoming a competing system of record.

Authority reports identify definition owner, source, evaluated time, watermark, policy version, completeness limits, and correction state.

## 20. Offline, Device, and Synchronization

EquineSync remains online-first with limited field recovery. Offline work may preserve a non-authoritative proposal containing actor, device, tenant/context, source versions, policy/watermark, local time, clock confidence, purpose, reason, and idempotency key. It may not create, expand, or enforce new authority locally.

Synchronization reauthenticates and reauthorizes. Stale, revoked, disputed, expired, wrong-tenant, duplicate, incompatible, or restriction-conflicting proposals fail closed. Visible states are saved, queued, syncing, blocked, conflicted, failed, reconciled, and superseded. `OFFLINE_AND_SYNCHRONIZATION_REQUIREMENTS.md` controls ordering, replay, retries, deduplication, correction, and evidence.

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Controls include least privilege, tenant isolation, minimum disclosure, anti-enumeration, step-up, short-lived projections, separation of duties, session invalidation, revocation propagation, support visibility, anomaly review, and reason-coded denial. Guardian, minor, protected-participant, care, financial, dispute, and location information receive heightened treatment.

Protective restrictions narrow access and do not create a substitute delegation. Consent, authorization, acknowledgment, agreement, relationship, and permission remain distinct. Every authority-changing action requires accountable-human attribution unless a separately authorized named system action is explicitly permitted.

## 22. AI and Automation Controls

AI may summarize cited evidence, flag conflicts, or draft a request for human confirmation under controlling AI governance. It may not create or infer identity, relationship, representation, delegation, consent, permission, restriction, provider authority, clinical, legal, financial, or safeguarding truth; approve high-risk action; or bypass denial.

Automation requires a named system actor, accountable owner, narrow purpose, current authority watermark, explicit scope, attributable evidence, reversible failure handling, and human escalation. No model or provider execution is authorized by this package.

## 23. Failure Modes, Recovery, Correction, and Reconciliation

Required failures include missing, stale, revoked, expired, disputed, version-incompatible, wrong-tenant, duplicate, replayed, clock-uncertain, source-unavailable, watermark-mismatched, partially delivered, or evidence-store-failed conditions. The safe outcome is deny, step-up, or preserve a non-authoritative proposal for controlled reconciliation.

Conflict resolution orders explicit restriction/revocation and current authoritative versions ahead of cached or derived allow. Recovery never broadens access. Correction retains original evidence and explains why a later decision differs.

## 24. Observability, Administration, Support, and Incident Operations

Future design signals include decision latency, denial categories, step-up, stale/version failures, revocation propagation, cross-tenant denial, support access, provider-boundary denial, emergency use, evidence failure, retry queues, and reconciliation backlog. Thresholds, alerts, dashboards, runbooks, staffing, and service targets remain `DEFERRED_TO_IMPLEMENTATION_ATLAS`.

Support access must be ticketed, purpose-bound, time-limited, attributable, visible where appropriate, revocable, and reviewable. Support identity or administrator role never creates universal authority.

## 25. Nonfunctional and Quality Attribute Requirements

Any future implementation must be deterministic for identical current inputs, fail closed, tenant-isolated, explainable, auditable, revocation-responsive, privacy-minimizing, accessible, localization-ready, resilient to poor connectivity, and testable under concurrency and replay. Numeric latency, propagation, recovery, availability, and retention targets remain `TBD_IMPLEMENTATION_ATLAS` and are not invented here.

## 26. Environment, Configuration, Feature Flags, and Secrets

Policy, projection, assurance, step-up, restriction, and emergency controls must be versioned governance/configuration records with controlled promotion, rollback, attribution, and evidence. Feature flags cannot bypass authorization or activate unapproved authority bases. Secrets may not enter decisions, logs, prompts, exports, or client bundles.

No environment or runtime is provisioned by this package.

## 27. Migration, Seed Data, and Reconciliation

No migration is authorized. A future authorized plan must inventory legacy roles, memberships, provider links, relationship claims, permissions, tokens, support grants, tenant context, and source versions; map only with evidence; quarantine ambiguity; preserve identifiers and provenance; support dry run and rollback; and prevent migration from manufacturing authority.

Seed data must never create production relationships, representations, delegations, provider authority, or permissions.

## 28. Engineering Work Packages and Implementation Sequence

`DEFERRED_TO_IMPLEMENTATION_ATLAS`. A documentary sequence may later cover canonical contracts, state models, decision oracle, enforcement, revocation propagation, evidence, offline proposals, support controls, provider boundaries, notices, observability, migration tooling, adversarial tests, and staged release controls.

This ordering is planning context only and grants no build, schema, migration, deployment, activation, or production authority.

## 29. Acceptance Criteria

`ACCEPTANCE_CRITERIA.csv` defines objective documentary criteria. Core outcomes include: role without source authority denies; relationship alone does not grant permission; delegation cannot exceed or outlive its source; restriction and revocation narrow immediately at the next trusted evaluation; stale watermarks invalidate cached/offline requests; cross-tenant requests deny without enumeration; provider connection/profile/API/appointment/payment/portal states grant no authority; and every consequential decision is reconstructable.

No criterion is represented as executed implementation evidence.

## 30. Test and Validation Matrix

`TEST_MATRIX.csv` maps design tests to requirements and acceptance criteria. It covers normal, denial, expiry, revocation, dispute, restriction, wrong tenant, stale cache, replay, duplicate, clock uncertainty, guardian/minor, provider, financial, support, emergency, offline, correction, export, and evidence reconstruction paths.

Results are `DESIGN_TEST_DEFINED_NOT_EXECUTED`. Deterministic package validation checks documentary integrity only.

## 31. Golden-Path Reproduction Scenarios

`GOLDEN_PATHS.md` defines documentary reproductions for bounded owner delegation, guardian-authorized participation, facility-context operational access, provider horse-specific access, and approved support access. Each path identifies source authority, accountable actors, acceptance where required, current versions, restrictions, minimum projection, notice, revocation, and evidence.

No path is an executed product scenario.

## 32. Adversarial, Negative, and Abuse Scenarios

`ADVERSARIAL_SCENARIOS.md` includes role-label escalation, forged representation, stale relationship, delegation overflow, source revocation mid-session, tenant substitution, enumeration, cached allow after restriction, provider self-activation, support impersonation, payment-created access, guardian ambiguity, AI-inferred authority, replay, mass export, notification leak, and offline conflict.

Expected outcomes fail closed and preserve attributable evidence without leaking protected facts.

## 33. Evidence Requirements, Coverage, and Manifest

`AUDIT_AND_EVIDENCE_REQUIREMENTS.csv` requires principal chain, accountable actor, tenant/session, requested action and subject, exact source versions, policy version, restriction and revocation state, watermark, projection, outcome, reasons, time, correlation, step-up, notice, correction, and supersession evidence.

`ARTIFACT_MANIFEST.json` inventories all 28 package files. `CHECKSUM_LEDGER.sha256` covers the other 27 files and intentionally excludes itself. Mechanical manifests and logs are not independent review evidence.

## 34. Deployment, Rollout, Rollback, and Release Controls

No deployment, rollout, release, or activation is authorized. Future release requires an adopted PIA, separately authorized implementation atlas, completed security/privacy/safeguarding review, objective test evidence, migration rehearsal, tenant-isolation proof, revocation proof, rollback criteria, operational readiness, and express Founder decisions.

Rollback must restore a safe deny posture without erasing decision history.

## 35. Enrollment and Onboarding Readiness

First-user enrollment readiness is `NO`. Adaptive onboarding must avoid unnecessary Facility or Organization creation and must not let onboarding order, invitation, email domain, payment, shared address, context, provider profile, schedule, or portal access create relationship or permission.

Initial relationships and authority bases must be minimal, explicit, reviewable, revocable, and explainable before any separate enrollment authorization.

## 36. Dependencies and Critical Path

Critical sources are Item 01 identity truth; Item 02 context; the locked Relationship, Permission, Agreement, Claims, Privacy, Safeguarding, Audit, and Records canons; state-qualified Component A evidence; and the approved GFD-003 allocation. Item 03 exports authority contracts to Items 02, 04, 06, 07, 08, 09, and 10 without taking their domain truth.

The GFD-007 policy is approved, but a compliant runtime is not provisioned. Fresh independent review therefore remains pending. Component A successor authority, owning-domain concurrence, emergency policy, legal boundaries, operational targets, and implementation architecture remain explicitly unresolved.

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

`UNRESOLVED_ITEMS_REGISTER.csv` preserves every known unresolved item and its source-qualified disposition. GFD-003 is resolved as a documentary allocation; it does not resolve predecessor lifecycle, legal capacity, emergency policy, implementation, operations, or independent review.

`FINDING_DISPOSITION_MATRIX.csv` records documentary gap treatment only and is not a formal reviewer finding register. No deviation from the 43-section structure is asserted.

## 38. Implementation Drift and As-Built Reconciliation

No as-built scope is accepted. Any later authorized implementation must map requirements to code, schema, policy, configuration, tests, deployment, operations, and evidence; record deviations; and return product or governance changes for approval. Existing behavior cannot resolve ambiguity or amend this candidate.

No application code, schema, migration, dependency, build artifact, provider configuration, or operational state is changed by this package.

## 39. Change-Control History

V0.2 is a separate successor candidate that preserves V0.1 byte-for-byte. It incorporates GFD-003, completes the directed documentary registers, strengthens provider and cross-PIA boundaries, and retains predecessor-qualified/open matters. `REVISION_CHANGELOG.csv` maps each documentary change to source and requirement identifiers.

No prior evidence is superseded, ratified, adopted, locked, or implementation-authorized.

## 40. Requirement Traceability Matrix

`REQUIREMENT_REGISTER.csv` assigns unique `RAP-REQ-*` identifiers. `REVISED_TRACEABILITY_MATRIX.csv` maps all 43 sections to sources, requirements, acceptance criteria, tests, decisions, and unresolved items. Relationship, representation/delegation, authorization input, restriction/revocation, state, permission, provider, API/event/job, evidence, privacy/safeguarding/records/claims, offline, acceptance, and test artifacts cross-reference those identifiers.

Deterministic validation checks identifier uniqueness and cross-register existence. It does not judge substantive correctness independently.

## 41. Five Mandatory Readiness Questions

### Question 1

**Can engineering build the capability without making unauthorized product decisions?**

**Answer:** `NO`

The documentary contract is substantially stronger, but predecessor authority, owning-domain concurrence, emergency policy, numeric quality targets, implementation architecture, and express implementation authorization remain absent.

### Question 2

**Can quality assurance determine objectively whether the capability works?**

**Answer:** `PARTIALLY_SATISFIED`

Acceptance criteria and design-test rows are traceable, but no implementation, executable fixtures, approved environment, or executed QA evidence exists.

### Question 3

**Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?**

**Answer:** `PARTIALLY_SATISFIED`

The package provides source, requirement, decision, and section traceability and passes deterministic integrity checks, but Component A sources remain state-qualified and compliant fresh independent review has not started.

### Question 4

**Can EquineSync safely operate, support, monitor, recover, and maintain the capability?**

**Answer:** `NO`

No implementation, approved environment, service target, runbook, monitoring, recovery proof, support readiness, or operational authorization exists.

### Question 5

**Can the Founder determine whether the capability is ready for first-user enrollment?**

**Answer:** `NO`

The documentary candidate is complete for compliant fresh review, but independent review, adoption, ratification, implementation, release, operational validation, and enrollment authorization remain pending.

## 42. Review, Approval, Authorization, and Disposition

Formal review: `NOT_STARTED`. Compliant runtime provisioned under this directive: `FALSE`. Independent review: `PENDING`. Founder approval of this V0.2 successor: `NOT_REQUESTED`. Adoption: `FALSE`. Ratification: `FALSE`. Constitutional lock: `FALSE`. Implementation: `FALSE`. Migration: `FALSE`. Release: `FALSE`. Enrollment: `FALSE`.

Exact disposition: `ITEM_03_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`.

## 43. Maintenance, Supersession, and Decommissioning

This V0.2 candidate must be frozen with its manifest and checksums before compliant fresh review. Any post-freeze change requires a new package version, change record, affected-review notice, checksum regeneration, and rerun deterministic validation. A later successor must name this version, preserve V0.1 and V0.2 lineage, reconcile every unresolved item, and repeat the exact five questions.

Decommissioning, retention disposition, implementation, or operational use requires separate authority.
