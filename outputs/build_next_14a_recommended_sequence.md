# BN14A Recommended Sequence

## Immediate Next Phase

### BN14B - Role UX + Hardening Cleanup

Reason: BN14A found that the app is far beyond the uploaded roadmap's starting
point, but it also found hardening and role UX cleanup that should be resolved
before new feature expansion.

Recommended BN14B scope:

1. Make Admin Portal route-lock tests portable from the current repo root.
2. Re-run route-lock and focused role-home tests.
3. Triage/fix duplicate notification categories in Settings if the fix is small
   and frontend-only.
4. Reconcile stale phase statuses in README/PRD files where safe.
5. Confirm duplicate-copy files are unused, then remove only with founder
   approval.
6. Produce a concise permission-matrix artifact for the uploaded roadmap's next
   phases.
7. No new product workflows.

Exit: current codebase is clean, portable, and ready for roadmap expansion.

## First New Roadmap Product Track

### BN15A - Today's Pulse Data Contract

Reason: the uploaded roadmap depends on Today's Pulse becoming the operational
hub for daily care, staff work, alerts, incidents, facility tickets, reminders,
and owner-visible change summaries.

Recommended scope:

1. Define Pulse input sources.
2. Define role-specific Pulse response shapes.
3. Define privacy rules for owner/guardian/rider summaries.
4. Define severity and urgency rankings.
5. Define how future modules register Pulse items.
6. No new UI beyond a small proof surface unless explicitly approved.

### BN15B - Horse Watchlist Foundation

1. Add watchlist state model.
2. Limit write roles.
3. Add audit-safe changes.
4. Prepare Today’s Pulse integration.

### BN15C - Horse Timeline Foundation

1. Create canonical timeline event shape.
2. Integrate existing HorseOps/owner-update/task events where safe.
3. Keep owner projections backend-authoritative.

### BN15D - Changed Since Last Login / Last Shift

1. Track user-specific read cursors.
2. Produce role-specific changed summaries.
3. Feed manager/staff/owner dashboard states.

### BN15E - Today's Pulse UI Integration + Mobile Evidence

1. Integrate Pulse into staff, manager, trainer, owner-safe, and admin-visible
   surfaces.
2. Capture mobile evidence.
3. Lock the new daily-care core before Phase 3 staff workflow expansion.

## Later Roadmap Order

After BN15:

1. Roadmap Phase 3 - Staff workflows, body checks, shift handoff, medication
   safety.
2. Roadmap Phase 4 - Facility tickets and hazards.
3. Roadmap Phase 5 - Client onboarding, gear, tack, grooming inventory.
4. Roadmap Phase 6 - Trainer recommendations and owner shopping list.
5. Roadmap Phase 7 - Owner communication preferences, media controls, digests.
6. Roadmap Phase 8 - Incidents, document compliance, service packages, billing
   approval.
7. Roadmap Phase 9 - Capital improvements.
8. Roadmap Phase 10 - Scheduling and conflicts.
9. Roadmap Phase 11 - Premium differentiators.
10. Roadmap Phase 12 - Search, smart notifications, quiet hours, platform
    reports.
11. Roadmap Phase 12A - Steed mascot/delight system.
12. Roadmap Phase 13 - Final go-live hardening.
13. Roadmap Phase 14 - Barn Brain.

## Do Not Start Yet

- Barn Brain.
- Steed mascot.
- Capital improvements.
- Full search.
- Push/native/offline workflows.
- Major dependency modernization.

