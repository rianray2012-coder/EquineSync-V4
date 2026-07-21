# Phase 1 Source Inventory

**Inventory date:** 2026-07-21  
**Repository:** `https://github.com/rianray2012-coder/EquineSync-V4.git`  
**Starting commit:** `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`  
**Inventory status:** `SOURCE_INVENTORIED`

This inventory was produced before drafting successor Phase 1 materials. Source artifacts are classified by authority, lifecycle, and permitted treatment. No source listed as sealed, locked, immutable, or historical may be edited by Phase 1 work.

## Current controlling authority

| Source | Identity | Classification | Treatment |
| --- | --- | --- | --- |
| `authority/PHASE_1_FOUNDER_DIRECTIVE_2026-07-21.md` | SHA-256 `da245bd5e051564e62dbc25dfad00f0f546ab4738425f5970369e4e9ab1af328` | `FOUNDER_DECISION`; active Phase 1 authority | Retain byte-identical; no Phase 2, Phase 3, production, external-provider, merge, PR, ratification, or Founder-decision action |
| `PHASE_1_AUTHORITATIVE_BASELINE_DETERMINATION.md` | Selected predecessor `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3` | `VERIFIED_REPOSITORY_EVIDENCE`; active Phase 1 record | Mutable only through a versioned successor if the remote baseline changes |

## Approved framework and canonical roles

| Family | Location | Count / identity | Classification | Treatment |
| --- | --- | --- | --- | --- |
| Framework package | `../../agent_config/V1.0.0/` | 69 files; framework V1.3; package V1.0.0 | `CONTROLLING_CONSTITUTIONAL_AUTHORITY`; Founder approved | `RETAINED_AS_ACTIVE_SOURCE`; no substantive role change |
| Canonical role registry | `../../agent_config/V1.0.0/config/agent_registry.json` | 8 roles, ES-RA-01 through ES-RA-08 | `CONTROLLING_CONSTITUTIONAL_AUTHORITY` | Canonical IDs and names control every Phase 1 profile |
| Shared schemas | `../../agent_config/V1.0.0/schemas/` | 19 JSON Schemas | `ADOPTED_OPERATIONAL_AUTHORITY` | Reuse where applicable; Phase 1 additions must not alter these files |
| Output templates | `../../agent_config/V1.0.0/templates/` | 14 templates | `ADOPTED_OPERATIONAL_AUTHORITY` | Reuse or reference; preserve originals |
| Installed Codex registrations | `../../../../.codex/agents/` | 8 role TOML files plus one runtime canary | `VERIFIED_REPOSITORY_EVIDENCE` only | Static configuration evidence; not proof of loaded runtime role identity |

### Canonical role source checksums

| Role ID | Canonical name | Approved prompt | SHA-256 |
| --- | --- | --- | --- |
| `ES-RA-01` | Drafting Agent | `../../agent_config/V1.0.0/prompts/ES-RA-01_DRAFTING_AGENT.md` | `a314d2348e4a2d2095a0a05dcfdc0b6d4280af6576056581bd473522861d2594` |
| `ES-RA-02` | Segregated Review Agent | `../../agent_config/V1.0.0/prompts/ES-RA-02_SEGREGATED_REVIEW_AGENT.md` | `3dcb1e3403a23a887664a4dbb103ee517fcc319bb3df3e000cdb47196f73e419` |
| `ES-RA-03` | Adversarial Challenge Agent | `../../agent_config/V1.0.0/prompts/ES-RA-03_ADVERSARIAL_CHALLENGE_AGENT.md` | `0b61fa393200e969476ba76ef563471a30f1f9a67035afb9f49b482204b1b52d` |
| `ES-RA-04` | Machine Validation Agent | `../../agent_config/V1.0.0/prompts/ES-RA-04_MACHINE_VALIDATION_AGENT.md` | `25066ab427e953500f9cb4da52b7a31bd9321e9f3a9f059e079f948a59fce438` |
| `ES-RA-05` | Evidence Custodian | `../../agent_config/V1.0.0/prompts/ES-RA-05_EVIDENCE_CUSTODIAN.md` | `1c75da2b648333a0cf05ed2e593d48a2c616bece0cba33c4c3c90587e0fda52a` |
| `ES-RA-06` | Domain Reviewer | `../../agent_config/V1.0.0/prompts/ES-RA-06_DOMAIN_REVIEWER.md` | `ecfdb7eba8e53f657a5122fa6e92d923d4736a157e14579453ef4627087e2a42` |
| `ES-RA-07` | Synthetic Golden-Path Specification Agent | `../../agent_config/V1.0.0/prompts/ES-RA-07_SYNTHETIC_GOLDEN_PATH_SPECIFICATION_AGENT.md` | `62c1021e72810578207cc9e34fb91c25618a9d491dd737bab04a2f39ee1ac319` |
| `ES-RA-08` | Executable Golden-Path Reproduction Controller | `../../agent_config/V1.0.0/prompts/ES-RA-08_EXECUTABLE_GOLDEN_PATH_REPRODUCTION_CONTROLLER.md` | `69e51f4555e0c78329049da6eac34c7895c706a5e6df3a1a835202542884163f` |

## Historical and immutable evidence

| Family | Location | Count | Status and controlling fact | Treatment |
| --- | --- | ---: | --- | --- |
| Calibration evidence | `../../calibration/` | 106 | Historical calibration, including successes, failures, and retries | `RETAINED_AS_HISTORICAL_EVIDENCE`; immutable |
| Installation evidence | `../../FINAL_INSTALLATION_VALIDATION_REPORT.md`, `../../INSTALLATION_RECORD.md`, `../../INSTALLATION_DIFF.md`, `../../PRE_ACTIVATION_HARDENING_REPORT.md`, `../../RUNTIME_CALIBRATION_REPORT.md` | 5 | Installation-level records | `RETAINED_AS_HISTORICAL_EVIDENCE`; immutable |
| Activation evidence | `../../activation/` | 37 | Activation blocked; role attempts passed 0/3; no operational activation | `RETAINED_AS_HISTORICAL_EVIDENCE`; immutable |
| Runtime-remediation evidence | `../../runtime_remediation/` | 620 | Preserves `agent_type=null`, `agent_role=null`, generic fallback, and `REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY` | `RETAINED_AS_HISTORICAL_EVIDENCE`; immutable |
| Runtime-requalification evidence | `../../runtime_requalification/` | 97 | Final disposition `FOUNDER_REVIEW_AGENTS_BLOCKED_BY_CONFIRMED_RUNTIME_PRODUCT_LIMITATION`; 0/8 identity probes and calibrations run | `RETAINED_AS_HISTORICAL_EVIDENCE`; immutable |
| Temporary non-agent fallback | `../../temporary_non_agent_fallback/FORA-NONAGENT-FALLBACK-2026-001/` | 4 | Authorized, available, not started; explicitly not a substitution for ES-RA roles | `RETAINED_AS_ACTIVE_SOURCE` and predecessor control; do not recharacterize |

## Applicable MIAP terminology controls

The current Founder directive controls terminology: MIAP means Master Implementation Atlas Program, and Product Implementation Atlases operate beneath and within MIAP. Existing `docs/implementation/MASTER_EQUINESYNC_IMPLEMENTATION_ATLAS_*` artifacts are background and planning/adoption evidence only for Phase 1 terminology. Phase 1 does not implement MIAP or any PIA.

## Mutable Phase 1 scope

Only `governance/founder_orchestrated_review/phase1/V1.0.0/` is the active mutable Phase 1 artifact root. Synthetic Pilot A fixtures and generated evidence must remain under that root. No reviewed source, prior run, sealed package, `.codex` registration, active PIA, default-branch file, or historical evidence family is mutable under this directive.

## Controlling conflict and disposition

Repository evidence and the current runtime confirm that exact runtime-native role selection is unavailable. A Role Configuration or prompt label cannot establish Reviewer Identity or prove that the runtime loaded the requested role. Phase 1 therefore proceeds as configuration-identified and procedurally segregated internal AI review only when its controls can be proven. Any role execution attempted under unresolved or broader-than-authorized permissions must fail closed and be preserved; it cannot be counted as a successful ES-RA execution.
