# Founder Permission and Rerun Decision Brief

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISION_REQUIRED`
- Decision: `FAC-PERMISSION-FD-001`

## Question

How should the valid fresh segregated review be authorized after the mandatory runtime permission check failed?

## Recommended answer — not Founder doctrine unless expressly adopted

Rerun the review in a new `read-only` parent session with `on-request` approvals, network denied, a complete `PASS` pre-spawn permission record, and the registered ES-RA-02 identity. Have the reviewer return its output to the parent/Evidence Custodian. This follows the existing approved control without creating an exception.

## Alternatives

1. **Narrow express exception:** Rian Ray may authorize a documented exception naming ES-RA-02; verification of commit `a17b82a3896193e355d77e930e300cfd43565409`; the exact non-production environment and data classification; read-only inputs; one narrow evidence output path; prohibited product/network/production actions; start/end time; approver; logging/evidence capture; cleanup; rollback; and revalidation. Broad unrestricted authority is not recommended.
2. **Defer:** retain the package at `FACILITY_PIA_FOUNDER_DECISIONS_INCORPORATED_PENDING_VALID_FRESH_SEGREGATED_REVIEW` until a compliant environment is available.

## Risk if unresolved

The package cannot validly claim fresh segregated-review pass or readiness for Founder design approval. Proceeding would create misleading assurance and violate repository runtime controls.

## Founder input

`FOUNDER_DECISION_REQUIRED` — no answer inferred from silence. All unaffected documentary work is complete and preserved.
