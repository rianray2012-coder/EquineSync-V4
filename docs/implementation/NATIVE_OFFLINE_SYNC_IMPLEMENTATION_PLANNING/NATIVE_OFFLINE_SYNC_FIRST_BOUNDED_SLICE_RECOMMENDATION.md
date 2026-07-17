# Native Offline Synchronization First Bounded Slice Recommendation

## Recommended Included Scope

Task inclusion is controlled by a server-owned workflow policy classification,
not by collection name, title text, UI category, or client assertion. Only tasks
explicitly classified `LOW_RISK_TASK_V1` may enter the first slice. Eligible
examples are administrative reminders, documentation follow-up, and
non-safety facility chores. Any unclassified task is online-only.

| Workflow | First-slice tier | Decision and reason |
| --- | --- | --- |
| Task creation | Tier 4 | Include `LOW_RISK_TASK_V1` only in local/test after the existing `client_request_id` contract and server-owned policy classification are verified through the new outbox. |
| Task completion | Tier 4 | Include `LOW_RISK_TASK_V1` only; existing `client_completion_id` provides a useful idempotency baseline. Preserve explicit pending state until canonical receipt. |
| Task skip | Tier 4 | Include with required reason and canonical rejection handling. |
| Approved bulk task completion | Tier 4 | Include only with per-task outcomes and no all-or-nothing success claim after partial failure. |
| Task update | Tier 3 initially; Tier 4 only after contract upgrade | Permit durable local proposal. Replay requires source revision plus operation idempotency; the current patch route has revision comparison but no complete replay identity. |
| QuickAdd draft persistence | Tier 2 | Include scoped draft persistence only. Do not convert generic QuickAdd submissions into queued canonical mutations. |
| Routine daily-care entry | Tier 2 only | Permit local draft after domain and field minimization review. Do not replay until care semantics and safety classification are approved. |
| Local mutation status | Supporting capability | Include explicit local, pending, syncing, canonical, conflict, rejected, blocked, and purged states. |
| Reconnect status | Supporting capability | Include truthful online/reconciling/blocked state without implying background synchronization. |
| Deterministic retry | Supporting capability | Include bounded foreground retry with idempotency and permission revalidation. |
| Queue inspection and recovery | Supporting capability | Include user-owned summary and safe retry/discard controls; no raw sensitive export or support mutation authority. |

## Explicitly Excluded

Medication, medication schedules, allergies, emergency instructions and contacts,
incidents, injuries and treatment, horse location changes, feed-plan changes,
transfers, ownership/custody/facility changes, financial transactions, agreements,
destructive deletion, permissions, roles, providers, public synchronization,
attachments, and external notifications are excluded.

Tasks that wrap or reference feeding, turnout, medication, health monitoring,
incidents, injuries, emergency response, horse location, transport, transfer,
permissions, agreements, billing, or provider work are excluded regardless of
their storage collection or UI label.

These workflows carry safety, legal, privacy, authority, financial, identity, or
external-effect risk that the first slice cannot resolve. RF31 remains separate.

## Data Boundary

The first slice uses synthetic data in local/test environments. Task projections
contain only stable IDs, short labels required for the workflow, revision,
status, assignment reference, due time where needed, and permission-safe display
fields. No medical, guardian/minor, financial, provider-private, legal,
relationship-authority, or broad horse-profile fields are stored.

## Acceptance Boundary

The first slice is a recommendation, not approval. Founder decisions are still
required for scope, platforms, persistence technology, feature flags, schema,
device matrix, P2 timing, and phase entry.
