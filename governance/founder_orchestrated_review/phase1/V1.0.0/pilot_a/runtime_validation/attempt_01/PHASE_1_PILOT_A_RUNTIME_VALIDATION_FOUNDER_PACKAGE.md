# Phase 1 Pilot A Runtime Validation Founder Package

**Package ID:** `ES-PH1-PILOT-A-RUNTIME-VALIDATION-2026-001-ATTEMPT-01`

**Predecessor:** `codex/founder-review-phase1-operating-model-v1` at `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`

**Evidence branch:** `codex/founder-review-phase1-pilot-a-runtime-validation-v1`
**Recommended disposition:** `PILOT_A_RUNTIME_VALIDATION_BLOCKED_BY_HOST_OR_ROLE_SELECTION`

## Executive finding

Pilot A cannot begin in the measured runtime. The host does not expose qualifying canonical-role selection, the parent permission profile is broader than all four role profiles, and required plugin/MCP/network isolation is absent. The gate correctly stopped before delegation.

## Runtime and permission result

- Runtime: Codex Desktop; CLI `0.144.6`; configured model `gpt-5.6-sol`; reasoning effort `xhigh`.
- Effective parent permissions: `danger-full-access`, approval `never`, unrestricted filesystem, network enabled.
- Required analytical-role permissions: `read-only`, approval `on-request`, network off.
- Required writable-role permissions: narrowly bounded `workspace-write`, approval `on-request`, network off.
- Canonical role-selection result: unavailable; `use_agent_identity=false` and no explicit selector is exposed.
- Isolation result: failed; 5 MCP servers and 14 plugins were enabled, including authenticated remote-service capability.
- Express Founder exception for these mismatches: none found.

## Required and executed roles

| Role | Required | Attempted | Executed | Qualified |
| --- | --- | --- | --- | --- |
| `ES-RA-02` Segregated Review Agent | Yes | No | No | No |
| `ES-RA-03` Adversarial Challenge Agent | Yes | No | No | No |
| `ES-RA-04` Machine Validation Agent | Yes | No | No | No |
| `ES-RA-05` Evidence Custodian | Yes | No | No | No |

Exact required: 4. Exact executed: 0. Qualifying: 0. Generic substitutions: 0. Temporary non-agent fallbacks treated as qualifying: 0.

`ES-RA-08` remains `Executable Golden-Path Reproduction Controller`; it was neither renamed nor treated as one of Pilot A's four minimum roles.

## Control results

- Behavioral canary: `NOT_EXECUTED`. Prior failed attempt 01 and corrected packet attempt 02 remain byte-preserved.
- Behavioral prompt injection: `NOT_EXECUTED`. Prior static coverage remains 10/10 but is not behavioral evidence.
- Deterministic defects: prior static oracle retains 14/14 control-signal detections; role-level detection is unavailable.
- Output custody: no role output exists. New preflight evidence is hashed by the runtime-validation checksum register.
- Reconciliation: not executed.
- Replay: not executed.
- Variance: not available.
- Role-output archive parity: not executed.

## Validation and assurance

The authoritative predecessor validator, rerun in a disposable full-history predecessor clone, recorded `31 PASS`, `0 FAIL`, and `1 BLOCKED`; the blocked check remains canonical Pilot A role execution. The new blocked-evidence validation recorded `30 PASS`, `0 FAIL`, `3 BLOCKED`, `5 SKIPPED`, and `8 UNAVAILABLE`.

Assurance remains `AI_ASSISTED_DOCUMENT_PREPARATION`. No evidence supports `SINGLE_EXECUTION_AI_REVIEW` or `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW`.

## Evidence custody and change control

- Fresh clone and remote synchronization were verified.
- The dedicated branch begins at the exact remote predecessor.
- Existing Phase 1 and Pilot A tree identities were recorded before additions.
- Historical files modified: 0.
- Sealed files changed: 0.
- Files deleted: 0.
- Prior failed evidence changed or removed: 0.
- New evidence is additive under `pilot_a/runtime_validation/attempt_01/`.

## Remaining blockers

1. Host runtime does not provide explicit canonical custom-agent selection and authoritative loaded-role identity evidence.
2. Parent sandbox and approval policy violate the mandatory runtime permission control for all four roles.
3. Network, MCP, plugin, connector, credential-capability, and external-service isolation is not enforced.
4. Role-specific frozen-input and output-path isolation is not technically enforced.

## Exact next controlled action

Provision a new host-enforced runtime that implements the minimum environment changes in `PILOT_A_RUNTIME_PREFLIGHT_REPORT.md`, then execute a new preserved Pilot A preflight attempt. Do not reuse or overwrite this attempt. Do not run any role until every permission category is neither `BROADER_THAN_AUTHORIZED` nor `UNVERIFIABLE` and canonical role selection produces authoritative non-null identity evidence.

No Phase 2 work, deployment, production action, merge, or pull request is authorized.
