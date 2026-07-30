# PR #66 Dependency Classification And Validation Review

## Reviewed State

- PR: #66, `Backend runtime dev dependency split draft`
- Reviewed head: `9f8b6e233a6ee9a23d9c9e9b8394376b3ab55606`
- Scope: `.github/workflows/ci.yml`, `backend/requirements-dev.txt`, and `backend/requirements.txt`.
- Checks: backend collectability, backend known-failure non-regression, frontend build, Vercel, and Vercel Preview Comments all successful in GitHub metadata.

## Dependency Split

Pre-change source: `backend/requirements.txt` at protected head `396f82c8a7600cae363142175d1d1448e9d2ece2`.

Moved dependencies:

| Package | Prior location | Proposed location | Purpose | Evidence |
| --- | --- | --- | --- | --- |
| `black==26.3.1` | `backend/requirements.txt:10` | `backend/requirements-dev.txt:4` | formatting | formatter tool; no runtime import found in raw backend scan |
| `flake8==7.3.0` | `backend/requirements.txt:26` | `backend/requirements-dev.txt:5` | linting | linter tool; no runtime import found in raw backend scan |
| `isort==8.0.1` | `backend/requirements.txt:48` | `backend/requirements-dev.txt:6` | import sorting | import sorter; no runtime import found in raw backend scan |
| `mypy==2.1.0` | `backend/requirements.txt:64` | `backend/requirements-dev.txt:7` | type checking | type checker; no runtime import found in raw backend scan |
| `pycodestyle==2.14.0` | `backend/requirements.txt:81` | `backend/requirements-dev.txt:8` | lint support | flake8/pycodestyle tooling; no runtime import found in raw backend scan |
| `pyflakes==3.4.0` | `backend/requirements.txt:85` | `backend/requirements-dev.txt:9` | lint support | flake8/pyflakes tooling; no runtime import found in raw backend scan |
| `pytest==9.0.3` | `backend/requirements.txt:90` | `backend/requirements-dev.txt:10` | testing | raw backend scan found `pytest` imports only under `backend/tests/` |

## Validation Evidence

- `backend/requirements-dev.txt:3` installs `-r requirements.txt`, preserving runtime requirements for test/dev installs.
- PR #66 removes exactly the seven direct tool/test entries from runtime requirements and re-adds the same versions to `requirements-dev.txt`; no package version upgrade or downgrade was found.
- `.github/workflows/ci.yml:46-51` and `.github/workflows/ci.yml:121-126` update backend CI cache keys and install commands to use `backend/requirements-dev.txt` where tests/tooling need it.
- Raw protected-head backend Python scan fetched 363 backend `.py` files. It found 60 moved-tool imports, all `pytest` under `backend/tests/`; non-test hits total: 0.
- No editable installs, extras, or constraints files are introduced. The only nested requirement reference is the intentional `-r requirements.txt` in `requirements-dev.txt`.
- No Docker, Vercel, deployment, frontend, product module, or lockfile file is changed.

## Review Result

No missing production dependency, duplicated dependency, direct transitive-only movement, or silent runtime behavior change was identified.

## Advisory Disposition

`APPROVE_FOR_FOUNDER_AUTHORIZED_MERGE`

This recommendation is advisory only and not self-executing.
