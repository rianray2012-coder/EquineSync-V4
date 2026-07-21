# Inheritance and Shared Control Register

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

| ID | Control | Owner/source | Treatment | Facility rule |
| --- | --- | --- | --- | --- |
| FAC-CTRL-001 | Identity/authentication | Identity V2.0 | INHERITS | Actor/account identity; no facility authority |
| FAC-CTRL-002 | Relationships/membership | Relationship V2.0 | INHERITS_AND_CONFIGURES | Typed associations; Relationship owns truth |
| FAC-CTRL-003 | Authorization/permissions | Permission V1.1; Agreement V2.1 | INHERITS | Action-time default denial; association and verification are not authority |
| FAC-CTRL-004 | Audit/evidence | Audit V2.0 | INHERITS_AND_EXTENDS | Adds topology context/change-set fields |
| FAC-CTRL-005 | Privacy/safeguarding | Privacy V2.0 | INHERITS_AND_EXTENDS | Protects precise location, layouts and occupants |
| FAC-CTRL-006 | Retention/correction | Record Stewardship V2.1 | INHERITS_AND_CONFIGURES | Schedules remain Founder/legal/operational decision |
| FAC-CTRL-007 | Notifications | Communications V2.0 | INHERITS_AND_TRIGGERS | Creates notice intent only |
| FAC-CTRL-008 | Search/public discovery | Search V2.0 | INHERITS_AND_CONFIGURES | Filter before retrieval; separate public projection |
| FAC-CTRL-009 | Operations/release | Platform Operations V2.0 | INHERITS | No release authority here |
| FAC-CTRL-010 | Configuration/flags | Configuration V2.0 | INHERITS | Cannot weaken controls |
| FAC-CTRL-011 | Backup/recovery | Resilience V1.0 | INHERITS_AND_EXTENDS | Reconcile topology/context after restore |
| FAC-CTRL-012 | Security incident | Security Incident V1.0 | INHERITS | Containment/disclosure outside domain ownership |
| FAC-CTRL-013 | Integrations/adapters | Developer Platform V2.0; External Architecture V2.0 | INHERITS_AND_CONFIGURES | Context-bound/no external authority |
| FAC-CTRL-014 | Horse continuity | Horse Lifecycle V3.1; Transfer Policy | DEPENDS_ON | Location/topology never transfers horse authority |
