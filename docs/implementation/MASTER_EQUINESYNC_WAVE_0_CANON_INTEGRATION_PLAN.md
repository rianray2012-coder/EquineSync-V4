# Master EquineSync Wave 0 Canon Integration Plan

## Authority

- Decision: `MEIA-FD02`
- Disposition: `APPROVE_WITH_MODIFICATION`
- Wave state: `AUTHORIZED_FOR_CONTROLLED_CANON_INTEGRATION_AND_LOCK`
- Runtime, production and launch authority: `FALSE`

## Integration sequence

1. Inventory current controlling, adopted, locked, candidate, historical, superseded, and planning-only artifacts.
2. Verify checksums and preserve locked/canonical bytes.
3. Reconcile current Canon Index, state, dependency, authority, ownership, findings, lock, and artifact registries.
4. Remove obsolete intermediate state claims from current indexes while preserving their source artifacts.
5. Record `MEIA-FD02` and Wave 0 authority in Atlas decision and program records without adopting the Atlas.
6. Validate paths, dependencies, authority cycles, source preservation, structured data, Markdown, and diff hygiene.
7. Produce the required reports, manifest, checksums, and independently verified lock archive.
8. Lock Wave 0 only if P0 is zero and no P1 blocks integration.

## Artifact set

The review set contains 31 authority-bearing or state-bearing artifacts: 14 constitutional/domain entries, seven current governance registries/instruments, five ATLAS state records, four RF27-RF30 baseline records, and the ATLAS5 controlled-intake record.

## Stop rules

Stop only the affected integration for checksum mismatch, unclear authority, conflicting controlling sources, locked-byte mutation, unsupported authority, or prohibited runtime/production activity. Classify unresolved artifacts conservatively rather than promoting them.

## Exit state

If validation passes: `WAVE_0_LOCKED`, `COMPLETE`, with implementation and production authority remaining false.
