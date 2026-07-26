# CGP-002 Validator Test Coverage

**Prompt ID:** `CGP-002`  
**Execution ID:** `CGEXEC-20260726-0001`  
**Package ID:** `ES-CGP-002-FOUNDATION-2026-07-26`

## Coverage Summary

CGP-002 provides deliberate validator coverage through:

- `test_positive_fixtures_pass_for_applicable_validators`
- `test_negative_register_fixtures_fail_for_specific_reasons`
- `test_malformed_csv_fixture_fails`
- `test_malformed_json_fixture_fails`
- `test_missing_evidence_artifact_fails`
- `test_placeholder_falsely_adopted_fails_portfolio_rule`
- `test_package_integrity_negative_fixtures_fail`
- `test_schema_fixtures_parse_and_validate_controlled_values`
- `test_validators_emit_json_and_are_not_placeholders`

The nine test functions are deliberate coverage. They exercise applicable positive fixtures, required rejection cases, parser failure paths, package-integrity failures, portfolio placeholder/adoption boundaries, schema fixture parsing, and validator implementation smoke checks. They are not incidental execution only.

## Validator Coverage Matrix

| Validator | Positive coverage | Negative coverage | Fixture or test identifier | Current applicable state | Retained limitation |
|---|---|---|---|---|---|
| `code-guide-structure` | Current portfolio structure is exercised by `run_all_validations.py` and `test_validators_emit_json_and_are_not_placeholders`. | Substantive negative structure mutation is reserved until later guide artifacts exist. | Current guide placeholders; `test_validators_emit_json_and_are_not_placeholders`. | `PASS` | Negative testing beyond implementation smoke is deferred because CGP-002 must not create completed or malformed guide content. |
| `control-registry` | `control_register_valid.csv` passes. | Duplicate control ID, missing governing authority, invalid assurance class, invalid evidence grade, missing activation boundary, missing high-risk negative test, and unrecognized controlled value all fail deliberately. | `test_positive_fixtures_pass_for_applicable_validators`; `test_negative_register_fixtures_fail_for_specific_reasons`. | `NOT_YET_APPLICABLE` for live register because no substantive controls exist. | Live register remains empty by authority boundary. |
| `invariant-registry` | `invariant_register_valid.csv` passes. | Duplicate invariant ID and missing verification method fail deliberately. | `test_positive_fixtures_pass_for_applicable_validators`; `test_negative_register_fixtures_fail_for_specific_reasons`. | `NOT_YET_APPLICABLE` for live register because no substantive invariants exist. | Live register remains empty by authority boundary. |
| `guide-questions` | `guide_questions_valid.csv` passes. | Unanswered required question fails deliberately. | `test_positive_fixtures_pass_for_applicable_validators`; `test_negative_register_fixtures_fail_for_specific_reasons`. | `NOT_YET_APPLICABLE` for live register because guide question answering is not authorized. | Live register remains empty by authority boundary. |
| `guide-dependencies` | `dependency_valid.csv` passes and live program dependencies pass. | Broken guide dependency, circular dependency, and superseded control without compatibility treatment fail deliberately. | `test_positive_fixtures_pass_for_applicable_validators`; `test_negative_register_fixtures_fail_for_specific_reasons`. | `PASS` | No substantive control dependencies are created. |
| `atlas-traceability` | Implementation smoke confirms validator executes and returns a controlled state. | Substantive negative atlas mapping is reserved until atlas-to-guide mapping is authorized. | `test_validators_emit_json_and_are_not_placeholders`. | `NOT_YET_APPLICABLE` | Live register remains empty; CGP-002 cannot create atlas mappings. |
| `repository-mapping` | Implementation smoke confirms validator executes and returns a controlled state. | Substantive negative repository mapping is reserved until repository-to-control mapping is authorized. | `test_validators_emit_json_and_are_not_placeholders`. | `NOT_YET_APPLICABLE` | Live register remains empty; CGP-002 cannot create repository mappings. |
| `control-verification` | Implementation smoke confirms validator executes and returns a controlled state. | Substantive negative verification coverage is reserved until controls and verification records exist. | `test_validators_emit_json_and_are_not_placeholders`. | `NOT_YET_APPLICABLE` | Live register remains empty; CGP-002 cannot create control verifications. |
| `implementation-profiles` | Implementation smoke confirms validator executes and returns a controlled state. | Substantive negative profile coverage is reserved until implementation profiles are authorized. | `test_validators_emit_json_and_are_not_placeholders`. | `NOT_YET_APPLICABLE` | No profile JSON files are authorized under CGP-002. |
| `evidence-records` | `evidence_valid.csv` provides valid fixture coverage through fixture data and parser coverage. | Missing evidence artifact fails deliberately. | `test_missing_evidence_artifact_fails`; `csv_parse` validation command. | `NOT_YET_APPLICABLE` for live register because implementation evidence is not authorized. | Live register remains empty by authority boundary. |
| `exceptions` | `exceptions_valid.csv` passes. | Expired exception fails deliberately. | `test_positive_fixtures_pass_for_applicable_validators`; `test_negative_register_fixtures_fail_for_specific_reasons`. | `NOT_YET_APPLICABLE` for live register because implementation exceptions are not authorized. | Live register remains empty by authority boundary. |
| `supersession` | Implementation smoke confirms validator executes and returns a controlled state. | Substantive negative supersession coverage is reserved until guide versions or control supersession records exist. | `test_validators_emit_json_and_are_not_placeholders`. | `NOT_YET_APPLICABLE` | Live register remains empty; no guide adoption or supersession is authorized. |
| `package-integrity` | Live package integrity passes. | Checksum mismatch and manifest omission package fixtures fail deliberately. | `validate_package_integrity.py --json`; `test_package_integrity_negative_fixtures_fail`. | `PASS` | None for CGP-002 package integrity. |
| `portfolio-consistency` | Live portfolio consistency passes. | Adopted guide without repository accession fails deliberately. | `run_all_validations.py --json`; `test_placeholder_falsely_adopted_fails_portfolio_rule`. | `PASS` | Future substantive guide adoption checks remain reserved until later prompts. |

## Disposition

Every validator has deliberate execution coverage. Validators with live `NOT_YET_APPLICABLE` status have documented limitations tied to CGP-002 authority boundaries, not missing implementation.

`VALIDATOR_TEST_COVERAGE_RECONCILED`

