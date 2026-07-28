# Code Guide Program V1.1 Reconciliation

Generated: 2026-07-28T13:18:07Z

This package reconciles the existing Code Guide Program repository state against the Founder-approved `ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1`.

| Item | Value | Evidence |
| --- | --- | --- |
| Protected baseline | integrate-emergent-final-zip | 6249c2fd79bfef897630855d633d62e830153414 |
| Accession PR | #45 | merged at 77a1565f73cde94acf62d4137360ad7749321f4e |
| Custody PR | #46 | merged at 6249c2fd79bfef897630855d633d62e830153414 |
| Approved V1.1 source | governance/implementation/code-guides/program-plan/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1.md | 9aa8cb29848ccf5b75a65320616a1196060589372bb0de09266fd32f3a9efd35 |
| Founder disposition | governance/implementation/code-guides/program-plan/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1/FOUNDER_APPROVAL_AND_RATIFICATION_DISPOSITION.md | a0ebd84d3acdce0be1c0650c19eab97e10e04ec0ba1b61885fbe0a4d5fcbc47c |
| Reconciliation determination | CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION_COMPLETE_REVISION_PROGRAM_REQUIRED |  |
| PR #44 impact | PR_44_REQUIRES_REBASE_AND_REVALIDATION_UNDER_NEW_CONTROLLING_BASELINE | f94c26188e8d35c413b366135df12057b58c2d7d |

## Determinations

- `CODE_GUIDE_PROGRAM_PLAN_V1_1_PROTECTEDLY_ACCESSIONED_AND_CUSTODY_COMPLETE`
- `CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION_COMPLETE_REVISION_PROGRAM_REQUIRED`
- `PR_44_REQUIRES_REBASE_AND_REVALIDATION_UNDER_NEW_CONTROLLING_BASELINE`

The V1.1 program plan is protectedly accessioned and custody-complete in the repository. The existing Code Guide Program is not yet fully V1.1-aligned and requires a separate authorized revision program before any guide, mapping, activation, implementation, deployment, pilot, or production-use claim may rely on V1.1 conformance.

## Scope Boundary

This package is documentary reconciliation only. It does not modify adopted guide bytes, approve guide activation, authorize implementation mapping, authorize implementation, authorize deployment, authorize pilot or production use, close GAP-0004, close retained warnings, close activation blockers, or approve proposed Founder decisions.

## Current Repository Findings

- Required V1.1 registers present: 13/19.
- Required V1.1 schemas present: 11/13.
- Required V1.1 implementation profiles present: 0/18.
- Required V1.1 templates present: 12/19.
- Required V1.1 validator filenames present: 14/15.
- Current assurance controlled values are `A1_STANDARD, A2_IMPORTANT, A3_HIGH, A4_CRITICAL` and do not exactly match the V1.1 A0-A4 model.
- Current evidence controlled values are `E0_ASSERTION, E1_MANUAL_OBSERVATION, E2_REPRODUCIBLE_LOCAL, E3_INDEPENDENT_CI, E4_CONTROLLED_ENVIRONMENT, E5_PRODUCTION` and do not exactly match the V1.1 E0-E5 model.
- PR #44 remains open, draft, unmerged, and based on `2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94` rather than the current protected V1.1 custody head `6249c2fd79bfef897630855d633d62e830153414`.

## Package Contents

The package includes inventories, crosswalks, status matrices, PR #44 impact assessment, authority boundary report, Founder decision register, successor workstream plan, validation report, validator, tests, package manifest, and checksum manifest.

## Required Closing Statements

- `PROGRAM_PLAN_V1_1_FOUNDER_APPROVED`
- `PROGRAM_PLAN_V1_1_CONTROLLING_ONLY_AFTER_PROTECTED_ACCESSION_AND_CUSTODY`
- `PR_44_REMAINS_OPEN_DRAFT_UNMERGED`
- `GUIDE_ACTIVATION_NOT_AUTHORIZED`
- `IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`
- `IMPLEMENTATION_NOT_AUTHORIZED`
- `DEPLOYMENT_NOT_AUTHORIZED`
- `PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED`
- `GAP_0004_REMAINS_OPEN`
- `RETAINED_WARNINGS_REMAIN_OPEN`
- `ACTIVATION_BLOCKERS_REMAIN_OPEN`
- `PROPOSED_FOUNDER_DECISIONS_REMAIN_UNAPPROVED`
- `NO_ADOPTED_GUIDE_BYTES_CHANGED`
- `NO_RUNTIME_IMPLEMENTATION_OCCURRED`
- `RECONCILIATION_PR_OPEN_DRAFT_UNMERGED`
