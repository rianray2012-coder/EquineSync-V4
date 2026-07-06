# RF9 Trainer Operating Center and Trainer Fluidity Plan

Date: 2026-07-06

Status: completed; RF9 is Codex-reviewed and locked.

## Purpose

RF9 should turn trainer-facing workflow from generic dashboard access into a
real operating center for lesson work, horse training work, assigned horses,
school/lesson-horse context, haul-in context, and trainer enrollment depth.
The gate must preserve RF1/RF2/RF7/RF8 trust boundaries: trainers only see
records they are allowed to operate on, and all new trainer workflow records
must link by stable IDs rather than display names.

## Entry Conditions

- RF8 is Codex-reviewed and locked.
- RF1 owner-safe and barn-scoped predicates remain locked.
- RF2 stable ID self-service predicates remain locked.
- RF5 enrollment path separation remains the public signup baseline.
- RF6 canonical-system decisions remain locked.
- RF7 owner/guardian/client portal safety remains locked.

## Strict Scope

RF9 may:

- inventory existing trainer routes, dashboards, enrollment path, lessons,
  training records, horse assignments, rider links, and haul-in/lesson package
  placeholders;
- add or harden trainer-specific source-of-truth predicates using stable
  `trainer_user_id`, `horse_id`, `rider_id`, `owner_user_id`, and
  `barn_id`/account context where the existing model supports it;
- separate lesson scheduling from horse training workflows where the current UI
  or backend conflates them;
- add trainer operating-center evidence, route tests, and frontend wiring when
  it stays inside existing app boundaries;
- document deferred trainer billing/package/payment truth for RF12 if not
  safely implemented here;
- document deferred multi-facility trainer fluidity if it needs account
  membership or grants beyond current schema.

RF9 must not:

- weaken owner/guardian privacy or expose staff/internal notes to clients;
- implement service-provider multi-barn grants, which remain RF10;
- implement broad billing/payment truth, Stripe changes, refunds, or package
  charging, which remain RF12 unless evidence-only;
- implement offline/native/mobile behavior, which remains RF15/RF16/BN22A;
- migrate Staff Tasks into Task Engine, which remains RF17 or a founder-approved
  follow-up;
- mark founder decisions accepted automatically;
- call external providers or mutate Stripe, Apple, Google, DocuSign, Resend,
  MongoDB Atlas, Vercel, Render, or UAT accounts.

## Target Workstreams

| Workstream | Goal | Evidence Required |
| --- | --- | --- |
| Trainer surface inventory | Map trainer dashboard, role home, routes, enrollment, lesson, training, rider, horse, and assignment surfaces. | Source scan with route/file references and RF0 finding mapping. |
| Trainer access predicates | Prove trainer-visible records are scoped by stable trainer/user/horse/rider/barn context. | Focused backend tests or proof rows for allowed and denied access. |
| Lessons vs training separation | Ensure lesson scheduling and horse training work are not treated as one generic workflow. | Source evidence and UI/API distinction, or explicit deferral row. |
| Trainer operating center UX | Provide a trainer-first workspace that exposes assigned horses, upcoming lessons, training plans, and action queues without leaking owner-only or staff-only content. | Frontend source evidence plus build/test proof. |
| Trainer enrollment depth | Harden trainer signup path beyond RF5 route selection. | Required-field inventory, review-gate evidence, and founder-decision rows for approval policy. |
| Multi-facility fluidity | Decide what can be safely supported now versus deferred to account-membership/grant work. | Explicit ready/blocked/deferred status and no overclaiming. |

## Acceptance Criteria

- RF9 report status is `ready` with zero blocker rows.
- Trainer workflows use stable IDs for trainer, horse, rider, owner, and barn
  context where records are created or filtered.
- Trainers cannot see unrelated barns, unrelated horses, unrelated owner data,
  guardian/minor restricted content, or staff-only notes.
- Lessons and horse training have clear separate workflow truth or an explicit
  founder-approved deferral.
- Trainer enrollment has a truthful public path, review posture, and required
  data inventory.
- Any billing/package, haul-in, school-horse, multi-facility, or assignment
  work not completed in RF9 is recorded as deferred with the owning future
  phase.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Prioritize trainer workflow order. | requires founder review | Choose first among lesson packages, horse training logs/plans, haul-ins, school horses, and multi-facility trainer context. |
| Decide trainer signup review posture. | requires founder review | RF5 kept trainer signup public but review-gated; RF9 should confirm approval and required-field policy. |
| Decide whether trainer package/billing truth belongs in RF9 or RF12. | requires founder review | Avoid overclaiming paid packages unless billing truth is implemented and tested. |
| Decide first-client trainer UAT scenarios. | requires founder review | Recommended: assigned-horse training update, lesson schedule, owner-visible training summary, and unrelated-horse denial. |

## Recommended Verification

- Focused RF9 tests.
- RF9 report generation with `--fail-on-blockers`.
- Any touched frontend build.
- Zip integrity and expected manifest check.
- `git diff --check`.
- Secret-shape scan.
