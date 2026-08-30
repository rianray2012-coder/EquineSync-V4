# Pilot Support Runbook

Status: Gate 7 pilot-readiness artifact
Owner: Founder / Rian Ray
Scope: Web-first / PWA-assisted pilot support only

This runbook governs support handling during the bounded EquineSync pilot. It
does not authorize production deployment, customer-facing live payments, legal
signature sends, provider-live expansion, public directory expansion, official
AI save, or AI autonomous mutation.

## Support Ownership

Primary support owner: Founder / Rian Ray.

Backup support operators must hold one of these platform roles before they may
triage pilot tickets:

- `super_admin`
- `platform_admin`
- `support_admin`

`billing_admin` and `read_only_auditor` may not own support tickets. Billing
or audit questions may be escalated to them outside the ticket assignment
field, but ticket ownership stays with a support-capable platform role.

## Pilot Intake Channels

The supported in-app channel is `/support`.

Participants should use the in-app support form for:

- Broken flows.
- Access or role issues.
- Billing or membership confusion.
- Data that appears incorrect.
- Workflow questions.
- Product feedback.
- Other pilot support needs.

The support form may include a page URL and device context. Participants should
not paste passwords, API keys, full payment details, legal documents, or more
horse health detail than needed to explain the issue.

## Severity Definitions

| Severity | Pilot Meaning | Initial Response Target | Escalation |
| --- | --- | --- | --- |
| `urgent` | Safety, privacy, payment, legal-send, access-boundary, cross-facility data, minor/guardian, or official-record concern. | Same day during pilot operating window. | Founder immediately; freeze affected workflow if risk is credible. |
| `high` | Blocks normal use for a pilot role, prevents onboarding, prevents care/task completion, or blocks admin triage. | One pilot business day. | Founder or platform admin. |
| `medium` | Blocks a limited task but a safe workaround exists. | Two pilot business days. | Support admin if repeated. |
| `low` | Cosmetic, confusing, copy, or enhancement feedback. | Triage during normal pilot review. | Defer to Gate 7 UX improvement or backlog lane. |

When severity is unclear, classify up to the safer severity until reviewed.

## Triage Workflow

1. Open `/admin/portal/support`.
2. Filter new tickets and review oldest urgent/high items first.
3. Confirm the ticket category, severity, submitter, role, facility context,
   and page URL.
4. Avoid copying sensitive free text into audit logs, pull requests, public
   issue titles, screenshots, or provider dashboards.
5. Change status to `in_progress` when active review starts.
6. Assign only to a support-capable platform user.
7. Add internal notes only when needed for support continuity.
8. Mark `waiting` if the participant or founder must supply information.
9. Mark `resolved` only after the participant-impacting issue is handled or a
   safe pilot workaround is explicitly communicated.

## Evidence And Privacy Handling

Allowed evidence:

- Redacted screenshots showing route, visible state, and non-sensitive labels.
- HTTP status codes and sanitized response shapes.
- Console error text after removing tokens, passwords, API keys, payment
  secrets, provider secrets, and unnecessary personal data.
- Opaque internal references such as redacted `st_` ticket ids.
- Boolean flag state for retained stop rules.

Do not store in evidence:

- Passwords, refresh tokens, access tokens, API keys, private keys, webhook
  secrets, or seed credentials.
- Full card numbers, bank data, payment method details, or unredacted Stripe
  object identifiers.
- Unredacted DocuSign or Adobe Sign envelope identifiers.
- Full owner documents, legal documents, or signature packets.
- Sensitive horse medical detail beyond what is necessary for a defect
  classification.
- Minor/guardian private details beyond the minimum needed for role-boundary
  proof.
- Internal support note bodies unless the evidence artifact is access-limited
  and the founder has approved its inclusion.

Support audit metadata should remain routing-only. Free-text ticket bodies and
internal notes may live in `support_tickets`, but audit rows must record only
safe facts such as category, severity, channel, and whether a message or note
was present.

## Account And Access Suspension

Use this path when a ticket suggests account misuse, incorrect role authority,
cross-facility visibility, or unsafe access:

1. Preserve the ticket and current evidence with redaction.
2. Do not delete the user or facility record as the first response.
3. Suspend or revoke the smallest affected access path available through the
   existing admin/account controls.
4. Confirm the affected user can no longer reach the unsafe workflow.
5. Keep read-only support/admin visibility available for diagnosis.
6. Record the action, reason, actor, and timestamp.
7. Restore access only after the cause is understood and founder or platform
   admin approval is recorded.

## Payment, Tax, And Subscription Stop Rules

During pilot, Stripe remains prepared but parked.

Do not enable or initiate:

- Customer-facing live Checkout.
- Live payment collection.
- Stripe Customer Portal.
- Live `automatic_tax`.
- Refund, dispute, payout, or customer-facing billing operations outside a
  separately approved Stripe go-live/support packet.

Pilot access should use founder-granted free/manual entitlement projection.
If a participant sees a payment prompt during pilot, classify it as at least
`high` and verify whether the prompt is informational, blocked by flags, or an
actual activation authority violation.

## Legal Signature Stop Rules

Do not send legal signature envelopes during the pilot unless a separate
founder authorization names the provider, environment, document type, signer
fixture, and rollback plan.

DocuSign sandbox proof does not authorize DocuSign production envelopes.
Adobe Sign remains deferred and inactive.

Any visible document-signing issue during pilot should be classified by whether
it is:

- Reference-only UI or evidence handling.
- Sandbox-only activation proof.
- A blocked or unauthorized legal send attempt.

## AI Stop Rules

AI may support draft-only extraction or review where separately proven, but
pilot support must preserve:

- No official AI save authority.
- No AI autonomous mutation.
- Human review required before any record-impacting use.
- Evidence that AI output did not write official records.

Any report that AI changed an official record without human approval is
`urgent` and must stop the affected workflow until verified.

## Provider And Directory Stop Rules

Do not expand provider-live activation or public provider directory behavior
during this pilot support lane.

Provider-facing issues may be triaged through support, but new live provider
capabilities, public listing expansion, provider billing, and provider legal
flows require separate founder approval.

## Rollback And Disable Guidance

For a credible pilot incident:

1. Stop the smallest unsafe action path first.
2. Keep read-only support/admin visibility available.
3. Preserve redacted evidence before cleanup.
4. Disable live payment/signature/AI/provider entry points by flag if they are
   implicated.
5. Use account or role suspension for access-boundary risk.
6. Keep pilot users on free/manual access while payment systems remain parked.
7. Record the rollback action in the ticket and audit trail.

## Lock Criteria For G7-03

G7-03 can lock when:

- `/support` renders for an authenticated pilot user.
- A support ticket can be submitted and confirmed.
- `/admin/portal/support` renders for a support-capable platform role.
- Support-admin access and denial tests pass.
- Support status, assignment, note, scrubbing, and audit tests pass.
- This runbook exists and carries the retained stop rules.
- Rendered evidence contains no credentials, payment secrets, provider secrets,
  legal documents, owner-hidden details, or unnecessary horse health detail.
