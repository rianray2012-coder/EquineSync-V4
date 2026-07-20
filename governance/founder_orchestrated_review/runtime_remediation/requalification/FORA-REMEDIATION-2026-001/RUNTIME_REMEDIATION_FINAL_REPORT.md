# Runtime Remediation Final Report

Final disposition: `REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY`

## Outcome

Static validation and connector isolation passed, but the first authorized custom-agent canary failed. The parent runtime recorded `agent_type=null`; the child runtime recorded `agent_role=null`; and the direct child returned no registered role, marker, or role-prompt path. The parent then supplied identity values absent from the direct child, which the scorer correctly rejected as substitution. All further agent use stopped immediately and no retry occurred.

## Root causes

- Prior custom-agent failure: the prior disposable `CODEX_HOME` lacked trust for its clean checkout, so Codex disabled the project `.codex` layer.
- Residual runtime blocker after trust correction: Codex CLI `0.144.6` exposed a spawn interface that did not serialize the requested custom `agent_type`; the generic child therefore had null role metadata.
- Prior connector activity: `remote_plugin=true` populated the Cloudflare plugin, whose required MCP declaration attempted authentication three times.

## Remediation applied

A reversible disposable profile now trusts only the exact execution checkout, retains multi-agent operation, enforces read-only policy, declares zero MCP servers/plugins, disables every identified plugin/app/connector autoload feature, sanitizes the environment, and removes copied control-plane authentication after each run. No sealed or registered-role file changed.

## Verification

- Static validation: `PASS` (`17/17`); installed system `16/16 PASS`
- Non-agent runtime probe: `PASS` (`14/14`)
- ES-RA-02 individual canary: `FAIL` (`agent_type=null`, `agent_role=null`)
- ES-RA-03 and ES-RA-06 individual canaries: not attempted due stop rule
- Three-role bounded batch: not attempted due stop rule
- Cloudflare MCP attempts during canary: `0`
- Other unauthorized connector attempts: `0`
- Child tool calls: `0`; workspace writes: `0`; workspace-write roles started: `0`
- Substantive review, production access, provider writes, PR, merge, tag, release, and deployment: none
- Fresh-clone verification: `PENDING`

The system remains inactive and blocked. A new Founder authorization and a runtime surface that preserves exact custom `agent_type` are required before any further agent attempt.

> No workspace-write review role, full operational activation, or substantive Founder-Orchestrated Review is authorized by this directive. Even after successful read-only requalification, further activity requires a separate, explicit Founder authorization.
