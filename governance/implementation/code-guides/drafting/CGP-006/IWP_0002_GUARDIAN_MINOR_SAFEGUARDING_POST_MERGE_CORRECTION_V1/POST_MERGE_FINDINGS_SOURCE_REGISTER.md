# Post-Merge Findings Source Register

Status: `TWO_ACCEPTED_IN_SCOPE_MEDIUM_FINDINGS_CORRECTED_PENDING_PROTECTED_MERGE`

Source: PR #71 post-merge Cursor Bugbot review threads observed on `2026-08-01T10:14:21Z`.

## Finding 1

- Title: `Legacy links omitted from expansions`
- Severity: `Medium`
- Bugbot ID: `80b38901-904e-475d-87be-66d21ea8c98f`
- Thread ID: `PRRT_kwDOS5bRRs6Vmf5A`
- Bugbot comment ID: `PRRC_kwDOS5bRRs7cPLYF`
- Acceptance comment ID: `PRRC_kwDOS5bRRs7cPMyM`
- Path: `backend/core/minor_communication.py`
- Additional path: `backend/routes/billing.py`
- Review state before correction merge: `UNRESOLVED`
- Corrective disposition: shared verified Guardian-link expansion helper used by messaging, billing, and recurring-charge owner expansion; unverified, contradictory, and cross-barn legacy links fail closed.

## Finding 2

- Title: `Materialized invoices omit state token`
- Severity: `Medium`
- Bugbot ID: `49c82b71-4410-47af-acac-a842765b9d64`
- Thread ID: `PRRT_kwDOS5bRRs6Vmf5B`
- Bugbot comment ID: `PRRC_kwDOS5bRRs7cPLYH`
- Acceptance comment ID: `PRRC_kwDOS5bRRs7cPM1c`
- Path: `backend/routes/recurring_charges.py`
- Review state before correction merge: `UNRESOLVED`
- Corrective disposition: materialization receives the authoritative gate result, copies the refreshed state token into the invoice, and `invoice.pay` treats missing minor payment tokens as an explicit fail-closed retry condition.

Thread treatment remains pending until the corrective PR is protectedly merged. No PR #71 thread is resolved by this package before protected-branch correction.
