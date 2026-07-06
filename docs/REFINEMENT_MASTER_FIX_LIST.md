# EquineSync Refinement Master Fix List

Date: 2026-07-06

Status: RF0, RF1, RF2, and RF3 CODEX-REVIEWED & LOCKED. RF4 is next.

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
| RF0-F06 | Feature-module shells still appear as production-like modules. | open P1 | RF4, RF17 | Routes and pages exist for `MobileReadiness`, `AdvancedReports`, `GroupMessaging`, `AI Automation`, `Forms & Signatures`, `Staff Tasks`, `Supply Inventory`, and others. Some are readiness/manifest surfaces. | Create feature registry; hide, relabel, or move readiness surfaces out of daily nav. |
| RF0-F07 | Staff scheduling, tasks, handoffs, and time clock are name-based. | partially fixed | RF2, RF8 | RF2 packages stable user-ID predicates for staff My Work, task status, handoffs, time-clock ownership, and payroll `staff_user_id` filtering in `backend/routes/backlog.py`. Frontend staff forms and legacy rows still use/display name fields. | RF8 must migrate/backfill workforce records to `staff_user_id` / `account_membership_id` and replace name text fields with staff selectors. |
| RF0-F08 | Staff Tasks and Task Engine are parallel task systems. | open P1 | RF6, RF8 | `backend/task_engine.py` is canonical for operational tasks, while `staff_task_assignments` and `/staff-tasks` exist in backlog surfaces. | Merge/demote Staff Tasks into Task Engine views or hide as readiness/admin-only. |
| RF0-F09 | Inventory and Supply Inventory are duplicated. | open P1 | RF6 | `/inventory` and `/supply-inventory` are both routed; `frontend/src/pages/Inventory.jsx` and `frontend/src/pages/SupplyInventory.jsx` are separate surfaces. | Choose canonical inventory and migrate/fold supply inventory. |
| RF0-F10 | Group Messaging tracks intent/status but does not necessarily deliver messages. | open P1 | RF13, RF17 | `frontend/src/pages/GroupMessaging.jsx` produces push preview/manifests and reads integration placeholders. | Build real delivery logs/recipient IDs or relabel/hide as readiness. |
| RF0-F11 | Advanced Reports imply Excel/PDF while export behavior may be manifest-based. | open P1 | RF12, RF17 | `backend/routes/backlog.py` report export returns manifest/download formats, while UI/routes expose advanced reporting. | Either generate real Excel/PDF or label manifest truthfully. |
| RF0-F12 | Owner payment flow can be configuration-ready rather than true payment collection. | partially fixed | RF1, RF12 | RF1 scopes owner payment prep by barn and stable account/invoice identity without horse-only authorization. Stripe collection truth remains RF12. | RF12 should make payment collection, refunds, voids, and Stripe state truthful. |
| RF0-F13 | QR/stall-card flow may not be a true QR encoder. | open P2 | RF11, RF17 | Mobile readiness/stall-card flows exist in `frontend/src/pages/MobileReadiness.jsx` and backlog QR hooks. | Build true QR generation or label as stall-card/readiness manifest. |
| RF0-F14 | Barn-location and arena-share defaults should use explicit publish state rather than role-inferred enabled state. | open P1 | RF1, RF11 | Arena/location surfaces include visibility fields and owner-access route groups; RF0 found no canonical publish-state model. | Add explicit publish/share state and backend enforcement. |
| RF0-F15 | Trainer fluidity is not fully built. | open P1 | RF9 | Trainer intake exists and explicitly does not create lessons, rider enrollments, horse assignments, permissions, or billing. Trainer dashboard delegates to generic dashboard. | Build trainer operating center after RF1/RF2 foundations. |
| RF0-F16 | Service provider multi-barn/client access is not fully built. | open P1 | RF10 | Service provider dashboard is a shell; `veterinarian` and `farrier` are legacy care-partner roles; no full provider access-grant model found. | Build provider profile/business/access-grant/appointment model after RF1/RF2 foundations. |
| RF0-F17 | Onboarding remains a major pain-point risk and should become guided import/setup. | partially fixed | RF3, RF5 | RF3 packages review-first CSV metadata and commit gating for horse/owner imports, explicit deferred import kinds, setup readiness truth, and integration readiness boundaries. First-value milestone analytics and richer import mapping remain RF5/RF18 follow-up work. | Review RF3, then decide whether richer row-level mapping UI is needed before first-client UAT. |
| RF0-F18 | Admin portal should become a product intelligence and customer-success center. | partially fixed | RF5 | Admin Portal has platform-role separation, users, facilities, billing, support, alerts, reports, integrations, settings, audit logs. RF5 User 360/Facility 360/account health/dunning/feature health/data quality are incomplete. | Extend admin portal into RF5 intelligence/customer-success surfaces with privacy-scrubbed analytics. |

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

Proceed to RF4 - Feature Completion Certification and Placeholder Elimination.

RF4 should be kept narrow:

1. Inventory every visible feature/module/nav item and classify it as hidden, scaffold, readiness, pilot beta, live, or deprecated.
2. Verify daily-user navigation does not present fake-live feature shells.
3. Move readiness/provider/setup surfaces to truthful admin/setup language where source already supports it.
4. No broad UX redesign, provider calls, schema rewrites, or completion of later RF domain models.
5. Evidence, tests, report, and package before lock.

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
