# Document 08 - Source Provenance Authority And Supersession Reconciliation

Readiness determination: `REVISION_ROUND_2_REMEDIATION_IN_PROGRESS_CONTENT_REVISION_REQUIRED`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

The source register now populates `duplicate_cluster_id` for duplicate cluster members and uses `NO_DUPLICATE_CLUSTER` for singleton rows. Dashboard counts distinguish unique hashes, duplicate clusters, redundant duplicate copies, and cluster-member rows.

Rows that contain adoption or lock evidence are labelled as source evidence only. They do not alter this package's `NOT_ADOPTED` state.

## V4 Purpose Scope Method And Limitations

Purpose: provide a reviewer-readable control surface for source reconciliation without creating adoption, activation, implementation, production, merge, certification, waiver, risk-acceptance, final-closure, or Founder-approval authority.

Scope: limited to the V4 bounded rereview package, the registers in this directory, authenticated source-review inputs, and the PR #90 documentary custody context.

Method: source custody, candidate-path handling, duplicate clusters, and authority labels. Reviewers should read register rows by row ID, source locator, evidence hash or byte count where present, status vocabulary, and retained-open fields. Blank, generic, or repeated analytical text is not closure evidence.

Limitations: this document is not a runtime assessment, legal opinion, production deployment record, certification report, or Founder decision. Open T1C rows remain open until independently adjudicated.

Evidence boundary: every conclusion must link to a package file, register row, source-review finding ID, validation report, or detached archive checksum. Absence of evidence must be recorded as open rather than inferred as remediated.
