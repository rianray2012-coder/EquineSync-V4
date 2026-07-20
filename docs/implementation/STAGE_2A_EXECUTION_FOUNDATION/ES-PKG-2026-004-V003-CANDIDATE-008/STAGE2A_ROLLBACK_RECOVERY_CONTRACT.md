# Stage 2A Rollback and Recovery Contract

- Package: `ES-PKG-2026-004-V003`
- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-008`
- Branch: `codex/stage2a-execution-foundation-remediation`
- Starting commit: `0be6172a28b75238c5facabf91d43ed09aaf0d54`
- F-0001: `F0001_REMAINS_OPEN_BLOCKING`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`
- Principal disposition: `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`

A durable recovery artifact survives a complete process stop/restart. The rehearsal restores datastore state, verifies exact digests, tests source restore in a disposable clone, and records the no-external-session/cache determination.
