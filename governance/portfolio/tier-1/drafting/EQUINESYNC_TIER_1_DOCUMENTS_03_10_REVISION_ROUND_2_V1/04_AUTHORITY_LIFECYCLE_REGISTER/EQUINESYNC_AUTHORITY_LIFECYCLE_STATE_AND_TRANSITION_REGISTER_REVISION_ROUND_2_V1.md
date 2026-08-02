# Document 04 - Authority Lifecycle State And Transition Register

Readiness determination: `REVISION_ROUND_2_EXTERNAL_REVIEW_REMEDIATED_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

The lifecycle model now covers all declared lifecycle states, including `DRAFT_UNMERGED`, `BLOCKED_EVIDENCE_REQUIRED`, `REJECTED`, and `REMEDIATION_REQUIRED`. `LIFECYCLE_TRANSITION_MATRIX.csv` is a 13-state transition matrix. Each permitted transition has transition-specific authority and evidence.

`INVALID_STATE_RULES.csv` includes `implementation_status` and `failure_capable` fields. Every rule marked `ENFORCED_BY_VALIDATOR` is implemented in the package validator. A rule must not be described as enforced unless the validator can fail on that condition.
