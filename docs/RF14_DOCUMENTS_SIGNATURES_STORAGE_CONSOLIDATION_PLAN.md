# RF14 Documents, Signatures, and Storage Consolidation Plan

Date: 2026-07-07

Status: superseded by locked RF14 evidence.

## Purpose

RF14 should make EquineSync document, signature, acknowledgement, signer-rule,
and storage claims truthful. It should separate legal signature workflows from
local acknowledgement/readiness records, prove owner/guardian/minor/provider
signer visibility, and record storage/provider boundaries without calling
DocuSign, Google Drive, S3, Vercel, Render, MongoDB Atlas, or UAT systems.

## Locked Inputs

- RF6 records Document Signatures as canonical legal-signature workflow truth;
  Digital Forms remains local acknowledgement/readiness until RF14.
- RF7 protects owner, guardian, and client document/request visibility.
- RF10 defers provider documents/signatures/storage truth to RF14.
- RF13 locks messaging/notification truth without provider delivery.
- BN6A-BN6E document-provider work remains a prior locked evidence chain; RF14
  must not turn sandbox/provider readiness into a production signature claim.

## Strict Scope

RF14 may:

- inventory document, file, digital-form, signature, acknowledgement, upload,
  scan, provider, owner/guardian, and service-provider document surfaces;
- identify canonical document/signature sources and noncanonical/readiness
  surfaces;
- harden backend-authoritative signer/recipient projections where existing
  data supports safe narrow fixes;
- add focused tests for guardian/minor signer rules, owner-safe document reads,
  provider document visibility, and local acknowledgement truth;
- make labels truthful where behavior is local acknowledgement, upload
  preparation, manifest readiness, or sandbox/provider readiness only;
- produce an RF14 report, review package, and founder-decision rows.

RF14 must not:

- call DocuSign, Google Drive, S3, Vercel, Render, MongoDB Atlas, Resend,
  Stripe, Apple, Google, QuickBooks, or UAT systems;
- create, send, void, download, store, or mutate live legal envelopes,
  provider documents, external files, signatures, templates, folders, or
  provider credentials;
- broaden owner, guardian, rider, staff, trainer, or provider document access;
- implement broad storage migration or delete legacy document records;
- auto-mark founder decisions accepted.

## Candidate Evidence Targets

| Area | RF14 Question | Expected RF14 Output |
| --- | --- | --- |
| Canonical document system | Which route/collection owns legal document and signature truth? | Decision table separating canonical, local acknowledgement, readiness, provider, and deferred surfaces. |
| Digital Forms | Are local forms confused with legal signatures? | Truthful labels/tests showing local acknowledgement or provider-readiness only. |
| Guardian/minor signer rules | Are minor/guardian requirements backend enforced or explicitly deferred? | Tests or founder-decision rows for guardian-required signing. |
| Owner document visibility | Can owners/guardians only see linked/recipient-scoped documents? | Focused backend tests for same-barn and cross-owner denial. |
| Provider documents | Can providers access only grant-scoped documents? | Scoped evidence or deferred founder-decision rows. |
| Upload/storage readiness | Are upload/scan/storage claims provider-readiness only unless real storage is wired? | Manifest/proof rows and no live storage provider calls. |
| Signature provider boundary | Are DocuSign/sandbox readiness and live envelope claims separated? | BN6 cross-reference and stale-copy scan preventing live-signature overclaims. |

## Acceptance Criteria

- RF14 report status is `ready` with zero blocker rows, or any blocker is
  explicitly recorded as `blocked` rather than hidden.
- Legal signatures, local acknowledgements, upload preparation, document scans,
  and provider readiness have truthful labels.
- Document/signature reads and signer projections are backend scoped by stable
  IDs where RF14 claims access control.
- Guardian/minor signer rules are enforced in source or recorded as deferred
  founder/UAT work without stronger launch claims.
- No live provider calls or external file/signature/storage mutations occur
  during RF14.
- Focused RF14 tests pass.
- Report generation passes.
- Zip integrity passes.
- Secret-shape scan is clean.
- Expected files only.

## Founder Decision Rows To Include

| Decision | Status | Notes |
| --- | --- | --- |
| Decide canonical legal-signature source. | requires founder review | Recommended: Document Signatures owns legal signature truth; Digital Forms remains local acknowledgement/readiness until upgraded. |
| Decide guardian/minor signer policy. | requires founder review | Confirm when guardian signatures are required, whether minors can acknowledge, and how signed authority is audited. |
| Decide provider document scope. | requires founder review | Confirm whether service providers can view/upload/sign documents and under which horse/provider grants. |
| Decide storage provider and retention posture. | requires founder review | Choose whether pilot uses local manifest/upload preparation or a live storage provider. |
| Decide live DocuSign timing. | requires founder review | RF14 should not convert sandbox/provider readiness into live envelope submission without explicit approval. |

## Suggested RF14 Files

- `BUILD_NEXT_RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION_README.md`
- `docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION.md`
- `backend/core/rf14_documents_signatures_storage_consolidation.py`
- `backend/scripts/build_rf14_documents_signatures_storage_consolidation.py`
- `backend/tests/test_rf14_documents_signatures_storage_consolidation.py`
- `outputs/rf14_documents_signatures_storage_consolidation_report.md`
- `outputs/build_next_rf14_documents_signatures_storage_consolidation.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf14_documents_signatures_storage_consolidation.py
.venv/bin/python backend/scripts/build_rf14_documents_signatures_storage_consolidation.py --fail-on-blockers
unzip -t outputs/build_next_rf14_documents_signatures_storage_consolidation.zip
```
