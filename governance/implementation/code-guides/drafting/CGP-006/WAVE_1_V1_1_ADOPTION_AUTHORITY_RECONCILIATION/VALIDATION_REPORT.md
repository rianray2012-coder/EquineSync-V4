# Validation Report

Validation commands for this package:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION/validators/validate_adoption_authority_reconciliation.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION/tests
git diff --check 513458bd9f0f6b321407720d35521b239cdedb85 -- governance/implementation/code-guides
```

## Expected Results

| Check | Expected Result |
| --- | --- |
| Protected starting head | `PASS` |
| PR #42 final head | `PASS` |
| PR #42 merge commit | `PASS` |
| Historical adoption record | `PASS` |
| Current V1.1 program status | `PASS` |
| Affected guides accounted for | `PASS` |
| Historical records preserved | `PASS` |
| Current status conflict | `NONE` |
| Current adoption state | `NOT_ADOPTED` |
| Current activation state | `NOT_ACTIVE` |
| Activation effective date | `NONE` |
| Guide content changed | `NO` |
| Approved source bytes changed | `NO` |
| Lifecycle stage advanced | `NO` |
| Implementation mapping created | `NO` |
| Application files changed | `NO` |
| GAP-0004 | `OPEN` |
| Retained warnings | `OPEN` |
| Activation blockers | `OPEN` |
| CGP-007 | `NOT_AUTHORIZED` |
| JSON and CSV parse | `PASS` |
| Manifest/checksum verification | `PASS` |
| Internal references | `PASS` |
| Authorized paths | `PASS` |
