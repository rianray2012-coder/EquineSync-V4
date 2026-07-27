# CGP-006 Document Classification Validation

**Prompt ID:** `CGP-006`
**Package ID:** `ES-CGP-006-DOCUMENT-CLASSIFICATION-GATE-2026-07-27`
**Determination:** `CGP_006_DOCUMENT_CLASSIFICATION_REFRESHED_WITH_NON_BLOCKING_WARNINGS_READY_FOR_FOUNDER_REVIEW`
**Validation artifact updated:** `2026-07-27`

## Validator Coverage

- `validation/validate_cgp006_document_classification.py` validates package completeness, classification values, path resolution, guide-family allocation coverage, 139 normative-row reconciliation, non-normative reference treatment, PR #23 contextual treatment, CGP-005 Technical Audit Appendix contextual treatment, Founder-approved context register coverage, conflict/provenance-gap treatment, tracker state, manifest counts, and checksum-ledger behavior.
- `validation/tests/test_cgp006_document_classification.py` covers the current package pass path and a required-file negative fixture.
- Existing portfolio validation remains in use through `validation/run_all_validations.py`.

## Static Reconciliation Results

- Total classification records: `2701`
- Reference corpus rows kept non-normative: `2511`
- Normative rows reconciled: `139`
- PR #23 contextual records: `10`
- CGP-006 contextual records: `31`
- CGP-005 Technical Audit Appendix contextual records: `10`
- Provenance gaps: `0`
- Blocking conflicts: `0`
- Unclassified pending-review records: `0`
- CGP-006 tracker blocker retained: `DOCUMENT_CLASSIFICATION_GATE`
- CGP-007: `NOT_ISSUED`

## Appendix Validation Results

- All final appendix package artifacts are classified.
- The appendix repository integration receipt is classified.
- Appendix artifacts are `FOUNDER_APPROVED_CONTEXT_NON_NORMATIVE`.
- No appendix artifact is counted as a normative row.
- CGP-005 approved normative source bytes remain unchanged.
- PR #23 remains contextual only.
- Retained gaps remain visible and non-blocking for this refresh.

## Command Evidence

Final local validation commands are recorded in the Codex execution transcript and should include:

- `python3 governance/implementation/code-guides/validation/validate_cgp006_document_classification.py --json`
- `python3 governance/implementation/code-guides/validation/validate_cgp006_initiation.py --json`
- `python3 governance/implementation/code-guides/validation/run_all_validations.py`
- `python3 -m unittest discover -s governance/implementation/code-guides/validation/tests`
- checksum verification for CGP-002, CGP-003, CGP-004, CGP-005, CGP-006 initiation, and CGP-006 classification ledgers

The classification package checksum ledger excludes itself and the classification manifest from self-hashing.
