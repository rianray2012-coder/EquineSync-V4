# Stage 2A Segregated Rereview — Attempt 009

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-009`
- Review source: frozen archive extracted only to disposable `/private/tmp` locations
- Repository candidate executed or imported: `NO`
- Completed UTC: `2026-07-20T12:00:45Z`
- Technical package-control result: `PASS`
- Recommendation: `PASS_RECOMMEND_ACCEPTANCE_AND_CONTROLLED_FINDING_CLOSURE`
- Overall readiness: `BLOCKED_BY_RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE`
- Technical findings: `P0 0 / P1 0 / P2 0`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`
- Self-closure: `NO`

## Frozen archive and read-only boundary

The frozen archive SHA-256 is `10a23100b1ccdcab2b7b05f5aa9deb1d5373b817fceb532d5474d6750e452a81`. Its internal manifest SHA-256 is `e2603777776a534abf23fe06efe26e92f35342c568be2c3c736f60909aa9f3be`; all 285 payload rows verified. The archive contains 288 physical files, no symlinks, and no unsafe paths. Clean extraction produced exact `288/288` byte parity with no missing, extra, or mismatched files.

The independently defined candidate tree digest—SHA-256 over sorted `relative-path NUL file-SHA256 newline` records—is `7f12cb7c3240e9fa4ca0d2f163009f21327b18ba60b9eb963700fa0a5c04f874`. Archive, manifest, and tree hashes remained unchanged after review. No Python bytecode residue was created.

No code was executed or imported from the repository candidate directory. Every validator and unit-control execution used a disposable extraction with `PYTHONDONTWRITEBYTECODE=1`. Temporary mutation copies were discarded.

## Validator and structural controls

The frozen packaged validator passed `23/23` from four invocation classes, all in `DETACHED_PACKAGE_SOURCE_PAYLOAD` mode:

1. Extracted package root — stdout SHA-256 `1021ba675b5e053ab0d418ea3f63b2bb3b4c790ae979457391f98bdbeabb34ba`.
2. Extracted nested `review_attempts/attempt-004` — stdout SHA-256 `4f51eff7d214b0b9955300710e56e50a5da154762f022cf072b1c57a4a59c629`.
3. External `/private/tmp` working directory — stdout SHA-256 `b6c668c8a1abc817ee8bbd3aba321702b9b151f2fa98fc50f277094495b1dc93`.
4. A second fresh temporary extraction — stdout SHA-256 `2e3e0a2c185265b43654f6f9050d307b52e47f3498baf75e8cbf54ab719e3bee`.

Every stderr stream was empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Independent structural checks passed:

- 131 JSON files parse; six CSV files contain 199 data rows.
- Exact JSON/CSV row-and-field parity holds for source 143, requirement 9, test 26, finding 5, provider 11, and F-0002 closure-evidence 5.
- All 143 detached source-payload files match their registered SHA-256 values.
- Traceability resolves nine requirements, five findings, 26 registered executable controls, and 115 output mappings without dangling references or generic all-requirement mappings.
- The two reused predecessor artifacts match their recorded SHA-256 values and remain explicitly noncontrolling. Five prior blocker checks are invalidated and five corrected-candidate reruns are recorded. `MV-016C` passes.

## Provider and startup semantics

The 11 provider events independently recompute to final chain SHA-256 `3774229e4f584a7714ff30fd611fb74877c78e8926e2341c4dc5aba3009eb937`. They bind to guard session `9a545fc415554dab98a6c1537ad0a621`, API PID/PGID `99186`, and registry SHA-256 `596a1707b8060e37c7dcbe3e42399173a928768521e22806818744bbef1db895`. Registry fields, reasons, configuration presence, boundary states, process fields, UTC timestamps, terminal arithmetic, provider summary rows, and proof fields all agree.

Outcomes are attempted 0, succeeded 0, failed 0, skipped 4, timed out 0, and unavailable 7. Network-attempt events and unattributed attempts are both zero.

The earlier semantic weaknesses now fail closed:

- Targeted frozen-source tests reject fully rehashed terminal-outcome, reason-code, PID-binding, and boundary-state mutations.
- Removing all embedded provider-event arrays and zeroing their counts and chain heads causes `MV-016A-provider-startup-measurement` to fail with coverage, binding, semantic, derivation, and proof errors.

Startup evidence matches its oracle: zero startup document writes and zero provider attempts. Four startup event records reconcile to three entered attempts—two succeeded and one failed—plus one unentered alternate profile classified skipped. None timed out or was unavailable.

## Evidence, redaction, and process identity

Both execution-evidence examples pass independent record-content hash and stdout/stderr hash recomputation. Expected and actual exit results agree: 0 for the pass fixture and 7 for the expected-failure fixture. Both result records correctly report `PASS`; semantic projections match before and after redaction, meaning is preserved, and unredacted sensitive matches are zero.

Packaged process evidence passes independent checks for PID/PGID equality, controlled ports, UTC identity timestamps, stable working directory `REPOSITORY_ROOT/stage2a`, stable runtime path, listener attribution, packaged command hashes, foreign-listener absence, and two-process controlled shutdown. Five targeted pure controls passed, covering provider rehash semantics and process command, group, timestamp, reparenting, and pre-listener termination boundaries.

Forging the packaged API command hash to 64 zeroes and changing its working directory to `/forged/c009/path` causes `MV-016B-process-identity` to fail with packaged identity and command/hash semantic errors. The control is now fail closed.

The full 36-test source suite has a noncontrolling detached-context limitation: 34 tests pass, while one test assumes a repository root and one historical mutation test hard-codes a Candidate 006 repository path. Their control objectives were independently satisfied against the current frozen Candidate 009 by four-location detached validation, current-package mutation checks, and five targeted runtime tests. This does not alter the package-control pass, but it is recorded rather than hidden.

## Failed Candidate 007 and Candidate 008 preservation

Candidate 007 remains preserved at archive SHA-256 `e89cbed1ac280e1acb4c9a2105177037a5b2335afe8f4f9df38ab3033902c04e` and internal-manifest SHA-256 `cb63e7e2da83368ad737ade7cc3b37d4b6b4281b4a6ab2dc6770f3e481964f1d`. All 274 manifest rows verify across 277 physical files, and its failed pre-review disposition records are present in Candidate 009's source payload.

Candidate 008 remains preserved at failed-assembly archive SHA-256 `d94da934bd820ed246f83e1a60453290c4178f6d15d57223103ee361fb61c9ca` and external-manifest SHA-256 `3f25672a322741603632b8c6b56522fce4eec807489ae18cde55c38a10101917`. All 282 manifest rows verify against all 282 archive files, and its failed-assembly records are present in Candidate 009's source payload.

## Five named blocker dispositions

This review recommends authorized controlled closure for all five technical package blockers. It does not self-close them.

- `ES-ADV-V003-R2-F-0004` — validator root resolution: `REMEDIATION_VERIFIED`; recommend authorized closure.
- `ES-ADV-V003-R2-F-0003` — traceability specificity: `REMEDIATION_VERIFIED`; recommend authorized closure.
- `ES-ADV-V003-R2-F-0001` — provider/startup measurement: `REMEDIATION_VERIFIED`; recommend authorized closure. This is the prior technical provider finding, not the separate readiness record named F-0001.
- `ES-ADV-V003-R2-F-0002` — evidence semantics and redaction: `REMEDIATION_VERIFIED`; recommend authorized closure.
- `ES-ADV-V003-R2-F-0005` — process identity and process-group verification: `REMEDIATION_VERIFIED`; recommend authorized closure.

## Package-control pass versus overall readiness

The package-control result is `PASS`. That result does not resolve or self-close the separate `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE` limitation. Its status remains `OPEN_BLOCKING_RUNTIME_LIMITATION`; direct evidence of resolution is false, and `F0001_REMAINS_OPEN_BLOCKING`.

The historical Mongo residue is separately classified `SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE`, attributed to a verified temporary segregated-review clone, contained and terminated with the port cleared. The orchestrator correctly refused the unverified foreign-path process. Its causal relationship to the runtime-selector limitation is `NOT_ESTABLISHED_DO_NOT_CONFLATE`, and no causal influence on the accepted reruns was established.

Therefore overall Stage 2A readiness remains blocked, `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`, `EXECUTION_NOT_AUTHORIZED`, and `NOT_EXTERNALLY_ASSURED`, notwithstanding the Candidate 009 package-control pass.
