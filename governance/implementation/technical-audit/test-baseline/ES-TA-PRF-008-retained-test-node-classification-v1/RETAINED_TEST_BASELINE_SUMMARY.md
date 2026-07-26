# Retained Test Baseline Summary

**Directive ID:** `ES-FOUNDER-AUTH-TA-PRF-001-008-2026-07-26-01`  
**Workstream:** `ES-TA-PRF-008` Retained Test-Node Classification  
**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`  
**Source baseline:** `backend/tests/ci_known_failure_baseline.json`  
**Source baseline SHA-256:** `1b51922055edf5e02e2fe7c9c178d016141bdad22c629f31f05878370d09bf0b`  
**Determination:** `ES_TA_PRF_008_NODE_CLASSIFICATION_DRAFT_PR_READY_FOR_FOUNDER_REVIEW`

## Canonical Counts

| Metric | Count |
| --- | ---: |
| Total collected | 2286 |
| Selected non-live | 1080 |
| Live deselected | 1206 |
| Passed | 919 |
| Failed | 158 |
| Errored | 3 |
| Skipped | 0 |
| Known failing or erroring node IDs | 161 |

## Classification Totals

| Dimension | Value | Count |
| --- | --- | ---: |
| Severity | P1 | 88 |
| Severity | P2 | 73 |
| Outcome | error | 3 |
| Outcome | failure | 158 |
| Disposition | BLOCKS_PILOT_UNTIL_REMEDIATED_OR_EXPLICITLY_EXCLUDED | 85 |
| Disposition | RETAINED_ERROR_REQUIRES_TEST_SETUP_REMEDIATION_OR_CONTROLLED_EXCLUSION | 3 |
| Disposition | RETAINED_PRE_PILOT_TECHNICAL_DEBT | 73 |

## Product Area Totals

| Product Area | Count |
| --- | ---: |
| Admin portal billing and provider controls | 6 |
| Admin portal read-only contract | 16 |
| Backend app assembly | 1 |
| Feature shell UX truth | 1 |
| HorseOps ledger indexes and mobile evidence | 8 |
| Launch trust and role journey safety | 1 |
| Legal e-signature provider readiness | 1 |
| Mobile, PWA, and app-store readiness | 11 |
| Multi-barn membership and account model | 5 |
| Role onboarding, first-login, and navigation | 47 |
| Staging, UAT, launch, and feature-certification evidence | 53 |
| Tenant and barn authorization | 3 |
| Today Pulse evidence and walkthrough | 8 |

## Pilot Gate Summary

- `P0` unresolved classifications: 0.
- `P1` retained nodes: 88. These require remediation, controlled exclusion, or exact Founder risk treatment before pilot readiness can be claimed.
- `P2` retained nodes: 73. These remain pre-pilot technical debt and evidence/readiness work.
- Unclassified nodes: 0.

## Scope Boundary

This branch adds classification evidence only. It does not change runtime code, tests, CI, marker allowlists, known-failure baseline entries, schemas, migrations, provider settings, production branches, deployment settings, payments, pilot enrollment, or public release channels.
