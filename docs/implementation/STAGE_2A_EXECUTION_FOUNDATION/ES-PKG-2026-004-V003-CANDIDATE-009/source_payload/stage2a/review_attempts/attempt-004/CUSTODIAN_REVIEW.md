# Stage 2A Evidence Custodian Review — Attempt 004

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-004`
- Verified UTC: `2026-07-20T08:59:31Z`
- Review mode: `READ_ONLY_NO_RUNTIME`
- Disposition: `CUSTODIAN_PASS_FOR_BYTE_INTEGRITY_PROVENANCE_AND_EVIDENCE_BOUNDARIES`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`

## Candidate 004 byte integrity

The frozen archive SHA-256 is `7d209ec231f9d8a0ad04809f7d8efd45630534ea24875042ae5b6893c16e7c0c`, matching the sidecar and frozen snapshot record.

- Archive entries/files: `210/210`; no directory entries.
- Expanded physical files: `210`.
- Manifest SHA-256: `927cad3b2b8142188e2e9cce3a069fd121361f2ddf489ba7c5fc9d9d51af591f`.
- Manifested payload: `207/207 PASS` with zero malformed, missing, or mismatched entries.
- Freeze controls excluded from the self-referential payload manifest: `DRAFT_REVIEW_SHA256SUMS.txt`, `DRAFT_REVIEW_SNAPSHOT_RECORD.json`, and `DRAFT_REVIEW_SNAPSHOT_RECORD.md`.
- Reconciliation: `207 payload + 3 freeze controls = 210 physical/archive files`.
- Archive-to-expanded equality: `210/210` byte-equal; zero archive-only, expanded-only, or byte-mismatched paths.
- ZIP CRC, duplicate-name, path-traversal, symlink, case-collision, and archive-root checks: `PASS`.

## Freeze lineage and identity

The candidate is consistently identified as the distinct fourth candidate and review attempt 4.

- Validated implementation: `daa10387e073952b823afde9b681e602cb70c7b8`, tree `4fa3b622d2b4f82d6423195bdf36c5af01fa95e4`.
- Assembly: `22ba2774a916d0c1df887d8dc4fe39538b95e67f`, tree `689bd800b7fefafb72cae4ecb9e4d6c3cc7202f6`, direct child of the implementation commit.
- Freeze: `52ec3c697dd731fd7e3b3a624333975ed1477d30`, tree `c74c6aa747311eec333b1210ce687934c120f51b`, direct child of the assembly commit.
- The freeze commit adds only `stage2a/review_attempts/attempt-004/FROZEN_SNAPSHOT_RECORD.json` and `.md`.
- Freeze-record JSON SHA-256: `f1a26a69eab472a1ebd67b0f42f2ed2acb9827ca71f183f60ac44e1327500e23`.

The package-internal provenance correctly avoids a circular self-reference and defers the freeze commit to the external frozen snapshot record.

## Preserved failed candidates

Both predecessor failed archives remain byte-for-byte unchanged:

- Attempt 002: SHA-256 `6f984649f8465e3410d95deaf9ece76f642bb0ab70eddb89252a858cc0b470b4`; manifest `e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b`; 111 physical files; ZIP CRC pass.
- Attempt 003: SHA-256 `86d87ca6d289f9ca3b3b3c48e565781469a553d8219b0c8a720b60aebf034ec0`; manifest `f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc`; 124 physical files; ZIP CRC pass. It is byte-equal to the original Candidate 003 frozen archive.

## Evidence reuse and current reruns

The reuse register accurately limits predecessor evidence to corroborative, noncontrolling use.

- The predecessor `16/16` lifecycle artifact is immutably identified by SHA-256 `7e03815edf4c3ec8293d480029908e1b92286245f2c670f27d0d0756ff4315c7` within manifest `e8a65076…`; its reuse is limited to stable fixture, cleanup, and recovery invariants.
- The predecessor 127-artifact dependency evidence is immutably identified by SHA-256 `be248999b1b320afc9eaea18224d42bd102877c77ad6d9f27916230dfe1f4a70` within the same manifest.
- The predecessor and current normalized dependency inventories both hash to `484d363380c4cdd8afa8765234e32d82d12157e1c1323b51bc15aaf94576b586`; the inventory text hashes to `450e5933a3bb34ca2ad81fd5c62332006369ca4cd45ba510864406aaa23c7298`.
- Candidate 004 contains new controlling reruns at `daa10387…`: lifecycle `PASS 16/16` and dependency evidence `PASS 127`, with zero dependency compatibility failures.

Disposition: `PASS_REUSE_BOUNDARY_ACCURATE`. Reused evidence does not substitute for or control the Candidate 004 result.

## Residue-event separation

The evidence maintains three distinct classifications:

1. `SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE` was a MongoDB process from a segregated temporary review clone. It was contained, terminated, and its port cleared. No database or orchestration validation from the active-residue interval was accepted; relevant checks were rerun afterward.
2. `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains an open runtime-capability limitation, not an implementation failure. Its record expressly says the causal relationship to the Mongo residue is not established and the two must not be conflated.
3. `CONTROLLED_IDENTITY_PROBE_TEMPORARY_PROCESS_RESIDUE` involved read-only `/usr/sbin/lsof` probes, not a MongoDB or application listener. No application or database process was terminated, no repository or sealed file changed, attempt 006 was discarded, and validation was rerun. Its record expressly disclaims attribution to either earlier event.

The three event JSON files are byte-equal to their packaged `source_payload` copies and are separately registered by their own classifications and hashes. Disposition: `PASS_THREE_DISTINCT_EVENTS_NOT_CONFLATED`.

## Custodian conclusion

No byte-integrity, manifest, extraction, identity, predecessor-preservation, reuse-boundary, or residue-classification discrepancy was found. This custodian pass does not close F-0001, authorize execution, establish production readiness, replace segregated or adversarial review, or provide external assurance. No services or runtime workflows were started.
