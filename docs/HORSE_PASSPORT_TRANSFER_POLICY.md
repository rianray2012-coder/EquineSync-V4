# Horse Passport Transfer Policy

Status: Founder-approved implementation policy for the first controlled
ownership-transfer slice.

## Purpose

Horse Passport transfer is a controlled ownership workflow, not a direct edit to
`horses.owner_id`, `horses.primary_owner_id`, or barn membership fields. The
workflow must preserve continuity for the horse while preventing old-owner,
old-barn, staff-only, provider, billing, document, and message data from moving
or remaining visible by accident.

## Policy

### Allowed in the first transfer slice

The initial transferable Passport content is limited to owner-safe, low-risk
categories:

- `identity_public`: name, breed, color, discipline, photo, and public profile
  descriptors.
- `ownership_record`: prior owner, new owner, source barn, destination barn, and
  acceptance timestamp.
- `care_summary`: owner-safe feed, hay, turnout, riding/training, and equipment
  summaries built through the same backend owner projection rules used by the
  Care Ledger owner summary.

### Explicitly blocked pending Product/Legal decision

The following categories must not be copied or exposed to the new owner by this
first transfer slice:

- raw daily checks;
- active alerts, alert triggers, and alert events;
- staff notes, handling warnings, and required staff experience;
- raw audit diffs or field values;
- private health documents, vet photos, and file attachments;
- messages and message history;
- invoices, payment, subscription, and billing records;
- provider contact details, provider grants, and live provider sync state.

### Required workflow states

Transfer requests use a small state machine:

- `owner_approved`: approved by the current owner and waiting for barn approval
  when custody or barn assignment changes.
- `barn_approved`: approved by the source barn admin/manager and ready for the
  named new owner.
- `pending_acceptance`: created and waiting for the new owner.
- `canceled`: canceled before acceptance.
- `accepted`: accepted by the named new owner.

Only active requests can be canceled. Only requests that are ready for new-owner
acceptance can be accepted. Accepted and canceled requests cannot be re-applied.

### Approval authority

The first slice requires current-owner approval before ownership can move.
Barn managers and admins cannot start an ownership transfer by themselves.

When the transfer changes barn custody or barn assignment, the source barn
admin/manager must approve after owner approval and before new-owner
acceptance. Same-barn owner-to-owner transfer does not require barn approval in
the first slice.

Admin override is reserved for a future audited correction/support path and is
not part of this first transfer workflow.

### Export before transfer

Before acceptance, the current owner or an authorized barn admin/manager can
preview the owner-safe export package. The export preview is the record of what
the initial transfer slice will carry. It is intentionally smaller than the
full Care Ledger.

### Access cutoff

On acceptance:

- the horse primary owner and legacy owner field move to the new owner;
- the prior owner is removed from secondary owner access;
- the destination barn is applied only when it is explicitly named in the
  transfer request;
- the transfer archive records the selected safe categories and policy version;
- audit metadata stays categorical and non-sensitive.

The prior owner cannot see future private records through the owner-scoped
Horse Ledger once ownership fields have moved.

## Still Open

Product/Legal still needs to decide whether any historical health photos,
documents, message history, invoices, provider data, or old-barn records can be
transferred, retained, exported only, or permanently withheld.
