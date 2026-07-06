# RF0 Current State Inventory

Generated: 2026-07-06

Scope: evidence-only RF0 intake. No RF1-RF18 implementation was performed.

Source handoff: `/Users/rianray/Downloads/equinesync_rf_refinement_roadmap_codex_handoff.md`

## RF0 Result

Overall status: `codex_reviewed_locked`

Recommended next phase: `RF1 - P0 Data Fences and Backend Capability Gates`

Reason: the highest-risk open findings are tenant/privacy/billing/export risks. RF1 must close those before broader feature completion, trainer/provider expansion, onboarding imports, or public-launch re-readiness.

## Scope Controls Preserved

- No new product behavior.
- No frontend route implementation.
- No backend route/schema/auth/permission mutation.
- No provider calls.
- No Stripe, Apple, Google, DocuSign, Resend, MongoDB, Vercel, Render, Atlas, App Store Connect, or Play Console mutation.
- No UAT/customer/founder acceptance mutation.
- No native app implementation.
- No app-store submission.

## Evidence Summary

| Area | Current Evidence | RF0 Classification |
| --- | --- | --- |
| Role routing/dashboard/intake state | `frontend/src/lib/roleNavigation.js`, `frontend/src/lib/roleLanding.js`, `frontend/src/App.js`, `frontend/src/pages/RoleIntake.jsx`, dashboard components under `frontend/src/features/dashboards/`. | Partially fixed: role shells and guards exist, but several role surfaces are still intake/readiness/generic. |
| Backend permission gates | `backend/core/permissions.py` has fail-closed capabilities and platform-role separation; many backlog routes use `require_permission`. | Partially fixed: RF1 must prove every sensitive direct route and write. |
| Owner-safe scoping | `backend/routes/horse_ledger.py` has stable owner checks and owner-safe projections; `backend/routes/owner_updates.py` scopes owner updates to owned horses. | Partially fixed: backlog owner portal still uses names/free text. |
| Feature-module exposure | `frontend/src/App.js` routes many backlog/readiness pages; `backend/routes/backlog.py` implements feature-module records and manifests. | Open P1: RF4/RF17 needed. |
| Provider/trainer support | `backend/routes/trainer_intake.py` is intake-only; service-provider dashboard is a shell; route/navigation support exists. | Open P1: RF9/RF10 needed after RF1/RF2. |
| Offline/app-store posture | Locked BN18D-BN21 docs and proof helpers preserve online-first/limited recovery and native-store deferral. No native project/service worker found in shallow source scan. | Deferred: RF15/RF16 future implementation. |
| Admin portal current state | `backend/routes/admin_portal/` and `frontend/src/pages/admin/` provide platform admin users, facilities, billing, support, alerts, reports, integrations, settings, and audit logs. | Partially fixed: RF5 intelligence/customer-success center not complete. |

## Known Finding Classification

| ID | Known Finding | Classification | RF Phase Mapping | Source Evidence |
| --- | --- | --- | --- | --- |
| RF0-F01 | Owner Portal and owner-facing surfaces need a true owner-safe horse endpoint. | partially fixed | RF1, RF7 | Stable owner-safe horse ledger path in `backend/routes/horse_ledger.py`; backlog owner-portal modules in `backend/routes/backlog.py` still use display-name/free-text fields. |
| RF0-F02 | Some backend writes still need explicit capability gates, not only barn stamping or frontend nav. | open P0 | RF1 | `backend/core/permissions.py` is present, but RF0 did not find a complete sensitive-route capability matrix. |
| RF0-F03 | QuickBooks invoice export must be barn-scoped. | open P0 | RF1, RF12 | `backend/routes/backlog.py` scopes expenses by barn but reads invoices with `db.invoices.find({})`. |
| RF0-F04 | Owner portal billing and related surfaces still rely on name/free-text fields. | open P0 | RF1, RF2, RF7, RF12 | `backend/routes/backlog.py` uses `full_name`, `owner_name`, `recipient_name`, and `shared_with` regex in owner-portal billing/forms/health/training surfaces. |
| RF0-F05 | Owner updates exist in two worlds. | partially fixed | RF6, RF7, RF17 | Canonical lifecycle exists in `backend/routes/owner_updates.py`; feature-module owner media update surface exists in `backend/routes/backlog.py`. |
| RF0-F06 | Feature-module shells still appear as production-like modules. | open P1 | RF4, RF17 | User-routed pages include Mobile Readiness, Advanced Reports, Group Messaging, AI Automation, Forms & Signatures, Staff Tasks, Supply Inventory. |
| RF0-F07 | Staff scheduling, tasks, handoffs, and time clock are name-based. | open P1 | RF2, RF8 | Staff portal code in `backend/routes/backlog.py` matches on `full_name`, `staff_name`, and `assigned_to`; frontend forms use staff-name fields. |
| RF0-F08 | Staff Tasks and Task Engine are parallel task systems. | open P1 | RF6, RF8 | `backend/task_engine.py` exists as canonical operational engine; `staff_task_assignments` and `/staff-tasks` also exist. |
| RF0-F09 | Inventory and Supply Inventory are duplicated. | open P1 | RF6 | `frontend/src/pages/Inventory.jsx`, `frontend/src/pages/SupplyInventory.jsx`, and routes for `/inventory` and `/supply-inventory` coexist. |
| RF0-F10 | Group Messaging tracks intent/status but may not deliver messages. | open P1 | RF13, RF17 | `frontend/src/pages/GroupMessaging.jsx` handles push preview/manifests and placeholder readiness. |
| RF0-F11 | Advanced Reports imply Excel/PDF while export behavior may be manifest-based. | open P1 | RF12, RF17 | `backend/routes/backlog.py` reports export returns `export_manifest_ready` and CSV/JSON download formats while the requested format is xlsx/pdf. |
| RF0-F12 | Owner payment flow can be configuration-ready rather than true collection. | open P0 | RF1, RF12 | `backend/routes/backlog.py` owner-portal payment preparation uses owner name fallback and returns provider posture, not proven collection. |
| RF0-F13 | QR/stall-card flow may not be a true QR encoder. | open P2 | RF11, RF17 | `frontend/src/pages/MobileReadiness.jsx` and backlog QR hooks are readiness/stall-card oriented. |
| RF0-F14 | Barn-location and arena-share defaults need explicit publish state. | open P1 | RF1, RF11 | Location/share routes exist; RF0 did not find a canonical publish-state model for owner/rider visibility. |
| RF0-F15 | Trainer fluidity is not fully built. | open P1 | RF9 | `backend/routes/trainer_intake.py` explicitly says it does not create lessons, enrollments, assignments, permissions, billing, DocuSign, or HorseOps data. |
| RF0-F16 | Service provider multi-barn/client access is not fully built. | open P1 | RF10 | Service-provider dashboard says data appears after facility grants access, but RF0 did not find provider grants/appointments/visit-note model. |
| RF0-F17 | Onboarding remains a major pain-point risk. | open P1 | RF3, RF5 | Current onboarding/readiness exists, but RF3 import concierge, review-first AI setup, and first-value milestone analytics are not complete. |
| RF0-F18 | Admin portal should become product intelligence/customer-success center. | partially fixed | RF5 | Admin Portal platform-role surfaces exist, but RF5 User 360, Facility 360, dunning/interventions, feature health, data quality, and account-health intelligence are incomplete. |

## RF Phase Mapping

| RF Phase | Findings Mapped |
| --- | --- |
| RF1 | RF0-F01, RF0-F02, RF0-F03, RF0-F04, RF0-F12, RF0-F14 |
| RF2 | RF0-F04, RF0-F07 |
| RF3 | RF0-F17 |
| RF4 | RF0-F06 |
| RF5 | RF0-F17, RF0-F18 |
| RF6 | RF0-F05, RF0-F08, RF0-F09 |
| RF7 | RF0-F01, RF0-F04, RF0-F05 |
| RF8 | RF0-F07, RF0-F08 |
| RF9 | RF0-F15 |
| RF10 | RF0-F16 |
| RF11 | RF0-F13, RF0-F14 |
| RF12 | RF0-F03, RF0-F04, RF0-F11, RF0-F12 |
| RF13 | RF0-F10 |
| RF14 | RF0-F04, RF0-F06 |
| RF15 | Offline/lock-screen limitations from locked BN18D/BN21 posture. |
| RF16 | Native App Store / Google Play deferred posture from locked BN18E/BN19/BN21. |
| RF17 | RF0-F05, RF0-F06, RF0-F10, RF0-F11, RF0-F13 |
| RF18 | Final regression/UAT/re-readiness after RF1-RF17. |

## Recommended RF1 Starting Checklist

1. Prove or add canonical owner-safe horse list endpoint.
2. Replace/guard owner portal name-based billing/form/health/training lookups.
3. Scope QuickBooks invoice export by barn/account.
4. Create sensitive-route capability matrix for horses, owners, riders, care, medications, vet records, injuries, wellness, tasks, lessons, training, incidents, invoices, exports, and reports.
5. Add backend tests proving cross-barn and direct-route denial behavior.

## RF0 Stop Condition

RF0 is Codex-reviewed and locked. Stop after RF0 documentation and inventory.
RF1 may proceed only as the next dedicated phase.
