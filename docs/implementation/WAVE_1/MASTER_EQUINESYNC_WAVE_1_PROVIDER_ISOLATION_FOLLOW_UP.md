# Master EquineSync Wave 1 Provider Isolation Follow-Up

Identifier: `W1-P2-08-TEST-PROVIDER-ISOLATION`

State: `OPEN_ASSIGNED_NONBLOCKING`

Owner: Platform Operations and Release Governance

Affected environments: local development, CI, isolated test, and future shared
non-production environments.

## Required Controls

- Scrub provider variables by default in ordinary tests.
- Require explicit opt-in for integration tests.
- Prefer fake/local provider adapters.
- Reject production-like credentials during non-provider test startup.
- Maintain environment and egress allowlists where feasible.
- Verify provider test mode before permitted integration contact.
- Keep credentials and fingerprints out of logs and evidence.
- Add CI checks that detect uncontrolled external calls.
- Document the separately approved integration-test procedure.

Review trigger: Platform Operations constitutional adoption, CI hardening,
shared-environment activation, or any provider integration-test proposal.

Closure criteria: executable startup guard, provider-test allowlist, no-network
ordinary test profile, CI regression proof, secret-safe logging proof, and an
approved integration-test runbook.

Target future vehicle: Platform Operations hardening package or a separately
authorized provider-isolation RF.

This follow-up is nonblocking for Wave 1 lock. It authorizes no provider,
credential, deployment, or production activity.
