# Post-Merge Findings Correction Custody Record

Status: `TWO_POST_MERGE_FINDINGS_CORRECTED`

Corrected findings:

- `Legacy links omitted from expansions` (`PRRT_kwDOS5bRRs6Vmf5A`, Bugbot `80b38901-904e-475d-87be-66d21ea8c98f`): PR #75 introduced `load_verified_guardian_linked_students`, applies the central verified barn-provenance rule to null or missing `barn_id` legacy candidates, rejects cross-barn, ambiguous, unverified, and contradictory links, and uses the helper in messaging and billing Guardian expansion.
- `Materialized invoices omit state token` (`PRRT_kwDOS5bRRs6Vmf5B`, Bugbot `49c82b71-4410-47af-acac-a842765b9d64`): PR #75 returns the authoritative payment-gate result to recurring-charge materialization, copies the refreshed `guardian_guard_state_token` into materialized invoices, and makes `invoice.pay` pass the invoice token as `expected_state_token` so stale or missing authorization fails closed.

Correction evidence paths:

- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/LEGACY_LINK_EXPANSION_CORRECTION_RECORD.md`
- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/STATE_TOKEN_PROPAGATION_CORRECTION_RECORD.md`
- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/FOCUSED_TEST_RESULTS.csv`
- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/PRIOR_SAFEGUARD_REGRESSION_RESULTS.csv`
- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/POSITIVE_CONTROL_RESULTS.csv`
- `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/VALIDATION_REPORT.md`

No dependency, lockfile, CI, branch-protection, destructive schema, provider, production-backfill, deployment, staging, pilot, production, Wave 2, CGP-007, GAP_0004, or unrelated PR #67/#68/#69 change is recorded.
