# Retained Test Classification Source Register

**Directive ID:** `ES-FOUNDER-AUTH-TA-PRF-001-008-2026-07-26-01`  
**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`

## Primary Source

| Source | SHA-256 | Use |
| --- | --- | --- |
| `backend/tests/ci_known_failure_baseline.json` | `1b51922055edf5e02e2fe7c9c178d016141bdad22c629f31f05878370d09bf0b` | Canonical node IDs, outcomes, counts, baseline schema, and baseline policy. |

## Supporting Sources

| Source | Use |
| --- | --- |
| `backend/tests/README.md` | CI evidence model, known-failure ratchet meaning, marker methodology, and local command semantics. |
| `backend/tests/_ci_classification.py` | Live marker and auxiliary marker methodology. |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv` | Founder decisions and pilot-gate effects for ES-TA-FD-001 through ES-TA-FD-008. |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv` | Finding-to-decision mapping and closure evidence requirements. |

## Method

Classification was derived from exact node IDs, source file families, test names, the existing known-failure baseline counts, and the approved Founder decision package. No test was deleted, skipped, xfailed, weakened, re-marked, or moved between live and non-live sets.

## Limitations

This package classifies retained nodes for governance and remediation sequencing. It does not prove the current runtime behavior for every node, does not close any technical finding, does not reduce the known-failure baseline, and does not authorize pilot or release activity.
