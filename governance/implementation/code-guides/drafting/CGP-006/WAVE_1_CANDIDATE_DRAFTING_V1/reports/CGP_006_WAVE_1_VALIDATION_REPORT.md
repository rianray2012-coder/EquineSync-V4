# CGP-006 Wave 1 Candidate Validation Report

**Package:** `ES-CGP-006-WAVE-1-CANDIDATE-DRAFTING-V1`
**Structured Founder review:** `CGP-006-WAVE-1-STRUCTURED-FOUNDER-REVIEW-V1`
**Founder candidate-baseline disposition:** `CGP_006_WAVE_1_CANDIDATE_GUIDES_FOUNDER_APPROVED_WITH_RETAINED_NON_BLOCKING_WARNINGS`
**Validation status:** `PASS`

## Required Validator Coverage

- Repository and authorized path scope: `COVERED`
- Guide status: `COVERED`
- Source integrity: `COVERED`
- Requirement support: `COVERED`
- Warning and gap treatment: `COVERED`
- Cross-guide dependency: `COVERED`
- Identifier uniqueness: `COVERED`
- Authority prohibition: `COVERED`
- Structured Founder-review registers: `COVERED`
- Candidate-baseline approval register: `COVERED`
- Mandatory-question review: `COVERED`
- Duplicate and terminology reconciliation: `COVERED`
- Manifest and checksum ledger: `COVERED`
- CGP-006 classification and initiation validators: `COVERED`
- Legacy source-accession/source-freeze treatment: `COVERED`

## Local Validator Result

Wave 1 validator PASS; Founder-review validator PASS; candidate-baseline approval validator PASS; CGP-006 document classification validator PASS; CGP-006 initiation validator PASS; documentary unit tests PASS; authorized path PASS; manifest/checksum PASS.

## Legacy Validator Treatment

`validate_source_accession.py` and `validate_source_freeze.py` remain recorded as `SUPERSEDED_BY_ACCESSIONED_BASELINE_VALIDATION` for this candidate-baseline approval phase. Repository evidence: the CGP-006 document classification manifest records `repository_accession_state=REPOSITORY_ACCESSIONED`, `source_freeze_amendment=NOT_REQUIRED`, and `approved_cgp005_source_bytes_changed=False`; this approval update changes only candidate package, review, report, manifest, checksum, and Wave 1 validation artifacts and does not alter source-accession files, source-freeze files, classification registers, or approved source bytes.

## GitHub Check State

Before approval update: `ALL_REPORTED_CHECKS_PASS: Backend known-failure non-regression gate; Backend suite is collectable; Frontend build; Vercel; Vercel Preview Comments`.

After approval update: `PENDING_PROTECTED_CHECKS_AFTER_PUSH`.

## Result Interpretation Boundary

A validation pass means the documentary candidate package records Founder approval for controlled candidate-baseline custody. It does not adopt, activate, make effective, implement, deploy, promote sources, issue CGP-007, or close retained warnings or gaps.
