# BN14B Roadmap Permission Matrix

Purpose: planning artifact for BN15 and later roadmap phases. This file records
expected role/action boundaries before new UI is exposed. It does not change
runtime permissions.

Roles:

- `platform_admin`: platform-level admin users with valid `platform_role`.
- `facility_admin`: barn-scoped `role="admin"`.
- `barn_owner`: founder/owner profile for a facility.
- `barn_manager`: barn operations manager.
- `trainer`: trainer role.
- `staff`: groom / working student / staff-role daily worker.
- `horse_owner`: barn-associated or individual horse owner.
- `guardian`: parent / guardian of minor rider.
- `rider`: lesson participant.

Legend:

- `R`: read.
- `C`: create.
- `U`: update.
- `A`: approve / publish / resolve.
- `E`: export.
- `O`: own records only.
- `Safe`: backend-projected owner-safe payload only.
- `No`: no access.

| Roadmap surface | Platform admin | Facility admin | Barn owner | Barn manager | Trainer | Staff | Horse owner | Guardian | Rider |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Today's Pulse | R cross-facility summary only | R barn | R barn/business | R barn ops | R assigned/program | R assigned work | R Safe own horse | R Safe linked rider | R Safe own rider profile |
| Changed Since Last Login | R cross-facility summary only | R barn | R barn/business | R barn ops | R assigned/program | R assigned work | R Safe own horse | R Safe linked rider | R Safe own rider profile |
| Horse Watchlist | R platform summary | R/C/U barn | R barn | R/C/U barn ops | R/C/U assigned horses | R assigned, U limited completion notes only | R Safe own horse if visible | R Safe linked rider/horse if visible | R Safe if explicitly visible |
| Horse Timeline | R platform summary | R barn | R barn | R/C barn ops events | R/C training events for assigned horses | R/C task/check events assigned only | R Safe own horse | R Safe linked rider/horse | R Safe own rider events |
| Staff checks / body checks | No raw staff payload | R/A barn | R business summary | R/C/U/A | R/C assigned horses | R/C assigned tasks | R Safe result only | R Safe if linked and approved | R Safe if approved |
| Medication safeguards | No raw staff payload | R/A barn | R business summary | R/C/U/A | R assigned if allowed | R/C assigned only | R Safe status only | R Safe if approved | No raw access |
| Facility tickets / hazards | R cross-facility summary only | R/C/U/A barn | R/C/U/A barn | R/C/U/A ops | R/C assigned/program areas | R/C assigned or observed hazards | C owner-visible request only, R Safe status | C guardian-visible request only, R Safe status | No unless explicitly exposed |
| Client onboarding / gear / tack | R summary only | R/C/U barn | R/C/U barn | R/C/U ops | R assigned training gear | R assigned care gear | R/C/U own items if enabled | R/C/U linked rider items if enabled | R own rider items if enabled |
| Trainer recommendations | R summary only | R/A barn | R/A business | R/A ops | R/C/U assigned | No unless assigned support | R/A own shopping list items | R/A linked rider items | R own recommendations if approved |
| Owner updates / media controls | R metadata only | R/C/U/A barn | R/A business | R/C/U/A | R/C/U/A assigned | No raw owner comms by default | R Safe own updates, prefs | R Safe linked rider updates, prefs | R Safe own rider updates |
| Incidents | R metadata only | R/C/U/A barn | R/A business | R/C/U/A | R/C assigned/program | R/C witnessed/assigned | R Safe if approved | R Safe if linked and approved | No raw access |
| Documents / signatures | R metadata only | R/C/U/A barn | R/A business | R/C/U/A ops | R/C assigned templates if allowed | No unless assigned | R/C own required docs | R/C linked minor docs | R own docs if adult/allowed |
| Billing approvals / add-ons | R platform billing summary | R/C/U/A barn billing | R/C/U/A business | R request only unless granted | R request only if enabled | No | R own charges/subscription | R linked rider billing if payer | No unless payer |
| Scheduling / conflicts | R summary only | R/C/U/A barn | R/C/U/A barn | R/C/U/A ops | R/C/U assigned lessons/blocks | R assigned shifts/tasks | R Safe barn/horse schedule | R Safe linked rider schedule | R Safe own lesson schedule |
| Reports | R/E platform reports | R/E barn reports | R/E business reports | R ops reports | R program reports | R own work summaries | R Safe own history | R Safe linked rider | R Safe own rider history |
| Search | R platform-scoped, scrubbed | R barn-scoped | R barn/business | R barn ops | R assigned/program | R assigned work | R Safe own | R Safe linked | R Safe own |
| Text/SMS notifications | Configure platform defaults only | Configure barn defaults only | Configure business defaults only | Configure staff ops defaults only | Configure program defaults only | Opt-in own delivery | Opt-in own delivery | Opt-in linked delivery | Opt-in own delivery |

## SMS/Text Notification Placement

Text/SMS notification options belong in roadmap Phase 12 - Platform Maturity,
inside Smart Notifications and Quiet Hours.

Required decisions before implementation:

- SMS provider.
- Phone verification flow.
- Explicit opt-in and unsubscribe language.
- Quiet hours by role and timezone.
- Emergency override rules.
- Rate limits and retry policy.
- Audit-safe delivery metadata.
- Minor/guardian delivery rules.

Do not add SMS/Text controls in BN14B or BN15A.

## BN15A Permission Focus

BN15A should use this matrix only to define Today's Pulse response shapes. It
should avoid broad write permissions until Watchlist, Timeline, and Changed
Since Last Login each receive their own gated implementation phase.

