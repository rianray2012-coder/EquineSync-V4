# Relationship, Authorization, and Permission PIA

**PIA ID:** `ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION`  
**Version:** `0.1`  
**Status:** `PIA_INITIAL_DRAFT_COMPLETE_REVIEW_BLOCKED`  
**Classification:** `FOUNDATIONAL`  
**MIAP relationship:** `SUBORDINATE_DESIGN_DOCUMENT`  
**Component A:** `RELATIONSHIP`  
**Component B:** `AUTHORIZATION`  
**Component C:** `PERMISSION`  
**Implementation Authority:** `FALSE`  
**Production Authority:** `FALSE`  
**First-User Enrollment Authority:** `FALSE`

This initial draft is preserved as the review object for a later qualified fresh review. It does not ratify the current Component A successor or its candidate ADRs. It uses locked canons and the underlying Founder-approved Relationship design as authority; successor remediation is state-qualified reference material only.

## 1. Document Control and Status

The Founder is the sole approval authority. The PIA program custodian owns this draft artifact; product, engineering, operational, privacy, security, safeguarding, and evidence owners remain unassigned pending qualified review. This V0.1 supersedes nothing. It is not adopted, locked, implemented, released, or enrollment-authorized.

Disposition: `PIA_INITIAL_DRAFT_COMPLETE_REVIEW_BLOCKED`.

## 2. Executive Summary

Item 03 establishes a single coherent authority chain across three distinct components. Component A records relationship and delegation truth. Component B assembles typed, versioned, purpose-bound inputs and produces attributable authorization decisions. Component C defines and enforces the final permission projection. Identity, context, role labels, payment, possession, provider status, and cached facts never manufacture authority.

The design is deny-by-default, time-aware, revocable, dispute-aware, purpose-limited, tenant-scoped, privacy-minimizing, explainable, and reconstructable. Missing, stale, disputed, revoked, expired, unsupported, or version-incompatible facts fail closed.

## 3. Purpose, Outcomes, and Success Measures

Purpose: give every protected EquineSync workflow one traceable contract for who may request, approve, perform, view, correct, delegate, revoke, or dispute an action, without collapsing identity, role, relationship, authorization, and permission.

Success requires: no inferred authority; full version lineage for consequential decisions; revocation and restriction propagation; protected-participant narrowing; tenant isolation; human-readable denial reasons; bounded offline behavior; and objective acceptance/test coverage before any implementation request.

## 4. Authoritative Sources and Inheritance

Controlling inputs are recorded in the batch source packet and `ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_TRACEABILITY_SOURCE_REGISTER.csv`. They include Master PIA Standard V1.1; locked Relationship V2.0 and Permission V1.1 canons; adopted Agreement, Consent, and Authorization V2.1; and applicable Identity, Privacy, Safeguarding, Claims, Audit, Records, Facility, and Financial canons.

The underlying Relationship PIA design remains Founder approved. The current Component A successor, candidate ADRs, counterparty contracts, and permission/audit candidates remain proposed and pending fresh review. They may identify risks and candidate controls but cannot be represented as ratified authority.

## 5. Scope, Boundaries, and Ownership

Included: canonical relationship claims; capacities; representation bases; delegations; source-authority chains; verification assessments; restrictions; disputes; authorization requests and decisions; permission projections; revocation watermarks; explanations; corrections; and evidence.

Excluded: identity authentication truth; Facility/Tenant/Organization topology; horse truth; care, scheduling, financial, communication, or provider workflow ownership; jurisdiction-specific legal conclusions; implementation architecture; schema; migrations; deployment; and enrollment.

Item 03 owns the authority contract. Each source PIA continues to own its domain facts, and each consuming PIA continues to own its workflow.

## 6. Definitions and Controlled Vocabulary

- **Relationship:** versioned evidence linking canonical parties or a party and subject under a defined type, capacity, scope, time, source, and status.
- **Representation basis:** the authority source under which one actor purports to act for another person or organization.
- **Delegation:** bounded, time-limited grant that cannot exceed current source authority and requires acceptance when applicable.
- **Authorization:** evaluation of current facts and policy for a requested action; it returns allow, deny, step-up, or bounded projection.
- **Permission:** enforceable action/resource/field/purpose/time projection resulting from current authorization, never a role label.
- **Restriction:** explicit narrowing or denial that overrides inferred allow unless a separately governed exception applies.
- **Authority watermark:** version marker used to invalidate stale sessions, caches, offline proposals, and integration requests.

Prohibited synonyms: account equals actor; role equals permission; relationship equals authority; verification equals universal trust; payment equals consent; custody equals ownership; invitation equals access; context equals authorization.

## 7. Actors, Roles, Relationships, and Authorities

Actors include individuals, guardians, owners, lessees, riders, trainers, staff, grooms, managers, Facility and Organization representatives, providers, support actors, administrators, auditors, system actors, and delegated actors. Every action distinguishes authenticated, acting, represented, approving, and executing principals as applicable.

Role is descriptive input. Relationship is canonical source fact. Representation and delegation identify bounded authority bases. Authorization evaluates the full request. Permission enforcement applies the result. No layer may silently perform another layer's job.

## 8. Capability Map and Release Classification

Required internal-design capabilities are relationship lifecycle, delegation, authorization decision, permission projection, restriction/revocation, evidence, and correction. Protected-participant, provider, support, financial, export, emergency, and cross-tenant actions are high-risk capabilities requiring explicit source authority and heightened evidence. Autonomous authority creation, silent privilege inheritance, global role grants, and stale offline enforcement are prohibited.

All capability classifications are design statements only. Release applicability is `DEFERRED_TO_IMPLEMENTATION_ATLAS` after Founder-approved design and separate authorization.

## 9. User and Operational Workflows

Core workflows are: assert and verify a relationship; accept, narrow, reject, renew, or revoke a delegation; request authorization; require step-up; return minimum necessary projection; enforce permission; explain denial; apply restriction; dispute and correct source facts; expire or supersede authority; invalidate stale material; and reconstruct a prior decision.

Each workflow must name trigger, prerequisites, principals, source facts, normal path, exceptions, notices, evidence, correction, closure, and offline treatment. Provider connection and support access require separately governed workflows and never create canonical relationship truth.

## 10. Business Rules and Decision Logic

1. Deny by default.
2. Verify active Tenant and applicable context without treating context as authority.
3. Require current identity, relationship, representation, delegation, restriction, agreement, source-authority, and policy versions as applicable.
4. A delegation cannot exceed, outlive, or survive invalidation of source authority.
5. Explicit denial, restriction, dispute, revocation, expiry, or protective narrowing overrides inferred allow.
6. Apply action, object, field, purpose, time, state, relationship, sensitivity, and protection predicates.
7. Return only the minimum permissible projection.
8. Preserve reason codes and exact evaluated versions.

## 11. Data Entities, Relationships, and Provenance

Material records include RelationshipClaim, RelationshipTypeVersion, PartyCapacity, RepresentationBasis, VerificationAssessment, DelegationGrant, SourceAuthorityReference, AuthorizationRequest, AuthorizationDecision, PermissionProjection, Restriction, DisputeReference, RevocationWatermark, DecisionExplanation, and Correction/Supersession Link.

Every record carries stable ID, version, tenant, source owner, provenance, effective/recorded time, actor attribution, status, scope, restriction, privacy classification, correlation ID, and supersession data as applicable. Derived decisions identify all material input versions.

## 12. Record Ownership, Stewardship, Correction, and Retention

Component A owns relationship and delegation records; Component B owns authorization request/decision evidence; Component C owns permission-policy references and enforcement outcomes. Agreements, identity, claims, facility, horse, finance, and workflow PIAs retain their own truth.

Correction creates an attributable successor and preserves prior versions. Ending access does not erase valid history. Retention and export follow Records, Privacy, Claims, Agreement, and legal-hold authority; no period is invented here.

## 13. State and Transition Models

RelationshipClaim: `ASSERTED -> PROVISIONAL -> ACTIVE`, with `DISPUTED`, `SUSPENDED`, `ENDED`, and `SUPERSEDED` transitions supported by evidence. VerificationAssessment is purpose-scoped and expires. DelegationGrant: `PENDING_ACCEPTANCE -> ACTIVE -> EXPIRED/REVOKED/INELIGIBLE/SUPERSEDED`; it may not silently reactivate. AuthorizationDecision is immutable and time-bound; a new evaluation creates a new decision.

Automatic transitions are limited to explicit expiry or fail-closed invalidation under a controlling rule. Automatic relationship activation, delegation renewal, dispute resolution, or authority expansion is prohibited.

## 14. Authorization and Permission Matrix

The matrix must distinguish who may initiate, approve, execute, view, correct, revoke, and dispute for each action family. It must identify source authority, scope, expiry, required assurance, step-up, separation of duties, protective restrictions, and emergency policy.

Final permission evaluation occurs server-side or in an equivalently trusted enforcement boundary. User-interface visibility is never proof of authority. Administrative or support access is purpose-bound, time-limited, attributable, reviewable, and never invisible impersonation.

## 15. User Interface and Experience Requirements

Users must see the active actor/capacity, represented party, Tenant/context, action scope, expiry, restrictions, and confirmation consequence before consequential action. Denials must provide safe, useful reason categories without leaking protected facts. Delegation, revocation, dispute, correction, and support access require accessible review surfaces.

The interface must never imply that a role, relationship badge, payment, invitation, provider connection, or successful login grants broader access than the current evaluated permission.

## 16. API, Event, Job, and Integration Contracts

Authorization inputs and outputs are typed, versioned, purpose-bound, integrity-protected, and tenant-scoped. Requests include actor chain, subject, resource, action, field set, purpose, source versions, policy versions, context, correlation, and freshness. Responses include outcome, bounded projection, reasons, step-up requirements, evaluated versions, watermark, generation, and expiry.

Revocation, expiry, restriction, dispute, supersession, and source invalidation publish attributable events. Jobs and integrations re-evaluate authority and may not promote external claims into canonical truth.

## 17. Notifications and Communications

Required notices may include invitation, delegation proposal/acceptance, authority change, restriction, revocation, dispute, support access, emergency use, correction, and failed high-risk action. Recipient, channel, delivery evidence, acknowledgment need, urgency, escalation, quiet-hours exception, and privacy projection come from the Communication canon and owning workflow.

Delivery does not prove receipt, consent, relationship, or authority.

## 18. Files, Media, and Document Handling

Agreement renderings, authority evidence, identity proofs, court or guardian documents, and provider artifacts are evidence objects, not self-executing authority. Exact versions, hashes, presentation context, access projection, retention basis, malware controls, and supersession links must be preserved. File possession or signature-provider status never creates capacity or permission.

## 19. Search, Reporting, and Analytics

Search and reporting consume permission-filtered projections and must prevent cross-tenant or restricted-record enumeration. Every authority report identifies definition, source, evaluated time, watermark, policy version, completeness limits, and correction status. Aggregates must not expose protected participants or sensitive relationships.

Analytics and reporting never become a competing source of relationship or permission truth.

## 20. Offline, Device, and Synchronization

EquineSync is online-first with limited field recovery. Offline work may queue a proposed action with actor, device, context, source versions, policy/watermark, timestamp, reason, and idempotency key. It may not create or expand authority locally. Synchronization re-authenticates and reauthorizes; stale, revoked, disputed, expired, wrong-tenant, duplicate, or incompatible proposals fail closed.

Users must see saved, queued, syncing, blocked, conflict, failed, and reconciled states. Ordering, retries, deduplication, clock uncertainty, revocation-watermark changes, evidence preservation, and safe correction are required because poor signal plus invisible state would be a trust failure.

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Controls include least privilege, tenant isolation, minimum disclosure, step-up, short-lived projections, secret exclusion from evidence, anti-enumeration, mass-export restrictions, session invalidation, separation of duties, support-access visibility, anomaly review, and reason-coded denial.

Guardian, minor, protected-participant, care, financial, dispute, and location data receive heightened treatment. Protective restriction narrows access and grants no delegation-derived authority absent a separately approved independent basis. Consent, authorization, acknowledgment, and agreement remain distinct.

## 22. AI and Automation Controls

AI may summarize source evidence, flag conflicts, propose explanations, or draft a request for human confirmation under the AI canon. It may not create identity, relationship, representation, delegation, consent, permission, restriction, clinical, financial, legal, or safeguarding truth; approve high-risk action; infer authority; or bypass denial.

Automation uses a named system actor, narrow purpose, explicit scope, attributable evidence, current watermark, human escalation, and reversible failure handling.

## 23. Failure Modes, Recovery, Correction, and Reconciliation

Required failures include missing/stale/version-incompatible facts, source outage, cache lag, watermark mismatch, cross-tenant request, disputed relationship, revoked delegation, expired agreement, denied projection, clock uncertainty, duplicate submission, partial event delivery, and evidence-store failure. The safe default is deny or preserve a non-authoritative proposal for controlled review.

Recovery never broadens access. Correction preserves prior decisions and explains why later evaluation differs. Reconciliation is attributable and may not erase the original evidence.

## 24. Observability, Administration, Support, and Incident Operations

Required design signals include authorization latency, denial categories, step-up rate, stale/version failures, watermark propagation, cross-tenant denials, support-access sessions, emergency use, evidence failures, retry queues, and reconciliation backlog. Thresholds, dashboards, alerts, runbooks, ownership, and retention are `DEFERRED_TO_IMPLEMENTATION_ATLAS` and require approval before operation.

Support access is ticketed, approved where required, purpose-bound, time-limited, visible, attributable, revocable, and reviewable.

## 25. Nonfunctional and Quality Attribute Requirements

The future implementation must be deterministic for identical current inputs, fail closed, tenant-isolated, explainable, auditable, revocation-responsive, privacy-minimizing, accessible, localization-ready, resilient to poor connectivity, and testable under concurrency and replay. Numeric service levels are `TBD_FOUNDER_DECISION` or `DEFERRED_TO_IMPLEMENTATION_ATLAS`; no unsupported target is invented.

## 26. Environment, Configuration, Feature Flags, and Secrets

Permission policy, projection rules, risk thresholds, step-up requirements, and emergency controls are versioned governance/configuration records with controlled promotion, rollback, and evidence. Feature flags cannot bypass authorization or activate unapproved authority bases. Secrets stay in approved secret stores and never enter logs, decisions, prompts, exports, or client bundles.

## 27. Migration, Seed Data, and Reconciliation

No migration is authorized. A future plan must inventory legacy roles, memberships, relationship claims, permissions, tokens, support grants, provider links, and tenant context; map only with adequate evidence; quarantine ambiguity; preserve identifiers and provenance; support dry run, restart, rollback, and reconciliation; and prevent migration from manufacturing authority.

## 28. Engineering Work Packages and Implementation Sequence

`DEFERRED_TO_IMPLEMENTATION_ATLAS`. The design-safe sequence is: canonical schemas/contracts; state models; authorization oracle; permission enforcement; revocation propagation; evidence; offline proposal handling; admin/support controls; notices; observability; migration tooling; adversarial testing; staged rollout. This sequence is planning only and grants no build authority.

## 29. Acceptance Criteria

Minimum criteria include: relationship does not itself grant permission; role label without source authority denies; delegation cannot exceed or outlive its source; protective restriction immediately narrows projections; stale watermark invalidates cached/offline requests; cross-tenant requests deny without enumeration; every consequential decision is reconstructable; provider or support connection grants no canonical authority; and correction preserves history.

Detailed acceptance IDs remain `TBD_SOURCE_VERIFICATION` pending review of the integrated register set.

## 30. Test and Validation Matrix

Required design tests cover happy path, denial, expiry, revocation, dispute, restriction, wrong tenant, stale cache, replay, duplicate, clock uncertainty, protected participant, financial scope, provider adapter, support access, emergency basis, offline queue, correction, export, and evidence reconstruction. Executable fixtures and results are absent because implementation is unauthorized.

## 31. Golden-Path Reproduction Scenarios

Golden paths include: owner delegates a bounded care task; guardian authorizes a permitted minor-participation action; facility manager receives scoped operational access; provider receives time-limited horse-specific access; and support actor receives approved case access. Each path proves source authority, acceptance where required, current versions, bounded projection, notice, revocation, and evidence.

## 32. Adversarial, Negative, and Abuse Scenarios

Scenarios include privilege via role label, forged representation, stale relationship, delegation chain overflow, source authority revoked mid-session, tenant-ID substitution, identifier enumeration, cached allow after restriction, provider self-activation, support impersonation, payment-created access, guardian ambiguity, AI-inferred authority, replay, mass export, notification leak, and offline duplicate/conflict.

Every scenario must fail safely and preserve attributable evidence without leaking secrets or protected facts.

## 33. Evidence Requirements, Coverage, and Manifest

Consequential evidence includes principal chain, tenant/session, requested action and subject, exact identity/relationship/representation/delegation/agreement/restriction/policy versions, authority watermark, projection, outcome, reasons, time, correlation, step-up, notice, and correction links. Evidence manifests record files, hashes, source, version, owner, retention basis, and validation state.

No mechanical manifest or log is substantive review proof.

## 34. Deployment, Rollout, Rollback, and Release Controls

No deployment or release is authorized. Future rollout requires Founder-approved PIA, implementation atlas, security/privacy/safeguarding review, objective tests, migration rehearsal, tenant-isolation proof, revocation proof, evidence proof, rollback criteria, support readiness, and explicit release and enrollment decisions.

Rollback must restore a safe deny posture without erasing decision history.

## 35. Enrollment and Onboarding Readiness

Not ready. Item 03 must support adaptive onboarding without forcing unnecessary Facility or Organization creation and without letting invitation, onboarding order, email domain, payment, or context create authority. Required initial relationships and authority bases must be minimal, explicit, reviewable, revocable, and explainable.

## 36. Dependencies and Critical Path

Critical predecessors are Item 01 identity truth, locked Relationship/Permission/Agreement/Claims/Privacy/Safeguarding/Audit/Records canons, and state-qualified Component A evidence. Item 02 supplies context but not authority. Every Item 04-10 protected workflow consumes Item 03.

Provider-network ownership remains `TBD_FOUNDER_DECISION` under `ES-PIA-GFD-003`. Qualified fresh review remains blocked under `ES-PIA-GFD-007`.

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

Open items are recorded in `ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_OPEN_ISSUES_REGISTER.csv`. The draft assumes no current successor or candidate ADR is ratified. No deviation from the canonical 43-section template is asserted. Principal risks are inferred authority, stale privilege, cross-tenant leakage, protected-participant exposure, provider-created authority, invisible support access, offline conflict, and evidence gaps.

## 38. Implementation Drift and As-Built Reconciliation

No as-built scope is accepted. A later authorized implementation must map every requirement to code, schema, policy, configuration, test, and operational evidence; record deviations; and return product or governance changes for approval. Existing application behavior cannot resolve ambiguity or amend this draft.

## 39. Change-Control History

V0.1 establishes the integrated A/B/C initial review object from the current source packet. It does not edit or supersede the frozen Relationship predecessor, the current Component A successor, candidate ADRs, or locked canons. Every later revision must preserve this V0.1 and link findings to exact changes.

## 40. Requirement Traceability Matrix

The initial section-level matrix is `ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_TRACEABILITY_MATRIX.csv`. Detailed requirement, workflow, entity, state, permission, acceptance, test, and evidence registers remain required before a strengthened candidate can be classified ready for Founder design review.

## 41. Five Mandatory Readiness Questions

### Question 1

**Can engineering build the capability without making unauthorized product decisions?**  
**Answer:** `NO`  
The authority model is bounded, but integrated detailed registers, owning-domain concurrence, numeric quality targets, provider ownership, and approved implementation architecture are absent.

### Question 2

**Can quality assurance determine objectively whether the capability works?**  
**Answer:** `PARTIALLY_SATISFIED`  
Observable acceptance themes and adversarial cases are defined, but detailed traceable test rows, fixtures, implementation, environments, and executed evidence are absent.

### Question 3

**Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?**  
**Answer:** `PARTIALLY_SATISFIED`  
The source packet and section matrix identify controlling authorities, but Component A successor material is state-qualified and no qualified fresh review has validated this integrated draft.

### Question 4

**Can EquineSync safely operate, support, monitor, recover, and maintain the capability?**  
**Answer:** `NO`  
No implementation, approved environment, operational controls, service targets, runbooks, monitoring, recovery proof, or support readiness exists.

### Question 5

**Can the Founder determine whether the capability is ready for first-user enrollment?**  
**Answer:** `NO`  
The draft is unreviewed; material registers, Founder decisions, implementation, objective validation, release, operations, and enrollment authority remain absent.

## 42. Review, Approval, Authorization, and Disposition

Fresh review: `NOT_STARTED_PERMISSION_GATE_FAILED`. Founder approval: `NOT_REQUESTED`. Adoption: `FALSE`. Lock: `FALSE`. Implementation: `FALSE`. Release: `FALSE`. Enrollment: `FALSE`.

Exact disposition: `PIA_INITIAL_DRAFT_COMPLETE_REVIEW_BLOCKED`.

## 43. Maintenance, Supersession, and Decommissioning

This V0.1 is immutable review evidence once frozen. A V0.2 may follow only after a fresh review and finding register. Supersession must name the prior version, preserve hashes and lineage, reconcile open issues, and repeat the five-question answers. Decommissioning requires a separately authorized retention and evidence plan.
