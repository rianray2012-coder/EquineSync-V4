# Runtime Remediation Final Report

## Final disposition

`INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED`

This is not Founder activation approval. No substantive Founder-Orchestrated Review Cycle began.

## Summary

- repository trust: `PASS`
- runtime surfaces tested: interactive CLI and `codex exec --json`
- canary: `PASS` on both required surfaces
- project-agent discovery: `8/8 PASS`
- custom instruction loading: `8/8 PASS`
- individual role registration schema: `8/8 PASS`
- sandbox provenance: `8/8 matched`; network denied in accepted child sessions
- bounded eight-role orchestration: `8/8 PASS` using controlled 3+5 batching
- behavioral calibration: `90/120` accepted; ES-RA-04 and ES-RA-06 failed
- sealed ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3` (`PASS`)
- sealed/package-controlled paths changed: none
- branch merged: no

## Minimum remediation implemented

- added a temporary read-only canary under `.codex/agents/`;
- added an additive runtime-remediation runner that retains the trusted config stack and supplies exact `agent_type` with `fork_turns="none"`;
- added schemas, raw parent outputs, stderr, prompts, timestamps, exit statuses, sanitized child-session provenance, matrices, reports, and integrity manifests under `runtime_remediation/`;
- preserved every failed attempt and retry.

## Sandbox and approval provenance

Accepted read-only roles ran with child `sandbox_policy.type=read-only`. Accepted writable roles ran with `workspace-write` and denied network. The ES-RA-05 probe created only its one authorized disposable file. Workspace-write is not a path-level allowlist, so the narrower location remained a procedural constraint corroborated by the file-diff result.

The noninteractive child sessions recorded `approval_policy=never` even where `on-request` was requested. Because all calibration inputs prohibited network, production, destructive activity, and actions needing escalation, no approval bypass was exercised. This limitation must be reconsidered before any operational activation.

## Unresolved limitations

1. ES-RA-04 and ES-RA-06 need role-specific calibration remediation and fresh accepted behavioral runs.
2. The parent output does not expose a resolved-agent-type field; child session `agent_role` metadata plus the private marker provide the proof.
3. The originating desktop/tool-backed collaboration surface does not expose first-class `agent_type` selection in this task; the supported CLI surfaces were used for reproducible proof.
4. JSONL provenance is not an operating-system syscall audit.
5. No personal-agent copy test was run because project-scoped discovery passed on both required surfaces.

## Disposition boundary

Do not activate, merge, or issue Founder approval from this result. The next permitted action is a narrowly scoped remediation and rerun for ES-RA-04 and ES-RA-06, followed by regeneration of the behavioral aggregate and this disposition.
