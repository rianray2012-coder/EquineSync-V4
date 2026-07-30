# EquineSync V4

EquineSync V4 is a private application repository for the EquineSync web platform, backend API, governance corpus, and mobile wrapper assets.

## Repository Status

This repository is under Founder-controlled governance. Current repository hygiene review records show 18 open gaps, 16 retained findings, and 15 candidate implementation work packages. No implementation work package is activated by this README.

No root license file is present. Until the Founder or legal reviewer selects a distribution policy, no open-source license or reuse grant is implied.

## Main Surfaces

- `backend/`: FastAPI backend, MongoDB integration, provider integration code, operational scripts, and backend tests.
- `frontend/`: Create React App frontend, Vercel configuration, Capacitor mobile wrapper configuration, and UI tests/build scripts.
- `.github/workflows/ci.yml`: existing CI for backend test collection, backend known-failure non-regression, and frontend build.
- `docs/`: product, deployment, governance, and evidence documentation.
- `governance/implementation/code-guides/`: Code Guide governance packages and review records.

## Tool Versions Used By CI

- Python: `3.11`
- Node.js: `20`
- Frontend package manager in CI: `npm ci --legacy-peer-deps`

The legacy peer dependency flag is part of the current evidenced install path and should not be removed without a separate dependency remediation decision.

## Backend Setup

Create a local Python environment, then install backend dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

For backend tests and development tooling, use the dev manifest if present on your branch:

```bash
pip install -r backend/requirements-dev.txt
```

Copy `backend/.env.example` to a local ignored `.env` file and fill local-only values. Do not commit real credentials, provider keys, JWT secrets, database URLs, or webhook secrets.

## Frontend Setup

```bash
cd frontend
npm ci --legacy-peer-deps
npm run build
```

Copy `frontend/.env.example` to a local ignored env file when running the frontend locally.

## Existing Deployment Documentation

Frontend Vercel deployment settings are documented in `docs/VERCEL_FRONTEND_DEPLOYMENT.md` and represented in `frontend/vercel.json`. Backend hosting/containerization decisions remain reserved for Founder disposition; this README does not authorize or change deployment configuration.

## Validation Boundaries

This README is orientation only. It does not close any governance gap or finding, activate an IWP, authorize staging/pilot/production use, select a license, rotate credentials, configure an external scanner, change branch protection, or merge any draft PR.
