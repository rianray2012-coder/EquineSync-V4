# BN14A Phase Matrix

Roadmap source: `/Users/rianray/Downloads/equinesync_phased_plan_md 2/`

Classification key:

- **Built** - product workflow exists with meaningful backend/frontend behavior.
- **Mostly Built** - workflow exists, but has known hardening or evidence gaps.
- **Partially Built** - important pieces exist, but the roadmap scope is not yet
  fully represented.
- **Foundation Only** - generic route/page/collection scaffolding exists, but
  the real workflow is not built.
- **Placeholder Only** - UI copy or setup-intent shell exists without a product
  workflow.
- **Missing** - no meaningful implementation found.
- **Deferred by Design** - intentionally later phase.

| Uploaded roadmap phase | Current status | Evidence in current code | BN14A assessment |
| --- | --- | --- | --- |
| Phase 0 - Foundation Audit and Cleanup | Mostly Built | Admin-8 seed safety, BN3 account memberships, BN4 invites, BN5 minor safeguards, BN6 DocuSign prep, BN7-BN13 evidence, `core/permissions.py`, `roleLanding.js`, `roleNavigation.js` | Do not restart Phase 0, but reconcile stale docs, dirty worktree, duplicate-copy files, route-lock portability, and a full permission matrix before expansion. |
| Phase 1 - Role-Based UX and Dashboard Stabilization | Mostly Built | `RoleHome.jsx`, `roleNavigation.js`, `roleLanding.js`, BN13B-P packages, role screenshot evidence | Role shells exist and Title Case polish is locked. Some role-home surfaces remain setup-intent / empty-state surfaces, not operational dashboards. BN14B should close remaining role UX/hardening gaps. |
| Phase 2 - Daily Care Core / Today's Pulse / Changed Since Last Login / Watchlist / Timeline | Partially Built | `Today.jsx`, `MyWork.jsx`, `task_engine.py`, `horse_ledger.py`, HorseOps 1A-K, owner-safe care ledger | Daily care primitives are strong, but the roadmap's unified Today’s Pulse, Changed Since Last Login/Shift, Horse Watchlist, and canonical Horse Timeline are not yet fully integrated. This should be the next product build track after BN14B. |
| Phase 3 - Staff Workflows / Body Checks / Shift Handoff / Medication Safety | Partially Built | `MyWork.jsx`, `Today.jsx`, `care.py`, `backlog.py` staff portal endpoints, `HealthCareLogs.jsx`, medication routes, HorseOps daily checks | Staff task and check foundations exist. Medication and handoff flows need roadmap-specific safety rules, escalation, audit, and mobile evidence before considered complete. |
| Phase 4 - Facility Tickets / Hazard Reporting / Repair Management | Foundation Only | `backlog.py` operations modules, `Equipment.jsx`, `/maintenance` route alias, `BarnLocations.jsx` | No dedicated facility ticket state machine found. Needs ticket module with hazards, assignment, status, costs, vendors, photo/docs, dashboard, and Today’s Pulse integration. |
| Phase 5 - Client Onboarding / Gear / Tack / Grooming Inventory | Partially Built | `Onboarding.jsx`, onboarding backend, `Equipment.jsx`, `SupplyInventory.jsx`, HorseOps equipment endpoints | Gear/equipment foundations exist. Client onboarding checklist, personal tack/grooming owner visibility, photos, lifecycle status, and timeline integration need dedicated build. |
| Phase 6 - Trainer Recommendations / Owner Shopping List | Foundation Only | `TrainingPlans.jsx`, `Training.jsx`, trainer role-home shell | Training records exist, but recommendation lifecycle, owner shopping list, approval/visibility, and item completion workflow are mostly new. |
| Phase 7 - Owner Updates / Communication Preferences / Media Controls / Digests | Partially Built | `owner_updates.py`, `OwnerUpdates.jsx`, `digests.py`, `GroupMessaging.jsx`, `Messaging.jsx`, owner-safe HorseOps | Strong owner-update and digest foundations exist. Communication preferences, no-news updates, photo/video controls, and digest governance need expansion. |
| Phase 8 - Business / Risk / Compliance / Billing Add-Ons / Service Packages | Partially Built | `Incidents.jsx`, `operations.py` incidents, `FormsSignatures.jsx`, `document_signatures.py`, 15R billing phases, recurring charges | Incidents, DocuSign, billing, and subscription foundations exist. Compliance center, service package builder, add-on charge capture, and billing approval queue need product-specific build. |
| Phase 9 - Capital Improvement Planning | Missing | No dedicated capital-improvements route/page identified | New module required. Should wait until core daily/staff/client workflows are stable. |
| Phase 10 - Scheduling / Arena Conflicts / Reschedule Requests / Shows / Clinics | Partially Built | `ArenaSchedule.jsx`, `Lessons.jsx`, `Competitions.jsx`, `PastureSchedule.jsx`, `backlog.py` arena schedule | Scheduling shells and records exist. Conflict warnings, reschedule requests, show/clinic planning, and role-safe owner/rider views need dedicated build. |
| Phase 11 - Premium Differentiators | Partially Built | `Rehab.jsx`, `WeightTrends.jsx`, `RideGps.jsx`, HorseOps weight/care records | Rehab and weight foundations exist. Digital whiteboard, horse transfer, premium packaging, and deeper body-condition workflow need build. |
| Phase 12 - Platform Maturity | Partially Built | Admin Portal reports/audit/alerts, `AuditLog.jsx`, `AdvancedReports.jsx`, notifications/digest backend | Admin maturity exists. Global permission-aware search, smart notifications, quiet hours, and major-data-type search integration remain future work. |
| Phase 12A - Steed Mascot System | Missing / Deferred by Design | No mascot component found | Defer until Phase 12 maturity. It should be a delight/polish layer, not a core workflow dependency. |
| Phase 13 - Go-Live Readiness | Partially Built | BN7-BN13 UAT/evidence, production deploy notes, Admin/HorseOps/billing hardening packages | Significant go-live groundwork exists, but new roadmap expansion means final go-live hardening must run again after core workflow buildout. |
| Phase 14 - Barn Brain Assistant | Deferred by Design | `AiAutomation.jsx` generic automation foundation | Do not start. Barn Brain should wait until records, permissions, search, audit, and Today’s Pulse are mature. |

## Summary

The current codebase is not a blank slate. It already satisfies much of the
foundation and role UX intent. The next risk is over-crediting generic
backlog pages as complete product workflows. BN14B should clean current
hardening/role UX gaps; BN15 should begin the new roadmap with Today's Pulse,
Watchlist, Timeline, and Changed Since Last Login.

