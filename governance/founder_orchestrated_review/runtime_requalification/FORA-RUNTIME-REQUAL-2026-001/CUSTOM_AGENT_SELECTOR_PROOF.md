# Custom-Agent Selector Proof

## Required proof

The controlling requirement was an actual child spawn whose request preserves the exact custom-agent identity from a repository-controlled `.codex/agents/*.toml` file. A normal prompt, task label, generic worker, fallback role, null `agent_type`, or unverified subprocess label does not satisfy this proof.

## Canary results

- CLI noninteractive: requested exact `agent_type=es_runtime_canary`; the parent reported that its `spawn_agent` interface had no selector field. Spawn calls: 0. Children: 0.
- CLI interactive: requested the same exact selector under a disposable read-only/on-request profile. The parent reported the selector field unavailable. Spawn calls: 0. Children: 0.
- Desktop current task: the exposed schema contains `task_name`, `message`, `fork_turns`, `model`, and `reasoning_effort`, but no `agent_type` or equivalent custom-agent selector. Formal role execution was also prohibited by the effective `danger-full-access` / `never` parent permissions.
- App-server diagnostic: config parsing and project-layer loading passed, but generated request schemas exposed no external custom-agent selector or spawn method.

No canary was counted as a review role. No generic child was launched. No prompt was relabeled as an agent. No substantive review occurred.

## Classification

This is not a repository configuration, profile precedence, trust, or invocation-syntax defect: static discovery and configuration serialization passed, while the execution interfaces themselves lacked the required selector. For `codex-cli 0.144.6` and every supported surface tested, the controlling selector is unavailable. Therefore the run stops at required execution-order step 4 and returns `FOUNDER_REVIEW_AGENTS_BLOCKED_BY_CONFIRMED_RUNTIME_PRODUCT_LIMITATION`.
