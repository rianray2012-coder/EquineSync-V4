# MASTER FINANCIAL TRUTH AND RESPONSIBILITY MODEL

**Document Type:** Tier 3 Foundational Domain Canon Candidate  
**Version:** 2.1  
**Status:** Expanded Constitutional Candidate for Controlled Cross-Canon Review and Founder Review  
**Product:** EquineSync  
**Canonical Domain:** Financial truth, financial responsibility, billing, payment evidence, settlement, accounting projection, reconciliation, disputes, continuity, and financial authority  
**Supersedes:** All prior proposed Version 1.0 and Version 2.0 candidates upon founder-approved controlled adoption  
**Canonical Consumers:** RF32 Barn Payment Issue Workflow; any future Payments and Financial Rails RF; Agreements; Identity; Relationships; Communications and Notice; Claims and Retention; Audit and Evidence; Record Stewardship and Retention; Horse Transfer and Passport Continuity; External Architecture and Adapters; Analytics; Platform Operations; Launch Readiness  
**Implementation Authorized:** No  
**Schema or Migration Authorized:** No  
**External Payment Activation Authorized:** No  
**Connected-Account Onboarding Authorized:** No  
**Production Mutation Authorized:** No  
**Public Launch Authority Created:** No

---

# 1. Purpose

This model establishes the constitutional rules by which EquineSync represents, separates, preserves, verifies, reconciles, projects, disputes, and governs financial facts and financial responsibility.

EquineSync serves a domain in which the horse receiving care, the person receiving a lesson, the legal owner, the guardian, the invoice recipient, the payer, the guarantor, the merchant, the trainer, the facility operator, the provider, and the settlement beneficiary may all be different parties. Those roles must remain explicit. Payment behavior must never be allowed to rewrite identity, ownership, guardianship, custody, authority, or care obligations.

The model protects against four recurring errors:

- treating a local application status as proof of external settlement;
- treating a processor event as the whole financial truth;
- treating payment as proof of legal or relationship authority;
- treating an accounting classification as a legal conclusion.

Version 2.1 closes the remaining constitutional gap by establishing one coherent model across EquineSync SaaS subscription billing, barn-issued invoices, customer payments to barns, provider compensation, connected-account or marketplace flows, accounting exports, revenue recognition, reconciliation, refunds, disputes, service restrictions, continuity, and evidence.

---

# 2. Constitutional Outcomes

Version 2.1 is intended to achieve the following outcomes:

1. one canonical vocabulary for financial objects and states;
2. explicit separation of financial programs and legal entities;
3. deterministic source-of-truth rules;
4. append-only financial history and correction by reversal or supersession;
5. processor evidence treated as scoped evidence rather than universal truth;
6. reconciliation as a first-class constitutional obligation;
7. strict authority, approval, and segregation-of-duties boundaries;
8. preservation of horse welfare, emergency care, and record continuity during financial disputes;
9. no inference of ownership, guardianship, creditworthiness, fraud, or lien validity from payment status alone;
10. a controlled path from constitutional adoption to later implementation planning without creating implementation authority here.

---

# 3. Canonical Financial Programs

EquineSync must distinguish at least the following financial programs. They may share infrastructure only through explicit, auditable boundaries.

### 3.1 EquineSync SaaS subscription billing
Billing by EquineSync for access to EquineSync products, plans, seats, storage, add-ons, or other platform services.

### 3.2 Barn and facility billing
Invoices issued by a barn, facility operator, boarding company, trainer, lesson business, or affiliated organization to its clients.

### 3.3 Independent provider billing
Charges and invoices issued by veterinarians, farriers, bodyworkers, haulers, photographers, clinicians, or other providers, whether collected inside or outside EquineSync.

### 3.4 Customer payment collection
Payment instructions, attempts, authorizations, captures, settlements, reversals, and refunds associated with barn, facility, provider, or platform obligations.

### 3.5 Marketplace or connected-account movement
Any future flow in which EquineSync facilitates payment to a connected recipient, takes a platform fee, initiates a transfer, maintains a reserve, or receives processor risk allocation.

### 3.6 Accounting projection and synchronization
Exports, journal suggestions, reconciliation files, or synchronization with QuickBooks or another accounting system.

### 3.7 Internal operational financial reporting
Aging, balances, revenue views, statements, exception reports, payout reports, and forecasts produced from authorized financial facts.

No program may silently borrow the authority, merchant identity, settlement state, or accounting treatment of another.

---

# 4. Layered Financial Truth

Financial truth is layered. Each layer answers a different question:

1. **Commercial obligation truth:** What duty to pay is asserted, under what agreement, service event, law, or approved policy?
2. **Charge truth:** What component amount was created and why?
3. **Invoice truth:** What was billed, by whom, to whom, for what period, and under what version?
4. **Payment-instruction truth:** What did an authorized party ask the platform or processor to do?
5. **Processor truth:** What does an external provider report about authorization, capture, refund, dispute, transfer, or payout?
6. **Settlement truth:** What amount actually settled, when, in what currency, and subject to what later reversal risk?
7. **Payout truth:** What amount moved from a processor balance to an external destination?
8. **Accounting truth:** How was an event classified or posted for a specific legal entity, book, period, and accounting policy?
9. **Dispute truth:** What part of the obligation or transaction is challenged, by whom, and with what evidence?
10. **Operational-access truth:** What service or feature consequence is permitted under a separate policy?

No layer may silently overwrite another. A single boolean such as `paid=true` is constitutionally insufficient.

---

# 5. Core Rules

- Financial truth is explicit, sourced, versioned, effective-dated, and auditable.
- Internal status is not proof of external settlement.
- Processor status is evidence within provider scope, not the whole truth.
- Payment is not proof of horse ownership, guardianship, custody, authority, or relationship.
- An invoice is not proof that the underlying obligation is valid.
- A chargeback is not proof of fraud or service failure.
- A write-off is an accounting act and does not automatically extinguish legal rights.
- A refund is money movement and does not by itself rescind an agreement.
- A dispute does not erase history.
- A financial hold must be scoped and must not endanger horse welfare.
- Corrections preserve the original record and use reversal, adjustment, credit note, debit note, or supersession.
- External financial side effects require separate implementation and production authority.

---

# 6. Canonical Vocabulary

The following terms have constitutional meaning:

- **Obligation:** An asserted duty to pay or transfer value.
- **Charge:** A priced component contributing to an obligation or invoice.
- **Invoice:** A versioned billing instrument issued by a specific legal or commercial party.
- **Payer:** A party expected or authorized to provide funds.
- **Payment-method owner:** The person or organization controlling the payment instrument.
- **Merchant or payee:** The party entitled to receive funds for a valid obligation.
- **Beneficiary:** The party for whose benefit value or service is provided.
- **Authorization:** Approval by a processor or financial institution to reserve or permit payment, not settlement.
- **Capture:** A processor action seeking collection of an authorized amount.
- **Settlement:** Confirmed financial completion according to an authorized external source, subject to later reversal or dispute.
- **Payout:** Transfer from a processor balance to an external destination.
- **Refund:** Return of all or part of a prior payment.
- **Credit:** An amount reducing a present or future obligation.
- **Waiver:** An authorized decision not to enforce some or all of an obligation.
- **Write-off:** An accounting decision concerning collectibility.
- **Reversal:** A new event negating or offsetting a prior financial event.
- **Dispute:** A challenge to an obligation, invoice, payment, fee, tax, refund, payout, or allocation.
- **Reconciliation:** Comparison of expected, internal, processor, accounting, and settlement evidence to identify and resolve differences.
- **Unapplied funds:** Received value not yet linked to an authorized obligation.
- **Deferred revenue:** Value collected or billed before the applicable recognition event.
- **Financial hold:** A temporary, scoped restriction on a financial mutation.

---

# 7. Financial Party and Responsibility Roles

Financial roles must be stored as explicit relationships or assignments, not inferred from account ownership or horse ownership.

The controlled role registry should support:

- legal owner;
- beneficial owner;
- service recipient;
- invoice recipient;
- payer;
- primary payer;
- secondary payer;
- split payer;
- guarantor;
- sponsor;
- guardian payer;
- non-guardian payer;
- payment-method owner;
- refund recipient;
- settlement beneficiary;
- merchant;
- connected recipient;
- tax-reporting party;
- collections contact;
- dispute claimant;
- dispute respondent;
- insurer;
- employer;
- organization subscriber;
- estate representative;
- successor organization;
- financial administrator;
- accounting preparer;
- accounting reviewer;
- refund approver;
- payout approver;
- reconciliation owner.

A single party may hold several roles, but one role must never be inferred from another.

---

# 8. Financial Responsibility Allocation

Every material obligation should identify responsible parties, allocation method, amount or percentage, effective period, priority, caps, conditions, source authority, dispute state, and supersession history.

Supported structures may include:

- single payer;
- fixed split;
- percentage split;
- capped contribution;
- sequential responsibility;
- contingent guarantor;
- sponsor contribution;
- insurer contribution;
- owner and lessee allocation;
- guardian and sponsor allocation;
- organization and individual allocation;
- deposit plus balance;
- recurring allocation;
- one-time allocation.

Joint and several responsibility must not be assumed. It requires an approved agreement or governing authority. Changes are effective-dated and must not rewrite prior responsibility periods.

---

# 9. Payers Without Accounts

EquineSync must support legitimate payers who do not maintain platform accounts. A future implementation may use an external contact record, secure invoice or payment link, scoped identity verification, consent capture, delivery evidence, and later account linkage.

Later account creation must link to historical financial activity without duplicating, reassigning, or broadening access to unrelated records.

---

# 10. Obligation Model

Every obligation should preserve at least:

```text
obligation_id
obligation_type
obligation_type_version
legal_entity_id
merchant_id
beneficiary_id
subject_type
subject_id
agreement_id
service_event_ids
responsibility_allocation_ids
currency
gross_amount
credit_amount
tax_amount
fee_amount
net_amount
effective_at
due_at
grace_period_end_at
status
dispute_status
collection_status
waiver_status
write_off_status
jurisdiction
governing_policy_version
created_at
created_by
updated_at
updated_by
correlation_id
```

The obligation is the commercial assertion. It remains distinct from an invoice, payment attempt, settlement, accounting posting, and collection action.

---

# 11. Controlled Obligation and Charge Types

A controlled registry should include boarding, training, lessons, clinics, hauling, veterinary care, farrier care, bodywork, medication, feed, supplements, bedding, turnout, stall, facility rental, arena rental, tack or equipment, repair or damage, late fee, service fee, membership, subscription, deposit, security deposit, cancellation fee, no-show fee, show expenses, reimbursement, refund obligation, tax, platform subscription, and connected-payment fee.

Free-form labels may be preserved for display, but they must not silently become canonical charge categories or accounting classifications.

---

# 12. Invoice Truth

An invoice is a versioned billing instrument. It must identify issuer, merchant, legal entity, recipient relationships, subjects, agreements, service period, line items, currency, totals, due date, delivery state, settlement state, dispute state, and supersession.

Canonical invoice states should distinguish:

`DRAFT`, `APPROVED`, `ISSUED`, `DELIVERY_PENDING`, `DELIVERED`, `DELIVERY_FAILED`, `PARTIALLY_PAID`, `PAID_INTERNAL`, `SETTLEMENT_PENDING`, `SETTLED`, `OVERDUE`, `PARTIALLY_DISPUTED`, `DISPUTED`, `VOID`, `CANCELED`, `PARTIALLY_REFUNDED`, `REFUNDED`, `WAIVED`, `WRITTEN_OFF`, `SUPERSEDED`, and `CLOSED`.

`PAID_INTERNAL` must remain distinct from `SETTLED`. Material changes after issuance require a versioned amendment, credit note, debit note, replacement invoice, or explicit supersession. Issued financial records must not be silently edited.

---

# 13. Line Items

Line items must remain severable so the system can support partial payment, partial dispute, partial refund, split responsibility, distinct tax treatment, and distinct accounting classification.

Each line item should preserve source service event, subject, quantity, unit, unit price, gross amount, discounts, tax, fee, credit, net amount, service date or period, provider, facility, horse, responsibility allocation, tax category, accounting category, and dispute state.

---

# 14. Financial Document Numbering

Invoice, receipt, credit note, debit note, refund, statement, and payout-document numbers must use governed numbering scopes. Numbering rules should identify legal entity, document type, environment, sequence, uniqueness, correction behavior, void handling, and jurisdictional requirements.

Production and test numbering must never share a sequence. Voided numbers remain preserved. Reuse of a prior number is prohibited unless a governing jurisdiction expressly requires a controlled exception.

---

# 15. Payment Lifecycle

The canonical payment lifecycle must distinguish:

`NOT_REQUESTED`, `REQUESTED`, `METHOD_SELECTED`, `AUTHORIZATION_PENDING`, `AUTHORIZED`, `DECLINED`, `CAPTURE_PENDING`, `CAPTURED`, `PROCESSING`, `SETTLEMENT_PENDING`, `SETTLED`, `PAYOUT_PENDING`, `PAID_OUT`, `FAILED`, `CANCELED`, `EXPIRED`, `REVERSED`, `PARTIALLY_REFUNDED`, `REFUND_PENDING`, `REFUNDED`, `DISPUTED`, `CHARGEBACK_OPENED`, `CHARGEBACK_WON`, and `CHARGEBACK_LOST`.

Provider-specific terms map through a versioned adapter. They cannot silently redefine canonical states.

---

# 16. Payment Object

A payment record should identify payer, payment-method owner, merchant, connected recipient where applicable, invoices, obligations, amount requested, authorized, captured, settled, refunded, and disputed, fees, net amount, timestamps, failure evidence, idempotency key, processor objects, policy version, and correlation identifiers.

A payment may relate to multiple invoices or obligations only through an explicit allocation model.

---

# 17. Payment Method Governance

Payment-method possession does not prove identity, ownership, guardianship, or authority. Raw card or bank credentials must not be stored by EquineSync when tokenized provider handling is available.

The system must distinguish cardholder or account owner, payer, invoice recipient, service recipient, authorized user, organization administrator, and refund recipient. Removal or revocation of a payment method must not erase historical evidence.

---

# 18. Idempotency and Duplicate Prevention

Every external financial mutation must use idempotency protections appropriate to the provider and command. Duplicate detection must consider idempotency key, amount, currency, merchant, payer, source invoice, provider object, timing window, and prior result.

A retry after timeout must first reconcile the prior attempt. Blind retries that could create duplicate charges, refunds, transfers, or payouts are prohibited.

---

# 19. Processor Evidence

Processor events must be authenticated, environment-scoped, replay-protected, versioned, timestamped, correlated, and retained according to financial and audit policy.

A webhook receipt does not by itself prove settlement. A dashboard view does not replace an auditable provider object or settlement report. Conflicting provider evidence creates an exception and must block false claims of completion.

---

# 20. Settlement and Payout Truth

Settlement and payout are separate. A payment may settle before the intended recipient receives a payout. A payout may aggregate many settlements, fees, refunds, disputes, reserves, and adjustments.

Payout records should identify connected recipient, destination reference, currency, gross settled amount, fees, reserves, offsets, net payout, expected date, paid date, failure evidence, and reconciliation reference.

A payout does not prove that every underlying obligation or invoice was valid.

---

# 21. Connected Accounts and Financial Identity

Connected-account onboarding, capability status, beneficial ownership verification, tax information, bank destination, representative authority, and processor risk status are distinct from EquineSync identity and relationship authority.

Changes to payout destinations or controlling representatives require elevated authority, step-up verification, notice, cooling-off or review where appropriate, audit, and rollback or hold controls. A connected-account status must not broaden platform permissions.

---

# 22. Platform and Marketplace Funds Flow

Any future marketplace or connected-payment flow must identify customer, merchant of record where applicable, service provider, platform, connected recipient, processor, platform fee, processor fee, transfer amount, reserve, refund responsibility, dispute responsibility, negative-balance responsibility, and customer support route.

EquineSync must not represent that it holds funds in escrow, trust, custody, or stored value unless separately authorized after legal and regulatory review. Platform fees must be disclosed, versioned, linked to the transaction, separately reported, and reversible where required.

---

# 23. Reconciliation

Reconciliation is a constitutional requirement, not an optional reporting feature.

A reconciliation compares:

- expected obligation and invoice state;
- internal payment command and event state;
- processor object and event state;
- settlement or bank evidence where authorized;
- payout and transfer evidence;
- accounting posting or export state.

Each exception should record exact discrepancy, affected amount, currency, legal entity, materiality, owner, age, retries, current hold, investigation notes, resolution, and closure evidence.

Manual correction may repair internal classification or linkage but may not fabricate provider settlement, payout, or refund evidence.

---

# 24. Reconciliation Frequency and Close

Future implementation planning must define reconciliation cadence by financial program and risk. High-risk money movement may require event-driven and daily reconciliation; lower-risk exports may use scheduled review.

Accounting period close must not occur while material reconciliation exceptions remain unresolved unless an authorized reviewer records a controlled exception, materiality rationale, and remediation plan.

---

# 25. Books, Ledgers, and Posting Architecture

EquineSync must distinguish user-facing operational records from accounting records. A future implementation may maintain operational subledgers or generate deterministic posting instructions for an external accounting system.

Potential ledger layers include accounts receivable, customer credits, deposits and prepayments, payment and settlement clearing, processor fees, connected-recipient payables, refund liabilities, tax liabilities, platform subscription billing, and general-ledger export.

This canon does not mandate a specific accounting product or schema. It requires that balances derive from governed events or postings, not direct balance mutation.

---

# 26. Journal Integrity and Correction

Canonical posted entries are append-only. Corrections create reversing and replacement entries. Every reversal identifies the original entry, reason, actor, effective date, posting period, approval, affected statements, tax effect, and payout or settlement effect.

The system must distinguish economic event date, service date, invoice date, posting date, settlement date, entry date, and correction date. Backdating may not conceal late entry, alter closed-period results silently, or evade audit history.

---

# 27. Accounting Periods

Financial periods may use `OPEN`, `SOFT_CLOSE`, `REVIEW`, `CLOSED`, `REOPENED`, and `PERMANENTLY_LOCKED` states.

After close, routine edits are prohibited. Corrections use current-period adjusting entries unless approved otherwise. Reopening requires elevated authority, reason, notice to affected reviewers, and preserved restatement evidence.

Period close must not block emergency care, current payments, authorized refunds, historical access, or dispute filing.

---

# 28. Accounts Receivable and Aging

Receivable states should distinguish current, due, overdue, partially paid, disputed, payment-plan active, collection review, referred, written off, settled, and legally stayed.

Aging basis must be explicit and versioned. Disputed and undisputed balances should be shown separately. Statements should distinguish opening balance, charges, payments, credits, refunds, disputes, adjustments, unapplied funds, and closing balance.

---

# 29. Unapplied Funds, Overpayments, and Credit Balances

Funds received without a clear obligation match are unapplied funds. They must not be silently applied to the oldest invoice without an approved rule or payer direction.

Overpayments may become refundable balances, customer credits, authorized applications to another obligation, or subjects of escheatment review where applicable.

Credit belongs to the legally or contractually entitled party. It does not silently transfer with a horse, barn departure, guardian change, organization acquisition, or account closure.

---

# 30. Payment Application and Allocation

Application order must follow a documented policy or payer instruction. A payment may be allocated by specified invoice, oldest undisputed balance, service period, principal before fee, deposit before recurring balance, or another approved rule.

Reallocation requires authority, reason, preservation of the original allocation, review of tax and payout effects, and notice where appropriate. Allocation must not manufacture delinquency on another obligation without a disclosed rule or payer direction.

---

# 31. Deposits, Prepayments, Packages, and Gift Instruments

Prepaid value may include lesson packages, training packages, clinic packages, boarding prepayments, account credits, promotional balances, service vouchers, refundable retainers, gift certificates, or gift cards.

Prepaid value remains a liability or deferred amount until service delivery, lawful forfeiture, lawful expiration, refund, or another approved recognition event.

Unit-based packages must preserve units purchased, consumed, remaining, expiration, transferability, cancellation, refund basis, restrictions, and price allocation. EquineSync may not implement regulated stored value, a wallet, banking, or money transmission without separate authorization.

---

# 32. Revenue Recognition

Billing, collection, settlement, and revenue recognition are distinct.

Revenue may be billed but unearned, earned but unbilled, paid but deferred, partially recognized, refunded after recognition, or disputed after recognition.

Recognition rules must be versioned by legal entity, service type, accounting basis, effective date, and jurisdiction where relevant. Triggers may include elapsed boarding period, completed lesson, delivered package unit, completed service, subscription period, milestone, or valid cancellation treatment.

EquineSync must distinguish cash-flow views from accrual-style operational views and must not present one as the other.

---

# 33. SaaS Subscription Billing

EquineSync SaaS subscription truth must distinguish plan, entitlement, seat count, billing period, trial, invoice, charge, payment, settlement, credit, refund, pause, cancellation, delinquency, grace period, downgrade, and service restriction.

Entitlement may follow an approved product policy, but entitlement status is not payment settlement. SaaS subscription billing must remain separate from barn-client invoices, connected-account movement, and provider payments.

---

# 34. Barn, Facility, and Provider Billing

Boarding, care, lessons, training, facility use, supplies, and provider services retain source-domain lineage. Every billed line item should link to an approved service event, agreement term, recurring rule, or authorized manual charge.

Barn owner, horse owner, guardian, rider, payer, guarantor, invoice recipient, provider, and beneficiary are independent roles. An organization may issue invoices without EquineSync becoming the merchant or creditor.

---

# 35. Multi-Entity and Intercompany Boundaries

EquineSync may serve property owners, facility operators, boarding companies, training companies, lesson providers, independent professionals, parent organizations, and affiliates.

Books, obligations, merchant identity, taxes, payouts, and records must remain legal-entity specific. One organization must not collect or retain funds for another without an approved agency, marketplace, transfer, or contractual arrangement.

Intercompany activity should identify originating entity, receiving entity, service or allocation basis, amount, tax treatment, approval, and reconciliation.

---

# 36. Taxes

Tax calculation, collection, exemption, reporting, remittance, and filing are distinct activities. Tax rules must be versioned by legal entity, jurisdiction, service or product category, effective date, pricing mode, and exemption evidence.

The system should distinguish tax-inclusive and tax-exclusive pricing, taxable and exempt line items, customer exemptions, marketplace-facilitator treatment, withholding where applicable, and rounding policy.

EquineSync does not provide tax advice and this canon does not authorize tax filing or remittance.

---

# 37. Fees, Commissions, Compensation, and Gratuities

Processor fees, platform fees, late fees, service fees, commissions, provider compensation, and gratuities must remain separately identified.

Compensation rules should preserve rate type, basis, effective period, legal entity, recipient, approval, reversals, and tax classification. Tips or gratuities must not be silently converted into platform revenue or wages. Payroll remains outside scope unless separately authorized.

---

# 38. Currency, Precision, and Foreign Exchange

Every financial object must carry an explicit currency. Amounts use approved precision and rounding rules. Cross-currency activity must preserve source amount, source currency, target amount, target currency, exchange-rate source, rate timestamp, spread or fee, and rounding result.

A future implementation must not silently convert currencies or combine balances across currencies. Foreign-exchange gains or losses require an approved accounting policy.

---

# 39. Refunds, Credits, Waivers, and Write-Offs

These actions are distinct:

- a refund returns prior payment value;
- a credit reduces a present or future obligation;
- a waiver reflects a decision not to enforce an obligation;
- a write-off changes accounting treatment and collectibility posture.

Each action requires authority, amount, scope, reason, effective date, source object, tax effect, accounting effect, recipient or destination, processor evidence where applicable, and audit.

Partial amounts and line-item scope must be supported. Refund destination must be governed and must not be changed merely because the current account holder differs from the original payer.

---

# 40. Disputes and Chargebacks

The platform must distinguish obligation dispute, invoice dispute, service dispute, payment dispute, processor dispute, chargeback, payout dispute, refund dispute, fee dispute, tax dispute, and responsibility-allocation dispute.

A dispute preserves claimant, respondent, amount, currency, reason, narrative, evidence, deadlines, temporary restrictions, processor reference, resolution, and appeal state.

Chargebacks do not automatically prove fraud, invalidate the obligation, or establish service quality. Neutral language is required unless a formal finding supports stronger terminology.

---

# 41. Collections and Delinquency

Delinquency states may include due, grace period, overdue, reminder sent, payment plan offered, payment plan active, promise to pay, collection review, referred, disputed, legally stayed, suspended, written off, and resolved.

Collection authority must define who may send reminders, assess late fees, establish plans, refer accounts, settle, waive, or write off.

Collections activity must not endanger horse welfare. Delinquency, lien assertion, horse release, possession, and legal ownership are separate matters. EquineSync may preserve claims and evidence but must not adjudicate lien validity.

---

# 42. Dunning and Retry Governance

Automated retry and dunning must have approved limits, timing, channel, opt-out or legal constraints, failure handling, and stop conditions.

Retries must cease or enter review when there is a dispute, suspected duplicate, expired authority, invalid payment method, processor ambiguity, legal stay, hardship policy trigger, or maximum attempt threshold.

Dunning communications must state the amount, reason, due date, current status, dispute route, possible service consequence, and what is not being decided.

---

# 43. Payment Plans and Hardship Arrangements

Payment plans must identify covered obligations, schedule, amounts, currency, due dates, grace rules, fees, default rules, modification authority, and effect on collections or service access.

Hardship information is sensitive and must receive restricted access. A hardship request must not become a generalized creditworthiness label or be exposed to unrelated staff.

---

# 44. Service Restrictions for Nonpayment

Permitted restrictions may include blocking new optional bookings, pausing non-essential services, requiring payment-method update, requiring administrator review, or suspending premium platform features under an approved policy.

Nonpayment must not automatically erase records, change ownership, remove guardian authority, block emergency care, delete Horse Passport history, destroy evidence, hide required medical information, or cancel existing obligations.

Restrictions require notice, reason, effective date, scope, review route, restoration conditions, and audit.

---

# 45. Emergency Care and Welfare Boundary

Financial uncertainty, delinquency, or dispute must not prevent recording or communicating emergency care. Emergency veterinary or welfare actions may create later financial obligations, but authority for care and responsibility for payment are separate questions.

A later RF must define emergency financial authorization, spending thresholds, notice, ratification, dispute handling, and welfare safeguards. This canon does not create authority to incur expenses on behalf of another party.

---

# 46. Horse Transfer, Departure, Estate, and Succession

Horse transfer, barn departure, death, estate administration, organization closure, or business succession must preserve financial history without transferring unrelated balances or access automatically.

Open obligations, deposits, credits, disputed charges, asserted liens, and payment plans require explicit continuity treatment. Payment status cannot establish title. A successor organization does not automatically inherit the predecessor's claims, customer credits, merchant identity, or processor accounts.

---

# 47. Minors, Guardians, and Household Privacy

Financial records concerning minors should route to authorized adults while preserving Safe Sport boundaries, scholarship confidentiality, and limited minor-facing information.

Guardian status, payer status, invoice-recipient status, and account administrator status are distinct. Household members must not automatically see one another's payment methods, hardship evidence, compensation, tax forms, or unrelated balances.

---

# 48. Financial Authority and Approval

Every financial command should identify actor, principal, role, organization or barn scope, source object revision, amount, currency, authority source, policy version, purpose, idempotency key, and evidence manifest.

Protected action classes include invoice issuance, manual charge, refund, credit, waiver, write-off, payout release, bank-detail change, settlement override, dispute concession, tax adjustment, commission change, period reopen, reconciliation repair, and collection referral.

Thresholds, reviewer classes, and emergency exceptions must be defined in controlled registries or implementation plans. This canon does not set monetary thresholds.

---

# 49. Segregation of Duties

Where dual control is required, one actor must not both request and independently approve the same protected action. The platform should support separation among preparer, approver, executor, reconciler, and auditor.

Break-glass action requires reason, limited scope, expiration, heightened logging, notice, and post-action review. Break-glass authority must not bypass provider controls or fabricate external evidence.

---

# 50. Permissions and Data Projection

Financial permissions must be relationship-aware, organization-scoped, action-specific, and field-specific. Access to invoices does not imply access to payment methods, tax documents, hardship records, provider earnings, connected-account details, or accounting books.

Exports and reports must apply the same permission and redaction rules as interactive views. Administrative status alone must not grant universal financial access.

---

# 51. Audit and Evidence

Audit records should preserve actor and principal, authority source, source records, before and after states, amount and currency, policy version, approvals, processor evidence references, correlation and causation, reconciliation exceptions, and resolution.

Financial evidence packages should preserve checksum, source, generation time, included period, filters, preparer, reviewer, and reproducibility information. Reports used as evidence must be reproducible from preserved facts and policy versions.

---

# 52. Record Stewardship and Retention

Financial records must align with the Master Record Stewardship and Retention Model. Retention must distinguish operational records, accounting evidence, processor evidence, tax records, disputes, contracts, notices, legal holds, and backups.

Deletion, account closure, or provider termination must not destroy records still subject to retention, dispute, tax, audit, legal-hold, or evidentiary obligations. Sensitive records require minimum-necessary access and secure disposal when authorized.

---

# 53. Communications and Notice

An invoice event, notice generation, attempted delivery, successful delivery, access, and acknowledgment are separate facts.

Financial notices should use plain language and identify amount, reason, due date, responsible party, status, dispute route, service impact, and what the notice does not decide. Notices should support accessible formats, preferred language, controlling-language identification, and delivery evidence.

---

# 54. Analytics and Reporting

Financial analytics may include invoiced revenue, recognized revenue, settled cash, receivables, aging, payment success, refunds, disputes, chargebacks, payout timing, subscription health, reconciliation age, and exception materiality.

Analytics must distinguish gross from net, invoiced from collected, collected from settled, settled from paid out, cash from accrual, current from restated, and disputed from undisputed. Analytics are projections and do not become financial truth.

---

# 55. AI Boundary

AI may assist with categorization suggestions, reconciliation summaries, anomaly surfacing, draft communications, and missing-information checklists only under approved AI governance and human review.

AI must not determine legal responsibility, infer fraud conclusively, assign creditworthiness, approve refunds, issue write-offs, release payouts, change tax treatment, resolve disputes, select payout destinations, initiate money movement, or represent uncertain status as settled.

---

# 56. External Adapter Boundary

Stripe, QuickBooks, banks, tax services, communications providers, and any later vendor are replaceable adapters. Provider objects map to canonical EquineSync objects through versioned contracts.

Adapters must enforce environment separation, signature verification, secret protection, idempotency, replay protection, degraded-state visibility, data minimization, portability, and provider-exit procedures.

No provider account, webhook, OAuth connection, API call, payment rail, accounting sync, or external write is activated by this document.

---

# 57. Environment and Secret Governance

Development, preview, staging, and production must use separate credentials, connected accounts, webhook endpoints, test data, payment methods, numbering, reporting, and logs.

Financial secrets require least privilege, secure storage, rotation, ownership documentation, incident response, and prohibition from client bundles, browser logs, analytics payloads, screenshots, tickets, or plain-text documentation.

---

# 58. Offline and Mobile Boundary

Offline capture may support draft invoices, draft expenses, notes, or evidence only under an approved implementation plan. Offline clients must not independently claim external authorization, capture, settlement, refund, payout, or tax completion.

Queued financial commands require visible pending state, stable idempotency keys, authority revalidation, conflict detection, safe cancellation where possible, and reconciliation after reconnection.

---

# 59. Migration and Legacy Reconciliation

Legacy fields such as `paid`, `balance`, `payer`, `owner_id`, `invoice_status`, `payment_status`, free-form notes, and provider identifiers must not be treated as verified financial truth merely because they exist.

Migration requires source provenance, trust classification, additive shadow mapping where appropriate, reconciliation, exception ledger, access-delta report, no silent dual write, rollback eligibility, and founder authorization.

A migration must not convert ambiguous local state into asserted external settlement.

---

# 60. Business Continuity and Disaster Recovery

Financial operations must define safe degraded behavior for processor outage, webhook outage, bank delay, accounting export failure, communications failure, storage failure, and identity outage.

During outages, EquineSync must avoid falsely marking transactions settled or repeating uncontrolled mutations. Recovery should include event replay, idempotency verification, reconciliation, discrepancy review, user notice where material, and post-incident audit.

---

# 61. Processor Exit and Portability

A provider-replacement plan must address customer references, tokens or migration constraints, connected accounts, open disputes, pending refunds, pending payouts, reserves, historical evidence, webhook shutdown, reconciliation, retention, deletion, and contract termination.

Provider exit must not erase the canonical history required to interpret prior transactions.

---

# 62. Explicit Product and Regulatory Boundaries

Unless separately authorized, EquineSync does not provide banking, lending, credit underwriting, credit scoring, debt buying, escrow, trust-account services, regulated stored value, money transmission, payroll, investment services, tax advice, legal advice, or insurance underwriting.

EquineSync may support records or integrations surrounding these activities only through a separately reviewed legal, compliance, architectural, and implementation boundary.

---

# 63. Controlled Registries Required

Future implementation should use founder-approved registries for:

- financial party and responsibility roles;
- obligation and charge types;
- invoice, payment, settlement, payout, refund, dispute, and collection states;
- books, ledgers, posting rules, and accounting periods;
- application and allocation rules;
- prepayment and package types;
- revenue-recognition policies;
- legal entities and merchant identities;
- intercompany transaction types;
- platform fees, processor fees, commissions, and gratuities;
- reserve and negative-balance types;
- tax categories, pricing modes, and exemption evidence;
- currencies, precision, and exchange-rate sources;
- document-numbering scopes;
- approval thresholds and segregation-of-duties classes;
- reconciliation exception types and materiality;
- financial audit package types;
- retention classes and export profiles;
- business-continuity states;
- implementation and production authority states.

---

# 64. Required Scenario Coverage

Any later implementation plan must cover at least:

- owner is not payer;
- payer is not guardian;
- payer has no account;
- split responsibility;
- guarantor and sponsor;
- insurer contribution;
- partial payment and partial refund;
- unapplied funds and overpayment;
- payment plan;
- failed payment and controlled retry;
- manual cash or check payment;
- processor timeout after capture;
- duplicate or replayed webhook;
- internal paid state without settlement;
- settlement without payout;
- payout failure;
- connected-account bank change;
- tax-exempt party;
- recurring billing and proration;
- prepaid lesson or training package;
- horse transfer with open balance;
- estate or successor responsibility;
- disputed service;
- chargeback;
- emergency veterinary expense;
- scholarship or confidential subsidy;
- deposit return;
- write-off and later recovery;
- legal stay or bankruptcy notice;
- multi-entity allocation;
- currency mismatch;
- offline queued attempt;
- provider outage;
- accounting export drift;
- full audit reproduction.

---

# 65. Canonical Invariants

The following invariants must be testable before implementation acceptance:

1. No single local status proves external settlement.
2. Every material amount has an explicit currency and precision rule.
3. Every protected mutation has authority and audit evidence.
4. Settled history is not overwritten.
5. Reversals link to original events.
6. Payment allocation conserves value.
7. Refunds cannot exceed authorized refundable value without a separately approved exception.
8. A processor retry cannot create an unreviewed duplicate.
9. Cross-entity money movement requires explicit authority.
10. Financial access does not expand identity or relationship authority.
11. Service restrictions do not erase records or block emergency care.
12. Accounting projections can be reconciled to source events.
13. Test and production financial truth cannot mix.
14. AI cannot execute or adjudicate financial authority.
15. Every provider can be replaced without losing canonical interpretation of history.

---

# 66. RF32 Dependency

RF32 Barn Payment Issue Workflow must consume this model and must:

- distinguish obligation, invoice, payment, settlement, payout, refund, dispute, and collection state;
- separate payer, owner, guardian, rider, guarantor, provider, and invoice recipient;
- support partial and split responsibility;
- preserve emergency care and welfare;
- preserve record and evidence continuity;
- avoid ownership, lien, fraud, or guardianship conclusions;
- provide neutral notices, review, and appeal paths;
- keep processor and internal evidence separate;
- prevent adverse silent allocation;
- define restoration after payment or resolution;
- remain planning-only until separately authorized.

---

# 67. Future Payments and Financial Rails RF Dependency

Any future rail-specific RF must define:

- legal entities and merchant identity;
- provider selection and replaceability;
- exact canonical-to-provider mapping;
- connected-account model;
- funds flow and fee disclosure;
- payment, settlement, payout, refund, dispute, and reserve state machines;
- webhook security and idempotency;
- reconciliation and exception operations;
- permissions and approval thresholds;
- data classification and retention;
- tax and accounting boundaries;
- migrations and rollback;
- support and incident runbooks;
- sandbox evidence;
- staged production activation;
- explicit founder production authority.

---

# 68. Accounting Integration Dependency

A QuickBooks or other accounting integration must remain an adapter and projection unless a later approved design establishes otherwise.

The integration RF must define directionality, source precedence, duplicate prevention, chart-of-accounts mapping, legal-entity scope, posting granularity, period lock behavior, tax mapping, reversals, deleted or edited external records, reconciliation, disconnect behavior, and historical evidence.

An accounting system may be authoritative for approved accounting books while EquineSync remains authoritative for its own domain obligations, invoices, relationships, and source events. The boundary must be explicit.

---

# 69. Implementation Gates

Before financial implementation, the following are required:

- founder approval and controlled adoption of this model;
- no unresolved P0 or blocking P1 canon conflict;
- exact domain schemas and state machines;
- permission and approval matrix;
- threat model;
- legal and tax review where applicable;
- provider and environment ownership;
- secret and webhook plan;
- reconciliation operating model;
- migration and rollback plan;
- executable invariant and adversarial tests;
- evidence package;
- separate implementation authorization.

Before production activation, additional requirements include contracts and accounts, environment isolation, live credentials, monitoring, incident and support runbooks, finance operations, reconciliation staffing, staged rollout, disable controls, recovery validation, and explicit founder production release authority.

---

# 70. Explicit Prohibitions

This document does not authorize:

- payment-provider activation;
- production charges, captures, refunds, transfers, or payouts;
- connected-account onboarding;
- banking or payout-detail changes;
- schema implementation or migration;
- data backfill;
- QuickBooks write synchronization;
- tax filing or remittance;
- collections activity;
- service suspension;
- payroll;
- legal conclusions;
- permission expansion;
- AI financial decision authority;
- RF32 implementation;
- any financial-rails RF opening unless separately directed;
- production mutation;
- public launch.

---

# 71. Version 2.1 Resolution of the Prior Gap

Version 2.1 resolves the previously identified constitutional gap by expressly:

1. separating EquineSync SaaS billing from barn, provider, and marketplace financial rails;
2. defining obligation, invoice, payment attempt, processor evidence, settlement, payout, accounting, and access as separate truths;
3. establishing source-of-truth and adapter rules;
4. making reconciliation and exception handling mandatory;
5. distinguishing refunds, credits, waivers, write-offs, disputes, and chargebacks;
6. defining connected-account and marketplace boundaries without authorizing them;
7. defining revenue recognition, period close, ledgers, and accounting projections;
8. preserving multi-entity and intercompany separation;
9. adding authority, approval, segregation of duties, and break-glass rules;
10. preserving horse welfare, emergency care, identity, relationship, transfer, and record boundaries;
11. adding continuity, provider exit, offline, migration, and audit requirements;
12. defining the prerequisites for RF32, future payment rails, and accounting integration work.

---

# 72. Founder Decision Posture

Version 2.1 adopts the following recommended constitutional posture for founder review:

- EquineSync may maintain operational financial subledgers and deterministic posting instructions, but a later implementation decision will select exact accounting architecture.
- Unapplied funds and overpayments remain separate until authorized application or refund.
- Payment application follows explicit policy or payer direction; no silent adverse allocation.
- Prepaid packages are deferred value until an approved recognition event.
- Revenue recognition is separate from invoicing, collection, settlement, and payout.
- Multi-entity support is permitted only with legal-entity-specific books, merchant identity, tax, and reconciliation.
- EquineSync is not deemed merchant of record, escrow holder, money transmitter, payroll provider, lender, or credit bureau by this canon.
- Connected-account activation and funds movement require a separate rail-specific RF.
- High-impact actions require configurable thresholds and segregation of duties.
- Financial privacy for minors, households, providers, and hardship evidence is mandatory.
- Processor exit, disaster recovery, audit reproducibility, and reconciliation are mandatory production prerequisites.

---

# 73. Adoption Criteria

This model is ready for founder-approved controlled adoption when:

- cross-canon review confirms alignment with Identity, Relationships, Agreements, Claims, Audit, Record Stewardship, Communications, External Architecture, Horse Transfer, and Platform Operations;
- prior Version 2.0 material is preserved in a delta or preservation record;
- no P0 finding remains;
- no blocking P1 finding remains;
- retained P2 observations are assigned and nonblocking;
- RF32 and future financial-rails dependencies are confirmed;
- controlled registries are accepted as future implementation dependencies rather than active schemas;
- explicit prohibitions remain intact;
- no production or implementation authority is implied;
- founder approval is recorded.

---

# 74. Required Controlled Review Outputs

The controlled review of Version 2.1 should produce:

1. `MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_ALIGNMENT_REPORT.md`
2. `MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_DELTA_MATRIX.md`
3. `MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_PRESERVATION_MATRIX.md`
4. `MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_FINDINGS_REGISTER.md`
5. proposed `CANON_INDEX.md` insertion;
6. proposed RF32 dependency amendment;
7. proposed future Payments and Financial Rails RF dependency text;
8. proposed accounting-integration dependency text;
9. repository financial reality inventory;
10. financial source-of-truth and reconciliation matrix;
11. funds-flow and legal-entity risk register;
12. complete non-implementation attestation;
13. founder decision record.

---

# 75. Lifecycle and Stop State

Current lifecycle:

`DRAFTED_V2_1 -> CONTROLLED_CROSS_CANON_REVIEW -> FOUNDER_REVIEW`

Future states require separate founder acts:

`FOUNDER_APPROVED -> CONTROLLED_ADOPTION -> LOCKED`

This candidate stops at:

`MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_READY_FOR_CONTROLLED_CROSS_CANON_REVIEW`

No adoption, lock, implementation, migration, payment activation, connected-account onboarding, accounting synchronization, production charge, production refund, payout, tax action, collections action, service restriction, permission change, RF opening, or public launch is authorized by Version 2.1.

---
