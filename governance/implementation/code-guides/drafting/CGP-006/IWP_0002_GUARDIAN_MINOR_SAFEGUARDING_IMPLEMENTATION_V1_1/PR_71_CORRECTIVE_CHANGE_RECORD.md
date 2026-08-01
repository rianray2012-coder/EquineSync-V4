# PR #71 Corrective Change Record

Status: `CORRECTIVE_REVISION_IN_PROGRESS`

Corrective scope remains limited to PR #71 and the authorized CGP-006 IWP-0002 V1.1 implementation/evidence files.

## Code Corrections

- `backend/core/minor_safety.py`: added student/workflow and workflow-level consent scope matching, retained exact existing-resource scope matching, and normalized legacy `guardian_links.barn_id` handling to fail closed unless barn proof is present.
- `backend/core/minor_communication.py`: resolves omitted message participants through student-profile fields, rider rows, and active guardian links before applying per-minor guardian coverage.
- `backend/routes/operations.py`: preserves unknown-age rider subjects, suppresses duplicate synthetic subjects when an explicit canonical student profile controls the workflow, uses stable create scopes, stores guard state tokens, and revalidates event approval transitions.
- `backend/routes/billing.py`: resolves payment subjects through explicit student, rider, horse-to-rider, owner/student, and guardian-link relationships; uses stable billing/student scopes; stores and enforces guard state tokens.
- `backend/routes/recurring_charges.py`: applies the same payment-subject and state-token model to create, update, and materialization.
- `backend/routes/document_signatures.py`: preserves the resolved document-bypass fix and adds persisted expected-state-token enforcement for guarded document create and sandbox-envelope transitions.
- `backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py`: preserves original `GMS-T-001` through `GMS-T-043` and adds corrective tests `GMS-T-044` through `GMS-T-054`.

## Boundaries

No deployment, staging, pilot, production activation, provider call, production-data access, direct protected-branch push, repository-ruleset change, unrelated PR mutation, GAP_0004 closure, Wave 2, or CGP-007 work was performed.
