# RF11 Property, Location, Map, and Community Help System

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF11 verifies and narrows EquineSync location, map, arena, stall-card, QR, and
community-help claims. The phase keeps existing web-first behavior honest:
published owner/parent location views must be explicit, owner-safe, and
bounded, while unbuilt map, native, offline, QR, and dispatch behavior remains
deferred.

## Implemented In RF11

- Barn-location share payloads now include explicit `share_state` metadata.
- Owner/parent barn-location shares still require the stored share setting to be
  enabled.
- Owner/parent barn-location views omit internal stall `notes` and pasture
  `weather_rule` text, and top-level share metadata omits internal
  `created_by`, `updated_by`, and `created_at` fields.
- Staff barn-location views keep operational notes and weather rules.
- Arena owner/parent share views include only `shared_with_owners` blocks and
  omit internal `owner_name`, `notes`, and staff/admin share metadata.
- Staff arena views keep staff-only blocks and private operational fields.
- Stall-card evidence remains truthful: local printable SVG readiness only, not
  true QR encoding or native scanning.

## Surface Inventory

| Surface | Current Evidence | RF11 Status |
| --- | --- | --- |
| Stall map | `frontend/src/App.js`, `backend/routes/backlog.py` `stall-map` module | inventoried |
| Barn locations | `/barn-location-share`, `BarnLocations` route | hardened for owner-safe projection |
| Pasture schedule | `pasture-schedule` module feeds location board | owner weather-rule text hidden |
| Arena schedule | `/arena-schedule-share`, `ArenaSchedule` route | owner visibility filtered |
| Emergency contacts/workflows | backlog modules and owner portal emergency route | inventoried; community/public escalation deferred |
| QR horse ID / stall card | `/integrations/qr-horse-id/{record_id}/stall-card` | local SVG claim only |

## Deferred Boundaries

| Boundary | Status | Owner |
| --- | --- | --- |
| Canonical property/location IDs and movement audit history | deferred | RF11 follow-up or RF18 |
| Live maps, geocoding, route navigation, or public map sharing | deferred | RF17/RF18 |
| Native shell, app-store/TestFlight readiness, or QR scanning | deferred | BN22A/RF17 |
| Public community-help network or emergency dispatch behavior | deferred | founder decision, RF13/RF18 |
| True QR-code image encoding | deferred | RF17/native follow-up |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Accept default property/location privacy posture. | requires founder review | Recommended default remains private until a barn admin or manager explicitly enables a share surface. |
| Decide owner/rider map visibility depth. | requires founder review | Current RF11 evidence covers explicitly published owner/parent location and arena shares only; rider map visibility remains deferred. |
| Decide community-help audience and escalation model. | requires founder review | Choose internal barn-only, linked owner/rider, service-provider, or broader community behavior before implementation. |
| Decide QR/stall-card claim level. | requires founder review | Current claim may say printable local stall-card SVG; it must not claim true QR encoding or native scanning. |

## Verification

RF11 is verified by:

- focused backend tests in
  `backend/tests/test_rf11_property_location_map_community_help.py`;
- report generation through
  `backend/scripts/build_rf11_property_location_map_community_help.py`;
- package integrity verification against
  `outputs/build_next_rf11_property_location_map_community_help.zip`;
- secret-shape scan over RF11 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync supports admin-enabled owner/parent barn-location and arena share
  views.
- Those owner/parent views use owner-safe projections and explicit share-state
  evidence, including sanitized share metadata.
- Printable stall-card SVG readiness exists for QR horse ID records.

Current launch claims must not say:

- EquineSync provides full public maps, universal location sharing, audited
  movement history, live route navigation, geocoding, dispatch, public
  community-help networking, true QR scanning, or offline/native map support.
