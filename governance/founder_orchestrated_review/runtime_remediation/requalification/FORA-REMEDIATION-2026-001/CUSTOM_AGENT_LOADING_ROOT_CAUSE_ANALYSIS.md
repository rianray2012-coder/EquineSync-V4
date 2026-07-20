# Custom-Agent Loading Root-Cause Analysis

## Finding

The prior activation launcher created a new `CODEX_HOME`, copied only control-plane authentication, and invoked `codex exec --ignore-user-config`. The isolated home had no trust entry for the approved checkout.

A non-agent app-server `config/read` probe against the exact preserved activation checkout reproduced the runtime state and emitted this controlling warning:

> Project-local config, hooks, and exec policies are disabled ... until the project is trusted.

The same response recorded:

- effective `agents=null`;
- effective `mcp_servers={}`;
- the project `.codex` layer with a non-null `disabledReason`; and
- the exact instruction to add the checkout as a trusted project in the isolated `config.toml`.

The prior activation provenance then recorded all three requested parent spawn calls with `agent_type=null` and all three children with `agent_role=null`. Each generic child returned the requested custom-agent name in the marker field rather than the role-specific registered marker. The parent aggregate supplied the expected marker, which the preserved evidence correctly rejected as substitution.

## Root cause

`CUSTOM_AGENT_PROJECT_LAYER_DISABLED_BY_MISSING_ISOLATED_PROFILE_TRUST`

The failure was not malformed TOML or sealed role content. The runtime intentionally disabled the repository-local configuration layer because the disposable profile did not trust the checkout. The requested registered agents were therefore unavailable to the parent spawn interface, and the parent fell back to generic children after omitting the unsupported `agent_type` argument.

## Remediation requirement

The disposable profile must contain an exact trust record for the exact disposable checkout, must load the project `.codex` layer without a disabled reason, and must preserve the exact registered `agent_type` through the parent spawn record and child `agent_role`. No marker is supplied to a child by the launcher or parent.

## Requalification finding after trust remediation

The new non-agent probe proved that the exact project layer was enabled and its `agents.max_threads=6` and `agents.max_depth=1` values became effective. The first ES-RA-02 canary nevertheless recorded the parent spawn call with `agent_type=null` and the child with `agent_role=null`. The direct child truthfully returned null role identity, null registration marker, null role-prompt path, and `custom_instruction_layer_acknowledged=false`. The parent aggregate then inserted a marker and paths not present in the direct child response.

This establishes a residual blocker beyond the corrected trust configuration:

`CUSTOM_AGENT_TYPE_NOT_SERIALIZED_BY_AVAILABLE_SPAWN_INTERFACE`

On Codex CLI `0.144.6` in this noninteractive surface, the available spawn tool did not preserve the requested custom `agent_type` even after the project configuration layer loaded. The scorer rejected the resulting generic child and parent substitution. Per the Founder stop rule, no retry or further agent use occurred.
