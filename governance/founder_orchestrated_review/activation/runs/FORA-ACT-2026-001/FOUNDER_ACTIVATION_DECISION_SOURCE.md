# Founder Activation Decision Source

Review ID: `FORA-ACT-REV-2026-001`

Decision: `FOUNDER_ACTIVATION_APPROVED_WITH_CONDITIONS`

Founder: Rian Ray

Founder Activation Approval: `TRUE`

Activation Authorized: `TRUE`

Substantive Review Commencement Authorized: `FALSE`

Merge Authorized: `FALSE`

Approved Technical Evidence Commit: `860da19970604197117b94a2ef7f23dba2dca694`

Approved Review-Package and Reconciliation Commit: `45c3bada313ba1196a52398780d1129255a000ee`

Approved Package ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3`

Decision date: July 19, 2026

Decision received for execution: `2026-07-20T03:26:33Z`

## Conditions

1. Activation must follow `CONTROLLED_ACTIVATION_PROCEDURE.md` without enlargement of scope.
2. Activation must be performed from a clean checkout of the approved branch and exact reviewed commits.
3. All eight registered review agents must pass the required response-only post-activation canaries.
4. The calibration-only `es_runtime_canary.toml` must remain separate from the eight registered review roles.
5. No production credentials, production routes, production data, provider writes, deployment capability, or production access may be present.
6. The observed noninteractive `approval_policy=never` must not be interpreted as permission or authority. Any action outside the expressly authorized activation sequence must fail closed.
7. `workspace-write` must not be treated as a role-specific path allowlist. Output boundaries must remain procedurally constrained and verified after activation.
8. All commands, prompts, outputs, provenance, failures, retries, checksums, and final results must be preserved.
9. Any failed activation or canary must result in `ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED` and no further agent use.
10. Substantive Founder-Orchestrated Review may not commence without a separate Founder authorization.
11. No pull request, merge, default-branch modification, tag, release, or deployment is authorized.

## Rationale

The installation and reconciliation evidence demonstrate sufficient technical readiness for controlled operational activation. Activation remains distinct from substantive review commencement, implementation authorization, production authority, and external assurance.

## Source provenance

This file is a faithful repository record of the Founder decision supplied directly by Rian Ray in the Codex task. It records authorization only for the bounded controlled activation. It is not substantive-review authorization, implementation authorization, production authority, external assurance, merge authorization, or deployment authorization.
