# RF11 Property, Location, Map, and Community Help System Plan

Date: 2026-07-06

Status: planned.

## Purpose

RF11 should turn EquineSync location, property, arena, stall-card, and community
help surfaces into truthful, permissioned models. The goal is to avoid
role-inferred sharing, text-only location truth, and overclaimed map/help
behavior.

## Entry Conditions

- RF10 is Codex-reviewed and locked.
- RF1 tenant and owner-safe data fences remain locked.
- RF4 feature-certification boundaries remain locked.
- RF6 canonical-system decisions remain locked.
- RF7 owner/guardian privacy boundaries remain locked.
- BN18D limited field-recovery posture remains locked: no full offline or
  native-store claims.

## Strict Scope

RF11 may:

- inventory current property, barn location, arena share, stall card, QR,
  owner-access, map, and community-help surfaces;
- define a canonical property/location/share-state model where existing source
  supports safe implementation;
- add backend-authoritative publish/share-state checks for property/location
  reads if narrowly scoped and tested;
- make stall-card and map claims truthful if QR generation or map behavior is
  not implemented;
- record founder-decision rows for public/private location visibility,
  emergency-help access, and owner/rider map permissions;
- produce focused tests, evidence report, and review package.

RF11 must not:

- call live maps, geocoding, Apple, Google, provider, Vercel, Render, Atlas,
  DocuSign, Resend, Stripe, or UAT-account systems;
- implement native/offline behavior;
- claim true QR encoding, live mapping, route navigation, dispatch, emergency
  response, or public community networking unless proven;
- expose private barn, owner, guardian/minor, staff-only, trailer, or home-land
  details without explicit publish/share state;
- mark founder decisions accepted automatically.

## Target Workstreams

| Workstream | Goal | Evidence Required |
| --- | --- | --- |
| Surface inventory | Map existing property/location/map/stall-card/help surfaces. | Source scan with file and route references. |
| Canonical location model | Choose canonical fields for home/current horse location, barn areas, arenas, stalls, and temporary movement. | Model notes and deferred rows for fields not implemented. |
| Publish/share state | Replace role-inferred access with explicit share state where possible. | Backend tests for public, owner, rider, provider, and staff-denied cases. |
| Movement audit | Ensure horse location changes are auditable or deferred honestly. | Source evidence or future-phase row. |
| Stall-card/QR truth | Keep identification/readiness claims truthful if true QR generation is absent. | Claim-boundary table and tests if behavior changes. |
| Community help boundary | Define whether help requests are internal barn, owner/rider visible, or public/community visible. | Founder-decision rows and no live-dispatch claims. |

## Acceptance Criteria

- RF11 report status is `ready` with zero blocker rows.
- No private location or emergency/help details leak across barns, owners,
  riders, providers, staff, or public routes.
- Any map, QR, public sharing, emergency-help, dispatch, route navigation,
  live-geocoding, or offline/native behavior not implemented is explicitly
  deferred with the owning future phase.
- Launch claims distinguish between location records, printable/stall-card
  identification, and true QR/map functionality.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Decide default property/location privacy posture. | requires founder review | Recommended default: private until explicitly published/shared. |
| Decide owner/rider map visibility. | requires founder review | Owners/riders should see only explicitly shared current/home location context. |
| Decide community-help audience. | requires founder review | Choose internal barn-only, linked owner/rider, service-provider, or broader community behavior before implementation. |
| Decide QR/stall-card claim level. | requires founder review | Current posture should remain stall-card/readiness unless true QR encoding is implemented and tested. |

## Recommended Verification

- Focused RF11 backend tests for publish/share-state access and denied reads.
- RF11 report generation with `--fail-on-blockers`.
- Frontend build if location/map/help UI is touched.
- Zip integrity and expected manifest check.
- `git diff --check`.
- Secret-shape scan.
