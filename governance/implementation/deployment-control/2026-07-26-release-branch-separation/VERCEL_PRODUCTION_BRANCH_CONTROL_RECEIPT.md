# VERCEL_PRODUCTION_BRANCH_CONTROL_RECEIPT

**Receipt ID:** `ES-DEPLOYMENT-CONTROL-VERCEL-2026-07-26-02`
**Project:** `equine-sync-v4`
**Project ID:** `prj_qNmEiAxdYJ5KljPPy4Q08A6ZQMR5`
**Team:** `equine-sync`
**Team ID:** `team_xdaFjbJfYEb41JRP8FwT1akX`
**Verification timestamp:** `2026-07-26T13:46:48Z`
**Determination:** `VERCEL_PRODUCTION_BRANCH_TRACKING_SEPARATED`

## Production Branch Tracking

| Field | Verified value |
|---|---|
| Linked repository | `rianray2012-coder/EquineSync-V4` |
| Git production branch | `release/production` |
| Previous production branch | `integrate-emergent-final-zip` |
| Git deployments | `enabled` |
| Custom production-domain auto-assignment | `enabled` |
| Project updated timestamp | `2026-07-26T13:37:56.249Z` |

## Current Production Deployment

| Field | Verified value |
|---|---|
| Deployment ID | `dpl_5Egs1VhrzdUhyJBcKWJpBRDpGB9Z` |
| Deployment URL | `equine-sync-v4-q70i6ebvk-equine-sync.vercel.app` |
| Target | `production` |
| Ready state | `READY` |
| Ready substate | `PROMOTED` |
| Commit SHA | `92e9ccae8695aa523181b4cfe60e554e6c5245bd` |
| Original commit ref | `integrate-emergent-final-zip` |
| Created timestamp | `2026-07-26T11:17:48.195Z` |
| Ready timestamp | `2026-07-26T11:18:56.259Z` |

Production aliases remained:

- `app.equine-sync.com`
- `equine-sync-v4.vercel.app`
- `equine-sync-v4-equine-sync.vercel.app`
- `equine-sync-v4-git-integrate-emergent-final-zip-equine-sync.vercel.app`

## Integration Branch Validation

After production branch tracking was changed, the integration branch advanced to:

`ff2748796bf858f49a3f85bad0578850e1deb846`

Vercel created deployment `dpl_3SPMAwoVqbZM3Mn9Yb7YgE1AKvvc` for that integration commit with:

| Field | Value |
|---|---|
| Branch | `integrate-emergent-final-zip` |
| Commit SHA | `ff2748796bf858f49a3f85bad0578850e1deb846` |
| Target | `null` |
| Environment | `preview` |
| Ready state | `READY` |
| Created timestamp | `2026-07-26T13:50:15.023Z` |
| Ready timestamp | `2026-07-26T13:52:24.539Z` |

This confirms that commits to `integrate-emergent-final-zip` no longer qualify as Vercel Production deployments.

## Environment And Domain Drift

No Vercel domain, production alias, or environment-variable value was changed under this verification. Environment variable metadata was observed only by key, target, id, and timestamp; secret values were not read or disclosed.

Observed environment keys/targets remained:

- `REACT_APP_BACKEND_URL` for `production`
- `REACT_APP_BACKEND_URL` for `preview`
- `REACT_APP_STRIPE_PUBLISHABLE_KEY` for `production`
- legacy `Variables` entry for `production`

## Non-Authorization Boundary

This receipt does not authorize production deployment, a new product release, Stripe secret configuration, payment activation, money movement, database migration, pilot activity, enrollment, acceptance of retained failures, governance supersession, archival deletion, or M4 work.
