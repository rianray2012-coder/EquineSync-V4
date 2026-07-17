# Native Offline Synchronization Implementation Authority Matrix

Current package authority is planning-only.

| Activity | Codex now | Future Phase 0 | Future Phases 1-6 | Production/release |
| --- | --- | --- | --- | --- |
| Read repository/canon | Allowed | Allowed | Allowed within scope | N/A |
| Create planning docs/evidence | Allowed | Allowed | Allowed | Does not grant release |
| Verify accepted hashes | Allowed | Allowed | Required | Required but insufficient |
| Runtime/frontend/backend code | Prohibited | Prohibited unless future directive says otherwise | Only exact separately authorized phase | Prohibited absent production directive |
| Prototype/POC | Prohibited | Prohibited | Only if explicit later directive | Prohibited |
| Dependency/package change | Prohibited | Prohibited | Explicit phase authority required | Separate release gate |
| Local schema/store | Prohibited | Prohibited | Phase 1 only after approval | Production prohibited |
| Server schema/route | Prohibited | Prohibited | Separate explicit authority | Production prohibited |
| Migration/backfill | Prohibited | Prohibited | Synthetic/local only if explicit | Production prohibited |
| Replay/background worker | Prohibited | Prohibited | Foreground test harness only if explicit; background excluded | Prohibited |
| Safety-critical workflow | Prohibited | Prohibited | Separate Tier 5 gate only | Prohibited |
| RF31 transfer behavior | Prohibited | Prohibited | Prohibited | RF31 only |
| Provider/external effects | Prohibited | Prohibited | Prohibited | Separate provider gate |
| Production/customer data | Prohibited | Prohibited | Prohibited | Separate production authorization |
| Deployment/public launch/app stores | Prohibited | Prohibited | Prohibited | Separate Founder authorization |
| Wave 2 reopen/Wave 3 | Prohibited | Prohibited | Prohibited | Separate Founder directive |

## Current Flags

```text
IMPLEMENTATION_PACKAGE_OPENED: FALSE
IMPLEMENTATION_PERFORMED: FALSE
PROTOTYPE_CREATED: FALSE
RUNTIME_CODE_CHANGED: FALSE
SCHEMA_CHANGED: FALSE
MIGRATION_RUN: FALSE
PRODUCTION_AUTHORITY: FALSE
RUNTIME_ACTIVATION_AUTHORITY: FALSE
PROVIDER_ACTIVATION_AUTHORITY: FALSE
PUBLIC_LAUNCH_AUTHORITY: FALSE
WAVE_3_AUTHORITY: FALSE
```
