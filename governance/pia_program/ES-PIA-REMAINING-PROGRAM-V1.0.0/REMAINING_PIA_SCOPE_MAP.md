# Remaining PIA Scope Map

**Status:** `TEN_ITEM_PORTFOLIO_PRESERVED_ITEM04_DOCUMENTARY_DESIGN_INTEGRATED`
**Authority:** `ES-PIA-PORTFOLIO-LOCK-V1.0.0`
**Implementation authority:** `FALSE`

The assessment directive names many product domains, but it expressly says that list is not a predetermined conclusion. The controlling Founder-directed portfolio contains ten PIAs and prohibits an eleventh without a separate Founder decision. This map consolidates the assessed domains while keeping identity, role, relationship, permission, and authority distinct.

| Position | PIA | Owned scope | Mandatory inbound boundaries | Key embedded assessment domains |
| ---: | --- | --- | --- | --- |
| 01 | Identity, Account, Actor, and Onboarding | Identity and enrollment truth | Privacy, safeguarding, records, audit | Identity; account; actor; onboarding; adaptive entity initiation |
| 02 | Facility, Tenant, and Organizational Structure | Operating context, topology, asset, and location identity | Identity, relationship, permission | Facility; tenant; organization; areas; location identity; asset identity |
| 03 | Relationship, Authorization, and Permission | Relationship truth, delegated authority, authorization inputs, permission evaluation | Identity and context | Relationships; permissions; consent/authorization boundary; restrictions; claims/disputes authority; provider relationship |
| 04 | Horse Identity, Profile, and Lifecycle | Founder-approved documentary canonical horse identity, profile, Passport, lifecycle, custody, duplicate, transfer, and continuity boundaries | Identity, context, authority, care, schedule, finance, privacy, audit | Horse identity; profile; lifecycle; passport; custody; transfer and continuity |
| 05 | Core Navigation, Search, and Application Shell | Shared experience and discovery | All domain truth and permission filtering | Navigation; search; shared reporting surface; platform administration |
| 06 | Task, Calendar, Scheduling, and Notification | Work, service-request state, scheduling, and time coordination | Context, authority, horse, communication delivery | Tasks; calendar; scheduling; service requests; assignments; work orders; reminders; notification triggers |
| 07 | Care Operations | Daily and safety-sensitive care execution | Horse, facility, authority, scheduling | Care; health support; medication records; feed; turnout; stall use; asset use/observations; staff/groom workflows; provider care coordination |
| 08 | Lessons, Training, Rider, and Guardian | Participation, competition/show/travel, and safeguarding-sensitive workflows | Identity, guardian/relationship authority, horse, scheduling, care | Lessons; training; rider/participant; guardian; competition; show; travel |
| 09 | Billing, Payments, and Financial Operations | Financial workflow and evidence | Identity, authority, agreements, claims, audit | Billing; invoicing; payments; refunds; provider/vendor obligations and payouts; reconciliation; financial exports |
| 10 | Owner Portal and Communications | Owner/provider-facing participation and communications | All domain truth and authority | Owner/provider portal surfaces; messages; notices; acknowledgments; delivery evidence; media |

## Item 04 Current Documentary Boundary

Item 04 V0.3 is now a Founder-approved documentary design baseline only. V0.1, V0.2, and V0.3 are preserved separately; the V0.3 artifact bytes are unchanged; `HOR-FD-001` through `HOR-FD-017` are approved documentary-only. Formal review, adoption, ratification, implementation, schema, migration, deployment, production use, external activation, and enrollment remain unauthorized.

## Cross-PIA controls that are not standalone PIAs

- mobile and offline behavior;
- privacy and data protection;
- audit, evidence, record stewardship, retention, correction, and export;
- AI and automation boundaries;
- external integrations and provider neutrality;
- configuration and feature management;
- platform operations, resilience, support, and recovery;
- reporting and analytics truth contracts; and
- security, abuse, safeguarding, consent, and incident controls.

Each PIA must instantiate these controls for its own actors, entities, workflows, failures, and acceptance criteria. A global canon does not substitute for domain-specific treatment.

## Founder-approved documentary ownership allocations

The following allocations are approved only as documentary design under the 2026-07-22 Founder approval record:

1. Item 08 owns competition/show/travel workflow truth; Item 04 horse lifecycle and eligibility; Item 06 scheduling/time; Item 09 fees, refunds, and financial consequences.
2. Item 02 owns asset/location identity; Item 07 care use and operational/safety observations; Item 06 service-request scheduling, assignment, and state; Item 09 charges and vendor obligations.
3. Item 03 owns provider relationship, representation, delegation, and authority; Item 07 care coordination; Item 10 participation/portal surfaces; Item 09 fees, obligations, payments, and payouts.
4. No Item 11 Reporting PIA exists. Domain PIAs own canonical truth and metric definitions; Item 05 owns shared reporting presentation, discovery, filtering, and administration without becoming a competing system of record.

All five decision statuses are `FOUNDER_APPROVED_DOCUMENTARY_DESIGN_ONLY`. These allocations do not authorize implementation, migration, deployment, activation, production use, enrollment, review completion, adoption, ratification, or lock.
