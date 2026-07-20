# Candidate 005 Assembly Failure Preservation

`ES-PKG-2026-004-V003-CANDIDATE-005` is preserved as a distinct pre-freeze failed assembly. Its `249` files were not modified during preservation. Repository-backed validation passed all three supported locations, but detached clean-copy validation scored `22/23` because dynamic imports created two bytecode-cache files inside `source_payload`, causing `MV-011-source-register` to fail closed.

- Manifest SHA-256: `a0937895498704028cf8f450f18555ac7b54b5417a96248d62702a6fa7aff75f`
- Archive SHA-256: `41cc9ae595dbe640cc9aedf79fe84267d58ddb84355682626e237eccd5d3595c`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`
