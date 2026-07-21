# Pilot A Role Selection Capability Report

**Assessment:** `RUNTIME_NATIVE_CANONICAL_ROLE_SELECTION_UNAVAILABLE`

**Execution eligible:** `NO`
**Roles invoked:** `0`

## Authoritative roles

| Role ID | Canonical name | Project custom-agent configuration | Approved execution profile | Profile checksum |
| --- | --- | --- | --- | --- |
| `ES-RA-02` | Segregated Review Agent | `.codex/agents/equinesync_segregated_review_agent.toml` | `profiles/ES-RA-02_REVIEW_EXECUTION_PROFILE_V1.0.0.json` | `7993cbfb88c6dd276a1fa9d65b32688f60baba27c6c25bfa87c8a35651a353ab` |
| `ES-RA-03` | Adversarial Challenge Agent | `.codex/agents/equinesync_adversarial_challenge_agent.toml` | `profiles/ES-RA-03_REVIEW_EXECUTION_PROFILE_V1.0.0.json` | `e39cf3d8160814e9f01b889046c5947ff868d9661121210a658be1e7b04ae0fb` |
| `ES-RA-04` | Machine Validation Agent | `.codex/agents/equinesync_machine_validation_agent.toml` | `profiles/ES-RA-04_REVIEW_EXECUTION_PROFILE_V1.0.0.json` | `c3a1bf6e279afd4682bdcc9139bc81880c0616f3ee51fffc4d3c95a416c5f8ab` |
| `ES-RA-05` | Evidence Custodian | `.codex/agents/equinesync_evidence_custodian.toml` | `profiles/ES-RA-05_REVIEW_EXECUTION_PROFILE_V1.0.0.json` | `c7192de66d109222a3572e84dabbc2e8ff87f4ddf7b5aeecfabaf833e4db2e0e` |

Static configuration presence does not prove runtime identity. The project files establish the requested role configuration only.

## Measured selection interfaces

| Interface | Selector evidence | Result |
| --- | --- | --- |
| Current host delegation request | Fields support task name, instructions, context fork, model, and reasoning effort; no canonical agent name, agent type, profile path, role ID, or checksum selector | `UNAVAILABLE` |
| `codex exec --help` | Supports model, generic configuration profile, sandbox, approval, directory, schema, and output controls; no project custom-agent selector | `UNAVAILABLE` |
| `codex features list` | `multi_agent` is enabled; `use_agent_identity` is under development and `false` | `UNAVAILABLE` |
| Runtime result schema | A generic child can be named by task but the interface does not guarantee a non-null loaded ES-RA identity or approved profile checksum | `UNVERIFIABLE` |

The generic `--profile` CLI option is a layered Codex configuration profile, not proof that one of the project-scoped `.codex/agents/` role profiles was selected. A task name or prompt instructing a generic child to behave like ES-RA-02, ES-RA-03, ES-RA-04, or ES-RA-05 would be textual impersonation and is prohibited by the Founder directive.

No generic child was launched as a canary because doing so could not satisfy the gate and would create misleading role-execution evidence.

## Required capability

A qualifying host must accept an explicit canonical custom-agent selector, load the exact project registration, emit authoritative requested and loaded role identifiers, emit the loaded profile or source checksum, and allow those records to be captured before substantive role work. A null, omitted, generic, inferred, or self-reported role identity fails closed.

`ES-RA-08` is preserved as `Executable Golden-Path Reproduction Controller`; no alias or coordinator substitution was made.
