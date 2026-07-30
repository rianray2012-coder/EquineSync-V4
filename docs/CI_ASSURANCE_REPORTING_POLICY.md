# CI Assurance Reporting Policy

This policy supports the CGP-006 repository hygiene and CI assurance draft PR. It creates visibility only; it does not activate an implementation work package or change branch protection.

## Current Mode

- New assurance reports are non-blocking.
- Report failures are evidence for Founder review, not merge blockers.
- No report may claim the repository is clean unless the underlying tool ran successfully and reported zero findings.
- Secret-pattern reporting must print counts and locations only. It must not print candidate values.
- No external scanner, repository app, SaaS service, or credentialed provider integration is configured by this policy.

## Ratchet Requirement

Before any report becomes blocking, a separate Founder-approved ratchet must define:

- the baseline count and source artifact;
- false-positive handling;
- allowed suppressions and reviewer authority;
- severity thresholds;
- rollback if a report blocks unrelated urgent work;
- whether the check should become required in branch protection.

## Dependency Monitoring

Dependabot is configured with a controlled cadence and low open-PR limits for Python, npm, and GitHub Actions. Auto-merge is not configured. Major-version updates require normal review and Founder disposition where they intersect React, runtime architecture, deployment, or governance constraints.

## Reserved Work

License scanning, Python dependency-audit tooling, SAST, CodeQL, historical secret scanning, and external scanner setup remain reserved until separately authorized.
