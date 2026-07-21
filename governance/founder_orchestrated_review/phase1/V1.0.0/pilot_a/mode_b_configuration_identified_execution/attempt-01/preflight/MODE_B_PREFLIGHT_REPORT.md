# Mode B Preflight Report

**Attempt:** `ES-PH1-PILOT-A-MODE-B-ATTEMPT-01`  
**Mode:** `CONFIGURATION_IDENTIFIED_MANUAL_ROLE_EXECUTION`  
**Predecessor:** `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`  
**Result:** `FAILED — ROLE EXECUTION PROHIBITED`

## Outcome

Attempt 01 failed before any role invocation. ES-RA-02, ES-RA-03, ES-RA-04, and ES-RA-05 were not attempted, executed, or qualified.

The original host-enforced boundary probe produced two blocking failures for every role:

1. The hidden oracle was readable (`exit 0`) because the fresh clone and oracle were under `/tmp`, a location readable through the active macOS runtime baseline.
2. The authorized `shasum` utility could not start (`exit 134`) because its required system Perl dynamic library was outside the read allowlist.

The same probe correctly denied sibling packet reads, credential-store reads, writes outside the assigned output directory, and network name resolution. It permitted assigned output writes.

## Bounded corrective observation

Relocating the clone outside `/tmp` and adding read-only access to `/System/Library/Perl` caused a representative ES-RA-04 probe to deny the oracle read (`exit 1`) and permit the authorized checksum command (`exit 0`). This is recorded only as a candidate control change for a separately authorized attempt.

It does not make Attempt 01 pass. The Founder directive requires a failed preflight to be preserved and prohibits consuming another retry without express authorization. No role was launched against the corrected candidate configuration.

## Other measured controls

- All four canonical Role Configuration source, file, payload, packet, manifest, and control-envelope hashes were recorded.
- Each packet contains only its own unique canary; no cross-role canary was present.
- Every output directory remained empty.
- Plugins resolved to an empty installed/available set when disabled.
- All five configured MCP entries resolved disabled.
- Apps/connectors, browsers, computer use, remote plugins, memories, hooks, goals, multi-agent features, image generation, skill dependency installation, and workspace dependencies resolved disabled.
- The ChatGPT authentication file existed for the host-owned provider connection but was denied to the sandboxed role command.
- A prompt-input probe showed no inherited drafting conversation and no previous role outputs. It did show host baseline developer and skill-description material, so the acceptability of that additional baseline context remains unresolved.
- The requested no-history, no-analytics, no-feedback, and no-OpenTelemetry overrides parsed successfully. Effective role-invocation tracing behavior was not observed because role execution was prohibited.

## Controlling disposition

`PILOT_A_CONFIGURATION_IDENTIFIED_EXECUTION_BLOCKED`

The supported assurance classification remains `AI_ASSISTED_DOCUMENT_PREPARATION`. The attempt does not support `SINGLE_EXECUTION_AI_REVIEW` or `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW`.
