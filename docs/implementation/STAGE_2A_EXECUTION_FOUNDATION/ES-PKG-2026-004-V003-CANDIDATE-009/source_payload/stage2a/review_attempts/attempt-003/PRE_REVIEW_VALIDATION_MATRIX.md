# Corrected Candidate Pre-Review Validation Matrix

- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-003`
- Frozen payload: `121`
- Frozen physical files / archive entries: `124/124`
- Manifest SHA-256: `f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc`
- Frozen archive SHA-256: `86d87ca6d289f9ca3b3b3c48e565781469a553d8219b0c8a720b60aebf034ec0`
- Package validation: `PASS — 23/23`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The packaged validator passed from the package root, a nested review directory, and an external `/private/tmp` invocation. The source and packaged validator copies produced identical results when invoked from the repository root. SHA-256 values for every validation output are recorded in the JSON companion.

The archived failed candidate was independently rechecked immediately after the corrected freeze. Its original manifest and archive SHA-256 values remain unchanged. No validation invocation modified either candidate.
