# CGP-005 Source Freeze Assurance Report

**Prompt:** `CGP-005`
**Execution ID:** `CGEXEC-20260726-0004`
**Baseline:** `ff2748796bf858f49a3f85bad0578850e1deb846`

CGP-005 selected all CGP-003 source records mapped to Wave 1 guides and froze their current baseline bytes. File sources are verified by SHA-256 and Git object SHA. Directory sources are verified by tracked-tree aggregate SHA-256 and child-file manifest entries in `governance/implementation/code-guides/source-freeze/WAVE_1_COMMON_SOURCE_FREEZE_MANIFEST.json`.

## Counts

- `CONTROLLING_FROZEN`: `403`
- `SUPPORTING_FROZEN`: `1363`
- `HISTORICAL_FROZEN`: `38`
- `IMPLEMENTATION_EVIDENCE_FROZEN`: `633`
- `EXCLUDED_PROPOSED`: `70`
- `EXCLUDED_BLOCKED`: `4`

- Unique Wave 1 source records: `2511`
- Directory sources with child manifests: `103`
- Child file bindings: `3158`

## Assurance Result

No P0 or P1 source-custody issue was identified. No controlling source is frozen from code, tests, CI, runtime behavior, proposed material, blocked material, or historical-only material. Repository evidence remains implementation evidence only.

CGP-006 was not begun.
