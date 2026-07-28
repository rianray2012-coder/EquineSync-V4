# Validation Report

Generated: 2026-07-28T13:18:07Z

## Local Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION/validators/validate_code_guide_program_v1_1_reconciliation.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION/tests
git diff --check HEAD^ HEAD -- governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION
```

## Expected Result

All package-local checks must pass before this branch is pushed as a draft reconciliation PR.

## Validation Scope

The validator checks package contents, package checksums, required closing statements, source hash and size, repository baseline, guide tracker non-activation boundary, PR #44 impact statement, and package-only path scope.

## Non-Validation Scope

This validation does not validate PR #44, activate any guide, verify implementation conformance, deploy software, authorize pilot or production use, or close retained warnings.
