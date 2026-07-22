# Attempt 03 Runtime Surface Probe

## Clean configuration probe

An isolated `.nosync` `CODEX_HOME` with no user configuration was used. The custom `attempt03_role` permission profile resolved with:

- assigned packet: read;
- assigned output: write;
- minimal runtime: read;
- network: disabled;
- approval policy: `on-request`;
- inherited shell environment: `none`.

The first diagnostic attempted `--strict-config` with `codex debug prompt-input`; the CLI rejected it with exit 1 because strict config is unsupported for the debug subcommand. This was a command-capability diagnostic, not a mandatory gate, and it made no model or provider request. The corrected prompt-input configuration probe returned exit 0.

## Plugin, MCP, connector, and feature state

- `codex plugin list --json`: exit 0; `installed: []`; `available: []`.
- `codex mcp list --json`: exit 0; `[]`.
- apps, plugins, remote plugin, plugin sharing, MCP-app enablement, auth elicitation, MCP elicitation, browser surfaces, computer use, image generation, workspace dependencies, memories, goals, and multi-agent features were overridden false.

## Decisive provider-bound diagnostic behavior

`codex doctor --json` returned process exit 1 because the isolated home had no credentials and the noninteractive terminal was `TERM=dumb`. Those local failures were not the decisive condition.

The command also reported live network activity:

- `network.provider_reachability`: `ok`; ChatGPT base URL reachable, HTTP 404;
- `network.websocket_reachability`: warning; OpenAI Responses WebSocket handshake reached the endpoint, HTTP 401 due to missing authentication.

These live requests occurred before complete formal preflight success. That violated the Attempt 03 Founder authorization and ended the attempt fail closed. No replacement diagnostic or role invocation followed.
