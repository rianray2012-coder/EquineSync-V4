# Validation Report

Required validation commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/validation/validate_activation_records.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/validation/tests -p 'test_validate_activation_records.py'
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/validation/validate_code_guide_v1_1_program_revision.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/validation/tests -p 'test_code_guide_v1_1_program_revision.py'
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION/validators/validate_revision_package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION/tests
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR/validators/validate_wave1_successor_package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR/tests
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_POST_CUSTODY_CLOSEOUT_AND_STATUS_RECONCILIATION/validators/validate_post_custody_closeout.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_POST_CUSTODY_CLOSEOUT_AND_STATUS_RECONCILIATION/tests
git diff --check
```

Mandatory validation requirements:

- protected starting head matches;
- PR #49 lineage matches;
- PR #50 lineage matches;
- PR #44 status and preserved head match;
- no stale current-status record remains in `PROGRAM_STATUS.md`;
- historical statements remain preserved;
- no historical global replacement occurred;
- no guide was activated;
- no activation effective date was created;
- no repository-specific implementation mapping was created;
- no application files changed;
- no adopted guide bytes changed;
- GAP-0004 remains open;
- retained warnings remain open;
- activation blockers remain open;
- CGP-007 remains unauthorized;
- package manifest and checksums verify;
- JSON and CSV files parse;
- authorized-path validation passes;
- `git diff --check` passes.
