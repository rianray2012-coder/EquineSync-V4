# Repository Trust and Profile Precedence Report

## Repository identity

- Repository: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- Source branch: `agent/install-founder-review-agents-v1.0.0`
- Source commit: `57210494c1e82e60efd4c329ebf34fda236972d8`
- Remediation branch: `codex/founder-review-agent-runtime-requalification-v1`
- Project custom-agent directory: `.codex/agents/`

## Disposable-profile proof

The CLI probes used isolated temporary Codex homes and a trusted project rooted at an exact clean clone. Plugin, connector, and MCP autoloading was removed. `codex app-server` `config/read` reported the project configuration layer loaded and enabled, `multi_agent=true`, `agents.max_threads=6`, `agents.max_depth=1`, and zero MCP servers. All eight repository role TOMLs plus the non-role canary parsed.

Configuration precedence was therefore:

1. bounded command-line sandbox and approval overrides;
2. disposable user profile;
3. trusted project `.codex` configuration and `.codex/agents/*.toml` files;
4. built-in defaults.

The failure remained after personal configuration, plugins, connectors, and MCP servers were excluded. The evidence therefore does not support a profile-precedence or trust diagnosis. The limitation occurred at the spawn interface: no exact custom-agent selector was exposed.

The current desktop task was not used for a formal role spawn because its effective permissions were broader than allowed by `RUNTIME_PERMISSION_CONTROL.md`, and its spawn schema independently lacked the selector.
