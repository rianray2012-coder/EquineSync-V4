# EquineSync Code Implementation Guide Program

**Current foundation prompt:** `CGP-002`
**Execution ID:** `CGEXEC-20260726-0001`
**Next prompt after CGP-002 return:** `CGP-003`
**Current controlling program-plan accession:** `ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1`

This directory is the canonical documentary and machine-readable home for the EquineSync Code Implementation Guide program.

## Foundation Components

- `schemas/CODE_GUIDE_CONTROLLED_VALUES.json` is the canonical controlled-value source.
- `schemas/` contains versioned JSON schema definitions for guides, controls, invariants, questions, dependencies, traceability, profiles, evidence, exceptions, and findings.
- `templates/` contains reusable generic templates for future guide work.
- `validation/` contains deterministic validators, fixtures, tests, and the portfolio entrypoint.
- `registers/` stores trackers, logs, dependency records, evidence records, findings, decisions, exceptions, supersession records, and session receipts.
- `reviews/`, `receipts/`, and `packages/` preserve validation, custody, and package records.

No official Code Guide program work exists without a prompt ID, execution ID, artifact inventory row, and receipt.

## Program Plan V1.1

The Founder-approved V1.1 Code Implementation Guide Creation, Review, and Assurance Plan is accessioned at:

`program-plan/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1.md`

Founder approval status:

`APPROVED_AS_CONTROLLING_DOCUMENTARY_PROGRAM_PLAN_PENDING_PROTECTED_REPOSITORY_ACCESSION_AND_CUSTODY`

Authority effect is controlling only after protected repository accession and separate post-merge custody are complete. The V1.1 plan does not authorize guide activation, implementation mapping, implementation, deployment, pilot use, production use, first-user enrollment, or runtime evidence by plan approval alone.

## Wave 1 Adoption Authority

PR #42 and adoption record `CGP006-W1-CAR-0001` are preserved as historical pre-V1.1 conditional-adoption authority. Under the current V1.1 program plan, that historical conditional adoption is not carried forward as V1.1 Stage 22 adoption evidence.

Founder Stage 22 documentary adoption is now approved for exact reviewed PR #54 bytes for `ES-CG-00`, `ES-CG-01`, `ES-CG-10`, and `ES-CG-13`. Stage 23 protected repository accession is authorized through PR #54 protected integration and remains pending separate custody until the custody receipt is protectedly merged. All four guides remain `NOT_ACTIVE`.

| guide | adoption | accession | custody | activation |
| --- | --- | --- | --- | --- |
| `ES-CG-00` | `ADOPTED` | `REPOSITORY_ACCESSIONED` | `PENDING_CUSTODY` | `NOT_ACTIVE` |
| `ES-CG-01` | `ADOPTED` | `REPOSITORY_ACCESSIONED` | `PENDING_CUSTODY` | `NOT_ACTIVE` |
| `ES-CG-10` | `ADOPTED` | `REPOSITORY_ACCESSIONED` | `PENDING_CUSTODY` | `NOT_ACTIVE` |
| `ES-CG-13` | `ADOPTED` | `REPOSITORY_ACCESSIONED` | `PENDING_CUSTODY` | `NOT_ACTIVE` |


`PROGRAM_PLAN_V1_1_CONTROLLING`
`ADOPTION_AUTHORITY_RECONCILIATION_CUSTODY_COMPLETE`
`PR_42_HISTORICAL_CONDITIONAL_ADOPTION_PRESERVED`
`PR_42_CONDITIONAL_ADOPTION_NOT_CARRIED_FORWARD_AS_V1_1_STAGE_22_ADOPTION`
`WAVE_1_V1_1_STAGE_22_ADOPTION_APPROVED`
`ES_CG_00_ADOPTED`
`ES_CG_01_ADOPTED`
`ES_CG_10_ADOPTED`
`ES_CG_13_ADOPTED`
`STAGE_23_PROTECTED_REPOSITORY_ACCESSION_AUTHORIZED`
`INDEPENDENT_TECHNICAL_REVIEW_RETAINED_AS_PRE_ACTIVATION_CONDITION`
`HUMAN_DOMAIN_EXPERT_REVIEW_RETAINED_AS_PRE_ACTIVATION_CONDITION`
`GAP_0004_REMAINS_OPEN`
`RETAINED_CONDITIONS_REMAIN_OPEN`
`RETAINED_WARNINGS_REMAIN_OPEN`
`ACTIVATION_BLOCKERS_REMAIN_OPEN`
`STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED`
`NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED`
`REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`
`IMPLEMENTATION_NOT_AUTHORIZED`
`DEPLOYMENT_NOT_AUTHORIZED`
`PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED`
`NO_ADOPTED_GUIDE_BYTES_CHANGED_AFTER_FOUNDER_REVIEW`
`NO_RUNTIME_IMPLEMENTATION_OCCURRED`
`WAVE_2_NOT_AUTHORIZED`
`CGP_007_NOT_AUTHORIZED`

## Boundary

CGP-002 establishes shared machinery only. It does not create substantive Code Guide controls, product policy, implementation authority, deployment authority, pilot authority, production authority, financial authority, messaging/community authority, AI authority, moderation authority, archival migration authority, or enrollment authority.
