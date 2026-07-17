# Master EquineSync Implementation Atlas Founder Decision Log

**State:** `PENDING_FOUNDER_DISPOSITIONS`  
**Allowed dispositions:** `APPROVE_AS_RECOMMENDED`, `APPROVE_WITH_MODIFICATION`, `DEFER_WITH_BLOCK`, `DEFER_WITHOUT_BLOCK`, `REJECT`, `REQUEST_ADDITIONAL_ANALYSIS`

No record below grants authority until a durable founder disposition expressly does so.

## MEIA-FD01 - Atlas disposition

- **Affected section/dependency:** Whole Atlas; review report and manifest; all canon and locked RF/ATLAS dependencies
- **Current state:** Controlled candidate; P0 0/P1 6/P2 3
- **Issue/importance:** Decide whether the corrected planning instrument may become adopted orchestration authority without becoming constitutional or operational authority.
- **Options:** Adopt; adopt with follow-up; revise/re-review; retain candidate; reject.
- **Recommendation/rationale:** `APPROVE_AS_RECOMMENDED` as `ADOPTED_PLANNING_ATLAS_NOT_LOCKED`, with all P1 implementation blocks and P2 observations retained. The candidate is accurate enough to coordinate work without authorizing it.
- **Approval/deferral consequences:** Approval creates one planning reference only; deferral preserves fragmented planning and blocks formal Atlas adoption.
- **Wave/authority impact:** All waves gain traceability; no Wave, implementation, or production authority.
- **Atlas change/language:** Status-only adoption record after separate authorization; do not alter candidate bytes during decision recording. Proposed: “Adopted planning and orchestration authority; implementation and production authority false.”
- **Blocking/nonblocking:** Blocks Atlas adoption; does not block unrelated already-authorized work. Review remains nonblocking.
- **Founder disposition:** `APPROVE_AS_RECOMMENDED`; `ADOPTED_PLANNING_ATLAS_NOT_LOCKED`

## MEIA-FD02 - Wave 0 convergence authorization

- **Affected section/dependency:** Wave 0; ATLAS Governance; Canon Index/registries; existing code and infrastructure evidence
- **Current state:** `AUTHORIZED_FOR_CONTROLLED_CANON_INTEGRATION_AND_LOCK`; completed for verified Wave 0 scope
- **Issue/importance:** Decide whether Codex may perform read-only inventory, traceability, decision-register, and backlog preparation.
- **Options:** Authorize documentation/read-only Wave 0; authorize a narrower subset; defer; request task-level package.
- **Recommendation/rationale:** `APPROVE_WITH_MODIFICATION`: authorize a separately bounded Wave 0 package limited to read-only discovery and documentation, with no code/schema/config/secrets/live-service changes.
- **Approval/deferral consequences:** Approval enables convergence evidence; deferral leaves P1-06 unresolved and affected implementation blocked.
- **Wave/authority impact:** Wave 0 only; no implementation or production authority.
- **Atlas change/language:** No current text change. Supplemental authorization must name paths, outputs, stop state, and prohibited actions.
- **Blocking/nonblocking:** Blocks Wave 0 execution; nonblocking for Atlas adoption.
- **Founder disposition:** `APPROVE_WITH_MODIFICATION` recorded by directive; governance/canon integration and lock only

## MEIA-FD03 - Identity lock disposition

- **Affected section/dependency:** Workstream B, Phase/Wave 1; adopted Identity V2.0 and completed lock review
- **Current state:** `IDENTITY_V2_0_LOCKED`; `CONTROLLING_AND_LOCKED`; two open nonblocking P2s
- **Issue/importance:** Decide constitutional immutability before identity-dependent implementation.
- **Options:** Lock; defer with Wave 1 block; return for correction.
- **Recommendation/rationale:** `APPROVE_AS_RECOMMENDED` through the separate Identity lock directive; lock evidence passed and operational authority remains false.
- **Approval/deferral consequences:** Approval stabilizes the dependency; deferral blocks Wave 1 runtime implementation but not Atlas adoption.
- **Wave/authority impact:** Wave 1 dependency only; no identity implementation authority.
- **Atlas change/language:** Update status only after actual lock. Proposed: “Identity V2.0 locked; P2s retained; implementation false.”
- **Blocking/nonblocking:** Blocks Wave 1 runtime; nonblocking for Atlas adoption and inventory.
- **Founder disposition:** `APPROVE_AS_RECOMMENDED` recorded through the Identity V2.0 final lock directive

## MEIA-FD04 - Pilot and public-launch scope

- **Affected section/dependency:** Release train, product experiences, Definition of Ready; Product Vision; Platform Operations candidate
- **Current state:** Unresolved
- **Issue/importance:** Define roles, modules, facility model, support, and safety boundaries for each release stage.
- **Options:** Single-barn pilot; selective multi-facility pilot; broader closed beta; defer public-launch scope.
- **Recommendation/rationale:** `DEFER_WITHOUT_BLOCK` for public launch while separately defining a narrow closed-pilot scope before release planning.
- **Approval/deferral consequences:** Approval bounds evidence and support; deferral blocks release promotion, not Atlas adoption or foundational planning.
- **Wave/authority impact:** Release gates and all user-facing waves
- **Atlas change/language:** Add selected pilot scope only after decision. Proposed language must enumerate roles/modules and exclusions.
- **Blocking/nonblocking:** Blocks pilot/release promotion; nonblocking for Atlas adoption and pre-release planning.
- **Founder disposition:** `PENDING`

## MEIA-FD05 - Identity/auth implementation posture

- **Affected section/dependency:** Wave 1; Identity, Permission, Relationship, External Architecture; current custom bcrypt/JWT implementation
- **Current state:** Existing custom implementation observed; replacement/provider decision absent
- **Issue/importance:** Avoid duplicate identity sources, unsafe migration, or ungoverned provider dependence.
- **Options:** Harden current system; adopt external provider later; hybrid/federation; defer provider selection.
- **Recommendation/rationale:** `REQUEST_ADDITIONAL_ANALYSIS`: first produce a read-only implementation inventory, threat model, recovery analysis, and migration alternatives.
- **Approval/deferral consequences:** Analysis supports a safe RF; deferral keeps Wave 1 implementation blocked.
- **Wave/authority impact:** Wave 1 and all protected workflows
- **Atlas change/language:** No vendor or protocol selection in Atlas. Supplemental language should remain provider-neutral.
- **Blocking/nonblocking:** Blocks identity implementation/migration/provider activation; nonblocking for Atlas adoption.
- **Founder disposition:** `PENDING`

## MEIA-FD06 - Communication strategy

- **Affected section/dependency:** Workstream F, Phase 4, Wave 5; Communication candidate; existing Resend-related code
- **Current state:** Delivery readiness and canonical adoption incomplete
- **Issue/importance:** Channel, consent, routing, sender, bounce, complaint, and evidence rules affect privacy and legal notice.
- **Options:** In-app only first; add email; add SMS/push later; split channels into separate RFs.
- **Recommendation/rationale:** `REQUEST_ADDITIONAL_ANALYSIS`: converge existing code and complete communication governance before provider decisions.
- **Approval/deferral consequences:** Analysis prevents duplicate/misdirected delivery; deferral blocks external transmission only.
- **Wave/authority impact:** Wave 5 and notification portions of Waves 3-8
- **Atlas change/language:** No current change; future selected scope must distinguish in-app state from external delivery.
- **Blocking/nonblocking:** Blocks email/SMS/push/notice activation; nonblocking for Atlas adoption and internal planning.
- **Founder disposition:** `PENDING`

## MEIA-FD07 - Agreement and DocuSign posture

- **Affected section/dependency:** Workstream G, Wave 5; Agreement, Identity, Relationship, Audit, Stewardship; existing DocuSign foundations
- **Current state:** Candidate governance and adapter foundations exist; production readiness unverified
- **Issue/importance:** Signer identity, capacity, exact text, envelope evidence, retention, and legal effect need one canonical lifecycle.
- **Options:** In-app agreement foundation first; DocuSign sandbox convergence; production DocuSign later; alternate provider.
- **Recommendation/rationale:** `APPROVE_WITH_MODIFICATION`: authorize future planning around canonical in-app agreement truth and sandbox-only adapter convergence, subject to a separate RF.
- **Approval/deferral consequences:** Approval sets direction without activation; deferral blocks agreement implementation and signatures.
- **Wave/authority impact:** Wave 5
- **Atlas change/language:** Supplemental: “External signature providers project execution evidence but do not create canonical authority or agreement truth.”
- **Blocking/nonblocking:** Blocks agreement/signature implementation and DocuSign production; nonblocking for Atlas adoption.
- **Founder disposition:** `PENDING`

## MEIA-FD08 - Financial Truth V2.1 and payment scope

- **Affected section/dependency:** Workstream H, Wave 6; Financial Truth; RF32; existing Stripe subscription billing
- **Current state:** V2.1 required; payment-rail scope unresolved
- **Issue/importance:** Subscription billing, barn invoices, customer payments, refunds, disputes, Connect, accounting, and settlement are distinct truth domains.
- **Options:** SaaS subscriptions only; add barn payment workflow; add Connect later; accounting export only; defer.
- **Recommendation/rationale:** `APPROVE_WITH_MODIFICATION`: complete Financial Truth V2.1 first and separately scope existing SaaS subscriptions from future barn/payment rails.
- **Approval/deferral consequences:** Approval enables governance completion; deferral blocks Wave 6 and RF35 but not Atlas adoption.
- **Wave/authority impact:** Wave 6; guardian/owner/admin financial surfaces
- **Atlas change/language:** Retain split Stripe classifications; future language must name authorized rail and source of truth.
- **Blocking/nonblocking:** Blocks financial implementation, migration, adapters, and production payments; nonblocking for Atlas adoption.
- **Founder disposition:** `PENDING`

## MEIA-FD09 - Calendar adapter direction

- **Affected section/dependency:** Phase 6/Wave 3; locked RF29; proposed RF36
- **Current state:** Canonical Calendar baseline locked and default-off; adapters/providers/persistence unauthorized
- **Issue/importance:** Directionality, ownership, recurrence, conflict, OAuth, revocation, and external deletion must preserve canonical truth.
- **Options:** ICS export only; one-way projections; controlled bidirectional sync; defer providers.
- **Recommendation/rationale:** `DEFER_WITH_BLOCK` until proposed RF36 kickoff; retain one-way/manual export as the lowest-risk evaluated baseline.
- **Approval/deferral consequences:** Deferral prevents premature synchronization while internal planning may continue.
- **Wave/authority impact:** Calendar adapter portion of Waves 3/6
- **Atlas change/language:** No change now; future decision must state directionality and provider-specific boundaries.
- **Blocking/nonblocking:** Blocks OAuth/provider sync and external writes; nonblocking for Atlas adoption and canonical internal planning.
- **Founder disposition:** `PENDING`

## MEIA-FD10 - Mobile/offline strategy

- **Affected section/dependency:** Phase/Wave 7; RF15/RF16 evidence; Platform Operations, Stewardship, Permission, Communication
- **Current state:** Strategy unresolved; no publication authority
- **Issue/importance:** Packaging, local storage, queued writes, conflict handling, device security, push, and app-store release have different risks.
- **Options:** PWA first; Capacitor; native apps; staged hybrid; defer publication.
- **Recommendation/rationale:** `APPROVE_WITH_MODIFICATION`: plan PWA/mobile-web reliability and offline architecture first; defer packaging and app-store decisions until evidence exists.
- **Approval/deferral consequences:** Approval focuses field reliability; deferral blocks packaging/publication, not responsive web work under future authority.
- **Wave/authority impact:** Wave 7
- **Atlas change/language:** Supplemental language should separate responsive/PWA reliability, offline writes, native packaging, push, and publication gates.
- **Blocking/nonblocking:** Blocks offline mutation architecture, native packaging, push activation, and publication; nonblocking for Atlas adoption.
- **Founder disposition:** `PENDING`

## MEIA-FD11 - ATLAS5 and RF33-RF36 sequence

- **Affected section/dependency:** Wave 10/external readiness; ATLAS5 intake; RF31/RF32 assignments
- **Current state:** ATLAS5 ready for founder review only; RF33-RF36 proposed/unopened
- **Issue/importance:** Preserve RF numbering and ensure external-service work follows Horse Transfer and Barn Payment governance.
- **Options:** Approve proposed sequence; revise/split RF34; defer ATLAS5; request dependency review.
- **Recommendation/rationale:** `APPROVE_WITH_MODIFICATION`: accept post-RF32 placement, then decide whether identity and communications remain combined before opening any RF.
- **Approval/deferral consequences:** Approval stabilizes roadmap numbering only; deferral leaves external-service progression unopened.
- **Wave/authority impact:** Future Waves 5, 6, and 10 external integrations
- **Atlas change/language:** Retain RF31/RF32 and proposed RF33-RF36 language; no kickoff state.
- **Blocking/nonblocking:** Blocks ATLAS5 advancement and RF33-RF36 opening; nonblocking for Atlas adoption.
- **Founder disposition:** `PENDING`

## MEIA-FD12 - First AI use case

- **Affected section/dependency:** Phase 9/Wave 10; RF30; AI Operating System; Permission, Stewardship, Audit, External Architecture
- **Current state:** RF30 locked deterministic-fake-only/default-off; real AI unauthorized
- **Issue/importance:** Any real use requires data classification, provider, evaluation, uncertainty, human review, cost, outage, and rollback governance.
- **Options:** Continue no real AI; authorize research package; select a low-risk advisory use case later; request broader analysis.
- **Recommendation/rationale:** `DEFER_WITHOUT_BLOCK`: retain no-real-AI posture until core deterministic workflows and governance dependencies mature.
- **Approval/deferral consequences:** Deferral preserves safety and does not affect non-AI waves.
- **Wave/authority impact:** Wave 10 AI only
- **Atlas change/language:** None; RF30 boundaries already explicit.
- **Blocking/nonblocking:** Blocks real model/provider/tool/action behavior; nonblocking for Atlas adoption and non-AI work.
- **Founder disposition:** `PENDING`

## MEIA-FD13 - Marketplace and enterprise timing

- **Affected section/dependency:** Phase/Wave 10; Product Vision, Ecosystem, Relationship, Financial, External Architecture, Platform Operations
- **Current state:** Deferred; no marketplace canon or implementation authority
- **Issue/importance:** Marketplace and enterprise scope can destabilize tenant, financial, legal, provider, API, and support foundations.
- **Options:** Defer; planning research only; provider directory without transactions; later governed marketplace; enterprise readiness first.
- **Recommendation/rationale:** `DEFER_WITHOUT_BLOCK` until core barn operations, financial governance, tenant isolation, and external-service readiness are proven.
- **Approval/deferral consequences:** Deferral protects core delivery and does not block earlier waves.
- **Wave/authority impact:** Wave 10 marketplace/enterprise only
- **Atlas change/language:** None; retain separate readiness and authority requirement.
- **Blocking/nonblocking:** Blocks marketplace/API/enterprise implementation; nonblocking for Atlas adoption and Waves 0-9.
- **Founder disposition:** `PENDING`
