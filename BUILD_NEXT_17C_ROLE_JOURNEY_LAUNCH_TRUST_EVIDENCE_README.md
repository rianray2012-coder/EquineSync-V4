# Build-Next-17C - Role Journey Launch Trust Evidence

Status: Codex-reviewed and locked; BN17D follow-up required.

Date: 2026-07-04

## Purpose

BN17C is an evidence-only launch-trust pass after locked BN17A and BN17B.
It verifies the current role journey shape without adding product behavior.

BN17C does not build new features. It records where the current code is clean,
where it is safe enough to preserve, and where BN17D must perform narrow
cleanup before founder launch acceptance.

## Scope

Evidence captured:

- Role dashboard route taxonomy.
- Post-login route resolver behavior.
- Role-specific navigation surfaces.
- Owner, guardian, rider, and service-provider dashboard safety.
- Admin Portal separation.
- Backend scoping surfaces for horses, HorseOps owner projections, and billing.
- Production-facing copy scan.
- Feature-shell exposure scan.
- Direct-route launch-trust findings.

Files changed:

- `outputs/bn17c_role_journey_launch_trust_evidence.md`
- `docs/LAUNCH_TRUST_CURRENT_PLAN.md`
- `docs/LAUNCH_TRUST_MASTER_FIX_LIST.md`
- `backend/tests/test_build_next_17c_role_journey_launch_trust_evidence.py`
- `memory/PRD.md`
- `BUILD_NEXT_17C_ROLE_JOURNEY_LAUNCH_TRUST_EVIDENCE_README.md`

## Main Result

The BN17A/BN17B role-dashboard split is holding:

- `/dashboard/facility`
- `/dashboard/manager`
- `/dashboard/staff`
- `/dashboard/trainer`
- `/dashboard/owner`
- `/dashboard/guardian`
- `/dashboard/rider`
- `/dashboard/service-provider`

Each route is role-gated at the frontend route level.

BN17C also found that several older product routes are still plain protected
routes rather than role/capability-gated routes. Backend scoping protects many
data paths, but launch-trust direct URL behavior should be cleaned up before
founder acceptance.

## Lock Note

BN17C is Codex-reviewed and locked as the post-BN17B evidence record.
It does not clear launch by itself. The lock preserves the findings and opens
BN17D as the next targeted cleanup phase for direct-route gates, production
copy, feature-shell classification, and follow-up role/scoping evidence.

## BN17D Required Follow-Up

BN17D should be a narrow cleanup phase for:

1. Direct-route role/capability gates on legacy product routes such as
   `/horses`, `/owners`, `/riders`, `/feed`, `/inventory`, `/incidents`,
   `/messaging`, `/settings`, `/today`, and related operational pages.
2. Production copy cleanup for dev-mode or later-phase language that appears
   in product UI source.
3. Feature-shell exposure classification: keep, hide, relabel, or move to a
   readiness/setup state.
4. Owner/service-provider direct URL safety review for all-horse, owner-list,
   billing, staff schedule, report, and admin-like surfaces.

## Strict Non-Scope

- No backend route/schema/auth/permission/privacy behavior changes.
- No frontend behavior fixes.
- No billing, Stripe, Resend, DocuSign, Text/SMS, Admin Portal, HorseOps,
  seed, UAT, landing-page, founder-accepted, pilot, or public-launch changes.
- No new workflow engines.

## Verification

Run:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_16b_setup_readiness_contract.py \
  backend/tests/test_build_next_16c_frontend_route_separation.py \
  backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py \
  backend/tests/test_build_next_17b_role_intake_split.py \
  backend/tests/test_build_next_17c_role_journey_launch_trust_evidence.py -q
```

Package:

`outputs/build_next_17c_role_journey_launch_trust_evidence.zip`
