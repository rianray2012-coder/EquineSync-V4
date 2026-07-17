# Master EquineSync Wave 2 Current-State Assessment

| Domain | Current runtime | Canonical direction | Drift |
| --- | --- | --- | --- |
| Horse registry | `horses`, Passport/Ledger projections | strengthen `horses` as stable registry | free-form patch, limited history/idempotency |
| Facility hierarchy | `facility_locations` | RF27 canonical owner | legacy `locations` and `stall_assignments` remain compatibility inputs |
| Horse assignment | `horse_location_assignments` | canonical assignment history | legacy stall rows must remain read-only |
| Daily care | care profiles, feed/medication/log collections | additive governed records | fragmented completion and correction contracts |
| Tasks | task engine collections | retain task engine | add canonical horse/location references and request identity |
| Incidents | `incidents` | retain and harden | thin validation and history |
| Inventory | `inventory` | retain and harden | adjustment lineage incomplete |
| Equipment | `horse_equipment` plus UI projections | canonical equipment records | facility equipment semantics incomplete |
| Maintenance | `facility_maintenance_tickets` | RF27 canonical owner | strengthen history and verification |
| Operations board | frontend projections | read-only projection | must never become write authority |

Existing frontend routes are retained. Wave 2 adds a governed API/service layer
and compatibility metadata; it does not duplicate UI or calendar truth.
