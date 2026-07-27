# CGP-006 Output Register

**Prompt ID:** `CGP-006`
**Execution ID:** `CGEXEC-20260726-0005`
**Package ID:** `ES-CGP-006-CONTROLLED-INITIATION-2026-07-26`

| Output ID | Artifact | Type | Required | Status | Purpose |
| --- | --- | --- | --- | --- | --- |
| CGP006-OUT-0001 | CGP_006_INITIATION_ASSESSMENT.md | DOCUMENTARY_ASSESSMENT | REQUIRED | FOUNDER_DISPOSITION_RECORDED | Defines discovered authority, approved bounded function, inputs, decisions, risks, validations, lifecycle, and boundaries. |
| CGP006-OUT-0002 | CGP_006_PR23_CONFLICT_ASSESSMENT.md | CONFLICT_ASSESSMENT | REQUIRED | PASS | Records PR23_REVIEWED_NON_CONFLICTING_WITH_CGP_BASELINE. |
| CGP006-OUT-0003 | CGP_006_SCOPE_AND_BOUNDARY.md | SCOPE_BOUNDARY | REQUIRED | FOUNDER_DISPOSITION_RECORDED | Frames approved bounded CGP-006 scope without adoption or activation. |
| CGP006-OUT-0004 | CGP_006_INPUT_REGISTER.md | INPUT_REGISTER | REQUIRED | COMPLETE | Lists aggregate and normative source inputs under two-layer model. |
| CGP006-OUT-0005 | CGP_006_OUTPUT_REGISTER.md | OUTPUT_REGISTER | REQUIRED | COMPLETE | Lists candidate package outputs. |
| CGP006-OUT-0006 | CGP_006_FOUNDER_DECISION_REGISTER.md | DECISION_REGISTER | REQUIRED | FOUNDER_APPROVED | Records the six Founder-approved decisions required before bounded candidate drafting or lifecycle changes. |
| CGP006-OUT-0007 | CGP_006_RISK_FINDING_DEVIATION_REGISTER.csv | RISK_REGISTER | REQUIRED | COMPLETE_WITH_RETAINED_FINDINGS | Records risks and retained conditions. |
| CGP006-OUT-0008 | CGP_006_VALIDATION_PLAN.md | VALIDATION_PLAN | REQUIRED | UPDATED_FOR_CLASSIFICATION_GATE | Defines gates and validator statuses. |
| CGP006-OUT-0009 | CGP_006_REPOSITORY_LIFECYCLE_PLAN.md | LIFECYCLE_PLAN | REQUIRED | APPROVED_FOR_PROTECTED_INTEGRATION | Defines branch, PR, receipt, and self-reference-safe lifecycle. |
| CGP006-OUT-0010 | CGP_006_AUTHORITY_BOUNDARY.md | AUTHORITY_BOUNDARY | REQUIRED | COMPLETE | Preserves non-authorization boundaries. |
| CGP006-OUT-0011 | CGP_006_PACKAGE_MANIFEST.json | MANIFEST | REQUIRED | GENERATED | Machine-readable file inventory. |
| CGP006-OUT-0012 | CGP_006_CHECKSUMS.sha256 | CHECKSUM_LEDGER | REQUIRED | GENERATED | SHA-256 ledger excluding itself. |
| CGP006-OUT-0013 | validate_cgp006_initiation.py | VALIDATOR | REQUIRED | IMPLEMENTED | Standalone documentary-safe package validator. |

No listed output is a substantive guide, adoption record, activation record, implementation profile, application change, CI product gate, deployment record, provider activation, pilot authorization, production authorization, financial activation, messaging or moderation activation, AI activation, archival authority, or enrollment authority.
