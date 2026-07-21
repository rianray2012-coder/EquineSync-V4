# Phase 1 Replay and Variance Standard

A replay receives a new execution ID and references the original. Record both profile hashes, input hashes, model/provider/runtime identifiers, permissions, available generation settings, output schemas, detected and omitted findings, new findings, severity changes, conclusion changes, and evaluation method.

Use one variance class: `NO_MATERIAL_VARIANCE`, `MINOR_NONDISPOSITIVE_VARIANCE`, `MATERIAL_FINDING_VARIANCE`, `MATERIAL_DISPOSITION_VARIANCE`, or `REPLAY_INVALID`.

Byte-identical LLM output is neither required nor claimed. A changed profile, candidate, input set, permission boundary, unauthorized predecessor output, or unresolved runtime identity makes the replay invalid. Material finding or disposition variance is preserved and escalated; it is never silently averaged.
