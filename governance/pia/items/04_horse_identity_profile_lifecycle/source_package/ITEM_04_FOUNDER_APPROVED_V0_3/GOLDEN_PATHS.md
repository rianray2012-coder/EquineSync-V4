# Item 04 Golden Paths

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source section:** `31. Golden-Path Reproduction Scenarios`
**Execution status:** `DESIGN_SCENARIOS_DEFINED_NOT_EXECUTED`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`


### `HOR-GP-001`: Horse-first onboarding for an individual owner

An individual owner creates a horse candidate with a barn name, approximate age, color, markings, and identity photographs. No Facility or Organization is required. Duplicate review finds no strong match. Asserted facts remain visibly unverified. Later registration and microchip evidence advance specific fields without changing the Horse ID.

### `HOR-GP-002`: Expected foal to independent horse identity

A breeding and pregnancy record identifies sire, genetic dam, recipient mare, breeder, and intended owner as separate references. At live birth, an authorized activation event creates an independent Horse ID linked to the predecessor records. The foal is not collapsed into the dam, recipient mare, breeder, or owner.

### `HOR-GP-003`: Rescue or first-known identity with incomplete history

A rescue creates a first-known horse identity with estimated age, unknown registered name, photographs, markings, and intake location. Unknown facts remain unknown. Later registry evidence links a prior name and identifier through correction and provenance rather than replacing the history.

### `HOR-GP-004`: Move to a new facility

Item 03 validates relationships and authority. Item 02 supplies both location identities. Item 04 records horse-centered location and continuity episodes while preserving the same Horse ID. Items 06, 07, 09, and 10 handle time, care, money, and notices. Former-facility access is recalculated.

### `HOR-GP-005`: Governed duplicate merge and later correction

Two records are reviewed using identifiers, origin, name history, photographs, and records. A separately authorized merge preserves both record IDs and downstream mappings. New evidence later shows an improper convergence; governed unmerge restores two coherent horses without erasing the merge history.

### `HOR-GP-006`: Sale with full continuity

An authorized transfer case validates horse identity, parties, evidence, restrictions, and continuity packet. The sale changes relationship and operational context, not Horse ID. Successor access is established, obsolete access is removed, and unresolved exceptions remain visible until closure.

### `HOR-GP-007`: Competition eligibility handoff

Item 04 records current registry, vaccination-document reference, age, and classification eligibility facts with source and expiry. Item 08 manages show entry; Item 06 manages dates; Item 09 manages fees. Workflow outcomes cannot rewrite canonical eligibility facts.

### `HOR-GP-008`: Retirement, death, memorialization, and archive

Retirement adapts expectations without hiding the horse. Later, an authorized death record preserves identity and history. A voluntary memorial projection contains only permitted content. Archive prevents ordinary mutation while allowing correction, legal hold, and claims. If death was entered incorrectly, an elevated successor correction restores active state and reconciles downstream projections.

### `HOR-GP-009`: Blind cross-tenant transfer handoff

A receiving party enters a purpose-bound transfer token and limited identity evidence. EquineSync performs a blind match and does not reveal the originating tenant or horse record. Item 03 validates the handoff authority. Only the minimum transfer and continuity projection is exchanged. The same canonical identity or governed cross-tenant identity linkage is established according to the approved `HOR-FD-016` decision, with no platform-wide horse directory.

### `HOR-GP-010`: Passport invalidation after a material restriction

An authorized Passport is downloaded with generated time, expiry, watermark, and verification reference. A later restriction makes the projection unsuitable for future reliance. EquineSync blocks new access and returns `REVOKED_FOR_FUTURE_RELIANCE` through the verification mechanism. The audit record remains. The system does not claim that an external copy was remotely erased.
