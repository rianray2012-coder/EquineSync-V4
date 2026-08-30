# Pilot Evidence Privacy Protocol

Status: Gate 7 pilot-readiness artifact
Owner: Founder / Rian Ray
Scope: Bounded EquineSync pilot evidence handling

This protocol governs evidence captured during the EquineSync pilot. It is an
operator-ready companion to the Privacy and Data Protection Model, Gate 6 lock,
Gate 7 opening packet, RF19 redaction rules, and Pilot Support Runbook.

This protocol does not authorize production deployment, customer-facing live
Checkout, live payment collection, Stripe Customer Portal activation, live
automatic tax activation, legal signature sends, DocuSign production envelopes,
Adobe Sign activation, provider-live expansion, public directory expansion,
official AI save, or AI autonomous mutation.

## Evidence Owner And Access

Primary evidence owner: Founder / Rian Ray.

Raw pilot evidence may be viewed only by the founder and specifically
authorized support, engineering, privacy, or legal reviewers who need it to
triage the issue. Redacted evidence may be attached to pull requests, lock
packets, and Gate 7 review packets when it proves the workflow outcome without
exposing protected information.

Evidence artifacts must identify the gate or support ticket they support. When
an artifact includes real participant data, owner documents, horse health
details, minor or guardian details, support free text, provider identifiers, or
payment identifiers, it must stay out of public pull request bodies and broadly
shared screenshots unless redacted first.

## Allowed Pilot Evidence

Allowed evidence includes:

- Redacted screenshots showing route, role, visible state, and non-sensitive
  labels.
- HTTP status codes and sanitized response shapes.
- Console errors after removing credentials, tokens, API keys, provider
  secrets, payment secrets, private URLs, and unnecessary personal data.
- Test account role labels, test barn names, test horse names, sanitized
  timestamps, sanitized success messages, and sanitized denial messages.
- Opaque local references such as support ticket ids when they do not expose
  provider, payment, legal, or private participant information.
- Boolean flag state for retained activation limits.
- Hashes or file names that prove artifact existence without exposing the
  contents of legal, owner, medical, or identity documents.

## Prohibited Pilot Evidence

Do not store or publish these values in Gate 7 evidence:

- Passwords, magic links, session tokens, access tokens, refresh tokens, API
  keys, JWT secrets, database URLs, private keys, webhook secrets, or seed
  credentials.
- Stripe secret keys, restricted keys, webhook signing secrets, Checkout URLs,
  client secrets, SetupIntent secrets, PaymentIntent secrets, card numbers,
  bank data, payment method details, payout details, or refund/dispute payloads.
- Unredacted Stripe Customer, Subscription, Checkout Session, Invoice,
  PaymentIntent, SetupIntent, Price, Product, Tax, or webhook event identifiers
  when the identifier is not necessary to prove a bounded provider result.
- DocuSign private keys, production envelope ids, recipient links, signing
  URLs, Adobe Sign agreement ids, provider tokens, or signed-document payloads.
- Full owner documents, legal documents, signature packets, horse medical
  records, medication details, private barn records, owner-hidden staff notes,
  or support internal note bodies.
- Minor, guardian, rider, emergency-contact, household, custody, safeguarding,
  location, or scheduling details beyond the minimum needed to prove the
  boundary under review.
- AI prompt, source document, extracted content, or model output containing
  participant, owner, horse-health, legal, payment, or private operational
  details unless the artifact is access-limited and explicitly approved for
  that review.

## Required Redaction Rules

Before evidence is added to a lock packet, pull request, issue, or shared
folder, remove or mask:

- Credentials, secrets, tokens, connection strings, and private keys.
- Real participant contact details and account recovery material.
- Payment and provider identifiers unless an opaque redacted suffix is required
  for reconciliation.
- Owner-hidden staff notes and internal support note bodies.
- Horse health, treatment, medication, valuation, custody, welfare, and
  location details unless minimum necessary for a safety or privacy
  classification.
- Minor and guardian details, including family relationship facts, consent
  context, school-like schedules, location patterns, or guardianship disputes.
- Legal-document content, signature packets, recipient links, and provider
  signing URLs.

Use the shortest evidence excerpt that proves the product state. Prefer counts,
statuses, role labels, boolean flags, and route names over full records.

## Storage Locations

Redacted Gate 7 evidence may be stored under `outputs/` when the artifact is
needed for a gate packet, lock record, or PR evidence link.

Working scratch material, raw captures, provider dashboard screenshots, local
browser recordings, and exploratory logs must stay in an unbundled working area
such as `work/` or another founder-controlled local evidence folder until
redacted. Raw evidence must not be bundled into implementation PRs.

Credential files, environment files, provider keys, and runtime secrets must
remain in ignored secret locations such as local `.env` files or the approved
secret store. Evidence may report presence flags and configuration status, but
must not print secret values.

## Retention And Disposition

Retain redacted evidence needed to support accepted Gate 7 decisions, PRs, and
lock records for the pilot review period and follow-on launch-readiness review.

Raw evidence should be deleted or access-restricted after the issue is resolved,
the redacted artifact is produced, and the founder confirms no legal, privacy,
incident, or dispute hold requires preservation. If a privacy, safety, billing,
legal, or access-boundary incident is credible, preserve the minimum necessary
raw evidence in a founder-controlled restricted location until the incident
owner releases it.

Do not use pilot evidence for marketing, sales demos, model training, provider
expansion, public launch claims, or unrelated analytics unless a separate
founder-approved privacy review authorizes that use.

## Support Evidence Handling

Support ticket descriptions and internal notes may contain sensitive free text.
They may be used for support continuity inside the support system, but audit
metadata, PR descriptions, issue titles, and public-facing evidence must stay
routing-only and redacted.

For support screenshots, show only the route, ticket state, category, severity,
assignment status, and sanitized timestamps unless the founder approves a more
detailed restricted artifact.

## Owner Documents And Legal Evidence

Owner document evidence must prove owner-safe status projection without copying
document contents. Prefer document type, local status, required signer count,
signed count, expiration state, and `live_signing_enabled=false`.

DocuSign and Adobe Sign evidence must remain provider-reference-only unless a
separate legal activation gate authorizes a specific signed-document handling
path. DocuSign sandbox proof does not authorize production envelope sending.
Adobe Sign remains deferred.

## Payment And Tax Evidence

Pilot billing evidence must show founder-granted free/manual access and no
payment collection. Evidence may show `billing_provider=manual`, zero amount,
null Checkout URL, null Checkout Session id, and retained flag state.

Do not expose live Checkout URLs, client secrets, payment method details, full
Stripe object identifiers, webhook signing secrets, tax transaction payloads, or
customer-facing billing operation screenshots unless separately approved and
redacted.

## Minors, Guardians, Riders, And Safety

Evidence involving minors, guardians, riders, emergency contacts, household
relationships, custody, safeguarding, or location patterns must use the minimum
necessary proof. Prefer role labels, denial states, guardian-required flags,
and sanitized status messages over personal facts.

If a screenshot or log would reveal a minor's identity, guardian relationship,
schedule, location, medical/safeguarding fact, or private communication, do not
place it in ordinary Gate 7 evidence. Preserve it only in a restricted
founder-controlled location if needed for incident handling.

## Horse Health And Barn Operations

Horse health, treatment, medication, location, custody, valuation, welfare,
and barn operational records can create safety and business risk. Evidence
should use seeded fixtures, synthetic names, counts, redacted summaries, or
status-only projections wherever possible.

Do not include real horse medical details, owner-hidden barn notes, staff
performance details, private schedules, or facility security patterns in shared
evidence.

## AI Evidence Handling

AI evidence must preserve draft-only and human-review boundaries:

- `draft_only=true`
- `review_required=true`
- `official_records_written=false`
- no official AI save authority
- no AI autonomous mutation

AI source files, prompts, model responses, extraction outputs, and review notes
must be redacted when they include participant, owner, horse-health, legal,
payment, provider, or private operational content. Evidence should prove the
guardrail state and no-save result without copying sensitive input or output.

## Privacy Incident Escalation

Classify as urgent and escalate to the founder immediately when evidence shows
or credibly suggests:

- Cross-facility, cross-owner, or unauthorized role visibility.
- Minor, guardian, safeguarding, custody, household, or private communication
  exposure.
- Owner document, legal-signature, signed-document, or provider-signing URL
  exposure.
- Payment, tax, Stripe, bank, card, Checkout, webhook, or billing-secret
  exposure.
- AI official-record mutation, autonomous mutation, or sensitive source/output
  exposure.
- Real horse health, medication, location, welfare, custody, or owner-hidden
  note exposure.

Preserve the minimum necessary evidence, redact before broad sharing, freeze
the smallest unsafe workflow, and record the action in the support or incident
record.

## Retained Activation Stop Rules

Gate 7 pilot evidence handling does not authorize:

- Production deployment.
- Customer-facing live Checkout.
- Live payment collection.
- Stripe Customer Portal activation.
- Live automatic tax activation.
- Legal signature sends.
- DocuSign production envelopes.
- Adobe Sign activation.
- Provider-live activation or public directory expansion.
- Official AI save authority.
- AI autonomous mutation.

Any evidence capture that would require one of these actions must stop until a
separate founder authorization names the scope, environment, fixture, rollback
plan, and evidence boundaries.
