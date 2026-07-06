# RF9 Trainer Operating Center and Trainer Fluidity

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF9 creates a real trainer operating-center foundation without expanding into
trainer billing packages, service-provider grants, or broad multi-facility
membership work.

## Completed Hardening

| Area | RF9 Status | Evidence |
| --- | --- | --- |
| Trainer operating-center API | ready | Adds `/trainer/operating-center`, scoped to trainer accounts, product facility gating, and stable trainer-owned lessons/training/plans/horses/riders. |
| Trainer directory | ready | Adds `/trainer/directory` for admin, barn manager, and trainer users so trainer selectors can use stable trainer IDs. |
| Lessons | ready | Trainer-created lessons stamp `trainer_id`; trainer lesson reads return only stable ID-linked trainer-owned records; missing/cross-barn rider or horse IDs fail closed. |
| Training logs | ready | Trainer-created training logs stamp `trainer_id`; trainer training reads return only stable ID-linked trainer-owned records; missing/cross-barn horse IDs fail closed. |
| Training Plans | ready | New training-plan creates require `horse_id` and `trainer_user_id`; backend stamps `horse_name` and `trainer_name` from trusted same-barn records. |
| Trainer dashboard | ready | `/dashboard/trainer` now renders a trainer-specific operating center instead of the generic facility dashboard. |
| Trainer intake | ready | Trainer intake remains current-user only, trainer-role scoped, review-gated setup intent; RF9 does not auto-create assignments or approve accounts. |

## Deferred or Founder-Decision Items

| Item | Status | Next Action |
| --- | --- | --- |
| Trainer package billing | deferred | RF12 owns billing/payment/package truth unless founder explicitly reorders it. |
| Haul-in and school-horse workflows | deferred | Founder should prioritize these against lessons and horse training before deeper implementation. |
| Multi-facility trainer fluidity | deferred | Broad multi-facility grants need account-membership/grant policy and UAT depth before claims. |
| Trainer first-client UAT | deferred | RF18 should run seeded trainer scenarios including unrelated-horse denial. |

## Founder Decision Rows

| Decision | Status | Phase |
| --- | --- | --- |
| Prioritize trainer workflow order. | requires founder review | RF9 |
| Decide trainer signup review posture. | requires founder review | RF9 |
| Decide whether trainer package/billing truth belongs in RF9 or RF12. | requires founder review | RF9/RF12 |
| Decide first-client trainer UAT scenarios. | requires founder review | RF9/RF18 |

## Launch Claim Boundary

Current launch/pilot claims may say trainers have an ID-scoped operating-center
read model for assigned work, plus stable-ID lesson/training/training-plan
creates for the RF9-covered workflows.

Do not claim:

- trainer package billing is implemented;
- Stripe trainer-package checkout or payment truth is complete;
- haul-in workflows are complete;
- school-horse workflows are complete;
- broad multi-facility trainer fluidity is complete;
- service-provider multi-barn grants are complete.

## Evidence

Generated report:
`outputs/rf9_trainer_operating_center_report.md`.

Review package:
`outputs/build_next_rf9_trainer_operating_center.zip`.
