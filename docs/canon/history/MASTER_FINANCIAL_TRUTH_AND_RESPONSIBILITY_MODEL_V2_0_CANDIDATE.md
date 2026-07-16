# Master Financial Truth and Responsibility Model

**Document Type:** Newly Created Constitutional Candidate
**Version:** 2.0
**Lifecycle State:** `CROSS_CANON_REVIEW`
**Creation Date:** 2026-07-12
**Historical Status:** Newly drafted; not recovered, backdated, adopted, or locked
**Founder Approval:** Pending
**Canon Adoption:** Not authorized
**Implementation, Schema, Migration, Processor, Payment, Payout, Refund, Tax, Permission, and Production Authorization:** None

## 1. Constitutional purpose

This candidate defines how EquineSync represents financial truth, responsibility, authorization, evidence, reconciliation, and continuity without confusing an internal status with movement of money or a financial role with ownership of a horse, account, organization, or record.

It is subordinate to Product Vision and Ecosystem authority, consumes Relationship, Record Stewardship, Claims/Disputes, Permission, and Audit boundaries, and constrains RF32 Barn Payment Issue Workflow, proposed RF35 Payments and Financial Rails, subscriptions, marketplace commerce, provider billing, and every future money-related feature.

## 2. Core constitutional rules

1. A financial record states what EquineSync knows and the evidence supporting it; it must not imply processor settlement that has not been verified.
2. Invoice, charge, authorization, capture, payment, payout, refund, credit, adjustment, dispute, chargeback, tax, fee, commission, balance, and settlement are distinct objects and states.
3. Legal owner, beneficial owner, payer, guarantor, invoice recipient, payment-method owner, merchant, platform, processor, payee, payout recipient, beneficiary, refund recipient, settlement source, and dispute claimant are distinct roles.
4. Payment does not prove horse ownership, custody, guardianship, authority, acceptance, or record access.
5. Failure or dispute does not erase horse history, emergency-care duties, claims participation, stewardship, or authored records.
6. External processors provide attributed evidence and execution capability; they do not replace EquineSync domain truth or authorization.
7. Financial effects require explicit authority, idempotency, audit lineage, segregation of duties, and reconciliation.
8. No AI system may approve, execute, conceal, or represent a financial action as settled.

## 3. Canonical principals and roles

| Principal or role | Meaning | Prohibited inference |
| --- | --- | --- |
| Obligor | Party asserted or verified to owe an obligation | Not automatically payer or owner |
| Payer | Party responsible for payment under a scoped relationship | Not automatically payment-method owner |
| Guarantor | Party with contingent responsibility | Not automatically primary obligor |
| Invoice recipient | Authorized recipient of an invoice or statement | Receipt does not create liability |
| Payment-method owner | Principal controlling a funding instrument | Not automatically payer or beneficiary |
| Merchant of record | Entity legally presenting the charge | Not automatically service provider or platform |
| Platform | EquineSync operating entity and software context | Must not claim processor-held funds as its own |
| Processor | External rail executing or reporting payment movement | Provider event remains evidence, not universal truth |
| Payee | Party entitled to receive funds under an obligation | Not automatically payout recipient |
| Payout recipient | Destination principal for a specific payout | Must be verified independently of payee identity |
| Beneficiary | Party economically benefiting from a transaction | Not automatically authorized actor |
| Refund recipient | Authorized destination for a refund | May differ from payer or payment-method owner by policy |
| Dispute claimant | Party asserting a financial claim | Claim is not a final determination |

All roles are effective-dated, purpose-limited, scoped, attributable, and independently permissioned under the Relationship and Permission Models.

## 4. Canonical financial objects

- Financial obligation: source-domain duty, amount basis, responsible roles, due terms, and authority.
- Invoice: versioned request for payment; never evidence of payment by itself.
- Invoice line: attributable quantity, service/product/tax/fee/credit basis, period, and source record.
- Charge request: proposed processor action bound to invoice/obligation and idempotency identity.
- Charge: processor-facing attempt with immutable request and status evidence.
- Payment: verified receipt/capture evidence against an obligation.
- Payment allocation: mapping from payment to obligations or invoice lines.
- Deposit: funds or obligation held for a governed future purpose.
- Credit: amount reducing a future/current obligation; not money movement unless separately settled.
- Adjustment: reasoned correction that preserves before/after state.
- Refund: authorized return of settled or captured funds with independent state.
- Payout: movement from settlement balance to a verified recipient.
- Fee and commission: separately attributable obligation or allocation, not hidden subtraction.
- Tax record: jurisdiction, calculation basis, rate/source, collection/remittance responsibility, and evidence.
- Dispute and chargeback: claims and processor processes with independent timelines and outcomes.
- Balance projection: computed view from canonical entries; never an independently editable truth.
- Reconciliation case: comparison among EquineSync obligations, processor evidence, bank/accounting evidence where authorized, and exceptions.

## 5. State separation

An invoice may be `DRAFT`, `ISSUED`, `PARTIALLY_PAID`, `PAID_INTERNAL_UNVERIFIED`, `SETTLED_VERIFIED`, `OVERDUE`, `DISPUTED`, `VOID`, or `WRITTEN_OFF` under approved policy. These states must not collapse.

A processor action may be `NOT_REQUESTED`, `REQUESTED`, `AUTHORIZED`, `DECLINED`, `CAPTURE_PENDING`, `CAPTURED`, `SETTLEMENT_PENDING`, `SETTLED`, `FAILED`, `REVERSED`, `REFUND_PENDING`, `REFUNDED`, `DISPUTED`, or `CHARGEBACK`. Provider terminology maps through a versioned adapter and cannot silently redefine canonical states.

## 6. Authority and approval

Financial commands identify actor, principal, role, organization/barn scope, obligation, amount/currency, source revision, authority source, policy version, purpose, idempotency key, and evidence manifest.

High-impact actions require thresholds and segregation of duties. Approval classes must distinguish invoice issue, write-off, refund, payout, bank/detail change, manual settlement override, dispute concession, tax adjustment, fee/commission change, and reconciliation repair. One actor must not request and independently approve the same protected action where dual control is required.

Thresholds, currencies, jurisdiction rules, reviewer classes, and emergency exceptions remain founder/legal/financial-policy decisions and are not established by this candidate.

## 7. Ledger continuity

Canonical financial entries are append-only and balanced within their approved accounting model. Corrections create reversing and replacement entries; they do not edit settled history. Every projection can reproduce its contributing entries, policy, currency, rounding, exchange-rate source if applicable, and effective time.

This candidate does not select double-entry implementation schemas or accounting software. A future implementation must prove conservation, allocation, precision, currency, duplicate prevention, and reconciliation invariants.

## 8. Processor evidence and reconciliation

Processor events are authenticated, replay-protected, attributed, versioned, and correlated. A webhook receipt does not equal final settlement. Conflicting or missing provider evidence creates a reconciliation exception and blocks false claims of payment, payout, refund, or chargeback completion.

Reconciliation compares expected obligation, internal request/entry state, processor object/event state, and authorized external settlement evidence. It records exact discrepancies, ownership, retries, age, materiality, and closure evidence. Manual correction cannot fabricate provider settlement.

## 9. Subscriptions and platform billing

Subscription entitlement, invoice, charge, payment, cancellation, credit, trial, pause, delinquency, and service restriction are distinct. Entitlement may follow approved product policy but cannot be represented as payment settlement. SaaS subscription billing remains separate from barn/provider/client financial rails and marketplace movement.

## 10. Barn and provider billing

Board, care, lessons, training, services, provider appointments, supplies, and facility charges retain source-domain lineage. Barn owner, horse owner, guardian, rider, payer, guarantor, invoice recipient, provider, and beneficiary roles remain independent. RF32 must preserve owner-safe messaging, neutral disputes, emergency obligations, and no ownership inference.

## 11. Marketplace transactions

Marketplace order, service fulfillment, platform fee, merchant status, connected account, payout, refund, dispute, and reputation effects are separately governed. No marketplace payout, custody of funds, escrow representation, connected-account activation, or seller underwriting is authorized by this candidate.

## 12. Refunds, reversals, disputes, and chargebacks

Refund authority, destination, amount, reason, source payment, fees, tax effect, and processor evidence are explicit. Reversal is a new financial event linked to the original. Disputes preserve claims, evidence, temporary restrictions, deadlines, notices, and appeal/review paths under the Claims Model. Chargeback outcome does not by itself determine contractual truth or service quality.

## 13. Taxes, fees, commissions, and adjustments

Tax calculation, collection, reporting, remittance, exemption, and jurisdiction require a separately approved tax policy and qualified review. Fees and commissions are disclosed, attributable, versioned, and reconciled. Adjustments require reason codes, authority, before/after evidence, and materiality review.

## 14. Privacy, security, and permissions

Financial data is minimum-necessary and field-projected. Payment credentials, bank details, tax identifiers, and processor secrets must not enter general records, logs, analytics, AI prompts, client bundles, or unsupported exports. Tokenized provider references do not grant access. Every sensitive read, export, override, and support action is audited.

## 15. Records, retention, legal hold, and export

Record Stewardship controls authorship, stewardship, retention, legal hold, correction, erasure, archival, and disposal. Financial records retain source and processor provenance. Export distinguishes user-readable statements, accounting export, processor evidence, legal production, and portability. Export does not transfer authority or erase retained obligations.

## 16. Offline and partial failure

Offline clients may draft non-authoritative data but cannot mark payment, refund, payout, settlement, dispute resolution, or write-off effective. Network timeout yields unknown/pending, not failure or success. Recovery uses idempotent lookup and reconciliation before retry. Partial completion remains visible and blocks duplicate action.

## 17. Duplicate and replay prevention

Every consequential command has stable idempotency identity and expected revision. Processor event IDs, object IDs, signatures, sequence/version, and payload hashes are recorded. Replay produces the prior result without duplicate charge, refund, payout, ledger entry, invoice, notice, audit, or analytics fact.

## 18. Audit and analytics

Audit captures actor/principal, authority, source records, before/after states, amount/currency, policy, approvals, processor evidence references, correlation/causation, and exception/reconciliation outcomes. Analytics use privacy-safe facts and never become financial truth. Metrics include payment latency, reconciliation age, failure/retry, duplicate prevention, dispute/chargeback, refund, payout, aging, and exception materiality.

## 19. AI boundary

AI may explain an authorized projection, categorize a reconciliation exception, or draft a non-binding communication under RF30 and later approval. It may not infer liability, change amounts, approve/refuse credit, initiate money movement, select payout destinations, resolve disputes, submit taxes, conceal uncertainty, or represent unverified status as settled.

## 20. External adapter boundary

Stripe or any later processor is replaceable. Adapter contracts map provider identity/states/evidence to canonical objects, enforce environment separation, verify signatures, protect secrets, prevent replay, expose degraded state, and support portability. No provider, OAuth, webhook, connected account, API call, or external action is activated by this document.

## 21. Claims and transfer continuity

Financial claims and asserted liens remain separate from Horse Passport identity and ownership authority. A transfer may preserve obligations and claim evidence without granting a financial party access to unrelated horse records. RF31 and RF32 decide their scoped workflows through separate founder decisions and cannot use payment state as title proof.

## 22. Required controlled registries

Future founder-approved registries must define financial object/state types, role types, authority sources, approval thresholds, currencies/precision, tax/fee/commission types, processor mappings, dispute/chargeback reasons, reconciliation exceptions, retention classes, audit events, analytics facts, export profiles, and implementation authorization.

## 23. Validation obligations

Required future tests include: invoice without payment; internal paid without settlement; partial allocation; duplicate/replayed webhook; timeout after capture; stale authority; cross-barn denial; guardian/payer separation; owner/payer separation; refund to wrong destination denial; payout detail change; chargeback; disputed service; tax precision; currency mismatch; offline attempt; reconciliation drift; manual override denial; legal hold; restricted export; AI prohibition; processor outage; rollback/compensation; and complete audit reproduction.

## 24. Implementation gates

Before implementation: founder approval, controlled adoption, conflict resolution, legal/tax review where applicable, exact schemas and state machines, threat model, permission matrix, provider/environment/secret ownership, reconciliation and rollback plan, migration strategy, executable adversarial tests, evidence package, and separate implementation authorization are required.

Before production: processor contracts/accounts, environment separation, credentials, webhooks, monitoring, incident/runbook, reconciliation operations, finance approval, data/retention review, staged rollout, rollback/disable controls, and explicit founder release authorization are required.

## 25. Lifecycle and stop state

Current lifecycle:

`DRAFTED -> CROSS_CANON_REVIEW -> FOUNDER_REVIEW`

Future states require separate founder acts:

`FOUNDER_APPROVED -> CONTROLLED_ADOPTION -> LOCKED`

This candidate stops at `CROSS_CANON_REVIEW` pending its review report and founder decision. It cannot be presented as recovered history or active canon.

`MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_0_READY_FOR_CROSS_CANON_REVIEW`
