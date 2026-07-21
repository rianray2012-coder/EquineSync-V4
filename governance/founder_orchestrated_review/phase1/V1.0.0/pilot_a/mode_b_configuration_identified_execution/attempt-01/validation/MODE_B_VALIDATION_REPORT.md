# Mode B Validation Report

## Deterministic totals

- Mode B preflight: 23 controls — 17 PASS, 3 FAIL, 1 UNVERIFIED, 1 NOT_EXECUTED, 1 UNRESOLVED.
- Required validation register: 22 checks — 15 PASS, 3 FAIL, 2 NOT_EXECUTED, 1 PASS_WITH_DECLARED_BLOCKER, 1 POST_COMMIT_REQUIRED.
- Repository unit tests: 4 passed, 0 failed.
- Disposable-predecessor Phase 1 validator `ES-PH1-VAL-2026-001-RUN-08`: 31 PASS, 1 BLOCKED, 32 total; status `PASS_WITH_DECLARED_BLOCKERS`.

The blocked Phase 1 validator check is `PILOT_ROLE_EXECUTION`, which correctly reports zero canonical roles executed. It does not make this Mode B attempt pass.

## Preserved command failures

The first unit-test command treated `V1.0.0` as a dotted Python module path and failed import. The corrected unittest discovery command passed all four tests. The first disposable-clone validator command was invoked from the clone's parent directory and failed to locate the script. Running the same validator from the cloned repository succeeded. Neither failed invocation was hidden or reclassified.

## Attempt-specific validation

All JSON and CSV artifacts parsed, all four Role Configuration and source hashes matched, every packet declared the hidden oracle and other role material absent, all four packet canaries were unique, no credential-key pattern was found, and predecessor evidence and fixture tree identities matched.

The controlling failures are the original hidden-oracle read and checksum-tool availability results. Behavioral prompt-injection, session-reuse, role-output schema, and hidden-oracle scoring are not available because launching a role after preflight failure was prohibited.

The commit object and remote equality are verified after the one evidence commit is created; those checks cannot truthfully be embedded as pre-commit facts in that same commit.
