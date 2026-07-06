# EquineSync Refinement Master Fix List

Date: 2026-07-06

Status: RF0, RF1, RF2, RF3, RF4, RF5, RF6, RF7, RF8, RF9, and RF10 CODEX-REVIEWED & LOCKED. RF11 is ready for planning.

## Classification Key

- `fixed`: Source evidence and tests show the issue is closed.
- `partially fixed`: A safe foundation exists, but the full RF finding is not closed.
- `open P0`: Trust, privacy, tenant isolation, billing/export leakage, or backend-authority risk.
- `open P1`: Important product truth, workflow completion, or customer-success risk.
- `open P2`: Important polish, consolidation, UX truth, or later-readiness work.
- `deferred`: Explicitly accepted as future work for the current pilot posture.
- `moot`: No longer applicable.
- `requires founder decision`: Needs explicit product/founder choice before implementation.

## Findings

| ID | Finding | Classification | RF Phase | Evidence / Current State | Required Fix Direction |
| --- | --- | --- | --- | --- | --- |
| RF0-F01 | Owner Portal and owner-facing surfaces need a true owner-safe horse endpoint. | fixed for RF7 portal inventory | RF1, RF7 | RF1 added owner-safe horse ledger endpoints and moved backlog owner-portal access predicates to stable owner/user/horse clauses. RF7 routes OwnerPortal owner/guardian horse inventory to `/owner-portal/horses` and normalizes the `{items}` response while staff preview users stay on `/horses`. | RF18 should browser-smoke seeded owner/guardian/staff-preview portal flows. RF17 still owns duplicated feature-module owner-media migration/hide. |
| RF0-F02 | Some backend writes still need explicit capability gates, not only barn stamping or frontend nav. | partially fixed | RF1, RF4 | RF1 proof tests assert backend financial/reporting capability gates backed by `backend/core/permissions.py`. Full feature certification remains RF4. | RF4 should finish route-by-route feature certification and hide or gate non-certified surfaces. |
| RF0-F03 | QuickBooks invoice export must be barn-scoped. | fixed | RF1, RF12 | RF1 scopes QuickBooks invoice export by `barn_id` in `backend/routes/backlog.py`. | RF12 should finish broader export/accounting truth beyond the RF1 leak fix. |
| RF0-F04 | Owner portal billing and related surfaces still rely on display/free-text fields. | partially fixed | RF1, RF2, RF7, RF12 | RF1 moved owner-portal access predicates to stable owner/user/horse clauses. RF2 records that remaining display/form fields are not authorization predicates for its narrow scope. | RF7/RF12 should finish canonical portal UX and payment truth; RF17 should retire misleading feature-shell form fields. |
| RF0-F05 | Owner updates exist in two worlds: real lifecycle backend and feature-module media tracker. | deferred after RF7 | RF6, RF7, RF17 | RF6 declares `backend/routes/owner_updates.py` / `db.owner_updates` canonical. RF7 preserves that canonical decision and records `owner_media_updates` as a migration/hide candidate without removing data or routes. | RF17 should migrate, hide, or redirect feature-module owner media updates. |
| RF0-F06 | Feature-module shells still appear as production-like modules. | partially fixed | RF4, RF17 | RF4 classifies all 32 feature-module keys and pins direct-route classifications for `MobileReadiness`, `AdvancedReports`, `GroupMessaging`, `AI Automation`, `Forms & Signatures`, `Staff Tasks`, `Supply Inventory`, and integration readiness surfaces. Daily role navigation is curated, but direct readiness/scaffold routes still need RF17 founder decisions. | Use the locked RF4 classifications to hide, relabel, redirect, or move readiness/scaffold surfaces out of daily nav in RF17. |
| RF0-F07 | Staff scheduling, tasks, handoffs, and time clock are name-based. | partially fixed for RF8 new rows | RF2, RF8 | RF2 packages stable user-ID predicates for staff My Work, task status, handoffs, time-clock ownership, and payroll `staff_user_id` filtering. RF8 adds a same-barn staff directory, requires stable staff IDs on new covered staff-module creates, normalizes submitted staff IDs server-side, and updates staff module create flows to submit `staff_user_id`, `assigned_user_id`, `incoming_staff_user_id`, and `outgoing_staff_user_id`. Legacy name-only rows remain. | RF18/backfill should migrate historical rows after founder approves the strategy. |
| RF0-F08 | Staff Tasks and Task Engine are parallel task systems. | deferred after RF8 | RF6, RF8, RF17 | RF6 declares Task Engine canonical for operational tasks. RF8 prevents new Staff Tasks ID drift but does not migrate or hide `staff_task_assignments`. | RF17 or a founder-approved RF8 follow-up should migrate, hide, or relabel Staff Tasks. |
| RF0-F09 | Inventory and Supply Inventory are duplicated. | partially fixed | RF6, RF17 | RF6 declares `/inventory` / `db.inventory` canonical. `/supply-inventory` and `supply_inventory_items` remain noncanonical until alias/migration/hide work. | RF17 should alias, migrate, or hide Supply Inventory. |
| RF0-F10 | Group Messaging tracks intent/status but does not necessarily deliver messages. | partially fixed | RF13, RF17 | RF4 relabels Group Messaging as push-preview/local-status readiness and records `sent` as local status, not external delivery. | RF13 must build real delivery logs/recipient IDs or RF17 must hide/demote the surface. |
| RF0-F11 | Advanced Reports imply Excel/PDF while export behavior may be manifest-based. | partially fixed | RF12, RF17 | RF4 labels Excel/PDF actions as export manifests while `backend/routes/backlog.py` report export returns manifest/download formats. | RF12 must generate real Excel/PDF or RF17 must keep the manifest-only label/hide the surface. |
| RF0-F12 | Owner payment flow can be configuration-ready rather than true payment collection. | partially fixed | RF1, RF12 | RF1 scopes owner payment prep by barn and stable account/invoice identity without horse-only authorization. Stripe collection truth remains RF12. | RF12 should make payment collection, refunds, voids, and Stripe state truthful. |
| RF0-F13 | QR/stall-card flow may not be a true QR encoder. | partially fixed | RF11, RF17 | RF4 labels Mobile Readiness as limited field-recovery and stall-card identification; backend QR records remain deterministic text records with printable image generation deferred. | RF11/RF17 should build true QR generation or keep the stall-card/readiness label. |
| RF0-F14 | Barn-location and arena-share defaults should use explicit publish state rather than role-inferred enabled state. | open P1 | RF1, RF11 | Arena/location surfaces include visibility fields and owner-access route groups; RF0 found no canonical publish-state model. | Add explicit publish/share state and backend enforcement. |
| RF0-F15 | Trainer fluidity is not fully built. | partially fixed for RF9 operating center | RF9 | RF9 adds an ID-scoped trainer operating-center read model, stable trainer-owned lesson/training semantics, stable-ID Training Plan creates, and a trainer-specific dashboard. Trainer package billing, haul-ins, school horses, and broad multi-facility grants remain deferred. | RF18 should UAT seeded trainer scenarios; RF12 owns package/billing truth; broader multi-facility grants need future account/grant policy. |
| RF0-F16 | Service provider multi-barn/client access is not fully built. | partially fixed for RF10 grant model | RF10 | RF10 adds active explicit horse-provider grants with same-barn stable `provider_user_id` assignment validation, provider-safe direct horse/care reads, provider-authored visit notes, safe grant projections, and a real service-provider dashboard. Canonical care writes, account-level cross-facility provider identity, provider invoices/payments, legal documents, messaging delivery, and external provider integrations remain deferred. | RF18 should UAT seeded provider grant, revocation, and denial scenarios; RF12/RF13/RF14 own payment, messaging, and document truth; future account-membership policy should prove stable cross-facility provider identity. |
| RF0-F17 | Onboarding remains a major pain-point risk and should become guided import/setup. | partially fixed | RF3, RF5 | RF3 packages review-first CSV metadata and commit gating for horse/owner imports, explicit deferred import kinds, setup readiness truth, and integration readiness boundaries. First-value milestone analytics and richer import mapping remain RF5/RF18 follow-up work. | Review RF3, then decide whether richer row-level mapping UI is needed before first-client UAT. |
| RF0-F18 | Admin portal should become a product intelligence and customer-success center. | partially fixed | RF5 | Admin Portal has platform-role separation, users, facilities, billing, support, alerts, reports, integrations, settings, audit logs. RF5 now inventories these account-health/customer-success surfaces. User 360/Facility 360/dunning/feature health/data quality are incomplete. | Extend admin portal into RF5 intelligence/customer-success surfaces with privacy-scrubbed analytics after founder acceptance of the opening gate. |
| RF0-F19 | General web-based enrollment and signup entry points are incomplete. | partially fixed | RF5, RF7, RF9, RF10, RF18 | RF5 adds `/enroll`, routes home/login Join actions to enrollment before credential collection, declares four public paths, and keeps rider/guardian/staff out of the main public path grid. RF9 preserves trainer intake as review-gated setup intent. RF10 records service-provider signup review posture as a founder decision without auto-approving provider accounts. | RF18 end-to-end UAT remains open; founder should accept trainer/provider review posture before stronger public claims. |
| RF0-F20 | Rider, guardian, and staff public self-signup must not grant full product access. | deferred after RF7 | RF5, RF7, RF18 | RF5 records those roles as invite-first and provides a limited seven-day individual-owner trial fallback when facility/trainer/provider contact information is supplied. RF7 keeps the caveat explicit but does not implement full server-side access caps. | RF18 must implement and test limited modified-individual-owner access that excludes barn owner, manager, trainer, and provider features before stronger claims. |
| RF0-F21 | Leasee access must preserve owner oversight and be invite-controlled. | deferred after RF7 | RF7, RF18 | RF5 records leasee access as invite-only from the horse owner or assigned trainer, with owner oversight preserved. RF7 documents the decision row but does not implement grant/revocation data models. | Implement leasee invites, scoped access, revocation, and owner oversight guarantees only after founder accepts the policy and RF18 UAT scope. |

## Founder / Product Decisions

| Decision | Classification | RF Phase | Notes |
| --- | --- | --- | --- |
| RF ordering and whether RF happens before broad public launch, after first-client pilot, or parallel to pilot. | requires founder decision | RF0, RF18 | RF0 recommends RF1 next before broad implementation. |
| Soft-warning and nonpayment enforcement policy. | requires founder decision | RF5, RF12 | Must not block critical horse-care access without explicit acceptance. |
| Discount/credit approval thresholds. | requires founder decision | RF5 | Needed before billing intervention tooling. |
| First onboarding import types. | requires founder decision | RF3 | Recommended first: horses, owners, riders, staff, service providers, feed/medication lists. |
| Trainer workflow priority. | requires founder decision | RF9 | Lesson packages, horse training, haul-ins, school horses, and multi-facility context need ordering. |
| Service-provider type priority. | requires founder decision | RF10 | Base model can support all types, but first UAT type should be selected. |
| Native App Store / Google Play timing. | deferred / requires founder decision | RF16 | Current BN19-BN21 posture defers native store distribution. |
| Offline workflows required for launch claims. | deferred / requires founder decision | RF15 | Current BN18D/BN21 posture permits limited recovery only. |
| Feature shells to hide immediately. | requires founder decision | RF4, RF17 | RF0 recommends auditing daily nav first. |
| Privacy boundaries for platform-admin insights. | requires founder decision | RF5 | Admin analytics must avoid sensitive free text and private content. |
| Web enrollment path ordering and copy. | requires founder decision | RF5, RF7, RF9, RF10 | RF5 proposed this order: Individual Horse Owner, Barn Owner / Manager, Service Provider, Trainer. Founder should accept or adjust before lock. |
| Rider/guardian/staff limited trial posture. | requires founder decision | RF5, RF7, RF18 | Accept invite-first access plus limited modified-individual-owner trial fallback, with server enforcement deferred beyond RF5. |
| Leasee invite authority. | requires founder decision | RF7 | Accept that leasee invites can only be sent by the horse owner or assigned trainer, while owner oversight remains intact. |
| Task Engine canonical ownership. | requires founder decision | RF6, RF8 | Accept Task Engine as canonical over Staff Tasks before RF8 migration/hide work. |
| Inventory canonical ownership. | requires founder decision | RF6, RF17 | Accept `/inventory` / `db.inventory` as canonical over Supply Inventory before alias/migration/hide work. |
| Owner Updates canonical ownership. | requires founder decision | RF6, RF7, RF17 | Accept `owner_updates` as canonical over feature-module owner media updates. |
| Document signature canonical ownership. | requires founder decision | RF6, RF14 | Accept Document Signatures as canonical legal-signature workflow truth while Digital Forms remains local acknowledgement/readiness. |
| Billing entitlement canonical ownership. | requires founder decision | RF6, RF12 | Accept account subscription rows as subscription entitlement truth, distinct from invoices/payment records/legacy membership. |
| Integration readiness canonical boundary. | requires founder decision | RF6, RF10, RF12, RF13, RF14, RF16, RF17 | Accept integration readiness as manifest/status evidence only until provider-specific phases prove live sync. |

## RF1 Locked Status

RF1 has been reviewed, fixed, reviewed again, and locked. The following RF0
findings are closed for RF1 scope:

| Finding | RF1 Status | Evidence |
| --- | --- | --- |
| RF0-F01 | fixed for RF1 | `GET /owner/horses` and `GET /owner-portal/horses` now exist with stable owner/guardian/rider predicates. |
| RF0-F02 | fixed for RF1 | RF1 proof tests assert backend financial/reporting capability gates. |
| RF0-F03 | fixed for RF1 | QuickBooks invoice export reads invoices by `barn_id`. |
| RF0-F04 | fixed for RF1 | Owner portal media/forms/health/emergency/training/billing predicates use stable owner/user/horse clauses. |
| RF0-F12 | fixed for RF1 | Owner billing and payment-prep invoice lookups are barn-scoped and account-identity-scoped, without horse-only authorization. |
| RF0-F14 | deferred | Canonical property/location/share publish state remains RF11. |

Founder review item: RF1 intentionally hides legacy owner-facing records that
only match by display/free-text name until RF2/RF7 migration links them to
stable IDs.

## Current Phase Recommendation

Proceed with RF11 - Property, Location, Map, and Community Help System.

RF6 identifies the canonical source of truth for duplicated operational tasks,
inventory, owner updates, documents/signatures, billing, and integration
readiness surfaces. It produces explicit migrate, alias, read-only, hide, or
defer decisions without broad schema rewrites or provider mutations.

## RF3 Locked Status

RF3 has been reviewed, fixed, re-reviewed, and locked. The following RF0 finding
is closed for RF3 review-first import and setup-readiness scope:

| Finding | RF3 Status | Evidence |
| --- | --- | --- |
| RF0-F17 | fixed for RF3 review-first horse/owner import and setup-readiness scope; still open for RF5/RF18 analytics and UAT depth | CSV preview returns row-review metadata, CSV commit requires `reviewed: true`, deferred import kinds are explicit, setup readiness remains backend-authoritative, and integration setup remains manifest-only. |

RF3 accepted/deferred founder decisions:

- Active import scope of horses and owners only is accepted for RF3.
- Richer row-level mapping UI is deferred to RF18 or a later founder-approved follow-up.
- Integration setup readiness remains manifest-only until provider phases.

## Lock Note

RF0 is Codex-reviewed and locked. The finding classifications remain evidence
intake only. RF1 is Codex-reviewed and locked for P0 data fences and backend
capability gates.

## RF2 Locked Status

RF2 has been reviewed, fixed, re-reviewed, and locked. The following RF0 finding
is closed for RF2 backend self-service scope:

| Finding | RF2 Status | Evidence |
| --- | --- | --- |
| RF0-F07 | fixed for RF2 backend self-service scope; still open for RF8 model completion | Staff My Work, staff task status, handoffs, and time-clock ownership now use stable user-ID predicates. Payroll export accepts `staff_user_id`. |

RF2 accepted/deferred founder decisions:

- Strict staff self-service matching for stable user-ID records only is accepted.
- Admin payroll `staff_name` filter retirement is deferred to RF8/RF12.
- Provider grants, message recipients, and full workforce backfill remain deferred
  to RF8/RF10/RF13.

## RF4 Locked Status

RF4 is Codex-reviewed and locked. The generated report is
`outputs/rf4_feature_completion_certification_report.md`.

RF4 closes the evidence/copy-certification portion of RF0-F06/F10/F11/F13, but
does not close the later implementation and UX-hiding work:

| Finding | RF4 Status | Evidence |
| --- | --- | --- |
| RF0-F06 | partially fixed for feature classification and truth labeling; still open for RF17 hide/move decisions | All 32 backend feature-module keys are classified; daily role navigation avoids the old generic feature shell menu; eight direct routes are explicitly classified. |
| RF0-F10 | partially fixed for current truth labeling | Group Messaging says push-preview/local-status, not external delivery; backend push manifests remain `preview_only`. |
| RF0-F11 | partially fixed for current truth labeling | Advanced Reports labels Excel/PDF outputs as manifests. |
| RF0-F13 | partially fixed for current truth labeling | Mobile Readiness says limited field-recovery and stall-card identification; true QR/native/offline work remains later. |
| RF4-REV-01 | fixed | Admin Portal permissions and owner role-intake fallback panels no longer render phase, placeholder-only, or shell-shipping copy. |

RF4 founder decisions:

- Accept RF4 classifications as current feature truth for review.
- Decide which readiness/scaffold pages stay visible before RF17.
- Accept manifest-only exports and push-preview wording until RF12/RF13
  implementation, or require hiding/demotion sooner.

## RF4 Pre-Lock Founder Enrollment Note

Founder requested that EquineSync add a general web-based enrollment workflow
before RF4 lock. This is now tracked as RF0-F19, mapped to RF5/RF7/RF9/RF10,
and should be included in RF5 planning:

- Add home-page signup and sign-in-page join/signup entry points for users who
  do not yet have accounts.
- Route users to a signup path selector before collecting credentials and
  critical signup data.
- Include an individual horse enrollment path for owners whose barns are not
  using EquineSync, owners keeping horses on their own land, and family/informal
  care contexts.
- Include distinct enrollment paths for barn/facility owners, trainers, service
  providers, and other relevant account types.
- Re-test all enrollment paths in RF18 before broader launch.

## RF5 Locked Status

RF5 is Codex-reviewed and locked with RF0-F19 included in the first RF5 pass.
RF5 adds home/login signup entry points, enrollment path selection, critical
signup data inventory, and admin/customer-success evidence. It does not
complete RF7, RF9, RF10, RF12, or RF18 inside this opening RF5 gate.

RF5 generated report:
`outputs/rf5_web_enrollment_account_health_report.md`.

RF5 package:
`outputs/build_next_rf5_web_enrollment_account_health.zip`.

| Finding | RF5 Status | Evidence |
| --- | --- | --- |
| RF0-F18 | partially fixed for inventory evidence | Admin Portal account-health/customer-success route inventory is captured; deeper privacy-scrubbed analytics and intervention workflows remain future RF5 work. |
| RF0-F19 | partially fixed for public enrollment entry path | `/enroll` is public; home/login Join actions route there; signup requires selected enrollment context; the main public grid is limited to individual horse owner, barn owner/manager, service provider, and trainer. |
| RF0-F20 | partially fixed for RF5 posture | Rider/guardian/staff access is invite-first in public copy, with a limited-trial fallback recorded but not enforced server-side. |
| RF0-F21 | recorded for RF7 | Leasee access is documented as owner/assigned-trainer invite-only with owner oversight preserved. |
| RF5-REV-01 | fixed | Rider, guardian, and staff are not exposed as main public enrollment paths; the signup role is locked to the selected enrollment path. |
| RF5-REV-02 | fixed | The limited-trial signup branch is separate from the standard paid-plan trial screen and does not present normal paid-plan trial copy. |

RF5 founder decisions:

- Accept the first public enrollment path order and labels.
- Decide which critical signup fields become required by path.
- Decide whether trainer and service-provider self-signup remains review-gated.
- Accept rider/guardian/staff invite-first access plus limited-trial fallback.
- Accept leasee invite authority and owner oversight requirements.
- Accept admin account-health inventory as opening evidence only.

## RF6 Locked Status

RF6 is Codex-reviewed and locked. It records canonical source-of-truth
decisions without data migration, route hiding, redirects, schemas, auth
changes, billing mutations, provider calls, or founder acceptance auto-marking.

RF6 generated report:
`outputs/rf6_canonical_systems_consolidation_report.md`.

RF6 package:
`outputs/build_next_rf6_canonical_systems_consolidation.zip`.

| Finding / Domain | RF6 Status | Evidence |
| --- | --- | --- |
| RF0-F05 | partially fixed for canonical decision | `owner_updates` is canonical; `owner_media_updates` remains migration/hide work. |
| RF0-F08 | partially fixed for canonical decision | Task Engine is canonical; Staff Tasks remains migration/hide work for RF8/RF17. |
| RF0-F09 | partially fixed for canonical decision | `/inventory` / `db.inventory` is canonical; Supply Inventory remains alias/migration/hide work. |
| Documents/signatures | canonical decision recorded | Document Signatures owns legal signature workflows; Digital Forms remains local acknowledgement/readiness until RF14. |
| Billing entitlements | canonical decision recorded | `account_subscriptions` / `account_usage_limits` are entitlement truth; legacy membership/payment feature records are not subscription truth. |
| Integration readiness | canonical readiness boundary recorded | `integration_connections` and prepare/export/preview manifests are readiness evidence only until provider phases. |

RF6 founder decisions:

- Accept Task Engine as canonical over Staff Tasks.
- Accept Inventory as canonical over Supply Inventory.
- Accept Owner Updates as canonical over owner media updates.
- Accept Document Signatures as canonical for legal signature workflows.
- Accept account subscription records as billing entitlement truth.
- Accept integration readiness as manifest/status evidence only until provider
  phases.

## RF7 Locked Status

RF7 is Codex-reviewed and locked. It hardens the owner/guardian/client portal
trust surface without broad feature expansion.

RF7 generated report:
`outputs/rf7_owner_client_portal_hardening_report.md`.

RF7 package:
`outputs/build_next_rf7_owner_client_portal_hardening.zip`.

| Finding / Domain | RF7 Status | Evidence |
| --- | --- | --- |
| RF0-F01 | fixed for RF7 portal inventory | Owner/guardian horse inventory uses `/owner-portal/horses`; staff preview remains on `/horses`. |
| Owner/guardian service requests | fixed for RF7 portal request path | Owner and guardian submissions use `/horse-ledger/{horse_id}/owner-service-requests`; guardian-linked parent users can submit/read only their own owner-care requests for guardian-linked horses. |
| RF0-F05 | deferred after RF7 | `owner_updates` remains canonical; feature-module `owner_media_updates` is still RF17 migration/hide work. |
| RF0-F20 | deferred after RF7 | Limited modified-individual-owner trial access caps remain RF18/UAT work. |
| RF0-F21 | deferred after RF7 | Leasee grant/revocation model remains founder-decision/RF18 work. |

RF7 lock verification:

- Focused RF7 tests passed.
- RF7 report generation passed with blocker failure enabled.
- Frontend build passed.
- Zip integrity and expected manifest checks passed.
- `git diff --check` and RF7 secret-shape scan passed.

RF8 may proceed as the Staff Workforce Model gate.

## RF8 Locked Status

RF8 is Codex-reviewed and locked. It hardens new staff-workforce creates without
historical data backfill or Staff Tasks migration.

RF8 generated report:
`outputs/rf8_staff_workforce_model_report.md`.

RF8 package:
`outputs/build_next_rf8_staff_workforce_model.zip`.

| Finding / Domain | RF8 Status | Evidence |
| --- | --- | --- |
| RF0-F07 | partially fixed for RF8 new rows | New staff scheduling, Staff Tasks, handoff, and time-clock creates require stable staff user IDs. Backend normalization verifies same-barn staff ids and stamps display names. |
| RF0-F08 | deferred after RF8 | Task Engine remains canonical, but Staff Tasks migration/hide is not performed. |
| Payroll export | partially fixed | `staff_user_id` filter remains stable; legacy `staff_name` filter remains for admin compatibility. |

RF8 does not mutate legacy staff rows, perform a historical backfill, delete
Staff Tasks, migrate Staff Tasks into Task Engine, change billing truth, add
provider grants, or mark founder decisions accepted.

Next phase: RF9 Trainer Operating Center and Trainer Fluidity. See
`docs/RF9_TRAINER_OPERATING_CENTER_PLAN.md`.

## RF9 Locked Status

RF9 is Codex-reviewed and locked. It hardens trainer-owned work without implementing
trainer package billing, haul-ins, school-horse workflows, or broad
multi-facility grants.

RF9 generated report:
`outputs/rf9_trainer_operating_center_report.md`.

RF9 package:
`outputs/build_next_rf9_trainer_operating_center.zip`.

| Finding / Domain | RF9 Status | Evidence |
| --- | --- | --- |
| RF0-F15 | partially fixed for RF9 operating center | Trainer dashboard now uses `/trainer/operating-center`; trainer lessons/training reads are stable-ID scoped; trainer-created lessons/training stamp `trainer_id`; Training Plans require stable `horse_id` and `trainer_user_id` on new creates. |
| RF0-F19 | partially fixed for trainer enrollment posture | Trainer intake remains trainer-role scoped and setup-intent only; RF9 records review posture and required-field decisions for founder review. |
| Trainer packages/billing | deferred | RF12 owns billing/payment/package truth unless founder explicitly reorders. |
| Multi-facility trainer grants | deferred | Current RF9 work remains barn-scoped; account-membership/grant policy remains future work. |

RF9 does not mutate Stripe, implement paid trainer packages, add
service-provider grants, implement haul-ins, implement school-horse workflows,
add native/offline behavior, or mark founder decisions accepted.

Next phase: RF10 Service Provider / Care Partner Multi-Barn Model. See
`docs/RF10_SERVICE_PROVIDER_CARE_PARTNER_PLAN.md`.

## RF10 Locked Status

RF10 is Codex-reviewed and locked. It hardens service-provider access through
explicit grants without implementing provider billing, payouts, messaging
delivery, legal document workflows, live provider calls, native/offline
behavior, or founder acceptance.

RF10 generated report:
`outputs/rf10_service_provider_care_partner_report.md`.

RF10 package:
`outputs/build_next_rf10_service_provider_care_partner.zip`.

| Finding / Domain | RF10 Status | Evidence |
| --- | --- | --- |
| RF0-F16 | partially fixed for RF10 grant model | Provider access now resolves active `horse_provider_assignments` linked to same-barn stable `provider_user_id` or explicit provider catalog rows; provider direct horse/care reads are grant-scoped; provider visit notes require a granted horse; raw grant rows are safely projected; dashboard uses `/service-provider/operating-center`. |
| RF0-F19 | partially fixed for provider enrollment posture | RF10 records service-provider signup review posture and grant authority as founder decisions without auto-approving service-provider accounts. |
| Provider billing/payments/payouts | deferred | RF12 owns billing/payment/provider invoice truth. |
| Provider documents/signatures/storage | deferred | RF14 owns legal document/signature/storage truth. |
| Provider messaging delivery | deferred | RF13 owns recipient and delivery truth. |
| Provider canonical care writes | deferred | RF10 keeps provider-authored care entries limited to provider visit notes; canonical care-write authority needs founder-approved policy and tests. |
| Account-level cross-facility provider identity | deferred | RF10 does not prove one stable provider account across unrelated barns; future account-membership policy and RF18 UAT should prove it before stronger multi-barn claims. |

RF10 does not mutate Stripe, implement provider invoices or payouts, call live
providers, implement messaging delivery, implement legal document workflows, add
provider canonical care-write authority, prove account-level cross-facility
provider identity, add native/offline behavior, or mark founder decisions
accepted.

Next phase: RF11 Property, Location, Map, and Community Help System. See
`docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP_PLAN.md`.
