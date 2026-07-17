# Master EquineSync Wave 2 Legacy Convergence Register

| Legacy source | Canonical target | Treatment |
| --- | --- | --- |
| `locations` | `facility_locations` | map/read compatibility; no new canonical writes |
| `stall_assignments` | `horse_location_assignments` | read-only adapter and exception-led migration |
| horse `stall` text | assignment projection | preserve text; no identity inference |
| horse owner/rider/trainer scalar IDs | relationship references | retain, validate, do not promote to legal authority |
| `feed_tasks` / `medication_logs` | governed care evidence | compatibility plus provenance |
| ad hoc incident/inventory rows | hardened same collections | additive lineage and history |

Ambiguous mappings are quarantined. No automatic horse merge or name-based
location guessing is permitted.
