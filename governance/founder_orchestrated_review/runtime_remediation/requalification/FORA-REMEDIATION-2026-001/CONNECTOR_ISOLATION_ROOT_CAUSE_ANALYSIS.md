# Connector-Isolation Root-Cause Analysis

## Finding

The prior activation's isolated configuration reported `mcp_servers={}`, so the three Cloudflare failures were not produced by an inherited explicit MCP entry in that isolated config.

However, the isolated runtime kept the default `features.remote_plugin=true`. During execution it populated a remote plugin cache containing the Cloudflare plugin. That plugin's `.mcp.json` declares a required `cloudflare-api` HTTP MCP server at `https://mcp.cloudflare.com/mcp`. The plugin metadata describes authenticated Cloudflare API and write capabilities.

The preserved activation `stderr.txt` contains exactly three Cloudflare MCP OAuth authentication failures, one for each generic read-only child. A separate non-agent startup probe also showed the isolated runtime attempting remote plugin catalog and installed-plugin synchronization.

Relevant preserved hashes:

- Cloudflare `.mcp.json`: `15a37d198742dbf258dd0e565e0303cfb1985e9e44fa6fe994942e70ec53f981`
- Cloudflare plugin manifest: `790ac166fa1f509f440e66d35c010e1cfb34d773726eb3a30a6a7553dacaf59a`
- Prior activation `stderr.txt`: `1e2ed3e4d5942b45867bc764a2326b7329c3b72f4aef51f2542175dd63e855bb`

## Root cause

`REMOTE_PLUGIN_AUTOLOAD_INTRODUCED_REQUIRED_CLOUDFLARE_MCP`

The isolated profile did not explicitly disable remote plugins, plugins, or apps. Account-backed remote plugin synchronization populated the Cloudflare plugin, whose required MCP declaration initialized and attempted OAuth despite the absence of an explicit isolated `mcp_servers` entry.

## Remediation requirement

The new disposable profile must disable remote plugins, plugins, apps, MCP-app integration, tool suggestion, browser/computer integrations, and authentication elicitation. It must configure no MCP servers, use a deployment-tool-free `PATH`, and prove through a non-agent config probe plus captured process stderr that no Cloudflare or unrelated connector starts.
