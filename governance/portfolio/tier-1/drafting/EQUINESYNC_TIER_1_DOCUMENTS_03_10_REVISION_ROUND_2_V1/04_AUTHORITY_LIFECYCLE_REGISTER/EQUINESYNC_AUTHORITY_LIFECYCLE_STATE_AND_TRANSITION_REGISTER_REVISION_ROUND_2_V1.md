# Document 04 - Authority Lifecycle State And Transition Register

Readiness determination: `REVISION_ROUND_2_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

This artifact incorporates `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md` by exact reference. If this document and the shared standard conflict, the stricter non-authorizing, evidence-preserving, source-authenticating interpretation controls until Founder direction resolves the conflict.

## Normalized Lifecycle System

Document 04 separates lifecycle state, authority state, adoption state, accession state, activation state, implementation authority, production authority, evidence status, uncertainty, suspension, supersession, and custody.

## Concrete Record-Level Example

`T1R2-LIFE-03` marks Document 03 as `FOUNDER_REVIEW_READY`, `NOT_ADOPTED`, `NOT_ACCESSIONED`, `NOT_ACTIVE`, and `IMPLEMENTATION_NOT_AUTHORIZED`.

## Invalid Combination Handling

`INVALID_STATE_RULES.csv` defines blocking conditions. The validator fails candidate packages that represent candidate evidence as adopted authority, active authority without adoption, or production authority without activation evidence.
