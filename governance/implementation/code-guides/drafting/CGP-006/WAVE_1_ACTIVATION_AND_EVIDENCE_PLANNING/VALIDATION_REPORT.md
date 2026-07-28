
# CGP-006 Wave 1 Validation Report

**Validation result:** `PASS`
**Generated at:** `2026-07-28T06:01:43Z`
**Python version:** `Python 3.14.6`
**Git version:** `git version 2.50.1 (Apple Git-155)`
**GitHub CLI version:** `gh version 2.96.0 (2026-07-02)`

## Inputs Reviewed

- `governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/`
- `governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/`
- `governance/implementation/code-guides/drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1/`
- `governance/implementation/code-guides/drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1/`
- `governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md`
- `governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION.md`
- GitHub PR `#42`
- GitHub PR `#43`
- Base branch `integrate-emergent-final-zip` at `2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94`

## Commands Recorded

| Command | Recorded Result |
| --- | --- |
| python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/validators/validate_activation_readiness_package.py | PASS |
| python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/tests/test_activation_readiness_package.py | PASS |
| shasum -a 256 -c governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/CHECKSUM_MANIFEST.sha256 | PASS |
| git diff --check | PASS |
| python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/validators/validate_activation_readiness_package.py --require-draft-pr | PENDING_DRAFT_PR_CREATION |

## Validator Coverage

The package-specific validator checks required deliverables, manifest completeness, checksum coverage, JSON and CSV parsing, unique identifiers, valid guide references, preserved conditions, preserved open warnings, GAP-0004 open status, non-activation statements, non-implementation-mapping boundaries, evidence status values, proposed Founder decision status, mandatory review question coverage, source-integrity preservation, package status consistency, draft PR state when requested, and `git diff --check`.

## Closing Statements

`ACTIVATION_NOT_AUTHORIZED`
`NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED`
`IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`
`IMPLEMENTATION_NOT_AUTHORIZED`
`GAP_0004_REMAINS_OPEN`
`RETAINED_WARNINGS_REMAIN_OPEN`
`NO_ADOPTED_SOURCE_BYTES_CHANGED`
`NO_RUNTIME_IMPLEMENTATION_OCCURRED`
`DRAFT_PR_OPEN_UNMERGED`
