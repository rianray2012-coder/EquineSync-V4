# Task, Calendar, Scheduling, and Notification Product Implementation Atlas

**PIA ID:** `ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION-V0.1.0`  
**Portfolio Position:** `06`  
**Version:** `0.1.0`  
**Draft Date:** `2026-07-22`  
**Status:** `ITEM_06_V0_1_INITIAL_DOCUMENTARY_DRAFT_FOUNDER_DECISIONS_INCORPORATED_REVIEW_NOT_STARTED`  
**PIA Type:** `CROSS-DOMAIN`  
**Classification:** `EQUINESYNC_INTERNAL`  
**Canonical Template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder / Approval Authority:** `Rian Ray`  
**Founder Decisions Incorporated:** `TCSN-FD-001` through `TCSN-FD-020`  
**Implementation Authority:** `FALSE`  
**Schema Authority:** `FALSE`  
**Migration Authority:** `FALSE`  
**Deployment Authority:** `FALSE`  
**Production Authority:** `FALSE`  
**First-User Enrollment Authority:** `FALSE`  
**Independent Review Completed:** `FALSE`  
**External Assurance:** `NOT_EXTERNALLY_ASSURED`

This initial documentary draft translates the Founder-approved direction for EquineSync tasks, calendar objects, scheduling, reminders, notification delivery, acknowledgment, escalation, offline execution, external calendar synchronization, and optional SMS into a controlled implementation-design baseline.

It does not authorize implementation, schema creation, migration, deployment, production activation, external-provider activation, pilot use, or first-user enrollment.

---

## 1. Document Control and Status

### 1.1 Current disposition

`ITEM_06_V0_1_INITIAL_DOCUMENTARY_DRAFT_FOUNDER_DECISIONS_INCORPORATED_REVIEW_NOT_STARTED`

### 1.2 Baseline status

| Baseline | Identifier | Status |
|---|---|---|
| As-designed | `ES-PIA-TCSN-V0.1.0` | Initial draft; Founder decisions incorporated; review not started |
| As-built | None | Not implemented |
| As-verified | None | No executed evidence |
| Operational | None | Not ready |
| Enrollment | None | Not authorized |

### 1.3 Authority boundary

Founder approval of the twenty design decisions authorizes their use as documentary requirements. It does not authorize code, database changes, provider selection, SMS activation, production credentials, migration, deployment, or enrollment.

### 1.4 Role-segregation disclosure

EquineSync is founder-led and may require one person to perform multiple governance and product functions. Later review must preserve procedural segregation through separate drafting, structured review, adversarial review, machine validation, evidence review, and explicit Founder disposition.

---

## 2. Executive Summary

EquineSync needs one coherent coordination system without collapsing fundamentally different records into a single digital tack trunk.

A task represents work. A calendar event represents time coordination. A schedule occurrence represents one instance of a timing rule. A notification represents delivery activity. An acknowledgment represents receipt or awareness. An escalation represents an unresolved risk response. None of those records, by itself, creates medical, financial, legal, relationship, guardian, employment, or professional authority.

The design therefore establishes:

- separate canonical records with explicit links;
- underlying-domain authority for substantive truth;
- EquineSync ownership of native scheduling truth;
- task-specific assignment and completion truth;
- notification-specific delivery evidence;
- configurable assignment, recurrence, delegation, conflict, escalation, and quiet-hours behavior;
- provider-neutral calendar adapters;
- offline barn and show-ground execution;
- initial notification channels of in-app, push, email, digest, optional SMS, and failed-delivery administration;
- strict separation between acknowledgment and completion;
- versioned automation provenance;
- feature-flagged external synchronization;
- controlled first-release boundaries.

### 2.1 Executive readiness

| Mandatory Question | Current Answer |
|---|---|
| Can engineering build without unauthorized product decisions? | `PARTIALLY_SATISFIED` |
| Can QA objectively determine whether it works? | `PARTIALLY_SATISFIED` |
| Can a reviewer trace it to governance and MIAP? | `PARTIALLY_SATISFIED` |
| Can EquineSync safely operate, support, monitor, recover, and maintain it? | `NO` |
| Can the Founder determine first-user enrollment readiness? | `NO` |

---

## 3. Purpose, Outcomes, and Success Measures

### 3.1 Purpose

Create a deterministic, horse-aware, role-aware, facility-aware, offline-capable coordination layer that helps users know what must happen, when it must happen, who is responsible, what changed, what failed, and what evidence exists.

### 3.2 Product outcomes

- Fewer missed horse-care and facility tasks.
- Clear responsibility without unauthorized access expansion.
- Reliable recurrence and time-zone behavior.
- Visible resource and welfare conflicts.
- Lower notification fatigue without hiding urgency.
- Better handoffs across staff, owners, trainers, providers, and substitutes.
- Traceable offline completion.
- Recoverable external-calendar synchronization.
- Clear evidence for support, correction, and dispute review.

### 3.3 Success measures

Later operational metrics should include task completion timeliness, exception rate, escalation rate, notification delivery rate, failed-delivery recovery, duplicate suppression, sync health, conflict frequency, override frequency, offline reconciliation success, and support correction rate.

Metrics must not reward raw message volume, maximum screen time, or coercive notification behavior.

---

## 4. Authority, Source, and Traceability Baseline

### 4.1 Controlling source families

This PIA must remain traceable to, at minimum:

- `ES-PIA-MASTER-STANDARD-V1.1`;
- Founder Adoption and Approval Record for the PIA Master Standard;
- Master Product Vision;
- RF29 Calendar Domain Canon;
- Master Barn Lifecycle and Operations Canon;
- Master Communication, Notification, and Notice Model;
- Master Identity, Account, and Actor Model;
- Master Relationship Model;
- Master Permission and Access-Control Model;
- Master Agreement, Consent, and Authorization Model;
- Master Record Stewardship and Retention Model;
- Master Audit Event and Evidence Model;
- Master External Architecture and Adapter Model;
- Master Platform Operations, Reliability, and Release Model;
- Master Platform Resilience, Backup, and Recovery Model;
- Master Configuration and Feature Flag Governance Model;
- Master Privacy and Data Protection Model;
- Master Minor, Guardianship, Safeguarding, and Protected Participant Model;
- Master AI Governance and Decision Boundary Model;
- applicable MIAP calendar, communication, offline, testing, release, and operations standards;
- Founder decisions `TCSN-FD-001` through `TCSN-FD-020`.

### 4.2 Current source-registration limitation

Exact repository paths, version states, hashes, page or line anchors, supersession relationships, and MIAP work-package links are not yet registered in this V0.1 file. That gap blocks complete governance traceability and implementation authorization.

### 4.3 Precedence

Where the PIA conflicts with controlling governance, the controlling governance prevails. Where another PIA owns substantive domain truth, this PIA coordinates timing and work but does not take ownership.

---

## 5. Scope

### 5.1 In scope

- native tasks;
- assignments, acceptance, claims, delegation, and substitution;
- task evidence, exceptions, correction, and completion;
- native calendar events;
- one-time and recurring schedules;
- calendar views and resource coordination;
- conflicts and authorized overrides;
- reminders and escalation;
- in-app, push, email, digest, and optional SMS;
- quiet hours and urgent overrides;
- failed-delivery queues;
- external calendar import, export, projection, and controlled synchronization;
- time zones and daylight-saving behavior;
- offline viewing and completion;
- audit, evidence, support, correction, and rollback requirements.

### 5.2 Cross-domain interfaces

This PIA may receive source instructions or requests from horse care, health, lessons, training, shows, facilities, providers, inventory, incidents, billing, safeguarding, agreements, and other owning PIAs.

### 5.3 Out of scope

- substantive medical instructions or medical authority;
- financial liability, invoicing, payment, or refund truth;
- legal notice content beyond delivery integration;
- full messaging and conversation threads;
- workforce employment classification or payroll;
- rider suitability decisions;
- show-entry ownership;
- marketplace booking and settlement;
- voice calling trees;
- WhatsApp or similar consumer channel activation;
- advanced route optimization;
- autonomous AI scheduling;
- unrestricted multi-provider bidirectional synchronization.

---

## 6. Domain Ownership and Cross-PIA Boundaries

| Record or decision | Authoritative owner | This PIA treatment |
|---|---|---|
| Care or medical instruction | Owning care or health PIA | References source and schedules authorized work |
| Task assignment and completion | Task operational record under Barn Operations authority | Owns task lifecycle |
| Calendar event identity and recurrence | RF29 Calendar domain | Owns event and recurrence lifecycle |
| Lesson participation | Lessons, Training, Riders, and Guardians PIA | Coordinates time only |
| Show or itinerary content | Shows, Events, Ride Times, and Itineraries PIA | Coordinates event timing and reminders |
| Financial obligation | Billing and Financial Operations PIA | May schedule due dates but does not create liability |
| Notification delivery evidence | Communication and Notice authority | Owns channel delivery and acknowledgment evidence |
| Identity and contact destination | Identity and Communication authorities | References verified destinations |
| Access decision | Permission and Relationship authorities | Enforces least privilege |
| External provider state | Adapter record | Never replaces canonical EquineSync authority |

---

## 7. Controlled Vocabulary

- **Task:** A governed record of work, obligation, or requested action.
- **Event:** A governed time-coordination record.
- **Schedule:** A rule or arrangement governing timing.
- **Occurrence:** One generated or created instance of a schedule or recurrence rule.
- **Reminder:** A notification intended to prompt awareness before or around an event or task.
- **Notification:** A delivery record through one or more channels.
- **Acknowledgment:** Evidence that a recipient affirmatively indicated receipt or awareness.
- **Acceptance:** Agreement to take responsibility for an assignment.
- **Completion:** Recorded performance or resolution of the task.
- **Exception:** A recorded variance, inability, substitution, or departure.
- **Escalation:** A risk-based response to noncompletion, failure, or urgency.
- **Hard conflict:** A conflict that blocks scheduling absent authorized override.
- **Soft conflict:** A conflict that warns and requires confirmation.
- **External-only event:** An event displayed from an external source without EquineSync operational ownership.
- **Quiet hours:** Recipient or tenant periods in which routine notifications may be suppressed or deferred.
- **Mandatory notice:** A communication that ordinary preferences may not suppress.
- **Optional SMS:** SMS delivery available in the initial controlled scope but not required for every user or communication class.

---

## 8. Capability and Release Classification

### 8.1 Initial controlled release

- native tasks;
- one-time and recurring schedules;
- assignment and acceptance;
- due instants and windows;
- evidence and exceptions;
- offline completion;
- risk-based escalation;
- in-app, push, email, digest, and optional SMS;
- basic calendar and resource views;
- administrator failed-delivery tools;
- Google Calendar synchronization only behind a feature flag after separate readiness.

### 8.2 Later controlled releases

- Microsoft bidirectional synchronization;
- enhanced Apple integration beyond ICS;
- advanced staffing and shift optimization;
- automated route and chore sequencing;
- full show-trip optimization;
- voice or emergency calling trees;
- advanced provider booking;
- AI schedule recommendations with approved human review.

### 8.3 Prohibited release inference

Documentary inclusion does not imply release approval. MIAP release planning must identify the exact slice, dependencies, evidence, feature flags, cohort, and rollback posture.

---

## 9. User and Operational Workflows

### 9.1 Create and assign a routine task

1. Select task template or create authorized task.
2. Identify source domain, horse, location, facility, instruction, due timing, and evidence requirement.
3. Select assignment mode.
4. Resolve recipient authority and minimum necessary access.
5. Create task and any linked event.
6. Send policy-appropriate notification.
7. Preserve creation evidence.

### 9.2 Accept, decline, or claim work

1. Recipient opens assignment.
2. System displays scope, due timing, required evidence, and authority context.
3. Recipient accepts, declines with reason, or claims if eligible.
4. Assignment state updates.
5. Escalation and substitute rules adjust.

### 9.3 Complete with evidence

1. Actor records actual time and status.
2. Actor supplies required evidence or exception.
3. System records offline or online context.
4. Completion is validated.
5. Linked escalation changes according to policy.
6. Notification of completion is routed only where authorized.

### 9.4 Enter late or backdated completion

1. Actor selects actual asserted completion time.
2. System preserves entry time and original due time.
3. Actor provides reason.
4. Existing escalation history remains.
5. High-risk task enters review where required.

### 9.5 Create or edit recurrence

1. Define rule, zone, start, exclusions, and end.
2. Preview occurrences.
3. Save rule version.
4. Edit one, this-and-following, or entire future series.
5. Preserve completed history and prior rule lineage.

### 9.6 Schedule a multi-resource event

1. Select people, horses, facilities, arenas, trailers, equipment, and providers.
2. Evaluate availability, welfare constraints, buffers, and guardian requirements.
3. Classify conflicts.
4. Block, warn, or disclose unknown status.
5. Record override if permitted.
6. Send invitations or reminders.

### 9.7 Import or synchronize external calendar data

1. Establish authorized connection.
2. Classify source and direction.
3. Map time zones and identities.
4. Prevent duplicates.
5. Reconcile changes and deletions.
6. Display sync health.
7. Record failures and retries.

### 9.8 Deliver routine notification

1. Resolve recipients and permitted channels.
2. Apply quiet hours, preferences, deduplication, and digest rules.
3. Send through approved channel.
4. Process provider evidence.
5. Retry or fall back according to policy.
6. Preserve final state.

### 9.9 Deliver urgent or mandatory notification

1. Confirm classification and authority.
2. Override quiet hours where authorized.
3. Avoid routine digest consolidation.
4. Use approved channel sequence.
5. Require acknowledgment where applicable.
6. Escalate failed delivery.

### 9.10 Use optional SMS

1. Confirm verified destination and permitted purpose.
2. Apply consent, opt-out, sensitivity, length, and cost controls.
3. Send minimum necessary content.
4. Process provider status.
5. Use approved fallback after failure.
6. Preserve evidence without treating failure as refusal.

### 9.11 Escalate missed task

1. Detect missed due window.
2. Determine risk class and grace period.
3. Evaluate acknowledgment, substitute coverage, operational hours, and prior attempts.
4. Notify next authorized recipient.
5. Stop, transform, or continue based on task state.
6. Preserve escalation chain.

### 9.12 Complete work offline

1. Display only previously authorized task data.
2. Record completion, exception, evidence, actor, device, and local context.
3. Mark record unsynchronized.
4. Retry on reconnect.
5. Reconcile duplicate or conflicting changes.
6. Enter review when deterministic resolution is unsafe.

---

## 10. Actor, Persona, Relationship, and Authority Model

Actors may include individual horse owners, barn-associated owners, trainers, facility administrators, grooms, staff, lesson participants, guardians, providers, support personnel, system services, and external adapters.

No role title alone grants authority. Every action must evaluate:

- authenticated actor;
- represented principal;
- tenant and facility context;
- horse relationship;
- assigned role;
- delegation;
- governing agreement or instruction;
- professional or safeguarding limitation;
- record sensitivity;
- requested action;
- current lifecycle state.

Support access must be time-bounded, purpose-limited, and audited.

---

## 11. Functional Requirements

The controlled requirement register for this draft contains 80 requirements.

| Requirement ID | Requirement |
| --- | --- |
| TCSN-REQ-001 | The system SHALL preserve separate canonical records for tasks, calendar events, schedule occurrences, notifications, acknowledgments, and escalations. |
| TCSN-REQ-002 | The underlying domain record SHALL remain authoritative for substantive care, medical, financial, safeguarding, contractual, facility, lesson, show, or provider truth. |
| TCSN-REQ-003 | The EquineSync calendar SHALL own EquineSync event identity, recurrence, schedule authority, time-zone treatment, and synchronization state. |
| TCSN-REQ-004 | The task record SHALL own assignment, execution, exception, and completion truth for operational work. |
| TCSN-REQ-005 | The notification record SHALL own delivery, failure, retry, channel, receipt, and acknowledgment evidence without mutating the underlying task or event. |
| TCSN-REQ-006 | A task SHALL NOT be created merely because an event exists unless an explicit rule or authorized actor creates or links it. |
| TCSN-REQ-007 | An event SHALL NOT be created merely because a task exists unless the task is scheduled or a user elects to place it on the calendar. |
| TCSN-REQ-008 | A calendar event or task assignment SHALL NOT independently create medical, legal, financial, relationship, employment, guardian, or access authority. |
| TCSN-REQ-009 | Every task, event, notification, escalation, and override SHALL identify one authoritative owning domain and one accountable record owner. |
| TCSN-REQ-010 | The system SHALL expose the source, authority, and governing instruction for every system-generated operational item. |
| TCSN-REQ-011 | Tasks SHALL support direct assignment, acceptance-required assignment, claimable assignment, suggested assignment, and emergency assignment. |
| TCSN-REQ-012 | Assignment mode SHALL be determined by task type, governing authority, risk class, and organizational configuration. |
| TCSN-REQ-013 | Assignment SHALL NOT grant broader access than the minimum information required to perform the work. |
| TCSN-REQ-014 | Delegation SHALL distinguish reassignment, retained-responsibility delegation, substitute coverage, authorized pool claim, emergency takeover, and supervisor override. |
| TCSN-REQ-015 | Delegation SHALL be prohibited when the task type, governing instruction, professional scope, safeguarding rule, or assigning authority does not permit it. |
| TCSN-REQ-016 | Tasks SHALL support due instants, due windows, start windows, no-fixed-time due dates, and unscheduled backlog states. |
| TCSN-REQ-017 | Task completion SHALL preserve completing actor, actual completion time, entered time, location context, instruction version, evidence, exception, offline status, and synchronization time. |
| TCSN-REQ-018 | A completion entered after the due time SHALL preserve the original due time and shall not erase an already-triggered escalation. |
| TCSN-REQ-019 | Backdated completion SHALL require an asserted completion time, entry time, entering actor, and reason. |
| TCSN-REQ-020 | High-risk late or backdated completion MAY require supervisor review according to policy. |
| TCSN-REQ-021 | Task completion states SHALL distinguish completed, completed-with-exception, unable-to-complete, declined, canceled, superseded, and duplicate. |
| TCSN-REQ-022 | Completion evidence requirements SHALL be configurable by task template and risk class. |
| TCSN-REQ-023 | A task SHALL NOT be marked complete solely because its notification was opened or acknowledged. |
| TCSN-REQ-024 | Task correction SHALL preserve original values, corrected values, reason, actor, effective time, and audit lineage. |
| TCSN-REQ-025 | Recurring tasks and events SHALL support editing one occurrence, this-and-following occurrences, or the entire future series. |
| TCSN-REQ-026 | Completed or historical occurrences SHALL NOT be silently rewritten by edits to a recurring series. |
| TCSN-REQ-027 | Recurrence SHALL support daily, weekly, monthly, interval, rule-based, and domain-generated patterns with explicit exclusions. |
| TCSN-REQ-028 | The system SHALL preserve recurrence rule version and occurrence-generation provenance. |
| TCSN-REQ-029 | Canceling a series SHALL preserve historical occurrences and identify the cancellation scope and reason. |
| TCSN-REQ-030 | Skipped or excepted occurrences SHALL remain queryable and auditable. |
| TCSN-REQ-031 | Calendar events SHALL distinguish EquineSync-source, imported, synchronized, external-only, tentative, canceled, conflicted, and failed-sync states. |
| TCSN-REQ-032 | Imported external events SHALL be visibly labeled and SHALL NOT silently become authoritative EquineSync operational records. |
| TCSN-REQ-033 | Google Calendar and Microsoft calendar synchronization MAY be bidirectional only when authorized and technically approved. |
| TCSN-REQ-034 | Apple Calendar initial support SHALL use controlled ICS subscription or export unless a later adapter is approved. |
| TCSN-REQ-035 | External adapters SHALL remain provider-neutral and replaceable. |
| TCSN-REQ-036 | External deletion SHALL NOT silently delete an authoritative EquineSync event without the approved conflict and deletion policy. |
| TCSN-REQ-037 | Synchronization SHALL provide duplicate prevention, idempotency, conflict visibility, revocation handling, retry, dead-letter treatment, and reconciliation. |
| TCSN-REQ-038 | The system SHALL display sync health and last successful synchronization for connected calendars. |
| TCSN-REQ-039 | Scheduling conflicts SHALL be classified as hard, soft, informational, or unknown-availability. |
| TCSN-REQ-040 | Conflict evaluation SHALL support people, horses, facilities, arenas, stalls, treatment spaces, trailers, equipment, providers, travel buffers, welfare limits, and guardian participation where applicable. |
| TCSN-REQ-041 | Hard conflicts SHALL block scheduling unless an authorized override exists. |
| TCSN-REQ-042 | Conflict overrides SHALL record actor, authority, reason, affected resources, time, and downstream notification behavior. |
| TCSN-REQ-043 | Unknown availability SHALL be disclosed rather than represented as confirmed availability. |
| TCSN-REQ-044 | Travel time and setup or recovery buffers MAY be configured as scheduling constraints. |
| TCSN-REQ-045 | The system SHALL preserve authoritative event time zone, facility time zone, user display time zone, UTC instant, and daylight-saving interpretation. |
| TCSN-REQ-046 | Travel or device time-zone change SHALL NOT silently shift the authoritative time of a horse-care or safety-critical schedule. |
| TCSN-REQ-047 | Ambiguous or nonexistent daylight-saving local times SHALL require deterministic handling and visible explanation. |
| TCSN-REQ-048 | Time changes SHALL preserve old and new values, source, actor, and notification effects. |
| TCSN-REQ-049 | Notifications SHALL support in-app, push, email, optional SMS, digest, and administrator-visible failed-delivery queues in the initial controlled scope. |
| TCSN-REQ-050 | SMS SHALL remain optional, consent-aware, cost-aware, and subject to channel suitability, contact verification, opt-out, and mandatory-notice rules. |
| TCSN-REQ-051 | Voice calling, WhatsApp or similar consumer channels, and automated emergency calling trees SHALL remain outside the initial scope unless separately authorized. |
| TCSN-REQ-052 | Notification states SHALL distinguish queued, sent, provider-accepted, delivered, viewed, acknowledged, failed, suppressed, expired, retried, dead-lettered, and superseded. |
| TCSN-REQ-053 | Acknowledgment SHALL be distinct from assignment acceptance, consent, professional approval, task completion, and legal assent. |
| TCSN-REQ-054 | Routine notifications MAY respect quiet hours, digests, preferences, and channel selections. |
| TCSN-REQ-055 | Safety-critical, welfare-critical, safeguarding, mandatory legal, or approved emergency communications MAY override quiet hours. |
| TCSN-REQ-056 | Every quiet-hours override SHALL preserve classification, reason, sender or automation, recipients, channel, delivery result, and acknowledgment requirement. |
| TCSN-REQ-057 | Notification routing SHALL apply recipient identity, relationship, role, tenant, facility, horse, guardian, and communication-capacity rules. |
| TCSN-REQ-058 | Routine notification volume SHALL support coalescing, duplicate suppression, per-horse grouping, per-facility grouping, and configurable digests. |
| TCSN-REQ-059 | Urgent or mandatory communications SHALL NOT be hidden inside routine digests. |
| TCSN-REQ-060 | Failed delivery SHALL trigger policy-based fallback, retry, escalation, or administrator review without being misrepresented as refusal or acknowledgment. |
| TCSN-REQ-061 | Missed-task escalation SHALL use configurable risk classes: routine, time-sensitive, welfare-sensitive, health-sensitive, safety-critical, safeguarding-sensitive, legal or mandatory notice, and emergency. |
| TCSN-REQ-062 | Escalation SHALL consider severity, due window, grace period, operational hours, acknowledgment, substitute coverage, responsible role, horse, and facility. |
| TCSN-REQ-063 | Escalation ceilings and recipient chains SHALL prevent uncontrolled message storms. |
| TCSN-REQ-064 | Escalation SHALL stop, continue, or transform according to completion, exception, acknowledgment, reassignment, cancellation, and recovery state. |
| TCSN-REQ-065 | Automated task or event creation SHALL be permitted only through explicit, versioned rules or authorized user action. |
| TCSN-REQ-066 | Every generated item SHALL identify source record, generating rule version, generating actor or service, cancellation behavior, and source-change behavior. |
| TCSN-REQ-067 | Care plans, medication schedules, provider recommendations, lesson bookings, show itineraries, maintenance plans, inventory thresholds, and incident follow-up MAY generate linked items through their owning PIAs. |
| TCSN-REQ-068 | AI SHALL NOT independently create or assign safety-critical, medical, safeguarding, legal, financial, or irreversible work without an approved human-review rule. |
| TCSN-REQ-069 | Users SHALL be able to create personal convenience reminders that do not change authoritative operational truth. |
| TCSN-REQ-070 | Mandatory, safety-critical, safeguarding, welfare, or legal reminders SHALL NOT be disabled through ordinary personal preferences. |
| TCSN-REQ-071 | Offline task viewing, execution, exception recording, and evidence capture SHALL be supported for previously authorized data. |
| TCSN-REQ-072 | Offline changes SHALL display unsynchronized status and preserve device, actor, local time, authoritative time context, and retry state. |
| TCSN-REQ-073 | Offline synchronization SHALL be idempotent and SHALL prevent duplicate completion or duplicate notifications. |
| TCSN-REQ-074 | Irreconcilable offline conflicts SHALL enter a review state rather than silently selecting the last write. |
| TCSN-REQ-075 | Revoked or expired access SHALL limit offline data availability and SHALL be reconciled at the earliest supported connection. |
| TCSN-REQ-076 | The initial controlled release SHALL include native tasks, one-time and recurring schedules, assignment and acceptance, due windows, offline completion, evidence, exceptions, escalation, in-app, push, email, optional SMS, basic calendar views, and failed-delivery administration. |
| TCSN-REQ-077 | Google Calendar synchronization MAY be activated behind a feature flag after adapter, security, privacy, test, and rollback readiness. |
| TCSN-REQ-078 | Advanced workforce optimization, automated route planning, broad marketplace booking, AI-generated schedules, voice trees, and full multi-provider bidirectional synchronization SHALL remain deferred. |
| TCSN-REQ-079 | All material actions SHALL produce auditable events and evidence sufficient for support, correction, dispute, and release review. |
| TCSN-REQ-080 | No implementation, deployment, production use, or enrollment SHALL be authorized solely by completion of this documentary draft. |

---

## 12. Calendar and Scheduling Model

Calendar events must support:

- title and user-safe display label;
- authoritative start and end;
- event time zone;
- all-day and floating-time behavior where approved;
- owning domain;
- source type;
- recurrence;
- participants and resources;
- location;
- linked tasks;
- visibility and sensitivity;
- conflict state;
- synchronization state;
- cancellation, correction, and supersession;
- audit history.

An event may coordinate work but cannot independently establish the substantive authority behind the work.

---

## 13. Task Model

A task must support:

- source domain and source record;
- instruction version;
- horse, facility, location, business, and resource references;
- assignment mode;
- assignee, pool, delegator, and accountable owner;
- risk class;
- due instant or due window;
- recurrence or schedule link;
- status and exception;
- evidence requirement;
- completion actor and timestamps;
- escalation policy;
- offline and synchronization state;
- correction and supersession lineage.

Task templates must be versioned. Updating a template must not silently rewrite issued historical tasks.

---

## 14. Notification and Notice Model

Notification delivery must separate:

- content or template;
- communication class;
- recipient resolution;
- destination verification;
- channel suitability;
- preference and quiet-hours handling;
- mandatory override authority;
- send attempt;
- provider evidence;
- delivery state;
- acknowledgment;
- fallback;
- retry;
- dead-letter;
- correction or supersession.

Optional SMS must use minimum necessary content, avoid unnecessary sensitive horse or personal details, and support verified-destination, opt-out, and cost controls.

---

## 15. Data Model and Entity Ownership

Core entities include:

- `Task`;
- `TaskTemplate`;
- `TaskAssignment`;
- `TaskDelegation`;
- `TaskCompletion`;
- `TaskException`;
- `TaskEvidenceReference`;
- `CalendarEvent`;
- `ScheduleRule`;
- `ScheduleOccurrence`;
- `ResourceReservation`;
- `ConflictRecord`;
- `ConflictOverride`;
- `Notification`;
- `NotificationAttempt`;
- `NotificationDestination`;
- `NotificationAcknowledgment`;
- `DigestBatch`;
- `EscalationPolicy`;
- `EscalationInstance`;
- `ExternalCalendarConnection`;
- `ExternalEventReference`;
- `SyncCheckpoint`;
- `DeadLetterItem`;
- `OfflineMutation`;
- `ReconciliationCase`;
- `AutomationRule`;
- `FeatureFlagReference`.

Every entity must have a stable identifier, tenant context, authoritative owner, lifecycle state, provenance, created and updated attribution, and retention classification.

---

## 16. State and Transition Model

### 16.1 Task states

`DRAFT → OPEN → OFFERED/PENDING_ACCEPTANCE/CLAIMABLE → ACCEPTED/ASSIGNED → IN_PROGRESS → COMPLETED/COMPLETED_WITH_EXCEPTION/UNABLE_TO_COMPLETE`

Additional controlled states include `DECLINED`, `REASSIGNED`, `DELEGATED`, `CANCELED`, `SUPERSEDED`, `DUPLICATE`, `UNDER_REVIEW`, and `ARCHIVED`.

### 16.2 Event states

`DRAFT → TENTATIVE → CONFIRMED → IN_PROGRESS → COMPLETED`

Additional states include `CANCELED`, `CONFLICTED`, `EXTERNAL_ONLY`, `SYNC_PENDING`, `SYNC_FAILED`, `SUPERSEDED`, and `ARCHIVED`.

### 16.3 Notification states

`QUEUED → SENT → PROVIDER_ACCEPTED → DELIVERED → VIEWED/ACKNOWLEDGED`

Failure branches include `FAILED`, `RETRY_SCHEDULED`, `SUPPRESSED`, `EXPIRED`, `DEAD_LETTERED`, and `SUPERSEDED`.

### 16.4 Escalation states

`NOT_APPLICABLE → ARMED → TRIGGERED → NOTIFIED → ACKNOWLEDGED/REASSIGNED → RESOLVED`

Failure or continuation states include `DELIVERY_FAILED`, `NEXT_LEVEL`, `MANUAL_REVIEW`, and `CLOSED_WITH_EXCEPTION`.

No state transition may be inferred solely from UI visibility.

---

## 17. Permission and Access-Control Model

The permission matrix must separately control:

- create task;
- assign task;
- accept or decline;
- claim;
- delegate;
- reassign;
- complete;
- enter late completion;
- correct completion;
- cancel;
- edit recurrence;
- override conflict;
- connect external calendar;
- enable bidirectional sync;
- view destinations;
- send optional SMS;
- trigger urgent override;
- inspect failed delivery;
- retry or dead-letter;
- correct notification evidence;
- administer feature flags;
- export evidence.

Access must be scoped by tenant, facility, horse, relationship, record, purpose, time, and role. Administrative status is not universal authority.

---

## 18. Privacy, Safeguarding, and Sensitive Data

- Calendar titles must avoid exposing sensitive medical, safeguarding, or personal information in broad views.
- SMS and push previews must use minimum necessary content.
- Minors and guardians must receive communications according to protected-participant rules.
- Location and travel details may require restricted visibility.
- Contact destinations must be verified, purpose-bound, and retained only as required.
- Failed-delivery administration must not expose unrelated message content.
- Notification analytics must avoid becoming a secondary sensitive-data store.
- Consent is not a universal lawful basis, and opt-out rules must distinguish optional messages from mandatory notices.

---

## 19. Security and Trust Requirements

- tenant isolation;
- authorization on every action;
- secure storage of provider tokens;
- encrypted transport;
- credential rotation and revocation;
- verified provider webhooks;
- idempotency;
- rate limiting;
- abuse and notification-storm controls;
- secure deep links;
- anti-enumeration controls;
- destination verification;
- audit of support and administrator actions;
- feature-flag fail-closed behavior;
- secrets excluded from logs and evidence exports;
- incident handling for misdelivery, unauthorized disclosure, or false completion.

Threat modeling must cover cross-tenant leakage, spoofed delivery, stolen devices, malicious reassignment, notification harassment, and schedule manipulation.

---

## 20. Audit, Evidence, and Recordkeeping

Audit evidence must preserve:

- actor and represented principal;
- action;
- record and prior version;
- authority basis;
- source domain;
- event time and record time;
- time zone;
- device and offline state where material;
- provider attempt and response identifiers;
- override reason;
- escalation history;
- correction and supersession;
- feature-flag state;
- support access;
- export or disclosure.

Audit evidence must not silently mutate and must remain available under applicable retention, legal hold, claims, and incident rules.

---

## 21. External Integrations and Adapter Requirements

Initial adapter posture:

- Google Calendar: controlled, feature-flagged synchronization after readiness.
- Microsoft/Outlook: approved design direction, activation deferred until adapter readiness.
- Apple Calendar: ICS subscription or export initially.
- SMS: optional initial-scope channel, provider selection and activation pending.
- Push and email: provider-neutral implementation required.

Adapters must expose connection state, consent or authorization state, token status, last sync, failure state, retry state, and revocation behavior.

External providers are processors or transport adapters, not canonical authorities.

---

## 22. API, Event, Job, and Webhook Contracts

Required later contracts include:

- task create, update, assign, accept, decline, claim, delegate, complete, correct, cancel;
- event create, update, recur, split, cancel, reserve, override;
- notification request, route, send, retry, acknowledge, suppress, supersede;
- escalation arm, trigger, advance, resolve;
- external calendar connect, sync, revoke, reconcile;
- offline mutation submit and reconcile;
- dead-letter inspect and replay;
- feature-flag activate and deactivate.

Events and jobs must be versioned, idempotent, tenant-scoped, observable, retry-safe, and auditable. Provider webhooks must be authenticated and replay-resistant.

---

## 23. Offline, Mobile, and Synchronization Behavior

The mobile experience must support barn realities: gloves, one-handed use, poor connectivity, outdoor glare, urgent interruptions, multiple horses, and shared responsibilities.

Offline behavior must define:

- what data may be cached;
- how long it may remain;
- how revocation is handled;
- how evidence is queued;
- how duplicate submissions are prevented;
- how conflicts are classified;
- what can be resolved automatically;
- what requires review;
- how users see unsynchronized status;
- how support diagnoses failures.

No offline claim may be treated as complete without deterministic sync and recovery behavior.

---

## 24. Time, Time Zone, Recurrence, and Daylight Saving

Every material time record must distinguish:

- UTC instant;
- authoritative local time;
- authoritative time zone;
- facility time zone;
- user display time zone;
- all-day or floating semantics;
- effective time;
- recorded time;
- recurrence rule;
- DST interpretation.

The system must preserve historical interpretation even if time-zone databases change.

---

## 25. Conflict Detection, Resolution, and Overrides

Conflict rules must be versioned and attributable. Conflict evaluation may include:

- person overlap;
- horse overlap;
- resource overlap;
- facility closure;
- arena or stall reservation;
- trailer or equipment availability;
- provider availability;
- travel or preparation buffer;
- horse workload and welfare;
- minor or guardian requirements;
- unknown availability.

Overrides require authority, reason, affected resources, and audit. Repeated overrides should be reportable for operational review.

---

## 26. Accessibility, Field Ergonomics, and User Experience

- Critical status must not depend on color alone.
- Due time, risk class, horse, assignee, and offline status must be quickly scannable.
- Completion must be achievable with minimal taps.
- High-risk completion must resist accidental confirmation.
- Screen readers must announce status and urgency meaningfully.
- Touch targets must support gloves and mobile use.
- Notification content must be concise and accessible.
- Time zones and conflicts must be understandable without technical jargon.
- Bulk task views must avoid hiding urgent items beneath routine volume.

---

## 27. Automation and AI Boundaries

Automation may generate routine tasks, events, reminders, and summaries only under explicit rules.

AI may assist with drafting, summarizing, organizing, suggesting schedule options, detecting potential conflicts, and proposing workload groupings. AI may not independently:

- prescribe or modify medical care;
- assign safety-critical work;
- override conflicts;
- infer authority;
- decide rider suitability;
- create legal or financial obligations;
- suppress mandatory notices;
- resolve disputed completion;
- delete evidence;
- activate providers or feature flags.

Every AI-derived suggestion must be labeled, attributable, reviewable, and reversible.

---

## 28. Reporting, Search, Analytics, and Metrics

Authorized users may search and report on:

- open and overdue tasks;
- assignment and acceptance;
- completion and exception;
- escalation;
- resource utilization;
- conflict and override frequency;
- notification delivery and failure;
- sync health;
- offline backlog;
- support corrections.

Reports must preserve source, freshness, time zone, missing data, and permission filters. Analytics may not create a competing source of operational truth.

---

## 29. Acceptance Criteria

| Acceptance ID | Acceptance Criterion |
| --- | --- |
| TCSN-AC-001 | Creating an unscheduled task does not create a calendar event. |
| TCSN-AC-002 | Creating an arena reservation does not create a completion task unless a rule explicitly requires one. |
| TCSN-AC-003 | A direct assignment is immediately active only when the assigning actor has authority. |
| TCSN-AC-004 | An acceptance-required assignment remains pending until accepted or otherwise resolved. |
| TCSN-AC-005 | A claimable task can be claimed only by an actor in the authorized pool. |
| TCSN-AC-006 | Completion records preserve actor, actual time, entry time, instruction version, evidence status, and sync status. |
| TCSN-AC-007 | Backdated completion preserves the original escalation history. |
| TCSN-AC-008 | Editing one recurrence occurrence does not alter completed history or unrelated future occurrences. |
| TCSN-AC-009 | Editing this-and-following splits or versions the series deterministically. |
| TCSN-AC-010 | An imported external event is visibly labeled and does not silently create an operational task. |
| TCSN-AC-011 | External event deletion follows the approved conflict policy and does not silently destroy EquineSync truth. |
| TCSN-AC-012 | A hard resource conflict blocks save absent an authorized override. |
| TCSN-AC-013 | A soft conflict requires a visible warning and confirmation. |
| TCSN-AC-014 | Unknown availability is displayed as unknown. |
| TCSN-AC-015 | Authoritative time remains stable when a user travels across time zones. |
| TCSN-AC-016 | DST ambiguity is handled deterministically and visibly. |
| TCSN-AC-017 | Viewing or acknowledging a notification does not complete its task. |
| TCSN-AC-018 | Quiet hours suppress routine notices but not an authorized safety-critical override. |
| TCSN-AC-019 | An urgent notice does not disappear inside a routine digest. |
| TCSN-AC-020 | A failed email can fall back to another approved channel according to policy. |
| TCSN-AC-021 | Optional SMS is sent only to a verified, permitted destination under applicable consent and opt-out rules. |
| TCSN-AC-022 | SMS failure enters retry or failed-delivery administration without being treated as refusal. |
| TCSN-AC-023 | Duplicate provider webhooks do not duplicate notification state transitions. |
| TCSN-AC-024 | A missed welfare-sensitive task escalates according to its risk policy. |
| TCSN-AC-025 | Completing, canceling, or reassigning a task changes escalation behavior according to the state model. |
| TCSN-AC-026 | Delegation does not expose unrelated horse, owner, medical, billing, or facility records. |
| TCSN-AC-027 | A generated task identifies its source record and rule version. |
| TCSN-AC-028 | Changing the source schedule produces the defined update, cancellation, or review behavior. |
| TCSN-AC-029 | AI cannot silently assign a high-risk task. |
| TCSN-AC-030 | A personal reminder may be disabled without deleting an authoritative operational requirement. |
| TCSN-AC-031 | A mandatory reminder cannot be disabled through ordinary user preferences. |
| TCSN-AC-032 | Offline completion remains visibly pending until synchronization. |
| TCSN-AC-033 | Repeated sync does not duplicate completion, evidence, or notification. |
| TCSN-AC-034 | Conflicting offline completions enter reconciliation rather than silently overwriting one another. |
| TCSN-AC-035 | Revoked access prevents new offline retrieval and is reconciled on reconnect. |
| TCSN-AC-036 | Administrators can inspect failed delivery, retry history, recipient resolution, and channel evidence without reading unrelated content. |
| TCSN-AC-037 | Support correction preserves the original record and reason. |
| TCSN-AC-038 | Feature-flag disablement stops new external sync while preserving recoverable state and evidence. |
| TCSN-AC-039 | The first-release capability set excludes advanced workforce and AI scheduling optimization. |
| TCSN-AC-040 | The readiness section uses only permitted answer values and does not claim implementation or enrollment authority. |

---

## 30. Test Strategy and Test Matrix

Testing must include unit, integration, contract, security, privacy, permission, offline, recurrence, time-zone, DST, accessibility, load, failure, rollback, and adversarial tests.

| Test ID | Test |
| --- | --- |
| TCSN-TST-001 | Unit test task/event separation. |
| TCSN-TST-002 | Unit test assignment mode authorization. |
| TCSN-TST-003 | Negative test assignment without authority. |
| TCSN-TST-004 | Unit test completion evidence fields. |
| TCSN-TST-005 | Backdated completion and escalation preservation. |
| TCSN-TST-006 | Recurring occurrence edit isolation. |
| TCSN-TST-007 | This-and-following recurrence split. |
| TCSN-TST-008 | Series cancellation history preservation. |
| TCSN-TST-009 | Imported event classification. |
| TCSN-TST-010 | External deletion conflict handling. |
| TCSN-TST-011 | Calendar duplicate and idempotency test. |
| TCSN-TST-012 | Hard conflict block test. |
| TCSN-TST-013 | Soft conflict warning test. |
| TCSN-TST-014 | Unknown availability rendering test. |
| TCSN-TST-015 | Travel buffer conflict test. |
| TCSN-TST-016 | Timezone travel stability test. |
| TCSN-TST-017 | DST spring-forward nonexistent-time test. |
| TCSN-TST-018 | DST fall-back ambiguous-time test. |
| TCSN-TST-019 | Notification state-machine test. |
| TCSN-TST-020 | Acknowledgment versus completion negative test. |
| TCSN-TST-021 | Quiet-hours routine suppression test. |
| TCSN-TST-022 | Safety override test. |
| TCSN-TST-023 | Digest exclusion for urgent notice. |
| TCSN-TST-024 | Email fallback behavior test. |
| TCSN-TST-025 | SMS verified-destination test. |
| TCSN-TST-026 | SMS opt-out and mandatory-notice coexistence test. |
| TCSN-TST-027 | Provider webhook authenticity test. |
| TCSN-TST-028 | Duplicate webhook idempotency test. |
| TCSN-TST-029 | Retry and dead-letter test. |
| TCSN-TST-030 | Partial multi-recipient failure test. |
| TCSN-TST-031 | Risk-class escalation timing test. |
| TCSN-TST-032 | Escalation stop and transform test. |
| TCSN-TST-033 | Delegation least-privilege test. |
| TCSN-TST-034 | Generated-item provenance test. |
| TCSN-TST-035 | Source-change propagation test. |
| TCSN-TST-036 | AI high-risk assignment prohibition test. |
| TCSN-TST-037 | Personal versus mandatory reminder test. |
| TCSN-TST-038 | Offline completion queue test. |
| TCSN-TST-039 | Offline duplicate prevention test. |
| TCSN-TST-040 | Offline conflict reconciliation test. |
| TCSN-TST-041 | Offline revocation reconciliation test. |
| TCSN-TST-042 | Failed-delivery admin permission test. |
| TCSN-TST-043 | Feature-flag disable and rollback test. |
| TCSN-TST-044 | Cross-tenant isolation test. |
| TCSN-TST-045 | Machine validation of IDs, readiness values, section order, and traceability completeness. |

No capability is verified merely because a happy-path message sends or a calendar item appears.

---

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

---

## 33. Operational Readiness, Monitoring, and Support

Before operational readiness, EquineSync must establish:

- service ownership;
- notification and sync dashboards;
- alert thresholds;
- provider health monitoring;
- queue and dead-letter visibility;
- escalation-storm detection;
- support runbooks;
- user correction workflows;
- incident response;
- token revocation;
- backup and restore;
- reconciliation tools;
- manual recovery;
- status communication;
- maintenance windows;
- provider exit and substitution plans.

Initial stop conditions include cross-tenant disclosure, unauthorized assignment, lost completion evidence, uncontrolled notification storms, urgent-delivery suppression, irreconcilable sync corruption, and inability to revoke provider access.

---

## 34. Deployment, Rollout, Rollback, and Feature Flags

The release plan must define:

- environments;
- provider sandbox and production separation;
- migration order;
- feature flags;
- controlled cohort;
- notification-channel activation;
- SMS activation and spend limits;
- calendar-adapter activation;
- telemetry;
- stop conditions;
- rollback triggers;
- rollback method;
- data limitations;
- customer communication;
- post-deployment verification.

External synchronization and optional SMS must be independently disableable without disabling native tasks or in-app notifications.

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

- `TCSN-P1-001`: Exact authoritative source paths, hashes, and source-location anchors are not yet registered.
- `TCSN-P1-002`: Cross-PIA contracts for care, lessons, shows, facilities, providers, and safeguarding are not yet finalized.
- `TCSN-P1-003`: Provider ADRs for push, email, SMS, Google, Microsoft, and ICS infrastructure are not approved.
- `TCSN-P1-004`: Numeric service levels, retry schedules, escalation timings, retention periods, and offline limits are not approved.
- `TCSN-P1-005`: Machine-readable companion registers and full backward traceability are not yet created.
- `TCSN-P1-006`: No implementation, executed tests, operational evidence, or enrollment evidence exists.

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

---

## 40. Requirement Traceability Matrix

### 40.1 Current draft mapping

| Requirement family | Primary sections | Acceptance | Tests | Gate |
|---|---|---|---|---|
| `TCSN-REQ-001` to `010` | 4, 6, 11, 15 | `AC-001`, `AC-002`, `AC-040` | `TST-001`, `TST-009`, `TST-045` | Design and implementation authorization |
| `TCSN-REQ-011` to `024` | 9, 10, 13, 16, 17 | `AC-003` to `AC-007`, `AC-026`, `AC-037` | `TST-002` to `TST-005`, `TST-033`, `TST-042` | Implementation authorization and verification |
| `TCSN-REQ-025` to `048` | 12, 16, 21, 24, 25 | `AC-008` to `AC-016` | `TST-006` to `TST-018` | Verification |
| `TCSN-REQ-049` to `064` | 14, 18, 19, 22 | `AC-017` to `AC-025`, `AC-036` | `TST-019` to `TST-032`, `TST-042` | Verification and operational readiness |
| `TCSN-REQ-065` to `070` | 11, 27 | `AC-027` to `AC-031` | `TST-034` to `TST-037` | Implementation authorization |
| `TCSN-REQ-071` to `075` | 23 | `AC-032` to `AC-035` | `TST-038` to `TST-041` | Verification and operational readiness |
| `TCSN-REQ-076` to `080` | 8, 34, 37, 41, 42 | `AC-038` to `AC-040` | `TST-043` to `TST-045` | Release and enrollment |

### 40.2 Completion rule

Before a candidate is frozen for structured review, a machine-readable matrix must map every requirement to exact source location, Founder decision, workflow, entity, state transition, permission, acceptance criterion, test, evidence item, work package, dependency, finding, and gate.

---

## 41. Five Mandatory Readiness Questions

### 41.1 Engineering buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?

**Answer:** `PARTIALLY_SATISFIED`

**Basis:** The draft defines domain boundaries, 80 requirements, workflows, state models, permissions, acceptance criteria, tests, release scope, and twenty resolved Founder decisions. Engineering would still need exact source registration, approved cross-PIA contracts, provider ADRs, numeric operational targets, machine-readable companion registers, and implementation authorization.

**Gate effect:** Implementation authorization remains blocked.

### 41.2 Objective QA verification

**Question:** Can quality assurance determine objectively whether the capability works?

**Answer:** `PARTIALLY_SATISFIED`

**Basis:** The draft provides 40 acceptance criteria, 45 design tests, eight golden paths, and 32 adversarial scenarios. Executable fixtures, approved environments, provider sandboxes, numeric thresholds, implemented code, and preserved test evidence do not yet exist.

**Gate effect:** Verification and implementation authorization remain blocked.

### 41.3 Governance and MIAP traceability

**Question:** Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?

**Answer:** `PARTIALLY_SATISFIED`

**Basis:** Controlling source families, ownership rules, Founder decisions, requirement IDs, and internal mappings are identified. Exact source paths, hashes, page or line anchors, MIAP work-package references, source-conflict register, and complete forward-backward machine traceability remain pending.

**Gate effect:** Implementation authorization remains blocked.

### 41.4 Operational safety and recovery

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?

**Answer:** `NO`

**Basis:** No implementation, monitoring, provider readiness, alert testing, failed-delivery operations, backup and restore evidence, rollback evidence, incident runbook validation, support training, or production configuration exists.

**Gate effect:** Operational-readiness and enrollment gates remain blocked.

### 41.5 First-user enrollment readiness

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?

**Answer:** `NO`

**Basis:** The initial cohort and release boundary are conceptually defined, but no implementation, as-built reconciliation, executed test evidence, operational readiness, onboarding material, support path, verified rollback, or Founder enrollment disposition exists.

**Gate effect:** First-user enrollment is not authorized.

---

## 42. Review, Approval, Authorization, and Disposition

### 42.1 Required review sequence

1. source verification and registration;
2. domain review;
3. calendar and recurrence architecture review;
4. task and barn-operations boundary review;
5. communication and notice review;
6. permission and relationship review;
7. privacy and safeguarding review;
8. security and threat review;
9. offline and resilience review;
10. adapter and provider review;
11. operational-readiness review;
12. adversarial challenge;
13. machine validation;
14. golden-path review;
15. evidence-plan review;
16. Founder disposition.

### 42.2 Current requested disposition

`ACCEPT_V0_1_AS_INITIAL_DRAFT_FOR_INTERNAL_REVIEW_AND_REVISION`

### 42.3 Prohibited current dispositions

This draft is not eligible for:

- implementation authorization;
- implementation conformity;
- verification;
- operational readiness;
- release readiness;
- first-user enrollment.

---

## 43. Maintenance, Supersession, and Decommissioning

This PIA must be reviewed when:

- controlling governance changes;
- a dependent PIA changes materially;
- provider behavior changes;
- calendar standards or APIs change;
- notification incidents reveal a gap;
- users reveal material workflow failure;
- offline behavior changes;
- implementation materially drifts;
- a major release is proposed;
- the capability is retired.

Supersession must preserve predecessor files, decisions, findings, evidence, and exact change lineage.

Decommissioning must define replacement capability, user communication, export, retention, adapter shutdown, token revocation, queue drainage, feature-flag removal, code removal, evidence preservation, and final archival disposition.

---

# Documentary Authority Notice

`NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT`

This V0.1 draft is a controlled design artifact only.
