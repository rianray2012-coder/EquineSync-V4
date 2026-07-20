# Stage 2A Segregated Rereview — Attempt 006

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-006`
- Freeze commit: `61b4851ad2d802834afb6bdf1b0981f778c68011`
- Completed UTC: `2026-07-20T10:30:37Z`
- Technical review result: `FAIL`
- Package-level result: `FAIL_SEMANTIC_ENFORCEMENT_GAPS`
- Disposition: `REMEDIATION_NOT_FULLY_VERIFIED_RETAIN_OPEN_FINDINGS`
- Technical findings: `P0 0 / P1 1 / P2 1`
- Services started by rereview: `NO`
- Self-closure: `NO`

## Frozen candidate and archive

The immutable candidate contains 256 physical files and no symlinks. Its 253-row internal manifest verified `253/253`, with manifest SHA-256 `e75db726bd1ca48a8ecbd6dd9d204b7189d4d3f015c3ce4e07a460ad792b0274`. The independently defined candidate tree digest—SHA-256 over sorted `relative-path NUL file-SHA256 newline` records—is `543c80cf7de31cccc20f851101989327e0c66154606431b1b3770acda601406a`.

The frozen archive SHA-256 is `de4145d04779e0d1aa2b73bfff870f54637818c7ad895d74db82b6e9aa232068`. Archive path safety and detached clean extraction passed. All 256 extracted files are byte-identical to the candidate; missing, extra, mismatched, and unsafe paths are all zero. The temporary extraction was removed.

No substantive frozen artifact was changed, and the archive was never modified. Three post-freeze Python bytecode-cache residue files were detected in the local candidate working copy, quarantined, and removed. The local candidate was restored against the canonical archive and finished at exact `256/256` byte parity; a final detached validation with bytecode disabled passed `23/23`. The final candidate tree digest, internal-manifest hash, and archive hash therefore equal the recorded pre-review values.

## Packaged validator and independent controls

The packaged validator passed `23/23` from all four reviewed locations:

1. Candidate package root, repository-backed mode; stdout SHA-256 `97787d62692c485be0d40eaa58260f1dd4ad1a24165c03f560de1afb86dd97b9`.
2. Nested candidate `review_attempts/attempt-004`, repository-backed mode; stdout SHA-256 `b9d448a076d3049c28ee6bf1e2c7e8807474dd1b6554d87342e520347b6a9bd8`.
3. External `/private/tmp`, repository-backed mode; stdout SHA-256 `d97c14307c58280724b45de22b6fff9760939d531e23c97e695a85f661d78d86`.
4. Detached clean archive extraction, `DETACHED_PACKAGE_SOURCE_PAYLOAD` mode; stdout SHA-256 `a72109cb47b508d2c925eaea093be6f6856eea8748cfe12e5f4c60a35cf99ba7`.

Each stderr stream was empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Independent checks established:

- All 116 JSON files parse. All six CSV files parse with 167 data rows. The six JSON/CSV pairs have exact row and field parity: source 111, requirement 9, test 26, finding 5, provider 11, and F-0002 closure evidence 5.
- All 111 source-register rows match detached payload hashes, recorded Git commit blobs, and applicable validated-implementation commit blobs.
- The trace graph resolves nine requirements, five findings, 26 executable test controls, 111 source records, and 115 output mappings without dangling references or generic all-requirement mappings.
- The pass and expected-failure execution-evidence records reconcile expected and actual exit values, required meaning, semantic projection, and redaction. The expected-failure command exited 7 and correctly yields an evidence result of `PASS` because 7 was the declared expected result.
- Startup evidence matches its oracle: zero startup document writes and zero provider network attempts. Four startup event records reconcile to three entered attempts—two succeeded and one failed—plus one unentered alternate profile classified skipped; none timed out or was unavailable.
- PID, PPID, PGID, command hash, executable, working directory, controlled port, launch nonce, and identity time are controlled. Conflict paths fail closed and verified process groups are terminated as groups.
- `PYTHONDWRITEBYTECODE=1 stage2a/.venv/bin/python -m unittest stage2a/tests/test_controls.py stage2a/tests/test_traceability_contract.py` ran 33 tests and passed. It did not start runtime services.
- No listeners remained on controlled ports 27029 or 8019 after review.

## Provider measurement disposition

The recorded provider evidence is internally consistent, but the provider defect is not technically closed. The public provider-register function no longer accepts caller-provided environment or ledger objects, and the unit control confirms that a supplied zero ledger is rejected. That improvement is insufficient because the frozen semantic verifier is not fail closed.

The frozen evidence contains 11 attributable provider capability events bound to guard session `276e33f8ad79448a90873506bddc97f1`, API PID/PGID `73778`, launch-nonce hash `38c96c4b5cee91debabf820593dafaf4fd293420e4f64cf39b29d0dc847f6814`, and registry hash `596a1707b8060e37c7dcbe3e42399173a928768521e22806818744bbef1db895`. Independent recomputation verified sequences 1–11 and final chain SHA-256 `216a28910b637f90523ccdee38f08672d957bbe9f288f1af1d47b01884d274af`.

The recorded derived outcomes are exact: attempted 0, succeeded 0, failed 0, skipped 4, timed out 0, and unavailable 7. Stripe, Resend, DocuSign, and object storage are present integrations with prerequisite-evaluation records; their provider boundaries were not exercised. Cloudflare API, SendGrid, Twilio, external AI, and analytics are represented as absent from runtime source, while Render and Vercel are represented as out-of-process deployment controls. There are zero recorded network-attempt events and zero recorded unattributed attempts.

Adversarial mutation invalidates promotion of those records to sufficient proof:

- Frozen `derive_provider_register` accepted a fully rehashed 11-event chain after every provider terminal outcome (`attempted`, `succeeded`, `failed`, `skipped`, `timed_out`, and `unavailable`) was set to zero. It still returned 11 rows and asserted `event_chain_valid=true`.
- The same frozen derivation accepted a fully rehashed Stripe event whose `reason_code` was changed to `FORGED_REASON_MISMATCH`; registry-reason semantics are not compared.
- In a temporary detached copy, all four embedded foundation network-guard `provider_events` arrays were removed and their `event_count` and `event_chain_sha256` were zeroed while summary register rows and proof assertions remained. `MV-016A-provider-startup-measurement` still returned `PASS`.

These results establish open P1 finding `ES-SEG-V003-R6-F-0001`, `PROVIDER_EVENT_SEMANTIC_ENFORCEMENT_NOT_FAIL_CLOSED`. Prior provider finding `ES-ADV-V003-R2-F-0001` must remain open and blocking.

## Process-identity enforcement disposition

The frozen runtime implementation itself passes: PPID, PGID, controlled port, command, executable, working directory, launch nonce, and identity timestamp conflicts are rejected, and conflict paths issue no signal. Process-group termination is present for verified owned processes.

The packaged evidence verifier is weaker than the runtime control. In a temporary detached package copy, `MV-016B-process-identity` still returned `PASS` after the packaged API identity `command_line_sha256` was changed to 64 zeroes and `working_directory` was changed to `/forged/c006/path`. It checks that the working directory is merely nonempty and does not validate the command hash or bind either value to an expected controlled identity.

This establishes open P2 finding `ES-SEG-V003-R6-F-0002`, `PACKAGED_PROCESS_IDENTITY_EVIDENCE_SEMANTICS_NOT_FAIL_CLOSED`. The runtime implementation is verified, but prior process-identity finding `ES-ADV-V003-R2-F-0005` must remain open pending package semantic enforcement.

## Five blocker dispositions

This segregated rereview recommends authorized closure for three prior blockers and retains two open. It does not self-close any finding.

- `ES-ADV-V003-R2-F-0004` — `PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT`: `REMEDIATION_VERIFIED`; residual severity none; recommend authorized closure. Four-location validation, including detached source-payload mode, passed `23/23`.
- `ES-ADV-V003-R2-F-0003` — `TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC`: `REMEDIATION_VERIFIED`; residual severity none; recommend authorized closure. All trace references and specificity controls passed.
- `ES-ADV-V003-R2-F-0001` — `PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT`: `REMEDIATION_NOT_VERIFIED`; residual severity P1; retain open and blocking. Hash-chain integrity does not enforce terminal outcomes or registry-reason semantics, and MV-016A accepts provider summary assertions without the embedded event chain.
- `ES-ADV-V003-R2-F-0002` — `EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT`: `REMEDIATION_VERIFIED`; residual severity none; recommend authorized closure. Exit semantics, hashes, meaning preservation, and redaction controls passed.
- `ES-ADV-V003-R2-F-0005` — `PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT`: `RUNTIME_IMPLEMENTATION_VERIFIED_PACKAGE_EVIDENCE_ENFORCEMENT_NOT_VERIFIED`; residual severity P2; retain open. Runtime conflict behavior is fail closed, but MV-016B accepts a zero command hash and arbitrary nonempty working directory in packaged identity evidence.

## Runtime-selector and F-0001 boundary

The package-level technical result does not close the separate runtime constraint. `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` remains `OPEN_BLOCKING_RUNTIME_LIMITATION`; direct evidence of its resolution remains false, and `F0001_REMAINS_OPEN_BLOCKING`. This is not a package implementation failure, but it continues to block principal Stage 2A disposition.

Accordingly, Candidate 006 fails the independent technical rereview on the P1 provider semantic gap and P2 package process-evidence gap. Separately, the runtime selector remains unresolved. The governing state remains `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`, `EXECUTION_NOT_AUTHORIZED`, and `NOT_EXTERNALLY_ASSURED`.

## Command evidence

Commands rerun or independently replicated included:

```text
git rev-parse HEAD
shasum -a 256 <candidate>/DRAFT_REVIEW_SHA256SUMS.txt <frozen-archive>
stage2a/.venv/bin/python <candidate>/validate_stage2a_package.py <candidate>
cd <candidate>/review_attempts/attempt-004 && stage2a/.venv/bin/python <candidate>/validate_stage2a_package.py <candidate>
cd /private/tmp && stage2a/.venv/bin/python <candidate>/validate_stage2a_package.py <candidate>
extract frozen archive to TemporaryDirectory; run packaged validator against extracted candidate
PYTHONDONTWRITEBYTECODE=1 stage2a/.venv/bin/python -m unittest stage2a/tests/test_controls.py stage2a/tests/test_traceability_contract.py
independent Python recomputation of manifest, archive, JSON/CSV, source Git blobs, trace graph, provider hash chain, startup arithmetic, evidence semantics, and process identity controls
temporary frozen-source adversarial rehash with all provider terminal outcomes zero; derive_provider_register accepted 11 rows and asserted valid chain
temporary frozen-source adversarial rehash with registry reason mismatch; derive_provider_register accepted 11 rows and asserted valid chain
temporary detached-package mutation removing all embedded foundation provider events while leaving summary/proof assertions; MV-016A passed
temporary detached-package mutation forging API command hash and working directory; MV-016B passed
custodian quarantine/removal of three post-freeze pycache residue files; canonical archive parity restored 256/256; detached bytecode-disabled validator passed 23/23
lsof -nP -iTCP:27029 -sTCP:LISTEN
lsof -nP -iTCP:8019 -sTCP:LISTEN
```
