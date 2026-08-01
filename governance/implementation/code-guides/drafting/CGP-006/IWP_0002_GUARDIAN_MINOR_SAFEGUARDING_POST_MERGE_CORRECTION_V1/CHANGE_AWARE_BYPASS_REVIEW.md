# Change-Aware Bypass Review

Status: `NO_KNOWN_BYPASS_REMAINING_IN_CORRECTIVE_SCOPE_PENDING_PR_REVIEW`

Reviewed bypass questions:

- Can a missing-barn legacy Guardian link be treated as local without proof?
  - Disposition: no. `load_verified_guardian_linked_students` loads null/missing barn candidates but applies the central provenance rule before returning a student.
- Can contradictory legacy provenance be accepted when one field matches the active barn?
  - Disposition: no. Populated provenance barn fields must collapse to the single active barn value.
- Can messaging omit `student_profile_id` and miss a verified legacy Guardian-linked minor?
  - Disposition: no. Participant expansion uses the shared helper for Guardian users.
- Can owner-based billing or recurring-charge subject discovery omit verified legacy Guardian-linked students?
  - Disposition: no. Both payment callers use the shared helper.
- Can materialized recurring invoices omit the token needed for later commit-time revalidation?
  - Disposition: no. The materializer copies `gate.get("state_token")` from the final authorization decision.
- Can a legacy minor-involved invoice without a stored token pay silently?
  - Disposition: no. `invoice.pay` supplies an explicit missing-token sentinel and receives the disclosure-safe authorization-changed retry result.
- Did the correction weaken prior PR #71 safeguards?
  - Disposition: no known weakening found in direct GMS-T-001 through GMS-T-059 execution.

Remaining gate:

The corrective PR must still receive GitHub checks and review. Any valid in-scope High, Medium, P0, P1, or P2 finding must be corrected before protected merge.
