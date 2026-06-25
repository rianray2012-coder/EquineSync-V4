# Build-Next-6B - Document Workflow Provider Contract

Status: ready for Codex review.

## Purpose

Build-Next-6B defines the real document workflow contract that will sit between
EquineSync and a third-party e-signature provider such as DocuSign. It keeps
the founder-approved hybrid model from BN6A:

- legal documents use third-party provider signatures;
- lower-risk operating acknowledgements stay in EquineSync.

This phase is still not a live signing implementation.

## What Shipped

- `backend/core/document_workflows.py`
  - launch document type matrix;
  - provider vs in-house workflow classification;
  - future collection/schema field constants;
  - adult/minor/guardian signer-routing helper;
  - provider-status to local-status mapping;
  - safe provider-envelope contract preview;
  - response projection scrubber;
  - audit-safe metadata scrubber.

- `backend/tests/test_build_next_6b_document_workflow_contract.py`
  - pins the document matrix;
  - verifies minor/guardian signer-routing behavior;
  - verifies provider status mapping;
  - verifies private provider/document data is stripped from projections;
  - verifies audit metadata keeps counts/status only;
  - guards against live envelope/provider-webhook implementation.

## Launch Document Matrix

Third-party provider-signature documents:

- General liability waiver.
- Minor participant liability waiver.
- Media / photo release.
- Emergency veterinary care authorization.
- Lesson program agreement.
- Boarding / facility services agreement.
- Trainer / service-provider agreement.

In-house acknowledgement documents:

- Arena / facility rules acknowledgement.
- Community program acknowledgement.
- Onboarding policy acknowledgement.

All document types default to `soft_warning` launch behavior. No hard
participation block is introduced in BN6B.

## Signer Routing Contract

- Adult subjects sign for themselves.
- Under-13 subjects remain parent-managed; guardian signs, subject does not.
- 13-17 and unknown-age subjects require a guardian and may also have a subject
  signer role for the later UX phase.
- Facility countersignature is required only for selected agreements such as
  lesson program, boarding/facility services, and trainer/service-provider
  agreements.
- Platform countersignature remains false for launch unless a later phase
  explicitly approves it.

## Provider Lifecycle Contract

Future DocuSign statuses map to local statuses:

- `created` -> `draft`
- `sent` -> `sent`
- `delivered` -> `viewed`
- `completed` -> `completed`
- `declined` -> `declined`
- `voided` -> `voided`
- `expired` -> `expired`
- unknown provider statuses -> `provider_attention`

## Privacy Boundary

BN6B source guards verify that projections and audit metadata do not expose:

- raw legal text;
- signed document bodies;
- raw provider payloads;
- provider tokens / private keys / webhook secrets;
- provider envelope, signature, or certificate references by default;
- guardian consent text;
- birthdates;
- staff notes;
- internal audit diffs.

## Strict Non-Goals

- No DocuSign SDK dependency.
- No provider API calls.
- No live envelope creation.
- No embedded signing URL generation.
- No provider webhook route.
- No signed document retrieval.
- No file storage workflow.
- No legal text generation.
- No participation-blocking gate.
- No billing, Stripe, Apple, Admin Portal capability, HorseOps, landing page,
  native app, push notification, offline sync, service worker, or Phase 16 work.

## Verification

Focused tests:

- `backend/tests/test_build_next_6b_document_workflow_contract.py`

Expected command:

```bash
PYTHONPATH=backend ./.venv/bin/python -m pytest backend/tests/test_build_next_6b_document_workflow_contract.py -q
```

If local pytest stalls in this checkout, the contract can be checked directly
with the same source-level assertions used in prior BN6 phases.

Local verification performed:

- Python compile passed for `backend/core/document_workflows.py` and
  `backend/tests/test_build_next_6b_document_workflow_contract.py`.
- Direct BN6B contract checks passed: 28 assertions.
- Local pytest still stalls while importing pytest internals before collecting
  this test file in the current checkout; Codex review should run the focused
  pytest file in its normal environment.

## Package

Target:

`outputs/build_next_6b_document_workflow_provider_plan.zip`

## Next Gate

After BN6B locks, the next implementation should be split into smaller phases:

- BN6C-1: document template and request schema foundation;
- BN6C-2: sandbox-only DocuSign envelope creation behind an explicit flag;
- BN6C-3: provider webhook status sync;
- BN6C-4: signer UX and admin evidence export.

No live document signing begins until founder/legal approval confirms document
language, provider environment, template mapping, retention policy, and launch
blocking rules.
