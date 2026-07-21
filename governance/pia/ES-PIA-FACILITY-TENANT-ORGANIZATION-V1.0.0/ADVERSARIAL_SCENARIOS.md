# Adversarial Scenarios

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

| Scenario ID | Attack/failure | Required outcome |
| --- | --- | --- |
| FAC-ADV-001 | Replace tenant_id in a request | Generic deny; no existence leak; denied attempt audited |
| FAC-ADV-002 | Reuse stale active context after membership revocation | Deny after per-request revalidation; invalidate cache |
| FAC-ADV-003 | Claim Organization admin role to edit a Facility | Association/role alone insufficient |
| FAC-ADV-004 | Call a background job after suspension | Job partition denied/dead-lettered; no write |
| FAC-ADV-005 | Replay offline move after authority expires | Quarantine/reject; no canonical mutation |
| FAC-ADV-006 | Create an Area parent cycle | Atomic 409; topology unchanged |
| FAC-ADV-007 | Poison fuzzy duplicate evidence | No auto-merge; reviewed quarantine remains |
| FAC-ADV-008 | Mass-assign verification or public fields | Allowlist rejects protected fields |
| FAC-ADV-009 | Enumerate inaccessible facilities through search/count/autocomplete | No distinguishable existence response |
| FAC-ADV-010 | Use expired support ticket | Immediate deny and audit |
| FAC-ADV-011 | Transfer Facility and expect horses/invoices to follow | Non-cascade; dependent domains unchanged pending their own authority |
| FAC-ADV-012 | Restore backup containing revoked membership/public projection | Reconciliation prevents restored stale state becoming current |
| FAC-ADV-013 | Retry webhook/event with same idempotency key | One material effect, repeated evidence linked |
| FAC-ADV-014 | Publish exact stall layout or occupant list | Privacy allowlist denies publication |
| FAC-ADV-015 | Open deep link for another context | No silent switch; explicit permitted selection required |
| FAC-ADV-016 | Use missing context and trigger legacy default primary fallback | Target design denies/quarantines; never assigns primary |
| FAC-ADV-017 | Close Organization and inherit every permission to successor | No inheritance; reauthorization required |
| FAC-ADV-018 | Treat signed lease as application authorization | Agreement is evidence input only; action-time authorization still required |
