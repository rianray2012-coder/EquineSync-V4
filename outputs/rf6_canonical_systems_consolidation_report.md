# RF6 Canonical Systems Consolidation Report

Phase: `RF6`
Overall status: `ready`

## Canonical Decision Rows

| Domain | Status | Posture | Canonical System | Duplicate Surface | Evidence | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| operational_tasks | ready | canonicalize | Task Engine (`backend/task_engine.py`, `/task-templates`, `/tasks`, `task_events`) | Staff Tasks feature module (`staff_task_assignments`, `/staff-tasks`, `/staff-portal/tasks/...`) | Task Engine is the source-backed operational task lifecycle; Staff Tasks remains a parallel feature-module assignment surface. | RF8 should migrate or hide Staff Tasks and route staff work views through Task Engine semantics. |
| inventory | ready | alias_or_migrate | Inventory (`/inventory`, `db.inventory`, `frontend/src/pages/Inventory.jsx`) | Supply Inventory feature module (`supply_inventory_items`, `/supply-inventory`) | The canonical Inventory route writes `db.inventory`; Supply Inventory is a separate feature-module collection. | RF17 should alias, migrate, or hide Supply Inventory so operators do not split stock truth. |
| owner_updates | ready | deprecate_duplicate | Owner Updates lifecycle (`backend/routes/owner_updates.py`, `db.owner_updates`) | Owner media update feature-module records (`owner_media_updates`, `/feature-modules/owner-updates`) | Owner Updates has a lifecycle model and owner-safe reads; owner media updates remain a feature-module/media tracker. | RF7/RF17 should migrate or hide owner media updates and keep owner-facing trust flows on Owner Updates. |
| documents_signatures | ready | split_by_risk_until_rf14 | Document Signatures workflows (`DOCUMENT_TEMPLATES_COLLECTION`, `DOCUMENT_REQUESTS_COLLECTION`) | Forms & Signatures local records (`digital_forms`, `/feature-modules/forms-signatures`) | Document Signatures owns legal signature workflow contracts; Forms & Signatures remains local form/status tracking. | RF14 should consolidate legal signatures, local acknowledgements, signer rules, and signed-document storage truth. |
| billing_entitlements | ready | canonicalize | Account subscription records (`account_subscriptions`, `account_usage_limits`, `/subscriptions/*`) | Legacy membership endpoints and feature-module payment/recurring-billing records | Subscription checkout/webhook and provider-neutral account rows are entitlement truth; legacy membership checkout is sunset. | RF12 should keep owner invoices, payment records, recurring billing, refunds, and exports clearly separate from entitlement truth. |
| integration_readiness | ready | readiness_only | Integration readiness manifests (`integration_connections`, prepare/export/preview endpoints) | Provider-specific live sync expectations in readiness surfaces | Integration records are readiness/manifest evidence, not live provider sync claims. | Provider phases should implement live sync one provider at a time before stronger claims; RF17 can move readiness surfaces under Admin Setup. |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Accept Task Engine as the canonical operational task system. | requires founder review | RF6, RF8 | Staff Tasks should be migrated into Task Engine, hidden, or kept admin-readiness only until RF8. |
| Accept Inventory as the canonical supply/inventory system. | requires founder review | RF6, RF17 | Supply Inventory should become alias/migration source or move out of daily navigation. |
| Accept Owner Updates as canonical over owner media update feature-module records. | requires founder review | RF6, RF7, RF17 | Feature-module owner media updates should be migrated, hidden, or kept read-only until RF7/RF17. |
| Accept document-signatures workflows as canonical for legal signature workflows. | requires founder review | RF6, RF14 | Digital forms remain local acknowledgement/readiness records until RF14 consolidates storage and signer rules. |
| Accept account subscription records as canonical billing entitlement truth. | requires founder review | RF6, RF12 | Legacy membership endpoints and feature-module payment records must not be used as subscription entitlement truth. |
| Accept integration readiness as manifest/status evidence only until provider phases. | requires founder review | RF6, RF10, RF12, RF13, RF14, RF16, RF17 | Provider-specific live sync claims remain deferred unless a later phase proves them. |

## RF6 Boundary

- RF6 chooses source-of-truth posture for duplicated systems; it does not migrate data or hide routes.
- RF6 does not add schemas, auth changes, provider calls, billing mutations, frontend workflow expansion, or founder acceptance auto-marking.
- RF6 leaves implementation depth to RF7, RF8, RF12, RF14, RF17, and provider-specific later phases.
- Current launch claims must not imply the deprecated/readiness surfaces are canonical live workflows until later phases complete the migration or hide work.
