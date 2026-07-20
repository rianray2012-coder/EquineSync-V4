# Candidate 004 Assembly Attempt 001 — Failed Closed

- Detected: `2026-07-20T08:32:15Z`
- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-004`
- Implementation commit: `91a900b84060ef611564e9a730c5968f2eb216d7`
- Result: `FAIL_CLOSED_NOT_FROZEN`
- Validator score: `22/24`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The one-time builder stopped before freeze because `MV-008-forbidden-status` and `MV-010-secret-values` failed in all four invocation locations. The failures were traced to the validator scanning immutable source-payload detection rules as active status assertions and treating bare detector prefixes as actual secret values.

The 197-file partial assembly was never frozen, reviewed, promoted, or represented as a candidate result. No runtime remained active and neither prior failed freeze changed. The validator is corrected in source, tested, committed, and the unfrozen Candidate 004 directory is rebuilt from source rather than edited in place.
