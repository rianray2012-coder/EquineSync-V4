# Controlled Founder-Orchestrated Review Agent Activation Procedure

**Procedure status:** Executed; activation blocked and inactive state preserved

**Review ID:** `FORA-ACT-REV-2026-001`

**Founder authority:** Rian Ray

## Purpose

This procedure defines the minimum controlled steps Codex may perform only after an explicit Founder activation decision. The existence of this procedure, the review package, or the decision JSON does not authorize activation.

## Preconditions

Before any activation implementation, the operator must:

1. obtain an explicit Founder decision recorded in `FOUNDER_ACTIVATION_DECISION.json`;
2. validate that record against `FOUNDER_ACTIVATION_DECISION.schema.json`;
3. confirm `founder_activation_approval=true`, `activation_authorized=true`, and a permitted approved decision value;
4. confirm `approved_by`, `approved_at`, and `approval_reference` contain explicit Founder evidence;
5. confirm the decision references the exact technical commit and review package reviewed by the Founder;
6. verify every condition when the decision is `FOUNDER_ACTIVATION_APPROVED_WITH_CONDITIONS`;
7. verify the target branch and commit from a clean checkout;
8. confirm no unreviewed role, sealed-package, calibration-suite, permission, or governance-authority changes occurred after review;
9. confirm the authorized environment has no production credentials, production routes, or production write capability unless a separate express Founder authorization names them; and
10. create a new activation-run ID and immutable pre-activation evidence directory.

Any failed or unresolved precondition stops activation.

## Controlled activation sequence

1. Record the exact Founder decision, reviewed commit, activation-run ID, environment, operator, timestamp, permissions, network state, paths, and prohibitions.
2. Revalidate repository identity, commit ancestry, manifest, checksums, ZIP hash, and neutral-to-approved decision-state transition.
3. Apply only the smallest activation-status change expressly authorized by the Founder. Do not alter role duties, segregation, sandbox settings, approval settings, or sealed content.
4. Do not infer substantive-review commencement from activation. Keep commencement disabled unless `substantive_review_commencement_authorized=true` and the Founder evidence expressly covers it.
5. Run a response-only post-activation canary for each registered agent type using its required sandbox class, denied network, exact `agent_type`, and `fork_turns="none"`.
6. Validate exact agent identity, registration marker, sandbox provenance, denied network, no unauthorized tool use, no child-created files, and no production access.
7. Preserve commands, prompts, parent and child provenance, outputs, stderr, exit codes, checksums, and any failed or repeated canary attempts.
8. Generate a machine-readable activation result and human-readable report that distinguish installation activation from review commencement and Founder disposition.
9. Commit and push only to the Founder-authorized branch. A pull request, merge, tag, release, deployment, or default-branch modification requires separate authorization.

## Post-activation acceptance gate

Activation may be recorded as technically completed only when:

- the decision record is valid and explicitly approved;
- all Founder conditions are verified;
- the activated commit matches the approved commit;
- every required canary passes;
- sandbox and network provenance match the role matrix;
- no unauthorized file, network, production, or connector activity occurred;
- all evidence checksums validate; and
- the final report still states whether substantive-review commencement is authorized.

Failure disposition: `ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED`.

## Rollback

If activation validation fails:

1. stop all further agent use;
2. preserve the first failure and every attempted rerun;
3. revert only the activation-status change through a new auditable commit or other Founder-authorized recoverable mechanism;
4. restore the last verified inactive configuration state;
5. rerun the inactive-state integrity checks and canary;
6. record residual effects, incomplete restoration, and any required Founder decision; and
7. do not resume activation without a new or reaffirmed explicit Founder authorization.

Rollback must not delete or rewrite the failed activation evidence.

## Current state

- Founder activation approval: `true`, with conditions
- Activation authorized: `true` for the bounded controlled sequence
- Activation run: `FORA-ACT-2026-001`
- Operational activation: blocked; not completed
- Failure disposition: `ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED`
- Read-only canary batch: failed because exact registered agent types were not loaded; `agent_type` and runtime `agent_role` were null
- Unauthorized connector activity: three failed Cloudflare MCP authentication attempts were recorded; no successful access or provider write was established
- Workspace-write canary batch: not started
- Retry: none; Founder condition 9 required all further review-agent use to stop
- Rollback: the approved checkout remained clean and byte-identical, so the last verified inactive role and sealed-package configuration was already preserved; no role/configuration rollback mutation was required
- Substantive-review commencement: not authorized and not performed
- Pull request, merge, default-branch modification, tag, release, deployment, production access, and provider write: not performed
