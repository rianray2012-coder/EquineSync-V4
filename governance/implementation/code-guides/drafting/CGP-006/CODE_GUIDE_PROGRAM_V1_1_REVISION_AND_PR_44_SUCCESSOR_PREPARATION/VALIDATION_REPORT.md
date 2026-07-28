# Validation Report

Required validation commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/validation/validate_code_guide_v1_1_program_revision.py
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/validation/validate_activation_records.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/validation/tests -p 'test_code_guide_v1_1_program_revision.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/validation/tests -p 'test_validate_activation_records.py'
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION/validators/validate_revision_package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION/tests
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR/validators/validate_wave1_successor_package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR/tests
git diff --check HEAD^ HEAD -- governance/implementation/code-guides
```

Every mandatory validation must return `PASS` before the draft PR is opened.
