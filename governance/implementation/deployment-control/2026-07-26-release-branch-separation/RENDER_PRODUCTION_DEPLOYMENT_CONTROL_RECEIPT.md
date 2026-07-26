# RENDER_PRODUCTION_DEPLOYMENT_CONTROL_RECEIPT

**Receipt ID:** `ES-DEPLOYMENT-CONTROL-RENDER-2026-07-26-02`
**Service:** `equine-sync-api`
**Service ID:** `srv-d8uc4eraml3c73dd2mng`
**Verification timestamp:** `2026-07-26T13:46:48Z`
**Determination:** `RENDER_DEPLOYMENT_SOURCE_SEPARATED_TO_RELEASE_BRANCH`

## Current Render Service State

| Field | Verified value |
|---|---|
| Service type | `web_service` |
| Repository | `https://github.com/rianray2012-coder/EquineSync-V4` |
| Branch | `release/production` |
| Root directory | `backend` |
| Runtime | `python` |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn server:app --host 0.0.0.0 --port $PORT` |
| Auto deploy | `yes` |
| Auto deploy trigger | `checksPass` |
| Service URL | `https://equine-sync-api.onrender.com` |
| Custom production API domain | `api.equine-sync.com` |
| Region | `oregon` |
| Plan | `starter` |
| Instances | `1` |
| Project | `EquineSync` |
| Environment | `Production` |

## Current Live Render Deployment

Changing the Render service branch triggered a service-update deployment from the release branch.

| Field | Verified value |
|---|---|
| Deploy ID | `dep-d9j0t73eo5us73alr3a0` |
| Status | `live` |
| Trigger | `service_updated` |
| Commit SHA | `92e9ccae8695aa523181b4cfe60e554e6c5245bd` |
| Commit message | `Merge CGP-003 repository integration metadata ...` |
| Created | `2026-07-26T13:41:48.795664Z` |
| Started | `2026-07-26T13:41:48.75599Z` |
| Finished | `2026-07-26T13:44:07.937178Z` |

Previous backend deployment:

| Field | Value |
|---|---|
| Deploy ID | `dep-d9iuh3eq1p3s73fntqeg` |
| Commit SHA | `550b3b91fb030dcfc898b4935c07f1d9fc1d9449` |
| Status after retargeting | `deactivated` |
| Trigger | `new_commit` |

## Runtime Verification

| Probe | Result |
|---|---|
| `GET https://api.equine-sync.com/api/health/ready` | `200`, production health body, `database=connected`, `indexes_ensured=true` |
| `POST https://api.equine-sync.com/api/webhook/stripe` | `500`, `Stripe webhook signing is not configured.` |

The legacy Stripe webhook remains fail-closed while `STRIPE_WEBHOOK_SECRET` is absent. No secret value was read or disclosed.

## Drift Assessment

No Render service URL, custom production API domain, root directory, build command, start command, runtime, plan, or environment-variable value was changed under this verification.

## Non-Authorization Boundary

This receipt does not authorize production deployment beyond the branch-retargeting service update already recorded, a new product release, Stripe secret configuration, payment activation, money movement, database migration, pilot activity, enrollment, acceptance of retained failures, governance supersession, archival deletion, or M4 work.
