# Owner Portal and Communications Data-Flow and Trust-Boundary Model

Status: `DOCUMENTARY_DESIGN_CANDIDATE`

## Boundary 1: Client to EquineSync edge

The web or mobile client authenticates through the Identity boundary. Requests include the active tenant/facility context and purpose. The client is never trusted as the source of relationship, permission, delivery, acknowledgment, or moderation truth.

## Boundary 2: Portal projection gateway to source domains

The projection gateway requests only fields allowed by the approved cross-PIA contracts. Source domains return versioned, provenance-bearing projections. The gateway applies action-time authorization and displays staleness and correction routes.

## Boundary 3: Communications core to delivery adapters

The communications core owns the communication, audience snapshot, delivery case, attempt, and acknowledgment records. Replaceable provider adapters execute channel delivery. Provider responses are evidence inputs and do not independently change authoritative communication meaning.

## Boundary 4: Community messaging to relationship and facility truth

Discovery and send require current facility enablement, individual participation, current same-facility owner eligibility, no block or restriction, and current authorization. Each-send revalidation protects against stale membership and facility changes.

## Boundary 5: Media pipeline

Attachments enter a quarantine and validation boundary. Type, size, malware, sensitivity, metadata, consent, and destination controls run before access. Signed or bounded access references enforce current authorization.

## Boundary 6: Moderation and support

Support mode and moderation cases are separate privileged contexts. Access is case-based, purpose-limited, least-privilege, attributable, time-bounded where feasible, and fully audited. Customer authorship is never impersonated.

## Boundary 7: Offline client

Approved content may be cached with clear staleness state. Offline composition remains a draft. Reconnect crosses an authorization boundary and must reauthenticate, reauthorize, revalidate relationship/community state, resolve conflicts, and prevent duplicates.

## Boundary 8: Audit and evidence custody

Material actions emit attributable evidence with actor, principal, facility, horse or conversation context, reason, outcome, source/policy version, time, and correlation reference. Logs and evidence must not unnecessarily contain message content, secrets, protected case data, or provider tokens.

## Fail-closed principles

- Uncertain authority or field disclosure: deny or withhold.
- Stale critical relationship or restriction facts: deny pending refresh.
- Uncertain provider delivery: expose uncertainty, not success.
- Unscanned or quarantined media: deny access.
- Offline queued action after block/revocation: do not send.
- Missing operational staffing or kill-switch readiness: do not activate community.
