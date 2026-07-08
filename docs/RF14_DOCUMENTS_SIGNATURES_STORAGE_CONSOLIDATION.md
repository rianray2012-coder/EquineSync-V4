# RF14 Documents, Signatures, and Storage Consolidation

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF14 consolidates EquineSync's document, signature, acknowledgement, signer,
and storage claims without enabling new provider behavior. It keeps the legal
signature path, local acknowledgement path, and document storage path truthful
for launch-readiness review.

## Implemented In RF14

- Guardian-required document requests now require at least one
  `guardian_user_ids` value before a request row is created.
- Document request projections continue to hide signer IDs and provider
  envelope/signature/certificate references by default.
- Digital Forms records normalize explicit truth fields:
  - `signature_scope=local_acknowledgement_only` and
    `legal_signature_status=not_legal_signature` for internal records;
  - `signature_scope=provider_readiness_only` and
    `legal_signature_status=provider_not_sent` for DocuSign-readiness rows.
- Owner portal form acknowledgement remains owner-scoped and records
  `signed_claim=local_acknowledgement_not_legal_signature`.
- Forms & Signatures UI labels records as local acknowledgements and
  signature-provider readiness, not live legal delivery.
- Document scan upload preparation labels storage as upload-intent-only and
  does not claim an external file mutation by RF14.

## Surface Inventory

| Surface | Current Evidence | RF14 Status |
| --- | --- | --- |
| Canonical legal signature workflow | `backend/core/document_workflows.py`, `backend/routes/document_signatures.py` | ready |
| Digital Forms local acknowledgement | `backend/routes/backlog.py`, `frontend/src/pages/FormsSignatures.jsx` | ready |
| Guardian/minor signer handling | `backend/routes/document_signatures.py` | ready, founder/legal review required |
| Owner portal form acknowledgement | `backend/routes/backlog.py` | ready |
| Document scan upload preparation | `backend/routes/backlog.py` | upload intent only |
| Signed document storage/retention/deletion | no production provider mutation in RF14 | deferred |
| Provider/trainer document visibility | RF10/RF14 founder decision | deferred |
| Live DocuSign envelope sending | no provider call in RF14 | deferred |

## Fixed Findings

| Finding | RF14 Fix | Evidence |
| --- | --- | --- |
| Guardian-required document requests could be created without a guardian signer ID. | Request creation now rejects guardian-required workflows when `guardian_user_ids` is empty. | Focused RF14 test covers rejection and successful guardian+subject request creation. |
| Digital Forms could imply legal signature completion. | Digital Forms now carry local acknowledgement/provider-readiness truth fields and UI labels avoid live legal delivery claims. | Backend normalization, owner acknowledgement update, UI label changes, focused RF14 tests. |
| Document scan upload preparation could be mistaken for production storage completion. | Manifest now includes `storage_claim=upload_intent_only_no_external_file_mutation_by_rf14` and an upload-intent-only message. | Focused RF14 upload-intent test and generated report. |

## Deferred Boundaries

| Boundary | Status | Owner |
| --- | --- | --- |
| Production DocuSign envelope sending/signing URLs | deferred | founder/legal/provider phase |
| Signed document archival and retention | deferred | founder/legal/storage phase |
| Production storage provider selection and deletion SLA | deferred | founder/legal/storage phase |
| Provider/trainer document visibility and signer grants | deferred | founder decision |
| Browser/UAT seeded guardian/minor/legal-signature flows | deferred | RF18 after founder/legal acceptance |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Confirm canonical legal-signature source. | requires founder review | Recommended: DocuSign-backed document-signature workflows are the legal-signature readiness path; Digital Forms remain local acknowledgement/readiness only. |
| Confirm guardian/minor signer policy. | requires founder review | RF14 enforces guardian IDs for guardian-required requests; founder/legal should confirm under-13 and 13-17 signing posture. |
| Confirm provider/trainer document scope. | requires founder review | Provider-facing document visibility and signature scope remain deferred until relationship grants and signer rules are accepted. |
| Confirm production storage provider and retention. | requires founder review | RF14 records scan upload intents only; production storage, retention, signed-document archival, and deletion SLAs need owner acceptance. |
| Confirm live DocuSign timing. | requires founder review | RF14 does not send live envelopes; provider activation should wait for credentials, legal approval, native posture, and UAT evidence. |

## Verification

RF14 is verified by:

- focused backend tests in
  `backend/tests/test_rf14_documents_signatures_storage_consolidation.py`;
- report generation through
  `backend/scripts/build_rf14_documents_signatures_storage_consolidation.py`;
- frontend build because RF14 changes Forms & Signatures UI copy;
- package integrity verification against
  `outputs/build_next_rf14_documents_signatures_storage_consolidation.zip`;
- secret-shape scan over RF14 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync has document/signature/storage readiness evidence.
- Guardian-required document requests require guardian IDs before local request
  creation.
- Digital Forms track local acknowledgement or provider readiness only.
- Document scan upload preparation returns upload-intent manifests.

Current launch claims must not say:

- EquineSync has live legal signature delivery, production DocuSign envelope
  sending, production signed-document storage, universal document retention,
  provider/trainer document access, storage deletion SLAs, or provider storage
  mutations implemented by RF14.
