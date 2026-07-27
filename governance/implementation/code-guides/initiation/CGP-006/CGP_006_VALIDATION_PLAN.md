# CGP-006 Validation Plan

**Prompt ID:** `CGP-006`
**Execution ID:** `CGEXEC-20260726-0005`

## Required Result States

Validation results must use only `PASS`, `FAIL`, `BLOCKED`, `WARNING`, or `NOT_YET_APPLICABLE`. A blocked or not-yet-applicable condition must not be converted into a pass.

## Initiation Package Validators

| Gate | Required status | Validation treatment |
| --- | --- | --- |
| Repository baseline verification | PASS | Remote default head must equal `3eb6825091241709f255b8ccf296987fa9b20724` at branch creation. |
| PR #23 non-conflict determination | PASS | `CGP_006_PR23_CONFLICT_ASSESSMENT.md` must record `PR23_REVIEWED_NON_CONFLICTING_WITH_CGP_BASELINE`. |
| Package completeness | PASS | All required CGP-006 package files must exist. |
| Manifest accuracy | PASS | Manifest paths must be unique, in Code Guide scope, and resolve in the repository. |
| Checksum accuracy | PASS | Checksum ledger must match file bytes and exclude itself from self-hashing. |
| Source classification | PASS | Reference corpus must remain `REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE`; normative crosswalk row count must remain 139. |
| Source-freeze preservation | PASS | Guide source-freeze row counts must remain ES-CG-00=29, ES-CG-01=34, ES-CG-13=45, ES-CG-10=31. |
| Unapproved source promotion | PASS | PR #23 and reference-only rows must not be promoted to normative status. |
| Unapproved adoption | PASS | No Wave 1 guide may change from `NOT_ADOPTED`. |
| Unapproved activation | PASS | No Wave 1 guide may become `ACTIVE`. |
| Founder-decision completeness | PASS | All CGP006-D-* entries must be recorded as `FOUNDER_APPROVED` with exact Founder-approved dispositions. |
| Tracker consistency | PASS | `CGP-005` remains accepted/accessioned and `CGP-006` is issued only for bounded Wave 1 candidate drafting with the document-classification gate required. |
| Classification gate | PASS | No candidate guide drafting may proceed until all proposed Wave 1 sources are classified, all 139 normative rows reconcile, and reference-only/PR #23 materials remain non-normative. |
| Path consistency and bounded diff | PASS | All package changes must remain under `governance/implementation/code-guides/`. |
| Receipt readiness | PASS | Repository lifecycle plan must preserve self-reference-safe receipt treatment. |

## Implemented Validator

`governance/implementation/code-guides/validation/validate_cgp006_initiation.py` validates package completeness, manifest and checksum accuracy, PR #23 conflict outcome, source-freeze preservation, Founder-decision approval status, tracker/adoption/activation boundaries, classification-gate preservation, and path scope.

## Classification And Drafting Validators Required

Before any candidate guide text is drafted, additional validators must check document classification, normative-source preservation, reference-only separation, PR #23 non-normative treatment, guide status markings, guide dependencies, source traceability, manifests, checksums, package completeness, and authority boundaries.

If the classification gate passes and candidate drafting begins, additional validators must check candidate guide draft completeness, control identifier uniqueness, invariant identifier uniqueness, question-answer traceability, normative-source citations, cross-guide dependency order, retained findings, and explicit `NOT_ADOPTED` / `NOT_ACTIVE` / no-implementation markings.
