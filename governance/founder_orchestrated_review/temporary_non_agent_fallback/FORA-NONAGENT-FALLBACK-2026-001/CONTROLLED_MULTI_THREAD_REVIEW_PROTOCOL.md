# Controlled Multi-Thread Non-Agent Review Protocol

## Purpose

This protocol operationalizes the temporary Founder-authorized fallback for segregated documentary and design review. It is not an agent-registration, activation, calibration, or orchestration protocol for `ES-RA-01` through `ES-RA-08`.

## Preconditions for each review cycle

Before opening review threads or creating review worktrees, record:

1. a unique review-cycle ID;
2. the exact frozen review object and its version, commit, or SHA-256;
3. included scope and explicit exclusions;
4. the documentary or design question assigned to each lane;
5. the required output and permitted disposition for each lane;
6. permitted repositories, paths, tools, and write locations;
7. a prohibition on implementation, product workflow execution, release, deployment, and production access;
8. the reconciliation method and Founder-reserved decisions.

If any controlling input is missing or mutable, do not begin that lane.

## Segregation controls

- Use one uniquely labeled non-agent thread per independent review lane.
- If worktrees are used, create one isolated worktree per lane from the same exact frozen commit.
- Do not label a thread, task, worktree, prompt, or output as an `ES-RA-*` role.
- Do not claim that a custom-agent identity or registration marker loaded.
- Do not share unpublished findings, preferred conclusions, or remediation plans between independent lanes before their initial outputs are complete.
- Keep review inputs read-only. Write only to the lane's explicitly authorized non-sealed evidence location.
- Preserve prompts, input identity, outputs, timestamps, failures, retries, and reconciliation records.

## Reconciliation controls

The coordinating thread may normalize formatting, identify agreements or conflicts, and assemble a Founder-facing package. It must preserve which lane made each observation and must not transform a lane conclusion into agent evidence, external assurance, or a Founder disposition.

## Required labels

Every output produced under this fallback must state:

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

and:

`NOT_ES_RA_AGENT_EVIDENCE`

## Continuing blockers

- `F-0001 = F0001_REMAINS_OPEN_BLOCKING`
- `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE = OPEN`
- Founder-Orchestrated Review Agent runtime registration = `0/8`
- execution = `EXECUTION_NOT_AUTHORIZED`
- assurance = `NOT_EXTERNALLY_ASSURED`
- Stage 2 = `EXECUTION_BASELINE_STILL_NOT_READY`

## Start condition

Status is `AUTHORIZED_AVAILABLE_NOT_STARTED_PENDING_SCOPED_REVIEW_DIRECTIVE` until a bounded directive identifies the frozen review object, lanes, scope, and deliverables.
