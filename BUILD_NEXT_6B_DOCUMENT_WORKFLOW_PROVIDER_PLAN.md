# Build-Next-6B - Document Workflow Provider Plan

Status: gated. Do not implement until founder approves this plan and legal
review requirements are confirmed.

## Purpose

Build-Next-6B turns the locked BN6A connector readiness layer into a concrete
plan for real document workflows. It decides the document templates, signer
roles, guardian routing, provider envelope lifecycle, webhook status sync,
retention rules, and launch behavior before any live signature requests are
created.

This phase may prepare the workflow contract. It must not send real DocuSign
envelopes until the founder confirms provider credentials, template setup, and
legal document language.

## Locked Inputs

- BN5-A through BN5-D minor / parent safeguards are locked.
- BN6A signature connector prep is locked.
- Hybrid model is approved:
  - legal documents use a third-party e-sign provider such as DocuSign;
  - lower-risk acknowledgements stay in-app.
- Under-13 users remain parent-managed.
- Guardian signatures must use the BN5 guardian/student relationship model.
- No legal language is final until founder/legal review approves it.

## Strict Scope

Allowed:

- Define document template records and provider-template mapping.
- Define document request and signature status records.
- Define signer routing for adults, minors, guardians, facility countersigners,
  and platform countersigners.
- Define DocuSign envelope lifecycle contract.
- Define provider webhook status sync contract.
- Define certificate/reference retention rules.
- Define soft-warning vs hard-block behavior by workflow.
- Add docs, tests, and safe placeholder routes only if explicitly scoped.

Not allowed without a separate approval:

- No live envelope creation.
- No embedded signing URL generation.
- No provider webhook endpoint receiving real provider events.
- No signed-document retrieval or file storage.
- No legal text generation.
- No participation gate that blocks lessons, boarding, arena use, or ownership
  workflows.
- No billing, Stripe, Apple, Admin Portal capability, HorseOps, landing page,
  native app, push notification, offline sync, service worker, or Phase 16 work.

## Document Type Matrix

BN6B must classify each document as `provider_signature` or
`in_house_acknowledgement`.

Legal / provider-signature candidates:

- General liability waiver.
- Minor participant liability waiver.
- Media / photo release.
- Emergency veterinary care authorization.
- Lesson program agreement.
- Boarding / facility services agreement.
- Trainer / service-provider agreement.

In-house acknowledgement candidates:

- Arena / facility rules acknowledgement.
- Community program acknowledgement.
- Onboarding policy acknowledgement.

For each document type, BN6B must decide:

- required customer types;
- required roles or relationship types;
- adult signer rules;
- guardian signer rules;
- whether facility countersignature is required;
- whether platform countersignature is required;
- expiration / renewal interval;
- soft-warning vs hard-block behavior;
- whether signed evidence must be exportable.

## Proposed Data Model

BN6B may introduce this schema only after review approval:

- `document_templates`
  - `id`
  - `barn_id` or `platform_template`
  - `document_type`
  - `display_name`
  - `workflow_kind`
  - `provider`
  - `provider_template_id`
  - `version`
  - `status`
  - `required_for_customer_types`
  - `required_for_roles`
  - `required_for_workflows`
  - `requires_guardian_signature`
  - `requires_facility_countersignature`
  - `requires_platform_countersignature`
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
  - `provider_certificate_ref`

- `document_acknowledgements`
  - `id`
  - `barn_id`
  - `policy_key`
  - `user_id`
  - `version`
  - `status`
  - `acknowledged_at`
  - `audit_metadata`

## Provider Contract

BN6B must define but not necessarily execute:

- how a local `document_request` maps to a DocuSign envelope;
- how a local signer maps to provider recipient records;
- how provider envelope IDs are stored without exposing them to unrelated users;
- how webhook status updates move local records through draft / sent / viewed /
  completed / declined / voided / expired;
- how provider certificates or audit references are retained;
- how provider failures are retried or surfaced to staff.

## Privacy / Safety Rules

- Never store raw legal text in audit metadata.
- Never store full signed document bodies in audit rows.
- Never expose provider private keys, access tokens, webhook secrets, or
  provider account IDs in API responses.
- Owner/minor-facing APIs must not expose private staff notes, guardian consent
  text, birthdates, raw provider payloads, or internal audit diffs.
- Missing-document responses must be scoped to the caller's relationship and
  must not leak another person's document status.
- Denied document actions must use generic errors unless the caller has the
  underlying person / horse / student context.

## Founder Decisions Required Before Implementation

1. Which DocuSign account/environment should be used first: demo/sandbox or
   production?
2. Will templates be created in DocuSign first, then mapped into EquineSync by
   `provider_template_id`?
3. Which launch workflows hard-block participation, and which only warn?
4. Which document types require guardian signature for minors?
5. Which document types require facility countersignature?
6. Which document types require annual renewal?
7. Should signed document PDFs be stored by EquineSync, or should EquineSync
   store only provider certificate/reference metadata?
8. Who can export signed evidence?

## Acceptance Criteria

- Document type matrix exists and is founder-approved.
- Provider-template mapping rules are approved.
- Signer routing rules are approved for adults, minors, guardians, facility
  countersigners, and platform countersigners.
- Retention and export policy is approved.
- Soft-warning vs hard-block behavior is approved by workflow.
- Privacy rules are encoded in tests or source guards.
- No live envelope is sent without a separate implementation approval.

## Suggested Files

If BN6B is executed as a planning / schema-contract phase:

- `BUILD_NEXT_6B_DOCUMENT_WORKFLOW_PROVIDER_README.md`
- `backend/core/document_workflows.py`
- `backend/tests/test_build_next_6b_document_workflow_contract.py`
- docs / PRD / roadmap updates

If BN6B is approved for implementation later, split into smaller sub-phases:

- BN6B-1 template and request schema foundation.
- BN6B-2 DocuSign envelope creation behind sandbox-only flag.
- BN6B-3 webhook status sync.
- BN6B-4 signer UX and admin evidence export.

## Review Package

Target:

`outputs/build_next_6b_document_workflow_provider_plan.zip`

## Stop Condition

Stop after packaging BN6B for Codex review. Do not begin live signing
implementation until BN6B is reviewed, locked, and founder/legal decisions are
approved.
