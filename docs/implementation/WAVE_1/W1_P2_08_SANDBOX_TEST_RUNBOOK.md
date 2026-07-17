# W1-P2-08 Sandbox Provider Test Runbook

Ordinary local, CI, and automated tests must keep every provider credential
empty and must permit only loopback dependencies.

An intentionally authorized sandbox test requires all of:

1. A separate founder or release-governance authorization naming the provider.
2. `APP_ENV=test` or an isolated non-production equivalent.
3. `ALLOW_SANDBOX_PROVIDER_TESTS=true`.
4. `PROVIDER_TEST_ENVIRONMENT=sandbox`.
5. Verified provider test-mode credentials supplied through the approved secret
   manager, never a repository file or shell history.
6. An endpoint allowlist, evidence capture, cleanup, and post-run secret scrub.

Production-like credentials are rejected in non-production even when sandbox
opt-in is set. This runbook grants no integration-test or provider authority.
