# Global Companion Formal Scan Master Report

- P0: `0`
- Open P1: `0`
- Adoption-blocking P2: `0`
- Lock-blocking P2: `0`

| Scan | Result | Notes |
| --- | --- | --- |
| dependency-cycle | PASS | Parsed 31 authoritative upstream edges; prohibited cycles: 0. Reciprocal peer/co-review edges excluded by rule. |
| orphan-requirement | PASS | Checked 232 requirements for source path and authority owner; missing source paths: 0. |
| orphan-control | PASS | Checked 15 target/source records for an authority classification. |
| orphan-Founder-decision | PASS | Checked 71 recovered decisions against RTM rows; orphans: 0. |
| duplicate-ID | PASS | Requirement IDs 232/232 unique; decision IDs 71/71 unique. |
| broken-reference | PASS | Validated every requirement source path; broken paths: 0. |
| stale-version | PASS | Versioned V1.0/V1.1/V1.2 candidates are preserved distinctly; no candidate was silently promoted by this package. |
| authority-owner | PASS | Checked authority owner on 232 requirements. |
| adoption-state consistency | PASS | Recorded adoption state for 15 target/source records; unknown states remain explicit and were not inferred. |
| lock-state consistency | PASS | Recorded lock state for 15 target/source records; unknown states remain explicit and were not inferred. |
| supersession-integrity | PASS | Historical sources and prospective successors are separately classified; no predecessor was overwritten. |
| expired-exception | PASS | Historical provenance exceptions were preserved; no dated exception represented itself as silently expired. |
| checksum-and-path completeness | PASS | Rehashed 15 discovered records; mismatches: 0. |
