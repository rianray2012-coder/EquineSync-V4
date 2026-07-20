# Stage 2A Adversarial Rereview — Attempt 006

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-006`
- Review mode: independent adversarial, read-only, no service start, mutations confined to disposable copies
- Result: `FAIL_REMEDIATION_AND_REFREEZE_REQUIRED`
- Principal disposition: `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`

## Immutable Snapshot

All 253 Candidate 006 manifest payloads remained byte-identical and passed SHA-256 verification; 256 frozen physical files and 256 archive entries were present. During review, one repository-candidate source import inadvertently created three Python bytecode cache residue files. The exact paths and hashes were preserved in `outputs/ES-PKG-2026-004-V003-CANDIDATE-006_POST_FREEZE_BYTECODE_RESIDUE.zip` at SHA-256 `829fb2df0175ab475a8abba27bf36539af7ad3a82bc5b05f09a21d2344eaa2c9`. Cleanup removed only those archive-absent files and empty directories. Post-cleanup byte parity with the canonical frozen archive was 256/256, and detached validation with bytecode writes disabled passed 23/23. No canonical payload was overwritten. The manifest SHA-256 remained `e75db726bd1ca48a8ecbd6dd9d204b7189d4d3f015c3ce4e07a460ad792b0274`. The frozen archive passed integrity verification and remained `de4145d04779e0d1aa2b73bfff870f54637818c7ad895d74db82b6e9aa232068`.

The failed 108-file freeze, Candidates 003 and 004, and the failed Candidate 005 assembly remained unchanged at manifest SHA-256 values `e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b`, `f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc`, `927cad3b2b8142188e2e9cce3a069fd121361f2ddf489ba7c5fc9d9d51af591f`, and `a0937895498704028cf8f450f18555ac7b54b5417a96248d62702a6fa7aff75f`. No service was started and no listener was present on controlled ports 8019 or 27029.

## Blocker Results

| Blocker | Result | Severity |
|---|---|---|
| `PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT` | Technically resolved. Four invocation locations passed 23/23; detached validation was read-only. | — |
| `TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC` | Technically resolved. False relationships, JSON/CSV divergence, and duplicate identifiers fail closed. | — |
| `PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT` | Not resolved. The package trusts provider summary/proof assertions without semantically rederiving the event chain. | P1 |
| `EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT` | Technically resolved. Independent meaning and credential-form probes fail closed. | — |
| `PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT` | Runtime signaling controls are resolved, but packaged process evidence still accepts forged command-hash and working-directory fields. | P2 |

## Resolved Technical Controls

The packaged validator passed 23/23 from package-root, nested, external, and detached clean-extraction working directories. The detached run loaded frozen `source_payload` and produced no file-list or content-hash difference. All 33 Candidate 006 source unit tests passed read-only.

Traceability now enforces exact source-controlled relationships. Wrong-but-existing output and finding relationships, JSON/CSV divergence, and duplicate mapping, test, requirement, and finding identifiers all failed `MV-011A` and the assembly validator.

The evidence redactor and independent projector correctly handled bare Bearer, authorization-bearer, `access_token`, and `client_secret` forms. The prior `operation=login password=hunter2 authentication denied` over-redaction probe changed the independent projection and was rejected; the projection did not retain `hunter2`. An unexpected `<REDACTED>` placeholder was detected, while ordinary near-miss names remained unchanged.

Runtime process controls also materially improved. Pure mocked checks rejected PPID, PGID, controlled-port, command-hash, executable, working-directory, launch-nonce, and timestamp conflicts. The conflict termination path refused to signal and `os.killpg` remained uncalled.

## Open Findings

### `ES-ADV-V003-R6-F-0001` — P1 — Provider event-chain assertions are not semantically rederived

Provider generation now creates process-bound, hash-chained capability events. An empty supplied ledger, ordinary event tamper, PID mismatch, and nonce mismatch all failed closed.

The remaining defect is material. After recomputing the unkeyed chain, provider derivation accepted an event with zero attempted outcomes and zero terminal outcomes. It also accepted a registry-inconsistent reason code. More decisively, a detached assembly copy with every embedded foundation provider event removed, event count set to zero, and chain head set to zero still passed 23/23. `MV-014` and `MV-016A` trusted the retained register rows and proof booleans instead of reconstructing the event chain.

The frozen Candidate 006 event chain itself is present and protected by the immutable manifest. The failure is that the claimed validating control cannot independently substantiate that evidence before freeze. Exact event schema, session identity, UTC, type, boundary/configuration state, reason, source identity, terminal arithmetic, value handling, network-attempt totals, chain reconstruction, and cross-artifact equality must be enforced. Missing-event and fully rehashed mutation tests are required.

### `ES-ADV-V003-R6-F-0002` — P2 — Packaged process evidence accepts forged identity fields

Runtime process identity and signaling fail closed. The package-evidence validator does not enforce the same relationships.

Candidate 006 preserves a pre-redaction `command_line_sha256` and a `packaged_command_line_sha256` over the path-redacted observed command. The frozen packaged hashes are internally consistent. A detached assembly mutation replaced `api_identity.packaged_command_line_sha256` with 64 zeroes; validation still returned PASS 23/23 and `MV-016B` passed. A separate mutation replaced `api_identity.working_directory` with `/forged/wrong/cwd`; validation again passed. The validator must recompute the packaged command hash, enforce raw-hash-basis and path-redaction metadata plus every identity value and relationship, and cross-check startup with shutdown PID/PGID evidence. Negative packaged-evidence mutations must cover PPID, PGID, port, command, executable, working directory, nonce, and timestamp.

## Additional Challenge Results

- Invalid predecessor reuse: none found. Reused evidence remains marked corroborative and non-controlling; invalidated blocker checks were rerun against Candidate 006.
- Hidden execution, production, CP-3, or external-assurance readiness claims: none found.
- Plausible live secrets: none found.
- `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains a separate open blocking runtime limitation and was not causally conflated with these findings.

## Final Adversarial Disposition

`FAIL_REMEDIATION_AND_REFREEZE_REQUIRED`

Candidate 006 must not be promoted or self-closed. The retained P1 provider-measurement blocker and P2 packaged process-evidence defect require controlled remediation, rerun, rebuild, a distinct immutable Candidate 007 freeze, and independent rereview.
