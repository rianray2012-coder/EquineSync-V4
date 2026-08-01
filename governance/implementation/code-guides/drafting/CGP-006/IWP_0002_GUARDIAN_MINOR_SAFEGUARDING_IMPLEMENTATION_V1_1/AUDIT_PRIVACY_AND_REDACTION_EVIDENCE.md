# Audit Privacy And Redaction Evidence

Status: `IMPLEMENTED_AND_TESTED`

Public API errors use generic stable codes such as `STUDENT_WORKFLOW_BLOCKED`, `COMMUNICATION_BLOCKED`, `DOCUMENT_ACTION_BLOCKED`, and `PAYMENT_ACTION_BLOCKED`. Internal audit metadata is projected through `audit_safe_guardian_minor_metadata` and retains reason codes without names, birthdates, message bodies, legal text, or payment details.

Evidence:
- `GMS-T-037`: public error minimizes relationship-state detail.
- `GMS-T-038`: audit metadata excludes private minor content, legal text, and payment details.
- `EXTERNAL_ERROR_AND_INTERNAL_AUDIT_CODE_MAP.csv`: public/internal mapping recorded.
