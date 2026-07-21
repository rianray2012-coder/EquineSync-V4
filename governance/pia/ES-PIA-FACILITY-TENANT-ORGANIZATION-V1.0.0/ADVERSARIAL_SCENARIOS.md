# Adversarial Scenarios

| ID | Attack or failure | Required response |
|---|---|---|
| ADV-01 | Role label becomes permission | Reject; role is only an input to Permission. |
| ADV-02 | Cross-tenant enumeration through ID, search, count, timing, autocomplete, or export | Return non-enumerating result; log suspicious attempts. |
| ADV-03 | Organization merge cascades permissions or memberships | Reject cascade; create domain reconciliation cases. |
| ADV-04 | Stale session retains old Tenant context | Expire/revalidate context before access; reject stale action. |
| ADV-05 | Offline write arrives after suspension | Reject or quarantine; never apply as authorized mutation. |
| ADV-06 | Support impersonation hides human actor | Reject; preserve support actor, represented principal, purpose and ticket. |
| ADV-07 | Duplicate address triggers automatic Facility merge | Create candidate only; require review and lineage. |
| ADV-08 | Public search exposes private Facility, precise location, minor area, horse location, or security detail | Suppress; only approved public projection is searchable. |
| ADV-09 | Lease, payment, ownership claim, contact, profile, or stewardship status becomes authority | Reject inference; require owning-domain decision. |
| ADV-10 | One physical Facility shared by two Tenants leaks occupancy/topology | Return tenant-specific projection only; shared identity carries no private facts. |
| ADV-11 | Restore replays an old active membership/context | Restore data but keep access revoked pending current reconciliation. |
| ADV-12 | Legacy row lacks Tenant but matches primary fallback | Quarantine; never assign to primary by convenience. |
