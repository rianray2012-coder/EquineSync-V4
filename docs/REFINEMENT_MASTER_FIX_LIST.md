# EquineSync Refinement Master Fix List

Date: 2026-07-06

Status: RF0, RF1, RF2, RF3, RF4, and RF5 CODEX-REVIEWED & LOCKED. RF6 is next.

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
| RF0-F01 | Owner Portal and owner-facing surfaces need a true owner-safe horse endpoint. | partially fixed | RF1, RF7 | RF1 added owner-safe horse ledger endpoints and moved backlog owner-portal access predicates to stable owner/user/horse clauses. RF7 still owns portal UX hardening and canonical surface cleanup. | RF7 should finish owner/guardian/rider portal response contracts and retire duplicated feature-module owner-update surfaces. |
| RF0-F02 | Some backend writes still need explicit capability gates, not only barn stamping or frontend nav. | partially fixed | RF1, RF4 | RF1 proof tests assert backend financial/reporting capability gates backed by `backend/core/permissions.py`. Full feature certification remains RF4. | RF4 should finish route-by-route feature certification and hide or gate non-certified surfaces. |
| RF0-F03 | QuickBooks invoice export must be barn-scoped. | fixed | RF1, RF12 | RF1 scopes QuickBooks invoice export by `barn_id` in `backend/routes/backlog.py`. | RF12 should finish broader export/accounting truth beyond the RF1 leak fix. |
| RF0-F04 | Owner portal billing and related surfaces still rely on display/free-text fields. | partially fixed | RF1, RF2, RF7, RF12 | RF1 moved owner-portal access predicates to stable owner/user/horse clauses. RF2 records that remaining display/form fields are not authorization predicates for its narrow scope. | RF7/RF12 should finish canonical portal UX and payment truth; RF17 should retire misleading feature-shell form fields. |
| RF0-F05 | Owner updates exist in two worlds: real lifecycle backend and feature-module media tracker. | partially fixed | RF6, RF7, RF17 | Real lifecycle exists in `backend/routes/owner_updates.py`; feature-module media update routes still exist in `backend/routes/backlog.py`. | Make `owner_updates` canonical; migrate/hide feature-module owner media updates. |
| RF0-F06 | Feature-module shells still appear as production-like modules. | partially fixed | RF4, RF17 | RF4 classifies all 32 feature-module keys and pins direct-route classifications for `MobileReadiness`, `AdvancedReports`, `GroupMessaging`, `AI Automation`, `Forms & Signatures`, `Staff Tasks`, `Supply Inventory`, and integration readiness surfaces. Daily role navigation is curated, but direct readiness/scaffold routes still need RF17 founder decisions. | Use the locked RF4 classifications to hide, relabel, redirect, or move readiness/scaffold surfaces out of daily nav in RF17. |
| RF0-F07 | Staff scheduling, tasks, handoffs, and time clock are name-based. | partially fixed | RF2, RF8 | RF2 packages stable user-ID predicates for staff My Work, task status, handoffs, time-clock ownership, and payroll `staff_user_id` filtering in `backend/routes/backlog.py`. Frontend staff forms and legacy rows still use/display name fields. | RF8 must migrate/backfill workforce records to `staff_user_id` / `account_membership_id` and replace name text fields with staff selectors. |
| RF0-F08 | Staff Tasks and Task Engine are parallel task systems. | open P1 | RF6, RF8 | `backend/task_engine.py` is canonical for operational tasks, while `staff_task_assignments` and `/staff-tasks` exist in backlog surfaces. | Merge/demote Staff Tasks into Task Engine views or hide as readiness/admin-only. |
| RF0-F09 | Inventory and Supply Inventory are duplicated. | open P1 | RF6 | `/inventory` and `/supply-inventory` are both routed; `frontend/src/pages/Inventory.jsx` and `frontend/src/pages/SupplyInventory.jsx` are separate surfaces. | Choose canonical inventory and migrate/fold supply inventory. |
| RF0-F10 | Group Messaging tracks intent/status but does not necessarily deliver messages. | partially fixed | RF13, RF17 | RF4 relabels Group Messaging as push-preview/local-status readiness and records `sent` as local status, not external delivery. | RF13 must build real delivery logs/recipient IDs or RF17 must hide/demote the surface. |
| RF0-F11 | Advanced Reports imply Excel/PDF while export behavior may be manifest-based. | partially fixed | RF12, RF17 | RF4 labels Excel/PDF actions as export manifests while `backend/routes/backlog.py` report export returns manifest/download formats. | RF12 must generate real Excel/PDF or RF17 must keep the manifest-only label/hide the surface. |
| RF0-F12 | Owner payment flow can be configuration-ready rather than true payment collection. | partially fixed | RF1, RF12 | RF1 scopes owner payment prep by barn and stable account/invoice identity without horse-only authorization. Stripe collection truth remains RF12. | RF12 should make payment collection, refunds, voids, and Stripe state truthful. |
| RF0-F13 | QR/stall-card flow may not be a true QR encoder. | partially fixed | RF11, RF17 | RF4 labels Mobile Readiness as limited field-recovery and stall-card identification; backend QR records remain deterministic text records with printable image generation deferred. | RF11/RF17 should build true QR generation or keep the stall-card/readiness label. |
| RF0-F14 | Barn-location and arena-share defaults should use explicit publish state rather than role-inferred enabled state. | open P1 | RF1, RF11 | Arena/location surfaces include visibility fields and owner-access route groups; RF0 found no canonical publish-state model. | Add explicit publish/share state and backend enforcement. |
| RF0-F15 | Trainer fluidity is not fully built. | open P1 | RF9 | Trainer intake exists and explicitly does not create lessons, rider enrollments, horse assignments, permissions, or billing. Trainer dashboard delegates to generic dashboard. | Build trainer operating center after RF1/RF2 foundations. |
| RF0-F16 | Service provider multi-barn/client access is not fully built. | open P1 | RF10 | Service provider dashboard is a shell; `veterinarian` and `farrier` are legacy care-partner roles; no full provider access-grant model found. | Build provider profile/business/access-grant/appointment model after RF1/RF2 foundations. |
| RF0-F17 | Onboarding remains a major pain-point risk and should become guided import/setup. | partially fixed | RF3, RF5 | RF3 packages review-first CSV metadata and commit gating for horse/owner imports, explicit deferred import kinds, setup readiness truth, and integration readiness boundaries. First-value milestone analytics and richer import mapping remain RF5/RF18 follow-up work. | Review RF3, then decide whether richer row-level mapping UI is needed before first-client UAT. |
| RF0-F18 | Admin portal should become a product intelligence and customer-success center. | partially fixed | RF5 | Admin Portal has platform-role separation, users, facilities, billing, support, alerts, reports, integrations, settings, audit logs. RF5 now inventories these account-health/customer-success surfaces. User 360/Facility 360/dunning/feature health/data quality are incomplete. | Extend admin portal into RF5 intelligence/customer-success surfaces with privacy-scrubbed analytics after founder acceptance of the opening gate. |
| RF0-F19 | General web-based enrollment and signup entry points are incomplete. | partially fixed | RF5, RF7, RF9, RF10, RF18 | RF5 adds `/enroll`, routes home/login Join actions to enrollment before credential collection, declares four public paths (individual horse owner, barn owner/manager, service provider, trainer), keeps rider/guardian/staff out of the main public path grid, and locks signup role/context to the selected path. Deeper enrollment workflows remain open. | RF7 should own individual horse/owner enrollment depth, limited-trial semantics, and leasee invites; RF9 trainer enrollment; RF10 service-provider enrollment; RF18 end-to-end UAT. |
| RF0-F20 | Rider, guardian, and staff public self-signup must not grant full product access. | partially fixed | RF5, RF7, RF18 | RF5 records those roles as invite-first and provides a limited seven-day individual-owner trial fallback when facility/trainer/provider contact information is supplied. Signup uses a separate limited-access branch instead of the standard paid-plan trial screen. Backend access caps and trial enforcement are not implemented in RF5. | RF7/RF18 must implement and test limited modified-individual-owner access that excludes barn owner, manager, trainer, and provider features. |
| RF0-F21 | Leasee access must preserve owner oversight and be invite-controlled. | open P1 | RF7 | RF5 records leasee access as invite-only from the horse owner or assigned trainer, with owner oversight preserved. No leasee grant model is implemented in RF5. | RF7 should implement leasee invites, scoped access, revocation, and owner oversight guarantees. |

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

Proceed to RF6 - Canonical Systems Consolidation.

RF6 should identify the canonical source of truth for duplicated operational
tasks, inventory, owner updates, documents/signatures, billing, and integration
readiness surfaces. It should produce explicit migrate, alias, read-only, hide,
or defer decisions without broad schema rewrites or provider mutations.

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
