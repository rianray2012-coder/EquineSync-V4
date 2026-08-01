# Directive Execution Record

Status: `PHASE_A_CORRECTIVE_IMPLEMENTATION_READY_FOR_DRAFT_PR`

Executed steps:

1. Authenticated the exact Founder directive file by SHA-256 and byte count.
2. Recorded the pasted request copy identity separately.
3. Revalidated PR #71 state, PR #72 state, unresolved PR #71 review threads, and absence of an existing correction PR.
4. Fetched the protected branch and reviewed drift from directive issuance head `d0d9528028982c1243f9e2a6b0f21a78f298276c` to live head `12d5ae6faf3627bb0786af46de953fda808d7156`.
5. Created correction branch `codex/cgp-006-iwp-0002-post-merge-correction-v1` from `12d5ae6faf3627bb0786af46de953fda808d7156`.
6. Implemented shared verified legacy Guardian-link expansion and applied it to messaging, billing, and recurring-charge owner expansion.
7. Implemented authoritative state-token propagation for recurring-charge materialized invoices and fail-closed `invoice.pay` handling for minor-involved legacy invoices without stored tokens.
8. Added focused tests `GMS-T-055` through `GMS-T-059`.
9. Re-ran syntax, direct focused tests, and diff checks.
10. Created this correction evidence package and package-local validator.

Deferred steps required by directive:

- Open the corrective PR as draft.
- Inspect GitHub checks and automated reviews.
- Correct every valid in-scope High, Medium, P0, P1, or P2 issue.
- Merge only by protected exact-head flow.
- After merge, reply to and resolve the two PR #71 threads.
- Then refresh PR #72 custody package and closure records without placing product code on PR #72.

No closure registers were updated in Phase A.
