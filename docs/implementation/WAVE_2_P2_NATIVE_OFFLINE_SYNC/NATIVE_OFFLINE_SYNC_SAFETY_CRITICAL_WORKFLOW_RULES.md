# Native Offline Sync Safety-Critical Workflow Rules

## Shared Controls

Every critical screen must show connectivity, last canonical synchronization time, source revision, local/canonical status, pending/conflict state, and whether the user is relying on stale data. Local acceptance is never labeled “synced.”

Critical entries are append-only, preserve original actor and observed time, require explicit acknowledgment of stale source data, and receive prioritized synchronization. Rejection or conflict remains visible until resolved.

## Workflow Rules

| Workflow | Required offline safeguards |
| --- | --- |
| Medication administration | Qualified capability lease; horse/medication identity confirmation; planned dose and last-sync age; duplicate-dose window check; immutable administration event; no order edits; mandatory reconciliation. |
| Allergies and emergency instructions | Encrypted read-only minimal projection; prominent age; emergency source and contact; no stale edit promoted automatically. |
| Feeding | Show plan revision and age; record delivered amount as observation; changed plan conflicts require supervisor review. |
| Turnout | Record observation and location transition; warn on stale restrictions, quarantine, injury, weather, or medical hold; impossible overlap enters conflict. |
| Horse location | Require horse and location stable IDs; no name matching; preserve timeline; never silently overwrite a newer assignment. |
| Incident/injury | Permit immediate timestamped observation; preserve media hashes; corrections additive; urgent escalation guidance remains available without claiming delivery. |
| Restricted/quarantine state | Read-only cached warning may remain; changing restriction offline is prohibited. |
| Ownership, custody, transfer | Offline prohibited; no local relationship claim changes authority. |

## Staleness

Staleness thresholds must be set by domain policy and approved in a future gate. Until then, safety-critical offline capability remains disabled. The UI must not use a generic green success state for aged or pending data.

## Escalation

Offline entry cannot promise notification delivery. The app must distinguish “recorded on this device” from “recipient notified.” Emergency UI must provide approved non-app escalation instructions appropriate to the facility and role.

## Review Qualifications

- Medication conflicts: clinically authorized reviewer.
- Location/quarantine conflicts: facility authority with required health escalation.
- Feed/turnout exceptions: assigned supervisor or authorized care lead.
- Incident corrections: authorized operational reviewer; original observation retained.

## Fail-Closed Conditions

Critical offline entry is unavailable when horse identity is ambiguous, required projection is absent or expired, device storage is not durable, encryption/key access fails, actor/barn/session cannot be proven, or the operation would create authority rather than record an observation.

