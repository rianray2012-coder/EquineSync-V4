# RF6 Canonical Systems Consolidation

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF6 chooses source-of-truth posture for duplicated EquineSync systems without
performing migration or feature expansion. The goal is to prevent future phases
from building on split truth.

## Canonical Decisions

| Domain | Canonical System | Duplicate / Noncanonical Surface | RF6 Decision |
| --- | --- | --- | --- |
| Operational tasks | Task Engine: `backend/task_engine.py`, `/task-templates`, `/tasks`, `task_events` | Staff Tasks feature module, `staff_task_assignments`, `/staff-tasks` | Task Engine is canonical. Staff Tasks should migrate into Task Engine semantics, become admin-readiness only, or be hidden in RF8/RF17. |
| Inventory | `/inventory`, `db.inventory`, `frontend/src/pages/Inventory.jsx` | Supply Inventory feature module, `supply_inventory_items`, `/supply-inventory` | Inventory is canonical. Supply Inventory should be aliased, migrated, or hidden before operators rely on it as a second stock ledger. |
| Owner updates | `backend/routes/owner_updates.py`, `db.owner_updates` | Feature-module owner media updates, `owner_media_updates`, `/feature-modules/owner-updates` | Owner Updates is canonical for owner trust lifecycle. Owner media updates should migrate or hide in RF7/RF17. |
| Documents and signatures | Document Signatures workflows, document templates, document requests | Forms & Signatures local records, `digital_forms` | Document Signatures is canonical for legal signature workflows. Digital forms remain local acknowledgement/readiness records until RF14 consolidation. |
| Billing entitlements | `account_subscriptions`, `account_usage_limits`, `/subscriptions/*` | Legacy membership endpoints, payment profile records, recurring billing feature records | Account subscription rows are entitlement truth. Legacy/payment feature records must not be treated as subscription truth. |
| Integration readiness | Integration readiness manifests, `integration_connections`, prepare/export/preview endpoints | Provider-specific live sync expectations | Readiness manifests are canonical for current setup status. Live provider sync remains later-phase work. |

## Boundaries

RF6 does not:

- migrate data;
- hide, redirect, or remove routes;
- add schemas, auth rules, permissions, provider calls, billing mutations, or
  frontend workflow expansion;
- mark founder decisions accepted;
- close RF7, RF8, RF12, RF14, RF17, or RF18.

## Founder Decisions

| Decision | Status | Phase |
| --- | --- | --- |
| Accept Task Engine as canonical over Staff Tasks. | requires founder review | RF6/RF8 |
| Accept Inventory as canonical over Supply Inventory. | requires founder review | RF6/RF17 |
| Accept Owner Updates as canonical over owner media updates. | requires founder review | RF6/RF7/RF17 |
| Accept Document Signatures as canonical for legal signature workflows. | requires founder review | RF6/RF14 |
| Accept account subscription records as billing entitlement truth. | requires founder review | RF6/RF12 |
| Accept integration readiness as manifest/status evidence only until provider phases. | requires founder review | RF6/RF10/RF12/RF13/RF14/RF16/RF17 |

## Evidence

Generated report:
`outputs/rf6_canonical_systems_consolidation_report.md`.

Review package:
`outputs/build_next_rf6_canonical_systems_consolidation.zip`.

## RF6 Lock Note

RF6 is Codex-reviewed and locked after a clean review. The generated report
status is `ready` with zero blocker rows.

The lock covers canonical source-of-truth decisions only. RF6 does not migrate
data, hide routes, redirect URLs, add schemas, change auth or permissions,
mutate billing, call providers, mark founder decisions accepted, or close RF7,
RF8, RF12, RF14, RF17, or RF18.
