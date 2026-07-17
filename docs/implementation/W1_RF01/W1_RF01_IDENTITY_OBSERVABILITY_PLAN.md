# W1-RF01 Identity Observability Plan

## Metrics

Authentication success/failure/lockout, verification and reset requests/completions, refresh success/replay/expiry, logout and revocation, authorization denial by capability/context, cross-tenant denial, pending-role denial, suspended-account attempts, admin identity actions, invite lifecycle, migration classification/delta, and audit pipeline health.

## Alerts

Credential-stuffing spikes, refresh reuse, repeated cross-tenant probes, platform-role mutation, abnormal recovery volume, audit-write failure, seed/UAT login in wrong environment, migration access expansion, and elevated-role enrollment attempts.

## Evidence Requirements

Privacy-minimized actor/account/context IDs, correlation/causation, policy version, outcome, latency, environment, and alert/runbook link. Never log passwords, raw tokens, secrets, or full sensitive payloads.

