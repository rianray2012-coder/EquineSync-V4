# Build-Next-17D - Role Journey Cleanup

Status: Codex-reviewed and locked.

Date: 2026-07-04

## Purpose

BN17D is the targeted cleanup phase opened by locked BN17C. It closes concrete
role-journey launch-trust findings without expanding the product surface.

No new product behavior.
No backend route/schema/auth/permission/privacy changes.

## Scope

Implemented:

- `BN17D-ROUTE-1`: added explicit frontend role gates to legacy product routes
  that were previously only login-protected inside `AppShell`.
- `BN17D-COPY-1`: cleaned production-facing dev, local-config, coming-soon,
  workflow-shell, and later-phase copy in the specific surfaces BN17C flagged.
- `BN17D-FEATURE-1`: classified exposed shells as either preserved,
  relabeled, or hidden from unsafe role navigation.
- `BN17D-SCOPE-1`: removed direct owner, guardian, unknown/default, and
  service-provider nav links into operational messaging until a role-specific
  messaging expansion exists.

Files changed:

- `frontend/src/App.js`
- `frontend/src/lib/roleNavigation.js`
- `frontend/src/components/onboarding/StaffStep.jsx`
- `frontend/src/components/NotificationPrefsCard.jsx`
- `frontend/src/pages/admin/AdminTopbar.jsx`
- `frontend/src/pages/FeatureWorkspace.jsx`
- `frontend/src/pages/FormsSignatures.jsx`
- `backend/tests/test_build_next_6_signature_connector.py`
- `backend/tests/test_build_next_17d_role_journey_cleanup.py`
- `docs/LAUNCH_TRUST_CURRENT_PLAN.md`
- `docs/LAUNCH_TRUST_MASTER_FIX_LIST.md`
- `outputs/bn17d_role_journey_cleanup_evidence.md`
- `memory/PRD.md`

## Direct Route Cleanup

The following legacy routes now use explicit BN17D role groups:

- `/today`
- `/horses`
- `/horses/:id`
- `/owners`
- `/riders`
- `/lessons`
- `/training`
- `/health`
- `/stall-rest`
- `/medications`
- `/turnout`
- `/feed`
- `/inventory`
- `/billing/success`
- `/incidents`
- `/messaging`
- `/settings`

Owner, guardian, rider, and service-provider dashboards remain their safe
dashboard shells. Operational messaging remains available to facility/admin,
manager, trainer, groom, and working-student roles only.

## Feature-Shell Classification

| Surface | BN17D action |
| --- | --- |
| Admin Portal search | Relabeled to neutral disabled `Search` placeholder. |
| Staff invite fallback | Preserved, but copy no longer exposes dev-mode, local env, or magic-link language. |
| Notification preferences | Preserved Inbox and Email delivery controls; future channels remain hidden until configured. |
| Generic feature workspace empty state | Relabeled from workflow-shell language to readiness-safe workspace copy. |
| Forms & Signatures provider readiness | Preserved readiness display; copy no longer references phases or later-phase sending. |
| Owner/guardian/provider Messaging nav | Hidden until role-specific messaging exists. |

## Strict Non-Scope

- No backend route/schema/auth/permission/privacy changes.
- No billing, Stripe, Resend, DocuSign, SMS/Text, Admin Portal capability,
  HorseOps, landing-page, seed, UAT account, founder-accepted, pilot, or
  public-launch changes.
- No new workflow engines.
- No provider-live proof. That remains BN18A.
- No production environment proof. That remains BN18B.
- No credentialed UAT acceptance. That remains BN18C/BN19.

## Verification

Completed locally:

- Focused BN6/BN16/BN17 source-level suite: 45/45 passed.
- Frontend production build: compiled successfully.
- Codex lock review: 45/45 focused tests passed; zip integrity passed.

Run:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_6_signature_connector.py \
  backend/tests/test_build_next_16b_setup_readiness_contract.py \
  backend/tests/test_build_next_16c_frontend_route_separation.py \
  backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py \
  backend/tests/test_build_next_17b_role_intake_split.py \
  backend/tests/test_build_next_17c_role_journey_launch_trust_evidence.py \
  backend/tests/test_build_next_17d_role_journey_cleanup.py -q
```

Package:

`outputs/build_next_17d_role_journey_cleanup.zip`

## Next Phase

After BN17D locks, proceed to BN18A provider-live proof.
