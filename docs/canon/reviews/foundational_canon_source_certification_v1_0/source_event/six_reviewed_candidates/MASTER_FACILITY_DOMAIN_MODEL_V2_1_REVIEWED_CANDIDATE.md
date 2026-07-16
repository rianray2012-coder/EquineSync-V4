# MASTER FACILITY DOMAIN MODEL

**Version:** 2.1  
**Status:** CONTROLLED SUCCESSOR CANDIDATE - NOT ADOPTED - NO IMPLEMENTATION AUTHORITY  
**Source posture:** Founder-controlled Version 2.0 draft located; expanded into a comprehensive physical-place constitutional candidate  
**Implementation authority:** FALSE  
**Production authority:** FALSE

# Executive Purpose

This Model defines the physical-place domain for EquineSync. It governs how campuses, parcels, structures, spaces, zones, routes, assets, utilities, hazards, resources, maps, capacity, occupancy, condition, and location history are represented.

It owns physical truth. The Barn Lifecycle owns operational use of that physical truth. The Business Lifecycle owns commercial and organizational activity conducted at the place.

# Domain Ownership Boundary

- This Model owns facility identity, hierarchy, physical attributes, location, condition, capacity, assets, utilities, hazards, maps, and decommissioning.
- It does not determine horse ownership, business ownership, legal title, tenancy rights, staff authority, financial responsibility, or service contracts.
- Property deeds, leases, inspections, permits, insurance records, maps, sensors, and user reports are evidence sources and may conflict.
- Physical occupancy and operational assignment are temporal relationships, not permanent attributes of the horse, person, or business.

# Facility Entity Hierarchy

## Primary Levels

- Facility or site
- Campus, parcel, tract, or managed area
- Structure or building
- Operational zone or exterior area
- Room, stall, pen, pasture, paddock, arena, aisle, run, wash rack, feed room, tack room, office, storage area, trailer area, or other space
- Subspace, fixture, asset, utility point, emergency resource, access point, or hazard

## Hierarchy Rules

- Hierarchy must support containment, adjacency, route, shared-resource, and overlapping-zone relationships.
- A space may have multiple operational labels but one governed identity.
- Temporary subdivisions and combined spaces require effective dates.
- Aliases and historical names must be preserved without creating duplicates.
- External address standards do not replace internal operational location identity.

# Identity, Provenance, and Temporal Truth

- Facility identity must remain stable across renaming, sale, lease, operator change, renovation, subdivision, or brand change.
- Physical changes require effective dates, provenance, responsible actor, and prior-state preservation.
- Unknown, estimated, measured, imported, verified, disputed, and superseded values must remain distinguishable.
- Geometry, dimensions, capacity, utilities, hazards, and condition may differ by source and require reconciliation.
- Material merges, splits, demolitions, or relocations must preserve lineage and historical references.

# Maps, Geometry, and Geospatial Representations

- Maps may represent parcels, structures, interiors, routes, gates, fences, utilities, emergency resources, evacuation paths, hazards, occupancy, and work zones.
- A map is a projection and may not be treated as current without source and effective-date context.
- Precise coordinates, access points, security systems, camera locations, chemical storage, animal locations, and emergency resources may be sensitive.
- Offline maps require version, freshness, encryption, and revocation considerations.
- User-generated sketches, aerial imagery, GIS data, vendor maps, and sensor layouts must retain source and confidence.
- Route optimization must account for closures, quarantine, restricted areas, weather, surface condition, and human accessibility.

# Occupancy, Capacity, and Suitability

- Design capacity, legal capacity, operational capacity, welfare capacity, reserved capacity, and temporarily available capacity are distinct.
- Occupancy assignments require subject, space, purpose, effective period, status, and responsible authority.
- Confirmed, reserved, pending, temporary, quarantine, hospital, unavailable, maintenance, and restricted states must be distinguishable.
- Capacity calculations must not imply legal compliance or welfare suitability without verified criteria.
- Suitability may depend on horse size, health, behavior, sex, herd compatibility, footing, fencing, climate, access, and care plan; the system may assist but not make final welfare determinations.

# Assets, Fixtures, Equipment, and Infrastructure

- Assets may be fixed, movable, shared, leased, borrowed, rented, or owned by different parties.
- Identity must support serial number, tag, QR code, location, responsible party, condition, maintenance, warranty, inspection, calibration, and retirement.
- Critical assets require heightened monitoring and failure escalation.
- Equipment assignment does not prove ownership.
- Asset history must survive relocation, transfer, replacement, and decommissioning where operational or evidentiary value remains.

# Utilities, Hazards, Security, and Emergency Resources

- Utilities may include water, electrical, fuel, drainage, ventilation, communications, fire systems, generators, wells, septic, and environmental controls.
- Hazards may include structural, electrical, fire, chemical, biological, environmental, security, footing, fencing, water, traffic, or access risks.
- Emergency resources may include extinguishers, hydrants, shutoffs, exits, first aid, trailers, evacuation zones, generators, and emergency supplies.
- Location and status of safety-critical resources require current verification, inspection history, and clear degraded-state behavior.
- Security details must be protected from broad disclosure and may require separate access from ordinary facility maps.

# Maintenance and Condition State

- Condition observations must retain source, date, confidence, severity, photos, and affected use.
- Maintenance classes include inspection, preventive, corrective, emergency, capital, cleaning, seasonal, and compliance-related work.
- An open maintenance issue may restrict a space, route, asset, utility, or capacity calculation.
- Completion does not erase the defect history and may require verification before return to service.
- AI may assist with image classification, duplicate detection, or priority suggestions but may not certify safety or compliance.

# Environment, Weather, and Connected Devices

- Environmental observations may include temperature, humidity, air quality, water status, soil, footing, precipitation, wind, heat index, and other conditions.
- Sensor data must retain device identity, calibration, timestamp, latency, quality, connectivity, and failure state.
- External weather and sensor data are observations, not unquestionable truth.
- Automated alerts and actions require thresholds, hysteresis, false-positive handling, review, and safe fallback.
- Connected gates, cameras, feeders, water monitors, trackers, and other devices require device governance, access control, incident response, and vendor exit planning.

# Privacy and Security of Place

- Exact horse location, private residence details, minor-associated areas, security systems, camera locations, access codes, evacuation resources, and valuable assets may be highly sensitive.
- Public facility discovery must use a separate projection and may generalize or suppress exact location and layout.
- Location sharing must be purpose-limited, time-aware, revocable, and protected against scraping or re-identification.
- Administrative and support access to maps and security details must be minimized and audited.
- Exports and integrations must not expose hidden map layers or sensitive attributes merely because the base facility is shareable.

# Facility Change, Transition, and Decommissioning

- Renovation, expansion, subdivision, consolidation, sale, lease change, operator change, disaster, demolition, or closure must preserve historical identity and effective dates.
- Changes must update affected capacity, routes, hazards, occupancy, maintenance, emergency plans, and integrations.
- Decommissioning must revoke credentials, disconnect devices, preserve required records, and prevent stale maps from appearing current.
- A successor operator does not automatically inherit private operational, customer, staff, security, or financial records.
- Historical facility references must remain resolvable for horse, incident, service, audit, and legal continuity.

# Domain Success Criteria

- Every physical object has a stable identity and understandable place in the hierarchy.
- Current maps, condition, capacity, and occupancy can be distinguished from history.
- Sensitive location and security information is protected.
- Operational systems can consume facility truth without redefining it.
- Changes and closure preserve lineage, evidence, and safe decommissioning.

# Cross-Canon Interpretation

This document must be interpreted consistently with the approved EquineSync Product Vision and controlling specialized canon. It owns the domain-level constitutional rules identified here, but it does not displace Identity, Relationship, Permission, Privacy, Record Stewardship, Claims, Audit, Communications, Financial Truth, AI, Reporting, Search, Integration, Resilience, or other specialized constitutional owners.

- Lower-order specifications may add implementation detail but may not contradict this model.
- Where two documents appear inconsistent, the conflict must be entered into controlled reconciliation rather than resolved through local implementation preference.
- Version references must be maintained through the Canon Catalog and traceability register.
- No UI label, database table, vendor object, or integration payload may redefine a constitutional concept.

# Authority Boundary

This successor candidate does not authorize canon adoption, canon lock, implementation, schema mutation, migration, permission expansion, external-processor activation, production access, AI activation, destructive action, public launch, or public compliance claims. Each requires separate authority under the applicable governance process.

# Successor Review Disposition

The document is recommended for founder review as an expanded controlled successor candidate. Creation, rendering, or delivery does not constitute approval, adoption, or lock.
