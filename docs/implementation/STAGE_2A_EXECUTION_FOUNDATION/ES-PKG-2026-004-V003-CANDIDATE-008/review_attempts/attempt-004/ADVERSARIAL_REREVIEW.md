# Stage 2A Adversarial Rereview — Attempt 004

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-004`
- Review mode: independent adversarial, read-only, no service start
- Result: `FAIL_REMEDIATION_AND_REFREEZE_REQUIRED`
- Principal disposition: `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`

## Immutable Snapshot

Candidate 004 remained unchanged throughout review. All 207 manifest payloads passed SHA-256 verification; 210 physical files and 210 archive entries were present. The manifest SHA-256 remained `927cad3b2b8142188e2e9cce3a069fd121361f2ddf489ba7c5fc9d9d51af591f`. The frozen archive passed integrity verification and remained `7d209ec231f9d8a0ad04809f7d8efd45630534ea24875042ae5b6893c16e7c0c`.

The failed 108-file freeze and Candidate 003 remained unchanged at manifest SHA-256 values `e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b` and `f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc`. No service was started and no listener was present on controlled ports 8019 or 27029.

## Blocker Results

| Blocker | Result | Severity |
|---|---|---|
| `PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT` | Technically resolved; detached and repository-backed candidate validation passed in all challenged working-directory modes. A separate validation-accounting defect remains. | — |
| `TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC` | Not resolved. False and unrelated cross-register relationships pass `MV-011A`. | P2 |
| `PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT` | Not resolved. Startup events are measured, but per-provider path evaluation is still synthesized from configuration plus a global zero ledger. | P1 |
| `EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT` | Not resolved. The semantic projection is tautological and accepts material meaning loss; common credential forms remain undetected. | P1 |
| `PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT` | Not resolved. The recorded controlled-port field is not enforced by `_expected` or `status`. | P2 |

## Open Findings

### `ES-ADV-V003-R4-F-0001` — P2 — Validation accounting is not exact

Assembly mode appends `MV-019-checksum-reconciliation` twice and reports 24/24 for only 23 unique check identifiers. Candidate mode reports 23/23. The validation command register also records `PASS_10_OF_10` for a unit suite whose immutable source and read-only rerun contain 21 passing tests. Unique check identifiers and the actual unit-test count must be enforced and regenerated before refreeze.

### `ES-ADV-V003-R4-F-0002` — P2 — Traceability checks existence, not relationship truth

In a detached temporary copy, the provider output row was changed to bogus control and finding IDs, the wrong gap, an unrelated registered toolchain test, and arbitrary nonempty role/rule/rationale. The provider finding was remapped to unrelated but existing toolchain remediation/test/evidence, and REQ-009 was given nonexistent source/test/evidence references. The validator still returned PASS 24/24 with `MV-011A` reporting no errors.

The validator must enforce closed identifier sets and explicit compatibility across requirements, controls, gaps, findings, remediation artifacts, executable tests, sources, evidence, artifact roles, and verification rules. Negative mutation tests must fail.

### `ES-ADV-V003-R4-F-0003` — P1 — Per-provider path evaluation is asserted

Startup attempt events now carry timestamps and event-derived attempted/succeeded/failed/skipped/timed-out/unavailable arithmetic. Nonzero unattributed network counts also fail closed. Those are material improvements.

However, `provider_register` receives only environment state and a network-ledger mapping. Supplying a syntactically valid zero ledger without executing any provider code still generated eleven `SKIPPED_NOT_CONFIGURED` rows with `provider_path_evaluated=true`. Per-provider results must be derived from attributable prerequisite or provider-boundary events, not stamped onto rows after startup.

### `ES-ADV-V003-R4-F-0004` — P1 — Semantic projection accepts meaning loss

The “before” semantic projection is produced by applying the same redactor used to create the “after” stream. It therefore cannot prove that nonsecret meaning survived redaction.

The adversarial full-record probe used:

```text
run complete
operation=login password=hunter2 authentication denied
```

The stored output became:

```text
run complete
operation=login password=<REDACTED>
```

The material outcome `authentication denied` was lost. With `required_meaning=["run complete"]`, the record remained schema-valid and semantic validation returned no errors. Bare `Bearer abc.def.ghi`, `access_token=opaque-value`, and `client_secret=opaque-value` also produced zero replacements and no residual-sensitive match.

An independently defined pre-redaction semantic projection and broader credential detection are required.

### `ES-ADV-V003-R4-F-0005` — P2 — Controlled-port identity is not enforced in status

Executable path, full argv, working directory, PPID, PGID, launch nonce, listener attribution, and timeout handling materially improved. The remaining defect is exact: `_expected` never compares `record.controlled_port`, and `status` does not do so before declaring listener identity verified.

A pure conflict probe supplied otherwise valid records declaring ports 9998 and 9999. The status path still reported the Mongo and API identities alive and listener-verified for fixed ports 27029 and 8019 with no attribution conflict. `_terminate` would refuse signaling later, but the startup/status evidence can first certify an internally inconsistent identity.

## Additional Challenge Results

- Root resolution: five candidate-mode invocation variants passed 23/23, including detached clean extraction from the frozen archive.
- Unit controls: 21/21 passed read-only.
- Invalid predecessor reuse: none found. Predecessor results are identified as corroborative and non-controlling; fresh Candidate 004 lifecycle evidence is bound to commit `daa10387e073952b823afde9b681e602cb70c7b8`.
- Hidden execution, production, CP-3, or external-assurance readiness claims: none found.
- Plausible live secrets: none found.
- `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains a separate open blocking runtime limitation and was not causally conflated with these findings.

## Final Adversarial Disposition

`FAIL_REMEDIATION_AND_REFREEZE_REQUIRED`

Candidate 004 must not be promoted or self-closed. The P1 semantic/provider findings and P2 traceability, process-port, and validation-accounting findings require remediation, rerun, rebuild, a distinct immutable freeze, and independent rereview.
