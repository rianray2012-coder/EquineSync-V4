# Runtime Permission Control

**Control status:** Installation-level mandatory control

**Applies to:** EquineSync Founder-Orchestrated Review Agent Framework V1.3 / configuration package V1.0.0

**Founder authority:** Rian Ray

## Purpose

This control hardens agent delegation without changing the sealed configuration package. It governs the parent session, the eight project-scoped custom agents, and the evidence required before any formal review-role spawn.

Codex custom-agent files can set a default `sandbox_mode` and approval policy. Those defaults are not an immutable security boundary: subagents inherit the parent permission mode, and the parent turn's live overrides may supersede a custom-agent default. The parent must therefore verify the effective mode before every spawn.

## Default parent permission mode

The default parent permission mode for a formal Founder-Orchestrated Review Cycle is `read-only` with interactive/on-request approval handling. Network access is denied unless the Founder Review Authorization expressly permits a named network purpose and environment.

The parent may use `workspace-write` only for a role whose matrix entry requires file creation or controlled execution. The authorization must name the permitted workspace and outputs. After that role is dispatched or completed, the parent must return to `read-only` before spawning a read-only role.

The parent must not spawn a read-only and workspace-write role under one unresolved live permission override. Separate parent sessions or explicit permission transitions are required when the modes differ.

## Role-to-sandbox matrix

| Agent | Role | Default sandbox | Approval policy | Authorized operating boundary | Output handling |
| --- | --- | --- | --- | --- | --- |
| ES-RA-01 | Drafting Agent | `workspace-write` | `on-request` | Founder-authorized candidate or remediation workspace | New versioned candidate and drafting outputs only |
| ES-RA-02 | Segregated Review Agent | `read-only` | `on-request` | Frozen package and controlling sources | Return response to parent for Evidence Custodian registration |
| ES-RA-03 | Adversarial Challenge Agent | `read-only` | `on-request` | Frozen package; analysis only by default | Return response to parent; separate authorization is required for writable testing |
| ES-RA-04 | Machine Validation Agent | `workspace-write` | `on-request` | Clean clone, isolated copy, container, or disposable validation workspace | Validation outputs, logs, and registered derivatives only |
| ES-RA-05 | Evidence Custodian | `workspace-write` | `on-request` | Controlled evidence workspace | Evidence, manifests, hashes, and custody records only |
| ES-RA-06 | Domain Reviewer | `read-only` | `on-request` | Frozen package and defined domain authorities | Return response to parent for Evidence Custodian registration |
| ES-RA-07 | Synthetic Golden-Path Specification Agent | `workspace-write` | `on-request` | Authorized specification and synthetic-fixture workspace | Specifications and synthetic fixtures only |
| ES-RA-08 | Executable Golden-Path Reproduction Controller | `workspace-write` | `on-request` | Founder-authorized non-production test environment | Execution evidence and cleanup/restoration records only |

No matrix entry grants production access.

## Mandatory pre-spawn check

Before each spawn, the parent must create and preserve a permission record containing:

1. review-cycle or calibration ID;
2. agent-run ID;
3. requested custom-agent name and ES-RA role;
4. Founder Review Authorization reference;
5. parent surface and parent permission mode;
6. all active live permission or approval overrides;
7. custom-agent configured `sandbox_mode` and `approval_policy`;
8. expected effective mode from this matrix;
9. actual effective mode, where the runtime exposes it;
10. authorized input paths, output paths, and environment;
11. network status and permitted destinations, if any;
12. confirmation that production access is absent;
13. exception reference, if applicable;
14. checker identity and timestamp; and
15. check result: `PASS`, `FAIL`, or `UNRESOLVED`.

The parent may spawn the role only when the check is `PASS`. An `UNRESOLVED` effective mode fails closed.

## Prohibited modes and overrides

For formal review cycles, the following are prohibited unless Rian Ray expressly authorizes a documented exception:

- `sandbox_mode = "danger-full-access"`;
- full-access or unrestricted permission profiles;
- `--yolo` or `--dangerously-bypass-approvals-and-sandbox`;
- approval bypass through `approval_policy = "never"` when an action might need escalation;
- ambient production credentials, production network routes, or production write access;
- broad writable roots that exceed the authorized workspace; and
- a parent live override broader than the role's matrix entry.

An exception must name the role, purpose, exact environment, data classification, permitted actions, prohibited actions, duration, approver, evidence capture, cleanup, rollback, and revalidation requirements. An exception never transfers Founder disposition authority to an agent.

## Technical enforcement and procedural restrictions

`read-only` is a technical Codex sandbox default for the three analytical roles. It limits writes, but it must not be treated as protection from every secret, connector, host capability, or prompt-injection risk.

`workspace-write` provides a workspace-level boundary, not a role-specific path allowlist inside the repository. It may allow writes elsewhere in the active workspace even when the role instructions name only a candidate, evidence, specification, or test directory. Those narrower path limits are procedural unless the role is launched in a separately isolated workspace enforced by the host.

The `.git` and `.codex` paths may be protected by the local Codex workspace sandbox, but this behavior is environment-dependent and does not replace the pre-spawn check. Connector, MCP, browser, and network permissions remain tool-specific. Parent live overrides can supersede custom-agent defaults.

For high-risk or writable runs, use a dedicated clean checkout, disposable directory, container, or other host-enforced isolation boundary whenever practical. Record what was technically enforced and what remained instruction-only.

## Evidence required after each run

Preserve:

- the pre-spawn permission record;
- the exact invocation and parent mode;
- requested and actually loaded agent identity;
- configured and observed sandbox mode;
- authorization and synthetic/frozen package identity;
- command/tool log and approval events;
- files created, changed, or attempted;
- network and connector activity;
- refusals, blocked actions, deviations, and first failures;
- rerun identifiers and the reason for every rerun; and
- the agent response and permitted or blocked disposition.

Self-reported sandbox identity is evidence of agent awareness, not proof of host enforcement. Host/runtime logs or a controlled enforcement probe are required to claim technical enforcement.

## Stop conditions

Stop before delegation or before substantive work when:

- the Founder Review Authorization is missing or does not record the parent permission mode;
- the package or baseline is unidentified, mutable, or drifted;
- the configured, parent, expected, or observed modes conflict;
- the effective mode is unavailable or unresolved;
- danger-full-access, unrestricted, `--yolo`, or approval bypass is present without an express exception;
- a role has access outside its authorized workspace or environment;
- production credentials, data, routes, or write capabilities are exposed;
- path-level isolation is assumed but not technically present;
- required permission evidence cannot be preserved;
- a role requests unauthorized elevation;
- the runtime loads the wrong custom agent; or
- continuation would create misleading assurance.

The parent records `PERMISSION_CHECK_FAILED` as an orchestration control result and does not begin the role's substantive procedure. This is not a Founder disposition and does not replace the role-specific dispositions in the sealed package.
