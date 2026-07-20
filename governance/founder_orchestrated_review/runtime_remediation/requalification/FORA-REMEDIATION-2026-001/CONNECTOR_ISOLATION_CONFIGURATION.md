# Connector Isolation Configuration

The canary launcher creates a fresh `CODEX_HOME`, copies only the minimum Codex control-plane authentication at run time, writes a profile that trusts only the exact clean checkout, and removes the temporary authentication material after evidence extraction.

The profile declares no MCP server or plugin and disables all discovered connector/autoload surfaces. The sanitized process environment contains only basic shell/runtime names; sensitive ambient variables are detected by name and not inherited. The command uses `--strict-config`, read-only sandboxing, disabled web search, and does not use `--ignore-user-config` because the disposable profile itself is the controlled user configuration needed to express checkout trust.

- Effective MCP servers: `0`
- Disabled connector/plugin features: `apps, auth_elicitation, browser_use, browser_use_external, browser_use_full_cdp_access, computer_use, enable_mcp_apps, in_app_browser, memories, plugins, remote_plugin, skill_mcp_dependency_install, tool_call_mcp_elicitation, tool_suggest, workspace_dependencies`
- Multi-agent feature: `True`
- Project layer count: `1`
- Project layer disabled reason: `None`
- Non-agent-probe Cloudflare attempts: `0`
- Production credentials, routes, and provider tools exposed: none

The Codex control-plane transport required to execute the authorized canary is not treated as role authority or as child network-tool use.
