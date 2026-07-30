# Proposed PR Segmentation And Dependency Plan

## Segment 1: Documentation And Repository Metadata

Branch: `codex/repository-hygiene-docs-metadata-v1`

Scope: replace placeholder root `README.md`, add non-secret `.env.example` files with `.gitignore` exceptions, link existing deployment/testing/governance/security documentation, and document observed Python/Node versions and commands. No license grant and no deployment/config change.

## Segment 2: Backend Dependency Classification And Split

Branch: `codex/backend-runtime-dev-dependency-split-v1`

Scope: move only directly evidenced dev/test tools from `backend/requirements.txt` to `backend/requirements-dev.txt`: `black`, `flake8`, `isort`, `mypy`, `pycodestyle`, `pyflakes`, and `pytest`. Preserve versions. Update CI backend test install steps to use the dev manifest. Retain runtime, provider, startup, database, maintenance, and uncertain packages in runtime requirements.

Safety gate: if CI proves startup or tests require a moved package through runtime-only install, revert the split. No package removal, no version upgrade, no broad dependency refresh.

## Segment 3: CI Assurance Visibility And Dependency Monitoring

Branch: `codex/ci-assurance-reporting-and-monitoring-v1`

Scope: add non-blocking report-only assurance jobs and conservative `.github/dependabot.yml`. Reports may include backend black/isort/flake8/mypy summaries, package-lock npm audit summary, secret-pattern count/location reporting with redacted values only, and explicit Python audit tool absence. No external scanner, no branch protection change, no auto-merge, no clean-scan claim.

## Reserved Work

Frontend dependency remediation, React/package upgrade/downgrade decisions, lockfile regeneration, license selection, Docker/backend deployment configuration, large-module refactoring, gap closure, finding closure, and IWP activation remain outside this directive.
