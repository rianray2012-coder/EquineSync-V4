
# CGP-006 Wave 1 Candidate Validation Report

**Package:** `ES-CGP-006-WAVE-1-CANDIDATE-DRAFTING-V1`
**Validation status:** `PASS`
**Validator:** `governance/implementation/code-guides/validation/validate_cgp006_wave1_candidate_drafting.py`
**Validator tests:** `governance/implementation/code-guides/validation/tests/test_cgp006_wave1_candidate_drafting.py`

## Required Validator Coverage

- Repository and authorized path scope: `COVERED`
- Guide status: `COVERED`
- Source integrity: `COVERED`
- Requirement support: `COVERED`
- Warning and gap treatment: `COVERED`
- Cross-guide dependency: `COVERED`
- Identifier uniqueness: `COVERED`
- Authority prohibition: `COVERED`
- Checksum ledger: `COVERED`

## Local Validator Result

`validate_cgp006_wave1_candidate_drafting.py --json: PASS; changed_paths_checked=39; controls=22; invariants=22; mandatory_questions=32; normative_rows=139; reference_use_rows=2511; context_use_rows=51; warnings=5; gaps=4`

## Local Validator Test Result

`PASS` - `python3 -m unittest governance.implementation.code-guides.validation.tests.test_cgp006_wave1_candidate_drafting: 2 tests OK`

## Result Interpretation Boundary

A validation pass means the documentary candidate package satisfies the bounded
drafting checks. It does not adopt, activate, merge, implement, deploy, promote
sources, issue CGP-007, or close retained warnings or gaps.
