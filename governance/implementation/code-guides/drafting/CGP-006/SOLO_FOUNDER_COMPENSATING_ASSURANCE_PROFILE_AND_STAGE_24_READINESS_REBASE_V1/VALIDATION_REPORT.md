# Validation Report

**Directive ID:** `CGP_006_SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_DIRECTIVE_V1_0_0`
**Validation status:** `PASS_WITH_LEGACY_VALIDATOR_SCOPE_NOTE`

## Package Validator Scope

The validator checks controlling determination hash and byte length, adopted guide bytes, approved tooling-intent source hashes and byte lengths, source-freeze hashes, required files, required continuing disclosures, tooling approval boundaries, non-independence wording, domain-review completion integrity, finding/warning/GAP closure boundaries, activation and implementation non-authorization, package-only path control, manifest integrity, checksum integrity, JSON parsing, and CSV parsing.

## Expected Command Set

- `python3 governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1/validators/validate_solo_founder_assurance_stage24_readiness.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1/tests/test_solo_founder_assurance_stage24_readiness.py`
- `python3 governance/implementation/code-guides/validation/validate_portfolio_consistency.py`
- `python3 governance/implementation/code-guides/validation/validate_repository_authority_alignment.py`
- `python3 governance/implementation/code-guides/validation/validate_activation_records.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest governance/implementation/code-guides/validation/tests/test_wave1_current_status_custody_table.py`
- `python3 -m json.tool SOURCE_FREEZE_MANIFEST.json`
- CSV parser sweep for package CSVs
- checksum verification
- authorized-path verification
- `git diff --check`

## Current Boundary Results

- Guide activation status: `NOT_ACTIVE`
- Implementation mapping status: `NOT_AUTHORIZED`
- Implementation status: `NOT_AUTHORIZED`
- Deployment status: `NOT_AUTHORIZED`
- Pilot status: `NOT_AUTHORIZED`
- Founder residual-risk acceptance: `PENDING_FOUNDER_DECISION`

## Executed Validation Results

| Check | Result |
| --- | --- |
| Package-local validator | `PASS` |
| Package-local tests | `PASS_38_TESTS` |
| Portfolio consistency | `PASS` |
| Repository authority alignment | `PASS` |
| Activation-record validation | `PASS` |
| Current Wave 1 custody/status tests | `PASS` |
| Controlled values schema parse | `PASS` |
| Package JSON and CSV parse sweep | `PASS` |
| Approved tooling source hash and byte-length verification | `PASS_7_APPROVED_SOURCES` |
| Source SHA-256 ledger verification | `PASS_57_SOURCE_ENTRIES` |
| Package checksum manifest verification | `PASS_41_CHECKSUM_ENTRIES` |
| Authorized path verification | `PASS_42_PACKAGE_FILES_ONLY` |
| `git diff --check` | `PASS` |

## Founder-Approved Multi-Agent Tooling Intent Validation

`MULTI_AGENT_TOOLING_INTENT_FOUNDER_APPROVED`

`FOUNDER_APPROVAL_DATE_2026_07_30`

`APPROVED_SHA256_VALUES_RECORDED`

`APPROVED_BYTE_LENGTHS_RECORDED`

`NO_SUBSTITUTED_SOURCE_AUTHORIZED`

`TOOLING_INTENT_IS_NON_VENDOR_LOCKED`

`NAMED_TOOLS_NOT_REQUIRED_FOR_LIMITED_STAGE_24_ACTIVATION`

`NO_EXTERNAL_TOOL_SETUP_AUTHORIZED_BY_THIS_DISPOSITION`

`PR_59_REMAINS_DRAFT_UNMERGED`

The package validator and tests cover missing or altered approved source files,
candidate or pending-approval overclaims, external-tool setup authority,
mandatory named-tool claims, Cursor Background Agent overreach, Claude Code write
authority, Google Jules present implementation authority, unvalidated agent
findings, agent self-approval or self-merge, path-scope violations, guide
activation, implementation mapping, implementation, deployment, pilot,
production, PR-ready markers, and second-PR markers.

## Legacy Validator Scope Note

`run_all_validations.py` was attempted and stopped after entering legacy repository-wide hash and source-accession work. `validate_code_guide_structure.py` reports pre-existing CGP-002 placeholder-rule failures for Wave 1 guides that are now adopted and repository-accessioned under later V1.1 authority. Those legacy checks were not used to amend this package and are not treated as current package validation failures.

## Continuing Statements

`PROGRAM_PLAN_V1_1_CONTROLLING`

`SOLO_FOUNDER_COMPENSATING_ASSURANCE_DETERMINATION_CONTROLLING`

`FOUNDER_SOLO_COMPENSATING_ASSURANCE_MODEL_APPLIES`

`EQUINESYNC_IS_A_SOLO_FOUNDER_PROJECT`

`FOUNDER_DOMAIN_OWNER_REVIEW_IS_NOT_INDEPENDENT`

`FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_IS_NOT_INDEPENDENT`

`MACHINE_ASSISTED_REVIEW_IS_NOT_INDEPENDENT_HUMAN_REVIEW`

`NO_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PERFORMED`

`NO_THIRD_PARTY_TECHNICAL_CERTIFICATION_CLAIMED`

`NO_THIRD_PARTY_DOMAIN_CERTIFICATION_CLAIMED`

`OBJECTIVE_TEST_AND_EVIDENCE_GATES_REQUIRED`

`FOUNDER_RESIDUAL_RISK_ACCEPTANCE_REQUIRED`

`GAP_0004_REMAINS_OPEN`

`NO_SILENT_FINDING_CLOSURE`

`NO_SILENT_WARNING_CLOSURE`

`NO_SILENT_CONDITION_CLOSURE`

`STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED`

`ES_CG_00_REMAINS_NOT_ACTIVE`

`ES_CG_01_REMAINS_NOT_ACTIVE`

`ES_CG_10_REMAINS_NOT_ACTIVE`

`ES_CG_13_REMAINS_NOT_ACTIVE`

`NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED`

`REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`

`IMPLEMENTATION_NOT_AUTHORIZED`

`DEPLOYMENT_NOT_AUTHORIZED`

`PILOT_NOT_AUTHORIZED`

`PRODUCTION_NOT_AUTHORIZED`

`WAVE_2_NOT_AUTHORIZED`

`CGP_007_NOT_AUTHORIZED`

`DRAFT_PR_OPEN_UNMERGED_PENDING_FOUNDER_STAGE_24_DISPOSITION`
