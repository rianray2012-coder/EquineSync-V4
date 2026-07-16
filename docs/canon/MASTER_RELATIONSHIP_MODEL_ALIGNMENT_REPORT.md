# Master Relationship Model Alignment Report

Status: `MASTER_RELATIONSHIP_MODEL_READY_FOR_FOUNDER_REVIEW`

## Intake Boundary

This report reviews the supplied `MASTER_RELATIONSHIP_MODEL.md` as proposed
canon. It does not adopt or lock the document, modify production code, change
permissions or Passport behavior, migrate data, open RF31-RF36, activate an
external service, or modify RF29 or RF30.

Source reviewed in full:

- Source path: `/Users/rianray/Downloads/MASTER_RELATIONSHIP_MODEL.md`
- Source lines: 1,622
- Source SHA-256: `b46602a552a4919bcc4fb1af4b1141c8929bf0ab47bc620079a00b7a44025fdf`

## Decision Summary

The model is suitable for founder review as the presumptive governing
relationship concept. No direct conflict with locked canon was proven. It
specializes and makes operational the existing principles that:

- horses retain identity across changing relationships;
- ownership, custody, access, authority, responsibility, and authorship are
  distinct;
- relationships and permissions are scoped, temporal, revocable, and audited;
- historical evidence survives the end of current access; and
- external vendors are adapters rather than domain authorities.

The model is not a description of current implementation. Repository reality is
fragmented and transitional. Adoption should therefore govern RF31, RF32, and
later convergence without implying that a canonical relationship store or
complete relationship graph already exists.

## Canon Placement

Proposed canonical path:

`docs/canon/MASTER_RELATIONSHIP_MODEL.md`

Proposed hierarchy: Tier 3 foundational domain canon, subordinate to the Master
Product Vision and Master Ecosystem Model, co-governing with the Horse, Barn,
Facility, and Business lifecycle/domain canons, and upstream of the Master
Permission Model's enforcement design.

Authority resolution:

1. Master Product Vision decides product purpose.
2. Master Ecosystem Model decides ecosystem identity and cross-domain placement.
3. Master Relationship Model decides relationship semantics and temporal truth.
4. Domain lifecycle canons decide domain-specific lifecycle behavior.
5. Master Permission Model decides authorization and field-level enforcement.
6. An unresolved contradiction stops work for founder review; no document may
   silently override another locked canon.

## Explicit Coverage Review

| Required area | Model coverage | Repository comparison |
| --- | --- | --- |
| Legal and co-ownership | Strong: legal, beneficial, percentage, syndicate, decision, dispute, and evidence concepts. | Current horse records use singular/list owner identifiers and derived Care Circle members; no verified temporal ownership ledger or percentage model was found. |
| Leases, custody, possession, boarding, training, riding | Strong conceptual separation and authority limits. | Lease grants remain deferred; custody is partly represented by barn/location assignment; trainer/rider links are mostly role and ID fields without a shared lifecycle. |
| Guardians and minors | Strong: authority, consent, communication, payment, court restrictions, and age-of-majority transition. | `guardian_links`, student profiles, account memberships, and a separate guardian-minor intake profile divide current truth. A payer is not consistently distinguished from a guardian everywhere. |
| Care Circle | Strong scope, acceptance, dates, revocation, and audit requirements. | `horse_care_circle_members` supports role, status, permissions, notifications, and audit, but defaults can derive owner/trainer/provider members from horse and assignment fields. It lacks the complete temporal, authority, verification, dispute, and supersession contract. |
| Service providers | Strong service-specific, least-privilege model for individual and business relationships. | Access is driven by active `horse_provider_assignments`; provider user, provider business, barn scope, grant authority, and historical access are not unified as one canonical relationship. |
| Staff, contractors, organizations, and facilities | Strong distinction among person, organization, operator, property owner, and facility scopes. | `users.barn_id`, `users.role`, additive `account_memberships`, facility locations, and route-level role sets coexist. Organization and facility are not consistently independent canonical principals. |
| Financial responsibility | Strong separation of payer, owner, guardian, recipient, guarantor, and allocation. | Invoices primarily use `owner_id`; local invoice state can be marked paid without proving provider settlement. Multi-payer allocation and temporal responsibility are absent. |
| Agreement responsibility | Strong party/effect/continuity principles. | Document requests model subject, guardian, and countersigner IDs, but agreement effects do not yet bind to versioned relationship records. |
| Calendar participation | Strong relationship-derived participation and visibility principle. | Locked RF29 synthetic Calendar envelopes use relationship arrays and permission projection, but runtime controls remain disabled and participants do not resolve through a canonical relationship service. |
| Communication routing | Strong: active scope, consent, guardian rules, and preferences govern recipients. | Notification preferences exist in several domain records; no single relationship-aware recipient resolver was found. Delivery does not prove authority or consent. |
| Start/end dates and revocation | Strong lifecycle and temporal contract. | Current status fields are mostly lowercase, collection-specific, and often lack effective dates, verification, supersession, and reason-coded termination. |
| Transfer, departure, and Passport continuity | Strong coordinated-transition and data-classification model. | Passport composes current records but explicitly exposes no transfer action. RF27 excludes ownership/custody change. Formal transfer, former/new access transition, and transfer history remain RF31 gaps. |
| Historical visibility and stewardship | Strong purpose-based principles and non-destructive correction. | Existing records preserve authorship unevenly; access often follows current barn or relationship fields. No shared post-termination access policy was found. |
| Disputes and competing claims | Strong neutral preservation and no-silent-winner rule. | No canonical relationship dispute or legal-hold workflow was found. Route-local latest/current fields could otherwise behave as the practical winner. |
| Death, retirement, sale, lease, trial, rescue, and estate | Broad and materially aligned with Horse Lifecycle canon. | Current horse status is not a governed relationship-transition engine. Estate, rescue/surrender, sale pending, and trial authority are not implemented as first-class relationships. |
| Duplicate horse scenarios | Strong continuity and human-review requirement. | No canonical transfer-time identity resolution or governed merge workflow was found. Matching by mutable attributes would be unsafe without confidence and review controls. |
| Audit lineage | Strong minimum event contract. | Care Circle, facility, agreement, Calendar, billing, and other domains use separate audit/event shapes. No shared relationship correlation contract exists. |
| Migration and extensibility | Strong quarantine, reconciliation, rollback, and no-production-mutation rules. | Relationship-like data is distributed across many collections and compatibility mirrors. Migration would be high risk and requires a separately authorized inventory and dry-run plan. |

## Locked Canon Alignment

### Aligned

- `MASTER_ECOSYSTEM_MODEL.md` already treats roles as relationships, requires
  current and historical graph edges, and prohibits collapsing ownership,
  custody, and access.
- `MASTER_HORSE_LIFECYCLE.md` already requires durable horse identity,
  transfer continuity, leases, custody, disputes, retirement, death, estates,
  duplicate prevention, and historical preservation.
- `MASTER_BUSINESS_LIFECYCLE.md` already distinguishes businesses from users,
  facilities, provider roles, and payment profiles.
- `MASTER_FACILITY_DOMAIN_MODEL.md` expressly prevents location assignment from
  implying ownership, custody, or Passport transfer approval.
- `MASTER_PERMISSION_MODEL.md` already requires context, relationship, scope,
  delegation, revocation, field projection, and preserved authorship.
- RF29's locked Calendar boundary agrees that external calendars are projections
  and do not own EquineSync-created event truth.
- RF30's locked AI boundary remains untouched; AI cannot infer, create, or alter
  relationship authority from this conceptual model.

### Terminology Reconciliation Needed

- The model calls RF31 `Horse Identity & Transfer Continuity`; repository
  governance assigns RF31 to `Horse Arrival and Transfer Continuity`, while the
  founder context uses `Horse Transfer / Passport Continuity`. Use one approved
  title and preserve RF27's ownership of physical intake.
- Canon and implementation use both `barn` and `facility`. The model should state
  that a barn may be a business, operating context, or colloquial place, while a
  facility is the canonical physical-place entity and an organization is the
  legal/operating principal.
- Proposed uppercase relationship statuses differ from current lowercase API and
  database conventions. Treat uppercase names as semantic vocabulary and require
  an explicit normalization map rather than a silent storage-format change.
- `owner`, `parent`, `vendor`, and similar values currently appear as user roles,
  membership relationship types, Care Circle member types, and business labels.
  The model correctly separates them, but a canonical type registry is still
  required.

## Principal Schema and Permission Gaps

1. No canonical `relationships` aggregate or service implements the proposed
   object, lifecycle, versioning, validation, or event contract.
2. Current horse access can derive from mutable ID arrays such as owner, guardian,
   rider, and trainer fields, plus barn scope and Care Circle records.
3. Care Circle defaults are type-based. They are safer than broad provider
   access because projections redact fields, but do not yet prove source
   authority, effective dates, acceptance, verification, or supersession.
4. Account memberships are explicitly compatibility mirrors for `users.barn_id`
   and `users.role`; they are not the final multi-context relationship model.
5. Guardian truth is split among `guardian_links`, user roles/memberships, student
   profiles, and guardian intake profiles. Multi-guardian conflict, court limits,
   age-of-majority transition, and payer-not-guardian cases need RF planning.
6. Provider access is grant-based and horse-scoped, but provider person,
   provider business, source authority, appointment scope, and post-service
   historical access are not one governed relationship.
7. Billing's `owner_id` does not represent the model's payer, recipient,
   guarantor, allocation, and effective-period distinctions.
8. Agreement signers and Calendar participants reference user IDs directly; they
   do not yet bind to a versioned relationship and authority snapshot.
9. Facility occupancy records describe location and presence, not ownership or
   custody. RF31 must preserve that locked RF27 boundary.
10. Current permissions are distributed across role guards, tenant filters,
    capability maps, grants, and projection functions. Relationship truth must
    not bypass existing field-level redaction during future convergence.

## Migration Risk Register

| Risk | Severity | Required planning response |
| --- | --- | --- |
| Inferring legal ownership from `owner_id`, creator, payer, or current barn | P1 | Import as unverified unless approved evidence establishes authority. |
| Turning derived Care Circle members into verified legal/operational relationships | P1 | Preserve provenance and require acceptance/verification rules by type. |
| Conflating organization, barn account, and physical facility | P1 | Establish canonical principals and explicit organization-facility relationships first. |
| Changing current permissions while backfilling relationships | P1 | Run additive shadow/dry-run reconciliation; no access expansion or contraction without separate authorization. |
| Losing former-barn/provider authorship through current-barn scoping | P1 | Define record stewardship and post-termination projection before transfer execution. |
| Equating invoice owner with payer or settled money | P1 | Backfill responsibility as unverified and preserve provider settlement lineage separately. |
| Duplicate active relationships from ID arrays, memberships, grants, and Care Circle rows | P1 | Use stable source keys, precedence rules, exception ledger, and idempotent replay. |
| Uppercase/lowercase status drift | P2 | Publish canonical semantic-to-storage normalization. |
| Binary relationship object cannot faithfully represent multi-party agreements, co-owner decisions, or group participation | P1 | Add a participant/party-edge pattern before schema authorization. |
| Privacy erasure and legal retention conflict with blanket soft-delete wording | P1 | Add legal/privacy exception and hold policy; do not let application deletion destroy required audit lineage. |

## Proposed CANON_INDEX.md Insertion

Insert in the Canon Hierarchy after the Master Ecosystem Model and before the
lifecycle/domain rows:

```markdown
| 3 | Master Relationship Model | `docs/canon/MASTER_RELATIONSHIP_MODEL.md` | founder-approved / available | Authority for explicit, temporal, scoped, auditable relationships among horses, people, organizations, facilities, providers, guardians, payers, agreements, permissions, transfers, and historical continuity. |
```

Add to the Mandatory Application Rule:

```markdown
Every RF or feature that creates, infers, modifies, suspends, disputes, revokes,
transfers, or consumes a relationship must trace to
`MASTER_RELATIONSHIP_MODEL.md`. Role labels, payment events, signatures,
calendar participation, facility membership, current possession, and external
provider events are not independent proof of authority.
```

The insertion must occur only after founder approval and preservation of the
reviewed source as `docs/canon/MASTER_RELATIONSHIP_MODEL.md`.

## Proposed RF Dependency Updates

### RF31

Add:

```markdown
Canonical dependency: `MASTER_RELATIONSHIP_MODEL.md`.

RF31 must implement horse transfer and Passport continuity as coordinated,
versioned relationship transitions. It must preserve RF27 physical-intake and
facility-location ownership boundaries; distinguish ownership, custody,
boarding, training, lease, payer, guardian, Care Circle, and provider authority;
preserve historical authorship and visibility rules; prevent duplicate horses;
and quarantine disputed or unverified claims. No transfer may infer legal
authority from creator, payer, signer, current barn, possession, or role alone.
```

### RF32

Add:

```markdown
Canonical dependency: `MASTER_RELATIONSHIP_MODEL.md`.

RF32 must model financial responsibility independently from legal ownership,
guardianship, riding, account identity, invoice recipient, and provider
settlement. Payment failure may alter only founder-approved operational effects;
it must not erase ownership, Passport history, emergency-care duties, guardian
authority, record stewardship, or dispute evidence. Payer changes and disputes
must be effective-dated, auditable, and historically preserved.
```

## ATLAS5 Dependency Update

Add to ATLAS5 predecessor language:

```markdown
ATLAS5 external-service readiness is downstream of the founder-approved Master
Relationship Model and RF31/RF32 planning. External vendors consume or report
relationship-linked events; DocuSign, Stripe, communications providers,
calendar providers, storage vendors, identity vendors, and AI providers do not
create EquineSync relationship authority. RF33-RF36 remain proposed and unopened.
```

## Founder Decisions

1. Approve the document as Tier 3 canon and approve the authority-resolution
   order stated above.
2. Approve one RF31 title while preserving RF27 physical intake boundaries.
3. Decide whether the canonical relationship contract is binary plus party-edge
   records, or supports first-class multi-party relationships.
4. Approve the initial controlled relationship-type and authority-source
   registries; the document currently describes categories but does not enumerate
   a closed launch registry.
5. Decide beneficial-ownership launch scope and legal/privacy treatment.
6. Decide co-owner voting/delegation depth and transfer approval thresholds.
7. Decide former-barn and former-provider direct historical access versus export
   or administrator-mediated access.
8. Decide which records are horse-canonical, organization-retained, party-private,
   consent-transferable, or legally restricted.
9. Approve the guardian/minor control model, multi-guardian conflicts, court-order
   handling, and age-of-majority transition.
10. Decide payer-without-account, guarantor, split-payer, and recipient rules for
    RF32.
11. Approve emergency authority, treatment, and spending limits by relationship.
12. Decide which disputes freeze transfers or permission changes and who may
    impose temporary restrictions.
13. Approve which imported relationships may be verified, self-attested, or
    quarantined.
14. Approve privacy-erasure, legal-retention, litigation-hold, and soft-delete
    precedence.
15. Decide whether breeding ownership, reproductive material, foster/sanctuary,
    law-enforcement seizure, and insurance-agent relationships belong in the
    initial registry or governed extensions.

## Stop-State Attestation

- Model locked: `false`
- Canon index changed: `false`
- RF31 or RF32 implemented/opened by this review: `false`
- RF33-RF36 opened: `false`
- Production code or data changed: `false`
- Permissions or Passport behavior changed: `false`
- External service activated: `false`
- RF29 or RF30 modified: `false`

`MASTER_RELATIONSHIP_MODEL_READY_FOR_FOUNDER_REVIEW`
