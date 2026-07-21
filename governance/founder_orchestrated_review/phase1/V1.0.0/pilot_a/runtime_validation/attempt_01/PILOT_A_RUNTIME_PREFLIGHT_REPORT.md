# Pilot A Runtime Preflight Report

**Preflight ID:** `ES-PH1-PILOT-A-RUNTIME-PREFLIGHT-2026-001-ATTEMPT-01`

**Recorded at:** `2026-07-21T21:55:02Z`

**Repository:** `https://github.com/rianray2012-coder/EquineSync-V4.git`

**Remote default branch:** `integrate-emergent-final-zip` at `acb518ea5a160820e64681ff95a16b010fe1156c`

**Authoritative predecessor:** `codex/founder-review-phase1-operating-model-v1` at `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`

**Execution branch:** `codex/founder-review-phase1-pilot-a-runtime-validation-v1`
**Disposition:** `PILOT_A_RUNTIME_VALIDATION_BLOCKED_BY_HOST_OR_ROLE_SELECTION`

## Authorization and authoritative inputs

The Founder directive authorizes Pilot A only in a host-enforced, permission-compliant runtime. The Phase 1 V1.0.0 package, Pilot A test plan, role profiles, tool-permission matrix, runtime permission control, blind-review model, prompt-injection controls, custody controls, replay standard, schemas, validation utility, failed canary evidence, and failed permission records were inspected from the exact predecessor.

The fresh clone fetched all remote branches and tags before the branch was created. The remote predecessor ref resolved exactly to `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`. The detached predecessor checkout, index, and worktree were clean before branch creation.

## Required Pilot A roles

| Role ID | Canonical role | Profile file SHA-256 | Required host mode |
| --- | --- | --- | --- |
| `ES-RA-02` | Segregated Review Agent | `39f4eb1312eee552b7e16d451f1007e15f432dcc8b1b750fd4fb9417d5afe21e` | `read-only`, `on-request`, network off |
| `ES-RA-03` | Adversarial Challenge Agent | `dd9d5690c45794059c8272e76f6d8b5bb2116a9a139dc369437bd5dfe6fc340a` | `read-only`, `on-request`, network off |
| `ES-RA-04` | Machine Validation Agent | `b1a99f88d96309fab2f1a1c55bb85eea609c4ca3549c979db02038606f1d5b78` | `workspace-write`, `on-request`, network off; bounded validation output only |
| `ES-RA-05` | Evidence Custodian | `6c7ccf954bb3624c0cdafef87a41b6c863d3077e7491192c4670427485818f9b` | `workspace-write`, `on-request`, network off; evidence output only |

`ES-RA-08` remains canonically named `Executable Golden-Path Reproduction Controller`. It is not one of the four minimum roles named by the authoritative Pilot A test plan.

## Runtime finding

The parent runtime was Codex Desktop with Codex CLI `0.144.6`, configured model `gpt-5.6-sol`, configured reasoning effort `xhigh`, `danger-full-access`, approval policy `never`, unrestricted filesystem access, and network access enabled. The controlling runtime permission policy expressly prohibits this parent mode for formal review roles without a documented Founder exception. No exception was present.

Runtime-native canonical-role selection was not available:

- the host delegation request exposes a generic task name, instructions, model, and reasoning effort but no canonical agent/profile selector;
- `codex exec --help` exposes no custom-agent or canonical-role selection option;
- `codex features list` reports `use_agent_identity` as `under development` and `false`; and
- no non-null authoritative role identifier could therefore be obtained without attempting a generic or inferred role, which the Founder directive prohibits.

Plugin and service isolation also failed. Five MCP servers were enabled, including three remote services; fourteen plugins were enabled; browser, external browser, computer-use, image generation, apps, remote-plugin, and web/network-capable functionality remained available. GitHub bearer-token configuration and Cloudflare OAuth capability were present. Credential values were not read or recorded.

## Failed controls

| Control | Result | Evidence |
| --- | --- | --- |
| Runtime-native canonical-role selector | `UNVERIFIABLE` | No selector in the delegation or CLI execution interface; `use_agent_identity=false` |
| Runtime-native role identity record | `UNVERIFIABLE` | No qualifying role was invoked; generic execution is prohibited |
| Parent sandbox for ES-RA-02 and ES-RA-03 | `BROADER_THAN_AUTHORIZED` | `danger-full-access` observed; `read-only` required |
| Parent sandbox for ES-RA-04 and ES-RA-05 | `BROADER_THAN_AUTHORIZED` | unrestricted host access observed; bounded `workspace-write` required |
| Approval policy | `BROADER_THAN_AUTHORIZED` | `never` observed; `on-request` required |
| Network boundary | `BROADER_THAN_AUTHORIZED` | network enabled; `OFF` required |
| Plugin/MCP/service isolation | `BROADER_THAN_AUTHORIZED` | 5 enabled MCP servers and 14 enabled plugins |
| Credential and production-access absence | `UNVERIFIABLE` | authenticated remote-service capability is configured; production route absence is not host-enforced or proven |
| Role-specific output-path isolation | `UNVERIFIABLE` | parent has unrestricted filesystem access; no host-enforced role path boundary exists |

Any one of the first two non-negotiable controls would block execution. Multiple structural host controls failed, so this was not a bounded configuration error eligible for the single corrected preflight retry.

## Repository and freeze evidence

- Phase 1 V1.0.0 predecessor tree: `ce706c6356fe3dd7179d6dc6ddb18948759b8241`
- Prior Pilot A tree: `ffeb0bafe39d6d55a2b73fc71aff7c9584d0e7d7`
- Prior Pilot A evidence tree: `7c7dc70d6c8a7b6f6e90cbe783950d5e06a1df8c`
- Prior Pilot A fixtures tree: `7534cffc668ca09425c973f42ec3cbaac86ebd64`
- Existing package manifest SHA-256: `43632e988ba27ae0b77c734af3c859e90d2493cc724378b58700aa24833d0a50`
- Existing Phase 1 archive SHA-256: `fc29bcd5d3a70457503decf0e53c9462b0ea09f5a7572494bd19160663fa1294`
- Candidate manifest SHA-256: `b385efe7bb7875f8edba93e4828db5c73af263e5ccb8dc1f442d7483248107ac`
- Expected-defect register SHA-256: `dd4f740ac250b3bc2772c2bfdd2db1ae78500400b975b87320871afd5e81ca14`
- Preserved failed canary attempt SHA-256: `a58ef01dbbb961262e394005a4ada4204360ef751ec2afa17c28868b5b9d08f9`
- Preserved corrected packet attempt SHA-256: `af6ee863db0e770e6eebd8fe85821eb6237c84bc696490bb55d8a4d860da13ef`

No historical file, sealed file, candidate fixture, failed evidence, or prior permission record was modified.

## Execution decision

Canonical roles attempted: **0**. Canonical roles executed: **0**. Generic agents used as substitutes: **0**. Non-agent fallback outputs used as qualifying evidence: **0**.

The Pilot A input freeze, role workspaces, behavioral canary tests, behavioral prompt-injection tests, sealing, reconciliation, replay, and variance procedures were not started because the preflight gate failed closed.

## Minimum environment change required

1. Start a new host session with `read-only` plus `on-request` approval for ES-RA-02 and ES-RA-03.
2. Use separate host sessions or explicit host-enforced transitions to narrowly bounded `workspace-write` plus `on-request` approval for ES-RA-04 and ES-RA-05.
3. Deny network and disable every plugin, MCP server, connector, external service, browser, provider credential, and unrelated repository-write capability before role launch.
4. Use a Codex host/runtime that exposes an explicit canonical custom-agent selector and records the requested and loaded non-null ES-RA identity plus profile checksum in authoritative runtime evidence.
5. Enforce frozen-input read boundaries and role-specific output directories at the host level, then rerun preflight as a new preserved attempt.

Do not weaken the role requirement or use textual impersonation. Phase 2 remains unauthorized.
