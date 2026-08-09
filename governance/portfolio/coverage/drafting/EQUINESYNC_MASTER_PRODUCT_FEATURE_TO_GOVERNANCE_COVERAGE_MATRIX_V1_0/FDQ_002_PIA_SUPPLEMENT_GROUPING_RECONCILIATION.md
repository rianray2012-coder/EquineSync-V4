# FDQ-002 PIA Supplement Grouping Reconciliation

**Decision question:** `FDQ-002` — PIA supplement grouping  
**Prior question:** Are the proposed fourteen PIA supplements the correct grouping for the 179 supplement-candidate rows?  
**Prior ripeness:** `PREREQUISITE_CORRECTION_REQUIRED`  
**Disposition:** `SUPERSEDED_AND_NARROWED`  
**Source-identity prerequisite:** `RESOLVED_FOR_GROUPING_REVIEW`  
**Bulk fourteen-supplement proposal:** `NOT_APPROVED_AS_A_CONTROLLING_ARCHITECTURE`  
**Founder bulk grouping decision required:** `NO`  
**Pilot effect:** `NOT_INDEPENDENTLY_BLOCKING`  
**Follow-on:** `NARROW_SCOPE_ONLY_WHERE_RECONCILIATION_IDENTIFIES_A_REAL_GAP`

## 1. Why the prior prerequisite no longer controls

The Matrix's supplement proposal was built while parent PIA source states were reported as `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` or successor text pending. Later primary-source reconciliation established a Founder-approved ten-PIA documentary baseline and recovered the previously missing Item 02 and Item 03 artifacts. The old parent-source status therefore cannot be used as the present reason to block supplement grouping review.

The original `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv` is preserved as historical evidence. Its fourteen proposed supplement groups are not deleted or rewritten to imply they were authoritative.

## 2. Reconciliation method

Each proposed supplement group was tested against:

1. the current Founder-approved parent PIA's stated scope and canonical ownership;
2. cross-PIA ownership and source-reference rules;
3. existing Founder decisions already governing ambiguous allocation;
4. constitutional/cross-domain governance where the subject is not properly owned by one PIA; and
5. whether a bounded residual workflow remains that is not adequately resolved by the existing parent baseline.

A group was then classified as one of:

- `EXISTING_PIA_ALREADY_COVERS`
- `EXISTING_PIA_COVERS_WITH_RETAINED_BOUNDARY_DECISION`
- `EXISTING_FOUNDER_SCOPE_DECISION_CONTROLS`
- `NON_PIA_CROSS_DOMAIN_CONTROL`
- `GENUINE_NARROWED_SUPPLEMENT_CANDIDATE`

## 3. Result

The fourteen-group proposal does not survive as a valid bulk supplement architecture.

- `10` proposed groups are already substantially owned by an existing Founder-approved PIA and do not presently justify a separate supplement solely because the Matrix marked feature rows `PIA_SUPPLEMENT_CANDIDATE`.
- `2` proposed groups are cross-domain control families rather than proper PIA supplements: Documents/Signatures and Media/Files.
- `1` proposed group, Inventory/Assets, is governed by an already-existing Founder allocation question, `FAC-FD-029 / ES-PIA-GFD-002`, concerning asset identity, lifecycle, maintenance truth, work-order orchestration and care/safety interfaces across Items 02, 06 and 07.
- `1` proposed group survives as a genuine narrowed supplement candidate: `DOC-SUP-PIA-08-EVENTS-TRAVEL`, because show/event/travel workflow ownership is assigned primarily to Item 08 while depending on Item 04 horse truth, Item 06 scheduling/time coordination and Item 03 authority.

The companion `PIA_SUPPLEMENT_GROUP_RECONCILIATION_V1_0.csv` records the disposition of every proposed group.

## 4. Important ownership corrections

### Identity and relationship

The proposed Identity/Access and Relationship/Guardianship supplements substantially duplicate existing Item 01 and Item 03 responsibilities. Sessions, recovery, invitations, enrollment, memberships, support access, service accounts, closure, duplicate identity, relationship verification, effective periods, delegation, restrictions, revocation and disputes belong in those existing baselines and their implementation contracts.

### Facility, inventory and maintenance

A broad Facility Operations supplement is not needed merely to restate Item 02's domain. Inventory/assets/maintenance cannot be solved by drafting a supplement around the unresolved boundary. `FAC-FD-029 / ES-PIA-GFD-002` must control the allocation among Items 02, 06 and 07.

### Shell, task/calendar, care, lessons, finance and communications

The current parent PIAs already state substantial workflow ownership for the rows grouped beneath these proposed supplements. Later implementation mapping, cross-PIA interface freeze, Code Guide work or as-built verification may still be required, but those are different lifecycle needs and do not establish that a new PIA supplement is needed.

### Documents/signatures

Global document, agreement, consent, waiver and signature truth is cross-domain. Item 10 may deliver notices, display attachments or participate in signature-provider integrations, but it should not become the universal owner of agreement/legal-effect truth. Those controls remain with Agreement/Consent/Authorization governance, Item 03 authority, records/audit/media governance and the consuming domain PIA.

### Media/files

Media/files are likewise cross-domain. Item 10 owns portal and communication attachment behavior, not the universal file/media lifecycle. Storage objects, renditions, OCR/transcripts, consent, publication, retention, evidence and derived-asset controls belong to the Media/Files governance family and consuming domains.

### Shows/events/travel

This is the only proposed group that remains supplement-shaped after reconciliation. Item 08 already identifies show entry, travel, ride times and itinerary as its workflow responsibility, while Item 04 retains horse identity/eligibility truth and Item 06 retains calendar/time coordination. A bounded Item 08 supplement may therefore be appropriate if the existing Item 08 requirements do not contain sufficient detail for implementation planning. It is not approved by this reconciliation and remains subject to a separate scope disposition before drafting/adoption if required.

## 5. FDQ-002 disposition

The Founder should not be asked to approve or reject the fourteen groups as a single package. The premise is obsolete because it combines stale source-state assumptions, already-covered PIA domains, cross-domain governance, and one pre-existing allocation decision.

Accordingly:

`FDQ-002 = SUPERSEDED_AND_NARROWED`

`PARENT_PIA_SOURCE_IDENTITY_PREREQUISITE = RESOLVED_FOR_GROUPING_REVIEW`

`FOURTEEN_SUPPLEMENT_BULK_ARCHITECTURE = RETIRED_AS_NONCONTROLLING_WORKING_HYPOTHESIS`

`BULK_FOUNDER_DECISION_REQUIRED = NO`

`SURVIVING_NARROWED_SUPPLEMENT_CANDIDATE = DOC-SUP-PIA-08-EVENTS-TRAVEL`

`EXISTING_SCOPE_DECISION_PRESERVED = FAC-FD-029 / ES-PIA-GFD-002`

`PILOT_EFFECT = NOT_INDEPENDENTLY_BLOCKING`

## 6. Authority boundary

This reconciliation is documentary source and ownership analysis. It does not amend any PIA, approve a supplement, resolve `FAC-FD-029`, authorize implementation mapping, activate any Code Guide, authorize implementation, expand pilot scope, authorize production, or establish runtime verification.

If a pilot capability depends on a residual gap, that capability must be tested against the controlling parent PIA and current implementation evidence directly. The retired fourteen-group proposal may not be used as an independent reason to block or authorize the bounded pilot.
