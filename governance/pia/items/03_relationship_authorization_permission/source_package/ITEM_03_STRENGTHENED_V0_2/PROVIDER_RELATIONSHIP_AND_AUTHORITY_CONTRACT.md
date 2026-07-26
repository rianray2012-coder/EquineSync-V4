# Provider Relationship and Authority Contract

**Contract ID:** `RAP-CONTRACT-PROVIDER-001`
**Founder decision:** `ES-PIA-GFD-003`
**Status:** `FOUNDER_APPROVED_DOCUMENTARY_ALLOCATION_NOT_IMPLEMENTATION_AUTHORITY`

## Approved ownership allocation

- Item 03 owns provider relationship, representation, delegation, and authority.
- Item 07 owns provider care coordination and care-workflow truth.
- Item 10 owns provider participation, communication, and portal surfaces.
- Item 09 owns provider fees, obligations, payments, and payouts.

Item 01 retains canonical identity. Item 02 retains facility, tenant, organization, asset, and location identity. Item 04 retains horse identity and lifecycle. Item 06 retains service-request scheduling, assignment, and state.

## Non-authority invariants

Provider connection, profile creation, directory listing, credential verification, professional status, facility association, organization association, API credential, integration connection, appointment participation, schedule assignment, care interaction, contract upload, invoice, payment, payout, portal access, portal visibility, onboarding completion, contact information, shared address, possession, or invitation never independently creates relationship, representation, delegation, authorization, or permission.

## Required authority chain

A provider action requires canonical provider and accountable-human identity, a current relationship claim, applicable representation basis, any required accepted delegation, purpose and resource scope, tenant/context, owning-domain constraints, agreements and restrictions, current source and policy versions, and final permission evaluation. Provider organizations act only through attributable principals and actors.

Authority is bounded by action, subject, resource, field, purpose, tenant, time, state, and revocation watermark. A provider may not self-activate, self-expand, delegate beyond source authority, infer horse/person access from an appointment, or convert care/payment evidence into canonical authority.

## Cross-PIA handoffs

| From | To | Contract |
| --- | --- | --- |
| Item 01 | Item 03 | Stable provider and accountable-human principal identifiers with assurance and lifecycle state. |
| Item 02 | Item 03 | Facility/tenant/organization context and asset/location references that constrain but do not grant authority. |
| Item 03 | Item 07 | Minimum provider care-action projection, purpose, subject, restrictions, expiry, and watermark. |
| Item 03 | Item 10 | Minimum participation/portal projection and safe denial/visibility rules. |
| Item 07 | Item 09 | Attributable service evidence; it does not create an obligation without Item 09 agreement/financial rules. |
| Item 09 | Item 03 | Financial status may restrict a separately authorized workflow only under an approved policy; it cannot create authority. |
| Item 06 | Items 03/07/10 | Schedule and assignment state used as context, never as authority. |

## Revocation, dispute, and correction

Revocation, restriction, relationship end, representation loss, delegation expiry, dispute hold, identity invalidation, or tenant-context change invalidates affected provider projections and pending offline proposals. Correction creates a successor, preserves prior evidence, and triggers re-evaluation; it does not rewrite history.

## Evidence

Every provider authority change records accountable human, principal chain, source basis and versions, scope, restrictions, decision, notice, time, correlation, and correction/supersession. Provider adapters and portal surfaces consume bounded projections and may not become a source of canonical authority.

## Limitation

GFD-003 is incorporated as documentary design only. No provider, model, integration, API, portal, payment rail, runtime, or production capability is created or activated.
