# ADR-REL-007: Migration, Deduplication, Quarantine, and Legacy Lineage

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-001`, `REL-FD-003`, `REL-FD-004`, `REL-FD-007`, `REL-FD-011`, `REL-FD-012`, `REL-FD-013`  
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

Adopt a staged, additive relationship migration with immutable lineage and quarantine by default for ambiguous authority-bearing records.

Migration stages:
1. inventory legacy sources and fields;
2. classify each source as explicit relationship evidence, inferred signal, role label, free text, or unknown;
3. map candidates to approved relationship type versions;
4. create migration candidates in a staging area;
5. run identity, party, subject, scope, duplicate, temporal, and conflict checks;
6. automatically activate only low-risk records that meet an approved deterministic rule;
7. quarantine ambiguous ownership, guardianship, fiduciary, delegation, facility-control, protected-participant, and disputed records;
8. obtain review or user confirmation as required;
9. reconcile counts and exceptions;
10. cut over through a separately approved plan.

Every migrated record must preserve:
- source system and record ID;
- source field/value snapshot or integrity reference;
- importer and run ID;
- transformation rule and version;
- confidence and classification;
- duplicate or conflict references;
- activation decision;
- reviewer where applicable;
- prior and successor identifiers.

Existing roles, invoices, payment history, horse-profile creators, emergency contacts, shared accounts, or possession fields must not be silently converted into verified authority.

## 3. Normative Technical Rules

- No destructive migration in the first relationship migration wave.
- Legacy sources remain read-only or archived until reconciliation and rollback criteria are met.
- Migration does not silently merge canonical identities or relationships.
- Quarantined records do not produce permissions.
- Counts, checksums, exception registers, and sample-based human review are required.
- Rollback disables new operational use while preserving imported lineage and evidence; it does not delete failed migration evidence.

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

### Direct in-place conversion

Rejected because it destroys lineage and makes rollback and exception handling unsafe.

### Convert every role or foreign key into active relationship

Rejected because legacy structures may be inferred, stale, ambiguous, or semantically overloaded.

### Discard ambiguous records

Rejected because historical and operational context may be important and requires controlled resolution.

## 10. Validation Obligations

- Legacy payer and horse creator do not become verified owners.
- Shared account is identified and quarantined rather than assigned to one person.
- Duplicate and conflicting relationship candidates remain separate.
- Dry-run and repeat-run determinism.
- Count and checksum reconciliation.
- Rollback and forward-correction rehearsal.
- Historical as-of reconstruction after migration.

## 11. Open Implementation Parameters

- Exact legacy sources and data volumes.
- Deterministic auto-activation rules by relationship type.
- Cutover strategy and dual-read period.
- Archive and decommission timeline.

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

`ADR-REL-007_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Migration cannot create an unqualified verified relationship; any verification result is claim-, evidence-, purpose-, and time-scoped.
- Public-signup and imported relationship claims remain provisional until current identity, source authority, agreement, safeguarding, evidence, and Authorization checks complete.
- No migration may collapse organization, tenant, facility, location, program, Care Circle, emergency-contact, or exceptional-access semantics.
- Predecessor records, rejected candidates, corrections, aliases, and supersession chains remain immutable and reconstructable.
