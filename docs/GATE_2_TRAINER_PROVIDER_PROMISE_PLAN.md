# Gate 2 Trainer and Provider Promise Plan

Date: 2026-08-29

Status: TP-1 and TP-2 Founder-accepted; TP-3 authorized for bounded implementation; no production launch authority.

## Purpose

Gate 2 public UI may describe EquineSync as the entry point for trainer and service-provider workflows, but it must not promise unrestricted client, horse, lesson, billing, messaging, payout, document, or multi-facility behavior before the governed product evidence supports those claims.

This plan keeps the current public funnel truthful while defining the work required to fully meet the expressed trainer/provider promise.

## Current Public Promise

| Audience | Gate 2 allowed wording | Current evidence boundary |
| --- | --- | --- |
| Trainer | Reviewed profile, trainer intake, assigned-work visibility, and a governed path toward client, horse, lesson, and program workflows. | RF9 supports trainer operating-center foundations and trainer intake, with explicit deferrals for package billing, haul-in/school-horse depth, multi-facility fluidity, and first-client UAT. |
| Service provider | Reviewed profile, grant-scoped horse context, provider operating-center access, and provider visit-note tools where approved. | RF10 supports explicit provider grants, provider operating center, direct horse/care scoping, and visit notes, with explicit deferrals for payments, legal documents, messaging delivery, external integrations, and broader cross-facility identity. |

## Gated Workstreams To Fully Meet The Promise

| Gate | Workstream | Required outcome | Proof required |
| --- | --- | --- | --- |
| TP-1 | Trainer signup review posture | Founder-approved policy for who can self-register, what fields are required, and what status unlocks trainer workspace access. | Admin-review route tests, signup copy tests, role-status transition tests, and screenshot proof of pending/approved/rejected states. |
| TP-2 | Trainer operating-center depth | Trainer home cleanly exposes only approved assigned horses, upcoming lessons, training plans, progress notes, and action queues. | Backend allow/deny tests for trainer-owned vs unrelated records, frontend route tests, and seeded UAT scenarios. |
| TP-3 | Trainer client and lesson workflows | Client/session language becomes true with governed lesson scheduling, owner-visible summaries, and stable trainer/horse/rider IDs. | Stable-ID persistence tests, cross-barn denial tests, owner-visibility tests, and UI proof across trainer and owner views. |
| TP-4 | Trainer billing/package truth | Any lesson packages, subscriptions, invoices, or payment claims are tied to RF12 billing evidence. | Stripe/catalog tests, no-price-mismatch tests, invoice/export tests, and production env readiness checks before launch claims. |
| TP-5 | Provider signup review posture | Founder-approved policy for provider categories, review fields, and first provider type for UAT. | Admin-review route tests, provider profile field tests, and seeded UAT for the approved provider category. |
| TP-6 | Provider grant operations | Barns can grant/revoke scoped provider access without exposing broad barn data. | Grant lifecycle tests, direct route denial tests, visit-note create/read tests, and audit evidence. |
| TP-7 | Provider communications, documents, and payment timing | Provider messaging, legal documents, invoices, payouts, and refunds remain deferred until their owning RF gates prove them. | RF12/RF13/RF14 evidence packages before any public claim expands beyond visit notes and grant-scoped context. |
| TP-8 | Premium UI proof | Trainer/provider public, signup, pending-review, approved, and dashboard states all use the Valencia palette and cohesive EquineSync language. | Visual review screenshots at desktop and mobile, brand drift search, parser check, production build, and accessibility smoke checks. |

## Stop Rules

- Do not claim broad multi-facility trainer or provider fluidity until account-membership and grant policy are implemented and tested.
- Do not claim provider payment, payout, refund, document, signature, or external integration readiness from RF10 alone.
- Do not claim trainer package billing or lesson-package payment readiness until RF12 proves it.
- Do not use brass, saddle, champagne, jet black, rustic western, or generic luxury language as product-facing brand direction.
- Equestrian imagery remains appropriate, but the Valencia palette is the overarching visual source of truth.

## Gate 2 Lock Requirements

- Public funnel copy avoids overclaiming current trainer/provider depth.
- Trust-strip copy describes reviewed paths, not a fully verified network.
- Auth/invite image alt text is equestrian but not generic luxury language.
- Touched UI uses `brand.*` or semantic tokens for new lavender/graphite accents.
- Parser checks pass.
- Full frontend build passes from a stable checkout or a documented non-code filesystem blocker is recorded.

## TP-1 and TP-2 Execution Notes

Date: 2026-08-29

TP-1 tightens the trainer review posture in signup and authenticated account banners. Trainer copy must say profile review, intake, and approved assigned-work visibility. It must not imply that a pending trainer can already access broad client, horse, lesson, billing, or multi-facility tools.

TP-2 upgrades the trainer home from intake-only perception to a read-only workspace summary backed by the RF9 trainer operating-center projection. The UI may show assigned-horse, upcoming-lesson, active-plan, recent-training, and rider-context counts or names returned by `/trainer/operating-center`; it must not link to private workflow surfaces or create assignments, lessons, students, documents, billing records, provider grants, or facility memberships from this screen.

TP-1/TP-2 are lockable only if:

- trainer signup and pending-review copy stay inside the reviewed/intake/assigned-work boundary;
- `RoleIntake` fetches `/trainer-intake/profile` and `/trainer/operating-center`;
- trainer home exposes `trainer-review-posture`, `trainer-operating-summary`, and `trainer-intake-shell` test surfaces;
- the trainer section does not link to lessons, horses, billing, admin, staff, invites, checkout, subscriptions, forms/signatures, students, or arena schedule;
- focused backend/frontend source tests, parser checks, brand drift checks, and a stable-lane frontend build pass.

## TP-1 and TP-2 Verification Result

Date: 2026-08-29

Result: review-clean for the bounded TP-1/TP-2 scope.

- Focused trainer intake/source test passed: `backend/tests/test_build_next_13g_trainer_intake_shell.py` reported 11 passed.
- Gate drift search passed for overclaim language, old Equine Sync naming, `equine-champagne`, generic luxury alt text, and broad verification claims in the scoped files.
- Parser check passed for the touched frontend files.
- Stable-lane production frontend build passed in `/Users/rianray/LocalDev/EquineSync-V4-gate2-clean-noncloud/frontend`.
- Earlier broader RF9 pytest collection in the cloud-backed checkout was not used as lock evidence because that environment stalled during pytest import; that caveat is superseded for the RF9/TP selected suite by the stable-lane proof recorded under TP-3 below.

Founder acceptance:

- On 2026-08-29, Founder accepted TP-1 and TP-2.
- This acceptance locks the bounded trainer signup review posture and trainer operating-center summary work as review-clean.
- This acceptance does not authorize production deployment, public-launch claims, trainer billing/package truth, provider grants, broad multi-facility trainer fluidity, or live provider/account mutation.

## TP-3 Authorization and Execution Boundary

Date: 2026-08-29

Founder authorization:

- Founder authorized TP-3 after accepting TP-1 and TP-2.

Authorized TP-3 scope:

- Make trainer client/session language true through stable-ID lesson and training context.
- Surface owner-visible trainer lesson/training summaries only through the existing owner-safe horse ledger contract.
- Preserve owner, barn, trainer, horse, and rider privacy boundaries.

TP-3 stop rules:

- Do not expose private trainer notes, staff-only critique, rider names, unrelated horses, unrelated trainers, unrelated barns, billing, packages, documents/signatures, or multi-facility trainer context.
- Do not create a broad trainer client directory from this gate.
- Do not treat TP-3 as production deployment or public-launch authority.

## TP-3 Verification Result

Date: 2026-08-29

Result: review-clean for the bounded TP-3 source/build scope.

- Owner horse ledger summaries now include a read-only `training_summary` block for explicitly owner-visible trainer lessons, training logs, and active plans.
- The owner-facing projection requires the owned horse's `horse_id`, same `barn_id`, and explicit `owner_visible` or owner-shared visibility before trainer work can appear.
- Owner summaries omit private lesson rows, unrelated-horse rows, rider names, trainer/private notes, staff-only critique, plan staff notes, billing, packages, documents/signatures, and multi-facility context.
- Focused TP-3 owner-summary test passed with 2 tests.
- Focused TP-3 plus trainer-intake shell regression passed with 13 tests.
- Parser check passed for touched frontend files.
- Stable-lane production frontend build passed in `/Users/rianray/LocalDev/EquineSync-V4-gate2-clean-noncloud/frontend`.
- RF9/TP collection and selected execution now pass in the stable non-cloud checkout after rebuilding `backend/.venv` from `backend/requirements.txt` plus `backend/requirements-dev.txt`.
- Canonical RF9/TP evidence runner added at `scripts/run_rf9_tp_evidence.sh`; it refuses to use system Python and runs collection plus selected execution through `backend/.venv/bin/python`.
- Stable-lane collection proof: `backend/.venv/bin/python -m pytest --collect-only -q backend/tests/test_rf9_trainer_operating_center.py backend/tests/test_build_next_13g_trainer_intake_shell.py backend/tests/test_tp3_trainer_client_lesson_owner_summary.py` collected 21 tests in 3.51s.
- Stable-lane RF9/TP execution proof: `backend/.venv/bin/python -m pytest -q backend/tests/test_rf9_trainer_operating_center.py backend/tests/test_build_next_13g_trainer_intake_shell.py backend/tests/test_tp3_trainer_client_lesson_owner_summary.py` passed 21 tests in 0.59s.
- Runner proof: `scripts/run_rf9_tp_evidence.sh` in `/Users/rianray/LocalDev/EquineSync-V4-gate2-clean-noncloud` collected 21 tests in 0.72s and passed 21 tests in 0.59s.
