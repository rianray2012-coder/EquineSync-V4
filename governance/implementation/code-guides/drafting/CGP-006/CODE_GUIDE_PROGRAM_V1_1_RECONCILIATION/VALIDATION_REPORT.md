# Validation Report

Updated: 2026-07-28T13:54:11Z

## Local Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION/validators/validate_code_guide_program_v1_1_reconciliation.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION/tests
git diff --check HEAD^ HEAD -- governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION
```

## Expected Result

All package-local checks must pass before this branch is pushed and PR #47 is prepared for protected review and merge.

## Validation Scope

The validator checks package contents, package checksums, required continuing statements, absence of outdated pre-disposition statements, source hash and size, repository baseline scope, guide tracker non-activation boundary, PR #44 successor treatment, and package-only path scope.

## Continuing Boundary

- `GUIDE_ACTIVATION_NOT_AUTHORIZED`
- `IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`
- `IMPLEMENTATION_NOT_AUTHORIZED`
- `DEPLOYMENT_NOT_AUTHORIZED`
- `PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED`
- `GAP_0004_REMAINS_OPEN`
- `RETAINED_WARNINGS_REMAIN_OPEN`
- `ACTIVATION_BLOCKERS_REMAIN_OPEN`
- `NO_ADOPTED_GUIDE_BYTES_CHANGED`
- `NO_RUNTIME_IMPLEMENTATION_OCCURRED`
