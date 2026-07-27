# Retained Test Classification Validation Report

**Directive ID:** `ES-FOUNDER-AUTH-TA-PRF-001-008-2026-07-26-01`  
**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`  
**Determination:** `ES_TA_PRF_008_NODE_CLASSIFICATION_DRAFT_PR_READY_FOR_FOUNDER_REVIEW`

## Validation Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Baseline schema recognized | PASS | `equinesync_pr3_known_failure_baseline_v1` |
| Canonical node count | PASS | 161 classified rows |
| Canonical failed/error counts | PASS | 158 failures and 3 errors |
| Unclassified rows | PASS | 0 |
| Known-failure baseline modified | PASS | No change made to `backend/tests/ci_known_failure_baseline.json` |
| Runtime/test/CI files modified | PASS | No runtime, test, CI, schema, migration, provider, or deployment file is part of this package |
| P0 classification count | PASS | 0 |
| P1 classification count | PASS | 88 |
| P2 classification count | PASS | 73 |

## Baseline Counts Reconciled

- Total collected: 2286
- Selected non-live: 1080
- Live deselected: 1206
- Passed: 919
- Failed: 158
- Errors: 3
- Skipped: 0
- Known failing or erroring node IDs: 161

## Residual Gate Status

Classification is complete for all retained nodes, but remediation remains open. No retained failure or error is waived, accepted as correct behavior, suppressed, skipped, xfailed, or approved for release.
