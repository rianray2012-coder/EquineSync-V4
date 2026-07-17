# Master EquineSync Wave 2 Legacy Convergence Report

Result: `COMPLETE_FOR_VERIFIED_WAVE_2_SCOPE`

| Legacy structure | Disposition |
| --- | --- |
| `locations` | preserved read-only compatibility source; mapped to `facility_locations` |
| legacy stall/turnout assignment names | aliased to canonical `primary_housing` / `secondary_presence` semantics |
| Stall Map and Barn Location Board | read-compatible projection; canonical writes only |
| historical assignments | preserved |
| ambiguous identity mapping | exception-required; no guessing |

No dual writable source of truth remains in the completed Wave 2 surface.

