# Candidate 006 Independent Evidence-Custody Rereview

Review ID: `STAGE2A_CUSTODIAN_REREVIEW_ATTEMPT_006`

Candidate: `ES-PKG-2026-004-V003-CANDIDATE-006`

Result: `CUSTODY_PASS_CANDIDATE_NOT_CLOSURE_READY_PROVIDER_P1_PROCESS_EVIDENCE_P2`

Self-closure: `NO`

Execution: `EXECUTION_NOT_AUTHORIZED`

Assurance: `NOT_EXTERNALLY_ASSURED`

## Custody and integrity

The frozen archive and all canonical Candidate 006 payload files remained unedited. The archive SHA-256 before and after review is:

`de4145d04779e0d1aa2b73bfff870f54637818c7ad895d74db82b6e9aa232068`

The payload-manifest SHA-256 before and after review is:

`e75db726bd1ca48a8ecbd6dd9d204b7189d4d3f015c3ce4e07a460ad792b0274`

All 253 manifested payload files pass SHA-256 verification. The archive contains 256 physical files, passes CRC validation, and has exact path and byte parity with all 256 files in the frozen candidate directory. The three intentionally unlisted physical files are the manifest itself and its JSON/Markdown snapshot records.

The independently calculated aggregate SHA-256 of the sorted physical-file SHA-256 listing is unchanged before and after review:

`baca85f43e307b9655d596b0b93f6ca7040e93b57c2aee45b0af61c385d5df3c`

No canonical candidate payload or archive byte changed. Three review-generated Python 3.11 bytecode cache files, which were absent from both the archive and manifest, were quarantined outside the candidate as `ES-PKG-2026-004-V003-CANDIDATE-006_POST_FREEZE_BYTECODE_RESIDUE.zip` at SHA-256 `829fb2df0175ab475a8abba27bf36539af7ad3a82bc5b05f09a21d2344eaa2c9`. Only those three archive-absent files were removed, restoring exact `256/256` path and byte parity. The detached validator then passed `23/23` with bytecode writing disabled.

## Independent validation

The recorded freeze-time validation matrix passes all four supported locations at `23/23`. A current detached clean extraction independently passes `23/23` using the frozen embedded source payload. A current invocation against Candidate 006 while it remains inside the now-modified active repository returns `22/23`: `MV-011-source-register` correctly identifies post-freeze hash drift in `stage2a/network_guard.py`, `stage2a/tests/test_controls.py`, and `stage2a/validate_stage2a_package.py`. Those active-source changes are outside frozen Candidate 006 and are not incorporated into this review.

Semantic probes independently confirmed:

- bare `Bearer`, `Authorization: Bearer`, `access_token`, and `client_secret` values are redacted;
- the non-secret `Bearer` scheme is preserved;
- raw probe secrets do not appear in the semantic projection serialization;
- before/after projections match for valid redaction;
- material over-redaction produces a projection mismatch;
- unexpected placeholders are rejected; and
- `token_count`, `secretary`, `bearer_species`, and `authorization_mode` near-misses remain unchanged.

The projector resides in a separate module that does not import the redactor. Persisted projection metadata omits its serialization and retains only safe hashes and counts.

Process-identity probes independently accepted a valid baseline and rejected conflicting controlled port, future/nonvalid identity time, PPID, executable, and working directory. Signal count remained zero when termination was presented with an identity conflict or a controlled-port conflict. This supports fail-closed runtime enforcement. It does not cure the frozen package-evidence validation gap: `MV-016B-process-identity` accepts a forged `api_identity.command_line_sha256` or `working_directory` because it neither recomputes the command hash from `observed_command_line` nor cross-checks the working directory against an independent trusted source.

Both provider event chains independently recompute without an error: each contains 11 process-bound, launch-nonce-bound, registry-bound provider events, both chain heads match, and both record zero provider/external and zero unattributed attempts. Startup arithmetic is exact: three attempts, two successes, one failure, one deliberately unentered skipped alternative, zero timeouts, and zero unavailable entered attempts. This establishes internal consistency of the frozen data, but not sufficient package validation: `MV-016A-provider-startup-measurement` accepts removal or zeroing of embedded `network_guard.provider_events` while the provider summary rows and proof fields remain unchanged. Provider provenance can therefore be severed without rejection.

## Five blocker recommendations

| Blocker | Evidence sufficiency | Custodian recommendation |
|---|---|---|
| `PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT` | `SUFFICIENT` | `RECOMMEND_CONTROLLED_CLOSURE_BY_AUTHORIZED_RECONCILIATION` |
| `TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC` | `SUFFICIENT` | `RECOMMEND_CONTROLLED_CLOSURE_BY_AUTHORIZED_RECONCILIATION` |
| `PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT` | `INSUFFICIENT_RETAIN_P1` | `DO_NOT_CLOSE_REMEDIATE_RERUN_REFREEZE_REREVIEW` |
| `EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT` | `SUFFICIENT` | `RECOMMEND_CONTROLLED_CLOSURE_BY_AUTHORIZED_RECONCILIATION` |
| `PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT` | `INSUFFICIENT_RETAIN_P2_PACKAGE_EVIDENCE_VALIDATION` | `DO_NOT_CLOSE_REMEDIATE_RERUN_REFREEZE_REREVIEW` |

These are recommendations, not finding closures. Candidate provenance and the finding matrix continue to say `REMEDIATED_PENDING_REREVIEW` and `self_closed=false`.

The validator-root evidence covers four supported invocation contexts. Traceability is contract-enforced against exact requirement, finding, source, test, implementation, evidence, and JSON/CSV relationships, with eight mutation tests passing. Semantic meaning is guarded by an independent projection and negative probes. Those three blocker classes are evidentially sufficient. Provider measurement retains a P1 evidence-provenance gap in `MV-016A`; process identity retains a P2 package-evidence validation gap in `MV-016B`, notwithstanding the stronger fail-closed runtime controls.

## Invalidated checks and current reruns

All five prior insufficient checks are explicitly invalidated and noncontrolling. Each has a current Candidate 006 rerun entry. The current implementation commit is `edd8ac0a59c9c0fce4408538e8596b10a9a97428`; the full lifecycle rerun passes `16/16`, and the dependency rerun passes with 127 artifacts. These aggregate rerun results do not override the adversarial evidence gaps: `MV-016A` does not require or recompute embedded provider-event provenance, and `MV-016B` does not independently cross-check the command hash or working directory. The provider P1 and process-evidence P2 blockers remain open.

## Predecessor reuse

Predecessor evidence is accurately limited to corroborative, noncontrolling use:

- lifecycle artifact SHA-256: `7e03815edf4c3ec8293d480029908e1b92286245f2c670f27d0d0756ff4315c7`;
- dependency artifact SHA-256: `be248999b1b320afc9eaea18224d42bd102877c77ad6d9f27916230dfe1f4a70`;
- containing predecessor manifest SHA-256: `e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b`;
- predecessor/current normalized dependency inventory SHA-256: `484d363380c4cdd8afa8765234e32d82d12157e1c1323b51bc15aaf94576b586`;
- predecessor/current dependency inventory text SHA-256: `450e5933a3bb34ca2ad81fd5c62332006369ca4cd45ba510864406aaa23c7298`; and
- current/packaged fixture-file SHA-256: `0aa525c43285874a3dd7887d466a185bae6fa07fcf1bf4ed45dae42da03eb81e`.

Current reruns, not predecessor results, control Candidate 006. No invalid predecessor reuse was found.

## Failed-candidate and earlier-freeze continuity

The failed archives remain byte-for-byte identified and internally consistent:

- Attempt 002: archive `6f984649f8465e3410d95deaf9ece76f642bb0ab70eddb89252a858cc0b470b4`, manifest `e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b`, `108/108` payload hashes, 111 physical files.
- Attempt 003: archive `86d87ca6d289f9ca3b3b3c48e565781469a553d8219b0c8a720b60aebf034ec0`, manifest `f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc`, `121/121` payload hashes, 124 physical files.
- Attempt 004: archive `7d209ec231f9d8a0ad04809f7d8efd45630534ea24875042ae5b6893c16e7c0c`, manifest `927cad3b2b8142188e2e9cce3a069fd121361f2ddf489ba7c5fc9d9d51af591f`, `207/207` payload hashes, 210 physical files.
- Candidate 005 assembly failure: archive `41cc9ae595dbe640cc9aedf79fe84267d58ddb84355682626e237eccd5d3595c`, manifest `a0937895498704028cf8f450f18555ac7b54b5417a96248d62702a6fa7aff75f`, exact `249/249` path and hash parity.

Candidate 005 remains correctly classified `PRE_FREEZE_ASSEMBLY_VALIDATION_FAILED`; it is preserved as failed evidence and is not presented as a successful frozen candidate. All four failed archives pass CRC validation.

## Residue-event separation

`SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE` remains `CONTAINED_TERMINATED_PORT_CLEARED`. No database or orchestration result from the active-residue interval was accepted, and affected checks were rerun after port clearance.

`RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains a separate `OPEN_BLOCKING_RUNTIME_LIMITATION` with no direct evidence of resolution. Its causal relationship to the process-residue event is `NOT_ESTABLISHED_DO_NOT_CONFLATE`. The residue event is closed operationally; the runtime limitation remains open and continues to block Stage 2A readiness.

## Reviewer-environment observations

System Python 3.14 lacked `jsonschema`, so it was not a valid candidate-toolchain test environment. The declared Python 3.11.11 candidate virtual environment was then used.

Running the embedded `source_payload` unit suite while it remained nested beneath the active Git repository produced 32 passes and one topology-specific root-resolution assertion failure: the embedded test-local `REPO` resolves to `source_payload`, while the validator correctly discovers the enclosing active Git repository. This is outside the declared root-repository and detached-extraction test topologies and does not contradict the recorded freeze-time matrix, the current detached `23/23` pass, or the controlling freeze-time root-repository `PASS_33_OF_33` unit result.

During probing, three Python 3.11 bytecode cache files were generated in the local candidate materialization. They were not archive members or manifested payload files. They were quarantined outside the candidate at SHA-256 `829fb2df0175ab475a8abba27bf36539af7ad3a82bc5b05f09a21d2344eaa2c9`, removed, and exact `256/256` frozen-archive parity was restored before final integrity verification.

## Boundary

No byte-integrity, manifest, archive-parity, semantic-projection, sensitive-slot, predecessor-reuse, failed-archive-continuity, or residue-classification discrepancy was found. Two material frozen-package validation gaps were confirmed: provider-event provenance can be removed or zeroed without `MV-016A` rejecting the package, and process command-hash or working-directory evidence can be forged without `MV-016B` rejecting the package.

This custodian review is limited to frozen Candidate 006 bytes and does not incorporate or attest any post-freeze source change. It does not close findings, authorize execution, establish production readiness, replace segregated/adversarial reconciliation, or provide external assurance. Three technical blocker classes are evidentially sufficient; provider P1 and process package-evidence P2 require remediation in a distinct successor candidate followed by rerun, refreeze, and independent rereview. `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains a separate unresolved blocking runtime limitation and must not be conflated with either retained evidence gap or the contained residue event.
