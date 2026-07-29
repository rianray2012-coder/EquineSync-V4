# Validation Report

**Package ID:** `CGP-006-WAVE-1-V1-1-GUIDE-COMPLETION-ADOPTION-CANDIDATE-PREPARATION`
**Result:** `PASS`
**Validator result:** `PASS`
**Unit-test result:** `OK`
**Negative-test result:** `14 tests passed, including required prohibited-state fixtures`
**git diff --check result:** `PASS`

Commands executed locally:

```text
python3 governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/validators/validate_guide_completion_adoption_candidate.py --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/tests
git diff --check f2cbd5c75e5cc4e8f5ef5bc5ea80508f36600994 -- governance/implementation/code-guides
```

Validated counts:

| item | count |
| --- | --- |
| Guides | 4 |
| Stage rows | 76 |
| Controls | 22 |
| Invariants | 22 |
| Mandatory questions | 32 |
| Risks | 22 |
| Verification rows | 44 |
| Atlas traceability rows | 22 |
| Repository responsibility rows | 22 |
| Scenarios | 20 |
| Open findings | 7 |
| Retained condition/warning/gap/blocker records | 23 |
| Package files | 124 |

The validator checks required files, guide directories, controlled values, unique identifiers, control completeness, invariant completeness, mandatory-question completeness, source references, cross-guide references, traceability references, prohibited implementation mappings, adoption-state boundaries, activation-state boundaries, evidence-grade validity, assurance-class validity, review-record completeness, scenario coverage, manifest completeness, checksum correctness, historical-byte preservation, frozen-source preservation, and authorized paths.
