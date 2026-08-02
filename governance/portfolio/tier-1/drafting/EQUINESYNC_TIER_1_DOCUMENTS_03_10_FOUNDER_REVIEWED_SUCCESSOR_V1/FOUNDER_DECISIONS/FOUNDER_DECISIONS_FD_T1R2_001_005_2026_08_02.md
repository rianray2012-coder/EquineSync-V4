# EQUINESYNC TIER 1 DOCUMENTS 03–10

## Founder Decisions FD-T1R2-001 Through FD-T1R2-005

**Founder:** Rian Ray
**Decision date:** August 2, 2026
**Applicable package:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_FINAL_DRAFT`
**Applicable draft PR:** PR #85
**Applicable review head:** `1a3c65c992b1a2f23d205a9d5dcd878ad37cd146`

## Controlling Authority Limitation

These decisions are documentary Founder decisions only.

Except where expressly stated below, these decisions do not authorize:

* implementation;
* activation;
* production use;
* deployment;
* certification;
* automatic closure of findings;
* direct protected-branch mutation;
* merge of PR #85 or any other pull request; or
* exercise of authority beyond the documentary scope of the applicable decision.

The following states remain controlling unless separately changed through an express Founder directive:

* `NOT_ACTIVE`
* `IMPLEMENTATION_NOT_AUTHORIZED`
* `PRODUCTION_USE_NOT_AUTHORIZED`
* `MERGE_NOT_AUTHORIZED`
* `CERTIFICATION_NOT_COMPLETE`
* `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

# FD-T1R2-001

## Approval of the 13-State Lifecycle Vocabulary and Documentary Transition Rules

### Founder Decision

`APPROVE`

I approve the validated 13-state lifecycle vocabulary and the associated documentary transition rules for use in EquineSync Tier 1 governance documentation.

This approval establishes the lifecycle vocabulary and rules as the controlling documentary framework for describing the status of Tier 1 governance artifacts.

### Scope of Approval

This approval applies to:

* the lifecycle state register;
* the lifecycle transition matrix;
* invalid-state rules;
* lifecycle definitions;
* lifecycle-related schemas and data dictionaries;
* validation rules enforcing exact lifecycle membership and transition consistency; and
* future Tier 1 governance documents that use this lifecycle framework.

### Conditions

1. The lifecycle framework must continue to distinguish documentary status from implementation, deployment, operational use, and production authorization.
2. Rejection, remediation, blocked, superseded, and historical states must remain available where applicable.
3. No lifecycle transition may be inferred from the existence of this approval.
4. Each actual transition requires the authority and evidence required for that specific transition.
5. Validators must continue to detect invalid combinations and unauthorized advancement.

### Authority Granted

Authority is granted to use the approved 13-state lifecycle vocabulary and transition rules in future Tier 1 governance drafting, review, validation, and status reporting.

### Authority Not Granted

This decision does not move any existing document into another lifecycle state.

It does not authorize adoption, lock, accession, activation, implementation, production use, certification, or merge of any specific artifact.

### Final Disposition

`FD-T1R2-001_APPROVED_WITH_DOCUMENTARY_SCOPE_ONLY`

---

# FD-T1R2-002

## Approval of the Governance Accountability Structure and Direction for Named Appointments

### Founder Decision

`APPROVE_WITH_MODIFICATIONS`

I approve the governance accountability structure and the defined accountable functions contained in the Tier 1 Documents 03–10 final draft.

I do not, through this decision alone, appoint unnamed or inferred individuals to those functions.

Named natural-person appointments must be recorded through a separate appointment schedule or authenticated Founder appointment instrument.

### Scope of Approval

This approval applies to:

* the governance ownership and accountability matrix;
* defined accountable functions;
* vacancy and succession controls;
* appointment-evidence requirements;
* acceptance-evidence requirements;
* review-calendar dependencies; and
* identification of controls that remain inoperative while a role is vacant.

### Founder Direction

Codex shall prepare a separate:

`TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE`

The schedule must identify, for each role:

* role title;
* responsibilities;
* authority limits;
* proposed appointee;
* appointment date;
* written acceptance status;
* vacancy status;
* succession or backup designation;
* conflicts or independence limitations; and
* controls affected if the position remains vacant.

No appointee may be inferred from repository activity, authorship, job title, ownership interest, or prior participation.

### Interim Status

Until named appointments are separately recorded:

* each unfilled role remains `VACANT_PENDING_FOUNDER_APPOINTMENT`;
* review activities assigned to that role remain `NOT_OPERATIVE_PENDING_APPOINTMENT`;
* no closure, acceptance, certification, or approval authority may be inferred for that role; and
* existing documentary work may continue where it does not require exercise of the vacant authority.

### Authority Granted

Authority is granted to use the approved accountability structure and to prepare the appointment schedule for Founder disposition.

### Authority Not Granted

This decision does not appoint any unnamed person.

It does not create employment, compensation, contract, spending, merge, adoption, activation, implementation, or production authority.

### Final Disposition

`FD-T1R2-002_ACCOUNTABILITY_STRUCTURE_APPROVED_NAMED_APPOINTMENTS_RETAINED_FOR_SEPARATE_FOUNDER_ACTION`

---

# FD-T1R2-003

## Approval of the Documentary Source-Control and Precedence Hierarchy

### Founder Decision

`APPROVE_WITH_MODIFICATIONS`

I approve the documentary source-control and precedence hierarchy established in the Tier 1 Documents 03–10 final draft, subject to the limitations and continuing controls below.

### Approved Hierarchy Principles

Where multiple sources conflict, overlap, duplicate, or purport to control the same subject, documentary precedence must be determined using authenticated evidence, including:

1. express Founder approval or direction;
2. formally adopted or locked governance authority;
3. later valid supersession evidence;
4. repository custody and accession evidence;
5. authenticated version and commit information;
6. complete source provenance;
7. express scope and authority limitations;
8. source-specific reconciliation evidence; and
9. unresolved-source treatment where no controlling source can yet be determined.

File recency, filename, location, authorship, or apparent completeness alone is not sufficient to establish controlling authority.

### Conditions

1. Duplicate clusters must retain valid foreign-key relationships.
2. Canonical sources must be identified through evidence rather than self-reference.
3. `SUPERSEDED` and `HISTORICAL_RETAINED` must remain distinct.
4. Sources lacking sufficient evidence must be marked `CANONICAL_NOT_DETERMINED`, `AUTHORITY_NOT_ESTABLISHED`, or an equivalent truthful state.
5. Historical evidence of approval or adoption must not be represented as approval or adoption of the present package.
6. Source-reconciliation arithmetic and dashboard totals must remain validator-enforced.
7. Approval of the hierarchy does not approve the substantive content of every indexed source.

### Authority Granted

Authority is granted to apply the approved documentary precedence hierarchy in future source reconciliation, provenance review, supersession analysis, and Tier 1 documentary preparation.

### Authority Not Granted

This decision does not automatically make any individual source controlling, adopted, active, implemented, or production-authorized.

It does not resolve any source marked as unresolved without sufficient evidence.

### Final Disposition

`FD-T1R2-003_SOURCE_CONTROL_HIERARCHY_APPROVED_WITH_EVIDENCE_AND_NONINFERENCE_CONTROLS`

---

# FD-T1R2-004

## Approval of the Residual-Risk and Finding Disposition Method

### Founder Decision

`APPROVE_WITH_MODIFICATIONS`

I approve the method and control framework for documenting, evaluating, remediating, waiving, accepting, deferring, closing, and reopening findings and residual risks.

I do not approve or accept all identified risks or findings in bulk.

### Scope of Approval

This approval applies to:

* the findings and risk taxonomy;
* severity and status controls;
* root-cause requirements;
* mitigation and remediation records;
* closure-evidence requirements;
* duplicate and staleness analysis;
* waiver requirements;
* waiver expiration controls;
* risk-acceptance authority;
* reopening requirements; and
* residual-risk reporting.

### Founder Direction

Each substantive finding or residual risk must receive an individual disposition.

Permitted individual dispositions are:

* `REQUIRE_REMEDIATION`;
* `ACCEPT_RESIDUAL_RISK`;
* `GRANT_TIME_BOUNDED_WAIVER`;
* `DEFER_WITH_RECORDED_BASIS`;
* `REJECT_PROPOSED_TREATMENT`;
* `CLOSE_WITH_VERIFIED_EVIDENCE`; or
* `REOPEN`.

### Conditions for Risk Acceptance

No item may be marked `ACCEPT_RESIDUAL_RISK` unless the record identifies:

* the exact risk;
* the affected control or requirement;
* severity and rationale;
* existing mitigation;
* remaining exposure;
* the person exercising acceptance authority;
* the scope of that authority;
* the acceptance date;
* the duration or review date;
* required monitoring; and
* any conditions or exclusions.

### Conditions for Closure

No finding may be closed solely because:

* a document was revised;
* a validator passed;
* a pull request was opened;
* a recommendation was acknowledged;
* a future activity is planned; or
* the finding is inconvenient or stale.

Closure requires the exact evidence required by the applicable finding.

### Treatment of F-12

F-12 remains partially remediated.

Any schema exemplar, demonstration row, or sample entry must remain clearly separated from actual findings and actual accepted risks.

No demonstration data is accepted as a real residual risk through this decision.

### Authority Granted

Authority is granted to use the approved findings and residual-risk control framework and to prepare item-specific dispositions for Founder or properly delegated authority.

### Authority Not Granted

This decision does not constitute blanket risk acceptance, blanket waiver, closure of all findings, operational risk acceptance, or approval of risks not individually presented.

### Final Disposition

`FD-T1R2-004_RISK_AND_FINDING_DISPOSITION_FRAMEWORK_APPROVED_NO_BULK_RISK_ACCEPTANCE`

---

# FD-T1R2-005

## Approval of Future Documentary Review, Adoption-Consideration, and Merge-Consideration Sequencing

### Founder Decision

`APPROVE_SEQUENCE_WITH_CONDITIONS`

I approve the following future sequencing framework for Tier 1 Documents 03–10:

1. complete Founder documentary review;
2. record and validate the five Founder decisions;
3. complete any decision-directed corrections;
4. rerun repository-aware and standalone package validation;
5. complete CI and review-thread evaluation;
6. prepare a Founder-approved documentary successor package;
7. separately assess documentary adoption readiness;
8. separately assess merge readiness;
9. obtain express Founder merge authority before any merge; and
10. complete post-merge custody verification if merge is later authorized.

### Conditions

1. PR #85 must remain draft until the Founder decision records and any resulting revisions are complete.
2. Auto-merge must remain disabled.
3. No pull request may be merged solely because it is included in the approved sequence.
4. CI must complete successfully or any failure must be expressly dispositioned.
5. Review threads must be resolved, truthfully deferred, or recorded as retained issues.
6. Base drift must be assessed before merge consideration.
7. Final package hashes and validation evidence must correspond to the exact commit proposed for merge.
8. Any adoption decision must be separately and expressly recorded.
9. Adoption does not itself authorize activation, implementation, production use, or certification.
10. Merge does not itself prove implementation or production readiness.

### Authority Granted

Authority is granted to follow the approved sequence and prepare the next documentary adoption-readiness and merge-readiness materials.

### Authority Not Granted

This decision does not authorize:

* merge of PR #85;
* merge of another PR;
* adoption of the final draft;
* activation;
* implementation;
* production use;
* certification;
* automatic closure of findings; or
* bypass of required validation or branch-protection controls.

### Final Disposition

`FD-T1R2-005_FUTURE_SEQUENCE_APPROVED_MERGE_AND_ADOPTION_REMAIN_SEPARATELY_AUTHORIZED_ACTIONS`

---

# Consolidated Founder Determination

The Founder decisions are recorded as follows:

| Decision    | Disposition                                                               |
| ----------- | ------------------------------------------------------------------------- |
| FD-T1R2-001 | Approved with documentary scope only                                      |
| FD-T1R2-002 | Accountability structure approved; named appointments reserved            |
| FD-T1R2-003 | Source hierarchy approved with evidence controls                          |
| FD-T1R2-004 | Risk and finding framework approved; no bulk risk acceptance              |
| FD-T1R2-005 | Future sequence approved; merge and adoption remain separately authorized |

These decisions authorize preparation of a Founder-reviewed successor package and any bounded documentary corrections necessary to implement the decisions.

They do not authorize merge, implementation, activation, production use, or certification.

## Resulting Status

* `FOUNDER_DIRECTION_RECORDED`
* `DOCUMENTARY_FRAMEWORK_APPROVED_AS_SPECIFIED`
* `NAMED_ROLE_APPOINTMENTS_REMAIN_OPEN`
* `ITEM_SPECIFIC_RISK_DISPOSITIONS_REMAIN_OPEN`
* `DOCUMENTARY_ADOPTION_NOT_YET_AUTHORIZED`
* `NOT_ACTIVE`
* `IMPLEMENTATION_NOT_AUTHORIZED`
* `PRODUCTION_USE_NOT_AUTHORIZED`
* `MERGE_NOT_AUTHORIZED`
* `CERTIFICATION_NOT_COMPLETE`
* `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
