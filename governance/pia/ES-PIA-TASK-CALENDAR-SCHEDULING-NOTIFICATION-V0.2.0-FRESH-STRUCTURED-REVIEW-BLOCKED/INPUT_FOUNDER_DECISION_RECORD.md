# Founder Decision Record
## Task, Calendar, Scheduling, and Notification PIA

**Decision record ID:** `ES-TCSN-FDR-2026-07-22-01`  
**Founder:** `Rian Ray`  
**Decision date:** `2026-07-22`  
**Status:** `APPROVED_FOR_DOCUMENTARY_DESIGN_USE`  
**Implementation authority:** `FALSE`

## Decision summary

The Founder approved `TCSN-FD-001` through `TCSN-FD-009` and `TCSN-FD-011` through `TCSN-FD-020` as recommended. `TCSN-FD-010` was approved with one modification: optional SMS is included in the initial controlled scope.

## Approved decisions

| Decision | Approved direction |
|---|---|
| `TCSN-FD-001` | Use one cross-domain PIA while preserving distinct authoritative owners and inherited governance boundaries. |
| `TCSN-FD-002` | The underlying domain record controls substantive truth; the EquineSync calendar controls scheduling truth; the task record controls assignment and completion truth; the notification record controls delivery and acknowledgment evidence; external calendars do not automatically own EquineSync truth. |
| `TCSN-FD-003` | Tasks and events remain distinct. A task need not appear on a calendar, and an event need not create a task. |
| `TCSN-FD-004` | Support direct, acceptance-required, claimable, suggested, and emergency assignment modes. |
| `TCSN-FD-005` | Completion preserves actor, actual and entered times, context, instruction version, evidence, exception, offline state, synchronization, and correction history. |
| `TCSN-FD-006` | Late and backdated completion is permitted only with preserved timing, reason, actor, escalation history, and risk-based review. |
| `TCSN-FD-007` | Recurrence editing supports this occurrence, this and following, and entire future series without rewriting completed history. |
| `TCSN-FD-008` | Overdue work escalates through configurable risk classes rather than one universal timer. |
| `TCSN-FD-009` | Routine notifications may honor quiet hours; authorized urgent, welfare, safeguarding, legal, and emergency communications may override them with evidence. |
| `TCSN-FD-010` | Initial controlled notification scope includes in-app, push, email, digest, optional SMS, and an administrator-visible failed-delivery queue. Voice calling, WhatsApp or similar consumer channels, and automated emergency calling trees remain deferred unless separately authorized. |
| `TCSN-FD-011` | Acknowledgment is separate from assignment acceptance, consent, approval, and task completion. |
| `TCSN-FD-012` | Google and Microsoft may support authorized bidirectional synchronization; Apple begins with ICS; adapters remain provider-neutral; conflicts, deletion, duplication, failure, and revocation remain visible. |
| `TCSN-FD-013` | Use hard, soft, informational, and unknown-availability conflict classes with authorized, audited overrides. |
| `TCSN-FD-014` | Support offline task execution with visible unsynchronized state, attribution, idempotency, deterministic reconciliation, and least-privilege caching. |
| `TCSN-FD-015` | Delegation is limited by task type and authority and distinguishes reassignment, retained-responsibility delegation, substitute coverage, pool claim, emergency takeover, and supervisor override. |
| `TCSN-FD-016` | Other domain records may generate tasks or events only through explicit, versioned automation rules with source and authority provenance. AI may not silently create high-risk assigned work. |
| `TCSN-FD-017` | Consolidate routine notifications using grouping, digests, and duplicate suppression without hiding urgent or mandatory communications. |
| `TCSN-FD-018` | Personal reminders may be disabled; mandatory, operational, safety, safeguarding, welfare, or legal reminders are controlled by authorized policy rather than ordinary preference. |
| `TCSN-FD-019` | Preserve authoritative event time zone, facility time zone, user display zone, UTC, DST interpretation, and original entered time. Travel must not silently shift authoritative care schedules. |
| `TCSN-FD-020` | Initial controlled release includes native tasks, recurrence, assignment and acceptance, due windows, offline completion, evidence, exceptions, escalation, in-app, push, email, optional SMS, basic calendar views, and failed-delivery administration. Advanced optimization, voice trees, broad marketplace booking, autonomous AI schedules, and unrestricted multi-provider sync remain deferred. |

## Authority limitation

These approvals authorize documentary requirements and design assumptions only. They do not authorize implementation, schema creation, migration, deployment, provider production activation, production use, pilot enrollment, or first-user enrollment.
