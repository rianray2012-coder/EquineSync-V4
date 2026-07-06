# RF9 Trainer Operating Center Report

Phase: `RF9`
Overall status: `ready`

## Status Rows

| Key | Area | Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| trainer_operating_center_endpoint | Trainer operating center API | ready | RF9 adds a read-only trainer operating-center endpoint, trainer-role scoped and product-facility gated. | RF18 should browser-smoke seeded trainer account scenarios. |
| lessons_training_trainer_id_scoped | Lesson and training stable trainer identity | ready | Trainer-created lessons/training stamp stable trainer IDs, trainer list reads are ID-scoped, and missing/cross-barn rider/horse references fail closed. | RF18 should add end-to-end trainer UAT with seeded cross-trainer denial cases. |
| training_plans_stable_ids | Training plans stable IDs | ready | New Training Plans require stable horse and trainer user IDs and stamp display names from trusted records. | RF17 can decide whether feature-module Training Plans remains pilot beta or becomes canonical trainer plan UI. |
| trainer_dashboard_not_generic | Trainer dashboard | ready | Trainer dashboard now renders a trainer-first operating center instead of the generic facility dashboard. | RF18 should capture trainer dashboard screenshots with seeded records. |
| trainer_intake_review_gate_retained | Trainer enrollment depth | ready | Trainer intake remains current-user only, trainer-role scoped, and setup-intent only; RF9 records review-gate decisions without auto-approving trainer accounts. | Founder should accept trainer signup review posture and required fields before broader public claims. |
| lessons_training_separate_workflows | Lessons versus horse training | ready | Lessons, training logs, and training plans remain distinct workflow surfaces in routing and trainer dashboard navigation. | RF18 should verify users understand the distinction during first-client UAT. |
| trainer_packages_billing_deferred | Trainer packages and billing | deferred | RF9 does not implement package charging, Stripe billing, refunds, discounts, or trainer package entitlement truth. | RF12 owns billing/payment truth unless founder explicitly reorders package billing work. |
| multi_facility_fluidity_deferred | Multi-facility trainer fluidity | deferred | RF9 uses current barn-scoped records; broad multi-facility trainer grants remain future account-membership/grant work. | RF10/RF18 should define provider-style grant semantics before broad multi-facility claims. |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Prioritize trainer workflow order. | requires founder review | RF9 | Choose first among lesson packages, horse training logs/plans, haul-ins, school horses, and multi-facility trainer context. |
| Decide trainer signup review posture. | requires founder review | RF9 | RF5 kept trainer signup public but review-gated; RF9 keeps the review posture documented. |
| Decide whether trainer package/billing truth belongs in RF9 or RF12. | requires founder review | RF9, RF12 | RF9 does not implement paid trainer packages or billing truth. |
| Decide first-client trainer UAT scenarios. | requires founder review | RF9, RF18 | Recommended scenarios: assigned-horse training update, lesson schedule, owner-visible training summary, and unrelated-horse denial. |

## RF9 Boundary

- RF9 hardens trainer-owned lessons, training logs, training plans, and the trainer dashboard using stable IDs.
- RF9 does not implement trainer package billing, Stripe changes, service-provider grants, broad multi-facility grants, native/offline behavior, or founder acceptance auto-marking.
- Current launch claims may say trainers have an ID-scoped operating-center read model for assigned work. They must not claim paid package billing, haul-in workflows, school-horse workflows, or broad multi-facility trainer fluidity are complete.
