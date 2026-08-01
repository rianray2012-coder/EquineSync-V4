# Payment Subject Resolution Evidence

Status: `CORRECTED`

Invoice and recurring-charge payment guards now resolve guarded payment subjects from:

- explicit `student_profile_id`;
- explicit `rider_id`;
- `horse_id` to rider to student;
- owner rows with a student profile relationship; and
- active guardian links for the invoice or recurring-charge owner.

If a resolved rider has no age, birthdate, or canonical student linkage, the route represents the rider as an unknown-age guarded subject instead of dropping the subject. Ordinary adult-owner or business invoices with no student, rider, horse-to-rider, or guardian-link evidence remain functional.

Evidence:

- `GMS-T-030`: minor payment defaults to denied without billing consent.
- `GMS-T-031`: payment outside approved scope denies.
- `GMS-T-048`: stale token after consent withdrawal denies.
- `GMS-T-052`: billing and recurring routes no longer skip unknown riders.
- `GMS-T-053`: payment create can use stable student/workflow consent.

No provider call was made or authorized.
