# Legacy Link Expansion Correction Record

Status: `IMPLEMENTED_AND_FOCUSED_TESTED`

Correction:

- Added `guardian_link_barn_proven` as the public wrapper for the central legacy Guardian-link barn provenance rule.
- Added `load_verified_guardian_linked_students` to resolve Guardian-linked students by Guardian user and active barn.
- Included explicit same-barn links.
- Treated `barn_id` null or missing as legacy candidates only.
- Accepted legacy candidates only when the central provenance rule proves the link belongs to the active barn and matching canonical student.
- Rejected cross-barn, ambiguous, unverified, and contradictory provenance.
- Did not manufacture or backfill barn identity.

Callers:

- `backend/core/minor_communication.py` now uses `load_verified_guardian_linked_students` during participant expansion.
- `backend/routes/billing.py` now uses `load_verified_guardian_linked_students` during owner/Guardian payment subject expansion.
- `backend/routes/recurring_charges.py` now uses `load_verified_guardian_linked_students` during owner/Guardian recurring-charge subject expansion.

Focused tests:

- `GMS-T-055` verifies explicit same-barn inclusion, explicit cross-barn exclusion, verified missing-barn legacy inclusion, unverified legacy exclusion, and contradictory provenance exclusion.
- `GMS-T-056` verifies messaging expansion includes verified legacy links and excludes unverified legacy links.
- `GMS-T-057` verifies billing and recurring payment paths use the shared helper instead of exact-barn-only Guardian-link queries.

Preserved safeguards:

- Existing central Guardian/Minor relationship, authority, consent, state-token, and public-error behavior is unchanged except for the narrow subject expansion correction.
- Missing-barn legacy rows are not treated as local without independent provenance.
