# CGP-002 Controlled Values

**Machine-readable source:** `schemas/CODE_GUIDE_CONTROLLED_VALUES.json`
**Source prompt:** `CGP-002`

CGP-002 establishes one canonical machine-readable source. Markdown below mirrors that source for reader convenience; validators load the JSON file.

## Guide Maturity States

- `PLANNED`
- `CHARTERED`
- `SOURCE_FROZEN`
- `CURRENT_STATE_ASSESSED`
- `DRAFTING`
- `INTERNAL_REVIEW`
- `TECHNICAL_REVIEW`
- `PRODUCT_REVIEW`
- `CROSS_GUIDE_REVIEW`
- `ADVERSARIAL_REVIEW`
- `SCENARIO_VALIDATED`
- `ASSURANCE_REVIEW`
- `ADOPTION_CANDIDATE`
- `ADOPTED`
- `REPOSITORY_ACCESSIONED`
- `ACTIVE`
- `REVISION_PENDING`
- `SUPERSEDED`
- `RETIRED`
- `BLOCKED`

## Prompt Execution States

- `NOT_ISSUED`
- `ISSUED`
- `IN_PROGRESS`
- `RETURNED`
- `ACCEPTED`
- `REVISION_REQUIRED`
- `BLOCKED`
- `SUPERSEDED`

## Assurance Classes

- `A1_STANDARD`
- `A2_IMPORTANT`
- `A3_HIGH`
- `A4_CRITICAL`

## Evidence Grades

- `E0_ASSERTION`
- `E1_MANUAL_OBSERVATION`
- `E2_REPRODUCIBLE_LOCAL`
- `E3_INDEPENDENT_CI`
- `E4_CONTROLLED_ENVIRONMENT`
- `E5_PRODUCTION`

## Finding Severities

- `P0`
- `P1`
- `P2`
- `P3`

## Applicability And Record States

- `REQUIRED`
- `OPTIONAL`
- `NOT_APPLICABLE`
- `NOT_YET_APPLICABLE`
- `PLANNED`
- `PARTIAL`
- `COMPLETE`
- `VERIFIED`
- `STALE`
- `INVALID`
- `MISSING`

## Task Dispositions

- `COMPLETE_READY_FOR_NEXT_STAGE`
- `COMPLETE_WITH_RETAINED_FINDINGS`
- `PARTIALLY_COMPLETE`
- `BLOCKED_FAIL_CLOSED`
- `REVISION_REQUIRED`

## Adoption Dispositions

- `APPROVED_FOR_CONTROLLED_ADOPTION`
- `APPROVED_WITH_RETAINED_GAPS`
- `REVISION_REQUIRED`
- `BLOCKED_PENDING_DECISION`
- `REJECTED`

## Adoption States

- `NOT_ADOPTED`
- `APPROVED_FOR_CONTROLLED_ADOPTION`
- `APPROVED_WITH_RETAINED_GAPS`
- `REVISION_REQUIRED`
- `BLOCKED_PENDING_DECISION`
- `REJECTED`
- `SUPERSEDED`

## Accession States

- `NOT_ACCESSIONED`
- `ACCESSION_PENDING`
- `REPOSITORY_ACCESSIONED`
- `CUSTODY_GAP`
- `SUPERSEDED`

## Activation States

- `NOT_ACTIVE`
- `ACTIVE`
- `BLOCKED`
- `SUPERSEDED`
- `RETIRED`

## Mapping States

- `IMPLEMENTED`
- `PARTIALLY_IMPLEMENTED`
- `PLANNED`
- `MISSING`
- `CONFLICTING`
- `NOT_APPLICABLE`

## Answer Statuses

- `UNANSWERED`
- `ANSWERED`
- `NOT_APPLICABLE`
- `BLOCKED_PENDING_DECISION`
- `DEFERRED`

## Validator Result Statuses

- `PASS`
- `FAIL`
- `WARNING`
- `NOT_YET_APPLICABLE`
- `BLOCKED`

## Boolean Text

- `YES`
- `NO`

## Verification Polarity

- `POSITIVE`
- `NEGATIVE`

CGP-002 does not authorize new product policy, guide controls, implementation profiles, deployment, adoption, or activation.
## CGP-003 Source Accession Controlled Values

CGP-003 extends the shared controlled values with source accession classes, authority statuses, checksum statuses, custody statuses, source-gap types, source-conflict types, source supersession statuses, and source-to-guide mapping types. The canonical machine-readable source is `schemas/CODE_GUIDE_CONTROLLED_VALUES.json`.

These additions classify source evidence only. They do not adopt external standards, draft guide controls, or activate any guide.
