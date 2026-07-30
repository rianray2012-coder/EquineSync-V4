# PR #67 CI, Permissions, Dependabot, And Reporting Review

## Reviewed State

- PR: #67, `CI assurance reporting and monitoring draft`
- Reviewed head: `982e417a66d641e93fc905a690c94095c8ee8570`
- Scope: `.github/dependabot.yml`, `.github/workflows/ci.yml`, and `docs/CI_ASSURANCE_REPORTING_POLICY.md`.
- Checks: backend collectability, backend known-failure non-regression, frontend build, Assurance visibility report, Vercel, and Vercel Preview Comments all successful in GitHub metadata.

## Positive Scope Findings

- Trigger conditions remain `push` to `integrate-emergent-final-zip` and `pull_request`; no `pull_request_target` trigger is introduced. Evidence: `.github/workflows/ci.yml:14-18`.
- The new assurance job is explicitly report-only and `continue-on-error: true`. Evidence: `.github/workflows/ci.yml:238-247`.
- Backend static tooling commands are run as evidence and forced to exit 0 at the end of the step. Evidence: `.github/workflows/ci.yml:267-297`.
- `npm audit` is report-only and exits 0 after recording counts. Evidence: `.github/workflows/ci.yml:299-325`.
- Secret-pattern reporting prints labels and file:line locations, not candidate values. Evidence: `.github/workflows/ci.yml:327-368`.
- Artifact upload is limited to `frontend/npm-audit.json`. Evidence: `.github/workflows/ci.yml:370-376`.
- Dependabot covers pip `/backend`, npm `/frontend`, and GitHub Actions `/` weekly with open PR limits of 3, 3, and 2. Evidence: `.github/dependabot.yml:1-30`.
- Policy text reserves external scanners, historical secret scanning, SAST, CodeQL, license scanning, and Python dependency-audit tooling. Evidence: `docs/CI_ASSURANCE_REPORTING_POLICY.md:28-30`.

## Required Corrections

1. PR #67 must be rebased or corrected after PR #66 so the assurance visibility job installs backend static tools from `backend/requirements-dev.txt`. Current evidence: `.github/workflows/ci.yml:263-280` installs `backend/requirements.txt` and then runs `black`, `isort`, `flake8`, and `mypy`. PR #66 moves those tools to `backend/requirements-dev.txt:3-10`. If PR #66 is merged and #67 is not corrected, the report job can lose the tools it is meant to report on.
2. PR #67 should declare explicit least-privilege workflow permissions before Founder disposition. Current evidence: `.github/workflows/ci.yml:14-31` enters `jobs` without a top-level or job-level `permissions` block. The job appears to need read-only repository access plus artifact upload behavior, not write access to contents, pull requests, issues, deployments, packages, or checks.

## Review Result

PR #67 is bounded and conservative in intent, but it requires correction before Founder disposition because of the cross-PR dependency with PR #66 and the missing explicit permissions declaration.

## Advisory Disposition

`APPROVE_AFTER_ENUMERATED_CORRECTIONS`

This recommendation is advisory only and not self-executing.
