# Workflow Register

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

### 11.1 Material business rules

1. A task, event, schedule, notification, acknowledgment, escalation, instruction, relationship, permission, and financial obligation are distinct records.
2. No calendar event or task creates medical, legal, financial, safeguarding, ownership, employment, guardian, or professional authority.
3. The substantive source domain controls the meaning of generated work.
4. Task assignment and assignment acceptance are distinct.
5. Acknowledgment, acceptance, start, completion, exception, and approval are distinct.
6. Direct assignment is valid only when the assigning actor has current authority.
7. Delegation is narrower than the delegator's authority and ends when its source authority ends.
8. Historical completion and recurrence occurrences are immutable except through attributed correction or supersession.
9. Backdating never erases the original due time, entry time, or escalation history.
10. Recurrence edits require an explicit occurrence scope.
11. External calendars are adapters and projections, not automatic owners of EquineSync truth.
12. An external deletion cannot silently destroy an authoritative EquineSync record.
13. Unknown availability is not free availability.
14. Hard conflicts fail closed absent an authorized and evidenced override.
15. Time-zone display may change; authoritative event time may not silently change.
16. Notifications do not mutate the underlying task or event unless a separately authorized command succeeds.
17. Quiet hours may suppress routine communication but not an authorized mandatory or safety-critical message.
18. A failed delivery is not a refusal, acceptance, acknowledgment, or completion.
19. Optional SMS is not the sole required channel for ordinary operation or mandatory evidence.
20. SMS content uses the minimum necessary information and a verified permitted destination.
21. Opting out of optional SMS does not disable mandatory in-app notices or other lawfully required channels.
22. Provider callbacks are untrusted until authenticated, validated, and idempotently applied.
23. Retries must not duplicate task, occurrence, delivery, or escalation side effects.
24. Escalation follows task risk, grace period, operational hours, coverage, and current state.
25. Acknowledgment alone cannot close a missed-task escalation unless the policy expressly defines an acknowledgment-only obligation.
26. Automated task creation requires a versioned rule and source record.
27. AI cannot independently create, assign, suppress, or resolve a consequential task.
28. Offline execution may use only previously authorized data and must expose unsynchronized state.
29. Irreconcilable offline conflicts enter review rather than last-write-wins.
30. Bulk actions re-evaluate authorization and validation for every item.
31. Task dependency cycles are prohibited.
32. RSVP or attendance response does not create authority, contract, payment obligation, or task completion.
33. Availability details are permission-filtered and may be represented as busy without revealing the event.
34. Notification templates are versioned, channel-specific, locale-aware, and preserved with each send.
35. Feature flags cannot bypass permission, evidence, safeguarding, retention, or audit controls.
36. Provider disablement must preserve native operation and recoverable queued state.
37. Seed and test data must be synthetic or approved and cannot silently enter production.
38. Migration and reconciliation are repeatable, dry-run capable, and evidence-producing.
39. Support correction preserves original records and cannot impersonate the original actor.
40. Documentary readiness does not create implementation, deployment, provider activation, production, or enrollment authority.

The controlled requirement register for this strengthened candidate contains 120 requirements.

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

### 11.2 Strengthened requirement additions

| Requirement ID | Requirement |
| --- | --- |
| TCSN-REQ-081 | Task dependencies SHALL form a directed acyclic graph; cycle creation SHALL be rejected with an explainable result. |
| TCSN-REQ-082 | Tasks SHALL support parent, child, checklist, blocking, blocked-by, and informational linkage without collapsing independent completion evidence. |
| TCSN-REQ-083 | Bulk assignment, rescheduling, completion, cancellation, and notification actions SHALL re-evaluate authorization and validation for each affected record. |
| TCSN-REQ-084 | Task, schedule, notification, and escalation templates SHALL be versioned; issued records SHALL preserve the exact version used. |
| TCSN-REQ-085 | Cancellation SHALL require scope, authority, reason, effective time, affected future occurrences, and notification treatment. |
| TCSN-REQ-086 | Calendar invitations SHALL support invited, tentative, accepted, declined, waitlisted, canceled, and no-response states. |
| TCSN-REQ-087 | RSVP, attendance, acceptance, assignment, payment, consent, and professional approval SHALL remain distinct. |
| TCSN-REQ-088 | Capacity and waitlist behavior SHALL be deterministic, permission-aware, auditable, and separate from payment or eligibility truth. |
| TCSN-REQ-089 | Availability queries SHALL return the minimum necessary result and MAY show busy or unavailable without revealing restricted event details. |
| TCSN-REQ-090 | Material schedule changes SHALL identify affected participants and resources and SHALL trigger policy-based update or cancellation notices. |
| TCSN-REQ-091 | Notification templates SHALL be versioned by communication class, channel, locale, tenant configuration, and effective period. |
| TCSN-REQ-092 | Channel rendering SHALL redact or transform content according to destination sensitivity, preview risk, recipient authority, and device context. |
| TCSN-REQ-093 | Every mandatory communication SHALL have an accessible supported fallback when the primary presentation is unusable. |
| TCSN-REQ-094 | Notification deduplication SHALL use a stable correlation key and SHALL preserve evidence of suppression or coalescing. |
| TCSN-REQ-095 | Rate limits, escalation ceilings, per-recipient caps, and circuit breakers SHALL prevent notification or retry storms. |
| TCSN-REQ-096 | SMS SHALL be sent only to a verified telephone destination with a recorded permitted-purpose and preference state. |
| TCSN-REQ-097 | Optional SMS SHALL support opt-out, preference change, destination correction, and re-verification without suppressing other required channels. |
| TCSN-REQ-098 | SMS SHALL NOT be the sole channel for a mandatory operational record when delivery evidence or user access requires another authoritative surface. |
| TCSN-REQ-099 | SMS content SHALL use minimum necessary information, avoid sensitive previews where feasible, and use secure authenticated links for detail. |
| TCSN-REQ-100 | SMS activation SHALL support tenant and platform spend caps, volume alerts, abuse controls, and immediate provider or feature disablement. |
| TCSN-REQ-101 | The capability SHALL emit service, queue, delivery, sync, offline, conflict, escalation, and permission telemetry with tenant-safe dimensions. |
| TCSN-REQ-102 | Service-level objectives and error budgets SHALL be versioned and linked to release scope, alerting, and stop conditions. |
| TCSN-REQ-103 | Alerts SHALL distinguish user-impacting failure, provider failure, backlog, data-integrity risk, security risk, and expected degraded mode. |
| TCSN-REQ-104 | Provider health SHALL be evaluated separately from EquineSync health and SHALL never be represented as native-system success. |
| TCSN-REQ-105 | Synthetic checks SHALL continuously exercise native task, notification, adapter, and recovery paths without using real user secrets or sensitive data. |
| TCSN-REQ-106 | Authorized administrative tools SHALL support inspect, replay, suppress, correct, reassign, reconcile, revoke, and export-evidence actions with least privilege. |
| TCSN-REQ-107 | Support correction SHALL preserve the original record, correction reason, support actor, approval where required, and affected downstream state. |
| TCSN-REQ-108 | Incident handling SHALL define severity, owner, acknowledgment target, containment, communication, recovery, evidence, and post-incident review. |
| TCSN-REQ-109 | Backup and restore SHALL preserve task, event, recurrence, completion, notification, escalation, adapter, audit, and configuration consistency. |
| TCSN-REQ-110 | Provider exit SHALL support credential revocation, data export where applicable, queue drainage, adapter disablement, replacement, and evidence preservation. |
| TCSN-REQ-111 | Every evidence item SHALL identify producer, date, environment, code version, PIA version, requirements, tests, result, limitations, checksum, custodian, and retention location. |
| TCSN-REQ-112 | Evidence indexes and manifests SHALL be machine-validatable and SHALL exclude unredacted secrets and unnecessary sensitive data. |
| TCSN-REQ-113 | Every requirement SHALL have a release classification and SHALL identify the gate at which it becomes mandatory. |
| TCSN-REQ-114 | External calendar sync and optional SMS SHALL default off in production until their separate activation evidence and Founder-authorized release scope exist. |
| TCSN-REQ-115 | Rollback SHALL preserve accepted user actions and evidence or explicitly identify any non-reversible data limitation before rollout. |
| TCSN-REQ-116 | Migration SHALL support inventory, dry run, deterministic mapping, exception quarantine, repeatability, rollback, and reconciliation evidence. |
| TCSN-REQ-117 | Seed and test data SHALL be synthetic or explicitly approved, visibly labeled, isolated by environment, and removable without affecting authoritative records. |
| TCSN-REQ-118 | Legacy recurrence and notification rules SHALL be mapped by explicit versioned transformation and SHALL not silently change authoritative time semantics. |
| TCSN-REQ-119 | Migration and reconciliation SHALL produce affected-record, unresolved-exception, duplicate-candidate, permission, and downstream-reference reports. |
| TCSN-REQ-120 | No migration, seed, provider, feature-flag, or configuration activity SHALL create implementation or production authority absent the applicable gate disposition. |

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

### 20.1 Evidence-production plan

| Evidence family | Evidence IDs | Produced by | Minimum content | Required gate |
|---|---|---|---|---|
| Documentary validation | `TCSN-EV-DOC-*` | PIA tooling or reviewer | Section order, ID uniqueness, links, answer vocabulary, checksums | Design approval |
| Requirement and traceability | `TCSN-EV-TRC-*` | Implementation governance | Forward and backward requirement links | Implementation authorization |
| Unit and contract tests | `TCSN-EV-TST-*` | Engineering and QA | Versioned output, environment, code and PIA versions | Verification |
| Permission and security | `TCSN-EV-SEC-*` | Security reviewer or test harness | Positive and negative access results, tenant isolation | Verification |
| Golden paths | `TCSN-EV-GP-*` | QA | Reproducible fixtures, steps, results, screenshots or traces | Verification and enrollment |
| Adversarial review | `TCSN-EV-ADV-*` | Segregated reviewer | Threat, abuse, failure, and misuse results | Design and verification |
| Notification providers | `TCSN-EV-NOT-*` | Integration QA | Send, delivery, failure, retry, opt-out, fallback, cost controls | Provider activation |
| Calendar adapters | `TCSN-EV-CAL-*` | Integration QA | Sync, conflict, revocation, deletion, duplicate, recovery | Adapter activation |
| Offline and reconciliation | `TCSN-EV-OFF-*` | Mobile QA | Queue, reconnect, conflict, revocation, duplicate prevention | Verification |
| Operations | `TCSN-EV-OPS-*` | Operations | Monitoring, alert, runbook, incident, support, restore, rollback | Operational readiness |
| Enrollment rehearsal | `TCSN-EV-ENR-*` | Founder and operations | Cohort, onboarding, support, stop, rollback, final disposition | First-user enrollment |

Evidence must demonstrate the actual version and environment tested. A plan, mockup, draft, or passing demonstration is not runtime evidence.

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


### 29.1 Strengthened acceptance additions

| Acceptance ID | Acceptance Criterion |
| --- | --- |
| TCSN-AC-041 | A task dependency cycle is rejected without altering existing valid dependencies. |
| TCSN-AC-042 | Bulk task action applies only to items for which the actor passes per-record authorization and returns item-level results. |
| TCSN-AC-043 | RSVP acceptance does not create assignment, payment, consent, or professional authority. |
| TCSN-AC-044 | An availability request may return busy without revealing a restricted title, horse, minor, location, or participant. |
| TCSN-AC-045 | A material schedule change sends versioned updates to the policy-defined affected recipients and resources. |
| TCSN-AC-046 | A notification record preserves the exact template version, locale, channel rendering, and redaction policy used. |
| TCSN-AC-047 | An optional SMS opt-out stops future optional SMS while preserving required in-app or other lawful mandatory communication. |
| TCSN-AC-048 | SMS volume or spend exceeding the configured limit blocks or pauses additional optional sends and alerts an authorized operator. |
| TCSN-AC-049 | A provider outage is displayed as provider degradation and does not mark native tasks or notices successful. |
| TCSN-AC-050 | A P0 or P1 operational condition generates the defined alert and incident record within its target. |
| TCSN-AC-051 | Backup restore reproduces linked task, event, occurrence, completion, notification, escalation, and audit relationships without orphaning. |
| TCSN-AC-052 | Provider exit revokes credentials and disables new sends or sync while preserving native records and evidence. |
| TCSN-AC-053 | A migration dry run produces no authoritative mutation and yields deterministic reconciliation reports. |
| TCSN-AC-054 | Synthetic seed data is visibly labeled, isolated, and cannot be mistaken for a real horse, person, task, or notification. |
| TCSN-AC-055 | The first-user gate yields a reproducible ready or not-ready determination without implying authorization before Founder disposition. |

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


### 30.1 Strengthened test additions

| Test ID | Test |
| --- | --- |
| TCSN-TST-046 | Dependency-cycle rejection test. |
| TCSN-TST-047 | Parent, child, blocker, and checklist independence test. |
| TCSN-TST-048 | Bulk per-record authorization and partial-result test. |
| TCSN-TST-049 | Invitation, RSVP, waitlist, and capacity state test. |
| TCSN-TST-050 | Availability privacy and busy-only projection test. |
| TCSN-TST-051 | Material schedule-change recipient-resolution test. |
| TCSN-TST-052 | Template version, locale, channel rendering, and redaction test. |
| TCSN-TST-053 | Correlation-key deduplication and suppression-evidence test. |
| TCSN-TST-054 | Notification rate limit, escalation ceiling, and circuit-breaker test. |
| TCSN-TST-055 | Optional SMS opt-out with mandatory-channel continuity test. |
| TCSN-TST-056 | SMS volume, spend-cap, abuse, and immediate-disable test. |
| TCSN-TST-057 | Service, queue, sync, and provider-health telemetry test. |
| TCSN-TST-058 | Alert target and incident-record creation test. |
| TCSN-TST-059 | Synthetic monitoring without real secrets or personal data test. |
| TCSN-TST-060 | Administrative replay, correction, and least-privilege test. |
| TCSN-TST-061 | Backup and relational restore rehearsal. |
| TCSN-TST-062 | Provider exit and credential revocation rehearsal. |
| TCSN-TST-063 | Migration dry-run repeatability and exception-report test. |
| TCSN-TST-064 | Synthetic seed-data isolation and cleanup test. |
| TCSN-TST-065 | First-user readiness decision rehearsal and evidence-index validation. |

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
