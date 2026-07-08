# RF14 Documents, Signatures, and Storage Consolidation Package

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Scope

RF14 is a narrow refinement gate for documents, signatures, acknowledgements,
signer policy, and storage truth. It reconciles the existing DocuSign readiness
foundation, Digital Forms local acknowledgement records, owner portal
acknowledgements, and document scan upload manifests without enabling live
provider behavior.

RF14 includes:

- guardian-required document request enforcement;
- default projection protection for signer IDs and provider references;
- Digital Forms local acknowledgement/provider-readiness truth fields;
- owner-scoped local acknowledgement truth for owner portal form signing;
- Forms & Signatures UI wording that avoids live legal delivery claims;
- document scan upload-intent-only storage claims;
- focused backend tests and a generated RF14 proof report;
- founder-decision rows for legal signature source, guardian/minor signer
  policy, provider document scope, storage retention, and live DocuSign timing.

RF14 does not include:

- DocuSign, Stripe, Apple, Google, Resend, MongoDB Atlas, Vercel, Render, S3,
  Google Drive, UAT, or provider calls;
- live envelope sending, signing URLs, provider callbacks beyond existing
  gated readiness, or signed-document storage;
- broad provider/trainer document access;
- production storage provider selection, retention, or deletion workflows;
- founder acceptance auto-marking.

## Evidence

- Source hardening:
  `backend/routes/document_signatures.py`,
  `backend/routes/backlog.py`,
  `frontend/src/pages/FormsSignatures.jsx`
- Proof core:
  `backend/core/rf14_documents_signatures_storage_consolidation.py`
- Report script:
  `backend/scripts/build_rf14_documents_signatures_storage_consolidation.py`
- Focused tests:
  `backend/tests/test_rf14_documents_signatures_storage_consolidation.py`
- Review doc:
  `docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION.md`
- Generated report:
  `outputs/rf14_documents_signatures_storage_consolidation_report.md`
- Review package:
  `outputs/build_next_rf14_documents_signatures_storage_consolidation.zip`

## Review Command

```bash
.venv/bin/python -m pytest backend/tests/test_rf14_documents_signatures_storage_consolidation.py
.venv/bin/python backend/scripts/build_rf14_documents_signatures_storage_consolidation.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf14_documents_signatures_storage_consolidation.zip
```

## Launch Claim Boundary

Current claims may say EquineSync has document/signature/storage readiness
evidence, guardian-required request enforcement, local acknowledgement truth
labels, and document scan upload-intent manifests.

Current claims must not say EquineSync has live legal signature delivery,
production DocuSign envelope sending, universal signed-document storage,
provider/trainer document access, production storage retention/deletion
workflows, or provider storage mutations implemented by RF14.
