# RF19 Official Staging UAT Evidence Capture Package

Date: 2026-07-07

Status: Prepared for Codex review.

## Scope

RF19 packages the official staging UAT evidence-capture gate after locked RF18.
It does not execute live provider workflows, approve public launch, or mark
founder acceptance.

RF19 includes:

- locked RF18 input evidence checks;
- official staging precondition checks;
- seven UAT evidence rows inherited from RF18;
- blocker rows for missing official staging URL/account/evidence artifacts;
- founder-decision rows for evidence acceptance and rerun/defer decisions.

RF19 does not include:

- production, staging, seeded-demo, or UAT account mutation by Codex;
- provider calls;
- App Store Connect or Google Play Console submission;
- live Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render,
  or storage-provider mutation;
- destructive migration or backfill execution;
- public launch approval;
- founder acceptance auto-marking.

## Evidence

- Proof core:
  `backend/core/rf19_staging_uat_evidence_capture.py`
- Report script:
  `backend/scripts/build_rf19_staging_uat_evidence_capture.py`
- Focused tests:
  `backend/tests/test_rf19_staging_uat_evidence_capture.py`
- Review doc:
  `docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE.md`
- Plan doc:
  `docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE_PLAN.md`
- Generated report:
  `outputs/rf19_staging_uat_evidence_capture_report.md`
- Review package:
  `outputs/build_next_rf19_staging_uat_evidence_capture.zip`

## Review Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf19_staging_uat_evidence_capture.py
.venv/bin/python backend/scripts/build_rf19_staging_uat_evidence_capture.py --zip-output outputs/build_next_rf19_staging_uat_evidence_capture.zip
unzip -t outputs/build_next_rf19_staging_uat_evidence_capture.zip
```

`--fail-on-blockers` is expected to return non-zero until official staging
context and sanitized evidence artifacts are supplied.

## Launch Claim Boundary

Current claims may say RF19 prepared the official staging UAT evidence ledger
and identified the missing staging/evidence inputs.

Current claims must keep launch approval, first-client UAT acceptance, store
availability, native billing compliance, full offline operation, live provider
sync, and migration/backfill completion out of scope for RF19.
