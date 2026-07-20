# Runtime Capability Matrix

Run: `FORA-RUNTIME-REQUAL-2026-001`

Codex: `codex-cli 0.144.6`

Result: **CUSTOM_AGENT_SELECTOR_UNAVAILABLE_ON_EVERY_SUPPORTED_RUNTIME_SURFACE_TESTED**

| Runtime surface | Classification | Exact selector tested | Selector available | Execution result |
|---|---|---|---:|---|
| Codex desktop current task | SUPPORTED_LOCAL_CLIENT | spawn_agent agent_type/name selector | NO | NOT_ATTEMPTED_PERMISSION_CONTROL_AND_SELECTOR_BLOCK |
| Codex CLI interactive | SUPPORTED_LOCAL_CLIENT | model-directed exact agent_type=es_runtime_canary spawn | NO | NO_SPAWN_CALL_NO_CHILD |
| Codex CLI exec --json | SUPPORTED_NONINTERACTIVE_CLI | model-directed exact agent_type=es_runtime_canary spawn | NO | NO_SPAWN_CALL_NO_CHILD |
| Codex app-server protocol | EXPERIMENTAL_PROTOCOL_DIAGNOSTIC_ONLY | generated request/params schema search for agent_type or agentRole selector | NO | CONFIG_READ_ONLY_NO_EXTERNAL_CUSTOM_AGENT_SPAWN_METHOD |

The current [official Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) describes project custom-agent files in `.codex/agents/` and says the `name` field identifies the custom agent. The repository configurations parse and the project layer loads. However, none of the supported execution surfaces exposed a field that could preserve that exact custom-agent identity in a spawn request. A configuration file being discoverable is not proof that its identity layer executed.

The app-server schema was inspected only as an additional diagnostic. It is not counted as a supported replacement execution path and did not expose an external custom-agent spawn method.
