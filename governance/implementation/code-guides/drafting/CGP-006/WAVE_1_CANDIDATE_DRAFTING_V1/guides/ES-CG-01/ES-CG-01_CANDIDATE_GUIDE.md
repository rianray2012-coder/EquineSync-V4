# ES-CG-01 Candidate Guide: Engineering Authority And Precedence

**Package:** `ES-CGP-006-WAVE-1-CANDIDATE-DRAFTING-V1`
**Candidate status:** `CANDIDATE_ONLY`
**Lifecycle status:** `FOUNDER_APPROVED_CANDIDATE_BASELINE`
**Founder review status:** `FOUNDER_REVIEW_COMPLETE`
**Founder candidate-baseline disposition:** `CGP_006_WAVE_1_CANDIDATE_GUIDES_FOUNDER_APPROVED_WITH_RETAINED_NON_BLOCKING_WARNINGS`
**Repository state:** `REPOSITORY_ACCESSIONED`
**Adoption status:** `NOT_ADOPTED`
**Activation status:** `NOT_ACTIVE`
**Repository integration authority:** `PROTECTED_REPOSITORY_INTEGRATION_ALLOWED_FOR_CUSTODY_ONLY`
**Implementation authority:** `IMPLEMENTATION_AUTHORITY_NOT_GRANTED`

## 1. Document Identity

- Document type: Wave 1 bounded candidate Code Guide draft.
- Guide title: Engineering Authority And Precedence.
- This document is review material and is not an adopted, active, or implementation-authorizing baseline.

## 2. Guide Identifier

- `ES-CG-01`

## 3. Candidate Version

- `0.1.0-candidate.1`

## 4. Lifecycle And Authority Status

- `CANDIDATE_ONLY`
- `FOUNDER_APPROVED_CANDIDATE_BASELINE`
- `FOUNDER_REVIEW_COMPLETE`
- `CGP_006_WAVE_1_CANDIDATE_GUIDES_FOUNDER_APPROVED_WITH_RETAINED_NON_BLOCKING_WARNINGS`
- `REPOSITORY_ACCESSIONED`
- `NOT_ADOPTED`
- `NOT_ACTIVE`
- `PROTECTED_REPOSITORY_INTEGRATION_ALLOWED_FOR_CUSTODY_ONLY`
- `IMPLEMENTATION_AUTHORITY_NOT_GRANTED`
- `PRODUCTION_AUTHORITY_NOT_GRANTED`
- `EFFECTIVE_DATE_NOT_APPLICABLE`
- `CGP-007_NOT_ISSUED`

## 5. Purpose

- Define candidate engineering authority and precedence treatment without converting code, tests, runtime behavior, or contextual material into implementation authority.

## 6. Scope

- Authority classes, precedence, Founder disposition, conflict treatment, supersession, and exception boundaries.
- Specialized handling for repository evidence, implementation evidence, external standards, and retained conflicts.
- Dependency on ES-CG-00 framework definitions and lifecycle separation.

## 7. Out-Of-Scope Matters

- Schemas, APIs, migrations, deployment specifications, runtime provider behavior, and code contracts.
- Completion or closure evidence mechanics assigned to ES-CG-13.
- Testing and verification rule details assigned to ES-CG-10.

## 8. Authority Basis

- Frozen normative rows allocated to ES-CG-01: 34.
- Unique normative source identifiers allocated to ES-CG-01: 34.
- Candidate mandatory language in this guide is traceable through the package source matrices.
- Founder-approved context and reference-corpus records remain non-normative and cannot independently create candidate requirements, controls, invariants, prohibitions, or implementation authority.

## 9. Relationship To CGP-005

- Uses the approved CGP-005 Wave 1 guide-specific source-freeze outputs as reconciled by CGP-006.
- Does not amend source bytes, source-freeze counts, reference-corpus counts, retained warnings, retained gaps, or guide allocations.

## 10. Relationship To CGP-006

- Drafted under the CGP-006 Founder-approved document classification gate and Wave 1 bounded candidate drafting handoff.
- Input refresh state: `MAJOR_REFRESH_COMPLETE`.
- CGP-006 authorizes candidate drafting only; it does not authorize guide adoption, activation, merge, implementation, CGP-007, or source promotion.

## 11. Dependency Position

- Drafted after ES-CG-00 Gate 1; inherits the framework and specializes engineering authority and precedence.

## 12. Inherited Definitions

- Inherits candidate framework from ES-CG-00 version 0.1.0-candidate.1.

## 13. Guide-Specific Definitions

- authority_precedence: Candidate ordering of controlling, supporting, historical, proposed, blocked, and implementation-evidence source treatment.
- founder_disposition: Founder-level decision state that can approve, retain, defer, or block a governance treatment.
- retained_conflict: A visible non-blocking conflict carried into candidate drafting without silent resolution.

## 14. Affected Actors, Records, Or Systems

- Founder, engineering authority reviewer, source custodian, Code Guide drafter.
- Authority registers, conflict register, source-freeze records, repository evidence records.

## 15. Candidate Principles

- Engineering authority is documentary unless later adopted and activated through authorized governance.
- Code and tests may be cited as evidence only when the frozen normative rows permit documentary treatment.
- Retained conflicts remain visible and cannot be resolved by silent drafting edits.

## 16. Candidate Controls

- Complete control records are in `registers/CGP_006_WAVE_1_CONTROL_REGISTER.csv`.

| control_identifier | title | related_invariant | implementation_status |
| --- | --- | --- | --- |
| ES-CG-01-CTRL-0001 | Candidate Authority Precedence | ES-CG-01-INV-0001 | NOT_AUTHORIZED |
| ES-CG-01-CTRL-0002 | Candidate Founder Disposition | ES-CG-01-INV-0002 | NOT_AUTHORIZED |
| ES-CG-01-CTRL-0003 | Candidate Conflict Treatment | ES-CG-01-INV-0003 | NOT_AUTHORIZED |
| ES-CG-01-CTRL-0004 | Candidate Supersession Treatment | ES-CG-01-INV-0004 | NOT_AUTHORIZED |
| ES-CG-01-CTRL-0005 | Candidate Exception Boundary | ES-CG-01-INV-0005 | NOT_AUTHORIZED |

## 17. Candidate Invariants

- Complete invariant records are in `registers/CGP_006_WAVE_1_INVARIANT_REGISTER.csv`.

| invariant_identifier | related_controls | implementation_status |
| --- | --- | --- |
| ES-CG-01-INV-0001 | ES-CG-01-CTRL-0001 | NOT_AUTHORIZED |
| ES-CG-01-INV-0002 | ES-CG-01-CTRL-0002 | NOT_AUTHORIZED |
| ES-CG-01-INV-0003 | ES-CG-01-CTRL-0003 | NOT_AUTHORIZED |
| ES-CG-01-INV-0004 | ES-CG-01-CTRL-0004 | NOT_AUTHORIZED |
| ES-CG-01-INV-0005 | ES-CG-01-CTRL-0005 | NOT_AUTHORIZED |

## 18. Mandatory-Question Answers

- Mandatory-question answers are candidate-only, remain partial, and are accepted as `PARTIALLY_ANSWERED_ACCEPTABLE_FOR_CANDIDATE_STAGE` for the Founder-approved candidate baseline only.

| question_identifier | answer_status | validation_status |
| --- | --- | --- |
| ES-CG-01-DQ-0001 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0002 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0003 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0004 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0005 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0006 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0007 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |
| ES-CG-01-DQ-0008 | PARTIALLY_ANSWERED | TRACEABLE_TO_FROZEN_NORMATIVE_ROWS |

## 19. Candidate Exceptions

- No active candidate exception is granted.
- Any future exception requires separate Founder authority before adoption or activation.

## 20. Prohibited Interpretations

- This guide is not adopted, not active, not merged, and not implementation-authorizing.
- This guide does not authorize application changes, product tests, CI changes, schemas, migrations, deployment, providers, pilots, production, financial operations, messaging, moderation, AI behavior, archive behavior, enrollment, PIAs, implementation atlases, or CGP-007.
- Contextual or reference-only material cannot be treated as mandatory authority.

## 21. Risks

- Candidate status overclaim.
- Source promotion by repetition of context or reference material.
- Retained warnings or gaps hidden during downstream review.

## 22. Failure Modes

- Code evidence is treated as direct governance authority.
- A retained conflict is closed without Founder disposition.
- An external standard is silently made binding.

## 23. Retained Warnings

| identifier | status | current_blocking_status | founder_decision_requirement |
| --- | --- | --- | --- |
| CGP006-CLF-0002 | RETAINED_NON_BLOCKING_WARNING | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP006-CLF-0003 | RETAINED_NON_BLOCKING_WARNING | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP006-CLF-0004 | RETAINED_NON_BLOCKING_WARNING | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP006-CLF-0005 | RETAINED_NON_BLOCKING_WARNING | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |

## 24. Retained Gaps

| identifier | status | current_blocking_status | founder_decision_requirement |
| --- | --- | --- | --- |
| CGP005-TA-APP-GAP-0001 | RETAINED_OPEN_GAP | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP005-TA-APP-GAP-0002 | RETAINED_OPEN_GAP | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP005-TA-APP-GAP-0003 | RETAINED_OPEN_GAP | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |
| CGP005-TA-APP-GAP-0004 | RETAINED_OPEN_GAP | NON_BLOCKING_FOR_CANDIDATE_DRAFTING | REQUIRED_BEFORE_ADOPTION_OR_ACTIVATION |

## 25. Unresolved Questions

- NONE_IDENTIFIED_FOR_CANDIDATE_DRAFTING

## 26. Founder Decisions Required

- NONE_REQUIRED_TO_COMPLETE_THIS_CANDIDATE_DRAFTING_PACKAGE
- FOUNDER_REVIEW_REQUIRED_BEFORE_ANY_ADOPTION_OR_ACTIVATION

## 27. Normative-Source Traceability

- ES-CG-01 normative row count: 34.
- Normative row range: CGP006-NR-0030 through CGP006-NR-0063.
- See `traceability/CGP_006_WAVE_1_NORMATIVE_ROW_DISPOSITION_MATRIX.csv`, `traceability/CGP_006_WAVE_1_CONTROL_TO_SOURCE_MATRIX.csv`, `traceability/CGP_006_WAVE_1_INVARIANT_TO_SOURCE_MATRIX.csv`, and `traceability/CGP_006_WAVE_1_MANDATORY_QUESTION_TO_SOURCE_MATRIX.csv`.

## 28. Contextual-Source Influence

- Contextual rows may influence interpretation, risk treatment, questions, exceptions, ambiguity identification, warning treatment, and gap treatment only.
- See `traceability/CGP_006_WAVE_1_CONTEXTUAL_SOURCE_USE_REGISTER.csv`.

## 29. Reference-Corpus Usage

- Reference-corpus rows remain `REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE` and support background, navigation, comparison, terminology discovery, duplicate detection, and historical understanding only.
- See `traceability/CGP_006_WAVE_1_REFERENCE_CORPUS_USE_REGISTER.csv`.

## 30. Cross-Guide Dependencies

- Drafted after ES-CG-00 Gate 1; inherits the framework and specializes engineering authority and precedence.
- See `traceability/CGP_006_WAVE_1_CROSS_GUIDE_DEPENDENCY_MATRIX.csv` and `traceability/CGP_006_WAVE_1_CROSS_GUIDE_CONFLICT_REGISTER.csv`.

## 31. Validation Criteria

- Guide status, source integrity, requirement support, warning/gap treatment, cross-guide dependency, identifier uniqueness, checksum, and authority-prohibition validators must pass for candidate package readiness.
- Required gate status: `ES_CG_01_COMPLETE_CANDIDATE_DRAFT_DEPENDENCY_VALIDATION_PASS`.

## 32. Adoption Prerequisites

- Founder review and separate adoption authority.
- Retained warnings and gaps carried into adoption review.
- No adoption occurs in this package.

## 33. Activation Prerequisites

- Separate activation authority after adoption.
- No activation occurs in this package.

## 34. Implementation Boundary

- `IMPLEMENTATION_AUTHORITY_NOT_GRANTED`
- Controls and invariants use `implementation_status = NOT_AUTHORIZED`.

## 35. Change-Control Requirements

- Any material source classification, source-byte, source-freeze, warning, gap, dependency, or authority change requires a later authorized workstream.
- This package cannot promote sources or issue CGP-007.

## 36. Version History

- 2026-07-27: `0.1.0-candidate.1` created as Wave 1 bounded candidate draft under CGP-006.
