# Build-Next-6 - Document / Signature Decision Gate

Status: hybrid model approved. BN6A connector prep is tracked in
`BUILD_NEXT_6A_SIGNATURE_CONNECTOR_PREP_README.md`.

## Purpose

Build-Next-6 decides how EquineSync will handle launch-critical documents,
waivers, releases, authorizations, and signatures before any document workflow is
built. The founder-approved direction is the hybrid model.

This is a decision and architecture phase. It must prevent a costly in-house
legal-signature rebuild if a third-party e-signature provider is the safer
choice.

## Locked Inputs

- BN5-A through BN5-D minor / parent safeguards are locked.
- Under-13 behavior remains `parent_managed_only` in product logic.
- Guardian / parent involvement is required for minor-sensitive workflows.
- No legal claims should be made by code or docs without founder-approved legal
  review.

## Strict Scope

Allowed:

- Document type inventory.
- Decision matrix: third-party e-signature, in-house acknowledgement tracking,
  or hybrid.
- Draft workflow map for who must sign what.
- Draft data model and API contract proposal.
- Retention, countersignature, audit, and export requirements.
- Legal/accounting review notes.
- Docs / roadmap / PRD updates.
- Optional source-only tests that assert no implementation routes were added.

Not allowed:

- No document signing implementation.
- No e-signature SDK integration.
- No provider API calls.
- No new document upload/storage workflow.
- No required-document participation gate.
- No billing, Stripe, Apple, Admin Portal, HorseOps, landing page, native app,
  push notification, offline sync, service worker, or Phase 16 work.
- No legal advice or binding legal language. Founder must route final language
  through legal counsel.

## Document Types To Inventory

Minimum launch-candidate list:

- General liability waiver.
- Minor participant liability waiver.
- Media / photo release.
- Emergency veterinary care authorization.
- Lesson program agreement.
- Boarding / facility services agreement.
- Arena use / facility rules acknowledgement.
- Trainer / service-provider agreement.
- Community program or scholarship acknowledgement, if offered at launch.

Each document type should answer:

- Required for which customer types?
- Required for which roles / relationships?
- Required for which workflows?
- Adult signer or guardian signer?
- Does the barn/facility need to countersign?
- Does the platform need to countersign?
- Does it expire?
- Is renewal required annually or per event?
- Should it block participation, only warn, or stay deferred?

## Decision Options

### Option A - Third-Party E-Signature Provider

Examples: Dropbox Sign, DocuSign, PandaDoc, Adobe Sign.

Pros:

- Stronger compliance posture.
- Audit certificate and signature evidence handled by provider.
- Better for waivers, releases, and countersignature workflows.

Cons:

- Cost and vendor dependency.
- Requires template/provider setup.
- Requires webhook and provider-status handling later.

Recommended for:

- Liability waivers.
- Minor waivers.
- Media releases.
- Any document requiring legally meaningful signature evidence.

### Option B - In-House Acknowledgement Tracking

Pros:

- Faster and simpler.
- Useful for non-legal operating acknowledgements.
- Can be built with existing audit patterns.

Cons:

- Not a full e-signature system.
- Weaker legal/compliance posture.
- Risky for liability waivers without counsel approval.

Recommended for:

- Facility rules acknowledgement.
- Non-legal onboarding checklists.
- Internal policy confirmations.

### Option C - Hybrid

Use third-party e-signature for legal documents and in-house acknowledgement for
operating policies.

Founder-approved default:

- **Option C**, pending founder/legal approval.

BN6A implements only the provider-readiness connector for a DocuSign-style
third-party provider. Live envelope creation, provider webhooks, signing URLs,
signed-document retrieval, and participation gates remain deferred.

## Proposed Data Model Draft

No collections are created in BN6. This is a proposal only.

Future collections may include:

- `document_templates`
  - `id`
  - `barn_id` or `platform_template`
  - `document_type`
  - `display_name`
  - `provider`
  - `provider_template_id`
  - `version`
  - `status`
  - `required_for_customer_types`
  - `required_for_roles`
  - `required_for_workflows`
  - `expires_after_days`

- `document_requests`
  - `id`
  - `barn_id`
  - `template_id`
  - `subject_user_id`
  - `subject_student_profile_id`
  - `required_signer_user_ids`
  - `provider_envelope_id`
  - `status`
  - `requested_by_user_id`
  - `created_at`
  - `expires_at`

- `document_signatures`
  - `id`
  - `barn_id`
  - `request_id`
  - `template_id`
  - `signer_user_id`
  - `relationship_to_subject`
  - `provider_signature_id`
  - `status`
  - `signed_at`
  - `audit_certificate_url` or provider reference

- `document_acknowledgements`
  - `id`
  - `barn_id`
  - `policy_key`
  - `user_id`
  - `version`
  - `status`
  - `acknowledged_at`
  - `audit_metadata`

## Required Privacy / Safety Rules

- Never store raw legal text in audit metadata.
- Never store full signed document bodies in audit rows.
- Do not expose minor birthdates, guardian consent text, or private notes in
  document-status APIs.
- Guardian signatures must be linked through the existing guardian/student
  relationship model from BN5.
- Under-13 flows must remain parent-managed.
- Denials or missing documents should not leak private document titles to users
  who cannot access the underlying person/horse/student context.

## Acceptance Criteria

- Founder-approved document type matrix exists.
- Founder chooses one of:
  - third-party e-signature;
  - in-house acknowledgement only;
  - hybrid.
- Legal/accounting review needs are explicitly captured.
- Draft future data model is approved or revised.
- Required-vs-soft-warning behavior is decided for each workflow.
- BN6 package includes a README and no product implementation.

## Suggested Files For BN6 Execution

- New `BUILD_NEXT_6_DOCUMENT_SIGNATURE_DECISION_README.md`
- Optional `backend/tests/test_build_next_6_document_signature_noop.py`
- Updates to:
  - `docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`
  - `docs/PHASED_EXECUTION_PLAN.md`
  - `memory/PRD.md`
  - `memory/ROADMAP.md`

## Review Package

Target:

`outputs/build_next_6_document_signature_decision.zip`

## Stop Condition

Stop after packaging BN6 for Codex review. Do not begin document/signature
implementation until BN6 is reviewed, locked, and founder/legal choices are
approved.
