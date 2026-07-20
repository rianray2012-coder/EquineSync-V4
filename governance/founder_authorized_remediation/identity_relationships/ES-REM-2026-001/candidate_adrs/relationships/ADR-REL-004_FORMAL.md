# ADR-REL-004: Evidence, Claim-Specific Verification, Disputes, Restrictions, and As-of Reconstruction

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-003`, `REL-FD-007`, `REL-FD-010`, `REL-FD-011`  
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

Separate RelationshipClaim, EvidenceReference, VerificationAssessment, Restriction, and DisputeReference into distinct records.

Verification is claim-specific and purpose-specific. A verification assessment must identify:
- the precise claim evaluated;
- evidence considered;
- reviewer or approved deterministic process;
- confidence or outcome;
- permitted purpose;
- limitations;
- effective and expiration dates;
- revalidation conditions;
- competing evidence or unresolved uncertainty.

Do not use a universal boolean `verified` as the authoritative model.

A dispute creates a new dispute state and Claims-domain reference. It does not overwrite the challenged relationship, automatically validate the challenger, or erase prior evidence.

Temporary restrictions are separate from final adjudication. They must be minimum necessary, attributable, reasoned, effective-dated, reviewable, and expire or be renewed under policy.

As-of reconstruction must be able to answer:
- what relationship claim and state was known at a requested effective time;
- what EquineSync had recorded at a requested transaction time;
- which evidence, verification, restrictions, and disputes were active;
- what facts were provided to Authorization for a consequential decision.

## 3. Normative Technical Rules

- Evidence content is stored or referenced under the owning record/privacy controls, not copied freely into relationship records.
- Evidence hash, source, uploader, issuer where known, classification, and retention category are preserved.
- Verification outcomes include at least VERIFIED_FOR_PURPOSE, INSUFFICIENT, CONFLICTING, EXPIRED, and NOT_REVIEWED.
- Protected mutations fail closed or enter quarantine if required evidence/audit persistence fails.
- Corrections supersede prior assessments; they do not rewrite them.

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

### Single verified flag

Rejected because it hides claim, purpose, evidence, expiry, and limitation.

### Dispute overwrites active relationship

Rejected because a challenge is not a final decision and historical truth must remain reconstructable.

### Evidence embedded directly in broad relationship payloads

Rejected because it increases privacy leakage and retention inconsistency.

## 10. Validation Obligations

- Identity evidence cannot verify ownership or guardianship claims.
- Conflicting evidence preserves both claims and visible dispute status.
- Temporary restriction expires or is reviewed under policy.
- As-of reconstruction for corrected dates and late-recorded evidence.
- Failed audit/evidence persistence prevents protected state mutation.
- Privacy tests for confidential evidence and dispute details.

## 11. Open Implementation Parameters

- Verification confidence vocabulary by relationship type.
- Evidence storage provider and encryption implementation.
- Review-service assignment and escalation times.
- Retention schedule by evidence class.

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

`ADR-REL-004_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Canonical relationship lifecycle uses neutral factual states and never an unqualified authoritative `VERIFIED` state.
- Verification is a separate `VerificationAssessment` projection scoped to an exact claim, evidence set, purpose, reviewer or approved process, effective interval, limitations, and revalidation conditions.
- Any displayed verification label is non-authoritative, purpose-qualified, time-bounded, and cannot become a universal trust badge or permission input without Authorization evaluation.
- Dispute, restriction, and verification history remains independently reconstructable.
