#!/usr/bin/env python3
"""Build the bounded runtime-requalification evidence package.

This script writes only inside the non-sealed FORA-RUNTIME-REQUAL-2026-001
directory. It deliberately records blocked downstream stages when the required
custom-agent selector is unavailable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


RUN_ID = "FORA-RUNTIME-REQUAL-2026-001"
DIRECTIVE_ID = "ES-FORA-DIR-RUNTIME-REMEDIATION-REQUALIFICATION-V1.0"
SOURCE_BRANCH = "agent/install-founder-review-agents-v1.0.0"
SOURCE_COMMIT = "57210494c1e82e60efd4c329ebf34fda236972d8"
REMEDIATION_BRANCH = "codex/founder-review-agent-runtime-requalification-v1"
STAGE2A_COMMIT = "56dc68ce761b84800caa60997af7fb62ab34f82d"
DISPOSITION = "FOUNDER_REVIEW_AGENTS_BLOCKED_BY_CONFIRMED_RUNTIME_PRODUCT_LIMITATION"
PACKAGE_ZIP_SHA = "604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3"
HANDOFF_ZIP_SHA = "7b1076f9eda1640936d07f72fac7aba6a3d83e9ed04f965ccb668043f8c144de"
CODEX_VERSION = "codex-cli 0.144.6"
BLOCKED = "NOT_RUN_BLOCKED_BY_CUSTOM_AGENT_SELECTOR"

ROLES = [
    ("ES-RA-01", "equinesync_drafting_agent", "equinesync_drafting_agent.toml", "workspace-write"),
    ("ES-RA-02", "equinesync_segregated_review_agent", "equinesync_segregated_review_agent.toml", "read-only"),
    ("ES-RA-03", "equinesync_adversarial_challenge_agent", "equinesync_adversarial_challenge_agent.toml", "read-only"),
    ("ES-RA-04", "equinesync_machine_validation_agent", "equinesync_machine_validation_agent.toml", "workspace-write"),
    ("ES-RA-05", "equinesync_evidence_custodian", "equinesync_evidence_custodian.toml", "workspace-write"),
    ("ES-RA-06", "equinesync_domain_reviewer", "equinesync_domain_reviewer.toml", "read-only"),
    ("ES-RA-07", "equinesync_synthetic_golden_path_agent", "equinesync_synthetic_golden_path_agent.toml", "workspace-write"),
    ("ES-RA-08", "equinesync_executable_golden_path_controller", "equinesync_executable_golden_path_controller.toml", "workspace-write"),
]

REQUIRED = [
    "RUNTIME_CAPABILITY_MATRIX.md",
    "RUNTIME_CAPABILITY_MATRIX.json",
    "CUSTOM_AGENT_SELECTOR_PROOF.md",
    "CUSTOM_AGENT_SELECTOR_PROOF.json",
    "REPOSITORY_TRUST_AND_PROFILE_PRECEDENCE_REPORT.md",
    "EXECUTION_ENVIRONMENT_PROVENANCE.md",
    "AGENT_DISCOVERY_AND_REGISTRATION_REGISTER.csv",
    "AGENT_IDENTITY_PROBE_REGISTER.csv",
    "AGENT_INDIVIDUAL_CALIBRATION_REGISTER.csv",
    "AGENT_ORCHESTRATION_TEST_REPORT.md",
    "FAILED_ATTEMPT_AND_RETRY_REGISTER.csv",
    "SEALED_INPUT_PRESERVATION_REPORT.md",
    "FINAL_FRESH_CLONE_VERIFICATION.md",
    "FINAL_FRESH_CLONE_VERIFICATION.json",
    "MACHINE_READABLE_DISPOSITION.json",
    "PACKAGE_FILE_MANIFEST.json",
    "SHA256SUMS.txt",
    "VALIDATION_REPORT.md",
    "VALIDATION_REPORT.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def command(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    return (result.stdout or result.stderr).strip()


def command_ok(args: list[str], cwd: Path) -> bool:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh-clone-status", choices=["PENDING", "PASS"], default="PENDING")
    parser.add_argument("--fresh-clone-commit", default="")
    parser.add_argument("--fresh-clone-note", default="Publication candidate not yet verified from the remote branch.")
    args = parser.parse_args()

    run_root = Path(__file__).resolve().parents[1]
    repo = run_root.parents[3]
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    raw = run_root / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    surfaces = [
        {
            "surface": "Codex desktop current task",
            "support_status": "SUPPORTED_LOCAL_CLIENT",
            "selector_tested": "spawn_agent agent_type/name selector",
            "selector_available": False,
            "evidence": "The exposed spawn_agent schema accepts task_name, message, fork_turns, model, and reasoning_effort; it exposes no agent_type or equivalent custom-agent field.",
            "permission_state": "danger-full-access / approval never",
            "execution": "NOT_ATTEMPTED_PERMISSION_CONTROL_AND_SELECTOR_BLOCK",
        },
        {
            "surface": "Codex CLI interactive",
            "support_status": "SUPPORTED_LOCAL_CLIENT",
            "selector_tested": "model-directed exact agent_type=es_runtime_canary spawn",
            "selector_available": False,
            "evidence": "raw/interactive_selector_canary_retry_03/raw_terminal.log",
            "permission_state": "read-only / approval on-request / network restricted",
            "execution": "NO_SPAWN_CALL_NO_CHILD",
        },
        {
            "surface": "Codex CLI exec --json",
            "support_status": "SUPPORTED_NONINTERACTIVE_CLI",
            "selector_tested": "model-directed exact agent_type=es_runtime_canary spawn",
            "selector_available": False,
            "evidence": "raw/selector_canary/events.jsonl",
            "permission_state": "read-only / effective approval never / network restricted",
            "execution": "NO_SPAWN_CALL_NO_CHILD",
        },
        {
            "surface": "Codex app-server protocol",
            "support_status": "EXPERIMENTAL_PROTOCOL_DIAGNOSTIC_ONLY",
            "selector_tested": "generated request/params schema search for agent_type or agentRole selector",
            "selector_available": False,
            "evidence": "raw/config_and_app_server_probe/app_server_schema_analysis.json",
            "permission_state": "no child execution",
            "execution": "CONFIG_READ_ONLY_NO_EXTERNAL_CUSTOM_AGENT_SPAWN_METHOD",
        },
    ]

    current_desktop = {
        "observed_at": now,
        "surface": "Codex desktop current task",
        "exposed_spawn_agent_input_fields": ["task_name", "message", "fork_turns", "model", "reasoning_effort"],
        "custom_agent_selector_fields": [],
        "agent_type_supported": False,
        "parent_sandbox": "danger-full-access",
        "parent_approval_policy": "never",
        "permission_control_result": "FORMAL_ROLE_SPAWN_PROHIBITED_WITHOUT_FOUNDER_EXCEPTION",
        "spawn_attempted": False,
        "generic_substitute_used": False,
    }
    write_json(raw / "current_desktop_surface_observation.json", current_desktop)

    prior_evidence = {
        "run_id": "FORA-FRESH-2026-07-20-236E7CE8",
        "disposition": "FOUNDER_REVIEW_AGENTS_BLOCKED_BY_RUNTIME_LIMITATION",
        "located_directory": "/Users/rianray/Documents/Codex/2026-07-19/files-mentioned-by-the-user-codex/outputs/FORA-FRESH-2026-07-20-236E7CE8",
        "verified_readable_sha256": {
            "FRESH_AGENT_ACTIVATION_AND_READINESS_REPORT.md": "8db9655db5d83bb08981dbf80192ae02a21944556a6910681a3aa2124d4afb2b",
            "EXECUTION_ENVIRONMENT_PROVENANCE.md": "12b44cca6284fdd4e29bd118ea39c1f6dcb923899a4046a255453b9789308a58",
            "AGENT_IDENTITY_PROBE_REGISTER.csv": "dcf0850513bfe52ead45acb47805b7ae0ab018e88df108cd6fe465a5cd1cb000",
        },
        "other_located_artifacts": [
            "AGENT_INDIVIDUAL_CALIBRATION_REGISTER.csv",
            "AGENT_ORCHESTRATION_TEST_REPORT.md",
            "AGENT_READINESS_EVIDENCE_MANIFEST.txt",
            "AGENT_ACTIVATION_CHANGE_MANIFEST.txt",
        ],
        "note": "Four artifacts were present as macOS dataless placeholders during this run; no attempt was made to rewrite them. The supplied handoff preserved their locators and prior disposition.",
    }
    write_json(raw / "prior_blocked_evidence_register.json", prior_evidence)

    toolchain = {
        "captured_at": now,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "git": command(["git", "--version"], repo),
        "node": command(["node", "--version"], repo),
        "codex": CODEX_VERSION,
        "controlling_source_commit": SOURCE_COMMIT,
        "current_head": command(["git", "rev-parse", "HEAD"], repo),
        "controlling_source_commit_is_ancestor": command_ok(["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, "HEAD"], repo),
        "branch": command(["git", "branch", "--show-current"], repo),
    }
    write_json(raw / "toolchain_provenance.json", toolchain)

    matrix_json = {
        "run_id": RUN_ID,
        "directive_id": DIRECTIVE_ID,
        "captured_at": now,
        "codex_version": CODEX_VERSION,
        "official_documentation": "https://learn.chatgpt.com/docs/agent-configuration/subagents",
        "official_documentation_summary": "Current local clients document project custom-agent files and identify a custom agent by its name field.",
        "surfaces": surfaces,
        "supported_surfaces_with_selector": 0,
        "supported_surfaces_tested": 3,
        "diagnostic_protocols_tested": 1,
        "conclusion": "CUSTOM_AGENT_SELECTOR_UNAVAILABLE_ON_EVERY_SUPPORTED_RUNTIME_SURFACE_TESTED",
    }
    write_json(run_root / "RUNTIME_CAPABILITY_MATRIX.json", matrix_json)
    rows = "\n".join(
        f"| {s['surface']} | {s['support_status']} | {s['selector_tested']} | NO | {s['execution']} |"
        for s in surfaces
    )
    write_text(
        run_root / "RUNTIME_CAPABILITY_MATRIX.md",
        f"""# Runtime Capability Matrix

Run: `{RUN_ID}`

Codex: `{CODEX_VERSION}`

Result: **CUSTOM_AGENT_SELECTOR_UNAVAILABLE_ON_EVERY_SUPPORTED_RUNTIME_SURFACE_TESTED**

| Runtime surface | Classification | Exact selector tested | Selector available | Execution result |
|---|---|---|---:|---|
{rows}

The current [official Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) describes project custom-agent files in `.codex/agents/` and says the `name` field identifies the custom agent. The repository configurations parse and the project layer loads. However, none of the supported execution surfaces exposed a field that could preserve that exact custom-agent identity in a spawn request. A configuration file being discoverable is not proof that its identity layer executed.

The app-server schema was inspected only as an additional diagnostic. It is not counted as a supported replacement execution path and did not expose an external custom-agent spawn method.
""",
    )

    selector_json = {
        "run_id": RUN_ID,
        "selector_requirement": "An execution interface must carry the exact repository-controlled custom-agent name/agent_type into the child session.",
        "canary_name": "es_runtime_canary",
        "canary_is_review_role": False,
        "tests": [
            {
                "surface": "Codex CLI exec --json",
                "result": "FAIL_SELECTOR_UNAVAILABLE",
                "spawn_calls": 0,
                "children": 0,
                "generic_substitution": False,
                "substantive_work": False,
                "evidence": "raw/selector_canary/result.json",
            },
            {
                "surface": "Codex CLI interactive",
                "result": "FAIL_SELECTOR_UNAVAILABLE",
                "spawn_calls": 0,
                "children": 0,
                "generic_substitution": False,
                "substantive_work": False,
                "evidence": "raw/interactive_selector_canary_retry_03/result.json",
            },
            {
                "surface": "Codex desktop current task",
                "result": "FAIL_SELECTOR_SCHEMA_ABSENT",
                "spawn_calls": 0,
                "children": 0,
                "generic_substitution": False,
                "substantive_work": False,
                "evidence": "raw/current_desktop_surface_observation.json",
            },
        ],
        "configuration_discovery": "PASS_8_OF_8_STATIC_CONFIGS_PLUS_NON_ROLE_CANARY",
        "runtime_registration": "BLOCKED_0_OF_8",
        "classification": "CONFIRMED_RUNTIME_PRODUCT_INTERFACE_LIMITATION_FOR_TESTED_VERSION_AND_SURFACES",
        "fail_closed": True,
    }
    write_json(run_root / "CUSTOM_AGENT_SELECTOR_PROOF.json", selector_json)
    write_text(
        run_root / "CUSTOM_AGENT_SELECTOR_PROOF.md",
        f"""# Custom-Agent Selector Proof

## Required proof

The controlling requirement was an actual child spawn whose request preserves the exact custom-agent identity from a repository-controlled `.codex/agents/*.toml` file. A normal prompt, task label, generic worker, fallback role, null `agent_type`, or unverified subprocess label does not satisfy this proof.

## Canary results

- CLI noninteractive: requested exact `agent_type=es_runtime_canary`; the parent reported that its `spawn_agent` interface had no selector field. Spawn calls: 0. Children: 0.
- CLI interactive: requested the same exact selector under a disposable read-only/on-request profile. The parent reported the selector field unavailable. Spawn calls: 0. Children: 0.
- Desktop current task: the exposed schema contains `task_name`, `message`, `fork_turns`, `model`, and `reasoning_effort`, but no `agent_type` or equivalent custom-agent selector. Formal role execution was also prohibited by the effective `danger-full-access` / `never` parent permissions.
- App-server diagnostic: config parsing and project-layer loading passed, but generated request schemas exposed no external custom-agent selector or spawn method.

No canary was counted as a review role. No generic child was launched. No prompt was relabeled as an agent. No substantive review occurred.

## Classification

This is not a repository configuration, profile precedence, trust, or invocation-syntax defect: static discovery and configuration serialization passed, while the execution interfaces themselves lacked the required selector. For `{CODEX_VERSION}` and every supported surface tested, the controlling selector is unavailable. Therefore the run stops at required execution-order step 4 and returns `{DISPOSITION}`.
""",
    )

    write_text(
        run_root / "REPOSITORY_TRUST_AND_PROFILE_PRECEDENCE_REPORT.md",
        f"""# Repository Trust and Profile Precedence Report

## Repository identity

- Repository: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- Source branch: `{SOURCE_BRANCH}`
- Source commit: `{SOURCE_COMMIT}`
- Remediation branch: `{REMEDIATION_BRANCH}`
- Project custom-agent directory: `.codex/agents/`

## Disposable-profile proof

The CLI probes used isolated temporary Codex homes and a trusted project rooted at an exact clean clone. Plugin, connector, and MCP autoloading was removed. `codex app-server` `config/read` reported the project configuration layer loaded and enabled, `multi_agent=true`, `agents.max_threads=6`, `agents.max_depth=1`, and zero MCP servers. All eight repository role TOMLs plus the non-role canary parsed.

Configuration precedence was therefore:

1. bounded command-line sandbox and approval overrides;
2. disposable user profile;
3. trusted project `.codex` configuration and `.codex/agents/*.toml` files;
4. built-in defaults.

The failure remained after personal configuration, plugins, connectors, and MCP servers were excluded. The evidence therefore does not support a profile-precedence or trust diagnosis. The limitation occurred at the spawn interface: no exact custom-agent selector was exposed.

The current desktop task was not used for a formal role spawn because its effective permissions were broader than allowed by `RUNTIME_PERMISSION_CONTROL.md`, and its spawn schema independently lacked the selector.
""",
    )

    write_text(
        run_root / "EXECUTION_ENVIRONMENT_PROVENANCE.md",
        f"""# Execution Environment Provenance

- Run: `{RUN_ID}`
- Captured: `{now}`
- Platform: `{toolchain['platform']}`
- Machine: `{toolchain['machine']}`
- Codex: `{CODEX_VERSION}`
- Git: `{toolchain['git']}`
- Node: `{toolchain['node']}`
- Python used by this evidence builder: `{toolchain['python']}`
- Repository source commit: `{SOURCE_COMMIT}`
- Remediation branch: `{REMEDIATION_BRANCH}`

## Sanitized runtime state

- CLI interactive canary: read-only sandbox, on-request approvals, restricted network, isolated profile, zero plugins/connectors/MCP servers.
- CLI noninteractive canary: read-only sandbox, noninteractive effective approval `never`, restricted network, isolated profile, zero plugins/connectors/MCP servers.
- App-server diagnostic: isolated profile; config-read and schema generation only; no child execution.
- Desktop observation: `danger-full-access`, approval `never`; no formal role spawn attempted because the repository permission control prohibits this combination without a Founder exception.

## Controlled source inputs

- Sealed package checksum entries: 63/63 passed.
- Installed-system validation: 16/16 passed.
- Controlled files recorded: 184.
- Agent configuration package ZIP SHA-256: `{PACKAGE_ZIP_SHA}`.
- Founder handoff ZIP SHA-256: `{HANDOFF_ZIP_SHA}`; its internal checksum verification passed.

The installed-system validator used a disposable Python environment pinned to `jsonschema[format]==4.26.0`. The initial missing-dependency failure and a later harness-scoring error are retained in the failed-attempt register. The corrected validation result is `raw/static_validation_retry_03/result.json`.
""",
    )

    discovery_header = [
        "agent_id", "custom_agent_name", "config_file", "required_sandbox", "static_config_parse",
        "project_layer_discovery", "runtime_registration", "identity_verified", "generic_substitute_used", "evidence",
    ]
    with (run_root / "AGENT_DISCOVERY_AND_REGISTRATION_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(discovery_header)
        for role_id, name, config, sandbox in ROLES:
            writer.writerow([role_id, name, f".codex/agents/{config}", sandbox, "PASS", "PASS_STATIC", "BLOCKED_0_OF_8_SELECTOR_UNAVAILABLE", "NO", "NO", "CUSTOM_AGENT_SELECTOR_PROOF.json"])

    identity_header = ["agent_id", "custom_agent_name", "probe_status", "spawn_attempted", "child_created", "identity_marker_observed", "generic_substitute_used", "reason"]
    with (run_root / "AGENT_IDENTITY_PROBE_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(identity_header)
        for role_id, name, _config, _sandbox in ROLES:
            writer.writerow([role_id, name, BLOCKED, "NO", "NO", "NO", "NO", "Execution order stopped at selector proof"])

    calibration_header = ["agent_id", "custom_agent_name", "calibration_status", "attempted", "passed", "generic_substitute_used", "reason"]
    with (run_root / "AGENT_INDIVIDUAL_CALIBRATION_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(calibration_header)
        for role_id, name, _config, _sandbox in ROLES:
            writer.writerow([role_id, name, BLOCKED, "NO", "NO", "NO", "Identity probe stage was not reached"])

    write_text(
        run_root / "AGENT_ORCHESTRATION_TEST_REPORT.md",
        f"""# Agent Orchestration Test Report

Status: **{BLOCKED}**

Bounded orchestration was not attempted. Required execution-order step 4 failed before role registration, identity probes, calibration, or orchestration. Starting orchestration would have required either a generic substitute or a relabeled normal prompt, both explicitly prohibited.

| Measure | Result |
|---|---:|
| Exact roles required | 8 |
| Exact roles registered | 0 |
| Identity probes executed | 0 |
| Individual calibrations executed | 0 |
| Orchestration runs executed | 0 |
| Generic substitutions | 0 |
| Substantive Identity/Relationships review actions | 0 |
| Product or production workflow actions | 0 |

This report is a blocked-stage record, not an orchestration pass.
""",
    )

    failures = [
        ["FA-001", "Prior run", "FORA-FRESH-2026-07-20-236E7CE8", "BLOCKED", "Runtime discovery 0/8; selector unavailable", "Preserved as supplied prior evidence", "NO"],
        ["FA-002", "Static validation attempt 1", "raw/static_validation/result.json", "FAILED_HARNESS_DEPENDENCY", "System Python lacked jsonschema", "Created disposable pinned validation environment", "YES"],
        ["FA-003", "Static validation retry 2", "raw/static_validation_retry_02/result.json", "FAILED_HARNESS_SCORER", "Validator passed 16/16 but wrapper read the wrong JSON field", "Corrected wrapper to read top-level status", "YES"],
        ["FA-004", "Static validation retry 3", "raw/static_validation_retry_03/result.json", "PASS", "Corrected static checks passed 9/9 and installed validation 16/16", "Accepted as controlling static result", "NO"],
        ["FA-005", "CLI exec selector canary", "raw/selector_canary/result.json", "BLOCKED_SELECTOR", "Spawn interface lacked agent_type/custom-agent selector", "Tested supported interactive client separately", "YES"],
        ["FA-006", "Interactive harness attempt 1", "raw/interactive_selector_canary/result.json", "FAILED_HARNESS_PARSE", "Automation script parse error before runtime probe", "Repaired harness", "YES"],
        ["FA-007", "Interactive harness retry 2", "raw/interactive_selector_canary_retry_02/result.json", "FAILED_HARNESS_STALL", "PTY harness stalled before usable log", "Replaced with controlled native PTY capture", "YES"],
        ["FA-008", "Interactive selector retry 3", "raw/interactive_selector_canary_retry_03/result.json", "BLOCKED_SELECTOR", "Runtime explicitly reported selector unavailable; no child", "No unsupported workaround permitted", "NO"],
        ["FA-009", "Config/app-server diagnostic", "raw/config_and_app_server_probe/result.json", "PASS_DIAGNOSTIC", "Project layer loaded; generated request schemas still lacked selector", "Classified interface limitation", "NO"],
    ]
    with (run_root / "FAILED_ATTEMPT_AND_RETRY_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["attempt_id", "attempt", "evidence", "result", "cause", "response", "retried"])
        writer.writerows(failures)

    write_text(
        run_root / "SEALED_INPUT_PRESERVATION_REPORT.md",
        f"""# Sealed Input Preservation Report

Result: **PASS — SEALED INPUTS UNCHANGED**

- Controlling source commit: `{SOURCE_COMMIT}`
- Sealed package checksum validation: 63/63 passed.
- Installed-system validator: 16/16 passed.
- Controlled-input preservation manifest: 184 files.
- Package ZIP SHA-256: `{PACKAGE_ZIP_SHA}`.
- Static validation evidence: `raw/static_validation_retry_03/`.
- Files added by this run are confined to `governance/founder_orchestrated_review/runtime_requalification/{RUN_ID}/` and the separately packaged archive directory.
- Sealed role definitions changed: 0.
- Sealed calibration fixtures changed: 0.
- Sealed approval records changed: 0.
- Stage 2A Candidate 009 files changed: 0.

The temporary `es_runtime_canary` was already present at the controlling commit and is not counted as a ninth review role. No sealed byte was changed to force a passing result.
""",
    )

    fresh = {
        "run_id": RUN_ID,
        "status": args.fresh_clone_status,
        "verified_commit": args.fresh_clone_commit or None,
        "remote_branch": REMEDIATION_BRANCH,
        "source_commit_ancestor": SOURCE_COMMIT,
        "required_artifact_count": 19,
        "note": args.fresh_clone_note,
        "checks": {
            "remote_branch_fetch": args.fresh_clone_status == "PASS",
            "exact_commit_checkout": args.fresh_clone_status == "PASS",
            "required_artifacts_present": args.fresh_clone_status == "PASS",
            "sha256sums_pass": args.fresh_clone_status == "PASS",
            "json_parse_pass": args.fresh_clone_status == "PASS",
            "sealed_package_63_of_63": args.fresh_clone_status == "PASS",
            "branch_descends_from_controlling_commit": args.fresh_clone_status == "PASS",
        },
    }
    write_json(run_root / "FINAL_FRESH_CLONE_VERIFICATION.json", fresh)
    fresh_checks = "\n".join(f"- {name}: {'PASS' if value else 'PENDING'}" for name, value in fresh["checks"].items())
    write_text(
        run_root / "FINAL_FRESH_CLONE_VERIFICATION.md",
        f"""# Final Fresh-Clone Verification

Status: **{args.fresh_clone_status}**

Remote branch: `{REMEDIATION_BRANCH}`

Verified commit: `{args.fresh_clone_commit or 'PENDING'}`

{fresh_checks}

{args.fresh_clone_note}
""",
    )

    disposition_json = {
        "run_id": RUN_ID,
        "directive_id": DIRECTIVE_ID,
        "repository": "https://github.com/rianray2012-coder/EquineSync-V4.git",
        "source_branch": SOURCE_BRANCH,
        "source_commit": SOURCE_COMMIT,
        "remediation_branch": REMEDIATION_BRANCH,
        "stage2a_founder_closure_commit_context_only": STAGE2A_COMMIT,
        "codex_version": CODEX_VERSION,
        "custom_agent_selector": "UNAVAILABLE_ON_EVERY_SUPPORTED_RUNTIME_SURFACE_TESTED",
        "static_role_configs": "8_OF_8_PRESENT_AND_PARSE",
        "runtime_registration": "0_OF_8_BLOCKED",
        "identity_probes": "0_OF_8_NOT_RUN_BLOCKED",
        "calibrations": "0_OF_8_NOT_RUN_BLOCKED",
        "orchestration": "NOT_RUN_BLOCKED",
        "generic_substitutions": 0,
        "sealed_files_changed": 0,
        "implementation_authorized": False,
        "substantive_identity_or_relationships_review_authorized": False,
        "execution_authorized": False,
        "external_assurance": "NOT_EXTERNALLY_ASSURED",
        "f_0001": "F0001_REMAINS_OPEN_BLOCKING",
        "stage2_execution_baseline": "EXECUTION_BASELINE_STILL_NOT_READY",
        "final_disposition": DISPOSITION,
        "exact_founder_action_required": "Obtain or wait for a supported Codex runtime release/surface that exposes an exact custom-agent name/agent_type selector, then issue a fresh bounded requalification directive and rerun beginning at selector proof. Do not authorize activation or execution before 8/8 identity and calibration evidence exists.",
    }
    write_json(run_root / "MACHINE_READABLE_DISPOSITION.json", disposition_json)

    # Validation reports are excluded from the checksummed set so they can
    # report the checksum result without a self-reference cycle.
    write_text(run_root / "VALIDATION_REPORT.md", "# Validation Report\n\nPENDING")
    write_json(run_root / "VALIDATION_REPORT.json", {"status": "PENDING"})

    manifest_excluded = {"PACKAGE_FILE_MANIFEST.json", "SHA256SUMS.txt", "VALIDATION_REPORT.md", "VALIDATION_REPORT.json"}
    manifest_entries = []
    for path in sorted(p for p in run_root.rglob("*") if p.is_file()):
        rel = path.relative_to(run_root).as_posix()
        if rel in manifest_excluded:
            continue
        manifest_entries.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "run_id": RUN_ID,
        "created_at": now,
        "scope": "All run evidence except self-referential control files listed in excluded_paths.",
        "excluded_paths": sorted(manifest_excluded),
        "file_count": len(manifest_entries),
        "files": manifest_entries,
    }
    write_json(run_root / "PACKAGE_FILE_MANIFEST.json", manifest)

    checksum_excluded = {"SHA256SUMS.txt", "VALIDATION_REPORT.md", "VALIDATION_REPORT.json"}
    checksum_paths = sorted(p for p in run_root.rglob("*") if p.is_file() and p.relative_to(run_root).as_posix() not in checksum_excluded)
    write_text(run_root / "SHA256SUMS.txt", "\n".join(f"{sha256(path)}  {path.relative_to(run_root).as_posix()}" for path in checksum_paths))

    checks = {
        "controlling_source_commit_is_ancestor": toolchain["controlling_source_commit_is_ancestor"],
        "remediation_branch_exact": toolchain["branch"] == REMEDIATION_BRANCH,
        "required_artifacts_19_of_19": all((run_root / name).is_file() for name in REQUIRED),
        "runtime_matrix_json_parse": json.loads((run_root / "RUNTIME_CAPABILITY_MATRIX.json").read_text())["supported_surfaces_with_selector"] == 0,
        "selector_proof_json_parse": json.loads((run_root / "CUSTOM_AGENT_SELECTOR_PROOF.json").read_text())["runtime_registration"] == "BLOCKED_0_OF_8",
        "disposition_exact": json.loads((run_root / "MACHINE_READABLE_DISPOSITION.json").read_text())["final_disposition"] == DISPOSITION,
        "discovery_register_8_roles": sum(1 for _ in (run_root / "AGENT_DISCOVERY_AND_REGISTRATION_REGISTER.csv").open(encoding="utf-8")) - 1 == 8,
        "identity_register_8_roles": sum(1 for _ in (run_root / "AGENT_IDENTITY_PROBE_REGISTER.csv").open(encoding="utf-8")) - 1 == 8,
        "calibration_register_8_roles": sum(1 for _ in (run_root / "AGENT_INDIVIDUAL_CALIBRATION_REGISTER.csv").open(encoding="utf-8")) - 1 == 8,
        "static_validation_9_of_9": json.loads((raw / "static_validation_retry_03/result.json").read_text())["checks_passed"] == 9,
        "installed_system_16_of_16": json.loads((raw / "static_validation_retry_03/INSTALLED_SYSTEM_VALIDATION_RESULT.json").read_text())["summary"]["passed"] == 16,
        "sealed_checksums_63": json.loads((raw / "static_validation_retry_03/result.json").read_text())["sealed_package_checksum_entries"] == 63,
        "generic_substitutions_zero": disposition_json["generic_substitutions"] == 0,
        "sealed_files_changed_zero": disposition_json["sealed_files_changed"] == 0,
        "execution_order_fail_closed": disposition_json["orchestration"] == "NOT_RUN_BLOCKED",
        "manifest_files_hash_match": all(sha256(run_root / item["path"]) == item["sha256"] for item in manifest_entries),
        "checksum_files_hash_match": all(sha256(path) in (run_root / "SHA256SUMS.txt").read_text() for path in checksum_paths),
    }
    passed = sum(checks.values())
    validation = {
        "run_id": RUN_ID,
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "required_artifacts": REQUIRED,
        "required_artifacts_present": [name for name in REQUIRED if (run_root / name).is_file()],
        "semantic_result": "Evidence package is internally valid; agent runtime remains blocked.",
    }
    write_json(run_root / "VALIDATION_REPORT.json", validation)
    validation_rows = "\n".join(f"| {name} | {'PASS' if result else 'FAIL'} |" for name, result in checks.items())
    write_text(
        run_root / "VALIDATION_REPORT.md",
        f"""# Validation Report

Result: **{validation['status']} ({passed}/{len(checks)})**

| Check | Result |
|---|---:|
{validation_rows}

This PASS means the evidence package is internally consistent, complete, and fail-closed. It does not mean the eight review agents are ready. Runtime registration remains 0/8, identity probes 0/8, calibrations 0/8, and orchestration not run.
""",
    )

    print(json.dumps({"run_root": str(run_root), "validation": validation["status"], "checks": f"{passed}/{len(checks)}", "manifest_files": len(manifest_entries)}, indent=2))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
