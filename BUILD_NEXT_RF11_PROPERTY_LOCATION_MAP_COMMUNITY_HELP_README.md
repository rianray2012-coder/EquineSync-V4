# RF11 Property, Location, Map, and Community Help Package

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Scope

RF11 is a narrow refinement gate for existing property, barn-location,
arena-share, stall-card, QR, and emergency/community-help surfaces.

RF11 includes:

- source inventory and evidence rows for current location/map/help surfaces;
- explicit share-state evidence for barn-location and arena-share reads;
- owner/parent-safe projections that omit internal staff notes, weather rules,
  owner-name/private arena notes, and staff/admin share metadata;
- focused backend tests for disabled shares, owner-safe projections, staff
  operational projections, and stall-card claim truth;
- generated RF11 report and review package.

RF11 does not include:

- live maps, geocoding, route navigation, dispatch, public community networking,
  native shell work, offline app behavior, true QR encoding, or QR scanning;
- provider calls or mutations to Stripe, Apple, Google, DocuSign, Resend,
  MongoDB Atlas, Vercel, Render, or UAT accounts;
- founder acceptance auto-marking.

## Evidence

- Source hardening: `backend/routes/backlog.py`
- Proof core: `backend/core/rf11_property_location_map_community_help.py`
- Report script: `backend/scripts/build_rf11_property_location_map_community_help.py`
- Focused tests: `backend/tests/test_rf11_property_location_map_community_help.py`
- Review doc: `docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP.md`
- Generated report: `outputs/rf11_property_location_map_community_help_report.md`
- Review package: `outputs/build_next_rf11_property_location_map_community_help.zip`

## Review Command

```bash
.venv/bin/python -m pytest backend/tests/test_rf11_property_location_map_community_help.py
.venv/bin/python backend/scripts/build_rf11_property_location_map_community_help.py --fail-on-blockers
unzip -t outputs/build_next_rf11_property_location_map_community_help.zip
```

## Launch Claim Boundary

Current claims may say EquineSync supports barn-admin-enabled owner/parent
location and arena share views with owner-safe projections.

Current claims must not say EquineSync has public maps, universal cached
location reads, audited movement history, route navigation, live geocoding,
dispatch, public community-help networking, true QR scanning, or offline/native
map support.
