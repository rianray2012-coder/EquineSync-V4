# W1-P2-08 Provider Isolation Plan

Objective: ensure ordinary local, test, and CI startup cannot inherit provider
credentials or contact live providers. The control runs before seed, indexes,
catalog provisioning, or workers. Sandbox contact remains separately gated.

Implementation: `core.provider_isolation.validate_provider_isolation`, startup
enforcement, CI environment scrubbing, loopback-only test proof, test-mode
credential validation, and the sandbox runbook.

Wave 1 behavior was not reopened or changed. No material Wave 1 defect was found.
