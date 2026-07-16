# Master Facility Domain Model

Status: Canon
Owner: Founder / Codex
Effective Date: 2026-07-10
Purpose: Define the canonical physical-facility model for EquineSync so RF27 and future facility work represent real barn operations without drifting into Passport transfer, billing, provider, calendar, or generic property-management scope.

## Facility Domain Doctrine

A facility is not only a customer address. It is the physical operating environment where horses, people, work, care, safety, logistics, and maintenance intersect.

EquineSync must model facilities in a way that supports:

- Horse-first current location truth.
- Barn-owner and manager operational command.
- Staff-friendly mobile workflows.
- Safe owner/provider visibility.
- Location-aware tasks and maintenance.
- Analytics and future AI events.
- Clear separation from Passport transfer, ownership, billing, and marketplace domains.

## Canonical Entity Hierarchy

| Entity | Parent | Category | Purpose |
| --- | --- | --- | --- |
| Facility | none | Root | Physical equine operation under one facility/business context. |
| Building | Facility | Structure | Barn, arena, storage building, or other major structure. |
| Barn | Facility or Building | Structure | Primary horse housing structure. |
| Wing | Building/Barn | Subdivision | Named area inside a barn or building. |
| Aisle | Building/Barn/Wing | Subdivision | Operational corridor grouping stalls and workflow movement. |
| Section | Any location | Subdivision | Flexible operational grouping. |
| Stall | Barn/Aisle/Section | Horse Location | Primary individual horse housing assignment. |
| Hospital Stall | Barn/Aisle/Section | Horse Location | Restricted stall for injury, treatment, or close monitoring. |
| Quarantine | Facility/Barn/Section | Horse Location/State | Biosecurity or intake separation location and status. |
| Pasture | Facility | Turnout | Group or individual turnout area. |
| Paddock | Facility/Pasture | Turnout | Smaller turnout or holding area. |
| Run | Barn/Stall/Paddock | Turnout | Attached or narrow turnout run. |
| Arena | Facility/Building | Work Area | Riding, lesson, training, or competition prep space. |
| Round Pen | Facility | Work Area | Training or controlled exercise area. |
| Wash Rack | Building/Barn | Care Area | Bathing, cooling, and grooming area. |
| Cross Ties | Building/Barn/Aisle | Care Area | Tacking, grooming, and vet/farrier prep area. |
| Feed Room | Building/Barn | Storage | Feed storage and preparation area. |
| Hay Loft | Building/Barn | Storage | Hay storage area with safety and inventory implications. |
| Storage | Facility/Building | Storage | General supplies, bedding, and equipment. |
| Trailer Parking | Facility | Logistics | Trailer, hauling, and event logistics location. |

## Required Location Attributes

Each location record should support:

- Stable ID.
- Facility ID.
- Parent location ID, where applicable.
- Location type.
- Display name.
- Active/inactive status.
- Capacity or occupancy limit, where applicable.
- Biosecurity/quarantine flag, where applicable.
- Horse-safe visibility classification.
- Owner/provider visibility classification.
- Maintenance relevance.
- Mobile ordering/sort position.
- Audit metadata.

## Horse Location Rules

- A horse may have one primary current physical location within a facility.
- A horse may have historical location assignments.
- A horse location assignment does not imply ownership, custody, transfer, or Passport relationship changes.
- Quarantine and hospital-stall context may be sensitive and must respect medical/privacy permissions.
- Owner and provider visibility must be explicitly scoped.

## Maintenance Rules

Maintenance tickets should attach to the most specific relevant location.

Examples:

- Broken stall latch -> Stall.
- Fence down -> Pasture or paddock.
- Water issue -> Stall, pasture, aisle, or barn area.
- Arena footing problem -> Arena.
- Feed room safety issue -> Feed Room.

Maintenance records must support:

- Opened state.
- Assigned owner.
- Safety impact.
- Horse/location impact.
- Priority.
- Closure state.
- Audit trail.

## Operational Reality Backbone

The facility model must support the minute-by-minute barn day:

1. Unlock gates.
2. Walk perimeter.
3. Check water.
4. Deliver hay/feed.
5. Coordinate AM meds or sensitive care handoff.
6. Remove blankets.
7. Execute turnout order.
8. Drag arenas and ready work areas.
9. Remove manure and check aisles.
10. Confirm staff readiness.
11. Handle vet/farrier/provider arrivals.
12. Prepare lessons and client arrival.
13. Respond to emergency interruptions.
14. Complete night checks.
15. Close facility.

RF27 should model the facility surfaces required for these actions while leaving full scheduling, provider operations, medical records, and billing workflows to their approved phases.

## Analytics Requirements

Facility records should emit analytics-ready events for:

- Location created.
- Location updated.
- Horse location assigned.
- Horse moved.
- Stall occupancy.
- Pasture occupancy.
- Maintenance opened.
- Maintenance closed.
- Opening readiness started.
- Opening readiness completed.
- Physical intake completed.

Analytics must follow `MASTER_ANALYTICS_FRAMEWORK.md`: definition before display, source before summary, permission before aggregation, and context before judgment.

## AI Requirements

Facility events should be AI-ready, but AI must not control facility operations.

Allowed future AI uses:

- Draft summaries.
- Suggest likely stall/turnout options for human review.
- Highlight congestion or maintenance hotspots.
- Identify onboarding bottlenecks.

AI must not:

- Move a horse.
- Assign quarantine.
- Close maintenance.
- Infer ownership or custody.
- Expose restricted horse location, health, or staff data.
- Present recommendations without source transparency.

## Domain Boundaries

RF27 owns physical facility and barn operations reality.

RF27 does not own:

- Passport transfer approvals.
- Former/new facility relationship continuity.
- Historical document release and intake.
- Ownership or custody changes.
- Provider marketplace operations.
- Calendar integrations.
- Billing issue workflows.
- Public launch approval.

Those belong to separately gated phases.
