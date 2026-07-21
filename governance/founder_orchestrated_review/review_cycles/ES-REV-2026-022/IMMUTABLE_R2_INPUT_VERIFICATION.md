# Immutable R2 Input Verification

## Result

`R2_INPUT_VERIFIED_UNCHANGED`

Verification occurred before the successor branch received review-cycle evidence and before any role launch was attempted.

## Identity

- Commit: `56b0a88722d983e05baec0d3b1ea5b7b88c24001`
- Tree: `a60e900c2d0eef17c1f1b8a98f01f5ff1e30647d`
- Package revision: `1.0.1-R2`
- Package files: `66`
- `PACKAGE_MANIFEST.json` SHA-256: `fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527`
- Prior blocked ZIP SHA-256: `f99bbe6de544b1bd688b0c283a75608471c499c63d6745f595f1e522756cd5a8`

## Deterministic checks

- Package checksum entries: all `OK`.
- Package validator: `25/25 PASSED`, `0 FAILED`.
- Sealed-source modifications: `0` according to `MV-016-sealed-sources`.
- Original relied sources: `39/39` hashes reproduced from the exact R2 commit objects.
- Mandatory source gaps requiring a new Founder design decision: `0` according to `MV-020A` and `MV-020B`.
- Identity and Relationships successor incorporation: explicitly `false` according to `MV-020-identity-segregation`.
- Machine-readable source-gap parity correction: deterministic check passed.
- FAC-FD-001 through FAC-FD-018 design-decision population: `18/18` present with implementation, adoption, and lock authority remaining false.

## Sparse checkout handling

The clean clone is sparse. A first filesystem-only source check resolved only 5 of the 39 original relied sources because 34 repository paths were intentionally absent from the sparse worktree. That check was not treated as a provenance failure. The authoritative verification was rerun against the exact Git objects at commit `56b0a88722d983e05baec0d3b1ea5b7b88c24001`; all 39 hashes matched.

## Boundary

These deterministic intake checks verify package identity and internal mechanical consistency. They are orchestrator intake evidence, not an ES-RA-04 Machine Validation Agent run, not an independent review, and not proof that the Facility PIA is substantively correct or implementation-ready.
