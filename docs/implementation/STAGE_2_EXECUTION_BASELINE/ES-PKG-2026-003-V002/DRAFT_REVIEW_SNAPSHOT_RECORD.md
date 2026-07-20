# Draft Review Snapshot Record

- Package: `ES-PKG-2026-003-V002`
- Frozen UTC: `2026-07-20T03:47:59Z`
- Listed files: `80`
- Manifest: `DRAFT_REVIEW_SNAPSHOT_SHA256SUMS.txt`
- Manifest SHA-256: `51b59d9dd3794db7486fb12da67aa2913b725058c47c3d648498b32ee0b8a3a6`
- Purpose: segregated and adversarial read-only review
- Execution: not performed

## Reproduction algorithm

Select every regular file recursively except the three snapshot-control files. Normalize each to a package-relative POSIX path, sort lexicographically, and emit lowercase SHA-256, two ASCII spaces, the path, and LF. Hash the exact manifest bytes with SHA-256. Any listed-file change invalidates the review and requires a new freeze and both reviews.
