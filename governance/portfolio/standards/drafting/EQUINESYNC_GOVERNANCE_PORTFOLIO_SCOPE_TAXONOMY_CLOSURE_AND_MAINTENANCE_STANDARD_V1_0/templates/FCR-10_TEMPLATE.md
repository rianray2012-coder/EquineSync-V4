# FCR-10 Production Authorization Template

Status: `TEMPLATE_ONLY_NO_CERTIFICATION_ISSUED`

Truth statement: `FOUNDER AUTHORITY MAY CHANGE THE REQUIRED INTERNAL GATE OR EVIDENCE SUFFICIENCY DETERMINATION, BUT IT MAY NOT CHANGE HISTORICAL FACT.`

## Required Common Fields

- `certification_id`: REQUIRED_NON_EMPTY
- `class_id`: REQUIRED_NON_EMPTY
- `status`: REQUIRED_NON_EMPTY
- `issued_at`: REQUIRED_NON_EMPTY
- `effective_at`: REQUIRED_NON_EMPTY
- `scope_summary`: REQUIRED_NON_EMPTY
- `artifact_path`: REQUIRED_NON_EMPTY
- `certifying_authority`: REQUIRED_NON_EMPTY
- `second_review`: REQUIRED_NON_EMPTY
- `dependent_claim_effect`: REQUIRED_NON_EMPTY
- `review_trigger`: REQUIRED_NON_EMPTY
- `limitations`: REQUIRED_NON_EMPTY
- `truth_statement`: REQUIRED_NON_EMPTY
- `class_payload`: REQUIRED_NON_EMPTY

## Required Class Payload

- `release_identity`: REQUIRED_NON_EMPTY
- `environment`: REQUIRED_NON_EMPTY
- `feature_scope`: REQUIRED_NON_EMPTY
- `data_scope`: REQUIRED_NON_EMPTY
- `user_scope`: REQUIRED_NON_EMPTY
- `evidence_relied_upon`: REQUIRED_NON_EMPTY
- `unresolved_risk_statement`: REQUIRED_NON_EMPTY
- `exception_attestation`: REQUIRED_NON_EMPTY
- `stop_conditions`: REQUIRED_NON_EMPTY
- `rollback_conditions`: REQUIRED_NON_EMPTY
- `effective_date`: REQUIRED_NON_EMPTY
- `expires_at_or_review_trigger`: REQUIRED_NON_EMPTY
- `second_review`: REQUIRED_NON_EMPTY
- `release_scope_only_statement`: REQUIRED_NON_EMPTY

No permanent waiver, production use, pilot use, adoption, activation, implementation, or certification is issued by this template.
