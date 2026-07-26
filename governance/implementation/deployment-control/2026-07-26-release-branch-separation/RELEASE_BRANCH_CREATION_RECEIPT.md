# RELEASE_BRANCH_CREATION_RECEIPT

**Receipt ID:** `ES-DEPLOYMENT-CONTROL-RELEASE-BRANCH-2026-07-26-02`
**Repository:** `rianray2012-coder/EquineSync-V4`
**Integration branch:** `integrate-emergent-final-zip`
**Production release branch:** `release/production`
**Verification timestamp:** `2026-07-26T13:46:48Z`
**Determination:** `RELEASE_BRANCH_CREATED_AND_PROTECTED`

## Branch Heads

| Branch | Verified remote head |
|---|---|
| `integrate-emergent-final-zip` | `ff2748796bf858f49a3f85bad0578850e1deb846` |
| `release/production` | `92e9ccae8695aa523181b4cfe60e554e6c5245bd` |

`release/production` was originally created from `92e9ccae8695aa523181b4cfe60e554e6c5245bd`, the production baseline commit already promoted on Vercel and later deployed on Render during service retargeting.

## Baseline Treatment

The integration branch has advanced beyond the release branch after repository governance work. This is expected under the separated model:

- `integrate-emergent-final-zip` remains the protected integration/custody branch.
- `release/production` remains the protected production-release source branch.
- Integration merges no longer automatically become production releases.
- Production release requires a future explicit release PR into `release/production`.

## Release Branch Ruleset

| Field | Value |
|---|---|
| Ruleset name | `M1 CI required checks for release/production` |
| Ruleset ID | `19765462` |
| Enforcement | `active` |
| Target | `branch` |
| Included ref | `refs/heads/release/production` |
| Bypass actors | none |
| Current user can bypass | `never` |

Enabled controls:

- pull requests required;
- branch deletion blocked;
- non-fast-forward/force-push updates blocked;
- conversation resolution required;
- strict required status checks enabled;
- branch must be current before merge;
- merge commits remain allowed;
- required approving review count remains `0` for the present sole-maintainer model.

Required checks:

- `Backend suite is collectable`
- `Backend known-failure non-regression gate`
- `Frontend build`

## Integration Branch Ruleset

The integration branch remains protected by ruleset `19756139`, `M1 CI required checks for integrate-emergent-final-zip`, with the same required checks and no bypass actors.

## Non-Authorization Boundary

This receipt records branch custody and protection only. It does not authorize production deployment, a new product release, Stripe secret configuration, payment activation, money movement, database migration, pilot activity, enrollment, acceptance of retained failures, governance supersession, archival deletion, or M4 work.
