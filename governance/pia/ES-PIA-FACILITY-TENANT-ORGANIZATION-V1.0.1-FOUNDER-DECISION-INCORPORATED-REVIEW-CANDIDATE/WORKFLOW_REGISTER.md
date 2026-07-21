# Workflow Register

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`  
**Execution status:** design specification only; no application or service was started

Every workflow requires attributable evidence, an explicit failure oracle, and audit records. Architecture concepts are progressively disclosed only when they serve the actor’s immediate purpose.

| Workflow | Name | Actor | Preconditions | Action | Expected design result | Decisions |
|---|---|---|---|---|---|---|
| FAC-WF-001 | Individual owner horse-first onboarding | Unaffiliated owner | Minimum Tenant isolation context exists | Add horse without Facility or Organization creation | Horse record is tenant-scoped; no Facility, Organization, membership, stewardship, or permission is inferred | FAC-FD-002;FAC-FD-017 |
| FAC-WF-002 | Later Facility association | Owner | Horse-first onboarding completed | Assert a boarding relationship and associate a real Facility | Temporal association is recorded; private projections remain isolated; authority remains separately evaluated | FAC-FD-004;FAC-FD-009;FAC-FD-017 |
| FAC-WF-003 | Independent trainer onboarding | Independent trainer | Minimum Tenant context exists | Create trainer operating context without legal Organization | No Organization is fabricated; no role label grants permission | FAC-FD-006;FAC-FD-011;FAC-FD-017 |
| FAC-WF-004 | Later Organization association | Trainer | Independent operation exists | Create or associate a real Organization with evidence | Temporal Organization relationship is recorded; prior history remains; access is separately granted | FAC-FD-003;FAC-FD-006;FAC-FD-017 |
| FAC-WF-005 | Facility topology setup | Facility operator | Explicit provisioning and permission inputs exist | Create Facility and governed containment nodes | One-parent effective containment and separate adjacency are auditable | FAC-FD-005;FAC-FD-007 |
| FAC-WF-006 | Shared Facility with separate Tenants | Two operators | Stable Facility identity and two active Tenants exist | Create two scoped temporal Tenant-Facility associations | Each Tenant sees only its private projection; shared topology facts are minimized | FAC-FD-002;FAC-FD-004;FAC-FD-010;FAC-FD-016 |
| FAC-WF-007 | Organization governs multiple Tenants | Organization representative | Verified Organization and control evidence exist | Establish temporal control links, then grant access per Tenant | Control and access remain separate; common ownership does not collapse isolation | FAC-FD-002;FAC-FD-003 |
| FAC-WF-008 | Active context switch | Multi-context user | Eligibility in target context exists | Switch Tenant and optional Facility with confirmation | Prior/new context, actor, version, and outcome are audited; wrong-context action fails closed | FAC-FD-009 |
| FAC-WF-009 | Duplicate Organization candidate | Reviewer | Similarity signals exist | Review candidate and decide without automatic merge | Uncertainty, conflict record, lineage, and reversal plan remain | FAC-FD-015 |
| FAC-WF-010 | Ambiguous legacy Facility import | Migration reviewer | Ambiguous source row exists in authorized future migration | Place row in tenant-scoped quarantine | No guessed entity, public projection, or authority is created | FAC-FD-018 |
| FAC-WF-011 | Provider capability association | Provider representative and Tenant authority | Real provider Organization and agreement evidence exist | Grant explicit governed capability for stated scope and period | Only stated capability is available; accountable human actor and audit remain | FAC-FD-006;FAC-FD-013 |
| FAC-WF-012 | Facility closure or transfer | Authorized topology-change reviewers | Proposed change and dependency inventory exist | Review, approve, effect, and reconcile change | Lineage persists; no horse, person, Relationship, invoice, permission, agreement, or evidence cascades | FAC-FD-007;FAC-FD-008 |

## Failure and recovery controls

Wrong-context, stale-evidence, ambiguous-identity, unsupported-association, and missing-permission paths fail closed without cross-Tenant enumeration. Retries are idempotent; interruption preserves the last confirmed state; recovery re-evaluates current context and authority. No workflow uses hidden manual repair, automatic merge, automatic authority, or automatic downstream transfer.
