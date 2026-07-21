# Workflow Register

All workflows are documentary candidates and are not authorized for execution.

## FAC-WF-001 - Create first operating context

**Flow:** Create Tenant; optionally create DRAFT Facility and real Organization; hand off membership and permission to owning domains; verify no automatic authority.  
**Decisions:** `FAC-FD-001;FAC-FD-002;FAC-FD-017`  
**Requirements:** `FAC-REQ-002;FAC-REQ-003;FAC-REQ-008;FAC-REQ-035`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-002 - Add second facility

**Flow:** Create stable Facility; verify address/topology; create explicit Tenant-Facility association; publish no public projection by default.  
**Decisions:** `FAC-FD-004;FAC-FD-005;FAC-FD-014`  
**Requirements:** `FAC-REQ-005;FAC-REQ-006;FAC-REQ-017`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-003 - Cross-facility professional

**Flow:** Keep one person identity; create separate Relationship-owned associations; require context switch and per-tenant authorization.  
**Decisions:** `FAC-FD-009;FAC-FD-010;FAC-FD-011;FAC-FD-013`  
**Requirements:** `FAC-REQ-003;FAC-REQ-009;FAC-REQ-011;FAC-REQ-012`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-004 - Restrict or retire facility area

**Flow:** Propose restriction; assess occupancy/routes; approve; effective-date state; invalidate projections; preserve history.  
**Decisions:** `FAC-FD-005;FAC-FD-007;FAC-FD-008`  
**Requirements:** `FAC-REQ-006;FAC-REQ-026;FAC-REQ-027;FAC-REQ-028`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-005 - Suspend tenant

**Flow:** Record cause and authority; suspend current and offline access; stop jobs and integrations; preserve records; issue notice handoff; require reviewed restoration.  
**Decisions:** `FAC-FD-007;FAC-FD-008;FAC-FD-009`  
**Requirements:** `FAC-REQ-014;FAC-REQ-015;FAC-REQ-029;FAC-REQ-032`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-006 - Transfer facility or change operator

**Flow:** Preserve Facility identity; create temporal operator association; reconcile every downstream domain explicitly; do not transfer private data or authority automatically.  
**Decisions:** `FAC-FD-004;FAC-FD-008`  
**Requirements:** `FAC-REQ-005;FAC-REQ-021;FAC-REQ-027`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-007 - Merge duplicate facility candidates

**Flow:** Detect; quarantine proposed pair; human review; compare tenant impact; approve lineage-preserving merge; reconcile and verify; retain reversal evidence.  
**Decisions:** `FAC-FD-015`  
**Requirements:** `FAC-REQ-007;FAC-REQ-022;FAC-REQ-023`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-008 - Switch active context

**Flow:** Select authorized tenant then optional facility; server validates; UI displays; audit prior/new context; invalidate stale work; require reconfirmation when needed.  
**Decisions:** `FAC-FD-009`  
**Requirements:** `FAC-REQ-011;FAC-REQ-012;FAC-REQ-013`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-009 - Import ambiguous legacy topology

**Flow:** Snapshot source; parse candidates; assign tenant only when evidenced; quarantine ambiguity; prevent public/authority effects; review and promote explicitly.  
**Decisions:** `FAC-FD-018`  
**Requirements:** `FAC-REQ-024;FAC-REQ-026;FAC-REQ-027`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-010 - Publish or revoke public facility projection

**Flow:** Verify competent authority; select minimal fields; generalize location; activate anti-enumeration; audit; propagate revocation to indexes and caches.  
**Decisions:** `FAC-FD-016`  
**Requirements:** `FAC-REQ-017;FAC-REQ-018;FAC-REQ-019;FAC-REQ-033`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-011 - Organization merger or split

**Flow:** Create proposed successor topology; preserve identities and lineage; separately reconcile tenants, facilities, agreements, relationships, permissions, and records.  
**Decisions:** `FAC-FD-003;FAC-FD-008`  
**Requirements:** `FAC-REQ-004;FAC-REQ-007;FAC-REQ-022`  
**Status:** `DRAFT_NOT_AUTHORIZED`

## FAC-WF-012 - Close and archive

**Flow:** Wind down; block new activity; reconcile dependencies; close; retain governed records; decommission physical projection; archive without erasing history.  
**Decisions:** `FAC-FD-007;FAC-FD-008`  
**Requirements:** `FAC-REQ-028;FAC-REQ-029;FAC-REQ-038`  
**Status:** `DRAFT_NOT_AUTHORIZED`
