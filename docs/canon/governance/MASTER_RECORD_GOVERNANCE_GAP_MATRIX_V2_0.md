# MASTER RECORD GOVERNANCE GAP MATRIX

**Document Version:** 2.0  
**Document Status:** Proposed Foundational Governance Operating Framework  
**Product:** EquineSync  
**Applies To:** Canon authority, record identity, ownership, stewardship, authorship, provenance, classification, correction, retention, legal hold, privacy erasure, historical access, transfer, export, external processing, backup, restoration, disposal, evidentiary integrity, governance maturity, and canon evolution  
**Primary Canon Dependency:** `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md`  
**Companion Canon Dependencies:** `MASTER_RELATIONSHIP_MODEL.md`, `MASTER_PERMISSION_MODEL.md`, `MASTER_HORSE_LIFECYCLE.md`, `MASTER_BARN_LIFECYCLE.md`, `MASTER_BUSINESS_LIFECYCLE.md`, `MASTER_FACILITY_DOMAIN_MODEL.md`, `MASTER_AI_OPERATING_SYSTEM.md`, `MASTER_ANALYTICS_FRAMEWORK.md`, RF29 Calendar canon, and RF30 AI boundary canon  
**Supersedes:** `MASTER_RECORD_GOVERNANCE_GAP_MATRIX.md` for future controlled review  
**Implementation Authorized:** No  
**Production Mutation Authorized:** No  
**Retention or Disposal Execution Authorized:** No  

---

## 1. Executive Purpose

Version 2.0 expands the original governance gap matrix into a durable governance operating framework.

It does not merely identify what is missing. It defines:

- who owns each governance question;
- which canon controls;
- how conflicting authority is resolved;
- how records progress through governed states;
- which stewardship powers exist;
- what a canonical record registry must contain;
- how repository maturity is measured;
- how risks are accepted and tracked;
- how canon changes are proposed, approved, versioned, and implemented.

This document remains non-implementing and non-binding until founder approval and controlled canon adoption.

---

## 2. Governance Principles

### Principle 1: Records never own relationships

A record may evidence, describe, or affect a relationship. It does not independently create relationship truth unless the controlling relationship canon and approved workflow expressly permit that effect.

### Principle 2: Relationships never determine authorship

A person may own, lease, ride, train, board, treat, or pay for a horse without being the author of every related record.

### Principle 3: Stewardship never grants access

Stewardship authority permits governed maintenance. It does not independently grant broad visibility, export, transfer, deletion, or disclosure.

### Principle 4: Retention never guarantees visibility

A retained record may remain inaccessible in ordinary workflows, available only in redacted form, export-only, or restricted to legal, support, security, or evidentiary use.

### Principle 5: Deletion never rewrites history

Where integrity matters, deletion, minimization, anonymization, or restriction must preserve the minimum lawful lineage required to explain what occurred.

### Principle 6: Evidence outranks convenience

A role label, payer field, file URL, creator reference, current possession, or most recent row must not override stronger provenance, verified authority, or controlled canon.

### Principle 7: External vendors never become canonical authority

Vendors may store, sign, settle, synchronize, transmit, or process records. They do not decide canonical ownership, relationship authority, retention, transfer rights, access, or final truth.

### Principle 8: Canonical truth is never inferred from legacy implementation alone

Existing schema, route, UI, import, or provider behavior is evidence of repository reality, not automatic governance authority.

### Principle 9: Human review outranks automation in contested or high-risk decisions

Automation may classify, recommend, reconcile, or flag. It must not silently adjudicate ownership, guardianship, legal authority, medical truth, privilege, dispute merit, or irreversible disposal.

### Principle 10: Every destructive operation must be controlled

Destructive action requires scope, authority, dry-run evidence, hold checks, dependency checks, audit, failure handling, and an explicitly approved finality boundary.

---

## 3. Governance Authority Hierarchy

When two sources conflict, resolve authority in the following order:

1. `MASTER_PRODUCT_VISION.md`
2. `MASTER_ECOSYSTEM_MODEL.md`
3. `MASTER_RELATIONSHIP_MODEL.md`
4. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md`
5. domain and lifecycle canons
6. `MASTER_PERMISSION_MODEL.md` for authorization enforcement and field projection
7. RF29 Calendar canon for Calendar ownership
8. RF30 and `MASTER_AI_OPERATING_SYSTEM.md` for AI restrictions
9. `MASTER_ANALYTICS_FRAMEWORK.md` for analytical use
10. approved RF plans and lock artifacts
11. implementation contracts
12. repository schema and code
13. UI behavior
14. external vendor state

A lower layer may implement a higher layer. It may not contradict it.

A material conflict between higher-authority canons must stop dependent implementation.

---

## 4. Canon Dependency Graph

```text
MASTER_PRODUCT_VISION
        |
        v
MASTER_ECOSYSTEM_MODEL
        |
        v
MASTER_RELATIONSHIP_MODEL
        |
        v
MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL
        |
        +------------------------------+
        |                              |
        v                              v
DOMAIN & LIFECYCLE CANONS      MASTER_PERMISSION_MODEL
        |                              |
        +---------------+--------------+
                        |
                        v
          RF29 / RF30 LOCKED BOUNDARIES
                        |
                        v
        RF31 / RF32 / PROPOSED RF33-RF36
                        |
                        v
        SCHEMAS / ROUTES / WORKERS / UI
                        |
                        v
              MIGRATION / ACTIVATION
                        |
                        v
                 PRODUCTION STATE
```

### 4.1 Dependency rule

No downstream artifact may weaken, bypass, or silently reinterpret an upstream authority.

### 4.2 Relationship and record boundary

The Relationship Model governs who or what is connected and with what authority.

The Record Stewardship Model governs which domain owns the record truth, who may steward it, how it is preserved, and how it is corrected, retained, transferred, or disposed.

### 4.3 Permission boundary

The Permission Model remains authoritative for access enforcement.

Classification, stewardship, authorship, ownership, retention, transferability, or historical continuity do not independently grant field access.

---

## 5. Governance Authority Matrix

| Governance Area | Canon Owner | Operational Steward | Approval Required | Founder Required | Primary Future Owner |
| --- | --- | --- | --- | --- | --- |
| Product purpose | Master Product Vision | Founder / Product | Canon change | Yes | Founder governance |
| Ecosystem entities and boundaries | Master Ecosystem Model | Architecture | Canon change | Yes | Founder governance |
| Relationship truth | Master Relationship Model | Relationship domain | Canon change or registry extension | Yes for material expansion | RF31 and later domain RFs |
| Record truth and stewardship | Record Stewardship Model | Record governance | Canon change or registry extension | Yes | Canon review and domain RFs |
| Authorization and redaction | Master Permission Model | Identity / Permission domain | Policy or implementation approval | Yes for material boundary changes | RF34 / domain RFs |
| Horse identity and continuity | Horse Lifecycle canon | Passport domain | Domain and RF approval | Yes for material changes | RF31 |
| Facility identity and location | Facility canon | Facility domain | Domain and RF approval | Yes for material changes | Facility RFs |
| Calendar ownership | RF29 locked canon | Calendar domain | Separate authorization | Yes for canon change | RF36 for adapters |
| AI behavior | RF30 and AI canon | AI domain | Separate authorization | Yes | Future AI RF |
| Analytics use | Analytics Framework | Analytics domain | Policy and RF approval | Yes for sensitive inference | Analytics RF |
| Agreements | Record and Relationship canon | Agreement domain | RF and provider readiness | Yes for legal-effect changes | RF33 |
| Identity and communications | Permission, Relationship, and Record canon | Identity / Communications | RF and provider readiness | Yes for major provider or minor policy changes | RF34 |
| Payments and settlement | Business, Relationship, and Record canon | Billing / Payments | RF and financial controls | Yes | RF32 / RF35 |
| Legal hold and discovery | Record canon plus legal policy | Designated legal custodian | Case-specific approval | Yes for policy | Future legal-governance RF |
| Retention and disposal | Record canon plus approved schedule | Data governance | Schedule and execution approval | Yes for policy | Future retention RF |
| Backup and restoration | Record canon plus infrastructure policy | Infrastructure | Environment approval | Yes for material policy | Infrastructure gate |
| Security and breach | Permission and Record canon | Security | Incident and policy approval | Yes for material policy | Security RF |
| Vendor processing | Record canon and ATLAS5 governance | Service owner | Readiness and activation approval | Yes | RF33-RF36 / ATLAS5 |

---

## 6. Canonical Record State Machine

```text
DRAFT
  |
  v
RECORDED
  |
  +------> QUARANTINED
  |             |
  |             v
  |         REJECTED / RELEASED
  |
  v
UNVERIFIED
  |
  v
VERIFIED
  |
  v
ACTIVE / FINAL
  |
  +------> DISPUTED
  |             |
  |             v
  |         RESOLVED
  |
  +------> CORRECTED
  |             |
  |             v
  |         SUPERSEDED
  |
  v
ARCHIVED
  |
  +------> HELD
  |             |
  |             v
  |         HOLD_RELEASED
  |
  v
DISPOSAL_ELIGIBLE
  |
  v
DISPOSAL_PENDING
  |
  +------> CANCELLED / BLOCKED
  |
  v
DISPOSED
```

### 6.1 State entry and exit requirements

| State | Entry Requirement | Exit Requirement | Required Evidence | Destructive Effect Allowed |
| --- | --- | --- | --- | --- |
| `DRAFT` | Authorized author begins content | Submit, abandon, or expire | Author, timestamp, intended type | Limited draft deletion only |
| `RECORDED` | Persisted with stable identity | Verification, quarantine, or void | Record ID, author, provenance | No |
| `UNVERIFIED` | Source accepted without full verification | Verify, reject, quarantine, supersede | Source and confidence | No |
| `VERIFIED` | Approved evidence or verifier confirms | Activate, dispute, correct, supersede | Verifier, basis, date | No |
| `ACTIVE` | Operationally effective | End, correct, dispute, archive | Effective time and authority | No |
| `FINAL` | Completion criteria satisfied | Correct, supersede, archive, hold | Finalizer and version | No |
| `DISPUTED` | Competing claim or challenge recorded | Resolve, reject, or preserve | Claims, evidence, temporary controls | No |
| `QUARANTINED` | Trust, integrity, identity, or conflict threshold triggered | Release, reject, or retain | Quarantine reason and reviewer | No |
| `CORRECTED` | Approved amendment exists | Supersede or archive | Original, correction, reason | No deletion of original by default |
| `SUPERSEDED` | Successor governs prospectively | Archive or hold | Successor link and effective boundary | No |
| `ARCHIVED` | Removed from ordinary active workflow | Restore to governed active state, hold, or disposal review | Archive authority and access mode | No |
| `HELD` | Approved preservation basis exists | Formal release | Hold scope, authority, date | No disposal |
| `DISPOSAL_ELIGIBLE` | Retention, dependency, and hold checks pass | Pending disposal or reclassification | Schedule and checks | No |
| `DISPOSAL_PENDING` | Approved destructive batch prepared | Dispose, cancel, or block | Dry run, approval, manifest | Not until final execution |
| `DISPOSED` | Final approved disposal completed | No ordinary reversal | Manifest, result, exceptions | Yes |

### 6.2 State-machine constraints

- `HELD` overrides ordinary disposal eligibility.
- `DISPUTED` does not automatically erase active operational effect.
- `CORRECTED` does not erase original authorship.
- `ARCHIVED` does not imply disposed.
- `DISPOSED` must not be used as a synonym for hidden, revoked, suspended, or inaccessible.
- Restored backups must reconcile against current state before records regain operational effect.

---

## 7. Stewardship Decision Matrix

### 7.1 Stewardship powers

| Power | Description |
| --- | --- |
| `CREATE` | Create a new record under an approved type and authority. |
| `AMEND` | Add a correction, addendum, or supplemental information. |
| `SUPERSEDE` | Replace operational effect prospectively while preserving lineage. |
| `VERIFY` | Confirm evidence quality or authority. |
| `CLASSIFY` | Apply sensitivity, transfer, retention, or legal status. |
| `ARCHIVE` | Remove from ordinary active workflows. |
| `TRANSFER` | Include in an approved transfer or disclosure package. |
| `EXPORT` | Produce a governed copy for an approved recipient and purpose. |
| `PLACE_HOLD` | Suspend ordinary disposal under approved authority. |
| `RELEASE_HOLD` | Release preservation after authorized review. |
| `MINIMIZE` | Remove or reduce unnecessary fields while preserving lawful integrity. |
| `DISPOSE` | Authorize or execute final approved destruction. |
| `OVERRIDE` | Apply narrowly approved exceptional action with heightened evidence. |

### 7.2 Default authority by record class

| Record Class | Create | Amend | Verify | Classify | Archive | Transfer | Export | Place Hold | Release Hold | Dispose | Override |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Horse identity | Passport steward | Passport steward | Approved verifier | Record governance | Passport steward | RF31 authority | Approved export role | Legal custodian | Legal custodian | Restricted | Founder-approved admin only |
| Ownership / transfer | Authorized claimant or admin | Non-destructive only | Approved ownership verifier | Record governance | Transfer steward | RF31 authority | Restricted | Legal custodian | Legal custodian | Highly restricted | No silent override |
| Daily care | Authorized care actor | Care steward | Supervisor where required | Domain policy | Care steward | Governed transfer class | Authorized projection | Legal custodian | Legal custodian | Schedule only | Emergency correction only |
| Medical | Provider or authorized care actor | Provider/addendum | Provider or approved reviewer | Medical governance | Medical steward | Consent/authority dependent | Restricted | Legal custodian | Legal custodian | Highly restricted | Break-glass access, not truth override |
| Guardian / minor | Authorized guardian workflow | Restricted | Approved verifier | Minor governance | Identity steward | Restricted | Restricted | Legal custodian | Legal custodian | Highly restricted | Court or legal authority only |
| Agreement | Agreement workflow | Addendum/supersession | Signature and authority verification | Legal/record governance | Agreement steward | Limited | Restricted | Legal custodian | Legal custodian | Schedule and legal review | No content rewrite |
| Financial | Billing workflow | Adjustment event | Reconciliation authority | Financial governance | Billing steward | Limited | Authorized report | Legal custodian | Legal custodian | Schedule and legal review | No settlement override without evidence |
| Calendar | Calendar domain | Calendar domain | As defined by RF29 | Calendar policy | Calendar steward | Projection only | Authorized projection | Legal custodian | Legal custodian | Schedule | Provider copy never overrides canon |
| Audit / security | System or security service | Addendum only | Security reviewer | Security governance | Security steward | Restricted | Restricted | Legal/security custodian | Legal/security custodian | Highly restricted | No silent mutation |
| Privileged legal | Authorized legal custodian | Restricted | Legal custodian | Legal custodian | Legal custodian | Restricted | Legal custodian | Legal custodian | Legal custodian | Legal review only | No ordinary admin override |
| Derived AI / analytics | Approved process | Regenerate or annotate | Human review where required | AI/analytics governance | Domain steward | Derived-only | Restricted | Legal custodian if in scope | Legal custodian | Source-linked disposal | Cannot override source truth |

### 7.3 Separation-of-duty rule

The same actor should not independently:

- create and verify a high-risk authority record;
- place and release a legal hold;
- approve and execute irreversible disposal;
- create and resolve a financial dispute;
- create and adjudicate an ownership claim;
- generate and canonize an AI-derived record.

Exceptions require explicit policy, reason, audit, and post-review.

---

## 8. Canonical Record Registry Specification

Every governed record type must contain or reference the following registry fields.

```text
record_type_id
record_type_name
record_type_version
canonical_domain
canonical_owner
operational_steward
allowed_authors
allowed_subject_types
allowed_relationship_contexts
required_authority_source
required_provenance
verification_policy
lifecycle_policy
correction_policy
supersession_policy
duplicate_policy
conflict_policy
sensitivity_class
field_classification_profile
attachment_classification_profile
retention_class
retention_schedule_reference
legal_hold_eligible
privacy_erasure_policy
transfer_class
historical_access_class
export_policy
external_processing_policy
backup_policy
restoration_policy
disposal_policy
required_audit_events
required_evidence_level
implementation_maturity
future_rf_owner
effective_version
approved_by
approved_at
supersedes_registry_version
```

### 8.1 Registry approval rules

A new material record type requires:

1. canonical domain assignment;
2. record owner and operational steward;
3. subject and author rules;
4. provenance and verification rules;
5. sensitivity and field-level classification;
6. correction and supersession behavior;
7. retention governance;
8. transfer and historical-access classification;
9. disposal and hold behavior;
10. permission and audit requirements;
11. founder approval where the type affects ownership, minors, legal rights, medical care, money movement, security, AI authority, or irreversible destruction.

### 8.2 Registry extension classes

| Change Class | Example | Required Review |
| --- | --- | --- |
| `CLARIFICATION` | Wording or non-material example | Documentation review |
| `NON_MATERIAL_EXTENSION` | New subtype within approved family | Domain and governance review |
| `MATERIAL_EXTENSION` | New authority, sensitive class, or transfer behavior | Founder approval |
| `BREAKING_CHANGE` | Changes access, retention, disposal, legal effect, or source of truth | Founder approval plus migration plan |
| `EMERGENCY_RESTRICTION` | Immediate access or processing restriction | Temporary authority plus retrospective review |

---

## 9. Repository Readiness and Maturity Model

| Level | Name | Required Condition |
| --- | --- | --- |
| `R0` | Concept Only | Idea exists without approved canon. |
| `R1` | Canon Defined | Governing semantics and boundaries are approved. |
| `R2` | Repository Planned | Models, routes, permissions, tests, and migration are designed. |
| `R3` | Schema Exists | Local schema or typed contract exists without activation claim. |
| `R4` | Service Exists | Domain services and routes exist locally. |
| `R5` | Permission Enforced | Backend authorization and field projection are tested. |
| `R6` | Audit and Failure Controls | Audit, idempotency, exceptions, recovery, and degraded paths are evidenced. |
| `R7` | Migration Ready | Inventory, mapping, quarantine, access deltas, rollback, and reconciliation are accepted. |
| `R8` | Founder Validated | Controlled evidence is founder accepted for the approved environment. |
| `R9` | Production Ready | Operational ownership, monitoring, backups, security, legal policy, and activation evidence are complete. |
| `R10` | Production Verified | Production behavior has been validated under separately authorized release governance. |

### 9.1 Maturity claim rule

A record category's maturity is the lowest level satisfied across:

- schema;
- service;
- permission;
- audit;
- migration;
- operational policy;
- vendor evidence;
- recovery;
- founder approval.

No category may claim a higher level by averaging strong and weak areas.

### 9.2 Current high-level maturity posture

| Domain | Indicative Maturity | Reason |
| --- | --- | --- |
| Relationship canon | R1-R2 | Founder-approved canon; implementation remains separate. |
| Record stewardship canon | R0-R1 | Proposed model and matrix; controlled review not complete. |
| RF29 Calendar core | R8 for accepted local synthetic scope | Locked and complete within bounded evidence; external activation remains unauthorized. |
| RF30 AI boundary | R8 for boundary controls | Locked deterministic-fake-only boundary; real AI remains unauthorized. |
| Horse transfer | R1-R2 | Canon dependencies exist; RF31 not opened. |
| Barn payment issue workflow | R1-R2 | Canon dependencies exist; RF32 not opened. |
| Agreements / e-signature | R3-R4 foundations | Repository foundations exist; canonical convergence and production governance remain incomplete. |
| Identity | R4-R6 foundations | Custom auth exists; broader identity and communication readiness remain incomplete. |
| Storage | R3-R4 foundations | Provider abstraction exists; private-object, backup, and production evidence remain incomplete. |
| External calendars | R1-R3 | Canon exists; provider adapters and activation remain unauthorized. |
| Retention / legal hold / disposal | R0-R1 | Governance proposed; implementation not authorized. |

---

## 10. Governance Risk Register

| Risk ID | Risk | Probability | Impact | Affected Canon / RF | Mitigation | Residual Risk | Owner | Acceptance Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GR-01 | Legacy fields promoted to canonical authority | High | Critical | Relationship, Record, RF31 | Provenance, verification, quarantine, additive shadow model | Medium | Record governance / RF31 | Founder required |
| GR-02 | Payment state treated as settlement truth | High | Critical | Business, Record, RF32/RF35 | Provider evidence boundary and reconciliation | Medium | Billing / Payments | Founder required |
| GR-03 | Sensitive files exposed by public URL behavior | Medium | Critical | Record, Permission, RF33 | Private-by-default object policy and scoped access | Low-Medium | Storage / Security | Founder required |
| GR-04 | Transfer package over-discloses private records | High | Critical | Relationship, Record, RF31 | Transfer classification and field-level redaction | Medium | RF31 | Founder required |
| GR-05 | Former party retains excessive live access | High | High | Permission, Record, RF31 | Purpose-bound historical access and export-only modes | Low-Medium | Permission / RF31 | Founder required |
| GR-06 | Backup restore revives deleted or revoked state | Medium | Critical | Record, Infrastructure | Restore replay and reconciliation | Medium | Infrastructure | Founder required |
| GR-07 | Legal hold absent or bypassed | Medium | Critical | Record / Legal | Hold registry, deletion blocks, release authority | Low-Medium | Legal custodian | Founder required |
| GR-08 | Automated disposal destroys required evidence | Medium | Critical | Record / Retention | Dry run, dual approval, hold and dependency checks | Low | Data governance | Founder required |
| GR-09 | AI-derived output becomes canonical truth | Medium | High | RF30, Record, AI | Derived-only status, human review, no promotion without governed authorship | Low | AI governance | Founder required |
| GR-10 | Embeddings or indexes retain deleted data | Medium | High | Record, AI, Search | Source lineage, deletion propagation, rebuild policy | Medium | AI / Search | Founder required |
| GR-11 | Guardian or minor records disclosed incorrectly | Medium | Critical | Relationship, Permission, Record | Multi-guardian restrictions and field-level projection | Low-Medium | Identity / Minor governance | Founder required |
| GR-12 | Privileged material accessible to broad admins | Medium | Critical | Record / Legal / Permission | Matter-based controls and restricted custodians | Low | Legal / Security | Founder required |
| GR-13 | Provider webhook replay creates duplicates | High | High | Record, Financial, RF35 | Signature, idempotency, canonical route ownership | Low-Medium | Payments | RF approval |
| GR-14 | Organization acquisition grants overbroad successor access | Medium | High | Business, Record | Record-by-record succession review | Medium | Business governance | Founder required |
| GR-15 | Cross-border processing violates policy | Low-Medium | High | Record / ATLAS5 | Residency registry and legal review | Medium | Infrastructure / Legal | Founder required |
| GR-16 | Audit records insufficient for evidentiary use | Medium | High | Record / Security | Canonical audit contract and chain-of-custody package | Low-Medium | Security / Platform | RF approval |
| GR-17 | Duplicate horse merge destroys identity lineage | Medium | Critical | Horse, Relationship, Record, RF31 | Human review, reversible link/merge evidence | Low | RF31 | Founder required |
| GR-18 | Soft delete confused with erasure or disposal | High | High | Record / Permission | Explicit lifecycle semantics | Low-Medium | Record governance | Founder required |
| GR-19 | Support or development logs retain sensitive content | Medium | High | Record / RF34 / Security | Redaction, environment controls, retention | Low | Communications / Security | RF approval |
| GR-20 | Canon change implemented without migration or access-delta review | Medium | Critical | All | Canon evolution workflow and implementation gate | Low | Founder governance | Founder required |

---

## 11. Canon Evolution Rules

### 11.1 Canon change lifecycle

```text
ISSUE OR GAP IDENTIFIED
        |
        v
CORRECTION LEDGER ENTRY
        |
        v
AUTHORITY AND IMPACT REVIEW
        |
        v
FOUNDER DECISION, IF REQUIRED
        |
        v
CANON REVISION
        |
        v
VERSION INCREMENT
        |
        v
DEPENDENCY UPDATE
        |
        v
IMPLEMENTATION OR MIGRATION PLAN
        |
        v
CONTROLLED EVIDENCE
        |
        v
FOUNDER ACCEPTANCE
        |
        v
LOCK OR RELEASE DECISION
```

### 11.2 Required canon-change fields

Every material change must record:

- change ID;
- source issue;
- affected canon;
- prior rule;
- proposed rule;
- rationale;
- authority;
- alternatives considered;
- affected record types;
- permission impact;
- migration impact;
- retention impact;
- legal-hold impact;
- external-service impact;
- required RF;
- required evidence;
- approval;
- effective version;
- superseded language.

### 11.3 Versioning

| Version Type | Use |
| --- | --- |
| Major | Changes authority, record identity, source of truth, permission boundary, retention precedence, transferability, or destructive behavior. |
| Minor | Adds governed categories, registries, scenarios, or non-breaking rules. |
| Patch | Corrects wording, references, formatting, or non-material ambiguity. |

### 11.4 Prospective default

Canon changes apply prospectively unless the approved decision explicitly authorizes:

- historical correction;
- migration;
- reclassification;
- access change;
- retention change;
- disposal effect.

### 11.5 No silent implementation

A canon change does not automatically authorize:

- schema changes;
- migrations;
- permission changes;
- vendor activation;
- production behavior;
- data backfill;
- retention execution;
- disposal;
- legal holds.

---

## 12. Gap Matrix Operating Instructions

The detailed gap matrix below remains the authoritative backlog of known governance issues.

Each row should eventually be updated with:

- maturity level;
- governance owner;
- evidence quality;
- accepted risk;
- decision status;
- target RF;
- closure evidence;
- final disposition.

No row may be considered closed merely because code exists.

---

## 13. Classification Rules

### 2.1 Canon coverage values

| Value | Meaning |
| --- | --- |
| `STRONG` | Existing or proposed canon gives a materially complete governing rule. |
| `PARTIAL` | Canon recognizes the subject but lacks a complete contract, registry, precedence rule, or founder decision. |
| `ABSENT` | No sufficient canonical rule has been identified. |
| `CONFLICTING` | Multiple canonical or planning sources appear capable of producing inconsistent outcomes. |

### 2.2 Repository coverage values

| Value | Meaning |
| --- | --- |
| `IMPLEMENTED_AND_EVIDENCED` | Behavior appears implemented and supported by current tests or governed evidence. |
| `PARTIAL_OR_FRAGMENTED` | Relevant fields, models, routes, or services exist, but record truth is divided or incompletely governed. |
| `FOUNDATION_ONLY` | Supporting infrastructure exists, but the governed record model is not complete. |
| `NOT_FOUND` | No reliable repository implementation has been identified. |
| `UNVERIFIED` | Behavior may exist, but the available evidence is insufficient to confirm it. |
| `OUTSIDE_REPOSITORY_EVIDENCE` | Vendor account, legal policy, or operational control cannot be proven from source alone. |

### 2.3 Finding classifications

Every gap should ultimately be assigned exactly one primary classification:

- `ALIGNED_CANON`
- `PROPOSED_CLARIFICATION`
- `REPOSITORY_IMPLEMENTATION_GAP`
- `FOUNDER_DECISION`
- `FUTURE_IMPLEMENTATION_WORK`

### 2.4 Severity

| Severity | Meaning |
| --- | --- |
| `P0` | A condition that could permit destructive loss, material unauthorized disclosure, false legal or financial authority, unsafe horse-care behavior, or an invalid production claim. |
| `P1` | A blocking governance or implementation ambiguity that must be resolved before dependent implementation or migration. |
| `P2` | A material improvement or evidence gap that should be resolved within the dependent RF or readiness gate. |
| `P3` | A lower-risk refinement, optimization, or documentation improvement. |

---

## 14. Cross-Cutting Governance Gaps

| ID | Governance Area | Canon Coverage | Repository Coverage | Gap / Conflict | Required Resolution | Primary Classification | Severity | Future Owner | Founder Decision | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-C01 | Canonical record registry | PARTIAL | NOT_FOUND | Record types may be created feature-by-feature without one controlled registry defining domain, steward, classification, retention, correction, transfer, and disposal. | Approve registry structure and initial governed record-type set. | FOUNDER_DECISION | P1 | Canon adoption / later implementation RF | Approve registry authority and change process. | Registry proposal; canon crosswalk; initial type inventory. |
| RG-C02 | Canonical record identifiers | PARTIAL | PARTIAL_OR_FRAGMENTED | IDs may be table-specific, provider-specific, mutable, or absent from exports and attachments. | Define stable identity, source aliases, version lineage, and duplicate rules. | FOUNDER_DECISION | P1 | Cross-domain foundation | Approve ID contract and version semantics. | Model inventory; source-ID map; duplicate examples. |
| RG-C03 | Record ownership versus stewardship | STRONG | PARTIAL_OR_FRAGMENTED | Creator, tenant, barn, file owner, route owner, and domain owner may be conflated. | Map each record type to canonical domain and authorized steward. | REPOSITORY_IMPLEMENTATION_GAP | P1 | Cross-domain foundation | None if canon adopted. | Repository inventory; steward matrix; route ownership. |
| RG-C04 | Authorship preservation | STRONG | PARTIAL_OR_FRAGMENTED | Editing, migration, imports, or administrative correction may overwrite or obscure original authorship. | Add immutable attribution and correction lineage. | FUTURE_IMPLEMENTATION_WORK | P1 | Domain RFs / migration | Approve administrative correction roles. | Before/after examples; audit fields; import provenance. |
| RG-C05 | Subject identity separation | STRONG | PARTIAL_OR_FRAGMENTED | Being the subject of a record may be treated as ownership, access, or stewardship. | Require explicit subject, owner, steward, author, and access dependencies. | PROPOSED_CLARIFICATION | P2 | Canon correction | Confirm authority order. | Canon traceability. |
| RG-C06 | Source-of-truth hierarchy | PARTIAL | PARTIAL_OR_FRAGMENTED | Current rows, events, imports, provider payloads, restored copies, and exports may conflict without precedence. | Define precedence by record type and reconciliation workflow. | FOUNDER_DECISION | P1 | Record registry / domain RFs | Approve precedence principles. | Conflict examples; provider mapping; restoration scenarios. |
| RG-C07 | Event time versus recorded time | PARTIAL | PARTIAL_OR_FRAGMENTED | Repository timestamps may not distinguish occurrence, awareness, recording, verification, and effective time. | Adopt time contract and migrate only under separate approval. | FUTURE_IMPLEMENTATION_WORK | P1 | Cross-domain foundation | Approve time semantics. | Schema inventory; timestamp crosswalk; scenario tests. |
| RG-C08 | Record versioning | PARTIAL | PARTIAL_OR_FRAGMENTED | Mutable updates may replace prior truth without a governed version or supersession chain. | Define version, amendment, supersession, void, and correction patterns. | FOUNDER_DECISION | P1 | Record registry / domain RFs | Approve which records require immutable version lineage. | Update-path inventory; audit comparison. |
| RG-C09 | Whole-record classification | PARTIAL | PARTIAL_OR_FRAGMENTED | Sensitivity may be inferred from route or user role rather than recorded classification. | Approve sensitivity registry and default-deny behavior. | FOUNDER_DECISION | P1 | Permission / record governance | Approve initial classes. | Field inventory; access tests. |
| RG-C10 | Field-level severability | PARTIAL | PARTIAL_OR_FRAGMENTED | Mixed-sensitivity records may be disclosed or transferred as all-or-nothing objects. | Define field-level classification, redaction, export, transfer, and erasure rules. | FOUNDER_DECISION | P1 | Permission Model / RF31 | Approve severability policy. | Projection maps; redaction tests; transfer examples. |
| RG-C11 | Attachment-level classification | PARTIAL | FOUNDATION_ONLY | Attachments may inherit broad parent access despite independent legal, medical, privacy, or copyright concerns. | Classify each attachment and require scoped access tokens. | FUTURE_IMPLEMENTATION_WORK | P1 | Storage / RF33 / medical domains | Approve inheritance versus independent classification. | Object-access review; signed URL tests; attachment inventory. |
| RG-C12 | Record lifecycle vocabulary | PARTIAL | PARTIAL_OR_FRAGMENTED | Draft, final, corrected, void, archived, quarantined, held, and disposed states may differ by feature. | Approve shared lifecycle mappings without forcing one physical enum. | FOUNDER_DECISION | P2 | Canon adoption / domain RFs | Approve semantic vocabulary. | State inventory; normalization maps. |
| RG-C13 | Correction and amendment | STRONG | PARTIAL_OR_FRAGMENTED | Direct overwrite or deletion may be possible for records requiring evidentiary lineage. | Implement domain-specific amendment and supersession controls. | FUTURE_IMPLEMENTATION_WORK | P1 | Domain RFs | Approve non-destructive record classes. | Route tests; audit evidence; corrected-record scenarios. |
| RG-C14 | Conflict-of-record resolution | PARTIAL | NOT_FOUND | Newest row or administrator choice could silently become truth. | Establish neutral conflict state, evidence comparison, decision authority, and appeal lineage. | FOUNDER_DECISION | P1 | Cross-domain governance | Approve conflict authority. | Conflict workflow; evidence package; audit tests. |
| RG-C15 | Duplicate resolution | PARTIAL | PARTIAL_OR_FRAGMENTED | Duplicate horses, invoices, agreements, people, media, and provider records may use inconsistent merge behavior. | Define candidate, quarantine, link, merge, reversal, and lineage standards. | FOUNDER_DECISION | P1 | RF31 plus domain RFs | Approve merge authority and thresholds. | Duplicate inventory; deterministic tests; reversal evidence. |
| RG-C16 | Record quarantine | PARTIAL | NOT_FOUND | Unverified imports and conflicting records may influence access, payment, medical, or transfer workflows. | Add quarantine state and prohibit authority effects until review. | FUTURE_IMPLEMENTATION_WORK | P1 | Migration / import RF | Approve quarantine thresholds. | Import scenarios; authority-denial tests. |
| RG-C17 | Provenance | STRONG | PARTIAL_OR_FRAGMENTED | Source system, source record, transformation, confidence, and importer may not be preserved uniformly. | Adopt provenance minimums across imports, vendors, migrations, and derived records. | REPOSITORY_IMPLEMENTATION_GAP | P1 | Cross-domain foundation | None beyond registry approval. | Field inventory; webhook and import samples. |
| RG-C18 | Verification status | STRONG | PARTIAL_OR_FRAGMENTED | Existing data may appear authoritative without verification state. | Add controlled verification semantics and prohibit implicit promotion. | FUTURE_IMPLEMENTATION_WORK | P1 | RF31 / imports / domain RFs | Approve verifier roles. | Verification tests; legacy classification report. |
| RG-C19 | Purpose limitation | PARTIAL | PARTIAL_OR_FRAGMENTED | Records collected for care, billing, safety, or support may be reused without explicit purpose governance. | Add purpose metadata and approved secondary-use rules. | FOUNDER_DECISION | P2 | Privacy / Analytics / AI | Approve compatible-use policy. | Data-flow maps; analytics and AI source review. |
| RG-C20 | Historical access | PARTIAL | PARTIAL_OR_FRAGMENTED | Ending a relationship may either remove too much access or preserve too much. | Define purpose, period, category, projection, and delivery mode for former parties. | FOUNDER_DECISION | P1 | RF31 / Permission Model | Approve in-app versus export-only access. | Historical-access matrix; denial tests. |
| RG-C21 | Retention schedule governance | PARTIAL | UNVERIFIED | No single controlled schedule, approval process, or versioning mechanism is established. | Approve governance process without inventing durations. | FOUNDER_DECISION | P1 | Record governance | Approve schedule owner and change authority. | Proposed schedule framework; legal-policy dependencies. |
| RG-C22 | Missing retention durations | ABSENT | UNVERIFIED | Many record categories have no approved duration. | Record gaps; prohibit automatic disposal until approved. | FOUNDER_DECISION | P1 | Record governance / legal review | Approve durations later by class and jurisdiction. | Record inventory; jurisdiction map. |
| RG-C23 | Retention versus live access | STRONG | PARTIAL_OR_FRAGMENTED | Retained records may remain visible because application access and retention are not separated. | Implement restricted archival access and export pathways. | FUTURE_IMPLEMENTATION_WORK | P1 | Permission / archive RF | Approve access modes. | Archived-record tests; access-delta evidence. |
| RG-C24 | Legal hold | PARTIAL | NOT_FOUND | No governed hold registry, scope, precedence, release, or disposal suspension is established. | Define hold workflow before any production activation. | FOUNDER_DECISION | P0 | Future legal-governance RF | Approve hold authority and workflow. | Hold scenarios; deletion-block tests; audit package. |
| RG-C25 | Privacy erasure versus retention | PARTIAL | PARTIAL_OR_FRAGMENTED | Account deletion, privacy requests, contractual retention, and legal preservation may collide. | Approve precedence, minimization, and restricted-preservation rules. | FOUNDER_DECISION | P0 | Privacy / legal governance | Approve precedence and decision authority. | Erasure scenarios; hold scenarios; field minimization plan. |
| RG-C26 | Automated disposal | PARTIAL | NOT_FOUND | No canonical dry-run, hold check, dependency check, approval, batch, rollback, or evidence standard is established. | Prohibit execution until safeguards are adopted and tested. | FUTURE_IMPLEMENTATION_WORK | P0 | Future retention implementation RF | Approve disposal authority. | Dry-run output; failure tests; audit and restore tests. |
| RG-C27 | Soft deletion semantics | PARTIAL | PARTIAL_OR_FRAGMENTED | Soft delete may be inconsistently used as archive, revocation, erasure, or destruction. | Define semantic states and route behavior by record type. | PROPOSED_CLARIFICATION | P1 | Domain RFs | Approve distinction between archive, restrict, and dispose. | Deleted-row inventory; route behavior tests. |
| RG-C28 | Export governance | PARTIAL | PARTIAL_OR_FRAGMENTED | Exports may lack manifest, redaction, scope, provenance, expiry, and chain-of-custody evidence. | Adopt governed export contract. | FUTURE_IMPLEMENTATION_WORK | P1 | RF31 / support / legal | Approve export authority and recipient verification. | Export package tests; manifest samples. |
| RG-C29 | Backup governance | PARTIAL | OUTSIDE_REPOSITORY_EVIDENCE | Backup scope, retention, encryption, residency, access, and testing are not provable from code alone. | Establish operational evidence and governed policy. | FOUNDER_DECISION | P1 | ATLAS5 / infrastructure governance | Approve backup policy owner. | Vendor evidence; restore reports; access roster. |
| RG-C30 | Restoration replay | PARTIAL | NOT_FOUND | Restores could revive deleted data, permissions, relationships, consent, or superseded records. | Require reconciliation and replay of post-backup governance changes. | FUTURE_IMPLEMENTATION_WORK | P0 | Infrastructure / data recovery RF | Approve recovery precedence. | Restore simulation; access and deletion delta. |
| RG-C31 | Cryptographic integrity | PARTIAL | FOUNDATION_ONLY | Hashing, object versions, signed manifests, and evidence packages are not consistently governed. | Define approved use by record category. | FOUNDER_DECISION | P2 | RF33 / legal / audit | Approve required classes and algorithms through implementation policy. | Artifact hash tests; manifest examples. |
| RG-C32 | Chain of custody | PARTIAL | NOT_FOUND | Legal, incident, agreement, medical, and export records may lack acquisition and transfer lineage. | Establish evidence-chain requirements. | FOUNDER_DECISION | P1 | Legal / incident / RF33 | Approve chain standard and custodians. | Evidence export scenario; audit fields. |
| RG-C33 | Discovery and subpoena workflow | PARTIAL | NOT_FOUND | Ordinary admins could be asked to fulfill high-risk requests without legal intake and least-disclosure workflow. | Create governed request intake, review, hold, production, and notice process. | FOUNDER_DECISION | P0 | Future legal-governance RF | Approve legal authority and user-notice policy. | Request scenarios; role tests; production manifest. |
| RG-C34 | Government and law-enforcement requests | PARTIAL | NOT_FOUND | Authentication, scope, notice restrictions, and production authority are undefined. | Establish separate governed workflow. | FOUNDER_DECISION | P0 | Future legal-governance RF | Approve request-handling policy. | Scenario library; escalation roster. |
| RG-C35 | Break-glass access | PARTIAL | PARTIAL_OR_FRAGMENTED | Emergency or administrator access may lack time limits, reason codes, scope, and post-review. | Approve break-glass policy and technical enforcement. | FOUNDER_DECISION | P0 | Permission / emergency RF | Approve eligible roles and record classes. | Emergency access tests; audit and review evidence. |
| RG-C36 | Data residency | PARTIAL | OUTSIDE_REPOSITORY_EVIDENCE | Storage and processor regions may not be mapped to record classes or customer obligations. | Create residency registry and escalation rule. | FOUNDER_DECISION | P1 | ATLAS5 / infrastructure | Approve residency posture. | Vendor region evidence; data-flow map. |
| RG-C37 | Cross-border processing | PARTIAL | OUTSIDE_REPOSITORY_EVIDENCE | Legal basis, safeguards, subprocessors, and government-access risk are unverified. | Add jurisdiction review before cross-border activation. | FOUNDER_DECISION | P1 | ATLAS5 / legal governance | Approve supported regions. | Vendor contracts; subprocessor list; transfer assessment. |
| RG-C38 | Organization succession | PARTIAL | NOT_FOUND | Merger, acquisition, dissolution, bankruptcy, receivership, and operator change may create overbroad successor access. | Define record-by-record succession review. | FOUNDER_DECISION | P1 | Business Lifecycle / future RF | Approve successor access principles. | Succession scenarios; access matrix. |
| RG-C39 | Privilege and work product | PARTIAL | NOT_FOUND | Legal materials may be visible to broad administrators or mixed with support records. | Create restricted matter-based handling and non-waiver controls. | FOUNDER_DECISION | P0 | Legal governance | Approve legal-record custodian roles. | Access tests; matter inventory; export restrictions. |
| RG-C40 | Security and breach records | PARTIAL | PARTIAL_OR_FRAGMENTED | Evidence, access, retention, legal review, and notification lineage may be fragmented. | Establish canonical security-incident record contract. | FUTURE_IMPLEMENTATION_WORK | P1 | Security / ATLAS5 | Approve record steward and retention governance. | Incident schema; access tests; notification evidence. |

---

## 15. Horse, Passport, Ownership, and Transfer Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-H01 | Canonical horse identity | STRONG | PARTIAL_OR_FRAGMENTED | Multiple names, registrations, imports, barn records, and duplicate profiles may compete. | Canonical ID, aliases, source evidence, duplicate quarantine, reversible merge. | RF31 | Approve merge threshold and authority. | False identity continuity or duplicate Passport. | P0 | Horse identity inventory; duplicate scenarios; merge reversal. |
| RG-H02 | Horse Passport record registry | PARTIAL | FOUNDATION_ONLY | Passport content may lack per-record classification, steward, transfer class, and retention class. | Passport-specific registry and transfer matrix. | RF31 | Approve always-canonical versus consent-transferable categories. | Over-disclosure or continuity failure. | P1 | Passport field inventory; transfer package examples. |
| RG-H03 | Ownership claims | STRONG | PARTIAL_OR_FRAGMENTED | Creator, payer, current barn, possession, or registration name may be mistaken for legal ownership. | Explicit claims, evidence, verification, disputes, and effective dates. | RF31 | Approve evidence standards. | False transfer authority. | P0 | Ownership-source map; denial tests. |
| RG-H04 | Verified ownership records | PARTIAL | NOT_FOUND | No complete verified ownership registry is established. | Versioned ownership edges plus evidentiary record package. | RF31 | Approve verification authority and launch scope. | Inability to prove authority safely. | P0 | Ownership workflow; evidence review; conflict tests. |
| RG-H05 | Co-ownership and syndicate records | PARTIAL | NOT_FOUND | Percentages, voting, disclosure, and successor rights are unresolved. | Multi-party group, allocations, voting rules, and transfer constraints. | RF31 or later | Approve support level and voting model. | Unauthorized transfer or disclosure. | P1 | Multi-owner scenarios. |
| RG-H06 | Lease records | PARTIAL | PARTIAL_OR_FRAGMENTED | Lease authority, record visibility, care authority, and termination may not be explicit. | Lease type, scope, effective dates, authority, transfer, historical access. | RF31 | Approve lease categories and disclosure. | Overbroad authority. | P1 | Lease scenarios; access tests. |
| RG-H07 | Custody and possession records | STRONG | PARTIAL_OR_FRAGMENTED | Physical custody may be conflated with ownership or record authority. | Explicit custody records, location, dates, purpose, emergency duties. | RF31 / facility domains | None beyond canon adoption. | False authority and care confusion. | P1 | Custody-to-permission tests. |
| RG-H08 | Transfer package classification | STRONG | NOT_FOUND | No complete matrix identifies horse-canonical, consent-transferable, organization-retained, private, restricted, or held records. | Record-category transfer matrix with redaction and manifest rules. | RF31 | Approve classification decisions. | Transfer over-disclosure or incomplete care history. | P0 | Matrix; export simulations; founder decisions. |
| RG-H09 | Transfer package manifest | PARTIAL | NOT_FOUND | Exports may lack IDs, versions, provenance, redactions, hashes, authority, and omissions. | Signed or governed manifest and chain-of-custody package. | RF31 | Approve integrity requirements. | Evidentiary weakness. | P1 | Transfer package evidence. |
| RG-H10 | Transfer effective-time coordination | PARTIAL | NOT_FOUND | Record access, relationship changes, notifications, future events, and payer changes may occur at inconsistent times. | Transactional or compensating workflow with recovery. | RF31 | Approve reversal and partial-completion policy. | Split authority state. | P0 | Failure and recovery scenarios. |
| RG-H11 | Former barn records | PARTIAL | PARTIAL_OR_FRAGMENTED | Former barn may retain too much current access or lose required authored history. | Period-bound read-only access or export-only model. | RF31 | Approve historical access mode. | Privacy breach or record loss. | P1 | Access matrix; former-barn scenarios. |
| RG-H12 | Private owner notes | PARTIAL | PARTIAL_OR_FRAGMENTED | Private notes may enter transfer packages or organization views. | Party-private classification and exclusion rules. | RF31 / Permission | Approve private-note treatment. | Sensitive disclosure. | P1 | Projection tests; export redaction. |
| RG-H13 | Horse death records | PARTIAL | PARTIAL_OR_FRAGMENTED | Death may end access or active workflows without clear record preservation and memorial state. | Death record, verification, active-state transitions, archive rules. | Horse Lifecycle RF | Approve who may record and verify death. | Irreversible status error or lost history. | P1 | Death and reversal scenarios. |
| RG-H14 | Missing, stolen, seized, and impounded records | PARTIAL | NOT_FOUND | Safety, disclosure, law-enforcement, and location data need special governance. | Restricted status, evidence preservation, alert controls, recovery lineage. | RF31 or later | Approve public/private visibility and verification. | Safety and legal exposure. | P1 | Scenario tests; access rules. |
| RG-H15 | Estate, trust, and fiduciary records | PARTIAL | NOT_FOUND | Fiduciary authority and record access may be asserted without document verification. | Authority evidence, effective period, limited access, succession. | RF31 | Approve verifier roles. | Unauthorized transfer or disclosure. | P0 | Estate and trust scenarios. |

---

## 16. Care, Medical, Provider, Incident, and Safety Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-M01 | Daily care records | PARTIAL | PARTIAL_OR_FRAGMENTED | Completion time, event time, actor, offline origin, exception, amendment, and horse-continuity class may be incomplete. | Canonical care-event contract and correction lineage. | Future care RF | Approve which care records follow horse. | Unsafe or inaccurate care history. | P0 | Care workflow inventory; degraded-state tests. |
| RG-M02 | Feed records | PARTIAL | PARTIAL_OR_FRAGMENTED | Current plan, historical instructions, organization operations, and horse continuity may be mixed. | Separate order, plan, execution, exception, and historical records. | Care / facility RF | Approve transferability. | Feeding error. | P0 | Plan-versus-administration scenarios. |
| RG-M03 | Medication orders | PARTIAL | PARTIAL_OR_FRAGMENTED | Provider order, owner instruction, barn plan, and administration may be conflated. | Distinct order, authorization, schedule, administration, refusal, and adverse-event records. | Medical RF | Approve author and steward roles. | Horse safety. | P0 | Medication chain tests. |
| RG-M04 | Medication administration | PARTIAL | PARTIAL_OR_FRAGMENTED | Actor, exact time, dose, route, exception, correction, and offline provenance may be incomplete. | Immutable administration event with amendment. | Medical RF | None after policy approval. | Horse safety and liability. | P0 | Positive, missed, duplicate, corrected-dose scenarios. |
| RG-M05 | Veterinary treatment records | PARTIAL | PARTIAL_OR_FRAGMENTED | Provider-authored records, uploaded documents, owner reports, and internal summaries may compete. | Source hierarchy, professional authorship, restricted notes, transfer and correction rules. | Medical / provider RF | Approve horse-canonical versus provider-retained scope. | Medical misinformation or over-disclosure. | P0 | Provider record inventory; conflict tests. |
| RG-M06 | Professional opinions | PARTIAL | PARTIAL_OR_FRAGMENTED | Opinion may be displayed as verified fact or altered by non-author stewards. | Explicit opinion classification and non-destructive addendum. | Medical / provider RF | Approve correction and dispute rules. | Misrepresentation. | P1 | Opinion-versus-fact scenarios. |
| RG-M07 | Farrier records | PARTIAL | PARTIAL_OR_FRAGMENTED | Hoof-care history and provider-private notes may not be separated. | Service record, findings, recommendations, media, invoice link, restricted notes. | Provider RF | Approve transfer class. | Continuity or privacy gap. | P1 | Farrier workflow and access tests. |
| RG-M08 | Bodywork, dental, chiropractic, and ancillary records | PARTIAL | PARTIAL_OR_FRAGMENTED | Provider-specific records may lack consistent identity, access, and retention. | Shared provider record contract with subtype registry. | Provider RF | Approve professional-note treatment. | Fragmented history. | P2 | Provider inventory. |
| RG-M09 | Incident records | PARTIAL | PARTIAL_OR_FRAGMENTED | Event time, knowledge time, witness records, media, notifications, claims, and legal hold may be disconnected. | Canonical incident package with linked evidence and restricted access. | Safety / incident RF | Approve steward and disclosure rules. | Liability and evidence failure. | P0 | Incident scenario library; chain of custody. |
| RG-M10 | Injury records | PARTIAL | PARTIAL_OR_FRAGMENTED | Injury observations, medical diagnosis, care response, and claim evidence may be merged. | Separate factual observation, professional diagnosis, response, and claim linkage. | Safety / medical RF | Approve classification. | Incorrect medical representation. | P0 | Injury scenarios and projection tests. |
| RG-M11 | Emergency authorizations | STRONG | PARTIAL_OR_FRAGMENTED | Authority limits, spending limits, expiry, revocation, and invocation evidence may be missing. | Versioned authorization and emergency-use event. | RF31 / emergency RF | Approve authority hierarchy and limits. | Unauthorized care or spend. | P0 | Emergency-use tests. |
| RG-M12 | Break-glass medical access | PARTIAL | PARTIAL_OR_FRAGMENTED | Emergency access may not be time-bound or reviewed. | Scoped grant, reason, expiry, audit, post-review. | Permission / emergency RF | Approve eligible roles. | Sensitive disclosure. | P0 | Break-glass tests. |
| RG-M13 | Safe Sport-related records | PARTIAL | NOT_FOUND | Reporting, access, evidence, guardian visibility, retaliation protection, and external reporting are undefined. | Restricted record class and governed workflow. | Future safety RF | Approve steward, escalation, and access rules. | Minor safety and legal exposure. | P0 | Scenario and access review. |
| RG-M14 | Insurance and claims records | PARTIAL | NOT_FOUND | Policies, claim evidence, communications, settlement, hold, and disclosure lack unified governance. | Canonical policy and claim record model. | Future insurance RF | Approve retention and custodian. | Financial and legal exposure. | P1 | Claim lifecycle scenarios. |
| RG-M15 | Media attached to care or incidents | PARTIAL | FOUNDATION_ONLY | Photos and video may retain broad URLs, metadata, or derivatives beyond source access. | Attachment classification, private storage, derivative deletion, chain of custody. | Storage / incident RF | Approve metadata and copyright rules. | Sensitive disclosure. | P0 | Object-access tests; derivative inventory. |

---

## 17. People, Rider, Guardian, Minor, and Communication Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-P01 | Canonical person identity | PARTIAL | PARTIAL_OR_FRAGMENTED | Multiple emails, invitations, roles, family accounts, and provider/client overlap may duplicate identities. | Canonical identity linkage, aliasing, merge review, and historical attribution. | RF34 or identity RF | Approve identity merge and verification. | Misattribution and access errors. | P0 | Identity duplicate inventory; merge scenarios. |
| RG-P02 | Account versus person record | STRONG | PARTIAL_OR_FRAGMENTED | Account deletion or suspension may be treated as person deletion. | Explicit separation and historical attribution. | RF34 | None beyond canon adoption. | Lost records or ongoing unauthorized access. | P1 | Account closure tests. |
| RG-P03 | Rider profile | PARTIAL | PARTIAL_OR_FRAGMENTED | Rider skill, safety, medical, guardian, lesson, and account data may be mixed. | Purpose-specific subrecords and projections. | Lesson / identity RF | Approve sensitive rider-profile fields. | Over-disclosure. | P1 | Field map; persona access tests. |
| RG-P04 | Guardian authority | STRONG | PARTIAL_OR_FRAGMENTED | Payer, emergency contact, household member, or inviter may be mistaken for guardian. | Verified guardian relationship and documentary restrictions. | RF31 / RF34 | Approve verification and conflict authority. | Minor access and consent failure. | P0 | Guardian scenarios; denial tests. |
| RG-P05 | Multi-guardian conflict | STRONG | NOT_FOUND | Different scopes, court orders, confidential contact, and conflicting instructions lack workflow. | Neutral conflict state and restricted access. | RF34 / future minor-safety RF | Approve temporary authority policy. | Minor safety and legal risk. | P0 | Multi-guardian scenario evidence. |
| RG-P06 | Age-of-majority transition | PARTIAL | NOT_FOUND | Minor records and guardian access may continue unchanged. | Effective transition, notices, consent refresh, historical controls. | RF34 | Approve jurisdiction handling and exceptions. | Privacy and control failure. | P1 | Transition scenarios. |
| RG-P07 | Consent records | PARTIAL | PARTIAL_OR_FRAGMENTED | Consent may be inferred from agreement signature, email delivery, or account creation. | Purpose, scope, version, grant, withdrawal, expiry, and evidence. | RF33 / RF34 | Approve consent hierarchy. | Unauthorized processing or contact. | P0 | Consent lifecycle tests. |
| RG-P08 | Communication records | PARTIAL | PARTIAL_OR_FRAGMENTED | Message, notification, template, delivery attempt, provider response, and legal notice may be conflated. | Separate canonical communication and provider-delivery records. | RF34 | Approve retention and audience. | Missing evidence or privacy breach. | P1 | Communication flow inventory. |
| RG-P09 | Direct messages | PARTIAL | PARTIAL_OR_FRAGMENTED | Privacy, moderation, minors, retention, export, and legal hold are unresolved. | Dedicated record class and participant-level access. | RF34 or later messaging RF | Approve minors and moderation policy. | High privacy and safety risk. | P0 | Messaging scenarios; access tests. |
| RG-P10 | Notifications | PARTIAL | PARTIAL_OR_FRAGMENTED | Delivery logs may be mistaken for consent, receipt, or canonical workflow state. | Notification request, attempt, provider result, acknowledgment, and retry records. | RF34 | Approve which notifications are evidentiary. | False notice claims. | P1 | Delivery and failure tests. |
| RG-P11 | Email preview and development logs | PARTIAL | UNVERIFIED | Sensitive content may be logged in development or support environments. | Redaction, environment restrictions, and retention controls. | RF34 / ATLAS5 | Approve logging policy. | Sensitive data exposure. | P0 | Log review; redaction tests. |
| RG-P12 | Identity verification records | PARTIAL | FOUNDATION_ONLY | Verification evidence, expiry, external vendor data, and restricted access are not fully governed. | Verification record class and minimum retention. | RF34 | Approve supported methods. | Identity fraud or over-retention. | P1 | Verification flow and storage map. |
| RG-P13 | Password and authentication records | PARTIAL | IMPLEMENTED_AND_EVIDENCED | Custom identity foundation exists, but security-record stewardship, retention, breach handling, and account succession need governance. | Canonical auth-event and credential lifecycle records. | RF34 | Approve MFA and replacement-provider posture. | Security risk. | P1 | Auth schema, lockout, refresh, and incident tests. |

---

## 18. Agreement, Financial, Tax, and Business Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-F01 | Agreement identity | PARTIAL | FOUNDATION_ONLY | Templates, envelopes, executed files, local records, and provider IDs may compete. | Canonical agreement ID, template version, party group, artifact lineage. | RF33 | Approve agreement domain owner. | Duplicate or misapplied agreement. | P0 | Agreement inventory; provider mapping. |
| RG-F02 | Executed agreement artifact | PARTIAL | FOUNDATION_ONLY | Signed artifact retention, immutability, private storage, hash, and replacement rules are unverified. | Private canonical artifact with integrity and access controls. | RF33 | Approve integrity and retention governance. | Evidentiary failure or disclosure. | P0 | Signed-file tests; object policy; hash evidence. |
| RG-F03 | Agreement party authority | STRONG | PARTIAL_OR_FRAGMENTED | Signer identity may be treated as authority without relationship or representative proof. | Party roles, authority source, verification, effective scope. | RF33 | Approve representative authority requirements. | Invalid agreement effect. | P0 | Signer-authority scenarios. |
| RG-F04 | Agreement supersession | PARTIAL | PARTIAL_OR_FRAGMENTED | Renewal or replacement may overwrite or obscure prior terms and effective periods. | Version chain and prospective supersession. | RF33 | Approve void, terminate, supersede semantics. | Contract-history ambiguity. | P1 | Renewal tests. |
| RG-F05 | Waivers and emergency authorizations | PARTIAL | PARTIAL_OR_FRAGMENTED | Waiver, participation, guardian consent, and emergency authority may be bundled. | Separate governed records with explicit effects. | RF33 / RF34 | Approve bundling limits. | Invalid consent or authority. | P0 | Agreement decomposition review. |
| RG-F06 | Invoice identity | PARTIAL | PARTIAL_OR_FRAGMENTED | Invoice number, database ID, provider payment ID, payer, recipient, and obligation may be conflated. | Canonical obligation and invoice identity model. | RF32 / RF35 | Approve obligation versus invoice semantics. | Financial misstatement. | P0 | Billing model inventory. |
| RG-F07 | Internal payment state | STRONG | PARTIAL_OR_FRAGMENTED | Local routes may mark invoices paid without provider-confirmed settlement. | Trust boundary and reconciliation state. | RF32 / RF35 | Approve allowed provisional states. | False settlement claim. | P0 | Route and webhook tests. |
| RG-F08 | Stripe provider evidence | PARTIAL | FOUNDATION_ONLY | Multiple webhook surfaces, naming inconsistencies, replay, and route ownership create ambiguity. | Canonical event owner, signature validation, idempotency, mapping, reconciliation. | RF35 | Approve retirement of legacy webhook. | Duplicate or false payment state. | P0 | Webhook inventory; replay tests. |
| RG-F09 | Payer responsibility | STRONG | PARTIAL_OR_FRAGMENTED | Payer may be inferred from owner, guardian, rider, account, or invoice recipient. | Effective-dated responsible-party record. | RF32 | Approve acceptance and non-account payer support. | Incorrect collection or disclosure. | P0 | Payer-change scenarios. |
| RG-F10 | Refunds, disputes, and chargebacks | PARTIAL | PARTIAL_OR_FRAGMENTED | Provider state may overwrite invoice history or erase responsibility. | Separate immutable financial events and mapped internal states. | RF35 | Approve operational effects. | Financial and audit error. | P1 | Provider lifecycle tests. |
| RG-F11 | Tax records | PARTIAL | NOT_FOUND | Filing evidence, organization scope, amendments, jurisdiction, and retention governance are undefined. | Tax-record class and restricted access. | Future finance/compliance RF | Approve custodian and retention process. | Regulatory exposure. | P1 | Tax record inventory and jurisdiction review. |
| RG-F12 | Provider settlement and marketplace records | PARTIAL | NOT_FOUND | Future split payments require payer, recipient, beneficiary, fee, settlement, reversal, and tax evidence. | Financial-rails record registry. | RF35 | Approve payment scope and platform role. | Money movement and compliance risk. | P0 | Payment architecture and legal review. |
| RG-F13 | Financial exports | PARTIAL | PARTIAL_OR_FRAGMENTED | Reports may not preserve source state, period, redaction, or adjustment lineage. | Governed export and snapshot contract. | RF32 / RF35 | Approve official versus informational reports. | Misleading financial evidence. | P1 | Export reconciliation. |
| RG-F14 | Business closure and open obligations | PARTIAL | NOT_FOUND | Closure may leave invoices, refunds, disputes, agreements, records, and access unresolved. | Controlled succession and wind-down record plan. | Business Lifecycle / later RF | Approve successor and customer access. | Data loss and financial disputes. | P1 | Closure scenario. |

---

## 19. Calendar, Facility, Inventory, and Operational Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-O01 | Canonical Calendar event | STRONG | IMPLEMENTED_AND_EVIDENCED | RF29 is locked, but persistence, external providers, and production activation remain unauthorized. | Preserve locked boundary; later adapters must use record projections. | RF36 | None unless scope changes. | Canon drift or external overwrite. | P1 | RF29 traceability; adapter tests later. |
| RG-O02 | Calendar participants | STRONG | FOUNDATION_ONLY | Free-floating attendee IDs may remain in legacy or compatibility paths. | Versioned participant edges with authority and visibility basis. | RF36 | Approve external attendee handling. | Improper event access. | P1 | Participant inventory; permission tests. |
| RG-O03 | External calendar copies | STRONG | FOUNDATION_ONLY | Provider copies may be mistaken for canonical events or deleted on disconnect. | Projection registry, sync state, conflict rules, disconnect behavior. | RF36 | Approve conflict policy. | Event loss or overwrite. | P0 | Sync conflict and disconnect scenarios. |
| RG-O04 | Facility identity records | STRONG | IMPLEMENTED_AND_EVIDENCED | Legacy stall map and location records may still coexist with canonical facility structures. | Continue convergence without destructive assumptions. | Later facility maintenance | None if RF28 closure preserved. | Fragmented location truth. | P2 | Legacy inventory and alias map. |
| RG-O05 | Horse location assignments | STRONG | IMPLEMENTED_AND_EVIDENCED | Historical occupancy, temporary custody, transfer timing, and correction lineage need continued alignment. | Versioned assignment and historical projection. | RF31 / facility domains | Approve overlapping assignment exceptions. | Care and emergency confusion. | P1 | Assignment scenarios. |
| RG-O06 | Maintenance records | PARTIAL | PARTIAL_OR_FRAGMENTED | Tickets, work orders, inspections, media, vendors, capital improvements, and facility history may lack one record lifecycle. | Operational record registry and attachment governance. | Future facility RF | Approve transfer during operator change. | Safety and liability gap. | P1 | Maintenance workflow inventory. |
| RG-O07 | Inventory identity | PARTIAL | PARTIAL_OR_FRAGMENTED | Items may be tracked by free text, owner, horse, facility, or purchase record without stable identity. | Canonical asset identity and custody history. | Inventory RF | Approve asset classes. | Loss and responsibility disputes. | P2 | Asset inventory and duplicate tests. |
| RG-O08 | Equipment assignments | PARTIAL | PARTIAL_OR_FRAGMENTED | Ownership, custody, location, horse assignment, and user possession may be conflated. | Separate ownership, custody, assignment, condition, and transfer. | Inventory RF | Approve personal versus organization property rules. | Property disputes. | P1 | Assignment scenarios. |
| RG-O09 | Facility maps and media | PARTIAL | FOUNDATION_ONLY | Maps, photos, diagrams, edits, and historical versions may lack authorship, effective date, and operator transition rules. | Versioned facility-document record class. | Facility RF | Approve archival and successor access. | Unsafe or stale operational information. | P1 | Map version tests. |
| RG-O10 | Organization-to-facility transition | STRONG | NOT_FOUND | New operator may inherit too much or too little historical and current data. | Succession review by record category and period. | Business / facility transition RF | Approve successor access. | Privacy and operational continuity risk. | P1 | Operator-change scenario. |

---

## 20. Storage, Files, Media, Backups, and Disaster Recovery

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-S01 | Object storage identity | PARTIAL | FOUNDATION_ONLY | Storage keys and public URLs may be treated as record identity. | Stable record IDs with storage-location aliases and object versions. | RF33 / storage RF | Approve object identity contract. | Broken references and access drift. | P1 | Storage abstraction review. |
| RG-S02 | Private object policy | PARTIAL | FOUNDATION_ONLY | S3-compatible/R2 abstraction exists, but private-bucket policy for legal and medical records is unverified. | Private-by-default sensitive object classes and scoped access. | RF33 / ATLAS5 | Approve storage policy. | Unauthorized disclosure. | P0 | Bucket policy; signed URL tests; environment evidence. |
| RG-S03 | Public URL behavior | PARTIAL | FOUNDATION_ONLY | Public-capable URLs may expose sensitive artifacts or survive permission changes. | Prohibit public URLs for restricted classes and expire derived access. | Storage RF | Approve exceptions. | High-severity data exposure. | P0 | URL inventory; revocation tests. |
| RG-S04 | Media copyright and license | PARTIAL | NOT_FOUND | Photographer, uploader, horse owner, facility, and subjects may hold different rights. | Copyright, license, consent, reuse, transfer, and attribution fields. | Media / legal RF | Approve default license treatment. | IP disputes. | P1 | Media scenarios and terms review. |
| RG-S05 | GPS and biometric metadata | PARTIAL | NOT_FOUND | Device metadata may be retained or disclosed without purpose controls. | Metadata minimization and separate sensitivity class. | Privacy / media RF | Approve collection and retention. | Privacy and security risk. | P1 | Metadata inventory. |
| RG-S06 | Thumbnails and previews | PARTIAL | FOUNDATION_ONLY | Derivatives may survive source deletion or inherit stale access. | Derivative lineage, permission inheritance, invalidation, disposal. | Storage RF | Approve derivative retention. | Residual disclosure. | P1 | Source-deletion tests. |
| RG-S07 | OCR and transcripts | PARTIAL | NOT_FOUND | Derived text may conflict with signed or source artifacts and be mistaken for authoritative content. | Derived classification, source linkage, confidence, correction, deletion. | RF33 / AI or document RF | Approve display and search use. | Misrepresentation. | P1 | OCR conflict scenarios. |
| RG-S08 | Backup inventory | PARTIAL | OUTSIDE_REPOSITORY_EVIDENCE | Backup systems, scope, custodians, regions, encryption, and retention are unverified. | Operational backup registry and evidence package. | ATLAS5 / infrastructure | Approve backup owner. | Data loss or over-retention. | P0 | Vendor/account evidence; restore test. |
| RG-S09 | Restore testing | PARTIAL | UNVERIFIED | No governed evidence proves restoration completeness and policy reconciliation. | Scheduled restore tests and access/retention replay. | Infrastructure RF | Approve test frequency and acceptance. | False recovery confidence. | P0 | Restore report; discrepancy ledger. |
| RG-S10 | Backup deletion | PARTIAL | UNVERIFIED | Privacy erasure and legal hold may not propagate to immutable backups. | Approved delayed-deletion, crypto-erasure, or restore-replay policy. | Infrastructure / privacy RF | Approve policy. | Regulatory and privacy conflict. | P1 | Backup architecture and deletion analysis. |
| RG-S11 | Lost encryption key | PARTIAL | NOT_FOUND | No canonical incident and recovery rule exists. | Security incident, affected-record inventory, notification, and availability response. | Security RF | Approve key-custodian model. | Permanent data loss. | P0 | Key-loss scenario. |
| RG-S12 | Corrupted attachment | STRONG | NOT_FOUND | No unified quarantine, replica comparison, chain, or user-notice process. | Corruption workflow and evidence. | Storage / incident RF | Approve replacement and notice policy. | Evidence loss. | P1 | Corruption and restore tests. |
| RG-S13 | Storage-provider migration | STRONG | NOT_FOUND | Provider change could alter URLs, metadata, residency, hashes, access, or retention. | Manifested migration, verification, access delta, rollback. | ATLAS5 / storage migration RF | Approve migration authority. | Loss or disclosure. | P0 | Dry run; checksum and permission comparison. |

---

## 21. AI, Analytics, Search, Index, Cache, and Derived Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-D01 | AI summaries | STRONG | FOUNDATION_ONLY | AI packages may exist, but RF30 permits deterministic-fake-only and default-off behavior. | Preserve derived-only status and source references before future activation. | Future AI RF after separate authorization | Approve whether any reviewed output may be promoted to a canonical human-authored record. | AI-generated misinformation becoming truth. | P0 | RF30 traceability; promotion scenario. |
| RG-D02 | AI recommendations | STRONG | FOUNDATION_ONLY | Recommendations could influence care, finance, safety, or transfer without authority boundaries. | Approval state, source lineage, confidence, and prohibited autonomous effects. | Future AI RF | Approve authority classes. | Unsafe or unauthorized action. | P0 | Approval and denial tests. |
| RG-D03 | Embeddings | PARTIAL | NOT_FOUND | Source deletion, permission change, tenant separation, and legal hold propagation are unresolved. | Embedding registry, lineage, deletion, regeneration, and isolation. | Future AI/search RF | Approve retention and deletion policy. | Residual sensitive data. | P0 | Source-deletion and access tests. |
| RG-D04 | Vector indexes | PARTIAL | NOT_FOUND | Vectors could aggregate data across tenants or outlive sources. | Tenant-scoped index, source manifest, rebuild, deletion, and hold behavior. | Future AI/search RF | Approve architecture. | Cross-tenant disclosure. | P0 | Isolation and rebuild tests. |
| RG-D05 | Search indexes | PARTIAL | PARTIAL_OR_FRAGMENTED | Search may expose stale or unauthorized content after permission changes. | Permission-aware indexing, invalidation, redaction, and deletion. | Search RF | Approve indexed fields and latency. | Sensitive disclosure. | P0 | Revocation and stale-index tests. |
| RG-D06 | Analytics datasets | PARTIAL | PARTIAL_OR_FRAGMENTED | Derived tables may outlive sources or enable re-identification and prohibited inference. | Purpose, cohort suppression, source lineage, retention, disposal. | Analytics RF | Approve suppression thresholds and retention. | Privacy and fairness risk. | P1 | Dataset inventory; re-identification review. |
| RG-D07 | Dashboards and reports | PARTIAL | PARTIAL_OR_FRAGMENTED | Snapshot time, source version, audience, and official status may be unclear. | Report metadata and official/informational distinction. | Analytics / reporting RF | Approve official-report classes. | Misleading business decisions. | P2 | Report lineage samples. |
| RG-D08 | Materialized views and projections | STRONG | PARTIAL_OR_FRAGMENTED | Projections may be edited or treated as independent truth. | Read-only or governed write-back boundaries and rebuild evidence. | Domain RFs | Approve exceptions. | Canon divergence. | P1 | Projection inventory and mutation tests. |
| RG-D09 | Application caches | PARTIAL | PARTIAL_OR_FRAGMENTED | Cached data may outlive permission, consent, deletion, or relationship changes. | Cache classification, TTL, invalidation, tenant isolation, and purge. | Platform RF | Approve maximum sensitivity in cache. | Unauthorized disclosure. | P0 | Permission-revocation and purge tests. |
| RG-D10 | Exports as derived copies | STRONG | PARTIAL_OR_FRAGMENTED | Export copies may be mistaken for continuing canonical truth. | Snapshot metadata, expiry, recipient warning, manifest, and access log. | RF31 / support / legal | Approve export validity and revocation language. | Stale records used as current truth. | P1 | Export package examples. |

---

## 22. Security, Audit, Support, Legal, and Administrative Records

| ID | Record Category | Canon Coverage | Repository Coverage | Gap / Conflict | Missing Implementation | Future RF | Founder Decision | Risk | Priority | Evidence Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RG-A01 | Audit event identity | PARTIAL | PARTIAL_OR_FRAGMENTED | Logs may lack policy version, permission decision, prior/after reference, correlation, or environment. | Canonical audit contract and immutability policy. | Platform / security RF | Approve required classes. | Weak evidence and debugging. | P1 | Audit field inventory. |
| RG-A02 | Audit retention | PARTIAL | UNVERIFIED | Duration, access, minimization, and legal hold behavior are unresolved. | Retention class and restricted-access policy. | Security / legal governance | Approve duration through later schedule. | Over-retention or missing evidence. | P1 | Log platform evidence. |
| RG-A03 | Administrative access records | PARTIAL | PARTIAL_OR_FRAGMENTED | Admin reads, exports, impersonation, corrections, and break-glass actions may not be uniformly audited. | High-risk admin action event model. | Permission / admin RF | Approve privileged admin roles. | Insider risk. | P0 | Admin action tests. |
| RG-A04 | Support tickets | PARTIAL | PARTIAL_OR_FRAGMENTED | Customer content, internal notes, security reports, legal requests, and product feedback may share one visibility model. | Ticket subtype classification and restricted escalation. | Support RF | Approve internal-note and customer-export rules. | Sensitive disclosure. | P1 | Ticket inventory and projection tests. |
| RG-A05 | Security incident records | PARTIAL | PARTIAL_OR_FRAGMENTED | Detection, containment, evidence, affected subjects, notice, and legal review may be disconnected. | Canonical incident record and evidence package. | Security RF | Approve steward and access roles. | Breach-response failure. | P0 | Incident tabletop evidence. |
| RG-A06 | Breach notification records | PARTIAL | NOT_FOUND | Notification basis, recipients, timing, delivery, regulator reporting, and exceptions are undefined. | Governed breach-notification record. | Security / legal RF | Approve authority and workflow. | Regulatory exposure. | P0 | Breach scenario. |
| RG-A07 | Privileged legal records | PARTIAL | NOT_FOUND | Broad platform admins may technically access files without matter-based controls. | Separate restricted store or projection, access approval, audit, export limits. | Legal governance RF | Approve custodians. | Privilege waiver. | P0 | Access tests and role review. |
| RG-A08 | Attorney work product | PARTIAL | NOT_FOUND | Work product may be mixed with ordinary support, dispute, or admin notes. | Explicit classification and restricted workflow. | Legal governance RF | Approve classification and disclosure. | Privilege and litigation risk. | P0 | Matter-record scenarios. |
| RG-A09 | Government request records | PARTIAL | NOT_FOUND | Request identity, authenticity, legal review, hold, production, notice, and closure lack governance. | Canonical request and production package. | Legal governance RF | Approve handling policy. | Unauthorized disclosure. | P0 | Request workflow tests. |
| RG-A10 | Compliance and regulatory records | PARTIAL | NOT_FOUND | Obligations, filings, attestations, evidence, jurisdiction, and retention are fragmented. | Compliance record registry. | Future compliance RF | Approve scope and owner. | Regulatory risk. | P1 | Compliance inventory. |
| RG-A11 | Migration evidence | STRONG | PARTIAL_OR_FRAGMENTED | Migration scripts may not preserve per-row provenance, access deltas, quarantine, rollback, and reconciliation. | Standard migration evidence package. | Every migration RF | None beyond adoption. | Silent authority or data drift. | P0 | Dry-run output; access-delta report. |
| RG-A12 | Deletion-job evidence | STRONG | NOT_FOUND | No controlled evidence package for selection, holds, failures, retries, and actual destruction. | Disposal manifest, approvals, results, exceptions, and alerts. | Future retention RF | Approve disposal reviewer. | Irreversible loss. | P0 | Synthetic deletion run only after authorization. |

---

## 23. Priority Founder Decisions

The following founder decisions should be resolved before the Record Stewardship and Retention Model is adopted or before dependent implementation begins.

### 12.1 Adoption-blocking decisions

1. Approve the canon tier and authority order.
2. Approve the canonical record registry structure.
3. Approve the initial record-type registry subset.
4. Approve canonical record ID and version-lineage requirements.
5. Approve the distinction among record owner, steward, author, subject, custodian, and viewer.
6. Approve sensitivity and stewardship class registries.
7. Approve field-level and attachment-level severability.
8. Approve conflict-of-record authority and neutral preservation rules.
9. Approve duplicate merge authority and reversible-evidence requirements.
10. Approve retention schedule governance without inventing durations.
11. Approve legal-hold authority, scope, precedence, release, and audit rules.
12. Approve privacy-erasure versus retention and hold precedence.
13. Approve historical in-app access versus export-only access.
14. Approve transfer-package disclosure categories.
15. Approve break-glass access roles and post-review.
16. Approve guardian, minor, and Safe Sport record restrictions.
17. Approve privileged and work-product custodians.
18. Approve restoration replay and deleted-data reconciliation.
19. Approve chain-of-custody requirements.
20. Approve derived-record policy for AI, analytics, embeddings, search indexes, and caches.
21. Approve organization succession and acquisition rules.
22. Approve data residency and jurisdiction escalation.
23. Approve imported-record trust and quarantine thresholds.

### 12.2 RF31-specific decisions

1. Which Passport records are always horse-canonical.
2. Which medical records transfer automatically, by consent, by redacted disclosure, or not at all.
3. Whether former barns retain direct application access or export-only access.
4. How private owner and trainer notes are classified.
5. Which transfer records require dual confirmation.
6. Which ownership evidence is sufficient for verified transfer.
7. Who may resolve disputed ownership or transfer claims.
8. How estate, trust, rescue, seizure, missing, stolen, and impound scenarios are handled.
9. What integrity evidence accompanies a transfer package.
10. How partially completed transfers are reversed or reconciled.

### 12.3 RF32-specific decisions

1. Canonical distinction between obligation, invoice, payment attempt, settlement, refund, dispute, chargeback, adjustment, and write-off.
2. Whether payment responsibility may be accepted without an EquineSync account.
3. Which operational restrictions may follow nonpayment.
4. Which restrictions are prohibited because they would affect ownership, guardian authority, emergency care, or record history.
5. How internal payment state is labeled before provider settlement.
6. Historical access for former payers and guarantors.
7. Financial dispute retention and export.
8. Owner-safe financial projection rules.

---

## 24. Future RF and Gate Mapping

| Workstream | Primary Gaps | Proposed Owner | Required Predecessors | Explicit Non-Goals |
| --- | --- | --- | --- | --- |
| Record canon adoption | RG-C01 through RG-C40 | Founder-controlled canon review | Full alignment report and correction ledger | No implementation or migration. |
| Horse transfer and Passport continuity | RG-H01 through RG-H15; RG-C10; RG-C20; RG-C28 | RF31 | Relationship Model; adopted Record Model; RF27 boundary | No physical intake redesign; no production migration. |
| Barn payment issue workflow | RG-F06 through RG-F10; RG-C06; RG-C20 | RF32 | Relationship Model; adopted Record Model | No Stripe Connect or production money movement. |
| Agreements and e-signature | RG-F01 through RG-F05; RG-S01 through RG-S03; RG-C31; RG-C32 | RF33 | Record canon; Relationship Model; private storage decision | No production sender activation without separate approval. |
| Identity and communications | RG-P01 through RG-P13; RG-C35 | RF34 | Record canon; Permission Model; guardian decisions | No automatic provider replacement or external messaging activation. |
| Financial rails | RG-F07 through RG-F13 | RF35 | RF32; record canon; payment-scope decision | No money movement without explicit authorization. |
| External calendars | RG-O01 through RG-O03 | RF36 | RF29 locked canon; record canon | No provider overwrite of canonical events. |
| Retention and disposal implementation | RG-C21 through RG-C27; RG-A12 | Future separately authorized RF | Adopted record canon; approved schedules; legal-hold workflow | No production deletion during planning. |
| Legal hold and discovery | RG-C24; RG-C33; RG-C34; RG-A07 through RG-A10 | Future legal-governance RF | Founder legal-policy decisions | No legal advice claim or production hold activation during planning. |
| Backup and disaster recovery | RG-C29; RG-C30; RG-S08 through RG-S13 | Infrastructure readiness gate | Vendor/account evidence; residency decision | No production restoration test without environment authorization. |
| AI, search, and analytics records | RG-D01 through RG-D10 | Future AI/Analytics RFs | RF30 lock; adopted record canon; permission and privacy controls | No real AI provider activation. |

---

## 25. Evidence Package Required Before Founder Adoption

A complete controlled review should produce:

1. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_ALIGNMENT_REPORT.md`
2. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_PROPOSED_CORRECTIONS.md`
3. this `MASTER_RECORD_GOVERNANCE_GAP_MATRIX.md`, updated with repository evidence
4. canonical record inventory
5. repository reality inventory
6. record-category transfer and historical-access matrix
7. proposed canonical record registry
8. proposed sensitivity registry
9. proposed stewardship registry
10. proposed retention-governance framework
11. legal-hold governance proposal
12. privacy-erasure precedence proposal
13. migration and access-delta risk assessment
14. backup and restoration replay assessment
15. founder decision ledger
16. validation-scenario assessment
17. proposed dependency language for RF31, RF32, RF33-RF36, and ATLAS5
18. proposed `CANON_INDEX.md` insertion text
19. non-implementation attestation
20. documentation and diff-hygiene evidence.

---

## 26. Non-Implementation Attestation

This matrix:

- does not adopt or lock the Record Stewardship and Retention Model;
- does not create a schema;
- does not create a route, service, worker, adapter, or UI;
- does not change permissions;
- does not change Passport or Care Circle behavior;
- does not migrate or backfill data;
- does not execute retention or disposal;
- does not activate legal holds;
- does not activate external services;
- does not modify RF29 or RF30;
- does not open RF31-RF36;
- does not claim legal completeness for every jurisdiction;
- does not establish jurisdiction-specific retention periods;
- does not claim repository implementation is complete.

---

## 27. Proposed Stop State

```text
MASTER_RECORD_GOVERNANCE_GAP_MATRIX_READY_FOR_CONTROLLED_REPOSITORY_VALIDATION
```

The next authorized step should be repository-backed validation and correction of this matrix during the controlled review of `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md`.

No canon adoption, implementation, migration, production mutation, retention execution, disposal execution, legal-hold activation, external-service activation, or RF state change is authorized by this artifact.

---

## 28. Version 2.0 Completion Criteria

This framework is ready for controlled founder review when:

- all ten governance expansions are reviewed;
- authority hierarchy is accepted;
- the dependency graph is accepted;
- governance principles are accepted;
- the record state machine is accepted;
- stewardship powers and separation of duties are accepted;
- the registry specification is accepted;
- the maturity model is accepted;
- the risk register is reviewed;
- canon evolution rules are accepted;
- every original matrix row remains preserved;
- no implementation is falsely claimed.

---

## 29. Version 2.0 Non-Implementation Attestation

Version 2.0:

- does not adopt or lock the Record Stewardship Model;
- does not create schemas or routes;
- does not change permissions;
- does not migrate or backfill data;
- does not execute retention, erasure, or disposal;
- does not activate legal holds;
- does not activate vendors;
- does not modify RF29 or RF30;
- does not open RF31-RF36;
- does not claim production readiness;
- does not establish jurisdiction-specific legal advice or retention periods.

---

## 30. Required Stop State

```text
MASTER_RECORD_GOVERNANCE_GAP_MATRIX_V2_0_READY_FOR_CONTROLLED_FOUNDER_REVIEW
```

No correction, adoption, lock, implementation, migration, production mutation, retention execution, disposal execution, legal-hold activation, external-service activation, or RF state change is authorized by this document.
