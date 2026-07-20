# Installed System Validation Report

**Result:** `PASS`

**Validation ID:** `ES-INSTALLED-SYSTEM-VALIDATION-V1.0.0`

**Repository branch:** `agent/install-founder-review-agents-v1.0.0`

**Repository commit at validation:** `57210494c1e82e60efd4c329ebf34fda236972d8`

**Completed:** `2026-07-20T18:51:07+00:00`

## Validation results

| Check | Status | Detail |
| --- | --- | --- |
| `SRC-001` Source ZIP SHA-256 | `PASS` | 604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3 |
| `SRC-002` Adjacent checksum file content | `PASS` | 604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3  EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip |
| `SRC-003` Adjacent checksum command | `PASS` | EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip: OK |
| `PKG-001` Package-controlled validator | `PASS` | PACKAGE VALIDATION PASSED |
| `PKG-002` ZIP-to-install exact byte identity | `PASS` | {"file_count": 67, "mismatches": 0} |
| `PKG-003` Manifest-listed byte identity | `PASS` | {"manifest_entries": 63, "mismatches": 0} |
| `PKG-004` Package manifest JSON Schema validation | `PASS` | PACKAGE_MANIFEST.json validates against package_manifest.schema.json |
| `AGT-000` Calibration-only runtime canary controls | `PASS` | {"approval_policy": "on-request", "classification": "CALIBRATION_ONLY_NOT_A_REGISTERED_REVIEW_ROLE", "file": ".codex/agents/es_runtime_canary.toml", "name": "es_runtime_canary", "sandbox_mode": "read-only"} |
| `AGT-001` Eight registered custom-agent TOMLs and controls | `PASS` | {"agent_count": 8, "names": ["equinesync_adversarial_challenge_agent", "equinesync_domain_reviewer", "equinesync_drafting_agent", "equinesync_evidence_custodian", "equinesync_executable_golden_path_controller", "equinesync_machine_validation_agent", "equinesync_segregated_review_agent", "equinesync_synthetic_golden_path_agent"], "sandbox_modes": {"equinesync_adversarial_challenge_agent": "read-only", "equinesync_domain_reviewer": "read-only", "equinesync_drafting_agent": "workspace-write", "equinesync_evidence_custodian": "workspace-write", "equinesync_executable_golden_path_controller": "workspace-write", "equinesync_machine_validation_agent": "workspace-write", "equinesync_segregated_review_agent": "read-only", "equinesync_synthetic_golden_path_agent": "workspace-write"}} |
| `AGT-002` Unique custom-agent names | `PASS` | 8 unique names |
| `SCH-001` Draft 2020-12 metaschema and $ref validation | `PASS` | {"draft": "2020-12", "ref_count": 0, "schema_count": 20} |
| `SCH-002` All supplied JSON examples | `PASS` | ["examples/EXAMPLE_REVIEW_AUTHORIZATION.json validates against review_authorization.schema.json"] |
| `SCH-003` Sample Founder Review Authorization | `PASS` | examples/EXAMPLE_REVIEW_AUTHORIZATION.json validates against review_authorization.schema.json |
| `XFL-001` Cross-file registry, policy, gate, version, role, prompt, schema, and template consistency | `PASS` | {"agent_ids": ["ES-RA-01", "ES-RA-02", "ES-RA-03", "ES-RA-04", "ES-RA-05", "ES-RA-06", "ES-RA-07", "ES-RA-08"], "gate_count": 5, "prompt_count": 8, "schema_count": 20, "template_count": 15} |
| `CFG-001` Project agent concurrency configuration | `PASS` | max_threads=6 max_depth=1 |
| `GOV-001` Source package and locked installation commit ancestry | `PASS` | HEAD descends from a1caf346fe7b07b1be7dde12f1b805a62b2e5f9b |

## Summary

- Checks: 16
- Passed: 16
- Failed: 0
- Draft 2020-12 metaschema validation is distinct from JSON parsing and was run with the Python `jsonschema` implementation.
- Package-manifest validation and exact ZIP-to-install byte comparison are distinct checks.

## Dependency and command evidence

- `governance/founder_orchestrated_review/validation/INSTALLED_SYSTEM_VALIDATION_DEPENDENCIES.json`
- `governance/founder_orchestrated_review/validation/INSTALLED_SYSTEM_VALIDATION_COMMAND_LOG.txt`

## Limitations

- Static validation does not prove runtime custom-agent registration or role compliance.
- TOML sandbox defaults can be superseded by the parent session's live permission overrides.
- Codex workspace-write is a workspace boundary, not path-level enforcement for role-specific output directories.
- Cross-file consistency checks cover the installation's declared invariants; they are not a proof of every semantic relationship in the framework.

## Scope statement

This report validates installation structure, sealed-package integrity, JSON Schema validity, supplied examples, and declared cross-file invariants. It does not start or simulate a substantive Founder-Orchestrated Review Cycle and does not issue a Founder disposition.
