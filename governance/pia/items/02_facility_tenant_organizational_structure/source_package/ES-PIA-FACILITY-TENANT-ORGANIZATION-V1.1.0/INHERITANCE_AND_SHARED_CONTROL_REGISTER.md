# Inheritance and Shared Control Register

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

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

## Founder-approved onboarding boundary

Identity and Horse domains own individual/horse creation; Relationship and Authorization own later associations and authority. Facility PIA owns neither. FAC-FD-017 permits no convenience-driven ownership transfer.
