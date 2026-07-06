# EquineSync Refinement Master Fix List

Date: 2026-07-06

Status: RF0 CODEX-REVIEWED & LOCKED. Do not implement RF1-RF18 from this file without a dedicated phase.

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
| RF0-F01 | Owner Portal and owner-facing surfaces need a true owner-safe horse endpoint. | partially fixed | RF1, RF7 | Owner-safe horse ledger endpoints exist in `backend/routes/horse_ledger.py` using stable owner IDs and owner-safe projections. Backlog owner-portal modules still use name/free-text matching in `backend/routes/backlog.py`. | In RF1, verify or add canonical `GET /owner/horses` / `GET /owner-portal/horses`; move owner-portal modules to stable owner/guardian/rider relationships. |
| RF0-F02 | Some backend writes still need explicit capability gates, not only barn stamping or frontend nav. | open P0 | RF1 | `backend/core/permissions.py` has fail-closed capabilities, but many direct routes still rely on broad route groups or module-local checks. | Create an RF1 route/capability matrix and add backend tests for sensitive writes. |
| RF0-F03 | QuickBooks invoice export must be barn-scoped. | open P0 | RF1, RF12 | `backend/routes/backlog.py` scopes expenses by barn but reads invoices with `db.invoices.find({})` in QuickBooks export. | Scope invoice export by barn/account and add cross-barn export regression. |
| RF0-F04 | Owner portal billing and related surfaces still rely on display/free-text fields. | open P0 | RF1, RF2, RF7, RF12 | Backlog owner portal uses `full_name`, `owner_name`, `recipient_name`, and `shared_with` regex in `backend/routes/backlog.py`. | Replace with stable IDs and temporary compatibility fields only where documented. |
| RF0-F05 | Owner updates exist in two worlds: real lifecycle backend and feature-module media tracker. | partially fixed | RF6, RF7, RF17 | Real lifecycle exists in `backend/routes/owner_updates.py`; feature-module media update routes still exist in `backend/routes/backlog.py`. | Make `owner_updates` canonical; migrate/hide feature-module owner media updates. |
| RF0-F06 | Feature-module shells still appear as production-like modules. | open P1 | RF4, RF17 | Routes and pages exist for `MobileReadiness`, `AdvancedReports`, `GroupMessaging`, `AI Automation`, `Forms & Signatures`, `Staff Tasks`, `Supply Inventory`, and others. Some are readiness/manifest surfaces. | Create feature registry; hide, relabel, or move readiness surfaces out of daily nav. |
| RF0-F07 | Staff scheduling, tasks, handoffs, and time clock are name-based. | open P1 | RF2, RF8 | Staff portal and forms use `staff_name`, `assigned_to`, `incoming_staff`, `outgoing_staff`, and `full_name` matching in `backend/routes/backlog.py` and frontend staff pages. | Migrate workforce records to `staff_user_id` / `account_membership_id`. |
| RF0-F08 | Staff Tasks and Task Engine are parallel task systems. | open P1 | RF6, RF8 | `backend/task_engine.py` is canonical for operational tasks, while `staff_task_assignments` and `/staff-tasks` exist in backlog surfaces. | Merge/demote Staff Tasks into Task Engine views or hide as readiness/admin-only. |
| RF0-F09 | Inventory and Supply Inventory are duplicated. | open P1 | RF6 | `/inventory` and `/supply-inventory` are both routed; `frontend/src/pages/Inventory.jsx` and `frontend/src/pages/SupplyInventory.jsx` are separate surfaces. | Choose canonical inventory and migrate/fold supply inventory. |
| RF0-F10 | Group Messaging tracks intent/status but does not necessarily deliver messages. | open P1 | RF13, RF17 | `frontend/src/pages/GroupMessaging.jsx` produces push preview/manifests and reads integration placeholders. | Build real delivery logs/recipient IDs or relabel/hide as readiness. |
| RF0-F11 | Advanced Reports imply Excel/PDF while export behavior may be manifest-based. | open P1 | RF12, RF17 | `backend/routes/backlog.py` report export returns manifest/download formats, while UI/routes expose advanced reporting. | Either generate real Excel/PDF or label manifest truthfully. |
| RF0-F12 | Owner payment flow can be configuration-ready rather than true payment collection. | open P0 | RF1, RF12 | Owner-portal payment prep in `backend/routes/backlog.py` returns provider readiness posture and owner lookup still includes name matching. | Scope by stable owner/invoice IDs and make Stripe collection state truthful. |
| RF0-F13 | QR/stall-card flow may not be a true QR encoder. | open P2 | RF11, RF17 | Mobile readiness/stall-card flows exist in `frontend/src/pages/MobileReadiness.jsx` and backlog QR hooks. | Build true QR generation or label as stall-card/readiness manifest. |
| RF0-F14 | Barn-location and arena-share defaults should use explicit publish state rather than role-inferred enabled state. | open P1 | RF1, RF11 | Arena/location surfaces include visibility fields and owner-access route groups; RF0 found no canonical publish-state model. | Add explicit publish/share state and backend enforcement. |
| RF0-F15 | Trainer fluidity is not fully built. | open P1 | RF9 | Trainer intake exists and explicitly does not create lessons, rider enrollments, horse assignments, permissions, or billing. Trainer dashboard delegates to generic dashboard. | Build trainer operating center after RF1/RF2 foundations. |
| RF0-F16 | Service provider multi-barn/client access is not fully built. | open P1 | RF10 | Service provider dashboard is a shell; `veterinarian` and `farrier` are legacy care-partner roles; no full provider access-grant model found. | Build provider profile/business/access-grant/appointment model after RF1/RF2 foundations. |
| RF0-F17 | Onboarding remains a major pain-point risk and should become guided import/setup. | open P1 | RF3, RF5 | Onboarding/readiness and setup surfaces exist, but RF3 import concierge, AI-assisted review-first mapping, and first-value milestone analytics are not built. | Build Onboarding 2.0 as review-first guided setup and import concierge. |
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

## Recommended Next Phase

Proceed to RF1 - P0 Data Fences and Backend Capability Gates.

RF1 should be kept narrow:

1. Owner-safe horse endpoint and owner-portal data fence proof.
2. QuickBooks invoice export barn/account scoping.
3. Owner billing/payment scoping proof.
4. Backend capability-gate matrix for sensitive writes.
5. Direct route regression tests for owner/staff/provider/trainer access boundaries.

## Lock Note

RF0 is Codex-reviewed and locked. The finding classifications remain evidence
intake only; RF1 fixes must be implemented and reviewed in a separate phase.
