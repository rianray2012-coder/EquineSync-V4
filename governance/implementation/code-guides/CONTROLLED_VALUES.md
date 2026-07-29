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
- `FOUNDER_APPROVED_FOR_REPOSITORY_INTEGRATION`
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
- `ADOPTED`
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
## CGP-004 Current-State Assessment Controlled Values

CGP-004 extends the shared controlled values with implementation-state, authority-alignment, and confidence vocabularies for repository assessment. These values classify inspected repository evidence only. They do not draft Code Guide controls, create implementation profiles, adopt product policy, or activate engineering gates.

### Repository Implementation States

- `IMPLEMENTED`
- `PARTIALLY_IMPLEMENTED`
- `SCAFFOLDED`
- `STUB`
- `TEST_ONLY`
- `LEGACY_ACTIVE`
- `LEGACY_INACTIVE`
- `DEAD_OR_UNREFERENCED`
- `PROPOSED_IN_DOCUMENTATION_ONLY`
- `MISSING`
- `UNKNOWN`

### Repository Authority Alignment States

- `ALIGNED_WITH_CONTROLLING_AUTHORITY`
- `PARTIALLY_ALIGNED`
- `IMPLEMENTED_BEYOND_DOCUMENTED_AUTHORITY`
- `CONFLICTS_WITH_CONTROLLING_AUTHORITY`
- `AUTHORITY_AMBIGUOUS`
- `NO_AUTHORITY_MAPPING_FOUND`
- `NOT_APPLICABLE`

### Confidence Levels

- `HIGH`
- `MEDIUM`
- `LOW`


## CGP-005 Source-Freeze Controlled Values

CGP-005 extends the shared controlled values with source-freeze inclusion categories and drafting-readiness dispositions. These values classify exact-byte source-freeze and readiness records only. They do not draft Code Guide controls, adopt a guide, activate an engineering gate, or authorize implementation.

### Source Freeze Inclusion Categories

- `CONTROLLING_FROZEN`
- `SUPPORTING_FROZEN`
- `HISTORICAL_FROZEN`
- `IMPLEMENTATION_EVIDENCE_FROZEN`
- `REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE`
- `EXCLUDED_SUPERSEDED`
- `EXCLUDED_PROPOSED`
- `EXCLUDED_BLOCKED`
- `EXCLUDED_OUT_OF_SCOPE`
- `PENDING_AUTHORITY`
- `MISSING_REQUIRED_SOURCE`

### Source Freeze Readiness Dispositions

- `CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW`
- `SOURCE_FREEZE_COMPLETE_READY_FOR_CGP_006_WHEN_AUTHORIZED`
- `SOURCE_FREEZE_COMPLETE_WITH_RETAINED_NON_BLOCKING_GAPS`
- `BLOCKED_BY_SOURCE_CUSTODY`
- `BLOCKED_BY_AUTHORITY_DECISION`
- `NOT_IN_WAVE_1`
