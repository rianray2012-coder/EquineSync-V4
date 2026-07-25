# Facility, Tenant, and Organizational Structure PIA V1.1.0

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## Control statements

- Portfolio position: `02` of exactly ten.
- PIA Master Standard: `ES-PIA-MASTER-STANDARD-V1.1`.
- As-designed baseline: this package.
- As-built baseline: not established.
- As-verified baseline: not established.

## 1. Document Control and Status

Identifier `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`; candidate version `1.1.0-candidate`; owner: Founder pending assignment; lifecycle: `FOUNDER_REVIEW`; disposition `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`. This is an as-designed candidate. It is not an as-built or as-verified baseline. No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.

## 2. Executive Summary

This PIA defines the candidate structural boundary among Tenant, Facility, Organization, Barn, and Facility Area. Tenant is the strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context; associations never create authority. FAC-FD-001 through FAC-FD-018 are incorporated as Founder-approved design doctrine; ten later-gate decisions remain open.

## 3. Purpose, Outcomes, and Success Measures

Outcomes are unambiguous topology, explicit active context, tenant isolation, preserved lineage, non-cascading transitions, and testable contracts. Success requires zero unresolved P0/P1 documentary defects, all identifiers resolved, a passing fresh segregated review, and a separate Founder design-approval decision. The ten later-gate decisions and separate implementation authorization remain required at their recorded gates.

## 4. Authoritative Sources and Inheritance

`SOURCE_REGISTER.md` records 34 exact sources, including the verified Founder incorporation directive. Facility, Barn, and Business canons provide primary domain truth. Identity, Relationship, Authorization, Permission, Privacy, Audit, Retention, Communications, Claims, Search, Operations, Resilience, Security, Integration and Adapter controls are inherited without weakening. Adoption records control lifecycle where a source body retains pre-adoption wording.

## 5. Scope, Boundaries, and Ownership

Owns structural definitions and identifiers; topology; lifecycle; typed Tenant/Facility/Organization associations; active context selection; duplicate quarantine; non-cascading transition rules; and structural API/event/job contracts. Does not own person identity, relationship truth, authorization, consent, horse ownership/custody, clinical authority, payments, record stewardship, communications delivery, search policy, platform operations or release. MIAP is the active cross-cutting implementation-governance profile, not an eleventh PIA and not Facility-domain truth.

## 6. Definitions and Controlled Vocabulary

Tenant: strict application isolation/governance context. Facility: durable physical place. Organization: durable entity identity. Barn: named operational context associated to a Facility/Area. Business: Organization-domain operating identity or classification; not a Tenant, physical Facility, Barn, relationship, or authority. Facility Area: nested physical/topological element. Association: sourced, typed, effective-dated relationship that is never authority. Active Context: explicitly selected and revalidated Tenant/Facility/Organization tuple.

## 7. Actors, Roles, Relationships, and Authorities

Actors include Founder/approval authority, tenant steward, facility steward, organization identity steward, relationship actor, authorization service, privacy/stewardship reviewers, support actor, evidence custodian and service identity. Labels such as owner, admin, operator or manager are claims/roles only; an action requires current authorization.

## 8. Capability Map and Release Classification

DESIGN: definitions, topology, lifecycles, workflows and boundaries. IMPLEMENTATION: persistence, APIs, context service, migration, support, suspension, offline and integrations. ENROLLMENT: adaptive onboarding, context UX, public projection and closure notices. This package advances only design drafting/review and grants none of the later milestones.

## 9. User and Operational Workflows

Fifteen end-to-end workflows appear in `WORKFLOW_REGISTER.md`, including adaptive first-user path selection, individual-owner/horse-first onboarding, structured facility/organization onboarding, creation, context selection, area change, organization association, operator change, duplicate merge, suspension, closure, public projection, import, correction and support investigation.

## 10. Business Rules and Decision Logic

Default deny; explicit context; associations are non-authorizing; topology changes are versioned and audited; closed identities are not reused; transfers and merges do not cascade; ambiguous imports quarantine; public data is a separate projection; disputed claims preserve uncertainty; FAC-FD-001 through FAC-FD-018 are controlling design doctrine; later-gate recommendations remain unapproved.

## 11. Data Entities, Relationships, and Provenance

Sixteen candidate entities are defined in `DATA_DICTIONARY.md`, including the non-authorizing ephemeral OnboardingPlan. Every material assertion includes stable identity, Tenant classification, source, time, actor/service, version and correction lineage. External identifiers are aliases or claims, never standalone authority.

## 12. Record Ownership, Stewardship, Correction, and Retention

Facility domain stewards physical identity/topology. Relationship domain stewards associations/membership. Authorization stewards action decisions. Corrections append change sets. Retention is field/purpose/hold-specific; numeric schedules remain `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION` under FAC-FD-022.

## 13. State and Transition Models

Candidate Tenant, Facility, Organization, Facility Area, and OnboardingPlan transitions are in `STATE_TRANSITION_MATRIX.csv`. No silent reactivation, destructive close, or state inference is permitted. Suspension must invalidate UI, API, jobs, search, exports, webhooks and integrations.

## 14. Authorization and Permission Matrix

`PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv` defines 19 candidate actions, including bounded onboarding initialization and later-context association. Every evaluation is action-, field-, tenant-, target-, facility-, organization-, purpose-, relationship-, and time-aware. Role, payment, agreement, facility assignment or organization association alone is insufficient.

## 15. User Interface and Experience Requirements

Persistent context header; explicit context switch; confirmation for consequential actions; before/after preview; effective times; uncertainty/quarantine labels; accessible errors; generic denial; no inaccessible-entity enumeration; public/private field preview; suspension and degraded-state banners.

## 16. API, Event, Job, and Integration Contracts

`API_EVENT_JOB_CONTRACTS.md` defines ten API, four event, and three job candidates, including bounded onboarding-plan, horse-first, and later-association interfaces. They require explicit context, idempotency, version checks, audit, non-enumerating failures, partition-safe retry and dead-letter quarantine. They are design interfaces, not implementation authorization.

## 17. Notifications and Communications

Material suspension, closure, association change, publication and support access should create governed notice intents. Delivery is not consent, authority or proof of receipt. Templates, recipients, failures, retries and escalation remain Communications-owned.

## 18. Files, Media, and Document Handling

Facility evidence files must be malware-scanned, tenant/context bound, classified, access-controlled, content-addressed where appropriate, retained under stewardship rules and excluded from public projection unless separately approved. No direct object locator may bypass authorization.

## 19. Search, Reporting, and Analytics

Permission filtering precedes retrieval, counts, autocomplete and ranking. Exact layouts, sensitive areas, occupants and precise coordinates remain private. Aggregates require re-identification review. Public search consumes only `PublicFacilityProjection`. Analytics cannot create cross-tenant discovery.

## 20. Offline, Device, and Synchronization Behavior

Candidate rule: offline may read a minimum, expiring authorized cache and capture context-neutral observations. It may not create/move/merge/transfer/close/decommission/reassign canonical topology. Every queued observation is untrusted until online context and authority revalidation.

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Tenant isolation is necessary but insufficient: enforce record, field, purpose and relationship scope. Private by default. Protect location/sensitive areas and minors. Rate-limit enumeration. Audit denied/material acts. Agreement/consent do not replace authorization. Support is ticketed and time-limited.

## 22. AI and Automation Controls

No AI/custom agent is activated. Automation may propose duplicate candidates or reconciliations only if separately authorized; it may not approve, merge, transfer, close, verify or authorize. Human accountable actors, confidence, inputs and evidence must remain visible.

## 23. Failure Modes, Recovery, Correction, and Reconciliation

Fail closed on missing/stale context, cycles, version conflicts, unknown partition, expired cache or ambiguous identity. Quarantine rather than default. Retry idempotently. Append corrections. Recovery must reconcile membership, permission, topology and publication before treating restored state as current.

## 24. Observability, Administration, Support, and Incident Operations

Candidate metrics: denied-by-context attempts, stale-context failures, suspended-surface probes, change-set reconciliation, quarantine age, public-projection drift, support access duration and dead letters. Support access uses ticket/reason/approval/expiry and immutable audit. Thresholds require authorization.

## 25. Nonfunctional and Quality Attribute Requirements

Isolation, integrity, availability, accessibility, usability, latency, scale, recovery and audit completeness require measurable budgets before implementation authorization. This design sets qualitative gates and does not invent numbers. Degraded behavior must be explicit and cannot imply stronger offline reliability.

## 26. Environment, Configuration, Feature Flags, and Secrets Boundaries

No environment may disable Tenant isolation, field authorization, audit, privacy or quarantine. Secrets remain external to documents. Test identities and datasets cannot cross environments. Configuration changes are versioned/audited and cannot create implementation or release authority.

## 27. Migration, Seed Data, and Data Reconciliation

No migration is authorized. Candidate future plan: inventory every record; resolve explicit Tenant/Facility/Organization identities; quarantine ambiguity; reconcile totals/hashes; dual-read only under a controlled work package; remove default-primary fallbacks only after verified cutover and rollback evidence.

## 28. Engineering Work Packages and Implementation Sequence

`ENGINEERING_WORK_PACKAGE_REGISTER.csv` contains candidate work packages only. The critical sequence is decision closure, fresh review, baseline approval, implementation authorization, model/context foundation, migration rehearsal, surface enforcement, UX/operations, evidence and release gates.

## 29. Acceptance Criteria

`ACCEPTANCE_CRITERIA.csv` maps every FAC-REQ to an objective documentary or future implementation proof. Draft-package acceptance is limited to completeness, traceability, review and validation; it is not proof that software behaves as designed.

## 30. Test and Validation Matrix

`TEST_MATRIX.csv` maps all requirements to positive, negative, cross-tenant, stale-context, lifecycle, recovery or document validation. Tests are specifications until separately executed against authorized implementation. This package ran documentary validators only.

## 31. Golden-Path Reproduction Scenarios

`GOLDEN_PATHS.md` includes eleven paths: adaptive path selection, individual-owner/horse-first onboarding, structured facility/organization onboarding, multi-facility context, multi-organization operation, area change, operator transition, duplicate reconciliation, suspension/reinstatement, closure, and public projection. Each preserves domain ownership and no-cascade rules.

## 32. Adversarial, Negative, and Abuse Scenarios

`ADVERSARIAL_SCENARIOS.md` contains twenty-two cases, including ID substitution, stale context, association-as-authority, partial suspension, offline replay, hierarchy cycles, duplicate poisoning, mass assignment, enumeration, support abuse, transfer cascade, public-location leakage, forced fictional topology, silent default assignment, account/entity conflation, and onboarding-derived authority.

## 33. Evidence Requirements, Coverage, and Manifest

`EVIDENCE_MANIFEST.json` links source, design, first-pass review, revision, second-pass review and validation evidence. Package hashes prove artifact integrity, not truth, approval, implementation or operation.

## 34. Deployment, Rollout, Rollback, and Release Controls

No deployment/rollout is authorized. A future authorized plan must define environments, flags that cannot weaken controls, migrations, rollback, reconciliation, observability, incident stop conditions, evidence and approval. Release authority remains Platform Operations/Founder controlled.

## 35. Enrollment and Onboarding Readiness

Not ready. Onboarding is adaptive: an individual-owner/horse-first path uses only the minimum technical Tenant isolation context and creates no Facility, Organization, Barn, or Business; a structured path creates only truthful selected entities and explicit associations. Neither path creates relationship or authority. Enrollment needs the four enrollment-gate Founder decisions, the six implementation-gate decisions, a passing fresh review, approved design, authorized/conformant implementation, evidence, support, and release gates.

## 36. Dependencies and Critical Path

`DEPENDENCY_REGISTER.csv` records canonical source, Founder decision, Authorization, Relationship, Privacy, Audit, Stewardship, Search, Platform Operations, implementation, migration, review and evidence dependencies. A passing fresh segregated review precedes Founder design approval; ten later-gate decisions remain required at their recorded implementation or enrollment gates.

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine. FAC-FD-019 through FAC-FD-028 remain open at later gates. Two residual P2 matters remain visible: retention decision and as-built legacy gap. There are no approved deviations. Assumption: the ten-item portfolio gate is controlling; it was validated before this package began.

## 38. Implementation Drift and As-Built Reconciliation

`AS_BUILT_RECONCILIATION.md` finds partial barn-scoping and account membership foundations but important `default`/`primary` fallbacks, Barn/Facility/Tenant conflation and no demonstrated complete Organization topology. This is legacy nonconformance evidence, not a reason to weaken design.

## 39. Change-Control History

`CHANGE_CONTROL_LOG.md` preserves source assembly, first draft, first review, challenge passes, revision, second review and final validation. Future material change requires impact analysis and a new controlled version; identifiers are not reused.

## 40. Requirement Traceability Matrix

`REQUIREMENT_REGISTER.csv` links every requirement to sources/decisions, performer, failure behavior, release class, acceptance criterion and test. Machine validation checks identifier uniqueness and reference coverage.

## 41. Five Mandatory Readiness Questions

1) Complete enough for a Founder design-approval decision after valid fresh review? Yes. Complete enough to build? No—six implementation-gate decisions and implementation authorization remain. 2) Correctly built? No implementation was evaluated. 3) Objectively verified? Documentary package only; software unverified. 4) Operationally safe? Not established. 5) Ready for first user? No.

## 42. Review, Approval, Authorization, and Disposition

One controlled drafting pass, individual first-pass review of every Phase 2/7 document, six isolated challenge passes, revision, individual second-pass review and machine validation were completed. Procedural segregation is documented; no ES-RA/custom agent identity is claimed. Fresh segregated review remains before the design-approval decision; ten later-gate Founder decisions remain open but do not block that review. Disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`.

## 43. Maintenance, Supersession, and Decommissioning

The PIA owner must monitor source changes and design drift. A material definition, ownership, permission, lifecycle or architecture change requires a major revision. Approved successors explicitly supersede this version. Candidate/retired artifacts remain in evidence; no package may silently disappear.

## Review incorporation record

The revised candidate explicitly resolves first-pass P1 findings by separating Barn from Tenant/Facility, declaring every association non-authorizing, applying suspension to all surfaces, and prohibiting transfer/merge cascade across people, horses, permissions, agreements, billing, private records and evidence. It resolves P2/P3 drafting defects by bounding offline writes, defining the public projection, preserving source-lifecycle precedence, separating verification from authority, adding stable contract IDs, and clarifying adaptive first-user onboarding. Ten later-gate Founder decisions and the legacy implementation gap remain visible.

## Founder doctrine incorporation addendum

FAC-FD-001 through FAC-FD-018 are controlling design doctrine dated 2026-07-21. Their approved answers are reproduced in `FOUNDER_DECISION_REGISTER.md` and traced in `FOUNDER_DECISION_INCORPORATION_REGISTER.csv`. FAC-FD-017 is controlled by `FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md`. These decisions do not approve this PIA as a whole and do not authorize implementation.
