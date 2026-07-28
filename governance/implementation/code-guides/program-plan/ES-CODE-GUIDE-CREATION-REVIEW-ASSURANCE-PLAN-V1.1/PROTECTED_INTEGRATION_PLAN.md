# Protected Integration Plan

## Accession Branch

Preferred branch:

`codex/code-guide-program-plan-v1-1-accession-v1`

Branch point:

`2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94`

## Required PR Treatment

1. Push the accession branch.
2. Open a draft PR against `integrate-emergent-final-zip`.
3. Verify the PR head.
4. Verify the protected base remains `2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94`.
5. Mark the PR ready only after validation passes.
6. Allow protected checks to run on the current PR head.
7. Merge through protected controls using an expected-head guard.
8. Do not use administrator bypass.
9. Do not force push.
10. Do not merge after protected-base drift.

## Post-Merge Custody

After merge, verify:

- final PR head;
- merge commit;
- merge timestamp;
- protected checks;
- resulting protected head;
- canonical source path;
- approved source hash and size;
- package file count;
- manifest and checksum result;
- historical-source treatment;
- continuing authority boundaries.

Then create a separate custody branch from the exact post-accession protected head.

## Stop Conditions

Stop if:

- protected base head differs from `2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94` before accession merge;
- approved source hash or byte length differs;
- PR #44 is no longer open, draft, unmerged, based on `integrate-emergent-final-zip`, or at `f94c26188e8d35c413b366135df12057b58c2d7d`;
- package-local validation fails;
- required protected checks fail, are stale, pending, cancelled, or not attached to the current PR head.
