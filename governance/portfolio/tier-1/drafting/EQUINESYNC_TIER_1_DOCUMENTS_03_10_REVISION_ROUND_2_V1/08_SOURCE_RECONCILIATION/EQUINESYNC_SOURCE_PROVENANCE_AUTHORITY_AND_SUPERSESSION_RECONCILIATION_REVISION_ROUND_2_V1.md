# Document 08 - Source Provenance Authority And Supersession Reconciliation

Readiness determination: `REVISION_ROUND_2_EXTERNAL_REVIEW_REMEDIATED_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

The source register now populates `duplicate_cluster_id` for duplicate cluster members and uses `NO_DUPLICATE_CLUSTER` for singleton rows. Dashboard counts distinguish unique hashes, duplicate clusters, redundant duplicate copies, and cluster-member rows.

Rows that contain adoption or lock evidence are labelled as source evidence only. They do not alter this package's `NOT_ADOPTED` state.
