# Facility V0.2 Validation Report

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V0.2-CONFORMANCE-CANDIDATE`  
**Validation type:** `DETERMINISTIC_DOCUMENTARY_STRUCTURE_AND_CROSS_REFERENCE_VALIDATION`  
**Result:** `PASS_WITH_DISCLOSED_SUBORDINATE_VALIDATOR_CONFLICT`  
**Independent review:** `NOT_STARTED_PERMISSION_GATE_FAILED`  
**Implementation authority:** `FALSE`

## Canonical V1.1 validation

`validate_facility_conformance.py` passed:

- 43 exact, ordered Part II headings from the adopted Master PIA Standard V1.1 PDF;
- five exact active readiness questions using the Founder-directed term `MIAP`;
- 19 source rows, including 16 repository-file hashes independently recomputed as exact matches;
- 55 unique requirements;
- 55 unique acceptance criteria with valid requirement references;
- 85 unique design tests with valid requirement references;
- 43 section trace rows;
- five allowed readiness-answer values with rationales and disclosed blockers;
- two Founder recommendations explicitly marked `RECOMMENDED_NOT_APPROVED`; and
- explicit denial of implementation authority.

## Authenticated creation-kit validator

The authenticated V1.0.0 creation-kit validator returned `FAIL` for three headings:

1. it expects `Purpose and Intended Outcome` instead of canonical `Purpose, Outcomes, and Success Measures`;
2. it expects `Scope, Boundaries, and Release Applicability` instead of canonical `Scope, Boundaries, and Ownership`; and
3. it expects `Founder Decisions Required` in section 35 instead of canonical `Enrollment and Onboarding Readiness`.

The kit Markdown template and validator are subordinate working derivatives. Renaming the controlling PDF headings to satisfy them would violate source precedence. The exact mismatch is therefore preserved as a disclosed validation conflict, not silently normalized.

## Limits

This pass is mechanical and documentary. It does not verify code, schema, migrations, environments, integrations, operations, recovery, deployment, enrollment, or current application behavior. It is not an ES-RA role output and cannot close any carried review finding. A fresh frozen review package in a qualified runtime remains mandatory.

`FACILITY_V0_2_DOCUMENTARY_VALIDATION_PASS_FRESH_REVIEW_REQUIRED`
