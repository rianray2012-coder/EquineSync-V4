# Build-Next-6C — Document Request Foundation

Status: Codex-reviewed and locked.

## Scope

BN6C turns the BN6B document workflow contract into a local template/request
foundation.

Implemented:

- `GET /api/document-signatures/document-types`
- `GET /api/document-signatures/templates`
- `POST /api/document-signatures/templates`
- `GET /api/document-signatures/requests`
- `POST /api/document-signatures/requests`
- `GET /api/document-signatures/requests/{request_id}`
- Forms & Signatures page panels for local document templates and local
  document requests.

Founder-approved recommendations used:

- Template registry plus local request creation.
- Facility `admin` / `barn_manager` users can create templates and requests for
  their own barn.
- Local template/request list and detail reads are manager-only in BN6C because
  request rows carry subject/request metadata. Owner-facing request access is
  deferred to the later signing/recipient experience.
- `provider_template_id` may be stored as a local reference, but it is never
  used to call DocuSign or any other provider in this phase.

## Guardrails

BN6C does not add:

- DocuSign SDK dependency.
- Provider API calls.
- Live envelope creation.
- Signing URL generation.
- Provider webhook receiver.
- Signed-document body or URL storage.
- Legal text storage.
- Hard participation gates.
- Billing, Admin Portal, HorseOps, landing, Stripe, Apple, native, offline, or
  push changes.

All launch effects remain `soft_warning`.

## Privacy

Normal API responses use the BN6B projection helper and strip provider envelope,
signature, and certificate refs by default.

Audit rows use `audit_safe_document_metadata()` and keep counts/status only:

- `required_signer_count`
- `signed_count`
- document type/workflow/provider/status

Audit rows do not include:

- raw legal text,
- provider payloads,
- provider envelope/signature/certificate refs,
- signer user-id lists,
- private notes,
- birthdates,
- tokens or secrets.

## Verification

Focused tests:

- `backend/tests/test_build_next_6c_document_request_foundation.py`
- BN6A + BN6B + BN6C focused suite:
  - `backend/tests/test_build_next_6_signature_connector.py`
  - `backend/tests/test_build_next_6b_document_workflow_contract.py`
  - `backend/tests/test_build_next_6c_document_request_foundation.py`
  - Result: `23 passed`.
  - Round-1 privacy fix adds one source-level guard for manager-only
    template/request reads.
- Python compile passed for:
  - `backend/routes/document_signatures.py`
  - `backend/core/document_workflows.py`
  - `backend/tests/test_build_next_6c_document_request_foundation.py`
- Frontend compile check: after refreshing local `frontend/node_modules` from
  the lockfile, `GENERATE_SOURCEMAP=false CI=true npm run build` completed
  successfully.

Acceptance checks:

- Template creation validates allowed document types only.
- Unknown/custom document type fails closed.
- Request creation computes signer roles for teen and under-13 minor profiles.
- Owner role cannot create local templates/requests.
- Owner/parent roles cannot read local template/request rows in BN6C.
- Audit metadata contains counts/status only.
- Source guards confirm no live signing/provider webhook implementation.

## Package

Expected zip:

- `outputs/build_next_6c_document_request_foundation.zip`

Lock result:

- Codex review found no remaining BN6C findings after the manager-only
  template/request read boundary was patched and verified.
- BN6A + BN6B + BN6C focused suite passed: `23 passed`.

## Deferred

- Live DocuSign envelope creation.
- Embedded recipient signing links.
- Provider webhook status sync.
- Signed PDF retrieval/storage.
- Required-document hard participation gate.
- Template legal copy management and legal approval workflow.
