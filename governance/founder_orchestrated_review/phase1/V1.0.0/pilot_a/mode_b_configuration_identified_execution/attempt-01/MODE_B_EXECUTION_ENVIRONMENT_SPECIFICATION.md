# Mode B Execution Environment Specification

**Attempt:** `ES-PH1-PILOT-A-MODE-B-ATTEMPT-01`  
**Mode:** `CONFIGURATION_IDENTIFIED_MANUAL_ROLE_EXECUTION`  
**Predecessor:** `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`  
**Execution date:** `2026-07-21`  

## Execution identity boundary

Each required role is a separate, fresh, ephemeral Codex CLI model invocation. The invocation is configuration-identified by the exact canonical profile version and checksum; it is not a native custom-agent selection and does not establish Reviewer Identity.

## Host boundary

Each role receives a different non-repository role area containing only its Role Configuration, submitted control envelope, frozen input packet, unique canary, and initially empty output directory. A named Codex permission profile:

- allows reads only within that role area plus the runtime's minimal executable set;
- allows writes only within that role's `output/` directory;
- denies direct network access to model-generated commands;
- uses approval policy `never`, so a denied operation cannot be escalated;
- excludes repository and Git metadata from the role area;
- denies access to sibling role areas, the hidden oracle, the repository, and the Codex credential store.

The model provider connection is host-owned and required to perform the authorized generic model invocation. It is not exposed as a role tool.

## Tool and context boundary

Plugins, MCP servers, apps/connectors, browser/computer-use features, image generation, memories, hooks, goals, collaboration/multi-agent features, and skill dependency installation are disabled. ES-RA-02 and ES-RA-03 receive no shell tool. ES-RA-04 and ES-RA-05 may receive only the sandboxed shell needed for allowlisted deterministic validation or hashing commands. No live web search is enabled.

Every execution uses `--ephemeral`, does not resume a session, has history persistence disabled, disables analytics and feedback, disables OpenTelemetry log and trace exporters, and does not log the submitted prompt through OpenTelemetry. The submitted prompt includes the exact Role Configuration, control envelope, input manifest, canary, output schema, and frozen synthetic packet bytes. It excludes the hidden oracle, other role packets, other role outputs, reconciliation material, and proposed Founder conclusions.

## Output and failure rule

The exact final model response is written by the host to the assigned output directory and then sealed by SHA-256 before another blind output may be disclosed. Any preflight failure blocks all four role invocations. Any role-level failure is preserved under its execution ID and is not overwritten.
