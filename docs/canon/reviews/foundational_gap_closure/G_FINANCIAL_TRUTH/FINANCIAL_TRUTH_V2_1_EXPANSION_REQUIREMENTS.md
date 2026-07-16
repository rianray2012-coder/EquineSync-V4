# Financial Truth V2.1 Expansion Requirements

## Founder disposition

- Financial Truth V2.0: `ACCEPT_WITH_MODIFICATION`
- Constitutional direction: approved
- Lock: not approved
- V2.1 expansion required before lock: true
- Implementation, schema, processor, payment, production, and release authorization: false

## Required expansions

### 1. Financial invariants

V2.1 must state immutable constitutional invariants, including:

- money cannot disappear or duplicate;
- settlement cannot precede the required authorization/capture evidence;
- refunds cannot exceed the eligible settled amount except through an explicitly governed independent credit;
- payouts cannot exceed available verified settlement and approved reserves;
- negative balances require explicit authority and visible provenance;
- every balance must be reproducible from canonical entries;
- currency conversion requires an attributable rate source, timestamp, precision, rounding, and gain/loss treatment;
- reversal and correction preserve original entries and conservation proofs;
- unknown processor outcomes remain pending and reconcile before retry.

### 2. Trust, escrow, held, and custodial funds

V2.1 must distinguish platform funds, merchant funds, customer funds, deposits, held-in-trust funds, escrow, custodial funds, processor reserves, and pass-through amounts. It must prohibit EquineSync from describing a balance as trust or escrow without the legal structure, account segregation, agreements, licensing, controls, reconciliation, and qualified review required for that representation.

Potential contexts include show entries, clinic fees, consignment, horse purchases, boarding/security deposits, and marketplace transactions. No held-funds capability is authorized by this requirement.

### 3. Multi-entity accounting

V2.1 must model organization boundaries, legal entities, barn operating contexts, facilities, trainers, providers, franchises, enterprises, associations, nonprofits, rescues, branches, and consolidated views without commingling obligations or funds. Inter-company obligations, settlements, shared ownership, allocations, eliminations, and transfer pricing require explicit entity, authority, jurisdiction, and evidence.

### 4. Revenue recognition boundaries

V2.1 must distinguish invoice, obligation, cash received, processor capture, verified settlement, earned revenue, unearned/deferred revenue, deposit liability, refund liability, payout payable, fee/commission revenue, tax liability, and write-off. Recognition policy requires qualified accounting review and must not be inferred from payment state alone.

### 5. Financial event provenance chain

Every financial event must reference its originating domain object, workflow, actor/principal, authority, relationship context, agreement/consent where applicable, policy version, source revision, evidence manifest, idempotency identity, correlation/causation chain, effective/recorded time, processor mapping, and reconciliation outcome.

## Required V2.1 evidence

1. Full integrated successor candidate rather than a detached appendix.
2. V2.0-to-V2.1 preservation matrix.
3. Cross-canon review against Relationship, Stewardship, Claims, Permission, Audit, Agreement, Identity, External Architecture, Business Lifecycle, RF31, RF32, and proposed RF35.
4. Legal/tax/accounting review requirements and founder decision ledger.
5. Invariant and failure-scenario library.
6. Updated dependency, state/lock, owner/steward, and implementation-authorization registries.
7. Checksum-backed founder review package.

`FINANCIAL_TRUTH_V2_1_EXPANSION_REQUIRED_BEFORE_LOCK`
