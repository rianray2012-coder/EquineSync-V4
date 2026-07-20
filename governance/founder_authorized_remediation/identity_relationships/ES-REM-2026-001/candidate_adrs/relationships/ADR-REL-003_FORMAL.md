# ADR-REL-003: Delegation Grants, Source-Authority Dependency Graph, Cycle Prevention, and Revocation Watermark

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-005`, `REL-FD-006`, `REL-FD-014`, `REL-FD-016`  
**Founder-approved recommendation:** `TRUE`  
**Formal wording ratified:** `FALSE`  
**Implementation authorized:** `FALSE`  
**Repository baseline:** `acb518ea5a160820e64681ff95a16b010fe1156c`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## 1. Context

The Relationships and Delegated Authority PIA V1.1.0 is Founder-approved as an
as-designed baseline. The Founder has approved the architecture recommendation
underlying this ADR. This document formalizes that recommendation into a
controlled architecture decision record.

The formal text remains subject to final ratification after source
reconciliation and cross-domain contract review. No implementation is
authorized by this ADR draft.

## 2. Decision

Adopt DelegationGrant as a first-class Relationship subtype backed by an explicit source-authority dependency graph.

Every grant must snapshot:
- delegator and delegate;
- exact source-authority references and versions;
- action registry version and permitted actions;
- prohibited actions;
- subject, horse, organization, tenant, facility, location, program, record, task, and purpose scopes as applicable;
- quantitative or financial limits;
- effective start and end;
- acceptance version and assurance;
- policy version;
- revocation state and reason.

Delegation depth defaults to one. Redelegation is denied unless the governing relationship type and Authorization policy explicitly permit it. Every proposed graph change must perform cycle detection and authority-containment checks.

Create a monotonically changing authority version or revocation watermark for each authority-bearing principal/context. Authorization must compare the request's referenced authority state with the current authoritative state before accepting a consequential action.

When a source relationship or authority expires, is revoked, suspended, narrowed, disputed, or superseded, dependent grants must become ineligible immediately or enter an explicitly defined protective restricted state. No dependent delegation may remain active merely because a stale session or offline cache still contains it.

## 3. Normative Technical Rules

- Default maximum delegation chain depth: 1.
- No silent renewal for high-risk grants.
- Material change creates a new immutable grant version and requires fresh delegate acceptance.
- Revocation propagation must cover sessions, caches, offline proposals, integrations, exports, scheduled jobs, and downstream grants.
- Authorization remains the final decision service; Relationship owns the delegation facts and dependency graph.
- Failure to validate every required source fails closed.

## 4. Architectural Boundaries

- Identity owns canonical actor, account, principal, assurance, and representation truth.
- Relationships owns relationship and delegation facts, lifecycle, provenance, and dependencies.
- Authorization owns the final allow, deny, projection, step-up, and revocation-enforcement decision.
- Agreement and Consent owns documentary authorization, signer capacity, consent, withdrawal, and execution.
- Claims owns contested-claim procedure and final operational dispute disposition.
- Protected Participant and Safeguarding may narrow or prohibit relationship effects.
- Horse, Facility, Business, and Operations domains own their respective domain truth.
- Audit and Evidence owns attributable reconstruction and protected evidence requirements.

No adjacent domain may silently rewrite relationship truth through a side effect.

## 5. Data and State Consequences

- Stable identifiers and immutable version references are required.
- State transitions must be server enforced, attributable, and auditable.
- Material corrections supersede prior records rather than erasing them.
- Historical and current-state representations must remain reconcilable.
- Unknown, stale, conflicting, or unsupported authority states fail closed.

## 6. API, Event, and Integration Consequences

Implementations derived from this ADR must define:

- idempotent commands;
- expected-version or equivalent concurrency controls;
- structured domain events;
- audit correlation identifiers;
- retry and duplicate behavior;
- error and quarantine dispositions;
- privacy-projected read contracts;
- revocation and invalidation propagation where applicable.

External systems receive purpose-limited projections and may not create or
alter canonical relationship authority.

## 7. Security, Privacy, and Safeguarding Consequences

- Tenant and purpose boundaries are mandatory.
- Relationship existence may itself be confidential.
- High-risk changes require stronger assurance and explicit authority.
- Protected-participant controls may impose stricter rules than ordinary relationship policy.
- Evidence and dispute material must not be exposed through broad relationship payloads.
- Support access remains bounded, attributable, and non-authoritative.

## 8. Offline and Failure Behavior

- Offline state cannot independently create authoritative relationship or delegation effects.
- Protected mutations must fail closed or enter a defined quarantine path if required evidence,
  authorization, audit, or persistence controls fail.
- Recovery must preserve the first failure and all subsequent corrective evidence.
- Partial success must not leave unsupported authority active.

## 9. Alternatives Considered

### Delegation as a role assignment

Rejected because roles are too broad and cannot encode source authority, exact action, subject, purpose, time, and dependency.

### JWT or session claims as the delegation record

Rejected because tokens are temporary representations and cannot serve as canonical revocable relationship truth.

### Recursive delegation without fixed limits

Rejected because it creates opaque authority chains and escalation risk.

## 10. Validation Obligations

- Delegator cannot grant absent or broader authority.
- Wrong horse, facility, purpose, task, action, time, or limit is denied.
- Cycle and unauthorized redelegation rejection.
- Source-authority expiry/revocation invalidates dependent grants.
- Stale authority watermark rejection.
- Material-change fresh-acceptance tests.
- Offline and integration revocation propagation tests.
- GP-05 prerequisite contract tests without implementing GP-05.

## 11. Open Implementation Parameters

- Concrete watermark storage and invalidation transport.
- Allowed low-risk delegation duration defaults.
- Any relationship types permitted to redelegate and their maximum depth.
- Latency target for revocation propagation.

## 12. Source and Traceability Obligations

Before final ratification, this ADR must trace to:

- the locked Master Relationship Model V2.0;
- the approved Relationships and Delegated Authority PIA V1.1.0;
- the applicable Founder decisions;
- the Identity PIA and formal Identity ADRs;
- the Authorization PIA and formal Authorization ADRs;
- relevant Agreement, Claims, Safeguarding, Audit, Privacy, Horse, Facility,
  Communication, and Record Stewardship controls.

## 13. Ratification Gate

Recommended formal ADR disposition after source and contract review:

`ADR-REL-003_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- When any required source authority expires, is revoked, suspended, narrowed, disputed, or superseded, every dependent grant becomes operationally ineligible immediately. A protective restricted state may preserve review and history only and grants zero delegation-derived authority unless an independently approved authority basis is separately established.
- Delegate acceptance is mandatory before activation whenever the grant creates duties, access, safety obligations, financial limits, or protected-participant interaction.
- Every delegation expires automatically by default. Every renewal revalidates current source authority, restrictions, assurance, and protected-participant constraints.
- No high-risk renewal is silent. Any material duty, risk, action, subject, facility, financial, or protective-exposure change requires a new immutable grant or replacement and fresh acceptance.
