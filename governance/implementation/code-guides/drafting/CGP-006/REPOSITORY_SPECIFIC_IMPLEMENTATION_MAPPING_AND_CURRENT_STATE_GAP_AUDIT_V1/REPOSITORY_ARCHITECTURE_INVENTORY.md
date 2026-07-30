
# Repository Architecture Inventory

## Observed Architecture

- Repository shape: split Python backend, React frontend, governance corpus, PIA portfolio, docs/canon, outputs, tests, and GitHub Actions.
- Backend runtime: FastAPI app assembled in `backend/server.py` with an `/api` router and `279` statically observed route decorators across backend route modules.
- Persistence: MongoDB via `backend/core/db.py`, with `92` production-code collection names observed by static scan.
- Frontend runtime: React app under `frontend/src`, route map in `frontend/src/App.js`, and `112` statically observed route lines.
- Mobile wrappers: Capacitor configuration and Android/iOS project directories under `frontend`.
- CI: `.github/workflows/ci.yml` defines backend collectability, backend known-failure non-regression, and frontend build jobs.
- Governance: Code Guide and PIA documentary sources live under `governance/implementation/code-guides`, `governance/pia`, and `governance/pia_portfolio`.

## Runtime Boundaries

Backend code owns server-side authentication, authorization, tenancy, billing/webhook, minor-safeguarding, audit, storage, and background processing decisions. Frontend route guards are user-experience controls and are not treated as server-side authorization proof.

## Data And Trust Boundaries

- Browser to backend API trust boundary: `frontend/src/lib/api.js` and route components call backend API paths.
- Auth trust boundary: JWT verification and user lookup occur in `backend/core/auth.py`; token claims are not accepted as the authoritative barn scope.
- Tenant trust boundary: `backend/core/tenancy.py` resolves and stamps `barn_id`; product routers are gated through strict or optional active-facility dependencies where wired.
- Platform-admin trust boundary: `backend/core/permissions.py` separates `platform_role` from barn-scoped `role`.
- External-provider boundary: Stripe, Resend, DocuSign, and S3/R2 code paths are repository references only for this audit; no external service was contacted.

## Inferred Architecture

`INFERENCE_REQUIRES_CONFIRMATION`: static source evidence suggests Mongo collection shapes are distributed across route modules, startup index creation, seed scripts, and docs rather than one centralized migration system. Runtime collection/index state requires a later authorized environment dump.

`INFERENCE_REQUIRES_CONFIRMATION`: route decorator counts are a static denominator, not proof of runtime reachability, authorization completeness, or deployment status.

## Inventory Counts

| Family | Count |
| --- | ---: |
| Tracked files | 4676 |
| Backend files | 379 |
| Frontend files | 314 |
| Governance files | 1322 |
| Docs files | 2329 |
| Backend route decorators | 279 |
| Frontend route lines | 112 |
| Production-code Mongo collections | 92 |
| Backend test files | 185 |


## Copilot Reconciliation Architecture Notes

The Copilot reconciliation added documentary evidence for repository root documentation/policy, backend dependency-boundary, CI assurance, frontend peer-dependency, secret-scan evidence, large-module reviewability, lockfile, and deployment-model documentation surfaces. These notes do not change architecture, product code, CI, dependency manifests, lockfiles, deployment configuration, schemas, or migrations.
