# Native Offline Synchronization Capability Tier Plan

## Tier Definitions

| Tier | Meaning |
| --- | --- |
| `TIER_0` | Online-only; no governed local projection or mutation. |
| `TIER_1` | Permission-safe offline view with expiry and purge. |
| `TIER_2` | Local draft only; no canonical claim or replay. |
| `TIER_3` | Durable local commit/proposal with explicit noncanonical state. |
| `TIER_4` | Offline mutation and replay under idempotency, revision, permission, conflict, and audit controls. |
| `TIER_5` | Safety-critical offline operation; separate domain and Founder authorization required. |

## Workflow Plan

| Workflow | Current | First phase | Future target | Prerequisites and risks | Approval |
| --- | --- | --- | --- | --- | --- |
| Server-classified `LOW_RISK_TASK_V1` creation | Tier 0 | Tier 4 local/test | Tier 4 | Storage, outbox, idempotency, field minimization, server-owned policy class | Founder slice approval |
| Server-classified `LOW_RISK_TASK_V1` completion/skip | Narrow Tier 4-like retry | Tier 4 governed local/test | Tier 4 | Preserve isolation, canonical receipt, partial outcomes, deny unclassified/safety tasks | Founder slice approval |
| Bulk task completion | Narrow Tier 4-like retry | Tier 4 local/test | Tier 4 | Per-item results, no false aggregate success | Founder slice approval |
| Task update | Tier 0 | Tier 3 | Tier 4 | Source revision, idempotency, conflict UI | Founder plus server contract approval |
| QuickAdd | Tier 2 session draft | Tier 2 | Domain-specific Tier 2-4 | Generic endpoints cannot share one mutation policy | Founder slice approval |
| Routine daily-care entry | Tier 0 | Tier 2 | Tier 4 or 5 by domain | Safety classification, staleness, qualified review | Domain/Founder gate |
| Task list projection | Tier 0 | Tier 1 after Phase 1 | Tier 1 | Retention, browser encryption limits, revocation | Privacy/security gate |
| Lessons/schedules | Tier 0 | Tier 0 | Tier 1-4 | RF29 identity, recurrence, attendance conflicts | Separate Calendar gate |
| Horse profile/Passport | Tier 0 | Tier 0 | Tier 1 selected fields | Field projection, medical and relationship privacy | Passport/Care Circle gate |
| Medication | Tier 0 | Tier 0 | Tier 5 only | Clinical safety, duplicate dose, lease, escalation | Separate safety Founder gate |
| Feed/turnout changes | Tier 0 | Tier 0 | Tier 4 or 5 | Plan revision, restrictions, conflict semantics | Barn operations/safety gate |
| Horse location | Tier 0 | Tier 0 | Tier 5 only | Timeline conflicts, custody, quarantine, safety | Separate safety Founder gate |
| Incident/injury | Tier 0 | Tier 0 | Tier 5 only | Emergency semantics, immutable evidence, privacy | Separate safety Founder gate |
| Attachments | Tier 0 | Tier 0 | Supporting Tier 2-5 | Encryption, resumable upload, orphan handling | Later attachment gate |
| Transfer/custody/ownership | Tier 0 | Tier 0 | Tier 0 unless RF31 authorizes | Legal authority and Passport continuity | RF31 only |
| Permission/role changes | Tier 0 | Tier 0 | Tier 0 | Canonical authorization cannot be device-created | Identity/Permission canon |
| Billing/refunds | Tier 0 | Tier 0 | Tier 0 | Financial truth and external effects | Financial gate |
| Agreements/consent | Tier 0 | Tier 0 | Tier 0 | Legal evidence and exact presentation | Agreement gate |
| Provider workflows | Tier 0 | Tier 0 | Separate decision | Grant scope, private data, external boundary | Provider gate |

No workflow enters Tier 5 under this plan.

Task collection membership, title keywords, or client-provided category never
establish tier eligibility. The canonical server policy class controls.
