# Golden Paths

## 31. Golden Paths

| Golden Path ID | Golden Path |
| --- | --- |
| TCSN-GP-001 | Create, assign, accept, complete, and audit a routine barn task. |
| TCSN-GP-002 | Create a recurring medication-support schedule from an authorized source, complete one occurrence offline, synchronize, and preserve evidence. |
| TCSN-GP-003 | Book a horse, trainer, and arena event with conflict detection and approved reminders. |
| TCSN-GP-004 | Import an external calendar event, classify it correctly, and avoid creating unauthorized operational truth. |
| TCSN-GP-005 | Trigger a missed welfare-sensitive task escalation, reassign to substitute coverage, and close the escalation with evidence. |
| TCSN-GP-006 | Send routine notifications through digest while sending an urgent override separately. |
| TCSN-GP-007 | Deliver an optional SMS to a verified permitted number, process delivery status, and reconcile fallback after failure. |
| TCSN-GP-008 | Disable external calendar synchronization by feature flag and preserve recoverable state, audit, and support visibility. |

Each golden path requires reproducible fixtures, expected results, evidence capture, and environment identity before it may support a verification claim.


### 31.1 Strengthened golden paths

| Golden Path ID | Golden Path |
| --- | --- |
| TCSN-GP-009 | Detect an external provider outage, continue native task operation, surface degradation, disable the adapter, recover, reconcile, and preserve evidence. |
| TCSN-GP-010 | Rehearse the controlled first-user workflow from invitation and configuration through one routine task, one scheduled event, one offline completion, one failed notification recovery, support contact, rollback check, and Founder readiness determination. |

---

## 32. Adversarial and Negative Scenarios

| Scenario ID | Scenario |
| --- | --- |
| TCSN-ADV-001 | A user attempts to complete a task by merely opening its notification. |
| TCSN-ADV-002 | An unauthorized actor assigns a medical task. |
| TCSN-ADV-003 | A delegate attempts to access unrelated medical or billing records. |
| TCSN-ADV-004 | A user backdates completion after escalation and tries to erase lateness. |
| TCSN-ADV-005 | A recurring-series edit attempts to rewrite completed history. |
| TCSN-ADV-006 | An external calendar deletes an EquineSync-created event. |
| TCSN-ADV-007 | A duplicate external webhook tries to create duplicate events. |
| TCSN-ADV-008 | A hard horse/resource conflict is hidden by UI-only logic. |
| TCSN-ADV-009 | Unknown provider availability is represented as free. |
| TCSN-ADV-010 | A device timezone change shifts a medication-support schedule. |
| TCSN-ADV-011 | A DST transition creates two occurrences or none without disclosure. |
| TCSN-ADV-012 | Routine quiet hours suppress an emergency notice. |
| TCSN-ADV-013 | An urgent notice is collapsed into a digest. |
| TCSN-ADV-014 | A failed SMS is treated as recipient refusal. |
| TCSN-ADV-015 | An unverified phone number receives sensitive SMS content. |
| TCSN-ADV-016 | A user opts out of optional SMS and the platform disables a mandatory in-app notice. |
| TCSN-ADV-017 | A provider spoof sends a false delivery webhook. |
| TCSN-ADV-018 | Retry logic creates a notification storm. |
| TCSN-ADV-019 | Escalation continues after cancellation and creates false alarms. |
| TCSN-ADV-020 | Escalation stops after acknowledgment even though the task remains incomplete. |
| TCSN-ADV-021 | A generated task loses its source record after source deletion. |
| TCSN-ADV-022 | An AI assistant silently assigns a high-risk task. |
| TCSN-ADV-023 | A user disables a mandatory welfare reminder. |
| TCSN-ADV-024 | Two devices complete the same task offline with conflicting evidence. |
| TCSN-ADV-025 | Revoked staff access remains active offline indefinitely. |
| TCSN-ADV-026 | A cross-tenant calendar query leaks another facility's events. |
| TCSN-ADV-027 | Support edits a completion without preserving the original. |
| TCSN-ADV-028 | A feature-flag rollback strands synchronization tokens or queued jobs. |
| TCSN-ADV-029 | A failed adapter silently reports healthy status. |
| TCSN-ADV-030 | A user interprets an imported event as an authoritative care instruction. |
| TCSN-ADV-031 | A task assignment is used to imply employment or professional authority. |
| TCSN-ADV-032 | A documentary draft is represented as production or enrollment approval. |


### 32.1 Strengthened adversarial additions

| Scenario ID | Scenario |
| --- | --- |
| TCSN-ADV-033 | A user creates a circular chain of blocking tasks to deadlock operations. |
| TCSN-ADV-034 | A bulk action attempts to bypass one horse or facility permission check. |
| TCSN-ADV-035 | An availability response leaks a minor, horse, location, or sensitive event title. |
| TCSN-ADV-036 | An RSVP is misused as consent, assignment acceptance, or payment authority. |
| TCSN-ADV-037 | A stale notification template sends superseded instructions. |
| TCSN-ADV-038 | A user opts out of SMS and the system suppresses all mandatory communication. |
| TCSN-ADV-039 | A loop creates uncontrolled SMS spend or recipient harassment. |
| TCSN-ADV-040 | A provider outage is represented as native success or silently drops queued work. |
| TCSN-ADV-041 | An administrator replays a dead-letter item after the underlying task was canceled. |
| TCSN-ADV-042 | A restore recovers tasks but loses linked completion, recurrence, or notification evidence. |
| TCSN-ADV-043 | Disabling a feature flag strands provider tokens, scheduled jobs, or unsent mandatory notices. |
| TCSN-ADV-044 | Synthetic seed records appear in production search, reports, notifications, or billing context. |
| TCSN-ADV-045 | Migration maps two legacy schedules into duplicate authoritative occurrences. |

---

## 33. Operational Readiness, Monitoring, and Support

### 33.1 Ownership

| Function | Interim owner | Required before operational activation |
|---|---|---|
| Product and approval | Rian Ray | Remains Founder authority unless delegated |
| Operational owner | Rian Ray until separately assigned | Named backup and on-call coverage |
| Support owner | Rian Ray until separately assigned | Support queue, response targets, and escalation path active |
| Engineering owner | Unassigned until implementation authorization | Named service owner for each work package |
| Security and incident owner | Unassigned | Named incident commander and backup |
| Evidence custodian | EquineSync Implementation Governance Function | Controlled evidence location and retention |
| Provider owner | Unassigned per adapter | Credential, spend, terms, outage, and exit accountability |

### 33.2 Required monitoring

Monitoring must cover native request success, latency, queue age, failed jobs, notification outcomes, SMS volume and spend, provider webhooks, calendar sync lag, duplicate suppression, conflict overrides, offline backlog, reconciliation cases, permission denials, cross-tenant anomalies, backup freshness, restore status, feature-flag state, and support correction.

### 33.3 Alert classes

| Severity | Example trigger | Acknowledgment target | Required response |
|---|---|---|---|
| `P0` | Cross-tenant disclosure, unauthorized safety-critical completion, corrupted authoritative timing, uncontrolled broad notification | 15 minutes | Contain, stop affected writes or sends, preserve evidence, notify Founder, begin incident process |
| `P1` | Broad urgent-delivery failure, persistent sync corruption, inability to revoke provider, restore failure | 30 minutes | Disable affected adapter or feature, enter degraded mode, communicate impact, reconcile |
| `P2` | Localized provider degradation, elevated retries, isolated reconciliation backlog | 4 business hours | Investigate, repair, monitor, record finding |
| `P3` | Cosmetic, low-impact, or documentation issue | Next planned maintenance | Track and correct |

### 33.4 Support workflows

Support must be able to:

1. identify the tenant, actor, task, event, notification, adapter, and correlation record;
2. inspect state without broad unrestricted content access;
3. explain whether a record is authoritative, projected, pending, failed, or reconciled;
4. correct permitted errors without deleting history;
5. reassign or cancel only with current authority;
6. replay only when idempotency and current-state checks pass;
7. revoke a destination or provider connection;
8. export a bounded evidence package;
9. escalate safety, safeguarding, privacy, security, or legal concerns; and
10. record the support action and outcome.

### 33.5 Recovery and continuity

The first-user operational design uses a 15-minute recovery-point target and a 4-hour recovery-time target for authoritative Item 06 records. Native tasks and in-app status must remain available when an external calendar or optional SMS provider is disabled, subject to platform-wide availability. Restore rehearsals must validate relational integrity, recurrence generation, deduplication state, queued work, notification evidence, and audit history.

### 33.6 Runbooks required

- native service degradation;
- urgent notification failure;
- SMS cost or abuse spike;
- calendar provider outage;
- webhook spoof or replay;
- queue backlog;
- duplicate occurrence or send;
- offline reconciliation conflict;
- cross-tenant or permission incident;
- lost or stolen device;
- provider credential revocation;
- backup and restore;
- release rollback;
- feature-flag emergency disablement;
- support correction and evidence export.

### 33.7 Stop conditions

Rollout or operation must stop for cross-tenant disclosure, inability to enforce authority, silent loss of completion evidence, duplicate consequential actions, uncontrolled notification volume, mandatory-notice suppression, time-zone corruption, unsafe offline access, unrecoverable adapter drift, inability to revoke provider credentials, failed backup or restore, or materially misleading health status.

### 33.8 Operational evidence state

This section fully defines the operational design and evidence required to answer Mandatory Question 4. No monitoring, alert, backup, restore, rollback, support, or incident evidence has yet been executed. The Operational-Readiness Gate therefore remains closed even though the PIA question is answered `YES_WITH_EVIDENCE` at the documentary-design level.

---

## 34. Deployment, Rollout, Rollback, Environment, and Configuration

### 34.1 Environment matrix

| Environment | Purpose | Permitted data | Provider posture | Restrictions |
|---|---|---|---|---|
| Local | Developer implementation | Synthetic only | Mocks or approved sandbox | No production credentials |
| Test | Automated integration and contract tests | Synthetic fixtures | Sandbox | Resettable and isolated |
| Staging | Release-candidate and operational rehearsal | Synthetic or approved de-identified data | Sandbox or isolated preproduction | No customer operation |
| Founder pilot | Controlled first-user candidate | Approved founder-controlled data after enrollment authorization | Production providers with bounded credentials | Cohort and feature limits |
| Production | General authorized use | Authorized live data | Production providers | Separate release disposition required |

### 34.2 Configuration

The following are versioned configuration, not hidden code constants: risk classes, grace periods, operational hours, digest windows, quiet hours, escalation chains, channel eligibility, SMS spend caps, recurrence limits, conflict rules, travel buffers, retry schedules, retention classes, provider endpoints, locale mappings, and feature scope.

Every material configuration change requires actor, authority, prior value, new value, reason, effective time, affected scope, validation, audit, rollback, and review date.

### 34.3 Feature flags

At minimum, separate flags must govern external calendar connection, bidirectional Google sync, Microsoft sync, ICS export, optional SMS, urgent SMS override eligibility, bulk operations, advanced conflict rules, and AI schedule suggestions. Provider-connected flags default off in production. Flags cannot bypass permissions, safeguarding, audit, retention, or evidence.

### 34.4 Secrets

Provider credentials, webhook secrets, signing keys, device tokens, telephone verification secrets, and adapter refresh tokens must use approved secret storage, rotation, scoped access, nonlogging, revocation, and incident procedures. No secret may be embedded in client code, PIA files, screenshots, test fixtures, analytics, or general evidence exports.

### 34.5 Migration, seed data, and reconciliation

No migration is authorized by this PIA. Any future migration must inventory legacy tasks, events, recurrence rules, completion history, recipients, destinations, and external identifiers; preserve source and effective time; dry-run deterministically; quarantine ambiguity; prevent duplicates; validate downstream references; support rollback; and produce reconciliation reports.

Seed data must be synthetic or expressly approved, environment-isolated, visibly marked, excluded from real notifications and external sync, and removable without affecting authoritative data.

### 34.6 Rollout

The first-user release is invite-only, founder-controlled, and limited to one facility and three to five primary workflows. Native task and calendar operation precedes adapter expansion. Optional SMS and Google synchronization are independently activated only after their evidence subsets pass. Microsoft and advanced Apple integration remain staged.

### 34.7 Rollback

Rollback must support immediate provider and feature disablement, restoration of the prior application release, queue pause, safe job drainage, credential revocation, recurrence-generation freeze, and post-rollback reconciliation. Accepted user actions and audit evidence must be preserved. Non-reversible data limitations must be disclosed before rollout.

### 34.8 Post-deployment verification

Each deployment must verify configuration, feature flags, secret references, native task creation and completion, one-time and recurring events, notification routing, optional SMS if active, adapter health if active, permission denial, offline queue, monitoring, alerts, backup freshness, support access, and rollback readiness.

---

## 35. Engineering Work Packages

Proposed work packages:

1. `TCSN-EWP-001` Domain entities and persistence.
2. `TCSN-EWP-002` Task assignment, delegation, completion, and evidence.
3. `TCSN-EWP-003` Calendar event, recurrence, occurrence, and time-zone engine.
4. `TCSN-EWP-004` Conflict and resource engine.
5. `TCSN-EWP-005` Notification routing and state machine.
6. `TCSN-EWP-006` Optional SMS adapter and controls.
7. `TCSN-EWP-007` Escalation engine.
8. `TCSN-EWP-008` Offline queue and reconciliation.
9. `TCSN-EWP-009` External calendar adapters and sync health.
10. `TCSN-EWP-010` Administrative, support, observability, and evidence tools.
11. `TCSN-EWP-011` Accessibility and field UX.
12. `TCSN-EWP-012` Test fixtures, adversarial harness, and release evidence.

No work package is authorized by this draft.

---

## 36. Dependencies and Critical Path

### 36.1 Material dependencies

- Identity and Account PIA;
- Relationships and Delegated Authority PIA;
- Permission and Access-Control PIA;
- Facility and Organizational Structure PIA;
- Horse Identity and Lifecycle PIA;
- Care Operations and Health PIAs;
- Lessons and Shows PIAs;
- Communication and Notice implementation contracts;
- External Adapter implementation contracts;
- Offline and resilience standards;
- provider selection ADRs;
- SMS legal, consent, cost, and destination controls;
- exact source registration and MIAP linkage.

### 36.2 Critical path

`Source registration → cross-PIA ownership contracts → data and state models → permissions → recurrence/time engine → task engine → notification and escalation engine → offline reconciliation → adapters → admin/support → test evidence → operational readiness → Founder enrollment decision`

---

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

### 37.1 Founder decisions

All twenty identified Founder decisions are resolved for documentary drafting.

| Decision | Status | Approved direction |
|---|---|---|
| `TCSN-FD-001` through `TCSN-FD-009` | Approved | Recommended answers adopted |
| `TCSN-FD-010` | Approved with modification | Optional SMS added to initial controlled scope |
| `TCSN-FD-011` through `TCSN-FD-020` | Approved | Recommended answers adopted |

### 37.2 Assumptions

- Exact provider choices remain unresolved.
- Native EquineSync records remain available even when adapters are disabled.
- SMS is optional and not the sole channel for ordinary operation.
- First-user enrollment will use a controlled cohort.
- Exact numeric service levels will be established before implementation authorization or release as applicable.

### 37.3 Findings

#### Closed by V0.2 documentary revision

- `TCSN-P1-001`: Source and inheritance posture was family-only. Closed through Section 4 source IDs, authority qualification, immutable baseline references, and freeze re-verification rule.
- `TCSN-P1-002`: Cross-domain ownership was insufficiently testable. Closed through shared-control, business-rule, entity, workflow, permission, and traceability additions.
- `TCSN-P1-003`: Provider selection risk was framed as an open product decision. Closed by provider-neutral contracts, mandatory selection controls, default-off flags, and separate activation gates. Exact provider procurement remains an implementation ADR, not an unresolved product decision.
- `TCSN-P1-004`: Numeric operational and quality targets were absent. Closed through Section 3 success measures and Sections 33 and 34 operating targets.
- `TCSN-P1-005`: Evidence and backward traceability were incomplete. Closed at the documentary-design level through Sections 20, 30, 40, and the companion validation report.
- `TCSN-P1-006`: The five questions were not fully answered. Closed through Section 41's evidence-based answers and separate downstream gate determinations.

#### Future execution conditions, not as-designed defects

- No as-built implementation exists.
- No test, operational, or enrollment evidence has been executed.
- Fresh structured review, Founder design disposition, approved work packages, implementation, as-built reconciliation, verification, operational readiness, and enrollment disposition remain required.

### 37.4 Retained risks

- notification fatigue;
- missed urgent communications;
- false or duplicate escalation;
- time-zone and DST error;
- offline conflict;
- external-provider drift;
- SMS cost and deliverability;
- contact-destination error;
- cross-tenant disclosure;
- unauthorized delegation;
- imported-event confusion;
- support overreach.

### 37.5 Deviations

No deviation is authorized.

---

## 38. Implementation Drift and As-Built Reconciliation

No as-built implementation is asserted.

Future reconciliation must compare:

- entities and identifiers;
- task and event separation;
- recurrence behavior;
- time-zone behavior;
- assignment modes;
- permissions;
- notification states;
- optional SMS controls;
- escalation rules;
- offline reconciliation;
- external adapters;
- feature flags;
- admin tools;
- monitoring;
- deferred scope.

The PIA must not be weakened to make nonconforming code appear compliant.

---

## 39. Change-Control History

| Version | Date | Change | Authority |
|---|---|---|---|
| `0.1.0` | `2026-07-22` | Initial controlled documentary draft incorporating Founder-approved decisions `TCSN-FD-001` through `TCSN-FD-020`, including optional SMS in initial scope | Documentary drafting only |
| `0.2.0` | `2026-07-22` | Internal review cycle; source, business-rule, requirement, test, evidence, operations, migration, traceability, and five-question strengthening | Documentary revision only |

---

## 40. Requirement Traceability Matrix

### 40.1 Requirement-family mapping

| Requirement range | Primary sources | Workflows | Core entities | Permission focus | Acceptance | Tests | Evidence | Gate |
|---|---|---|---|---|---|---|---|---|
| `001-010` | `SRC-001`, `002`, `005`, `006`, `007` | All ownership workflows | Task, Event, Notification | Owner and source authority | `AC-001`, `002`, `040` | `TST-001`, `009`, `045` | `EV-DOC`, `EV-TRC` | Design and implementation authorization |
| `011-024` | `SRC-006`, `008`, `009`, `010`, `013` | Assignment, delegation, completion | Assignment, Delegation, Completion | Assign, accept, delegate, complete, correct | `AC-003-007`, `026`, `037` | `TST-002-005`, `033`, `042` | `EV-TST`, `EV-SEC` | Implementation authorization and verification |
| `025-048` | `SRC-005`, `014`, `016` | Recurrence, scheduling, sync, time | Event, Rule, Occurrence, Conflict | Edit, override, connect | `AC-008-016` | `TST-006-018` | `EV-CAL`, `EV-TST` | Verification |
| `049-064` | `SRC-007`, `011`, `018`, `019` | Notify, acknowledge, escalate | Notification, Attempt, Acknowledgment, Escalation | Send, override, inspect | `AC-017-025`, `036` | `TST-019-032`, `042` | `EV-NOT`, `EV-SEC` | Verification and operations |
| `065-080` | `SRC-002`, `015`, `016`, `017`, `020` | Automation, offline, release | Rule, OfflineMutation, FeatureFlag | Automate, reconcile, activate | `AC-027-040` | `TST-034-045` | `EV-OFF`, `EV-OPS` | Implementation, operations, enrollment |
| `081-090` | `SRC-005`, `006`, `008-010` | Dependencies, bulk, RSVP, availability | TaskLink, Invitation, Reservation | Bulk action and visibility | `AC-041-045` | `TST-046-051` | `EV-TST`, `EV-SEC` | Verification |
| `091-100` | `SRC-007`, `011`, `018`, `019` | Template, SMS, dedup, limits | TemplateVersion, Destination, SpendControl | Send, opt out, override | `AC-046-048` | `TST-052-056` | `EV-NOT` | Provider activation and operations |
| `101-110` | `SRC-013-017` | Monitor, support, restore, exit | Metric, Alert, Incident, Backup, ProviderExit | Admin and support | `AC-049-052` | `TST-057-062` | `EV-OPS` | Operational readiness |
| `111-120` | `SRC-002`, `012`, `013`, `015-017`, `021` | Evidence, release, migration | EvidenceItem, Manifest, MigrationRun | Evidence and release authority | `AC-053-055` | `TST-063-065` | `EV-DOC`, `EV-TRC`, `EV-ENR` | Implementation authorization and enrollment |

### 40.2 Forward and backward traceability rule

Every normative requirement has a stable ID and a source family, workflow, entity, permission, acceptance, test, evidence family, work-package family, and gate mapping. Companion machine-readable registers must expand the family mapping to one row per requirement before a frozen implementation-authority package is submitted.

### 40.3 Founder-decision mapping

- `FD-001-003`: domain scope, truth hierarchy, task-event distinction, mapped to `REQ-001-010`.
- `FD-004-007`: assignment, completion, backdating, recurrence, mapped to `REQ-011-030`.
- `FD-008-011`: escalation, quiet hours, channels including optional SMS, acknowledgment, mapped to `REQ-049-064` and `091-100`.
- `FD-012-015`: external sync, conflicts, offline, delegation, mapped to `REQ-031-048`, `071-075`, and `081-090`.
- `FD-016-020`: automation, fatigue, reminders, time zones, release boundary, mapped to `REQ-058-080` and `101-120`.

### 40.4 Traceability evidence

The V0.2 validation companion confirms section count, contiguous identifier ranges, permitted readiness answers, Founder-decision range, and authority prohibitions. Exact repository file paths and package checksums must be generated at freeze and do not permit content reinterpretation.

---

## 41. Five Mandatory Readiness Questions

The answers below evaluate whether the strengthened PIA provides a complete decision and evidence framework. They do not claim that software has been built, tested, deployed, or enrolled. Downstream gates remain separately controlled.

### 41.1 Engineering buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?

**Answer:** `YES_WITH_EVIDENCE`

**Evidence and explanation:**

- twenty Founder decisions are resolved and mapped;
- 120 normative requirements define product behavior and prohibitions;
- material business rules, workflows, state models, entity ownership, permissions, dependencies, configuration, migration, and release boundaries are explicit;
- provider choice is constrained through provider-neutral contracts, security, privacy, cost, evidence, exit, and default-off activation requirements rather than left as a product-policy invention;
- numeric first-release quality and operational targets are defined;
- no unresolved product decision is delegated to engineering.

**Supporting sections:** 3 through 17, 21 through 27, 34 through 40.

**Downstream gate determination:** Engineering may not begin until the Founder approves the design or implementation package, freezes the baseline, and authorizes bounded work packages. The answer is affirmative; the authority gate remains closed.

### 41.2 Objective QA verification

**Question:** Can quality assurance determine objectively whether the capability works?

**Answer:** `YES_WITH_EVIDENCE`

**Evidence and explanation:**

- 55 measurable acceptance criteria;
- 65 identified tests covering positive, negative, contract, permission, security, offline, recurrence, time-zone, provider, migration, recovery, and readiness behavior;
- 10 golden paths, including provider outage and first-user rehearsal;
- 45 adversarial scenarios;
- measurable success targets and operational thresholds;
- evidence fields, producers, integrity, retention, and gate mappings.

**Supporting sections:** 3, 20, 29 through 33, 40.

**Downstream gate determination:** QA can design and execute objective verification without making product decisions. No verification result is claimed until an approved as-built baseline and evidence exist.

### 41.3 Governance and MIAP traceability

**Question:** Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?

**Answer:** `YES_WITH_EVIDENCE`

**Evidence and explanation:**

- the locked constitutional commit and tag are registered;
- the exact PIA Master Standard and adoption-record hashes are registered;
- twenty inherited source families and the MIAP authority relationship are identified and qualified;
- shared controls, ownership, Founder decisions, requirements, workflows, entities, permissions, acceptance, tests, evidence, work packages, and gates are mapped in both directions at the controlled family level;
- package freeze requires repository path and checksum regeneration without permitting substantive reinterpretation.

**Supporting sections:** 1, 4 through 6, 37, 39, and 40.

**Downstream gate determination:** Documentary traceability is sufficient for structured review and implementation-package preparation. Fresh source and checksum custody validation remains required at freeze.

### 41.4 Operational safety and recovery

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?

**Answer:** `YES_WITH_EVIDENCE`

**Evidence and explanation:**

- operational and support ownership roles are defined;
- measurable service, delivery, sync, offline, recovery, and support targets are defined;
- monitoring, alerts, incident severity, support permissions, administrative tools, degraded mode, stop conditions, backup, restore, rollback, provider exit, and runbooks are specified;
- external providers can be independently disabled while preserving native records and evidence;
- operational evidence families and required rehearsal outputs are defined.

**Supporting sections:** 3, 19 through 23, 33, 34, 37, and 40.

**Downstream gate determination:** The PIA fully specifies how safe operation must be proven. The Operational-Readiness Gate remains closed until the controls are implemented, rehearsed, and evidenced. `YES_WITH_EVIDENCE` is a documentary sufficiency answer, not an assertion that production operations are active.

### 41.5 First-user enrollment readiness determination

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?

**Answer:** `YES_WITH_EVIDENCE`

**Evidence and explanation:**

The Founder can make a reproducible determination using:

- release classification and bounded first-user scope;
- the twenty approved product decisions;
- 120 requirements and gate mappings;
- required as-built reconciliation;
- acceptance, tests, golden paths, adversarial scenarios, and evidence manifest;
- operational ownership, support, monitoring, recovery, and rollback requirements;
- unresolved findings and retained-risk registers;
- provider-specific activation gates;
- first-user rehearsal and stop conditions; and
- an explicit Founder disposition.

**Current determination:** `NOT_READY_FOR_FIRST_USER_ENROLLMENT` because no implementation, as-built reconciliation, executed verification, operational rehearsal, onboarding evidence, or enrollment disposition exists.

**Required future enrollment evidence:** implemented first-user scope; Questions 1 through 5 revalidated against the as-built and as-verified baselines; no unresolved P0 or P1; passed enrollment golden path; active monitoring and support; tested backup, restore, and rollback; provider evidence for each active adapter; onboarding instructions; disclosed and accepted P2 risks; and Founder issuance of `VERIFIED_AND_READY_FOR_CONTROLLED_FIRST_USER_ENROLLMENT`.

**Supporting sections:** 8, 20, 29 through 34, 37 through 43.

---

## 42. Review, Approval, Authorization, and Disposition

### 42.1 Review record

| Review function | Version | Date | Disposition | Findings |
|---|---|---|---|---|
| Internal documentary drafting review | `0.1.0` | `2026-07-22` | `REVISION_REQUIRED` | Six P1 documentary findings; no P0 |
| Internal revision validation | `0.2.0` | `2026-07-22` | `PASS_FOR_DOCUMENTARY_STRUCTURE_AND_ID_INTEGRITY` | V0.2 created; fresh structured review pending |
| Domain review | `0.2.0` | Pending | Not performed | Pending |
| Architecture review | `0.2.0` | Pending | Not performed | Pending |
| Security and privacy review | `0.2.0` | Pending | Not performed | Pending |
| Safeguarding review | `0.2.0` | Pending | Not performed | Pending |
| Segregated review | `0.2.0` | Pending | Not performed | Pending |
| Adversarial challenge | `0.2.0` | Pending | Not performed | Pending |
| Machine validation | `0.2.0` | `2026-07-22` | Documentary validation pass | Companion JSON produced |
| Golden-path review | `0.2.0` | Pending | Design paths defined; execution not performed | Pending as-built |
| Evidence review | `0.2.0` | Pending | Evidence plan defined; runtime evidence absent | Pending as-built |
| Operational readiness | `0.2.0` | Pending | Design complete; execution absent | Gate closed |

### 42.2 Internal review disposition

`V0_2_MATERIALLY_STRENGTHENED_ALL_FIVE_READINESS_QUESTIONS_FULLY_ANSWERED_READY_FOR_FRESH_STRUCTURED_REVIEW_NO_IMPLEMENTATION_AUTHORITY`

### 42.3 Requested Founder disposition

`FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`

This requested disposition would approve the as-designed Item 06 baseline for downstream package preparation. It would not authorize code, schema, migration, provider activation, deployment, production use, or first-user enrollment.

### 42.4 Separate future dispositions

Implementation authorization, verification, operational readiness, external-provider activation, and first-user enrollment each require their own later evidence and Founder disposition. No approval may be inferred from silence, drafting completion, or a passing documentary validation.

---

## 43. First-User Enrollment, Maintenance, Supersession, and Decommissioning

### 43.1 First-user enrollment gate

The controlled first-user candidate is invite-only, founder-controlled, and limited to one facility and three to five primary workflows. Enrollment cannot begin until:

- the approved first-user capability slice is implemented;
- as-built reconciliation passes;
- all applicable acceptance criteria and tests pass;
- Golden Path `TCSN-GP-010` passes;
- relevant adversarial scenarios pass or have accepted nonblocking P2 treatment;
- no relevant P0 or P1 remains;
- monitoring, alerts, support, administrative tools, backup, restore, and rollback are active and tested;
- active providers have separate activation evidence;
- onboarding and user-support instructions are ready;
- retained P2 risks are disclosed and accepted;
- the evidence package is frozen and checksummed; and
- the Founder issues `VERIFIED_AND_READY_FOR_CONTROLLED_FIRST_USER_ENROLLMENT`.

### 43.2 Maintenance triggers

Review this PIA when a controlling canon changes, a dependent PIA changes materially, a provider contract or behavior changes, calendar or notification standards change, a material incident occurs, offline or time-zone behavior changes, implementation drifts, a new channel is proposed, SMS scope expands, a major release is proposed, or the capability is retired.

### 43.3 Supersession

A successor must preserve this version, the V0.1 predecessor, review findings, Founder decisions, requirement and test lineage, source posture, evidence, and the exact reason for each material change. Supersession never erases as-built or as-verified history.

### 43.4 Decommissioning

Decommissioning must define replacement capability, user communication, data export, retention, legal hold, queue drainage, cancellation of future occurrences, adapter shutdown, credential revocation, notification suppression, evidence preservation, feature-flag removal, code removal, support period, and final Founder disposition.

---

# Documentary Authority Notice

`NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_PROVIDER_ACTIVATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT`

This V0.2 strengthened candidate is a controlled as-designed artifact only.
