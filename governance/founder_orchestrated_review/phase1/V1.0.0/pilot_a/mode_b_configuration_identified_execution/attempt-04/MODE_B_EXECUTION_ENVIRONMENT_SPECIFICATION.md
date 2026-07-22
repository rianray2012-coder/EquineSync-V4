# Mode B Attempt 04 Execution Environment Specification

## Runtime

- Execution method: `CONFIGURATION_IDENTIFIED_MANUAL_ROLE_EXECUTION`
- Host: macOS arm64
- Codex CLI: `0.144.6`
- Model/provider: `gpt-5.6-sol` / OpenAI
- Required canonical roles: ES-RA-02, ES-RA-03, ES-RA-04, ES-RA-05
- Review classification ceiling: `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW`

## No-provider preflight

`codex doctor` and `codex doctor --json` were not invoked. The replacement diagnostic was first proven inside an OS network-denied sandbox. Formal preflight used local static checks and Codex sandbox profiles with `network.enabled=false`. It recorded exact argv, PIDs, PPIDs, child processes, and denial logs. Before the execution boundary there were zero provider requests, network connections/resolutions, actual credential accesses, model responses, or canonical role invocations.

## Role boundary

Each Role Execution received a complete host serialization of only its own frozen packet. Analytical roles had shell and unified execution disabled. Validation and custody roles had the deterministic command allowlist. Every role profile denied direct network and disabled plugins, MCP, connectors, browser, computer use, image generation, user configuration, rules, persistence, and telemetry. Host-owned provider transport began only after the passed boundary.

## Disclosed limitations

- All successful roles used one model and provider; this is not multi-provider corroboration.
- Configuration and Execution Identity do not prove a distinct natural-person Reviewer Identity or native custom-agent selection.
- The packet's standard JSON Schema was rejected by provider-side strict structured-output enforcement. The failed invocation is preserved; successful executions retained the exact schema in the frozen packet and were deterministically validated by the host.
- Post-boundary TCP connection count was not established as a complete denominator; application-level requests, event streams, and outputs are preserved.
