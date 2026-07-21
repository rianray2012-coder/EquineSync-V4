# Document Overview and Rationale

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

| Artifact | Purpose | Primary reader |
| --- | --- | --- |
| ACCEPTANCE_CRITERIA.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| ADVERSARIAL_SCENARIOS.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| API_EVENT_JOB_CONTRACTS.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| AS_BUILT_RECONCILIATION.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| CHANGE_CONTROL_LOG.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| DATA_DICTIONARY.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| DEPENDENCY_REGISTER.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| DOCUMENTARY_CHANGE_MANIFEST.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| DOCUMENT_OVERVIEW_AND_RATIONALE.md | Index of every current successor artifact | Founder / fresh reviewer / applicable control owner |
| ENGINEERING_WORK_PACKAGE_REGISTER.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| EVIDENCE_MANIFEST.json | Machine-readable package or evidence record | Founder / fresh reviewer / applicable control owner |
| FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md | Adaptive-onboarding refinement and cross-artifact evidence | Founder / fresh reviewer / applicable control owner |
| FAC_FD_017_CROSS_ARTIFACT_REVIEW.csv | Adaptive-onboarding refinement and cross-artifact evidence | Founder / fresh reviewer / applicable control owner |
| FINAL_DISPOSITION.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_BRIEF.md | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_GATE_STATUS_REGISTER.csv | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_INCORPORATION_REGISTER.csv | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_INCORPORATION_SUMMARY.md | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_RECOMMENDATION_MATRIX.json | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_DECISION_REGISTER.md | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| FOUNDER_INPUT_QUESTIONS.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FOUNDER_INPUT_QUESTION_REGISTER.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| FOUNDER_REVIEW_PACKET.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FRESH_SEGREGATED_REVIEW_EVIDENCE_INDEX.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| FRESH_SEGREGATED_REVIEW_FINDINGS.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| FRESH_SEGREGATED_REVIEW_REPORT.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FROZEN_PREDECESSOR_INTEGRITY_REPORT.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FROZEN_REVISED_CANDIDATE_MANIFEST.txt | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| FROZEN_REVISED_CANDIDATE_SHA256SUMS.txt | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| GOLDEN_PATHS.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| INHERITANCE_AND_SHARED_CONTROL_REGISTER.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| INTERNAL_CONSISTENCY_VALIDATION_REPORT.md | Documentary traceability or consistency validation | Founder / fresh reviewer / applicable control owner |
| PACKAGE_MANIFEST.json | Machine-readable package or evidence record | Founder / fresh reviewer / applicable control owner |
| PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json | Machine-readable package or evidence record | Founder / fresh reviewer / applicable control owner |
| PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| REQUIREMENT_REGISTER.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| RESIDUAL_P2_STATUS.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| RISK_FINDING_DEVIATION_REGISTER.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| SOURCE_REGISTER.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| STARTUP_VERIFICATION_EVIDENCE.json | Machine-readable package or evidence record | Founder / fresh reviewer / applicable control owner |
| STARTUP_VERIFICATION_EVIDENCE.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| STATE_TRANSITION_MATRIX.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| TEST_MATRIX.csv | Machine-readable governance register or matrix | Founder / fresh reviewer / applicable control owner |
| TRACEABILITY_VALIDATION_REPORT.md | Documentary traceability or consistency validation | Founder / fresh reviewer / applicable control owner |
| WORKFLOW_REGISTER.md | Human-readable design, review, risk, evidence, or control artifact | Founder / fresh reviewer / applicable control owner |
| build_founder_decision_incorporation.py | Reproducible documentary builder/validator; no product implementation | Founder / fresh reviewer / applicable control owner |
| freeze_revised_candidate.py | Reproducible documentary builder/validator; no product implementation | Founder / fresh reviewer / applicable control owner |
| source_evidence/FOUNDER_DECISION_INCORPORATION_DIRECTIVE.md | Founder authority, incorporation, gate, or briefing evidence | Founder / fresh reviewer / applicable control owner |
| validate_founder_decision_incorporation.py | Reproducible documentary builder/validator; no product implementation | Founder / fresh reviewer / applicable control owner |

Predecessor evidence is preserved under `predecessor_evidence/v1.0.0/` and remains explicitly non-controlling for V1.1.0 decisions.
