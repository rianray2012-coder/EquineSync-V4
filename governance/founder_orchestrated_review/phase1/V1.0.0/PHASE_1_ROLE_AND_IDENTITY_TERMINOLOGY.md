# Phase 1 Role and Identity Terminology

- `ROLE_CONFIGURATION`: approved instructions, restrictions, tools, schemas, boundaries, authority, and prohibited authority assigned to one ES-RA role.
- `ROLE_EXECUTION`: one bounded invocation using a specific version of a Role Configuration.
- `EXECUTION_IDENTITY`: execution ID, role ID, configuration version and checksum, model, provider, runtime, input manifest, permissions, timestamps, outputs, validation evidence, and output hashes.
- `REVIEWER_IDENTITY`: a separately identifiable natural person or legally or organizationally distinct reviewer. Neither a Role Configuration nor Execution Identity proves it.
- `BLIND_INITIAL_OUTPUT`: an initial substantive output sealed before receipt of another blind reviewer’s output.
- `FROZEN_CANDIDATE`: uniquely identified read-only review bytes plus a deterministic manifest.
- `RECONCILIATION`: post-sealing comparison that preserves each original finding and conflict.
- `CONFIGURATION_IDENTIFIED_AND_PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW`: the accurate description of a qualifying Phase 1 process.
- `MIAP`: Master Implementation Atlas Program.
- `PIA`: Product Implementation Atlas operating beneath and within MIAP.

“Coordinator” describes a workflow function. It is not a canonical ES-RA role in Framework V1.3 and cannot be used to rename ES-RA-08, the Executable Golden-Path Reproduction Controller.
