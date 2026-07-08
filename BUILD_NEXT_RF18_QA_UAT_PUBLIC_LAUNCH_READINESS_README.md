# RF18 QA, UAT, Migration, and Public Launch Re-Readiness Package

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Scope

RF18 is an evidence-only QA/UAT/public-launch re-readiness gate across the
locked RF1-RF17 refinement track. It proves source evidence is organized and
launch boundaries are explicit, while keeping public launch no-go until staging
UAT and founder acceptance are actually completed.

RF18 includes:

- locked RF1-RF17 report/doc/package evidence matrix;
- launch-critical source evidence checks;
- overclaim guards for public launch, app-store availability, full offline
  support, native billing, and provider-delivery claims;
- UAT rows for enrollment, owner/guardian visibility, staff/trainer workflows,
  service-provider grants, billing/payment/export truth, documents/messaging,
  field reliability, and native shell smoke;
- migration/backfill classification rows;
- founder-decision rows.

RF18 does not include:

- production, staging, seeded-demo, or UAT account mutation;
- provider calls;
- App Store Connect or Google Play Console submission;
- live Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render,
  or storage-provider mutation;
- destructive migration or backfill execution;
- public launch approval;
- founder acceptance auto-marking.

## Evidence

- Proof core:
  `backend/core/rf18_qa_uat_public_launch_readiness.py`
- Report script:
  `backend/scripts/build_rf18_qa_uat_public_launch_readiness.py`
- Focused tests:
  `backend/tests/test_rf18_qa_uat_public_launch_readiness.py`
- Review doc:
  `docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md`
- Plan doc:
  `docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS_PLAN.md`
- Generated report:
  `outputs/rf18_qa_uat_public_launch_readiness_report.md`
- Review package:
  `outputs/build_next_rf18_qa_uat_public_launch_readiness.zip`

## Review Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf18_qa_uat_public_launch_readiness.py
.venv/bin/python backend/scripts/build_rf18_qa_uat_public_launch_readiness.py --fail-on-blockers --zip-output outputs/build_next_rf18_qa_uat_public_launch_readiness.zip
unzip -t outputs/build_next_rf18_qa_uat_public_launch_readiness.zip
```

## Launch Claim Boundary

Current claims may say RF18 has prepared a source-backed launch-readiness and
UAT evidence ledger across RF1-RF17.

Current claims must keep launch approval, first-client UAT acceptance, store
availability, native billing compliance, full offline operation, live provider
sync, and migration/backfill completion out of scope for RF18.
